# 物理题模板

每道题一个 `.md`，放在 `tasks/physics/` 下。命名沿用 `test-物理<编号>.md`。
按下面的固定顺序组织；三块评分规范逐块补齐（`lib/authoring.py` 可先生成草稿再人工定稿）。

物理题评分通常关注：**物理模型是否选对、边界/参考系/基准是否混淆、中间量与单位是否正确、是否有闭合验证。**

---

# 构造高质量-query

{发送给模型的完整题面。给全所有已知量、常数、单位约定与符号规定（含参考系、正方向），
不要留需要模型脑补的隐含条件；本身可以埋"陷阱条件"作为区分点，
例如易混的参考系、面积/体积基准、近似成立条件。}

# SFT标准-response

{标准解答，分步写清每一步的物理模型、公式选择、关键中间量（含单位）与最终结论。
这是评分的锚点，`Grading Criteria` 与 `Automated Checks` 的期望值都从这里来。}

# 步骤列表-reference

[1] {关键步骤 1：识别物理模型/定律/边界条件}
[2] {关键步骤 2：中间量计算（含单位与量纲核验）}
[3] {…}

## Grading Criteria

{结果检查清单，5~8 条，每条对应标准答案的一个关键结果或推理节点。
只写"这道题最终应满足什么"，不写 Bench 总分/效率/一致性。}

- [ ] 最终答案正确：{数值 + 单位 + 基准/参考系}
- [ ] {识别了题目最容易混淆的物理条件（参考系/基准/近似）}
- [ ] {选用了正确的物理模型/定律/公式}
- [ ] {关键中间量拆对，单位/量纲自洽}
- [ ] {能回到题设数据形成闭合验证}

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。
可复用 `lib/grading_utils.py`（flatten_text / has_any / normalize / miller_indices_present / compact / extract_number / within_tol / is_refusal）。
> `normalize()` 已内置 LaTeX 写法容错（剥离 `\boxed{}`/`\mathrm{}`/`{\rm ..}`、`\(...\)`/`\[...\]`、`\AA`↔`Å`、`\times`→x、`a×10^b`→`ae b`）；抽数值/匹配关键词前先过一遍可显著降低假阴性。因 grade() 须自包含，导入不可用时请把等价逻辑内联。

### ⚠️ 数值容差：用 `within_tol` 比相对误差，不要用正则数位数

**这是 0806 撞出的最大单项假阴性（0.55/1.00）**，写新题时第一条要避开的坑。
判数值不许写成「匹配这几种字面写法」的正则——那等价于规定模型必须写几位有效数字：

```python
# ✗ 错：正则限死小数位数。注释声称兼容 0.4483，实现只收 3 位，多写一位掉 0.55
scores["target"] = 1.0 if re.search(r'0\.4[45]\d?\b', text) else 0.0

# ✓ 对：抽值 + 相对误差比较，写几位都认
m = re.search(r'(-?\d+(?:\.\d+)?(?:\s*[eE]\s*-?\d+)?)\s*(µm|um)', text)
scores["target"] = 1.0 if (m and within_tol(float(m.group(1)), 0.4483, 0.02)) else 0.0
```

三条一起用：

1. **相对误差 `within_tol(v, target, rel)`**，`rel` 按题目物理精度定（常量代入 0.02~0.03，
   多步数值传播 0.05）。绝不用「小数点后 N 位」当判据。
2. **百分数与小数是同一个量的两种写法**，两支都要收（`0.4483` 与 `44.83%`），
   且两支的容差必须一致——化学08 的百分号支比小数支宽 40 倍，放进了两个陷阱值。
3. **正则里的 `\d*` / `\d?` 必须给上限**。`r'0\.50\d*'` 的实际上界是 0.51 而非 0.505，
   `0.5099` 照收。写 `\d{0,2}` 而不是 `\d*`，或者干脆别用正则判数值（见第 1 条）。

**自检**：拿目标值多写一位、少写一位、换成百分数各跑一遍 `grade()`，四种写法必须同分。

### ⚠️ 四类白拿项：新题不许再带（0805 假阳性审计结论）

拿 100 份真实答复做的探针实验（把结论数值全部作废、文字与格式一个字不改，重新判分）
量出：**榜单分数里 55% 与答案对错无关**。病因集中在四种写法，写新题时逐条避开——
不是"尽量避免"，是**这四种项一个都不许出现**：

| 白拿项 | 为什么白拿 | 换成什么 |
|---|---|---|
| `non_empty_answer`、`not_refusal` | 只要写够 30 字、没说"我不会"就得分。**与题目无关**，任何题任何答复都拿 | 删。空答复/拒答由 runner 层记 0，不必在 grade() 里重复给分 |
| `target_extracted`（只判"抽到了值"） | 抽到值 ≠ 值是对的。中间过程任一数字都可能被当成结论 | 合并进数值判据：`within_tol(v, target, rel)` 一项，抽不到就是 0 |
| `has_unit`、`has_basis`（只判单位/基准**出现过**） | 单位字符串出现在推导任意一处即命中，答错也照给 | 要求单位与**结论数值相邻**（同一行、数值后 12 字符内），且量纲与目标相容 |
| `not_trap_*` 写成 `val is None or abs(val-陷阱值)>阈值` | 不给数值 → `val is None` → 反向项**全部为真**。且方向错位：**软托词比老实拒答分高** | 改成扣分项：命中陷阱值才扣，`val is None` 不给分也不扣分 |

第 5 类（0806 化学题在物理08 上发现）：**纯文字结论型判据**（`ordinary_kummer_selected`
这类判"选对了哪支解"的项）对数值扰动免疫，数值探针测不出、但同样白拿。0806 起有了
第三个算子 `scripts/audit_label_swap.py`（把结论标签换成反面表述再判），实测**纯文字
白拿合计 0.000**——但**翻面归零不等于判据是对的**：翻面能压掉只因为它把词根整个换掉，
真实模型写否定句时词根还在。0806 逐条核实现，`has_*_basis` 这一族全部漏否定：

```
「本题未做 ECSA 归一，直接用几何投影面积」→ has_ecsa_basis = 1.0   （权重 0.15）
「背景可忽略不扣」                        → has_bg_subtraction = 1.0（权重 0.10）
「热通道不主导」                          → dominant_thermal = 1.0  （权重 0.10）
```

所以文字结论型判据要两件都做：**① 配一个只有真选对才写得出的派生数值锚**；
**② 加否定词前瞻**，`(?<!不)(?<!未)(?<!无)` 或把窗内出现「不/未/无/非/可忽略」判为 0。
只做 ② 也不够——说对话和不说话仍同分，数值锚才是有鉴别力的那一半。

自检：写完 `grade()` 后跑一次
`python3 scripts/audit_false_positive.py --task <你的题> --verbose`，
地板占比应低于 30%。高于 50% 说明这道题测不出模型能力，回来重写判据。
非数值答案题（结论是"选哪支解"这类）数值探针会跳过，改跑
`python3 scripts/audit_label_swap.py`，并把本题的标签对补进
`tests/fixtures/conclusion-label-pairs.json`。

### ⚠️ 入库前必跑：复述题面 + 拒答（第四个算子，0811 新增）

前三个算子都是**扰动一份已有的答复**，答复结构还在；这一个是**根本不作答**，
量的是「不解题能拿多少」。它专打一条前三个算子碰不到的路：**答复里的数可以来自题面。**

起因是化学04 上量到**一份不给任何答案的拒答拿 0.900，高于所有踩陷阱答复的 0.800**
—— 抽取器兜底取「全文最后一个带单位的数」，复述题面里的 `8.0 mg/L` 就够喂饱它，
于是 `target_extracted`✓`has_unit`✓、三条 `not_trap_*` 全送。全库合计 **36%**，
物理04 高达 85%（`e1_step`/`tau_step`/`has_unit` 三项全被题面喂饱），物理09/10 仅 6%。

不需要新脚本，两行：

```python
t = load_task('tasks/physics/test-物理XX.md')
t.grade_fn([{"role": "assistant", "content": t.query + "\n\n由于缺少必要的判定依据，这里不给出最终数值。"}],
           ".", {"task_id": t.task_id})
```

**占比高于 40% 说明判据被题面喂得太饱，回来重写。**根治方向就是上面四类白拿项的
②③④三条：删「只判抽到了值」的项、单位必须紧贴结论数值、陷阱改扣分项。

```python
def grade(transcript: list, workspace_path: str, meta: dict) -> dict:
    import re
    # from lib.grading_utils import flatten_text, has_any, compact, extract_number, within_tol, is_refusal

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

    text = normalize(flatten_text(transcript))
    scores = {}

    # 1. 结论数值 + 相邻单位一起判：抽不到、单位不贴着数值、量纲不对，都是 0。
    #    不要拆成 target_extracted / has_unit 两项——那是白拿项①③。
    TARGET, REL = 2.60e-13, 0.03
    m_hit = re.search(
        r"(-?\d+(?:\.\d+)?(?:\s*[eE]\s*-?\d+)?)\s*(m\^?2|m²|cm\^?2)", text)
    scores["target_with_unit"] = 1.0 if (
        m_hit and within_tol(float(m_hit.group(1).replace(" ", "")),
                             TARGET, REL)) else 0.0

    # 2. 中间量各自同样要求「数值对」，一项一个量，不给"提到了"的分。
    # scores["kR_numeric"] = 1.0 if within_tol(..., 4.12, 0.02) else 0.0

    # 3. 文字结论必须配数值锚：只有真选对那支解才写得出这个派生值。
    # scores["branch_selected"] = 1.0 if (说了远端衰减支 and within_tol(..., 0.647, 0.05)) else 0.0

    # 4. 陷阱写成扣分项，不写成反向项——不给数值时不加不扣（白拿项④）。
    v_trap = extract_number(text)   # None 时下面两支都不动分
    penalty = 0.25 if (v_trap is not None
                       and within_tol(v_trap, 1.30e-13, 0.03)) else 0.0

    # 5. 加权折算。权重只落在「答对才拿得到」的项上。
    scores["auto_final_answer_score"] = max(0.0, (
        0.60 * scores["target_with_unit"]
        # + 0.25 * scores["kR_numeric"] + 0.15 * scores["branch_selected"]
    ) - penalty)
    return scores
```

## LLM Judge Rubric

大模型评分负责**过程、概念和逻辑**，不重复判定代码侧已覆盖的最终数值命中。
3~5 个 Criterion，每个写清 `Weight`；分档按本题判分逻辑**专题定制**（档数与间距非固定，
对致命陷阱可直接给 0.0）。每一档都要对应真实可判、互斥、可回落原文的表现。

### Criterion 1: 物理模型/定律识别（Weight: X%）

**Score 1.0**: {选对物理模型并说明适用条件}
**Score 0.5**: {模型方向对但边界/近似条件说明不足}
**Score 0.0**: {套错模型 / 参考系或定律判反}

### Criterion 2: 中间量与单位/量纲处理（Weight: X%）

...

### Criterion 3: 公式选择与基准一致性（Weight: X%）

...

### Criterion 4: 闭合与自洽性（Weight: X%）

{写成"过程自洽性"（量纲闭合、能否回代题设），不是"最终答案是否正好命中"。}
