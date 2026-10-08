"""Writing eval results to a file you can commit.

A scorecard in version control turns "I think it got better" into a diff.
Reviewers see the number move, the failing case ids change, and the cost change
-- all in the same pull request as the prompt edit that caused it.

Markdown rather than JSON because the primary reader is a person, and GitHub
renders it inline in the diff.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from agentic_ai.evals.runner import EvalReport


def to_markdown(report: EvalReport, *, include_outputs: bool = False) -> str:
    """Render ``report`` as a Markdown scorecard.

    Args:
        report: The run to render.
        include_outputs: Append each failing case's full output. Useful while
            debugging, too noisy to commit.

    Returns:
        Markdown text.
    """
    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        f"# Scorecard: {report.system_name}",
        "",
        f"- **Dataset**: `{report.dataset_name}` ({report.total} cases)",
        f"- **Pass rate**: {report.passed}/{report.total} ({report.pass_rate:.0%})",
        f"- **Mean score**: {report.mean_score:.2f}",
        f"- **Latency**: {report.mean_duration_s:.1f}s per case",
        f"- **Run at**: {stamp}",
    ]
    if report.judge_usage.total_tokens:
        lines.append(f"- **Judge tokens**: {report.judge_usage.total_tokens:,}")
    if report.errored:
        lines.append(f"- **Errored**: {len(report.errored)} case(s)")
    lines.append("")

    failures = report.failures_by_check()
    if failures:
        lines += [
            "## Failures by check",
            "",
            "| Check | Cases failing |",
            "| --- | --- |",
            *(f"| `{name}` | {count} |" for name, count in failures.items()),
            "",
            "> Read the top row first. One check dominating usually means one",
            "> fixable cause, not a generally weak system.",
            "",
        ]

    lines += [
        "## Cases",
        "",
        "| Case | Result | Score | Time | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in report.results:
        mark = "pass" if result.passed else "**FAIL**"
        note = result.error or "; ".join(s.reason for s in result.scores.failures if s.reason)
        lines.append(
            f"| `{result.case.id}` | {mark} | {result.scores.overall:.2f} | "
            f"{result.duration_s:.1f}s | {_cell(note)} |"
        )
    lines.append("")

    if include_outputs and any(not r.passed for r in report.results):
        lines += ["## Failing outputs", ""]
        for result in report.results:
            if result.passed:
                continue
            lines += [
                f"### `{result.case.id}`",
                "",
                f"**Input**: {result.case.input}",
                "",
                "```text",
                result.output.strip() or "(empty)",
                "```",
                "",
            ]

    return "\n".join(lines)


def _cell(text: str, limit: int = 140) -> str:
    """Make text safe for one Markdown table cell."""
    flat = " ".join(text.split()).replace("|", "\\|")
    return flat[:limit] + ("..." if len(flat) > limit else "")


def write_scorecard(
    report: EvalReport,
    path: str | Path,
    *,
    include_outputs: bool = False,
) -> Path:
    """Write a Markdown scorecard, creating parent directories as needed."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(to_markdown(report, include_outputs=include_outputs), encoding="utf-8")
    return destination
