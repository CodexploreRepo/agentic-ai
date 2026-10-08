---
title: Reliability and retries
description: Failing well in a system that fails often.
---

# Reliability and retries

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 08. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 08**.*

## What this page will cover

- Four failure classes: provider errors, tool errors, model mistakes, and runs that never terminate
- Retry with backoff for transport errors; retry with the error message for model mistakes -- different problems
- Why blind retries on a non-idempotent tool are how agents send three emails
- Timeouts at every level: tool, step, run
- Circuit breakers on tools, and graceful degradation when one is down
- Checkpointing so a long run resumes instead of restarting

## Sources

- Koenigstein, *AI Agents* -- ch. 6
- *Beyond Component Testing: Validating Agentic AI Systems* (arXiv:2607.29405)

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
