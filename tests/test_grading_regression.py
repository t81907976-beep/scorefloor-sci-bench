#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
判分器回归测试：拿 0804 那 100 个 run 当回归集，断言判分器**不做任何人工校正**
就能直接复现当日人工校正后的分。

这是「判分可以全自动出分、人工校正降级为抽查」的验收条件。三类断言：

  1. 复现人工校正（22 个 run / 7 题）：判分器自动分必须等于当日人工校正权威值。
  2. 真错必须维持（化学05/09/10）：复核确认真实错误的题，分数不得高于原始自动分——
     容错层只放宽表现形式，绝不能把答错的救活（假阳性防线）。
  3. 单调不减：任何 run 的新自动分不得低于 0804 的原始自动分。容错层三档取最优、
     原文档位始终参评，所以任何倒退都说明归一化把原本能匹配的文本改坏了。

用法：
    python3 tests/test_grading_regression.py          # 全部
    python3 tests/test_grading_regression.py -v       # 逐 run 打印
    python3 -m pytest tests/                          # 若装了 pytest
"""

from __future__ import annotations

import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)

from lib.task_loader import discover_tasks  # noqa: E402

_FIXTURE = os.path.join(_ROOT, "tests", "fixtures",
                        "regression-20260804.json")
_TOL = 1e-6


def _load():
    with open(_FIXTURE, encoding="utf-8") as f:
        return json.load(f)


def _grade_all():
    """对回归集每个 run 重跑判分，返回 [(case, 实际分, 明细)]。"""
    tasks = {t.task_id: t for t in discover_tasks(os.path.join(_ROOT, "tasks"))}
    out = []
    for case in _load()["cases"]:
        task = tasks.get(case["task"])
        if task is None or task.grade_fn is None:
            continue
        detail = task.grade_fn(
            [{"role": "assistant", "content": case["answer"]}],
            _ROOT, {"task_id": case["task"]},
        ) or {}
        out.append((case, float(detail.get("auto_final_answer_score") or 0.0), detail))
    return out


def test_reproduces_manual_correction(graded=None, verbose=False):
    """断言 1：判分器自动分 == 当日人工校正权威值。"""
    bad = []
    n = 0
    for case, actual, _ in (graded or _grade_all()):
        man = case.get("manual_corrected")
        if man is None:
            continue
        n += 1
        if abs(actual - float(man)) > _TOL:
            bad.append((case["task"], case["run"], man, actual))
    if verbose:
        print(f"  [1] 复现人工校正：{n - len(bad)}/{n} 通过")
    assert not bad, "自动分未复现人工校正值：" + "; ".join(
        f"{t} run{r} 期望 {m} 实得 {a}" for t, r, m, a in bad)


def test_true_errors_stay_wrong(graded=None, verbose=False):
    """断言 2：复核确认真错的题不得因容错层涨分（假阳性防线）。"""
    bad = []
    n = 0
    for case, actual, _ in (graded or _grade_all()):
        if not case.get("true_error_task"):
            continue
        n += 1
        if actual > case["original_auto"] + _TOL:
            bad.append((case["task"], case["run"], case["original_auto"], actual))
    if verbose:
        print(f"  [2] 真错维持：{n - len(bad)}/{n} 通过")
    assert not bad, "真错题被容错层放行（疑似假阳性）：" + "; ".join(
        f"{t} run{r} 原 {o} → 现 {a}" for t, r, o, a in bad)


def test_monotonic_no_regression(graded=None, verbose=False):
    """断言 3：任何 run 的分不得低于 0804 原始自动分。

    豁免：带 `monotonic_exempt` 的 run 跳过。这个字段只在**已证实 0804 那次
    原始自动分本身是假阳性**时才允许加，且必须同时写 `monotonic_exempt_reason`
    说明假阳性的机制——否则它就成了"分数掉了就开豁免"的后门，把这道闸废掉。
    原始分保留不改（历史事实），只豁免断言，这样假阳性曾经存在这件事还查得到。
    """
    bad = []
    exempt = 0
    graded = graded or _grade_all()
    for case, actual, _ in graded:
        if case.get("monotonic_exempt"):
            exempt += 1
            continue
        if actual < case["original_auto"] - _TOL:
            bad.append((case["task"], case["run"], case["original_auto"], actual))
    if verbose:
        tail = f"（豁免 {exempt}）" if exempt else ""
        print(f"  [3] 单调不减：{len(graded) - len(bad) - exempt}/"
              f"{len(graded) - exempt} 通过{tail}")
    assert not bad, "分数出现倒退（归一化改坏了原本能匹配的文本）：" + "; ".join(
        f"{t} run{r} 原 {o} → 现 {a}" for t, r, o, a in bad)


def test_fixture_matches_expected(graded=None, verbose=False):
    """断言 4：判分器产出与 fixture 记录的 expected_score 逐 run 一致。

    前三条锁的是「该对的对、该错的错」，这条锁的是「一个字都不许漂」——
    任何判分逻辑改动只要动了任一 run 的分，这里就会红，迫使改动者显式更新 fixture。
    """
    bad = []
    graded = graded or _grade_all()
    for case, actual, _ in graded:
        if abs(actual - case["expected_score"]) > _TOL:
            bad.append((case["task"], case["run"], case["expected_score"], actual))
    if verbose:
        print(f"  [4] 与 fixture 一致：{len(graded) - len(bad)}/{len(graded)} 通过")
    assert not bad, (
        f"{len(bad)} 个 run 与 fixture 不一致（若为有意改动，"
        f"用 scripts/refresh_regression.py 更新）：" + "; ".join(
            f"{t} run{r} 期望 {e} 实得 {a}" for t, r, e, a in bad[:8]))


def main() -> int:
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    graded = _grade_all()
    print(f"回归集 {len(graded)} run（{_FIXTURE.split('/')[-1]}）")
    failures = []
    for fn in (test_reproduces_manual_correction, test_true_errors_stay_wrong,
               test_monotonic_no_regression, test_fixture_matches_expected):
        try:
            fn(graded, verbose=True)
        except AssertionError as exc:
            failures.append(f"{fn.__name__}: {exc}")
    if verbose:
        variants = {}
        for case, _, detail in graded:
            variants[detail.get("_grade_variant")] = \
                variants.get(detail.get("_grade_variant"), 0) + 1
        print(f"  命中档位分布：{variants}")
    if failures:
        print("\n✗ FAILED")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\n✓ 全部通过：判分器无需人工校正即可复现权威分")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
