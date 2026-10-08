---
title: Prompt chaining
description: Split one hard call into several easy ones.
---

# Prompt chaining

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 01. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 01**.*

## What this page will cover

- Why decomposition raises accuracy: each call gets a narrower job and a shorter context
- The shape: output of step N is input to step N+1, with a validation gate between
- Where it beats an agent loop: fixed, known sequences -- no reason to pay for the model to rediscover the steps each run
- Failure mode: errors compound. A 95%-accurate step run five times is 77% accurate end to end
- Adding gates: cheap deterministic checks between steps, so a bad intermediate stops the chain instead of poisoning it
- Worked comparison against a single mega-prompt on the Module 01 eval set

## Sources

- Anthropic, *Building Effective Agents* -- prompt chaining as the first workflow to reach for
- Gulli, *Agentic Design Patterns* -- ch. on prompt chaining

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
