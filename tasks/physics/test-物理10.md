# 构造高质量-query
某层状溴化物钙钛矿靶材经烧结后,需要只根据低角粉末XRD峰位判断其Bravais格子。样品来自同一块单相靶材研磨所得；经其他表征确认,在本题所列5.0°≤2θ≤50.0°范围内没有来自杂质相、第二相或样品台的可分辨杂峰,所列可分辨峰均来自同一晶相。装样时持续旋转；用Si标样校准后,2θ零点误差小于0.01°。在5.0°≤2θ≤50.0°范围内,若某衍射线相对最强峰积分强度大于2%,均可被检出；并且在本题用于判定Bravais格子的低角范围内,除Bravais格点导致的系统消光外,几何允许反射不会因基元结构因子的偶然相消而低于该检出限。实测到的Cu Kα粉末峰位如下,括号内为峰位不确定度:14.75(2)°,23.97(2)°,29.77(2)°,32.03(2)°,32.44(2)°,35.81(2)°,44.27(3)°,44.60(3)°,45.30(3)°,46.53(3)°,49.08(3)°。同时,谱图在7.36°,22.78°,27.24°,33.32°附近各±0.06°窗口内没有可分辨峰。已知靶材的化学式单元摩尔质量为335.3 g mol^-1,烧结体真实密度为6100 kg m^-3。Cu Kα波长取λ=1.5406 Å,阿伏伽德罗常数取N_A=6.02214076×10^23 mol^-1。忽略Kα1/Kα2双线分裂和折射修正。试由峰位反推晶系和Bravais格子类型,给出低角各观测峰的hkl指标、晶胞参数a、c、晶胞体积,并用密度判断每个常规晶胞中的化学式单元数Z。注意:题中没有预先说明晶系；必须先用峰位计算判据排除或接受可能模型,再决定后续指标化路线。
# SFT标准-response
1. 由布拉格定律 2d\sin\theta=\lambda,取一阶衍射 n=1,定义 Q=1/d^2=4\sin^2\theta/\lambda^2。对给定峰位可得对应的 Q 值,低角峰序列中 14.75°、29.77°、45.30° 的 Q 近似满足 1:4:9,说明它们属于同一晶轴方向的 00l 系列。

2. 将 14.75° 视为 002 峰:
   d002=\lambda/(2\sin\theta)≈1.5406/(2\sin7.375°)≈6.00 Å,
   因而 c=2d002≈12.00 Å。
   由此 1/c^2≈0.006944 Å^-2。

3. 用 23.97° 峰定 a。若取该峰为 101,则四方晶系公式为
   1/d^2=(h^2+k^2)/a^2+l^2/c^2,
   即 Q101=1/a^2+1/c^2。
   由 Q101≈0.0727 Å^-2,得
   1/a^2≈0.0727-0.006944=0.06576 Å^-2,
   所以 a≈3.90 Å。
   该值也与 32.44°→110、46.53°→200 等峰相互吻合。

4. 用四方晶胞公式检验全部观测峰,可一致指标化为:
   14.75°→002,23.97°→101,29.77°→004,32.03°→103,32.44°→110,35.81°→112,44.27°→105,44.60°→114,45.30°→006,46.53°→200,49.08°→202。
   这些峰全部满足四方晶系倒易点阵关系。

5. 判定 Bravais 格子类型。若为简单四方 P 格子,则 001、100、102、111 等几何允许反射应出现；题目明确在对应 2θ≈7.36°、22.78°、27.24°、33.32° 的窗口内无可分辨峰,并且题设已排除杂相、样品台峰、检出限问题以及基元结构因子的偶然相消。上述缺失峰恰好满足体心四方 I 格子的系统消光条件 h+k+l 为奇数时消光,因此 Bravais 格子应为体心四方（I tetragonal,tI）。

6. 晶胞体积为
   V=a^2c≈(3.90 Å)^2×12.00 Å≈182.5 Å^3。
   换算为 SI 单位:V≈1.825×10^-28 m^3。

7. 由密度求常规晶胞内化学式单元数 Z:
   ρ=ZM/(N_A V),故 Z=ρN_A V/M。
   代入 ρ=6100 kg m^-3,M=335.3 g mol^-1=0.3353 kg mol^-1,N_A=6.02214076×10^23 mol^-1,V=1.825×10^-28 m^3,得
   Z≈6100×6.02214076×10^23×1.825×10^-28/0.3353≈2.00。

结论:该样品的晶系为四方晶系,Bravais 格子为体心四方（I tetragonal,tI）；a=b≈3.90 Å,c≈12.00 Å,V≈182.5 Å^3,常规晶胞中 Z=2。
# 步骤列表-reference
1. **计算 \(Q\) 值并确认 \(00l\) 系列**  
   由布拉格方程 \(2d\sin\theta = \lambda\)，定义  
   \[
   Q = \frac{1}{d^2} = \frac{4\sin^2\theta}{\lambda^2}.
   \]  
   低角峰 14.75°、29.77°、45.30° 的 \(Q\) 值比约为 \(1:4:9\)，判为 \((002)、(004)、(006)\) 的 \(00l\) 系列。

2. **求 \(c\) 轴长度**  
   取 (002) 峰：  
   \[
   d_{002} = \frac{\lambda}{2\sin\theta} \approx 6.00\ \text{Å} \quad\Rightarrow\quad c = 2d_{002} \approx 12.00\ \text{Å},
   \]  
   则 \(\displaystyle \frac{1}{c^2} \approx 0.006944\ \text{Å}^{-2}\)。

3. **求 \(a\) 轴长度**  
   将 23.97° 峰指为 (101)，四方晶系公式  
   \[
   \frac{1}{d^2} = \frac{h^2+k^2}{a^2} + \frac{l^2}{c^2},
   \]  
   \(Q_{101} = \frac{1}{a^2} + \frac{1}{c^2} \approx 0.0727\ \text{Å}^{-2}\)，解得  
   \[
   \frac{1}{a^2} \approx 0.06576\ \text{Å}^{-2} \quad\Rightarrow\quad a \approx 3.90\ \text{Å}.
   \]  
   该值与 32.44°→(110)、46.53°→(200) 等峰自洽。

4. **全部观测峰的指标化**  
   使用四方晶胞公式 \(Q = \frac{h^2+k^2}{a^2} + \frac{l^2}{c^2}\)，所有 11 个峰均可指标化为体心四方反射：  
   \((002), (101), (004), (103), (110), (112), (105), (114), (006), (200), (202)\)。

5. **Bravais 格子判定**  
   若为简单四方 P 格子，应出现 \((001)、(100)、(102)、(111)\) 等反射，对应 \(2\theta \approx 7.36^\circ, 22.78^\circ, 27.24^\circ, 33.32^\circ\)，实测均无峰。这些缺失满足体心四方 I 格子的系统消光条件 \(h+k+l = 2n\)，奇数时消光。由此判定为体心四方（tI）。

6. **晶胞体积**  
   \[
   V = a^2c \approx (3.90\ \text{Å})^2 \times 12.00\ \text{Å} \approx 182.5\ \text{Å}^3 = 1.825\times10^{-28}\ \text{m}^3.
   \]

7. **化学式单元数 \(Z\)**  
   由密度公式 \(\rho = \frac{ZM}{N_A V}\)，  
   \[
   Z = \frac{\rho N_A V}{M} \approx \frac{6100 \times 6.022\times10^{23} \times 1.825\times10^{-28}}{0.3353} \approx 2.00,
   \]  
   与体心四方晶胞含 2 个格点一致。


## Grading Criteria

- [ ] 明确判定晶系为四方晶系，并将 Bravais 格子判定为体心四方（I tetragonal，tI），而不是简单四方 P。
- [ ] 给出晶胞参数 \(a=b\approx3.90\ \text{Å}\)、\(c\approx12.00\ \text{Å}\)。
- [ ] 将 11 个观测峰依次指标化为 \((002),(101),(004),(103),(110),(112),(105),(114),(006),(200),(202)\)。
- [ ] 利用无峰窗口说明 \((001),(100),(102),(111)\) 等奇和反射缺失，并正确给出体心消光条件 \(h+k+l\) 为奇数时消光。
- [ ] 给出常规晶胞体积 \(V\approx182.5\ \text{Å}^3\)，或等价的 \(1.825\times10^{-28}\ \text{m}^3\)。
- [ ] 使用密度关系得到每个常规晶胞中的化学式单元数 \(Z\approx2\)。
- [ ] 结果应与 \(14.75^\circ,29.77^\circ,45.30^\circ\) 分别属于 \((002),(004),(006)\) 的 \(00l\) 系列相一致。

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程（本段由 lib.authoring 自动生成并通过双向自检）。

```python
def grade(transcript: list, workspace_path: str, meta: dict) -> dict:
    import re

    def extract_content(item):
        content = item.get("content", "") if isinstance(item, dict) else ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for seg in content:
                if isinstance(seg, str):
                    parts.append(seg)
                elif isinstance(seg, dict):
                    value = seg.get("text", "")
                    if isinstance(value, str):
                        parts.append(value)
            return "\n".join(parts)
        return str(content) if content is not None else ""

    def get_final_answer(items):
        for item in reversed(items if isinstance(items, list) else []):
            if isinstance(item, dict) and item.get("role") == "assistant":
                return extract_content(item)
        return ""

    def normalize(s):
        s = str(s)
        table = str.maketrans({
            "−": "-", "–": "-", "—": "-",
            "×": "x", "·": "*",
            "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
            "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
            "⁻": "-", "⁺": "+",
            "\u212b": "\u00c5"  # ANGSTROM SIGN → Å，统一两种码位
        })
        s = s.translate(table)
        # LaTeX 等价写法归一：先把需保留语义的命令映射成符号，再丢弃其余命令
        s = re.sub(r"\\(?:mathring\s*\{A\}|text\s*\{Å\}|AA|angstrom)", "Å", s, flags=re.I)
        s = re.sub(r"\\times", "x", s)
        s = re.sub(r"\\cdot", "*", s)
        s = re.sub(r"\\(?:simeq|approx|sim|cong|doteq)", "≈", s)
        # 去掉字体/装饰包裹，保留花括号内内容：\boxed{..} \mathrm{..} {\rm ..} 等
        for _ in range(3):
            s = re.sub(
                r"\\(?:boxed|mathrm|mathbf|mathit|operatorname|text|textrm|rm|bm|bf|it)"
                r"\s*\{([^{}]*)\}", r"\1", s)
            s = re.sub(r"\{\s*\\(?:rm|it|bf|sf|mathrm|mathbf)\s+([^{}]*)\}", r"\1", s)
        s = re.sub(
            r"([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*[xX*]\s*10\s*\^?\{?\s*([+-]?\d+)\}?",
            r"\1e\2",
            s
        )
        # 丢弃 LaTeX 细空格 (\,\;\ ) 与其余反斜杠命令，再去花括号/$
        s = re.sub(r"\\[,;:!> ]", " ", s)
        s = re.sub(r"\\[\(\)\[\]]", " ", s)  # 去掉 LaTeX 行内/行间数学定界符 \( \) \[ \]
        s = re.sub(r"\\[a-zA-Z]+", " ", s)
        s = s.replace("$", "").replace("{", " ").replace("}", " ")
        s = re.sub(r"\s+", " ", s)
        return s

    def is_refusal(s):
        low = s.lower()
        refusal_phrases = [
            "无法回答", "不能回答", "无法确定", "信息不足",
            "无法判断", "抱歉，我不能", "i cannot answer",
            "i can't answer", "insufficient information"
        ]
        return any(p in low for p in refusal_phrases)

    def close(v, target, rel=0.03, abs_tol=0.0):
        return abs(v - target) <= max(abs_tol, abs(target) * rel)

    def floats_from_matches(pattern, s, flags=re.I):
        vals = []
        for m in re.finditer(pattern, s, flags):
            try:
                vals.append(float(m.group(1)))
            except Exception:
                pass
        return vals

    def has_near(pattern, target, rel=0.03, abs_tol=0.0):
        return any(close(v, target, rel, abs_tol)
                   for v in floats_from_matches(pattern, text_n))

    def has_peak_assignment(peak, hkl):
        p = re.escape(peak)
        h = r"\(?\s*" + r"\s*".join(list(hkl)) + r"\s*\)?"
        forward = p + r"\s*(?:°|度)?\s*.{0,14}?" + h
        reverse = h + r"\s*.{0,14}?" + p + r"\s*(?:°|度)?"
        return bool(re.search(forward, text_n, re.I) or
                    re.search(reverse, text_n, re.I))

    text = get_final_answer(transcript)
    text_n = normalize(text)
    compact = re.sub(r"\s+", "", text_n)
    low = text_n.lower()

    non_empty_answer = 1.0 if len(re.sub(r"\s+", "", text)) >= 30 else 0.0
    not_refusal = 0.0 if is_refusal(text) else 1.0

    crystal_system_tetragonal = 1.0 if re.search(
        r"四方晶系|四方系|tetragonal", text_n, re.I
    ) else 0.0

    bravais_body_centered_tetragonal = 1.0 if re.search(
        r"体心四方|体心型四方|I\s*(?:型)?四方|I\s+tetragonal|\btI\b",
        text_n, re.I
    ) else 0.0

    num = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?)"
    a_patterns = [
        r"\ba\s*=\s*b\s*(?:=|≈|~|约为?|为)\s*" + num,
        r"(?:晶胞参数|晶格常数)?\s*\ba\s*(?:=|≈|~|约为?|为)\s*" + num
    ]
    c_patterns = [
        r"(?:晶胞参数|晶格常数)?\s*\bc\s*(?:=|≈|~|约为?|为)\s*" + num
    ]
    a_ok = any(has_near(p, 3.90, 0.035) for p in a_patterns)
    c_ok = any(has_near(p, 12.00, 0.035) for p in c_patterns)
    angstrom_present = bool(re.search(r"Å|埃|angstrom", text_n, re.I))
    lattice_parameters = 1.0 if a_ok and c_ok and angstrom_present else 0.0

    volume_patterns = [
        r"(?:\bV\b|晶胞体积|体积)\s*(?:=|≈|~|约为?|为)?\s*" + num,
        num + r"\s*(?:Å|埃)\s*(?:\^?\s*3)\b",
        num + r"\s*m\s*(?:\^?\s*3)\b"
    ]
    volume_vals = []
    for pat in volume_patterns:
        volume_vals.extend(floats_from_matches(pat, text_n))
    volume_ok = any(close(v, 182.5, 0.04) for v in volume_vals)
    volume_ok = volume_ok or any(close(v, 1.825e-28, 0.05) for v in volume_vals)
    cell_volume = 1.0 if volume_ok else 0.0

    z_vals = floats_from_matches(
        r"\bZ\s*(?:=|≈|~|约为?|为)\s*" + num, text_n
    )
    formula_units_z2 = 1.0 if any(close(v, 2.0, 0.06, 0.08) for v in z_vals) else 0.0

    assignments = [
        ("14.75", "002"),
        ("23.97", "101"),
        ("29.77", "004"),
        ("32.03", "103"),
        ("32.44", "110"),
        ("35.81", "112"),
        ("44.27", "105"),
        ("44.60", "114"),
        ("45.30", "006"),
        ("46.53", "200"),
        ("49.08", "202")
    ]
    assignment_hits = sum(
        1 for peak, hkl in assignments if has_peak_assignment(peak, hkl)
    )
    observed_peak_indexing = assignment_hits / float(len(assignments))

    extinction_absent_word = bool(
        re.search(r"消光|禁戒|缺失|无峰|不出现|禁阻|系统性?缺失|"
                  r"absent|extinct|forbidden|missing|systematic", text_n, re.I))
    hkl_symbol = bool(re.search(r"h\s*\+\s*k\s*\+\s*l", text_n, re.I))
    # I 格子消光条件的两种等价正确写法：
    #   允许式 h+k+l=2n（偶数）  或  禁戒式 h+k+l 为奇数时消光
    cond_even = bool(re.search(
        r"h\s*\+\s*k\s*\+\s*l\s*(?:=|＝|为|is|等于)?\s*(?:2n|even|偶)", text_n, re.I))
    cond_odd = bool(
        hkl_symbol and re.search(r"奇数|odd", text_n, re.I))
    extinction_formula = bool(extinction_absent_word and (cond_even or cond_odd))

    absent_positions = ["7.36", "22.78", "27.24", "33.32"]
    absent_count = sum(1 for x in absent_positions if x in text_n)
    absent_hkls = ["001", "100", "102", "111"]
    absent_hkl_count = 0
    for hkl in absent_hkls:
        spaced = r"\s*".join(list(hkl))
        # (a) 括号包裹（半/全角）；(b) 紧跟角度/波长注记；
        # (c) 作为独立 Miller 三元组 token（两侧非数字/字母、且不接单位或百分号），
        #     以兼容 LaTeX \(001\) 归一后失去括号、或英文逗号列举 "001, 102 and 111"
        bare = (r"(?<![\d.a-zA-Z])" + spaced +
                r"(?![\d.]|\s*(?:%|Å|nm|g|mol|°|度|meV|eV|K\b))")
        if re.search(r"[\(（]\s*" + spaced + r"\s*[\)）]", text_n) or \
           re.search(spaced + r"\s*[（(]\s*\d", text_n) or \
           re.search(bare, text_n):
            absent_hkl_count += 1
    absences_ok = absent_count >= 3 or absent_hkl_count >= 3
    # 若已把体心消光条件写清、且把缺峰与体心格子挂钩，即算判定成立；
    # 「直接列出体心禁戒的 001/100/102/111」这种写法也应接受
    body_centered_named = bool(re.search(
        r"体心|body[\s-]*cent|I[\s-]*(?:型)?(?:四方|centered|centred)|\btI\b",
        text_n, re.I))
    extinction_and_absences = 1.0 if (
        (extinction_formula and absences_ok)
        or (body_centered_named and extinction_absent_word and absences_ok
            and (hkl_symbol or absent_hkl_count >= 3))
    ) else 0.0

    checks = {
        "non_empty_answer": non_empty_answer,
        "not_refusal": not_refusal,
        "crystal_system_tetragonal": crystal_system_tetragonal,
        "bravais_body_centered_tetragonal": bravais_body_centered_tetragonal,
        "lattice_parameters_a_c": lattice_parameters,
        "cell_volume": cell_volume,
        "formula_units_z2": formula_units_z2,
        "observed_peak_indexing": observed_peak_indexing,
        "body_centering_extinction_and_absences": extinction_and_absences
    }

    weights = {
        "non_empty_answer": 0.03,
        "not_refusal": 0.03,
        "crystal_system_tetragonal": 0.10,
        "bravais_body_centered_tetragonal": 0.20,
        "lattice_parameters_a_c": 0.14,
        "cell_volume": 0.10,
        "formula_units_z2": 0.10,
        "observed_peak_indexing": 0.20,
        "body_centering_extinction_and_absences": 0.10
    }

    score = sum(checks[k] * weights[k] for k in weights)
    checks["auto_final_answer_score"] = round(score, 6)
    return checks
```

## LLM Judge Rubric

### Criterion 1：从峰位建立四方倒易点阵模型
**Weight: 25%**

- **Score 1.0：** 明确使用 \(Q=4\sin^2\theta/\lambda^2\)，识别 14.75°、29.77°、45.30° 的 \(Q\) 比约为 \(1:4:9\)，并合理地将其作为同一 \(00l\) 系列；进一步说明为何取偶数级次后可建立四方晶胞。
- **Score 0.5：** 能识别三个峰属于同一方向的谐波系列并据此建立四方模型，但未明确计算 \(Q\)，或没有充分解释为何采用 \((002),(004),(006)\) 而不是 \((001),(002),(003)\)。
- **Score 0.0：** 直接预设晶系而未用峰位关系验证，或错误地把三个峰当作互不相关的反射，导致后续指标化没有统一倒易点阵依据。

### Criterion 2：晶胞参数求解与全谱自洽验证
**Weight: 25%**

- **Score 1.0：** 正确说明由首个 \(00l\) 峰确定 \(c\)，再由独立的非 \(00l\) 峰确定 \(a\)，并用四方关系式对其余峰作交叉验证；指标化体现出同一组参数可统一解释所有观测峰。
- **Score 0.5：** 参数求解路线基本合理，但只使用一两个峰，未检查其余峰的自洽性；或指标化有少量孤立错误但不改变整体模型。
- **Score 0.0：** 将首峰错误当作 \((001)\) 后仍未利用无峰窗口检验，使 \(c\) 缩短一半；或通过逐峰任意指定指标来迁就峰位，没有形成统一的晶胞模型。

### Criterion 3：系统消光与 Bravais 格子判定
**Weight: 35%**

- **Score 1.0：** 将题给四个无峰窗口与具体的低角奇和反射联系起来，使用 \(h+k+l\) 为奇数时系统消光这一条件区分 I 格子与 P 格子，并正确利用题设中“无偶然结构因子相消、无杂峰、检出充分”的限制。
- **Score 0.5：** 知道应根据系统消光判定体心点阵，也给出奇和消光条件，但没有将条件与无峰窗口或 P/I 模型比较充分对应。
- **Score 0.0：** 把缺峰归因于择优取向、强度过弱、杂相或基元结构因子偶然相消；把奇和消光误写为偶和消光；或者据此判为简单四方、底心点阵等错误 Bravais 格子。

### Criterion 4：密度计算的物理与量纲逻辑
**Weight: 15%**

- **Score 1.0：** 正确建立 \(\rho=ZM/(N_AV)\)，区分常规晶胞体积与摩尔体积，并正确处理 Å³ 到 m³、g/mol 到 kg/mol 的单位换算；所得整数 \(Z\) 被用作独立合理性检查，而非用于强行预设点阵。
- **Score 0.5：** 密度关系正确且最终取合理整数，但单位换算或有效数字说明不完整。
- **Score 0.0：** 漏掉 \(N_A\)、错误转换 Å³、混淆质量密度与摩尔密度，或以“体心有两个格点”为由直接断言 \(Z\)，没有使用给定密度数据。
