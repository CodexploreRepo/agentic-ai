# Conventions for this repo

Notes for anyone — human or model — adding to this project. The point of
writing them down is that modules land one at a time over months, and
consistency is what makes the result feel like one body of work rather than
nine.

## The IP rule, first

This repo teaches concepts from paid courses and books but publishes **only
original expression**. See [ATTRIBUTION.md](ATTRIBUTION.md).

- Third-party material lives in `_private/` (git-ignored) and is used only to
  build a *checklist of concepts*
- Never read a source's code while writing ours — take the concept, close the
  tab, write the implementation
- Labs use domains native to this project (video research, channel analytics,
  tech-news digests), deliberately different from any source's examples
- `tools/check_no_course_files.py` enforces this on commit and in CI

## Structure

| Path | Holds | Rule |
|---|---|---|
| `docs/` | Prose knowledge base | Markdown, readable on GitHub, published via `docs-site/` |
| `docs-site/` | Docusaurus app only | No content here — it reads `../docs` |
| `src/agentic_ai/` | The library | Typed, tested, no notebook-only code |
| `labs/NN-slug/` | One notebook per module | **Never defines a pattern** — imports it |
| `projects/` | End-to-end capstones | Applications, not notebooks |
| `tests/` | Unit tests | No network, no API keys, no spend |
| `tools/` | Repo scripts | Typed and linted like `src/` |
| `episodes/` | Video scripting notes | Git-ignored except `TEMPLATE.md` |

## The load-bearing rule

**A lab notebook never defines a pattern.** Patterns live in
`src/agentic_ai/patterns/`, with tests. Notebooks import them and show them
being used, measured, and broken.

This is what stops the repo rotting. A pattern defined in a notebook cannot be
tested, reused, or fixed in one place.

## Adding a module

Clone Module 01's shape — it is the template:

1. `docs/modules/NN-slug/index.mdx` — brief with `<WatchReadCode>` and `<YouTube>`
2. Reference pages in the relevant section, replacing the generated outline
3. `src/agentic_ai/patterns/<pattern>.py` — replace the `NotImplementedError`
   stub with a real implementation plus tests
4. `labs/NN-slug/` — notebook, `systems.py`, `evals/*.yaml`, `run_evals.py`,
   `exercises/README.md`
5. Add the lab's rendered page to `docs-site/sidebars.ts`
6. Add a `lab-NN` and `eval-NN` target to the `Makefile`
7. Update the status badge and the episode row in `docs/modules/index.mdx`

## Code conventions

- `mypy --strict` and `ruff` must pass: `make check`
- Docstrings explain **why**, not what — the signature says what
- Model ids and prices go in `src/agentic_ai/models.py`, nowhere else
- Config goes through `agentic_ai.settings`; nothing reads `os.environ` directly
- New providers implement the `LLMClient` protocol in `llm/base.py` and nothing
  else leaks out
- Tool errors are returned as text, never raised at the model — recovery
  depends on it

## Writing conventions

- Explain when and why, not just what; state trade-offs in both directions
- Say when something is the wrong choice — those paragraphs are the most useful
- Every claim that one approach beats another needs an eval result
- Every page ends with a `## Sources` section and a link to the attribution page
- Status badges are honest: `Outline` means outline
- Use `:::note` admonitions in `.md`; only `.mdx` pages can use components
- `.md` is parsed as CommonMark, `.mdx` as MDX — generated notebook pages must
  be `.md`, or notebook output breaks the build

## Evals are the standard

Every module makes a claim. The claim is tested, not asserted, and sometimes it
loses — those are the most useful modules. Scorecards are committed so a prompt
change arrives in a PR with the number it moved.

## Commands

```bash
make setup        # install
make check        # lint + types + tests
make test         # tests only, free
make eval-01      # [spends money] Module 01's acceptance test
make docs-serve   # site, locally
make docs         # site build, fails on broken links
```
