---
title: What is an agent?
description: The difference between a workflow and an agent, and why the distinction is about control rather than intelligence.
---

# What is an agent?

:::note[Reference page]
Written and reviewed. Covered in [Module 01](/modules/01-foundations/).
:::

The word "agent" is used for everything from a chatbot with a search box to a
system that opens pull requests unsupervised. That range makes the term almost
useless in conversation and actively dangerous in design reviews, because two
people can agree to "build an agent" and mean systems with completely
different failure modes.

Here is the distinction that has held up in practice:

> **A workflow follows a path you decided. An agent decides its own path.**

Not "an agent is smarter". Not "an agent uses tools" — workflows use tools
constantly. The question is **who chooses the control flow**: you, in code, at
development time; or the model, at runtime.

## The same task, both ways

Take a concrete job: *produce a research brief on a topic*.

**As a workflow**, you decide the steps:

```python
def research_brief(topic: str) -> str:
    questions = generate_questions(topic)        # you chose: 1 model call
    results = [search(q) for q in questions]     # you chose: one search each
    return synthesise(topic, results)            # you chose: 1 model call
```

Three stages, in that order, every time. If the topic needs six searches, it
gets one per question anyway. If the first search answers everything, it still
runs the rest.

**As an agent**, you decide the *goal and the means*, and the model decides the
sequence:

```python
run_agent(
    f"Produce a research brief on: {topic}",
    toolbox=Toolbox(search_web, fetch_page),
    system="Research thoroughly, cite sources, stop when you can answer well.",
)
```

Now the model chooses how many searches to run, whether to fetch a full page
after a promising snippet, and when it has enough. Three searches for an easy
topic, nine and two page fetches for a hard one.

## What you trade

That flexibility is not free, and the trade is the whole decision:

| | Workflow | Agent |
|---|---|---|
| **Control flow** | Fixed, written by you | Chosen by the model per run |
| **Cost** | Predictable | Varies, sometimes wildly |
| **Latency** | Predictable | Varies with step count |
| **Debugging** | Read the code | Read the trace |
| **Handles the unexpected** | No — unhandled cases fall through | Often, which is the point |
| **Fails** | Visibly, in one place | Quietly, by taking a bad path |

That last row is the one that surprises people. A broken workflow throws an
exception. A broken agent returns a fluent, confident, wrong answer, having
called the wrong tool four times on the way. Nothing crashes. This is why
[evaluation](/evaluation/eval-driven-development) is not an optional later
step in agentic work — without it you have no way to know which of those two
things just happened.

## It is a spectrum, not a binary

Real systems sit between the extremes, and most good ones sit closer to the
workflow end than their authors expected. A fixed three-stage pipeline where
stage two is a model deciding which of four tools to call is mostly a workflow
with a pinch of agency — and that is frequently the right design.

The [autonomy spectrum](/foundations/autonomy-spectrum) makes this precise.
The practical habit it encourages: **give away only as much control as the task
actually requires.** Every degree of autonomy you hand over buys adaptability
and costs predictability, and the second one is what you will be asked about
when something goes wrong in production.

## "Agentic" as the useful adjective

This is why the field has largely settled on *agentic* rather than *agent*.
"Is it an agent?" invites a yes/no argument about a word. "How agentic is it,
and where?" invites a design discussion: which decisions does the model make,
which do we make, and can we defend each choice?

A system can be agentic in one place and rigidly scripted everywhere else.
That is usually the shape you want.

## What comes next

- [Anatomy of an agent](/foundations/anatomy-of-an-agent) — the five parts every agentic system has
- [The autonomy spectrum](/foundations/autonomy-spectrum) — how much control to hand over
- [When not to use agents](/foundations/when-not-to-use-agents) — the cases where this is the wrong tool
- [Task decomposition](/foundations/task-decomposition) — turning a job into steps you can evaluate

## Sources

- DeepLearning.AI, [*Agentic AI*](https://www.deeplearning.ai/courses/agentic-ai) — the autonomy framing and the "agentic" adjective
- Anthropic, *Building Effective Agents* — the workflow/agent distinction as a control-flow question
- Koenigstein, *AI Agents: The Definitive Guide*, ch. 1-2

---

*See [attribution and originality policy](/references/attribution).*
