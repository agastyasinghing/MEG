"""Static checks for PRD-P1-WX-STAGE2-REAL-INGESTION-PLANNING-APPROVAL-01.

These tests validate a docs-only approval request for a possible later real
Weather Bot Stage 2 ingestion planning gate. They do not create ingestion,
connectors, source fetching, scoring, runtime behavior, or data artifacts.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / (
    "docs/prd/"
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLANNING-APPROVAL-01_"
    "REAL_INGESTION_PLANNING_APPROVAL_REQUEST.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-REAL-INGESTION-PLANNING-APPROVAL-01"
ASSIGNMENT_HEADING = "## Machine-checkable real ingestion planning approval-request assignments"
FORBIDDEN_HEADING = "## Forbidden real ingestion planning approval-request values"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Strategic framing",
    "Stage ladder position",
    "Human approval context",
    "Real ingestion planning approval-request boundary",
    "Why real ingestion planning may be useful later",
    "Requested future planning scope",
    "Explicitly excluded scope",
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
    "Closed real ingestion planning approval-request vocabulary",
    "Forbidden real ingestion planning approval-request values",
    "Machine-checkable real ingestion planning approval-request assignments",
    "Later-ticket handoff",
    "Acceptance criteria",
)

REQUIRED_REFERENCES = (
    "docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
    "MEG_ACTIVE_STATE",
    "WEATHER_BOT_PACKET",
    "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01",
    "PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01",
)

REQUIRED_SCOPE_STATEMENTS = (
    "This is a real ingestion planning approval request only.",
    "Real ingestion planning is not approved by this document.",
    "Real ingestion implementation is not approved by this document.",
    "No ingestion code is created by this document.",
    "Provider/API connector implementation is not approved by this document.",
    "Source fetching is not approved by this document.",
    "External API calls are not approved by this document.",
    "Credentials/secrets/config loading is not approved by this document.",
    "Forecast pulls are not approved by this document.",
    "Scraping, polling, streaming, scheduling, queues, jobs, and background tasks are not approved by this document.",
    "Scoring/backtesting/runtime/trading/order-placement/autonomy remain unapproved.",
    "No static ingestion boundary skeleton expansion is created or approved by this document.",
    "No loader expansion is created or approved by this document.",
    "No fixture JSON files are read by new source/runtime code.",
    "No fixture JSON files are created or modified.",
    "No fixture README files are created or modified.",
    "No historical-label data files are created.",
    "No generated data is created.",
    "future real ingestion planning requires separate explicit human approval after this request",
    "Future real ingestion implementation requires a later separate approval chain.",
    "Future provider/API connector implementation requires a later separate approval chain.",
    "Future source fetching requires a later separate approval chain.",
    "Future scoring/backtesting requires separate explicit approval.",
    "Future runtime/trading requires separate explicit approval.",
    "Current fixture, loading, loader, ingestion planning, static ingestion skeleton, and closeout documents do not imply real ingestion readiness, provider readiness, source readiness, scoring readiness, runtime readiness, production readiness, or trading readiness.",
)

PLANNING_ONLY_MARKERS = (
    "real ingestion planning vocabulary",
    "source-intake boundary vocabulary",
    "provider/source category taxonomy for planning only",
    "allowed future source-intake modes for planning only",
    "prohibited source-intake modes",
    "required human approval gates before any source fetching",
    "source identity/provenance requirements before any real ingestion",
    "access-date/retrieval-context requirements",
    "no-lookahead safeguards",
    "separation between static descriptors and real ingestion artifacts",
    "separation between static loader, static ingestion skeleton, and future real ingestion",
    "fail-closed blockers for missing source identity",
    "provider connector planning approval requests",
    "source-fetching implementation approval requests",
    "scoring/backtesting/runtime/trading approval requests",
    "Requested future planning scope stays planning-only and fail-closed.",
)

ALLOWED_ASSIGNMENTS = {
    "real ingestion planning approval stage": {
        "stage_2_real_ingestion_planning_approval_request",
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
        "real_ingestion_boundary_vocabulary_planning",
        "source_intake_boundary_planning",
        "provider_source_category_taxonomy_planning",
        "allowed_source_intake_mode_planning",
        "prohibited_source_intake_mode_planning",
        "pre_fetch_human_approval_gate_planning",
        "source_identity_provenance_planning",
        "access_date_retrieval_context_planning",
        "no_lookahead_safeguard_planning",
        "static_descriptor_real_ingestion_separation_planning",
        "static_loader_real_ingestion_separation_planning",
        "static_skeleton_real_ingestion_separation_planning",
        "fail_closed_real_ingestion_blocker_planning",
        "provider_connector_handoff_planning",
        "source_fetching_handoff_planning",
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
        "may_request_real_ingestion_planning_ticket",
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
        "real_ingestion",
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
    text = _read_prd()
    assert CANONICAL_ID in text


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


def test_requested_future_planning_scope_stays_planning_only_and_fail_closed() -> None:
    text = _read_prd()
    for marker in PLANNING_ONLY_MARKERS:
        assert marker in text


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _read_prd()
    section = _extract_section(text, ASSIGNMENT_HEADING)
    assert section.strip()
    assert "## Later-ticket handoff" not in section
    assert FORBIDDEN_HEADING in text
    assert text.find(FORBIDDEN_HEADING) < text.find(ASSIGNMENT_HEADING)


def test_closed_set_assignments_use_only_allowed_values() -> None:
    assignments = _actual_assignments()
    for name, values in assignments.items():
        assert values <= ALLOWED_ASSIGNMENTS[name], name


def test_every_allowed_value_appears_in_machine_checkable_assignments() -> None:
    assignments = _actual_assignments()
    assert assignments == ALLOWED_ASSIGNMENTS


def test_forbidden_examples_are_documented_but_not_parsed_as_actual_values() -> None:
    text = _read_prd()
    forbidden_section = _extract_section(text, FORBIDDEN_HEADING)
    for example in FORBIDDEN_EXAMPLES:
        assert f"- {example}" in forbidden_section
    actual_values = {value for values in _actual_assignments().values() for value in values}
    assert actual_values.isdisjoint(FORBIDDEN_EXAMPLES)
