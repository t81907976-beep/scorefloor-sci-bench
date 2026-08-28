# 构造高质量-query	
一段接地金属漂移管中有一束由残余气体电离形成的中性化电子流,管长远大于扰动波长,可近似作一维无限系统。离子为单电荷 Ar^+。初态管内无静电场,且两端电极没有直流电流输出。电子速度分析器给出两个关于 v=0 对称的 Lorentzian 峰,峰心在 ±u,两个峰的半高全宽均为 W；仪器只能给出总电子数密度 n_e,未分别给出两峰粒子数。

为避免 Lorentzian 数学尾部带来的非物理歧义,约定如下:Lorentzian 只作为低速核心的解析速度分布模型并用于 Landau 速度积分的解析延拓；其归一化密度按全实轴积分定义。涉及总动量或直流电流的一阶矩约束时,均按 Cauchy 主值意义理解,等价于先引入关于 v=0 对称的高能物理截断、完成电流约束后再取截断远大于 u,W 的极限。因此可用零直流电流条件确定两峰权重,但不把 Lorentzian 的高能尾部解释为真实超光速粒子或用于高阶矩物理判断。

已知 n_e=7.50×10^10 cm^-3,u=1.80×10^6 m/s,W=240 km/s,待考察的纵向扰动波数 k=5.50 cm^-1,扰动约定为 exp[i(kx-ωt)]。要求最后自行检查非相对论近似是否在主导速度尺度上自洽。

设电子电荷量大小为 e=1.602176634×10^-19 C,电子质量 m_e=9.1093837015×10^-31 kg,真空介电常数 ε0=8.8541878128×10^-12 F/m,原子质量单位 m_u=1.66053906660×10^-27 kg,氩离子质量取 M_i=39.95 m_u,光速 c=2.99792458×10^8 m/s。

关于离子响应采用如下明确判据:先完全忽略离子动力学,仅以静止中性化正电背景处理电子双流,求候选不稳定增长率 γ_e；再计算 Λ=ω_pi/γ_e,其中 ω_pi=[n_i e^2/(M_i ε0)]^1/2 且由准中性 n_i=n_e。若 Λ<0.10,则认为一个增长时间内离子动力学极化可忽略,最终采用电子双流模型；若 Λ≥0.10,则必须把 Ar^+ 的动力学极化率纳入最终色散方程。若需要纳入离子动力学,约定离子初态为冷、静止、均匀背景,即 f_i0(v)=n_i δ(v),其线性极化率取 χ_i=-ω_pi^2/ω^2。

要求:
1. 由系统封闭性和边界条件自行写出电子平衡分布 f0(v),注意 W 与 Lorentzian 半宽参数的区别,并说明直流电流条件的主值/对称截断含义；
2. 对 t>0 的初值问题判定 Landau 围道方向、共振极点绕行方式和 δ 项符号；
3. 不预设离子是否能作为静止背景。先用电子双流模型求候选根,再按给定判据参数 Λ 决定是否需要把 Ar^+ 的动力学极化率纳入最终色散方程；
4. 求最终应采用模型下的色散根,判定稳定或不稳定,并给出主不稳定根增长率。
# SFT标准-response	
1. 平衡分布与电流约束
已知 n_e=7.50×10^10 cm^-3=7.50×10^16 m^-3,k=5.50 cm^-1=550 m^-1。
Lorentzian 的半高全宽为 W=240 km/s,因此半高半宽参数为 a=W/2=120 km/s=1.20×10^5 m/s。
设两峰中心分别在 ±u,u=1.80×10^6 m/s。题目要求直流电流按 Cauchy 主值/对称截断理解；由于两个峰关于 v=0 对称,零直流电流给出两峰权重相等:n_+=n_-=n_e/2。
因此电子平衡分布为
f0(v)=(n_e/2π)·a[(v-u)^2+a^2]^{-1}+(n_e/2π)·a[(v+u)^2+a^2]^{-1}。

2. Landau 因果处方
扰动取 exp[i(kx-ωt)]。对 t>0 的初值问题,ω 平面取 ω→ω+i0^+ 的因果延拓；等价地,在速度积分中共振点按 Landau 处方绕开,从而单峰 Lorentzian 的解析结果给出
χ_j=-ω_pj^2/(ω-kv_j+i k a)^2。
这里 +i k a 表示 Lorentzian 半宽导致的统一下移,最终使模态的虚部向负方向平移。

3. 先忽略离子,求电子双流候选根
电子总等离子体频率
ω_pe=[n_e e^2/(m_e ε0)]^1/2 ≈ 1.545×10^10 s^-1。
定义
A=ku=550×1.80×10^6=9.90×10^8 s^-1,
B=ka=550×1.20×10^5=6.60×10^7 s^-1。
两峰电子模型的介电函数为
ε(ω,k)=1-(ω_pe^2/2)[(ω-A+iB)^{-2}+(ω+A+iB)^{-2}]=0。
令 ζ=ω+iB,则方程化为
(ζ^2-A^2)^2-ω_pe^2(ζ^2+A^2)=0。
设 x=ζ^2,则
x^2-(2A^2+ω_pe^2)x+(A^4-ω_pe^2A^2)=0。
取数值后得到负根
x_-≈-9.65×10^17 s^-2,
故
Ω=√(-x_-)≈9.82×10^8 s^-1。
于是不稳定根为
ω_u=i(Ω-B)≈i(9.82×10^8-6.60×10^7)≈+i 9.16×10^8 s^-1。
因此电子双流主增长率
γ_e≈9.16×10^8 s^-1。
其余根为
ω≈-i(Ω+B)≈-i1.05×10^9 s^-1,
以及高频振荡根
ω≈±1.55×10^10-i6.60×10^7 s^-1。

4. 依据题设判据决定是否纳入离子动力学
氩离子质量
M_i=39.95 m_u≈39.95×1.66053906660×10^-27=6.634×10^-26 kg。
准中性下 n_i=n_e。
离子等离子体频率
ω_pi=[n_i e^2/(M_i ε0)]^1/2 ≈ 5.72×10^7 s^-1。
因此
Λ=ω_pi/γ_e≈5.72×10^7 / 9.16×10^8≈6.24×10^-2。
由于 Λ<0.10,按题目规定,一个增长时间内离子动力学极化可忽略,最终必须采用电子双流模型,不把 Ar^+ 的 χ_i=-ω_pi^2/ω^2 纳入最终色散方程。

5. 稳定性与最终结论
最终模型下系统存在不稳定模,主不稳定根为
ω≈+i 9.16×10^8 s^-1,
对应增长率
γ≈9.16×10^8 s^-1。
因此该系统是不稳定的,且主不稳定模为非振荡增长模。

6. 非相对论自洽性检查
主速度尺度包括 u=1.80×10^6 m/s、a=1.20×10^5 m/s,以及相速度尺度 γ/k≈(9.16×10^8)/550≈1.67×10^6 m/s。
它们都远小于光速 c=2.998×10^8 m/s,最大比值约 6.0×10^-3,故非相对论近似在主导速度尺度上自洽。
# 步骤列表-reference
1. **平衡分布与电流约束**  
   \[
   n_e = 7.50\times10^{10}\ \text{cm}^{-3} = 7.50\times10^{16}\ \text{m}^{-3},\quad
   k = 5.50\ \text{cm}^{-1} = 550\ \text{m}^{-1},\quad
   a = \frac{W}{2} = 120\ \text{km/s} = 1.20\times10^{5}\ \text{m/s}.
   \]  
   零直流电流（Cauchy主值）与对称性 ⇒ 两峰权重相等，电子平衡分布：  
   \[
   f_0(v) = \frac{n_e}{2\pi}\frac{a}{(v-u)^2+a^2} + \frac{n_e}{2\pi}\frac{a}{(v+u)^2+a^2}.
   \]

2. **Landau因果处方**  
   扰动 \(\exp[i(kx-\omega t)]\)，因果初值问题要求围道从极点下方绕过（或 \(\omega\to\omega+i0^+\)）。单峰Lorentzian解析结果给出极化率：  
   \[
   \chi_j = -\frac{\omega_{pj}^2}{(\omega - k v_j + i k a)^2}.
   \]

3. **电子双流候选根**  
   \[
   \omega_{pe} = \sqrt{\frac{n_e e^2}{m_e\varepsilon_0}} \approx 1.545\times10^{10}\ \text{s}^{-1},\quad
   A = ku = 9.90\times10^8\ \text{s}^{-1},\quad
   B = ka = 6.60\times10^7\ \text{s}^{-1}.
   \]  
   介电函数：  
   \[
   \varepsilon(\omega,k) = 1 - \frac{\omega_{pe}^2}{2}\left[(\omega - A + iB)^{-2} + (\omega + A + iB)^{-2}\right] = 0.
   \]  
   令 \(\zeta = \omega + iB\)，得 \((\zeta^2 - A^2)^2 = \omega_{pe}^2(\zeta^2 + A^2)\)。设 \(x = \zeta^2\)：  
   \[
   x^2 - (2A^2 + \omega_{pe}^2)x + (A^4 - \omega_{pe}^2 A^2) = 0.
   \]  
   负根 \(x_- \approx -9.65\times10^{17}\ \text{s}^{-2}\)，\(\Omega = \sqrt{-x_-} \approx 9.82\times10^8\ \text{s}^{-1}\)。  
   不稳定根：  
   \[
   \omega_u = i(\Omega - B) \approx i\,9.16\times10^8\ \text{s}^{-1},\quad
   \gamma_e \approx 9.16\times10^8\ \text{s}^{-1}.
   \]  
   其余根：\(\omega \approx -i(\Omega+B) \approx -i\,1.05\times10^9\ \text{s}^{-1}\)，高频阻尼模 \(\omega \approx \pm 1.55\times10^{10} - i\,6.60\times10^7\ \text{s}^{-1}\).

4. **离子动力学判据**  
   \[
   M_i = 39.95\,m_u \approx 6.634\times10^{-26}\ \text{kg},\quad
   \omega_{pi} = \sqrt{\frac{n_i e^2}{M_i\varepsilon_0}} \approx 5.72\times10^7\ \text{s}^{-1}.
   \]  
   \[
   \Lambda = \frac{\omega_{pi}}{\gamma_e} \approx 6.24\times10^{-2} < 0.10.
   \]  
   按判据离子动力学可忽略，最终采用电子双流模型（不纳入 \(\chi_i = -\omega_{pi}^2/\omega^2\)）。

5. **稳定性与非相对论自洽**  
   系统不稳定，主不稳定模为纯增长模：  
   \[
   \boxed{\omega \approx +i\,9.16\times10^8\ \text{s}^{-1}},\quad \gamma \approx 9.16\times10^8\ \text{s}^{-1}.
   \]  
   速度尺度 \(u\)、\(a\)、\(\gamma/k \sim 1.67\times10^6\ \text{m/s}\) 均远小于 \(c\)，非相对论近似自洽。


## Grading Criteria

- [ ] 正确完成单位换算并区分半高全宽与半高半宽：\(n_e=7.50\times10^{16}\,\mathrm{m^{-3}}\)、\(k=550\,\mathrm{m^{-1}}\)、\(a=W/2=1.20\times10^5\,\mathrm{m/s}\)。
- [ ] 由零直流电流的 Cauchy 主值/关于 \(v=0\) 的对称截断条件得到两峰权重相等 \(n_+=n_-=n_e/2\)，并写出两个中心位于 \(\pm u\)、半宽为 \(a\) 的归一化 Lorentzian 之和。
- [ ] 对 \(\exp[i(kx-\omega t)]\) 使用正确的 Landau 因果处方：共振极点从下方绕过或等价地取 \(\omega\to\omega+i0^+\)，电子单峰极化率分母必须为 \((\omega-kv_j+ika)^2\)。
- [ ] 电子双流候选计算给出 \(\omega_{pe}\approx1.545\times10^{10}\,\mathrm{s^{-1}}\)、\(A=ku=9.90\times10^8\,\mathrm{s^{-1}}\)、\(B=ka=6.60\times10^7\,\mathrm{s^{-1}}\)，以及候选增长率 \(\gamma_e\approx9.16\times10^8\,\mathrm{s^{-1}}\)。
- [ ] 正确计算 \(\omega_{pi}\approx5.72\times10^7\,\mathrm{s^{-1}}\) 和 \(\Lambda\approx6.24\times10^{-2}<0.10\)，并据题设判据明确选择忽略离子动力学、不把 \(\chi_i=-\omega_{pi}^2/\omega^2\) 纳入最终方程。
- [ ] 最终判定系统不稳定，主根为纯增长根 \(\omega\approx+i\,9.16\times10^8\,\mathrm{s^{-1}}\)，而非阻尼根或需要加入离子后的根。
- [ ] 使用 \(u\)、\(a\) 和 \(\gamma/k\) 等主导速度尺度与 \(c\) 比较，确认其最大量级约为 \(6.0\times10^{-3}c\)，非相对论近似自洽。

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程（本段由 lib.authoring 自动生成并通过双向自检）。

```python
def grade(transcript: list, workspace_path: str, meta: dict) -> dict:
    import re

    def get_content(item):
        content = item.get("content", "") if isinstance(item, dict) else ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for segment in content:
                if isinstance(segment, str):
                    parts.append(segment)
                elif isinstance(segment, dict):
                    value = segment.get("text", "")
                    if isinstance(value, str):
                        parts.append(value)
            return "\n".join(parts)
        return str(content) if content is not None else ""

    def get_final_answer(items):
        if not isinstance(items, list):
            return ""
        for item in reversed(items):
            if isinstance(item, dict) and item.get("role") == "assistant":
                text = get_content(item)
                if text.strip():
                    return text
        return ""

    def normalize(text):
        """统一上标与科学计数法，并剥掉 markdown/LaTeX 装饰后再做字面比对。

        不做写法容错会把「表述差异」记成「答错」，产生集体假阴性：
          - markdown 强调：`系统**不稳定**` 要能命中字面「系统不稳定」；
          - LaTeX 装饰壳：`\\text{m/s}`、`\\boxed{...}`、`\\mathrm{Re}\\,\\omega` 剥壳留内容；
          - `\\frac{W}{2}` → `(w)/(2)`，与裸写 `W/2` 等价；
          - 希腊字母统一为单字符，且 lower() 后 `\\Gamma`/`Γ` 与 `\\gamma`/`γ` 同形，
            使半宽符号写成 a / Γ / Δ 的三种流派在 `+ika` 类判据里可比。
        """
        table = str.maketrans({
            "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
            "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
            "⁺": "+", "⁻": "-", "−": "-", "–": "-", "—": "-",
            "＋": "+", "×": "×"
        })
        s = text.translate(table)
        s = s.replace("\\times", "×").replace("\\cdot", "×")
        s = re.sub(
            r"(\d+(?:\.\d+)?)\s*[×xX]\s*10\s*(?:\^)?\s*\{?\s*([+-]?\d+)\s*\}?",
            r"\1e\2",
            s
        )
        s = s.replace("E", "e").lower()
        s = s.replace("**", "").replace("__", "")
        s = re.sub(r"\\(?:left|right|bigg?|displaystyle|q?quad|;|!)", " ", s)
        for _ in range(3):
            s = re.sub(
                r"\\(?:boxed|text|mathrm|mathbf|mathcal|operatorname|rm|bf|it)"
                r"\s*\{([^{}]*)\}",
                r"\1", s)
        s = re.sub(r"\\[tdc]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"(\1)/(\2)", s)
        for tex, ch in (("\\omega", "ω"), ("\\gamma", "γ"), ("\\delta", "δ"),
                        ("\\alpha", "α"), ("\\beta", "β"), ("\\lambda", "λ"),
                        ("\\varepsilon", "ε"), ("\\epsilon", "ε"),
                        ("\\pi", "π"), ("\\chi", "χ"), ("\\zeta", "ζ"),
                        ("\\xi", "ξ"), ("\\tilde", ""), ("\\hat", ""),
                        ("\\ll", "≪"), ("\\approx", "≈"), ("\\simeq", "≈")):
            s = s.replace(tex, ch)
        s = re.sub(r"\\[,:>\s]", " ", s)
        return s.replace("$", "").replace("{", "").replace("}", "")

    def all_numbers(text):
        pattern = r"(?<![\w.])[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[-+]?\d+)?"
        out = []
        for token in re.findall(pattern, text):
            try:
                out.append(float(token))
            except Exception:
                pass
        return out

    def close(value, target, rel=0.03):
        if target == 0:
            return abs(value) <= rel
        return abs(value - target) / abs(target) <= rel

    def has_num(target, rel=0.03):
        return any(close(v, target, rel) for v in numbers)

    def contains_any(options):
        return any(option in norm for option in options)

    def contains_any_compact(options):
        """在去掉全部空白的文本上比对字面。

        中文结论里常插入符号或空格（`从极点 v=ω/k **下方** 绕过`），
        按 norm 逐字匹配会漏判，故按 compact 比对。
        """
        return any(option in compact for option in options)

    def positive_i_root(target, rel=0.03):
        """确认答复把主根的正虚部（增长率）定在 target 上。

        原先只认 `+i9.16e8` 一种写法。实际答复普遍写成等价形式：
        `ω=iγ, γ≈9.16e8`、`γ=Im ω≈9.16e8`、`γ=γ_cold−kΔ≈9.2e8`，
        只认单一写法会让全部答复集体判 0。这里三种模板都接受，但仍要求
        数值落在 target 的 rel 容差内（冷根 9.82e8 因此不会被误收）。
        """
        num = r"([0-9]+(?:\.[0-9]+)?(?:e[+-]?\d+)?)"
        patterns = (
            r"\+\s*i\s*" + num,               # +i9.16e8
            r"im\s*ω\s*[≈=~]\s*" + num,       # Im ω ≈ 9.16e8
            r"γ[^\n]{0,30}?[≈=~]\s*" + num,   # γ=…≈9.16e8（含 γ_e、γ=γ_cold−kΔ）
        )
        for pattern in patterns:
            for match in re.finditer(pattern, norm):
                try:
                    if close(float(match.group(1)), target, rel):
                        return True
                except Exception:
                    pass
        return False

    def refused(text):
        refusal_phrases = [
            "我无法回答", "我不能回答", "无法完成", "不能完成",
            "抱歉，我无法", "抱歉，无法", "as an ai", "i cannot answer",
            "i can't answer", "unable to answer"
        ]
        low = text.lower()
        return any(p in low for p in refusal_phrases)

    answer = get_final_answer(transcript)
    norm = normalize(answer)
    compact = re.sub(r"\s+", "", norm)
    numbers = all_numbers(norm)

    non_empty_answer = 1.0 if len(answer.strip()) >= 30 else 0.0
    not_refusal = 1.0 if answer.strip() and not refused(answer) else 0.0

    # 单位换算的硬证据：要么显式写出 SI 值，要么给出只有换算正确才可能得到的派生量
    # （ω_pe 只能由 n_e[m^-3] 算出、ku 只能由 k[m^-1] 算出）。只认显式复述会把
    # 「没复述中间量」误判成「换算错」。
    density_ok = (
        (has_num(7.50e16, 0.03) and contains_any(["m^-3", "m-3"]))
        or has_num(1.545e10, 0.02)
    )
    k_ok = (
        (has_num(550.0, 0.01) and contains_any(["m^-1", "m-1"]))
        or has_num(9.90e8, 0.02)
    )
    # 半宽符号各家写作 a / Γ / Δ，写法容 `W/2`、`\frac{W}{2}`、HWHM、半宽(参数)
    halfwidth_language = contains_any_compact([
        "w/2", "(w)/(2)", "w／2", "半高半宽", "半宽参数", "半宽", "hwhm"
    ])
    halfwidth_ok = (
        has_num(1.20e5, 0.03) and halfwidth_language
        and contains_any(["m/s", "m·s^-1", "m s^-1"])
    )
    parameter_setup = 1.0 if density_ok and k_ok and halfwidth_ok else 0.0

    # 等权结论的常见写法：直接说等权 / 解出 α=1/2 / 写成各 n_e/2
    equal_weight_language = contains_any_compact([
        "两峰权重相等", "权重相等", "权重必须相等", "两峰粒子数相等",
        "等权", "各权重1/2", "权重1/2", "α=1/2", "α=½", "2α-1=0",
        "n_+=n_-=n_e/2", "n+=n-=ne/2", "各为n_e/2", "各占n_e/2", "各占一半"
    ])
    pv_language = contains_any_compact([
        "cauchy主值", "柯西主值", "对称截断", "主值意义", "主值",
        "pv∫", "p∫"
    ])
    distribution_evidence = (
        ("(v-u)" in compact or "(v−u)" in compact)
        and ("(v+u)" in compact)
        and ("π" in norm or "pi" in norm)
    )
    equilibrium_distribution = 1.0 if (
        equal_weight_language and pv_language and distribution_evidence
    ) else 0.0

    # 半宽符号写作 a / Γ / Δ 均可（normalize 后 Γ、Δ 已折成 γ、δ），判据只看
    # 「极化率分母里那一项取 +ik·(半宽)」这一结构。
    plus_ika = bool(re.search(r"\+\s*i\s*\*?\s*k\s*\*?\s*[aγδ]", compact))
    # 错号的判据必须限定在分母内（`+ika)^2` 的镜像）：答复常写 ω=Ω_cold−ikΓ，
    # 这是从 Ω 回到 ω 的正确平移，不能当成极化率符号写错。
    minus_ika = bool(re.search(r"-\s*i\s*\*?\s*k\s*\*?\s*[aγδ]\s*\)", compact))
    causal_direction = contains_any_compact([
        "下方绕过", "下方绕行", "下方通过", "下方绕开", "极点下方",
        "ω→ω+i0", "ω->ω+i0", "ω+i0^+", "omega→omega+i0", "omega->omega+i0"
    ])
    landau_sign = 1.0 if plus_ika and causal_direction and not minus_ika else 0.0

    electron_candidate = 1.0 if (
        has_num(1.545e10, 0.03)
        and has_num(9.90e8, 0.03)
        and has_num(6.60e7, 0.03)
        and has_num(9.16e8, 0.03)
    ) else 0.0

    ion_frequency_ok = has_num(5.72e7, 0.03)
    lambda_ok = has_num(6.24e-2, 0.04)
    threshold_ok = (
        contains_any_compact(["λ<0.10", "lambda<0.10", "λ<0.1"])
        or (
            has_num(0.10, 0.01)
            and contains_any_compact(["小于0.10", "低于0.10", "<0.10"])
        )
    )
    # 「忽略离子」的等价表述：直接说离子/Ar⁺ 动力学可忽略、说动力学极化可忽略、
    # 说把离子当静止中性化背景、或明确最终采用电子双流模型且不引入 χ_i。
    ion_ignored = contains_any_compact([
        "离子动力学可忽略", "忽略离子动力学", "动力学极化可忽略",
        "ar^+动力学可忽略", "ar+动力学可忽略", "离子来不及极化",
        "无需纳入离子", "无需引入χ_i", "无需引入χi", "不纳入χ_i", "不纳入χi",
        "不把ar^+", "静止正电背景", "静止中性背景", "静止中性化背景",
        "中性化背景", "最终采用电子双流模型", "采用电子双流模型",
        "最终模型=电子双流",
    ])
    explicitly_include_ions = contains_any_compact([
        "必须纳入离子动力学", "需要纳入离子动力学", "必须纳入χ_i",
        "最终加入离子极化", "最终应纳入离子", "最终纳入离子",
    ])
    ion_decision = 1.0 if (
        ion_frequency_ok and lambda_ok and threshold_ok
        and ion_ignored and not explicitly_include_ions
    ) else 0.0

    unstable_language = contains_any_compact([
        "系统不稳定", "存在不稳定模", "不稳定的", "判定不稳定", "仍强不稳定",
    ])
    # 「纯增长」的等价表述：纯虚根 / Re ω=0 / 无实频振荡，都是同一个物理结论。
    pure_growth_language = contains_any_compact([
        "纯增长", "非振荡增长", "非振荡的增长", "无实频振荡", "无实频",
        "纯虚根", "纯虚", "reω=0", "re(ω)=0",
    ])
    correct_positive_root = positive_i_root(9.16e8, 0.03)
    final_instability = 1.0 if (
        unstable_language and pure_growth_language and correct_positive_root
    ) else 0.0

    nonrel_conclusion = contains_any_compact([
        "非相对论近似自洽", "非相对论自洽", "非相对论近似在主导速度尺度上自洽",
        "远小于光速", "远小于c", "均≪c", "≪c",
    ])
    speed_scale_ok = (
        has_num(1.67e6, 0.04)
        or has_num(6.0e-3, 0.08)
        or has_num(0.006, 0.08)
    )
    nonrelativistic_check = 1.0 if nonrel_conclusion and speed_scale_ok else 0.0

    scores = {
        "non_empty_answer": non_empty_answer,
        "not_refusal": not_refusal,
        "parameter_setup": parameter_setup,
        "equilibrium_distribution": equilibrium_distribution,
        "landau_causal_sign": landau_sign,
        "electron_candidate_root": electron_candidate,
        "ion_model_decision": ion_decision,
        "final_instability_direction": final_instability,
        "nonrelativistic_self_consistency": nonrelativistic_check,
    }

    weights = {
        "non_empty_answer": 0.03,
        "not_refusal": 0.03,
        "parameter_setup": 0.10,
        "equilibrium_distribution": 0.08,
        "landau_causal_sign": 0.16,
        "electron_candidate_root": 0.20,
        "ion_model_decision": 0.20,
        "final_instability_direction": 0.12,
        "nonrelativistic_self_consistency": 0.08,
    }

    total = 0.0
    for key, weight in weights.items():
        total += scores[key] * weight
    scores["auto_final_answer_score"] = round(total, 6)
    return scores
```

## LLM Judge Rubric

### Criterion 1：平衡分布的封闭性、电流约束与 Lorentzian 参数解释
**Weight: 25%**

- **Score 1.0:** 明确区分 FWHM \(W\) 与半宽 \(a=W/2\)；从零直流电流及关于 \(v=0\) 的对称主值截断推出两峰权重相等；说明主值约定只用于一阶矩约束，不将 Lorentzian 尾部作高阶矩或真实高速粒子解释。
- **Score 0.5:** 得到正确的双峰形式和相等权重，但没有解释 Cauchy 主值/对称截断，或未说明其与 Lorentzian 数学尾部的关系。
- **Score 0.0:** 把 \(W\) 直接当作 Lorentzian 半宽、不能由电流约束确定权重，或使用单峰/不等权双峰且未给出有效理由。

### Criterion 2：Landau 初值处方与极化率符号
**Weight: 25%**

- **Score 1.0:** 从 \(t>0\) 初值问题及 \(\exp[i(kx-\omega t)]\) 的约定正确确定解析延拓和绕极点方向，并一致推出 Lorentzian 极化率中的 \(+ika\)；能够解释该项使模态频率整体向负虚部平移。
- **Score 0.5:** 最终采用了正确的 \(+ika\)，但因果延拓、围道方向或频率平移的说明不完整。
- **Score 0.0:** 使用 \(-ika\)、从极点错误一侧绕行，或给出的围道叙述与所写极化率符号相互矛盾。

### Criterion 3：电子双流色散方程与根分支选择
**Weight: 30%**

- **Score 1.0:** 正确将两峰极化率相加，通过 \(\zeta=\omega+iB\) 把方程化为关于 \(x=\zeta^2\) 的二次方程；识别负的 \(x\) 分支产生纯虚根，并在从 \(\zeta\) 返回 \(\omega\) 时正确扣除 \(B\)，从而选出增长支。
- **Score 0.5:** 色散方程和不稳定分支总体正确，但代数化简、其他根的归属或 \(B\) 所致平移的说明有轻微缺失。
- **Score 0.0:** 漏掉一个电子峰、把负根误当作稳定支、把阻尼根当作增长根，或在 \(\zeta\) 与 \(\omega\) 之间使用错误的虚部平移方向。

### Criterion 4：模型选择顺序、离子判据与近似自洽性
**Weight: 20%**

- **Score 1.0:** 严格遵循“先求电子候选增长率，再计算 \(\Lambda\)，最后按阈值选择模型”的顺序；正确解释 \(\Lambda<0.10\) 意味着一个增长时间内离子极化不足以显著响应；非相对论检查使用了漂移、宽度及模态相速度等相关尺度。
- **Score 0.5:** 最终模型选择正确，但没有清楚解释时间尺度比较，或非相对论检查只比较了单一速度尺度。
- **Score 0.0:** 预先加入离子而不执行题设判据、将 \(\Lambda<0.10\) 错解为必须加入离子、用加入离子后的根反过来定义题设要求的 \(\gamma_e\)，或完全没有进行非相对论自洽性检查。
