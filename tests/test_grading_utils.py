#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lib/grading_utils.normalize() 的单元测试。

分两类：
  - 能力用例：0804 那批真实假阴性的最小复现，断言归一化后能被裸算式正则命中。
  - 不变量用例：归一化**只动表现形式**。断言归一前后「数字序列」与「希腊字母集合」
    完全一致——这是防止容错层悄悄改动数值、把假阴性治成假阳性的护栏。

用法：
    python3 tests/test_grading_utils.py
    python3 -m pytest tests/ -q
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.grading_utils import drop_subscript, normalize  # noqa: E402

# (输入, 归一化后必须命中的正则, 说明) —— 均取自 0804 真实假阴性
_CAPABILITY = [
    (r"\[\boxed{\sigma_{\rm el}\approx 2.60\times10^{-13}\ \mathrm{m^{2}}}\]",
     r"σ_el\s*≈\s*2\.60e-13\s*m\^2", "物理03：\\sigma→σ + \\boxed + \\times10 + 硬空格"),
    (r"\(\delta_1 \approx 0.35\)",
     r"δ_1\s*≈\s*0\.35", "物理07：δ 相移在行内公式里"),
    (r"j = -1.25\ \mathrm{A\,m^{-2}}",
     r"j\s*=\s*-1\.25\s*A\s*m\^-2", "化学03：单位埋在 \\mathrm 壳里 + 硬空格"),
    (r"\[k_0 \approx 3.2\times 10^{-8}\ \text{cm s}^{-1}\]",
     r"cm\s*s\^-1", "化学01：\\text{} 单位壳"),
    (r"C_0 = 3.00\times\frac{50.00}{10.00}=15.0\ \mathrm{mg·L^{-1}}",
     r"15\.0\s*mgL\^-1", "化学04：\\frac + \\mathrm + 中点符"),
    (r"V=182.5\ {\rm \AA^3}",
     r"V=182\.5\s*Å\^3", "物理10：{\\rm \\AA} 花括号字体壳"),
    (r"\delta^{18}O_0 \approx -5.0\permil",
     r"-5\.0‰", "化学07：\\permil 单位命令须保成 ‰ 而非被删"),
    (r"x^{2n+1}", r"x\^2n\+1", "上标花括号拆壳不吞内容"),
    (r"\sigma_{tot}=1.5", r"σ_tot=1\.5", "下标花括号内容紧贴、不留空格"),
]

_NUM = re.compile(r"-?\d+(?:\.\d+)?")
_GREEK_CHARS = re.compile(r"[Ͱ-Ͽ]")

# 不变量用例：真实答复片段
_INVARIANT = [
    r"\[\boxed{j\approx -1.25\ \mathrm{A\,m^{-2}}}\]",
    r"\sigma_{\rm el}\approx 2.6\times10^{7}\ \AA^2\approx 2.6\times10^{-13}\ \mathrm{m^2}",
    r"\delta D_0\approx -30.0\permil,\qquad \lambda \simeq 0.50",
    r"k_0 = 8.5\times10^{-5}\ \mathrm{cm\,s^{-1}}\quad(\text{ECSA 基准})",
    r"\frac{\partial j}{\partial E}=F k^0 f\left[\alpha_a c_R e^{\alpha_a f\xi}\right]",
]


def test_capability(verbose: bool = False) -> list:
    """归一化后应能被题库那种裸算式正则命中。"""
    bad = []
    for src, pat, why in _CAPABILITY:
        out = normalize(src)
        if not re.search(pat, out):
            bad.append(f"{why}\n      输入 {src!r}\n      归一 {out!r}\n      期望 /{pat}/")
    if verbose:
        print(f"  [能力] {len(_CAPABILITY) - len(bad)}/{len(_CAPABILITY)} 通过")
    return bad


def test_numbers_preserved(verbose: bool = False) -> list:
    """不变量：数字序列不变。

    唯一允许的变形是 `a×10^b` → `ae b` 科学计数法折叠，此时 10 与指数会合进
    e 记法。故比对时把两侧都做同样折叠后再取数字序列。
    """
    bad = []
    for src in _INVARIANT:
        before = _NUM.findall(re.sub(
            r"([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*(?:\\times|[×x*])\s*10\s*\^?\{?\s*([+-]?\d+)\}?",
            r"\1e\2", src))
        after = _NUM.findall(normalize(src))
        if before != after:
            bad.append(f"数字序列变了\n      输入 {src!r}\n"
                       f"      前 {before}\n      后 {after}")
    if verbose:
        print(f"  [不变量·数字] {len(_INVARIANT) - len(bad)}/{len(_INVARIANT)} 通过")
    return bad


def test_greek_not_lost(verbose: bool = False) -> list:
    """不变量：希腊字母只会变多（命令→unicode），绝不会变少。"""
    bad = []
    for src in _INVARIANT:
        before = set(_GREEK_CHARS.findall(src))
        after = set(_GREEK_CHARS.findall(normalize(src)))
        if not before <= after:
            bad.append(f"希腊字母丢失 {before - after}\n      输入 {src!r}")
    if verbose:
        print(f"  [不变量·希腊字母] {len(_INVARIANT) - len(bad)}/{len(_INVARIANT)} 通过")
    return bad


def test_idempotent(verbose: bool = False) -> list:
    """归一化应幂等：normalize(normalize(x)) == normalize(x)。

    不幂等意味着拆壳没跑到不动点，多档取最优就会依赖调用次数、结果不可复现。
    """
    bad = []
    for src in _INVARIANT + [c[0] for c in _CAPABILITY]:
        once = normalize(src)
        if normalize(once) != once:
            bad.append(f"不幂等\n      一次 {once!r}\n      两次 {normalize(once)!r}")
    if verbose:
        n = len(_INVARIANT) + len(_CAPABILITY)
        print(f"  [幂等] {n - len(bad)}/{n} 通过")
    return bad


def test_drop_subscript(verbose: bool = False) -> list:
    """drop_subscript 只去字母/希腊字母后紧跟的下标下划线。"""
    cases = [("k_0", "k0"), ("σ_tot", "σtot"), ("δ_1", "δ1"),
             ("c_{Ox}", "c_{Ox}"), ("_leading", "_leading"), ("2_5", "2_5")]
    bad = [f"drop_subscript({s!r}) → {drop_subscript(s)!r}，期望 {e!r}"
           for s, e in cases if drop_subscript(s) != e]
    if verbose:
        print(f"  [drop_subscript] {len(cases) - len(bad)}/{len(cases)} 通过")
    return bad


def main() -> int:
    print("lib/grading_utils.normalize() 单元测试")
    failures = []
    for fn in (test_capability, test_numbers_preserved, test_greek_not_lost,
               test_idempotent, test_drop_subscript):
        for msg in fn(verbose=True):
            failures.append(f"{fn.__name__}: {msg}")
    if failures:
        print("\n✗ FAILED")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\n✓ 全部通过")
    return 0


# pytest 入口：把返回列表转成 assert
def test_all():
    for fn in (test_capability, test_numbers_preserved, test_greek_not_lost,
               test_idempotent, test_drop_subscript):
        bad = fn()
        assert not bad, f"{fn.__name__}: " + "; ".join(bad)


if __name__ == "__main__":
    raise SystemExit(main())
