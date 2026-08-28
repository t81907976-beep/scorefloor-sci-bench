# 题目

CO2电解槽内探针 `Ox+e⇌Red`，`I<0` 为还原，`jgeo=I/Ageo`，`x` 由电极指向溶液。温度 `25.0℃`，即 `T=298.15 K`；`Ageo=0.196 cm2`，`ECSA=0.588 cm2`，`I=-12.0 μA`，`Eapp-E0′=-81.5 mV`，`Ru=24.0 Ω cmgeo2`；`cOx*=1.00 mM`，`cRed*=1.00 mM`，`DOx=0.000006 cm2 s-1`，`DRed=0.000008 cm2 s-1`，`δ=50.0 μm`，`αa=0.42`，`αc=0.58`，`n=1`，`R=8.314 J mol-1 K-1`，`F=96485 C mol-1`。EIS以 `Ω cmgeo2` 给出：高频截距 `24.0 Ω cmgeo2`，`45°` 外推右截距 `597 Ω cmgeo2`，低频平台 `980 Ω cmgeo2`。求该 `Ox/Red` 探针在 `ECSA` 基准下的本征标准速率常数 `k0`。

# 答案

1. EIS 分叉判据：阻抗以 `Ω cm_geo^2` 给出，高频截距为 `Ru=24.0 Ω cm_geo^2`；`45°` 外推右截距为 `Ru+Rct,geo=597 Ω cm_geo^2`，所以 `Rct,geo=597-24.0=573 Ω cm_geo^2`。低频平台为 `Ru+Rct,geo+RD=980 Ω cm_geo^2`，所以 `RD=980-597=383 Ω cm_geo^2`。`RD` 是有限扩散小信号平台，不可当作 `Rct` 反演 `k0`。
2. 直流几何电流密度：`j_geo=I/A_geo=(-12.0×10^-6 A)/(0.196 cm^2)=-6.122×10^-5 A cm_geo^-2`。扩散层厚度 `δ=50.0 μm=5.00×10^-3 cm`。题设 `x` 由电极指向溶液，Fick 通量正向离开电极；阴极还原消耗 `Ox` 并生成 `Red`，因此 `N_Ox=j_geo/F`，`N_Red=-j_geo/F`，且 `N_i=D_i(c_i,s-c_i,*)/δ`。
3. 表面浓度：`c_Ox,s=c_Ox,*+j_geoδ/(F D_Ox)=4.71×10^-7 mol cm^-3=0.471 mM`；`c_Red,s=c_Red,*-j_geoδ/(F D_Red)=1.397×10^-6 mol cm^-3=1.397 mM`。`Ox` 下降、`Red` 上升，且由于扩散系数不同，浓度改变量不同。
4. 欧姆降校正：`Ru` 是面积归一电阻，所以使用 `j_geo Ru`，不是 `I × Ω cm^2`。`E_int-E0′=(E_app-E0′)-j_geo Ru=-0.0815-(-6.122×10^-5×24.0)=-0.08003 V`。
5. 面积基准转换：EIS 的 `Rct` 为几何面积基准，而 `k0` 要求 `ECSA` 基准。`ECSA/A_geo=0.588/0.196=3.000`，因此 `Rct,ECSA=Rct,geo(ECSA/A_geo)=573×3.000=1719 Ω cm_ECSA^2`，故 `(∂j_ECSA/∂E)_c=1/Rct,ECSA=5.82×10^-4 A cm_ECSA^-2 V^-1`。
6. 非零偏置 BV 斜率：对 `Ox+e⇌Red`，取阳极电流为正，`j_ECSA=F k0[c_Red,s exp(α_a fξ)-c_Ox,s exp(-α_c fξ)]`，其中 `f=F/RT=38.92 V^-1`，`ξ=E_int-E0′=-0.08003 V`。固定表面浓度的小信号电荷转移导数为 `∂j_ECSA/∂E=F k0 f[α_a c_Red,s exp(α_a fξ)+α_c c_Ox,s exp(-α_c fξ)]`。这里不能使用零偏置 `RT/(nFI0)` 模板，也不能使用体相浓度。
7. 数值代入：`exp(α_a fξ)=0.270`，`exp(-α_c fξ)=6.09`。加权浓度项 `B=0.42(1.397×10^-6)(0.270)+0.58(4.71×10^-7)(6.09)=1.82×10^-6 mol cm^-3`。于是 `k0=(1/Rct,ECSA)/(F f B)=8.5×10^-5 cm s^-1`。
8. 闭合检查：代回 BV 得 `j_ECSA≈-2.04×10^-5 A cm_ECSA^-2`，乘 `ECSA/A_geo=3.000` 后为 `j_geo≈-6.12×10^-5 A cm_geo^-2`，对应 `I≈-12.0 μA`；代回微分式得 `Rct,geo≈573 Ω cm_geo^2`，与 EIS 右截距 `597=24+573` 一致。

## 解题思路

[1] 先由 EIS 截距判断 `Rct,geo=597-24.0=573 Ω cmgeo2`，并确认低频平台只给 `RD=383 Ω cmgeo2`，不作为 `Rct`。  
[2] 按 `I<0`、`x` 由电极指向溶液和 Fick 通量符号，用直流电流密度修正界面浓度，得 `cOx,s=0.471 mM`、`cRed,s=1.397 mM`。  
[3] 用面积归一 `Ru` 做直流 IR 校正，得到 `Eint-E0′=(Eapp-E0′)-jgeoRu=-0.0800 V`。  
[4] 在非零偏置下写固定表面浓度的 BV 微分斜率，并把 EIS 的几何面积 `Rct` 换算到 `ECSA` 基准。  
[5] 由 `∂jECSA/∂E=1/Rct,ECSA` 反演 `k0`，并用 BV 电流与 `Rct,geo` 回代闭合，得 `k0=8.5×10^-5 cm s^-1`。

## Grading Criteria

- [ ] 最终答案给出 `k0`，且数值接近标准答案、单位正确、明确是 `ECSA` 基准。
- [ ] 解答从 EIS 截距得到 `Rct,geo=597-24=573 Ω cmgeo2`，没有把低频平台直接当作 `Rct`。
- [ ] 解答考虑直流电流造成的表面浓度变化，而不是直接使用体相浓度反演 `k0`。
- [ ] 解答正确处理欧姆降校正，并保持几何面积基准与 `ECSA` 基准的转换一致。
- [ ] 解答使用适用于非零偏置条件的 BV 微分斜率关系，而不是直接套用零偏置交换电流模板。
- [ ] 解答的最终结果能与题设电流或 EIS 截距形成自洽闭合。

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。

### v3 口径改造（2026-08-11）

实测：地板 **50% → 0%**（scramble / integers / flip-sign 三档全 0），第四算子（复述题面 + 拒答）**0.35 → 0.0**。五个 run：0.30 / 1.0 / 1.0 / 1.0 / 1.0（原 0.5 / 1.0 / 1.0 / 1.0 / 1.0）。run1 的 0.5→0.30 是 **归因订正**，见回归集 fixture 里该 run 的 `monotonic_exempt_reason`：那 0.5 **整份都是白拿**（`non_empty_answer` 0.10 + `not_refusal` 0.10 + `has_rate_unit` 0.15 + `has_ecsa_basis` 0.15，`k0_numeric` 读 0.0、相对误差 0.9996），而该 run 的 `k_0≈3.2×10⁻⁸ cm s⁻¹` 比标准值 8.5×10⁻⁵ 低三个数量级、表面浓度算成 0.824/1.132 mM（正确值 0.471/1.397）、且从未把 `R_ct` 换算到 ECSA 基准。新的 0.30 是**真实判据**给的：它确实算对了 `j_geo=-6.12×10⁻⁵`、`ΔE_Ω=-1.47 mV`、`η≈-80.0 mV`（`ir_correction_eint` 0.15）与 `j_ECSA=-2.04×10⁻⁵`（`ecsa_basis_conversion` 0.15）。

改造清单与理由：

- **删掉 `non_empty_answer`（0.10）+ `not_refusal`（0.10）**：存在性判据。
- **`k0_numeric`（0.50）+ `has_rate_unit`（0.15）+ `has_ecsa_basis`（0.15）三项合并为 `k0_ecsa_numeric`（0.40）**，这是 **item B（量纲门）在本题的落地**：旧口径下单位与基准是**两个独立的存在性项**，`cm/s` 与 `ECSA` 在**题面里原样就有**（题面写"求该 Ox/Red 探针在 `ECSA` 基准下的本征标准速率常数 `k0`"、`DOx=0.000006 cm2 s-1`），复述题面即命中 0.30，纯数值扰动 5/5 存活、probe4 实测拿 0.35。现在改成 8.5×10⁻⁵ 落窗、**且** ±70/60 字符内同时出现 `cm s⁻¹` 量纲、`k0` 符号、`ECSA` 基准 —— 三者贴着结论数值才算，单位/基准不再能脱离数值单独得分。
- **删掉 `extract_k0`（35 行）与 `k0_extracted` / `k0_relative_error` 追溯字段**：抽取器的全部职能（结论式定位、`\boxed{}` 优先、上标与 markdown 容错）已由归一化 + 邻接窗承担；而"抽到了一个数"本身正是白拿②。错值的追溯信息改由下面四条陷阱标记承担，它们直接指出踩了哪一个分支。
- **删掉 `has_ecsa_basis` 的整套否定否决机制（`ECSA_KW`/`NEG`/`NORM_KW`/`GEO_KW` 三支）**：那套东西是给"关键词存在性"打的补丁 —— 判据本身既然从"全文有没有 ECSA"改成"ECSA 是否贴着正确的结论数值"，说反话就不可能命中，否决支自然失去存在意义。
- **新增四条派生量判据**，全部逐条对着题面查过、**题面一条都不含**：
  - `surface_conc_shift`（0.20）：`c_Ox,s≈4.71×10⁻⁷` **且** `c_Red,s≈1.397×10⁻⁶`（或 mM 写法）同时给出。这是"直流电流造成界面浓度偏移"的唯一硬证据，也是 run1 唯一算错的中间量族。
  - `ir_correction_eint`（0.15）：`j_geo≈-6.12×10⁻⁵` **且** 界面过电位 `-0.08003 V` / `-80.0 mV` / 欧姆降 `1.47 mV` 之一。
  - `ecsa_basis_conversion`（0.15）：`ECSA/A_geo=3.00` 或 `j_ECSA≈2.04×10⁻⁵` 落窗，且 ±80/60 字符内有 `ECSA`/`活性面积`/`A_geo`/`几何` 语义。
  - `bv_nonzero_bias_exp`（0.10）：两个指数因子 `exp(α_a fξ)=0.270` **与** `exp(-α_c fξ)=6.09` 同时给出 —— 这是"用了非零偏置 BV 微分斜率、而非零偏置 `RT/(nFI0)` 模板"的可核验指纹。
- **EIS 截距（`R_ct,geo=597-24=573`、`R_D=980-597=383`）故意不设判据**：573 与 383 都是**题给常数的线性组合**（化学06 已记录过这条 —— `2n₁+n₂=1.5` 因此被删），且都是整数，`--integers` 档下结构性不可见。这一条判读留给大模型 Criterion 1，代码侧只用 `hit_rd_as_rct` 的反向指纹兜住"把 980/383 当 R_ct"。
- **新增四条分支陷阱扣分（各 0.25）**，独立复算的分支指纹如下，窗口按刚好互斥设计：

  | 分支 | k0 / 特征值 |
  |---|---:|
  | 标准（ECSA 基准 + 表面浓度 + 非零偏置） | **8.5×10⁻⁵** |
  | `hit_geo_basis_k0`：漏做面积换算，用 `R_ct,geo=573` | 2.55×10⁻⁴ |
  | `hit_bulk_conc`：用体相 1.00 mM 代替表面浓度 | 4.25×10⁻⁵ |
  | `hit_zero_bias_template`：套零偏置 `R_ct=RT/(nFI₀)` | 1.55×10⁻⁴ |
  | `hit_rd_as_rct`：把低频平台 980 或 `R_D`=383 当 `R_ct` | 4.97×10⁻⁵ / 1.27×10⁻⁴ |

  四条**全部在剪掉假设/否证从句的 `hyp` 上匹配**。这是必需的：正确答复普遍会把错误分支的数值写出来再排除（本题参考解自己就写了"`RD` 不可当作 `Rct` 反演 `k0`""不能使用零偏置 `RT/(nFI0)` 模板，也不能使用体相浓度"）。已用合成答复验证：正确 + 显式否证四个分支 → 1.0 无扣分；四个错分支各自 → 0.2/0.15/0.0/0.05 且只打对应那一条标记。
- **等权口径**：删项不重新归一化，分母就是剩下 5 项的权重和（1.00），扣分在其上做减法，最后 clamp 到 [0, 1]。

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
        """剥掉推理模型的思维链，只留真正的最终答复正文。

        闭合的 <think>...</think> 直接删除；未闭合（答复在思考中被截断，
        从未产出最终答案）则丢弃 <think> 之后的全部内容，避免把推理里
        试算过的候选 k0 误判成最终答案。
        """
        s = re.sub(r'<(think|thinking|reasoning)>.*?</\1>', ' ', s,
                   flags=re.IGNORECASE | re.DOTALL)
        s = re.split(r'<(?:think|thinking|reasoning)>', s,
                     flags=re.IGNORECASE)[0]
        return s

    def normalize(text):
        """统一上标/乘号并剥掉 markdown、LaTeX 装饰，便于邻接窗匹配。

        写法容错（不做容错会把「表述差异」记成「答错」，5 次答复集体假阴性）：
          - `\\boxed{k_0\\approx 8.5\\times10^{-5}\\ \\text{cm/s}}` 要能命中；
          - `**k0 ≈ 8.5×10⁻⁵ cm/s**` 的 markdown 强调与 Unicode 上标同样要命中；
          - 符号名容 k0 / k^0 / k_0 / k⁰。
        ⚠️ `_{...}` 下标必须展平：五个 run 全写 `k^0_{\\rm ECSA}`、`c_{\\rm Ox,s}`，
        不压的话邻接窗里的 `ecsa` 与数值之间夹着 `_{\\rm ` 这段壳，
        虽然窗够宽仍能覆盖，但 `k\\s*[_^]?\\s*0` 这类符号支会被 `_{` 打断。
        """
        t = text.lower()
        table = str.maketrans({
            "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5",
            "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-",
            "−": "-", "–": "-", "—": "-", "×": "x", "·": " ",
        })
        t = t.translate(table)
        t = t.replace("\\times", "x").replace("\\cdot", " ")
        t = re.sub(r"\\(?:approx|simeq|cong|sim)", "≈", t)
        for _ in range(3):
            t = re.sub(
                r"\\(?:boxed|text|mathrm|mathbf|operatorname|rm|bf|it)"
                r"\s*\{([^{}]*)\}", r"\1", t)
        t = re.sub(r"\\[,;:!> ]", " ", t)
        t = t.replace("$", " ").replace("**", " ")
        t = re.sub(r"_\s*\{\s*([^{}]{0,12})\s*\}", r"_\1", t)
        return re.sub(r"[ \t]+", " ", t)

    text = normalize(strip_reasoning(flatten_text(transcript)))

    # 假设/否证从句剪枝版：四条分支陷阱标记只在这上面匹配。
    # 正确答复普遍把错误分支的数值写出来再排除（本题参考解自己就写了
    # 「RD 不可当作 Rct 反演 k0」「不能使用零偏置 RT/(nFI0) 模板，
    # 也不能使用体相浓度」），不剪的话满分答复会被自己的否证句反扣 1.00。
    _NEG = (r'(?:若|如果|倘若|假如|不(?:能|应|是|可|得|要|作|将|用)|并非|而非'
            r'|不可|排除|否决|误(?:取|用|将|把|设|以|当)|错误(?:地)?|注意)')
    hyp = re.sub(_NEG + r'[^。\n；;]{0,120}', ' ', text)

    def has_any(patterns, s=None):
        s = text if s is None else s
        return any(re.search(p, s, flags=re.IGNORECASE) for p in patterns)

    scores = {}

    # 1. 结论 k0：数值 + 量纲 + ECSA 基准三者**必须贴着结论数值**（item B）。
    #    旧口径把这三件事拆成 k0_numeric(0.50) + has_rate_unit(0.15)
    #    + has_ecsa_basis(0.15) 三个独立项，而 `cm/s` 与 `ECSA` 题面原样就有
    #    （题面写「求该 Ox/Red 探针在 ECSA 基准下的…k0」、`DOx=0.000006 cm2 s-1`），
    #    复述题面即白拿 0.30，纯数值扰动 5/5 存活。现在要求 8.5e-5 落窗且
    #    ±70/60 字符内同时出现量纲、k0 符号、ECSA 基准 —— 单位与基准不再能
    #    脱离数值单独得分，这就是量纲门在本题的落地。
    #    窗口 8.3~8.7e-5：题面 20% 相对容差在这一位有效数字上就是 ±0.2 的量级，
    #    而最近的错误分支 4.25e-5（体相浓度）与 1.55e-4（零偏置）都在一个
    #    数量级之外，不存在与错误分支争窗的问题。
    UNIT = r'cm\s*(?:\\,)?\s*(?:/\s*s|s\s*\^?\{?\s*-\s*1|sec)'
    K0V = (r'(?<![\d.])8\.[3-7]\d*\s*'
           r'(?:x\s*10\s*\^?\{?\s*-\s*5|e\s*-\s*0?5)')
    k0_ok = False
    for m in re.finditer(K0V, text, flags=re.IGNORECASE):
        seg = text[max(0, m.start() - 70):m.end() + 60]
        if (re.search(UNIT, seg, flags=re.IGNORECASE)
                and re.search(r'k\s*[_^]?\s*0|k0', seg, flags=re.IGNORECASE)
                and re.search(r'ecsa|电化学活性面积|活性面积', seg,
                              flags=re.IGNORECASE)):
            k0_ok = True
            break
    scores["k0_ecsa_numeric"] = 1.0 if k0_ok else 0.0

    # 2. 直流电流造成的界面浓度偏移：c_Ox,s≈4.71e-7 与 c_Red,s≈1.397e-6
    #    必须同时给出。缺一个说明没真做浓度修正（体相 1.00 mM 两个值相同，
    #    只报一个无法与「直接用体相」区分）。两个值题面都不含。
    cox = has_any([
        r'(?<![\d.])4\.7[01]\d*\s*(?:x\s*10\s*\^?\{?\s*-\s*7|e\s*-\s*0?7)',
        r'(?<![\d.])0\.47[01]\d*\s*m\s*m'])
    cred = has_any([
        r'(?<![\d.])1\.(?:39[5-9]|40\d*)\s*'
        r'(?:x\s*10\s*\^?\{?\s*-\s*6|e\s*-\s*0?6)',
        r'(?<![\d.])1\.(?:39[5-9]|40)\d*\s*m\s*m'])
    scores["surface_conc_shift"] = 1.0 if (cox and cred) else 0.0

    # 3. 面积归一 Ru 的欧姆降校正：j_geo≈-6.12e-5 **且** 界面过电位
    #    -0.08003 V / -80.0 mV / 欧姆降 1.47 mV 之一。三个都是派生量。
    jg = has_any([r'(?<![\d.])6\.1[12]\d*\s*'
                  r'(?:x\s*10\s*\^?\{?\s*-\s*5|e\s*-\s*0?5)'])
    ei = has_any([r'(?<![\d.])0\.0800\d*', r'(?<![\d.])80\.0\d*\s*m\s*v',
                  r'(?<![\d.])1\.4[67]\d*\s*m\s*v'])
    scores["ir_correction_eint"] = 1.0 if (jg and ei) else 0.0

    # 4. 几何 → ECSA 面积基准换算：ECSA/A_geo=3.00 或 j_ECSA≈2.04e-5 落窗，
    #    且邻接窗内有面积基准语义（裸 3.00 会误命中别处的比值）。
    conv = False
    for m in re.finditer(r'(?<![\d.])(?:3\.00\d*|2\.0[345]\d*\s*'
                         r'(?:x\s*10\s*\^?\{?\s*-\s*5|e\s*-\s*0?5))(?![\d])',
                         text, flags=re.IGNORECASE):
        seg = text[max(0, m.start() - 80):m.end() + 60]
        if re.search(r'ecsa|活性面积|a_?geo|几何', seg, flags=re.IGNORECASE):
            conv = True
            break
    scores["ecsa_basis_conversion"] = 1.0 if conv else 0.0

    # 5. 非零偏置 BV 微分斜率的两个指数因子必须同时给出：
    #    exp(α_a fξ)=0.270 与 exp(-α_c fξ)=6.09。这是「用了非零偏置斜率
    #    而非零偏置 RT/(nFI0) 模板」的可核验指纹 —— 零偏置模板下两个指数
    #    都等于 1，写不出这两个数。
    scores["bv_nonzero_bias_exp"] = 1.0 if (
        has_any([r'(?<![\d.])0\.27[01]\d*(?![\d])'])
        and has_any([r'(?<![\d.])6\.0[89]\d*(?![\d])',
                     r'(?<![\d.])6\.1[01]\d*(?![\d])'])) else 0.0

    _WEIGHTS = {
        "k0_ecsa_numeric": 0.40,
        "surface_conc_shift": 0.20,
        "ir_correction_eint": 0.15,
        "ecsa_basis_conversion": 0.15,
        "bv_nonzero_bias_exp": 0.10,
    }
    earned = sum(w for k, w in _WEIGHTS.items() if scores[k] == 1.0)

    # ---- 分支陷阱：命中即扣分（各 0.25），一律在剪掉否证从句的 hyp 上匹配 ----
    #    独立复算的分支指纹（窗口按刚好互斥设计）：
    #      标准 8.5e-5 / 几何基准 2.55e-4 / 体相浓度 4.25e-5
    #      / 零偏置模板 1.55e-4 / RD 当 Rct 4.97e-5(980) 或 1.27e-4(383×3)
    scores["hit_rd_as_rct"] = 1.0 if has_any([
        r'r\s*_?\{?\s*ct\s*(?:,?\s*geo)?\s*[=≈约]\s*(?:980|956|383)(?![\d])',
        r'(?:980|383)[^\n]{0,20}(?:当作|作为|即|视为)[^\n]{0,10}'
        r'r\s*_?\{?\s*ct',
        r'(?<![\d.])4\.9[5-9]\d*\s*(?:x\s*10\s*\^?\{?\s*-\s*5|e\s*-\s*0?5)',
        r'(?<![\d.])1\.2[6-8]\d*\s*(?:x\s*10\s*\^?\{?\s*-\s*4|e\s*-\s*0?4)',
    ], hyp) else 0.0

    #    漏做面积基准换算，直接用 R_ct,geo=573 反演 → k0≈2.55e-4。
    scores["hit_geo_basis_k0"] = 1.0 if has_any([
        r'(?<![\d.])2\.5[3-7]\d*\s*(?:x\s*10\s*\^?\{?\s*-\s*4|e\s*-\s*0?4)',
    ], hyp) else 0.0

    #    用体相 1.00 mM 代替表面浓度 → k0≈4.25e-5。
    scores["hit_bulk_conc"] = 1.0 if has_any([
        r'(?<![\d.])4\.2[3-7]\d*\s*(?:x\s*10\s*\^?\{?\s*-\s*5|e\s*-\s*0?5)',
    ], hyp) else 0.0

    #    套零偏置交换电流模板 R_ct=RT/(nFI0) → k0≈1.55e-4。
    scores["hit_zero_bias_template"] = 1.0 if has_any([
        r'(?<![\d.])1\.5[3-6]\d*\s*(?:x\s*10\s*\^?\{?\s*-\s*4|e\s*-\s*0?4)',
        r'rt\s*/\s*\(?\s*n?\s*f\s*[ij]\s*_?\{?\s*0',
    ], hyp) else 0.0

    penalty = 0.25 * (
        scores["hit_rd_as_rct"] + scores["hit_geo_basis_k0"]
        + scores["hit_bulk_conc"] + scores["hit_zero_bias_template"])

    # 代码侧最终答复证据分：只反映最终答案是否可自动确认。
    scores["auto_final_answer_score"] = round(
        max(0.0, min(1.0, earned - penalty)), 3)

    return scores
```

## LLM Judge Rubric

大模型评分负责**过程、概念和逻辑**，不重复评价代码已经检查过的最终 `k0` 数值命中。若代码侧显示最终数值错误，大模型仍应按过程质量独立评分，但不能替代最终答案硬检查。

### Criterion 1: EIS 截距判读与 Rct/RD 区分（Weight: 25%）

**Score 1.0**: 明确指出 `597-24=573 Ω cmgeo2` 是 `Rct,geo`，`980-597=383 Ω cmgeo2` 是扩散平台/扩散电阻贡献，并说明低频平台或 `RD` 不能用于反演 `k0`。  
**Score 0.75**: 正确得到 `Rct,geo=573`，并提到低频平台不是主反演对象，但没有完整给出 `RD=383` 或解释略弱。  
**Score 0.5**: 得到 `Rct,geo=573`，但没有讨论 `RD` 或低频平台的物理含义。  
**Score 0.25**: 有 EIS 截距处理意识，但截距来源或面积归一含义表达混乱。  
**Score 0.0**: 把 `980`、低频平台或 `RD=383` 当作 `Rct`，或完全没有 EIS 截距判读。

### Criterion 2: 表面浓度与符号约定（Weight: 25%）

**Score 1.0**: 正确使用 `I<0` 为还原、`x` 由电极指向溶液和 Fick 通量约定，说明 `Ox` 被消耗、`Red` 被生成，并得到 `cOx,s≈0.471 mM`、`cRed,s≈1.397 mM`。  
**Score 0.75**: 表面浓度数值和方向正确，但对符号约定或通量方向解释不完整。  
**Score 0.5**: 使用了表面浓度，方向大体正确，但缺少一个关键数值或解释。  
**Score 0.25**: 意识到需要浓度修正，但公式、符号或单位处理存在明显问题。  
**Score 0.0**: 直接使用体相浓度反演，或把 `Ox/Red` 表面浓度变化方向写反。

### Criterion 3: 欧姆降、面积基准与 BV 斜率选择（Weight: 30%）

**Score 1.0**: 正确使用面积归一 `Ru` 做 `jgeo Ru` 校正，得到 `Eint-E0′≈-0.08003 V`；正确将几何面积 `Rct` 转为 `Rct,ECSA=1719 Ω cmECSA2`；并使用非零偏置、固定表面浓度的 BV 微分斜率反演。  
**Score 0.75**: 三个核心环节基本正确，但其中一个解释不完整，例如没有说明为什么不能用零偏置模板。  
**Score 0.5**: 完成面积转换和 BV 反演主路径，但欧姆降、非零偏置或表面浓度固定条件有一处明显缺口。  
**Score 0.25**: 有 BV 或面积转换意识，但公式选择或基准处理存在较大混乱。  
**Score 0.0**: 混淆几何面积和 `ECSA` 基准，或错误套用零偏置 `RT/(nFI0)` 模板，或用错误电势反演。

### Criterion 4: 闭合检查与自洽性（Weight: 20%）

**Score 1.0**: 能回代 BV 电流或微分斜率，说明结果可回到 `I≈-12.0 μA` 或 `Rct,geo≈573 Ω cmgeo2`，与题设 EIS 截距一致。  
**Score 0.75**: 有闭合检查，但只验证了电流或截距中的一项，或表达略简略。  
**Score 0.5**: 主推导前后基本自洽，但没有明确闭合检查。  
**Score 0.25**: 有尝试自洽说明，但不能真正回到题设数据。  
**Score 0.0**: 推导前后矛盾，或最终结果无法与题设电流/EIS 数据对应。
