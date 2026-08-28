"""
ScoreFloor-Sci-Bench — 单题评分工具 (Grading Utilities)

供各题 `Automated Checks` 里的 grade() 复用：文本抽取、归一化、数值/单位匹配。
只做代码侧硬证据抽取，不评价推导过程（过程/逻辑由 LLM Judge Rubric 负责）。
"""

from __future__ import annotations

import re
from typing import List, Optional


# --------------------------------------------------------------------------
# transcript / 文本抽取
# --------------------------------------------------------------------------
def flatten_text(items: list) -> str:
    """把 transcript（list[dict|str]）拍平成纯文本，兼容多种字段名。"""
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


def has_any(text: str, patterns: List[str]) -> bool:
    """text 是否命中任一正则（忽略大小写）。"""
    return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)


# --------------------------------------------------------------------------
# 归一化：统一乘号/负号/上标/空白 + LaTeX 写法容错，便于数值与构型抽取
# --------------------------------------------------------------------------
_SUP = {
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-",
}
# U+212B ANGSTROM SIGN → U+00C5，两种埃字符码位统一。
# `·` 一律去掉而不是换成 `x`：它绝大多数出现在单位乘积里（`mg·L⁻¹`），而题库
# 单位正则普遍按 `mg\s*/?\s*L` 这类紧邻写法写，去掉才匹配得上；换成 `x` 反而失配。
_REPL = {"×": "x", "·": "", "−": "-", "–": "-", "—": "-", "﹣": "-",
         "\u212b": "\u00c5", **_SUP}

# LaTeX 希腊字母命令 → unicode。题库 check 写的是 σ/δ/β 等 unicode 字符，
# 模型输出的是 \sigma/\delta/\beta，纯表现形式差异。
_GREEK = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε",
    "varepsilon": "ε", "zeta": "ζ", "eta": "η", "theta": "θ", "vartheta": "θ",
    "iota": "ι", "kappa": "κ", "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ",
    "omicron": "ο", "pi": "π", "varpi": "π", "rho": "ρ", "varrho": "ρ",
    "sigma": "σ", "varsigma": "σ", "tau": "τ", "upsilon": "υ", "phi": "φ",
    "varphi": "φ", "chi": "χ", "psi": "ψ", "omega": "ω",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ",
    "Pi": "Π", "Sigma": "Σ", "Upsilon": "Υ", "Phi": "Φ", "Psi": "Ψ",
    "Omega": "Ω",
}

# 保留语义的 LaTeX 命令 → 符号（在剥离其余命令前先替换）。
# 收尾一律用 (?![A-Za-z]) 而不是 \b：`_` 在正则里算单词字符，`\sigma_tot` 的
# "sigma" 后面没有 \b；`\times10^7` 的 "times" 后面紧跟数字也没有 \b——
# 用 \b 会让这两种最常见的写法整片漏掉。
_LATEX_SEMANTIC = [
    (r"\\(?:mathring\s*\{\s*A\s*\}|text\s*\{\s*Å\s*\}|AA|angstrom)(?![A-Za-z])", "Å"),
    (r"\\times(?![A-Za-z])", "x"),
    (r"\\cdot(?![A-Za-z])", ""),
    (r"\\(?:simeq|approx|sim|cong|doteq)(?![A-Za-z])", "≈"),
    (r"\\(?:leq|le)(?![A-Za-z])", "<="),
    (r"\\(?:geq|ge)(?![A-Za-z])", ">="),
    (r"\\(?:to|rightarrow|Rightarrow|implies|longrightarrow)(?![A-Za-z])", "->"),
    (r"\\pm(?![A-Za-z])", "+-"),
    # 单位/计量类命令。必须显式列出：normalize 收尾会把未列出的 \command 一律
    # 删成空格，`\permil` 那样的单位命令会连带把 ‰ 抹掉，而题库单位项正是按
    # `‰|permil` 匹配的（化学08 run1 的 has_unit 假阴性就是这么来的）。
    (r"\\(?:permil|perthousand|promille)(?![A-Za-z])", "‰"),
    (r"\\(?:celsius|degreeCelsius)(?![A-Za-z])", "°C"),
    (r"\\(?:degree|deg)(?![A-Za-z])", "°"),
    (r"\\(?:micro|mu m)(?![A-Za-z])", "μ"),
    (r"\\ohm(?![A-Za-z])", "Ω"),
    (r"\\percent(?![A-Za-z])", "%"),
]
# 字体/装饰包裹命令：\boxed{..} \mathrm{..} \text{..} 等，保留花括号内内容
_LATEX_WRAPPER = (
    r"\\(?:boxed|mathrm|mathbf|mathit|mathsf|operatorname|text|textrm|textbf"
    r"|rm|bm|bf|it|sf|displaystyle)\s*\{([^{}]*)\}"
)
_LATEX_BRACE_RM = r"\{\s*\\(?:rm|it|bf|sf|mathrm|mathbf)\s+([^{}]*)\}"
# 间距/尺寸命令：不先清掉，它们会卡在花括号里妨碍拆壳
_LATEX_SPACING = (
    r"\\(?:left|right|bigl?|bigr?|Bigl?|Bigr?|biggl?|biggr?|Biggl?|Biggr?"
    r"|quad|qquad|hspace|thinspace|negthinspace)(?![A-Za-z])"
)
# 无花括号的字体切换命令（`\sigma_\rm el`、`j_\rm geo`）
_LATEX_FONT_BARE = (
    r"\\(?:mathrm|mathbf|mathit|mathsf|textrm|textbf|rm|bf|it|sf)(?![A-Za-z])"
)


def normalize(text: str) -> str:
    """统一符号并压缩空白，并对常见 LaTeX 写法做容错归一。

    处理：上标/乘号/负号/埃字符统一；希腊字母命令 → unicode；剥离
    \\boxed{}/\\mathrm{}/{\\rm ..} 等装饰包裹、`^{..}`/`_{..}` 上下标花括号、
    \\frac、\\(...\\)/\\[...\\] 数学定界符、\\, 细空格与 LaTeX 硬空格 `\\ `、
    其余 \\command；`a x 10^b` → `ae b`。
    目的：让「同一物理答案的不同 LaTeX 写法」在数值/关键词匹配前落到同一文本上，
    降低 grade() 假阴性（如 `V=182.5\\ {\\rm \\AA^3}` 与 `V=182.5 Å³`、
    `\\boxed{\\sigma\\approx 2.6\\times10^{-13}\\ \\mathrm{m^{2}}}` 与 `σ≈2.6e-13 m^2`）。

    只动表现形式，不动任何数值、符号与量纲——见 tests/test_grading_utils.py
    的不变量用例（数字序列、希腊字母集合在归一前后必须一致）。
    """
    for k, v in _REPL.items():
        text = text.replace(k, v)
    # 希腊字母先落地，否则会被后面「剥离其余 \command」一步吞成空格
    text = re.sub(r"\\([A-Za-z]+)(?![A-Za-z])",
                  lambda m: _GREEK.get(m.group(1), m.group(0)), text)
    for pat, sub in _LATEX_SEMANTIC:
        text = re.sub(pat, sub, text, flags=re.IGNORECASE)
    # 间距/尺寸命令与无花括号字体命令先清，避免卡在花括号里妨碍拆壳
    text = re.sub(_LATEX_SPACING, " ", text)
    text = re.sub(_LATEX_FONT_BARE, "", text)
    text = re.sub(r"\\[,;:!>]", " ", text)
    # 「\ 」（反斜杠+空白）是 LaTeX 硬空格，数值与单位之间最常见的一种；
    # 不清掉它，`-1.25\ A m^-2` 里的 \s* 匹配不过去，单位永远取不到。
    text = re.sub(r"\\(?=\s)", " ", text)
    text = text.replace("\\%", "%").replace("\\_", "_")
    # 拆壳跑到不动点：壳是嵌套的（`\boxed{...\mathrm{m^{2}}}`），单遍替换会因为
    # `[^{}]*` 撞上内层花括号而失配。上下标花括号一并拆掉：题库单位正则按
    # `m\s*\^?\{?\s*-?2` 这类写法写，`^{2}` 不拆则 `\s*` 匹配不过花括号。
    # 上下标内容 strip 掉两侧空白，否则 `\sigma_{\rm el}` 会落成 `σ_ el`
    # （`\rm` 先被清成空格），与题库写的 `σ_el` 差一个空格而失配。
    _tight = lambda m: m.group(0)[0] + m.group(1).strip()  # noqa: E731
    for _ in range(12):
        prev = text
        text = re.sub(r"\^\s*\{([^{}]*)\}", _tight, text)
        text = re.sub(r"_\s*\{([^{}]*)\}", _tight, text)
        text = re.sub(_LATEX_WRAPPER, r"\1", text)
        text = re.sub(_LATEX_BRACE_RM, r"\1", text)
        text = re.sub(r"\\(?:d?frac)\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"(\1)/(\2)", text)
        if text == prev:
            break
    # a×10^b / a x 10^{b} → ae b（供 extract_number 的 e 记法分支消费）
    text = re.sub(
        r"([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*[xX*]\s*10\s*\^?\{?\s*([+-]?\d+)\}?",
        r"\1e\2", text)
    # 数学定界符、剩余反斜杠命令，再去花括号/$。孤立花括号只是分组符号，
    # 留着会挡在数值与单位之间（`-1.25 {A m^-2}` 里的 `{` 就足以让单位正则失配）。
    text = re.sub(r"\\\\", " ", text)
    text = re.sub(r"\\[\(\)\[\]]", " ", text)
    # 其余未识别的 \command：保留命令名而不是删成空格。删除是有损的——题库里有
    # 按命令名本身匹配的项（化学08 的单位项写作 `‰|permil`），删掉就再也匹配不到；
    # 保留只会多出一个单词 token，对「存在性」类 check 单调有利，也不会凭空造出数字。
    text = re.sub(r"\\([a-zA-Z]+)", r" \1 ", text)
    text = text.replace("$", "").replace("{", " ").replace("}", " ")
    return re.sub(r"\s+", " ", text)


def drop_subscript(text: str) -> str:
    """去掉紧跟字母/希腊字母的下标下划线：`k_0`→`k0`、`σ_tot`→`σtot`。

    题库 check 普遍只写了 `k0` / `k^0` 两种写法（如化学01 的 `k\\s*(?:\\^\\s*0|0)`），
    漏了最常见的数学写法 `k_0`；下标下划线纯属排版，去掉不改变数值或符号。
    比 normalize() 更激进（会把 `x_1` 与 `x1` 视作同一 token），因此单独提供，
    由各题 grade() 按需在 normalize() 之后再调用一次。
    """
    return re.sub(r"(?<=[A-Za-z\u0370-\u03ff])_(?=[0-9A-Za-z])", "", text)


def miller_indices_present(text: str, hkl: str) -> bool:
    """判定 Miller 指数三元组（如 "001"）是否作为独立指标出现，容多种写法。

    命中：(001)/（001）/`001`（紧跟角度/波长注记）/ 英文逗号列举或 LaTeX 归一后失去
    括号的独立三元组 token。排除：正文杂散数字（后接单位/百分号，或嵌在更长数字里）。
    需先对 text 调用 normalize()。
    """
    spaced = r"\s*".join(list(hkl))
    bare = (r"(?<![\d.a-zA-Z])" + spaced +
            r"(?![\d.]|\s*(?:%|Å|nm|g|mol|°|度|meV|eV|K\b))")
    return bool(
        re.search(r"[\(（]\s*" + spaced + r"\s*[\)）]", text)
        or re.search(spaced + r"\s*[（(]\s*\d", text)
        or re.search(bare, text)
    )


def compact(text: str) -> str:
    """进一步去掉括号/分隔符，用于匹配 (5R,6S) / 5R6S / 5R-6S 等等价写法。"""
    return re.sub(r"[\s\(\)\[\]\{\}\-–—·,，:：]", "", text.lower())


# --------------------------------------------------------------------------
# 数值抽取
# --------------------------------------------------------------------------
def _to_float(num: str, exp: Optional[str]) -> float:
    val = float(num)
    if exp:
        val *= 10 ** int(exp)
    return val


def extract_number(text: str, label: str) -> Optional[float]:
    """
    抽取形如 `<label> = 1.25 x 10^-3` / `<label>≈4.17e-2` 的数值（含科学计数/×10^/e 记法）。
    label 为正则片段，例如 r"k\\s*0"、"j"、"w_?2"。
    """
    t = normalize(text)
    pat = (
        rf"{label}\s*[:=≈~约]?\s*(-?\d+\.?\d*)"
        r"(?:\s*x?\s*10\s*\^?\{?\s*(-?\d+)\}?|\s*e\s*(-?\d+))?"
    )
    m = re.search(pat, t, flags=re.IGNORECASE)
    if not m:
        return None
    return _to_float(m.group(1), m.group(2) or m.group(3))


def within_tol(value: Optional[float], target: float, rel_tol: float) -> bool:
    """相对误差判定：|value-target| <= |target|*rel_tol。"""
    if value is None:
        return False
    return abs(value - target) <= abs(target) * rel_tol


def is_refusal(text: str) -> bool:
    """是否为拒答/无法作答。"""
    return has_any(text, [
        r"无法回答", r"不能回答", r"不会做", r"拒绝",
        r"i cannot", r"i can'?t", r"cannot solve",
    ])
