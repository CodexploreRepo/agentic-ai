"""Planning: decide the steps before taking them.

The agent loop in :mod:`agentic_ai.patterns.tool_use` plans implicitly, one
step at a time, which is fine until the task has dependencies the model cannot
see from step one. Explicit planning splits the work: produce a plan, then
execute it.

What you gain is inspectability -- a plan can be shown to a user, checked
against a budget, or rejected before a single tool runs. What you pay is a
model call and the risk of a plan made on worse information than the executor
will eventually have. The interesting design question is therefore not whether
to plan but whether to *replan*, and on what trigger.

Built in Module 05.

Planned interface::

    plan(task: str, ...) -> Plan
    execute_plan(plan: Plan, ...) -> PlanResult
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import NoReturn


@dataclass(frozen=True, slots=True)
class Step:
    """One planned step."""

    description: str
    #: Indices of steps that must complete first. Empty means it can run now,
    #: which is also what makes parallel execution possible.
    depends_on: tuple[int, ...] = ()
    tool: str | None = None


@dataclass
class Plan:
    """An ordered set of steps, with the reasoning that produced it."""

    goal: str
    steps: list[Step] = field(default_factory=list)
    rationale: str = ""


def plan(*args: object, **kwargs: object) -> NoReturn:
    """Not implemented yet -- built in Module 05.

    Raises:
        NotImplementedError: Always. See docs/patterns/planning.md.
    """
    raise NotImplementedError("plan() is built in Module 05. See docs/patterns/planning.md.")
