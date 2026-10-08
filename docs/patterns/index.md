---
title: Pattern catalogue
description: Every agentic design pattern in this repo, with a table for choosing between them.
---

# Pattern catalogue

:::note[Reference page]
Written and reviewed. Individual pattern pages land with their modules.
:::

Patterns are the vocabulary of agentic design. Each one is a page here and
working code in
[`agentic_ai.patterns`](https://github.com/CodexploreRepo/agentic-ai/blob/main/src/agentic_ai/patterns/).

The order below is roughly by increasing autonomy — and that is also the order
to try them in.

## Choosing one

| Pattern | Use it when | Autonomy | Cost multiple |
|---|---|---|---|
| [Prompt chaining](/patterns/prompt-chaining) | The steps are fixed and known | Level 1 | ~steps |
| [Routing](/patterns/routing) | Inputs fall into distinct categories | Level 1 | ~1.1x |
| [Reflection](/patterns/reflection) | Quality matters more than latency, and a critic has real leverage | Level 1-2 | 2-3x |
| [Tool use](/patterns/tool-use) | The agent needs outside information or actions | Level 2 | varies |
| [ReAct](/patterns/react) | You need the reasoning visible and auditable | Level 2 | varies |
| [Planning](/patterns/planning) | The step structure genuinely varies by input | Level 3 | varies + 1 |
| [Multi-agent](/patterns/multi-agent) | Subtasks need different tools, permissions or context | Level 3 | n x varies |
| [Human in the loop](/patterns/human-in-the-loop) | Actions are irreversible or high-stakes | any | +wait |

"Cost multiple" is relative to a single model call, and is the number most
often left out of pattern discussions. Reflection at 2-3x is cheap if it moves
your pass rate; expensive if it does not. You will not know which without an
[eval set](/evaluation/eval-driven-development).

## The composition rule

Patterns compose, and most real systems are two or three of them. A support
agent might route by intent, then run a tool-using loop, then reflect before
sending, with a human gate on refunds.

Compose deliberately, though, and one at a time:

> **Add one pattern. Measure. Keep it only if the number moved.**

Stacking four patterns because each sounded good produces a system that is
slow, expensive, and impossible to attribute improvement to. Every pattern you
add multiplies cost and latency and adds a failure mode.

## The pattern not on the list

The highest-value move in agentic engineering is frequently to **remove** a
pattern — to notice that the loop always runs exactly twice, or that the
planner always produces the same three steps, and replace it with the fixed
version. That is a real result, and it ships faster and breaks less.

See [when not to use agents](/foundations/when-not-to-use-agents).

## Sources

- Anthropic, *Building Effective Agents* — the composable-patterns thesis
- DeepLearning.AI, [*Agentic AI*](https://www.deeplearning.ai/courses/agentic-ai) — reflection, tool use, planning, multi-agent as the four core patterns
- Gulli, *Agentic Design Patterns* — a broader 21-pattern catalogue, cross-checked against this one
- Koenigstein, *AI Agents: The Definitive Guide*, ch. 2

---

*See [attribution and originality policy](/references/attribution).*
