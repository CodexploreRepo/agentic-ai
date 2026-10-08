---
title: Tool use
description: Give the model hands, and a loop to use them in.
---

# Tool use

:::note[Reference page]
Written and reviewed.
:::

*Covered in **Module 03**.*

## What this page will cover

- This page is the reference for the loop built in Module 01; see also the anatomy page
- Tool schemas as prompt: the description is the only hint the model gets about when to choose this tool
- Error text as a recovery channel -- why `Toolbox.dispatch` returns errors instead of raising
- Result truncation and why it is a default rather than an option
- Tool granularity: few broad tools vs many narrow ones, and what each does to selection accuracy
- Parallel tool calls, and the state hazards they introduce
- Code execution as the universal tool, and the sandboxing it demands (see Safety)

## Sources

- Yao et al., *ReAct* (arXiv:2210.03629)
- Anthropic tool use documentation
- Koenigstein, *AI Agents* -- ch. 5, Interfaces and Tooling

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
