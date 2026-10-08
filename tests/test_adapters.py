"""Message translation for each provider.

These are the pure functions inside the adapters. They need no network and no
keys, and they are where provider differences actually live -- so they are
worth testing even though the SDK call around them is not.
"""

from __future__ import annotations

from agentic_ai.llm.anthropic import _to_anthropic_messages
from agentic_ai.llm.base import Message, ToolCall, split_system
from agentic_ai.llm.gemini import _to_gemini_contents
from agentic_ai.llm.openai import _parse_arguments, _to_openai_messages

CALL = ToolCall(id="c1", name="search", arguments={"q": "mcp"})

CONVERSATION = [
    Message.system("You are terse."),
    Message.user("find something"),
    Message.assistant("looking", (CALL,)),
    Message.tool_result("c1", "result text"),
]


def test_system_messages_are_split_out() -> None:
    system, rest = split_system(CONVERSATION)
    assert system == "You are terse."
    assert all(m.role != "system" for m in rest)


def test_multiple_system_messages_are_joined() -> None:
    system, _ = split_system([Message.system("a"), Message.system("b")])
    assert system == "a\n\nb"


class TestAnthropic:
    def test_tool_results_become_user_blocks(self) -> None:
        # Anthropic has no `tool` role: results ride inside a user message.
        _, rest = split_system(CONVERSATION)
        out = _to_anthropic_messages(rest)
        assert out[-1]["role"] == "user"
        assert out[-1]["content"][0]["type"] == "tool_result"
        assert out[-1]["content"][0]["tool_use_id"] == "c1"

    def test_assistant_text_and_tool_use_share_one_turn(self) -> None:
        _, rest = split_system(CONVERSATION)
        out = _to_anthropic_messages(rest)
        types = [block["type"] for block in out[1]["content"]]
        assert types == ["text", "tool_use"]

    def test_consecutive_tool_results_merge_into_one_message(self) -> None:
        # Anthropic expects every result for a turn to arrive together.
        messages = [
            Message.assistant("", (CALL, ToolCall(id="c2", name="search", arguments={}))),
            Message.tool_result("c1", "one"),
            Message.tool_result("c2", "two"),
        ]
        out = _to_anthropic_messages(messages)
        assert len(out) == 2
        assert len(out[1]["content"]) == 2

    def test_empty_assistant_turn_still_has_content(self) -> None:
        # The API rejects an empty content list.
        out = _to_anthropic_messages([Message.assistant("")])
        assert out[0]["content"] == [{"type": "text", "text": ""}]


class TestOpenAI:
    def test_tool_results_use_the_tool_role(self) -> None:
        _, rest = split_system(CONVERSATION)
        out = _to_openai_messages(rest)
        assert out[-1]["role"] == "tool"
        assert out[-1]["tool_call_id"] == "c1"

    def test_tool_call_arguments_are_json_encoded(self) -> None:
        _, rest = split_system(CONVERSATION)
        out = _to_openai_messages(rest)
        assert out[1]["tool_calls"][0]["function"]["arguments"] == '{"q": "mcp"}'

    def test_invalid_tool_arguments_degrade_instead_of_raising(self) -> None:
        # Models do emit broken JSON here; the loop must survive it and let
        # the model correct itself next turn.
        parsed = _parse_arguments("{not json")
        assert parsed["_error"]
        assert parsed["_raw"] == "{not json"

    def test_empty_arguments_parse_to_an_empty_dict(self) -> None:
        assert _parse_arguments("") == {}


class TestGemini:
    def test_assistant_role_is_renamed_to_model(self) -> None:
        _, rest = split_system(CONVERSATION)
        out = _to_gemini_contents(rest)
        assert out[1]["role"] == "model"

    def test_tool_results_become_function_responses(self) -> None:
        _, rest = split_system(CONVERSATION)
        out = _to_gemini_contents(rest)
        assert "function_response" in out[-1]["parts"][0]

    def test_tool_calls_become_function_call_parts(self) -> None:
        _, rest = split_system(CONVERSATION)
        out = _to_gemini_contents(rest)
        call = out[1]["parts"][-1]["function_call"]
        assert call["name"] == "search"
        assert call["args"] == {"q": "mcp"}


def test_every_adapter_round_trips_the_same_conversation() -> None:
    # The claim the adapter layer makes is that one conversation works
    # everywhere. Assert it for all three rather than trusting it.
    _, rest = split_system(CONVERSATION)
    for translate in (_to_anthropic_messages, _to_openai_messages, _to_gemini_contents):
        out = translate(rest)
        assert len(out) >= 3
        assert all(isinstance(entry, dict) for entry in out)
