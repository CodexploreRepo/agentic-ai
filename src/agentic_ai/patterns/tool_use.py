"""The agent loop.

This is the smallest thing that deserves to be called an agent: a model, some
tools, and a loop that keeps going until the model stops asking for tools.

    think -> call tools -> observe results -> think again -> ... -> answer

Everything else in this repo is a variation on it. Reflection runs it twice
with a critic in between. Planning puts a decomposition step in front. A
multi-agent system is several of these with a message bus. Which is why it is
worth reading this file end to end once: about eighty lines of control flow
sits underneath every framework you will ever evaluate.

Three details in here are the ones that bite people in production, and all
three are choices rather than defaults:

1. **A step limit.** Without one, a tool the model cannot satisfy produces an
   infinite loop that bills you the whole way.
2. **Tool errors go back to the model as text.** A model told *why* its call
   failed usually fixes it next turn. A model handed an exception sees nothing.
3. **The loop records what it did.** The final answer does not reveal that the
   agent searched four times and gave up; the trace does.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

from agentic_ai.errors import MaxStepsExceeded
from agentic_ai.llm.base import ChatResponse, LLMClient, Message, Usage
from agentic_ai.llm.cost import BudgetGuard
from agentic_ai.llm.registry import get_client
from agentic_ai.obs.trace import Trace
from agentic_ai.tools.registry import Toolbox

StopReason = Literal["finished", "max_steps", "stop_condition"]

DEFAULT_MAX_STEPS = 10


@dataclass
class AgentResult:
    """Everything one agent run produced -- answer and evidence both.

    The answer alone is not enough to evaluate a run, which is why ``steps``,
    ``messages`` and ``trace`` come back with it. Module 04 builds error
    analysis on exactly these fields.
    """

    output: str
    messages: list[Message]
    steps: int
    stopped_because: StopReason
    usage: Usage = field(default_factory=Usage)
    cost_usd: float = 0.0
    tool_calls_made: tuple[str, ...] = ()
    trace: Trace | None = None

    @property
    def succeeded(self) -> bool:
        """Whether the loop ended because the model was done.

        Check this. A run that hit its step limit still returns text, and that
        text is the model's last unfinished thought rather than an answer.
        """
        return self.stopped_because == "finished"

    def summary(self) -> str:
        """One line for printing at the end of a lab."""
        tools = f", {len(self.tool_calls_made)} tool calls" if self.tool_calls_made else ""
        return (
            f"{self.stopped_because} after {self.steps} step"
            f"{'s' if self.steps != 1 else ''}{tools} · "
            f"{self.usage.total_tokens:,} tokens · ~${self.cost_usd:.4f}"
        )


def run_agent(
    task: str,
    *,
    client: LLMClient | None = None,
    model: str | None = None,
    system: str | None = None,
    toolbox: Toolbox | None = None,
    max_steps: int = DEFAULT_MAX_STEPS,
    temperature: float | None = None,
    budget: BudgetGuard | None = None,
    trace: Trace | None = None,
    on_step: Callable[[int, ChatResponse], None] | None = None,
    stop_when: Callable[[ChatResponse], bool] | None = None,
    raise_on_max_steps: bool = False,
) -> AgentResult:
    """Run the think-act-observe loop until the model stops asking for tools.

    Args:
        task: What the agent should do, as the first user message.
        client: Model client; defaults to the configured provider.
        model: Model id; defaults to the provider's workhorse model.
        system: System prompt. This is where the agent's role, constraints and
            stopping criteria belong.
        toolbox: Tools available. With no toolbox this degenerates to a single
            model call, which is a useful baseline to measure against.
        max_steps: Ceiling on model calls. A loop that needs more than ten is
            usually missing a tool rather than steps.
        temperature: ``None`` keeps the provider default.
        budget: Spend guard. One is created from settings if omitted, so a
            runaway loop stops rather than bills.
        trace: Trace to record into. One is created if omitted.
        on_step: Called after each model response -- useful in a notebook to
            show progress instead of staring at a blank cell.
        stop_when: Extra stop condition checked after each response. Return
            ``True`` to end the run early.
        raise_on_max_steps: Raise instead of returning a partial result.
            ``False`` suits exploration; ``True`` suits production, where a
            truncated answer is worse than a failure you can see.

    Returns:
        The answer plus the evidence needed to evaluate it.

    Raises:
        MaxStepsExceeded: Step limit hit and ``raise_on_max_steps`` is set.
        BudgetExceeded: The run crossed its USD ceiling.
    """
    client = client or get_client()
    toolbox = toolbox if toolbox is not None else Toolbox()
    budget = budget or BudgetGuard.from_settings()
    owns_trace = trace is None
    trace = trace or Trace("agent")

    messages: list[Message] = [Message.user(task)]
    tool_calls_made: list[str] = []
    steps = 0
    output = ""
    stopped_because: StopReason = "max_steps"

    try:
        with trace.span("agent", kind="run", task=task[:200], max_steps=max_steps):
            while steps < max_steps:
                steps += 1

                with trace.span(f"step-{steps}", kind="llm", tools=len(toolbox)) as span:
                    response = client.chat(
                        messages,
                        model=model,
                        tools=toolbox.specs or None,
                        system=system,
                        temperature=temperature,
                    )
                    span.attributes["model"] = response.model
                    span.attributes["tokens"] = response.usage.total_tokens
                    span.attributes["stop_reason"] = response.stop_reason
                    budget.record(response.usage, response.model)

                messages.append(response.message)
                if on_step is not None:
                    on_step(steps, response)

                if stop_when is not None and stop_when(response):
                    output = response.text
                    stopped_because = "stop_condition"
                    break

                if not response.wants_tools:
                    # No tool requested means the model considers itself done.
                    output = response.text
                    stopped_because = "finished"
                    break

                for call in response.tool_calls:
                    tool_calls_made.append(call.name)
                    with trace.span(call.name, kind="tool", arguments=call.arguments) as span:
                        result = toolbox.dispatch(call)
                        span.attributes["result_chars"] = len(result)
                        # dispatch() returns errors as text rather than
                        # raising, so flag them for the trace reader.
                        span.attributes["looks_like_error"] = result.startswith("Error:")
                    messages.append(Message.tool_result(call.id, result))
            else:
                # Loop exhausted: keep the last assistant text, but the caller
                # must be able to tell it apart from a real answer.
                output = next(
                    (m.content for m in reversed(messages) if m.role == "assistant" and m.content),
                    "",
                )
                if raise_on_max_steps:
                    raise MaxStepsExceeded(max_steps)
    finally:
        if owns_trace:
            trace.flush()

    return AgentResult(
        output=output,
        messages=messages,
        steps=steps,
        stopped_because=stopped_because,
        usage=budget.usage,
        cost_usd=budget.spent_usd,
        tool_calls_made=tuple(tool_calls_made),
        trace=trace,
    )
