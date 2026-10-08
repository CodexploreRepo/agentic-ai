"""Running a system over an eval set.

The runner is intentionally ignorant of what it is evaluating. It takes a
callable from input string to output string, which means the same harness
scores a single prompt, an agent loop, a reflection chain, or a whole
multi-agent team -- and so comparisons between them are apples to apples.

That is the point of Module 01's lab: the only honest way to claim an agentic
workflow beats one big prompt is to put both behind the same signature and run
the same cases through each.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

from agentic_ai.evals.dataset import EvalCase, EvalDataset
from agentic_ai.evals.judges import (
    CaseScores,
    Score,
    check_contains,
    check_non_empty,
    judge_with_rubric,
)
from agentic_ai.llm.base import LLMClient, Usage

#: A system under evaluation: input text in, output text out.
System = Callable[[str], str]


@dataclass
class CaseResult:
    """One case, run and scored."""

    case: EvalCase
    output: str
    scores: CaseScores
    duration_s: float = 0.0
    error: str | None = None

    @property
    def passed(self) -> bool:
        """Whether the case passed every check and did not raise."""
        return self.error is None and self.scores.passed


@dataclass
class EvalReport:
    """Results for a whole run, with the aggregates worth looking at."""

    system_name: str
    dataset_name: str
    results: list[CaseResult] = field(default_factory=list)
    judge_usage: Usage = field(default_factory=Usage)
    started_at: float = field(default_factory=time.time)

    @property
    def total(self) -> int:
        """Number of cases run."""
        return len(self.results)

    @property
    def passed(self) -> int:
        """Number of cases that passed every check."""
        return sum(1 for r in self.results if r.passed)

    @property
    def pass_rate(self) -> float:
        """Fraction of cases passing. The headline number."""
        return self.passed / self.total if self.total else 0.0

    @property
    def mean_score(self) -> float:
        """Mean of per-case mean scores.

        Softer than ``pass_rate`` and useful alongside it: a change that moves
        mean score without moving pass rate is making failures less bad, which
        is progress you would otherwise not see.
        """
        if not self.results:
            return 0.0
        return sum(r.scores.overall for r in self.results) / len(self.results)

    @property
    def errored(self) -> list[CaseResult]:
        """Cases where the system raised rather than answered."""
        return [r for r in self.results if r.error is not None]

    @property
    def mean_duration_s(self) -> float:
        """Average wall-clock seconds per case."""
        if not self.results:
            return 0.0
        return sum(r.duration_s for r in self.results) / len(self.results)

    def failures_by_check(self) -> dict[str, int]:
        """How many cases each named check failed.

        This is where error analysis starts. One check failing across most
        cases is a single fixable cause; failures spread evenly across checks
        usually mean the system is weak rather than broken.
        """
        tally: dict[str, int] = {}
        for result in self.results:
            for score in result.scores.failures:
                key = score.name.split(":", 1)[0]
                tally[key] = tally.get(key, 0) + 1
        return dict(sorted(tally.items(), key=lambda kv: -kv[1]))

    def summary(self) -> str:
        """One line, for printing as the run finishes."""
        return (
            f"{self.system_name} on {self.dataset_name}: "
            f"{self.passed}/{self.total} passed ({self.pass_rate:.0%}), "
            f"mean score {self.mean_score:.2f}, "
            f"{self.mean_duration_s:.1f}s/case"
        )


def evaluate(
    system: System,
    dataset: EvalDataset,
    *,
    system_name: str = "system",
    use_judge: bool = True,
    judge_client: LLMClient | None = None,
    judge_model: str | None = None,
    extra_checks: Sequence[Callable[[str, EvalCase], list[Score]]] = (),
    on_case: Callable[[CaseResult], None] | None = None,
) -> EvalReport:
    """Run ``system`` over every case in ``dataset`` and score the outputs.

    Args:
        system: The thing being evaluated. Input string in, output string out.
        dataset: Cases to run.
        system_name: Label used in reports. Name variants precisely
            ("single-prompt", "agentic-v2") -- you will be comparing these
            later and "new" ages badly.
        use_judge: Whether to run the LLM judge on cases that have a rubric.
            Turn it off for a fast, free pass over deterministic checks only.
        judge_client: Client for judging; defaults to the configured provider.
        judge_model: Judge model; defaults to the strongest for that provider.
        extra_checks: Additional scoring functions, for checks specific to one
            lab (for example "cites at least two distinct URLs").
        on_case: Called after each case -- use it to show progress rather than
            leaving a notebook cell blank for two minutes.

    Returns:
        The full report. A case where the system raised is recorded as a
        failure with its error, never silently skipped.
    """
    report = EvalReport(system_name=system_name, dataset_name=dataset.name)

    for case in dataset:
        started = time.perf_counter()
        output = ""
        error: str | None = None
        try:
            output = system(case.input)
        except Exception as exc:
            # A crash is a result. Letting it propagate would lose every case
            # scored so far, which on a paid eval run is an expensive way to
            # learn that case 9 has an empty input.
            error = f"{type(exc).__name__}: {exc}"

        case_scores = CaseScores(case_id=case.id)
        if error is not None:
            case_scores.scores.append(Score(name="no_error", value=0.0, reason=error))
        else:
            case_scores.scores.append(check_non_empty(output))
            case_scores.scores.extend(check_contains(output, case))
            for check in extra_checks:
                case_scores.scores.extend(check(output, case))
            if use_judge and case.rubric:
                score, usage = judge_with_rubric(
                    output, case, client=judge_client, model=judge_model
                )
                case_scores.scores.append(score)
                case_scores.usage = case_scores.usage + usage
                report.judge_usage = report.judge_usage + usage

        result = CaseResult(
            case=case,
            output=output,
            scores=case_scores,
            duration_s=time.perf_counter() - started,
            error=error,
        )
        report.results.append(result)
        if on_case is not None:
            on_case(result)

    return report


def compare(baseline: EvalReport, candidate: EvalReport) -> str:
    """Summarise whether ``candidate`` beat ``baseline``.

    Deliberately blunt about small differences. On a twelve-case set a
    one-case swing is noise, and the fastest way to waste a week is to chase a
    number that moved because of sampling.
    """
    delta_pass = candidate.pass_rate - baseline.pass_rate
    delta_score = candidate.mean_score - baseline.mean_score
    cases = max(baseline.total, 1)
    one_case = 1.0 / cases

    if abs(delta_pass) < one_case * 1.5:
        verdict = f"no clear difference (within ~1 case on {cases} cases)"
    elif delta_pass > 0:
        verdict = f"{candidate.system_name} is better"
    else:
        verdict = f"{candidate.system_name} is worse"

    return (
        f"{baseline.system_name}: {baseline.pass_rate:.0%} pass, "
        f"{baseline.mean_score:.2f} mean\n"
        f"{candidate.system_name}: {candidate.pass_rate:.0%} pass, "
        f"{candidate.mean_score:.2f} mean\n"
        f"delta: {delta_pass:+.0%} pass, {delta_score:+.2f} mean -> {verdict}"
    )
