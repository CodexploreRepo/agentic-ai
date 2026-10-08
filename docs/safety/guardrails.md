---
title: Guardrails
description: Constraints that hold when the model misbehaves.
---

# Guardrails

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 09. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 09**.*

## What this page will cover

- Input, output and action guardrails -- three different placements, three different jobs
- Deterministic guardrails first: allowlists, schema validation, spend ceilings, rate limits
- Model-based guardrails (classifiers, judges) and their false-positive cost
- The design principle: a guardrail the model can talk its way past is not a guardrail. Enforce outside the model
- Failing closed vs failing open, chosen per action rather than globally
- Logging every guardrail trigger -- they are your best source of eval cases

## Sources

- OpenAI, *A Practical Guide to Building Agents* -- guardrails
- Koenigstein, *AI Agents* -- ch. 9

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
