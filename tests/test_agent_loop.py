"""The agent loop: stopping, recovering, counting."""

from __future__ import annotations

import pytest
from conftest import FakeLLM, reply, tool_reply

from agentic_ai.errors import MaxStepsExceeded
from agentic_ai.llm.cost import BudgetGuard
from agentic_ai.patterns import run_agent
from agentic_ai.tools import Toolbox, tool


@tool
def shout(text: str) -> str:
    """Return the text in capitals.

    Args:
        text: What to shout.
    """
    return text.upper()


@tool
def always_fails() -> str:
    """A tool that never works."""
    raise RuntimeError("disk on fire")


def test_no_tool_request_ends_the_loop() -> None:
    client = FakeLLM([reply("Done.")])
    result = run_agent("do a thing", client=client, budget=BudgetGuard())

    assert result.output == "Done."
    assert result.steps == 1
    assert result.stopped_because == "finished"
    assert result.succeeded


def test_tool_result_is_fed_back_and_the_loop_continues() -> None:
    client = FakeLLM([tool_reply("shout", {"text": "hello"}), reply("It said HELLO.")])
    result = run_agent("shout hello", client=client, toolbox=Toolbox(shout), budget=BudgetGuard())

    assert result.steps == 2
    assert result.tool_calls_made == ("shout",)
    assert result.succeeded
    # The second call must carry the tool result back to the model.
    second_call_messages = client.calls[1]["messages"]
    assert any(
        m.role == "tool" and m.content == "HELLO"
        for m in second_call_messages  # type: ignore[union-attr]
    )


def test_tool_failure_is_reported_to_the_model_rather_than_raised() -> None:
    # This is the behaviour that makes agents recoverable: the model is told
    # what went wrong and gets another turn.
    client = FakeLLM([tool_reply("always_fails"), reply("I could not do that.")])
    result = run_agent("try it", client=client, toolbox=Toolbox(always_fails), budget=BudgetGuard())

    assert result.succeeded
    tool_messages = [m for m in result.messages if m.role == "tool"]
    assert "disk on fire" in tool_messages[0].content


def test_step_limit_stops_a_model_that_never_finishes() -> None:
    # A model stuck requesting tools forever is the classic runaway loop.
    client = FakeLLM([tool_reply("shout", {"text": "again"})])
    result = run_agent(
        "loop forever",
        client=client,
        toolbox=Toolbox(shout),
        max_steps=4,
        budget=BudgetGuard(),
    )

    assert result.steps == 4
    assert result.stopped_because == "max_steps"
    assert not result.succeeded


def test_step_limit_can_raise_instead() -> None:
    client = FakeLLM([tool_reply("shout", {"text": "again"})])
    with pytest.raises(MaxStepsExceeded):
        run_agent(
            "loop forever",
            client=client,
            toolbox=Toolbox(shout),
            max_steps=2,
            budget=BudgetGuard(),
            raise_on_max_steps=True,
        )


def test_stop_when_ends_the_run_early() -> None:
    client = FakeLLM([reply("PARTIAL"), reply("more")])
    result = run_agent(
        "go",
        client=client,
        budget=BudgetGuard(),
        stop_when=lambda response: "PARTIAL" in response.text,
    )

    assert result.stopped_because == "stop_condition"
    assert result.steps == 1


def test_usage_and_cost_accumulate_across_steps() -> None:
    client = FakeLLM([tool_reply("shout", {"text": "hi"}), reply("done")])
    result = run_agent("go", client=client, toolbox=Toolbox(shout), budget=BudgetGuard())

    # Two model calls at 10 in / 10 out each.
    assert result.usage.input_tokens == 20
    assert result.usage.output_tokens == 20


def test_on_step_callback_sees_every_response() -> None:
    seen: list[int] = []
    client = FakeLLM([tool_reply("shout", {"text": "hi"}), reply("done")])
    run_agent(
        "go",
        client=client,
        toolbox=Toolbox(shout),
        budget=BudgetGuard(),
        on_step=lambda step, _response: seen.append(step),
    )
    assert seen == [1, 2]


def test_the_run_is_traced() -> None:
    client = FakeLLM([tool_reply("shout", {"text": "hi"}), reply("done")])
    result = run_agent("go", client=client, toolbox=Toolbox(shout), budget=BudgetGuard())

    assert result.trace is not None
    kinds = [s.kind for s in result.trace.spans]
    assert "run" in kinds
    assert kinds.count("llm") == 2
    assert kinds.count("tool") == 1


def test_tools_are_offered_to_the_model() -> None:
    client = FakeLLM([reply("done")])
    run_agent("go", client=client, toolbox=Toolbox(shout), budget=BudgetGuard())
    assert client.calls[0]["tools"] == ["shout"]


def test_no_toolbox_means_a_single_plain_call() -> None:
    # The baseline every agentic workflow has to beat.
    client = FakeLLM([reply("one shot answer")])
    result = run_agent("go", client=client, budget=BudgetGuard())
    assert client.calls[0]["tools"] is None
    assert result.steps == 1
