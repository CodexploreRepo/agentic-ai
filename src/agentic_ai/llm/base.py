"""One shape for every model provider.

Agent patterns are provider-independent ideas. Reflection is reflection whether
Claude or GPT is doing the critiquing. But provider SDKs disagree about almost
everything -- where the system prompt goes, how tool calls come back, what a
tool result looks like on the way in -- and if you let those disagreements reach
your pattern code, the pattern stops being readable and starts being a pile of
``if provider ==`` branches.

So the types in this module are the contract. Each adapter in this package
translates one SDK into these types and nothing else leaks out. Pattern code in
``agentic_ai.patterns`` imports only from here.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Literal, Protocol, runtime_checkable

Role = Literal["system", "user", "assistant", "tool"]

#: Why the model stopped. Normalised across providers: ``"tool_use"`` means it
#: wants tools run, ``"stop"`` means it finished, ``"max_tokens"`` means it was
#: cut off mid-thought (treat that as a failure, not an answer).
StopReason = Literal["stop", "tool_use", "max_tokens", "other"]


@dataclass(frozen=True, slots=True)
class ToolCall:
    """A model's request to run one tool."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    """A tool as described *to* the model: name, purpose, JSON Schema for args.

    The description is not documentation -- it is prompt. It is the only thing
    telling the model when this tool is the right choice, so it earns the same
    care as any other prompt you write.
    """

    name: str
    description: str
    parameters: dict[str, Any]


@dataclass(frozen=True, slots=True)
class Message:
    """One turn of conversation.

    Construct these with the classmethods rather than the raw initialiser; they
    keep the role/field combinations valid (a tool result needs its
    ``tool_call_id``, an assistant tool-use turn needs its ``tool_calls``).
    """

    role: Role
    content: str = ""
    tool_calls: tuple[ToolCall, ...] = ()
    #: Set only on ``role="tool"``: which ToolCall this answers.
    tool_call_id: str | None = None

    @classmethod
    def system(cls, content: str) -> Message:
        """Instructions for the model."""
        return cls(role="system", content=content)

    @classmethod
    def user(cls, content: str) -> Message:
        """Input from the user (or from an outer agent)."""
        return cls(role="user", content=content)

    @classmethod
    def assistant(cls, content: str = "", tool_calls: tuple[ToolCall, ...] = ()) -> Message:
        """A model turn, optionally requesting tools."""
        return cls(role="assistant", content=content, tool_calls=tool_calls)

    @classmethod
    def tool_result(cls, tool_call_id: str, content: str) -> Message:
        """The result of running one tool, on its way back to the model."""
        return cls(role="tool", content=content, tool_call_id=tool_call_id)


@dataclass(frozen=True, slots=True)
class Usage:
    """Token counts for one or more calls.

    Addable so a whole run can be summed: ``sum(usages, Usage())``.
    """

    input_tokens: int = 0
    output_tokens: int = 0
    #: Tokens served from the provider's prompt cache. Counted separately
    #: because they are billed at a fraction of the input rate, and because a
    #: cache hit rate near zero on a long-running agent is a cost bug.
    cached_input_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        """Every token the call touched, cached or not."""
        return self.input_tokens + self.output_tokens + self.cached_input_tokens

    def __add__(self, other: Usage) -> Usage:
        """Combine two usage records."""
        return Usage(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            cached_input_tokens=self.cached_input_tokens + other.cached_input_tokens,
        )

    __radd__ = __add__


@dataclass(frozen=True, slots=True)
class ChatResponse:
    """What one model call returned, normalised."""

    message: Message
    model: str
    usage: Usage = field(default_factory=Usage)
    stop_reason: StopReason = "stop"
    #: The untouched provider payload. Kept so a lab can show what the
    #: abstraction is hiding -- useful when teaching, essential when debugging.
    raw: Any = None

    @property
    def text(self) -> str:
        """The assistant's text content."""
        return self.message.content

    @property
    def tool_calls(self) -> tuple[ToolCall, ...]:
        """Tools the model asked to run; empty if it did not ask for any."""
        return self.message.tool_calls

    @property
    def wants_tools(self) -> bool:
        """Whether the agent loop should run tools and call again."""
        return bool(self.message.tool_calls)

    def with_text(self, content: str) -> ChatResponse:
        """Copy with replaced text, for post-processing steps."""
        return replace(self, message=replace(self.message, content=content))


@runtime_checkable
class LLMClient(Protocol):
    """The only model interface the rest of this library knows about.

    A ``Protocol`` rather than a base class so that a test double is just an
    object with a ``chat`` method -- no imports, no inheritance, no mocking
    framework. See ``tests/conftest.py`` for how small a fake can be.
    """

    provider: str

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
        """Send a conversation and get one response.

        Args:
            messages: Conversation so far. A ``system`` role message here is
                accepted and routed correctly per provider, but prefer the
                ``system`` argument -- it is unambiguous.
            model: Model id; defaults to the provider's workhorse model.
            tools: Tools the model may call this turn.
            system: System prompt.
            temperature: ``None`` leaves the provider default alone.
            max_tokens: Ceiling on the response.

        Returns:
            The normalised response.

        Raises:
            ProviderError: The provider rejected the call or sent something
                this adapter could not read.
        """
        ...


def split_system(messages: list[Message]) -> tuple[str | None, list[Message]]:
    """Pull ``system`` messages out of a conversation.

    Anthropic and Google take the system prompt as a separate argument, OpenAI
    takes it as a message. Rather than make callers remember which, every
    adapter calls this and handles the result its own way. Multiple system
    messages are joined, which is what callers almost always mean.
    """
    system_parts = [m.content for m in messages if m.role == "system" and m.content]
    rest = [m for m in messages if m.role != "system"]
    return ("\n\n".join(system_parts) or None), rest
