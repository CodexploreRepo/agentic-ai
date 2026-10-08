---
title: Task decomposition
description: Turning a vague job into steps you can build, measure and fix.
---

# Task decomposition

:::note[Reference page]
Written and reviewed. Covered in [Module 01](/modules/01-foundations/).
:::

Before you choose a pattern, you have to know what the work actually is.
Decomposition is that step, and it is doing two jobs at once: finding the steps
an agent will take, and finding **the places you can measure**.

The second job is the one people skip, and it is the reason their agent is
unimprovable later.

## Start from how a person would do it

The most reliable decomposition technique is to describe how a competent human
would do the task, out loud, in order. For "produce a research brief on a
topic":

1. Work out what questions the brief needs to answer
2. Search for each one
3. Skim results; open the promising ones properly
4. Notice what is still missing and search again
5. Write it up, with sources
6. Check the write-up is actually supported by what was found

Six steps. Now look at what they tell you.

## Read the decomposition for design decisions

**Step 4 is a loop, and its length depends on the topic.** That single
observation is what makes this task a candidate for an agent rather than a
pipeline — the variability is real, not imagined. Had every step been
fixed-length, [a chain](/patterns/prompt-chaining) would be the right answer.

**Steps 2 and 3 need tools.** Search and fetch. That is your toolbox, and it
came from the decomposition rather than from guessing.

**Step 6 is a critic.** A separate check on the output of step 5, with a
different job. That is [reflection](/patterns/reflection), and noticing it now
tells you where it would slot in later.

**Steps 1 and 6 are measurable in isolation.** You can judge a question list
without doing the research, and judge whether a brief is supported by its
sources without rewriting it. Those are your
[component evals](/evaluation/component-vs-end-to-end).

## Write the failure modes down too

For each step, ask what going wrong looks like. This takes ten minutes and
saves days:

| Step | Failure | Detectable? |
|---|---|---|
| Generate questions | Too broad, or misses the obvious one | Yes — read the list |
| Search | Bad query, no useful results | Yes — empty or off-topic results |
| Fetch | Page is paywalled or JS-only | Yes — short or empty text |
| Decide to continue | Stops too early; loops forever | Yes — step count |
| Write up | Fluent but unsupported by sources | **Hard** — needs a judge |
| Self-check | Approves its own bad work | **Hard** — needs ground truth |

The two hard rows are where your evaluation effort belongs. The easy rows
become cheap deterministic checks you write once and never think about again.

This table is also the first draft of your eval set: each row is a case you
should deliberately include.

## Granularity: how fine is too fine

Decompose until each step has **one job and one obvious failure mode**, then
stop.

- *Too coarse:* "research the topic" — you cannot tell which part broke
- *Too fine:* "lowercase the query string" — now you are writing the program,
  not designing it

A good test: can you describe a step's output well enough to judge it without
seeing the input? If not, the step is doing more than one thing.

## Decomposition is not the architecture

A common mistake is to assume each step becomes a component — six steps, six
model calls, perhaps six agents. It does not follow. Decomposition tells you
what the work is; architecture is a separate decision about who does it.

Our six steps could be:

- **One model call** — all six described in a prompt. The Module 01 baseline.
- **A chain** — three or four calls in fixed order, skipping the loop.
- **One agent loop** — the model does 1-6 itself with two tools. What Module 01 builds.
- **A plan-and-execute agent** — the model plans the questions, then works through them.
- **A team** — a researcher and a writer with different tools.

All five are defensible. The decomposition is the same in every case, which is
exactly why it is worth doing before you pick. And because you now have a
decomposition, you can [compare them on the same eval set](/evaluation/eval-driven-development)
rather than arguing about them.

## The practical sequence

1. Describe how a person would do it, step by step
2. Mark which steps vary in length — that is where agency may be needed
3. Mark which steps need tools — that is your toolbox
4. Write each step's failure mode and whether it is cheaply detectable
5. Turn the detectable ones into checks, and the undetectable ones into eval cases
6. *Then* choose an architecture, and measure it against the simplest alternative

Step 6 comes last. That ordering is the whole point.

## Sources

- DeepLearning.AI, [*Agentic AI*](https://www.deeplearning.ai/courses/agentic-ai) — task decomposition and identifying workflow steps
- Anthropic, *Building Effective Agents* — decomposition as the route to accuracy
- Koenigstein, *AI Agents: The Definitive Guide*, ch. 2-3

---

*See [attribution and originality policy](/references/attribution).*
