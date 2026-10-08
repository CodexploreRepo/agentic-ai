---
title: Papers
description: The primary literature behind the patterns, with what each one actually contributed.
---

# Papers

Cited across this site. Annotated with **what each paper contributed**, because
a reading list without that is just a list.

Ordered roughly by how much you would miss by skipping it.

## Start here

**ReAct: Synergizing Reasoning and Acting in Language Models**
Yao et al., ICLR 2023 — [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)

The paper that made the agent loop explicit: interleave reasoning with tool
calls rather than doing all the thinking up front. Native tool calling has
since absorbed most of the mechanism, but the idea that the *reasoning step
should be visible and inspectable* is the part that survived, and the reason
traces are designed the way they are. See [ReAct](/patterns/react).

**Reflexion: Language Agents with Verbal Reinforcement Learning**
Shinn et al., NeurIPS 2023 — [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)

Self-critique as a feedback loop, with the critique kept in context across
attempts. The important detail, often skipped when the pattern is summarised:
it works best when the feedback comes from **an external signal** — a test
result, an error — rather than the model's own opinion of its work. See
[reflection](/patterns/reflection).

**Self-Refine: Iterative Refinement with Self-Feedback**
Madaan et al., NeurIPS 2023 — [arXiv:2303.17651](https://arxiv.org/abs/2303.17651)

The pure self-critique case, without external signal, and useful precisely
because it quantifies a smaller gain. Read alongside Reflexion to see how much
of reflection's value comes from the signal rather than the loop.

## Evaluation

**Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena**
Zheng et al., 2023 — [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)

The reference for using models as graders, and more importantly for the biases
that make naive judges useless: position bias, verbosity bias, and
self-enhancement. If you take one thing from it, take the practice of
validating your judge against human labels on a sample. See
[LLM as judge](/evaluation/llm-as-judge).

**AgentBench: Evaluating LLMs as Agents**
Liu et al., 2023 — [arXiv:2308.03688](https://arxiv.org/abs/2308.03688)

Multi-environment agent benchmarking. Useful less for its leaderboard than for
making the harness question visible: what the agent was allowed to do, how many
attempts it got, and what counted as success. Those choices move results more
than model choice does. See [benchmarks](/evaluation/benchmarks).

## Surveys, for orientation

**A Survey on Large Language Model based Autonomous Agents**
Wang et al., 2023 — [arXiv:2308.11432](https://arxiv.org/abs/2308.11432)

The early taxonomy — profile, memory, planning, action — that much of the
field's vocabulary still comes from. Dated in its specifics, still the
clearest map of the conceptual territory.

**Agentic AI: A Comprehensive Survey of Architectures, Applications, and
Future Directions**
2025 — [arXiv:2510.25445](https://arxiv.org/abs/2510.25445)

A more recent sweep. Best used as an index into subfields rather than read
front to back.

## Planning and search

**Language Agent Tree Search**
Zhou et al., 2023 — [arXiv:2310.04406](https://arxiv.org/abs/2310.04406)

Monte Carlo tree search over agent trajectories. Strong results, and a useful
demonstration of the cost ceiling: searching over plans multiplies spend by the
branching factor, which is why it rarely leaves benchmarks. See
[planning](/patterns/planning).

## Memory and context

**Anatomy of Agentic Memory: Taxonomy and Empirical Analysis**
2026 — [arXiv:2602.19320](https://arxiv.org/abs/2602.19320)

A structure-oriented taxonomy of agent memory with empirical comparison. The
useful contribution is separating memory *structure* from memory *management
policy* — the second being where most systems actually go wrong. See
[memory and state](/building-blocks/memory-and-state).

## Safety

**Trustworthy Agentic AI: A Cybersecurity and Systems Survey**
2026 — [arXiv:2609.13731](https://arxiv.org/abs/2609.13731)

Threat landscape and defence architectures for agentic systems, organised as a
trustworthiness taxonomy. Read it after
[prompt injection](/safety/prompt-injection), by which point its categories
will mean something concrete.

**Beyond Component Testing: Validating Agentic AI Systems**
2026 — [arXiv:2607.29405](https://arxiv.org/abs/2607.29405)

Why component-level tests can all pass while the system fails, and what to do
about it. Pairs with
[component vs end-to-end evals](/evaluation/component-vs-end-to-end).

---

Non-academic sources — vendor engineering guides and books — are listed in the
[reading list](/references/reading-list). Full crediting in
[attribution](/references/attribution).
