"""Model identifiers and their prices, in one place.

Model names and prices churn faster than anything else in an agent codebase.
Keeping them here means updating a frontier model across the whole repo --
library, labs, evals -- is a one-line edit rather than a grep-and-pray.

Prices are USD per million tokens and are approximate; treat the numbers from
``agentic_ai.llm.cost`` as an order-of-magnitude guide for teaching purposes,
not as billing truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

Provider = str


@dataclass(frozen=True, slots=True)
class ModelInfo:
    """What the library needs to know about a model to use and price it."""

    id: str
    provider: Provider
    context_window: int
    input_usd_per_mtok: float
    output_usd_per_mtok: float
    notes: str = ""


# --- Anthropic -------------------------------------------------------------
CLAUDE_OPUS_5: Final = ModelInfo(
    id="claude-opus-5",
    provider="anthropic",
    context_window=200_000,
    input_usd_per_mtok=15.0,
    output_usd_per_mtok=75.0,
    notes="Most capable. Use for planning, judging, and hard reasoning steps.",
)
CLAUDE_SONNET_5: Final = ModelInfo(
    id="claude-sonnet-5",
    provider="anthropic",
    context_window=200_000,
    input_usd_per_mtok=3.0,
    output_usd_per_mtok=15.0,
    notes="The default workhorse: strong tool use at a price you can loop on.",
)
CLAUDE_HAIKU_45: Final = ModelInfo(
    id="claude-haiku-4-5-20251001",
    provider="anthropic",
    context_window=200_000,
    input_usd_per_mtok=1.0,
    output_usd_per_mtok=5.0,
    notes="Cheap and fast. Good for routing, classification, and extraction.",
)

# --- OpenAI ----------------------------------------------------------------
GPT_5: Final = ModelInfo(
    id="gpt-5",
    provider="openai",
    context_window=400_000,
    input_usd_per_mtok=1.25,
    output_usd_per_mtok=10.0,
)
GPT_5_MINI: Final = ModelInfo(
    id="gpt-5-mini",
    provider="openai",
    context_window=400_000,
    input_usd_per_mtok=0.25,
    output_usd_per_mtok=2.0,
)

# --- Google ----------------------------------------------------------------
GEMINI_25_PRO: Final = ModelInfo(
    id="gemini-2.5-pro",
    provider="google",
    context_window=1_048_576,
    input_usd_per_mtok=1.25,
    output_usd_per_mtok=10.0,
)
GEMINI_25_FLASH: Final = ModelInfo(
    id="gemini-2.5-flash",
    provider="google",
    context_window=1_048_576,
    input_usd_per_mtok=0.30,
    output_usd_per_mtok=2.50,
)

REGISTRY: Final[dict[str, ModelInfo]] = {
    m.id: m
    for m in (
        CLAUDE_OPUS_5,
        CLAUDE_SONNET_5,
        CLAUDE_HAIKU_45,
        GPT_5,
        GPT_5_MINI,
        GEMINI_25_PRO,
        GEMINI_25_FLASH,
    )
}

#: The model each provider uses when a call doesn't name one. Mid-tier on
#: purpose -- agent loops make many calls, and the frontier model is rarely
#: what makes the difference between a working and a broken loop.
DEFAULT_MODEL: Final[dict[Provider, str]] = {
    "anthropic": CLAUDE_SONNET_5.id,
    "openai": GPT_5.id,
    "google": GEMINI_25_FLASH.id,
}

#: Model used wherever the library needs a cheap, fast decision (routing,
#: classification) rather than a careful one.
FAST_MODEL: Final[dict[Provider, str]] = {
    "anthropic": CLAUDE_HAIKU_45.id,
    "openai": GPT_5_MINI.id,
    "google": GEMINI_25_FLASH.id,
}

#: Model used for LLM-as-judge. Deliberately the strongest available: a judge
#: that is weaker than the system it grades produces evals you cannot trust.
JUDGE_MODEL: Final[dict[Provider, str]] = {
    "anthropic": CLAUDE_OPUS_5.id,
    "openai": GPT_5.id,
    "google": GEMINI_25_PRO.id,
}


def lookup(model_id: str) -> ModelInfo | None:
    """Return what we know about ``model_id``, or ``None`` if it is unlisted.

    Unlisted models work fine -- they just can't be priced. Returning ``None``
    rather than raising keeps the library usable the day a new model ships.
    """
    return REGISTRY.get(model_id)
