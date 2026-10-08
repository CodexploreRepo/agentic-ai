---
title: Setup
description: Get the labs running with uv, one API key, and a spend ceiling.
---

# Setup

Fifteen minutes, one API key. The tests run without any key at all, so you can
check the install before spending anything.

## 1. Clone and install

This repo uses [`uv`](https://docs.astral.sh/uv/). If you do not have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh    # macOS / Linux
```

Then:

```bash
git clone https://github.com/CodexploreRepo/agentic-ai.git
cd agentic-ai
make setup
```

`make setup` runs `uv sync --extra labs` and installs the pre-commit hooks.
Python 3.11 or newer; `uv` will fetch a suitable interpreter if yours is older.

## 2. Verify before you spend

```bash
make test
```

Sixty-odd tests, under a second, **no API keys and no network**. They pass
because the LLM client is a `Protocol`, so the test double is a plain class
with a `chat` method. If this is green, your install is fine.

## 3. Add one provider key

```bash
cp .env.example .env
```

Fill in **one** of these. You do not need all three:

```bash
ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...
# GOOGLE_API_KEY=...

AGENTIC_DEFAULT_PROVIDER=anthropic
```

Every lab goes through `get_client()`, which reads that default. Switching
provider is one line in `.env` — and running a lab against a second provider
is the cheapest way to find out whether a prompt you wrote is robust or just
over-fitted to one model's habits.

## 4. Add a search key for the research labs

Module 01's lab searches the web. [Tavily](https://tavily.com)'s free tier is
enough for every lab here:

```bash
TAVILY_API_KEY=tvly-...
```

## 5. Set a spend ceiling

This matters more than it looks:

```bash
AGENTIC_RUN_BUDGET_USD=1.00
```

The most common way to lose money on agents is not an expensive model — it is a
loop that retries a failing tool a few hundred times. Every run in this repo
carries a [`BudgetGuard`](/production/cost-and-latency) that raises
`BudgetExceeded` the moment it crosses the ceiling, rather than logging a
warning and continuing.

Keep the default while you are learning. Lab 01 costs a few cents.

## Running things

```bash
make lab-01        # open Module 01's notebook
make eval-01       # run its eval set, write a scorecard
make test          # unit tests, free
make lint          # ruff + mypy
make docs-serve    # this site, locally
```

`make help` lists everything.

## Checking your keys work

```bash
uv run python -c "
from agentic_ai.llm import available_providers
print('ready:', available_providers() or 'none - check your .env')
"
```

## Troubleshooting

**`ConfigError: no API key for 'anthropic'`** — `.env` is missing, in the wrong
directory, or the variable is misspelled. It must be at the repo root. If you
edited it inside a running notebook, run `get_settings.cache_clear()`.

**`ModuleNotFoundError: tavily`** — the search tool is in the optional `labs`
extra: `uv sync --extra labs`.

**`BudgetExceeded`** — working as intended. Either the run is looping (read the
trace in `.runs/` and find the tool that keeps failing) or the ceiling is
genuinely too low for what you are doing.

**Notebook cannot import `agentic_ai`** — select the `.venv` interpreter as the
kernel, or launch via `make lab-01`, which does it for you.

## What gets written where

| Path | What | Committed? |
|---|---|---|
| `.runs/` | JSONL traces, one file per run | No |
| `*.scorecard.md` | Eval results | Yes, deliberately |
| `_private/` | Your own notes, third-party material | **Never** — [see why](/references/attribution) |

## Next

- [Learning paths](/start-here/learning-paths)
- [Module 01](/modules/01-foundations/)
