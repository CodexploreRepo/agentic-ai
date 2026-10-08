---
title: Reading list
description: What to read beyond this site, ordered by what you are trying to do.
---

# Reading list

Everything worth reading about agents, grouped by the problem it solves rather
than by publisher. Papers have [their own page](/references/papers).

## If you are starting out

**[Agentic AI](https://www.deeplearning.ai/courses/agentic-ai)** — DeepLearning.AI,
Andrew Ng. The course this curriculum's first five modules follow in concept
order. Strong on the evaluation-first mindset, which is the part most
tutorials omit. Take it.

**Building Effective Agents** — Anthropic engineering. Short, opinionated, and
the most valuable thing you can read in thirty minutes. The argument that
simple composable patterns beat frameworks is the one that shapes this repo.

**A Practical Guide to Building Agents** — OpenAI. A good complement: more
structured, more concrete about guardrails and handoffs.

## If you are shipping to production

**Koenigstein, *AI Agents: The Definitive Guide*** (O'Reilly) — the most
complete treatment of the production half: architectures, model selection,
interfaces, deployment, benchmarking, safety. The reference behind Modules
06–09 here. Intermediate to advanced; worth the effort.

**Huyen, *AI Engineering*** (O'Reilly) — broader than agents, and the chapter
on RAG and agents is the clearest short treatment of agent failure modes and
evaluation in print. Read it if you are responsible for whether something works.

**OpenTelemetry GenAI semantic conventions** — the standard for agent
telemetry. Dry, and the right thing to instrument against rather than
inventing your own span names. See
[observability](/production/observability-and-tracing).

## If you want the pattern catalogue

**Gulli, *Agentic Design Patterns*** — 424 pages, free, 21 patterns with code.
Broader than this site's catalogue and useful as a cross-check. Some patterns
are thin, but coverage is the point.

**Model Context Protocol specification** — read the spec rather than a summary.
It is short, and the primitives (tools, resources, prompts) are clearer in the
original. See [MCP](/building-blocks/mcp).

## If you are worried about security

**Simon Willison's writing on prompt injection** — the clearest sustained
thinking available on indirect injection and the "lethal trifecta" of private
data, untrusted content, and an exfiltration path. Start with the lethal
trifecta framing and work backwards.

**OWASP Top 10 for LLM Applications** — the checklist form. Useful for review
conversations; less useful for understanding why.

**NIST AI Risk Management Framework** — if you need to speak to a risk
function. Heavy, and occasionally necessary.

## Staying current

Agents move fast enough that anything over a year old needs checking:

- **Provider engineering blogs** — Anthropic, OpenAI and Google publish the
  practical material first, often months ahead of books
- **Framework changelogs** — the fastest way to see where the abstractions are
  actually settling
- **Simon Willison's blog** — consistently early and sceptical, which is a rare
  pair
- **Latent Space** — practitioner interviews; good for hearing what broke in
  production

## A note on dates

Model names, prices, APIs and framework idioms in this field go stale in
months. This site keeps all model identifiers and prices in
[one file](https://github.com/CodexploreRepo/agentic-ai/blob/main/src/agentic_ai/models.py)
so they can be corrected in one edit, and dates its claims where they are
likely to expire.

If you find something here that has aged badly,
[open an issue](https://github.com/CodexploreRepo/agentic-ai/issues).

---

Full crediting in [attribution](/references/attribution).
