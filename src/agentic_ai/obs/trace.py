"""Seeing what the agent actually did.

The defining debugging problem of agentic systems is that the output tells you
almost nothing about the process. An agent that returns a plausible-looking
answer may have called the wrong tool four times, silently swallowed an error,
and guessed. You cannot tell from the answer, and you cannot tell from a stack
trace, because nothing crashed.

A trace is the fix: one append-only record per run, with a span per step. This
implementation is deliberately about a hundred lines -- no collector, no
service, just JSONL on disk -- because the concept is what matters and a
reader can hold all of it in their head. Module 08 replaces it with
OpenTelemetry, by which point you know what you are asking the collector for.
"""

from __future__ import annotations

import json
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from agentic_ai.settings import get_settings

SpanKind = Literal["run", "llm", "tool", "step", "eval", "custom"]


@dataclass
class Span:
    """One timed unit of agent work."""

    name: str
    kind: SpanKind
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    parent_id: str | None = None
    started_at: float = field(default_factory=time.time)
    ended_at: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    @property
    def duration_s(self) -> float:
        """Elapsed seconds; measured to now if the span is still open."""
        return (self.ended_at or time.time()) - self.started_at

    def to_dict(self) -> dict[str, Any]:
        """Flat JSON-serialisable form, one line of the trace file."""
        return {
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "kind": self.kind,
            "started_at": self.started_at,
            "duration_s": round(self.duration_s, 4),
            "error": self.error,
            **{f"attr.{k}": v for k, v in self.attributes.items()},
        }


class Trace:
    """Collects spans for one run and writes them as JSONL.

    Use as a context manager so the file is flushed even when the run raises --
    which is exactly when you most want the trace::

        with Trace("video-brief") as tr:
            with tr.span("plan", kind="llm") as s:
                s.attributes["model"] = "claude-sonnet-5"
    """

    def __init__(self, name: str, *, write: bool = True, trace_dir: Path | None = None) -> None:
        self.name = name
        self.run_id = f"{time.strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:6]}"
        self.spans: list[Span] = []
        self._stack: list[str] = []
        self._write = write
        self._dir = trace_dir or (get_settings().trace_path() if write else None)

    @property
    def path(self) -> Path | None:
        """Where this trace will be written, or ``None`` in memory-only mode."""
        if self._dir is None:
            return None
        return self._dir / f"{self.name}-{self.run_id}.jsonl"

    @contextmanager
    def span(self, name: str, *, kind: SpanKind = "step", **attributes: Any) -> Iterator[Span]:
        """Open a span, nested under whatever span is currently open."""
        span = Span(
            name=name,
            kind=kind,
            parent_id=self._stack[-1] if self._stack else None,
            attributes=dict(attributes),
        )
        self.spans.append(span)
        self._stack.append(span.span_id)
        try:
            yield span
        except Exception as exc:
            # Record the failure on the span before it propagates: a trace that
            # stops at the point of failure is the one you need to read.
            span.error = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            span.ended_at = time.time()
            self._stack.pop()

    def event(self, name: str, **attributes: Any) -> None:
        """Record a zero-duration point of interest."""
        span = Span(
            name=name,
            kind="custom",
            parent_id=self._stack[-1] if self._stack else None,
            attributes=dict(attributes),
        )
        span.ended_at = span.started_at
        self.spans.append(span)

    def flush(self) -> Path | None:
        """Write every span to disk. Returns the file path, or ``None``."""
        path = self.path
        if path is None:
            return None
        with path.open("w", encoding="utf-8") as handle:
            for span in self.spans:
                handle.write(json.dumps(span.to_dict(), default=str) + "\n")
        return path

    def summary(self) -> str:
        """Compact per-kind breakdown, for printing at the end of a lab."""
        by_kind: dict[str, tuple[int, float]] = {}
        for span in self.spans:
            count, total = by_kind.get(span.kind, (0, 0.0))
            by_kind[span.kind] = (count + 1, total + span.duration_s)
        parts = [f"{k} x{c} {t:.1f}s" for k, (c, t) in sorted(by_kind.items())]
        errors = sum(1 for s in self.spans if s.error)
        error_note = f" · {errors} error{'s' if errors != 1 else ''}" if errors else ""
        return f"trace {self.name}: " + ", ".join(parts) + error_note

    def __enter__(self) -> Trace:
        """Enter the trace context."""
        return self

    def __exit__(self, *exc_info: object) -> None:
        """Flush on the way out, successful or not."""
        if self._write:
            self.flush()


#: A trace that records nothing, for code paths where tracing is optional.
#: Saves every caller an ``if trace is not None`` branch.
NULL_TRACE = Trace("null", write=False)
