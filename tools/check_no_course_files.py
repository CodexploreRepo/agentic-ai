#!/usr/bin/env python3
"""Pre-commit guard against committing third-party course material.

This repo teaches concepts drawn from paid courses, but publishes only original
expression (see ATTRIBUTION.md). That promise is easy to break by accident -- a
stray `git add -A` after dropping a downloaded notebook into the tree is all it
takes. This hook makes that mistake loud instead of silent.

Two checks:

1. Any path inside a quarantine directory (`_private/`) is rejected outright.
   Those directories exist to hold downloaded material.
2. Any filename matching a known course-artefact naming pattern is rejected,
   because those names are strong evidence the file was downloaded rather than
   written here.

By default only staged files are checked, which is what a pre-commit hook
wants. With ``--all``, every tracked file is checked instead -- CI runs it that
way, because a local hook can be skipped with ``--no-verify``.

Exit code 1 blocks the commit.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# Directories whose contents must never be committed, at any depth.
QUARANTINE_DIRS = ("_private",)

# Filename patterns characteristic of downloaded course artefacts. Deliberately
# narrow: these should not collide with anything we would legitimately write.
COURSE_ARTEFACT_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"(?i)graded", "'graded' in the name -- graded labs/assignments are course artefacts"),
    (r"(?i)^C\d+[_-]?M\d+", "DeepLearning.AI 'C<n>M<n>' course/module filename prefix"),
    (r"(?i)_assignment", "'_assignment' in the name -- course assignment artefact"),
    (r"(?i)solution.*\.ipynb$", "an assignment solution notebook"),
    (r"(?i)^(lecture|slides)[_-]", "lecture slides or notes from a course"),
    (r"(?i)(transcript|subtitles)", "a lecture transcript"),
)

ALLOWLIST = frozenset(
    {
        # This hook itself names the patterns it blocks.
        "tools/check_no_course_files.py",
        "ATTRIBUTION.md",
        ".pre-commit-config.yaml",
    }
)


def _git(*args: str) -> list[str]:
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=True)
    return [line for line in result.stdout.splitlines() if line.strip()]


def staged_paths() -> list[str]:
    """Paths added, copied, modified or renamed in the index."""
    return _git("diff", "--cached", "--name-only", "--diff-filter=ACMR")


def tracked_paths() -> list[str]:
    """Every file git knows about."""
    return _git("ls-files")


def violations(paths: list[str]) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for path in paths:
        if path in ALLOWLIST:
            continue
        parts = Path(path).parts
        if any(part in QUARANTINE_DIRS for part in parts):
            quarantine = "/, ".join(QUARANTINE_DIRS)
            found.append((path, f"lives under a quarantine directory ({quarantine}/)"))
            continue
        name = Path(path).name
        for pattern, reason in COURSE_ARTEFACT_PATTERNS:
            if re.search(pattern, name):
                found.append((path, f"has {reason}"))
                break
    return found


def main(argv: list[str] | None = None) -> int:
    check_all = "--all" in (argv if argv is not None else sys.argv[1:])
    paths = tracked_paths() if check_all else staged_paths()
    scope = "tracked" if check_all else "staged"

    found = violations(paths)
    if not found:
        print(f"IP guard: {len(paths)} {scope} file(s) checked, nothing suspicious.")
        return 0

    print(
        f"\nBLOCKED: {scope} files look like third-party course material.\n",
        file=sys.stderr,
    )
    for path, reason in found:
        print(f"  {path}\n      -> {reason}", file=sys.stderr)
    print(
        "\nThis repo publishes only original expression (see ATTRIBUTION.md).\n"
        "Move downloaded material into _private/ and unstage it:\n"
        "    git restore --staged <path>      # or, before the first commit:\n"
        "    git rm --cached <path>\n"
        "\nIf a file is genuinely original and tripped a name pattern, rename it\n"
        "or add it to ALLOWLIST in tools/check_no_course_files.py.\n",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
