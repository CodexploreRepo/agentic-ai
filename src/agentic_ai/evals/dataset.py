"""Eval cases: the set of examples you judge a change against.

An eval set is the single highest-leverage artefact in an agent project, and
the one teams skip. Without it, "did that prompt change help?" is answered by
reading three outputs and feeling optimistic.

The format here is deliberately plain YAML so cases can be written by hand, in
bulk, by someone who is not the engineer. Start with ten cases drawn from real
failures. Ten real cases beat a hundred invented ones, because invented cases
encode what you *think* breaks.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from agentic_ai.errors import ConfigError


@dataclass(frozen=True, slots=True)
class EvalCase:
    """One example to run the system against.

    Attributes:
        id: Stable identifier. Keep it stable across edits -- it is how you
            track whether case 7 is still broken three weeks later.
        input: What goes into the system.
        expect_contains: Substrings that must appear, case-insensitively.
            Crude, cheap, and surprisingly effective for factual grounding.
        expect_absent: Substrings that must not appear. Good for the failure
            you are actively fighting ("As an AI language model").
        rubric: Criteria for an LLM judge, when correctness is not a substring.
        tags: Free-form labels for slicing results by category.
        metadata: Anything else the case needs.
    """

    id: str
    input: str
    expect_contains: tuple[str, ...] = ()
    expect_absent: tuple[str, ...] = ()
    rubric: str = ""
    tags: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvalDataset:
    """A named collection of cases."""

    name: str
    cases: list[EvalCase] = field(default_factory=list)

    def __iter__(self) -> Iterator[EvalCase]:
        """Iterate over cases."""
        return iter(self.cases)

    def __len__(self) -> int:
        """How many cases."""
        return len(self.cases)

    def filter_by_tag(self, tag: str) -> EvalDataset:
        """A new dataset of just the cases carrying ``tag``.

        Slicing by tag is how you find out that your overall score of 80% is
        95% on short questions and 40% on multi-hop ones -- which is a
        different problem than "80%".
        """
        return EvalDataset(
            name=f"{self.name}[{tag}]",
            cases=[c for c in self.cases if tag in c.tags],
        )

    @classmethod
    def from_yaml(cls, path: str | Path) -> EvalDataset:
        """Load cases from a YAML file.

        Expected shape::

            name: video-briefs
            cases:
              - id: vb-01
                input: "Explain MCP for a backend developer"
                expect_contains: ["Model Context Protocol"]
                tags: [definition]

        Raises:
            ConfigError: The file is missing or malformed, with the reason.
        """
        file = Path(path)
        if not file.exists():
            raise ConfigError(f"eval dataset not found: {file}")

        raw = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
        if not isinstance(raw, dict) or "cases" not in raw:
            raise ConfigError(f"{file}: expected a mapping with a 'cases' key")

        cases: list[EvalCase] = []
        for index, entry in enumerate(raw["cases"]):
            if not isinstance(entry, dict) or "input" not in entry:
                raise ConfigError(f"{file}: case {index} needs at least an 'input'")
            cases.append(
                EvalCase(
                    id=str(entry.get("id") or f"case-{index + 1:02d}"),
                    input=str(entry["input"]),
                    expect_contains=tuple(entry.get("expect_contains", ())),
                    expect_absent=tuple(entry.get("expect_absent", ())),
                    rubric=str(entry.get("rubric", "")),
                    tags=tuple(entry.get("tags", ())),
                    metadata=dict(entry.get("metadata", {})),
                )
            )

        duplicates = {c.id for c in cases if sum(1 for o in cases if o.id == c.id) > 1}
        if duplicates:
            raise ConfigError(f"{file}: duplicate case ids: {', '.join(sorted(duplicates))}")

        return cls(name=str(raw.get("name") or file.stem), cases=cases)
