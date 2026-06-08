"""Static checks for the Stage 2 historical-label loading planning closeout."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01_HISTORICAL_LABEL_LOADING_VALIDATION_PLANNING_CLOSEOUT_CHECKPOINT.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01"
ASSIGNMENT_HEADING = "## Machine-checkable historical-label loading planning closeout assignments"

ALLOWED_ASSIGNMENTS: dict[str, set[str]] = {
    "historical label loading planning closeout stage": {
        "stage_2_historical_label_loading_validation_planning_closeout_checkpoint",
    },
    "closeout status": {
        "v1_complete",
        "hold_for_review",
        "blocked_pending_gap",
        "unclear",
    },
    "planning artifact status": {
        "present",
        "missing",
        "not_applicable",
    },
    "planning boundary status": {
        "preserved",
        "violated",
        "unclear",
    },
    "planned contract coverage": {
        "static_fixture_reader_boundary_planned",
        "synthetic_real_fixture_distinction_planned",
        "source_provenance_validation_planned",
        "no_lookahead_validation_planned",
        "reviewer_note_validation_planned",
        "fail_closed_blocker_mapping_planned",
        "validation_posture_mapping_planned",
        "non_operational_test_only_boundary_planned",
    },
    "data posture": {
        "no_fixture_files_created",
        "no_fixture_files_modified",
        "no_historical_label_data_created",
        "no_generated_data_created",
        "no_loader_created",
        "no_runtime_data_access",
        "no_source_fetching",
        "planning_closeout_only",
    },
    "next gate category": {
        "hold",
        "targeted_loading_planning_refinement_if_gap_found",
        "active_state_update_if_needed",
        "historical_label_loading_implementation_approval_request_if_chosen",
        "ingestion_planning_approval_request_if_chosen",
        "scoring_backtesting_planning_approval_request_if_chosen",
        "runtime_observation_planning_approval_request_if_chosen",
        "trading_order_autonomy_later_explicit_approval_only",
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


def _planning_inventory_section(text: str) -> str:
    marker = "## Historical-label loading planning inventory\n"
    assert marker in text
    section_start = text.index(marker) + len(marker)
    next_heading = text.find("\n## ", section_start)
    assert next_heading != -1
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


def test_closeout_prd_exists_with_canonical_id_and_required_source_references() -> None:
    assert PRD_PATH.is_file()
    text = _prd_text()
    for required in (
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "MEG_ACTIVE_STATE",
        "WEATHER_BOT_PACKET",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-APPROVAL-01",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-01",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01",
        "Stage 2 skeleton closeout",
    ):
        assert required in text


def test_planning_inventory_lists_exactly_the_planning_artifacts() -> None:
    section = _planning_inventory_section(_prd_text())
    observed = [line.strip() for line in section.splitlines() if line.strip()]
    assert observed == [
        "- docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-APPROVAL-01_HISTORICAL_LABEL_LOADING_VALIDATION_PLANNING_APPROVAL_REQUEST.md",
        "- docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-01_STATIC_HISTORICAL_LABEL_LOADING_VALIDATION_PLANNING.md",
        "- tests/core/test_prd_p1_wx_stage2_historical_label_loading_approval_01.py",
        "- tests/core/test_prd_p1_wx_stage2_historical_label_loading_plan_01.py",
    ]


def test_closeout_only_scope_and_required_non_approval_language() -> None:
    text = _prd_text()
    required_phrases = (
        "This is a historical-label loading/validation planning closeout/checkpoint only",
        "Historical-label loading/validation planning v1 is complete for now",
        "Historical-label loading implementation is not approved",
        "No loader was created",
        "No fixture JSON files were read by source/runtime code",
        "No fixture JSON files were created or modified",
        "No fixture README files were created or modified",
        "No historical-label data files were created",
        "No generated data was created",
        "No ingestion was created or approved",
        "No provider/API connectors were created or approved",
        "No external API calls were created or approved",
        "No credentials/secrets/config loading was created or approved",
        "No forecast pulls were created or approved",
        "No scoring/probability scoring was created or approved",
        "No backtesting/paper simulation was created or approved",
        "No runtime observation was created or approved",
        "No trading/order placement/position sizing/autonomy was created or approved",
        "No production behavior was created or approved",
        "Future implementation requires a separate explicit implementation approval request",
        "Future ingestion requires a separate explicit approval request",
        "Future scoring/backtesting requires a separate explicit approval request",
        "Future runtime/trading requires a separate explicit approval request",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_separation_and_hold_posture_are_documented() -> None:
    text = _prd_text()
    for required in (
        "planned a non-operational reader boundary",
        "source/provenance checks",
        "access-date checks",
        "no-lookahead note checks",
        "reviewer-note checks",
        "fail-closed validation posture",
        "Planned separation from ingestion/connectors",
        "Planned separation from scoring/backtesting",
        "Planned separation from runtime/trading",
        "recommended posture is hold/checkpoint unless a concrete loading-planning gap is found or the user explicitly chooses a later approval/request/planning gate",
    ):
        assert required in text


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _prd_text()
    section = _assignment_section(text)
    assert section.strip()
    assert "## Acceptance criteria" not in section
    assert "v1_complete/hold_for_review" not in section
    assert "preserved/violated" not in section
    assert "source_backed/reviewer_inferred" not in section
    assert "confirmed/unclear" not in section


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


def test_normal_non_approval_prose_terms_are_allowed_outside_assignments() -> None:
    text = _prd_text()
    section = _assignment_section(text)
    for prose_term in ("approved", "mixed", "partial", "live", "production", "C++", "Rust"):
        assert prose_term in text
    for prose_term in ("approved", "mixed", "partial", "live", "C++", "Rust"):
        assert prose_term not in section


def test_closeout_prd_and_static_test_avoid_implementation_fragments() -> None:
    combined = _prd_text() + "\n" + Path(__file__).read_text(encoding="utf-8")
    lowered = combined.lower()
    for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS:
        assert fragment not in lowered
