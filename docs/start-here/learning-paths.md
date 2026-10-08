---
title: Learning paths
description: Four routes through this material, depending on why you are here.
---

# Learning paths

The curriculum is nine modules in order, but not everyone should start at the
start. Pick the route that matches why you are here.

## "I have a weekend"

The shortest path to building something real.

1. [What is an agent?](/foundations/what-is-an-agent) — the control-flow distinction
2. [Anatomy of an agent](/foundations/anatomy-of-an-agent) — the five parts
3. [Eval-driven development](/evaluation/eval-driven-development) — write ten cases first
4. [Module 01 lab](/labs/) — build the research agent, measure it against a single prompt
5. [When not to use agents](/foundations/when-not-to-use-agents) — the counterweight

Finish and you can build a tool-using agent and demonstrate it beats the
obvious alternative. That is more than most agent demos manage.

## "I need to ship this at work"

Production concerns first. Skim the patterns; you will meet them again.

1. [The autonomy spectrum](/foundations/autonomy-spectrum) — then argue for the lowest level that works
2. [Eval-driven development](/evaluation/eval-driven-development) and [error analysis](/evaluation/error-analysis)
3. [Observability and tracing](/production/observability-and-tracing) — you will need this on day one, not later
4. [Cost and latency](/production/cost-and-latency) — the two numbers that decide whether you ship
5. [Guardrails](/safety/guardrails) and [prompt injection](/safety/prompt-injection)
6. [Architecture](/production/architecture) and [reliability](/production/reliability-and-retries)
7. Then the patterns, as the need arises

The uncomfortable advice: **build the eval set and the tracing before the
agent.** Teams that do it the other way spend their second month unable to
explain why last week's version was better.

## "I want to understand how frameworks work"

Read the primitives, then the frameworks will hold no surprises.

1. [`llm/base.py`](https://github.com/CodexploreRepo/agentic-ai/blob/main/src/agentic_ai/llm/base.py) — one shape for every provider
2. [`patterns/tool_use.py`](https://github.com/CodexploreRepo/agentic-ai/blob/main/src/agentic_ai/patterns/tool_use.py) — the loop, in full
3. [`tools/registry.py`](https://github.com/CodexploreRepo/agentic-ai/blob/main/src/agentic_ai/tools/registry.py) — type hints to JSON Schema
4. [Anatomy of an agent](/foundations/anatomy-of-an-agent) — the five parts to look for in any framework
5. [Frameworks](/frameworks/) — the same agent, four ways, measured on one eval set

Reading those three files takes an hour and makes every agent framework legible.

## "I am following the course"

If you are taking
[DeepLearning.AI's *Agentic AI*](https://www.deeplearning.ai/courses/agentic-ai)
alongside this — which is the recommended way to use it — Modules 01–05 follow
the same concept order, so they interleave naturally:

| Course module | Read here | Build here |
|---|---|---|
| Introduction to agentic workflows | [Module 01](/modules/01-foundations/) | Research brief agent |
| Reflection | [Module 02](/modules/02-reflection/) | Draft-and-critique |
| Tool use | [Module 03](/modules/03-tool-use/) | Toolbox and code execution |
| Practical tips | [Module 04](/modules/04-evaluation/) | Component evals, error analysis |
| Highly autonomous agents | [Module 05](/modules/05-planning-multi-agent/) | Planner, router, team |

Then keep going: [Modules 06–09](/modules/) cover memory, MCP, observability
and safety, which the course does not reach.

The labs here deliberately use **different domains** from the course's, so you
build two different things with the same ideas rather than the same thing
twice. That is a better use of your time, and it is also what keeps this
material independent — see [attribution](/references/attribution).

## Whichever route you take

Two pages are load-bearing no matter why you are here:

- [Eval-driven development](/evaluation/eval-driven-development) — without it you cannot tell whether anything you do helps
- [When not to use agents](/foundations/when-not-to-use-agents) — the skill of recognising the cases that need something simpler
