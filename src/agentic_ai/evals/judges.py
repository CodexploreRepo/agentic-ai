"""Scoring one output.

Two kinds of check, and the order matters. Deterministic checks are free,
instant, and never wrong about what they measure -- run them first and run them
always. An LLM judge is for the part that genuinely needs reading: is this
brief actually useful, is this answer actually grounded in the sources.

The standing risk with LLM judges is that they are agreeable. A judge asked
"is this good?" says yes. A judge given a rubric, asked to find specific
problems, and required to produce a number *after* its reasoning is much harder
to flatter. That ordering is baked into the prompt below on purpose.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from agentic_ai.evals.dataset import EvalCase
from agentic_ai.llm.base import LLMClient, Message, Usage
from agentic_ai.llm.registry import get_client
from agentic_ai.models import JUDGE_MODEL


@dataclass(frozen=True, slots=True)
class Score:
    """The result of one check.

    ``value`` is always 0.0--1.0 so that heterogeneous checks can be averaged.
    ``reason`` exists because a bare number tells you a case failed but not
    what to do about it, and that is the whole job of an eval.
    """

    name: str
    value: float
    reason: str = ""

    @property
    def passed(self) -> bool:
        """Treat anything at or above 0.5 as a pass."""
        return self.value >= 0.5


@dataclass
class CaseScores:
    """Every score for one case, plus what the judging cost."""

    case_id: str
    scores: list[Score] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)

    @property
    def overall(self) -> float:
        """Mean of all scores, or 0.0 when nothing was checked."""
        if not self.scores:
            return 0.0
        return sum(s.value for s in self.scores) / len(self.scores)

    @property
    def passed(self) -> bool:
        """A case passes only if every individual check passed.

        Deliberately strict: a brief that is well written but cites nothing is
        not 50% correct, it is wrong.
        """
        return bool(self.scores) and all(s.passed for s in self.scores)

    @property
    def failures(self) -> list[Score]:
        """The checks that failed -- the input to error analysis."""
        return [s for s in self.scores if not s.passed]


def check_contains(output: str, case: EvalCase) -> list[Score]:
    """Check required and forbidden substrings, case-insensitively."""
    haystack = output.lower()
    scores: list[Score] = []

    for needle in case.expect_contains:
        found = needle.lower() in haystack
        scores.append(
            Score(
                name=f"contains:{needle[:40]}",
                value=1.0 if found else 0.0,
                reason="" if found else f"expected to find {needle!r}",
            )
        )

    for needle in case.expect_absent:
        absent = needle.lower() not in haystack
        scores.append(
            Score(
                name=f"absent:{needle[:40]}",
                value=1.0 if absent else 0.0,
                reason="" if absent else f"should not contain {needle!r}",
            )
        )

    return scores


def check_non_empty(output: str, min_chars: int = 40) -> Score:
    """Check the system produced something at all.

    Worth having explicitly: an agent that hits its step limit returns a short
    fragment, and without this check that failure scores as "no substring
    violations" and quietly passes.
    """
    length = len(output.strip())
    return Score(
        name="non_empty",
        value=1.0 if length >= min_chars else 0.0,
        reason="" if length >= min_chars else f"output was {length} chars, need {min_chars}",
    )


_JUDGE_SYSTEM = """You are a strict evaluator. You are not here to be encouraging.

You will receive a TASK, a RUBRIC, and a RESPONSE. Judge only whether the
RESPONSE satisfies the RUBRIC for that TASK. Ignore style unless the rubric
mentions it. Do not reward length, confidence, or fluency.

Work in this order:
1. List the specific ways the response fails the rubric. If there are none, say so.
2. Only then assign a score.

Scoring guide:
  1.0  satisfies every rubric criterion
  0.7  satisfies the main criteria, one minor gap
  0.4  addresses the task but misses a criterion that matters
  0.0  fails the task, or is unsupported by the sources it cites

Reply with JSON only, no prose outside it:
{"issues": ["..."], "score": 0.0, "reason": "one sentence"}"""


def judge_with_rubric(
    output: str,
    case: EvalCase,
    *,
    client: LLMClient | None = None,
    model: str | None = None,
) -> tuple[Score, Usage]:
    """Score ``output`` against ``case.rubric`` using a model.

    Uses the strongest configured model by default: a judge weaker than the
    system it grades produces numbers you cannot act on.

    Returns:
        The score, and the judging call's token usage so it can be billed to
        the eval run rather than hidden.
    """
    if not case.rubric:
        return Score(name="rubric", value=1.0, reason="no rubric for this case"), Usage()

    client = client or get_client()
    judge_model = model or JUDGE_MODEL.get(client.provider)

    response = client.chat(
        [Message.user(f"TASK:\n{case.input}\n\nRUBRIC:\n{case.rubric}\n\nRESPONSE:\n{output}")],
        system=_JUDGE_SYSTEM,
        model=judge_model,
        temperature=0.0,
        max_tokens=1024,
    )

    verdict = _parse_verdict(response.text)
    issues = verdict.get("issues") or []
    reason = str(verdict.get("reason", "")).strip()
    if issues and isinstance(issues, list):
        reason = f"{reason} Issues: {'; '.join(str(i) for i in issues[:3])}".strip()

    return Score(name="rubric", value=_clamp(verdict.get("score")), reason=reason), response.usage


def _parse_verdict(text: str) -> dict[str, object]:
    """Extract the judge's JSON, tolerating code fences and stray prose."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match is None:
        return {"score": 0.0, "reason": f"judge returned no JSON: {text[:120]}"}
    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError:
        return {"score": 0.0, "reason": f"judge returned invalid JSON: {text[:120]}"}
    return parsed if isinstance(parsed, dict) else {"score": 0.0, "reason": "unexpected JSON shape"}


def _clamp(value: object) -> float:
    """Coerce a judge's score into 0.0--1.0, treating nonsense as failure."""
    try:
        return max(0.0, min(1.0, float(value)))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0
