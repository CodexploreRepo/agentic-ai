---
title: Glossary
description: The vocabulary of agentic AI, defined precisely and without hype.
---

# Glossary

:::note[Reference page]
Written and reviewed. Covered in [Module 01](/modules/01-foundations/).
:::

Terms as this repo uses them. Where the industry uses a word loosely, that is
noted rather than smoothed over.

### Agent

A system where the **model chooses the control flow** — which steps to take,
in what order, how many times. Contrast with a workflow, where you chose.
See [what is an agent](/foundations/what-is-an-agent).

### Agentic

The useful adjective. A system is agentic *in degree* and *in places*, rather
than being an agent or not. Prefer "how agentic is this, and where?" to "is
this an agent?".

### Agent loop

The cycle of model decision, tool execution, observation, repeat, until the
model stops requesting tools or a limit is hit. The irreducible core of every
agent. See [tool use](/patterns/tool-use).

### Agent Skills

A packaging format for reusable agent capabilities — instructions, scripts and
resources that an agent loads when relevant. Complementary to MCP: skills
package *know-how*, MCP connects to *systems*.

### Context engineering

Deciding what goes into the model's context window at each step, treated as a
budgeting problem. Broader than prompt engineering, which is about wording.
See [context engineering](/building-blocks/context-engineering).

### Context window

The maximum tokens a model can attend to at once. A constraint, not a feature —
a bigger window invites the mistake of filling it.

### Error analysis

Reading failing cases by hand, grouping them by cause, counting the groups, and
fixing the biggest. The highest-yield activity in an agent project. See
[error analysis](/evaluation/error-analysis).

### Eval / eval set

A list of inputs with expectations, used to measure whether a change helped.
See [eval-driven development](/evaluation/eval-driven-development).

### Function calling

See *tool use*. "Function calling" usually refers to the provider API
mechanism; "tool use" to the pattern. Used interchangeably in practice.

### Guardrail

A constraint that holds when the model misbehaves. The test of a real
guardrail: **the model cannot talk its way past it**, because it is enforced
outside the model. See [guardrails](/safety/guardrails).

### Hallucination

Confidently stated output unsupported by the model's inputs or the world. In
agents the sharper concern is *unfaithful* output — a claim not supported by
the tool results the agent actually retrieved, which is detectable.

### Human in the loop (HITL)

A person placed at a specific decision point: approving an action, resolving
ambiguity, or handling escalation. See [human in the loop](/patterns/human-in-the-loop).

### LLM-as-judge

Using a model to score another model's output against a rubric. Necessary for
open-ended output; prone to agreeableness, position bias and verbosity bias.
See [LLM as judge](/evaluation/llm-as-judge).

### MCP (Model Context Protocol)

An open protocol for connecting agents to external tools, resources and
prompts, so an integration is written once rather than per agent. See
[MCP](/building-blocks/mcp).

### Memory

Four distinct things share this name: message history, scratchpad, retrieved
context, and durable cross-run facts. "Add memory" is not a task until you say
which. See [memory and state](/building-blocks/memory-and-state).

### Multi-agent system

Several agents with narrower jobs, coordinating. The design decision is the
**communication pattern**, not the agent count. See
[multi-agent systems](/patterns/multi-agent).

### Planning

Producing an explicit plan artefact before acting, rather than deciding one
step at a time. Buys inspectability and approval gates; costs a call made on
less information. See [planning](/patterns/planning).

### Prompt caching

Provider-side reuse of a repeated context prefix, billed at a fraction of the
input rate. Makes stable prompt prefixes an architectural concern.

### Prompt chaining

Several model calls in an order **you** fixed, each with a narrower job.
A workflow, not an agent. See [prompt chaining](/patterns/prompt-chaining).

### Prompt injection

An attack where instructions hidden in content the agent reads are followed as
if they came from you. Indirect injection — via a fetched page, email or
document — is the form that matters for agents. See
[prompt injection](/safety/prompt-injection).

### ReAct

*Reason + Act.* Interleaving explicit reasoning with tool calls. Its main
contribution was making the reasoning step visible and inspectable; native tool
calling has absorbed most of the rest. See [ReAct](/patterns/react).

### Reflection

Having the system critique and revise its own output. Works in proportion to
the **critic's leverage** — a checklist, a stricter model, or ideally a real
signal like a test failure. See [reflection](/patterns/reflection).

### Routing

Classifying the input, then dispatching to the handler that fits. The cheapest
useful pattern, and the honest answer to many requests for "an agent". See
[routing](/patterns/routing).

### Span

One timed unit of work in a trace — a run, a step, a model call, a tool call.

### Step limit

A ceiling on model calls in one run. Prevents runaway loops. A run that hits it
is usually missing a tool, not short of steps.

### Structured output

Getting typed data back rather than prose, via JSON mode, schema enforcement,
or a tool call used as an output channel. See
[structured outputs](/building-blocks/structured-outputs).

### Tool

A function the agent can call. Two halves: the callable the runtime executes,
and the schema plus description **the model reads to decide when to use it**.
That description is prompt, not documentation.

### Tool use

The pattern where the model chooses which tools to call and with what
arguments. The level of autonomy most useful agents operate at. See
[tool use](/patterns/tool-use).

### Trace

An append-only record of what one run actually did, span by span. The only
artefact that makes an agent failure reproducible, because the output does not
reveal the path taken. See
[observability and tracing](/production/observability-and-tracing).

### Workflow

A system where **you** chose the control flow. Cheaper, more predictable and
easier to test than an agent, and frequently the right answer. See
[when not to use agents](/foundations/when-not-to-use-agents).

---

*See [attribution and originality policy](/references/attribution).*
