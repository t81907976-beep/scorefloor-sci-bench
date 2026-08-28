"""
ScoreFloor-Sci-Bench — 出题补全节点 (Task Authoring)

用户只手填一道题的前三段（query / SFT标准-response / 步骤列表-reference），
本模块调网关 LLM 自动补全后三段（Grading Criteria / Automated Checks 的 grade() /
LLM Judge Rubric），并用「标准答案高分 + 反例低分」双向自检保证生成的 grade()
真有区分度；通过后才把三段追加回 .md。

链路：
    load 半成品 → 检测后三段是否为空 → 生成（含反例）→ 编译+沙盒跑 grade()
    → 自检（ref 高、反例低）→ 不过则回喂失败原因重写（最多 N 次）→ 写回文件

对外主入口：author_task(path, model, ...) 。runner 的 `author` 子命令调它。
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import List, Optional

from .providers import BaseProvider
from .task_loader import (
    _extract_python_block,
    _find_section,
    _promote_bare_labels,
    _split_sections,
)

# 自检阈值：标准答案至少拿到 REF_MIN；每份反例要么绝对 ≤ CE_MAX，
# 要么比标准答案低至少 MARGIN。三者满足才算这份 grade() 有区分度。
REF_MIN = 0.80
CE_MAX = 0.55
MARGIN = 0.25

# 生成输出用的分节标记（比 JSON 更适合承载含大量特殊字符的 python 代码）
_MARK = {
    "grading": "===GRADING_CRITERIA===",
    "checks": "===AUTOMATED_CHECKS===",
    "rubric": "===LLM_JUDGE_RUBRIC===",
    "ce": "===COUNTEREXAMPLE",  # 后接 _1===/_2===
    "end": "===END===",
}


@dataclass
class HalfTask:
    """半成品题目：只解析出前三段与后三段是否已存在。"""

    task_id: str
    subject: str
    path: str
    raw_text: str
    query: str
    reference: str
    steps_body: str
    has_grading: bool
    has_checks: bool
    has_rubric: bool

    @property
    def n_steps(self) -> int:
        return max(len([l for l in self.steps_body.splitlines()
                        if re.match(r"^\s*\[\d+\]", l)]), 1)

    @property
    def complete(self) -> bool:
        return self.has_grading and self.has_checks and self.has_rubric


@dataclass
class AuthorResult:
    """补全结果。ok=False 时 reason 说明卡在哪。"""

    ok: bool
    task_id: str
    grading: str = ""
    checks: str = ""      # 完整 ```python ...``` 代码块外的纯代码
    rubric: str = ""
    counterexamples: List[str] = field(default_factory=list)
    ref_score: Optional[float] = None
    ce_scores: List[float] = field(default_factory=list)
    attempts: int = 0
    reason: str = ""
    written: bool = False


AUTHOR_SYSTEM = (
    "你是 ScoreFloor-Sci-Bench 的出题评分规范作者。用户给你一道题的题面、标准解答与关键步骤，"
    "你要产出三块评分规范：结果检查清单(Grading Criteria)、可执行的 Python 评分脚本(grade 函数)、"
    "以及交给裁判模型的过程 Rubric。你还要造出会踩本题核心陷阱的错误答复，用于验证脚本区分度。"
    "严格按要求的分节标记输出，不要输出任何多余解释。"
)

# ⚠️ 必须是 raw 字符串。模板里大量出现 LaTeX 命令，非 raw 时 Python 会把
# `\boxed`→退格+oxed、`\text`/`\times`→制表符+ext/imes、`\approx`→响铃+pprox、
# `\rm`→回车+m 全部吃掉，发给出题模型的写法容错指引变成乱码（0728 引入，0811 修）。
# 同时注意：本模板走 .format()，字面花括号必须写成 {{ }}，否则 LaTeX 的 `{..}`
# 会被当成占位符，_build_prompt 直接抛 IndexError。
AUTHOR_PROMPT = r"""下面是一道题已填好的前三段。请补全后三段评分规范，并额外造出 {n_ce} 份"会踩本题核心陷阱的错误答复"用于自检。

【题面 query】
{query}

【标准解答 SFT-response】
{reference}

【关键步骤 steps（共 {n_steps} 步，即基准步骤数 N0）】
{steps}

====================  你要产出的内容  ====================

1) Grading Criteria：5~8 条结果检查清单，每条对应标准答案的一个关键结果或推理节点，写成 markdown 的 `- [ ] ...` 列表。只写"这道题最终应满足什么"，不写 Bench 总分/效率/一致性。

2) grade() 评分脚本，必须严格满足：
   - 函数签名固定为 `def grade(transcript: list, workspace_path: str, meta: dict) -> dict:`
   - **自包含**：所有辅助函数(取文本、抽数值、判容差、判拒答)都在函数体内定义，不 import lib、不依赖 meta 里的答案(meta 只有 task_id)。可以 `import re`。
   - transcript 是 `[{{"role":"assistant","content":"<答复全文>"}}, ...]`，content 可能是 str 或 [{{"text":...}}] 段列表，取文本时都要兼容。
   - 只检查**最终答复的硬证据**(数值命中/单位/关键结论方向)，不评推导过程。
   - 返回一个**扁平 dict**，每个检查项一个 0~1 的键，且**必须**含 `auto_final_answer_score`(所有检查项加权，权重和=1.0)。
   - **禁止出现下列白拿项**(0805 假阳性审计：100 份真实答复把结论数值全部作废、文字与格式一字不改重判，仍拿到 55% 的分，病因全在这几种写法)：
     · `non_empty_answer` / `not_refusal`：与题目无关，任何答复都拿。空答复与拒答由 runner 层记 0，不要在 grade() 里重复给分。
     · `target_extracted` 这类只判"抽到了值"的项：抽到值 ≠ 值对。必须与容差判据合并成一项，抽不到即 0。
     · `has_unit` / `has_basis` 这类只判单位或基准**出现过**的项：单位串出现在推导任意一处就命中，答错照给。要判就要求单位**紧贴结论数值**(同一行、数值后 12 字符内)且量纲与目标相容。
     · 反向项写成 `val is None or abs(val-陷阱值)>阈值`：不给数值时反向项全为真，导致**软托词比老实拒答分高**。陷阱一律写成扣分项——命中陷阱值才扣，`val is None` 不加不扣。
     · 纯文字结论型判据(判"选对了哪支解"之类)对数值扰动免疫、探针测不出但同样白拿：每个文字结论必须**配一个只有真选对才写得出的派生数值**作锚，**并且加否定词前瞻**——0806 实测「本题未做 ECSA 归一」让 `has_ecsa_basis` 拿满、「热通道不主导」让 `dominant_thermal` 拿满，说反话与说对话同分。窗内出现「不/未/无/非/可忽略」应判 0。
   - 权重只许落在"答对才拿得到"的项上。写完后跑 `python3 scripts/audit_false_positive.py --task <题号> --verbose` 自检，地板占比应低于 30%；高于 50% 说明这道题测不出模型能力，必须重写判据。非数值答案题数值探针会跳过，改跑 `python3 scripts/audit_label_swap.py`。
   - **数值容差用相对误差比较，绝不用正则限死小数位数**(0806 撞出的最大单项假阴性，0.55/1.00)：
     · 写 `abs(v-target)/abs(target)<=0.03`，不写 `re.search(r'0\.4[45]\d?', text)`——后者等价于规定模型必须写几位有效数字，多写一位就掉分。
     · 百分数与小数是同一个量的两种写法，两支都要收(`0.4483` 与 `44.83%`)，且**两支容差必须一致**——0806 化学08 的百分号支比小数支宽 40 倍，把两个陷阱值放进了正确窗。
     · 正则里的 `\d*` / `\d?` 必须给上限：`r'0\.50\d*'` 的实际上界是 0.51 而非 0.505，`0.5099` 照收。写 `\d{{0,2}}`。
     · 自检：把目标值多写一位、少写一位、换成百分数各判一遍，四种写法必须同分。
     · 科学计数法(`×10^`, `e-6`, `⁻`)要兼容。
   - **写法容错(自包含 normalize()，务必内置，否则同一物理答案的不同 LaTeX 写法会假阴性)**：在抽数值/匹配关键词前，先把答复文本过一遍 normalize()，至少做到——
     · 上标/乘号/负号统一：`²³⁻`→`23-`、`×·−—`→`x*-`；`Å`(ANGSTROM SIGN)与 `Å` 统一码位。
     · 剥离 LaTeX 装饰包裹但保留内容：`\boxed{{..}}`/`\mathrm{{..}}`/`\text{{..}}`/`{{\rm ..}}` 等(多轮剥离嵌套)。
     · 去数学定界符与命令：`\(...\)`/`\[...\]`、`\,\;`细空格、其余 `\command`；`\AA`/`\text{{Å}}`/`\mathring{{A}}`→`Å`，`\times`→`x`，`\approx\simeq`→`≈`。
     · `a×10^b` / `a x 10^{{b}}` → `ae b` 供科学计数法分支消费。
   - **等价物理写法双向匹配**：同一结论的不同正确表述都要接受。例：消光条件既可写允许式 `h+k+l=2n`(偶数)也可写禁戒式「h+k+l 为奇数时消光」，二者物理等价须都命中；晶面/指标三元组除 `(hkl)` 括号包裹外，也要匹配「独立 token」写法(两侧非数字/字母、不接单位)以兼容英文逗号列举 `001, 102 and 111` 及归一后去括号的 hkl。这类写法容错可参考 `lib/grading_utils.py` 的 `normalize()`/`miller_indices_present()`，但因 grade() 须自包含，请把等价逻辑**内联**进函数体。
   - **区分度**：对本题核心防御位(最易搞反/最易踩的陷阱)必须设独立检查项——标准答案应命中、下面你造的反例应命中不到。不要把 `auto_final_answer_score` 写成恒为高分。

3) LLM Judge Rubric：3~5 个 Criterion，每个写清 `Weight: X%`，分档(Score 1.0 / 0.5 / 0.0，可按需要增减档)专题定制，每档对应真实可判、互斥、可回落原文的表现。对致命陷阱那一档可直接给 0.0。不要重复判定 grade() 已覆盖的最终数值命中，只评过程/概念/逻辑。

4) 反例：{n_ce} 份完整的"错误答复文本"(就像模型真的会写出来的解答，几百字即可)，每份必须**踩到本题一个核心陷阱**(如把主支/归属搞反、漏关键项导致数量级错、误判近似成立)，使得用你上面写的 grade() 去评时，`auto_final_answer_score` 明显低于标准答案。

====================  输出格式(严格)  ====================
{grading_mark}
<这里是 Grading Criteria 的 markdown 列表>
{checks_mark}
```python
<这里是完整 grade() 源码>
```
{rubric_mark}
<这里是 LLM Judge Rubric 的 markdown>
{ce_mark}_1===
<第 1 份错误答复全文>
{ce_mark}_2===
<第 2 份错误答复全文>
{end_mark}
"""

RETRY_SUFFIX = """\

======= 上一版自检未通过，请修正后重新输出全部四部分 =======
失败原因：{reason}
自检数据：标准答案得分={ref}，反例得分={ce}。
要求：标准答案得分应 ≥ {ref_min}；每份反例得分应 ≤ {ce_max} 或比标准答案低 ≥ {margin}。
若标准答案得分偏低 → 放宽对标准答案的命中判据(容差/正则)；
若反例得分偏高 → 收紧核心防御位检查项，使其能抓住反例踩的陷阱。
请重新输出（仍严格用分节标记），不要解释改动。
"""


# --------------------------------------------------------------------------
# 解析半成品 & LLM 输出
# --------------------------------------------------------------------------
def load_half_task(path: str) -> HalfTask:
    """解析半成品：拿到前三段，判断后三段是否已存在（正文非空）。"""
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    text = _promote_bare_labels(raw)
    sections = _split_sections(text)
    task_id = os.path.splitext(os.path.basename(path))[0]
    subject = os.path.basename(os.path.dirname(path))

    query = _find_section(sections, "query", "构造高质量", "题目")
    reference = _find_section(sections, "SFT", "标准-response", "标准答案", "答案")
    steps_body = _find_section(sections, "步骤列表", "步骤列表-reference", "解题思路")

    grading = _find_section(sections, "Grading Criteria", "结果检查", "评分要点")
    checks = _find_section(sections, "Automated Checks")
    rubric = _find_section(sections, "LLM Judge Rubric", "Judge Rubric")

    return HalfTask(
        task_id=task_id, subject=subject, path=path, raw_text=raw,
        query=query, reference=reference, steps_body=steps_body,
        has_grading=bool(grading.strip()),
        has_checks=bool(_extract_python_block(checks).strip()),
        has_rubric=bool(rubric.strip()),
    )


def _slice(text: str, start_mark: str, *end_marks: str) -> str:
    """取 start_mark 之后、到最近一个 end_mark 之前的正文。"""
    i = text.find(start_mark)
    if i == -1:
        return ""
    i += len(start_mark)
    end = len(text)
    for em in end_marks:
        j = text.find(em, i)
        if j != -1:
            end = min(end, j)
    return text[i:end].strip()


def parse_author_output(text: str, n_ce: int) -> dict:
    """把 LLM 的分节输出拆成 grading/checks(纯代码)/rubric/counterexamples。"""
    ce_mark = _MARK["ce"]
    grading = _slice(text, _MARK["grading"], _MARK["checks"])
    checks_block = _slice(text, _MARK["checks"], _MARK["rubric"])
    rubric = _slice(text, _MARK["rubric"], f"{ce_mark}_1===", ce_mark, _MARK["end"])

    code = _extract_python_block(checks_block) or checks_block

    counterexamples = []
    for k in range(1, n_ce + 1):
        nxt = f"{ce_mark}_{k + 1}==="
        ce = _slice(text, f"{ce_mark}_{k}===", nxt, _MARK["end"])
        if ce:
            counterexamples.append(ce)
    return {
        "grading": grading,
        "code": code.strip(),
        "rubric": rubric,
        "counterexamples": counterexamples,
    }


# --------------------------------------------------------------------------
# 沙盒编译并运行 grade()
# --------------------------------------------------------------------------
def compile_grade(code: str):
    """编译 grade() 源码，返回 callable；失败抛 ValueError。"""
    if not code.strip():
        raise ValueError("生成的 grade() 代码为空")
    ns: dict = {}
    try:
        exec(compile(code, "<authored-grade>", "exec"), ns)  # noqa: S102
    except SyntaxError as exc:
        raise ValueError(f"grade() 语法错误: {exc}") from exc
    fn = ns.get("grade")
    if not callable(fn):
        raise ValueError("代码块未定义 grade()")
    return fn


def score_answer(grade_fn, answer: str, task_id: str) -> float:
    """用 grade() 给一条答复打 auto_final_answer_score。"""
    transcript = [{"role": "assistant", "content": answer}]
    detail = grade_fn(transcript, ".", {"task_id": task_id})
    if not isinstance(detail, dict):
        raise ValueError(f"grade() 未返回 dict，而是 {type(detail).__name__}")
    if "auto_final_answer_score" not in detail:
        raise ValueError("grade() 返回值缺少 auto_final_answer_score")
    return float(detail["auto_final_answer_score"])


def self_check(code: str, reference: str, counterexamples: List[str],
               task_id: str) -> tuple:
    """
    双向自检：标准答案应高分、反例应低分。
    返回 (ok, ref_score, ce_scores, reason)。任一环节异常都视为不过。
    """
    try:
        grade_fn = compile_grade(code)
    except ValueError as exc:
        return False, None, [], str(exc)

    try:
        ref_score = score_answer(grade_fn, reference, task_id)
    except Exception as exc:
        return False, None, [], f"标准答案跑 grade() 出错: {exc}"

    ce_scores = []
    for i, ce in enumerate(counterexamples, 1):
        try:
            ce_scores.append(score_answer(grade_fn, ce, task_id))
        except Exception as exc:
            return False, ref_score, ce_scores, f"反例{i}跑 grade() 出错: {exc}"

    if ref_score < REF_MIN:
        return False, ref_score, ce_scores, (
            f"标准答案得分 {ref_score:.3f} < {REF_MIN}（命中判据太严）")

    for i, cs in enumerate(ce_scores, 1):
        if not (cs <= CE_MAX or cs <= ref_score - MARGIN):
            return False, ref_score, ce_scores, (
                f"反例{i}得分 {cs:.3f} 过高（未 ≤{CE_MAX}，也未比标准答案低 {MARGIN}）"
                "——核心防御位没抓住陷阱")

    if not counterexamples:
        return False, ref_score, ce_scores, "未生成任何反例，无法验证区分度"

    return True, ref_score, ce_scores, ""


# --------------------------------------------------------------------------
# 主流程：生成 → 自检 → 重试 → 写回
# --------------------------------------------------------------------------
def _build_prompt(half: HalfTask, n_ce: int) -> str:
    steps = half.steps_body.strip() or "（未提供）"
    return AUTHOR_PROMPT.format(
        n_ce=n_ce, query=half.query or "（未提供）",
        reference=half.reference or "（未提供）", steps=steps, n_steps=half.n_steps,
        grading_mark=_MARK["grading"], checks_mark=_MARK["checks"],
        rubric_mark=_MARK["rubric"], ce_mark=_MARK["ce"], end_mark=_MARK["end"],
    )


def author_task(path: str, model: BaseProvider, *, n_ce: int = 2,
                max_attempts: int = 3, write: bool = True,
                verbose: bool = True) -> AuthorResult:
    """
    对一个半成品 .md 补全后三段并自检。write=True 时通过后追加写回文件。
    """
    half = load_half_task(path)
    if not half.query.strip() or not half.reference.strip():
        return AuthorResult(ok=False, task_id=half.task_id,
                            reason="前三段不完整：缺 query 或 SFT标准-response")
    if half.complete:
        return AuthorResult(ok=False, task_id=half.task_id,
                            reason="后三段已存在，跳过（如需重写请先删除原三段）")

    prompt = _build_prompt(half, n_ce)
    last_reason = ""
    ref_score = None
    ce_scores: List[float] = []

    for attempt in range(1, max_attempts + 1):
        if verbose:
            print(f"  · 生成尝试 {attempt}/{max_attempts} …")
        full_prompt = prompt
        if attempt > 1:
            full_prompt += RETRY_SUFFIX.format(
                reason=last_reason, ref=ref_score, ce=ce_scores,
                ref_min=REF_MIN, ce_max=CE_MAX, margin=MARGIN)

        out = model.chat(full_prompt, system=AUTHOR_SYSTEM).text
        parsed = parse_author_output(out, n_ce)

        if not parsed["code"]:
            last_reason = "输出中未找到 grade() 代码块"
            if verbose:
                print(f"    ✗ {last_reason}")
            continue

        ok, ref_score, ce_scores, reason = self_check(
            parsed["code"], half.reference, parsed["counterexamples"], half.task_id)
        last_reason = reason

        if verbose:
            ce_str = ", ".join(f"{c:.3f}" for c in ce_scores) if ce_scores else "—"
            print(f"    自检: 标准答案={ref_score if ref_score is None else round(ref_score,3)}"
                  f" 反例=[{ce_str}] → {'通过' if ok else '未过：'+reason}")

        if ok:
            result = AuthorResult(
                ok=True, task_id=half.task_id,
                grading=parsed["grading"], checks=parsed["code"],
                rubric=parsed["rubric"], counterexamples=parsed["counterexamples"],
                ref_score=ref_score, ce_scores=ce_scores, attempts=attempt)
            if write:
                _write_back(half, result)
                result.written = True
            return result

    return AuthorResult(ok=False, task_id=half.task_id, attempts=max_attempts,
                        ref_score=ref_score, ce_scores=ce_scores,
                        reason=f"{max_attempts} 次生成均未通过自检；最后一次：{last_reason}")


def _write_back(half: HalfTask, res: AuthorResult) -> None:
    """把后三段追加到原文件末尾，保留前三段原文不动。"""
    block = f"""

## Grading Criteria

{res.grading}

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程（本段由 lib.authoring 自动生成并通过双向自检）。

```python
{res.checks}
```

## LLM Judge Rubric

{res.rubric}
"""
    text = half.raw_text.rstrip() + "\n" + block
    with open(half.path, "w", encoding="utf-8") as f:
        f.write(text)
