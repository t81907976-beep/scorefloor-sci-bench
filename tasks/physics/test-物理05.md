# 构造高质量-query

芯片式 87Rb 里德伯电场计以 5p3/2 为初态扫描 E1 耦合光。相对该态的电离阈值跃迁波数
T=20874.300 cm^-1。场电离标定名义 n 的谱线：A 系列为 19478.439(12)、20211.556(16)、
20488.631(20)，B 系列为 19907.160(12)、20363.139(16)、20558.872(20)，误差均 ±0.003 cm^-1。
取 R_Rb=109736.6 cm^-1。

(1) 判定 A、B 两系列各属哪个里德伯系列、轨道角动量 l 为多少；
(2) 反演 A 系列的里兹量子亏损；
(3) 按 5% 精度判断 n=12、n=20 能否用相邻能级间隔的 n*^-3 微分近似；
(4) 说明误用裸 n 代替有效主量子数对半径 r、寿命 τ 标度的影响。

请完整写出判据、推理与计算过程。最后单独用一行给出结论，格式为：
【结果】A系列: …(l=…), δA=…; B系列: …(l=…), δB=…; n=12 n*^-3近似: 可用/不可用(误差…); n=20 n*^-3近似: 可用/不可用(误差…); 标度须用 n*/裸 n（给出高估因子）

# SFT标准-response

**最终结论：**
- **A 系列 = ns（l=0），δA≈3.13**（随 n 缓慢变化：δA(12)=3.13345、δA(16)=3.13224、δA(20)=3.13181；
  里兹展开 δ0≈3.1312、δ2≈0.178）。
- **B 系列 = nd（l=2），δB≈1.348**（δB(12)=1.34800、δB(16)=1.34800、δB(20)=1.34799，基本恒定）。
- **n=12：相对误差≈17.2%＞5%，不能用 n*^-3 微分近似**；**n=20：相对误差≈8.98%＞5%，同样不能用**。
- 半径 **r∝n*²**、寿命 **τ∝n*³** 必须用有效主量子数 n*，误用裸 n **高估**：n=12 半径 1.83×、寿命 2.48×；
  n=20 半径 1.41×、寿命 1.67×。

正确推理链（基准 7 步 N0=7）：

1. **能量零点与束缚波数**：T=20874.300 cm⁻¹ 是相对共同初态 5p3/2 的**阈值跃迁波数**；观测 ν̃_n 也是
   5p3/2→里德伯态的**跃迁波数**，不是里德伯电子束缚波数。故须先算束缚波数 **B_n=T-ν̃_n**，
   再由 B_n=R_Rb/(n*)² 得 **n*=√(R_Rb/B_n)**、量子亏损 **δ(n)=n-n***。
2. **A 系列反演**：B12=1395.861→n*12=8.86655→δA(12)=3.13345；B16=662.744→n*16=12.86776→δA(16)=3.13224；
   B20=385.669→n*20=16.86819→δA(20)=3.13181。δA≈3.13，随 n 有可分辨的缓慢变化。
3. **B 系列反演**：B12=967.140→n*12=10.65200→δB(12)=1.34800；B16=511.161→n*16=14.65200→δB(16)=1.34800；
   B20=315.428→n*20=18.65201→δB(20)=1.34799。δB≈1.348，基本恒定。
4. **系列与 l 判定**：初态 5p3/2，l=1；E1 选择定则 Δl=±1 ⇒ 末态 l=0（ns）或 l=2（nd）。碱金属中 s 电子
   穿透原子实强、量子亏损大，d 电子穿透弱、量子亏损小 ⇒ **A（δ≈3.13）为 ns（l=0）**，**B（δ≈1.348）为
   nd（l=2）**。j 分裂未由数据分辨，不影响 l 归属。
5. **A 系列里兹量子亏损**：σ_ν̃=0.003 cm⁻¹，由 n*=√(R/B) 得 σ_δ=n*³σ_ν̃/(2R_Rb)：σ_δ(12)≈9.5e-6、
   σ_δ(20)≈6.6e-5。而 δA(12)-δA(20)≈1.64e-3 远大于合成不确定度 ⇒ 常量子亏损近似在该精度下不成立。
   低阶里兹展开 **δA(n)≈δ0+δ2/(n-δ0)²**，拟合得 **δ0≈3.1312、δ2≈0.178**。
6. **n*^-3 相邻间隔 5% 检验**：精确间隔 Δν̃_n=B_n-B_{n+1}=R_Rb/(n*_n)²-R_Rb/(n*_{n+1})²，微分近似
   Δν̃_der=2R_Rb/(n*_n)³。**n*_{n+1} 须由里兹量子亏损在 n+1 处算**（δ 非严格常数）。
   n=12：δA(13)≈3.13303、n*13≈9.86697、Δν̃12=268.710，Δν̃der,12=314.86，误差 **≈17.2%＞5% → 不可用**。
   n=20：δA(21)≈3.13176、n*21≈17.86824、Δν̃20=41.963，Δν̃der,20=45.73，误差 **≈8.98%＞5% → 不可用**。
7. **裸 n 对标度的影响**：r∝n*²、τ∝n*³ 须用 n*。误用裸 n 的高估因子 r_bare/r=(n/n*)²、τ_bare/τ=(n/n*)³：
   n=12（n*/n=0.7389）半径高估 1/0.5457≈**1.83×**、寿命高估 1/0.4038≈**2.48×**；
   n=20（n*/n=0.8434）半径高估 **1.41×**、寿命高估 **1.67×**。

# 步骤列表-reference

[1] 能量零点：ν̃ 是跃迁波数，须算束缚波数 B_n=T-ν̃_n，n*=√(R_Rb/B_n)、δ=n-n*。
[2] A 系列反演：B12/16/20→n*=8.867/12.868/16.868→δA(12/16/20)=3.13345/3.13224/3.13181，δA≈3.13。
[3] B 系列反演：n*=10.652/14.652/18.652→δB(12/16/20)=1.34800/1.34800/1.34799，δB≈1.348。
[4] 系列/l 判定：Δl=±1 + 穿透强弱 → A（大 δ）=ns(l=0)、B（小 δ）=nd(l=2)，不搞反。
[5] 里兹量子亏损：σ_δ≪δ 变化量 → 常量子亏损不成立，里兹展开 δ0≈3.1312、δ2≈0.178。
[6] 5% 检验：n*_{n+1} 用里兹算，精确间隔 vs 2R/n*³，n=12≈17.2%、n=20≈8.98%，均＞5% 不可用。
[7] 裸 n 标度：r∝n*²、τ∝n*³ 须用 n*，裸 n 高估 n=12(1.83×/2.48×)、n=20(1.41×/1.67×)。

## Grading Criteria

- [ ] 识别观测量是跃迁波数、须算束缚波数 B_n=T-ν̃_n，再由 n*=√(R_Rb/B_n) 得 n* 与 δ=n-n*（不得把 ν̃ 直接当束缚能反演）。
- [ ] 由 E1 选择定则 Δl=±1 + s/d 穿透量子亏损大小，判 **A=ns（l=0）、B=nd（l=2）**，不得搞反；δA≈3.13、δB≈1.348。
- [ ] 用误差传递说明常量子亏损不成立，给里兹展开 δ0≈3.1312、δ2≈0.178。
- [ ] **用 n*_{n+1}（里兹）算精确间隔与 2R/n*³ 微分近似比较，n=12≈17.2%、n=20≈8.98%，两者均＞5% 不可用（核心防御位）。**
- [ ] 明确 r∝n*²、τ∝n*³ 须用 n* 不用裸 n，并给出裸 n 高估因子（n=12：1.83×/2.48×；n=20：1.41×/1.67×）。

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。本 grade() 已内联全部锚点与阈值，不依赖外部 meta。

> **v2 天然多 gate**：本题终答是一组耦合结论（δA/δB、系列/l 归属、两个 5% 判定、n* 标度因子），四个
> gate 相互独立、区分度天然分层。核心防御位 gate = **「n*⁻³ 微分近似可用/不可用」判定**：判"可用"（上当）
> → 该分项 0，且逻辑分封顶 ≤0.30。

```python
def grade(transcript: list, workspace_path: str, meta: dict) -> dict:
    import re

    ANSWER_TAG = "【结果】"

    def _content(m):
        c = m.get("content", "")
        if isinstance(c, list):
            return " ".join(seg.get("text", "") for seg in c if isinstance(seg, dict))
        return c if isinstance(c, str) else ""

    assistant_msgs = [_content(m) for m in transcript if m.get("role") == "assistant"]
    full = "\n".join(assistant_msgs)
    full_l = full.lower()
    final_msg = assistant_msgs[-1] if assistant_msgs else ""

    anchor_region = final_msg
    if ANSWER_TAG in final_msg:
        anchor_region = final_msg.split(ANSWER_TAG, 1)[1][:500]

    def _nums(pattern, text):
        vals = []
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            seg = text[m.end():m.end() + 32]
            sm = re.search(r'([0-9]*\.?[0-9]+)', seg)
            if sm and sm.group(1):
                vals.append(float(sm.group(1)))
        return vals

    def _close(v, target, tol):
        return v is not None and target != 0 and abs(v - target) / abs(target) <= tol

    out = {}

    # ---- δA（A 系列量子亏损，目标 3.13；容差 3%）----
    da_vals = _nums(r'(?:δ\s*_?\s*a|δ\s*a|delta_?a|a\s*系列.{0,12}?(?:量子亏损|亏损|δ|delta)|量子亏损.{0,6}?(?:δ_?a)?)\s*[:=≈约]?', full_l)
    da_hit = any(_close(v, 3.13, 0.03) for v in da_vals) or ("3.13" in full)

    # ---- δB（B 系列量子亏损，目标 1.348；容差 3%）----
    db_vals = _nums(r'(?:δ\s*_?\s*b|δ\s*b|delta_?b|b\s*系列.{0,12}?(?:量子亏损|亏损|δ|delta))\s*[:=≈约]?', full_l)
    db_hit = any(_close(v, 1.348, 0.03) for v in db_vals) or ("1.348" in full) or ("1.35" in full and "b" in full_l)

    # ---- 系列/l 归属：A=ns(l=0)、B=nd(l=2)，且未搞反 ----
    has_ns = bool(re.search(r'\bns\b|l\s*=\s*0|s\s*系列|s\s*态|l=0', full_l))
    has_nd = bool(re.search(r'\bnd\b|l\s*=\s*2|d\s*系列|d\s*态|l=2', full_l))
    a_ns = bool(re.search(r'a[\s，,、]{0,6}(?:系列)?[^\n。；;]{0,20}(ns|l\s*=\s*0|s\s*系列|s\s*态)', full_l)) or (has_ns and da_hit)
    b_nd = bool(re.search(r'b[\s，,、]{0,6}(?:系列)?[^\n。；;]{0,20}(nd|l\s*=\s*2|d\s*系列|d\s*态)', full_l)) or (has_nd and db_hit)
    assign_swapped = bool(re.search(r'a[\s，,、]{0,6}(?:系列)?[^\n。；;]{0,20}(nd|l\s*=\s*2)', full_l)) \
        or bool(re.search(r'b[\s，,、]{0,6}(?:系列)?[^\n。；;]{0,20}(ns|l\s*=\s*0)', full_l))
    assign_ok = a_ns and b_nd and not assign_swapped

    # ---- 5% 检验：n=12、n=20 均判"不可用"（核心防御 gate）----
    err12 = bool(re.search(r'1[67]\.\d\s*%', full)) or ("17.2" in full) or ("17%" in full)
    err20 = bool(re.search(r'[89]\.\d{1,2}\s*%', full)) or ("8.98" in full) or ("9.0" in full and "%" in full)
    no_fit_flag = bool(re.search(
        r'(不能|不可|不适用|不成立|失效|均不|都不)[^\n。；;]{0,24}(近似|n\*?\s*\^?\s*-?\s*3|微分|间隔)', full_l)) \
        or bool(re.search(
        r'(近似|微分近似|n\*?\s*\^?\s*-?\s*3|间隔)[^\n。；;]{0,24}(不能|不可|不适用|不成立|失效|均不|都不)', full_l))
    approx_both_fail = no_fit_flag and err12 and err20

    # ---- 裸 n 标度：r∝n*²、τ∝n*³ 须用 n*，给高估因子 ----
    scale_use_nstar = bool(re.search(
        r'(有效主量子数|n\*|n\^?\*|裸\s*n)[^\n。；;]{0,40}(半径|寿命|标度|尺度|r\s*∝|τ\s*∝|不能用|须用|应用|而非)', full_l)) \
        or ("裸 n" in full) or ("裸n" in full)
    scale_factor_ok = (("1.83" in full and "2.48" in full) or ("1.41" in full and "1.67" in full)) \
        or bool(re.search(r'高估.{0,10}(1\.8|2\.4|1\.4|1\.6)', full))

    non_empty = 1.0 if len(full.strip()) >= 30 else 0.0
    refusal = bool(re.search(r"(无法回答|不能回答|不会做|拒绝作答|i cannot|i can't|cannot solve)", full_l))
    not_refusal = 0.0 if refusal else 1.0

    # 核心命中（0.50）：δA≈3.13 且系列/l 归属正确(0.25) + n=12/n=20 均判 n*^-3 不可用(0.25)
    core = 0.25 * (1.0 if (da_hit and assign_ok) else 0.0) \
         + 0.25 * (1.0 if approx_both_fail else 0.0)
    has_unit = 1.0 if (re.search(r"cm\s*\^?\{?\s*-?\s*1|cm⁻¹|cm-1", full_l)
                       or ("n*" in full_l) or ("有效主量子数" in full) or ("无量纲" in full)) else 0.0
    scale_final = 0.15 if (scale_use_nstar and scale_factor_ok) else (0.075 if scale_use_nstar else 0.0)

    final_answer = 0.10 * non_empty + 0.10 * not_refusal + core + 0.15 * has_unit + scale_final
    out["non_empty_answer"] = non_empty
    out["not_refusal"] = not_refusal
    out["core_hit"] = round(core, 4)
    out["has_unit"] = has_unit
    out["nstar_scaling"] = round(scale_final, 4)
    out["assign_swapped"] = 1.0 if assign_swapped else 0.0
    out["approx_both_fail"] = 1.0 if approx_both_fail else 0.0

    # numeric 锚点命中率（5 锚点：δA、δB、n=12 误差、n=20 误差、裸 n 高估因子）
    anchors = [
        da_hit and assign_ok,
        db_hit,
        err12 and no_fit_flag,
        err20 and no_fit_flag,
        scale_use_nstar and scale_factor_ok,
    ]
    out["numeric_anchor_hit_rate"] = round(sum(1 for h in anchors if h) / 5.0, 4)

    out["auto_final_answer_score"] = round(final_answer, 4)
    return out
```

## LLM Judge Rubric

大模型评分负责**过程、概念与逻辑**，不重复判定代码已覆盖的最终数值命中。本题为**天然多 gate 题**（4 个
独立 gate），逻辑分设「n*⁻³ 近似可用/不可用」为决定性 gate；步骤分只评方法动作是否执行到位。

### Criterion 1: 步骤分（方法动作，Weight: 1/3）

按 S1–S5 各 0.20 累加（缺一步扣该项分），与 gate 对错解耦：

- **S1 能量零点与束缚波数（0.20）**：识别 ν̃ 是跃迁波数，算 B_n=T-ν̃、n*=√(R_Rb/B_n)、δ=n-n*。
- **S2 两系列反演 + 系列/l 判定（0.20）**：δA≈3.13、δB≈1.348；由 Δl=±1+穿透判 A=ns(l=0)、B=nd(l=2)。
- **S3 里兹量子亏损（0.20）**：误差传递 σ_δ、常量子亏损不成立，里兹展开 δ0≈3.1312、δ2≈0.178。
- **S4 5% 检验（0.20）**：用 n*_{n+1}（里兹）算精确间隔与 2R/n*³ 微分近似，n=12≈17.2%、n=20≈8.98%。
- **S5 裸 n 标度影响（0.20）**：r∝n*²、τ∝n*³，裸 n 高估因子 n=12(1.83×/2.48×)、n=20(1.41×/1.67×)。

> 参考档位：全覆盖 S1–S5 ≈ 1.0；漏 S3 里兹展开或 S5 只给定性方向未给因子 ≈ 0.5；
> 漏减 T 硬套 R/n²、缺系列反演与 5% 检验 ≈ 0.0。

### Criterion 2: 逻辑分（Weight: 1/3，核心防御位）

L1 能量零点（0.30）+ L2 系列/l 归属（0.25）+ L3 n* 非裸 n（0.25）+ L4 自洽性（0.20），
其中**「n*⁻³ 近似判定」是决定性 gate**：

- **L1 能量零点（0.30）**：明确观测量是**跃迁波数**、须先减 T 得束缚波数 B_n=T-ν̃，未把 ν̃ 直接当束缚能
  反演（漏减 T 则该项 0）。
- **L2 系列/l 归属（0.25）**：大 δ→ns(l=0)、小 δ→nd(l=2)，由 E1 选择定则 Δl=±1 + 穿透强弱判定，**未搞反**。
- **L3 n* 非裸 n（0.25）**：标度 r∝n*²/τ∝n*³ 与 n*⁻³ 近似均用 **n* 而非裸 n**；量子亏损非严格常数须里兹展开。
- **L4 自洽性（0.20）**：误差传递、里兹拟合、5% 检验、标度因子各结论前后不矛盾。

> **决定性 gate**：把 n=12/n=20 判成"n*⁻³ 近似可用"（认定量子亏损严格常数、跳过误差传递）即踩 P5 核心陷阱
> → L3/L4 相关分项判 0，**逻辑分封顶 ≤0.30**。
> 参考档位：L1–L4 全对 ≈ 1.0；机制未点破或量级表述含糊 ≈ 0.5；踩 P5 陷阱（漏减 T / 系列 l 搞反 /
> 用裸 n 代 n* / 误判近似成立）→ 对应项判 0，逻辑分显著低于 0.5。（即便脚本最终答复分因某分项蒙对给了分，
> 逻辑分仍独立判。）

> **最终答复分（脚本评，权重 1/3）** 不在此 rubric 内，由 `grade()` 客观给出（δA/系列 + 两个 5% 判定 +
> n* 标度加权）。LLM 不重复评最终答复分。
