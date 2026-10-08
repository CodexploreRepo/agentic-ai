---
title: Memory and state
description: What the agent carries between steps and between runs.
---

# Memory and state

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 06. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 06**.*

## What this page will cover

- Four distinct things called memory: the message history, a scratchpad, retrieved documents, and durable user facts
- Within-run state vs across-run state -- different problems, different storage
- Summarisation and compaction: what to keep, what to drop, and how to tell when compaction lost something load-bearing
- Episodic vs semantic memory, and the write policy problem (what is worth remembering?)
- Memory as an attack surface -- a poisoned memory persists across runs

## Sources

- Koenigstein, *AI Agents* -- ch. 3
- *Anatomy of Agentic Memory* (arXiv:2602.19320)
- Anthropic engineering posts on context management

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
