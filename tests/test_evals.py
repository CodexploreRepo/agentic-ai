"""The eval harness: loading cases, scoring, comparing, reporting."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_ai.errors import ConfigError
from agentic_ai.evals import (
    EvalCase,
    EvalDataset,
    check_contains,
    check_non_empty,
    compare,
    evaluate,
    to_markdown,
    write_scorecard,
)

DATASET_YAML = """
name: demo
cases:
  - id: d-01
    input: What is MCP?
    expect_contains: ["Model Context Protocol"]
    tags: [definition]
  - id: d-02
    input: Summarise agent loops
    expect_absent: ["As an AI language model"]
    tags: [style]
"""


@pytest.fixture
def dataset(tmp_path: Path) -> EvalDataset:
    path = tmp_path / "cases.yaml"
    path.write_text(DATASET_YAML, encoding="utf-8")
    return EvalDataset.from_yaml(path)


def test_cases_load_from_yaml(dataset: EvalDataset) -> None:
    assert dataset.name == "demo"
    assert len(dataset) == 2
    assert dataset.cases[0].expect_contains == ("Model Context Protocol",)


def test_missing_file_says_so(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="not found"):
        EvalDataset.from_yaml(tmp_path / "nope.yaml")


def test_duplicate_ids_are_rejected(tmp_path: Path) -> None:
    # Duplicate ids silently break per-case tracking across runs, which is the
    # main thing an eval set is for.
    path = tmp_path / "dupes.yaml"
    path.write_text("cases:\n  - {id: a, input: x}\n  - {id: a, input: y}\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="duplicate case ids"):
        EvalDataset.from_yaml(path)


def test_tag_filter_slices_the_set(dataset: EvalDataset) -> None:
    assert len(dataset.filter_by_tag("definition")) == 1


def test_required_substring_check() -> None:
    case = EvalCase(id="x", input="q", expect_contains=("needle",))
    assert check_contains("a NEEDLE here", case)[0].passed
    assert not check_contains("nothing", case)[0].passed


def test_forbidden_substring_check() -> None:
    case = EvalCase(id="x", input="q", expect_absent=("sorry",))
    assert check_contains("fine", case)[0].passed
    assert not check_contains("I am Sorry", case)[0].passed


def test_short_output_fails_the_non_empty_check() -> None:
    # Catches the truncated fragment an agent returns when it hits its step limit.
    assert not check_non_empty("hi").passed
    assert check_non_empty("x" * 100).passed


def test_evaluate_scores_every_case(dataset: EvalDataset) -> None:
    report = evaluate(
        lambda _input: "The Model Context Protocol is a standard for tool access." * 2,
        dataset,
        system_name="good",
        use_judge=False,
    )
    assert report.total == 2
    assert report.pass_rate == 1.0


def test_a_crashing_system_is_recorded_not_propagated(dataset: EvalDataset) -> None:
    def broken(_input: str) -> str:
        raise RuntimeError("nope")

    report = evaluate(broken, dataset, use_judge=False)
    assert report.total == 2
    assert report.pass_rate == 0.0
    assert len(report.errored) == 2


def test_failures_are_tallied_by_check(dataset: EvalDataset) -> None:
    report = evaluate(lambda _input: "x" * 100, dataset, use_judge=False)
    tally = report.failures_by_check()
    assert tally.get("contains") == 1


def test_extra_checks_are_applied(dataset: EvalDataset) -> None:
    from agentic_ai.evals.judges import Score

    def must_cite(output: str, _case: EvalCase) -> list[Score]:
        return [Score(name="cites", value=1.0 if "http" in output else 0.0)]

    report = evaluate(lambda _i: "x" * 100, dataset, use_judge=False, extra_checks=[must_cite])
    assert report.failures_by_check().get("cites") == 2


def test_compare_calls_a_one_case_swing_noise(dataset: EvalDataset) -> None:
    # On a 2-case set nothing is significant; the helper must say so rather
    # than reporting a dramatic percentage.
    good = evaluate(lambda _i: "Model Context Protocol " * 10, dataset, use_judge=False)
    bad = evaluate(lambda _i: "x" * 100, dataset, use_judge=False)
    assert "no clear difference" in compare(good, bad) or "worse" in compare(good, bad)


def test_scorecard_renders_and_writes(dataset: EvalDataset, tmp_path: Path) -> None:
    report = evaluate(lambda _i: "x" * 100, dataset, system_name="v1", use_judge=False)
    markdown = to_markdown(report, include_outputs=True)
    assert "# Scorecard: v1" in markdown
    assert "d-01" in markdown
    assert "Failures by check" in markdown

    written = write_scorecard(report, tmp_path / "out" / "card.md")
    assert written.exists()


def test_pipes_in_output_do_not_break_the_table(dataset: EvalDataset) -> None:
    case = EvalCase(id="p", input="q", expect_contains=("a|b",))
    report = evaluate(lambda _i: "x" * 100, EvalDataset("piped", [case]), use_judge=False)
    row = next(line for line in to_markdown(report).splitlines() if "`p`" in line)
    # The pipe must be escaped, leaving exactly six unescaped cell delimiters.
    assert "a\\|b" in row
    assert row.replace("\\|", "").count("|") == 6
