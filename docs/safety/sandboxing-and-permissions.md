---
title: Sandboxing and permissions
description: What the agent is allowed to touch.
---

# Sandboxing and permissions

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 09. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 09**.*

## What this page will cover

- Code execution is the most useful tool and the most dangerous one
- Isolation levels: subprocess, container, microVM, remote service -- and what each actually contains
- Filesystem and network policy: deny by default, allowlist what the task needs
- Credential scoping: the agent's token should be weaker than the developer's, per tool and per tenant
- Destructive-action gates: confirmation, dry-run, and reversibility as a design requirement
- Resource limits: CPU, memory, wall clock, and spend

## Sources

- Koenigstein, *AI Agents* -- ch. 9
- Anthropic guidance on sandboxed code execution

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
