"""
ScoreFloor-Sci-Bench — LLM 裁判 (Judge)

裁判模型负责**过程、概念、逻辑**，对应单次成功率里的 步骤分 与 逻辑分：
  - logic_score  : 按题目 `## LLM Judge Rubric` 的各带权 Criterion 打分后加权得到（0~1）
  - step_score   : 关键步骤完成度（0~1）
  - actual_steps : 该次答复的有效步骤数 N_i（排除错误/冗余/无关），供效率项使用

裁判不重复判定代码侧已覆盖的最终数值命中（那部分在 Automated Checks 里）。
裁判被要求只输出严格 JSON，本模块负责稳健解析。
"""

from __future__ import annotations

import json
import re
from typing import List, Optional

from .providers import BaseProvider

JUDGE_SYSTEM = (
    "你是严格、客观的解题过程评审。你只评估解题过程、概念与逻辑，"
    "不重复判定最终数值答案是否命中（那由代码侧负责）。"
    "所有分数为 0~1 浮点数。你必须只输出一个 JSON 对象，不要输出任何多余文字。"
)

JUDGE_PROMPT_TEMPLATE = """\
下面给你一道题的【标准答案要点】【关键步骤列表】【评分细则 Rubric】，以及【待评模型答复】。
请依据 Rubric 对该答复的过程与逻辑打分。

规则：
1. 只看答复真正写出来的内容，不要脑补未写出的正确推导。
2. logic_score：按 Rubric 每个 Criterion 打 0~1，再用各自 Weight 加权求和（Weight 之和视为 100%）。
3. step_score：对照【关键步骤列表】，估计有效完成了多大比例的关键步骤（0~1）。
4. actual_steps：数出该答复中真正有效（正确且相关）的步骤/推理节点个数，排除错误、冗余、重复、无关步骤，取整数。
5. 严格只输出如下 JSON（数值用小数）：
{{"logic_score": <0~1>, "step_score": <0~1>, "actual_steps": <整数>, "criteria": [{{"name": "...", "weight": <0~1>, "score": <0~1>, "reason": "..."}}], "comment": "一句话总评"}}

【标准答案要点】
{reference}

【关键步骤列表】（共 {n_steps} 步，作为基准步骤数 N0）
{steps}

【评分细则 Rubric】
{rubric}

【待评模型答复】
{answer}
"""


def _extract_json(text: str) -> Optional[dict]:
    """从裁判输出里抽取第一个 JSON 对象，容忍 ```json 包裹或前后噪声。"""
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    candidates = []
    if fenced:
        candidates.append(fenced.group(1))
    # 退化：找第一个 { 到最后一个 } 的最大括号块
    first, last = text.find("{"), text.rfind("}")
    if first != -1 and last != -1 and last > first:
        candidates.append(text[first:last + 1])
    for cand in candidates:
        try:
            return json.loads(cand)
        except json.JSONDecodeError:
            continue
    return None


def _clip01(x, default: float = 0.0) -> float:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return default
    return max(0.0, min(1.0, v))


# 裁判占总分约 53%（step+logic 占 S_i 的 2/3，且 step_score 门控整个 20% 效率项），
# 而四个扰动算子完全不覆盖它。所以裁判侧的每一种「判不出来」都必须留痕、可计数，
# 不能静默折算成一个看起来正常的分数。三种失效各自打标：
#   parse_error   裁判输出里没有可解析的 JSON
#   missing_keys  有 JSON 但缺 logic_score / step_score —— 否则与「真判 0 分」同形
#   scale_error   分值 > 1.0（裁判换成百分制），旧实现会被 _clip01 静默截成满分 1.0
JUDGE_FAILURE_FLAGS = ("parse_error", "missing_keys", "scale_error")


def judge_failure_kinds(detail: Optional[dict]) -> List[str]:
    """从落盘的 judge_detail 里取出失效标记，供 runner 汇总计数。"""
    if not isinstance(detail, dict):
        return []
    return [k for k in JUDGE_FAILURE_FLAGS if detail.get(k)]


class JudgeResult:
    def __init__(self, logic_score: float, step_score: float,
                 actual_steps: int, detail: dict):
        self.logic_score = logic_score
        self.step_score = step_score
        self.actual_steps = actual_steps
        self.detail = detail


def judge_answer(judge: BaseProvider, *, reference: str, steps: List[str],
                 rubric: str, answer: str, baseline_steps: int) -> JudgeResult:
    """调用裁判模型对单条答复评过程分。解析失败时回退为保守 0 分并记录原文。"""
    prompt = JUDGE_PROMPT_TEMPLATE.format(
        reference=reference or "（未提供）",
        n_steps=len(steps) or baseline_steps,
        steps="\n".join(steps) if steps else "（未提供）",
        rubric=rubric or "（未提供，按通用过程质量评估）",
        answer=answer,
    )
    result = judge.chat(prompt, system=JUDGE_SYSTEM)
    parsed = _extract_json(result.text)

    if not parsed:
        return JudgeResult(
            logic_score=0.0, step_score=0.0, actual_steps=baseline_steps,
            detail={"parse_error": True, "raw": result.text[:2000]},
        )

    detail = dict(parsed)

    # 缺 key 与「真判 0 分」必须可区分
    missing = [k for k in ("logic_score", "step_score") if parsed.get(k) is None]
    if missing:
        detail["missing_keys"] = missing

    # 标度错：0~1 之外的分值说明裁判不在本 rubric 的标度上。此时宁可记 0 并喊出来，
    # 也不能像旧实现那样截成 1.0——静默给满分会把全库过程分拉满且事后无从区分。
    raw_vals = [parsed.get("logic_score"), parsed.get("step_score")]
    out_of_scale = []
    for k, v in zip(("logic_score", "step_score"), raw_vals):
        try:
            if v is not None and float(v) > 1.0:
                out_of_scale.append(k)
        except (TypeError, ValueError):
            continue
    if out_of_scale:
        detail["scale_error"] = out_of_scale
        return JudgeResult(logic_score=0.0, step_score=0.0,
                           actual_steps=baseline_steps, detail=detail)

    logic = _clip01(parsed.get("logic_score"))
    step = _clip01(parsed.get("step_score"))

    # `or baseline_steps` 会把裁判明确给出的 actual_steps=0 吞成「与参考解一样多」，
    # 让 scoring-rules 第六节对 N=0 的规定永不触发。这里只在「缺字段」时回退。
    raw_steps = parsed.get("actual_steps")
    if raw_steps is None:
        actual = baseline_steps
    else:
        try:
            actual = int(raw_steps)
        except (TypeError, ValueError):
            actual = baseline_steps
    actual = max(actual, 0)

    return JudgeResult(logic_score=logic, step_score=step, actual_steps=actual,
                       detail=detail)
