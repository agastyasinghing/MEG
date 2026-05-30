"""Static closeout checks for PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = (
    REPO_ROOT
    / "docs"
    / "prd"
    / "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01_STAGE_2_SKELETON_CLOSEOUT_CHECKPOINT.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01"
MACHINE_HEADING = "## Machine-checkable Stage 2 skeleton closeout assignments"

ALLOWED_ASSIGNMENTS = {
    "closeout stage": {"stage_2_skeleton_closeout_checkpoint"},
    "closeout status": {"v1_complete", "hold_for_review", "blocked_pending_gap", "unclear"},
    "subphase artifact status": {"present", "missing", "not_applicable"},
    "boundary status": {"preserved", "violated", "unclear"},
    "next gate category": {
        "static_fixture_data_approval_request",
        "static_historical_label_fixture_planning",
        "static_fixture_implementation_if_approved",
        "historical_label_loading_validation_planning_if_approved",
        "provider_source_integration_planning_if_approved",
        "scoring_backtesting_planning_if_approved",
        "paper_simulation_planning_if_approved",
        "runtime_observation_planning_if_approved",
        "trading_order_autonomy_later_explicit_approval_only",
        "hold",
    },
    "non-approval category": {
        "historical_label_data",
        "fixtures_or_generated_data",
        "ingestion",
        "provider_integration",
        "connectors",
        "external_api_calls",
        "credentials_secrets_config",
        "forecast_pulls",
        "model_scoring",
        "probability_scoring",
        "backtesting",
        "paper_simulation",
        "runtime_observation",
        "trading_order_autonomy",
        "production_behavior",
        "cplusplus_rust_runtime",
        "other_unclear",
    },
    "evidence status": {"source_backed", "reviewer_inferred", "missing", "conflicting", "not_applicable"},
    "label confidence": {"confirmed", "unclear", "unknown"},
}

FORBIDDEN_EXAMPLES = {
    "v1_complete/hold_for_review",
    "preserved/violated",
    "source_backed/reviewer_inferred",
    "confirmed/unclear",
    "partial",
    "mixed",
    "likely_confirmed",
    "maybe",
    "approved",
    "configured",
    "available",
    "trade_ready",
    "auto_execute",
    "autonomous",
    "live",
    "production",
    "provider_ready",
    "model_ready",
    "backtest_ready",
    "ready_for_ingestion",
    "ready_for_scoring",
    "ready_for_runtime",
    "ready_for_trading",
    "implementation_ready",
    "ingestion_ready",
    "scoring_ready",
    "simulation_ready",
    "runtime_ready",
    "trading_ready",
    "approved_for_fixtures",
    "approved_for_ingestion",
    "approved_for_runtime",
    "approved_for_scoring",
    "approved_for_trading",
}


def _read_closeout() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    start = text.index(MACHINE_HEADING)
    remainder = text[start + len(MACHINE_HEADING) :]
    match = re.search(r"\n## ", remainder)
    if match is None:
        return remainder
    return remainder[: match.start()]


def _assignment_values(section: str) -> dict[str, list[str]]:
    observed = {name: [] for name in ALLOWED_ASSIGNMENTS}
    assignment_pattern = re.compile(r"^- (?P<name>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
    for match in assignment_pattern.finditer(section):
        name = match.group("name")
        value = match.group("value")
        assert name in ALLOWED_ASSIGNMENTS, f"Unexpected assignment name: {name}"
        observed[name].append(value)
    return observed


def test_closeout_prd_exists_with_canonical_id_and_required_references() -> None:
    assert PRD_PATH.is_file()
    text = _read_closeout()

    required = [
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "PRD-P1-WX-STAGE2-SKELETON-01",
        "PRD-P1-WX-STAGE2-SKELETON-02",
        "PRD-P1-WX-STAGE2-SKELETON-03",
        "meg/weather/stage2/historical_label.py",
        "tests/core/test_prd_p1_wx_stage2_skeleton_01_historical_label.py",
        "tests/core/test_prd_p1_wx_stage2_skeleton_02_validation_coverage.py",
        "tests/core/test_prd_p1_wx_stage2_skeleton_03_mapping_builder_validation.py",
    ]
    for expected in required:
        assert expected in text


def test_closeout_summarizes_scope_status_and_non_approvals() -> None:
    text = _read_closeout().lower()

    required_phrases = [
        "v1 complete",
        "hold for review",
        "supplied-metadata-only",
        "does not ingest",
        "no ingestion",
        "provider/api connectors",
        "external api calls",
        "credentials/secrets/config loading",
        "forecast pulls",
        "historical-label data",
        "fixtures",
        "generated data",
        "model scoring",
        "probability scoring",
        "backtesting",
        "runtime observation",
        "trading",
        "order placement",
        "autonomy",
        "future approval gates",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_required_sections_are_present() -> None:
    text = _read_closeout()
    sections = [
        "## 1. Status and scope",
        "## 2. Strategic framing",
        "## 3. Stage ladder position",
        "## 4. Stage 2 skeleton subphase inventory",
        "## 5. What the skeleton now supports",
        "## 6. Validation coverage completed",
        "## 7. Supplied-metadata-only boundary",
        "## 8. Fail-closed behavior summary",
        "## 9. Closed value sets preserved",
        "## 10. Explicit non-approval boundaries",
        "## 11. What remains unbuilt",
        "## 12. Future approval gates",
        "## 13. Recommended hold/checkpoint posture",
        "## 14. Allowed future next-step categories",
        "## 15. Forbidden future next-step categories",
        "## 16. Files covered by closeout",
        "## 17. Validation commands",
        "## 18. Later-ticket handoff",
        "## 19. Acceptance criteria",
    ]
    for section in sections:
        assert section in text


def test_machine_checkable_assignment_section_uses_only_closed_sets() -> None:
    text = _read_closeout()
    assert MACHINE_HEADING in text
    section = _machine_section(text)
    observed = _assignment_values(section)

    for name, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert observed[name], f"Missing assignments for {name}"
        assert set(observed[name]) <= allowed_values
        assert allowed_values <= set(observed[name]), f"Missing allowed values for {name}"


def test_forbidden_examples_are_documented_but_not_actual_assignments() -> None:
    text = _read_closeout()
    section = _machine_section(text)
    observed = _assignment_values(section)
    actual_values = {value for values in observed.values() for value in values}

    for forbidden in FORBIDDEN_EXAMPLES:
        assert forbidden in text
        assert forbidden not in actual_values


def test_machine_parser_is_section_scoped() -> None:
    text = _read_closeout()
    section = _machine_section(text)

    assert "Forbidden examples" not in section
    assert "partial" in text
    assert "partial" not in section
