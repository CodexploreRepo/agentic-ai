---
title: Planning
description: Decide the steps before taking them.
---

# Planning

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 05. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 05**.*

## What this page will cover

- Implicit planning (the agent loop) vs explicit planning (a plan artefact you can inspect)
- What a plan buys you: approval gates, cost estimates, parallelism, and a user-visible 'here is what I am about to do'
- What it costs: a model call made on less information than the executor will have
- Replanning triggers: step failure, new information, budget pressure -- and the danger of replanning on every step
- Dependency graphs and parallel execution
- Tree search over plans (LATS) and why it is rarely worth it outside benchmarks
- Code: `agentic_ai.patterns.planning`

## Sources

- Zhou et al., *Language Agent Tree Search* (arXiv:2310.04406)
- Koenigstein, *AI Agents* -- ch. 3, Advanced Planning, Reasoning, and Scalable Execution
- Gulli, *Agentic Design Patterns* -- planning patterns

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
