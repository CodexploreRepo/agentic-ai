---
title: Frameworks
description: Do you need an agent framework at all, and if so which one?
---

# Frameworks

:::note[Reference page]
Written and reviewed. Individual framework pages land after Module 05.
:::

This section comes near the end of the curriculum on purpose. Frameworks are
easier to judge once you have written the loop yourself — at which point most
of their abstractions become obvious rather than magical, and you can tell
which ones are buying you something.

## The prior question

> Do you need one?

The honest answer for a lot of projects is no. What an agent actually requires
is an HTTP client, a loop, a tool registry, and a trace. This repo's
[`src/agentic_ai/`](https://github.com/CodexploreRepo/agentic-ai/tree/main/src/agentic_ai)
is roughly 1,200 lines of exactly that, and it is readable in an afternoon.

What a framework buys you is real, though: prebuilt integrations, a visual
debugger, checkpointing, and someone else's well-tested opinion about state
management. What it costs is a layer between you and the model call, and a
dependency whose upgrade schedule is not yours.

The threshold worth using: **adopt a framework when you need something it does
that you would otherwise have to build and maintain** — durable execution,
time-travel debugging, a large catalogue of integrations. Not because it is
what people use.

## The four compared here

| | Shape | Strongest at |
|---|---|---|
| [No framework](/frameworks/no-framework) | Direct SDK calls | Inspectability; nothing hidden |
| [Claude Agent SDK](/frameworks/claude-agent-sdk) | Agent with a computer | Shell/filesystem work, MCP, Skills, permissions |
| [OpenAI Agents SDK](/frameworks/openai-agents-sdk) | Agents, handoffs, guardrails | Coherent multi-agent vocabulary, built-in tracing |
| [LangGraph](/frameworks/langgraph) | Explicit state machine | Long-running, resumable, human-approved workflows |

## How this section judges them

Not by feature list. The [comparison page](/frameworks/comparison) rebuilds
**the same task** — Module 01's research brief agent — four ways, and measures
each on:

- Lines of code
- Pass rate on the *same* twelve-case eval set
- Cost per task
- p50 latency
- What a failure looks like, and how long it takes to find

That last row is the one that decides things in practice, and the one no
feature list covers.

## Reading any framework quickly

The [anatomy of an agent](/foundations/anatomy-of-an-agent) gives you the
checklist. Pick up an unfamiliar framework and find where it put each of the
five parts, then ask:

- Is the loop visible, or buried in a `.run()` you cannot step through?
- Can you see the exact messages sent to the model?
- What is the default step limit — and is there one?
- How are tool errors surfaced: to you, or to the model?
- What does it record by default?

Five questions, twenty minutes, and you will know more about whether it
survives your production incident than a week of reading its docs.

## A standing caveat

These APIs move quarterly. Every specific claim in this section is dated, and
anything here more than a year old should be checked against the framework's
own changelog before you rely on it.

## Sources

- Anthropic, *Building Effective Agents* — the case for starting without a framework
- Each framework's own documentation
- Koenigstein, *AI Agents: The Definitive Guide*, ch. 5

---

*See [attribution and originality policy](/references/attribution).*
