# Contributing

Corrections, clarifications and additions are all welcome — especially
corrections. This field moves fast enough that anything here over a year old
deserves checking.

## The one hard rule

**No third-party course material. Ever.**

This repo teaches concepts drawn from paid courses and books, but publishes
only original expression. See [ATTRIBUTION.md](ATTRIBUTION.md) for the full
policy. In practice:

- Do not contribute notebooks, slides, transcripts or quiz questions from any course
- Do not contribute code adapted from a course lab — write it from the concept
- Put any downloaded reference material in `_private/`, which is git-ignored

A pre-commit hook (`tools/check_no_course_files.py`) enforces this, and the
same check runs in CI against every tracked file, because a local hook can be
skipped with `--no-verify`.

## Getting set up

```bash
make setup     # uv sync + pre-commit install
make check     # lint, type-check, test — must be green
```

Tests need no API keys and make no network calls.

## What good looks like here

**Prose.** Explain *when* and *why*, not just *what*. A page that lists an
API's parameters is documentation; a page that says which parameter matters and
what breaks when you get it wrong is worth reading. State trade-offs in both
directions, and say when a pattern is the wrong choice.

**Code.** Must be typed (`mypy --strict` passes), linted, and tested.
Docstrings explain the reasoning, not the signature — the signature is already
there. Match the voice of the surrounding code.

**Claims.** Anything asserting that one approach beats another needs an eval
result, not an opinion. That is the standard the rest of the repo holds itself
to, and it is the most valuable thing about it.

**Sources.** Every docs page ends with what it drew on. Add to it rather than
replacing it.

## Pull requests

- One topic per PR
- `make check` green
- If you changed a prompt, a model, or a pattern, include the eval scorecard
  diff. "I think it's better" is not reviewable; a number is
- If you added a page, add it to `docs-site/sidebars.ts` — the build fails on
  broken links, on purpose

## Reporting a problem

[Open an issue](https://github.com/CodexploreRepo/agentic-ai/issues). Useful
reports include what you ran, what you expected, and what happened. If it is a
docs problem, the page URL is enough.

If you believe a page reproduces someone's protected expression, say so and it
will be rewritten or removed promptly.
