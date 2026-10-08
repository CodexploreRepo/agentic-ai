---
title: LLM as judge
description: Using a model to score outputs, without fooling yourself.
---

# LLM as judge

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 04. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 04**.*

## What this page will cover

- When a judge is appropriate: open-ended output, no reference answer, criteria a person could state
- When it is not: anything a deterministic check can decide, and anything the judge model is worse at than the system
- Agreeableness as the default failure. Rubrics, forced issue-listing before scoring, and low temperature
- Position and verbosity bias in pairwise comparison, and how to control for them
- Validating the judge against human labels on a sample -- the step that makes the numbers mean anything
- Cost: a judge call per case per run adds up fast. Budget it explicitly
- `agentic_ai.evals.judges.judge_with_rubric`

## Sources

- Zheng et al., *Judging LLM-as-a-Judge* (arXiv:2306.05685)
- Huyen, *AI Engineering* -- AI as a judge

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
