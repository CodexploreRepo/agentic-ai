---
title: Attribution & originality
description: What this site owes to its sources, and how it stays original.
---

# Attribution & originality

This site is a learning resource **written from scratch**. It draws its subject
matter from paid courses, published books, vendor engineering guides and
academic papers — all credited below — but every page of prose, every line of
code, every prompt and every dataset here is original work produced for this
project.

This page exists so that claim is checkable rather than merely asserted.

## The rule we work by

> Ideas and techniques are free to teach. Specific expression is not.

When a source teaches a concept — the reflection pattern, say — we take away
*the concept and the vocabulary*, then write our own explanation, our own
implementation, our own prompts, and our own worked example on our own data.
We do not adapt, closely paraphrase, retitle or "refactor" someone else's
notebook, slide or chapter.

## What this project never contains

- Quiz or exam questions from any course
- Lecture slides, lecture notes or video transcripts from any course
- Course lab notebooks, graded or ungraded, in original or modified form
- Solutions to any course's graded assignments
- Links to third-party repositories that redistribute the above

Downloaded third-party material is quarantined in a git-ignored directory and
used only to build a *checklist of concepts to cover*. A pre-commit hook
([`tools/check_no_course_files.py`](https://github.com/CodexploreRepo/agentic-ai/blob/main/tools/check_no_course_files.py))
blocks commits of anything in that directory or bearing a course-artefact
filename — so the policy is enforced by the toolchain, not by memory.

## Deliberate divergence in the labs

The labs here use domains native to this project — a video research brief
agent, a channel analytics SQL agent, a tech-news digest swarm — rather than
the example domains used by our sources.

That keeps the material independent. It also makes it more useful to the people
it is written for, which is a happy coincidence rather than the main reason.

## Sources

### Primary influence on the learning path

**[Agentic AI](https://www.deeplearning.ai/courses/agentic-ai)** — DeepLearning.AI,
taught by Andrew Ng. The order in which this curriculum introduces autonomy,
reflection, tool use, evaluation and planning/multi-agent systems is inspired
by this course, as is its insistence on evaluation-driven development from day
one. **Highly recommended — take it.** No course material is reproduced here.

### Books

- **Koenigstein, Nicole.** *AI Agents: The Definitive Guide: Design, Deployment,
  and Evaluation for Production.* O'Reilly Media. — Principal reference for the
  production half of this site: architectures, model selection, interfaces and
  tooling, deployment, benchmarking, and safety.
- **Gulli, Antonio.** *Agentic Design Patterns: A Hands-On Guide to Building
  Intelligent Systems.* — Cross-checked against our
  [pattern catalogue](/patterns/) for coverage and naming.
- **Huyen, Chip.** *AI Engineering: Building Applications with Foundation
  Models.* O'Reilly Media. — Framing for failure modes and evaluation.

### Vendor engineering guides

- **Anthropic** — *Building Effective Agents*; Agent Skills and Model Context
  Protocol engineering posts. Source of the "simple, composable patterns over
  frameworks" thesis that shapes this repo's library design.
- **OpenAI** — *A Practical Guide to Building Agents*. Vocabulary for
  guardrails and orchestration.
- **Google** — agent whitepapers and Gemini agent documentation.

### Papers

Cited inline where relevant and collected in
[papers](/references/papers).

## Licensing

- Code — [MIT](https://github.com/CodexploreRepo/agentic-ai/blob/main/LICENSE)
- Prose — [CC BY 4.0](https://github.com/CodexploreRepo/agentic-ai/blob/main/LICENSE-docs)

Third-party material that is quoted or cited remains under its own terms.
Quotations are kept short, clearly marked and attributed; we paraphrase by
default.

## Found a problem?

If you believe any page here reproduces someone's protected expression, please
[open an issue](https://github.com/CodexploreRepo/agentic-ai/issues) and we
will rewrite or remove it promptly.
