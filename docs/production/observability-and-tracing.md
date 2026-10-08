---
title: Observability and tracing
description: Seeing what the agent did.
---

# Observability and tracing

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 08. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 08**.*

## What this page will cover

- Why standard APM is insufficient: nothing crashed, and the output looks fine
- The span model for agents: run, step, model call, tool call -- and the attributes worth recording on each
- OpenTelemetry and GenAI semantic conventions; replacing this repo's JSONL tracer with a real collector
- What to log and what never to log: prompts and outputs contain user data
- Online signals: tool error rate, step-count distribution, step-limit hits, cache hit rate, cost per successful task
- Closing the loop -- production traces become tomorrow's eval cases
- `agentic_ai.obs.trace` as the minimal version of all this

## Sources

- OpenTelemetry GenAI semantic conventions
- Koenigstein, *AI Agents* -- ch. 6

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
