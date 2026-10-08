---
title: Projects
description: Three end-to-end capstones that combine several modules.
sidebar_label: Overview
---

# Projects

Modules teach one idea at a time. Projects are where several have to work
together, with the awkward bits left in — real data, real failure modes, real
cost.

:::note[Planned]
Scaffolding exists in
[`projects/`](https://github.com/CodexploreRepo/agentic-ai/tree/main/projects).
Each project ships after the modules it depends on.
:::

## 1. Research agent

**Needs:** Modules 01, 02, 03, 06

The Module 01 lab, grown up: reflection on the draft, a real retrieval layer
over a document store, memory of what it has already researched, and an eval
set that grew out of its own production failures.

The interesting problem is **grounding** — making every claim traceable to a
source, and detecting the ones that are not.

## 2. SQL analyst

**Needs:** Modules 02, 03, 04, 09

Natural-language questions against a channel-analytics database. The agent
writes SQL, runs it, reads the error, and fixes it — the database being a
critic that is never agreeable.

The interesting problems are **schema context** (the schema does not fit in the
window) and **containment** (a read-only credential is not optional).

## 3. Support swarm

**Needs:** Modules 05, 06, 08, 09

A routed, multi-agent support system: triage, then a specialist, with a human
gate on anything touching money, and tracing good enough to answer "why did it
say that?" a week later.

The interesting problem is proving the swarm beats one well-prompted agent —
which, on a good day, it does not.

## What makes these projects rather than labs

| | Lab | Project |
|---|---|---|
| Scope | One pattern | Several, composed |
| Data | Small, curated | Messy, real-shaped |
| Evals | 12 cases | 50+, grown from failures |
| Ops | Prints its cost | Traced, budgeted, deployable |
| Ends when | The pattern is demonstrated | It survives a week of use |

## Suggested use

Do the modules first. Then pick the project closest to something you actually
need, and change the domain to yours — the point is to hit the problems that
only appear at full scale, and those arrive faster when you care about the
output.
