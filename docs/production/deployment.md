---
title: Deployment
description: Getting it live and keeping it live.
---

# Deployment

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 08. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 08**.*

## What this page will cover

- Packaging: the agent, its tools, and the sandbox tool execution needs
- Configuration and secrets: per-environment model ids, keys, budgets
- Rollout: shadow runs against production traffic, then canary by percentage, with the eval set as the gate
- Prompt and model versioning -- a prompt change is a deploy, and needs the same rollback story
- Regression testing on every change, which is why the eval set is committed next to the code
- Runbooks: what to do when the provider is down, the budget alarm fires, or the step-limit rate spikes

## Sources

- Koenigstein, *AI Agents* -- ch. 6

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
