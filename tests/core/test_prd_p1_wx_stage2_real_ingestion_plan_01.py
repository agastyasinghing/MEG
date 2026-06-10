"""Static checks for PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01.

These tests validate the Weather Bot Stage 2 real ingestion boundary planning
artifact without creating ingestion, connectors, source fetching, scoring,
runtime behavior, or data artifacts.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01_REAL_INGESTION_BOUNDARY_PLANNING.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01"
ASSIGNMENT_HEADING = "## Machine-checkable real ingestion boundary planning assignments"
FORBIDDEN_HEADING = "## Forbidden real ingestion boundary planning values"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Strategic framing",
    "Stage ladder position",
    "Human approval basis",
    "Planning-only boundary",
    "Real ingestion boundary vocabulary",
    "Source-intake boundary vocabulary",
    "Provider/source category taxonomy",
    "Allowed future source-intake modes",
    "Prohibited source-intake modes",
    "Pre-fetch human approval gates",
    "Source identity and provenance requirements",
    "Access-date and retrieval-context requirements",
    "No-lookahead safeguards",
    "Static-descriptor-to-real-ingestion separation",
    "Static-loader-to-real-ingestion separation",
    "Static-skeleton-to-real-ingestion separation",
    "Fail-closed real-ingestion blocker taxonomy",
    "Provider connector handoff rules",
    "Source-fetching handoff rules",
    "Scoring/backtesting handoff rules",
    "Runtime/trading handoff rules",
    "What this planning document confirms",
    "What remains unbuilt",
    "Explicit non-approval boundaries",
    "Future gates",
    "Closed real ingestion boundary planning vocabulary",
    "Forbidden real ingestion boundary planning values",
    "Machine-checkable real ingestion boundary planning assignments",
    "Acceptance criteria",
    "Later-ticket handoff",
)

REQUIRED_REFERENCES = (
    "standalone MEG Weather Bot PRD",
    "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
    "MEG_ACTIVE_STATE",
    "WEATHER_BOT_PACKET",
    "PRD-P1-WX-STAGE2-REAL-INGESTION-PLANNING-APPROVAL-01",
    "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01",
    "PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01",
)

REQUIRED_SCOPE_STATEMENTS = (
    "This is real ingestion boundary planning only",
    "Real ingestion implementation is not approved",
    "no ingestion code is created",
    "Provider/API connector implementation is not approved",
    "Source fetching is not approved",
    "external API calls are not approved",
    "credentials/secrets/config loading is not approved",
    "forecast pulls are not approved",
    "scraping, polling, streaming, scheduling, queues, jobs, or background tasks",
    "Scoring/backtesting/runtime/trading/order-placement/autonomy remain unapproved",
    "No static ingestion boundary skeleton expansion is created or approved",
    "No loader expansion is created or approved",
    "no fixture JSON files are read by new source/runtime code",
    "no fixture JSON files are created or modified",
    "no fixture README files are created or modified",
    "no historical-label data files are created",
    "no generated data is created",
    "Future real ingestion implementation requires a later separate approval chain",
    "Future provider/API connector implementation requires a later separate approval chain",
    "Future source fetching requires a later separate approval chain",
)

CONCRETE_DETAIL_PROHIBITIONS = (
    "no function signatures",
    "no classes",
    "no modules",
    "no CLI commands",
    "no scripts",
    "no configs",
    "no DB schemas",
    "no APIs",
    "no connector interfaces",
    "no runtime workflows",
    "no job schedules",
    "no queue names",
    "no provider-specific client behavior",
    "no file formats beyond planning vocabulary",
)

ALLOWED_ASSIGNMENTS = {
    "real ingestion planning stage": {"stage_2_real_ingestion_boundary_planning"},
    "planning status": {
        "planning_prepared",
        "implementation_not_approved",
        "source_fetching_not_approved",
        "human_review_required",
        "blocked_pending_fix",
        "unclear",
    },
    "planned boundary category": {
        "real_ingestion_boundary_vocabulary",
        "source_intake_boundary_vocabulary",
        "provider_source_category_taxonomy",
        "allowed_source_intake_mode",
        "prohibited_source_intake_mode",
        "pre_fetch_human_approval_gate",
        "source_identity_requirement",
        "source_provenance_requirement",
        "access_date_requirement",
        "retrieval_context_requirement",
        "no_lookahead_requirement",
        "static_descriptor_real_ingestion_separation",
        "static_loader_real_ingestion_separation",
        "static_skeleton_real_ingestion_separation",
        "fail_closed_real_ingestion_blocker_taxonomy",
        "provider_connector_handoff",
        "source_fetching_handoff",
        "scoring_backtesting_handoff",
        "runtime_trading_handoff",
    },
    "provider/source category": {
        "official_resolution_source",
        "venue_rule_source",
        "weather_station_source",
        "market_metadata_source",
        "forecast_provider_source",
        "exchange_market_source",
        "manual_research_note",
        "human_reviewed_fixture_source",
        "not_applicable",
    },
    "allowed source-intake mode": {
        "human_reviewed_manual_entry",
        "offline_static_descriptor",
        "future_provider_connector_after_approval",
        "future_source_fetch_after_approval",
        "future_manual_upload_after_approval",
        "not_applicable",
    },
    "prohibited source-intake mode": {
        "unauthenticated_runtime_scrape",
        "private_credentials_without_approval",
        "live_market_feed_without_approval",
        "unreviewed_bulk_dataset",
        "unattributed_social_post",
        "unverified_ai_summary",
        "unknown_source",
        "not_applicable",
    },
    "planned blocker category": {
        "missing_source_identity",
        "missing_access_date",
        "missing_retrieval_context",
        "missing_source_provenance",
        "missing_venue_rule",
        "missing_resolver_source",
        "unsupported_source_category",
        "unsupported_access_mode",
        "prohibited_access_mode",
        "private_credentials_required",
        "source_conflict",
        "provider_conflict",
        "time_window_conflict",
        "fixture_real_ingestion_confusion",
        "static_loader_real_ingestion_confusion",
        "static_skeleton_real_ingestion_confusion",
        "runtime_drift",
        "connector_drift",
        "scoring_drift",
        "trading_drift",
        "other_unclear",
    },
    "boundary status": {
        "preserved",
        "not_approved",
        "explicitly_out_of_scope",
        "separate_human_approval_required",
        "blocked",
        "unclear",
    },
    "future ticket permission": {
        "may_request_real_ingestion_implementation_approval_later",
        "may_request_provider_connector_planning_later",
        "may_request_source_fetching_planning_later",
        "may_request_scoring_backtesting_planning_later",
        "may_request_runtime_observation_planning_later",
        "must_not_create_real_ingestion_now",
        "must_not_create_connectors",
        "must_not_create_source_fetching",
        "must_not_create_external_api_calls",
        "must_not_create_runtime",
        "must_not_create_scoring",
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
        "planning_only",
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
    "planning_prepared/implementation_not_approved",
    "preserved/not_approved",
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


def test_planning_prd_exists_and_contains_canonical_id() -> None:
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


def test_document_avoids_concrete_implementation_details() -> None:
    text = _read_prd()
    for prohibition in CONCRETE_DETAIL_PROHIBITIONS:
        assert prohibition in text


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _read_prd()
    section = _extract_section(text, ASSIGNMENT_HEADING)
    assert section.strip()
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
