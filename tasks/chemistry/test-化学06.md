# 构造高质量-query	
封闭微反应釜共聚M1/M2,初装M1 100.00 g(M=100.00),M2 120.00 g(M=120.00)；20 min体积收缩15.00 mL(有人按15%低转化处理)。每消耗1 mol M1/M2收缩20.00/10.00 mL。r1=0.300,r2=0.700；瞬时F1=(r1f1^2+f1f2)/(r1f1^2+2f1f2+r2f2^2)。求此时累计聚合物中M1单元摩尔分数。
# SFT标准-response	
1. 先判断模型与题给量的含义。题目给出的是 20 min 时体积收缩 15.00 mL,而不是总单体转化率 15%。Mayo-Lewis 方程给出的是瞬时共聚物组成 F1,不能直接把初始瞬时组成当作累计聚合物组成。封闭釜、无补料、无挥发和副反应信息时,累计聚合物中各单元摩尔数等于相应单体累计消耗摩尔数。

2. 初始物质的量:
M1: n1,0=100.00 g/(100.00 g mol^-1)=1.0000 mol；
M2: n2,0=120.00 g/(120.00 g mol^-1)=1.0000 mol。

3. 设反应后釜内剩余单体为 n1、n2,令 q=n1/n2,则 f1=n1/(n1+n2)=q/(1+q),f2=1/(1+q)。Mayo-Lewis 方程可写为
F1=(r1q^2+q)/(r1q^2+2q+r2)。
瞬时消耗满足
(-dn1)/(-dn2)=F1/(1-F1)=q(r1q+1)/(q+r2)。
又 n1=qn2,所以 dn1/dn2=q+n2(dq/dn2)。代入 r1=0.300、r2=0.700 得
n2(dq/dn2)=q(0.300-0.700q)/(q+0.700),
因此
 d ln n2=(q+0.700)dq/[q(0.300-0.700q)]。

4. 从初始 q0=1、n2,0=1.0000 mol 积分到 q:
ln(n2/1.0000)=∫_1^q (u+0.700)/[u(0.300-0.700u)] du
=(7/3)ln q-(79/21)ln[(0.700q-0.300)/0.400]。
所以
n2(q)=q^(7/3)[0.400/(0.700q-0.300)]^(79/21),
n1(q)=q n2(q)。

5. 用体积收缩衡算确定反应终点。每消耗 1 mol M1 收缩 20.00 mL,每消耗 1 mol M2 收缩 10.00 mL,因此
15.00=20.00(1.0000-n1)+10.00(1.0000-n2)。
将 n1(q)、n2(q) 代入求解,得到
q≈1.251,n2≈0.428 mol,n1≈0.536 mol。
回代:20.00(1-0.536)+10.00(1-0.428)≈15.00 mL,收缩衡算闭合。

6. 累计消耗量即进入聚合物的单元摩尔数:
N1=1.0000-0.536≈0.464 mol,
N2=1.0000-0.428≈0.572 mol。
累计聚合物中 M1 单元摩尔分数为
X1,cum=N1/(N1+N2)=0.464/(0.464+0.572)≈0.448。

因此,20 min 时累计聚合物中 M1 结构单元摩尔分数约为 0.448,即 44.8 mol%。
# 步骤列表-reference
[1] 将初始质量换算为初始物质的量,确认Mayo-Lewis方程使用摩尔分数基准
[2] 判断体积收缩不是总转化率,且瞬时F1不能直接等于累计组成
[3] 由Mayo-Lewis方程和封闭体系单体物料衡算建立dn1/dn2组成漂移方程
[4] 积分得到n2(q)、n1(q),再用体积收缩方程求终点单体量
[5] 由单体消耗量计算累计聚合物中M1单元摩尔分数,并回代检查体积收缩残差

## Grading Criteria

- [ ] 最终答案给出累计聚合物中 M1 单元摩尔分数 `F̄₁ ≈ 0.448（44.8 mol%）`，且明确这是累计组成而非初始瞬时组成 F1,0。
- [ ] 初始摩尔换算 `n₁,₀ = 100.00/100.00 = 1.000 mol`、`n₂,₀ = 120.00/120.00 = 1.000 mol`，`f₁,₀ = 0.5`，确认 Mayo-Lewis 用摩尔分数基准。
- [ ] 判断体积收缩 15.00 mL **不等于**总转化率 15%，且瞬时 F1 不能直接当累计组成（排除"按 15% 低转化处理"陷阱）。
- [ ] 建立体积收缩衡算 `20(1−n₁)+10(1−n₂)=15`（或 `2Δn₁+Δn₂=1.5`），把体积收缩联系到单体消耗量。
- [ ] 由 Mayo-Lewis + 封闭体系物料衡算建立组成漂移方程并积分（Skeist），求解得 `q≈1.251`（或等价地 n₁≈0.536、n₂≈0.428 / Δn₁≈0.464、Δn₂≈0.572，总转化率≈52%）。
- [ ] 由累计消耗量 `F̄₁ = N₁/(N₁+N₂) = 0.464/(0.464+0.572) ≈ 0.448`，并回代体积收缩衡算闭合（残差≈0）。

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。

### v3 口径改造（2026-08-11）

实测：地板 **35% → 0%**（scramble / integers / flip-sign 三档全 0），第四算子（复述题面 + 拒答）**0.35 → 0.0**。五个 run 全判 1.0（原 1.0 / 1.0 / 1.0 / 0.9 / 1.0；五个 run 都是正确答复、无 `true_error_task`。run4 的 0.9→1.0 是修掉一个假阴性：它把漂移解写成 `u≈1.25`，旧 `has_intermediate` 的模式写死了 `q\s*[=≈约]\s*1\.2[0-9]`，符号名不同就漏判 —— 新的 `drift_q` 先走数值窗，符号名不再影响判定）。

改造清单与理由：

- **删掉 `non_empty_answer`（0.10）+ `not_refusal`（0.10）**：存在性判据，与答案对不对无关。
- **删掉 `has_unit`（0.15）**：它的每一条模式（`摩尔分数`、`mol %`、裸 `%`、`F_1`、`累计`）**题面里原样就有**，复述题面再拒答就白拿 0.15，纯数值扰动 5/5 存活。本题答案本身是无量纲摩尔分数，没有可独立核验的量纲信息，故整项删除。
- **删掉 `target_extracted` / `target_match`**：后者原本直接等于前者，等于同一判据计两次权重。
- **`target_F1_cum` 要求"累计"语义绑定**：旧 `target_extracted` 只问全文有没有 `0.44x`/`44.x%` —— 而**瞬时初始组成 F1,0 = 13/30 ≈ 0.433 与目标 0.448 只差 0.015**，裸数值窗根本分不开"累计组成"和"瞬时组成"，正是题面点名的陷阱。现在要求落窗值前后 ±120 字符内出现 `累计`/`cumulative`/`平均组成`/`X1,cum`，且紧邻左侧 40 字符内不得是`瞬时`。
- **`has_intermediate` 拆成三项实数判据**，并删掉裸整数百分号旁路：旧实现的 `\b5[012]\.?\d?\s*%`（总转化率≈52%）是**裸整数分支**，默认扰动器只动小数，这条分支结构性不可见；且五个 run 实测一次都没写过百分号形式的总转化率。改为：
  - `endpoint_monomers`（0.25）：终点单体量 n₁≈0.536 **且** n₂≈0.428 同时落窗；
  - `drift_q`（0.20）：组成漂移积分的解 q≈1.251；
  - `cumulative_units`（0.15）：累计消耗 N₁≈0.464 **且** N₂≈0.572 同时落窗。
  三项都是推导结果，题面不含任何一个。
- **删掉 `shrinkage_closure` 候选项**：体积收缩衡算 `2n₁+n₂=1.5` 的两个数字（2、1.5）都是题给系数的直接化简，`--integers` 扰动下 run2 实测假阳性存活；且 run5 写成 `20n₁+10n₂=15` 的等价形式，同一判据既漏又假阳。**题给常数的线性组合不构成数值锚。**
- **两条陷阱标记升为真扣分，并补第三条**（各 0.25）：`hit_low_conv_0433`（把瞬时初始组成 0.433 当累计组成）、`hit_wrong_0773`（锁在恒比点 f1=0.3 → 0.773）、新增 `hit_treat_as_15pct`（把 15.00 mL 收缩直接当 15% 转化率）。第三条带否证豁免——五个 run 里每一个都写了"不能把 15 mL 当成 15%"，若不先剪掉否定从句，正确答复会被自己的否证句反扣分。
- **等权口径**：删项不重新归一化，分母就是剩下 4 项的权重和（1.00），扣分在其上做减法，最后 clamp 到 [0, 1]。

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

    def strip_reasoning(s):
        """剥掉推理模型的思维链，只留最终答复正文。未闭合的 <think> 之后全部丢弃，
        避免把推理里试算过的候选组成误判成最终答案。"""
        s = re.sub(r'<(think|thinking|reasoning)>.*?</\1>', ' ', s,
                   flags=re.IGNORECASE | re.DOTALL)
        s = re.split(r'<(?:think|thinking|reasoning)>', s,
                     flags=re.IGNORECASE)[0]
        return s

    _SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉₊₋", "0123456789+-")

    raw = strip_reasoning(flatten_text(transcript))
    raw = raw.translate(_SUB)
    for a, b in (("−", "-"), ("—", "-"), ("–", "-"), ("×", "x"),
                 ("·", "*"), ("⋅", "*"), ("≅", "≈"), ("≃", "≈")):
        raw = raw.replace(a, b)
    raw = re.sub(r'\\(?:approx|simeq|sim)', '≈', raw)
    raw = re.sub(r'\\[tdc]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}',
                 r'(\1)/(\2)', raw)
    for _ in range(3):
        raw = re.sub(r'\\(?:boxed|text|mathrm|mathbf|operatorname|rm|bar'
                     r'|bf|it)\s*\{([^{}]*)\}', r'\1', raw)
    raw = re.sub(r'\\[,;:!]|\\ ', ' ', raw)
    for ch in ("$", "\\(", "\\)", "\\[", "\\]"):
        raw = raw.replace(ch, " ")
    raw = raw.replace("**", " ")
    text = raw.lower()

    def numbers(s):
        out = []
        for m in re.finditer(r'(?<![\d.eE^])(\d{1,7}(?:\.\d+)?)'
                             r'(?![\d.]*\s*(?:\^|x\s*10|e[+-]?\d))', s):
            try:
                out.append(float(m.group(1)))
            except ValueError:
                pass
        return out

    nums = numbers(text)

    def in_win(lo, hi):
        return any(lo <= v <= hi for v in nums)

    def has_any(patterns, s=None):
        s = text if s is None else s
        return any(re.search(p, s, flags=re.IGNORECASE) for p in patterns)

    scores = {}

    _CUM = (r'累计|cumulative|平均组成'
            r'|f\s*[-‾¯]?\s*_?\s*1\s*,?\s*cum|x\s*_?1\s*,?\s*cum')

    # 1. 目标值 F̄₁ ≈ 0.448，且必须是**累计**组成。
    #    题面点名的陷阱是"瞬时初始组成当累计组成"，而 F1,0=13/30≈0.433 与
    #    目标 0.448 只差 0.015 —— 裸数值窗分不开这两者，必须要求语义绑定：
    #    落窗值 ±120 字符内出现"累计/cumulative/平均组成/X1,cum"，
    #    且紧邻左侧 40 字符内不是"瞬时"。
    target_cum = False
    for m in re.finditer(r'(?<![\d.])0\.4(?:4[3-9]\d*|5[012]?)(?![\d])'
                         r'|(?<![\d.])44\.[3-9]\d*|(?<![\d.])45\.[012]\d*',
                         text):
        seg = text[max(0, m.start() - 120):m.end() + 60]
        if re.search(_CUM, seg, re.IGNORECASE) and not re.search(
                r'瞬时[^。\n]{0,12}$', text[max(0, m.start() - 40):m.start()]):
            target_cum = True
            break
    scores["target_F1_cum"] = 1.0 if target_cum else 0.0

    # 2. 终点单体量：n₁≈0.536 与 n₂≈0.428 必须同时给出（两者由收缩衡算与
    #    漂移积分联立才能定出，缺一个说明没真解出终点）。
    scores["endpoint_monomers"] = 1.0 if (
        in_win(0.5340, 0.5375) and in_win(0.4270, 0.4292)) else 0.0

    # 3. 组成漂移方程积分的解 q=n₁/n₂≈1.251（Skeist 积分 + 收缩衡算联立）。
    scores["drift_q"] = 1.0 if (
        in_win(1.2480, 1.2530)
        or has_any([r'(?:q|y|u)\s*[≈=约]\s*1\.2[45]'])) else 0.0

    # 4. 累计消耗量 N₁≈0.464 与 N₂≈0.572 同时落窗（F̄₁ 的分子分母）。
    scores["cumulative_units"] = 1.0 if (
        in_win(0.4630, 0.4660) and in_win(0.5705, 0.5730)) else 0.0

    _WEIGHTS = {
        "target_F1_cum": 0.40,
        "endpoint_monomers": 0.25,
        "drift_q": 0.20,
        "cumulative_units": 0.15,
    }
    earned = sum(w for k, w in _WEIGHTS.items() if scores[k] == 1.0)

    # ---- 陷阱标记：命中即扣分，不再只是"供追溯" ----
    #    只记录不扣分等于把"答错"和"没答"抹平，软性答错反而优于诚实拒答。
    #    陷阱一：按 15% 低转化，直接用初始瞬时组成 F1,0=13/30≈0.433 当累计组成。
    scores["hit_low_conv_0433"] = 1.0 if (
        in_win(0.4310, 0.4345)
        or has_any([r'13\s*/\s*30', r'43\.3\s*%'])) else 0.0

    #    陷阱二：误把最终游离组成锁在恒比点 f1=0.3 → F̄₁≈0.773 的错误路径。
    scores["hit_wrong_0773"] = 1.0 if (
        in_win(0.7700, 0.7760)
        or has_any([r'17\s*/\s*22', r'77\.3\s*%'])) else 0.0

    #    陷阱三：把 15.00 mL 体积收缩直接当成 15% 总转化率。
    #    必须先剪掉否证从句 —— 五个 run 每一个都写了"不能把 15 mL 当成 15%"，
    #    不剪的话正确答复会被自己的否证句反扣分。
    _conv_claim = re.sub(
        r'(?:不(?:能|是|应|可|得|要)|并非|而非|不属于|排除|误|错误地)'
        r'[^。\n；;]{0,30}?(?:15\s*%|转化率)', ' ', text)
    scores["hit_treat_as_15pct"] = 1.0 if has_any([
        r'(?:按|视为|当作|取|即)\s*(?:总)?转化率\s*(?:为|=|≈)?\s*15\s*%',
        r'15\s*%\s*(?:的)?(?:总)?转化率',
    ], _conv_claim) else 0.0

    penalty = 0.25 * (
        scores["hit_low_conv_0433"] + scores["hit_wrong_0773"]
        + scores["hit_treat_as_15pct"])

    # 代码侧最终答复证据分：只反映最终答案是否可自动确认。
    scores["auto_final_answer_score"] = round(
        max(0.0, min(1.0, earned - penalty)), 3)

    return scores
```

## LLM Judge Rubric

大模型评分负责**过程、概念和逻辑**，不重复评价代码已经检查过的最终数值命中。若代码侧显示最终值错误，大模型仍应按过程质量独立评分，但不能替代最终答案硬检查。

### Criterion 1: 量意判读与陷阱规避（Weight: 20%）

**Score 1.0**: 明确指出体积收缩 15.00 mL **不是**总转化率 15%，且瞬时共聚组成 F1 **不能**直接当累计聚合物组成；据此拒绝"低转化近似=初始瞬时组成"的捷径。  
**Score 0.5**: 意识到需要用累计组成而非瞬时组成，但未显式点破"15 mL≠15% 转化"这一题面陷阱，或论证含糊。  
**Score 0.0**: 直接按 15% 低转化处理、用初始瞬时组成 F1,0≈0.433 当最终答案，落入题设陷阱。

### Criterion 2: 初始换算与体积收缩衡算（Weight: 25%）

**Score 1.0**: 正确换算 n₁,₀=n₂,₀=1.000 mol、f₁,₀=0.5，并建立体积收缩衡算 `20(1−n₁)+10(1−n₂)=15`（或 `2Δn₁+Δn₂=1.5`），把体积数据正确联系到单体消耗量。  
**Score 0.5**: 初始换算正确并写出收缩方程，但收缩系数/物料关系有次要代数瑕疵，不影响主干。  
**Score 0.0**: 初始摩尔或收缩衡算建立错误（如把 120 g 直接当 1.2 mol 用错式量、收缩方程系数颠倒），导致后续消耗量偏离。

### Criterion 3: 组成漂移方程与积分求解（Weight: 35%）

**Score 1.0**: 由 Mayo-Lewis `dn₁/dn₂=F1/(1−F1)` + 封闭体系衡算建立组成漂移/Skeist 积分方程，正确积分并与体积收缩联立，解出 `q≈1.251`（或 n₁≈0.536、n₂≈0.428 / Δn₁≈0.464、Δn₂≈0.572，转化率≈52%）。  
**Score 0.6**: 建立了正确的 Skeist/漂移积分框架并联立求解，主干正确但积分常数、数值迭代或某一中间量有次要偏差。  
**Score 0.3**: 意识到高转化需积分，但方程建立不完整或数值解明显偏离（如漂移方向判反、积分式系数错）。  
**Score 0.0**: 完全不做组成漂移积分，或用错误的稳态/恒比点假设替代积分（如误设 r₁+r₂=1 存在恒比点把 f₁ 锁在 0.3），导致最终答案严重偏离。

### Criterion 4: 累计组成计算与闭合自洽（Weight: 20%）

**Score 1.0**: 由累计消耗量 `F̄₁=N₁/(N₁+N₂)≈0.448` 得最终答案，并回代体积收缩衡算验证残差≈0，全程自洽。  
**Score 0.5**: 给出 F̄₁ 计算式并得到合理数值，但未做体积收缩回代闭合检查。  
**Score 0.0**: 累计组成公式用错（如用剩余单体分数或瞬时 F1 代替累计消耗比），或结果与前述消耗量不自洽。