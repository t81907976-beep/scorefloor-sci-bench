#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
假阳性审计：量化「答案全错但仍然拿到的分」。

方法：把答复里所有小数乘 3（数值全部作废、文字与格式完全不动），重新判分。
理想判分器应该给接近 0；实际拿到的分就是**假阳性地板**——靠写对格式、
提到关键词、单位正确白拿的分，与答案对错无关。

为什么这件事和假阴性同等重要：归一化容错是单调涨分的，它能救回假阴性，
但同样会把「答错却被宽正则蒙对」的分一起放大。地板越高，榜单越测不出模型能力。

局限：数值扰动只对「答案是数值」的题有意义。构型判定这类非数值答案的题
（化学05）在 SKIP 里排除，需要另设扰动算子（换构型标签），暂未实现。

用法：
    python3 scripts/audit_false_positive.py                      # 用默认回归集
    python3 scripts/audit_false_positive.py --verbose             # 逐 check 列出白拿项
    python3 scripts/audit_false_positive.py --task test-物理04
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)

from lib.task_loader import discover_tasks  # noqa: E402

_FIXTURE = os.path.join(_ROOT, "tests", "fixtures",
                        "regression-20260804.json")

# 答案本身非数值的题：数值扰动不构成「答错」，排除以免误报
_NON_NUMERIC = {"test-化学05"}

_DECIMAL = re.compile(r"-?\d+\.\d+")

# 「含整数」档的数值正则：小数 + 整数都吃。
# 为什么需要它：只扰动小数的话，**凡是用整数写结论的题，答案根本没被作废**，
# 地板被系统性低估。实测物理10 地板 0.580 → 0.360。
# 但它不是无脑更好——扰动整数会在别处造出伪命中（物理05 从 0.440 涨到 0.700），
# 所以默认关，且必须配合 --per-check 逐 check 定，不能一刀切当成新基线。
#
# ⚠️ 0806 更正：早先这里写过「化学03 地板 0.857 → 0.515」，那个数是错的。
# 化学03 在仅小数 / ≥2 位小数 / 裸整数 / 带保护整数四档下真实值分别是
# 0.857 / 0.857 / 0.600 / 0.857——**带保护后压不下去**，0.515 复现不出来
# （最接近的是裸整数档的 0.600，且那 0.257 全是 `_PROTECT` 拦掉的自伤）。
# 化学题从未出现过 0.515，此数系记录串档，不要再引用。
_NUMBER = re.compile(r"-?\d+(?:\.\d+)?")

# 扰动整数时必须放过的位置。命中这些的整数一律原样保留：
#   - 科学计数法的底数 10 与指数：`1.92×10^2` 若把 10 改掉，留下的裸 2 会伪造
#     「结论 = 2」的命中（化学题记录过的坑，在仅小数档不可能发生，含整数档会）。
#     ⚠️ 指数支要带 `(?!\.\d)`：`e^{-1.772}` 这种**指数本身是结论小数**的写法，
#     少了它整数部分 `-1` 进保护区、`_NUMBER` 从这个 `1` 起匹配的 `1.772` 整条留下，
#     于是原文别处的数被扰动成 `1.772`（0.886×2）时，判据反而"命中"了一个
#     并非原文结论的值。0813 化学15 `derived_intermediate` 的伪命中就是它。
#   - LaTeX 结构里的数字：`\frac{1}{2}`、`(2l+1)`、`P_0(0)`、`10^{-13}` 的花括号内容
#     ——这些是公式骨架不是结论值，改了只制造噪声。⚠️ 分子分母两支都要带 `(?=\})`：
#     少了它，`\frac{0.6837}{…}` 的整数部分 `0` 会被划进保护区，`_NUMBER` 从这个 `0`
#     起匹配到的整个小数 `0.6837` 就整条原样留下——结论值在含整数档下**没被作废**，
#     反而伪造出「答错还命中」。0813 化学14 的 `derived_intermediate` +3x 伪命中就是它。
#   - `\mathrm{...}` / `\text{...}` 内的数字：那里面装的是**单位与化学式**，
#     不是结论数值。不保护会把 `A\,m^{-2}` 改成 `A\,m^{-14}`（单位串被改 → 探针
#     不再是「只动数值」，has_unit 类判据的下降是探针自己造的，不是真白拿），
#     以及把 `N(OH)_2` 改成 `N(OH)_26`（化学物种身份被改 → 化学09 的沉淀顺序
#     结论整段失效）。实测这一条把不变量违反率从 73/100 降到 0/100。
#   - 下标数字：`_2`、`_{3}` 同理，是符号身份不是结论值
_PROTECT = (
    re.compile(r"(?<![\d.])10(?=\s*\^|\s*\*\*|\s*\{)"),        # 科学计数法底数
    re.compile(r"(?<=\^)\s*\{?\s*[-+]?\d+(?!\.\d)"),            # 指数
    re.compile(r"(?<=[eE])[-+]?\d+(?![\d.])"),                  # e 记号指数
    re.compile(r"(?<=\\frac\{)\d+(?=\})|(?<=\}\{)\d+(?=\})"),   # \frac 分子分母
    re.compile(r"\d+(?=\s*l\s*\+\s*1)"),                        # (2l+1) 类简并因子
    re.compile(r"\\(?:mathrm|text|mathbf|operatorname)\s*\{"
               r"[^{}]*(?:\{[^{}]*\}[^{}]*)*\}"),                # 单位串与化学式整体
    re.compile(r"_\s*\{?\s*[-+]?\d+"),                          # 下标
)

# 逐个数值轮换的扰动因子。等比缩放（全体 ×3）是**保序保比**的：它证伪不了
# 「A>B」「A/B≈5e-6」这类由数值自身算出来的判据，那些项会假性地留在地板里。
# 用互不相同的因子轮换才能同时打断大小序与比值。
_SCRAMBLE = (2.0, 7.0, 0.31, 13.0, 0.077, 3.0, 41.0, 0.19)


def _protected_spans(text: str) -> list:
    """返回不许扰动的字符区间（科学计数法底数/指数、LaTeX 公式骨架）。"""
    spans = []
    for pat in _PROTECT:
        spans.extend((m.start(), m.end()) for m in pat.finditer(text))
    return spans


def _in_spans(pos: int, spans: list) -> bool:
    return any(a <= pos < b for a, b in spans)


def perturb_numbers(text: str, factor: float = 3.0) -> str:
    """把所有小数乘 factor。只动数值，文字/单位/格式一律不动。"""
    def bump(m):
        try:
            return f"{float(m.group(0)) * factor:.6g}"
        except ValueError:
            return m.group(0)
    return _DECIMAL.sub(bump, text)


def perturb_scramble(text: str, flip_sign: bool = False,
                     integers: bool = False) -> str:
    """逐个数值乘不同因子：打断大小序与比值，比等比缩放更彻底地作废答案。

    flip_sign=True 时因子额外取负。**任何正因子扰动都保号**，于是
    `sign_cathodic_negative`（判 j<0）这类纯符号判据、以及
    `branch_consistent`（说「积累」⟺ 自报 u>0）这类靠符号成立的自洽判据，
    对乘因子完全免疫、会假性地留在地板里。翻符号是压掉它们的唯一办法。

    翻符号**默认关**：它同时会把「符号本来就该为负」的正确答案改成正号，
    对不判符号的题属于无意义噪声。要单独量化符号类项的贡献时才开。

    integers=True 时连整数一起扰动（`_NUMBER` 档），但跳过 `_PROTECT` 保护区。
    默认关，见 `_NUMBER` 的注释：它修掉一批低估、又造出一批伪命中。
    """
    counter = [0]
    spans = _protected_spans(text) if integers else []

    def bump(m):
        if integers and _in_spans(m.start(), spans):
            return m.group(0)
        try:
            v = float(m.group(0)) * _SCRAMBLE[counter[0] % len(_SCRAMBLE)]
        except ValueError:
            return m.group(0)
        finally:
            counter[0] += 1
        return f"{-v if flip_sign else v:.6g}"
    return (_NUMBER if integers else _DECIMAL).sub(bump, text)


def _mixed_report(cases, tasks, args) -> int:
    """按题定档的地板表：这是当前推荐口径。

    定档规则：一道题在「含整数」档下**不产生任何新伪命中**（没有哪个 check
    从仅小数档的「不命中」翻成命中）就采用含整数档的地板，否则保守退回仅小数档。

    为什么按题而不按 check 定：地板是题级聚合量，一道题里只要有一个 check 在
    含整数档下变噪声，该题的含整数地板就不可信；而 check 级混合会拼出
    「题目从未实际产生过的分数组合」，与 `_robust_grade` 不逐 check 挑最优是同一个道理。
    """
    real = collections.defaultdict(list)
    f_dec = collections.defaultdict(list)
    f_int = collections.defaultdict(list)
    new_fp = collections.Counter()

    for case in cases:
        tid = case["task"]
        if args.task and tid != args.task:
            continue
        if tid in _NON_NUMERIC:
            continue
        task = tasks.get(tid)
        if task is None or task.grade_fn is None:
            continue

        def grade(text):
            return task.grade_fn([{"role": "assistant", "content": text}],
                                 _ROOT, {"task_id": tid}) or {}

        d_real = grade(case["answer"])
        d_dec = grade(perturb_scramble(case["answer"], flip_sign=args.flip_sign))
        d_int = grade(perturb_scramble(case["answer"], flip_sign=args.flip_sign,
                                       integers=True))
        real[tid].append(float(d_real.get("auto_final_answer_score") or 0))
        f_dec[tid].append(float(d_dec.get("auto_final_answer_score") or 0))
        f_int[tid].append(float(d_int.get("auto_final_answer_score") or 0))

        for k, v in d_int.items():
            if k.startswith("_") or k == "auto_final_answer_score":
                continue
            if not isinstance(v, (int, float, bool)):
                continue
            # 新伪命中有两种，都要算：
            #   (a) 真实答复本来拿着这一项，含整数档压不掉而仅小数档压掉了 —— 白拿；
            #   (b) 真实答复**本来就没拿**这一项，含整数档反而把它点亮 —— 凭空造分，
            #       比 (a) 更坏。0813 化学15：某答复写的括号内小计 48.338 被 ×2.0 扰动成
            #       96.676，正好是标准解的 q_NO,ex，`no_joint_partition_function`
            #       在答案全错时被点亮 0.16。漏掉 (b) 会让该题误采含整数档地板。
            if float(v) != 1.0 or float(d_dec.get(k) or 0) == 1.0:
                continue
            new_fp[tid] += 1

    if not real:
        print("无可审计的 run。")
        return 1

    print("混合档假阳性地板（按题定档：含整数档无新伪命中则采用之）\n")
    print(f"{'题目':<14}{'真实分':>8}{'仅小数':>8}{'含整数':>8}{'定档':>8}{'采用地板':>9}  区分度")
    print("-" * 66)
    tot_r = tot_c = tot_d = tot_i = 0.0
    rows = []
    for tid in real:
        r = sum(real[tid]) / len(real[tid])
        d = sum(f_dec[tid]) / len(f_dec[tid])
        i = sum(f_int[tid]) / len(f_int[tid])
        use_int = new_fp[tid] == 0
        rows.append((tid, r, d, i, use_int, i if use_int else d))
    for tid, r, d, i, use_int, chosen in sorted(rows, key=lambda x: -x[5]):
        tot_r += r
        tot_c += chosen
        tot_d += d
        tot_i += i
        bar = "█" * int((r - chosen) * 20)
        print(f"{tid:<14}{r:>8.3f}{d:>8.3f}{i:>8.3f}"
              f"{'含整数' if use_int else '仅小数':>8}{chosen:>9.3f}  {bar}")
    n = len(rows)
    print("-" * 66)
    print(f"{'合计':<14}{tot_r / n:>8.3f}{tot_d / n:>8.3f}{tot_i / n:>8.3f}"
          f"{'混合':>8}{tot_c / n:>9.3f}")
    print(f"\n地板占比：仅小数 {tot_d / tot_r:.0%} ／ 含整数 {tot_i / tot_r:.0%} ／ "
          f"**混合 {tot_c / tot_r:.0%}**")
    print(f"真正区分答案对错的分 {(tot_r - tot_c) / n:.4f}／满分 1.0")
    print(f"退回仅小数档的题：{', '.join(t for t, *_ , u, _c in rows if not u) or '（无）'}")
    return 0


def _per_check_report(cases, tasks, args) -> int:
    """逐 check 对比「仅小数」与「含整数」两档的白拿次数。

    为什么必须逐 check 看、不能只看总分：「含整数」档在多数题上压低地板
    （答案真的被作废了），但在少数 check 上**造出新的伪命中**——把整数改掉后
    恰好落进另一个容差带，或让某个反向判据从「不成立」翻成「成立」。
    实测物理05 地板反而从 0.440 涨到 0.700。总分掩盖了方向相反的两类变化，
    只有逐 check 的差值能区分「修掉低估」与「造出噪声」。

    输出三段：新增伪命中（含整数档独有，需要保守用仅小数档）、
    修掉的低估（仅小数档独有，说明该 check 需要含整数档）、以及每题地板对照。
    """
    only_dec = collections.Counter()
    with_int = collections.Counter()
    floor_dec = collections.defaultdict(list)
    floor_int = collections.defaultdict(list)
    real = collections.defaultdict(list)

    for case in cases:
        tid = case["task"]
        if args.task and tid != args.task:
            continue
        if tid in _NON_NUMERIC:
            continue
        task = tasks.get(tid)
        if task is None or task.grade_fn is None:
            continue

        def grade(text):
            return task.grade_fn([{"role": "assistant", "content": text}],
                                 _ROOT, {"task_id": tid}) or {}

        d_real = grade(case["answer"])
        d_dec = grade(perturb_scramble(case["answer"], flip_sign=args.flip_sign))
        d_int = grade(perturb_scramble(case["answer"], flip_sign=args.flip_sign,
                                       integers=True))
        real[tid].append(float(d_real.get("auto_final_answer_score") or 0))
        floor_dec[tid].append(float(d_dec.get("auto_final_answer_score") or 0))
        floor_int[tid].append(float(d_int.get("auto_final_answer_score") or 0))

        for bucket, detail in ((only_dec, d_dec), (with_int, d_int)):
            for k, v in detail.items():
                if k.startswith("_") or k == "auto_final_answer_score":
                    continue
                if isinstance(v, bool):
                    hit, was = float(v), float(bool(d_real.get(k)))
                elif isinstance(v, (int, float)):
                    hit, was = float(v), float(d_real.get(k) or 0)
                else:
                    continue
                if hit == 1.0 and was == 1.0:
                    bucket[f"{tid}::{k}"] += 1

    if not real:
        print("无可审计的 run。")
        return 1

    print("逐 check 对照：扰动算子「仅小数」 vs 「含整数」\n")
    print("① 含整数档新造出的伪命中（该 check 应留在仅小数档）")
    worse = [(k, with_int[k] - only_dec[k]) for k in with_int
             if with_int[k] > only_dec[k]]
    for k, d in sorted(worse, key=lambda x: -x[1]):
        print(f"  +{d}x  {k}   （仅小数 {only_dec[k]}x → 含整数 {with_int[k]}x）")
    if not worse:
        print("  （无）")

    print("\n② 含整数档修掉的低估（该 check 需要含整数档才压得住）")
    better = [(k, only_dec[k] - with_int[k]) for k in only_dec
              if only_dec[k] > with_int[k]]
    for k, d in sorted(better, key=lambda x: -x[1]):
        print(f"  -{d}x  {k}   （仅小数 {only_dec[k]}x → 含整数 {with_int[k]}x）")
    if not better:
        print("  （无）")

    print(f"\n③ 每题地板对照\n{'题目':<14}{'真实分':>8}{'仅小数':>8}{'含整数':>8}{'差':>8}")
    print("-" * 50)
    tr = td = ti = 0.0
    for tid in sorted(real, key=lambda t: sum(floor_int[t]) / len(floor_int[t])
                      - sum(floor_dec[t]) / len(floor_dec[t])):
        r = sum(real[tid]) / len(real[tid])
        fd = sum(floor_dec[tid]) / len(floor_dec[tid])
        fi = sum(floor_int[tid]) / len(floor_int[tid])
        tr += r
        td += fd
        ti += fi
        flag = "  ⚠ 反涨" if fi > fd + 1e-9 else ""
        print(f"{tid:<14}{r:>8.3f}{fd:>8.3f}{fi:>8.3f}{fi - fd:>+8.3f}{flag}")
    n = len(real)
    print("-" * 50)
    print(f"{'合计':<14}{tr / n:>8.3f}{td / n:>8.3f}{ti / n:>8.3f}{(ti - td) / n:>+8.3f}")
    print(f"\n地板占比：仅小数 {td / tr:.0%}  →  含整数 {ti / tr:.0%}")
    print("⚠️ 「含整数」不是新基线：①里的 check 在该档下是噪声，需逐 check 定档。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="假阳性审计：量化答案全错时的白拿分")
    ap.add_argument("--fixture", default=_FIXTURE)
    ap.add_argument("--task", default="", help="只看这道题")
    ap.add_argument("--verbose", action="store_true", help="列出白拿的 check 项")
    ap.add_argument("--factor", type=float, default=3.0, help="数值扰动倍数")
    ap.add_argument("--scramble", action="store_true",
                    help="逐值乘不同因子（打断大小序与比值），而非全体等比放大")
    ap.add_argument("--flip-sign", action="store_true",
                    help="扰动时额外翻符号，压掉 sign_* 这类纯符号判据（隐含 --scramble）")
    ap.add_argument("--integers", action="store_true",
                    help="连整数一起扰动（保护科学计数法底数与 LaTeX 骨架）；"
                         "隐含 --scramble。默认只扰动小数")
    ap.add_argument("--per-check", action="store_true",
                    help="对比「仅小数」与「含整数」两档的逐 check 白拿次数，"
                         "找出含整数档造出的新伪命中（决定该 check 用哪档）")
    ap.add_argument("--mixed", action="store_true",
                    help="按题定档出地板表：该题在含整数档下不产生新伪命中就用含整数档，"
                         "否则保守退回仅小数档。这是当前推荐的地板口径")
    args = ap.parse_args()

    if args.flip_sign or args.integers:
        args.scramble = True

    def perturb(text: str) -> str:
        if args.scramble:
            return perturb_scramble(text, flip_sign=args.flip_sign,
                                    integers=args.integers)
        return perturb_numbers(text, args.factor)

    with open(args.fixture, encoding="utf-8") as f:
        cases = json.load(f)["cases"]
    tasks = {t.task_id: t for t in discover_tasks(os.path.join(_ROOT, "tasks"))}

    if args.per_check:
        return _per_check_report(cases, tasks, args)
    if args.mixed:
        return _mixed_report(cases, tasks, args)

    per = collections.defaultdict(lambda: {"real": [], "floor": []})
    free_checks = collections.Counter()
    skipped = set()

    for case in cases:
        tid = case["task"]
        if args.task and tid != args.task:
            continue
        if tid in _NON_NUMERIC:
            skipped.add(tid)
            continue
        task = tasks.get(tid)
        if task is None or task.grade_fn is None:
            continue

        def grade(text):
            return task.grade_fn([{"role": "assistant", "content": text}],
                                 _ROOT, {"task_id": tid}) or {}

        d_real = grade(case["answer"])
        d_fake = grade(perturb(case["answer"]))
        per[tid]["real"].append(float(d_real.get("auto_final_answer_score") or 0))
        per[tid]["floor"].append(float(d_fake.get("auto_final_answer_score") or 0))

        for k, v in d_fake.items():
            if k.startswith("_") or k == "auto_final_answer_score":
                continue
            # bool 必须收进来：化学题 grade() 的 check 项返回 True/False 而非 1.0/0.0，
            # 早先版本用 `isinstance(v, bool) → skip` 排除非数值，把化学的全部
            # check 项一并排掉了，--verbose 对化学题永远打印空列表。
            if isinstance(v, bool):
                v_f, v_r = float(v), float(bool(d_real.get(k)))
            elif isinstance(v, (int, float)):
                v_f, v_r = float(v), float(d_real.get(k) or 0)
            else:
                continue
            if v_f == 1.0 and v_r == 1.0:
                free_checks[f"{tid}::{k}"] += 1

    if not per:
        print("无可审计的 run。")
        return 1

    print(f"{'题目':<14}{'真实分':>8}{'假阳性地板':>11}{'地板占比':>9}  区分度")
    print("-" * 60)
    tot_r = tot_f = 0.0
    for tid in sorted(per, key=lambda t: -sum(per[t]["floor"]) / len(per[t]["floor"])):
        r = sum(per[tid]["real"]) / len(per[tid]["real"])
        f = sum(per[tid]["floor"]) / len(per[tid]["floor"])
        tot_r += r
        tot_f += f
        bar = "█" * int((r - f) * 20)
        print(f"{tid:<14}{r:>8.3f}{f:>11.3f}{(f / r if r else 0):>9.0%}  {bar}")
    n = len(per)
    print("-" * 60)
    print(f"{'合计':<14}{tot_r / n:>8.3f}{tot_f / n:>11.3f}{(tot_f / tot_r):>9.0%}")
    print(f"\n真正区分答案对错的分只有 {(tot_r - tot_f) / n:.4f}／"
          f"满分 1.0（其余 {tot_f / n:.4f} 是格式与关键词白拿）")
    if skipped:
        print(f"已跳过非数值答案题：{', '.join(sorted(skipped))}（需另设扰动算子）")

    if args.verbose:
        print("\n数值全错后仍然给分的 check 项（白拿项，按次数）：")
        for k, v in free_checks.most_common(40):
            print(f"  {v}x  {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
