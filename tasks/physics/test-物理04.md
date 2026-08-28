# 构造高质量-query

在铯喷泉旁运行的单离子 138Ba+ 光钟中，关激光后初态全在 a=5D5/2。只开 493nm 探测，
g=6S1/2 发亮，D 态暗。已知 b=5D3/2→g 速率 β=0.0125 s^-1；测得亮概率
B(10,30,80s)=0.2349, 0.5453, 0.8618。另有 5 V/cm 杂散场，最近 6P3/2 距 a 为
1.20e4 cm^-1，偶极矩 2.0 ea0，A(P→g)=1.2e8 s^-1。

求 a 寿命、a→g 与 a→b 分支，并判定诱导 E1 可否忽略。

请完整写出速率方程、拟合与推理过程。最后单独用一行给出结论，格式为：
【结果】τ_a=…；A(a→g)=…（Br…）；A(a→b)=…（Br…）；诱导E1: 可忽略/不可忽略（给出 A_ind/Γ）

# SFT标准-response

**最终结论：**
- a 态寿命 **τ_a = 1/Γ = 33.3 s**（Γ = 3.00×10⁻² s⁻¹）
- **a→g 部分速率 A(a→g)=x=2.70×10⁻² s⁻¹，Br(a→g)=90.0%（主支）**
- **a→b 部分速率 A(a→b)=y=3.00×10⁻³ s⁻¹，Br(a→b)=10.0%**
- 5 V/cm 杂散场诱导 E1：**A_ind≈1.5×10⁻⁷ s⁻¹，A_ind/Γ≈5.1×10⁻⁶（ppm 级），可忽略**

正确推理链（基准 6 步 N0=6）：

1. **探测含义与速率模型**：关激光后无泵浦，a 只向 g=6S1/2 与 b=5D3/2 自发衰变，b 再以
   β=0.0125 s⁻¹ 衰变到 g；只开 493 nm 时 g 亮、D 暗，故亮概率 **B(t)=N_g(t)**。设 x=A(a→g)、
   y=A(a→b)、Γ=x+y。
2. **耦合速率方程**：Ṅ_a=-ΓN_a，Ṅ_b=yN_a-βN_b，Ṅ_g=xN_a+βN_b，初值 N_a(0)=1、N_b(0)=N_g(0)=0。
   解得 N_a=e^(-Γt)，N_b=y/(β-Γ)·(e^(-Γt)-e^(-βt))，
   **B(t)=1-e^(-Γt)-y/(β-Γ)·(e^(-Γt)-e^(-βt))**。
   **关键点：g 由 a→g 直接布居 + b→g 回补两路共同填充；b 是"暗态储库"，其未衰完的布居把 B(t)
   压在纯指数 1-e^(-Γt) 之下，必须显式扣除。**
3. **三点拟合**：代 B(10)=0.2349、B(30)=0.5453、B(80)=0.8618，得 **Γ=3.00×10⁻² s⁻¹、
   y=3.00×10⁻³ s⁻¹**（三点自洽，残差 <0.1%）。
4. **寿命与分支**：τ_a=1/Γ=33.3 s；A(a→b)=y=3.00×10⁻³ s⁻¹；A(a→g)=x=Γ−y=2.70×10⁻² s⁻¹；
   **Br(a→g)=x/Γ=90.0%（主支）、Br(a→b)=y/Γ=10.0%**。
5. **跃迁类型（选择定则）**：5D5/2→6S1/2 为偶宇称间跃迁，E1 宇称禁戒；M1 要 ΔJ=0,±1，而
   5/2→1/2 是 ΔJ=2 故 M1 禁戒；E2 宇称守恒且允许 ΔJ=2，故 **a→g 主要为 E2 通道**。a→b 为
   5/2→3/2、ΔJ=1，M1 与 E2 均可贡献。
6. **杂散场诱导 E1 估算**：E=5 V/cm=500 V/m，d=2ea₀=1.695×10⁻²⁹ C·m，能隙
   ΔE=hc×1.20×10⁴ cm⁻¹=2.384×10⁻¹⁹ J，混合系数 η=dE/ΔE=3.56×10⁻⁸；二阶微扰诱导 E1 速率
   **A_ind≈η²·A(P→g)=(3.56×10⁻⁸)²×1.2×10⁸=1.5×10⁻⁷ s⁻¹**，与本征 Γ 比 **A_ind/Γ≈5.1×10⁻⁶**
   （ppm 级），故诱导 E1 **可忽略**。

# 步骤列表-reference

[1] 探测含义与速率模型：只开 493nm 时 B(t)=N_g；设 x=A(a→g)、y=A(a→b)、Γ=x+y。
[2] 耦合速率方程含 b→g 回补：Ṅ_a=-ΓN_a、Ṅ_b=yN_a-βN_b、Ṅ_g=xN_a+βN_b，解出 B(t)=1-e^(-Γt)-y/(β-Γ)(e^(-Γt)-e^(-βt))。
[3] 三点拟合 B(10/30/80)=0.2349/0.5453/0.8618 → Γ=3.00e-2、y=3.00e-3（残差<0.1%）。
[4] τ_a=1/Γ=33.3 s；A(a→g)=2.70e-2（90.0% 主支）、A(a→b)=3.00e-3（10.0%）。
[5] 选择定则：a→g 偶宇称间跃迁 E1 禁戒、ΔJ=2 M1 禁戒 → E2 主导；a→b（ΔJ=1）M1+E2。
[6] 诱导 E1：η=dE/ΔE=3.56e-8，A_ind≈η²·A(P→g)≈1.5e-7 s⁻¹，A_ind/Γ≈5.1e-6（ppm）→ 可忽略。

## Grading Criteria

- [ ] 建立含 b→g 回补的耦合速率方程，识别 B(t)=N_g 由两路填充、b 为暗态储库须显式扣除（不得写成纯单指数 1-e^(-Γt)）。
- [ ] 由三点数据拟合出 Γ=3.00×10⁻² s⁻¹、y=3.00×10⁻³ s⁻¹，给出 τ_a=33.3 s。
- [ ] **a→g 为主支（90.0%），a→b 为次支（10.0%）——不得搞反。**
- [ ] 正确用选择定则判 a→g 主要为 E2、a→b 为 M1+E2。
- [ ] 诱导 E1 用二阶微扰 η²·A(P→g) 估算，得 A_ind/Γ≈5×10⁻⁶，判"可忽略"。

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。本 grade() 已内联全部锚点与阈值，不依赖外部 meta。

> **v2 梯度评分**：本题最终答复分不再对核心结论做 0/命中二值，而按「量级台阶」给分——
> τ_a 命中 0.30 / 量级对偏 15–100%（如 49.8 s）半分 0.15 / 量级错 0；分支方向对且 90/10 得 0.20 /
> 方向对值偏（如 60/40）0.10 / 搞反 0；诱导 E1 可忽略+量级 5e-6 得 0.20 / 可忽略量级错 0.10。
> 目的：把「部分对」的中段模型从底部塌陷带里拉出来。

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
        anchor_region = final_msg.split(ANSWER_TAG, 1)[1][:400]
    region_l = anchor_region.lower()

    def _nums(pattern, text):
        vals = []
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            seg = text[m.end():m.end() + 40]
            sm = re.search(
                r'([0-9]*\.?[0-9]+)\s*(?:[×x*]\s*10\s*\^?\{?\s*([-+]?\d+)\s*\}?|e\s*([-+]?\d+))?',
                seg, flags=re.IGNORECASE)
            if sm and sm.group(1):
                v = float(sm.group(1))
                exp = sm.group(2) or sm.group(3)
                if exp:
                    v *= 10 ** int(exp)
                vals.append(v)
        return vals

    def _relerr(v, target):
        return abs(v - target) / abs(target) if (v is not None and target != 0) else None

    out = {}

    # ---- τ_a 量级台阶（目标 33.3 s）----
    tau_vals = _nums(r'(?:τ\s*_?\s*a|tau_?a|a\s*态?\s*寿命|寿命)\s*[:=≈约]?', full)
    tau_errs = [e for e in (_relerr(v, 33.3) for v in tau_vals) if e is not None]
    tau_min = min(tau_errs) if tau_errs else None
    if tau_min is not None and tau_min <= 0.15:
        tau_step = 0.30
    elif tau_min is not None and tau_min <= 1.0:
        tau_step = 0.15
    else:
        tau_step = 0.0

    # ---- 主支归属量级台阶 ----
    says_ag_dominant = bool(re.search(
        r'(a\s*[→\-]+\s*g|a→g)[^\n]{0,40}(90(\.0)?\s*%|0\.90|主支|主要?分支|dominant)', full_l))
    says_swapped = bool(re.search(
        r'(a\s*[→\-]+\s*b|a→b)[^\n]{0,40}(8[0-9](\.\d)?\s*%|0\.8[0-9]|主支|dominant)', full_l)) \
        or bool(re.search(r'(a\s*[→\-]+\s*g|a→g)[^\n]{0,40}(1[0-9](\.\d)?\s*%|0\.1[0-9])', full_l))
    ag_direction = bool(re.search(
        r'(a\s*[→\-]+\s*g|a→g)[^\n]{0,40}(主支|主要|较大|更大|larger|dominant|[5-9][0-9](\.\d)?\s*%)', full_l))
    if says_ag_dominant and not says_swapped:
        branch_step = 0.20
    elif ag_direction and not says_swapped:
        branch_step = 0.10
    else:
        branch_step = 0.0

    # ---- 诱导 E1 量级台阶 ----
    e1_negligible = bool(re.search(r'(可忽略|忽略|negligible|ppm)', region_l)) \
        or bool(re.search(r'(诱导\s*e1|induced\s*e1|杂散场)[^\n]{0,60}(可忽略|忽略|negligible)', full_l))
    ratio_vals = _nums(r'(?:a_?\s*ind\s*/\s*[γΓ]|a_?ind\s*/\s*gamma|比例?|ratio)\s*[:=≈约]?', full_l)
    ratio_ok = any(1e-7 <= v <= 5e-5 for v in ratio_vals) \
        or ("10^-6" in full or "10⁻⁶" in full or "e-6" in full_l or "5.1" in full)
    if e1_negligible and ratio_ok:
        e1_step = 0.20
    elif e1_negligible:
        e1_step = 0.10
    else:
        e1_step = 0.0

    non_empty = 1.0 if len(full.strip()) >= 30 else 0.0
    refusal = bool(re.search(r"(无法回答|不能回答|不会做|拒绝作答|i cannot|i can't|cannot solve)", full_l))
    not_refusal = 0.0 if refusal else 1.0
    has_unit = 1.0 if re.search(r"(s\s*\^?\{?\s*-?\s*1|s⁻¹|s\^-1|/\s*s|\d\s*s\b)", full_l) else 0.0

    final_answer = 0.10 * non_empty + 0.10 * not_refusal + tau_step + branch_step \
        + e1_step + 0.10 * has_unit
    out["non_empty_answer"] = non_empty
    out["not_refusal"] = not_refusal
    out["tau_step"] = round(tau_step, 4)
    out["branch_step"] = round(branch_step, 4)
    out["e1_step"] = round(e1_step, 4)
    out["has_unit"] = has_unit

    # numeric 锚点命中率（4 锚点：τ_a、A(a→g)/主支、A(a→b)/10%、A_ind/Γ）
    ab_ok = bool(re.search(r'(a\s*[→\-]+\s*b|a→b)[^\n]{0,40}(10(\.0)?\s*%|0\.10)', full_l)) \
        or any(_relerr(v, 3.0e-3) is not None and _relerr(v, 3.0e-3) <= 0.15
               for v in _nums(r'(a\s*[→\-]+\s*b|a→b)\s*[:=≈约]?', full_l))
    anchors = [tau_step >= 0.30, branch_step >= 0.20, ab_ok, ratio_ok and e1_negligible]
    out["numeric_anchor_hit_rate"] = round(sum(1 for h in anchors if h) / 4.0, 4)

    out["auto_final_answer_score"] = round(final_answer, 4)
    return out
```

## LLM Judge Rubric

大模型评分负责**过程、概念与逻辑**，不重复判定代码已覆盖的最终数值命中。本题为**单 gate 高防御题**，
逻辑分按 v2 收敛为「主支归属四级台阶」（gate 专列、占逻辑分 60%）；步骤分与 gate 对错**解耦**，
只评方法动作是否执行到位。

### Criterion 1: 步骤分（方法动作，Weight: 1/3）

与主支归属对错解耦，S1–S5 各 0.20 累加：

- **S1 探测含义与速率模型（0.20）**：说明只开 493nm 时 B(t)=N_g，设 x=A(a→g)、y=A(a→b)、Γ=x+y。
- **S2 耦合方程与解析解（0.20）**：写出含 b→g 回补的三方程并解出 N_a、N_b、B(t)。
- **S3 三点拟合方法（0.20）**：以 B(10/30/80) 联立拟合 Γ、y（方法到位即给，数值偏不在此扣）。
- **S4 寿命/分支代数（0.20）**：τ_a=1/Γ、A(a→b)=y、A(a→g)=Γ−y、Br=x/Γ 代数正确。
- **S5 选择定则 + 诱导 E1 二阶微扰（0.20）**：a→g 判 E2、a→b 判 M1+E2；诱导 E1 用 η²·A(P→g) 估算。

> 一个 gate 栽了但方法框架漂亮的模型，步骤分仍应高于"方法也崩"的模型。

### Criterion 2: 逻辑分（Weight: 1/3，核心防御位）

主支归属四级台阶（占逻辑分 0.60）+ 诱导 E1 阶数（0.20）+ 自洽性（0.20）：

**主支归属 gate（0.60）**
- **G4（0.60）**：正确耦合方程反演 → a→g 90% 主支，且**显式点破 b 暗态储库延迟回补**须扣除。
- **G3（0.36）**：主支方向对（a→g 较大）但数值偏 / 机制点破不足。
- **G2（0.24）**：建了多通道方程但**主支搞反**（把 a→b 当主支，EB5.1 那种走法）。
- **G1（0.00）**：单指数硬套 / 漏 b→g 回补 / 编造分支。

**诱导 E1 阶数（0.20）**：用二阶微扰 η²（而非一阶 ∝η）估算诱导 E1 速率给满；一阶或漏估给 0。
**自洽性（0.20）**：三点拟合残差自洽、τ/分支/E1 各结论前后不矛盾；拟合不能复现三点则大扣。

> 参考档位：G4+二阶+自洽 ≈ 1.0；主支方向对值偏（G3）而 E1/自洽薄弱 ≈ 0.5；主支搞反或单指数硬套
> → gate 落 G2/G1，逻辑分显著低于 0.5。（即便脚本最终答复分因某分项蒙对给了分，逻辑分仍独立判。）

> **最终答复分（脚本评，权重 1/3）** 不在此 rubric 内，由 `grade()` 客观给出（τ_a + 主支 + 诱导 E1
> 量级梯度加权）。LLM 不重复评最终答复分。
