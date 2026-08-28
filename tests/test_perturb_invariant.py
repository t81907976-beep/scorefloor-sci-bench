#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
假阳性探针的**不变量**测试：扰动算子只许改结论数值，不许改别的。

为什么这条护栏必须存在：探针的全部说服力建立在「文字、单位、格式一个字不改」
之上。一旦算子顺手改了单位串或化学式，`has_unit` / `has_order` 这类判据的
下降就是探针自己造的，而不是真的白拿分——地板会被系统性**高估**，结论反向失真。
这类失真不报错、不崩溃，只是安静地给出一个更"好看"的数字，必须靠断言锁住。

「含整数」档是这条护栏的主要客户：裸的 `-?\d+(?:\.\d+)?` 会把
`A\,m^{-2}` 改成 `A\,m^{-14}`、把 `N(OH)_2` 改成 `N(OH)_26`
（实测 100 份答复里 73 份被破坏）。加保护后降到 0/100。

用法：
    python3 tests/test_perturb_invariant.py
    python3 -m pytest tests/ -q
"""

from __future__ import annotations

import json
import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)

from scripts.audit_false_positive import (  # noqa: E402
    perturb_numbers, perturb_scramble,
)

_FIXTURE = os.path.join(_ROOT, "tests", "fixtures",
                        "regression-20260804.json")

# 不变量：这些片段扰动前后必须逐个一字不差
_UNIT_BLOCK = re.compile(r"\\(?:mathrm|text|mathbf|operatorname)\s*\{"
                         r"[^{}]*(?:\{[^{}]*\}[^{}]*)*\}")
# 科学计数法底数：`×10^` / `\times 10^` 的出现次数不许变（底数被改会留下裸数字伪造命中）
_SCI_BASE = re.compile(r"(?:\\times|×|\*)\s*10\s*\^")
# 下标数字：`_2`、`_{3}` 是符号身份（化学式配比、能级编号），不是结论值
_SUBSCRIPT = re.compile(r"_\s*\{?\s*\d+")


def _answers():
    with open(_FIXTURE, encoding="utf-8") as f:
        return [(c["task"], c["run"], c["answer"]) for c in json.load(f)["cases"]]


def _check(fn, label, verbose=False):
    bad = []
    answers = _answers()
    for task, run, text in answers:
        out = fn(text)
        if _UNIT_BLOCK.findall(text) != _UNIT_BLOCK.findall(out):
            bad.append((task, run, "单位串/化学式被改"))
        elif len(_SCI_BASE.findall(text)) != len(_SCI_BASE.findall(out)):
            bad.append((task, run, "科学计数法底数被改"))
        elif _SUBSCRIPT.findall(text) != _SUBSCRIPT.findall(out):
            bad.append((task, run, "下标被改"))
    if verbose:
        print(f"  [{label}] {len(answers) - len(bad)}/{len(answers)} 通过")
    assert not bad, f"{label} 破坏了非数值内容：" + "; ".join(
        f"{t} run{r}（{why}）" for t, r, why in bad[:6])


def test_decimal_operator_preserves_form(verbose=False):
    """仅小数档：只吃带小数点的数，天然不碰单位与下标。"""
    _check(lambda s: perturb_scramble(s), "仅小数档", verbose)


def test_integer_operator_preserves_form(verbose=False):
    """含整数档：必须靠 _PROTECT 保住单位串、科学计数法底数与下标。"""
    _check(lambda s: perturb_scramble(s, integers=True), "含整数档", verbose)


def test_factor_operator_preserves_form(verbose=False):
    """等比缩放档（--factor）同样只动小数。"""
    _check(lambda s: perturb_numbers(s, 3.0), "等比缩放档", verbose)


def test_answers_actually_change(verbose=False):
    """反向断言：算子必须**真的**改动了数值，否则地板测的是原文、恒等于真实分。"""
    unchanged = [(t, r) for t, r, s in _answers()
                 if perturb_scramble(s, integers=True) == s]
    if verbose:
        print(f"  [算子有效] {len(_answers()) - len(unchanged)}/{len(_answers())} 通过")
    assert not unchanged, "这些答复扰动后与原文完全相同：" + "; ".join(
        f"{t} run{r}" for t, r in unchanged[:6])


def main() -> int:
    print("假阳性探针不变量测试（100 份真实答复）")
    failures = []
    for fn in (test_decimal_operator_preserves_form,
               test_integer_operator_preserves_form,
               test_factor_operator_preserves_form,
               test_answers_actually_change):
        try:
            fn(verbose=True)
        except AssertionError as exc:
            failures.append(f"{fn.__name__}: {exc}")
    if failures:
        print("\n✗ FAILED")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\n✓ 全部通过：扰动算子只动结论数值")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
