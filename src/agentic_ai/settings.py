"""Configuration, read once from the environment.

Keys and budgets come from ``.env`` (git-ignored) or the real environment.
Nothing in this library reads ``os.environ`` directly -- it goes through here,
so there is exactly one place to look when a key isn't being picked up.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from agentic_ai.errors import ConfigError

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Everything configurable, with defaults that work for a solo learner."""

    model_config = SettingsConfigDict(
        env_file=(REPO_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Provider credentials ---------------------------------------------
    anthropic_api_key: SecretStr | None = None
    openai_api_key: SecretStr | None = None
    google_api_key: SecretStr | None = None
    tavily_api_key: SecretStr | None = None

    # --- Behaviour --------------------------------------------------------
    agentic_default_provider: str = "anthropic"

    #: Hard ceiling on spend per run, in USD. ``0`` disables the guard. The
    #: default is deliberately small: the most common way to lose money on
    #: agents is a loop that retries a failing tool a few hundred times.
    agentic_run_budget_usd: float = Field(default=1.00, ge=0)

    agentic_trace_dir: Path = Path(".runs")

    @property
    def default_provider(self) -> str:
        """Provider used when a call doesn't name one."""
        return self.agentic_default_provider.strip().lower()

    def key_for(self, provider: str) -> str:
        """Return the API key for ``provider``, or explain what's missing.

        Raises:
            ConfigError: No key configured, with the variable name to set.
        """
        attr = {
            "anthropic": "anthropic_api_key",
            "openai": "openai_api_key",
            "google": "google_api_key",
            "tavily": "tavily_api_key",
        }.get(provider.lower())
        if attr is None:
            raise ConfigError(
                f"unknown provider {provider!r}; expected one of anthropic, openai, google, tavily"
            )
        secret: SecretStr | None = getattr(self, attr)
        if secret is None or not secret.get_secret_value().strip():
            raise ConfigError(
                f"no API key for {provider!r}. Set {attr.upper()} in your .env "
                f"(copy .env.example if you haven't). You only need one model "
                f"provider to run the labs."
            )
        return secret.get_secret_value()

    def has_key(self, provider: str) -> bool:
        """Whether ``provider`` is usable, without raising.

        Used by tests and labs to skip gracefully instead of exploding.
        """
        try:
            self.key_for(provider)
        except ConfigError:
            return False
        return True

    def trace_path(self) -> Path:
        """Absolute trace directory, created on first use."""
        path = self.agentic_trace_dir
        if not path.is_absolute():
            path = REPO_ROOT / path
        path.mkdir(parents=True, exist_ok=True)
        return path


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """The process-wide settings object.

    Cached so that a notebook re-running a cell doesn't re-read ``.env`` and so
    everything agrees on one budget. Call ``get_settings.cache_clear()`` after
    editing ``.env`` mid-session.
    """
    return Settings()
