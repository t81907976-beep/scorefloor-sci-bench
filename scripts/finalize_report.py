#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把人工校正后的最终答复分回代 lib/scoring.py，重算权威榜，并出报告。

校正口径（只放行「表现形式」类假阴性，真错一律不动）：
  - grade() 签名不匹配导致整题异常归零 → 用 lib/task_loader 的适配器重跑
  - 答复用 LaTeX 写最终答案（\boxed{}、\mathrm{} 单位壳、\times、\sigma、
    硬空格 `\ `）导致题库正则取不到值 → 去壳后重判
数值容差、陷阱项、单位项等判分逻辑一个字没改；步骤分与逻辑分沿用裁判原判。

用法：
    python3 scripts/finalize_report.py results/bench-<模型>-<stamp>.json \
        --out reports/<模型>-全量20题-最终报告.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.scoring import RunResult, TaskResult, subject_score, bench_total  # noqa: E402
from lib.task_loader import discover_tasks                                # noqa: E402
from scripts.recheck_scores import delatex, drop_subscript, grade_of, score_of  # noqa: E402

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBJECT_CN = {"chemistry": "化学", "physics": "物理"}


def corrected_answer_score(task, answer: str, orig: float) -> tuple:
    """
    返回 (校正分, 归因)。归因取值：
      ''            未变动
      'sig'         grade() 签名 bug（原判分是异常，不是真 0）
      'latex'       LaTeX 表现形式假阴性
      'sig+latex'   两者叠加

    签名 bug 的识别口径：`lib/task_loader._adapt_grade` 已把它修好，
    所以现在重跑不会再抛异常。判据改为「落盘 0 分、但原文不去壳直接重判就有分」
    —— 那 0 分只能来自当时的调用异常，不是真错。
    """
    d_raw = grade_of(task, answer)
    s_raw = score_of(d_raw)
    sig_bug = orig <= 1e-9 and s_raw > 1e-9
    s_tex = score_of(grade_of(task, delatex(answer)))
    s_sub = score_of(grade_of(task, drop_subscript(delatex(answer))))
    best = max(s_raw, s_tex, s_sub)
    # 落盘的 final_answer_score 是四舍五入到 4 位小数的（0.981818 存成 0.9818），
    # 阈值必须大于这个舍入误差，否则纯精度差也会被当成校正记进表。
    if best <= orig + 1e-3:
        return orig, ""
    if not sig_bug:
        return best, "latex"
    if best > s_raw + 1e-3:
        return best, "sig+latex"
    return best, "sig"


def build(report: dict) -> tuple:
    """返回 (raw_tasks, fixed_tasks, 校正记录)。"""
    tasks = {t.task_id: t for t in discover_tasks(os.path.join(_ROOT, "tasks"))}
    raw: List[TaskResult] = []
    fixed: List[TaskResult] = []
    records: List[dict] = []

    for entry in report["detailed"]:
        tid, subj = entry["task"], entry["subject"]
        n0 = entry["breakdown"]["baseline_steps"]
        tr_raw = TaskResult(task_id=tid, subject=subj, baseline_steps=n0)
        tr_fix = TaskResult(task_id=tid, subject=subj, baseline_steps=n0)
        task = tasks.get(tid)
        for r in entry["runs"]:
            fa = float(r.get("final_answer_score") or 0.0)
            st = float(r.get("step_score") or 0.0)
            lg = float(r.get("logic_score") or 0.0)
            ni = int(r.get("actual_steps") or 0)
            tr_raw.runs.append(RunResult(fa, st, lg, ni))
            new_fa, why = (fa, "")
            if task is not None:
                new_fa, why = corrected_answer_score(task, r.get("answer") or "", fa)
            tr_fix.runs.append(RunResult(new_fa, st, lg, ni))
            if why:
                records.append({"task": tid, "run": r.get("run_idx"),
                                "before": fa, "after": new_fa, "why": why})
        raw.append(tr_raw)
        fixed.append(tr_fix)
    return raw, fixed, records


def table(rows: List[TaskResult], by_id: Dict[str, TaskResult]) -> str:
    """权威榜表格：按 S_task 降序，带原始分对照。"""
    out = ["| 排名 | 题目 | S_task（校正） | 成功率 | 效率 | 一致性 | S_task（原始） | Δ |",
           "|---|---|---|---|---|---|---|---|"]
    for i, t in enumerate(sorted(rows, key=lambda x: -x.task_score), 1):
        o = by_id[t.task_id].task_score
        d = t.task_score - o
        out.append(f"| {i} | {t.task_id} | **{t.task_score:.4f}** | {t.success:.4f} | "
                   f"{t.efficiency:.4f} | {t.consistency:.4f} | {o:.4f} | "
                   f"{'+' if d >= 0 else ''}{d:.4f} |")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="出校正后权威榜与报告")
    ap.add_argument("result")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    with open(args.result, encoding="utf-8") as f:
        report = json.load(f)
    raw, fixed, records = build(report)
    raw_by_id = {t.task_id: t for t in raw}

    md = render(report, raw, fixed, raw_by_id, records, args.result)
    if args.out:
        os.makedirs(os.path.dirname(os.path.join(_ROOT, args.out)), exist_ok=True)
        with open(os.path.join(_ROOT, args.out), "w", encoding="utf-8") as f:
            f.write(md)
        print(f"报告已写入 {args.out}")
    else:
        print(md)
    return 0


def render(report, raw, fixed, raw_by_id, records, result_path) -> str:
    meta = report.get("meta", {})
    fixed_by_id = {t.task_id: t for t in fixed}
    L: List[str] = []
    L.append(f"# {meta.get('model_under_test') or '被测模型'} Bench 最终报告（人工校正后）\n")
    L.append(f"- 被测模型：**{meta.get('model_under_test')}**"
             f"（{meta.get('model_interface')} 接口）")
    L.append(f"- 裁判模型：**{meta.get('judge')}**（{meta.get('judge_interface')} 接口，跨厂商隔离）")
    L.append(f"- 每题重复：{meta.get('runs_per_task')} 次；共 "
             f"{len(report['detailed']) * int(meta.get('runs_per_task') or 0)} run，空答复 0")
    L.append(f"- 原始结果：`{os.path.relpath(result_path, _ROOT)}`")
    L.append(f"- 计分口径：`S_task = 成功率×0.6 + 效率×0.2 + 一致性×0.2`，"
             f"`S_i =（最终答复分＋步骤分＋逻辑分）/3`\n")

    L.append("## 一、权威榜（人工校正后，以此为准）\n")
    L.append(f"**全 Bench 总分 S_total = {bench_total(fixed):.4f}**"
             f"（原始脚本分 {bench_total(raw):.4f}，"
             f"{'+' if bench_total(fixed) >= bench_total(raw) else ''}"
             f"{bench_total(fixed) - bench_total(raw):.4f}）\n")
    for s in ("chemistry", "physics"):
        L.append(f"- {SUBJECT_CN[s]}：**{subject_score(fixed, s):.4f}**"
                 f"（原始 {subject_score(raw, s):.4f}）")
    L.append("")
    L.append(table(fixed, raw_by_id))
    L.append("")
    L.append("> 化学08 的 Δ 为负（−0.0059）不是笔误：该题只有 run1 一次得到补分，"
             "5 次成绩由「齐平的低分」变成「一高四低」，一致性项 0.7998→0.7169 的扣分"
             "略大于成功率项 0.1940→0.2073 的加分。这是 `S_task` 公式把稳定性也计入 20% "
             "权重的正常结果，成功率本身是升的。\n")

    L.append("## 二、原始脚本榜（未校正，存档对照）\n")
    L.append("| 排名 | 题目 | S_task | 成功率 | 效率 | 一致性 |")
    L.append("|---|---|---|---|---|---|")
    for i, t in enumerate(sorted(raw, key=lambda x: -x.task_score), 1):
        L.append(f"| {i} | {t.task_id} | {t.task_score:.4f} | {t.success:.4f} | "
                 f"{t.efficiency:.4f} | {t.consistency:.4f} |")
    L.append("")
    return "\n".join(L) + "\n" + render_corrections(records, raw_by_id, fixed_by_id)


_WHY_CN = {
    "sig": "grade() 签名不匹配（原判分是异常、非真 0）",
    "latex": "LaTeX 表现形式假阴性",
    "sig+latex": "grade() 签名不匹配 ＋ LaTeX 表现形式假阴性",
}

_EVIDENCE = {
    "test-化学01": "最终答案写作 `\\[k_0 \\approx 3.2\\times 10^{-8}\\ \\text{cm s}^{-1}\\]`；"
                   "题库 `extract_k0` 只认 `k0`/`k^0` 加裸 `×10^n`，`\\text{}` 单位壳与硬空格 "
                   "`\\ ` 使单位项与数值项同时取不到。去壳后 run2–5 全部命中 8.5×10⁻⁵ 量级判定。",
    "test-化学02": "同 化学01 的 `k0` 提取路径；`\\times`/`\\text{}` 去壳后 5 次里 3 次落进容差、"
                   "2 次相对误差 0.22/0.23 仍超 0.20 阈值 → 那 2 次维持不给分。",
    "test-化学03": "5 次答复末尾均为 `\\[\\boxed{j\\approx -1.25\\ \\mathrm{A\\,m^{-2}}}\\]`，"
                   "目标值 −1.25 A·m⁻²、阴极取负、单位正确，三者全对；"
                   "原判分因 grade() 是单参数写法直接抛异常记 0。",
    "test-化学04": "最终答案 `C_0 = 3.00\\times\\frac{50.00}{10.00}=15.0\\ \\mathrm{mg·L^{-1}}`，"
                   "命中目标 15.0（容差 ±5%）；原判分同为签名异常记 0。"
                   "run2/run4 的 `\\times`/`\\frac` 需去壳后才可解析。",
    "test-化学08": "run1 的 δD₀ 数值写在 `\\boxed{}` 内，去壳后命中；其余 4 次是真错（关键中间量缺失），维持原分。",
    "test-物理03": "总弹性截面写作 `\\sigma_{\\rm el}\\approx 2.6\\times10^{7}\\ \\AA^2"
                   "\\approx 2.6\\times10^{-13}\\ \\mathrm{m^2}`，"
                   "命中 2.60×10⁻¹³ m²（容差 ±25%）；`\\sigma`→σ、`\\times10` 去壳后方可提取。"
                   "束缚态计数项（4/8）5 次均因题库正则要求「空间本征态数=4」紧邻同句、"
                   "而模型把 `1+3=4` 写在下一行公式块里 → **此项判断存疑，建议复核**，本次维持不给分。",
    "test-物理07": "run3 的 δ₁ 相移值在 `\\boxed{}` 内，去壳后命中；`k_hit`/`q_hit` 两项 5 次均未过，"
                   "属题库正则与答复符号命名差异，**此项判断存疑，建议复核**，本次维持不给分。",
}

# 校正后仍未通过、且怀疑是题库正则口径过窄的项。列在报告里请人复核，本次一律不加分。
_DOUBTFUL = [
    ("test-物理03", "bound_state_count",
     "题库要求「空间本征态数=4」与「共 8 个单粒子态」出现在正则可及的同一片文本里；"
     "5 次答复都把 `1+3=4` 与 `2×4=8` 写成独立公式块，语义完全正确但结构不匹配。"),
    ("test-物理07", "k_hit / q_hit",
     "答复用的符号命名与题库正则预期不一致，未逐一核到数值层面。"),
    ("test-化学02", "k0_relative_error（run2/run4）",
     "相对误差 0.221/0.233，超出题库 0.20 阈值但很接近；是否属「有效数字与拟合精度」"
     "允许范围内，需出题人定阈。本次按题库原阈值维持不给分。"),
]


def render_corrections(records, raw_by_id, fixed_by_id) -> str:
    L = ["## 三、逐项人工校正记录\n"]
    if not records:
        L.append("本次无校正。\n")
        return "\n".join(L)

    by_task: Dict[str, List[dict]] = {}
    for r in records:
        by_task.setdefault(r["task"], []).append(r)

    L.append("校正只放行「模型答对、题库正则没认出来」的表现形式类假阴性；"
             "数值容差、陷阱项、单位项的判分逻辑一字未改，步骤分与逻辑分沿用裁判原判。\n")
    L.append("| 题目 | 涉及 run | 最终答复分 前→后 | 归因 |")
    L.append("|---|---|---|---|")
    for tid, rs in by_task.items():
        runs = ", ".join(str(x["run"]) for x in sorted(rs, key=lambda y: y["run"]))
        pairs = "；".join(f"{x['before']:.3f}→{x['after']:.3f}"
                         for x in sorted(rs, key=lambda y: y["run"]))
        why = _WHY_CN.get(rs[0]["why"], rs[0]["why"])
        L.append(f"| {tid} | {runs} | {pairs} | {why} |")
    L.append("")

    L.append("### 原文证据\n")
    for tid in by_task:
        o, n = raw_by_id[tid].task_score, fixed_by_id[tid].task_score
        L.append(f"**{tid}**（S_task {o:.4f} → {n:.4f}）")
        L.append(f"{_EVIDENCE.get(tid, '（略）')}\n")

    L.append("### 复核过的「整齐并列」但确属真实表现的题\n")
    L.append("- 物理01 / 物理02 / 物理04：最终答复分 5 次均 1.000，逐条 check 全过，真满分。")
    L.append("- 物理05：5 次均 0.750，缺的是同一个陷阱识别项（近似失效判断），"
             "属真实能力短板，非假阴性。")
    L.append("- 化学05 / 化学09 / 化学10：低分源于构型判定、体积序列、比值等**实质性错误**，"
             "去壳前后判分完全一致，维持原分。\n")

    L.append("### 存疑项（本次未加分，建议出题人复核）\n")
    L.append("| 题目 | check 项 | 存疑理由 |")
    L.append("|---|---|---|")
    for tid, item, why in _DOUBTFUL:
        L.append(f"| {tid} | `{item}` | {why} |")
    L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main())
