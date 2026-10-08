#!/usr/bin/env python3
"""Render lab notebooks into Markdown pages for the docs site.

Why Markdown and not MDX: Docusaurus parses ``.md`` as CommonMark and ``.mdx``
as MDX. Notebook output is full of braces and angle brackets -- dict reprs,
type annotations, HTML fragments -- every one of which MDX tries to interpret
as JSX and chokes on. Emitting ``.md`` sidesteps the whole class of problem
without escaping anything.

Notebooks are *not* executed here. Execution needs API keys and spends money,
so it happens locally via ``make labs-exec`` and the outputs are committed.
This script only converts what is already there.

Run with ``make nb2md`` (or directly; it takes no arguments).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LABS_DIR = REPO_ROOT / "labs"
OUT_DIR = REPO_ROOT / "docs" / "labs"
GITHUB_BLOB = "https://github.com/CodexploreRepo/agentic-ai/blob/main"
COLAB = "https://colab.research.google.com/github/CodexploreRepo/agentic-ai/blob/main"

HEADER = """---
title: "{title}"
description: "Lab notebook rendered from {relpath}"
---

:::note[Generated page]
Rendered from [`{relpath}`]({GITHUB_BLOB}/{relpath}) -- do not edit this page
directly, edit the notebook. Outputs shown are from the last local run.

[Open in Colab]({COLAB}/{relpath}) ·
[View on GitHub]({GITHUB_BLOB}/{relpath})
:::

"""


def humanise(stem: str) -> str:
    """Turn ``01_first_agentic_workflow`` into ``01 - First Agentic Workflow``."""
    cleaned = stem.replace("_", " ").replace("-", " ").strip()
    match = re.match(r"^(\d+)\s+(.*)$", cleaned)
    if match:
        number, rest = match.groups()
        return f"{number} - {rest.title()}"
    return cleaned.title()


def convert(notebook: Path) -> str:
    """Convert one notebook to Markdown using nbconvert."""
    import nbformat
    from nbconvert import MarkdownExporter

    nb = nbformat.read(notebook, as_version=4)
    exporter = MarkdownExporter()
    # The template emits its own title; strip nbconvert's resource preamble.
    exporter.exclude_input_prompt = True
    exporter.exclude_output_prompt = True
    body, _resources = exporter.from_notebook_node(nb)
    return str(body)


def main() -> int:
    """Render every lab notebook. Returns a process exit code."""
    if not LABS_DIR.exists():
        print("no labs/ directory yet, nothing to render")
        return 0

    notebooks = sorted(
        path for path in LABS_DIR.glob("*/*.ipynb") if ".ipynb_checkpoints" not in path.parts
    )
    if not notebooks:
        print("no lab notebooks found, nothing to render")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for notebook in notebooks:
        relpath = notebook.relative_to(REPO_ROOT).as_posix()
        try:
            body = convert(notebook)
        except Exception as exc:
            print(f"FAILED {relpath}: {exc}", file=sys.stderr)
            return 1

        header = HEADER.format(
            title=humanise(notebook.stem),
            relpath=relpath,
            GITHUB_BLOB=GITHUB_BLOB,
            COLAB=COLAB,
        )
        # Flatten the lab's directory into the filename so every rendered page
        # sits directly under docs/labs/ and the sidebar stays one level deep.
        out_name = f"{notebook.parent.name}-{notebook.stem}.md"
        (OUT_DIR / out_name).write_text(header + body, encoding="utf-8")
        print(f"rendered {relpath} -> docs/labs/{out_name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
