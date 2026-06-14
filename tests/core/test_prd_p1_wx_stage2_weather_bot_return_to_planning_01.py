"""Static checks for Weather Bot return-to-planning checkpoint.

These tests use only the Python standard library and validate a docs/static-test-only
planning checkpoint. They do not approve or implement provider connectors, source
fetching, forecast pulls, scoring, backtesting, runtime behavior, execution,
trading, autonomy, production behavior, migrations, workflows, dependencies,
generated data, or fixture changes.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01_AFTER_ARCHITECTURE_ALIGNMENT_CLOSEOUT.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01"
NEXT_TICKET = "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01"
MACHINE_HEADING = "## Machine-checkable Weather Bot return assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Why Weather Bot can resume planning",
    "Architecture alignment closeout dependency",
    "Weather Bot completed work summary",
    "Current Weather Bot stage posture",
    "Offline real-ingestion implementation posture",
    "Canonical identifier posture",
    "Explicit non-approval boundaries",
    "Next safe Weather Bot planning tracks",
    "Blocked implementation work",
    "Recommended next ticket",
    "Machine-checkable Weather Bot return assignments",
    "Acceptance criteria",
)

ALLOWED_ASSIGNMENTS = {
    "weather bot return stage": {"return_to_weather_bot_planning_after_architecture_alignment"},
    "architecture alignment status": {
        "meg_arch_align_08_complete",
        "architecture_detour_closed_out",
        "canonical_id_posture_recorded",
        "market_id_compatibility_posture_recorded",
    },
    "weather bot posture": {
        "weather_bot_planning_can_resume",
        "gated_planning_only",
        "implementation_not_approved",
        "provider_source_scoring_runtime_trading_not_approved",
    },
    "offline ingestion posture": {
        "offline_real_ingestion_skeleton_exists",
        "offline_real_ingestion_drift_guard_hardened",
        "offline_real_ingestion_closeout_exists",
        "real_ingestion_runtime_not_approved",
    },
    "provider source posture": {
        "provider_connectors_not_approved",
        "source_fetching_not_approved",
        "forecast_pulls_not_approved",
        "provider_source_planning_only",
    },
    "scoring runtime posture": {
        "scoring_not_approved",
        "backtesting_not_approved",
        "runtime_behavior_not_approved",
        "trading_not_approved",
        "autonomy_not_approved",
        "production_not_approved",
    },
    "implementation posture": {
        "planning_checkpoint_only",
        "docs_static_test_only",
        "no_provider_connector",
        "no_source_fetching",
        "no_forecast_pull",
        "no_scoring_backtesting",
        "no_runtime_behavior",
        "no_execution_trading",
        "no_autonomy",
        "no_production_behavior",
    },
    "recommended next track": {
        "provider_source_compatibility_planning",
        "source_fetching_approval_request_planning",
        "forecast_resolution_source_mapping_planning",
        "scoring_backtesting_approval_request_planning",
        "stage2_active_state_refresh",
    },
    "evidence status": {"source_backed", "reviewer_inferred", "missing", "conflicting", "not_applicable"},
    "label confidence": {"confirmed", "unclear", "unknown"},
}

ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)


def _read_artifact() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, f"Missing section: {heading}"
    section = match.group("section")
    assert section.strip(), f"Section is empty: {heading}"
    return section


def _machine_section(text: str) -> str:
    match = re.search(
        rf"^{re.escape(MACHINE_HEADING)}\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, "Machine-checkable Weather Bot return assignment section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable Weather Bot return assignment section is empty"
    return section


def _assignments(text: str) -> dict[str, set[str]]:
    section = _machine_section(text)
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def test_planning_document_exists_and_canonical_id_appears() -> None:
    assert ARTIFACT_PATH.exists()
    assert CANONICAL_ID in _read_artifact()


def test_all_required_sections_appear() -> None:
    text = _read_artifact()
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_architecture_alignment_08_and_weather_bot_return_are_stated() -> None:
    text = _read_artifact()
    assert "MEG-ARCH-ALIGN-08 is complete" in text
    assert "architecture-alignment detour is closed out enough to return to Weather Bot planning" in text
    assert "Weather Bot may resume gated planning/approval work" in text


def test_return_is_limited_to_planning_approval_only() -> None:
    text = _read_artifact()
    assert "planning checkpoint only" in text
    assert "docs/static-test-only" in text
    assert "Returning to Weather Bot means returning to planning/approval only, not implementation." in text
    assert "No implementation is approved by this checkpoint." in text


def test_completed_weather_bot_work_summary_appears() -> None:
    section = _section(_read_artifact(), "Weather Bot completed work summary")
    required_phrases = (
        "Static fixture and loading/validation path exists.",
        "Static ingestion boundary skeleton exists.",
        "Real-ingestion planning exists.",
        "Weather Bot offline real-ingestion skeleton exists.",
        "Drift-guard hardening exists.",
        "Weather Bot real-ingestion implementation closeout exists.",
        "Offline real-ingestion implementation closeout exists.",
        "Architecture alignment closeout now clears the repo-level identifier detour.",
    )
    for phrase in required_phrases:
        assert phrase in section


def test_offline_real_ingestion_skeleton_and_closeout_are_mentioned() -> None:
    text = _read_artifact()
    assert "Weather Bot offline real-ingestion skeleton exists" in text
    assert "Weather Bot real-ingestion implementation closeout exists" in text
    assert "Offline real-ingestion implementation closeout exists" in text


def test_provider_source_forecast_remain_unapproved() -> None:
    text = _read_artifact()
    for phrase in (
        "Provider connectors are not approved.",
        "Source fetching is not approved.",
        "Forecast pulls are not approved.",
    ):
        assert phrase in text


def test_scoring_runtime_trading_autonomy_production_remain_unapproved() -> None:
    text = _read_artifact()
    for phrase in (
        "Scoring is not approved.",
        "Backtesting is not approved.",
        "Runtime behavior is not approved.",
        "Trading is not approved.",
        "Autonomy is not approved.",
        "Production behavior is not approved.",
    ):
        assert phrase in text


def test_no_implementation_is_approved_or_implemented() -> None:
    text = _read_artifact()
    for phrase in (
        "No provider connector is implemented.",
        "No source fetching is implemented.",
        "No forecast pull is implemented.",
        "No scoring/backtesting is implemented.",
        "No runtime/trading/autonomy behavior is implemented.",
        "No production behavior is implemented.",
        "No implementation is approved or implemented by this checkpoint.",
    ):
        assert phrase in text


def test_recommended_next_ticket_is_provider_source_compatibility_planning() -> None:
    section = _section(_read_artifact(), "Recommended next ticket")
    assert NEXT_TICKET in section
    assert "planning/approval only" in section


def test_machine_checkable_section_exists_and_parser_is_section_scoped() -> None:
    text = _read_artifact()
    section = _machine_section(text)
    assert "## Acceptance criteria" not in section
    assert "- weather bot return stage: return_to_weather_bot_planning_after_architecture_alignment" in section

    synthetic_text = (
        f"{MACHINE_HEADING}\n"
        "- weather bot return stage: return_to_weather_bot_planning_after_architecture_alignment\n"
        "## Acceptance criteria\n"
        "- weather bot return stage: unapproved_actual_value\n"
    )
    assert _assignments(synthetic_text) == {
        "weather bot return stage": {"return_to_weather_bot_planning_after_architecture_alignment"}
    }


def test_every_allowed_closed_set_machine_checkable_value_appears() -> None:
    assignments = _assignments(_read_artifact())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field] == allowed_values


def test_no_unapproved_actual_assignment_values_appear() -> None:
    assignments = _assignments(_read_artifact())
    for field, actual_values in assignments.items():
        assert field in ALLOWED_ASSIGNMENTS
        assert actual_values <= ALLOWED_ASSIGNMENTS[field]
