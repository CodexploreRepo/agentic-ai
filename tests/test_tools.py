"""Tool schema derivation and dispatch."""

from __future__ import annotations

from typing import Literal

import pytest

from agentic_ai.llm.base import ToolCall
from agentic_ai.tools import Tool, Toolbox, tool


@tool
def greet(name: str, excited: bool = False, times: int = 1) -> str:
    """Greet somebody by name.

    Args:
        name: Who to greet.
        excited: Whether to add an exclamation mark.
        times: How many times to repeat the greeting.
    """
    suffix = "!" if excited else "."
    return " ".join([f"Hello {name}{suffix}"] * times)


def test_schema_comes_from_type_hints() -> None:
    props = greet.spec.parameters["properties"]
    assert props["name"]["type"] == "string"
    assert props["excited"]["type"] == "boolean"
    assert props["times"]["type"] == "integer"


def test_only_arguments_without_defaults_are_required() -> None:
    assert greet.spec.parameters["required"] == ["name"]
    assert greet.spec.parameters["properties"]["times"]["default"] == 1


def test_descriptions_come_from_the_docstring() -> None:
    assert greet.spec.description == "Greet somebody by name."
    assert greet.spec.parameters["properties"]["name"]["description"] == "Who to greet."


def test_literal_becomes_an_enum() -> None:
    @tool
    def pick(mode: Literal["fast", "careful"]) -> str:
        """Pick a mode.

        Args:
            mode: Which mode.
        """
        return mode

    assert pick.spec.parameters["properties"]["mode"]["enum"] == ["fast", "careful"]


def test_list_becomes_a_typed_array() -> None:
    @tool
    def tally(words: list[str]) -> str:
        """Count words.

        Args:
            words: The words.
        """
        return str(len(words))

    schema = tally.spec.parameters["properties"]["words"]
    assert schema["type"] == "array"
    assert schema["items"]["type"] == "string"


def test_tool_stays_callable() -> None:
    assert greet(name="Quan", excited=True) == "Hello Quan!"


def test_long_results_are_truncated_visibly() -> None:
    @tool(max_result_chars=50)
    def verbose() -> str:
        """Return too much."""
        return "x" * 500

    result = verbose.run({})
    assert "truncated" in result
    assert len(result) < 500


def test_toolbox_dispatches_by_name() -> None:
    box = Toolbox(greet)
    result = box.dispatch(ToolCall(id="1", name="greet", arguments={"name": "World"}))
    assert result == "Hello World."


def test_unknown_tool_returns_a_recoverable_error() -> None:
    # The loop must survive a hallucinated tool name, and the model needs to be
    # told what it could have called instead.
    box = Toolbox(greet)
    result = box.dispatch(ToolCall(id="1", name="nope", arguments={}))
    assert "no tool named" in result
    assert "greet" in result


def test_bad_arguments_are_reported_not_raised() -> None:
    box = Toolbox(greet)
    result = box.dispatch(ToolCall(id="1", name="greet", arguments={"wrong": 1}))
    assert result.startswith("Error:")


def test_tool_exceptions_become_error_text() -> None:
    @tool
    def explode() -> str:
        """Always fails."""
        raise RuntimeError("boom")

    result = Toolbox(explode).dispatch(ToolCall(id="1", name="explode", arguments={}))
    assert "boom" in result


def test_duplicate_names_are_rejected() -> None:
    with pytest.raises(ValueError, match="two tools named"):
        Toolbox(greet, greet)


def test_toolbox_reports_its_contents() -> None:
    box = Toolbox(greet)
    assert len(box) == 1
    assert "greet" in box
    assert isinstance(box.specs[0].name, str)
    assert isinstance(greet, Tool)
