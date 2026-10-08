---
title: Routing
description: Classify the input, then send it to the handler that fits.
---

# Routing

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 05. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 05**.*

## What this page will cover

- The economics: one cheap classification call to avoid sending every case to your most expensive model
- Writing route descriptions as *conditions*, not handler summaries -- the classifier reads these as its decision criteria
- Confidence thresholds and the default route: what happens when the classifier is unsure
- Routing to models vs routing to prompts vs routing to whole subsystems
- Measuring a router: accuracy per route, plus the cost of a misroute (asymmetric -- sending an easy case to the big model costs money, the reverse costs trust)
- When routing replaces an agent entirely: `agentic_ai.patterns.routing`

## Sources

- Anthropic, *Building Effective Agents* -- routing workflow
- OpenAI, *A Practical Guide to Building Agents* -- triage and handoffs

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
