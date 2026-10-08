"""Evaluation harness: datasets, runners, judges, scorecards.

Evaluation comes before patterns in this curriculum on purpose. Every later
module makes a claim -- reflection improves drafts, planning helps on
multi-step tasks, a second agent earns its latency -- and a claim you cannot
measure is just a preference.
"""

from __future__ import annotations

from agentic_ai.evals.dataset import EvalCase, EvalDataset
from agentic_ai.evals.judges import (
    CaseScores,
    Score,
    check_contains,
    check_non_empty,
    judge_with_rubric,
)
from agentic_ai.evals.report import to_markdown, write_scorecard
from agentic_ai.evals.runner import (
    CaseResult,
    EvalReport,
    System,
    compare,
    evaluate,
)

__all__ = [
    "CaseResult",
    "CaseScores",
    "EvalCase",
    "EvalDataset",
    "EvalReport",
    "Score",
    "System",
    "check_contains",
    "check_non_empty",
    "compare",
    "evaluate",
    "judge_with_rubric",
    "to_markdown",
    "write_scorecard",
]
