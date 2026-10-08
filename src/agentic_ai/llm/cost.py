"""What a run cost, and stopping it before it costs more.

Agents spend money in a loop, which makes them the first LLM application where
cost is a correctness concern rather than an accounting one. A tool that always
returns an error the model doesn't understand produces a polite, determined
agent that retries until your budget is gone.

So cost here is not a report you read afterwards. ``BudgetGuard`` is checked on
every call and raises :class:`~agentic_ai.errors.BudgetExceeded` the moment a
run crosses its ceiling.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from agentic_ai.errors import BudgetExceeded
from agentic_ai.llm.base import Usage
from agentic_ai.models import lookup
from agentic_ai.settings import get_settings

#: Providers bill cached input tokens at a fraction of the normal input rate.
#: The exact discount varies; 10% is the right order of magnitude and keeps the
#: arithmetic honest about caching being worth setting up.
CACHED_INPUT_DISCOUNT = 0.10


def estimate_usd(usage: Usage, model_id: str) -> float:
    """Estimate the USD cost of ``usage`` on ``model_id``.

    Returns ``0.0`` for models absent from :mod:`agentic_ai.models` -- an
    unpriced model should not break a run, and a zero is visibly wrong in a
    scorecard, which is the behaviour we want.
    """
    info = lookup(model_id)
    if info is None:
        return 0.0
    per_token_in = info.input_usd_per_mtok / 1_000_000
    per_token_out = info.output_usd_per_mtok / 1_000_000
    return (
        usage.input_tokens * per_token_in
        + usage.cached_input_tokens * per_token_in * CACHED_INPUT_DISCOUNT
        + usage.output_tokens * per_token_out
    )


@dataclass
class BudgetGuard:
    """Accumulates spend for one run and refuses to let it overrun.

    Not thread-safe, and intentionally so: one guard belongs to one run, and
    sharing one across concurrent runs would make the ceiling meaningless.

    Example:
        >>> guard = BudgetGuard(budget_usd=0.50)
        >>> guard.record(Usage(input_tokens=1000, output_tokens=500), "claude-sonnet-5")
        >>> round(guard.spent_usd, 6)
        0.0105
    """

    #: Ceiling in USD. ``0`` disables enforcement but still tracks spend.
    budget_usd: float = 0.0
    spent_usd: float = 0.0
    calls: int = 0
    usage: Usage = field(default_factory=Usage)
    #: Spend split by model, so a scorecard can show where the money went --
    #: usually a judge model called once per case.
    by_model: dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_settings(cls) -> BudgetGuard:
        """Build a guard using ``AGENTIC_RUN_BUDGET_USD``."""
        return cls(budget_usd=get_settings().agentic_run_budget_usd)

    def record(self, usage: Usage, model_id: str) -> float:
        """Add one call's usage and return its cost.

        Raises:
            BudgetExceeded: The run has now crossed its ceiling. Raised *after*
                recording, so the guard's totals reflect what was actually
                spent rather than what fit inside the budget.
        """
        cost = estimate_usd(usage, model_id)
        self.spent_usd += cost
        self.calls += 1
        self.usage = self.usage + usage
        self.by_model[model_id] = self.by_model.get(model_id, 0.0) + cost

        if self.budget_usd > 0 and self.spent_usd > self.budget_usd:
            raise BudgetExceeded(self.spent_usd, self.budget_usd)
        return cost

    @property
    def remaining_usd(self) -> float:
        """Headroom left, or ``inf`` when unenforced."""
        if self.budget_usd <= 0:
            return float("inf")
        return max(0.0, self.budget_usd - self.spent_usd)

    def summary(self) -> str:
        """A one-line human-readable total, for printing at the end of a lab."""
        cache_note = ""
        if self.usage.cached_input_tokens:
            share = self.usage.cached_input_tokens / max(
                1, self.usage.input_tokens + self.usage.cached_input_tokens
            )
            cache_note = f", {share:.0%} of input cached"
        return (
            f"{self.calls} call{'s' if self.calls != 1 else ''} · "
            f"{self.usage.total_tokens:,} tokens{cache_note} · "
            f"~${self.spent_usd:.4f}"
        )
