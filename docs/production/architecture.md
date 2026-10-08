---
title: Architecture
description: Where an agent sits in a real system.
---

# Architecture

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 08. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 08**.*

## What this page will cover

- The request path: synchronous answer, background job, or streamed partial results -- and what each implies for timeouts
- Agents are long-running and stateful, which breaks assumptions in most request/response stacks
- Queues, workers and durable execution: surviving a process restart mid-run
- Where state lives: conversation store, trace store, memory store, and the eval corpus they all feed
- Idempotency keys for tool side effects
- Multi-tenancy and per-tenant credentials for tools

## Sources

- Koenigstein, *AI Agents* -- ch. 6, Deploying Agents in Real Products
- *From Prompt-Response to Goal-Directed Systems* (arXiv:2602.10479)

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
