---
title: The autonomy spectrum
description: Five levels of agent autonomy, and how to choose the right one for a task.
---

# The autonomy spectrum

:::note[Reference page]
Written and reviewed. Covered in [Module 01](/modules/01-foundations/).
:::

"How agentic should this be?" is a design decision you make per task, not per
system. These five levels give it a vocabulary.

Think of each level as answering: **what does the model get to decide?**

## Level 0 — Scripted

The model fills in text. You decide everything else.

> Summarise this document into three bullets.

One call, fixed prompt, fixed output shape. No tools, no branching. Most
production LLM features are still this, and that is fine — it is cheap, fast,
and testable like any other function.

## Level 1 — Chained

The model runs several times in an order you fixed.

> Extract the claims, then check each against the source, then write the summary.

The model decides content at each stage; you decide the stages. Accuracy goes
up because each call has a narrower job. Cost and latency stay predictable
because the step count does not change. See
[prompt chaining](/patterns/prompt-chaining).

## Level 2 — Tool-using

The model chooses *which* tools to call and *with what arguments*. You still
bound the loop.

> Answer the question. You may search the web and fetch pages. At most ten steps.

This is where most useful agents live, and where this repo's
[agent loop](/patterns/tool-use) operates. The model's freedom is real but
fenced: a fixed tool set, a step ceiling, a spend ceiling.

**This is the level to default to.** It handles genuine variability while
keeping failure contained.

## Level 3 — Planning

The model decides the *structure* of the work, not just the next step: it
produces a plan, then executes it, possibly replanning.

> Here is the goal and a toolbox. Work out how to achieve it.

Now the step count, the order, and sometimes the subtasks themselves are the
model's. You gain the ability to handle tasks you did not anticipate. You lose
the ability to predict what will happen. See [planning](/patterns/planning).

## Level 4 — Self-directed

The agent sets its own goals, or persists across sessions pursuing standing
objectives, or modifies its own tools and instructions.

> Monitor this system. Fix what you can. Escalate what you cannot.

Genuinely useful in narrow, well-instrumented, reversible domains. Mostly
still a research frontier, and the level where the gap between a demo and
something you would leave running overnight is widest.

## Choosing a level

Do not pick by ambition. Pick by what the task's *variability* and *risk*
actually demand:

| Ask | If yes | If no |
|---|---|---|
| Does the sequence of steps genuinely vary between inputs? | Level 2+ | Level 0-1 |
| Can you enumerate the tools up front? | Level 2 is enough | Level 3 |
| Are mistakes reversible? | Higher autonomy is affordable | Stay low, add approval |
| Can you detect a bad outcome automatically? | Higher autonomy is affordable | Stay low |
| Is the cost per run bounded? | Higher autonomy is affordable | Add hard ceilings first |

The two rows about detection and reversibility matter more than the two about
capability. An agent operating where mistakes are silent and permanent is a
bad design at any level of model quality — see
[the risk framework](/safety/risk-framework).

## The direction to move in

Start at the lowest level that could possibly work. Build the
[eval set](/evaluation/eval-driven-development) first. Move up a level only
when the evals show the current level failing on cases you care about, and
you can point to *which* cases.

Teams that start at Level 3 because it sounds more impressive end up debugging
a system whose failures they cannot reproduce, using a model whose decisions
they never constrained. Teams that start at Level 0 and climb have a working
baseline at every step, and a measurement showing why each climb was worth it.

## Sources

- DeepLearning.AI, [*Agentic AI*](https://www.deeplearning.ai/courses/agentic-ai) — degrees of autonomy
- Anthropic, *Building Effective Agents* — workflows versus agents, and the case for simplicity
- Koenigstein, *AI Agents: The Definitive Guide*, ch. 2

---

*See [attribution and originality policy](/references/attribution).*
