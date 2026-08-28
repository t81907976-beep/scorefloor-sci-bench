#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
刷新判分回归集的 expected_score。

用途：判分逻辑**有意**改动后，tests/test_grading_regression.py 的断言 4
（逐 run 一致）会红。先确认断言 1–3（复现人工校正 / 真错维持 / 单调不减）仍绿，
再跑本脚本把 expected_score 更新到新判分器的产出。

⚠️ 不要在断言 1–3 红的时候跑这个——那说明判分器改坏了，不是 fixture 过期。
本脚本只动 expected_score，不动 manual_corrected / original_auto / true_error_task
这三个权威字段（它们是 0804 人工复核的事实，只能人工修）。

用法：
    python3 scripts/refresh_regression.py            # 预览差异，不写盘
    python3 scripts/refresh_regression.py --write    # 确认后写入
"""

from __future__ import annotations

import argparse
import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)

from lib.task_loader import discover_tasks  # noqa: E402

_FIXTURE = os.path.join(_ROOT, "tests", "fixtures",
                        "regression-20260804.json")


def main() -> int:
    ap = argparse.ArgumentParser(description="刷新回归集 expected_score")
    ap.add_argument("--write", action="store_true", help="确认写盘（默认只预览）")
    ap.add_argument("--fixture", default=_FIXTURE)
    args = ap.parse_args()

    with open(args.fixture, encoding="utf-8") as f:
        fx = json.load(f)
    tasks = {t.task_id: t for t in discover_tasks(os.path.join(_ROOT, "tasks"))}

    changed = []
    for case in fx["cases"]:
        task = tasks.get(case["task"])
        if task is None or task.grade_fn is None:
            continue
        detail = task.grade_fn(
            [{"role": "assistant", "content": case["answer"]}],
            _ROOT, {"task_id": case["task"]},
        ) or {}
        new = float(detail.get("auto_final_answer_score") or 0.0)
        old = case["expected_score"]
        if abs(new - old) > 1e-9:
            changed.append((case["task"], case["run"], old, new,
                            case.get("manual_corrected"),
                            detail.get("_grade_variant")))
        case["expected_score"] = new
        case["variant"] = detail.get("_grade_variant")

    if not changed:
        print("无变化，fixture 已是最新。")
        return 0

    print(f"{len(changed)} 个 run 的分数变化：")
    print(f"{'题目':<14}{'run':>4}{'旧':>8}{'新':>8}{'Δ':>8}  档位  人工校正值")
    for tid, run, old, new, man, var in changed:
        mark = "  ⚠ 该 run 有人工校正权威值，改动需重新复核" if man is not None else ""
        print(f"{tid:<14}{run:>4}{old:>8.3f}{new:>8.3f}{new - old:>+8.3f}  "
              f"{var}{mark}")

    if not args.write:
        print("\n预览模式，未写盘。确认无误后加 --write。")
        return 0
    with open(args.fixture, "w", encoding="utf-8") as f:
        json.dump(fx, f, ensure_ascii=False, indent=1)
    print(f"\n已写入 {args.fixture}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
