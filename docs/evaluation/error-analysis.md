---
title: Error analysis
description: Finding the one broken thing instead of guessing.
---

# Error analysis

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 04. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 04**.*

## What this page will cover

- The loop: run the eval set, read the failures, group them, count the groups, fix the biggest group
- Reading twenty failing traces by hand -- unglamorous, and still the highest-yield hour in an agent project
- Building a failure taxonomy specific to your system, rather than using someone else's
- From taxonomy to targeted check: once a failure mode is named, make it a scored check so it cannot come back unnoticed
- Slicing by tag to find the subpopulation hiding inside an aggregate score
- `EvalReport.failures_by_check()` as the starting point

## Sources

- DeepLearning.AI *Agentic AI* -- error analysis as the core development skill
- Huyen, *AI Engineering* -- agent failure modes

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
