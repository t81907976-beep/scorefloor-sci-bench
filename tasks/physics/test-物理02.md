# 构造高质量-query

一只用于低噪声电场标定的镀金导体微粒悬浮在足够大的绝缘硅油槽中。硅油可看作均匀、线性、
各向同性介质，相对介电常数 εr=2.20。微粒未用导线接地，释放前不带净电荷；外部平行板在远离
微粒处产生近似均匀电场 E0=1.50 kV/m，方向沿实验室 z 轴。显微测量给出三个互相垂直的半轴读数
A=0.7500 mil、B=12.700 μm、C=0.2500 mil（1 mil=25.400 μm），A、B、C 分别平行于实验室
x、y、z 轴。每个长度读数的标准不确定度均为 0.010 μm。约定：若任意两半轴的差值不超过 3 倍
合成标准不确定度，则视为相等并用相应退化坐标；否则按真正三轴椭球处理。取
ε0=8.8541878128×10^-12 F/m。忽略重力沉降、边缘效应与介质损耗。

(1) 依据测量数据和判据判断应采用球坐标、旋转椭球坐标还是三轴共焦椭球坐标（不得预设三轴情形）；
(2) 若判定为三轴情形，建立外部共焦椭球坐标（α=a²、β=b²、γ=c²，λ、μ、ν 为
    x²/(s+α)+y²/(s+β)+z²/(s+γ)=1 的三个实根），说明外部区域和各坐标取值范围；
(3) 分离均匀介质内 Laplace 方程 ∇²Φ=0，推出三变量满足的同一形式 Lamé 方程，说明分离常数不独立；
(4) 由静电平衡、封闭性、远场与对称性确定应选取的椭球谐模式与径向解组合；
(5) 求导体沿 z 方向的诱导偶极矩 pz 并给出 SI 数值（Φind≈pz z/(4πε0εr r³)）。

请完整写出判据、推理与计算过程。最后单独用一行给出结论，格式为：
【结果】坐标类型: …；a,b,c=…；退极化因子 L_z=…；pz=…（方向…）

# SFT标准-response

**最终结论：**
- **坐标类型：三轴共焦椭球坐标**。u_c=√2·0.010=0.01414 μm，阈值 3u_c=0.04243 μm；三对轴差
  |a-b|=|b-c|=6.350 μm、|a-c|=12.700 μm 均 ≫ 阈值 ⇒ 不能退化为球/旋转椭球，必须用真正三轴共焦椭球坐标。
- **半轴**：a=19.050 μm、b=12.700 μm、c=6.350 μm（**比 3:2:1**，a>b>c）；α=a²=3.629025×10⁻¹⁰、
  β=b²=1.612900×10⁻¹⁰、γ=c²=4.032250×10⁻¹¹ m²。外部区 **λ∈[0,∞)、μ∈[-β,-γ]、ν∈[-α,-β]**，导体面 λ=0。
- **Lamé 方程**：4P·E''+2P'·E'+[-n(n+1)s+B]·E=0，P(s)=(s+α)(s+β)(s+γ)，n、B 三变量共用 ⇒ **仅两个独立分离常数**。
- **选模**：外场 Φ∞=-E0 z 关于 z 奇、关于 x/y 偶 ⇒ n=1 的 z 型谐模 E_z(s)=√(s+γ)，配衰减解
  I(λ)=∫_λ^∞ ds/[(s+γ)√P]，Φ=-E0 z[1-I(λ)/I(0)]（表面常数、远场趋 -E0 z）。
- **退极化因子**：z 为最短轴 ⇒ **L_z≈0.5766**（最大；L_x≈0.1563、L_y≈0.2672，L_x+L_y+L_z=1.000）。
- **诱导偶极矩 pz≈3.26×10⁻²² C·m，沿 +z**（与外加场同向）。

正确推理链（基准 6 步）：

1. **单位换算 + 不确定度判据**：A=0.7500 mil=19.050 μm、B=12.700 μm、C=0.2500 mil=6.350 μm（比 3:2:1）。
   两轴差的合成标准不确定度 u_c=√(u²+u²)=√2·0.010=0.01414 μm，阈值 3u_c=0.04243 μm。三对差 6.350/6.350/12.700 μm
   均 ≫ 阈值 ⇒ 不可退化，**采用三轴共焦椭球坐标**（不预设三轴）。
2. **椭球参数与坐标范围**：a>b>c，α=a²、β=b²、γ=c²（α>β>γ>0）。λ、μ、ν 为
   x²/(s+α)+y²/(s+β)+z²/(s+γ)=1 三实根，排序 -α≤ν≤-β≤μ≤-γ≤λ<∞。外部区 λ∈[0,∞)、μ∈[-β,-γ]、
   ν∈[-α,-β]，导体面 λ=0（x²/a²+y²/b²+z²/c²=1）。
3. **Laplace 分离 → Lamé 方程**：介质均匀线性各向同性、外部无自由电荷 ⇒ ∇²Φ=0。令 Φ=L(λ)M(μ)N(ν)、
   P(s)=(s+α)(s+β)(s+γ)，分离得同形 Lamé 方程 4P·E''+2P'·E'+[-n(n+1)s+B]·E=0，n、B 三变量共用，
   **只有两个独立分离常数**（非三个）。
4. **选模 + 径向解**：Φ∞=-E0 z 关于 z 奇、关于 x/y 偶 ⇒ 只取 n=1 的 z 型谐模 E_z(s)=√(s+γ)。Q=0 排除单极；
   远场衰减取第二类解 I(λ)=∫_λ^∞ ds/[(s+γ)√P]，得 Φ=-E0 z[1-I(λ)/I(0)]（λ=0 表面为常数、λ→∞ 趋 -E0 z）。
5. **退极化因子（对号入座）**：L_z=(abc/2)∫_0^∞ ds/[(s+c²)√((s+a²)(s+b²)(s+c²))]=(abc/2)I(0)。**z 是最短轴**
   ⇒ 沿短轴退极化最强 ⇒ **L_z≈0.5766 最大**（L_x≈0.1563、L_y≈0.2672，和为 1；数值积分）。
6. **诱导偶极矩**：远场 Φind≈(2E0)/(3I(0))·z/r³，比对 Φind≈pz z/(4πε0εr r³) ⇒
   **pz=4πε0εr·abc·E0/(3L_z)**。代入 ε0εr=1.947921×10⁻¹¹ F/m、abc=1.536287×10⁻¹⁵ m³、E0=1500 V/m、
   L_z=0.5766 ⇒ **pz≈3.26×10⁻²² C·m，沿 +z**。校验：a=b=c 时 L=1/3、pz=12πεR³E0 回到导体球标准式。

# 步骤列表-reference

[1] 换算 + 不确定度判据：A/B/C→19.050/12.700/6.350 μm（3:2:1）；u_c=√2·0.010=0.01414、3u_c=0.0424 μm，三差 ≫ 阈值 → 三轴共焦椭球坐标（不预设）。
[2] 椭球参数 + 坐标范围：α/β/γ=a²/b²/c²；外部区 λ∈[0,∞)、μ∈[-β,-γ]、ν∈[-α,-β]，导体面 λ=0。
[3] Laplace 分离 → 同形 Lamé 方程 4P E''+2P'E'+[-n(n+1)s+B]E=0，n、B 三变量共用、仅两个独立分离常数。
[4] 对称性选 n=1 的 z 型谐模 E_z=√(s+γ)，配衰减解 I(λ)，Φ=-E0 z[1-I(λ)/I(0)]。
[5] 退极化因子 L_z=(abc/2)I(0)≈0.5766（z 短轴取最大，L_x+L_y+L_z=1）。
[6] 诱导偶极矩 pz=4πε0εr abc E0/(3L_z)≈3.26×10⁻²² C·m，沿 +z；球极限回到 pz=12πεR³E0 校验。

## Grading Criteria

- [ ] 用 3u_c 判据（u_c=√2·0.010=0.01414 μm、阈值 0.0424 μm）判定为**三轴共焦椭球坐标**，不预设三轴。
- [ ] 半轴换算 a=19.050、b=12.700、c=6.350 μm（比 3:2:1），给外部区 λ∈[0,∞)、μ∈[-β,-γ]、ν∈[-α,-β]、导体面 λ=0。
- [ ] 分离 ∇²Φ=0 得同形 Lamé 方程，说明 n、B 三变量共用、**仅两个独立分离常数**。
- [ ] 由对称性选 n=1 的 z 型谐模 E_z=√(s+γ)，配衰减解得 Φ=-E0 z[1-I(λ)/I(0)]。
- [ ] **识别 z 为最短轴 ⇒ L_z≈0.5766 最大**（非 0.17），L_x+L_y+L_z=1 自洽。
- [ ] 用 ε=ε0εr（非真空 ε0）、导体公式 pz=4πε0εr·abc·E0/(3L_z)（非介质椭球 (εr-1) 式）得 pz≈3.26×10⁻²² C·m 沿 +z。

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。本 grade() 已内联全部锚点与阈值，不依赖外部 meta。

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
    full_norm = re.sub(r'\\text\{|\}|\\,|\\ |\\mathrm\{|\\;|\{|\s', '', full_l)
    full_norm = full_norm.replace("\\cdot", "·").replace("\\times", "×").replace("\\approx", "≈")

    def _nums(pattern, text):
        vals = []
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            seg = text[m.end():m.end() + 48]
            sm = re.search(
                r'([-+]?)\s*([0-9]*\.?[0-9]+)\s*'
                r'(?:[×x*]\s*10\s*\^?\{?\s*([-+]?\d+)\s*\}?|e\s*([-+]?\d+))?',
                seg, flags=re.IGNORECASE)
            if sm and sm.group(2):
                v = float(sm.group(2))
                exp = sm.group(3) or sm.group(4)
                if exp:
                    v *= 10 ** int(exp)
                if sm.group(1) == '-':
                    v = -v
                vals.append(v)
        return vals

    def _mag_ok(v, target, tol=0.20):
        return v is not None and target != 0 and abs(abs(v) - abs(target)) / abs(target) <= tol

    out = {}

    pz_sci = _nums(r'(?:p_?z|pz|诱导偶极矩|偶极矩|boxed)[:=≈约]?', full_norm)
    pz_vals = [v for v in pz_sci if abs(v) < 1e-15]
    pz_hit = any(_mag_ok(v, 3.26e-22, 0.20) for v in pz_vals) \
             or bool(re.search(r'3\.2[0-9]×10\^?-22', full_norm))

    lz_all = _nums(r'(?:l_?z|n_?z|退极化因子|去极化因子|退极化系数|退极化积分)[:=≈约]?', full_norm)
    lz_vals = [v for v in lz_all if 0 < abs(v) <= 1.0]
    lz_hit = any(_mag_ok(v, 0.5766, 0.10) for v in lz_vals) or ("0.576" in full or "0.577" in full)
    lz_wrong_axis = any(0.10 <= abs(v) <= 0.35 for v in lz_vals) and not lz_hit

    triaxial = bool(re.search(r'三轴|共焦椭球|triaxial|scalene|ellipsoidal\s+coordinate', full_l))
    crit_uc = ("0.0424" in full) or ("0.04243" in full) or ("0.01414" in full) or ("0.014142" in full) \
              or bool(re.search(r'(√\s*2|\\sqrt\{?2|1\.414)\s*[×x*·]?\s*(u|0\.010)', full_norm)) \
              or ("合成标准不确定度" in full) or ("合成不确定度" in full)
    triaxial_by_crit = triaxial and crit_uc

    axes_ok = ("19.05" in full and "12.7" in full and "6.35" in full) \
              or ("3:2:1" in full.replace(" ", "")) or ("3 : 2 : 1" in full)

    non_empty = 1.0 if len(full.strip()) >= 30 else 0.0
    refusal = bool(re.search(r"(无法回答|不能回答|不会做|拒绝作答|i cannot|i can't|cannot solve)", full_l))
    not_refusal = 0.0 if refusal else 1.0

    core = 0.25 * (1.0 if pz_hit else 0.0) \
         + 0.25 * (1.0 if triaxial_by_crit else 0.0)
    has_unit = 1.0 if re.search(r"c\s*[·⋅.]?\s*m|c\s*·\s*m|coulomb\s*[- ]?\s*met", full_norm) else 0.0
    lz_final = 0.15 if lz_hit else 0.0

    final_answer = 0.10 * non_empty + 0.10 * not_refusal + core + 0.15 * has_unit + lz_final
    out["non_empty_answer"] = non_empty
    out["not_refusal"] = not_refusal
    out["pz_hit"] = 1.0 if pz_hit else 0.0
    out["triaxial_by_criterion"] = 1.0 if triaxial_by_crit else 0.0
    out["has_unit"] = has_unit
    out["depolarization_Lz"] = round(lz_final, 4)

    anchors = [pz_hit, lz_hit, axes_ok, triaxial_by_crit]
    out["numeric_anchor_hit_rate"] = round(sum(1 for h in anchors if h) / 4.0, 4)

    out["auto_final_answer_score"] = round(final_answer, 4)
    return out
```

## LLM Judge Rubric

大模型评分负责**过程、概念与逻辑**，不重复判定代码已覆盖的最终数值命中。

### Criterion 1: 坐标类型由判据定（Weight: 30%，核心防御位）

**Score 1.0**: 明确用 3u_c 合成不确定度判据（u_c=√2·0.010=0.01414、3u_c=0.0424 μm）客观判定坐标类型，三对轴差 ≫ 阈值 ⇒ 三轴共焦椭球，未预设三轴、未误判球/旋转椭球。
**Score 0.5**: 判为三轴且大体正确，但只凭"读数不同"直觉、未算 u_c 判据。
**Score 0.0**: 预设三轴无判据，或误判为球/旋转椭球。

### Criterion 2: Lamé 分离 + 选模 + 径向解（Weight: 25%）

**Score 1.0**: 建立外部坐标与范围（λ∈[0,∞)、导体面 λ=0），分离得同形 Lamé 方程、n/B 共用仅两个独立常数；由对称性选 n=1 的 z 型谐模 E_z=√(s+γ)，配衰减解得 Φ=-E0 z[1-I(λ)/I(0)]。
**Score 0.5**: 主链对但分离常数不独立或选模由对称性某处说明不完整。
**Score 0.0**: 未分离/误用球谐、选模与对称性不符。

### Criterion 3: 退极化因子对号 + 介质/导体公式（Weight: 30%，核心防御位）

**Score 1.0**: **z 为最短轴 ⇒ L_z 最大 ≈0.577**（不是最小 0.17），L_x+L_y+L_z=1 自洽；用 ε=ε0εr（非真空 ε0）、导体极限 pz=4πε·abc·E0/(3L_z)，未套介质椭球 (εr-1) 极化式。
**Score 0.5**: L_z 轴向对号对但介质因子/导体公式某处含糊。
**Score 0.0**: 把 L_z 当最小值（≈0.17）致 pz 偏数倍，或漏乘 εr，或套介质椭球 (εr-1) 公式。

### Criterion 4: 自洽性（Weight: 15%）

**Score 1.0**: 分离常数不独立、选模由对称性、球极限回到 pz=12πεR³E0，各结论前后不矛盾。
**Score 0.5**: 基本自洽但缺球极限校验。
**Score 0.0**: 前后矛盾或无自洽说明。
