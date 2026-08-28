# 构造高质量-query	
25.0 ℃时,100.0 mL电镀再生液含M(NO₃)₂、N(NO₃)₂各2.00 mmol·L⁻¹,HL 40.0 mmol·L⁻¹,HNO₃ 2.00 mmol·L⁻¹及NaNO₃ 50.0 mmol·L⁻¹。以1.000 mol·L⁻¹ NaOH滴定,加入体积范围为0至1.60 mL。金属、配体物种限于M²⁺、N²⁺、L⁻、HL、ML₃⁻、NL₃⁻以及M(OH)₂(s)、N(OH)₂(s)。HL的pKa为11.50；配合物累积稳定常数对应X²⁺+3L⁻⇌XL₃⁻,lgβM=15.00、lgβN=17.477；M(OH)₂和N(OH)₂的热力学溶度积分别为10⁻¹⁶·⁰⁰和10⁻¹⁹·⁰⁰；水的热力学离子积为10⁻¹⁴·⁰⁰。常数均采用1 mol·L⁻¹溶液标准浓度和纯固体标准态。各离子的活度系数按lgγi=−0.509zi²[√I/(1+√I)−0.3I]计算,其中I=½Σcizi²,浓度单位为mol·L⁻¹。确定0至1.60 mL NaOH滴定范围内的平衡固相序列,并给出所有固相出现或消失的临界滴定体积。
# SFT标准-response	
设NaOH加入体积为v mL,溶液体积为V=(100.0+v) mL。初始物质的量为nM,T=nN,T=0.200 mmol,nHL,T=4.000 mmol,nHNO3=0.200 mmol,nNaNO3=5.000 mmol。总硝酸根为6.000 mmol,因此加入NaOH后的固定离子分析浓度为[Na+]=(5.000+v)/(100.0+v),[NO3−]=6.000/(100.0+v),浓度单位为mol·L−1。

记g=γ±1为一价离子的活度系数,二价离子的活度系数为γ2。Davies公式为lg g=−0.509[√I/(1+√I)−0.3I],γ2=10^{−0.509×4[√I/(1+√I)−0.3I]},或等价地γ2=g4。

酸碱平衡采用活度形式:
Ka=aH+aL−/aHL=10−11.50,Kw=aH+aOH−=10−14.00。
若以浓度h=[H+]、o=[OH−]、l=[L−]、H=[HL]表示,则
Ka=g2hl/H,Kw=g2ho。
两式相除得l/o=(Ka/Kw)H=10^{2.50}H=316.2278H。

配合物平衡为
βX=aXL3−/(aX2+aL−3),
故[XL3−]=βXγ2g2[X2+]l3。
其中βM=1015.00,βN=1017.477≈3.00×1017。
配体守恒为
LT=H+l+3[ML3−]+3[NL3−],
金属守恒为
0.200 mmol=V([X2+]+[XL3−])+nX,s。
加入碱量可由质子当量守恒写为
v=0.200+1000V{l+3[ML3−]+3[NL3−]+o−h}+2nM,s+2nN,s,
其中v以mL、V以L、各浓度以mol·L−1计,固相物质的量以mmol计。该式同时等价于完整电荷守恒,且包含了HL去质子化、配体进入配合物、金属氢氧化物沉淀以及水中OH−的贡献。

对X(OH)2(s),饱和条件为
QX=aX2+aOH−2=γ2[X2+] (go)2=Ksp,X。
Ksp,M=10−16,Ksp,N=10−19。无固相时要求QX≤Ksp,X；有固相时要求QX=Ksp,X且nX,s≥0。

第一临界点:N(OH)2(s)出现。
在无固相分支上令QN=Ksp,N。数值联立配体守恒、金属守恒、酸碱平衡、电荷或质子当量守恒及Davies方程,得到I≈0.064 mol·L−1,g≈0.809,游离N2+浓度约1.996×10−3 mol·L−1,aOH−≈1.1×10−8,pH≈6.04。对应加入碱量v1≈0.200 mL。此时M的离子积约为10−19,远小于10−16,因此只有N(OH)2(s)开始出现。

第二临界点:M(OH)2(s)出现。
在仅有N(OH)2(s)的分支上,令QM=Ksp,M,同时保持QN=Ksp,N,并满足N固相量非负和M总量守恒。数值结果约为I≈0.0617 mol·L−1,g≈0.809,若以浓度表示则[OH−]≈(4.3±0.8)×10−7 mol·L−1；相应的M游离离子与ML3−之和达到M总分析浓度。加入碱量为v2≈0.628 mL,按另一套舍入可写为0.629 mL。越过该点后,若不引入M(OH)2(s),则QM>Ksp,M,所以M(OH)2(s)必须出现。

第三临界点:M(OH)2(s)消失。
在双固相共存区,两个金属均满足饱和条件。由
[X2+]=Ksp,X/(γ2g2o2),
可得
[ML3−]=βMKsp,M l3/o2=βMKsp,M(l/o)2l,
[NL3−]=βNKsp,N l3/o2=βNKsp,N(l/o)2l。
因βMKsp,M=10−1=0.1000,βNKsp,N=10−1.523≈0.029985,所以
[NL3−]/[ML3−]≈0.29985。
继续滴定时,配体去质子化增强,络合促进沉淀溶解。令M固相量降至零,即
V([M2+]+[ML3−])=0.200 mmol,且N(OH)2仍饱和。数值解为I≈0.0620 mol·L−1,g≈0.809,pH≈9.20,[L−]≈2.0×10−4 mol·L−1,[ML3−]≈1.97×10−3 mol·L−1,[NL3−]≈5.92×10−4 mol·L−1。由完整质子当量守恒得到v3≈1.282 mL。此时N固相仍有剩余,故只有M(OH)2(s)消失。

第四临界点:N(OH)2(s)消失。
在仅有N(OH)2(s)的分支上,M已经全部溶解,M满足无固相金属守恒,同时N满足QN=Ksp,N。令N固相量降至零,即
V([N2+]+[NL3−])=0.200 mmol。
数值结果约为I≈0.0640 mol·L−1,g≈0.809,[L−]≈9.2×10−4 mol·L−1,[OH−]≈1.1×10−4 mol·L−1,pH≈9.95,且[NL3−]≈1.97×10−3 mol·L−1。加入碱量为v4≈1.505 mL。此后两种金属均无固相,必须检查未选固相的离子积。

在v=1.60 mL处的无固相平衡计算给出约QM/Ksp,M≈0.15,QN/Ksp,N≈0.50,均小于1,因此在题目给定范围上限内不会发生固相重新出现。

故最终固相区间为:
1. 0≤v<0.200 mL:无固相；
2. 0.200<v<0.628（约0.629）mL:仅N(OH)2(s)；
3. 0.628（约0.629）<v<1.282 mL:M(OH)2(s)+N(OH)2(s)；
4. 1.282<v<1.505 mL:仅N(OH)2(s)；
5. 1.505<v≤1.600 mL:无固相。
临界滴定体积为0.200、约0.628（或0.629）、1.282和1.505 mL。
# 步骤列表-reference
[1] 建立活度、酸解离、配合平衡、物料守恒、电荷守恒及固相互补条件；将NaOH物质的量通过电荷守恒转换为滴定体积,并保持浓度单位和1 mol·L⁻¹标准态一致。
[2] 在无固相分支上检验两种氢氧化物的离子积,确定N(OH)₂首先饱和,并由完整电荷守恒得到v₁≈0.200 mL。
[3] 在仅有N(OH)₂固相的分支上令M(OH)₂达到饱和,计入M、N配合物及全部电荷项,得到v₂≈0.629 mL。
[4] 在双固相分支上联立两种Ksp条件和金属、配体守恒,判断M固相量由零变正、随后达到极大值并再溶解；由M固相量降为零的边界得到v₃≈1.282 mL。
[5] 在仅有N(OH)₂固相的分支上求N固相量降为零的边界,完整计入约0.0112 mmol OH⁻并检验无固相终点,得到v₄≈1.505 mL及最终固相序列。

## Grading Criteria

- [ ] 最终给出完整的**四段固相序列**：`0≤v<0.200` 无固相 → `0.200~0.628` 仅 N(OH)₂ → `0.628~1.282` M(OH)₂+N(OH)₂ 双固相 → `1.282~1.505` 仅 N(OH)₂ → `1.505~1.600` 无固相，而不是只报"先 N 后 M 一起沉淀"这类单调序列。
- [ ] 四个临界体积全部命中：`v₁≈0.200 mL`、`v₂≈0.628（或 0.629）mL`、`v₃≈1.282 mL`、`v₄≈1.505 mL`，且各自对应正确的事件（出现 / 出现 / 消失 / 消失）。
- [ ] 正确判定**沉淀顺序**：尽管 N²⁺ 的配合物更稳（lgβN=17.477 > lgβM=15.00），但 Ksp,N=10⁻¹⁹ 比 Ksp,M=10⁻¹⁶ 小三个数量级，N(OH)₂ 先沉淀；不得因 β 更大就反推 N 更难沉淀。
- [ ] 识别本题的**非单调**核心：M(OH)₂ 先出现（v₂）后又完全溶解（v₃），中途 n(M,s) 经过极大值（约 0.157 mmol @ v≈1.01 mL）；固相序列不是单向累积。
- [ ] 全程用**活度**判据而非浓度：Ka、Kw、β、Ksp 均写成活度形式，二价离子活度系数取 γ₂=γ₁⁴（由 lgγi=−0.509zi²[√I/(1+√I)−0.3I] 得），并对 I=½Σcizi² 做迭代自洽（I≈0.062~0.064）。
- [ ] 把 NaOH 加入量正确换算成滴定体积：质子当量/电荷守恒中必须同时含 HL 去质子化、L⁻ 进入 ML₃⁻/NL₃⁻ 的 3 倍计数、**沉淀消耗的 2n(X,s)**、以及游离 OH⁻（v₄ 附近约 0.0112 mmol，量级不可忽略）。
- [ ] 双固相区给出解析关系：由 [XL₃⁻]=βX·Ksp,X·l³/o² 得 `[NL₃⁻]/[ML₃⁻]=βN·Ksp,N/(βM·Ksp,M)=10⁻⁰·⁵²³≈0.300`，为常数（与 v 无关）。
- [ ] 在上限 v=1.600 mL 处回检两个离子积均未重新饱和（QM/Ksp,M≈0.17、QN/Ksp,N≈0.56，均<1），说明题给区间内固相不会再出现。

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。

**本题容差必须专题定制**：四个临界体积里 v₁ 与 v₄ 对建模误差**极不敏感**（几乎所有分支都能得到 0.200 与 1.505），真正的判别力集中在 **v₂** 与 **v₃** 上。独立复算（延拓 + 二分，收敛到 1e−14）给出各分支指纹：

| 分支 | v₁ | v₂ | v₃ | v₄ |
|---|---:|---:|---:|---:|
| **标准（活度 + 配合物 + 完整质子当量守恒）** | **0.2001** | **0.6280** | **1.2817** | **1.5049** |
| 错 A：忽略活度系数（γ=1，浓度当活度） | 0.2000 | **0.6147** | 1.2819 | 1.5049 |
| 错 B：忽略 ML₃⁻/NL₃⁻ 配合物 | 0.1999 | **0.6002** | **不存在**（固相永不溶解） | **不存在** |
| 错 C：质子当量守恒漏掉沉淀 2n(X,s) 项 | 0.2001 | **0.2334** | **1.0015** | 1.5049 |
| 错 D：漏掉游离 OH⁻ 项 | **0.0000** | 0.6280 | 1.2788 | **1.4938** |
| 错 E：I 冻结在初值 0.064 不迭代 | 0.2001 | 0.6282 | 1.2817 | 1.5049 |

> 说明：错 E 与标准解差异只在 1e−4 mL 量级（低于题面 0.001 mL 分辨），代码侧**不作为可判别错误**，只由 LLM 侧看是否做了自洽迭代。因此 v₂ 的容差窗口设成 0.626~0.631，刚好排除错 A 的 0.6147 与错 B 的 0.6002，同时容纳标准答案两套舍入 0.628/0.629。

**v3 全面重写（0811）。** 地板 **70%**（全库第二高），四处病因：

1. `non_empty_answer`/`not_refusal` 占 0.15 权重，与题目无关（白拿①）。
2. `has_unit` 收 `\bml\b|毫升|临界体积|滴定体积` —— **题面本身就要求"给出临界滴定体积"**，
   任何答复必写，5/5 无条件命中（白拿③，也是"别用题干自带的词当判据"那条）。
3. `target_v1~v4` 只判"某个数落在窗内 + 附近有体积语义"，**不判这个体积对应哪个事件**。
   把 v₂（M 出现）和 v₃（M 消失）的值互换照样满分，而这两个正是本题唯一有判别力的坐标。
4. `hit_monotonic_sequence` 写成 `0.0 if has_sequence else 1.0` —— 纯反向项，四个 run 命中
   但不扣分，只当标记（白拿④的变体）。

改法：删前两项；`has_unit` 整项删除（语义已并入体积判据的 `\bml\b` 邻域要求）；四个体积
改成 **`_event_hit(值窗, 物种, 事件)`** —— 值必须落窗、且同一行/±90 字符内同时出现物种
（M/N(OH)₂）与正确事件（出现 / 消失），**互换 v₂ v₃ 即判 0**；`has_order` 由纯文字改成
`dual_solid_ratio`，只收双固相区的派生常数 `[NL₃⁻]/[ML₃⁻]=βN·Ksp,N/(βM·Ksp,M)≈0.300`
（题面只给 lgβ 与 Ksp，0.300 与 10^−0.523 必须自己算）；顺序判反改成扣分项。

实测：地板 **70% → 0%**（三档算子 scramble / integers / flip-sign 全 0），第四算子 **0.0**，
标签替换算子（全文 M(OH)₂↔N(OH)₂ 互换）下 `v2_appear_M` 与 `nonmonotonic_sequence` 全部 1→0。
五个 run 判 0.75 / 0.0 / 0.3 / 0.0 / 0.0。

四处踩过的坑记在这里：

- **`10^-19` 不能当"按 Ksp 判顺序"的数值锚** —— 它是题面自带的常数，抄题就有；扰动后
  run3 仍靠它 5/5 命中。换成派生的 `0.300` / `10^-0.523` 才是"算过才写得出"。
- **`0.15[678]`（n(M,s) 极大值 0.157 mmol）与 `0.0112`（游离 OH⁻）合并进
  `activity_intermediate`**：单个活度系数 `0.807` 一支不够，五个 run 里没人写出，
  真实分会集体塌到同一档。
- **顺序判反的扣分项不能只看"M 先析出"** —— `M(OH)₂ 也是先析出后因形成 ML₃⁻ 而溶解`
  说的是**同一物种的时间线**，不是两物种的先后。已加后视窗排除 `先…后…溶解` 句式，
  正反例各 2 条过测（run1 因此从 0.45 回到 0.75）。
- **绑定不能按"行"做，必须按"格"做。** `_event_hit` 的第一版把物种与事件放在
  ±90 字符窗内"各自出现过"就算命中，标签替换后 `v2_appear_M` 仍 1/1 —— 表格第三列
  `| M(OH)₂(s) → M(OH)₂(s)+N(OH)₂(s) |` 里两个物种都在，窗口横跨过去后绑定条件恒真。
  第二版改按 `\n` 切行并禁止跨 `|`，仍然漏 —— **`lib/task_loader.py::_robust_grade`
  会拿 `normalized` 档重判一遍，而 `grading_utils.normalize` 把换行全压成空格**，
  "同一行"退化成"全文"。定稿按 `[|\n]` 一起切格、只看数值所在格及左右各一格，
  物种与事件必须同格且间距 ≤16 字符、中间不夹另一物种。
  **纪律：凡依赖行内邻接的判据，必须在 `normalized` 档上单独验一遍** ——
  那一档没有换行，只有竖线还活着。

⚠️ 本代码块内所有注释必须缩进或写进 docstring：顶格 `# ` 会被 `_split_sections`
当成 markdown 标题，截断本段落导致 `grade_fn is None`（化学04 踩过）。

```python
def grade(transcript: list, workspace_path: str, meta: dict) -> dict:
    import re

    def flatten_text(items):
        parts = []
        for item in items:
            if isinstance(item, dict):
                for key in ("content", "text", "message", "output"):
                    value = item.get(key)
                    if isinstance(value, str):
                        parts.append(value)
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)

    def has_any(text, patterns):
        return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)

    def strip_reasoning(s):
        """剥掉推理模型的思维链，只留真正的最终答复正文。

        闭合的 <think>...</think> 直接删除；未闭合（答复在思考中被截断，
        从未产出最终答案）则丢弃 <think> 之后的全部内容，避免把推理里
        试算过的候选临界体积误判成最终答案。
        """
        s = re.sub(r'<(think|thinking|reasoning)>.*?</\1>', ' ', s,
                   flags=re.IGNORECASE | re.DOTALL)
        s = re.split(r'<(?:think|thinking|reasoning)>', s, flags=re.IGNORECASE)[0]
        return s

    raw = strip_reasoning(flatten_text(transcript))
    for a, b in (("−", "-"), ("—", "-"), ("﹣", "-"), ("×", "x"),
                 ("₁", "1"), ("₂", "2"), ("₃", "3"), ("₄", "4"),
                 ("⁻", "-"), ("²", "2"), ("³", "3")):
        raw = raw.replace(a, b)
    for _ in range(3):
        raw = re.sub(r"\\(?:boxed|text|mathrm|mathbf|operatorname|rm|bf|it)"
                     r"\s*\{([^{}]*)\}", r"\1", raw)
    raw = re.sub(r"\\[,;:!]|\\ |\\\\", " ", raw)
    for ch in ("$", "**", "\\(", "\\)", "\\[", "\\]"):
        raw = raw.replace(ch, " ")
    text = raw.lower()
    scores = {}

    SP_N = r'n\s*\(?\s*oh\s*\)?\s*_?\{?\s*2'
    SP_M = r'm\s*\(?\s*oh\s*\)?\s*_?\{?\s*2'
    APPEAR = r'(?:出现|析出|沉淀|生成|产生|形成|饱和|开始|首次|首现)'
    GONE = r'(?:消失|溶解|回溶|溶完|溶尽|溶掉|全部溶|先溶|不再存在|耗尽|消耗完)'
    V1 = r'\b0\.(?:19[7-9]\d*|20[0-4]\d*)\b'
    V2 = r'\b0\.6(?:2[6-9]|3[01])\d*\b|\b0\.63\b'
    V3 = r'\b1\.2(?:7[89]|8[0-6])\d*\b|\b1\.28\b'
    V4 = r'\b1\.5(?:0\d*|1[01]?)\b'

    def _cells(s):
        """按表格竖线与换行切"格"，返回 [(start, end)]。

        不能只按 `\\n` 切：`lib/task_loader.py::_robust_grade` 会拿
        `normalized` 档重判一遍，而 `grading_utils.normalize` **把换行全压成空格**，
        整篇答复变成一行。此时"同一行"退化为"全文"，四个体积判据一起失效
        （标签替换后 `v2_appear_M` 仍 1/1 命中就是这么来的：翻面后
        `| 0.198 mL | M(OH)_2 首次饱和析出 |` 这一行还在，跨行拿它凑出了绑定）。
        竖线是表格写法里唯一在 normalize 后仍然存活的分隔符，必须一起当边界。
        """
        out, prev = [], 0
        for m in re.finditer(r'[|\n]', s):
            out.append((prev, m.start()))
            prev = m.end()
        out.append((prev, len(s)))
        return out

    CELLS = _cells(text)

    def _event_hit(num_pat, species, other, event):
        """体积值落窗 **且** 同格内「物种」与「事件词」紧邻绑定。

        旧版只判「数落窗 + 附近有体积语义」，于是把 v2（M 出现）与 v3（M 消失）
        的值互换照样满分 —— 而这两个坐标是本题唯一有判别力的地方。

        绑定的三重约束（缺一个就能被标签替换算子绕过，都是实测逼出来的）：
        1. 体积语义（mL/毫升/体积/V₁~V₄）在数值所在格 ±1 格内出现；
        2. 物种与事件词落在**同一格**里，间距 ≤16 字符，且中间不得夹另一物种 ——
           `| 0.629 mL | N(OH)_2 饱和析出 | M(OH)_2(s)->M(OH)_2(s)+N(OH)_2(s) |`
           这种表格行的第三列里两个物种都在，跨格取词的话"物种与事件各自出现过"
           永远成立，等于没判绑定；
        3. 只允许数值所在格及左右各一格 —— 表格把体积与事件分列两格是常见写法，
           但再往外就会串到相邻行（normalize 压掉换行后尤其危险）。

        改完后 `scripts/audit_label_swap.py` 把全文 M(OH)₂↔N(OH)₂ 互换，
        v1~v4 全部 1 → 0，绑定确认真的生效。
        """
        for m in re.finditer(num_pat, text):
            idx = next((i for i, (a, b) in enumerate(CELLS)
                        if a <= m.start() < b), None)
            if idx is None:
                continue
            near = [CELLS[j] for j in (idx - 1, idx, idx + 1)
                    if 0 <= j < len(CELLS)]
            if not re.search(r'\bml\b|毫升|体积|v\s*_?\{?\s*[1-4]',
                             " ".join(text[a:b] for a, b in near), re.I):
                continue
            for a, b in near:
                cell = text[a:b]
                for sm in re.finditer(species, cell, re.I):
                    for em in re.finditer(event, cell):
                        p, q = sorted(((sm.start(), sm.end()),
                                       (em.start(), em.end())))
                        gap = cell[p[1]:q[0]]
                        if len(gap) > 16 or re.search(other, gap, re.I):
                            continue
                        return True
        return False

    WEIGHTS = {
        "v1_appear_N": 0.05,
        "v2_appear_M": 0.20,
        "v3_dissolve_M": 0.20,
        "v4_dissolve_N": 0.10,
        "nonmonotonic_sequence": 0.20,
        "dual_solid_ratio": 0.10,
        "activity_intermediate": 0.15,
    }

    ION_N = r'(?<![a-z])n\s*(?:2\s*)?\+'
    ION_M = r'(?<![a-z])m\s*(?:2\s*)?\+'
    ANY_N = SP_N + r'|' + ION_N
    ANY_M = SP_M + r'|' + ION_M

    scores["v1_appear_N"] = 1.0 if _event_hit(
        V1, ANY_N, ANY_M, APPEAR) else 0.0
    scores["v2_appear_M"] = 1.0 if _event_hit(
        V2, ANY_M, ANY_N, APPEAR) else 0.0
    scores["v3_dissolve_M"] = 1.0 if _event_hit(
        V3, ANY_M, ANY_N, GONE) else 0.0
    _v4_label = re.search(
        r'第\s*(?:四|4)\s*临界点[^。\n]{0,6}' + SP_N + r'[^。\n]{0,8}' + GONE,
        text) and re.search(V4, text)
    scores["v4_dissolve_N"] = 1.0 if (
        _event_hit(V4, ANY_N, ANY_M, GONE) or _v4_label) else 0.0

    seq_M = re.search(SP_M + r'[^。\n|]{0,30}' + GONE, text) or \
        re.search(GONE + r'[^。\n|]{0,20}' + SP_M, text)
    seq_N = re.search(SP_N + r'[^。\n|]{0,30}' + GONE, text) or \
        re.search(GONE + r'[^。\n|]{0,20}' + SP_N, text)
    seq_none = re.search(r'无固相|没有固相|不存在固相|无沉淀', text)
    seq_num = re.search(V3, text) and re.search(V4, text)
    scores["nonmonotonic_sequence"] = 1.0 if (
        seq_M and seq_N and seq_none and seq_num) else 0.0

    scores["dual_solid_ratio"] = 1.0 if re.search(
        r'0\.300(?![\d])|0\.29\d(?![\d])'
        r'|10\s*\^?\s*\{?\s*-\s*0\.52\d*|0\.523'
        r'|双固相[^。\n]{0,6}共存'
        r'|m\s*\(?\s*oh\s*\)?\s*_?\{?\s*2[^。\n]{0,4}\)?\s*\(?s?\)?\s*\+\s*'
        r'n\s*\(?\s*oh\s*\)?\s*_?\{?\s*2', text, re.I) else 0.0

    scores["activity_intermediate"] = 1.0 if re.search(
        r'0\.80[6-9]\d*|0\.81[01](?![\d])'
        r'|(?:γ|gamma|g)\s*_?\s*[1±]?\s*[≈=约]\s*0\.8[01]'
        r'|(?:γ|gamma)\s*_?\s*2\s*[≈=约]\s*0\.4[23]\d*'
        r'|i\s*[≈=约~]\s*0\.06[0-5]\d*'
        r'|0\.0112|0\.011[0-3](?![\d])'
        r'|0\.15[678](?![\d])'
        r'|0\.0299\d*|0\.02998', text, re.IGNORECASE) else 0.0

    earned = sum(w for k, w in WEIGHTS.items() if scores[k])

    penalty = 0.0
    scores["hit_no_solid_at_all"] = 1.0 if re.search(
        r'(?:没有|无|不会有|未|不)[^。\n]{0,8}(?:任何)?[^。\n]{0,4}固相'
        r'(?![^。\n]{0,6}(?:重新|再次|再度|又))[^。\n]{0,8}(?:析出|出现|生成)'
        r'|全程[^。\n]{0,6}(?:无固相|液相)'
        r'|(?:出现|消失)[^。\n]{0,10}体积[^。\n]{0,6}(?:都)?不存在', text) else 0.0

    rev = re.search(
        SP_M + r'[^。\n]{0,20}(?:先|首先|最先|率先)' + APPEAR
        + r'|(?:先|首先|最先|率先)' + APPEAR + r'[^。\n]{0,16}' + SP_M, text)
    scores["hit_order_reversed"] = 1.0 if (
        rev and not re.search(r'[^。；\n]{0,12}(?:后|再|随后|接着)[^。；\n]{0,14}'
                              + GONE, text[rev.end():rev.end() + 40])) else 0.0

    scores["hit_ignore_activity"] = 1.0 if re.search(r'\b0\.61[3-6]\d*\b', text) else 0.0
    scores["hit_no_solid_term"] = 1.0 if re.search(
        r'\b0\.23[2-5]\d*\b|\b1\.00[01]\d*\s*m?l\b', text) else 0.0

    for k in ("hit_no_solid_at_all", "hit_order_reversed",
              "hit_ignore_activity", "hit_no_solid_term"):
        if scores[k]:
            penalty += 0.25

    scores["auto_final_answer_score"] = round(
        max(0.0, min(1.0, earned - penalty)), 3)
    return scores
```

## LLM Judge Rubric

大模型评分负责**过程、概念和逻辑**，不重复评价代码已经检查过的临界体积数值命中。若代码侧显示体积错误，大模型仍应按过程质量独立评分，但不能替代最终答案硬检查。

本题的特殊性：v₁≈0.200 mL 与 v₄≈1.505 mL 在几乎所有建模分支下都能算出（含忽略活度、冻结离子强度），因此"我算出 0.200 和 1.505 了"**不构成**建模正确性的证据。裁判必须看模型是否在**双固相分支上真正联立两个 Ksp**、是否把 NaOH 量按**完整质子当量守恒**换算成体积，而不是看它报了几个数。

### Criterion 1: 沉淀顺序判定与 Ksp/β 的竞争关系（Weight: 25%）

**Score 1.0**: 在无固相分支上分别计算两个离子积 QM、QN 与各自 Ksp 比较，指出 **N(OH)₂ 先饱和**——原因是 Ksp,N=10⁻¹⁹ 比 Ksp,M=10⁻¹⁶ 小三个数量级，这一因素压过 N 的配合物更稳（lgβN=17.477 > lgβM=15.00）带来的相反倾向；并给出 v₁ 处 QM/Ksp,M≈10⁻³ 这类定量对照说明此时 M 远未饱和。
**Score 0.6**: 正确判出 N(OH)₂ 先沉淀并做了离子积比较，但只凭 Ksp 大小直接下结论，未讨论 β 差异带来的反向拉力，也未给出另一金属离子积的定量余量。
**Score 0.3**: 结论正确但论证是定性套话（"N 的溶度积更小所以先沉淀"），全程没有真正算过任一离子积，或把配合物对游离 [X²⁺] 的削减完全忽略。
**Score 0.0**: 判成 M(OH)₂ 先沉淀，或因 lgβN 更大而推断 N 更难沉淀（把配合物稳定性当沉淀顺序的决定因素），顺序从根上错。

### Criterion 2: 活度模型与离子强度自洽（Weight: 20%）

**Score 1.0**: 全部平衡常数写成**活度**形式（Ka=a_H·a_L/a_HL、Kw=a_H·a_OH、β=a_XL3/(a_X·a_L³)、Ksp=a_X·a_OH²），由 lgγi=−0.509zi²[√I/(1+√I)−0.3I] 得二价离子 **γ₂=γ₁⁴**，并对 I=½Σcizi² 做**迭代自洽**（I≈0.062~0.064、γ₁≈0.807~0.809），说明主导 I 的是 NaNO₃ 底液而非微量金属物种。
**Score 0.6**: 用了活度形式并正确取 γ₂=γ₁⁴，但把 I 直接冻结在初值 0.064 不迭代（本题该近似只造成 ~10⁻⁴ mL 偏差，属可接受的次要偏差），或未交代 γ₂ 与 γ₁ 的 z² 关系来源。
**Score 0.3**: 意识到要做活度校正但只对部分常数（如只对 Ksp、不对 β 或 Ka）应用，或把二价离子也按一价 γ₁ 处理，活度模型内部不一致。
**Score 0.0**: 全程用浓度代替活度（γ≡1），或写出 Davies 式后从未真正代入数值，题给活度公式沦为摆设。

### Criterion 3: 完整质子当量/电荷守恒 → 滴定体积换算（Weight: 30%）

**Score 1.0**: 建立 `v = n_HNO3 + 1000V{l + 3[ML₃⁻] + 3[NL₃⁻] + o − h} + 2n(M,s) + 2n(N,s)` 这类完整守恒式（或等价的完整电荷守恒），四项贡献齐全并说清各自来源：HL 去质子化、每个 XL₃⁻ 计 **3 个** L⁻、每 mol X(OH)₂ 沉淀消耗 **2 mol** OH⁻、以及游离 OH⁻（在 v₄ 附近约 **0.0112 mmol**，相对 1.505 mL 不可忽略）；并核对该式与电荷守恒等价。
**Score 0.6**: 守恒式主干正确、四类贡献都在，但某一项系数或量级有次要偏差（如 XL₃⁻ 的 3 倍计数写错一次、OH⁻ 项只做量级估计未代入），不影响临界体积的量级与序列结构。
**Score 0.3**: 只用了物料守恒 + 平衡常数而未建立可解出 v 的守恒关系（把 v 当成外部扫描参数逐点试，却不写出 v 与溶液组成的显式约束）；或漏掉沉淀的 2n(X,s) 项（该错误把 v₂ 从 0.628 拖到 0.233、v₃ 从 1.282 拖到 1.00，属结构性错误但仍保留部分推理骨架）。
**Score 0.0**: 用"加入的 NaOH 全部用于中和 HL"这类线性化的当量式直接除算体积（即把滴定曲线当分段线性），或完全不做体积换算而只给 pH 节点，题目要求的临界**体积**从未真正求出。

### Criterion 4: 双固相分支联立与非单调性识别（Weight: 25%）

**Score 1.0**: 在双固相区**同时**施加 QM=Ksp,M 与 QN=Ksp,N，由 [X²⁺]=Ksp,X/(γ₂γ₁²o²) 推出 [XL₃⁻]=βX·Ksp,X·l³/o²，从而得到与 v 无关的常数比 **[NL₃⁻]/[ML₃⁻]=βN·Ksp,N/(βM·Ksp,M)=10⁻⁰·⁵²³≈0.300**；并明确识别 **n(M,s) 先增后减**（极大约 0.157 mmol @ v≈1.01 mL）、由配体去质子化增强促成 M(OH)₂ **完全回溶**，用 n(X,s)≥0 的互补条件定位 v₃、v₄，最后在 v=1.600 mL 回检 QM/Ksp,M≈0.17、QN/Ksp,N≈0.56 均<1，确认区间内固相不再出现。
**Score 0.6**: 正确联立两个 Ksp 并识别出 M(OH)₂ 会回溶、给出四段序列，但缺少常数比 0.300 的解析结论，或未做 v=1.600 处的重饱和回检，或对 n(M,s) 的非单调走势只有结论没有依据。
**Score 0.3**: 意识到络合会促溶、提到固相可能减少，但双固相区未真正联立两个饱和条件（只按单一 Ksp 处理，另一金属仍走无固相守恒），导致 v₃ 只能定性断言；或把 n(X,s)≥0 的互补条件当成事后检查而非定界条件。
**Score 0.0**: 给出单向累积的固相序列（沉淀出现后就一直存在，只有"仅 N → N+M"两段），完全没有识别 M(OH)₂ 在 v₃ 消失、N(OH)₂ 在 v₄ 消失；或忽略 ML₃⁻/NL₃⁻ 配合物（此时固相永不溶解，v₃、v₄ 在物理上不存在），本题的核心机制整体缺失。
