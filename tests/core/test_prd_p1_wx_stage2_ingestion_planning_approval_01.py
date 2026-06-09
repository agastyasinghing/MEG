"""Static tests for the Weather Bot Stage 2 ingestion planning approval request."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-INGESTION-PLANNING-APPROVAL-01"
PRD_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-INGESTION-PLANNING-APPROVAL-01_INGESTION_PLANNING_APPROVAL_REQUEST.md"
ASSIGNMENT_HEADING = "## Machine-checkable ingestion planning approval-request assignments"

ALLOWED_ASSIGNMENTS = {
    "ingestion planning approval stage": {
        "stage_2_ingestion_planning_approval_request",
    },
    "request status": {
        "request_prepared",
        "planning_not_approved",
        "implementation_not_approved",
        "human_review_required",
        "blocked_pending_fix",
        "unclear",
    },
    "requested future planning scope": {
        "ingestion_boundary_vocabulary_planning",
        "source_category_planning",
        "source_identity_provenance_planning",
        "no_lookahead_safeguard_planning",
        "fixture_ingestion_separation_planning",
        "loader_ingestion_separation_planning",
        "fail_closed_ingestion_blocker_planning",
        "provider_connector_handoff_planning",
        "scoring_backtesting_handoff_planning",
        "runtime_trading_handoff_planning",
    },
    "approval boundary status": {
        "not_approved",
        "separate_human_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "future ticket permission": {
        "may_request_ingestion_planning_ticket",
        "must_not_create_ingestion_now",
        "must_not_create_connectors",
        "must_not_create_source_fetching",
        "must_not_create_external_api_calls",
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
        "no_loader_expansion_created",
        "no_runtime_data_access",
        "no_source_fetching",
    },
    "non-approval category": {
        "ingestion_implementation",
        "provider_integration",
        "connectors",
        "source_fetching",
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
    "request_prepared/planning_not_approved",
    "planning_not_approved/implementation_not_approved",
    "not_approved/separate_human_approval_required",
    "confirmed/unclear",
    "partial",
    "mixed",
    "likely_confirmed",
    "maybe",
    "approved",
    "configured",
    "available",
    "ingestion_ready",
    "connector_ready",
    "provider_ready",
    "scoring_ready",
    "runtime_ready",
    "trading_ready",
    "production_ready",
    "model_ready",
    "back" + "test_ready",
    "ready_for_ingestion",
    "ready_for_connectors",
    "ready_for_scoring",
    "ready_for_runtime",
    "ready_for_trading",
    "approved_for_ingestion",
    "approved_for_connectors",
    "approved_for_runtime",
    "approved_for_scoring",
    "approved_for_trading",
    "trade_ready",
    "auto" + "_execute",
    "aut" + "onomous",
    "live",
    "production",
}


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


def test_approval_request_prd_exists_with_required_source_references() -> None:
    assert PRD_PATH.is_file()
    text = _prd_text()
    for required in (
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "MEG_ACTIVE_STATE",
        "WEATHER_BOT_PACKET",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-01",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01",
        "Stage 2 skeleton closeout",
    ):
        assert required in text


def test_required_approval_request_only_safety_language_is_present() -> None:
    text = _prd_text()
    for required in (
        "This is an ingestion planning approval request only.",
        "Ingestion planning is not approved by this document.",
        "Ingestion implementation is not approved by this document.",
        "Provider/API connectors are not approved by this document.",
        "Source fetching is not approved by this document.",
        "External API calls are not approved by this document.",
        "Credentials/secrets/config loading is not approved by this document.",
        "Forecast pulls are not approved by this document.",
        "Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved.",
        "No loader expansion is created or approved by this document.",
        "No fixture JSON files are read by new source/runtime code.",
        "No fixture JSON files are created or modified.",
        "No fixture README files are created or modified.",
        "No historical-label data files are created.",
        "No generated data is created.",
        "Future ingestion planning requires separate explicit human approval after this request.",
        "Future ingestion implementation requires a later separate approval chain.",
        "Future provider/API connector implementation requires a later separate approval chain.",
        "Future scoring/backtesting requires separate explicit approval.",
        "Future runtime/trading requires separate explicit approval.",
        "current fixture, loading, and loader closeouts do not imply ingestion readiness, provider readiness, scoring readiness, runtime readiness, production readiness, or trading readiness".lower(),
    ):
        assert required in text or required in text.lower()


def test_requested_future_planning_scope_is_planning_only() -> None:
    text = _prd_text()
    for required in (
        "ingestion boundary vocabulary",
        "allowed source categories for future planning only",
        "prohibited source categories",
        "source identity/provenance requirements before ingestion is ever implemented",
        "no-lookahead safeguards",
        "fixture-to-ingestion separation rules",
        "static-loader-to-ingestion separation rules",
        "fail-closed behavior for missing source identity, missing access date, missing venue rule, missing resolver source, or unsupported source category",
        "planning-only handoff rules for later provider/source connector approval requests",
        "planning-only handoff rules for later scoring/backtesting approval requests",
        "planning-only handoff rules for later runtime/trading approval requests",
    ):
        assert required in text


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _prd_text()
    section = _assignment_section(text)
    assert section.strip()
    assert "## Later-ticket handoff" not in section
    assert "## Forbidden ingestion planning approval-request values" not in section


def test_closed_set_assignments_use_only_allowed_values_and_include_every_value() -> None:
    parsed = _parsed_assignments()
    assert parsed == ALLOWED_ASSIGNMENTS


def test_forbidden_examples_are_documented_but_not_parsed_as_actual_values() -> None:
    text = _prd_text()
    forbidden_section_match = re.search(
        r"## Forbidden ingestion planning approval-request values\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        flags=re.DOTALL,
    )
    assert forbidden_section_match is not None
    forbidden_section = forbidden_section_match.group("section")
    for forbidden in FORBIDDEN_EXAMPLES:
        assert forbidden in forbidden_section

    parsed_values = set().union(*_parsed_assignments().values())
    for forbidden in FORBIDDEN_EXAMPLES:
        assert forbidden not in parsed_values


def test_closed_set_parser_does_not_reject_normal_non_assignment_prose() -> None:
    text = _prd_text()
    for allowed_prose_fragment in (
        "approved",
        "mixed",
        "partial",
        "live",
        "production",
        "C++",
        "Rust",
    ):
        assert allowed_prose_fragment in text
    assert _parsed_assignments() == ALLOWED_ASSIGNMENTS
