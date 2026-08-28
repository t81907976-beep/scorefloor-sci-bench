# 数学题模板

每道题一个 `.md`，放在 `tasks/math/` 下。命名沿用 `test-数学<编号>.md`。
按下面的固定顺序组织；三块评分规范逐块补齐（`lib/authoring.py` 可先生成草稿再人工定稿）。

数学题评分通常关注：**定理/公式是否适用、推导是否成立、关键步骤是否完整、结果是否可验证。**

---

# 构造高质量-query

{发送给模型的完整题面。给全所有已知量、定义域、约束与记号约定，
不要留需要模型脑补的隐含条件；本身可以埋"陷阱条件"作为区分点，
例如易被忽略的边界情形、退化解、定义域限制。}

# SFT标准-response

{标准解答，分步写清每一步用到的定理/引理、关键中间量与最终结论。
这是评分的锚点，`Grading Criteria` 与 `Automated Checks` 的期望值都从这里来。}

# 步骤列表-reference

[1] {关键步骤 1：识别可用定理/建立方程/选定方法}
[2] {关键步骤 2：关键变形或中间量}
[3] {…}

## Grading Criteria

{结果检查清单，5~8 条，每条对应标准答案的一个关键结果或推理节点。
只写"这道题最终应满足什么"，不写 Bench 总分/效率/一致性。}

- [ ] 最终答案正确：{数值/表达式 + 定义域/取值范围}
- [ ] {识别了适用的定理/公式，且验证了适用条件}
- [ ] {关键变形/中间量推对}
- [ ] {处理了容易漏掉的边界/退化/多解情形}
- [ ] {结果可代回原题验证，形成闭合}

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

    # 2. 抽取最终答案（数值/表达式）并判容差或等价
    # scores["target_extracted"] = ...
    # scores["target_numeric"]   = ...   # within_tol(value, target, rel_tol)

    # 3. 关键条件/多解/定义域是否命中
    # scores["has_domain"] = ...

    # 4. 加权折算最终答复证据分
    scores["auto_final_answer_score"] = 0.0  # 0.10*非空 + 0.10*非拒答 + ...
    return scores
```

## LLM Judge Rubric

大模型评分负责**过程、概念和逻辑**，不重复判定代码侧已覆盖的最终数值命中。
3~5 个 Criterion，每个写清 `Weight`；分档按本题判分逻辑**专题定制**（档数与间距非固定，
对致命陷阱可直接给 0.0）。每一档都要对应真实可判、互斥、可回落原文的表现。

### Criterion 1: 定理/方法选择（Weight: X%）

**Score 1.0**: {选对定理并验证了适用条件}
**Score 0.5**: {方法方向对但未验证适用条件或有小缺口}
**Score 0.0**: {用了不适用的定理 / 方法完全错误}

### Criterion 2: 关键推导与中间量（Weight: X%）

...

### Criterion 3: 边界/多解/特殊情形处理（Weight: X%）

...

### Criterion 4: 闭合与自洽性（Weight: X%）

{写成"过程自洽性"（能否代回原题、逻辑是否前后一致），不是"最终答案是否正好命中"。}
