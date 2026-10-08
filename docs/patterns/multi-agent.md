---
title: Multi-agent systems
description: Several agents, each with a narrower job.
---

# Multi-agent systems

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 05. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 05**.*

## What this page will cover

- The honest case for multiple agents: different tools, different permissions, different context windows
- The dishonest case: one agent with a muddled prompt, split in two
- Topologies: supervisor and workers, pipeline, shared scratchpad, debate
- Communication is the design decision -- agent count is not
- Correlated failure: agents built on the same model agreeing confidently and wrongly
- Cost and latency arithmetic: every handoff is a full model call plus context re-establishment
- Code: `agentic_ai.patterns.multi_agent`

## Sources

- Anthropic, *Building Effective Agents* -- orchestrator-workers
- Wang et al., *A Survey on LLM based Autonomous Agents* (arXiv:2308.11432)
- Koenigstein, *AI Agents* -- ch. 2, Architectures and Patterns

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
