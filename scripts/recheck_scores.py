#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人工校正辅助：对已落盘的 bench 结果重新判分，定位 grade() 假阴性。

做两件事，都不改判分逻辑本身：
  1. 修 grade() 签名不匹配（化学03/04 写成 grade(answer)，被三参数调用直接抛异常
     → 整题 5 次全 0）。已在 lib/task_loader.py 的 _adapt_grade 里下沉修好，
     这里只是重新跑一遍拿到真实分。
  2. 对答复文本做 LaTeX 去壳预处理后再判一次，识别「模型答对但正则没匹配上」的
     假阴性。去壳只动表现形式（\approx→≈、\mathrm{}/\rm 去壳、\boxed{} 拆壳、
     \times→x、\,\;\! 等间距命令去掉），不动任何数值与符号。

用法：
    python3 scripts/recheck_scores.py results/bench-<模型>-<stamp>.json
    python3 scripts/recheck_scores.py <结果json> --task test-化学03 --verbose
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.task_loader import discover_tasks  # noqa: E402

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


_GREEK = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε",
    "varepsilon": "ε", "zeta": "ζ", "eta": "η", "theta": "θ", "vartheta": "θ",
    "iota": "ι", "kappa": "κ", "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ",
    "pi": "π", "rho": "ρ", "varrho": "ρ", "sigma": "σ", "varsigma": "σ",
    "tau": "τ", "upsilon": "υ", "phi": "φ", "varphi": "φ", "chi": "χ",
    "psi": "ψ", "omega": "ω",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ",
    "Pi": "Π", "Sigma": "Σ", "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω",
}


def delatex(text: str) -> str:
    """
    把 LaTeX 表现形式还原成裸算式，只动形式不动内容。
    目的：让「\boxed{j\approx -1.25\ \mathrm{A\,m^{-2}}}」能被
    「j ≈ -1.25 A m^-2」这类正则命中。

    壳是嵌套的（\boxed{...\mathrm{A\,m^{-2}}}），单遍替换会因为
    `[^{}]*` 撞上内层花括号而失配，所以所有拆壳规则跑到不动点为止。
    """
    t = text
    # 希腊字母命令 → unicode。题库 check 写的是 σ / β / α 等 unicode 字符，
    # 模型输出的是 \sigma / \beta，纯表现形式差异。
    # 结尾用 (?![A-Za-z]) 而不是 \b：`_` 在正则里算单词字符，
    # `\sigma_tot` 的 "sigma" 后面没有 \b，用 \b 会整片漏掉带下标的写法。
    t = re.sub(r"\\([A-Za-z]+)(?![A-Za-z])",
               lambda m: _GREEK.get(m.group(1), m.group(0)), t)
    # 关系符与二元运算符。收尾一律用 (?![A-Za-z]) 而不是 \b：
    # `\times10^7` 里 "times" 后面紧跟数字，两侧都是单词字符、没有 \b，
    # 用 \b 会让最常见的 `\times10` 整片漏掉。
    t = re.sub(r"\\(?:approx|simeq|cong|sim)(?![A-Za-z])", "≈", t)
    t = re.sub(r"\\(?:le|leq)(?![A-Za-z])", "<=", t)
    t = re.sub(r"\\(?:ge|geq)(?![A-Za-z])", ">=", t)
    t = re.sub(r"\\(?:times|cdot)(?![A-Za-z])", "x", t)
    t = re.sub(r"\\pm(?![A-Za-z])", "+-", t)
    # 间距／尺寸／定界命令先清掉，避免它们卡在花括号里妨碍拆壳
    t = re.sub(r"\\(?:left|right|big|Big|bigg|Bigg|displaystyle|quad|qquad)\b", " ", t)
    t = re.sub(r"\\[,;:!]", " ", t)
    # 「\ 」（反斜杠+空白）是 LaTeX 硬空格，数值与单位之间最常见的一种；
    # 不清掉它，`-1.25\ A m^-2` 里的 \s* 匹配不过去，单位永远取不到。
    t = re.sub(r"\\(?=\s)", " ", t)
    t = t.replace("\\%", "%").replace("\\_", "_")
    # 无花括号的字体切换命令（`\sigma_\rm el`、`j_\rm geo`）
    t = re.sub(r"\\(?:mathrm|mathbf|mathit|mathsf|textrm|textbf|rm|bf|it|sf)\b", "", t)

    # 拆壳跑到不动点：上下标花括号、单位/文本壳、\boxed、分数
    for _ in range(12):
        prev = t
        t = re.sub(r"\^\s*\{([^{}]*)\}", r"^\1", t)
        t = re.sub(r"_\s*\{([^{}]*)\}", r"_\1", t)
        t = re.sub(r"\\(?:mathrm|mathbf|mathit|mathsf|text|textrm|textbf|rm|bf|it)"
                   r"\s*\{([^{}]*)\}", r"\1", t)
        t = re.sub(r"\{\s*\\(?:rm|bf|it|sf)\s+([^{}]*)\}", r"\1", t)
        t = re.sub(r"\\boxed\s*\{([^{}]*)\}", r"\1", t)
        t = re.sub(r"\\(?:d?frac)\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"(\1)/(\2)", t)
        if t == prev:
            break

    # 行间/行内公式定界符与剩余转义符
    t = t.replace("\\[", " ").replace("\\]", " ")
    t = t.replace("\\(", " ").replace("\\)", " ")
    t = re.sub(r"\\\\", " ", t)
    t = re.sub(r"\$+", " ", t)
    # 剩下的孤立花括号只是分组符号，留着会挡在数值与单位之间
    # （`-1.25 {A m^-2}` 里的 `{` 就足以让单位正则失配）。
    t = t.replace("{", " ").replace("}", " ")
    return t


def drop_subscript(text: str) -> str:
    """
    去掉紧跟字母/希腊字母的下标下划线：`k_0`→`k0`、`σ_tot`→`σtot`。

    题库 check 普遍只写了 `k0` / `k^0` 两种写法（如化学01 的
    `k\s*(?:\^\s*0|0)`），漏了最常见的数学写法 `k_0`；下标下划线纯属排版，
    去掉它不改变任何数值或符号。作为比 delatex 更激进的第三档单独统计。
    """
    return re.sub(r"(?<=[A-Za-z\u0370-\u03ff])_(?=[0-9A-Za-z])", "", text)


def grade_of(task, answer: str) -> dict:
    if task.grade_fn is None:
        return {}
    try:
        return task.grade_fn([{"role": "assistant", "content": answer}],
                             _ROOT, {"task_id": task.task_id}) or {}
    except Exception as exc:  # noqa: BLE001
        return {"grade_error": str(exc)}


def score_of(detail: dict) -> float:
    try:
        return float(detail.get("auto_final_answer_score", 0.0))
    except (TypeError, ValueError):
        return 0.0


def failed_checks(detail: dict) -> List[str]:
    """未通过项。题库里 check 值有 True/False 也有 1.0/0.0 两种写法，都要认。"""
    out = []
    for k, v in detail.items():
        if k == "auto_final_answer_score":
            continue
        if v is False or (isinstance(v, (int, float)) and not isinstance(v, bool)
                          and float(v) == 0.0):
            out.append(k)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="重新判分，定位 grade() 假阴性")
    ap.add_argument("result", help="results/bench-*.json")
    ap.add_argument("--task", default="", help="只看这道题")
    ap.add_argument("--verbose", action="store_true", help="逐 run 列出未通过项")
    ap.add_argument("--out", default="", help="把校正后明细写成 json")
    args = ap.parse_args()

    with open(args.result, encoding="utf-8") as f:
        report = json.load(f)

    tasks = {t.task_id: t for t in discover_tasks(os.path.join(_ROOT, "tasks"))}
    rows: List[dict] = []

    for entry in report.get("detailed", []):
        tid = entry["task"]
        if args.task and tid != args.task:
            continue
        task = tasks.get(tid)
        if task is None:
            continue
        for r in entry["runs"]:
            ans = r.get("answer") or ""
            orig = float(r.get("final_answer_score") or 0.0)
            d_raw = grade_of(task, ans)
            d_tex = grade_of(task, delatex(ans))
            d_sub = grade_of(task, drop_subscript(delatex(ans)))
            s_raw, s_tex = score_of(d_raw), score_of(d_tex)
            s_sub = score_of(d_sub)
            best = max(s_raw, s_tex, s_sub)
            best_detail = d_sub if s_sub >= max(s_raw, s_tex) else (
                d_tex if s_tex >= s_raw else d_raw)
            rows.append({
                "task": tid, "run": r.get("run_idx"),
                "orig": orig, "regraded": s_raw, "delatexed": s_tex,
                "no_subscript": s_sub,
                "corrected": best, "empty_answer": not ans.strip(),
                "sig_bug": "grade_error" in d_raw and "positional argument" in str(d_raw),
                "still_failing": failed_checks(best_detail),
            })

    # 按题汇总
    by_task: Dict[str, List[dict]] = {}
    for row in rows:
        by_task.setdefault(row["task"], []).append(row)

    print(f"{'题目':<16}{'原始均值':>9}{'校正均值':>10}{'Δ':>8}   说明")
    print("-" * 78)
    for tid, rs in by_task.items():
        o = sum(x["orig"] for x in rs) / len(rs)
        c = sum(x["corrected"] for x in rs) / len(rs)
        notes = []
        if any(x["sig_bug"] for x in rs):
            notes.append("签名bug全题归零")
        n_tex = sum(1 for x in rs if x["delatexed"] > x["regraded"])
        if n_tex:
            notes.append(f"LaTeX假阴性{n_tex}/{len(rs)}")
        n_sub = sum(1 for x in rs
                    if x["no_subscript"] > max(x["delatexed"], x["regraded"]))
        if n_sub:
            notes.append(f"下标假阴性{n_sub}/{len(rs)}")
        n_empty = sum(1 for x in rs if x["empty_answer"])
        if n_empty:
            notes.append(f"空答复{n_empty}")
        mark = "  ←" if abs(c - o) > 1e-6 else ""
        print(f"{tid:<16}{o:>9.3f}{c:>10.3f}{c - o:>+8.3f}   {'; '.join(notes)}{mark}")
        if args.verbose:
            for x in rs:
                print(f"    run{x['run']}  {x['orig']:.3f} → {x['corrected']:.3f}"
                      f"   未过: {', '.join(x['still_failing']) or '（全过）'}")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        print(f"\n明细已写入 {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
