"""Getting a client without naming a vendor.

``get_client()`` is how every lab and pattern in this repo obtains a model. It
means a notebook written against Claude runs against GPT by changing one line
in ``.env`` -- which is the whole point of the adapter layer, and also the
cheapest way to find out whether a prompt you wrote is robust or just
over-fitted to one model's habits.
"""

from __future__ import annotations

from functools import lru_cache

from agentic_ai.errors import ConfigError
from agentic_ai.llm.base import LLMClient
from agentic_ai.settings import get_settings

_PROVIDERS = ("anthropic", "openai", "google")


@lru_cache(maxsize=8)
def get_client(provider: str | None = None) -> LLMClient:
    """Return a client for ``provider``, defaulting to the configured one.

    Clients are cached per provider: the SDKs hold connection pools, and
    rebuilding one per call in a notebook is a slow, silent waste.

    Args:
        provider: ``"anthropic"``, ``"openai"``, or ``"google"``. ``None`` uses
            ``AGENTIC_DEFAULT_PROVIDER``.

    Returns:
        A ready client satisfying :class:`~agentic_ai.llm.base.LLMClient`.

    Raises:
        ConfigError: Unknown provider, or no API key configured for it.
    """
    name = (provider or get_settings().default_provider).strip().lower()

    if name == "anthropic":
        from agentic_ai.llm.anthropic import AnthropicClient

        return AnthropicClient()
    if name == "openai":
        from agentic_ai.llm.openai import OpenAIClient

        return OpenAIClient()
    if name == "google":
        from agentic_ai.llm.gemini import GeminiClient

        return GeminiClient()

    raise ConfigError(f"unknown provider {name!r}; expected one of {', '.join(_PROVIDERS)}")


def available_providers() -> tuple[str, ...]:
    """Providers that have a usable API key right now.

    Labs use this to pick a provider automatically, so a reader with only an
    OpenAI key isn't stopped by a notebook that defaults to Anthropic.
    """
    settings = get_settings()
    return tuple(p for p in _PROVIDERS if settings.has_key(p))
