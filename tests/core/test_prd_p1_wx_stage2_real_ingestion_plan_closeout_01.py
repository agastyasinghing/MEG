"""Static checks for PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01.

These tests validate the Weather Bot Stage 2 real ingestion boundary planning
closeout without creating ingestion, connectors, source fetching, scoring,
runtime behavior, or data artifacts.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / (
    "docs/prd/"
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01_"
    "REAL_INGESTION_BOUNDARY_PLANNING_CLOSEOUT_CHECKPOINT.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01"
ASSIGNMENT_HEADING = "## Machine-checkable real ingestion boundary planning closeout assignments"
FORBIDDEN_HEADING = "## Forbidden real ingestion planning closeout values"
INVENTORY_HEADING = "## Planning inventory"

EXPECTED_INVENTORY = [
    "docs/prd/PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01_REAL_INGESTION_BOUNDARY_PLANNING.md",
    "tests/core/test_prd_p1_wx_stage2_real_ingestion_plan_01.py",
]

REQUIRED_SECTIONS = (
    "Status and scope",
    "Strategic framing",
    "Stage ladder position",
    "Planning inventory",
    "Real ingestion boundary planning summary",
    "Source-intake boundary summary",
    "Provider/source category taxonomy summary",
    "Allowed source-intake mode summary",
    "Prohibited source-intake mode summary",
    "Pre-fetch human approval gate summary",
    "Source identity and provenance planning summary",
    "Access-date and retrieval-context planning summary",
    "No-lookahead safeguard summary",
    "Separation boundary summary",
    "Fail-closed blocker taxonomy summary",
    "Handoff rule summary",
    "What this closeout confirms",
    "What remains unbuilt",
    "Explicit non-approval boundaries",
    "Future gates",
    "Recommended hold/checkpoint posture",
    "Closed real ingestion planning closeout vocabulary",
    "Forbidden real ingestion planning closeout values",
    "Machine-checkable real ingestion boundary planning closeout assignments",
    "Acceptance criteria",
    "Later-ticket handoff",
)

ALLOWED_ASSIGNMENTS = {
    "real ingestion planning closeout stage": {
        "stage_2_real_ingestion_boundary_planning_closeout_checkpoint",
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
    "planned coverage": {
        "real_ingestion_boundary_vocabulary_planned",
        "source_intake_boundary_vocabulary_planned",
        "provider_source_category_taxonomy_planned",
        "allowed_source_intake_mode_planned",
        "prohibited_source_intake_mode_planned",
        "pre_fetch_human_approval_gate_planned",
        "source_identity_requirement_planned",
        "source_provenance_requirement_planned",
        "access_date_requirement_planned",
        "retrieval_context_requirement_planned",
        "no_lookahead_requirement_planned",
        "static_descriptor_real_ingestion_separation_planned",
        "static_loader_real_ingestion_separation_planned",
        "static_skeleton_real_ingestion_separation_planned",
        "fail_closed_blocker_taxonomy_planned",
        "provider_connector_handoff_planned",
        "source_fetching_handoff_planned",
        "scoring_backtesting_handoff_planned",
        "runtime_trading_handoff_planned",
    },
    "data posture": {
        "no_fixture_files_created",
        "no_fixture_files_modified",
        "no_historical_label_data_created",
        "no_generated_data_created",
        "no_loader_expansion_created",
        "no_static_ingestion_skeleton_expansion_created",
        "no_real_ingestion_artifacts_created",
        "no_runtime_data_access",
        "no_source_fetching",
        "planning_closeout_only",
    },
    "next gate category": {
        "hold",
        "targeted_real_ingestion_planning_refinement_if_gap_found",
        "active_state_update_if_needed",
        "real_ingestion_implementation_approval_request_if_chosen",
        "provider_connector_planning_approval_request_if_chosen",
        "source_fetching_planning_approval_request_if_chosen",
        "scoring_backtesting_planning_approval_request_if_chosen",
        "runtime_observation_planning_approval_request_if_chosen",
        "trading_order_autonomy_later_explicit_approval_only",
    },
    "non-approval category": {
        "real_ingestion_implementation",
        "provider_integration",
        "connectors",
        "source_fetching",
        "external_api_calls",
        "credentials_secrets_config",
        "forecast_pulls",
        "scraping_polling_streaming",
        "scheduling_queues_jobs",
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
    "real_ingestion_ready",
    "ingestion_ready",
    "connector_ready",
    "provider_ready",
    "source_ready",
    "scoring_ready",
    "runtime_ready",
    "trading_ready",
    "production_ready",
    "model_ready",
    "backtest_ready",
    "ready_for_ingestion",
    "ready_for_connectors",
    "ready_for_source_fetching",
    "ready_for_scoring",
    "ready_for_runtime",
    "ready_for_trading",
    "approved_for_real_ingestion",
    "approved_for_ingestion",
    "approved_for_connectors",
    "approved_for_source_fetching",
    "approved_for_runtime",
    "approved_for_scoring",
    "approved_for_trading",
    "trade_ready",
    "auto_execute",
    "autonomous",
    "live",
    "production",
}

REQUIRED_REFERENCES = (
    "docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
    "standalone MEG Weather Bot PRD",
    "MEG_ACTIVE_STATE",
    "WEATHER_BOT_PACKET",
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01",
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLANNING-APPROVAL-01",
    "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01",
)

REQUIRED_SCOPE_PHRASES = (
    "This is real ingestion boundary planning closeout/checkpoint only",
    "Real ingestion boundary planning v1 is complete for now",
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01` is closed out by this document",
    "Real ingestion implementation is not approved",
    "no ingestion code is created",
    "Provider/API connector implementation is not approved",
    "Source fetching is not approved",
    "External API calls are not approved",
    "Credentials/secrets/config loading is not approved",
    "Forecast pulls are not approved",
    "Scraping, polling, streaming, scheduling, queues, jobs, and background tasks are not approved",
    "Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved",
    "No static ingestion boundary skeleton expansion is created or approved",
    "No loader expansion is created or approved",
    "No fixture JSON files are read by new source/runtime code",
    "No fixture JSON files are created or modified",
    "No fixture README files are created or modified",
    "No historical-label data files are created",
    "No generated data is created",
    "future real ingestion implementation requires a later separate approval chain",
    "future provider/API connector implementation requires a later separate approval chain",
    "future source fetching requires a later separate approval chain",
    "future scoring/backtesting requires separate explicit approval",
    "future runtime/trading requires separate explicit approval",
    "do not imply real ingestion readiness, provider readiness, source readiness, scoring readiness, runtime readiness, production readiness, or trading readiness",
    "recommended posture is hold/checkpoint unless a concrete real ingestion planning gap is found or the user explicitly chooses a later approval/request/planning gate",
)

IMPLEMENTATION_DETAIL_PROHIBITIONS = (
    "function signature",
    "class diagram",
    "module path for runtime",
    "CLI command",
    "cron schedule",
    "queue name",
    "provider client",
    "database schema",
    "endpoint route",
    "configuration key",
)


def _read_prd() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def _extract_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^{re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)", re.S | re.M)
    match = pattern.search(text)
    assert match, f"Missing section: {heading}"
    return match.group("body")


def _assignment_pairs(section: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for line in section.splitlines():
        if not line.startswith("- "):
            continue
        key, separator, value = line[2:].partition(": ")
        assert separator, f"Assignment line is not key/value formatted: {line}"
        pairs.append((key, value))
    return pairs


def test_closeout_prd_exists_and_has_canonical_references() -> None:
    assert PRD_PATH.exists()
    text = _read_prd()

    assert CANONICAL_ID in text
    for reference in REQUIRED_REFERENCES:
        assert reference in text


def test_required_sections_are_present() -> None:
    text = _read_prd()

    for section in REQUIRED_SECTIONS:
        assert f"## {section}" in text


def test_planning_inventory_lists_exactly_expected_artifacts() -> None:
    inventory = _extract_section(_read_prd(), INVENTORY_HEADING)
    observed = [line[2:] for line in inventory.splitlines() if line.startswith("- ")]

    assert observed == EXPECTED_INVENTORY


def test_required_closeout_and_non_approval_scope_is_stated() -> None:
    text = _read_prd()

    for phrase in REQUIRED_SCOPE_PHRASES:
        assert phrase in text


def test_machine_checkable_assignment_section_exists_and_is_scoped() -> None:
    text = _read_prd()
    section = _extract_section(text, ASSIGNMENT_HEADING)

    assert section.strip()
    assert "## Acceptance criteria" not in section
    assert "Forbidden real ingestion planning closeout values" not in section


def test_closed_set_assignments_use_only_allowed_values() -> None:
    section = _extract_section(_read_prd(), ASSIGNMENT_HEADING)
    pairs = _assignment_pairs(section)

    assert pairs
    for key, value in pairs:
        assert key in ALLOWED_ASSIGNMENTS, f"Unexpected assignment key: {key}"
        assert value in ALLOWED_ASSIGNMENTS[key], f"Unexpected value for {key}: {value}"


def test_every_allowed_value_appears_in_machine_checkable_assignments() -> None:
    section = _extract_section(_read_prd(), ASSIGNMENT_HEADING)
    observed: dict[str, set[str]] = {key: set() for key in ALLOWED_ASSIGNMENTS}
    for key, value in _assignment_pairs(section):
        observed.setdefault(key, set()).add(value)

    assert observed == ALLOWED_ASSIGNMENTS


def test_forbidden_examples_are_documented_but_not_parsed_as_assignments() -> None:
    text = _read_prd()
    forbidden_section = _extract_section(text, FORBIDDEN_HEADING)
    assignment_values = {value for _, value in _assignment_pairs(_extract_section(text, ASSIGNMENT_HEADING))}

    for example in FORBIDDEN_EXAMPLES:
        assert f"`{example}`" in forbidden_section
        assert example not in assignment_values


def test_no_concrete_implementation_details_are_introduced() -> None:
    text = _read_prd()

    for prohibited in IMPLEMENTATION_DETAIL_PROHIBITIONS:
        assert prohibited not in text
