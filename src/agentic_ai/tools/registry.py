"""Turning Python functions into tools a model can call.

A tool has two audiences. The runtime needs a callable with real arguments; the
model needs a name, a description and a JSON Schema. Writing both by hand means
they drift, and a schema that disagrees with the function is a bug you only
discover when the model trips over it mid-run.

So we derive the model-facing half from the Python half. Type hints become the
schema, the docstring becomes the description, and the ``Args:`` section
becomes per-parameter descriptions -- which matters more than it looks, because
those descriptions are the only hint the model gets about what you meant by
``max_results``.

    >>> @tool
    ... def add(a: int, b: int = 0) -> str:
    ...     '''Add two numbers.
    ...
    ...     Args:
    ...         a: First number.
    ...         b: Second number.
    ...     '''
    ...     return str(a + b)
    >>> add.spec.parameters["required"]
    ['a']
    >>> add(a=2, b=3)
    '5'
"""

from __future__ import annotations

import inspect
import json
import re
import types
import typing
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, Union, get_args, get_origin, overload

from agentic_ai.errors import ToolExecutionError
from agentic_ai.llm.base import ToolCall, ToolSpec

_PRIMITIVES: dict[type, str] = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
}

#: How much of a tool's return value is handed to the model. Tool output is the
#: main way an agent's context window fills up with material nobody chose, so
#: truncation is a default rather than an option. Raise it per tool when the
#: tool genuinely needs to return a lot.
DEFAULT_MAX_RESULT_CHARS = 8_000


def _json_type(annotation: Any) -> dict[str, Any]:
    """Map a type annotation onto a JSON Schema fragment.

    Unknown types degrade to ``{"type": "string"}``: a slightly loose schema
    costs one confused tool call, while raising at import time costs the reader
    their whole notebook.
    """
    if annotation is inspect.Parameter.empty or annotation is Any:
        return {"type": "string"}
    if annotation in _PRIMITIVES:
        return {"type": _PRIMITIVES[annotation]}

    origin = get_origin(annotation)

    if origin is Literal:
        options = list(get_args(annotation))
        kinds = {type(o) for o in options}
        base = _PRIMITIVES.get(kinds.pop(), "string") if len(kinds) == 1 else "string"
        return {"type": base, "enum": options}

    if origin in (Union, types.UnionType):
        args = [a for a in get_args(annotation) if a is not type(None)]
        schema = _json_type(args[0]) if args else {"type": "string"}
        if len(get_args(annotation)) > len(args):
            schema = {**schema, "nullable": True}
        return schema

    if origin in (list, set, tuple):
        item_args = get_args(annotation)
        return {
            "type": "array",
            "items": _json_type(item_args[0]) if item_args else {"type": "string"},
        }

    if origin is dict:
        return {"type": "object"}

    return {"type": "string"}


def _parse_docstring(doc: str | None) -> tuple[str, dict[str, str]]:
    """Split a Google-style docstring into a summary and per-argument help."""
    if not doc:
        return "", {}
    text = inspect.cleandoc(doc)
    match = re.search(r"^\s*(?:Args|Arguments|Parameters):\s*$", text, re.MULTILINE)
    if match is None:
        return text.split("\n\nReturns:")[0].strip(), {}

    summary = text[: match.start()].strip()
    body = text[match.end() :]
    # Stop at the next top-level section.
    body = re.split(
        r"^\s*(?:Returns|Raises|Yields|Example[s]?|Note[s]?):\s*$", body, flags=re.MULTILINE
    )[0]

    args: dict[str, str] = {}
    current: str | None = None
    for line in body.splitlines():
        if not line.strip():
            continue
        header = re.match(r"^\s{0,8}(\*{0,2}\w+)\s*(?:\([^)]*\))?\s*:\s*(.*)$", line)
        if header:
            current = header.group(1).lstrip("*")
            args[current] = header.group(2).strip()
        elif current:
            args[current] = f"{args[current]} {line.strip()}".strip()
    return summary, args


@dataclass
class Tool:
    """A callable paired with the schema that describes it to a model."""

    fn: Callable[..., Any]
    spec: ToolSpec
    max_result_chars: int = DEFAULT_MAX_RESULT_CHARS

    @property
    def name(self) -> str:
        """The tool's name, as the model sees it."""
        return self.spec.name

    def __call__(self, **kwargs: Any) -> Any:
        """Call the underlying function directly, unwrapped."""
        return self.fn(**kwargs)

    def run(self, arguments: dict[str, Any]) -> str:
        """Execute the tool and return a string for the model.

        Everything is coerced to a string because that is what goes back into
        the conversation. Long results are truncated with a visible marker --
        silently dropping half a tool result produces an agent that confidently
        reasons from a sentence that was cut in two.

        Raises:
            ToolExecutionError: The tool raised, or was called with arguments
                it does not accept. Agent loops catch this and report it to the
                model rather than aborting the run.
        """
        try:
            result = self.fn(**arguments)
        except TypeError as exc:
            raise ToolExecutionError(
                self.name,
                f"{exc}. Schema expects: {json.dumps(self.spec.parameters.get('properties', {}))}",
            ) from exc
        except Exception as exc:
            raise ToolExecutionError(self.name, str(exc)) from exc

        text = result if isinstance(result, str) else json.dumps(result, default=str, indent=2)
        if len(text) > self.max_result_chars:
            omitted = len(text) - self.max_result_chars
            text = (
                text[: self.max_result_chars] + f"\n\n[truncated: {omitted:,} more characters. "
                "Narrow the query or request a specific portion.]"
            )
        return text


@overload
def tool(fn: Callable[..., Any]) -> Tool: ...


@overload
def tool(
    *,
    name: str | None = ...,
    description: str | None = ...,
    max_result_chars: int = ...,
) -> Callable[[Callable[..., Any]], Tool]: ...


def tool(
    fn: Callable[..., Any] | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
    max_result_chars: int = DEFAULT_MAX_RESULT_CHARS,
) -> Tool | Callable[[Callable[..., Any]], Tool]:
    """Describe a function to a model. Usable bare or with arguments.

    Args:
        fn: The function, when used as a bare ``@tool``.
        name: Override the tool name (defaults to the function name).
        description: Override the description (defaults to the docstring).
        max_result_chars: Truncation ceiling for this tool's output.

    Returns:
        A :class:`Tool`, or a decorator producing one.
    """

    def decorate(func: Callable[..., Any]) -> Tool:
        summary, arg_docs = _parse_docstring(func.__doc__)
        hints = typing.get_type_hints(func)
        signature = inspect.signature(func)

        properties: dict[str, Any] = {}
        required: list[str] = []
        for param_name, param in signature.parameters.items():
            if param_name == "self" or param.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue
            schema = _json_type(hints.get(param_name, param.annotation))
            if param_name in arg_docs:
                schema["description"] = arg_docs[param_name]
            if param.default is not inspect.Parameter.empty:
                schema["default"] = param.default
            else:
                required.append(param_name)
            properties[param_name] = schema

        return Tool(
            fn=func,
            spec=ToolSpec(
                name=name or func.__name__,
                description=description or summary or f"Call {func.__name__}.",
                parameters={
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            ),
            max_result_chars=max_result_chars,
        )

    return decorate(fn) if fn is not None else decorate


class Toolbox:
    """The set of tools one agent may use.

    Exists so an agent loop takes a single object instead of juggling a list of
    specs and a name-to-callable dict that can fall out of sync.
    """

    def __init__(self, *tools: Tool) -> None:
        self._tools: dict[str, Tool] = {}
        for item in tools:
            self.add(item)

    def add(self, item: Tool) -> Toolbox:
        """Register a tool. Returns self, so calls chain."""
        if item.name in self._tools:
            raise ValueError(
                f"two tools named {item.name!r}. Models pick tools by name, so "
                "duplicates make the choice ambiguous -- rename one."
            )
        self._tools[item.name] = item
        return self

    @property
    def specs(self) -> list[ToolSpec]:
        """Schemas to send to the model."""
        return [t.spec for t in self._tools.values()]

    @property
    def names(self) -> tuple[str, ...]:
        """Registered tool names, in registration order."""
        return tuple(self._tools)

    def __contains__(self, name: object) -> bool:
        """Whether a tool of this name is registered."""
        return name in self._tools

    def __len__(self) -> int:
        """How many tools are registered."""
        return len(self._tools)

    def dispatch(self, call: ToolCall) -> str:
        """Run one model-requested tool call and return its result as text.

        A call naming an unregistered tool returns an error string listing what
        *is* available, rather than raising. Models hallucinate tool names
        occasionally, and a loop that recovers beats a loop that dies.
        """
        item = self._tools.get(call.name)
        if item is None:
            return (
                f"Error: no tool named {call.name!r}. "
                f"Available tools: {', '.join(self.names) or 'none'}."
            )
        try:
            return item.run(call.arguments)
        except ToolExecutionError as exc:
            return f"Error: {exc}"
