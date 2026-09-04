# 构造高质量-query	
一条封闭的环形微流控电泳通道被用于研究带正电胶体在强场下的拥挤输运。通道截面积恒定,可把胶体的轴向线浓度 C(s,t) 看成一维连续介质变量。沿环形通道取顺时针弧长坐标 s,并在某一标记处把环“剪开”读数,读数范围为 0≤s<300 cm。通道中不存在粒子产生、吸附或泄漏。

在忽略扩散的短时间内,C 满足守恒律
C_t+[J(C)]_s=0,
J(C)=U C_max f(a),
a=\frac{C}{C_max},
其中
f(a)=a(1-a)(1+4a)。
这里 a 是无量纲占据率,U 是由电泳迁移率给出的速度尺度,不代表单个胶体能达到的最大速度。胶体为一价正电,迁移率按 Einstein 关系估计:
U=\mu E,\qquad \mu=\frac{D F}{R T}。
已知 D=9.00×10^{-6} cm^2/s,电场强度 E=450 V/cm,温度 T=300 K。取 Faraday 常数 F=96485.33212 C/mol,气体常数 R=8.314462618 J/(mol·K)。

初始占据率 a(s,0) 的读数如下:
0≤s<40 cm:a=0.10；
40 cm≤s<85 cm:a=0.20；
85 cm≤s≤115 cm:a 从 0.20 线性增至 0.55；
115 cm<s<160 cm:a=0.55；
160 cm≤s≤210 cm:a 从 0.55 线性降至 0.06；
210 cm<s<300 cm:a=0.06。

要求:判断所有可能早期几何候选是否满足物理熵条件,求首个物理可接受激波的生成时刻和生成位置,并说明哪些候选必须淘汰。注意题中长度和场强单位混用,计算前需统一单位。

请完整写出判据、推理与计算过程。最后单独用一行给出结论,格式为:
【结果】U=…；s=40 跳跃: …；s=0/300 跳跃: …；首个物理激波 t=…、s=…；下降段激波 t=…（与首个激波的先后关系…）
# SFT标准-response	
设 a=C/C_max,则方程化为
 a_t + [U f(a)]_s = 0,
其中 f(a)=a(1-a)(1+4a)=a+3a^2-4a^3,
所以 f'(a)=1+6a-12a^2,f''(a)=6-24a。

1) 先算速度尺度 U
Einstein 关系给出
U=DFE/(RT)。
取统一单位后,D=9.00×10^-6 cm^2/s,E=450 V/cm,T=300 K,
U=9.00×10^-6×96485.33212×450 /(8.314462618×300)
≈0.15666 cm/s
（等价于 1.5666×10^-3 m/s）。

2) 检查初始跳跃候选
初始分布在 s=40 cm 处有跳跃:a_L=0.10,a_R=0.20。
计算
f(0.10)=0.126,f(0.20)=0.288,
Rankine-Hugoniot 速度为
s_RH = U [f(a_R)-f(a_L)]/(a_R-a_L)=1.62U。
两侧特征速度
c_L=U f'(0.10)=1.48U,
c_R=U f'(0.20)=1.72U。
因 c_L < s_RH < c_R,特征线发散,这是稀疏波而不是物理激波,因此淘汰。

环形通道剪开处 s=0/300 cm 也要检查:左侧 a_L=0.06,右侧 a_R=0.10。
计算
f(0.06)=0.069936,f(0.10)=0.126,
s_RH=U[0.126-0.069936]/0.04=1.4016U,
而
c_L=U f'(0.06)=1.3168U,
c_R=U f'(0.10)=1.48U。
同样有 c_L < s_RH < c_R,故也是稀疏波候选,必须淘汰。

3) 计算连续斜坡段的首次破裂时间
对光滑初值,特征满足
s = s0 + U f'(a0(s0)) t,
首次破裂条件是
1 + U f''(a0) a0'(s0) t = 0。

(1) 85≤s≤115 cm 上升段:a 从 0.20 线性增至 0.55。
其斜率为
a0' = (0.55-0.20)/(115-85)=0.35/30=0.0116667 cm^-1。
该段中 a>0.25 时 f''(a)=6-24a<0,出现压缩；最强压缩在右端 a=0.55 处。
此处
f''(0.55)=6-24×0.55=-7.2,
于是
U f'' a0' = -U×7.2×0.0116667 = -0.084U。
首个破裂时刻
t1 = 1/(0.084U) ≈ 1/[0.084×0.15666] ≈ 76.0 s。
生成位置由该特征出发点 s0=115 cm 给出:
 f'(0.55)=1+6×0.55-12×0.55^2=0.67,
 s1 = 115 + U f'(0.55) t1
    = 115 + 0.67/0.084
    ≈ 122.98 cm。
所以该段产生的首个物理激波为 t≈76.0 s,s≈123 cm。

(2) 160≤s≤210 cm 下降段:a 从 0.55 线性降至 0.06。
斜率
 a0'=(0.06-0.55)/(210-160)=-0.49/50=-0.0098 cm^-1。
该段中 a<0.25 时 f''(a)>0 才压缩,最强压缩在右端 a=0.06。
此处
f''(0.06)=6-24×0.06=4.56,
所以
U f'' a0' = -U×4.56×0.0098 = -0.044688U。
首个破裂时刻
t2 = 1/(0.044688U) ≈ 142.8 s,
明显晚于 t1。
对应位置
f'(0.06)=1+6×0.06-12×0.06^2=1.3168,
 s2 = 210 + U f'(0.06)t2
    = 210 + 1.3168/0.044688
    ≈ 239.5 cm。

4) 结论
所有早期几何候选中:
- s=40 cm 的跳跃:稀疏波,淘汰；
- s=0/300 cm 的周期性跳跃:稀疏波,淘汰；
- 85–115 cm 上升斜坡:形成首个物理可接受激波,t≈76.0 s,s≈123 cm；
- 160–210 cm 下降斜坡:也会形成激波,但更晚,t≈142.8 s。

因此首个物理可接受激波生成于 t≈76.0 s,生成位置 s≈123 cm（约 1.23 m）。

【结果】U≈0.157 cm/s；s=40 跳跃: 稀疏波(淘汰)；s=0/300 跳跃: 稀疏波(淘汰)；首个物理激波 t≈76.0 s、s≈123 cm；下降段激波 t≈142.8 s(更晚)
# 步骤列表-reference
1.  **问题转化与控制方程**：将线浓度 \(C\) 转化为无量纲占据率 \(a=C/C_{\max}\)，守恒方程化为 \(a_t + [U f(a)]_s = 0\)，其中通量函数 \(f(a)=a(1-a)(1+4a)=a+3a^2-4a^3\)，特征速度为 \(c(a)=U f'(a)=U(1+6a-12a^2)\)。
2.  **参数计算**：速度尺度由 Einstein 关系得 \(U = \frac{D F E}{R T} \approx 0.15666\ \text{cm/s}\)。
3.  **初始间断检验**：
    *   \(s=40\ \text{cm}\) 间断 (\(a_L=0.10,\ a_R=0.20\)) 的 Rankine-Hugoniot 速度为 \(s_{RH}=1.62U\)，因特征速度满足 \(c_L=1.48U < s_{RH} < 1.72U=c_R\)，为稀疏波，淘汰。
    *   \(s=0/300\ \text{cm}\) 间断 (\(a_L=0.06,\ a_R=0.10\)) 的 \(s_{RH}=1.4016U\)，满足 \(c_L=1.3168U < s_{RH} < 1.48U=c_R\)，同为稀疏波，淘汰。
4.  **连续区激波形成**：激波形成条件为特征线汇聚，即 \(t = -\frac{1}{U f''(a_0) a'_0(s_0)}\)。
    *   \(85 \le s \le 115\ \text{cm}\) 上升段 (\(a'_0=0.01167\ \text{cm}^{-1}\)) 在右端点 \(a=0.55\) 处首先破裂，\(f''(0.55)=-7.2\)，生成时刻 \(t_1 = \frac{1}{U \cdot 7.2 \cdot 0.01167} \approx 76.0\ \text{s}\)，生成位置 \(s_1 = 115 + U f'(0.55) t_1 \approx 123.0\ \text{cm}\)。
    *   \(160 \le s \le 210\ \text{cm}\) 下降段 (\(a'_0=-0.0098\ \text{cm}^{-1}\)) 在右端点 \(a=0.06\) 处破裂更晚，\(f''(0.06)=4.56\)，生成时刻 \(t_2 \approx 142.8\ \text{s}\)。
5.  **结论**：首个物理可接受激波由上升斜坡段形成，生成于 \(t \approx 76.0\ \text{s}\)，位置 \(s \approx 123.0\ \text{cm}\)；两个初始跳跃和下降斜坡形成的激波均被排除或晚于该激波。

## Grading Criteria

- [ ] 单位统一后速度尺度 U=DFE/(RT)≈0.157 cm/s（识别 D、E 已同为 cm 制，无需再换算长度单位）。
- [ ] 通量导数正确：f'(a)=1+6a-12a²、f''(a)=6-24a，特征速度 c(a)=U f'(a)。
- [ ] s=40 cm 跳跃(a_L=0.10→a_R=0.20)判为**稀疏波淘汰**：c_L<s_RH<c_R（1.48U<1.62U<1.72U），特征发散不满足熵条件。
- [ ] 环形剪开处 s=0/300 cm 周期性跳跃(a_L=0.06,a_R=0.10)同样判为**稀疏波淘汰**（1.317U<1.402U<1.48U）——不能漏掉这个环形边界候选。
- [ ] 连续段破裂时刻 t=-1/[U f''(a₀) a₀'(s₀)]，上升段在 a=0.55 端 f''<0 处最先破裂：t₁≈76.0 s、s₁≈123 cm。
- [ ] 下降段在 a=0.06 端 f''>0 处破裂，t₂≈142.8 s，晚于 t₁，故被淘汰为"非首个"。
- [ ] 最终结论：首个物理可接受激波 t≈76.0 s、s≈123 cm；两个跳跃为稀疏波、下降段更晚，均排除。

## Automated Checks

代码评分只检查最终答复的硬证据，不评价推导过程。本 grade() 已内联全部锚点与阈值，不依赖外部 meta。

```python
def grade(transcript: list, workspace_path: str, meta: dict) -> dict:
    import re

    ANSWER_TAG = "【结果】"

    def _content(m):
        c = m.get("content", "")
        if isinstance(c, list):
            return " ".join(seg.get("text", "") for seg in c if isinstance(seg, dict))
        return c if isinstance(c, str) else ""

    assistant_msgs = [_content(m) for m in transcript if m.get("role") == "assistant"]
    full = "\n".join(assistant_msgs)
    full_l = full.lower()
    final_msg = assistant_msgs[-1] if assistant_msgs else ""

    anchor_region = final_msg
    if ANSWER_TAG in final_msg:
        anchor_region = final_msg.split(ANSWER_TAG, 1)[1][:400]

    def _nums(pattern, text):
        vals = []
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            seg = text[m.end():m.end() + 48]
            sm = re.search(
                r'([-+]?)\s*([0-9]*\.?[0-9]+)\s*'
                r'(?:[×x*]\s*10\s*\^?\{?\s*([-+]?\d+)\s*\}?|e\s*([-+]?\d+))?',
                seg, flags=re.IGNORECASE)
            if sm and sm.group(2):
                v = float(sm.group(2))
                exp = sm.group(3) or sm.group(4)
                if exp:
                    v *= 10 ** int(exp)
                if sm.group(1) == '-':
                    v = -v
                vals.append(v)
        return vals

    def _mag_ok(v, target, tol=0.05):
        return v is not None and target != 0 and abs(v - target) / abs(target) <= tol

    out = {}

    # 速度尺度 U≈0.157 cm/s
    u_vals = _nums(r'(?:U|速度尺度|速度)\s*[:=≈约]?', full)
    u_hit = any(_mag_ok(v, 0.15666, 0.05) for v in u_vals)

    # 首个激波时刻 t≈76.0 s
    t1_vals = _nums(r'(?:t\s*_?\s*1|首个|首次|生成时刻|破裂时刻|t\s*≈)\s*[:=≈约]?', full_l)
    t1_hit = any(_mag_ok(v, 76.0, 0.05) for v in t1_vals)

    # 首个激波位置 s≈123 cm
    s1_vals = _nums(r'(?:s\s*_?\s*1|生成位置|位置\s*s|s\s*≈|s\s*=)\s*[:=≈约]?', full_l)
    s1_hit = any(_mag_ok(v, 123.0, 0.05) for v in s1_vals)

    # 下降段激波时刻 t≈142.8 s
    t2_vals = _nums(r'(?:t\s*_?\s*2|下降段|下降斜坡)\s*[:=≈约]?', full_l)
    t2_hit = any(_mag_ok(v, 142.8, 0.06) for v in t2_vals)

    # ---- 两个跳跃识别为稀疏波（0.20 核心防御位）----
    # 旧写法是**纯关键词**判据，数值全错后 5/5 原样留存（白拿）。病因在题面第 25 行：
    # 结论格式行原样写着「s=40 跳跃: 稀疏波/激波(淘汰/保留)；s=0/300 跳跃: 稀疏波/激波(淘汰/保留)」
    # —— `稀疏波`、`淘汰`、`40`、`0/300` 四个词全在同一行，复述题面即同时喂饱
    # rarefaction_kw、jump40、jump0 三个条件，这 0.20 与答案对错完全无关。
    # 按白拿口径加**派生数值锚同现闸门**：结论词的 ±120 字邻接窗内必须出现该跳跃
    # 自己的派生量（题面一个都没给，只有真做了熵条件检验才写得出）：
    #   s=40   跳跃：c_L=1.48U、s_RH=1.62U、c_R=1.72U，或通量 f(0.10)=0.126、f(0.20)=0.288
    #   s=0/300 跳跃：s_RH=1.4016U、c_L=1.3168U，或 f(0.06)=0.069936
    # 窗口取 ±120 字（±80 会漏掉 run3 的 s=0/300 段，那份把数值算在结论前两句）。
    _CONCL = r'稀疏|淘汰|排除|不是激波|发散|不满足'
    _N40 = r'1\.48\d*|1\.62\d*|1\.7[12]\d*|0\.126\d*|0\.288\d*'
    _N0 = r'1\.31[67]\d*|1\.40[012]\d*|0\.0699\d*'

    def _concl_with_num(nums, span=120):
        """结论词邻接窗内是否同现该跳跃的派生数值锚。"""
        for m in re.finditer(_CONCL, full_l):
            seg = full_l[max(0, m.start() - span):m.end() + span]
            if re.search(nums, seg):
                return True
        return False

    rarefaction_kw = bool(re.search(r'稀疏波|rarefaction|膨胀波|特征.{0,6}(发散|张开)', full_l))
    jump40 = bool(re.search(r'(40)[^\n。；;]{0,40}(稀疏|淘汰|排除|不是激波|发散)', full_l)) \
        and _concl_with_num(_N40)
    jump0 = bool(re.search(r'(0\s*/\s*300|300|剪开|周期|环形边界|环形.{0,4}间断)[^\n。；;]{0,40}(稀疏|淘汰|排除|发散)', full_l)) \
        and _concl_with_num(_N0)
    both_rarefaction = rarefaction_kw and jump40 and jump0

    # ---- 上升段为首个激波、下降段更晚 ----
    # 旧写法 `(上升|85).{0,60}(首个|最先|先破裂|最早)` + `(下降|160|t_2)…(更晚|晚于)`
    # 同样是纯关键词 + 字符距离，两头都出问题：
    #   ① 后半句被题面第 25 行的「下降段激波 t=…(更早/更晚)」直接喂饱（复述即命中）；
    #   ② 前半句靠 60 字窗口，run0/run1 结论写对了却没套住（真实分被压低 0.10），
    #      而扰动后数字长度一变、窗口反而套住了 —— run0 real=0 → 扰动档=1，
    #      属于**凭空造分**（比单纯白拿更坏）。
    # 收紧为：破裂序的文字结论必须与两段各自的时刻锚在 ±60 字邻接窗内同现 ——
    # 上升段侧 t1≈76.0 s、下降段侧 t2≈142.8 s，两个时刻题面都没给。
    def _order_side(kw, nums, span=60):
        for m in re.finditer(kw, full_l):
            seg = full_l[max(0, m.start() - span):m.end() + span]
            if re.search(nums, seg):
                return True
        return False

    order_ok = _order_side(r'上升|升段|首个|最先|最早|先破裂', r'7[56]\.\d') \
        and _order_side(r'更晚|晚于|较晚|滞后', r'14[23]\.\d')

    # 以下三项按化学03 第 237-238 行口径**权重归零**、只留作诊断输出（键不删，
    # 供审计脚本与回归 fixture 的逐项对照）：空答与拒答由 runner 层记 0，
    # 在 grade() 里再给一遍就是与题目无关的白拿（白拿①）；has_unit 判的是
    # 「全文任何位置出现某单位」，而 `cm/s`、`cm`、`s` 题面原样全有（题面写
    # 「D=9.00×10^{-6} cm^2/s」「E=450 V/cm」），复述题面即命中（白拿②③）。
    # 注：has_unit 在旧版就已不进总分，这里只补上归零口径的说明。
    non_empty = 1.0 if len(full.strip()) >= 30 else 0.0
    refusal = bool(re.search(r"(无法回答|不能回答|不会做|拒绝作答|i cannot|i can't|cannot solve)", full_l))
    not_refusal = 0.0 if refusal else 1.0

    has_unit = 1.0 if re.search(r'cm\s*/\s*s|cm/s|\bs\b|秒|\bcm\b', full_l) else 0.0

    # ---- 折算：归零 non_empty(0.10)+not_refusal(0.10)=0.20 后，剩下的实质项
    #      按 1/(1-0.20)=1.25 等比放大，完全正确的答复仍是 1.0。----
    _RESCALE = 1.25
    core = (0.20 * (1.0 if t1_hit else 0.0)
            + 0.15 * (1.0 if s1_hit else 0.0)
            + 0.10 * (1.0 if u_hit else 0.0)) * _RESCALE
    defense = (0.20 * (1.0 if both_rarefaction else 0.0)
               + 0.10 * (1.0 if order_ok else 0.0)
               + 0.05 * (1.0 if t2_hit else 0.0)) * _RESCALE

    final_answer = max(0.0, min(1.0, core + defense))
    out["non_empty_answer"] = non_empty
    out["not_refusal"] = not_refusal
    out["u_hit"] = 1.0 if u_hit else 0.0
    out["t1_hit"] = 1.0 if t1_hit else 0.0
    out["s1_hit"] = 1.0 if s1_hit else 0.0
    out["t2_hit"] = 1.0 if t2_hit else 0.0
    out["both_jumps_rarefaction"] = 1.0 if both_rarefaction else 0.0
    out["shock_order_ok"] = 1.0 if order_ok else 0.0
    out["has_unit"] = has_unit

    anchors = [u_hit, t1_hit, s1_hit, t2_hit, both_rarefaction]
    out["numeric_anchor_hit_rate"] = round(sum(1 for h in anchors if h) / 5.0, 4)

    out["auto_final_answer_score"] = round(final_answer, 4)
    return out
```

## LLM Judge Rubric

大模型评分负责**过程、概念与逻辑**，不重复判定代码已覆盖的最终数值命中。

### Criterion 1: 单位统一 + 通量结构 + 特征速度（Weight: 25%）

**Score 1.0**: 识别 D(cm²/s)、E(V/cm) 已同属 cm 制、长度按 cm 统一（不误做多余的 m↔cm 换算），U=DFE/(RT)≈0.157 cm/s；正确给出 f'(a)=1+6a-12a²、f''(a)=6-24a 与 c(a)=U f'(a)。
**Score 0.5**: U 数量级对但单位处理含糊，或 f'/f'' 有一处系数错致特征速度偏差。
**Score 0.0**: 未统一单位（U 差数量级），或通量导数结构性错误。

### Criterion 2: 两个初始跳跃的熵条件判定（Weight: 35%，核心防御位）

**Score 1.0**: 对 s=40 与 s=0/300 两处跳跃都用 c_L<s_RH<c_R（特征发散）判为**稀疏波、淘汰**；**尤其识别出环形剪开处 s=0/300 也是一个必须检验的周期性间断候选**，未遗漏。
**Score 0.5**: 正确判 s=40 为稀疏波，但漏掉/误判环形边界 s=0/300 这个候选，或熵判据表述含糊。
**Score 0.0**: 把发散特征的跳跃当成物理激波（踩熵条件陷阱），或完全不做 R-H 与特征速度比较。

### Criterion 3: 连续段破裂机制 + 首个激波选取（Weight: 40%）

**Score 1.0**: 用 t=-1/[U f''(a₀)a₀'(s₀)] 定破裂时刻，正确判断上升段在 a=0.55(f''<0)端、下降段在 a=0.06(f''>0)端最先压缩；比较 t₁≈76 s < t₂≈143 s，选上升段为**首个**物理激波、位置 s₁≈123 cm；下降段更晚被淘汰为非首个。
**Score 0.5**: 破裂公式与首个时刻 t₁ 对，但压缩端点判断或 t₁/t₂ 先后比较有一处含糊、位置 s₁ 未算或算错。
**Score 0.0**: 破裂机制用错（如按端点 a 值最大处而非 f''·a₀' 最大处），或把下降段/更晚的激波当成首个。
