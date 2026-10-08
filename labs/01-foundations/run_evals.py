#!/usr/bin/env python3
"""Run Lab 01's eval set against both systems and write scorecards.

This is the lab's acceptance test. The module claims that an iterative,
multi-step workflow beats a single prompt. That claim is either visible in
these numbers or it is not true for this task.

    make eval-01

Costs a few cents per system. Both systems share one eval set and one judge,
so the comparison is fair.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB_DIR))

from systems import research_agent, single_prompt

from agentic_ai.evals import (
    EvalCase,
    EvalDataset,
    Score,
    compare,
    evaluate,
    write_scorecard,
)
from agentic_ai.evals.runner import CaseResult
from agentic_ai.llm import available_providers

CASES = LAB_DIR / "evals" / "video_brief_cases.yaml"
MIN_DISTINCT_SOURCES = 2


def cites_sources(output: str, _case: EvalCase) -> list[Score]:
    """Require at least two distinct cited URLs.

    The failure this lab most wants to surface is confident prose with nothing
    behind it. A rubric judge catches some of it; counting URLs catches it for
    free, every time, and cannot be talked out of the result.
    """
    import re

    urls = set(re.findall(r"https?://[^\s\)\]\>,]+", output))
    # An admission of thin sourcing is the correct answer to the `obscure`
    # cases, so do not penalise it for lacking citations.
    admits = any(
        phrase in output.lower()
        for phrase in ("could not find", "no reliable", "not find reliable", "unable to find")
    )
    ok = len(urls) >= MIN_DISTINCT_SOURCES or admits
    return [
        Score(
            name="cites_sources",
            value=1.0 if ok else 0.0,
            reason="" if ok else f"found {len(urls)} distinct URL(s), need {MIN_DISTINCT_SOURCES}",
        )
    ]


def progress(result: CaseResult) -> None:
    """Print one line per case so a long run is not a blank terminal."""
    mark = "ok  " if result.passed else "FAIL"
    reasons = "; ".join(s.reason for s in result.scores.failures if s.reason)
    print(f"  [{mark}] {result.case.id}  {result.duration_s:5.1f}s  {reasons[:90]}")


def main() -> int:
    """Run both systems and write scorecards. Returns a process exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-judge",
        action="store_true",
        help="skip LLM judging -- fast and free, but only checks the deterministic parts",
    )
    parser.add_argument(
        "--only",
        choices=["baseline", "agentic"],
        help="run just one system",
    )
    args = parser.parse_args()

    if not available_providers():
        print(
            "No model provider configured. Add one key to .env -- see docs/start-here/setup.md",
            file=sys.stderr,
        )
        return 1

    dataset = EvalDataset.from_yaml(CASES)
    print(f"Eval set: {dataset.name}, {len(dataset)} cases")
    print(f"Judge: {'off' if args.no_judge else 'on'}\n")

    reports = {}

    if args.only != "agentic":
        print("Running baseline (single prompt, no tools)...")
        reports["baseline"] = evaluate(
            single_prompt,
            dataset,
            system_name="single-prompt",
            use_judge=not args.no_judge,
            extra_checks=[cites_sources],
            on_case=progress,
        )
        print()

    if args.only != "baseline":
        print("Running agentic (loop with search + fetch)...")
        reports["agentic"] = evaluate(
            research_agent,
            dataset,
            system_name="agentic",
            use_judge=not args.no_judge,
            extra_checks=[cites_sources],
            on_case=progress,
        )
        print()

    out_dir = LAB_DIR / "evals"
    for key, report in reports.items():
        print(report.summary())
        path = write_scorecard(report, out_dir / f"{key}.scorecard.md", include_outputs=False)
        print(f"  scorecard -> {path.relative_to(LAB_DIR.parents[1])}")

        failures = report.failures_by_check()
        if failures:
            top = ", ".join(f"{name} ({count})" for name, count in list(failures.items())[:3])
            print(f"  top failing checks: {top}")
        print()

    if len(reports) == 2:
        print("=" * 68)
        print(compare(reports["baseline"], reports["agentic"]))
        print("=" * 68)
        print(
            "\nIf the agentic system did not clearly win, that is a result, not a\n"
            "bug. Read the per-case rows: it usually wins on `current` and\n"
            "`obscure` cases and ties on `definition` ones -- which is an\n"
            "argument for routing, not for always using the agent."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
