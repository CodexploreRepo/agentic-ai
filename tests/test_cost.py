"""Cost estimation and the budget guard."""

from __future__ import annotations

import pytest

from agentic_ai.errors import BudgetExceeded
from agentic_ai.llm.base import Usage
from agentic_ai.llm.cost import BudgetGuard, estimate_usd
from agentic_ai.models import CLAUDE_SONNET_5


def test_cost_follows_the_published_rates() -> None:
    usage = Usage(input_tokens=1_000_000, output_tokens=0)
    assert estimate_usd(usage, CLAUDE_SONNET_5.id) == pytest.approx(
        CLAUDE_SONNET_5.input_usd_per_mtok
    )


def test_cached_input_is_cheaper_than_fresh_input() -> None:
    fresh = estimate_usd(Usage(input_tokens=100_000), CLAUDE_SONNET_5.id)
    cached = estimate_usd(Usage(cached_input_tokens=100_000), CLAUDE_SONNET_5.id)
    assert cached < fresh


def test_unknown_models_cost_zero_rather_than_exploding() -> None:
    # A model shipping before we list it must not break a run.
    assert estimate_usd(Usage(input_tokens=1000), "some-model-from-next-year") == 0.0


def test_the_guard_raises_once_the_ceiling_is_crossed() -> None:
    guard = BudgetGuard(budget_usd=0.01)
    with pytest.raises(BudgetExceeded) as exc:
        for _ in range(100):
            guard.record(Usage(input_tokens=10_000, output_tokens=10_000), CLAUDE_SONNET_5.id)
    assert exc.value.budget_usd == 0.01
    assert guard.spent_usd > 0.01


def test_a_zero_budget_tracks_without_enforcing() -> None:
    guard = BudgetGuard(budget_usd=0)
    guard.record(Usage(input_tokens=10_000_000, output_tokens=10_000_000), CLAUDE_SONNET_5.id)
    assert guard.spent_usd > 0
    assert guard.remaining_usd == float("inf")


def test_spend_is_attributed_per_model() -> None:
    guard = BudgetGuard()
    guard.record(Usage(input_tokens=1000), CLAUDE_SONNET_5.id)
    guard.record(Usage(input_tokens=1000), "claude-opus-5")
    assert set(guard.by_model) == {CLAUDE_SONNET_5.id, "claude-opus-5"}
    assert guard.by_model["claude-opus-5"] > guard.by_model[CLAUDE_SONNET_5.id]


def test_usage_adds_up() -> None:
    total = Usage(input_tokens=1, output_tokens=2) + Usage(input_tokens=3, output_tokens=4)
    assert (total.input_tokens, total.output_tokens) == (4, 6)
    assert total.total_tokens == 10
