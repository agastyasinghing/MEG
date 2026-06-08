"""Static checks for the Stage 2 historical-label loading planning PRD."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-01_STATIC_HISTORICAL_LABEL_LOADING_VALIDATION_PLANNING.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-01"
ASSIGNMENT_HEADING = "## Machine-checkable historical-label loading planning assignments"

ALLOWED_ASSIGNMENTS: dict[str, set[str]] = {
    "historical label loading planning stage": {
        "stage_2_static_historical_label_loading_validation_planning",
    },
    "planning status": {
        "planning_prepared",
        "implementation_not_approved",
        "loader_not_created",
        "human_review_required",
        "blocked_pending_fix",
        "unclear",
    },
    "planned contract category": {
        "static_fixture_reader_boundary",
        "synthetic_fixture_distinction",
        "real_source_backed_fixture_distinction",
        "source_provenance_validation_boundary",
        "no_lookahead_validation_boundary",
        "reviewer_note_validation_boundary",
        "fail_closed_blocker_mapping",
        "validation_posture_mapping",
        "non_operational_test_only_boundary",
    },
    "planned input category": {
        "synthetic_fixture_json",
        "real_source_backed_fixture_json",
        "fixture_readme",
        "source_note",
        "access_date",
        "no_lookahead_note",
        "reviewer_note",
        "validation_posture",
        "not_applicable",
    },
    "planned validation posture": {
        "pass",
        "caution",
        "blocked",
        "unknown",
        "not_applicable",
    },
    "planned blocker category": {
        "missing_required_field",
        "invalid_closed_set_value",
        "missing_source_note",
        "missing_access_date",
        "missing_no_lookahead_note",
        "missing_reviewer_note",
        "source_conflict",
        "unsupported_resolution_source",
        "venue_rule_mismatch",
        "synthetic_real_fixture_confusion",
        "runtime_or_ingestion_drift",
        "scoring_or_backtesting_drift",
        "trading_or_autonomy_drift",
        "other_unclear",
    },
    "boundary status": {
        "preserved",
        "not_approved",
        "explicitly_out_of_scope",
        "separate_human_approval_required",
        "blocked",
    },
    "future ticket permission": {
        "may_request_loader_implementation_approval_later",
        "must_not_create_loader_now",
        "must_not_create_ingestion",
        "must_not_create_connectors",
        "must_not_create_runtime",
        "must_not_create_scoring",
        "must_not_create_backtesting",
        "must_not_create_trading",
        "blocked_until_human_decision",
    },
    "data posture": {
        "no_fixture_files_created",
        "no_fixture_files_modified",
        "no_historical_label_data_created",
        "no_generated_data_created",
        "no_loader_created",
        "no_runtime_data_access",
        "no_source_fetching",
        "planning_only",
    },
    "non-approval category": {
        "historical_label_loading_implementation",
        "real_historical_label_data_expansion",
        "generated_data",
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
    "evidence status": {
        "source_backed",
        "reviewer_inferred",
        "missing",
        "conflicting",
        "not_applicable",
    },
    "label confidence": {
        "confirmed",
        "unclear",
        "unknown",
    },
}

FORBIDDEN_EXAMPLES = {
    "planning_prepared/implementation_not_approved",
    "preserved/not_approved",
    "pass/caution",
    "blocked/unknown",
    "confirmed/unclear",
    "partial",
    "mixed",
    "likely_confirmed",
    "maybe",
    "approved",
    "configured",
    "available",
    "loader_ready",
    "data_ready",
    "ingestion_ready",
    "scoring_ready",
    "runtime_ready",
    "trading_ready",
    "production_ready",
    "provider_ready",
    "model_ready",
    "back" + "test_ready",
    "ready_for_loading",
    "ready_for_ingestion",
    "ready_for_scoring",
    "ready_for_runtime",
    "ready_for_trading",
    "approved_for_loading",
    "approved_for_ingestion",
    "approved_for_runtime",
    "approved_for_scoring",
    "approved_for_trading",
    "trade_ready",
    "auto" + "_execute",
    "aut" + "onomous",
    "live",
    "production",
}

FORBIDDEN_IMPLEMENTATION_FRAGMENTS = (
    "os." + "environ",
    "load_" + "dot" + "env",
    "dot" + "env",
    "requests" + ".",
    "http" + "x.",
    "aio" + "http",
    "urllib." + "request",
    "api_" + "key",
    "secret_" + "key",
    "weather_" + "api_" + "key",
    "fast" + "api",
    "fl" + "ask",
    "sql" + "alchemy",
    "pan" + "das",
    "pol" + "ars",
    "duck" + "db",
    "read_" + "csv",
    "to_" + "csv",
    "json." + "load",
    "json" + "lines",
    "par" + "quet",
    "pre" + "dict",
)


def _prd_text() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def _assignment_section(text: str) -> str:
    marker = ASSIGNMENT_HEADING + "\n"
    assert marker in text
    section_start = text.index(marker) + len(marker)
    next_heading = text.find("\n## ", section_start)
    if next_heading == -1:
        return text[section_start:]
    return text[section_start:next_heading]


def _parsed_assignments() -> dict[str, set[str]]:
    section = _assignment_section(_prd_text())
    parsed = {prefix: set() for prefix in ALLOWED_ASSIGNMENTS}
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        assert line.startswith("- "), line
        body = line[2:]
        prefix, separator, value = body.partition(": ")
        assert separator == ": ", line
        assert prefix in ALLOWED_ASSIGNMENTS, line
        parsed[prefix].add(value)
    return parsed


def test_planning_prd_exists_with_canonical_id_and_source_references() -> None:
    assert PRD_PATH.is_file()
    text = _prd_text()
    for required in (
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "MEG_ACTIVE_STATE",
        "WEATHER_BOT_PACKET",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-APPROVAL-01",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01",
        "Stage 2 skeleton closeout",
    ):
        assert required in text


def test_planning_only_scope_and_required_non_approval_language() -> None:
    text = _prd_text()
    required_phrases = (
        "This is historical-label loading/validation planning only",
        "Historical-label loading implementation is not approved",
        "No loader is created",
        "No fixture JSON files are read by source/runtime code",
        "No fixture JSON files are created or modified",
        "No fixture README files are created or modified",
        "No historical-label data files are created",
        "No generated data is created",
        "No ingestion is created or approved",
        "No provider/API connectors are created or approved",
        "No external API calls are created or approved",
        "No credentials/secrets/config loading is created or approved",
        "No forecast pulls are created or approved",
        "No scoring or probability scoring is created or approved",
        "No backtesting or paper simulation is created or approved",
        "No runtime observation is created or approved",
        "No trading, order placement, position sizing, or autonomy is created or approved",
        "No production behavior is created or approved",
        "Future implementation requires a separate explicit implementation approval request",
        "Future ingestion requires a separate explicit approval request",
        "Future scoring/backtesting requires a separate explicit approval request",
        "Future runtime/trading requires a separate explicit approval request",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_planned_validation_boundaries_and_separation_are_documented() -> None:
    text = _prd_text()
    for required in (
        "Source/provenance checks",
        "Access-date checks",
        "No-lookahead note checks",
        "Reviewer-note checks",
        "fail closed",
        "Planned separation from ingestion",
        "Planned separation from provider/API connectors",
        "Planned separation from scoring/backtesting",
        "Planned separation from runtime/trading",
        "refuse to fetch, scrape, poll, enrich, or connect to a provider",
        "Refuse to turn fixture examples into operational datasets",
    ):
        assert required in text


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _prd_text()
    section = _assignment_section(text)
    assert section.strip()
    assert "## Acceptance criteria" not in section
    assert "planning_prepared/implementation_not_approved" not in section
    assert "preserved/not_approved" not in section
    assert "pass/caution" not in section


def test_closed_set_assignments_use_only_allowed_values_and_cover_every_value() -> None:
    parsed = _parsed_assignments()
    assert set(parsed) == set(ALLOWED_ASSIGNMENTS)
    for prefix, allowed_values in ALLOWED_ASSIGNMENTS.items():
        observed = parsed[prefix]
        assert observed <= allowed_values, f"Unexpected values for {prefix}: {observed - allowed_values}"
        assert observed == allowed_values, f"Missing values for {prefix}: {allowed_values - observed}"


def test_forbidden_examples_are_documented_but_not_actual_assignments() -> None:
    text = _prd_text()
    actual_values = {value for values in _parsed_assignments().values() for value in values}
    for example in FORBIDDEN_EXAMPLES:
        assert example in text
        assert example not in actual_values


def test_planning_prd_and_static_test_avoid_implementation_fragments() -> None:
    combined = _prd_text() + "\n" + Path(__file__).read_text(encoding="utf-8")
    lowered = combined.lower()
    for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS:
        assert fragment not in lowered
