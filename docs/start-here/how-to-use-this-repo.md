---
title: How to use this repo
description: The three parts of this project and how they fit together.
---

# How to use this repo

Everything here exists in three forms, and knowing which one you want saves a
lot of clicking.

## 1. The knowledge base — what you are reading

Prose, organised two ways at once.

**[Modules](/modules/)** are the sequential path: nine of them, one per video,
in the order they should be learned. Each module page is a brief — outcomes,
prerequisites, and links to the pages and code it covers.

**Reference sections** are the encyclopaedia:
[foundations](/foundations/what-is-an-agent),
[patterns](/patterns/),
[building blocks](/building-blocks/models),
[evaluation](/evaluation/eval-driven-development),
[production](/production/architecture),
[safety](/safety/guardrails) and
[frameworks](/frameworks/). These pages stand alone and cross-link back to the
module that teaches them.

The split exists because this site has two kinds of reader: someone working
through a series, and someone who landed here from a search engine in eighteen
months wanting one answer. Optimising for only the first is how course
repositories become unusable the moment the course ends.

## 2. The library — `src/agentic_ai/`

Reusable, tested Python. A provider-agnostic LLM client, the agent loop, the
tool registry, the eval harness, and tracing.

One rule shapes it: **a notebook never defines a pattern.** Patterns live in
`src/`, with tests, and the notebooks import them. A pattern that exists only
inside a notebook cannot be tested, reused, or improved — and every course
repository that works that way rots.

Worth reading directly, in this order:

| File | Why |
|---|---|
| [`patterns/tool_use.py`](https://github.com/CodexploreRepo/agentic-ai/blob/main/src/agentic_ai/patterns/tool_use.py) | The agent loop. Eighty lines, underneath every framework |
| [`llm/base.py`](https://github.com/CodexploreRepo/agentic-ai/blob/main/src/agentic_ai/llm/base.py) | The provider-agnostic contract |
| [`tools/registry.py`](https://github.com/CodexploreRepo/agentic-ai/blob/main/src/agentic_ai/tools/registry.py) | Type hints to JSON Schema |
| [`evals/runner.py`](https://github.com/CodexploreRepo/agentic-ai/blob/main/src/agentic_ai/evals/runner.py) | How a claim gets measured |

## 3. The labs — `labs/`

One notebook per module. Each lab imports the library, uses the pattern,
**measures it**, and then breaks it on purpose — because the failure mode is
the part you remember.

Labs come with an eval set, so every claim a lab makes is checkable:

```bash
make lab-01      # open the notebook
make eval-01     # run its eval set and write a scorecard
```

## Which order to use them in

Reading alone works; the pages are self-contained. But the sequence that
actually sticks is:

1. **Watch** the video for the shape of the thing
2. **Read** the module's pages for the detail
3. **Run** the lab, then change something and watch the eval score move

Step 3 is where it stops being theory. Getting a number to move — or
discovering that your clever change moved nothing — is a different kind of
learning from reading about it.

## Conventions worth knowing

- **Status badges.** Pages say whether they are written or still an outline.
  Outlines list their intended headings and sources, which is useful for
  deciding what to study next.
- **Sources on every page.** Each page credits what it drew on, under
  [this attribution policy](/references/attribution).
- **Cost warnings.** Anything that spends money says so, and
  [a budget guard](/production/cost-and-latency) is on by default.

## Next

- [Setup](/start-here/setup) — get the code running, one API key
- [Learning paths](/start-here/learning-paths) — pick a route by how much time you have
- [Module 01](/modules/01-foundations/) — start
