"""Anthropic adapter.

Shape of the API worth knowing, because it differs from OpenAI's in ways that
matter to an agent loop:

* The system prompt is a top-level argument, not a message.
* Content is a *list of blocks*, so one assistant turn can hold text and
  several ``tool_use`` blocks together.
* Tool results go back as ``tool_result`` blocks inside a **user** message, not
  as a separate ``tool`` role.
"""

from __future__ import annotations

from typing import Any, cast

from agentic_ai.errors import ProviderError
from agentic_ai.llm.base import (
    ChatResponse,
    Message,
    StopReason,
    ToolCall,
    ToolSpec,
    Usage,
    split_system,
)
from agentic_ai.models import DEFAULT_MODEL
from agentic_ai.settings import get_settings

_STOP_REASONS: dict[str, StopReason] = {
    "end_turn": "stop",
    "stop_sequence": "stop",
    "tool_use": "tool_use",
    "max_tokens": "max_tokens",
}


class AnthropicClient:
    """Wraps the ``anthropic`` SDK in this library's ``LLMClient`` shape."""

    provider = "anthropic"

    def __init__(self, api_key: str | None = None) -> None:
        import anthropic

        key = api_key or get_settings().key_for("anthropic")
        self._client = anthropic.Anthropic(api_key=key)

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
        """Send a conversation to Claude. See the protocol for argument meanings."""
        inline_system, rest = split_system(messages)
        system_prompt = system or inline_system

        kwargs: dict[str, Any] = {
            "model": model or DEFAULT_MODEL["anthropic"],
            "max_tokens": max_tokens,
            "messages": _to_anthropic_messages(rest),
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        if tools:
            kwargs["tools"] = [
                {"name": t.name, "description": t.description, "input_schema": t.parameters}
                for t in tools
            ]
        if temperature is not None:
            kwargs["temperature"] = temperature

        try:
            response = self._client.messages.create(**kwargs)
        except Exception as exc:  # re-raised as ProviderError so callers catch one type
            raise ProviderError(f"Anthropic call failed: {exc}") from exc

        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        arguments=cast(dict[str, Any], block.input or {}),
                    )
                )

        return ChatResponse(
            message=Message.assistant("\n".join(text_parts), tuple(tool_calls)),
            model=response.model,
            usage=Usage(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                cached_input_tokens=getattr(response.usage, "cache_read_input_tokens", 0) or 0,
            ),
            stop_reason=_STOP_REASONS.get(response.stop_reason or "", "other"),
            raw=response,
        )


def _to_anthropic_messages(messages: list[Message]) -> list[dict[str, Any]]:
    """Translate our messages into Anthropic's block format.

    Consecutive tool results are merged into a single user message, because
    Anthropic expects every ``tool_result`` for a turn to arrive together.
    """
    out: list[dict[str, Any]] = []
    for msg in messages:
        if msg.role == "tool":
            block = {
                "type": "tool_result",
                "tool_use_id": msg.tool_call_id,
                "content": msg.content,
            }
            if out and out[-1]["role"] == "user" and isinstance(out[-1]["content"], list):
                out[-1]["content"].append(block)
            else:
                out.append({"role": "user", "content": [block]})
        elif msg.role == "assistant":
            content: list[dict[str, Any]] = []
            if msg.content:
                content.append({"type": "text", "text": msg.content})
            content.extend(
                {"type": "tool_use", "id": tc.id, "name": tc.name, "input": tc.arguments}
                for tc in msg.tool_calls
            )
            out.append({"role": "assistant", "content": content or [{"type": "text", "text": ""}]})
        else:
            out.append({"role": "user", "content": msg.content})
    return out
