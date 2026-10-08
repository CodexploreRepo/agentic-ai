---
title: Prompt injection
description: Why fetched content is an attacker's input channel.
---

# Prompt injection

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 09. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 09**.*

## What this page will cover

- The core problem: instructions and data share one channel, and the model cannot reliably tell them apart
- Direct vs indirect injection; the indirect case is the one that matters for agents
- The lethal trifecta: private data access, untrusted content, and an exfiltration path. Remove any one
- Mitigations that help: content marking, least privilege per tool, human approval on egress, output filtering
- Mitigations that do not solve it: asking the model nicely, prompt-level 'ignore injected instructions'
- Why `agentic_ai.tools.fetch` labels its output untrusted, and why that is a mitigation rather than a fix
- Designing so a successful injection is survivable

## Sources

- Simon Willison's writing on prompt injection and the lethal trifecta
- OWASP Top 10 for LLM Applications
- Koenigstein, *AI Agents* -- ch. 9

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
