# Attribution & Originality Policy

This repository is a **learning resource written from scratch**. It draws its
subject matter from paid courses, published books, vendor engineering guides and
academic papers — all credited below — but every line of prose, code, prompt and
dataset here is original work produced for this project.

This page exists so that claim is checkable rather than merely asserted.

## The rule we work by

> Ideas and techniques are free to teach. Specific expression is not.

Concretely, when a source teaches a concept (say, the reflection pattern), we take
away *the concept and the vocabulary*, then write our own explanation, our own
implementation, our own prompts, and our own worked example on our own dataset.
We do not adapt, paraphrase closely, retitle, or "refactor" someone else's
notebook, slide, or chapter.

## What this repository never contains

- Quiz or exam questions from any course.
- Lecture slides, lecture notes, or video transcripts from any course.
- Course lab notebooks — graded or ungraded — in original or modified form.
- Solutions to any course's graded assignments.
- Links to third-party repositories that redistribute the above.

Downloaded third-party material is quarantined in the git-ignored `_private/`
directory and used only to build a *checklist of concepts to cover*. A
pre-commit hook (`tools/check_no_course_files.py`) blocks commits of anything in
that directory or bearing a course-artefact filename, so the policy is enforced
by the toolchain and not by memory.

## Deliberate divergence in the labs

Our labs use domains native to this project — a video research-brief agent, a
channel analytics SQL agent, a tech-news digest swarm — rather than the example
domains used by our sources. This keeps the teaching material independent and,
conveniently, makes it more useful to the audience it is written for.

## Sources

### Primary influence on the learning path

- **[Agentic AI](https://www.deeplearning.ai/courses/agentic-ai)** — DeepLearning.AI, taught by
  Andrew Ng. The order in which this curriculum introduces autonomy, reflection, tool use,
  evaluation, and planning/multi-agent systems is inspired by this course, as is its
  insistence on evaluation-driven development from day one. Highly recommended — take it.
  No course material is reproduced here.

### Books

- Koenigstein, Nicole. *AI Agents: The Definitive Guide: Design, Deployment, and Evaluation
  for Production.* O'Reilly Media. — Principal reference for the production half of this
  knowledge base: architectures, model selection, interfaces and tooling, deployment,
  benchmarking, and safety.
- Gulli, Antonio. *Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems.*
  — Cross-checked against our pattern catalogue for coverage and naming.
- Huyen, Chip. *AI Engineering: Building Applications with Foundation Models.* O'Reilly Media.
  — Framing for failure modes and evaluation.

### Vendor engineering guides

- Anthropic — *Building Effective Agents*; Agent Skills and Model Context Protocol
  engineering posts. Source of the "simple, composable patterns over frameworks" thesis
  that shapes this repo's library design.
- OpenAI — *A Practical Guide to Building Agents*. Vocabulary for guardrails and orchestration.
- Google — agent whitepapers and Gemini agent documentation.

### Papers

Cited inline on the relevant pages; collected in
[`docs/references/papers.md`](docs/references/papers.md). Core set:

- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models*, ICLR 2023
  ([arXiv:2210.03629](https://arxiv.org/abs/2210.03629))
- Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning*, NeurIPS 2023
  ([arXiv:2303.11366](https://arxiv.org/abs/2303.11366))
- Zhou et al., *Language Agent Tree Search*, 2023 ([arXiv:2310.04406](https://arxiv.org/abs/2310.04406))
- Wang et al., *A Survey on Large Language Model based Autonomous Agents*, 2023
  ([arXiv:2308.11432](https://arxiv.org/abs/2308.11432))
- *Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions*,
  2025 ([arXiv:2510.25445](https://arxiv.org/abs/2510.25445))

## Licensing of this work

- Code (`src/`, `labs/`, `projects/`, `tools/`, `tests/`) — [MIT](LICENSE)
- Prose (`docs/`) — [CC BY 4.0](LICENSE-docs)

Third-party material that is quoted or cited remains under its own terms; quotations
are kept short, clearly marked, and attributed.

## Found a problem?

If you believe any page here reproduces someone's protected expression, please
[open an issue](https://github.com/CodexploreRepo/agentic-ai/issues) and we will
rewrite or remove it promptly.
