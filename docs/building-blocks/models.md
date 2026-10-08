---
title: Choosing a model
description: Capability, latency and cost are one decision, not three.
---

# Choosing a model

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 04. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 04**.*

## What this page will cover

- Tiering within one system: a cheap model for routing and extraction, a strong one for planning and judging
- What actually differs between tiers for agents: tool-selection accuracy and instruction adherence, more than raw knowledge
- Reasoning effort / thinking budgets and when they pay for themselves
- Context window as a design constraint, not a feature -- a bigger window invites the mistake of filling it
- Measuring substitution: swap the model, re-run the eval set, compare cost and pass rate (this repo's adapter layer exists to make that a one-line change)
- Model IDs and prices live in `agentic_ai/models.py`

## Sources

- Koenigstein, *AI Agents* -- ch. 4, The Models Behind the Agents
- Huyen, *AI Engineering* -- model selection

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
