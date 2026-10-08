"""Reflection: make the system critique its own work before shipping it.

The idea is older than LLMs and almost embarrassingly simple: a first draft
produced under pressure to be fluent is worse than a second draft produced
after someone asked "what's wrong with this?". Give a model its own output and
a critic's brief, and it finds real problems -- missing citations, unsupported
claims, unhandled cases -- that it did not notice while generating.

Two things decide whether it actually helps:

* **The critic needs leverage the generator lacked.** A critic with the same
  prompt, same model and same information mostly produces agreeable noise.
  Leverage comes from a different role, a checklist, a stricter model, or --
  best of all -- a real signal: a linter, a test run, a SQL error.
* **It must be able to stop.** Revision loops that run a fixed number of times
  spend money making good drafts different. The loop should exit when the
  critic has nothing material left to say.

Built in Module 02.

Planned interface::

    reflect(
        task: str,
        *,
        generate: Callable[[str], str] | None = None,
        critique: Callable[[str, str], Critique] | None = None,
        max_rounds: int = 3,
    ) -> ReflectionResult
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import NoReturn

from agentic_ai.llm.base import Usage


@dataclass(frozen=True, slots=True)
class Critique:
    """One round of criticism of a draft."""

    #: Whether the critic considers the draft good enough to stop.
    acceptable: bool
    #: Specific, actionable problems. Vague criticism produces vague revisions.
    issues: tuple[str, ...] = ()
    notes: str = ""


@dataclass
class ReflectionResult:
    """The final draft plus the history that produced it."""

    output: str
    drafts: list[str] = field(default_factory=list)
    critiques: list[Critique] = field(default_factory=list)
    rounds: int = 0
    usage: Usage = field(default_factory=Usage)
    cost_usd: float = 0.0


def reflect(*args: object, **kwargs: object) -> NoReturn:
    """Not implemented yet -- see the module docstring.

    Raises:
        NotImplementedError: Always. This pattern is built in Module 02; the
            interface is published here so Module 01's docs can link to it.
    """
    raise NotImplementedError(
        "reflect() is built in Module 02. See docs/patterns/reflection.md for the design, "
        "or agentic_ai.patterns.run_agent for the loop it is built on."
    )
