#!/usr/bin/env python3
"""单题多模型单次抓取：对一道题各模型跑 1 次，失败重试 1-2 次后放弃（记 pass）。

默认走 SSE 流式。原因：本类难题的推理模型单次要跑十几分钟，非流式请求会被
中间网关按空闲超时切断（网关侧表现为 HTTP 504），流式下 token 持续到达
才能把长答复完整拿回来。

用法：
    python3 scripts/fetch_single.py test-化学09 --models "model-a,model-b" \
            --tag 化学09 --timeout 3600 --attempts 3

token 预算按模型查 MODEL_MAX_TOKENS 表（部分长思考模型要开到百万量级），
`--max-tokens` 显式给值时统一覆盖。
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import sys
import time

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from lib.providers import build_provider, load_dotenv_if_present  # noqa: E402
from lib.task_loader import discover_tasks                         # noqa: E402


# 按模型的 token 预算。max_tokens 对推理模型是「思维链 + 正文」的总额度，
# 给小了会在思考里烧光、返回空正文 + finish_reason=length（不是模型不会做）。
# 实测部分长思考模型在本题库的难题上思维链能到 5 万字，32k 预算下必然截断，
# 遇到这类模型把它的名字填进下表、开到百万量级。
MODEL_MAX_TOKENS: dict = {
    # "your-long-thinking-model": 1000000,
}
DEFAULT_MAX_TOKENS = 32000

# 部分模型只接受固定采样温度，传别的值会被端点按参数校验拒掉
# （HTTP 400 invalid temperature: only 1 is allowed for this model），
# 那不是模型不会做，也不该记 pass —— 把它的名字填进下表即可。
MODEL_TEMPERATURE: dict = {
    # "your-fixed-temperature-model": 1.0,
}


def max_tokens_for(model: str, override: int = 0) -> int:
    """--max-tokens 显式给了就用它；否则按模型查表，查不到用默认值。"""
    return override or MODEL_MAX_TOKENS.get(model, DEFAULT_MAX_TOKENS)


def temperature_for(model: str, default: float) -> float:
    """只接受固定温度的模型按表覆盖，其余沿用 config.json 的取值。"""
    return MODEL_TEMPERATURE.get(model, default)


def fetch(cfg: dict, model: str, query: str, attempts: int) -> dict:
    last = ""
    budget = max_tokens_for(model, cfg.get("_max_tokens_override", 0))
    temp = temperature_for(model, cfg.get("temperature", 0.7))
    for i in range(1, attempts + 1):
        t0 = time.time()
        try:
            provider = build_provider(dict(cfg, model=model, max_tokens=budget,
                                           temperature=temp))
            res = provider.chat(query)
            text, raw = res.text, res.raw or {}
            el = round(time.time() - t0, 1)
            if not text.strip():
                # 只有思维链、没有正文：模型在思考中被 max_tokens 截断
                last = (f"空正文（reasoning {len(raw.get('reasoning') or '')} 字，"
                        f"finish_reason={raw.get('finish_reason')}，"
                        f"max_tokens={budget}）")
                print(f"  ✗ {model} 第 {i} 次：{last}（{el}s）", flush=True)
                continue
            print(f"  ✓ {model} 第 {i} 次成功（{el}s，正文 {len(text)} 字，"
                  f"思维链 {len(raw.get('reasoning') or '')} 字，"
                  f"finish={raw.get('finish_reason')}）", flush=True)
            return {"model": model, "ok": True, "text": text, "elapsed_s": el,
                    "attempt": i, "finish_reason": raw.get("finish_reason"),
                    "reasoning_chars": len(raw.get("reasoning") or ""),
                    "chars": len(text), "max_tokens": budget,
                    "temperature": temp,
                    "usage": raw.get("usage")}
        except Exception as exc:
            el = round(time.time() - t0, 1)
            last = str(exc)
            print(f"  ✗ {model} 第 {i} 次失败（{el}s）：{last.splitlines()[0][:110]}",
                  flush=True)
    return {"model": model, "ok": False, "error": last[:800],
            "attempt": attempts, "max_tokens": budget,
            "temperature": temp}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("task")
    ap.add_argument("--models", required=True)
    ap.add_argument("--tag", default="")
    ap.add_argument("--config", default=os.path.join(_ROOT, "config.json"))
    ap.add_argument("--max-tokens", type=int, default=0,
                    help="覆盖所有模型的 token 预算；不给则按 MODEL_MAX_TOKENS 查表")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--attempts", type=int, default=3)
    ap.add_argument("--concurrency", type=int, default=5)
    ap.add_argument("--no-stream", action="store_true",
                    help="关掉流式（默认流式，长思考答复不要关）")
    args = ap.parse_args()

    load_dotenv_if_present()
    with open(args.config, encoding="utf-8") as f:
        config = json.load(f)
    cfg = dict(config["model_under_test"], timeout=args.timeout,
               stream=not args.no_stream)
    cfg["_max_tokens_override"] = args.max_tokens

    task = discover_tasks(os.path.join(_ROOT, "tasks"), task_ids=[args.task])[0]
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    budgets = ", ".join(f"{m}={max_tokens_for(m, args.max_tokens)}" for m in models)
    print(f"题目 {task.task_id}（N0={task.baseline_steps}）；模型 {len(models)} 个；"
          f"每模型 1 次答复，最多 {args.attempts} 次尝试；"
          f"{'流式' if cfg['stream'] else '非流式'}\n"
          f"token 预算：{budgets}\n",
          flush=True)

    with cf.ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        runs = list(ex.map(lambda m: fetch(cfg, m, task.query, args.attempts), models))

    stamp = time.strftime("%Y%m%d-%H%M%S")
    tag = args.tag or task.task_id
    out = os.path.join(_ROOT, "results", f"single-{tag}-{stamp}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"task": task.task_id, "N0": task.baseline_steps,
                   "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "max_tokens_override": args.max_tokens or None,
                   "stream": cfg["stream"],
                   "runs": runs},
                  f, ensure_ascii=False, indent=2)

    ok = [r["model"] for r in runs if r["ok"]]
    bad = [r["model"] for r in runs if not r["ok"]]
    print(f"\n成功 {len(ok)}/{len(runs)}：{', '.join(ok) or '无'}")
    if bad:
        print(f"放弃（pass）：{', '.join(bad)}")
    print(f"落盘：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
