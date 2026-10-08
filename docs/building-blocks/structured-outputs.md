---
title: Structured outputs
description: Getting data back, not prose.
---

# Structured outputs

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 03. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 03**.*

## What this page will cover

- Three mechanisms: JSON mode, constrained decoding / schema enforcement, and a tool call used as an output channel
- Pydantic models as the single source of truth for a schema
- Validation at the boundary, and what to do on a validation failure (retry with the error is usually right)
- Why structured output reduces downstream parsing bugs more than it improves model accuracy
- Cost: schema constraints can reduce answer quality on genuinely open-ended tasks

## Sources

- Provider structured-output documentation
- Huyen, *AI Engineering* -- structured outputs

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
