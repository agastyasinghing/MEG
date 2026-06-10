"""Static checks for PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-APPROVAL-01.

These tests validate a docs-only approval request for a possible later narrow
static Weather Bot Stage 2 ingestion skeleton. They do not create ingestion,
connectors, source fetching, scoring, runtime behavior, or data artifacts.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / (
    "docs/prd/"
    "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-APPROVAL-01_"
    "INGESTION_IMPLEMENTATION_APPROVAL_REQUEST.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-APPROVAL-01"
ASSIGNMENT_HEADING = "## Machine-checkable ingestion implementation approval-request assignments"
FORBIDDEN_HEADING = "## Forbidden ingestion implementation approval-request values"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Strategic framing",
    "Stage ladder position",
    "Human approval context",
    "Ingestion implementation approval-request boundary",
    "Why a static ingestion skeleton may be useful later",
    "Requested future implementation scope",
    "Explicitly excluded scope",
    "Relationship to Stage 2 skeleton",
    "Relationship to static fixtures",
    "Relationship to real source-backed fixtures",
    "Relationship to static historical-label loader",
    "Relationship to ingestion boundary planning",
    "Relationship to provider/API connectors",
    "Relationship to source fetching",
    "Relationship to scoring/backtesting",
    "Relationship to runtime/trading",
    "Human approval checklist",
    "Approval decision options",
    "Explicit non-approval boundaries",
    "Closed ingestion implementation approval-request vocabulary",
    "Forbidden ingestion implementation approval-request values",
    "Machine-checkable ingestion implementation approval-request assignments",
    "Later-ticket handoff",
    "Acceptance criteria",
)

REQUIRED_REFERENCES = (
    "docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
    "MEG_ACTIVE_STATE",
    "WEATHER_BOT_PACKET",
    "PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-INGESTION-PLAN-01",
    "PRD-P1-WX-STAGE2-INGESTION-PLANNING-APPROVAL-01",
    "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01",
)

REQUIRED_SCOPE_STATEMENTS = (
    "This is an ingestion implementation approval request only.",
    "Ingestion implementation is not approved by this document.",
    "No ingestion code is created by this document.",
    "Provider/API connector implementation is not approved by this document.",
    "Source fetching is not approved by this document.",
    "External API calls are not approved by this document.",
    "Credentials/secrets/config loading is not approved by this document.",
    "Forecast pulls are not approved by this document.",
    "Scraping, polling, streaming, scheduling, queues, jobs, and background tasks are not approved by this document.",
    "Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved.",
    "No loader expansion is created or approved by this document.",
    "No fixture JSON files are read by new source/runtime code.",
    "No fixture JSON files are created or modified.",
    "No fixture README files are created or modified.",
    "No historical-label data files are created.",
    "No generated data is created.",
    "future ingestion implementation requires separate explicit human approval after this request",
    "Future provider/API connector implementation requires a later separate approval chain.",
    "Future source fetching requires a later separate approval chain.",
    "Future scoring/backtesting requires separate explicit approval.",
    "Future runtime/trading requires separate explicit approval.",
    "Current fixture, loading, loader, ingestion-planning, and ingestion-closeout documents do not imply ingestion readiness, provider readiness, scoring readiness, runtime readiness, production readiness, or trading readiness",
)

NARROW_SCOPE_MARKERS = (
    "narrow static ingestion skeleton",
    "static validation",
    "already-human-reviewed source descriptors",
    "fail-closed blockers",
    "tests under `tests/core`",
    "no runtime source fetching",
    "no external API calls",
    "no provider connector behavior",
    "no file writes",
    "no generated data",
    "no database writes",
    "no forecast pulls",
    "no scoring",
    "no backtesting",
    "no paper simulation",
    "no runtime observation",
    "no trading/order/autonomy",
)

ALLOWED_ASSIGNMENTS = {
    "ingestion implementation approval stage": {
        "stage_2_ingestion_implementation_approval_request",
    },
    "request status": {
        "request_prepared",
        "implementation_not_approved",
        "human_review_required",
        "blocked_pending_fix",
        "unclear",
    },
    "requested future implementation scope": {
        "static_ingestion_boundary_module_if_later_approved",
        "human_reviewed_source_descriptor_validation_if_later_approved",
        "source_identity_validation_if_later_approved",
        "source_provenance_validation_if_later_approved",
        "access_date_validation_if_later_approved",
        "no_lookahead_validation_if_later_approved",
        "fixture_ingestion_separation_validation_if_later_approved",
        "loader_ingestion_separation_validation_if_later_approved",
        "prohibited_source_category_validation_if_later_approved",
        "fail_closed_blocker_validation_if_later_approved",
        "tests_core_static_validation_if_later_approved",
        "no_connectors_no_runtime_no_scoring",
    },
    "approval boundary status": {
        "not_approved",
        "separate_human_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "future ticket permission": {
        "may_request_ingestion_implementation_ticket",
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
        "no_ingestion_artifacts_created",
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
    "request_prepared/implementation_not_approved",
    "not_approved/separate_human_approval_required",
    "source_backed/reviewer_inferred",
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
    "source_ready",
    "scoring_ready",
    "runtime_ready",
    "trading_ready",
    "production_ready",
    "model_ready",
    "back" + "test_ready",
    "ready_for_ingestion",
    "ready_for_connectors",
    "ready_for_source_fetching",
    "ready_for_scoring",
    "ready_for_runtime",
    "ready_for_trading",
    "approved_for_ingestion",
    "approved_for_connectors",
    "approved_for_source_fetching",
    "approved_for_runtime",
    "approved_for_scoring",
    "approved_for_trading",
    "trade_ready",
    "auto" + "_execute",
    "aut" + "onomous",
    "live",
    "production",
}

ASSIGNMENT_LINE_RE = re.compile(
    r"^- (?P<key>ingestion implementation approval stage|request status|"
    r"requested future implementation scope|approval boundary status|"
    r"future ticket permission|data posture|non-approval category|"
    r"evidence status|label confidence): (?P<value>[a-z0-9_]+)$"
)


def _read_prd() -> str:
    assert PRD_PATH.exists(), f"Missing approval-request PRD: {PRD_PATH}"
    return PRD_PATH.read_text(encoding="utf-8")


def _extract_section(text: str, heading: str) -> str:
    start = text.find(heading)
    assert start != -1, f"Missing section heading: {heading}"
    body_start = start + len(heading)
    next_heading = text.find("\n## ", body_start)
    if next_heading == -1:
        return text[body_start:]
    return text[body_start:next_heading]


def _parse_assignments(text: str) -> dict[str, set[str]]:
    section = _extract_section(text, ASSIGNMENT_HEADING)
    parsed: dict[str, set[str]] = {key: set() for key in ALLOWED_ASSIGNMENTS}
    unexpected_lines: list[str] = []

    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = ASSIGNMENT_LINE_RE.match(line)
        if not match:
            unexpected_lines.append(line)
            continue
        parsed[match.group("key")].add(match.group("value"))

    assert not unexpected_lines, f"Unexpected machine-checkable assignment lines: {unexpected_lines}"
    return parsed


def test_approval_request_prd_exists_and_has_required_sections() -> None:
    text = _read_prd()

    assert CANONICAL_ID in text
    for section in REQUIRED_SECTIONS:
        assert f"## {section}" in text


def test_required_context_references_are_present() -> None:
    text = _read_prd()

    for reference in REQUIRED_REFERENCES:
        assert reference in text


def test_approval_request_only_scope_and_non_approvals_are_stated() -> None:
    text = _read_prd()

    for statement in REQUIRED_SCOPE_STATEMENTS:
        assert statement in text


def test_requested_future_scope_is_narrow_static_test_oriented_and_fail_closed() -> None:
    text = _read_prd()

    for marker in NARROW_SCOPE_MARKERS:
        assert marker in text

    prohibited_now_requests = (
        "does not ask permission to implement ingestion now",
        "implement connectors now",
        "fetch or scrape data now",
        "add API clients now",
        "add secrets/config now",
        "add forecast pulls now",
        "score probabilities now",
        "backtest now",
        "run runtime observation now",
        "trade now",
        "place orders now",
        "act autonomously now",
    )
    for marker in prohibited_now_requests:
        assert marker in text


def test_machine_checkable_assignment_section_uses_only_allowed_values() -> None:
    text = _read_prd()
    parsed = _parse_assignments(text)

    assert set(parsed) == set(ALLOWED_ASSIGNMENTS)
    for key, values in parsed.items():
        assert values <= ALLOWED_ASSIGNMENTS[key], f"Unexpected values for {key}: {values}"


def test_every_allowed_closed_set_value_appears_in_machine_checkable_section() -> None:
    text = _read_prd()
    parsed = _parse_assignments(text)

    for key, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert parsed[key] == allowed_values, f"Missing values for {key}: {allowed_values - parsed[key]}"


def test_forbidden_examples_are_documented_but_not_parsed_as_actual_values() -> None:
    text = _read_prd()
    forbidden_section = _extract_section(text, FORBIDDEN_HEADING)
    parsed = _parse_assignments(text)
    actual_values = set().union(*parsed.values())

    for forbidden in FORBIDDEN_EXAMPLES:
        assert forbidden in forbidden_section
        assert forbidden not in actual_values


def test_machine_checkable_parsing_is_section_scoped() -> None:
    text = _read_prd()
    assignment_section = _extract_section(text, ASSIGNMENT_HEADING)

    assert "request_prepared/implementation_not_approved" not in assignment_section
    assert "not_approved/separate_human_approval_required" not in assignment_section
    assert "source_backed/reviewer_inferred" not in assignment_section
    assert "confirmed/unclear" not in assignment_section
    assert "ready_for_ingestion" not in assignment_section
    assert "approved_for_ingestion" not in assignment_section


def test_positive_approval_drift_phrases_are_absent() -> None:
    text = _read_prd().lower()
    positive_approval_phrases = (
        "ingestion implementation " + "approved",
        "connector " + "approved",
        "provider integration " + "approved",
        "source fetching " + "approved",
        "external api calls " + "approved",
        "scoring " + "approved",
        "backtesting " + "approved",
        "runtime " + "approved",
        "trading " + "approved",
        "order placement " + "approved",
        "autonomy " + "approved",
        "production " + "approved",
        "connector implementation " + "approved",
        "provider implementation " + "approved",
    )

    for phrase in positive_approval_phrases:
        assert phrase not in text
