"""Shared test fixtures.

The important thing here is ``FakeLLM``. Because ``LLMClient`` is a Protocol,
a usable test double is a plain class with a ``chat`` method -- no mocking
library, no patching, no network. That is a deliberate design payoff of the
adapter layer, and it is why the whole suite runs in under a second with no API
keys configured.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from agentic_ai.llm.base import ChatResponse, Message, ToolCall, ToolSpec, Usage


class FakeLLM:
    """A scripted model. Returns queued responses in order, then repeats the last.

    Also records every call so tests can assert on what the agent loop actually
    sent -- which is usually the interesting part.
    """

    provider = "fake"

    def __init__(self, responses: list[ChatResponse] | None = None) -> None:
        self.responses = responses or []
        self.calls: list[dict[str, object]] = []

    def chat(
        self,
        messages: list[Message],
        *,
        model: str | None = None,
        tools: list[ToolSpec] | None = None,
        system: str | None = None,
        temperature: float | None = None,
        max_tokens: int = 4096,
    ) -> ChatResponse:
        """Return the next scripted response."""
        self.calls.append(
            {
                "messages": list(messages),
                "model": model,
                "tools": [t.name for t in tools] if tools else None,
                "system": system,
                "temperature": temperature,
            }
        )
        if not self.responses:
            return reply("(no scripted response)")
        index = min(len(self.calls) - 1, len(self.responses) - 1)
        return self.responses[index]


def reply(text: str, *, model: str = "fake-1", tokens: int = 10) -> ChatResponse:
    """Build a plain text response."""
    return ChatResponse(
        message=Message.assistant(text),
        model=model,
        usage=Usage(input_tokens=tokens, output_tokens=tokens),
        stop_reason="stop",
    )


def tool_reply(
    name: str,
    arguments: dict[str, object] | None = None,
    *,
    call_id: str = "call-1",
    text: str = "",
    model: str = "fake-1",
) -> ChatResponse:
    """Build a response that asks for one tool call."""
    return ChatResponse(
        message=Message.assistant(
            text, (ToolCall(id=call_id, name=name, arguments=dict(arguments or {})),)
        ),
        model=model,
        usage=Usage(input_tokens=10, output_tokens=10),
        stop_reason="tool_use",
    )


@pytest.fixture
def fake_llm() -> FakeLLM:
    """An unscripted fake model."""
    return FakeLLM()


@pytest.fixture(autouse=True)
def isolate_traces(tmp_path: object, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Keep tests from writing trace files into the repo."""
    monkeypatch.setenv("AGENTIC_TRACE_DIR", str(tmp_path))
    from agentic_ai.settings import get_settings

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
