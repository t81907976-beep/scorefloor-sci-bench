"""
ScoreFloor-Sci-Bench — 模型客户端抽象 (Model Providers)

被测模型 / 裁判模型统一走这里。当前实现两种接口：
  - OpenAICompatProvider  OpenAI 兼容 /chat/completions，文心 / 豆包 / deepseek / gpt / GLM 等
  - AnthropicProvider     Anthropic 原生 /messages，Claude 系列（Opus / Sonnet / Haiku / Fable）

两者都只需填 base_url + api_key + model。网关对 Claude 同时提供两种格式，
走原生 /messages 可用上 Anthropic 独有参数（system 顶层字段、thinking 等）。

预留扩展：新增一个 provider 只需继承 BaseProvider 并在 PROVIDERS 里注册。
runner 只依赖 BaseProvider.chat()，不关心底层是哪家。
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Type


@dataclass
class ChatResult:
    """一次模型调用的结果。text 为纯文本答复，raw 保留原始响应便于排查。"""

    text: str
    raw: dict = field(default_factory=dict)


class BaseProvider:
    """模型客户端基类。子类只需实现 chat()。"""

    name = "base"

    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        timeout: int = 120,
        extra: Optional[dict] = None,
        stream: bool = False,
    ):
        self.model = model
        self.api_key = api_key
        self.base_url = (base_url or "").rstrip("/")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.extra = extra or {}
        # 流式：长思考答复走 SSE，避免中间网关按空闲超时切断（表现为 HTTP 504）
        self.stream = stream

    def chat(self, prompt: str, system: Optional[str] = None) -> ChatResult:
        raise NotImplementedError


# 这些状态码重试无意义：多半是 Token / 模型名 / 参数写错，直接报出来让用户改配置。
_FATAL_HTTP_CODES = {400, 401, 403, 404, 422}

_HTTP_HINTS = {
    400: "（请求参数或模型名不被接受，检查 config.json 的 model 是否在网关模型列表里）",
    401: "（鉴权失败，检查 .env 里的 MODEL_API_KEY / JUDGE_API_KEY 是否为有效的网关 Token）",
    403: "（无权限，检查该 Token 是否被授权使用这个模型）",
    404: "（端点或模型不存在，检查 base_url 是否以 /v1 结尾、model 名是否拼写正确）",
    422: "（参数校验失败，检查 temperature / max_tokens 等取值）",
}


def _read_error_body(exc: urllib.error.HTTPError, limit: int = 500) -> str:
    """读出 HTTPError 的响应体，网关的错误原因都在这里。"""
    try:
        body = exc.read().decode("utf-8", errors="replace").strip()
    except Exception:
        return "(无响应体)"
    return body[:limit] or "(空响应体)"


def _hint_for(code: int) -> str:
    return _HTTP_HINTS.get(code, "")


class _SamplingWasted(RuntimeError):
    """
    本次抽样作废：网关 502/503/504 判定生成太久，或思考段吃光 max_tokens 致正文为空。

    这两种都不是能力问题、也不是稳定的网络故障，而是「这一抽样运气不好」。
    正确做法是保持同一 max_tokens 直接重新抽样，见 _with_resample()。
    """


# 网关侧超时/过载：重试同一请求没意义，直接作废本次抽样去重抽。
_GATEWAY_CODES = (502, 503, 504)


def _with_resample(send: Callable[[], ChatResult], max_resamples: int,
                   model: str, url: str) -> ChatResult:
    """
    把「一次抽样」包成「最多 max_resamples 次重抽」。

    作废条件两种：send() 抛 _SamplingWasted（网关 5xx），或返回空正文
    （多为思考吃光 max_tokens）。期间的空答复/网关错误都不当作有效结果。

    max_resamples=0 时行为与不带重抽的主线一致：只做单次抽样内的网络短重试，
    空正文照旧返回、交由上层（runner 心跳/统计）处理，不抛异常。
    """
    def _finish_of(res: ChatResult):
        raw = res.raw or {}
        if raw.get("finish_reason") is not None:
            return raw["finish_reason"]
        return ((raw.get("choices") or [{}])[0]).get("finish_reason")

    last_err: Optional[Exception] = None
    for _ in range(max_resamples + 1):
        try:
            res = send()
        except _SamplingWasted as exc:
            last_err = exc
            continue
        if res.text.strip() or max_resamples == 0:
            return res
        last_err = RuntimeError(f"空答复 finish_reason={_finish_of(res)}")
    # 重抽耗尽仍为空：返回空结果交上层记录，不中断整轮。
    return ChatResult(text="", raw={"resample_exhausted": True,
                                    "last_error": str(last_err),
                                    "model": model, "url": url})


def _post_json(url: str, payload: dict, headers: dict, timeout: int,
               model: str, parse: Callable[[dict], str],
               waste_on_gateway_error: bool = False) -> ChatResult:
    """
    POST JSON 并用 parse() 从响应体里取出答复文本。

    重试策略与错误呈现对所有 provider 一致：4xx 配置类错误直接带响应体抛出，
    5xx / 网络抖动退避重试 3 次。parse 由各 provider 提供（响应结构不同）。
    waste_on_gateway_error=True 时网关 5xx 不再退避重试，直接抛 _SamplingWasted
    交给 _with_resample 重抽。
    """
    data = json.dumps(payload).encode("utf-8")
    last_err: Optional[Exception] = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            return ChatResult(text=parse(body), raw=body)
        except urllib.error.HTTPError as exc:
            detail = _read_error_body(exc)
            if exc.code in _FATAL_HTTP_CODES:
                # 鉴权/模型名/参数错误重试也不会好，直接带响应体报出来
                raise RuntimeError(
                    f"模型调用失败（{model} @ {url}）：HTTP {exc.code} {exc.reason}"
                    f"{_hint_for(exc.code)}\n响应：{detail}"
                ) from exc
            if waste_on_gateway_error and exc.code in _GATEWAY_CODES:
                raise _SamplingWasted(
                    f"网关 HTTP {exc.code} {exc.reason}：{detail}") from exc
            last_err = RuntimeError(f"HTTP {exc.code} {exc.reason}：{detail}")
            time.sleep(2 * (attempt + 1))
        except (urllib.error.URLError, KeyError, IndexError, TypeError, TimeoutError) as exc:
            last_err = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"模型调用失败（{model} @ {url}，已重试 3 次）：{last_err}")


def _post_sse(url: str, payload: dict, headers: dict, timeout: int, model: str,
              on_event: Callable[[dict, dict], None],
              waste_on_gateway_error: bool = False) -> ChatResult:
    """
    POST 流式请求并逐条消费 SSE。

    存在的原因：推理模型在难题上单次可跑十几分钟，非流式请求会被中间网关按
    空闲超时切断（网关侧表现为 HTTP 504 Gateway Time-out，且不可靠重试）。
    流式下 token 持续到达，网关不会判定空闲，长答复才能完整拿回来。

    on_event(事件 dict, 累积器 dict) 由各 provider 提供，负责把增量塞进累积器。
    累积器约定字段：text（正文）、reasoning（思维链，仅记录不计入 text）、
    finish_reason、usage。

    waste_on_gateway_error=True 时，网关 5xx 与「一个字正文都没收到就断流」
    都算本次抽样作废（抛 _SamplingWasted），交给 _with_resample 重抽。
    """
    data = json.dumps(dict(payload, stream=True)).encode("utf-8")
    acc: dict = {"text": "", "reasoning": "", "finish_reason": None, "usage": None}
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line or not line.startswith("data:"):
                    continue
                chunk = line[5:].strip()
                if chunk == "[DONE]":
                    break
                try:
                    event = json.loads(chunk)
                except json.JSONDecodeError:
                    continue
                on_event(event, acc)
    except urllib.error.HTTPError as exc:
        detail = _read_error_body(exc)
        if waste_on_gateway_error and exc.code in _GATEWAY_CODES:
            raise _SamplingWasted(
                f"网关 HTTP {exc.code} {exc.reason}：{detail}") from exc
        raise RuntimeError(
            f"模型流式调用失败（{model} @ {url}）：HTTP {exc.code} {exc.reason}"
            f"{_hint_for(exc.code)}\n响应：{detail}"
        ) from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        # 已经收到部分正文时不算彻底失败，返回已收到的内容并标记截断
        if acc["text"].strip():
            acc["finish_reason"] = f"stream_interrupted: {exc}"
            return ChatResult(text=acc["text"], raw=acc)
        if waste_on_gateway_error:
            # 只有思维链、正文一个字都没出就断了 → 本次抽样作废
            raise _SamplingWasted(
                f"断流且无正文（reasoning {len(acc['reasoning'])} 字）：{exc}") from exc
        raise RuntimeError(f"模型流式调用失败（{model} @ {url}）：{exc}") from exc

    return ChatResult(text=acc["text"], raw=acc)



class OpenAICompatProvider(BaseProvider):
    """OpenAI 兼容的 /chat/completions 接口。无第三方依赖，仅用标准库。"""

    name = "openai"

    @staticmethod
    def _on_event(event: dict, acc: dict) -> None:
        for choice in event.get("choices") or []:
            delta = choice.get("delta") or {}
            piece = delta.get("content")
            if isinstance(piece, str):
                acc["text"] += piece
            # DeepSeek / GLM 等把思维链放在 reasoning_content，只记录不计入正文
            think = delta.get("reasoning_content") or delta.get("reasoning")
            if isinstance(think, str):
                acc["reasoning"] += think
            if choice.get("finish_reason"):
                acc["finish_reason"] = choice["finish_reason"]
        if event.get("usage"):
            acc["usage"] = event["usage"]

    def chat(self, prompt: str, system: Optional[str] = None) -> ChatResult:
        if not self.base_url:
            raise ValueError("OpenAICompatProvider 需要 base_url，例如 https://api.openai.com/v1")

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        # max_resamples 是本类的控制字段，不能混进发给网关的 payload。
        max_resamples = int(self.extra.get("max_resamples", 0))
        gateway_extra = {k: v for k, v in self.extra.items() if k != "max_resamples"}

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        payload.update(gateway_extra)

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # 思考型模型（DeepSeek-V4-Pro / Kimi 等）经网关有两种「本次抽样作废」的
        # 失败：① 思考段吃光 max_tokens → finish_reason=="length" 且正文空；
        # ② 生成太久触发网关 502/503/504。两者都不是能力问题、也非稳定网络故障，
        # 而是「这一抽样运气不好」，正确做法是保持同一 max_tokens 重新抽样。
        # 非思考型模型无需重抽；给思考型模型在 config 的 extra 里配 max_resamples 即可。
        url = f"{self.base_url}/chat/completions"

        def send() -> ChatResult:
            if self.stream:
                return _post_sse(
                    url=url, payload=payload, headers=headers, timeout=self.timeout,
                    model=self.model, on_event=self._on_event,
                    waste_on_gateway_error=max_resamples > 0,
                )
            return _post_json(
                url=url, payload=payload, headers=headers, timeout=self.timeout,
                model=self.model,
                parse=lambda body: body["choices"][0]["message"]["content"] or "",
                waste_on_gateway_error=max_resamples > 0,
            )

        return _with_resample(send, max_resamples, self.model, url)


class AnthropicProvider(BaseProvider):
    """
    Anthropic 原生 Messages 接口（POST {base_url}/messages）。用于 Claude 系列。

    与 OpenAI 兼容格式的差异：
      · system 是顶层字段，不是 messages 里的一条
      · max_tokens 必填
      · 答复在 content 数组里，取 type == "text" 的块拼接（thinking 块被跳过）
    无第三方依赖，仅用标准库。
    """

    name = "anthropic"

    @staticmethod
    def _extract_text(body: dict) -> str:
        blocks = body.get("content") or []
        texts = [b.get("text", "") for b in blocks
                 if isinstance(b, dict) and b.get("type") == "text"]
        if not texts:
            raise KeyError(f"响应 content 里没有 text 块：{json.dumps(body, ensure_ascii=False)[:300]}")
        return "\n".join(t for t in texts if t)

    @staticmethod
    def _on_event(event: dict, acc: dict) -> None:
        """消费 Anthropic SSE：只累计 text_delta，thinking_delta 单独记录。"""
        etype = event.get("type")
        if etype == "content_block_delta":
            delta = event.get("delta") or {}
            if delta.get("type") == "text_delta":
                acc["text"] += delta.get("text", "")
            elif delta.get("type") == "thinking_delta":
                acc["reasoning"] += delta.get("thinking", "")
        elif etype == "message_delta":
            stop = (event.get("delta") or {}).get("stop_reason")
            if stop:
                acc["finish_reason"] = stop
            if event.get("usage"):
                acc["usage"] = event["usage"]

    def chat(self, prompt: str, system: Optional[str] = None) -> ChatResult:
        if not self.base_url:
            raise ValueError("AnthropicProvider 需要 base_url，例如 https://api.anthropic.com/v1")

        # max_resamples 是本类的控制字段，不能混进发给网关的 payload。
        max_resamples = int(self.extra.get("max_resamples", 0))
        gateway_extra = {k: v for k, v in self.extra.items() if k != "max_resamples"}

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system
        payload.update(gateway_extra)

        headers = {
            "Content-Type": "application/json",
            # 网关认 Authorization，原生 Anthropic 认 x-api-key + anthropic-version，都带上
            "anthropic-version": "2023-06-01",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            headers["x-api-key"] = self.api_key

        url = f"{self.base_url}/messages"

        def send() -> ChatResult:
            if self.stream:
                return _post_sse(
                    url=url, payload=payload, headers=headers, timeout=self.timeout,
                    model=self.model, on_event=self._on_event,
                    waste_on_gateway_error=max_resamples > 0,
                )
            return _post_json(
                url=url, payload=payload, headers=headers, timeout=self.timeout,
                model=self.model, parse=self._extract_text,
                waste_on_gateway_error=max_resamples > 0,
            )

        return _with_resample(send, max_resamples, self.model, url)


# provider 注册表：扩展新接口时在这里加一行。
PROVIDERS: Dict[str, Type[BaseProvider]] = {
    "openai": OpenAICompatProvider,
    "openai-compat": OpenAICompatProvider,
    "anthropic": AnthropicProvider,
    "claude": AnthropicProvider,
}


# --------------------------------------------------------------------------
# 可选的模型白名单：只用于配置预检时给出可读的报错，不做硬校验。
# 默认为空 —— 端点与可用模型由用户自己的 config.json 决定。
# 想启用预检提示：把你端点上的模型 id 填进 KNOWN_MODELS，
# 实时清单可用 ./scripts/run.sh --list-models 拉取（GET {base_url}/models）。
# --------------------------------------------------------------------------
KNOWN_MODELS: tuple = ()


def has_model_allowlist(base_url: Optional[str]) -> bool:
    """是否配置了模型白名单。空白名单表示不做任何名称预检。"""
    return bool(KNOWN_MODELS)


# Claude 模型名不统一：有的带 Claude 前缀，有的只有厂商代号。
# 按代号识别，覆盖两种写法。
_CLAUDE_NAME_RE = re.compile(r"claude|\b(fable|opus|sonnet|haiku)\b", re.IGNORECASE)


def is_claude_model(model: Optional[str]) -> bool:
    return bool(_CLAUDE_NAME_RE.search(model or ""))


def list_models(base_url: str, api_key: Optional[str], timeout: int = 30) -> List[str]:
    """拉取端点实际可用的模型 id 列表（GET /models）。"""
    url = f"{base_url.rstrip('/')}/models"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"拉取模型列表失败（{url}）：HTTP {exc.code} {exc.reason}"
            f"{_hint_for(exc.code)}\n响应：{_read_error_body(exc)}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"拉取模型列表失败（{url}）：{exc}") from exc
    return [m.get("id", "") for m in body.get("data", []) if m.get("id")]


_DOTENV_LOADED = False


def load_dotenv_if_present() -> None:
    """
    可选：从项目根的 .env 读取 KEY=VALUE 到环境变量，方便持久化网关 Token，
    免去每次开新终端重复 export。仅补齐尚未设置的变量，不覆盖已有环境变量；
    零第三方依赖。.env 已加入 .gitignore，不会被提交。
    """
    global _DOTENV_LOADED
    if _DOTENV_LOADED:
        return
    _DOTENV_LOADED = True

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, ".env")
    if not os.path.isfile(path):
        return

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def build_provider(cfg: dict) -> BaseProvider:
    """
    从配置字典构造 provider。字段：
      provider   provider 名，见 PROVIDERS；填 "auto"（默认）则按模型名自动选：
                 Claude 系列 → anthropic（/messages），其余 → openai（/chat/completions）
      model      模型名（必填）
      api_key    或用 api_key_env 指定环境变量名
      base_url   接口根地址，例如 https://api.example.com/v1
      temperature / max_tokens / timeout / extra
      stream     走 SSE 流式（长思考答复必需，否则中间网关空闲超时切断，报 HTTP 504）
    """
    model = cfg["model"]
    kind = cfg.get("provider", "auto")
    if kind == "auto":
        kind = "anthropic" if is_claude_model(model) else "openai"
    if kind not in PROVIDERS:
        raise ValueError(f"未知 provider: {kind}，可用: {sorted(PROVIDERS)} 或 auto")

    api_key = cfg.get("api_key")
    if not api_key and cfg.get("api_key_env"):
        load_dotenv_if_present()
        api_key = os.environ.get(cfg["api_key_env"])

    base_url = cfg.get("base_url")

    if not api_key:
        env_name = cfg.get("api_key_env") or "MODEL_API_KEY"
        raise ValueError(
            f"缺少 API Token：环境变量 {env_name} 未设置。\n"
            f"请任选其一：\n"
            f"  · 在项目根新建 .env，写入一行 {env_name}=你的-Token\n"
            f"  · export {env_name}=你的-Token\n"
            f"（只想自检链路可加 --dry-run，不需要 Token）"
        )

    if has_model_allowlist(base_url) and model not in KNOWN_MODELS:
        print(
            f"  ⚠ 模型名 “{model}” 不在已知模型清单里，调用可能返回 400/404。\n"
            f"    可运行 ./scripts/run.sh --list-models 拉取端点实时清单。"
        )

    return PROVIDERS[kind](
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=cfg.get("temperature", 0.7),
        max_tokens=cfg.get("max_tokens", 4096),
        timeout=cfg.get("timeout", 120),
        extra=cfg.get("extra"),
        stream=bool(cfg.get("stream", False)),
    )
