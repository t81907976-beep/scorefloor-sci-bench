# 构造高质量-query	
298 K暗态n-SrTiO₃阴极处理体相浓度为1.00 mM的氧化剂,施加相对平带电势0.300 V的阴极偏压。参数为:施主浓度ND=1.00×10²² m⁻³,有效导带态密度NC=3.00×10²⁶ m⁻³,相对介电常数εr=300,双电层电容Cdl=0.0500 F·m⁻²,标准界面速率常数k0=1.00×10⁻⁵ m·s⁻¹,重组能λ=0.600 eV,氧化剂扩散系数D=8.00×10⁻¹⁰ m²·s⁻¹,膜厚δ=5.00×10⁻⁵ m,电子转移数n=1。取元电荷e=1.602176634×10⁻¹⁹ C,玻尔兹曼常数kB=1.380649×10⁻²³ J·K⁻¹,真空介电常数ε0=8.8541878128×10⁻¹² F·m⁻¹,法拉第常数F=96485.33212 C·mol⁻¹。

令u=eψs/(kBT)、VT=kBT/e、ε=εrε0。电势分配及空间电荷满足V=VTu+|Qs|/Cdl和Qs²=2εkBTND(eᵘ−u−1)。应根据阴极偏压自行选择n型半导体的积累或耗尽支路,并确定Qs的符号。定义双电层反应过电位η=V−VTu,其单位为V。

界面电子转移服从Marcus-Gerischer模型:kMG=k0eᵘI,其中I=⟨exp[−(x+λ−eη)²/(4λkBT)]⟩。这里x、λ和eη均为能量；若统一以eV计算,则eη的数值等于η eV,kBT也应写成eV。对于非简并三维抛物导带,热电子相对导带底的归一化能量分布为p(x)=2√x exp[−x/(kBT)]/[√π(kBT)^(3/2)],x≥0；是否可采用该非简并分布须根据求得的表面电子浓度与NC自行判断。

将界面反应与厚度为δ的稳态平面扩散膜串联,界面浓度记为cs,满足kMGcs=(D/δ)(cb−cs)。求唯一稳态阴极电流密度,并判别载流子是否简并、能带弯曲支路以及主要限速环节。规定阳极电流为正。
# SFT标准-response	
1. 基本参数与单位换算
体相浓度为cb=1.00 mM=1.00 mol·m⁻³。298 K时
kBT=(1.380649×10⁻²³)(298)=4.11433×10⁻²¹ J,
VT=kBT/e=0.0256797 V。
半导体介电常数为
ε=εrε0=300×8.8541878128×10⁻¹²=2.65626×10⁻⁹ F·m⁻¹。

2. 能带弯曲支路和空间电荷符号
对n型半导体,所给阴极偏压使电子向表面积累,因此选择u>0的积累支路。积累电荷由过量电子构成,故半导体空间电荷满足Qs<0。

空间电荷绝对值为
|Qs|=[2εkBTND(eᵘ−u−1)]^(1/2)。
数值上
[2εkBTND]^(1/2)=4.6752×10⁻⁴ C·m⁻²,
所以电势分配方程为
0.300=0.0256797u+0.0093504√(eᵘ−u−1)。
在u>0上,右端严格单调增加,因而积累支路只有一个解。数值求得
u=5.6415,eᵘ=281.89。
于是
ψs=VTu=0.14487 V,
η=V−ψs=0.15513 V,
|Qs|=Cdlη=(0.0500)(0.15513)=7.756×10⁻³ C·m⁻²。
因此
Qs=−7.756×10⁻³ C·m⁻²。

3. 非简并条件检验
由题给Poisson-Boltzmann模型,表面电子浓度为
ns≈NDeᵘ=(1.00×10²²)(281.89)=2.819×10²⁴ m⁻³。
它与有效导带态密度之比为
ns/NC=2.819×10²⁴/(3.00×10²⁶)=9.40×10⁻³≪1。
等价地,
EC−EF,s=kBT ln(NC/ns)≈0.1198 eV≈4.67kBT。
因此表面电子仍为非简并载流子,可以使用题给的Boltzmann型三维抛物导带热电子分布。

4. Marcus-Gerischer重叠因子
统一以eV表示能量:
kBT=0.0256797 eV,λ=0.600 eV,eη的数值为0.15513 eV,
故λ−eη=0.44487 eV。
重叠积分为
I=∫₀∞[2√x exp(−x/kBT)/(√π(kBT)^(3/2))]exp{−[x+λ−eη]²/(4λkBT)}dx。
代入上述数值进行数值积分,得到
I≈2.46×10⁻²。

5. 界面电子转移速率
由
kMG=k0eᵘI,
得到
kMG=(1.00×10⁻⁵)(281.89)(2.46×10⁻²)
≈6.94×10⁻⁵ m·s⁻¹。

6. 膜扩散与界面反应串联
扩散膜传质系数为
km=D/δ=(8.00×10⁻¹⁰)/(5.00×10⁻⁵)
=1.60×10⁻⁵ m·s⁻¹。
稳态条件为
kMGcs=km(cb−cs),
因此
cs=kmcb/(kMG+km)
≈0.1875 mol·m⁻³。
有效串联速率常数为
keff=kMGkm/(kMG+km)
≈1.300×10⁻⁵ m·s⁻¹。
相应的氧化剂还原摩尔通量为
J=keffcb≈1.300×10⁻⁵ mol·m⁻²·s⁻¹。

7. 电流密度及符号
氧化剂在阴极被还原,而题目规定阳极电流为正,因此
j=−nFJ。
代入n=1得
j=−(96485.33212)(1.300×10⁻⁵)
≈−1.254 A·m⁻²。
由于1 A·m⁻²=0.1 mA·cm⁻²,故
j≈−0.1254 mA·cm⁻²。
按合理有效数字可写为
j≈−1.25 A·m⁻²=−0.125 mA·cm⁻²。

8. 限速环节判别
达姆科勒数为
Da=kMG/km≈6.94×10⁻⁵/(1.60×10⁻⁵)≈4.33。
因为kMG>km,膜扩散比界面电子转移更慢。扩散阻力占总串联阻力的比例为
(1/km)/(1/km+1/kMG)=kMG/(kMG+km)≈0.813。
扩散极限电流密度大小为
|jlim|=nFkmcb≈1.544 A·m⁻²,
实际电流约为扩散极限的81.3%。因此该过程并非完全扩散极限,而是界面反应和膜扩散串联控制,其中膜传质为主要限速环节。
# 步骤列表-reference
[1] 计算VT和ε,依据n型半导体在阴极偏压下的能带弯曲选择u>0的电子积累支路,并联立空间电荷与双电层电势分配,求得u=5.641、ψs=0.1449 V和η=0.1551 V。
[2] 由ns=ND eᵘ求得表面电子浓度,并用ns/NC=9.40×10⁻³及EC−EF=4.67kBT判定表面电子仍为非简并,可使用Boltzmann抛物带热电子分布。
[3] 将x、λ、kBT和eη统一用eV表示,数值计算Marcus-Gerischer重叠积分I=2.46×10⁻²,得到kMG=6.93×10⁻⁵ m·s⁻¹。
[4] 计算膜传质系数km=D/δ=1.60×10⁻⁵ m·s⁻¹,并由界面反应与膜扩散串联得到keff=1.30×10⁻⁵ m·s⁻¹；Da=4.33表明主要受膜传质限制。
[5] 用j=−nFcbkeff计算唯一稳态阴极电流密度,得到j=−1.25 A·m⁻²,即阴极电流密度大小为0.125 mA·cm⁻²。

# Grading Criteria

- [ ] 最终稳态电流密度正确：j≈−1.25 A·m⁻²（等价 −0.125 mA·cm⁻²），阴极还原电流取负号，符合“阳极电流为正”的规定。
- [ ] 能带弯曲支路判对：n型半导体在阴极偏压下取电子积累支路（u>0），且空间电荷取 Qs<0。
- [ ] 电势分配闭合求解：联立 V=VTu+|Qs|/Cdl 与 Qs²=2εkBTND(eᵘ−u−1)，解得 u≈5.64、ψs≈0.145 V、η≈0.155 V。
- [ ] 非简并判据成立：由 ns=ND·eᵘ 得 ns/NC≈9.4×10⁻³≪1（或 EC−EF,s≈4.7kBT），据此确认可用非简并 Boltzmann 抛物带热电子分布。
- [ ] Marcus-Gerischer 重叠积分能量单位统一（x、λ、eη、kBT 均以 eV 计），得 I≈2.46×10⁻²，进而 kMG=k0·eᵘ·I≈6.9×10⁻⁵ m·s⁻¹。
- [ ] 界面反应与膜扩散串联正确：km=D/δ=1.60×10⁻⁵ m·s⁻¹，keff=kMG·km/(kMG+km)≈1.30×10⁻⁵ m·s⁻¹。
- [ ] 限速环节判别正确：Da=kMG/km≈4.3，膜扩散阻力约占 81%，判为界面反应与膜扩散串联控制、以膜传质为主要限速。

# Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。

**v3 全面重写（0811）。** 旧版七项里五项与答案对错无关：`non_empty_answer`/`not_refusal`
（白拿①）、`target_extracted` 只判"抽到值"（②）、`has_unit` 只判"抽到单位"（③）、
`has_basis` 是裸 `re.search("积累|accumulat")` —— 纯文字项，对数值扰动完全免疫，且
**说反话与说对话同分**（⑤）。地板 **86%**。改法：删前两项，把 `target_extracted` /
`has_unit` / `target_numeric` / `sign_cathodic_negative` 四项合并成一项
`target_with_unit`（抽不到、单位不贴、量纲不对、符号为正都是 0），裸文字的 `has_basis`
换成六个"算过才写得出"的派生量（u≈5.64 / η≈0.155 / ns/NC≈9.4e-3 / I≈2.46e-2 /
kMG≈6.9e-5 与 keff≈1.30e-5 / 限速判据），符号为正与耗尽支路改扣分项。

实测：地板 **86% → 0%**、第四算子（复述题面+拒答）**0.0**，`--flip-sign` 与含整数档
`--integers` 同为 **0%**，五个真实 run 全 1.0（与 fixture 的 `manual_corrected` 一致，
无需改权威值）。

含整数档单独逼出两个"探针结构上碰不到"的支，都记在下面的判据注释里：**派生量若落在
`_PROTECT` 保护区内（`\frac{}` 分子、`^{}` 指数、`\mathrm{}` 单位串、下标），这一支
等于没有判据。**`2.82×10^24` 与 `e^{5.642}` 各中一条，5/5 与 4/5 假阳性，只能换支或
绑标签。另一条是**裸小数支必须加左边界前查**：`6.9x10^-5` 没有 `(?<![\d.])` 时会被
`k_eff ≈ 16.9x10^-5` 命中。

`rate_limiting_diffusion` 的每一个数值支都必须**绑到自己的标签上**。第一版写成裸的
`4\.3\d*` / `1\.5[45]\d*` / `0\.1(?:9|87|88)`，扰动后 run2/3/5 仍命中（残留地板
0.0858）—— 命中的是 `0.0095x 0.31 =54.32e-3` 里的 `4.3`、`c_b=0.19 mM` 里的 `0.19`
这类与限速判别无关的碎片。裸 `81\s*%` 一支已删：`81` 是整数，只扰小数的探针永远碰不到
它（符号式旁路的整数变体，同化学04 的"稀释 5 倍"）；改收 `81.3%` 或 `0.81x`。

`to_float` 原先写 `exp: str | None` —— **PEP 604 在 Python 3.9.6（本机版本）上于 def
时求值即报 `TypeError`**，凡有脚本 exec 这段代码就会炸。已改成裸参数。

⚠️ **本代码块内所有注释必须缩进或写进 docstring。** 顶格的 `# ` 会被
`lib/task_loader.py::_split_sections` 当成 markdown 标题，截断 `Automated Checks`
段落，`_extract_python_block` 返回空串 → `grade_fn is None`（化学04 踩过）。

```python
import re

def normalize(text: str) -> str:
    """统一乘号、负号、上标、空白与常见 LaTeX 写法，便于抽取。

    LaTeX 容错（否则 `\\boxed{j \\approx -1.25\\ \\text{A/m}^2}` 这类写法会整体漏判）：
    剥离 \\boxed{}/\\text{}/\\mathrm{} 等装饰包裹但保留内容、`\\approx`→≈、
    去掉 \\, 细空格与 $ 定界符、去 markdown 强调号。
    """
    repl = {
        "×": "x", "·": "", "−": "-", "—": "-", "﹣": "-",
        "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
        "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-",
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    text = re.sub(r"\\(?:approx|simeq|sim|cong)", "≈", text)
    text = re.sub(r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"(\1)/(\2)", text)
    for _ in range(3):
        text = re.sub(
            r"\\(?:boxed|text|mathrm|mathbf|operatorname|rm|bf|it)\s*\{([^{}]*)\}",
            r"\1", text)
    text = re.sub(r"\\[,;:!> ]", " ", text)
    text = re.sub(r"\\[\(\)\[\]]", " ", text)
    text = text.replace("$", "").replace("*", "")
    text = text.replace("{", " ").replace("}", " ")
    return re.sub(r"\s+", " ", text)


def to_float(num, exp):
    """不写 `exp: str | None` —— PEP 604 在本机 Python 3.9.6 上 def 时即报 TypeError。"""
    val = float(num)
    if exp:
        val *= 10 ** int(exp)
    return val


def extract_current_density(text: str):
    """
    抽取最终电流密度 j，统一换算到 A·m⁻²（1 mA·cm⁻² = 10 A·m⁻²）。
    兼容科学计数法、x10^、e 记法、A/m^2 与 mA/cm^2 变体。

    写法容错：符号名容 j / i / j_geo（`i=-nFJ=...` 这类写法过去漏判）；数值与单位之间
    容许插入等价推导链（`j=-nFJ=-96485x1.30e-5≈-1.25 A·m-2`），故用「最后一个
    数值 + 单位」而非「符号后紧跟的第一个数值」定位；单位容 A·m-2 / A m^-2 / A/m2。
    跳过 `|j|=...` 绝对值式（其值恒正、不带符号信息），取最后一处带符号的结论式，
    避免答复先写 |j|=1.25 再写 j=-1.25 时被前者截获而误判符号。
    """
    t = normalize(text)
    num = r"(-?\d+\.?\d*)(?:\s*x?\s*10\s*\^?\s*(-?\d+)|\s*e\s*(-?\d+))?"
    unit = (r"(mA\s*[/·]?\s*cm\s*\^?\s*-?2|mA\s*cm\s*-?2"
            r"|A\s*[/·]?\s*m\s*\^?\s*-?2|A\s*m\s*-?2)")
    # 先定位「j/i ... = 数值 单位」整段，再在段内取紧贴单位的那个数值
    pat = (r"(\|?)\s*(?:j|i)(?:_?geo)?\s*(\|?)\s*[=≈~]"
           + r"[^\n]{0,160}?" + num + r"\s*" + unit)
    hits = [m for m in re.finditer(pat, t, re.IGNORECASE)
            if not (m.group(1) or m.group(2))]
    if not hits:
        return None, None
    _l, _r, n, e1, e2, u = hits[-1].groups()
    val = to_float(n, e1 or e2)
    u = u.lower().replace(" ", "")
    if u.startswith("ma"):  # mA/cm^2 -> A/m^2
        val *= 10.0
    return val, u


_X = r"(?:x|\\times|\\cdot|\*)"


def sci(mant, exp):
    """科学计数法的写法容错。

    `2.46×10⁻²` 经 normalize 后可能是 `2.46x10^-2`、`2.46x 10 ^ -2`、`2.46e-2`，
    上标 `⁻²` 已被替换成 `-2`，乘号已统一成 `x`，但 `\\times` 可能残留。

    开头的 `(?<![\\d.])` 是必需的左边界：没有它，`k_eff ≈ 16.9x10^-5` 会命中
    `6.9x10^-5` 这一支（run5 在含整数档上实测假阳性）。凡以裸小数开头的判据支
    都要加同一个前查。
    """
    return (r"(?<![\d.])(?:" + mant + r"\s*(?:" + _X + r")?\s*10\s*\^?\s*\{?\s*" + exp
            + r"|" + mant + r"\s*e\s*" + exp + r")")


_SCORED = ("target_with_unit", "u_solved", "eta_or_qs", "nondegenerate_ratio",
           "overlap_integral", "kmg_or_keff", "rate_limiting_diffusion")


def grade(answer: str) -> dict:
    """`_SCORED` 里没有 non_empty_answer / not_refusal：空答与拒答由 runner 层记 0，
    在 grade() 里再给一遍就是与题目无关的白拿（白拿项①）。
    """
    t = normalize(answer or "")
    checks = {}
    j, unit = extract_current_density(answer)

    # 1. 结论值 + 单位 + 符号一起判：抽不到、单位缺失、符号为正、量纲不对都是 0。
    #    不拆成 target_extracted / has_unit / target_numeric / sign_* 四项
    #    （白拿②③；且四项彼此蕴含 —— target_numeric=1 必然 target_extracted=1）。
    TARGET = -1.25
    checks["target_with_unit"] = (
        j is not None and unit is not None and j < 0
        and abs(j - TARGET) <= abs(TARGET) * 0.08)

    # 2. 电势分配的闭合解 u≈5.64（无量纲，题面只给 V/VT/Cdl，u 必须自己解超越方程）。
    #    必须绑到 `u=` 标签或无量纲/kBT 语境上：裸 `5\.6[34]\d*` 在含整数档会命中
    #    `e^{5.642}` 这种落在 `^{...}` 保护区内的指数（run1/3/4/5 假阳性）。
    checks["u_solved"] = bool(re.search(
        r'u\s*[=≈约~]\s*\+?\s*5\.6[34]\d*'
        r'|5\.6[34]\d*[^。；\n]{0,12}(?:无量纲|kT|k_?B\s*T)', t, re.I))

    # 3. 过电位 η≈0.155 V，或等价的 ψs≈0.1449 V / Qs≈-7.75e-3 C·m⁻²。
    checks["eta_or_qs"] = bool(
        re.search(r'0\.155\d*', t) or re.search(r'0\.1449', t)
        or re.search(sci(r'-\s*7\.7[56]\d*', r'-\s*3'), t))

    # 4. 非简并判据：ns/NC≈9.4e-3，或 EC-EF,s≈0.119 eV=4.67kBT。
    #    ⚠️ `2.8x10^24`（ns 本身）一支已删：答复普遍写成 `\frac{2.82\times10^{24}}{…}`，
    #    而 `2` 落在 `_PROTECT` 的 `(?<=\\frac\{)\d+` 保护区内 —— 含整数档的探针
    #    结构上碰不到它，5/5 假阳性。派生量落在保护区里就等于没有判据，只能换支。
    checks["nondegenerate_ratio"] = bool(
        re.search(sci(r'9\.4\d*', r'-\s*3'), t)
        or re.search(r'0\.119\d*|4\.6[67]\s*k', t, re.I))

    # 5. Marcus–Gerischer 重叠积分 I≈2.46e-2（必须自己做能量积分才写得出）。
    checks["overlap_integral"] = bool(re.search(sci(r'2\.4[56]\d*', r'-\s*2'), t))

    # 6. 串联耦合：kMG≈6.9e-5 与 keff≈1.30e-5 **同时**出现。
    #    要求两个独立派生量，一次数值扰动不可能把两个都打回原值（化学04 的单锚教训）。
    checks["kmg_or_keff"] = bool(
        re.search(sci(r'6\.9[0-9]?\d*', r'-\s*5'), t)
        and re.search(sci(r'1\.30?\d*', r'-\s*5'), t))

    # 7. 限速环节判别：文字结论 + 数值锚。数值锚的每一支都绑到自己的标签上 ——
    #    裸 `4\.3\d*` / `1\.5[45]\d*` / `0\.1(?:9|87|88)` 会命中扰动后的无关碎片
    #    （`0.0095x 0.31 =54.32e-3`、`c_b=0.19 mM`），run2/3/5 各留一处假阳性。
    #    裸 `81\s*%` 一支不许加：整数，只扰小数的探针碰不到（符号式旁路的整数变体）。
    rl_pos = re.search(r'(?:主要)?限速[^。；\n]{0,12}(?:扩散|传质|膜)'
                       r'|(?:扩散|传质|膜)[^。；\n]{0,10}(?:限速|更慢|较慢|占主)', t)
    rl_num = re.search(
        r'(?:Da|达姆科勒)[^0-9\n]{0,12}4\.3\d*'
        r'|4\.3\d*(?![\d.])[^。；\n]{0,8}(?:倍|x)'
        r'|81\.3\s*\\?%|0\.81[0-9](?![\d])'
        r'|(?:lim|极限)[^0-9\n]{0,24}-?\s*1\.5[45]\d*'
        r'|-?\s*1\.5[45]\d*\s*(?:\\?m?athrm\s*)?A'
        r'|c\s*_?\s*s[^0-9\n]{0,16}0\.1(?:9|87|88)\d*', t, re.I)
    checks["rate_limiting_diffusion"] = bool(rl_pos and rl_num)

    passed = sum(bool(checks[k]) for k in _SCORED)

    # 8. 两个陷阱改**扣分项**（白拿④）：命中才扣，缺值不加不扣。
    #    旧式 `val is None or ...` 在缺值时反向项全为真，软托词比老实拒答分高。
    penalty = 0.0
    checks["hit_sign_positive"] = j is not None and j > 0
    checks["hit_depletion_branch"] = bool(
        re.search(r'耗尽[^。；\n而]{0,6}(?:支路|分支)', t)
        and not re.search(r'积累[^。；\n]{0,8}(?:支路|分支)', t))
    for k in ("hit_sign_positive", "hit_depletion_branch"):
        if checks[k]:
            penalty += 0.25

    # 9. 等权折算（口径按 0811 物理题 §6：删项后不重新归一化，
    #    分母就是剩下的计分项数，扣分项在其上做减法）。
    checks["auto_final_answer_score"] = round(
        max(0.0, min(1.0, passed / len(_SCORED) - penalty)), 3)
    return checks
```

# LLM Judge Rubric

仅评过程、概念与逻辑自洽，不重复判定最终数值命中（该项由 Automated Checks 覆盖）。

### Criterion 1: 能带弯曲支路与空间电荷符号识别（Weight: 0.30）

- Score 1.0：明确判定 n型半导体阴极偏压下为电子积累支路（u>0），并正确给出 Qs<0；对“积累 vs 耗尽”的选择有物理依据。
- Score 0.75：正确选择积累支路并求解，但 Qs 符号说明含糊或缺少物理依据。
- Score 0.5：识别到需要在积累/耗尽间选择，但支路选反或符号错误其一，后续被迫修正。
- Score 0.25：未区分支路，直接套用某一分支公式，恰好部分自洽。
- Score 0.0：完全忽略能带弯曲方向，或按 p型/耗尽错误建模。

### Criterion 2: 电势分配闭合求解（Weight: 0.25）

- Score 1.0：正确联立 V=VTu+|Qs|/Cdl 与 Qs²=2εkBTND(eᵘ−u−1)，说明积累支路单调性→唯一解，解出 u、ψs、η 且自洽。
- Score 0.75：联立方程正确并数值求解，但未论证解唯一或个别中间量略偏。
- Score 0.5：方程建立基本正确，但电势分配（ψs 与 η 拆分）或双电层过电位定义有混淆。
- Score 0.25：仅写出部分关系式，未真正闭合求 u。
- Score 0.0：电势分配缺失或用错模型（如忽略双电层电容项）。

### Criterion 3: 非简并判据与 Marcus-Gerischer 处理（Weight: 0.25）

- Score 1.0：用 ns/NC（或 EC−EF,s）定量判定非简并并据此启用 Boltzmann 抛物带分布；重叠积分 I 中 x、λ、eη、kBT 能量单位统一，逻辑正确。
- Score 0.75：非简并判定与 I 计算方法正确，但单位统一或判据表述略有疏漏。
- Score 0.5：完成 I 计算但未做非简并检验，或能量单位混用需读者脑补。
- Score 0.25：套用 Marcus 表达式但重叠积分处理错误（如漏 eᵘ 因子或积分变量错误）。
- Score 0.0：未使用 Marcus-Gerischer 模型或概念性套错公式。

### Criterion 4: 串联耦合与限速环节判别自洽（Weight: 0.20）

- Score 1.0：正确串联界面反应与膜扩散（keff=kMG·km/(kMG+km)），并用 Da 或阻力占比定量判定膜传质为主要限速，结论与数值一致。
- Score 0.75：串联公式与 keff 正确，限速判别方向对但缺定量支撑。
- Score 0.5：串联关系正确，但限速环节判反或仅定性猜测。
- Score 0.25：把界面反应与扩散当作独立/取最小而非串联电阻叠加。
- Score 0.0：未建立串联稳态关系，或限速分析与自身数值矛盾。