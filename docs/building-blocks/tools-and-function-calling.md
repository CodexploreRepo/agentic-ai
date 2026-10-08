---
title: Tools and function calling
description: How a model asks for work to be done.
---

# Tools and function calling

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 03. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 03**.*

## What this page will cover

- The wire protocol: schema in, tool-call request out, result back as a message
- Deriving schemas from type hints -- what `agentic_ai.tools.tool` does and why hand-written schemas drift
- Required vs optional arguments, enums, and nested objects (and why deep nesting hurts selection accuracy)
- Idempotency and retries: the model will call your tool twice
- Returning errors the model can act on, versus errors it can only apologise for
- Permissions per tool, and why read and write tools deserve different gates

## Sources

- Anthropic and OpenAI tool-use documentation
- Koenigstein, *AI Agents* -- ch. 5

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
