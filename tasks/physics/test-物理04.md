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

    _NUM = (r'(?<![\d.])([0-9]*\.?[0-9]+)\s*'
            r'(?:[×x*]\s*10\s*\^?\{?\s*([-+]?\d+)\s*\}?|e\s*([-+]?\d+))?')

    def _nums(pattern, text, window=40):
        """收集标签后邻接窗内的**全部**数值，连带每个数前后的上下文串。

        返回 (值, 数后 20 字符, 标签与数之间的间隔串)。后两项供单位与「同一条赋值链」判定。

        旧实现每个标签只取窗内第一个数，这是假阴性来源：`τ_a = 1/Γ = 33.3 s` 里
        第一个数是 `1/Γ` 的 `1`，真正的结论 33.3 被顶掉 —— 本题自己的 SFT 标准答案
        因此只拿半分。同一个坑物理03 的 `extract_plain/extract_scientific` 已经修过。
        """
        vals = []
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            seg = text[m.end():m.end() + window]
            for sm in re.finditer(_NUM, seg, flags=re.IGNORECASE):
                v = float(sm.group(1))
                exp = sm.group(2) or sm.group(3)
                if exp:
                    v *= 10 ** int(exp)
                vals.append((v, seg[sm.end():sm.end() + 20], seg[:sm.start()]))
        return vals

    def _relerr(v, target):
        return abs(v - target) / abs(target) if (v is not None and target != 0) else None

    def _hit(vals, target, tol):
        return any(_relerr(v, target) <= tol for v, _tail, _gap in vals)

    out = {}

    # ---- τ_a 量级台阶（目标 33.3 s）----
    # 按白拿口径收紧两处：
    # ①τ 值必须紧跟**秒量纲**。裸数会把 `τ_a=1/Γ` 的 `1` 和 `Γ=3.00×10⁻²` 一起收进来，
    #   而 `1` 是整数、任何数值扰动都动不到它，它对 33.3 的相对差 0.97 恰好落在旧半分带内
    #   → 每份答复白拿 0.15（判的是「写了个数」不是「算对了」）。
    # ②半分带由「相对差 ≤1.0」改成「倍数落在 0.5~1.5 之间」。相对差 ≤1.0 对任何小于
    #   2×33.3 的正数都成立（是条半直线，向下无界），×0.31/×0.19/×0.077 的扰动全落在
    #   里面、结构上压不掉；按倍数两侧算才是「量级对」的本意（49.8 s=1.50× 仍在带内）。
    # ③τ 值必须与 τ 标签处在**同一条赋值链**上：标签与数之间不许出现中文或全角标点。
    #   `τ_a=…=66.66 s . 对于 t=30 s ：` 里的 `t=30 s` 也带秒量纲、30/33.3=0.90 正落在
    #   满档带内，窗口一长就整份白拿满档（run4 实测）。题面给的 B(10/30/80 s) 三个时间点
    #   都是整数、数值扰动动不到，必须靠「跨句就不算」把它们挡在窗外。
    _SEC = re.compile(r'^[\\\s,;:!>{]{0,12}(?:mathrm|text|rm)?[\s{]{0,4}(?:s|秒)'
                      r'(?![\w^⁻]|\s*\^|\s*-\s*1)')
    _BREAK = re.compile(r'[一-鿿　-〿＀-￯]')  # 中文与全角标点
    tau_vals = [v for v, tail, gap in _nums(
        r'(?:τ\s*_?\s*a|tau_?a|a\s*态?\s*寿命|寿命)\s*[:=≈约]?', full, 80)
        if _SEC.match(tail) and not _BREAK.search(gap)]
    tau_ratio = [v / 33.3 for v in tau_vals if v > 0]
    if any(abs(r - 1.0) <= 0.15 for r in tau_ratio):
        tau_frac = 1.0
    elif any(0.5 <= r <= 1.5 for r in tau_ratio):
        tau_frac = 0.5
    else:
        tau_frac = 0.0

    # ---- 主支归属量级台阶 ----
    # 收紧两处：
    # ①分支窗不许跨 `；`/`、`/`，` 等分隔符。旧窗从 a→g 起算 40 字符，长到能吃进后面
    #   a→b 的 10.0%，把题面格式行（`A(a→g)=…（Br…）；A(a→b)=…（Br…）`）诱导出来的
    #   **正确**写法误判成「主支搞反」—— 本题自己的 SFT 标准答案实测只拿 0.65 就是它。
    # ②两级台阶都要求数值同现。旧版 `主支|主要|较大|dominant` 是纯关键词支，数值全错时
    #   一字不动就给分；主支归属是本题核心防御位，只认结论词等于没判。
    # ③裸小数支必须先挂上 `Br`/分支比 标签。`0.5~0.9` 这个区间在本题里同时是「多数分支」
    #   和「被扰动过的部分速率」：run5 的 `A(a→g)=2.70×10⁻²` 在含整数档被扰成
    #   `A(a→g)=0.513`，无标签的裸小数支直接把它当成「a→g 占多数」给了半档。
    #   百分号支不需要这层保护（`%` 自带分支比语义）。
    _S = r'[^\n；;、，,]'
    AG = r'(?:a\s*[→\-]+\s*g|a→g)'
    AB = r'(?:a\s*[→\-]+\s*b|a→b)'
    _BR = r'(?:br|分支比|分支|branching)' + _S + r'{0,12}?'
    MAJ = (r'(?:(?<![\d.])90(?:\.\d+)?\s*\\?%'
           r'|' + _BR + r'(?<![\d.])0\.9(?:0\d*)?(?![\d]))')
    MIN = (r'(?:(?<![\d.])10(?:\.\d+)?\s*\\?%'
           r'|' + _BR + r'(?<![\d.])0\.1(?:0\d*)?(?![\d]))')
    MOST = (r'(?:(?<![\d.])[5-9][0-9](?:\.\d+)?\s*\\?%'
            r'|' + _BR + r'(?<![\d.])0\.[5-9]\d*(?![\d]))')

    def _win(label, pat, span=40):
        return bool(re.search(label + _S + r'{0,%d}?' % span + pat, full_l))

    says_ag_dominant = _win(AG, MAJ)
    says_swapped = (_win(AB, MAJ) or _win(AG, MIN)
                    or _win(AB, r'(?:主支|主要分支|dominant)', 24))
    ag_direction = _win(AG, MOST)
    if says_ag_dominant and not says_swapped:
        branch_frac = 1.0
    elif ag_direction and not says_swapped:
        branch_frac = 0.5
    else:
        branch_frac = 0.0

    # ---- 诱导 E1 量级台阶 ----
    # 收紧三处：
    # ①删掉 `or ("5.1" in full)` 与 `"10^-6"/"10⁻⁶"/"e-6" in full` 这几支裸子串锚 ——
    #   答复里任何位置出现 "5.1" 或任何 10^-6 都算命中，而指数落在扰动算子的保护区里、
    #   数值全错后一字不动 → 5/5 白拿满档 0.20。
    # ②「可忽略」不再单独给分：文字结论必须与数值锚同现（照化学03 rate_limiting_diffusion）。
    #   「可否忽略」是二值判断，光押一边不算算对。
    # ③容差带从 [1e-7, 5e-5]（宽三个数量级，×0.31 的扰动还落在里面）收成绕真值 ±15%，
    #   且满档要求 A_ind≈1.5×10⁻⁷ 与 A_ind/Γ≈5.1×10⁻⁶ **两个独立派生量同时**命中 ——
    #   一次数值扰动不可能把两个都打回原值（化学03 §6 的单锚教训）。
    IND = r'a\s*_?\s*\{?\s*(?:\\?(?:mathrm|text|rm)\s*\{)?\s*ind'
    ratio_vals = _nums(
        IND + r'[^0-9\n]{0,12}?(?:/|\}\s*\{)\s*\\?(?:gamma|[γΓ])\s*\}?\s*[:=≈约]?',
        full_l, 40)
    a_ind_vals = _nums(IND + r'[^0-9\n]{0,40}?[:=≈约]', full_l, 60)
    ratio_ok = _hit(ratio_vals, 5.1e-6, 0.15)
    a_ind_ok = _hit(a_ind_vals, 1.5e-7, 0.15)
    e1_negligible = bool(re.search(r'(可忽略|忽略|negligible|ppm)', region_l)) \
        or bool(re.search(r'(诱导\s*e1|induced\s*e1|杂散场)[^\n]{0,60}(可忽略|忽略|negligible)', full_l))
    if e1_negligible and ratio_ok and a_ind_ok:
        e1_frac = 1.0
    elif e1_negligible and (ratio_ok or a_ind_ok):
        e1_frac = 0.5
    else:
        e1_frac = 0.0

    non_empty = 1.0 if len(full.strip()) >= 30 else 0.0
    refusal = bool(re.search(r"(无法回答|不能回答|不会做|拒绝作答|i cannot|i can't|cannot solve)", full_l))
    not_refusal = 0.0 if refusal else 1.0
    has_unit = 1.0 if re.search(r"(s\s*\^?\{?\s*-?\s*1|s⁻¹|s\^-1|/\s*s|\d\s*s\b)", full_l) else 0.0

    # 白拿口径收紧（照化学03 `_SCORED` 的注释）：三项权重归零，只留在返回 dict 里
    # 当诊断项输出 ——
    #   · non_empty_answer / not_refusal：空答与拒答由 runner 层记 0，在 grade() 里
    #     再给一遍就是与题目无关的白拿（白拿项①）；
    #   · has_unit：「全文任何位置出现 s⁻¹」的裸单位存在性检查，数值全错也一字不动
    #     （白拿项②③）。秒量纲已作为 τ_a 结论值的**邻接条件**参与判定，不再单列计权。
    # 释放出的 0.10×3=0.30 按比例回填三个实质项：新权重 = 旧权重/(1−0.30)。
    # 三项全中仍是满分 1.0（(0.30+0.20+0.20)/0.70=1.0），真实分不因归零而下降。
    W_TAU, W_BRANCH, W_E1 = 0.30 / 0.70, 0.20 / 0.70, 0.20 / 0.70
    tau_step = W_TAU * tau_frac
    branch_step = W_BRANCH * branch_frac
    e1_step = W_E1 * e1_frac

    final_answer = tau_step + branch_step + e1_step
    out["non_empty_answer"] = non_empty
    out["not_refusal"] = not_refusal
    out["tau_step"] = round(tau_step, 4)
    out["branch_step"] = round(branch_step, 4)
    out["e1_step"] = round(e1_step, 4)
    out["has_unit"] = has_unit

    # numeric 锚点命中率（4 锚点：τ_a、A(a→g)/主支、A(a→b)/10%、A_ind/Γ）
    ab_ok = _win(AB, MIN) or any(
        _relerr(v, 3.0e-3) <= 0.15
        for v, _t, _g in _nums(AB + r'\s*[:=≈约]?', full_l))
    anchors = [tau_frac >= 1.0, branch_frac >= 1.0, ab_ok,
               ratio_ok and a_ind_ok and e1_negligible]
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
- **G2（0.24）**：建了多通道方程但**主支搞反**（把 a→b 当主支）。
- **G1（0.00）**：单指数硬套 / 漏 b→g 回补 / 编造分支。

**诱导 E1 阶数（0.20）**：用二阶微扰 η²（而非一阶 ∝η）估算诱导 E1 速率给满；一阶或漏估给 0。
**自洽性（0.20）**：三点拟合残差自洽、τ/分支/E1 各结论前后不矛盾；拟合不能复现三点则大扣。

> 参考档位：G4+二阶+自洽 ≈ 1.0；主支方向对值偏（G3）而 E1/自洽薄弱 ≈ 0.5；主支搞反或单指数硬套
> → gate 落 G2/G1，逻辑分显著低于 0.5。（即便脚本最终答复分因某分项蒙对给了分，逻辑分仍独立判。）

> **最终答复分（脚本评，权重 1/3）** 不在此 rubric 内，由 `grade()` 客观给出（τ_a + 主支 + 诱导 E1
> 量级梯度加权）。LLM 不重复评最终答复分。
