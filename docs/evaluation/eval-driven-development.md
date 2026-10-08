---
title: Eval-driven development
description: Why the eval set comes before the agent, and how to build one in an hour.
---

# Eval-driven development

:::note[Reference page]
Written and reviewed. Covered in [Module 01](/modules/01-foundations/).
:::

This page sits early in the curriculum on purpose, before a single pattern.
That ordering is the most useful idea in agentic engineering and the one most
often learned too late.

## The problem it solves

An agent fails differently from normal software. Normal software throws an
exception at the line that broke. An agent returns a fluent, confident,
plausible answer, having called the wrong tool four times on the way. Nothing
crashes. Nothing logs an error.

So "did my change help?" cannot be answered by running it and looking. You
read three outputs, they seem fine, you ship, and the regression surfaces a
week later in a case you never tried.

An eval set is the answer, and it is less work than it sounds.

## What an eval set is

A list of inputs with expectations. That is all:

```yaml
name: video-briefs
cases:
  - id: vb-01
    input: "Explain the Model Context Protocol for a backend developer"
    expect_contains: ["Model Context Protocol"]
    rubric: >
      States what problem MCP solves, names at least two of its primitives,
      and cites at least one source URL.
    tags: [definition, current]
```

Ten of those is a working eval set. Not a hundred — **ten real cases beat a
hundred invented ones**, because invented cases encode what you *think* breaks.

## Where the cases come from

In order of value:

1. **Real failures.** Something went wrong; it becomes case 1. This is the
   best source and the reason to start collecting from day one.
2. **Cases you are nervous about.** The topic with no good sources. The
   ambiguous request. The input that is 50 words of context and one question.
3. **The boring middle.** A few cases that should obviously work, so you notice
   when a change for the hard cases breaks the easy ones. It happens constantly.

What not to do: generate a hundred cases with a model and call it an eval set.
You get a measurement of how well your system handles synthetic input.

## Three kinds of check, in this order

**Deterministic checks** are free, instant, and never wrong about what they
measure. Run them always: required substrings, forbidden phrases, valid JSON,
non-empty output, at least two distinct cited URLs.

```python
expect_contains: ["Model Context Protocol"]
expect_absent: ["As an AI language model"]
```

Crude, and they catch more than you would guess. The `non_empty` check alone
catches the truncated fragment an agent returns when it hits its step limit —
a failure that otherwise scores as "no violations" and passes.

**[LLM-as-judge](/evaluation/llm-as-judge)** for the part that genuinely needs
reading: is this brief useful, is this claim supported by the source. Use a
rubric, require the judge to list problems *before* scoring, and use your
strongest model — a judge weaker than the system it grades produces numbers
you cannot act on.

**Human review** on a sample, to check the judge agrees with you. Skip this
and your judge's bias becomes your metric.

## The loop

```
write 10 cases  ->  build the simplest thing  ->  run evals  ->
read the failures  ->  fix the biggest group  ->  run evals  ->  ...
```

Two parts matter more than the rest.

**Build the simplest thing first.** A single prompt. It is your baseline, and
it is how you find out whether the agent you were about to build is actually
better. Sometimes it is not, and finding that out in an hour rather than a
fortnight is the entire return on this practice.

**Read the failures.** Not the score — the actual failing outputs, twenty of
them, by hand. Group them. Count the groups. The biggest group is what you fix
next. This is [error analysis](/evaluation/error-analysis), it is unglamorous,
and it remains the highest-yield hour in an agent project.

## In this repo

The harness lives in [`agentic_ai.evals`](https://github.com/CodexploreRepo/agentic-ai/blob/main/src/agentic_ai/evals/):

```python
from agentic_ai.evals import EvalDataset, evaluate, compare

dataset = EvalDataset.from_yaml("labs/01-foundations/evals/video_brief_cases.yaml")

baseline = evaluate(single_prompt, dataset, system_name="single-prompt")
agentic  = evaluate(research_agent, dataset, system_name="agentic")

print(compare(baseline, agentic))
```

`evaluate` takes any callable from string to string, which is deliberate: the
same harness scores a single prompt, an agent loop, a reflection chain or a
multi-agent team, so comparisons between them are apples to apples. That is
the only honest way to claim an agentic workflow beat one big prompt, and it is
exactly what [Lab 01](/labs/) does.

## Two numbers, and a warning about both

`pass_rate` is the headline: the fraction of cases passing every check.
`mean_score` is softer and worth watching alongside it — a change that moves
mean score without moving pass rate is making failures *less bad*, which is
progress you would otherwise not see.

The warning: **on ten cases, a one-case swing is noise.** Ten percentage
points looks like a result and is not. `compare()` deliberately refuses to
call differences within about one case, because the fastest way to waste a week
is chasing a number that moved because of sampling.

## Commit the scorecard

Write the result to Markdown and commit it next to the code:

```python
from agentic_ai.evals import write_scorecard
write_scorecard(agentic, "labs/01-foundations/evals/agentic.scorecard.md")
```

Now a prompt change arrives in a pull request with the number it moved, the
case ids that changed, and what it cost. "I think it got better" becomes a
diff.

## Sources

- DeepLearning.AI, [*Agentic AI*](https://www.deeplearning.ai/courses/agentic-ai) — evaluation-driven development and error analysis as the central development loop
- Huyen, *AI Engineering* — evaluation methodology and agent failure modes
- Koenigstein, *AI Agents: The Definitive Guide*, ch. 7

---

*See [attribution and originality policy](/references/attribution).*
