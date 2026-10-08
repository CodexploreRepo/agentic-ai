"""Agentic design patterns as reusable, tested code.

Each pattern is a function here and a page in ``docs/patterns/``. The code is
the authority on behaviour; the page explains when to reach for it and when
not to. Labs import from this package -- a notebook in this repo never defines
a pattern inline, because a pattern that only exists in a notebook cannot be
tested, reused, or improved.
"""

from __future__ import annotations

from agentic_ai.patterns.tool_use import (
    DEFAULT_MAX_STEPS,
    AgentResult,
    run_agent,
)

__all__ = ["DEFAULT_MAX_STEPS", "AgentResult", "run_agent"]
