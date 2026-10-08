---
title: Cost and latency
description: The two numbers that decide whether you ship.
---

# Cost and latency

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 04. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 04**.*

## What this page will cover

- Cost per *successful* task is the only cost metric worth tracking -- per-token cost hides retries
- Where the money actually goes: re-sending the whole history every step, and judge calls in evals
- Prompt caching: stable prefixes, what invalidates them, and realistic savings
- Model tiering and early exit
- Latency: steps are serial and each is a round trip. Parallel tool calls, speculative execution, streaming for perceived latency
- Budget guards as a correctness feature -- `agentic_ai.llm.cost.BudgetGuard`

## Sources

- Provider pricing and caching documentation
- Koenigstein, *AI Agents* -- ch. 6

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
