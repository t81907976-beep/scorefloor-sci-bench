# 生物题模板

每道题一个 `.md`，放在 `tasks/biology/` 下。命名沿用 `test-生物<编号>.md`。
按下面的固定顺序组织；三块评分规范逐块补齐（`lib/authoring.py` 可先生成草稿再人工定稿）。

生物题评分通常关注：**概念是否对应题设、机制链条是否一致、是否误用相近术语、结论是否和材料一致。**

---

# 构造高质量-query

{发送给模型的完整题面。给全所有背景材料、实验条件、已知数据与术语约定，
不要留需要模型脑补的隐含条件；本身可以埋"陷阱条件"作为区分点，
例如易混的相近概念、材料中被忽略的关键限定、反直觉的实验现象。}

# SFT标准-response

{标准解答，分步写清每一步的概念对应、机制链条与最终结论。
这是评分的锚点，`Grading Criteria` 与 `Automated Checks` 的期望值都从这里来。}

# 步骤列表-reference

[1] {关键步骤 1：识别题设对应的概念/机制}
[2] {关键步骤 2：机制链条推理或数据解读}
[3] {…}

## Grading Criteria

{结果检查清单，5~8 条，每条对应标准答案的一个关键结果或推理节点。
只写"这道题最终应满足什么"，不写 Bench 总分/效率/一致性。}

- [ ] 最终结论正确：{结论 + 关键判据/依据}
- [ ] {概念对应题设，未误用相近术语}
- [ ] {机制链条完整且方向正确}
- [ ] {结论与题目所给材料/数据一致}
- [ ] {排除了易混的干扰选项/错误机制}

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。
可复用 `lib/grading_utils.py`（flatten_text / has_any / normalize / miller_indices_present / compact / extract_number / within_tol / is_refusal）。
> `normalize()` 已内置 LaTeX 写法容错（剥离 `\boxed{}`/`\mathrm{}`/`{\rm ..}`、`\(...\)`/`\[...\]`、`\AA`↔`Å`、`\times`→x、`a×10^b`→`ae b`）；抽数值/匹配关键词前先过一遍可显著降低假阴性。因 grade() 须自包含，导入不可用时请把等价逻辑内联。

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

    text = flatten_text(transcript)
    scores = {}

    # 1. 非空 / 非拒答
    scores["non_empty_answer"] = 0.0 if len(text.strip()) < 30 else 1.0
    scores["not_refusal"] = 0.0  # ... 拒答关键词检测

    # 2. 抽取最终结论 / 关键术语命中
    # scores["conclusion_extracted"] = ...
    # scores["key_term_hit"]         = ...   # has_any(text, [关键术语正则])

    # 3. 干扰项/错误机制陷阱标记（命中记 1，供逻辑分回落）
    # scores["hit_distractor"] = ...

    # 4. 加权折算最终答复证据分
    scores["auto_final_answer_score"] = 0.0  # 0.10*非空 + 0.10*非拒答 + ...
    return scores
```

## LLM Judge Rubric

大模型评分负责**过程、概念和逻辑**，不重复判定代码侧已覆盖的最终结论命中。
3~5 个 Criterion，每个写清 `Weight`；分档按本题判分逻辑**专题定制**（档数与间距非固定，
对致命陷阱可直接给 0.0）。每一档都要对应真实可判、互斥、可回落原文的表现。

### Criterion 1: 概念/机制识别（Weight: X%）

**Score 1.0**: {概念对应题设、机制识别准确}
**Score 0.5**: {方向对但混用相近概念或机制说明不足}
**Score 0.0**: {概念判错 / 误用相近术语导致机制判反}

### Criterion 2: 机制链条推理（Weight: X%）

...

### Criterion 3: 与材料/数据的一致性（Weight: X%）

...

### Criterion 4: 干扰项排除与自洽性（Weight: X%）

{写成"过程自洽性"（结论与材料是否一致、有无排除干扰机制），不是"最终结论是否正好命中"。}
