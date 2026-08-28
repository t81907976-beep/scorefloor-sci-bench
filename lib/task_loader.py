"""
ScoreFloor-Sci-Bench — 题目解析 (Task Loader)

把 tasks/<学科>/test-*.md 解析成可执行的 Task：
  - query        : `# 构造高质量-query` 段落，作为发给被测模型的题面
  - reference     : `# SFT标准-response` 段落，作为裁判参考的标准答案
  - steps         : `# 步骤列表-reference` 里的 [n] 步骤，条数即基准步骤数 N0
  - grade_fn      : `## Automated Checks` 代码块里的 grade()，动态编译
  - rubric        : `## LLM Judge Rubric` 段落原文，交给裁判模型
不改题面、不改 grade 逻辑，只做抽取与编译。
"""

from __future__ import annotations

import inspect
import os
import re
from dataclasses import dataclass
from typing import Callable, List, Optional

from . import grading_utils

# 注入进每道题 grade() 命名空间的共享容错工具。题内不写 import 也能直接用，
# 从而不必每题内联一份 LaTeX 归一拷贝（0804 的 8 题假阴性正是内联版各自缺料）。
_GRADING_BUILTINS = {
    name: getattr(grading_utils, name)
    for name in ("flatten_text", "has_any", "normalize", "drop_subscript",
                 "miller_indices_present", "compact", "extract_number",
                 "within_tol", "is_refusal")
}


@dataclass
class Task:
    task_id: str          # 文件名去扩展名，如 test-化学05
    subject: str          # 学科，取自所在子目录，如 chemistry
    path: str
    query: str
    reference: str
    steps: List[str]
    rubric: str
    grade_fn: Optional[Callable]
    checks_src: str = ""  # Automated Checks 的 python 源码原文，只用于缓存指纹（不参与判分）

    @property
    def baseline_steps(self) -> int:
        """基准步骤数 N0 = 步骤列表条数（至少 1，避免除零）。"""
        return max(len(self.steps), 1)


# 少数题目用「裸标签行」而非 markdown 标题（如 test-化学02 的 "构造高质量-query"）。
# 解析前把这些已知裸标签行提升为一级标题，统一走标题切段逻辑。
_BARE_LABELS = ("构造高质量-query", "SFT标准-response", "步骤列表-reference")


def _promote_bare_labels(text: str) -> str:
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped in _BARE_LABELS:
            out.append(f"# {stripped}")
        else:
            out.append(line)
    return "\n".join(out)


# 段落标题正则：匹配 `# xxx` 或 `## xxx`
def _split_sections(text: str) -> dict:
    """
    按 markdown 标题切段，返回 {标题: 正文}。
    正文包含该标题下所有更深层级的子标题内容（例如 `## LLM Judge Rubric`
    的正文会包含其下所有 `### Criterion`），直到遇到同级或更高级标题为止。
    """
    # 先收集所有标题的位置与层级
    lines = text.splitlines()
    heads = []  # (行号, 层级, 标题)
    for idx, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if m:
            heads.append((idx, len(m.group(1)), m.group(2).strip()))

    sections = {}
    for i, (start, level, title) in enumerate(heads):
        # 找下一个同级或更高级（层级数 <=）的标题作为本段结束
        end = len(lines)
        for j in range(i + 1, len(heads)):
            if heads[j][1] <= level:
                end = heads[j][0]
                break
        body = "\n".join(lines[start + 1:end]).strip()
        sections.setdefault(title, body)
    return sections


# 评分块标题：这些段落属于「怎么判分」，不属于题面/标准答案/步骤，
# 抽 query/reference/steps 时必须在此截断。
_GRADING_HEADS = ("Grading Criteria", "Automated Checks", "LLM Judge Rubric",
                  "Judge Rubric")


def _cut_at_grading(body: str) -> str:
    """把正文截断到第一个评分块标题之前。

    题库里标题层级不统一：化学01 用 `# 答案`（一级）而评分块用 `## Grading
    Criteria`（二级），按层级切段时评分块会被当作「答案」的子内容一起吞进
    reference——裁判于是连 rubric 和 grade() 源码一起看到，既污染判分基准，
    也让 grade() 自检时把代码里的 `无法回答` 字面误判成拒答。
    """
    lines = body.splitlines()
    for idx, line in enumerate(lines):
        m = re.match(r"^#{1,6}\s+(.*?)\s*$", line)
        if m and any(h.lower() in m.group(1).lower() for h in _GRADING_HEADS):
            return "\n".join(lines[:idx]).strip()
    return body


def _find_section(sections: dict, *keywords: str) -> str:
    """标题包含任一关键词就返回该段正文（大小写不敏感）。"""
    for title, body in sections.items():
        low = title.lower()
        if any(k.lower() in low for k in keywords):
            return body
    return ""


def _extract_python_block(body: str) -> str:
    """从 Automated Checks 段落里抽取 ```python ...``` 代码块。"""
    m = re.search(r"```python\s*(.*?)```", body, flags=re.DOTALL)
    return m.group(1) if m else ""


def _answer_from_transcript(transcript) -> str:
    """把 transcript 拼成纯答复文本，供单参数 grade(answer) 使用。

    ⚠️ 只收 assistant 消息。早先版本无条件拼接全部消息，会把 user 侧的**题面原文**
    一起喂给 grade()——而多道题的 `has_*` 关键词判据判的词（化学04 的「标准加入」、
    化学03 的「积累」）恰好就在题面里，于是模型什么都不写也能命中，凭空造出白拿项。
    这是判分调用层能造出假阳性的一条隐蔽路径，必须在拼接处就掐掉。
    """
    if isinstance(transcript, str):
        return transcript
    parts = []
    for msg in transcript or []:
        if isinstance(msg, dict):
            if msg.get("role") in (None, "assistant"):
                parts.append(str(msg.get("content") or ""))
        else:
            parts.append(str(msg))
    return "\n".join(p for p in parts if p)


def _adapt_grade(fn: Callable) -> Callable:
    """
    统一 grade() 调用口径为 grade(transcript, workspace_path, meta)。

    题目里存在两种历史写法：多数题是三参数版，少数题（化学03/04）写成
    `grade(answer: str)`。后者被三参数调用会抛
    「takes 1 positional argument but 3 were given」，
    整题 5 次全部记 0 分——即「整齐并列」型集体假阴性。
    这里按形参个数适配，单参数版自动喂扁平化后的答复文本。
    """
    try:
        params = inspect.signature(fn).parameters
        n_pos = sum(1 for p in params.values()
                    if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD))
        # *args 版按三参数调用即可，不必适配
        has_varargs = any(p.kind is p.VAR_POSITIONAL for p in params.values())
    except (TypeError, ValueError):
        return fn
    if n_pos >= 3 or has_varargs:
        return fn

    def _adapted(transcript, workspace_path=None, meta=None):
        answer = _answer_from_transcript(transcript)
        if n_pos <= 1:
            return fn(answer)
        return fn(answer, workspace_path)

    _adapted.__name__ = f"grade_{n_pos}arg_adapted"
    return _adapted


def _variants(transcript) -> List[tuple]:
    """生成答复文本的多档写法变体：(档位名, 变体 transcript)。

    第 0 档必须是原文：题库里存在把 LaTeX 命令本身当标签词用的正则
    （物理02 的 `(?:p_?z|pz|...|boxed)` 拿 `boxed` 当「最终答案」的标志词），
    壳一拆这个词就没了。保留原文档位，多档取最优才能保证单调不减。
    """
    norm = grading_utils.normalize
    both = lambda s: grading_utils.drop_subscript(norm(s))  # noqa: E731

    if isinstance(transcript, str):
        return [("raw", transcript), ("normalized", norm(transcript)),
                ("no_subscript", both(transcript))]

    def remap(fn):
        out = []
        for item in (transcript or []):
            if isinstance(item, dict):
                new = dict(item)
                for key in ("content", "text", "message", "output"):
                    if isinstance(new.get(key), str):
                        new[key] = fn(new[key])
                out.append(new)
            elif isinstance(item, str):
                out.append(fn(item))
            else:
                out.append(item)
        return out

    return [("raw", transcript), ("normalized", remap(norm)),
            ("no_subscript", remap(both))]


def _score_of(detail) -> float:
    if not isinstance(detail, dict):
        return 0.0
    try:
        return float(detail.get("auto_final_answer_score", 0.0) or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _robust_grade(fn: Callable) -> Callable:
    """把题目 grade() 包成「多档写法重判、取最高分」的判分器。

    动机（0804 全量榜的头号系统性偏差）：题库 grade() 的正则普遍按裸算式写
    （`j = -1.25 A m^-2`），模型答案却是 `\\[\\boxed{j\\approx -1.25\\ \\mathrm{A\\,m^{-2}}}\\]`。
    20 题里 8 题因此假阴性，只能靠 scripts/recheck_scores.py 事后人工校正。
    把「多档写法」这一层放到判分调用处，题库文件无需逐题内联归一拷贝，
    人工校正随之从必走工序降格为回归测试。

    三档：原文 / normalize() 归一 / 再 drop_subscript()。取 auto_final_answer_score
    最高的那一档整份返回（不逐 check 挑最优，避免拼出题目从未产生过的组合）。
    单调不减：原文档位始终参评，任何现存题目的分数只会涨不会跌。
    额外写入 `_grade_variant` 标注命中档位，便于回归断言与假阳性审计。

    ⚠️ 只放宽「表现形式」，不放宽判分标准：容差、陷阱项、单位项的逻辑全在题内，
    这一层不碰。它救的是「答对但没认出来」，救不了也不该救「答错」——
    假阳性须靠收紧抽取口径解决，不在本层。

    入口另做一件事：**把 str 形态的 transcript 归一成 list**（见 _graded 内注释）。
    """
    def _graded(transcript, workspace_path, meta):
        # str transcript 归一（2026-08-11 修）。
        #
        # 隔离验证时直接 `grade_fn("答复全文", ...)` 是最自然的调法，但题内取文本的
        # 辅助函数一律按 list 写，收到 str 会静默产出语义完全错误的结果——不是报错：
        #
        #     for item in items:          # items 是 str 时逐字符迭代
        #         elif isinstance(item, str): parts.append(item)
        #     "\n".join(parts)            # 'qt≈0.259' → 'q\nt\n≈\n0\n.\n2\n5\n9'
        #
        # 碎成单字后任何多字符正则都失配。实测 20 题里 18 题受影响，三种形态：
        #   · 抛异常（物理01/02/04~07：'str' has no attribute 'get'）——可见，最轻
        #   · 静默归零（物理08/09：自带 isinstance(items, list) 守卫直接 return ""）
        #   · 静默降分（物理03 1.000→0.150、物理10 1.000→0.030、化学01/02/05~10）
        # 后两种最危险：看到低分只会以为「判据没命中」，不会怀疑调法。化学题 0806
        # 报的「化学01 has_rate_unit 五连 0.0」就是这么来的，白跑一轮往来。
        #
        # 修在这里而不是逐题加护栏，与 0805 定的原则一致（判分调用口径的缺陷修在
        # 调用层，不逐题内联）：逐题改只能覆盖含 flatten_text() 的 9 题，物理01/02/
        # 04~07 里根本没有那个函数，物理08/09 无处可加。一处改则 20 题全覆盖，
        # 且新题自动免疫。tasks/ 一个字不动，榜单口径零风险（runner 本来就传 list）。
        if isinstance(transcript, str):
            transcript = [{"role": "assistant", "content": transcript}]
        best_detail, best_score, best_tag = None, -1.0, "raw"
        for tag, variant in _variants(transcript):
            try:
                detail = fn(variant, workspace_path, meta)
            except Exception as exc:  # noqa: BLE001 某一档炸掉不连坐其他档
                if best_detail is None:
                    best_detail = {"grade_error": str(exc)}
                continue
            score = _score_of(detail)
            if score > best_score:
                best_detail, best_score, best_tag = detail, score, tag
        if isinstance(best_detail, dict):
            best_detail = dict(best_detail)
            best_detail["_grade_variant"] = best_tag
        return best_detail if best_detail is not None else {}

    return _graded


def _compile_grade(code: str, task_id: str) -> Optional[Callable]:
    """
    编译 grade() 代码块，统一返回 grade(transcript, workspace_path, meta) 形态。

    题库里存在两种签名：三参数 `grade(transcript, workspace_path, meta)`（多数），
    与单参数 `grade(answer: str)`（化学03/04）。runner 一律按三参数调用，单参数题
    过去会抛 TypeError 被 run_once 吞掉、final 分静默记 0。这里按实际参数个数适配，
    单参数的自动喂拼好的答复文本。
    """
    if not code.strip():
        return None
    # 共享容错工具预置进 exec 命名空间：grade() 必须自包含（题目 md 里不能依赖
    # import 路径），但把 lib/grading_utils 的函数当内建注入后，题内可直接调用
    # normalize()/flatten_text()，无需每题内联一份拷贝——写法容错只在共享层维护一处。
    # 题内若自己 def 了同名函数，局部定义照旧覆盖注入版，不破坏既有题目。
    ns: dict = dict(_GRADING_BUILTINS)
    try:
        exec(compile(code, f"<grade:{task_id}>", "exec"), ns)  # noqa: S102 题目内置评分逻辑
    except SyntaxError as exc:
        raise ValueError(f"{task_id} 的 Automated Checks 代码块编译失败: {exc}") from exc
    fn = ns.get("grade")
    if not callable(fn):
        raise ValueError(f"{task_id} 的 Automated Checks 代码块未定义 grade()")
    # 两层包装的顺序是有意的：先 _adapt_grade 统一签名，再 _robust_grade 套多档重判。
    # 反过来会让 _robust_grade 直接以三参数调用单参数题，每一档都抛 TypeError。
    return _robust_grade(_adapt_grade(fn))


# 步骤行两种写法：`[1] ...`（多数题）与 `1. ...` / `1、...` / `1：...`（物理 06-10）。
# 前者优先，只有一条都没匹配到时才回退到后者，避免正文里的普通编号列表被误当成步骤。
_STEP_BRACKET = re.compile(r"^\s*\[\d+\]")
# `[.](?!\d)` 排除小数点：grade() 源码里的 `0.10 * scores[...]` 不该被当成步骤行。
_STEP_NUMBERED = re.compile(r"^\s*(\d+)\s*(?:[.](?!\d)|[、：:])\s*\S")


def _extract_steps(body: str) -> List[str]:
    """
    从步骤列表段落抽取步骤，支持两种写法：
      1. `[1] ...`（化学全部 + 物理01~05）——优先
      2. `1. ...` / `1：...` / `1、...`（物理06~10）——仅当没有 `[n]` 行时启用

    步骤可跨多行（含 LaTeX 公式块），续行归并到当前步骤，直到下一个步骤起始行。

    第 2 种写法容易误命中正文里的编号（`grade()` 源码里的 `0.10 * scores[...]`、
    注释里以「47.0、」开头的行），因此要求**编号从 1 开始严格递增**，只保留接得上
    序号的行。物理07 曾因此把 grade() 注释里两行算成步骤，N0 由 6 虚报成 8、
    S_eff 被静默压低——序号递增与 `_cut_at_grading()` 是这个 bug 的两道独立防线。
    """
    lines = body.splitlines()

    steps: List[str] = []
    for line in lines:
        if _STEP_BRACKET.match(line):
            steps.append(line.strip())
        elif steps and line.strip():
            steps[-1] += "\n" + line.rstrip()
    if steps:
        return steps

    expected = 1
    for line in lines:
        m = _STEP_NUMBERED.match(line)
        if m and int(m.group(1)) == expected:
            steps.append(line.strip())
            expected += 1
        elif steps and line.strip():
            steps[-1] += "\n" + line.rstrip()
    return steps


def load_task(path: str) -> Task:
    with open(path, encoding="utf-8") as f:
        text = f.read()

    text = _promote_bare_labels(text)
    sections = _split_sections(text)
    task_id = os.path.splitext(os.path.basename(path))[0]
    subject = os.path.basename(os.path.dirname(path))

    query = _cut_at_grading(_find_section(sections, "query", "构造高质量", "题目"))
    reference = _cut_at_grading(
        _find_section(sections, "SFT", "标准-response", "标准答案", "答案"))
    steps_body = _cut_at_grading(
        _find_section(sections, "步骤列表", "步骤列表-reference", "解题思路"))
    rubric = _find_section(sections, "LLM Judge Rubric", "Judge Rubric")
    checks_body = _find_section(sections, "Automated Checks")

    checks_src = _extract_python_block(checks_body)
    grade_fn = _compile_grade(checks_src, task_id)

    return Task(
        task_id=task_id,
        subject=subject,
        path=path,
        query=query,
        reference=reference,
        steps=_extract_steps(steps_body),
        rubric=rubric,
        grade_fn=grade_fn,
        checks_src=checks_src,
    )


def discover_tasks(tasks_dir: str, subjects: Optional[List[str]] = None,
                   task_ids: Optional[List[str]] = None) -> List[Task]:
    """
    遍历 tasks_dir 下各学科子目录里的 test-*.md。
      subjects  只加载这些学科（None=全部）
      task_ids  只加载这些题（按 task_id 或文件名匹配，None=全部）
    模板文件（TASK_TEMPLATE.md）自动跳过。
    """
    found: List[Task] = []
    for root, _dirs, files in os.walk(tasks_dir):
        for fn in sorted(files):
            if not fn.endswith(".md") or fn.upper().startswith("TASK_TEMPLATE"):
                continue
            subject = os.path.basename(root)
            if subjects and subject not in subjects:
                continue
            tid = os.path.splitext(fn)[0]
            if task_ids and tid not in task_ids and fn not in task_ids:
                continue
            found.append(load_task(os.path.join(root, fn)))
    return found
