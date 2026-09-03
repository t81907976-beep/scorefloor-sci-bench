#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签替换审计：量化**纯文字结论型判据**的白拿分——数值探针测不到的第 5 类。

背景：`audit_false_positive.py` 靠扰动数值作废答案。但 `ordinary_kummer_selected`、
`has_phase`、`dominant_thermal` 这类判据只看「话说没说」，答复里一个数字都不用改，
它们就照样命中。0806 一轮清点估这类项在化学十题上合计 2.83／10.0（约 28% 的分只判话说没说）。

方法（与数值探针对偶）：**保留全文，只把结论标签替换成反面表述**。
`\\lambda` 还是 `\\lambda`、单位还是那个单位、段落结构一字不动，只有结论的**语义**翻了面。
一个真正在判「结论对不对」的判据必须从 1 掉到 0；掉不下去，它判的就是关键词存在性。

## 实测结论

**化学侧（0806，22 项清单跑满 fixture 100 份答复）：纯文字白拿合计 = 0.000。**
清单里每一项都能被三个算子中的某一个压掉：16 项被本算子压到 0，2 项在本算子下存活但
它们的实现匹配的是数值/符号（化学03 `sign_cathodic_negative` 归 `--flip-sign`、
化学06 `has_intermediate` 归数值档），已按 `covered_by` 剔除、不重复计账。

即那 2.83 是**按「读起来像文字判据」归类**得到的上界；按「实现里到底匹配什么」
逐条核下来，化学侧的第 5 类不构成独立的白拿缺口。**但这不等于判据没问题** —— 见下。

**物理侧（0903，补进 15 项判断分叉题眼）：纯文字白拿合计 = 0.443。**
13 项翻面后正确归零，两项确认白拿：

  · 物理05 `approx_both_fail` 0.385（1/4）—— 24 字窗跨从句渗漏。某答复另有一句
    「量子亏损**不可**忽略，所有半径、能级**间隔**、寿命…」，`不可` 与 `间隔` 落在同一窗内，
    于是 no_fit_flag 被一句与 5% 检验无关的话喂饱。
  · 物理03 `bound_state_types` 0.059（5/5）—— 三个条件全是全文存在性，而 `l=0`、`l=1`、
    `2l+1` 三个串在分波展开式 Σ(2l+1)sin²δ_l 里必然出现，任何写了标准公式的答复都命中。
    该题源文件的判据注释自己就写着「本清单没有本题条目 = 这一项无任何算子覆盖」。

**另有 0.517 权重对否定句免疫，本算子按现行协议测不出来**（物理01
`both_approx_usable` 0.231 + 物理04 `e1_step` 0.286）：隔离验证把 `可用`→`不可用`、
`可忽略`→`不可忽略`（其余一字不动），两项 5/5 维持满档。见下一节。

## 判据本身的缺陷（翻面能压掉 ≠ 判据是对的）

翻面归零只证明「说反话拿不到分」，不证明「说对话才拿到分」。逐条核实现时发现
**四条判据收否定句／收错词**，隔离验证（单值串，只留待测那一句）如下：

1. 化学01 `has_ecsa_basis` / 化学02 `has_intrinsic_or_ecsa_basis` 是纯存在性：
   「本题**未做** ECSA 归一，直接用几何投影面积」→ 两项都 = 1.0。声明「我没按活性面积」
   与声明「我按了活性面积」同分，各白拿 0.15。
2. 化学02 还收 `异相` —— 那是电子转移机理的描述词、不是面积基准声明。
   「速率常数由**异相**电子转移动力学给出，未做面积归一」→ 1.0（改成「表观相」→ 0.0）。
   任何写「异相电子转移」的答复白拿这 0.15。
3. 化学04 `has_bg_subtraction` 收裸词 `背景`／裸词 `扣除`：
   「背景可忽略**不扣**」→ 1.0（改成「基线可忽略不减」→ 0.0）。
4. 化学05 `dominant_thermal` 的 `热.{0,6}(通道|主导)` 窗吃得下一个否定词：
   「热通道**不**主导，本反应走光化学通道」→ 1.0（改成「光通道主导」→ 0.0）。
5. 物理01 `both_approx_usable` 的 `(可用|成立|适用|满足|有效)` 白名单同族（0903 补）：
   「导引中心近似**不**可用」→ 0.2308 满档。`不可用` 里含 `可用`，说反话同分。
6. 物理04 `e1_step` 的 `(可忽略|忽略|negligible|ppm)` 有两个洞（0903 补）：
   「诱导 E1 **不可**忽略」→ 0.2857 满档；且裸 `ppm` 是量级词不是裁决词，
   凡写「约几个 ppm」即命中。「可否忽略」是二值判断，光押一边不该算算对。
   同题的正面样板是物理09 `final_instability_direction` —— 它自带
   `(不是|并非|没有|不存在|不会|无)不稳定|系统(是)?稳定` 否定否决闸，物理01/04 该照它改。

这些要靠**收紧判据**修，不是靠加扰动算子。翻面之所以仍能压掉它们，是因为翻面
把词根整个换掉了；真实模型写否定句时词根还在 —— 所以「本算子测不出白拿」与
「判据没缺陷」是两件事，第 5 类的真实风险在**否定句**而不在数值免疫。

输出六段：
  ① 翻面后仍然命中的判据 —— 权重照拿；`covered_by` 标注是否已被别的算子覆盖
  ② 翻面后正确归零的判据 —— 判据是好的，这项有真实鉴别力
  ③ 每题白拿权重合计（只算 covered_by=label 的项）
  ④ 附带损伤：翻面**不该影响**的其他判据却掉了分 —— 说明替换串破坏了邻接窗口，
     是探针自伤，替换规则要改（与 `_PROTECT` 的教训同一类）。同一判据的派生键
     （`core_hit` 含它、`numeric_anchor_hit_rate` 拿它当锚）在清单里用 `aliases` 声明后跳过
  ⑤ 跳过：该 run 原文没写这个结论标签，替换零生效
  ⑥ 失效／未覆盖的清单项 —— 0903 新增，见 `_report_stale` 的注释

标签对清单在 `tests/fixtures/conclusion-label-pairs.json`：底稿 19 项先在化学十题上起草，
再按每个判据的**真实实现**逐条校准（4 项归类改成数值、化学10 `has_phase` 的标签对整条重写、
物理08 3 项自出），0903 补齐物理 01–07/09/10 的 15 项判断分叉题眼、退休 4 项已删判据，
校准理由写在各项 `_note` 里。

用法：
    python3 scripts/audit_label_swap.py                    # 全部
    python3 scripts/audit_label_swap.py --task test-物理08  # 只看一题
    python3 scripts/audit_label_swap.py --verbose           # 打印每个 run 翻面前后的分值
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
_PAIRS = os.path.join(_ROOT, "tests", "fixtures",
                      "conclusion-label-pairs.json")


def swap_labels(text: str, pairs: list) -> tuple:
    """按序全文替换，返回 (翻面后文本, 实际生效的替换数)。

    返回生效数是必需的：**一次都没替换成功**说明这份答复根本没写该结论标签，
    此时判据本来就该是 0，把它算成「白拿」是探针自己造的假阳性。
    调用方必须据此跳过。
    """
    out, n = text, 0
    for pat, rep in pairs:
        out, k = re.subn(pat, rep, out)
        n += k
    return out, n


def _report_stale(stale) -> None:
    """清单里已经对不上题库的条目。

    必须显式报出来：原先这三种情况（题目没了 / fixture 里没有该题的 run /
    grade() 不再输出这个键）都是 `continue` 静默跳过，于是一条**失效的清单项**
    与一条**通过审计的清单项**在输出里完全一样 —— 0903 逐项体检才发现化学03/04
    的四项早在 v3 重写时随判据被删（`has_basis`→`rate_limiting_diffusion`、
    `has_bg_subtraction`→`bg_subtracted_numeric` 等），而化学11–15 五项从来没跑过
    （回归 fixture 只有 20 题 × 5 run，不含化学11–15）。清单一直号称覆盖
    「化学 15 题」，实际在跑的只有 11 项。
    """
    if not stale:
        return
    print("\n⑥ ⚠️ 失效／未覆盖的清单项（不进上面任何一段统计）")
    for tid, check, why in stale:
        print(f"   {tid:<14}{check:<40}{why}")


def _report(rows, damage, skipped, verbose=False) -> int:
    print("标签替换审计：纯文字结论型判据的白拿分（数值探针测不到的第 5 类）\n")

    free = [r for r in rows if r["still_hit"] > 0]
    good = [r for r in rows if r["still_hit"] == 0 and r["applicable"] > 0]

    print("① 结论翻面后**仍然命中**的判据 —— 确认白拿，权重照拿")
    print(f"   {'题目':<14}{'判据':<40}{'权重':>6}{'仍命中':>8}   {'其他算子'}")
    print("   " + "-" * 82)
    by_task = collections.defaultdict(float)
    for r in sorted(free, key=lambda x: -x["weight"] * x["still_hit"]):
        ratio = f"{r['still_hit']}/{r['applicable']}"
        cov = r["covered_by"]
        # covered_by 非 label 的项，其实现匹配的是数值或符号，已被数值探针/翻符号档
        # 压掉。它们在标签替换下存活是**预期的**（替换动不到实现看的那部分），
        # 不是新增白拿，不能计入第 5 类合计 —— 否则会与数值探针的账重复计一遍。
        counted = cov.startswith("label")
        if counted:
            by_task[r["task"]] += r["weight"]
        note = "—" if counted else f"已被 {cov} 覆盖"
        print(f"   {r['task']:<14}{r['check']:<40}{r['weight']:>6.3f}{ratio:>8}   {note}")
    if not free:
        print("   （无——所有文字结论判据都能被翻面压掉）")

    print("\n② 结论翻面后**正确归零**的判据 —— 有真实鉴别力")
    for r in sorted(good, key=lambda x: -x["weight"]):
        tail = f"（其中 {r['partial']} 次只掉了一部分）" if r.get("partial") else ""
        print(f"   {r['task']:<14}{r['check']:<40}{r['weight']:>6.3f}"
              f"{'0/' + str(r['applicable']):>8}  {tail}")
    if not good:
        print("   （无）")

    print("\n③ 每题白拿权重合计（**纯文字**部分，已剔除数值/符号探针已覆盖的项）")
    if by_task:
        print(f"   {'题目':<14}{'白拿权重':>10}")
        print("   " + "-" * 26)
        for tid, w in sorted(by_task.items(), key=lambda x: -x[1]):
            print(f"   {tid:<14}{w:>10.3f}")
        print("   " + "-" * 26)
        print(f"   {'合计':<14}{sum(by_task.values()):>10.3f}")
    else:
        print("   合计 0.000 —— 清单内每一项都能被三个算子中的某一个压掉。")

    if damage:
        print("\n④ ⚠️ 附带损伤：替换串破坏了**不相关**判据（探针自伤，替换规则要改）")
        for (tid, victim, culprit), n in sorted(damage.items(), key=lambda x: -x[1]):
            print(f"   {n}x  {tid}::{victim}  被 {culprit} 的替换压掉")
    else:
        print("\n④ 附带损伤：无。替换只动了目标判据，未破坏其他判据的邻接窗口。")

    if skipped:
        print("\n⑤ 跳过（该 run 原文没写这个结论标签，替换零生效，本来就该是 0）")
        for k, n in sorted(skipped.items(), key=lambda x: -x[1]):
            print(f"   {n}x  {k}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="标签替换审计：文字结论型判据的白拿分")
    ap.add_argument("--fixture", default=_FIXTURE)
    ap.add_argument("--pairs", default=_PAIRS)
    ap.add_argument("--task", default="", help="只看这道题")
    ap.add_argument("--verbose", action="store_true", help="打印翻面前后的文本片段")
    args = ap.parse_args()

    with open(args.fixture, encoding="utf-8") as f:
        cases = json.load(f)["cases"]
    with open(args.pairs, encoding="utf-8") as f:
        items = json.load(f)["items"]
    tasks = {t.task_id: t for t in discover_tasks(os.path.join(_ROOT, "tasks"))}

    rows = []
    damage = collections.Counter()
    skipped = collections.Counter()
    stale = []

    for item in items:
        tid, check = item["task"], item["check"]
        if args.task and tid != args.task:
            continue
        task = tasks.get(tid)
        if task is None or task.grade_fn is None:
            stale.append((tid, check, "题目不存在或没有 grade()"))
            continue
        runs = [c for c in cases if c["task"] == tid]
        if not runs:
            stale.append((tid, check, "fixture 里没有这道题的 run"))
            continue

        def grade(text):
            return task.grade_fn([{"role": "assistant", "content": text}],
                                 _ROOT, {"task_id": tid}) or {}

        if check not in grade(runs[0]["answer"]):
            stale.append((tid, check, "grade() 已不再输出这个键"))
            continue

        applicable = still_hit = partial = 0
        for case in runs:
            d_real = grade(case["answer"])
            # ⚠️ 0903：原判据写 `!= 1.0 → continue`，而物理题有一批 check 直接返回
            # **加权值**（物理01 `both_approx_usable`=0.2308、物理04 `tau_step`=0.4286、
            # `branch_step`/`e1_step`=0.2857），还有按比例给分的（物理10
            # `observed_peak_indexing`=0.909）。这些 check 一条都进不了统计，
            # 「翻面后该判据应从 1 掉到 0」这个协议在它们身上从未被执行过。
            # 改成「本来有分」即入选，「翻面后分没掉」即算白拿。
            v_real = float(d_real.get(check) or 0)
            if v_real <= 0:
                continue                      # 原文本来就没拿到这项，不参与统计
            swapped, n = swap_labels(case["answer"], item["pairs"])
            if n == 0:
                skipped[f"{tid}::{check}"] += 1
                continue                      # 替换零生效，见 swap_labels docstring
            applicable += 1
            d_swap = grade(swapped)
            v_swap = float(d_swap.get(check) or 0)
            if v_swap >= v_real:
                still_hit += 1
            elif v_swap > 0:
                partial += 1                  # 掉了一部分：判据只有一半在判结论
            if args.verbose:
                print(f"  [{tid} run{case['run']} {check}] 生效 {n} 处替换，"
                      f"{v_real:.4f} → {v_swap:.4f}")
            # aliases：题库里存在 `scores["a"] = scores["b"]` 这种同一判据两个字段名
            # （化学05 config_correct = config_extracted）。它们必然同落，
            # 算成「附带损伤」是探针自己的假阳性，清单里显式声明后跳过。
            same = {check, *item.get("aliases", [])}
            for k, v in d_swap.items():
                if k.startswith("_") or k == "auto_final_answer_score" or k in same:
                    continue
                if not isinstance(v, (int, float, bool)):
                    continue
                v_r, v_s = float(d_real.get(k) or 0), float(v)
                if v_r > 0 and v_s < v_r:
                    damage[(tid, k, check)] += 1

        if applicable or skipped.get(f"{tid}::{check}"):
            rows.append({"task": tid, "check": check,
                         "weight": float(item.get("weight") or 0),
                         "covered_by": str(item.get("covered_by") or "label"),
                         "applicable": applicable, "still_hit": still_hit,
                         "partial": partial})

    if not rows:
        print("无可审计项。")
        _report_stale(stale)
        return 1
    rc = _report(rows, damage, skipped, args.verbose)
    _report_stale(stale)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
