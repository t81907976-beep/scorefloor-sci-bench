# 题目文件模板

每道题一个 `.md`，放在 `tasks/<学科>/` 下。命名沿用 `test-<学科><编号>.md`。
按下面的固定顺序组织；三块评分规范逐块补齐（`lib/authoring.py` 可先生成草稿再人工定稿）。

---

# 构造高质量-query

{发送给模型的完整题面。给全所有已知量、常数、单位约定与符号规定，
不要留需要模型脑补的隐含条件；本身可以埋"陷阱条件"作为区分点。}

# SFT标准-response

{标准解答，分步写清每一步的关键中间量、公式选择与最终结论。
这是评分的锚点，`Grading Criteria` 与 `Automated Checks` 的期望值都从这里来。}

# 步骤列表-reference

[1] {关键步骤 1：识别模型/定则/边界条件}
[2] {关键步骤 2：中间量计算}
[3] {…}

## Grading Criteria

{结果检查清单，5~8 条，每条对应标准答案的一个关键结果或推理节点。
只写"这道题最终应满足什么"，不写 Bench 总分/效率/一致性，不写代码/LLM 分工。}

- [ ] 最终答案正确：{数值 + 单位 + 基准}
- [ ] {识别了题目最容易混淆的关键条件}
- [ ] {使用了正确的模型/公式}
- [ ] {关键中间量拆对}
- [ ] {能回到题设数据形成闭合}

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。
可复用 `lib/grading_utils.py`（flatten_text / has_any / normalize / miller_indices_present / compact / extract_number / within_tol / is_refusal）。
> `normalize()` 已内置 LaTeX 写法容错（剥离 `\boxed{}`/`\mathrm{}`/`{\rm ..}`、`\(...\)`/`\[...\]`、`\AA`↔`Å`、`\times`→x、`a×10^b`→`ae b`）；抽数值/匹配关键词前先过一遍可显著降低假阴性。因 grade() 须自包含，导入不可用时请把等价逻辑内联。

### ⚠️ 五类白拿项：新题一个都不许带（0805 假阳性审计结论）

做法：把 100 份真实答复的**结论数值全部作废**（文字、单位、格式一字不改）后重判，
残留分数就是"假阳性地板"。实测榜单分数里 **55% 与答案对错无关**，病因集中在这五种写法。

| 白拿项 | 为什么白拿 | 换成什么 |
|---|---|---|
| `non_empty_answer`、`not_refusal` | 写够 30 字、没说"我不会"就得分，与题目无关 | 删。空答/拒答由 runner 层记 0 |
| `target_extracted`（只判抽到值） | 抽到值 ≠ 值对；中间量任一数字都可能被当结论 | 合并成 `within_tol(v, target, rel)` 一项，抽不到即 0 |
| `has_unit`、`has_basis`（只判出现过） | 字符串出现在推导任意一处即命中，答错照给 | 单位须与结论数值相邻且量纲相容；基准须带否定否决 |
| `not_trap_*` 写成 `val is None or abs(val-陷阱值)>阈值` | 缺值 → 反向项全为真；软托词比老实拒答分高 | 改扣分项：命中陷阱才扣，缺值不加不扣 |
| 纯文字结论型判据 | 对数值扰动免疫，探针测不出；**说反话与说对话同分** | 配数值锚 + 否定否决 |

第 6 类盲区（0811）：**符号式旁路**。判据允许不含小数的符号写法命中时，数值扰动永远碰不到
它（实测 `h = φ/a_w` 把 `h ≈ 0.750` 扰成 `1.5`，`has_basis` 仍为 1.0）。写符号支要清楚它
测不到，靠人工互斥窗或并联数值锚兜住。

三条容易漏的细节：`\d*` 没有上界（`0\.50\d*` 实际收到 0.51）；百分数支通常比小数支松一档
（`\b2[45](?:\.\d)?\s*%` 放行 24.0~25.9%，错误分支全在里面）；`target_*` 的接受窗不许与
`hit_*` 的触发窗重叠。存在"错误方法也能拟合观测"的题，必须把各分支答案指纹表写进前言，
容差窗按指纹设成互斥——**"残差为零"不构成正确性证据**。

⚠️ **改窗宽必须机械地各造一串验边界，不能靠读正则**（0811 两侧各错一次同一个洞）：
「窗内最远端」「窗内最远端补零」「窗外最近端」三种都要跑。`0\.50(?:[0-5]\d*)?` 的
`\d*` 仍无界（实际上界 0.5059）；而收成 `[0-4]\d?|5(?![0-9])` 又会毙掉窗内的 `0.5050`
—— **尾随零属于同一个数，必须放行**。

自检：写完 `grade()` 后跑两条

```bash
python3 scripts/audit_false_positive.py --task <你的题> --verbose   # 地板占比 <30%
```

```python
# 第四算子：复述题面 + 拒答，占比 >40% 说明判据被题面喂饱
t.grade_fn([{"role": "assistant", "content": t.query + "\n\n由于缺少必要的判定依据，这里不给出最终数值。"}],
           ".", {"task_id": t.task_id})
```

地板占比高于 50% 说明这道题测不出模型能力，回来重写判据。

```python
def grade(transcript: list, workspace_path: str, meta: dict) -> dict:
    import re
    # from lib.grading_utils import flatten_text, has_any, compact, extract_number, within_tol

    def flatten_text(items):
        # 不必加 str 护栏：0811 起 `lib/task_loader.py` 的 `_robust_grade` 入口已把
        # str 形态的 transcript 归一成 list（20/20 题实测 str 档 == list 档）。
        # 题内再加一层是防御调用方，会让后来的人以为这是题目该管的事。
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

    text = flatten_text(transcript)
    scores = {}

    # 1. 结论数值 + 相邻单位一起判：抽不到、单位不贴着数值、量纲不对，都是 0。
    #    不要拆成 target_extracted / has_unit 两项（白拿项②③）。
    # scores["target_with_unit"] = 1.0 if (m and within_tol(...)) else 0.0

    # 2. 中间量：一项一个量，只收"算过才写得出"的派生值，不收题面自带的数。
    # scores["kR_numeric"] = 1.0 if within_tol(..., 4.12, 0.02) else 0.0

    # 3. 文字结论必须配数值锚 + 否定否决（说反话不能与说对话同分）。
    #    否决式要把否定词绑到被判的动作上，跨度内禁 `而`，避免误伤对比句。
    # NEG = r'(?:不|未|非|无|没有|并不|而不|不是|无需|不必|忽略|not|without|no\b)'
    # scores["branch_selected"] = 1.0 if (positive and not negated and 数值锚命中) else 0.0

    # 4. 陷阱写成扣分项，不写成反向项——不给数值时不加不扣（白拿项④）。
    # penalty = 0.25 if (v is not None and within_tol(v, 陷阱值, 0.03)) else 0.0

    # 5. 加权折算。权重只落在「答对才拿得到」的项上，不给非空/非拒答留权重。
    scores["auto_final_answer_score"] = 0.0
    return scores
```

## LLM Judge Rubric

大模型评分负责**过程、概念和逻辑**，不重复判定代码侧已覆盖的最终数值命中。
3~5 个 Criterion，每个写清 `Weight`；分档按本题判分逻辑**专题定制**（档数与间距非固定，
对致命陷阱可直接给 0.0，不必平均分布）。每一档都要对应真实可判、互斥、可回落原文的表现。

### Criterion 1: {关键模型/机制识别}（Weight: X%）

**Score 1.0**: {完全正确的表现}
**Score 0.5**: {方向对但有关键缺口}
**Score 0.0**: {判反 / 套错模板等致命错误}

### Criterion 2: {中间量或边界条件处理}（Weight: X%）

...

### Criterion 3: {公式/模板选择}（Weight: X%）

...

### Criterion 4: {闭合与自洽性}（Weight: X%）

{写成"过程自洽性"，不是"最终答案是否正好命中"。}
