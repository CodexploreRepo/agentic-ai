---
title: Reflection
description: Make the system critique and revise its own output.
---

# Reflection

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 02. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 02**.*

## What this page will cover

- Generator and critic as separate roles, even when they are the same model
- Where critic leverage comes from: a checklist, a stricter model, a different persona -- or a real signal
- External feedback beats self-critique: a linter, a test run, a SQL error, a failing assertion
- Stopping: critic-driven exit vs fixed rounds, and why fixed rounds spend money making drafts different rather than better
- Measuring it: does round 2 actually beat round 1 on your eval set? Often it does not
- Cost model: reflection roughly doubles or triples spend per task. Earn it
- Code: `agentic_ai.patterns.reflection`

## Sources

- Shinn et al., *Reflexion* (arXiv:2303.11366)
- Madaan et al., *Self-Refine* (arXiv:2303.17651)
- Anthropic, *Building Effective Agents* -- evaluator-optimizer loop

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
