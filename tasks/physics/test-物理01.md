# 构造高质量-query

ITER 中性束注入器磁绝缘弯段中，考虑远离侧壁鞘层和边界有限回旋半径效应的体等离子体区域。
D+ 等离子体随半径 R=1.00 m 的环形磁力线运动，局部磁场 B=50.0 mT，密度 n=3.00×10^12 cm^-3，
电子温度 Te=12.0 eV，离子温度 Ti=4.00 eV，侧壁间距 6.00 cm 且绝缘，初始 Ey=0。设电子和 D+
均为各向同性 Maxwell 分布，无宏观平行流或束流成分；环形磁场满足局部托卡马克环向场近似 B∝1/R，
因此 |∇B|/B=1/R，且热平均梯度 B 漂移与曲率漂移同向相加。定义 +y 方向为 D+ 热平均梯度 B 漂移与
曲率漂移的方向，因此由两种粒子非均匀磁场漂移产生的电流取 +y 为正。取 e=1.602176634×10^-19 C，
mD=3.3435837724×10^-27 kg，me=9.1093837015×10^-31 kg，ε0=8.8541878128×10^-12 F·m^-1。

问 t=10.0 μs 时可否在体等离子体区域使用导引中心近似和准中性近似？利用绝缘侧壁的零法向总电流
条件，求自洽 dEy/dt、极化电流密度 jp，以及 t=10.0 μs 时 D+ 和电子的极化漂移速度。

请完整写出判据、推理与计算过程。最后单独用一行给出结论，格式为：
【结果】导引中心近似: 可用/不可用；准中性近似: 可用/不可用；dEy/dt=…；jp=…；vp,i(D+)=…；vp,e(电子)=…

# SFT标准-response

**最终结论：**
- **导引中心近似：可用**。热回旋半径 ρi≈8.17 mm、ρe≈0.234 mm 均 ≪ 磁场非均匀尺度 R=1.00 m；
  ρi/a≈0.27（a=3 cm 半壁距）虽不算极小，但题设限定"远离侧壁鞘层与边界有限回旋半径效应的体区"，故体区可用。
  离子回旋周期 2π/Ωi≈2.62 μs，t=10 μs≈3.8 个离子回旋周期，回旋平均意义下成立。
- **准中性近似：可用**。电子德拜长度 λDe≈14.9 μm ≪ 侧壁尺度 6 cm 与 R=1 m。
- **dEy/dt ≈ -7.66×10⁷ V·m⁻¹·s⁻¹**（自洽、常量）。
- **jp ≈ -3.08×10² A/m²（-y，恰好抵消 +y 的非均匀磁场漂移电流 jB≈+308 A/m²）**。
- **vp,i(D+) ≈ -6.40×10² m/s（-y）**；**vp,e(电子) ≈ +1.74×10⁻¹ m/s（+y）**。
- 附：Ey(10 μs)=(dEy/dt)·t ≈ -7.66×10² V/m。

正确推理链（基准 6 步）：

1. **单位换算 + 特征量**：B=5.00×10⁻² T，n=3.00×10¹⁸ m⁻³，a=3.00×10⁻² m，t=1.00×10⁻⁵ s，
   kTe=1.9226×10⁻¹⁸ J，kTi=6.4087×10⁻¹⁹ J。Ωi=eB/mD=2.40×10⁶ s⁻¹、Ωe=eB/me=8.79×10⁹ s⁻¹。
   热回旋半径用 vth,⊥=√(2kT/m)：ρi=√(2mD·kTi)/(eB)=8.17×10⁻³ m、ρe=√(2me·kTe)/(eB)=2.34×10⁻⁴ m。
2. **导引中心近似判定**：ρi、ρe ≪ R=1 m（∇B 尺度）；ρi/a≈0.27 但题设限定体区、排除边界有限回旋半径
   效应；2π/Ωi≈2.62 μs、t≈3.8 个回旋周期 → 体区导引中心近似**可用**。
3. **准中性近似判定**：λDe=√(ε0·kTe/(n·e²))=1.49×10⁻⁵ m ≪ 6 cm、R=1 m → 体区准中性**可用**；
   横向电场靠边界表面电荷建立。
4. **非均匀磁场漂移电流**：各向同性 Maxwell 有 ⟨v⊥²⟩=2kT/m、⟨v∥²⟩=kT/m。B∝1/R、grad-B 与曲率同向相加时
   单粒子热平均漂移 vB,s=[m⟨v⊥²⟩/2+m⟨v∥²⟩]/(qsBR)=**2kTs/(qsBR)**。D+ 沿 +y、电子沿 -y，但两者电流**均沿 +y**，
   故 **jB=Σ ns qs vB,s = 2n(kTi+kTe)/(BR) ≈ +3.08×10² A/m²**（≈308）。
5. **绝缘壁零净电流闭合**：E×B 漂移对离子、电子相同，**不产生净电流**；随时间变化的 Ey 产生极化漂移
   vp,s=ms/(qsB²)·dEy/dt，极化电流 jp=Σ ns qs vp,s=**n(mD+me)/B²·dEy/dt**。绝缘壁法向净电流为零 ⇒ jp+jB=0
   ⇒ **dEy/dt=-jB·B²/[n(mD+me)]**。代入 n(mD+me)/B²=4.013×10⁻⁶，得 **dEy/dt≈-7.66×10⁷ V·m⁻¹·s⁻¹**；
   于是 **jp=-jB≈-3.08×10² A/m²（-y）**，Ey(t)=(dEy/dt)t≈-7.66×10² V/m。
6. **极化漂移速度（离子主导）**：vp,i=mD/(eB²)·dEy/dt≈**-6.40×10² m/s（-y）**；
   vp,e=me/(-eB²)·dEy/dt≈**+1.74×10⁻¹ m/s（+y）**（因 me≪mD 故电子极化漂移可忽略地小）。
   校验：n·e·(vp,i-vp,e)≈-3.08×10² A/m²，与 jp 一致。位移电流 ε0·dEy/dt≈-6.8×10⁻⁴ A/m²，仅为粒子极化电流的 2.2×10⁻⁶。

# 步骤列表-reference

[1] 单位换算 + 特征量：Ωi≈2.4e6 s⁻¹，ρi=√(2mD·kTi)/(eB)≈8.2 mm、ρe≈0.23 mm、λDe≈14.9 μm。
[2] 两近似判定：ρ≪R=1 m + 回旋周期 2π/Ωi≈2.62 μs → 导引中心可用；λDe≪壁距 6 cm → 准中性可用。
[3] 热平均漂移：各向同性 Maxwell 取 ⟨v⊥²⟩=2kT/m、⟨v∥²⟩=kT/m，得 vB,s=2kTs/(qsBR)。
[4] 非均匀磁场漂移电流两粒子同向相加 jB=2n(kTi+kTe)/(BR)≈+308 A/m²（+y）。
[5] 绝缘壁零净电流闭合：E×B 无净电流，jp+jB=0 → dEy/dt=-jB·B²/[n(mD+me)]≈-7.66e7、jp≈-308 A/m²（-y）。
[6] 极化漂移离子主导：vp,i=mD/(eB²)·dEy/dt≈-640 m/s（-y）、vp,e≈+0.17 m/s（+y）；n·e·(vp,i-vp,e)=jp 校验。

## Grading Criteria

- [ ] 两近似均判"可用"，并给出 ρ≪R（ρi≈8.2 mm）、λDe≪壁距（≈14.9 μm）的量级判据。
- [ ] 各向同性 Maxwell 下取 ⟨v⊥²⟩=2kT/m、⟨v∥²⟩=kT/m，grad-B+曲率同向相加得 vB,s=2kTs/(qsBR)。
- [ ] 两粒子非均匀磁场漂移电流**同向相加** jB=2n(kTi+kTe)/(BR)≈308 A/m²（+y），不是相减。
- [ ] 识别 E×B **无净电流**，绝缘壁零净电流由**极化电流**平衡漂移电流：jp=-jB，dEy/dt≈-7.66×10⁷。
- [ ] 极化漂移**离子主导**：vp,i≈-6.4×10² m/s（-y）、vp,e≈+0.17 m/s（+y），电子极化漂移未写成同量级。
- [ ] 可回代校验 n·e·(vp,i-vp,e)=jp。

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

    _SUP = str.maketrans({c: d for c, d in zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")})

    def _normalize(t):
        """统一上标与 LaTeX 分式，便于 _nums 抓「符号=科学计数值」。

        写法容错（不做容错会把「表述差异」记成「答错」，5 次答复集体假阴性）：
          - 结论行普遍写 `dEy/dt=-7.66×10⁷`（Unicode 上标），原正则只认
            `10^7`/`10^{7}`，5 次全部漏判；
          - 正文里写 `\\frac{dE_y}{dt}=...`，`}{` 隔开后 `dEy/dt` 一处都匹配不到，
            展平成 `dE_y/dt` 才能对上；
          - `\\dot E_y` 是同一个量的另一种写法，一并归一。
        """
        t = t.replace("−", "-").replace("–", "-").replace("—", "-")
        t = re.sub(r"10\s*([⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+)",
                   lambda m: "10^" + m.group(1).translate(_SUP), t)
        t = re.sub(r"\\[tdc]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\1/\2", t)
        t = re.sub(r"\\dot\s*\{?\s*E\s*\}?\s*_?\{?\s*y\s*\}?", "dEy/dt", t)
        t = t.replace("\\times", "×").replace("\\approx", "≈")
        for _ in range(3):
            t = re.sub(r"\\(?:boxed|text|mathrm|mathbf|operatorname|rm|bf|it)"
                       r"\s*\{([^{}]*)\}", r"\1", t)
        return t.replace("$", "").replace("**", "")

    assistant_msgs = [_normalize(_content(m)) for m in transcript
                      if m.get("role") == "assistant"]
    full = "\n".join(assistant_msgs)
    full_l = full.lower()
    final_msg = assistant_msgs[-1] if assistant_msgs else ""

    anchor_region = final_msg
    if ANSWER_TAG in final_msg:
        anchor_region = final_msg.split(ANSWER_TAG, 1)[1][:400]

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

    def _mag_ok(v, target, tol=0.15):
        return v is not None and target != 0 and abs(abs(v) - abs(target)) / abs(target) <= tol

    out = {}

    dey_vals = _nums(r'(?:d\s*e\s*_?\s*y\s*/\s*d\s*t|de_?y/dt|dey/dt|电场变化率|电场变化速率)\s*[:=≈约]?', full_l)
    dey_hit = any(_mag_ok(v, 7.66e7) for v in dey_vals)

    jp_vals = _nums(r'(?:j\s*_?\s*p|jp|极化电流密度|极化电流)\s*[:=≈约]?', full_l)
    jp_hit = any(_mag_ok(v, 308.0) for v in jp_vals)

    # 赋值号设为必需：原来 `[:=≈约]?` 可选，闭合校验里的 `n·e·(vp,i-vp,e)≈-3.08×10²`
    # 会让 `vp,e)` 也命中并抓到 308，把「电子极化漂移量级写错」的陷阱位误触发
    # （连 SFT 标准答案都被判 vpi_hit=0）。只认真正的「符号=数值」写法。
    vpi_vals = _nums(r'(?<![-−])(?:v\s*_?\s*p\s*,?\s*i|vp,?i|v_?pi|d\+?\s*极化漂移|离子极化漂移)'
                     r'(?:\([^)]{0,6}\))?\s*[:=≈约]', full_l)
    vpi_hit = any(_mag_ok(v, 640.0) for v in vpi_vals)

    vpe_vals = _nums(r'(?<![-−])(?:v\s*_?\s*p\s*,?\s*e|vp,?e|v_?pe|电子极化漂移)'
                     r'(?:\([^)]{0,6}\))?\s*[:=≈约]', full_l)
    vpe_hit = any(_mag_ok(v, 0.174, 0.30) for v in vpe_vals)
    vpe_wrong_order = any(abs(v) > 10.0 for v in vpe_vals)

    gc_usable = bool(re.search(r'(导引中心|导心|guiding[\s-]?center)[^\n。；;]{0,30}(可用|成立|适用|满足|有效)', full_l))
    qn_usable = bool(re.search(r'(准中性|quasi[\s-]?neutral)[^\n。；;]{0,30}(可用|成立|适用|满足|有效)', full_l))
    both_usable = gc_usable and qn_usable
    rho_ok = ("8.1" in full or "8.2" in full or "8.17" in full) or bool(re.search(r'ρ\s*_?\s*i', full_l)) \
             or ("回旋半径" in full)
    lde_ok = ("14.9" in full or "1.49" in full or "15 μm" in full_l or "15μm" in full_l) \
             or ("德拜" in full) or ("λde" in full_l) or ("λ_de" in full_l)
    approx_quant = rho_ok and lde_ok

    non_empty = 1.0 if len(full.strip()) >= 30 else 0.0
    refusal = bool(re.search(r"(无法回答|不能回答|不会做|拒绝作答|i cannot|i can't|cannot solve)", full_l))
    not_refusal = 0.0 if refusal else 1.0

    core = 0.25 * (1.0 if dey_hit else 0.0) \
         + 0.25 * (1.0 if (vpi_hit and not vpe_wrong_order) else 0.0)
    has_unit = 1.0 if re.search(
        r"(v\s*[·⋅]?\s*m\s*\^?\{?\s*-?\s*1\s*\}?\s*[·⋅]?\s*s|v/\(?m\s*[·⋅]?\s*s\)?|"
        r"v\s*m⁻¹\s*s⁻¹|a\s*/\s*m\s*\^?\{?\s*2|a\s*m\s*\^?\{?\s*-?\s*2|a/m²|m\s*/\s*s|m\s*s\s*\^?\{?\s*-?\s*1)",
        full_l) else 0.0
    approx_final = 0.15 if (both_usable and approx_quant) else (0.075 if both_usable else 0.0)

    final_answer = 0.10 * non_empty + 0.10 * not_refusal + core + 0.15 * has_unit + approx_final
    out["non_empty_answer"] = non_empty
    out["not_refusal"] = not_refusal
    out["dey_hit"] = 1.0 if dey_hit else 0.0
    out["vpi_hit"] = 1.0 if (vpi_hit and not vpe_wrong_order) else 0.0
    out["has_unit"] = has_unit
    out["both_approx_usable"] = round(approx_final, 4)

    anchors = [dey_hit, jp_hit, vpi_hit, vpe_hit and not vpe_wrong_order]
    out["numeric_anchor_hit_rate"] = round(sum(1 for h in anchors if h) / 4.0, 4)

    out["auto_final_answer_score"] = round(final_answer, 4)
    return out
```

## LLM Judge Rubric

大模型评分负责**过程、概念与逻辑**，不重复判定代码已覆盖的最终数值命中。

### Criterion 1: 近似判据 + 热平均漂移 + jB（Weight: 40%）

**Score 1.0**: 用 ρi/ρe≪R 与回旋周期判导引中心可用、λDe≪壁距判准中性可用（均给量级判据）；取 ⟨v⊥²⟩=2kT/m、⟨v∥²⟩=kT/m 得 vB,s=2kTs/(qsBR)；两粒子电流**同向相加** jB=2n(kTi+kTe)/(BR)≈308 A/m²（+y）。
**Score 0.5**: 近似结论对但只给结论未给量级判据，或热平均系数缺曲率项/漏 √2 因子致 jB 差 2 倍。
**Score 0.0**: 未给近似判据，或把两粒子电流相减（当成 kTi-kTe/近似为零）。

### Criterion 2: E×B 无净电流 → 极化电流平衡（Weight: 35%，核心防御位）

**Score 1.0**: 明确 E×B 对两粒子相同、不产生净电流，绝缘壁零净电流由**极化电流**平衡非均匀磁场漂移电流：jp=-jB，dEy/dt=-jB·B²/[n(mD+me)]≈-7.66×10⁷。
**Score 0.5**: 用到极化电流平衡但机制表述含糊，或 dEy/dt 数值/符号有一处含混。
**Score 0.0**: 误用 E×B 去平衡绝缘壁电流（踩 P5 陷阱），闭合逻辑错。

### Criterion 3: 极化离子主导 + 符号 + 自洽（Weight: 25%）

**Score 1.0**: mD≫me → 极化漂移/电流由离子主导、vp,e 极小；dEy/dt、jp、vp,i 符号（-y）正确；n·e·(vp,i-vp,e)=jp 校验一致。
**Score 0.5**: 离子主导识别对，但 vp,e 量级或某处符号含糊、无闭合校验。
**Score 0.0**: 把电子极化漂移写成与离子同量级，或 dEy/dt / vp,i 符号搞反。
