"""Multi-agent systems: several agents, each with a narrower job.

Worth being sceptical here. Multiple agents genuinely help when subtasks need
different tools, different permissions, or different context -- a researcher
that may browse the web and a writer that may not, say. They help much less
when the real problem is one agent with a muddled prompt, and splitting it adds
latency, cost, and a new failure mode: agents that agree with each other
confidently and wrongly.

The useful question is what the agents are allowed to say to each other.
Supervisor-and-workers, a shared scratchpad, and a free-for-all debate produce
very different systems, and the communication pattern -- not the agent count --
is what determines whether the thing works.

Built in Module 05.

Planned interface::

    class Agent: ...                     # role, system prompt, toolbox, model
    run_supervisor(agents, task, ...) -> TeamResult
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import NoReturn

from agentic_ai.llm.base import Usage
from agentic_ai.tools.registry import Toolbox


@dataclass
class Agent:
    """One named participant with its own brief and tools."""

    name: str
    system: str
    toolbox: Toolbox = field(default_factory=Toolbox)
    model: str | None = None
    #: Ceiling on this agent's own loop, independent of the team's budget.
    max_steps: int = 8


@dataclass
class TeamResult:
    """What a team produced, and the transcript of how they got there."""

    output: str
    transcript: list[tuple[str, str]] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)
    cost_usd: float = 0.0


def run_supervisor(*args: object, **kwargs: object) -> NoReturn:
    """Not implemented yet -- built in Module 05.

    Raises:
        NotImplementedError: Always. See docs/patterns/multi-agent.md.
    """
    raise NotImplementedError(
        "run_supervisor() is built in Module 05. See docs/patterns/multi-agent.md."
    )
