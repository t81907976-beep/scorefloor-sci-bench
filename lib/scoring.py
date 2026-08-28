"""
ScoreFloor-Sci-Bench — 总计分引擎 (Scoring Engine)

实现 docs/scoring-rules.md 里的分层计分口径：

    单次运行成功率 S_i = (最终答复分 + 步骤分 + 逻辑分) / 3
    单任务成功率   S_success = mean(S_1..S_5)
    单任务效率     S_eff      = mean(S_i * E_norm_i)
    单任务一致性   S_consistency = max(1 - CV, 0)
    单任务总分     S_task = S_success*0.6 + S_eff*0.2 + S_consistency*0.2
    学科/全 Bench  S_total = mean(S_task)

其中效率：
    E_raw_i  = N0 / N_i
    E_norm_i = min(E_raw_i / E_max, 1)   # E_max 默认 1.5
    E_norm_i = 0                          # 反向激励闸门：step_score == 0（空转）时

所有分数归一化到 0~1。边界规则见 scoring-rules.md 第六节。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean, pstdev
from typing import List, Optional


E_MAX_DEFAULT = 1.5  # 效率上限：步骤精简至基准的约 67% 时效率拿满


# --------------------------------------------------------------------------
# 单次运行
# --------------------------------------------------------------------------
@dataclass
class RunResult:
    """一道题的第 i 次运行结果。三块子维度均为 0~1。"""

    final_answer_score: float   # 最终答复分（代码侧硬证据折算）
    step_score: float           # 步骤分
    logic_score: float          # 逻辑分（LLM Judge Rubric 折算）
    actual_steps: int           # 该次有效步骤数 N_i（排除错误/冗余/无关）

    @property
    def success(self) -> float:
        """单次运行成功率 S_i = (最终答复分 + 步骤分 + 逻辑分) / 3。"""
        return (self.final_answer_score + self.step_score + self.logic_score) / 3.0

    def raw_efficiency(self, baseline_steps: int) -> float:
        """原始效率系数 E_raw = N0 / N_i。N_i=0 时按 E_max 计（见边界规则）。"""
        if self.actual_steps <= 0:
            return E_MAX_DEFAULT
        return baseline_steps / self.actual_steps

    def norm_efficiency(self, baseline_steps: int, e_max: float = E_MAX_DEFAULT) -> float:
        """
        归一化效率系数 E_norm = min(E_raw / E_max, 1)，但**空转 run 一律记 0**。

        反向激励闸门：
        原式只看步骤数不看有没有在解题，`N_i` 小就给高分，于是「一步不推、
        直接报个数」拿到 E_norm 满分。0804 化学09 实测：

            run2  N_i=1  422 字  step=0.0  logic=0.0  → E_norm 1.0（效率满分）
            run5  N_i=1  501 字  step=0.0  logic=0.0  → E_norm 1.0
            run1  N_i=3  1337 字 step=0.15 logic=0.24 → E_norm 0.4（唯一真在解的被压）

        裁判已判出 run2/run5 是空转（step 与 logic 双 0），效率项却给满分——
        两项在同一个 run 上结论相反，而效率占 20% 权重。全库 `corr(S_success,
        mean N_i) = +0.5835`：步骤越多分越高，与「效率」的立意正好反过来。

        ⚠️ **此处只允许判 `> 0`，不得改成阈值比较**（`step_score > 0.3` 这类）。
        两条理由：
          1. `step_score` 是裁判给的，裁判换标度它就整体平移，任何非零阈值都会
             跟着漂，而 `> 0` 是「有没有推导」这个事实本身，标度无关。
          2. 曾提过的另一版是闸在 `S_i > 0.3` 上——那是架在**被审计的结果分**上，
             地板高于 0.3 的题（化学04 地板 0.840、物理08 0.550）闸门形同不存在，
             等于用一个已知被污染的量去守另一个量。闸在过程上才与答案正确性解耦。
        """
        if self.step_score <= 0:
            return 0.0
        return min(self.raw_efficiency(baseline_steps) / e_max, 1.0)

    def efficiency_score(self, baseline_steps: int, e_max: float = E_MAX_DEFAULT) -> float:
        """单次效率得分 S_eff_i = S_i * E_norm_i（有效成功的效率）。"""
        return self.success * self.norm_efficiency(baseline_steps, e_max)


# --------------------------------------------------------------------------
# 单任务（同题重复 N 次，默认 5 次）
# --------------------------------------------------------------------------
@dataclass
class TaskResult:
    """一道题的完整评分：聚合多次运行 → 成功率/效率/一致性 → 单题总分。"""

    task_id: str
    baseline_steps: int                       # 基准步骤数 N0（标准答案最优解步骤数）
    runs: List[RunResult] = field(default_factory=list)
    e_max: float = E_MAX_DEFAULT
    subject: str = ""                         # 学科：chemistry / math / physics / biology

    # 权重
    w_success: float = 0.6
    w_eff: float = 0.2
    w_consistency: float = 0.2

    # ---- 成功率 (60%) ----
    @property
    def success(self) -> float:
        """S_success = mean(S_i)。"""
        if not self.runs:
            return 0.0
        return mean(r.success for r in self.runs)

    # ---- 效率 (20%) ----
    @property
    def efficiency(self) -> float:
        """S_eff = mean(S_i * E_norm_i)。"""
        if not self.runs:
            return 0.0
        return mean(r.efficiency_score(self.baseline_steps, self.e_max) for r in self.runs)

    # ---- 一致性 (20%) ----
    @property
    def consistency(self) -> float:
        """S_consistency = max(1 - CV, 0)，CV = σ/μ。μ=0（全错）时视为稳定，CV=0。"""
        if not self.runs:
            return 0.0
        mu = self.success
        if mu <= 0:
            return 1.0  # 5 次全错视为稳定表现 → CV=0 → 一致性=1
        sigma = pstdev([r.success for r in self.runs]) if len(self.runs) > 1 else 0.0
        cv = sigma / mu
        return max(1.0 - cv, 0.0)

    # ---- 单任务总分 ----
    @property
    def task_score(self) -> float:
        """S_task = S_success*0.6 + S_eff*0.2 + S_consistency*0.2。"""
        return (
            self.success * self.w_success
            + self.efficiency * self.w_eff
            + self.consistency * self.w_consistency
        )

    def breakdown(self) -> dict:
        """返回可打印/落库的完整拆分。"""
        return {
            "task_id": self.task_id,
            "subject": self.subject,
            "baseline_steps": self.baseline_steps,
            "n_runs": len(self.runs),
            "per_run": [
                {
                    "S_i": round(r.success, 4),
                    "N_i": r.actual_steps,
                    "E_norm": round(r.norm_efficiency(self.baseline_steps, self.e_max), 4),
                    "S_eff_i": round(r.efficiency_score(self.baseline_steps, self.e_max), 4),
                }
                for r in self.runs
            ],
            "S_success": round(self.success, 4),
            "S_eff": round(self.efficiency, 4),
            "S_consistency": round(self.consistency, 4),
            "S_task": round(self.task_score, 4),
        }


# --------------------------------------------------------------------------
# 学科 / 全 Bench
# --------------------------------------------------------------------------
def subject_score(tasks: List[TaskResult], subject: Optional[str] = None) -> float:
    """分学科总分 = 该学科所有单题总分的算术平均。subject=None 时统计全部。"""
    selected = [t for t in tasks if subject is None or t.subject == subject]
    if not selected:
        return 0.0
    return mean(t.task_score for t in selected)


def bench_total(tasks: List[TaskResult]) -> float:
    """全 Bench 总分 S_total = mean(S_task)。"""
    return subject_score(tasks, subject=None)


def summarize(tasks: List[TaskResult]) -> dict:
    """汇总：全 Bench 总分 + 各学科分 + 每题拆分。"""
    subjects = sorted({t.subject for t in tasks if t.subject})
    return {
        "bench_total": round(bench_total(tasks), 4),
        "by_subject": {s: round(subject_score(tasks, s), 4) for s in subjects},
        "tasks": [t.breakdown() for t in tasks],
    }


if __name__ == "__main__":
    # 自检：复刻 scoring-rules.md 第七节的计算示例（N0=10, E_max=1.5）
    demo = TaskResult(
        task_id="demo",
        baseline_steps=10,
        e_max=1.5,
        runs=[
            RunResult(1.0, 1.0, 1.0, 8),
            RunResult(1.0, 0.5, 1.0, 10),
            RunResult(0.0, 0.5, 0.5, 12),
            RunResult(1.0, 1.0, 0.5, 9),
            RunResult(1.0, 0.5, 1.0, 11),
        ],
    )
    b = demo.breakdown()
    print("S_success   =", b["S_success"], "(期望 ≈ 0.7666)")
    print("S_eff       =", b["S_eff"], "(期望 ≈ 0.539)")
    print("S_consistency=", b["S_consistency"], "(期望 ≈ 0.705)")
    print("S_task      =", b["S_task"], "(期望 ≈ 0.709)")

    # 自检：反向激励闸门。空转 run（step_score=0）效率必须为 0，
    # 且不能顺手改成阈值比较——step_score 极小但非零时闸门要放行。
    spin = RunResult(0.5, 0.0, 0.0, 1)      # 一步不推、直接报个数
    real = RunResult(0.5, 0.15, 0.24, 3)    # 真在解题，步骤偏多
    tiny = RunResult(0.5, 0.01, 0.10, 1)    # step 极小但非零 → 必须放行
    assert spin.norm_efficiency(5) == 0.0, "空转 run 的 E_norm 必须为 0"
    assert real.norm_efficiency(5) > 0.0, "真在解题的 run 不该被闸掉"
    assert tiny.norm_efficiency(5) == 1.0, "闸门只判 > 0，不得退化成阈值比较"
    print("反向激励闸门 = 空转 0.0 / 真解 %.4f / 极小非零 %.4f  ✓"
          % (real.norm_efficiency(5), tiny.norm_efficiency(5)))
