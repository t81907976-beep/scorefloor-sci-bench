# 构造高质量-query	
D-D中子发生器准直器涂层中,中子与涂层内某一核尺度团簇的相互作用可近似为中心势散射。这里的“团簇”指固定在材料中的核尺度重团簇,质量远大于中子质量,计算中可视为无限重固定散射中心,因此两体相对运动的约化质量取μ=m_n；入射中子的实验室能量即相对运动能量。忽略自旋、库仑作用与吸收,势能取实的球对称硬芯方阱形式:V(r)=∞,r<0.35 fm；V(r)=-45.0 MeV,0.35 fm<r<2.00 fm；V(r)=0,r>2.00 fm。入射中子能量E=2.00 MeV。取ℏc=197.3269804 MeV·fm,m_n c^2=939.5654205 MeV,由此自洽计算得ℏ²/(2m_n)=20.721 MeV·fm²。判定“需保留的分波”时,采用截断判据:若某一分波对总弹性截面的贡献(4π/k²)(2l+1)sin²δ_l<10^-3 barn,则可忽略。求本能量下需保留的分波、δ0和δ1、总弹性截面,并用光学定理作一致性检验；最后判定是否存在s波束缚态,若存在给出束缚能。
# SFT标准-response	
1. 运动学与波数:散射中心视为无限重,因此约化质量μ=m_n,实验室入射能量就是相对运动能量。取C=ℏ²/(2m_n)=20.721 MeV·fm²。外区波数为k=sqrt(E/C)=sqrt(2.00/20.721)=0.3108 fm^-1。阱区散射态波数为q=sqrt((E+45.0)/C)=sqrt(47.0/20.721)=1.506 fm^-1。硬芯半径a=0.35 fm,阱外半径R=2.00 fm,阱宽d=R-a=1.65 fm。

2. 分波匹配条件:对l分波,外区可写为u_l^out=A[j_l(kr)-tanδ_l n_l(kr)]；阱区需满足硬芯边界u_l(a)=0,因此可写为u_l^in=B[j_l(qr)n_l(qa)-n_l(qr)j_l(qa)]。在r=R处连续u_l和u_l',令L_l=u_l^in'(R)/u_l^in(R),得到tanδ_l=[k j_l'(kR)-L_l j_l(kR)]/[k n_l'(kR)-L_l n_l(kR)],其中球贝塞尔函数导数是对其自变量求导。

3. s波相移:l=0时可直接用硬芯边界写成u_in=A sin[q(r-a)],u_out=B sin(kr+δ0)。在R处匹配对数导数:q cot(qd)=k cot(kR+δ0)。因此δ0=arctan[(k/q)tan(qd)]-kR,取主值并允许相移按π等价。代入qd=1.506×1.65≈2.485,kR≈0.6216,得δ0≈-0.779 rad。

4. p波相移:对l=1使用上述球贝塞尔匹配。数值代入qa≈0.527,qR≈3.012,kR≈0.622,得到内区对数导数L_1≈-0.75 fm^-1,进而tanδ1≈0.70,所以δ1≈+0.611 rad。

5. 截断判据:每个分波贡献为σ_l=(4π/k²)(2l+1)sin²δ_l。这里4π/k²≈130.1 fm²=1.301 barn。题设阈值为10^-3 barn=0.1 fm²。l=0、l=1贡献远大于0.1 fm²；l=2计算得到δ2约为4×10^-4 rad量级,其贡献约10^-6 barn,远小于阈值；更高l更小。因此本能量下保留s波和p波,即l=0,1。

6. 总弹性截面:sin²δ0≈sin²(0.779)≈0.494,sin²δ1≈sin²(0.611)≈0.329。于是Σ=(2l+1)sin²δ_l≈1×0.494+3×0.329≈1.48。σ_el=(4π/k²)Σ≈130.1×1.48 fm²≈1.92×10^2 fm²。由于1 barn=100 fm²,故σ_el≈1.92 barn。

7. 光学定理检验:实势无吸收,故σ_tot=σ_el。分波散射振幅满足f(0)=k^-1 Σ_l(2l+1)e^{iδ_l}sinδ_l,因此Im f(0)=k^-1 Σ_l(2l+1)sin²δ_l≈1.48/0.3108≈4.76 fm。光学定理给出σ_tot=(4π/k)Im f(0)≈(4π/0.3108)×4.76 fm²≈1.92×10^2 fm²≈1.92 barn,与部分波求和一致。

8. s波束缚态:令束缚能量E=-B,B>0。外区衰减常数κ=sqrt(B/C),阱区波数α=sqrt((45.0-B)/C)。s波硬芯边界仍给u_in∝sin[α(r-a)],外区u_out∝exp[-κ(r-R)]。在R处匹配对数导数得α cot(αd)=-κ,并有α²+κ²=45.0/C。令x=αd,β=d sqrt(45.0/C)≈2.432,则束缚态方程等价于x=β sin x,且物理解位于π/2<x<π。该区间有且只有一个根,数值x≈2.10,因此α≈x/d≈1.27 fm^-1。束缚能B=45.0-Cα²≈11.4 MeV。所以存在一个s波束缚态,能级相对于阱外零势能为E≈-11.4 MeV。
# 步骤列表-reference
1：散射中心视为无限重，约化质量 $\mu=m_n$，外区波数 $k=\sqrt{E/C}=0.3108\ \text{fm}^{-1}$，阱区散射态波数 $q=\sqrt{(E+45.0)/C}=1.506\ \text{fm}^{-1}$，其中 $C=\hbar^2/(2m_n)=20.721\ \text{MeV}\cdot\text{fm}^2$；硬芯半径 $a=0.35\ \text{fm}$，阱外半径 $R=2.00\ \text{fm}$。

2：s 波（$l=0$）匹配——$q\cot(qd)=k\cot(kR+\delta_0)$，$d=R-a=1.65\ \text{fm}$，解得 $\delta_0\approx-0.779\ \text{rad}$；p 波（$l=1$）由球贝塞尔函数在 $r=R$ 处匹配 $u_l$ 与 $u_l'$ 得 $\delta_1\approx+0.611\ \text{rad}$。

3：截断判据——$4\pi/k^2\approx130.1\ \text{fm}^2=1.301\ \text{barn}$，阈值 $10^{-3}\ \text{barn}$；$l=0,1$ 贡献远大于阈值，$l=2$ 贡献 $\sim10^{-6}\ \text{barn}$ 可忽略，故保留 $s$ 波和 $p$ 波。

4：总弹性截面 $\sigma_{\text{el}}=(4\pi/k^2)\sum_l(2l+1)\sin^2\delta_l=1.301\times(1\times0.494+3\times0.329)\approx1.92\ \text{barn}$。

5：光学定理检验——$\operatorname{Im}f(0)=k^{-1}\sum_l(2l+1)\sin^2\delta_l\approx4.76\ \text{fm}$，$\sigma_{\text{tot}}=(4\pi/k)\operatorname{Im}f(0)\approx1.92\ \text{barn}$，与部分波求和一致。

6：$s$ 波束缚态——令 $E=-B$，$\kappa=\sqrt{B/C}$、$\alpha=\sqrt{(45.0-B)/C}$，匹配对数导数得 $\alpha\cot(\alpha d)=-\kappa$ 且 $\alpha^2+\kappa^2=45.0/C$；化为 $x=\beta\sin x$（$\beta=d\sqrt{45.0/C}\approx2.432$），在 $\pi/2<x<\pi$ 内有唯一解 $x\approx2.10$，$\alpha\approx1.27\ \text{fm}^{-1}$，束缚能 $B=45.0-C\alpha^2\approx11.4\ \text{MeV}$；存在 $s$ 波束缚态。

## Grading Criteria

- [ ] 约化质量陷阱：识别散射中心无限重 ⇒ μ=m_n（**不是 m_n/2**）、实验室入射能量即相对运动能量；取 C=ħ²/(2m_n)=20.721 MeV·fm²，外区 k=√(E/C)≈0.3108 fm⁻¹、阱区 q=√((E+45.0)/C)≈1.506 fm⁻¹。
- [ ] 硬芯边界处理：内区波函数在 r=a=0.35 fm 处为零，s 波取 u_in∝sin[q(r-a)]（移位宗量），阱宽 d=R−a=1.65 fm（**不是 R=2.00 fm**）。
- [ ] s 波相移：由 q cot(qd)=k cot(kR+δ0) 得 δ0≈−0.779 rad；p 波由球贝塞尔函数在 r=R 处匹配 u_l 与 u_l' 得 δ1≈+0.611 rad。
- [ ] 截断判据：σ_l=(4π/k²)(2l+1)sin²δ_l，4π/k²≈130.1 fm²=1.301 barn，阈值 10⁻³ barn；l=0、1 贡献远超阈值、l=2 贡献 ~10⁻⁶ barn 可忽略 ⇒ 保留 s 波和 p 波（l=0,1）。
- [ ] 总弹性截面：σ_el=(4π/k²)Σ(2l+1)sin²δ_l=1.301×(1×0.494+3×0.329)≈1.92 barn（≈192 fm²）。
- [ ] 光学定理一致性：实势无吸收 ⇒ σ_tot=σ_el，Im f(0)=k⁻¹Σ(2l+1)sin²δ_l≈4.76 fm，σ_tot=(4π/k)Im f(0)≈1.92 barn，与部分波求和自洽。
- [ ] s 波束缚态：α cot(αd)=−κ 且 α²+κ²=45.0/C ⇒ x=β sin x（β≈2.432），在 π/2<x<π 内**唯一根** x≈2.10，得 α≈1.27 fm⁻¹、束缚能 B≈11.4 MeV；存在一个 s 波束缚态。

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。本 grade() 已内联全部锚点与阈值，不依赖外部 meta。

```python
def grade(transcript: list, workspace_path: str, meta: dict) -> dict:
    import re

    def _content(m):
        c = m.get("content", "")
        if isinstance(c, list):
            return " ".join(seg.get("text", "") for seg in c if isinstance(seg, dict))
        return c if isinstance(c, str) else ""

    _SUP = str.maketrans({c: d for c, d in zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")})

    def _normalize(t):
        """剥掉 LaTeX 装饰并统一上标，便于 _nums 按符号抓值。

        写法容错（不做容错会把「表述差异」记成「答错」，5 次答复集体假阴性）：
          - `\\sigma_{\\text{el}}=...\\approx1.937\\ \\text{b}`：不剥 `{\\text{el}}`
            就会在符号与结论数值之间插进整段花括号，σ 一处都抓不到；
          - `\\text{Im}\\,f(0)`：不剥壳则光学定理判据永远为假；
          - `B_s\\approx11.45`、`E_B=...11.45`：束缚能标签写法多样；
          - Unicode 下标 `δ₀`/`δ₁` 归一成 `δ0`/`δ1`，否则分波相移一处都匹配不到；
          - Unicode 上标 `10⁻⁷` 与 `\\times` 统一成 `10^-7`、`×`。
        """
        t = t.replace("−", "-").replace("–", "-").replace("—", "-")
        t = t.translate(str.maketrans({"₀": "0", "₁": "1", "₂": "2", "₃": "3",
                                       "₄": "4", "₅": "5"}))
        t = re.sub(r"10\s*([⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+)",
                   lambda m: "10^" + m.group(1).translate(_SUP), t)
        t = t.replace("\\times", "×").replace("\\cdot", " ")
        t = re.sub(r"\\(?:approx|simeq|cong|sim)", "≈", t)
        t = re.sub(r"\\[tdc]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"(\1)/(\2)", t)
        for _ in range(4):
            t = re.sub(r"\\(?:boxed|text|mathrm|mathbf|operatorname|rm|bf|it)"
                       r"\s*\{([^{}]*)\}", r"\1", t)
        t = re.sub(r"\\[,;:!> ]", " ", t)
        return t.replace("$", "").replace("**", "")

    assistant_msgs = [_normalize(_content(m)) for m in transcript
                      if m.get("role") == "assistant"]
    full = "\n".join(assistant_msgs)
    full_l = full.lower()

    def _nums(pattern, text, span=56):
        """收集标签后窗口内的**全部**数值，而不是只取紧邻的第一个。

        原实现只 re.search 一次：`k=\\sqrt{47.0/20.721}=1.50606` 抓到的是根号里的
        47.0、`tan δ₀=-0.987, δ₀≈-44.6°(-0.779 rad)` 抓到的是 tan 值，
        结论正确却判成算错。改为窗口内全量收集，由调用方按各自目标 any() 判命中。
        """
        vals = []
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            seg = text[m.end():m.end() + span]
            for sm in re.finditer(
                    r'([-+]?)\s*([0-9]*\.?[0-9]+)\s*'
                    r'(?:[×x*]\s*10\s*\^?\{?\s*([-+]?\d+)\s*\}?|e\s*([-+]?\d+))?',
                    seg, flags=re.IGNORECASE):
                if not sm.group(2):
                    continue
                v = float(sm.group(2))
                exp = sm.group(3) or sm.group(4)
                if exp:
                    v *= 10 ** int(exp)
                if sm.group(1) == '-':
                    v = -v
                vals.append(v)
        return vals

    def _nums_u(pattern, text, unit, span=56):
        """与 _nums 同样在标签后窗口内全量收集，但**只收紧跟单位的数值**。

        只放宽窗口不锚单位会走到另一个极端：窗口里 `(4π/k^2)`、`(2l+1)`、
        `代入qd=1.506×1.65≈2.485` 这些无关数字也被收进来，2 落进 1.92 的 8% 带、
        2.485 落进 2.3626 的 10% 带，于是把结论改错的答复照样判命中——检查项
        失去了「答错要扣分」的能力。相移必带 rad/°、截面必带 barn/fm²、
        束缚能必带 MeV，用单位把结论值和过程中的裸数字分开。
        """
        vals = []
        num = (r'([-+]?)\s*([0-9]*\.?[0-9]+)\s*'
               r'(?:[×x*]\s*10\s*\^?\{?\s*([-+]?\d+)\s*\}?|e\s*([-+]?\d+))?')
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            seg = text[m.end():m.end() + span]
            for sm in re.finditer(num + r'\s*\\?[,;: ]*\s*(?:' + unit + r')',
                                  seg, flags=re.IGNORECASE):
                if not sm.group(2):
                    continue
                v = float(sm.group(2))
                exp = sm.group(3) or sm.group(4)
                if exp:
                    v *= 10 ** int(exp)
                if sm.group(1) == '-':
                    v = -v
                vals.append(v)
        return vals

    _U_RAD = r'rad|弧度|°|\^\s*\\?\s*circ|\\circ|度'
    _U_AREA = r'barn|b(?![a-z])|fm\s*\^?\{?\s*2|fm²'
    _U_MEV = r'mev'

    def _mag_ok(v, target, tol=0.06):
        return v is not None and target != 0 and abs(abs(v) - abs(target)) / abs(target) <= tol

    out = {}

    # 外区波数 k≈0.3108 fm^-1（间接证实 μ=m_n 而非 m_n/2；若误用约化质量 k 会差 √2）
    k_vals = _nums(r'(?<![a-z])k\s*[:=≈约]', full_l)
    k_hit = any(_mag_ok(v, 0.3108) for v in k_vals)

    # 阱区波数 q≈1.506 fm^-1。答复普遍把阱内波数记作 K（大写）而非题解的 q，
    # full 已 lower()，两者不可区分；但 k≈0.311 与 q≈1.506 相差近 5 倍，
    # 用 any() 按各自目标判命中不会互相污染，故记号一并接受。
    q_vals = _nums(r'(?<![a-z])(?:q|k(?:\s*_?\s*in)?)\s*[:=≈约]', full_l)
    q_hit = any(_mag_ok(v, 1.506) for v in q_vals)

    # s 波相移 δ0≈-0.779 rad（≈-44.6°，或等价支 2.363 rad≈135.4°）。
    # 相移只定义到 mod π：答复多按 Levinson 定理取 (0,π) 内的等价支
    # δ0=π-0.779=2.363 rad（135.4°），与 -0.779 是同一个相移，只认 -0.779
    # 会把「取物理支表述」记成算错。数值必须紧跟 rad/° 才计入，否则窗口里的
    # `代入qd=1.506×1.65≈2.485` 会假冒 2.363。
    d0_vals = _nums_u(r'(?:δ\s*_?\s*0|delta\s*_?\s*0|δ0|相移\s*δ?\s*0|s\s*波相移)\s*[:=≈约]?',
                      full_l, _U_RAD)
    d0_hit = any(_mag_ok(v, 0.779, 0.10) or _mag_ok(v, 2.3626, 0.10)
                 or _mag_ok(v, 44.6, 0.10) or _mag_ok(v, 135.4, 0.10)
                 for v in d0_vals)

    # p 波相移 δ1≈+0.611 rad（≈35.0°）
    d1_vals = _nums_u(r'(?:δ\s*_?\s*1|delta\s*_?\s*1|δ1|p\s*波相移)\s*[:=≈约]?',
                      full_l, _U_RAD)
    d1_hit = any(_mag_ok(v, 0.611, 0.10) or _mag_ok(v, 35.0, 0.10) for v in d1_vals)

    # 总弹性截面 σ_el≈1.92 barn（≈192 fm²）。σ 与结论数值常被下标、\frac 或换行
    # 隔开（`σ_el=σ_0+σ_1≈1.937 b`），故窗口放宽到 56 字符，但只收「数值+截面单位」，
    # 否则 `(4π/k^2)(2l+1)` 里的裸 2 会落进 1.92 的容差带、答错也判命中。
    sig_vals = _nums_u(r'(?:σ\s*_?\s*(?:el|tot)?|sigma|总弹性截面|总截面|弹性截面)\s*[:=≈约]?',
                       full_l, _U_AREA)
    sig_hit = any(_mag_ok(v, 1.92, 0.08) or _mag_ok(v, 192.0, 0.08) for v in sig_vals)

    # s 波束缚能 B≈11.4 MeV。标签写法多样：B、B_s、E_B、束缚能、结合能。
    b_vals = _nums_u(r'(?:束缚能|结合能|(?:e\s*_?\s*b|b\s*_?\s*s?)\s*[:=≈约]|束缚态.{0,6}能)'
                     r'\s*[:=≈约]?', full_l, _U_MEV)
    b_hit = any(_mag_ok(v, 11.4, 0.08) for v in b_vals)

    # 保留 s、p 两个分波（l=0,1），防御位：不能只留 s 波或误加高分波
    retain_sp = bool(re.search(
        r'(保留|需保留|截断).{0,40}(s\s*波.{0,6}p\s*波|p\s*波.{0,6}s\s*波|l\s*=\s*0.{0,6}1|l\s*=\s*0\s*[,，、]\s*1)',
        full_l)) or bool(re.search(r'l\s*=\s*0\s*[,，、和与]\s*1', full_l))

    # 光学定理一致性检验存在。剥壳后 `\text{Im}\,f(0)` → `im f(0)`；
    # 答复也常写 `4π/k · Im f(0)` 或 `σ_tot=σ_el`（实势无吸收）作为检验落点。
    optical = bool(re.search(r'光学定理', full)) and bool(re.search(
        r'im\s*\,?\s*f\s*\(?\s*0|σ\s*_?\s*(?:tot)?\s*=\s*\(?\s*4\s*π\s*/\s*k'
        r'|4\s*π\s*/\s*k\s*\)?\s*[\s·⋅]*im'
        r'|σ\s*_?\s*tot\s*=\s*σ\s*_?\s*el', full_l))

    # 存在束缚态判定
    bound_exists = bool(re.search(r'存在.{0,8}s\s*波.{0,4}束缚态|存在.{0,4}(一个)?.{0,4}s\s*波束缚态|s\s*波束缚态.{0,6}存在', full_l)) \
                   or bool(re.search(r'存在(一个)?束缚态', full_l))

    non_empty = 1.0 if len(full.strip()) >= 30 else 0.0
    refusal = bool(re.search(r"(无法回答|不能回答|不会做|拒绝作答|i cannot|i can't|cannot solve)", full_l))
    not_refusal = 0.0 if refusal else 1.0

    has_unit = 1.0 if re.search(r'fm\s*\^?\{?\s*-?\s*1|fm⁻¹|barn|fm\s*\^?\{?\s*2|fm²|mev|rad', full_l) else 0.0

    core = 0.15 * (1.0 if d0_hit else 0.0) \
         + 0.15 * (1.0 if d1_hit else 0.0) \
         + 0.20 * (1.0 if sig_hit else 0.0) \
         + 0.15 * (1.0 if b_hit else 0.0)
    defense = 0.10 * (1.0 if retain_sp else 0.0)

    final_answer = 0.10 * non_empty + 0.10 * not_refusal + core + defense + 0.05 * has_unit

    out["non_empty_answer"] = non_empty
    out["not_refusal"] = not_refusal
    out["k_hit"] = 1.0 if k_hit else 0.0
    out["q_hit"] = 1.0 if q_hit else 0.0
    out["delta0_hit"] = 1.0 if d0_hit else 0.0
    out["delta1_hit"] = 1.0 if d1_hit else 0.0
    out["sigma_el_hit"] = 1.0 if sig_hit else 0.0
    out["bound_energy_hit"] = 1.0 if b_hit else 0.0
    out["retain_s_p_waves"] = 1.0 if retain_sp else 0.0
    out["optical_theorem_check"] = 1.0 if optical else 0.0
    out["bound_state_exists"] = 1.0 if bound_exists else 0.0
    out["has_unit"] = has_unit

    anchors = [d0_hit, d1_hit, sig_hit, b_hit, retain_sp]
    out["numeric_anchor_hit_rate"] = round(sum(1 for h in anchors if h) / 5.0, 4)

    out["auto_final_answer_score"] = round(final_answer, 4)
    return out
```

## LLM Judge Rubric

大模型评分负责**过程、概念与逻辑**，不重复判定代码已覆盖的最终数值命中。

### Criterion 1: 运动学 + 约化质量 + 硬芯边界（Weight: 30%，核心防御位）

**Score 1.0**: 识别散射中心无限重 ⇒ 约化质量 μ=m_n（**非 m_n/2**）、实验室能量即相对运动能量；取 C=ħ²/(2m_n)=20.721 MeV·fm²，得 k=√(E/C)≈0.3108 fm⁻¹、q=√((E+45.0)/C)≈1.506 fm⁻¹；并正确处理硬芯边界——内区波在 r=a=0.35 fm 处为零、s 波取移位宗量 u_in∝sin[q(r-a)]、阱宽 d=R−a=1.65 fm。
**Score 0.5**: 波数量级对但约化质量说明含糊，或硬芯边界/阱宽 d 处理有一处含混（如误用 d=R 但后续数值仍大致自洽）。
**Score 0.0**: 误取 μ=m_n/2（k、q 差 √2 因子），或忽略硬芯边界（未让内区波在 r=a 处为零 / 用 d=R=2.00 fm）。

### Criterion 2: 分波相移 + 截断判据 + 总截面 + 光学定理（Weight: 40%）

**Score 1.0**: 由 s 波匹配 q cot(qd)=k cot(kR+δ0) 得 δ0≈−0.779 rad、p 波球贝塞尔匹配得 δ1≈+0.611 rad；用 σ_l=(4π/k²)(2l+1)sin²δ_l 与 10⁻³ barn 阈值论证 l=2 贡献 ~10⁻⁶ barn 可忽略、**保留 s、p 波（l=0,1）**；得 σ_el≈1.92 barn；并用光学定理 σ_tot=(4π/k)Im f(0)（无吸收 σ_tot=σ_el）作一致性检验且结果吻合。
**Score 0.5**: 相移与总截面大致正确，但截断判据表述含糊（未用阈值量级论证）、或光学定理检验缺失/未回到同一数值、或 δ0/δ1 有一处符号或数值含混。
**Score 0.0**: 相移公式/匹配条件用错，或截断判据缺失（如仅凭 kR 机械只留 s 波、或漏留 p 波、或误加高分波），或总截面与相移不对应。

### Criterion 3: s 波束缚态存在性 + 唯一根 + 束缚能（Weight: 30%）

**Score 1.0**: 令 E=−B，由对数导数匹配得 α cot(αd)=−κ 且 α²+κ²=45.0/C，化为 x=β sin x（β=d√(45.0/C)≈2.432）；正确论证物理解在 π/2<x<π 内**有且仅有一个根** x≈2.10，得 α≈1.27 fm⁻¹、束缚能 B=45.0−Cα²≈11.4 MeV，判定存在一个 s 波束缚态。
**Score 0.5**: 建立束缚态超越方程并得到束缚态存在，但根区间/唯一性论证含糊，或 B 数值有一处偏差。
**Score 0.0**: 束缚态方程建立错误（如未用硬芯移位宗量 / κ、α 关系错），或误判束缚态不存在、或束缚能数量级错误。