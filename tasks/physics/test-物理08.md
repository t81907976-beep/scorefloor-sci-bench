# 构造高质量-query
在一个用半导体二维电子气制作的无源微波量子模拟器中,传输线末端的横向包络可用有效质量方程描述。由于边缘附近的栅压渐变,半轴区域 x≥0 上的等效势能为

V(x)=-U0 sech²(x/L)。

器件左端 x=0 接的是理想无耗的可调反应性端接；实验人员没有给出端接参数,只说明该端接不吸收能量,也不向系统注入粒子。谱线分析给出一个边缘局域模相对于远处连续谱底的能量为 E=-4.806529902×10^-22 J。已知有效质量 m*=0.067 me,势阱深度 U0=0.0120 eV,边缘长度尺度 L=80.0 Å。

设该端接在低能包络近似下等效为 Robin 边界

ψ'(0)=ψ(0)/λ。

求使上述能量 E 对应于物理边缘局域模的 Robin 长度 λ,结果用 nm 表示。同时必须自行判断 x→∞ 的超几何连接该采用哪一类 Kummer 连接公式：判据是该处两分支的指数差是否为整数,若为整数则必须改用整数差退化的对数型公式。

常数:me=9.1093837015×10^-31 kg,ℏ=1.054571817×10^-34 J·s,1 eV=1.602176634×10^-19 J。不得把 x=0 附近的偶、奇局部解直接当成全局物理解；必须通过远端物理性筛选线性组合。
# SFT标准-response
1. 写出半轴上的定态方程:
[-ℏ²/(2m*) d²/dx² - U0 sech²(x/L)]ψ = Eψ,x≥0。
题给 E = -4.806529902×10^-22 J = -3.0000 meV,U0 = 0.0120 eV = 12.0 meV,L = 80.0 Å = 8.00 nm,m* = 0.067 me。

2. 计算能量尺度:
ℏ²/(2me) = 3.809982116 eV·Å²,所以
ℏ²/(2m*) = 3.809982116/0.067 = 56.86540472 eV·Å²。
于是
ℏ²/(2m*L²) = 56.86540472/80.0² = 0.00888521949 eV。
定义无量纲参数
α² = |E| / [ℏ²/(2m*L²)] = 0.00300000000/0.00888521949 = 0.33763984,
所以 α = 0.5810678。
势阱强度参数满足
ν(ν+1) = U0 / [ℏ²/(2m*L²)] = 0.0120/0.00888521949 = 1.35055937,
故
ν = [-1 + sqrt(1 + 4×1.35055937)]/2 = 0.765132。

3. 远端物理性筛选:
令 z = tanh(x/L)。当 x→∞ 时,z→1。束缚态必须在无穷远指数衰减,不能含增长支,因此只能保留衰减的全局物理解。对于超几何表示,连接到 z→1 时的指数差为 ±α = ±0.5810678,不是整数,所以应使用普通 Kummer 连接公式,而不是整数差退化的对数型连接公式。

4. 物理解可写成关联 Legendre 形式:
ψ(x) = C P_ν^{-α}(tanh(x/L)),
其中 ν = 0.765132,α = 0.5810678。

5. 在 x = 0 处,z = 0,且 dz/dx|0 = 1/L。Robin 条件为
ψ'(0) = ψ(0)/λ,
因此
λ = ψ(0)/ψ'(0) = L·P_ν^{-α}(0) / [dP_ν^{-α}(z)/dz]_{z=0}。
用标准公式
P_ν^μ(0) = 2^μ√π / {Γ[(1-ν-μ)/2] Γ[1+(ν-μ)/2]},
[dP_ν^μ/dz]_{0} = -2^{μ+1}√π / {Γ[(-ν-μ)/2] Γ[(1+ν-μ)/2]},
取 μ = -α,可得
[dP_ν^{-α}/dz]_{0} / P_ν^{-α}(0)
= -2 Γ[(1-ν+α)/2] Γ[1+(ν+α)/2] / {Γ[(α-ν)/2] Γ[(1+ν+α)/2]}。
代入 ν = 0.765132,α = 0.5810678,得到
[dP_ν^{-α}/dz]_{0} / P_ν^{-α}(0) ≈ 0.36774。
于是
ψ'(0)/ψ(0) = (1/L)×0.36774 = 0.36774/(8.00 nm) = 0.045967 nm^-1,
所以
λ = 1 / 0.045967 nm^-1 = 21.75 nm ≈ 21.8 nm。

6. 结论:
使给定能量 E 对应于物理边缘局域模的 Robin 长度为
λ ≈ 21.8 nm,
且 x→∞ 的超几何连接应使用普通 Kummer 连接公式,不应使用整数差退化的对数型连接公式。
# 步骤列表-reference
1：定态方程 $-\hbar^2/(2m^*)\,\mathrm{d}^2\psi/\mathrm{d}x^2-U_0\operatorname{sech}^2(x/L)\psi=E\psi$，$x\geq0$，其中 $E=-3.0000\ \text{meV}$、$U_0=12.0\ \text{meV}$、$L=8.00\ \text{nm}$、$m^*=0.067m_e$。

2：$\hbar^2/(2m^*L^2)=0.008885\ \text{eV}$，定义 $\alpha=\sqrt{|E|/[\hbar^2/(2m^*L^2)]}=0.58107$、$\nu(\nu+1)=U_0/[\hbar^2/(2m^*L^2)]=1.35056$ 得 $\nu=0.76513$。

3：远端连接——$x\to\infty$ 时 $z=\tanh(x/L)\to1$，束缚态要求指数衰减不含增长支，两分支指数差 $\pm\alpha=\pm0.58107$ 非整数，故应使用普通 Kummer 连接公式而非整数差退化的对数型连接公式。

4：远端筛选后的全局物理解写为关联 Legendre 函数 $\psi(x)=C\,P_\nu^{-\alpha}(\tanh(x/L))$，保证 $x\to\infty$ 指数衰减。

5：$x=0$ 处 $z=0$、$\mathrm{d}z/\mathrm{d}x|_0=1/L$，Robin 边界 $\psi'(0)=\psi(0)/\lambda$ 给出 $\lambda=\psi(0)/\psi'(0)=L\cdot P_\nu^{-\alpha}(0)/[\mathrm{d}P_\nu^{-\alpha}/\mathrm{d}z]_0$；代入 $P_\nu^\mu(0)$ 及其导数标准公式得 $\lambda=1/[(1/L)\cdot0.36774]=21.75\ \text{nm}\approx21.8\ \text{nm}$。


## Grading Criteria

- [ ] 正确换算并给出无量纲参数：\(\alpha\approx0.58107\)，\(\nu\approx0.76513\)。
- [ ] 明确指出束缚态必须在 \(x\to\infty\) 衰减，并排除含指数增长支的局部解线性组合。
- [ ] 远端筛选后的全局物理解取为 \(\psi(x)\propto P_\nu^{-\alpha}(\tanh(x/L))\)，而不是未经远端筛选的 \(x=0\) 偶解或奇解。
- [ ] 正确判断远端两分支的指数差不是整数，因此使用普通 Kummer 连接公式。
- [ ] 明确排除整数差退化的对数型连接公式。
- [ ] 正确由 Robin 条件得到 \(\lambda=\psi(0)/\psi'(0)=L\,P_\nu^{-\alpha}(0)/[P_\nu^{-\alpha}]'(0)\)。
- [ ] 最终给出正的 Robin 长度 \(\lambda\approx21.8\ \mathrm{nm}\)，数值和单位均正确。

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程（本段由 lib.authoring 自动生成并通过双向自检）。

```python
def grade(transcript: list, workspace_path: str, meta: dict) -> dict:
    import re

    def content_to_text(content):
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    value = item.get("text", "")
                    if isinstance(value, str):
                        parts.append(value)
            return "\n".join(parts)
        if isinstance(content, dict):
            value = content.get("text", "")
            return value if isinstance(value, str) else ""
        return ""

    def get_final_assistant_text(items):
        if not isinstance(items, list):
            return ""
        for item in reversed(items):
            if isinstance(item, dict) and item.get("role") == "assistant":
                return content_to_text(item.get("content", ""))
        return ""

    def normalize(s):
        if not isinstance(s, str):
            return ""
        table = str.maketrans({
            "−": "-", "–": "-", "—": "-", "⁻": "-",
            "⁺": "+", "⁰": "0", "¹": "1", "²": "2",
            "³": "3", "⁴": "4", "⁵": "5", "⁶": "6",
            "⁷": "7", "⁸": "8", "⁹": "9",
            "×": "x", "·": "*", "，": ","
        })
        s = s.translate(table)
        # LaTeX 关系符与细空格必须先归一：答复普遍写
        # `\alpha=\sqrt{|E|/[\hbar^2/(2m^*L^2)]}\approx 0.5811`，
        # 不把 `\approx` 折成 `≈`，compact 后就成了 `approx0.5811`，
        # numbers() 的 `(?<![\w.])` 前查被字母 x 挡住、整个数值取不到，
        # 派生量判据（α、ν）因此 5/5 集体假阴性。
        s = re.sub(r"(?i)\\(?:approx|approxeq|simeq|cong|doteq)", "≈", s)
        s = re.sub(r"\\[,;:!>]|\\q?quad", " ", s)
        s = re.sub(
            r"(?i)([-+]?(?:\d+(?:\.\d*)?|\.\d+))\s*(?:x|\*)\s*10\s*\^?\s*([-+]?\d+)",
            r"\1e\2",
            s
        )
        return s

    def numbers(s):
        out = []
        pattern = r"(?<![\w.])[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
        for match in re.finditer(pattern, normalize(s)):
            try:
                out.append(float(match.group(0)))
            except Exception:
                pass
        return out

    def close(value, target, rel=0.03):
        if target == 0:
            return abs(value) <= rel
        return abs(value - target) / abs(target) <= rel

    def has_labeled_value_near(label_pattern, target, rel=0.03, win=70):
        """在 compact（去空白）文本上判「符号标签之后的邻域里出现该目标值」。

        原 has_labeled_value 要求「标签 (=|≈) 数值」紧邻，已删（无调用点）：答复
        普遍先写定义式再落数值 —— `\\alpha=\\sqrt{|E|/[\\hbar^2/(2m^*L^2)]}≈0.5811`、
        `q=L\\sqrt{-2m^*E}/\\hbar≈0.58107`、`s=(-1+\\sqrt{1+4(...)})/2≈0.76513`，
        标签与数值之间隔着整条公式，5/5 答复集体判 0（假阴性）。
        判据要看的是「这个无量纲参数算对没有」，故改为标签后 win 字符内找目标值；
        判别力仍全部落在 3% 数值窗上，算错的答复照样进不来。
        """
        for match in re.finditer(label_pattern, compact, re.I):
            for value in numbers(compact[match.end():match.end() + win]):
                if close(value, target, rel):
                    return True
        return False

    def has_robin_length(s):
        ns = normalize(s)
        chunks = re.split(r"[\n。；;!?！？]", ns)
        for chunk in chunks:
            low = chunk.lower()
            has_label = ("λ" in chunk or "lambda" in low or "robin" in low or "罗宾" in chunk)
            has_nm = re.search(r"(?i)\bnm\b|纳米", chunk) is not None
            if has_label and has_nm:
                for value in numbers(chunk):
                    if value > 0 and close(value, 21.8, 0.03):
                        return True

        label_matches = list(re.finditer(r"(?i)λ|lambda|robin|罗宾", ns))
        for match in label_matches:
            window = ns[max(0, match.start() - 60):min(len(ns), match.end() + 140)]
            if re.search(r"(?i)\bnm\b|纳米", window):
                for value in numbers(window):
                    if value > 0 and close(value, 21.8, 0.03):
                        return True
        return False

    def is_refusal(s):
        low = s.lower()
        refusal_phrases = [
            "无法回答", "不能回答", "无法求解", "不能求解",
            "信息不足", "无法确定", "没有足够信息",
            "i cannot answer", "i can't answer", "cannot determine",
            "insufficient information", "unable to solve"
        ]
        return any(p in low for p in refusal_phrases)

    text = get_final_assistant_text(transcript)
    norm = normalize(text)
    low = norm.lower()
    # compact 提到前面来：数值锚判据都要在去空白文本上比对，
    # 否则显示公式里的换行会把「标签 → 数值」的邻域切断。
    compact = re.sub(r"\s+", "", norm)

    # non_empty_answer / not_refusal 的权重已归零（白拿项①）：空答与拒答由 runner
    # 层记 0，在 grade() 里再给一遍就是与题目无关的白拿。两键保留只作诊断输出。
    non_empty_answer = 1.0 if len(re.sub(r"\s+", "", text)) >= 30 else 0.0
    not_refusal = 1.0 if text.strip() and not is_refusal(text) else 0.0

    # 两个无量纲参数的符号各家不同：衰减指数写 α / β / η / κ / ρ / μ / q，
    # 势阱强度参数写 ν / s。只认 SFT 用的 α、ν 会把「记号不同」记成「算错」。
    # 单字母标签要挡掉 LaTeX 命令内部的字母（`\sqrt` 里的 q、s；`\ast` 里的 s），
    # 否则邻域判据会从公式骨架里起跳。
    DECAY_LABEL = (r"(?:α|β|η|κ|ρ|μ|\\?(?:alpha|beta|eta|kappa|rho|mu)"
                   r"|(?<![A-Za-z\\])q(?![A-Za-z]))")
    WELL_LABEL = r"(?:ν|\\?nu|(?<![A-Za-z\\])s(?![A-Za-z]))"
    # 同时接受平方形式（α²=0.33764、ν(ν+1)=1.35056），那是只有换算正确才写得出的派生量。
    decay_exponent_ok = (
        has_labeled_value_near(DECAY_LABEL, 0.58107, 0.03)
        or has_labeled_value_near(DECAY_LABEL, 0.337640, 0.03)
    )
    well_strength_ok = (
        has_labeled_value_near(WELL_LABEL, 0.76513, 0.03)
        or has_labeled_value_near(WELL_LABEL, 1.35056, 0.03)
    )
    dimensionless_parameters = 1.0 if decay_exponent_ok and well_strength_ok else 0.0

    robin_length_nm = 1.0 if has_robin_length(norm) else 0.0

    # ⚠️ 以下三项原本是**纯关键词判据**，数值全错也一字不动地满分（实测
    # ordinary_kummer 5/5、noninteger 5/5、decaying 3/5 白拿）。而且它们的判据词
    # 本身就在题面里：题面把「普通 Kummer 连接公式 vs 整数差退化的对数型连接公式」
    # 连正确答案一起枚举，并直接写明「不得把 x=0 偶奇局部解当全局解」——
    # 复述题面即命中，属于题面喂饱的白拿。
    # 因此统一挂上派生数值锚 decay_exponent_ok（α=κL=0.58107，或等价的 α²=0.33764）：
    # 远端两分支的指数差就是 ±α、衰减支就是 e^{-αx/L}，α 既是「非整数 ⇒ 用普通
    # Kummer」这个结论的判据本身，也是「保留衰减支」的衰减率；它只能由 E、U0、L、m*
    # 换算后解出，题面没给。数值扰动把 α 打掉后这三项一并归零。
    has_kummer = "kummer" in low
    has_ordinary = (
        re.search(r"普通.{0,16}kummer|kummer.{0,16}普通", low) is not None
        or re.search(r"ordinary.{0,16}kummer|standard.{0,16}kummer", low) is not None
        or re.search(r"非退化.{0,16}kummer|non[- ]?degenerate.{0,16}kummer", low) is not None
    )
    ordinary_kummer_selected = 1.0 if (
        has_kummer and has_ordinary and decay_exponent_ok
    ) else 0.0

    noninteger = (
        "非整数" in norm or "不是整数" in norm or "不为整数" in norm
        or re.search(r"(?i)non[- ]?integer|not an integer", norm) is not None
    )
    # 否定词表原来只有「不应/不能/不可/无需/不是/而非/排除/不采用/不使用」，
    # 实际答复更常写「不出现整数差退化的对数型连接」「不需要…对数型公式」
    # 「无对数退化」「不会出现对数项」，措辞不同但结论一致，只认原表会集体判 0。
    rejects_log = (
        re.search(r"(?:不应|不能|不可|不需|无需|不是|不会|不出现|不产生|不存在|不含"
                  r"|无|没有|而非|排除|不采用|不使用)"
                  r"[^\n]{0,24}(?:整数差|退化|对数|简并|ln)", norm) is not None
        or re.search(r"(?:整数差|退化|对数)[^\n]{0,24}"
                     r"(?:不应使用|不能使用|不适用|不需要|无需|不出现|排除)", norm) is not None
        or re.search(r"(?i)(?:not|rather than|instead of|no)[^\n]{0,25}"
                     r"(?:logarithmic|degenerate|log terms?)", norm) is not None
    )
    # 同挂 α 数值锚：「指数差非整数」这句话的全部内容就是 ±α=±0.58107 不是整数，
    # 没算出 α 而只写「不是整数」的，是在复述题面第 12 行的选项枚举。
    noninteger_and_no_log = 1.0 if (
        noninteger and rejects_log and decay_exponent_ok
    ) else 0.0

    has_decay = (
        "衰减" in norm or "指数下降" in norm
        or re.search(r"(?i)\bdecay(?:s|ed|ing)?\b", norm) is not None
    )
    # 「排除增长支」的等价表述远多于原来那三条模板：答复更常正面表述筛选结果
    # （`唯一衰减(recessive)解`、`只有 Ferrers 函数给出 →0`、`必须衰减故只保留…`），
    # 而不是反面声明「舍弃增长支」。只认反面模板会让 5 次全对的答复集体判 0。
    # 判据改为：出现「唯一/只有/只保留/必须取…」这类筛选语，且其邻域谈的是
    # 衰减/有界/局域（compact 上比对，避免公式里的空白与换行切断邻域；
    # compact 已在上文统一定义）。
    selection_words = (r"(?:唯一|只有|只能保留|只保留|仅保留|必须(?:取|选|保留|衰减)"
                       r"|舍弃|排除|不含|去掉|不能含|不得含|含增长)")
    physical_words = (r"(?:衰减|有界|→0|->0|recessive|指数下降|局域|束缚模|物理解"
                      r"|decay)")
    selection_near_decay = any(
        re.search(physical_words,
                  compact[max(0, m.start() - 160):m.end() + 160]) is not None
        for m in re.finditer(selection_words, compact)
    )
    rejects_growth = (
        selection_near_decay
        or re.search(r"(?:不含|排除|舍弃|去掉|消除|不能含|不得含).{0,20}(?:增长|发散)", norm) is not None
        or re.search(r"(?:增长|发散).{0,20}(?:支被舍弃|支应舍弃|系数为零)", norm) is not None
        or re.search(r"(?i)(?:exclude|discard|remove|no).{0,20}(?:growing|growth|divergent)", norm) is not None
    )
    # 反向保险：明确说保留/采用增长支的，无论措辞多齐全都不给分。
    keeps_growth = re.search(
        r"(?:保留|取|采用|选(?:取|用)?)\s*(?:了)?\s*(?:e\^?\{?\+|增长支|增长解|发散支|发散解)",
        compact) is not None
    # 同挂 α 数值锚：衰减支的衰减率就是 α（ψ∝e^{-αx/L}），题面第 14 行已经把
    # 「不得把 x=0 偶奇局部解当全局解」这条防御逻辑写进去了，只认文字等于白送。
    decaying_global_branch = 1.0 if (
        has_decay and rejects_growth and not keeps_growth and decay_exponent_ok
    ) else 0.0

    # 权重按白拿口径重分配：归零 non_empty_answer + not_refusal 共 0.10，
    # 其余各项按 旧权重/(1-0.10) 等比放大（和仍为 1.000，完全正确的答复照拿 1.0）。
    weights = {
        "non_empty_answer": 0.0,
        "not_refusal": 0.0,
        "dimensionless_parameters": 0.111111,
        "robin_length_nm": 0.388889,
        "ordinary_kummer_selected": 0.222222,
        "noninteger_and_no_log": 0.111111,
        "decaying_global_branch": 0.166667
    }

    checks = {
        "non_empty_answer": non_empty_answer,
        "not_refusal": not_refusal,
        "dimensionless_parameters": dimensionless_parameters,
        "robin_length_nm": robin_length_nm,
        "ordinary_kummer_selected": ordinary_kummer_selected,
        "noninteger_and_no_log": noninteger_and_no_log,
        "decaying_global_branch": decaying_global_branch
    }

    total = 0.0
    for key, weight in weights.items():
        total += checks[key] * weight

    checks["auto_final_answer_score"] = round(total, 6)
    return checks
```

## LLM Judge Rubric

### Criterion 1：远端物理性筛选与全局解的构造  
**Weight: 35%**

- **Score 1.0:** 明确说明 \(x=0\) 附近定义的偶、奇局部解一般都含有远端增长成分，不能仅凭局部奇偶性确定物理解；通过 \(x\to\infty\) 的束缚态条件消去增长支，并得到与 \(P_\nu^{-\alpha}(\tanh(x/L))\) 等价的全局衰减解。
- **Score 0.5:** 知道必须施加无穷远衰减条件，也选取了正确类型的全局解，但未解释为什么局部偶解或奇解不能直接作为物理解，或没有清楚说明增长支的消除。
- **Score 0.0:** 直接把 \(x=0\) 的偶解、奇解当作全局物理解；未施加远端条件；或保留了随 \(x\to\infty\) 增长的分支。

### Criterion 2：超几何连接公式的判据  
**Weight: 25%**

- **Score 1.0:** 从 \(z=\tanh(x/L)\to1\) 附近的两个独立渐近指数出发，正确识别指数差与 \(\alpha\) 有关，并说明其不满足整数差退化条件，因此非退化连接公式适用。
- **Score 0.5:** 连接公式类型判断正确，并提到“指数差非整数”，但没有把该判据与远端两个分支的渐近行为清楚联系起来。
- **Score 0.0:** 因参数中出现整数、半整数或误把 \(2\alpha\) 四舍五入为整数而采用对数型退化公式；或完全没有给出连接公式选择的依据。

### Criterion 3：Robin 条件与对数导数  
**Weight: 25%**

- **Score 1.0:** 正确使用 \(z=\tanh(x/L)\) 的链式法则，在 \(z=0\) 处写出 \(\psi'(0)/\psi(0)=(1/L)P'(0)/P(0)\)，并由 \(\psi'(0)=\psi(0)/\lambda\) 得到 \(\lambda=L\,P(0)/P'(0)\)。符号、倒数关系和 \(1/L\) 因子均正确。
- **Score 0.5:** Robin 条件的总体处理正确，但中间省略了链式法则或特殊函数在零点的计算依据；最终逻辑仍能看出是在求全局衰减解的边界对数导数。
- **Score 0.0:** 把 \(\lambda\) 写成 \(\psi'(0)/\psi(0)\)，漏掉 \(L\) 或 \(1/L\) 因子，错误倒置比值，或用未经远端筛选的局部解计算边界导数。

### Criterion 4：参数化、单位与内部一致性  
**Weight: 15%**

- **Score 1.0:** 能量、长度和有效质量的单位换算一致；\(\alpha\) 与 \(\nu\) 的定义分别来自束缚能和势阱强度；所选 \(\nu\) 根及 \(\alpha>0\) 与衰减边界条件一致。
- **Score 0.5:** 参数定义基本正确，但省略部分单位换算或根的选择说明，且不影响后续概念推理。
- **Score 0.0:** 能量或长度换算出现数量级错误；混淆 \(\alpha\) 与 \(\nu\)；选择使远端解增长的符号；或各步骤使用互不一致的参数。
