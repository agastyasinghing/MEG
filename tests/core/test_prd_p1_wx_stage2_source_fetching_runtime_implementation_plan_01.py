"""Static checks for Weather Bot narrow source-fetching runtime implementation plan."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-IMPLEMENTATION-PLAN-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-fetching runtime implementation-plan assignments"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to runtime approval decision", "Relationship to runtime approval request",
    "Relationship to static scaffold closeout", "Relationship to narrow implementation plan",
    "Relationship to Weather Bot PRD and architecture alignment", "Runtime implementation plan objective",
    "Approved planning authority", "Planned future runtime scaffold surfaces",
    "Planned source identity runtime scaffold", "Planned retrieval context runtime scaffold",
    "Planned provider/source family runtime scaffold", "Planned manual review gate runtime scaffold",
    "Planned no-lookahead metadata runtime scaffold", "Planned fail-closed validation runtime scaffold",
    "Planned static audit runtime scaffold", "Future module boundary", "Future data-shape boundary",
    "Future test boundary", "Future fail-closed boundary", "Scope not implemented by this plan",
    "Scope not approved for execution", "Provider/source execution boundary", "Credential/config boundary",
    "Generated-data and fixture boundary", "Trading/autonomy/production boundary", "Canonical identifier posture",
    "Provider/source compatibility posture", "Offline-ingestion boundary posture", "Test-scope posture",
    "Risk and failure-mode posture", "Explicit non-execution boundaries", "Blocked implementation work",
    "Recommended next ticket", "Machine-checkable source-fetching runtime implementation-plan assignments",
    "Acceptance criteria",
)
RELATIONSHIP_IDS = {
    CANONICAL_ID,
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-APPROVAL-DECISION-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-APPROVAL-REQUEST-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLAN-01",
    "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01",
    "MEG-ARCH-ALIGN-08",
    "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD",
}
SCAFFOLD_SURFACES = {
    "source_identity_recording_runtime_plan", "retrieval_context_recording_runtime_plan",
    "provider_source_family_recording_runtime_plan", "manual_review_gate_runtime_plan",
    "no_lookahead_metadata_gate_runtime_plan", "fail_closed_validation_gate_runtime_plan",
    "static_audit_surface_runtime_plan",
}
MODULE_BOUNDARIES = {
    "source_identity_runtime_plan", "retrieval_context_runtime_plan", "provider_source_family_runtime_plan",
    "manual_review_gate_runtime_plan", "no_lookahead_metadata_runtime_plan", "fail_closed_validation_runtime_plan",
    "static_audit_surface_runtime_plan",
}
FIELD_BOUNDARIES = {
    "source_id", "source_family", "source_uri_descriptor", "accessed_at_utc", "retrieved_at_utc",
    "available_at_utc", "market_resolution_time_utc", "decision_time_utc", "no_lookahead_verified",
    "manual_review_required", "review_status", "provenance_notes", "runtime_recording_mode", "runtime_gate_status",
}
FAIL_CLOSED = {
    "missing_source_identity", "unknown_source_family", "missing_access_time", "missing_retrieval_time",
    "missing_availability_time", "missing_decision_time", "missing_market_resolution_time",
    "missing_no_lookahead_verification", "manual_review_required_not_complete", "unsupported_source_family",
    "ambiguous_credential_config_posture", "ambiguous_generated_data_fixture_posture", "runtime_gate_status_missing",
}
NOT_EXECUTED_SCOPE = {
    "runtime_source_fetching", "source_fetching_implementation", "provider_connector_implementation",
    "provider_client_creation", "live_provider_source_fetching", "forecast_pull_execution", "api_call_execution",
    "scraping_execution", "file_download_execution", "provider_sdk_execution", "credentials_config_loading",
    "generated_data_creation", "fixture_data_modification", "scoring_implementation", "backtesting_implementation",
    "runtime_trading_behavior", "order_placement", "autonomy_behavior", "production_behavior",
}
SOURCE_FAMILIES = {"forecast_provider_family", "historical_observation_provider_family", "official_resolution_source_family", "market_metadata_source_family", "manual_human_review_source_family", "unsupported_source_family", "unknown_source_family"}
RETRIEVAL_MODES = {"manual_descriptor_only", "static_fixture_reference_only", "later_source_fetching_request", "later_provider_connector_request", "prohibited_until_explicit_approval", "unknown_requires_review"}
ACCESS_METHODS = {"manual_review", "static_reference", "api_call", "scraping", "file_download", "provider_sdk", "unknown_requires_review"}
PROVIDER_POSTURE = {"provider_connectors_not_approved", "provider_clients_not_created", "live_provider_source_fetching_not_approved", "forecast_pulls_not_approved", "api_calls_not_approved", "scraping_not_approved", "runtime_plan_only"}
IMPLEMENTATION_POSTURE = {"plan_only", "docs_static_test_only", "runtime_execution_not_approved", "no_runtime_source_fetching", "no_code_implementation", "no_provider_connector", "no_provider_client", "no_live_provider_fetching", "no_forecast_pull", "no_api_call", "no_scraping", "no_file_download", "no_provider_sdk", "no_credentials_config_loading", "no_scoring_backtesting", "no_runtime_trading", "no_order_placement", "no_autonomy", "no_production_behavior", "no_generated_data", "no_fixture_change", "no_workflow_change", "no_dependency_change", "no_database_migration", "no_schema_change", "no_source_code_migration", "no_compatibility_shim"}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_runtime_implementation_plan"},
    "runtime implementation plan status": {"docs_static_test_only", "plan_only", "post_pr_260_runtime_approval_decision"},
    "current state posture": {"runtime_plan_recorded_only", "runtime_execution_not_approved"},
    "approved planning authority": {"approve_narrow_source_fetching_runtime_implementation_plan"},
    "planned future runtime scaffold surface": SCAFFOLD_SURFACES,
    "future module boundary": MODULE_BOUNDARIES,
    "future field boundary": FIELD_BOUNDARIES,
    "future fail closed boundary": FAIL_CLOSED,
    "not executed scope": NOT_EXECUTED_SCOPE,
    "provider source posture": PROVIDER_POSTURE,
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "implementation posture": IMPLEMENTATION_POSTURE,
    "recommended next track": {"narrow_source_fetching_runtime_static_scaffold"},
    "conditional next track": {"hold_checkpoint_if_runtime_scaffold_not_desired", "runtime_plan_revision_if_scope_too_broad", "runtime_scaffold_requires_separate_implementation_approval"},
    "evidence status": {"runtime_implementation_plan_recorded"},
    "label confidence": {"confirmed"},
}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)


def _read() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, f"Missing section: {heading}"
    assert match.group("section").strip(), f"Section is empty: {heading}"
    return match.group("section")


def _machine_section(text: str) -> str:
    return _section(text, MACHINE_HEADING.removeprefix("## "))


def _assignments(text: str) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(_machine_section(text)):
        result.setdefault(match.group("field"), set()).add(match.group("value"))
    return result


def test_document_exists_canonical_sections_and_relationships() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert f"Canonical ID: {CANONICAL_ID}" in text
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)
    for relationship_id in RELATIONSHIP_IDS:
        assert relationship_id in text


def test_required_plan_only_posture_and_non_approval_language() -> None:
    text = _read()
    required = [
        "runtime implementation plan artifact", "docs/static-test-only", "plan-only",
        "post-PR #260 runtime approval-decision state",
        "PR #260 created `PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-APPROVAL-DECISION-01`",
        "PR #260 selected `approve_narrow_source_fetching_runtime_implementation_plan`",
        "runtime implementation plan only", "defines only a future narrow runtime implementation scaffold",
        "does not implement runtime source fetching", "does not modify runtime code",
        "does not create provider connectors", "does not create provider clients", "does not call providers",
        "does not approve live provider/source fetching", "does not approve forecast pulls", "does not approve API calls",
        "does not approve scraping", "does not approve file downloads", "does not approve provider SDK usage",
        "does not approve credentials/secrets/config loading", "does not approve generated data",
        "does not approve fixture changes", "does not approve scoring", "does not approve backtesting",
        "does not approve runtime trading", "does not approve order placement", "does not approve autonomy",
        "does not approve production behavior", "Weather Bot models the market settlement rule, not generic weather",
        "No routing on `market_id` is introduced or approved", "Recommended next track: `narrow_source_fetching_runtime_static_scaffold`",
    ]
    for phrase in required:
        assert phrase in text
    for value in SCAFFOLD_SURFACES | MODULE_BOUNDARIES | FIELD_BOUNDARIES | FAIL_CLOSED | NOT_EXECUTED_SCOPE | SOURCE_FAMILIES | RETRIEVAL_MODES | ACCESS_METHODS:
        assert f"`{value}`" in text
    for identifier in ("condition_id", "token_id", "outcome"):
        assert f"`{identifier}`" in text


def test_machine_checkable_assignments_are_section_scoped_and_allowed() -> None:
    assignments = _assignments(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field]
        assert assignments[field] <= allowed_values
        assert allowed_values <= assignments[field]
    assert assignments["approved planning authority"] == {"approve_narrow_source_fetching_runtime_implementation_plan"}
    assert assignments["planned future runtime scaffold surface"] == SCAFFOLD_SURFACES
    assert assignments["future module boundary"] == MODULE_BOUNDARIES
    assert assignments["future field boundary"] == FIELD_BOUNDARIES
    assert assignments["future fail closed boundary"] == FAIL_CLOSED
    assert assignments["not executed scope"] == NOT_EXECUTED_SCOPE
    assert assignments["recommended next track"] == {"narrow_source_fetching_runtime_static_scaffold"}


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- recommended next track: narrow_source_fetching_runtime_static_scaffold\n"
        "## Later heading\n"
        "- recommended next track: runtime_source_fetching\n"
    )
    assert _assignments(synthetic) == {"recommended next track": {"narrow_source_fetching_runtime_static_scaffold"}}


def test_document_does_not_assert_runtime_source_provider_trading_or_production_approval() -> None:
    text = _read().lower()
    forbidden_positive_patterns = [
        r"runtime source fetching is approved", r"source fetching implementation is approved",
        r"provider connector implementation is approved", r"provider connectors are created", r"provider clients are created",
        r"provider calls are approved", r"live provider/source fetching is approved", r"forecast pulls are approved",
        r"api calls are approved", r"scraping is approved", r"file downloads are approved",
        r"provider sdk usage is approved", r"credentials/secrets/config loading is approved", r"generated data is approved",
        r"fixture changes are approved", r"scoring is approved", r"backtesting is approved",
        r"runtime trading is approved", r"order placement is approved", r"autonomy is approved",
        r"production behavior is approved",
    ]
    for pattern in forbidden_positive_patterns:
        assert not re.search(pattern, text)
