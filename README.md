# Agentic AI — a knowledge hub

> **📖 Read the knowledge base → [codexplorerepo.github.io/agentic-ai](https://codexplorerepo.github.io/agentic-ai/)**
> **📺 Watch the series → [CodeXplore on YouTube](https://www.youtube.com/@CodeXplore)**

A reference library and written curriculum for building AI agents that actually survive
contact with production: patterns from first principles, measured with evals, instrumented,
and guarded.

This repo is built around one opinion, borrowed from Anthropic and earned the hard way:
**most agent problems are solved by simple, composable patterns, not by frameworks.** So the
code here teaches the primitives — an agent loop you can read in one sitting — and treats
frameworks as a later chapter you can take or leave.

## What's here

| | |
|---|---|
| [`docs/`](docs/) | The knowledge base. Readable on GitHub, published as a site. |
| [`src/agentic_ai/`](src/agentic_ai/) | The library: provider-agnostic LLM client, patterns, tools, evals, tracing. |
| [`labs/`](labs/) | One notebook per module. Imports the library, measures the pattern, breaks it. |
| [`projects/`](projects/) | End-to-end capstones. |
| [`tests/`](tests/) | Unit tests for the library; no network, no spend. |

## Curriculum

| # | Module | You'll be able to |
|---|---|---|
| 01 | [Foundations & the evals mindset](docs/modules/01-foundations/) | Tell an agent from a workflow, decompose a task, and prove a change helped |
| 02 | Reflection | Make a system critique and improve its own output |
| 03 | Tool use & code execution | Give an agent hands, safely |
| 04 | Evaluation & error analysis | Find the one broken component instead of guessing |
| 05 | Planning & multi-agent systems | Decide when more agents help, and when they just add latency |
| 06 | Memory & context engineering | Keep an agent coherent past its context window |
| 07 | MCP & integrations | Connect agents to real systems over a standard protocol |
| 08 | Observability & production | See what your agent did, and what it cost |
| 09 | Safety, guardrails & security | Survive prompt injection and untrusted tool output |

Modules 01–05 follow the concept order of [DeepLearning.AI's *Agentic AI*
course](https://www.deeplearning.ai/courses/agentic-ai) — take it, it's good. Modules 06–09
cover the production ground that courses usually skip. All content here is original; see
[ATTRIBUTION.md](ATTRIBUTION.md).

## Quick start

```bash
git clone https://github.com/CodexploreRepo/agentic-ai.git
cd agentic-ai
make setup                  # uv sync + pre-commit install
cp .env.example .env        # add ONE model provider key to start
make test                   # should be green, no API keys needed
```

Then open the first lab:

```bash
make lab-01
```

Full setup notes, including cost control: [`docs/start-here/setup.md`](docs/start-here/setup.md).

## Two ways to use this

- **Following the series?** Start at [Module 01](docs/modules/01-foundations/) and go in order.
  Each module is one video, one doc set, one notebook.
- **Landed here from a search?** Go straight to the reference section — the
  [pattern catalogue](docs/patterns/), [building blocks](docs/building-blocks/),
  [evaluation](docs/evaluation/), [production](docs/production/), and [safety](docs/safety/)
  pages stand alone and cross-link back to the module that teaches them.

## Contributing

Corrections and additions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). One hard rule:
**no third-party course material, ever.** A pre-commit hook enforces it.

## License

Code [MIT](LICENSE) · prose [CC BY 4.0](LICENSE-docs)
