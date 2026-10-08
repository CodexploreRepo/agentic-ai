---
title: Component vs end-to-end evals
description: Two questions that need two kinds of test.
---

# Component vs end-to-end evals

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 04. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 04**.*

## What this page will cover

- End-to-end evals answer 'is the product good?'; component evals answer 'which part is bad?'
- You need both, and they fail differently: end-to-end tests are realistic but uninformative, component tests are informative but can all pass while the product is broken
- Picking component boundaries: retrieval, tool selection, argument construction, synthesis
- Tool-selection accuracy as the single most useful component metric for agents
- Trace-based evaluation: scoring the path, not just the answer
- Cost discipline -- component evals are cheap enough to run on every commit, end-to-end evals usually are not

## Sources

- Koenigstein, *AI Agents* -- ch. 7, Benchmarking LLMs and Agentic Systems
- DeepLearning.AI *Agentic AI* -- component-level evals

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
