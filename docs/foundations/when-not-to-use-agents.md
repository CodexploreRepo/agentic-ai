---
title: When not to use agents
description: The cases where an agent is the wrong tool, and what to build instead.
---

# When not to use agents

:::note[Reference page]
Written and reviewed. Covered in [Module 01](/modules/01-foundations/).
:::

A curriculum about agents has an obvious bias, so this page exists to push
back. Most tasks people reach for an agent to solve are better solved
otherwise, and recognising those cases quickly is a more valuable skill than
any pattern in this repo.

## The steps never vary

If you can write the sequence down and it is the same every time, write it
down. A three-stage pipeline is cheaper, faster, easier to test, and will not
surprise you at 2am.

> **Signal:** you find yourself writing a system prompt that enumerates the
> steps in order. You have just written a workflow in English rather than in
> Python. Write it in Python.

**Build instead:** [prompt chaining](/patterns/prompt-chaining).

## The task is really classification

"Work out which of five things the user wants, then do that thing" is a router
plus five straight-line handlers. It will beat an agent on cost, latency and
debuggability, and you can measure its accuracy directly.

**Build instead:** [routing](/patterns/routing).

## Mistakes are silent and permanent

Autonomy is affordable in proportion to how easily you can **detect** and
**undo** a bad outcome. An agent acting where you can do neither is a bad
design regardless of how good the model is.

Payments, deletions, outbound communication, anything legally binding: either
add an approval gate, or make the action reversible first, or do not automate
the decision.

**Build instead:** [human in the loop](/patterns/human-in-the-loop) and
[the risk framework](/safety/risk-framework).

## You cannot define success

This is the one that quietly kills projects. If you cannot write ten test cases
with expected outcomes, you cannot tell whether a change helped, which means
you cannot improve the system — you can only change it and hope.

That is not an argument for a different architecture. It is an argument for
stopping and defining success first.

**Build instead:** an [eval set](/evaluation/eval-driven-development). Then
decide the architecture.

## Latency or cost is hard-capped

An agent's step count varies by input, so its cost and latency are
distributions, not numbers. If the requirement is "under 500ms" or "under a
tenth of a cent", an agentic loop will not meet it reliably, and the tail is
what will hurt you.

**Build instead:** a single call to a cheaper model, with a fallback path for
the cases it cannot handle.

## A deterministic solution exists

If a SQL query, a regular expression, or an API call answers the question
exactly, use it. Wrapping a solved problem in a model adds cost, latency, and
a new failure mode, in exchange for nothing.

The useful version of this: let the model *write* the SQL once, review it, then
ship the SQL.

## The honest summary

Agents earn their complexity when **the path genuinely varies and you can tell
whether the outcome was good.** Both halves are required. Variability without
measurability gives you an unmaintainable system; measurability without
variability means you should have written a workflow.

Everything else in this repo assumes you have checked both.

## Sources

- Anthropic, *Building Effective Agents* — "find the simplest solution possible, and only increase complexity when needed"
- DeepLearning.AI, [*Agentic AI*](https://www.deeplearning.ai/courses/agentic-ai) — identifying tasks suited to agentic implementation
- Koenigstein, *AI Agents: The Definitive Guide*, ch. 2

---

*See [attribution and originality policy](/references/attribution).*
