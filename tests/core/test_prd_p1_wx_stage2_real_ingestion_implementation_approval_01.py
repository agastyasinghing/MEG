"""Static checks for PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-APPROVAL-01.

These tests validate the Weather Bot Stage 2 real ingestion implementation
approval-request artifact without creating ingestion, connectors, source fetching,
scoring, runtime behavior, or data artifacts.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / (
    "docs/prd/"
    "PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-APPROVAL-01_REAL_INGESTION_IMPLEMENTATION_APPROVAL_REQUEST.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-APPROVAL-01"
ASSIGNMENT_HEADING = "## Machine-checkable real ingestion implementation approval-request assignments"
FORBIDDEN_HEADING = "## Forbidden real ingestion implementation approval-request values"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Strategic framing",
    "Stage ladder position",
    "Human approval context",
    "Real ingestion implementation approval-request boundary",
    "Why real ingestion implementation may be useful later",
    "Requested future implementation scope",
    "Explicitly excluded scope",
    "Relationship to real ingestion boundary planning",
    "Relationship to static ingestion boundary skeleton",
    "Relationship to provider/API connectors",
    "Relationship to source fetching",
    "Relationship to external API calls",
    "Relationship to credentials/secrets/config",
    "Relationship to forecast pulls",
    "Relationship to scoring/backtesting",
    "Relationship to runtime/trading",
    "Human approval checklist",
    "Approval decision options",
    "Explicit non-approval boundaries",
    "Closed real ingestion implementation approval-request vocabulary",
    "Forbidden real ingestion implementation approval-request values",
    "Machine-checkable real ingestion implementation approval-request assignments",
    "Later-ticket handoff",
    "Acceptance criteria",
)

REQUIRED_REFERENCES = (
    "standalone MEG Weather Bot PRD",
    "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
    "MEG_ACTIVE_STATE",
    "WEATHER_BOT_PACKET",
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01",
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLANNING-APPROVAL-01",
    "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01",
)

REQUIRED_SCOPE_STATEMENTS = (
    "This is a real ingestion implementation approval request only",
    "Real ingestion implementation is not approved by this document",
    "no ingestion code is created by this document",
    "Provider/API connector implementation is not approved by this document",
    "Source fetching is not approved by this document",
    "External API calls are not approved by this document",
    "Credentials/secrets/config loading is not approved by this document",
    "Forecast pulls are not approved by this document",
    "scraping, polling, streaming, scheduling, queues, jobs, background tasks",
    "Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved",
    "No static ingestion boundary skeleton expansion is created or approved by this document",
    "No loader expansion is created or approved",
    "No fixture JSON files are read by new source/runtime code",
    "No fixture JSON files are created or modified",
    "No fixture README files are created or modified",
    "No historical-label data files are created",
    "No generated data is created",
    "Future real ingestion implementation requires separate explicit human approval after this request",
    "Future provider/API connector implementation requires a later separate approval chain",
    "Future source fetching requires a later separate approval chain",
    "Future scoring/backtesting requires separate explicit approval",
    "Future runtime/trading requires separate explicit approval",
    "do not imply real ingestion readiness, provider readiness, source readiness, scoring readiness, runtime readiness, production readiness, or trading readiness",
)

REQUESTED_FUTURE_SCOPE_STATEMENTS = (
    "consumes caller-supplied, already-reviewed source descriptors",
    "uses the already-planned real ingestion boundary vocabulary",
    "enforces required source identity, provenance, access-date, retrieval-context, and no-lookahead metadata",
    "enforces allowed and prohibited source-intake modes as static inputs",
    "validates fail-closed blocker categories",
    "separates real-ingestion artifacts from static fixtures, static loaders, and static ingestion skeletons",
    "remains offline and static unless a later source-fetching approval chain is granted",
    "includes `tests/core` static and unit tests",
)

ALLOWED_ASSIGNMENTS = {
    "real ingestion implementation approval stage": {
        "stage_2_real_ingestion_implementation_approval_request",
    },
    "request status": {
        "request_prepared",
        "implementation_not_approved",
        "human_review_required",
        "blocked_pending_fix",
        "unclear",
    },
    "requested future implementation scope": {
        "offline_real_ingestion_skeleton",
        "caller_supplied_source_descriptor_validation",
        "real_ingestion_boundary_vocabulary_enforcement",
        "source_identity_provenance_validation",
        "access_date_retrieval_context_validation",
        "no_lookahead_validation",
        "allowed_source_intake_mode_validation",
        "prohibited_source_intake_mode_validation",
        "fail_closed_blocker_validation",
        "static_descriptor_real_ingestion_separation",
        "static_loader_real_ingestion_separation",
        "static_skeleton_real_ingestion_separation",
        "tests_core_static_and_unit_coverage",
    },
    "approval boundary status": {
        "not_approved",
        "separate_human_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "future ticket permission": {
        "may_request_real_ingestion_implementation_ticket",
        "must_not_create_real_ingestion_now",
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
        "no_static_ingestion_skeleton_expansion_created",
        "no_real_ingestion_artifacts_created",
        "no_runtime_data_access",
        "no_source_fetching",
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

ASSIGNMENT_RE = re.compile(r"^- ([^:]+): (\S+)\s*$", re.MULTILINE)


def _read_prd() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def _extract_section(text: str, heading: str) -> str:
    start = text.find(heading)
    assert start != -1, heading
    body_start = start + len(heading)
    next_heading = text.find("\n## ", body_start)
    if next_heading == -1:
        return text[body_start:]
    return text[body_start:next_heading]


def _actual_assignments() -> dict[str, set[str]]:
    section = _extract_section(_read_prd(), ASSIGNMENT_HEADING)
    assignments = {name: set() for name in ALLOWED_ASSIGNMENTS}
    for name, value in ASSIGNMENT_RE.findall(section):
        assert name in ALLOWED_ASSIGNMENTS, name
        assignments[name].add(value)
    return assignments


def test_approval_request_prd_exists_and_contains_canonical_id() -> None:
    assert PRD_PATH.exists()
    assert CANONICAL_ID in _read_prd()


def test_required_sections_are_present() -> None:
    text = _read_prd()
    for section in REQUIRED_SECTIONS:
        assert f"## {section}" in text


def test_required_references_are_present() -> None:
    text = _read_prd()
    for reference in REQUIRED_REFERENCES:
        assert reference in text


def test_required_non_approval_scope_statements_are_present() -> None:
    text = _read_prd()
    for statement in REQUIRED_SCOPE_STATEMENTS:
        assert statement in text


def test_requested_future_scope_stays_offline_static_and_caller_supplied() -> None:
    text = _read_prd()
    for statement in REQUESTED_FUTURE_SCOPE_STATEMENTS:
        assert statement in text


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _read_prd()
    section = _extract_section(text, ASSIGNMENT_HEADING)
    assert section.strip()
    assert "## Later-ticket handoff" not in section
    assert "## Acceptance criteria" not in section
    assert FORBIDDEN_HEADING in text
    assert text.find(FORBIDDEN_HEADING) < text.find(ASSIGNMENT_HEADING)


def test_closed_set_assignments_use_only_allowed_values() -> None:
    assignments = _actual_assignments()
    for name, values in assignments.items():
        assert values <= ALLOWED_ASSIGNMENTS[name], name


def test_every_allowed_value_appears_in_machine_checkable_assignments() -> None:
    assert _actual_assignments() == ALLOWED_ASSIGNMENTS


def test_forbidden_examples_are_documented_but_not_parsed_as_actual_values() -> None:
    text = _read_prd()
    forbidden_section = _extract_section(text, FORBIDDEN_HEADING)
    for example in FORBIDDEN_EXAMPLES:
        assert f"- {example}" in forbidden_section
    actual_values = {value for values in _actual_assignments().values() for value in values}
    assert actual_values.isdisjoint(FORBIDDEN_EXAMPLES)
