"""OpenAI adapter.

Uses Chat Completions rather than the Responses API on purpose: it is the shape
most readers already have in their head, and it maps onto our message types
without hiding the agent loop behind server-side state. The teaching goal here
is for the loop to be visible.
"""

from __future__ import annotations

import json
from typing import Any

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
    "stop": "stop",
    "tool_calls": "tool_use",
    "function_call": "tool_use",
    "length": "max_tokens",
}


class OpenAIClient:
    """Wraps the ``openai`` SDK in this library's ``LLMClient`` shape."""

    provider = "openai"

    def __init__(self, api_key: str | None = None) -> None:
        import openai

        key = api_key or get_settings().key_for("openai")
        self._client = openai.OpenAI(api_key=key)

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
        """Send a conversation to an OpenAI model. See the protocol for argument meanings."""
        inline_system, rest = split_system(messages)
        system_prompt = system or inline_system

        payload: list[dict[str, Any]] = []
        if system_prompt:
            payload.append({"role": "system", "content": system_prompt})
        payload.extend(_to_openai_messages(rest))

        kwargs: dict[str, Any] = {
            "model": model or DEFAULT_MODEL["openai"],
            "messages": payload,
            "max_completion_tokens": max_tokens,
        }
        if tools:
            kwargs["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.parameters,
                    },
                }
                for t in tools
            ]
        if temperature is not None:
            kwargs["temperature"] = temperature

        try:
            response = self._client.chat.completions.create(**kwargs)
        except Exception as exc:  # re-raised as ProviderError so callers catch one type
            raise ProviderError(f"OpenAI call failed: {exc}") from exc

        if not response.choices:
            raise ProviderError("OpenAI returned no choices")
        choice = response.choices[0]

        tool_calls: list[ToolCall] = []
        for call in choice.message.tool_calls or []:
            if getattr(call, "type", "function") != "function":
                continue
            tool_calls.append(
                ToolCall(
                    id=call.id,
                    name=call.function.name,
                    arguments=_parse_arguments(call.function.arguments),
                )
            )

        usage = response.usage
        cached = 0
        if usage is not None and usage.prompt_tokens_details is not None:
            cached = usage.prompt_tokens_details.cached_tokens or 0

        return ChatResponse(
            message=Message.assistant(choice.message.content or "", tuple(tool_calls)),
            model=response.model,
            usage=Usage(
                # OpenAI counts cached tokens inside prompt_tokens; we report
                # them separately, so subtract to avoid double-counting cost.
                input_tokens=(usage.prompt_tokens - cached) if usage else 0,
                output_tokens=usage.completion_tokens if usage else 0,
                cached_input_tokens=cached,
            ),
            stop_reason=_STOP_REASONS.get(choice.finish_reason or "", "other"),
            raw=response,
        )


def _parse_arguments(raw: str) -> dict[str, Any]:
    """Decode a tool-call argument blob.

    Models occasionally emit invalid JSON here. Returning the broken payload
    under a ``_raw`` key, rather than raising, lets the agent loop hand the
    problem back to the model -- which usually fixes it on the next turn.
    """
    try:
        parsed = json.loads(raw or "{}")
    except json.JSONDecodeError:
        return {"_raw": raw, "_error": "arguments were not valid JSON"}
    return parsed if isinstance(parsed, dict) else {"_raw": parsed}


def _to_openai_messages(messages: list[Message]) -> list[dict[str, Any]]:
    """Translate our messages into Chat Completions format."""
    out: list[dict[str, Any]] = []
    for msg in messages:
        if msg.role == "tool":
            out.append({"role": "tool", "tool_call_id": msg.tool_call_id, "content": msg.content})
        elif msg.role == "assistant":
            entry: dict[str, Any] = {"role": "assistant", "content": msg.content or None}
            if msg.tool_calls:
                entry["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments),
                        },
                    }
                    for tc in msg.tool_calls
                ]
            out.append(entry)
        else:
            out.append({"role": "user", "content": msg.content})
    return out
