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

    logic = _clip01(parsed.get("logic_score"))
    step = _clip01(parsed.get("step_score"))
    try:
        actual = int(parsed.get("actual_steps") or baseline_steps)
    except (TypeError, ValueError):
        actual = baseline_steps
    actual = max(actual, 0)

    return JudgeResult(logic_score=logic, step_score=step, actual_steps=actual,
                       detail=parsed)
