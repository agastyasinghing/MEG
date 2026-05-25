"""Static contract checks for PRD-P1-WX-04 weather summary/status observability planning."""

from __future__ import annotations

from pathlib import Path
import re

DOC_PATH = Path("docs/prd/PRD-P1-WX-04_WEATHER_BOT_RESULT_STATUS_OBSERVABILITY_SUMMARY_CONTRACT.md")

ALLOWED = {
    "readiness state": {"missing", "disabled", "unapproved", "invalid", "ready"},
    "summary severity": {"info", "caution", "blocked"},
    "review posture": {"informational", "review_only", "blocked"},
}

FORBIDDEN_MACHINE_VALUES = {
    "missing/invalid",
    "disabled/unapproved",
    "ready/disabled",
    "info/caution",
    "caution/blocked",
    "informational/review_only",
    "review_only/blocked",
    "partial",
    "mixed",
    "ready_with_warnings",
    "maybe_ready",
    "approved",
    "configured",
    "available",
    "unknown",
    "warning",
    "error",
    "critical",
    "success",
    "ok",
    "actionable",
    "trade_ready",
    "auto_execute",
    "autonomous",
    "live",
}


def _text() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    match = re.search(
        r"^## Machine-checkable summary/status assignments\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, "Missing required machine-checkable assignment section heading."
    return match.group("section")


def _parse_assignments(section: str) -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {field: [] for field in ALLOWED}
    for field in ALLOWED:
        pattern = rf"{re.escape(field)}:\s*([a-z0-9_/-]+)"
        parsed[field] = [m.group(1) for m in re.finditer(pattern, section.lower())]
    return parsed


def test_prd_exists_and_core_references_present() -> None:
    assert DOC_PATH.exists(), f"Missing PRD document: {DOC_PATH}"
    lower = _text().lower()

    required_terms = [
        "prd-p1-wx-04",
        "prd-p1-wx-01",
        "prd-p1-wx-02",
        "prd-p1-wx-03",
        "result/status/observability",
        "summary contract",
        "closed summary/status field vocabulary",
        "machine-checkable summary/status assignments",
        "safe observability",
        "human-review",
        "non-goals",
        "wx-research-01",
        "wx-research-02",
        "wx-research-03",
        "wx-research-04",
        "wx-prd-synth-01",
        "opus",
        "forbidden summary/status values",
    ]
    missing = [term for term in required_terms if term not in lower]
    assert not missing, f"Missing required terms: {missing}"


def test_machine_checkable_assignments_use_only_closed_sets() -> None:
    section = _machine_section(_text())
    parsed = _parse_assignments(section)

    for field, allowed_values in ALLOWED.items():
        values = parsed[field]
        assert values, f"No machine-checkable assignments found for {field}."

        invalid = sorted({value for value in values if value not in allowed_values})
        assert not invalid, f"Invalid parsed values for {field}: {invalid}"

        forbidden_present = sorted({value for value in values if value in FORBIDDEN_MACHINE_VALUES})
        assert not forbidden_present, f"Forbidden machine-checkable values detected for {field}: {forbidden_present}"

        missing_allowed = sorted(allowed_values - set(values))
        assert not missing_allowed, f"Machine-checkable assignments missing {field} values: {missing_allowed}"


def test_non_approval_boundaries_present() -> None:
    lower = _text().lower()
    required_non_approval_terms = [
        "status implementation",
        "observability implementation",
        "dashboard implementation",
        "metrics/logging implementation",
        "config-loading implementation",
        "environment-variable loading",
        "secret reading",
        "connector implementation",
        "external api calls",
        "credentials",
        "runtime execution",
        "forecast pulls",
        "trading",
        "order placement",
        "autonomy",
    ]

    missing = [term for term in required_non_approval_terms if term not in lower]
    assert not missing, f"Missing non-approval boundary terms: {missing}"
