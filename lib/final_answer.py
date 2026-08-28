"""
ScoreFloor-Sci-Bench — 结论块抽取与量纲判分 (Final Answer Extraction)

给 grade() 用的「收紧口径」层，与 grading_utils 的「放宽写法」层配对：

  grading_utils.normalize()  放宽表现形式 → 治假阴性（答对了要认出来）
  final_answer.match()       收紧抽取口径 → 治假阳性（答错了不许拿分）

做三件事：
  1. 只在**结论块**里找答案（题面要求的 `【结果】…` 那一行），而不是满篇文章乱捞。
     满篇捞是假阳性的头号来源：中间过程的任一数字、正文里随口一句单位，
     都会被当成最终答案（物理04 数值全错后 tau_step 仍拿一半分，就是这么来的）。
  2. **量纲闸门**：值的单位必须与目标量纲相容才算命中。纯标准库实现，无第三方依赖。
     这一条挡掉「数字碰巧对上、量纲完全不搭」的蒙分。
  3. **量级台阶**：命中 / 量级对但偏 / 不命中三档，保留题库既有的梯度评分哲学。

设计上刻意**不强制**结论块存在：找不到块就退化到最后一条消息全文。
不遵守格式不该被扣分——我们要测的是答案对不对，不是听不听话。
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

# 量纲向量维度顺序：长度 质量 时间 电流 温度 物质量 光强
_DIM = Tuple[int, int, int, int, int, int, int]
_ONE: _DIM = (0, 0, 0, 0, 0, 0, 0)


def _d(**kw) -> _DIM:
    order = ("m", "kg", "s", "A", "K", "mol", "cd")
    return tuple(kw.get(k, 0) for k in order)  # type: ignore[return-value]


# 单位符号 → (换算到 SI 的因子, 量纲)。gram 而非 kg 作词条，便于统一加词头。
_UNIT: Dict[str, Tuple[float, _DIM]] = {
    "m": (1.0, _d(m=1)), "g": (1e-3, _d(kg=1)), "s": (1.0, _d(s=1)),
    "A": (1.0, _d(A=1)), "K": (1.0, _d(K=1)), "mol": (1.0, _d(mol=1)),
    "cd": (1.0, _d(cd=1)),
    "L": (1e-3, _d(m=3)), "l": (1e-3, _d(m=3)),
    "Å": (1e-10, _d(m=1)), "min": (60.0, _d(s=1)), "h": (3600.0, _d(s=1)),
    "N": (1.0, _d(kg=1, m=1, s=-2)), "J": (1.0, _d(kg=1, m=2, s=-2)),
    "W": (1.0, _d(kg=1, m=2, s=-3)), "Pa": (1.0, _d(kg=1, m=-1, s=-2)),
    "C": (1.0, _d(s=1, A=1)), "V": (1.0, _d(kg=1, m=2, s=-3, A=-1)),
    "Ω": (1.0, _d(kg=1, m=2, s=-3, A=-2)),
    "F": (1.0, _d(kg=-1, m=-2, s=4, A=2)),
    "S": (1.0, _d(kg=-1, m=-2, s=3, A=2)),
    "T": (1.0, _d(kg=1, s=-2, A=-1)), "Hz": (1.0, _d(s=-1)),
    "eV": (1.602176634e-19, _d(kg=1, m=2, s=-2)),
    "%": (0.01, _ONE), "‰": (1e-3, _ONE), "rad": (1.0, _ONE),
}

_PREFIX = {"Y": 1e24, "Z": 1e21, "E": 1e18, "P": 1e15, "T": 1e12, "G": 1e9,
           "M": 1e6, "k": 1e3, "h": 1e2, "d": 1e-1, "c": 1e-2, "m": 1e-3,
           "μ": 1e-6, "u": 1e-6, "n": 1e-9, "p": 1e-12, "f": 1e-15, "a": 1e-18}


def _one_unit(tok: str) -> Optional[Tuple[float, _DIM]]:
    """单个单位词条（可带词头）→ (因子, 量纲)。不认识返回 None。"""
    if tok in _UNIT:
        return _UNIT[tok]
    # 词头 + 词条。先试整体再试剥词头，避免 "min"(分钟) 被读成 milli-inch。
    if len(tok) >= 2 and tok[0] in _PREFIX and tok[1:] in _UNIT:
        factor, dim = _UNIT[tok[1:]]
        return factor * _PREFIX[tok[0]], dim
    return None


_UNIT_TOKEN = re.compile(
    r"([A-Za-zΩÅμ‰%]+)\s*\^?\s*\{?\s*(-?\d+)?\s*\}?"
)

# 单位词条按长度降序，供 _split_run 做最长匹配。
_UNIT_KEYS = sorted(_UNIT.keys(), key=len, reverse=True)


def _split_run(run: str) -> Optional[List[str]]:
    """把连写的字母串切成已知单位词条序列：`mgL`→['mg','L']、`cms`→['cm','s']。

    为什么必须有这一步：grading_utils.normalize() 会把 `·` 删掉（题库单位正则
    普遍按 `mg\\s*/?\\s*L` 这种紧邻写法写，删掉才匹配得上），于是 `mg·L⁻¹`
    归一后变成 `mgL-1`——单个词条查表必然失败。切不开就返回 None，不猜。

    **取词条数最少的切法**，这一点是必需的而非优化：`mg` 既能读成 milli-gram
    （1 个词条）也能读成 metre·gram（2 个词条），后者量纲完全错。贪心地「最长
    词条优先」会先命中裸 `m` 而给出错的那个，必须比较全部切法取最短。
    """
    if not run:
        return []
    best: Optional[List[str]] = None

    def offer(cand: Optional[List[str]]) -> None:
        nonlocal best
        if cand is not None and (best is None or len(cand) < len(best)):
            best = cand

    for key in _UNIT_KEYS:                      # 裸词条
        if run.startswith(key):
            rest = _split_run(run[len(key):])
            if rest is not None:
                offer([key] + rest)
    if len(run) >= 2 and run[0] in _PREFIX:     # 词头 + 词条
        for key in _UNIT_KEYS:
            if run[1:].startswith(key):
                rest = _split_run(run[1 + len(key):])
                if rest is not None:
                    offer([run[0] + key] + rest)
    return best


def parse_unit(text: str) -> Optional[Tuple[float, _DIM]]:
    """解析单位串 → (换算到 SI 的因子, 量纲向量)。

    支持 `mg/L`、`cm s^-1`、`A m^-2`、`mol dm^-3`、`s⁻¹`（须先 normalize），
    以及分隔符被 normalize 删掉后的连写形式 `mgL-1`、`Am-2`、`moldm-3`。
    任一词条切不开/不认识就整体返回 None——宁可判「无法判定」也不要猜，
    猜错方向会造出新的假阳性。
    """
    text = text.strip()
    if not text:
        return None
    factor, dim = 1.0, list(_ONE)
    # `/` 之后的所有词条指数取反：`mg/L` → mg · L^-1
    for part, sign in _split_slash(text):
        pos = 0
        while pos < len(part):
            m = _UNIT_TOKEN.match(part, pos)
            if not m:
                if part[pos] in " ·*":
                    pos += 1
                    continue
                return None
            toks = _split_run(m.group(1))
            if not toks:
                return None
            exp = int(m.group(2) or 1) * sign
            for i, tok in enumerate(toks):
                got = _one_unit(tok)
                if got is None:
                    return None
                f, d = got
                # 指数只施加给连写串的**最后一个**词条：`mgL-1` = mg·L^-1，
                # 而不是 (mg·L)^-1。这是化学单位最常见的写法。
                e = exp if i == len(toks) - 1 else sign
                factor *= f ** e
                dim = [a + b * e for a, b in zip(dim, d)]
            pos = m.end()
    return factor, tuple(dim)  # type: ignore[return-value]


def _split_slash(text: str) -> List[Tuple[str, int]]:
    parts = text.split("/")
    return [(parts[0], 1)] + [(p, -1) for p in parts[1:]]


# --------------------------------------------------------------------------
# 结论块定位
# --------------------------------------------------------------------------
# 题库现有三种结论标记；`FINAL:` 是新增协议，其余是既有题面/答复已在用的。
# `答案：`/`答：`/`结论：` 收进来的理由：化学题题面没有格式要求，但模型自发写
# 「**答案：…**」的比例很高（化学04 5 个 run 里 4 个），能白捡一部分「只在块内取值」的收益。
_BLOCK_MARKS = (r"FINAL\s*[:：]", r"【结果】", r"【结论】",
                r"最终(?:结论|答案|结果)\s*[:：]?",
                r"答案\s*[:：]", r"答\s*[:：]", r"结论\s*[:：]")


def final_block(text: str, span: int = 600) -> str:
    """取结论块正文。取**最后一次**出现的标记之后 span 个字符。

    找不到标记返回全文——不遵守格式不扣分，只是失去「收紧口径」的收益。
    取最后一次而非第一次：模型常在开头写"最终结论"做摘要、末尾再正式给一遍，
    末尾那份才是定稿。
    """
    best = -1
    for mark in _BLOCK_MARKS:
        for m in re.finditer(mark, text, flags=re.IGNORECASE):
            if m.end() > best:
                best = m.end()
    return text if best < 0 else text[best:best + span]


# --------------------------------------------------------------------------
# 键值抽取 + 判分
# --------------------------------------------------------------------------
_NUM = (r"([+-]?(?:\d+(?:\.\d*)?|\.\d+))"
        r"(?:\s*[xX*]\s*10\s*\^?\{?\s*([+-]?\d+)\}?|\s*[eE]\s*([+-]?\d+))?")
# 单位紧跟数值：懒惰吃到第一个「不可能属于单位」的字符为止。
# 收尾必须用「非单位字符」而不是列举分隔符——结论块里紧跟单位的可能是
# 全角括号（`s^-1（Br 0.900）`）、顿号、破折号，列举法总会漏，漏一个就整条失配。
_UNIT_CHARS = r"A-Za-zΩÅμ‰%/·^\-\{\}\d "
_UNIT_AFTER = rf"[ \t]*([{_UNIT_CHARS}]{{0,24}}?)(?=[^{_UNIT_CHARS}]|$)"
# `=（0.108）/（0.0360）` 这类把值裹进括号的写法很常见，允许一个前导开括号。
_ASSIGN = r"\s*[:=≈~约]?\s*\(?\s*"


def _candidates(block: str, label: str):
    """产出 (值, 单位串) 全部候选，按出现顺序。"""
    for m in re.finditer(rf"{label}{_ASSIGN}{_NUM}{_UNIT_AFTER}",
                         block, flags=re.IGNORECASE):
        val = float(m.group(1))
        exp = m.group(2) or m.group(3)
        if exp:
            val *= 10 ** int(exp)
        unit = _cut_next_label(m.group(4) or "", block[m.end():m.end() + 1])
        yield val, (unit or None)


def _cut_next_label(unit: str, nxt: str) -> str:
    """去掉被吞进单位串尾部的**下一个量的名字**。

    结论块里各量常挤在一行（normalize 会把换行折成空格）：
        `C_0 = 15.0 mg/L C_x = 3.00 mg/L`
    单位串按「吃到第一个非单位字符为止」抓取，会连 `C_x` 的 `C` 一起吃进来，
    得到 `mg/L C`——而它**照样解析成功**（C = 库仑），量纲变成 mg·L⁻¹·s·A，
    与目标不相容，于是这个本来正确的候选被量纲闸门静默淘汰。

    判据：抓取停在 `_ = : ：` 这类只可能属于「新赋值」的字符前，
    则单位串最后一个空格分段是下一个量的标签，删掉。
    """
    if nxt in ("_", "=", ":", "：") and " " in unit.strip():
        return unit.strip().rsplit(" ", 1)[0]
    return unit.strip()


def find_value(block: str, label: str, want: Optional[_DIM] = None):
    """在块内按 label 取 (数值, 单位串)。label 为正则片段。

    给了 want（目标量纲）时，**跳过单位量纲不相容的候选**。这一条在没有结论块、
    只能拿全文当块的情况下是决定性的：化学04 的 `原废水取样 10.00 mL` 会被
    `(?:总|原|废水)…` 这类标签正则捞到，量纲一比（体积 vs 浓度）立刻淘汰。

    多个候选时取**最后一个**：模型常在中途算一遍、末尾再复述定稿，末尾那份才算。

    ⚠️ label 里若带 `[^=\n]{0,24}` 这类「跳过若干字再取数」的填充段，务必写成
    **懒惰** `{0,24}?`。贪婪版会把 `总Pb浓度为 15.0 mgL^-1` 一路吃到 `mgL^`、
    只剩 `-1` 当数值，抽出 1.0 而不是 15.0——而且它照样"抽到了值"，
    不报错、只是安静地错，比抽不到更难发现。
    """
    picked = None
    for val, unit in _candidates(block, label):
        if want is not None and unit is not None:
            got = parse_unit(unit)
            if got is not None and got[1] != want:
                continue          # 量纲不搭：不是我们要的那个量
        picked = (val, unit)
    return picked if picked else (None, None)


def match(block: str, label: str, target: float, unit: str = "",
          rel_tol: float = 0.05, loose_tol: float = 1.0,
          require_unit: bool = False) -> dict:
    """结论块内按 label 判一个量，返回梯度结果。

      hit        命中（相对误差 <= rel_tol 且量纲相容）
      near       量级对但偏（误差 <= loose_tol），给半分用
      dim_ok     量纲相容（unit 为空则不判、记 None）
      value      抽到的值（已换算到目标单位）；抽不到为 None
      score      1.0 / 0.5 / 0.0 三档

    量纲不相容一律判 0，即使数字碰巧对上——这是假阳性的主闸门。

    单位缺失（模型没写单位）的处置由 `require_unit` 决定：
      False（默认）不因此判 0，只是拿不到量纲加分——测的是答案不是格式。
      True         判 0。分析化学这类语境下「15.0」与「15.0 mg/L」不等价，
                   漏单位是实质缺陷；用这一档把 has_unit 收进量纲闸门，
                   既不留「漏单位无代价」的漏洞，也不额外造一个白拿项
                   （它只会扣分、不会凭「写了单位」加分）。
    """
    want = parse_unit(unit) if unit else None
    raw, unit_str = find_value(block, label, want[1] if want else None)
    dim_ok: Optional[bool] = None
    val = raw

    if raw is not None and want is not None:
        got = parse_unit(unit_str) if unit_str else None
        if got is None:
            dim_ok = None          # 没写单位或看不懂：不判，按目标单位裸值比
        else:
            dim_ok = got[1] == want[1]
            if dim_ok:
                val = raw * got[0] / want[0]   # 换算到目标单位再比数值

    if val is None or dim_ok is False or (require_unit and dim_ok is not True):
        score, err = 0.0, None
    else:
        err = abs(val - target) / abs(target) if target else None
        score = 1.0 if (err is not None and err <= rel_tol) else \
            0.5 if (err is not None and err <= loose_tol) else 0.0

    return {"value": val, "raw": raw, "unit": unit_str, "dim_ok": dim_ok,
            "rel_err": err, "hit": score >= 1.0, "near": score == 0.5,
            "score": score}
