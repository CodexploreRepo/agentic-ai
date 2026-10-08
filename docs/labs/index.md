---
title: Labs
description: Runnable notebooks, one per module — each one measures the pattern it teaches.
sidebar_label: Overview
---

# Labs

One notebook per module, in
[`labs/`](https://github.com/CodexploreRepo/agentic-ai/tree/main/labs). Each
lab does three things in order: **use** the pattern, **measure** it, then
**break** it on purpose.

The third part is deliberate. Reading that a step limit prevents runaway loops
is forgettable. Removing the step limit, watching the budget guard fire, and
seeing what it cost is not.

## The ground rule

A lab **never defines a pattern**. It imports from
[`agentic_ai`](https://github.com/CodexploreRepo/agentic-ai/tree/main/src/agentic_ai)
and shows the pattern being used.

That rule is why this repo should still work in two years. A pattern defined
inside a notebook cannot be tested, reused, or fixed in one place — and every
course repository built that way rots into a folder of cells that no longer
run.

## Available now

| Lab | Module | What you build | Cost |
|---|---|---|---|
| [01 — Your first agentic workflow](https://github.com/CodexploreRepo/agentic-ai/blob/main/labs/01-foundations/01_first_agentic_workflow.ipynb) | [01](/modules/01-foundations/) | A video research brief agent, versus the single prompt it must beat | a few cents |

Labs 02–09 land with their modules.

## Running a lab

```bash
make setup       # once
make lab-01      # opens the notebook with the right kernel
make eval-01     # runs its eval set, writes a scorecard
```

You need one model provider key and a Tavily key for the research labs. See
[setup](/start-here/setup).

## Cost control

Every lab prints what it spent. A
[`BudgetGuard`](/production/cost-and-latency) is active by default and raises
rather than warns:

```bash
AGENTIC_RUN_BUDGET_USD=1.00     # in your .env
```

Keep that default while learning. If a lab trips it, read the trace in
`.runs/` — a tripped budget almost always means a tool is failing in a way the
model keeps retrying, which is exactly the lesson.

## Reading a lab without running it

Rendered versions of each notebook, outputs included, are published to this
site under this section as modules ship. They are generated from the
notebooks by
[`tools/nb2md.py`](https://github.com/CodexploreRepo/agentic-ai/blob/main/tools/nb2md.py),
so they cannot drift from the code.
