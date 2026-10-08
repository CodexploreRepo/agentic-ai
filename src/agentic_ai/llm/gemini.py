"""Google Gemini adapter.

Included mainly so the provider-agnostic claim is tested by a third
implementation rather than asserted by two. Gemini's vocabulary differs more
than OpenAI's and Anthropic's do from each other: turns are "contents" with
"parts", the assistant role is called ``model``, and tool results are
``functionResponse`` parts.
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
    "STOP": "stop",
    "MAX_TOKENS": "max_tokens",
}


class GeminiClient:
    """Wraps ``google-genai`` in this library's ``LLMClient`` shape."""

    provider = "google"

    def __init__(self, api_key: str | None = None) -> None:
        from google import genai

        key = api_key or get_settings().key_for("google")
        self._client = genai.Client(api_key=key)

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
        """Send a conversation to Gemini. See the protocol for argument meanings."""
        inline_system, rest = split_system(messages)
        system_prompt = system or inline_system

        config: dict[str, Any] = {"max_output_tokens": max_tokens}
        if system_prompt:
            config["system_instruction"] = system_prompt
        if temperature is not None:
            config["temperature"] = temperature
        if tools:
            config["tools"] = [
                {
                    "function_declarations": [
                        {"name": t.name, "description": t.description, "parameters": t.parameters}
                        for t in tools
                    ]
                }
            ]

        model_id = model or DEFAULT_MODEL["google"]
        try:
            response = self._client.models.generate_content(
                model=model_id,
                contents=_to_gemini_contents(rest),
                # The SDK types this as a TypedDict; we build it dynamically
                # because which keys apply depends on the call.
                config=cast(Any, config),
            )
        except Exception as exc:  # re-raised as ProviderError so callers catch one type
            raise ProviderError(f"Gemini call failed: {exc}") from exc

        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        candidates = response.candidates or []
        finish_reason = ""
        if candidates:
            finish_reason = str(getattr(candidates[0], "finish_reason", "") or "")
            content = getattr(candidates[0], "content", None)
            for index, part in enumerate(getattr(content, "parts", None) or []):
                if getattr(part, "text", None):
                    text_parts.append(part.text)
                call = getattr(part, "function_call", None)
                if call is not None:
                    tool_calls.append(
                        ToolCall(
                            # Gemini does not always return a call id, but the
                            # agent loop needs one to match results to calls.
                            id=getattr(call, "id", None) or f"{call.name}-{index}",
                            name=call.name,
                            arguments=dict(call.args or {}),
                        )
                    )

        meta = response.usage_metadata
        return ChatResponse(
            message=Message.assistant("\n".join(text_parts), tuple(tool_calls)),
            model=model_id,
            usage=Usage(
                input_tokens=getattr(meta, "prompt_token_count", 0) or 0,
                output_tokens=getattr(meta, "candidates_token_count", 0) or 0,
                cached_input_tokens=getattr(meta, "cached_content_token_count", 0) or 0,
            ),
            stop_reason=(
                "tool_use" if tool_calls else _STOP_REASONS.get(finish_reason.upper(), "other")
            ),
            raw=response,
        )


def _to_gemini_contents(messages: list[Message]) -> list[dict[str, Any]]:
    """Translate our messages into Gemini ``contents``."""
    out: list[dict[str, Any]] = []
    for msg in messages:
        if msg.role == "tool":
            out.append(
                {
                    "role": "user",
                    "parts": [
                        {
                            "function_response": {
                                "name": msg.tool_call_id or "tool",
                                "response": {"result": msg.content},
                            }
                        }
                    ],
                }
            )
        elif msg.role == "assistant":
            parts: list[dict[str, Any]] = []
            if msg.content:
                parts.append({"text": msg.content})
            parts.extend(
                {"function_call": {"name": tc.name, "args": tc.arguments}} for tc in msg.tool_calls
            )
            out.append({"role": "model", "parts": parts or [{"text": ""}]})
        else:
            out.append({"role": "user", "parts": [{"text": msg.content}]})
    return out
