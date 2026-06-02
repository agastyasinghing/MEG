"""Static tests for the Stage 2 historical-label loading approval request.

This module verifies documentation-only planning-approval posture. It uses only
Python standard-library helpers and parses closed-set assignments only from the
machine-checkable section of the approval-request PRD.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-APPROVAL-01_HISTORICAL_LABEL_LOADING_VALIDATION_PLANNING_APPROVAL_REQUEST.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-APPROVAL-01"
ASSIGNMENT_HEADING = "## Machine-checkable historical-label loading approval-request assignments"

ALLOWED_ASSIGNMENTS = {
    "historical label loading approval stage": {
        "stage_2_historical_label_loading_validation_planning_approval_request",
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
        "static_loading_contract_planning",
        "fixture_reader_boundary_planning",
        "provenance_validation_planning",
        "no_lookahead_validation_planning",
        "synthetic_real_fixture_distinction_planning",
        "blocked_caution_pass_posture_planning",
        "no_ingestion_no_runtime_no_scoring_planning",
    },
    "approval boundary status": {
        "not_approved",
        "separate_human_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "future ticket permission": {
        "may_request_historical_label_loading_validation_planning_ticket",
        "must_not_create_loader_now",
        "must_not_create_ingestion",
        "must_not_create_runtime",
        "must_not_create_scoring",
        "must_not_create_trading",
        "blocked_until_human_decision",
    },
    "data posture": {
        "no_historical_label_data_created",
        "no_generated_data_created",
        "no_fixture_files_modified",
        "no_loader_created",
        "no_runtime_data_access",
        "no_source_fetching",
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
        "back" + "testing",
        "paper_" + "simulation",
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
        assert line.startswith("- ")
        body = line[2:]
        prefix, separator, value = body.partition(": ")
        assert separator == ": "
        assert prefix in ALLOWED_ASSIGNMENTS
        parsed[prefix].add(value)
    return parsed


def test_approval_request_prd_exists_with_canonical_id_and_source_references() -> None:
    assert PRD_PATH.is_file()
    text = _prd_text()
    for required in (
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "MEG_ACTIVE_STATE",
        "WEATHER_BOT_PACKET",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01",
    ):
        assert required in text


def test_approval_request_only_scope_and_non_approval_language() -> None:
    text = _prd_text()
    required_phrases = (
        "This is a historical-label loading/validation planning approval request only",
        "Historical-label loading planning is not approved by this document",
        "Historical-label loading implementation is not approved by this document",
        "Ingestion is not approved by this document",
        "Provider/API connectors are not approved by this document",
        "External API calls are not approved by this document",
        "Credentials/secrets/config loading is not approved by this document",
        "Forecast pulls are not approved by this document",
        "Scoring/backtesting/runtime/trading/order-placement/autonomy remain unapproved",
        "Fixture files are not created or modified",
        "Historical-label data files are not created",
        "Generated data is not created",
        "Future historical-label loading/validation planning requires separate explicit human approval",
        "Future historical-label loading implementation requires a later separate approval chain",
        "Current fixture closeouts do not imply loading readiness, ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_requested_scope_is_later_planning_only_without_implementation_permission() -> None:
    text = _prd_text()
    allowed_planning_fragments = (
        "How static fixture JSONs could eventually be read by tests or planning-only validators",
        "How future historical-label loading boundaries should remain static and fail-closed",
        "How source/provenance/no-lookahead fields should be checked before any future loader exists",
        "How synthetic fixtures and real source-backed fixtures would be distinguished",
        "How blocked/caution/pass validation postures would be handled in planning",
        "How any future loading implementation would remain separate from ingestion, provider/API connectors, scoring, runtime, and trading",
        "How historical-label loading planning would avoid creating production behavior",
    )
    for fragment in allowed_planning_fragments:
        assert fragment in text

    forbidden_permission_fragments = (
        "does not ask permission to implement a loader",
        "load fixture data at runtime",
        "ingest data",
        "call providers",
        "fetch or scrape data",
        "pull forecasts",
        "score probabilities",
        "run paper simulation",
        "run runtime observation",
        "trade",
        "place orders",
        "act autonomously",
    )
    for fragment in forbidden_permission_fragments:
        assert fragment in text


def test_machine_checkable_assignment_section_exists_and_uses_only_allowed_values() -> None:
    parsed = _parsed_assignments()
    for prefix, observed_values in parsed.items():
        assert observed_values <= ALLOWED_ASSIGNMENTS[prefix]


def test_every_allowed_closed_set_value_appears_in_machine_checkable_section() -> None:
    parsed = _parsed_assignments()
    assert parsed == ALLOWED_ASSIGNMENTS


def test_forbidden_examples_are_documented_but_not_parsed_as_actual_values() -> None:
    text = _prd_text()
    section = _assignment_section(text)
    forbidden_heading = "## Forbidden historical-label loading approval-request values"
    assert forbidden_heading in text
    actual_values = set().union(*_parsed_assignments().values())
    for value in FORBIDDEN_EXAMPLES:
        assert value in text
        assert value not in actual_values


def test_prd_and_static_test_do_not_include_disallowed_connector_or_secret_fragments() -> None:
    checked_paths = (PRD_PATH, Path(__file__))
    for path in checked_paths:
        text = path.read_text(encoding="utf-8")
        for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS:
            assert fragment not in text
