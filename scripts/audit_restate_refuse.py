#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四算子：复述题面 + 拒答。

前三个算子（数值扰动、翻符号、结论标签替换）都需要一份**真实答复**做底本，
所以它们测的是「答复里有多少分与答案对错无关」。这一条不需要底本：

    输入 = 题面原文 + 一句「很抱歉，我无法给出可靠的答案」

这份输入**没有回答任何东西**，理想得分是 0.000。它拿到的任何分都直接暴露两类病：

  ① 存在性判据（`non_empty_answer` / `not_refusal`）—— 拒答文本照样够长、
     照样不含判据认得的拒答词根；
  ② 题面自带常数被当成数值锚 —— 复述题面即命中。第二类是这个算子独有的
     发现能力：数值扰动会把题面里的常数一起扰掉，所以它看不见「锚取自题面」
     这个错误；而复述题面把题给常数一字不改地送进判据。

化学题 0812 实测：10/10 题 0.000。物理题 10/10 题非零（0.06~0.55），
病因是 `non_empty_answer`/`not_refusal`（十题全带）+ `has_unit`（物理04/05/06/07）
+ 五条纯文字结论判据（物理02/03/06/07/08）。

用法：
    python3 scripts/audit_restate_refuse.py
    python3 scripts/audit_restate_refuse.py --task test-化学05
    python3 scripts/audit_restate_refuse.py --subject chemistry
"""

from __future__ import annotations

import argparse
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)

from lib.task_loader import discover_tasks  # noqa: E402

# 拒答句刻意写得「软」：不含「不会」「不知道」这类最容易被 not_refusal 收进
# 黑名单的词根，模拟真实模型给不出答案时的托词。这正是 not_trap_* 方向错位
# 的镜像 —— 软托词比老实拒答更难被判据识别。
_REFUSAL = "\n\n很抱歉，这道题的建模过于复杂，我无法给出可靠的答案。"


def main() -> int:
    ap = argparse.ArgumentParser(description="第四算子：复述题面 + 拒答")
    ap.add_argument("--task", default="", help="只看这道题")
    ap.add_argument("--subject", default="", help="只看这个学科目录（chemistry/physics）")
    args = ap.parse_args()

    rows = []
    for task in discover_tasks(os.path.join(_ROOT, "tasks")):
        if task.grade_fn is None:
            continue
        if args.task and task.task_id != args.task:
            continue
        if args.subject and args.subject not in (task.path or ""):
            continue
        detail = task.grade_fn(
            [{"role": "assistant", "content": task.query + _REFUSAL}],
            _ROOT, {"task_id": task.task_id}) or {}
        score = float(detail.get("auto_final_answer_score") or 0)
        hits = [k for k, v in detail.items()
                if not k.startswith("_") and k != "auto_final_answer_score"
                and isinstance(v, (int, float, bool)) and float(v) == 1.0]
        rows.append((task.task_id, score, hits))

    if not rows:
        print("无可审计的题。")
        return 1

    print("第四算子：复述题面 + 拒答（理想得分 0.000）\n")
    print(f"{'题目':<14}{'得分':>7}   命中项")
    print("-" * 78)
    for tid, score, hits in sorted(rows, key=lambda x: -x[1]):
        print(f"{tid:<14}{score:>7.3f}   {', '.join(hits) if hits else '—'}")
    print("-" * 78)

    for label, key in (("化学", "化学"), ("物理", "物理")):
        sub = [r for r in rows if key in r[0]]
        if not sub:
            continue
        nonzero = sum(1 for r in sub if r[1] > 0)
        print(f"{label} {len(sub)} 题：平均 {sum(r[1] for r in sub) / len(sub):.3f}，"
              f"非零 {nonzero}/{len(sub)} 题")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
