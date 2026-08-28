#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人工校正取证：把某题某 run 的答复尾部、原始/去壳后各 check 明细并排打出来，
用于确认「去壳后变绿」的项确实是表现形式问题、而不是判分被放水。

用法：
    python3 scripts/evidence.py <结果json> test-化学01 [--run 1] [--tail 900]
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.task_loader import discover_tasks            # noqa: E402
from scripts.recheck_scores import delatex, grade_of  # noqa: E402

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    ap = argparse.ArgumentParser(description="人工校正取证")
    ap.add_argument("result")
    ap.add_argument("task")
    ap.add_argument("--run", type=int, default=0, help="0=全部 run")
    ap.add_argument("--tail", type=int, default=900, help="答复尾部字符数")
    args = ap.parse_args()

    with open(args.result, encoding="utf-8") as f:
        report = json.load(f)
    task = {t.task_id: t for t in discover_tasks(os.path.join(_ROOT, "tasks"))}[args.task]

    for entry in report.get("detailed", []):
        if entry["task"] != args.task:
            continue
        for r in entry["runs"]:
            if args.run and r.get("run_idx") != args.run:
                continue
            ans = r.get("answer") or ""
            d_raw, d_tex = grade_of(task, ans), grade_of(task, delatex(ans))
            print("=" * 96)
            print(f"{args.task} run {r.get('run_idx')}   落盘分={r.get('final_answer_score')}")
            print("-" * 96)
            keys = [k for k in dict(d_raw, **d_tex) if k != "auto_final_answer_score"]
            for k in keys:
                a, b = d_raw.get(k), d_tex.get(k)
                flag = "  ← 去壳后转正" if a is False and b is True else ""
                print(f"  {k:<40} 原始={str(a):<7} 去壳={str(b):<7}{flag}")
            print(f"  {'auto_final_answer_score':<40} "
                  f"原始={d_raw.get('auto_final_answer_score')} "
                  f"去壳={d_tex.get('auto_final_answer_score')}")
            print("-" * 96)
            print("答复尾部原文：")
            print(ans[-args.tail:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
