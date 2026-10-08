"""Exception types raised across the library.

Every error here is deliberate: agent code fails in ways that are easy to paper
over with a bare ``except``, and a vague failure three tool-calls deep is the
single most expensive thing to debug. Each exception below names a distinct
cause so a traceback tells you which layer broke.
"""

from __future__ import annotations


class AgenticError(Exception):
    """Base class for every error this library raises."""


class ConfigError(AgenticError):
    """Configuration is missing or contradictory (e.g. no API key for a provider)."""


class ProviderError(AgenticError):
    """A model provider rejected the request or returned something unusable."""


class ToolExecutionError(AgenticError):
    """A tool raised while the agent was calling it.

    Agent loops catch this and feed the message back to the model as a tool
    result, because a model that is told *why* its call failed will usually fix
    it. The exception still carries the original cause for logs.
    """

    def __init__(self, tool_name: str, message: str) -> None:
        self.tool_name = tool_name
        super().__init__(f"tool {tool_name!r} failed: {message}")


class BudgetExceeded(AgenticError):
    """A run tried to spend past its configured USD ceiling.

    Raised rather than logged, because the entire point of a budget guard is to
    stop the run. See ``agentic_ai.llm.cost.BudgetGuard``.
    """

    def __init__(self, spent_usd: float, budget_usd: float) -> None:
        self.spent_usd = spent_usd
        self.budget_usd = budget_usd
        super().__init__(
            f"run budget exceeded: spent ${spent_usd:.4f} of ${budget_usd:.2f} ceiling. "
            "Raise AGENTIC_RUN_BUDGET_USD or shorten the run."
        )


class MaxStepsExceeded(AgenticError):
    """An agent loop hit its step limit without reaching a stop condition.

    Nearly always a symptom rather than a cause: a tool that never returns what
    the model expects, or a goal the model cannot tell it has achieved.
    """

    def __init__(self, max_steps: int) -> None:
        self.max_steps = max_steps
        super().__init__(
            f"agent did not finish within {max_steps} steps. Inspect the trace: the model is "
            "probably retrying a tool that keeps disappointing it."
        )
