"""Static checks for Weather Bot narrow source-fetching runtime approval request."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-APPROVAL-REQUEST-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-fetching runtime approval-request assignments"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to static scaffold closeout", "Relationship to static scaffold",
    "Relationship to narrow implementation plan", "Relationship to implementation approval decision",
    "Relationship to Weather Bot PRD and architecture alignment", "Runtime approval request objective",
    "Request-only posture", "Requested future runtime decision scope", "Scope not approved by this request",
    "Source identity runtime request boundary", "Retrieval context runtime request boundary",
    "Provider/source family runtime request boundary", "Manual review gate runtime request boundary",
    "No-lookahead metadata runtime request boundary", "Fail-closed validation runtime request boundary",
    "Static audit surface runtime request boundary", "Provider/source execution boundary", "Credential/config boundary",
    "Generated-data and fixture boundary", "Trading/autonomy/production boundary", "Canonical identifier posture",
    "Provider/source compatibility posture", "Offline-ingestion boundary posture", "Test-scope posture",
    "Risk and failure-mode posture", "Explicit non-approval boundaries", "Blocked implementation work",
    "Recommended next ticket", "Machine-checkable source-fetching runtime approval-request assignments",
    "Acceptance criteria",
)
RELATIONSHIP_IDS = {
    CANONICAL_ID,
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLAN-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-DECISION-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-REQUEST-01",
    "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01",
    "MEG-ARCH-ALIGN-08",
    "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD",
}
REQUESTED_RUNTIME_SCOPE = {
    "source_identity_recording_runtime", "retrieval_context_recording_runtime",
    "provider_source_family_recording_runtime", "manual_review_gate_runtime",
    "no_lookahead_metadata_gate_runtime", "fail_closed_validation_gate_runtime", "static_audit_surface_runtime",
}
NOT_APPROVED_SCOPE = {
    "runtime_source_fetching_approved", "source_fetching_implementation_approved",
    "provider_connector_implementation_approved", "provider_client_creation_approved",
    "live_provider_source_fetching_approved", "forecast_pull_execution_approved", "api_call_execution_approved",
    "scraping_execution_approved", "file_download_execution_approved", "provider_sdk_execution_approved",
    "credentials_config_loading_approved", "generated_data_creation_approved", "fixture_data_modification_approved",
    "scoring_implementation_approved", "backtesting_implementation_approved", "runtime_trading_behavior_approved",
    "order_placement_approved", "autonomy_behavior_approved", "production_behavior_approved",
}
SOURCE_FAMILIES = {"forecast_provider_family", "historical_observation_provider_family", "official_resolution_source_family", "market_metadata_source_family", "manual_human_review_source_family", "unsupported_source_family", "unknown_source_family"}
RETRIEVAL_MODES = {"manual_descriptor_only", "static_fixture_reference_only", "later_source_fetching_request", "later_provider_connector_request", "prohibited_until_explicit_approval", "unknown_requires_review"}
ACCESS_METHODS = {"manual_review", "static_reference", "api_call", "scraping", "file_download", "provider_sdk", "unknown_requires_review"}
CREDENTIAL_VALUES = {"none_required", "credentials_required_later", "config_required_later", "secrets_required_later", "unknown_requires_review"}
GENERATED_FIXTURE_VALUES = {"no_generated_data", "no_fixture_change", "generated_data_requires_later_approval", "fixture_change_requires_later_approval", "unknown_requires_review"}
PROVIDER_POSTURE = {"provider_connectors_not_approved", "provider_clients_not_created", "live_provider_source_fetching_not_approved", "forecast_pulls_not_approved", "api_calls_not_approved", "scraping_not_approved", "runtime_approval_request_only"}
IMPLEMENTATION_POSTURE = {"request_only", "docs_static_test_only", "runtime_not_approved", "no_runtime_source_fetching", "no_code_implementation", "no_provider_connector", "no_provider_client", "no_live_provider_fetching", "no_forecast_pull", "no_api_call", "no_scraping", "no_file_download", "no_provider_sdk", "no_credentials_config_loading", "no_scoring_backtesting", "no_runtime_trading", "no_order_placement", "no_autonomy", "no_production_behavior", "no_generated_data", "no_fixture_change", "no_workflow_change", "no_dependency_change", "no_database_migration", "no_schema_change", "no_source_code_migration", "no_compatibility_shim"}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_runtime_approval_request"},
    "runtime approval request status": {"docs_static_test_only", "request_only", "post_pr_258_static_scaffold_closeout"},
    "current state posture": {"runtime_not_approved", "approval_request_only"},
    "requested future runtime decision scope": REQUESTED_RUNTIME_SCOPE,
    "not approved scope": NOT_APPROVED_SCOPE,
    "provider source posture": PROVIDER_POSTURE,
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "implementation posture": IMPLEMENTATION_POSTURE,
    "recommended next track": {"narrow_source_fetching_runtime_approval_decision"},
    "conditional next track": {"hold_checkpoint_if_runtime_approval_denied", "request_revision_if_scope_too_broad", "implementation_plan_revision_if_static_gap_found"},
    "evidence status": {"runtime_approval_request_recorded"},
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


def test_required_request_only_posture_and_non_approval_language() -> None:
    text = _read()
    required = [
        "narrow source-fetching runtime approval request artifact only", "docs/static-test-only/request-only",
        "PR #258 is the latest completed static-scaffold closeout predecessor",
        "PR #258 created `PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-CLOSEOUT-01`",
        "PR #258 recommended `narrow_source_fetching_runtime_approval_request`",
        "does not grant runtime approval", "does not implement runtime source fetching", "does not modify runtime code",
        "does not create provider connectors", "does not create provider clients", "does not call providers",
        "does not approve live provider/source fetching", "does not approve forecast pulls", "does not approve API calls",
        "does not approve scraping", "does not approve file downloads", "does not approve provider SDK usage",
        "does not approve credentials/secrets/config loading", "does not approve generated data",
        "does not approve fixture changes", "does not approve scoring", "does not approve backtesting",
        "does not approve runtime trading", "does not approve order placement", "does not approve autonomy",
        "does not approve production behavior", "A later separate approval decision is required before any runtime/source/provider execution",
        "Weather Bot models the market settlement rule, not generic weather", "No routing on `market_id` is introduced or approved",
        "Recommended next track: `narrow_source_fetching_runtime_approval_decision`",
    ]
    for phrase in required:
        assert phrase in text
    for value in (REQUESTED_RUNTIME_SCOPE | NOT_APPROVED_SCOPE | SOURCE_FAMILIES | RETRIEVAL_MODES | ACCESS_METHODS | CREDENTIAL_VALUES | GENERATED_FIXTURE_VALUES):
        assert value in text
    for identifier in ("condition_id", "token_id", "outcome"):
        assert f"`{identifier}`" in text


def test_machine_checkable_assignments_are_section_scoped_and_allowed() -> None:
    assignments = _assignments(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field]
        assert assignments[field] <= allowed_values
    assert assignments["requested future runtime decision scope"] == REQUESTED_RUNTIME_SCOPE
    assert assignments["not approved scope"] == NOT_APPROVED_SCOPE
    assert assignments["recommended next track"] == {"narrow_source_fetching_runtime_approval_decision"}


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- recommended next track: narrow_source_fetching_runtime_approval_decision\n"
        "## Later heading\n"
        "- recommended next track: runtime_behavior_approved\n"
    )
    assert _assignments(synthetic) == {"recommended next track": {"narrow_source_fetching_runtime_approval_decision"}}


def test_document_does_not_assert_unsafe_approval() -> None:
    text = _read().lower()
    forbidden_positive_patterns = [
        r"runtime source fetching approved", r"source fetching implementation approved",
        r"provider connector implementation approved", r"provider clients created", r"live provider source fetching approved",
        r"forecast pulls approved", r"api calls approved", r"scraping approved", r"file downloads approved",
        r"provider sdk usage approved", r"credentials/secrets/config loading approved", r"generated data approved",
        r"fixture changes approved", r"scoring approved", r"backtesting approved", r"runtime trading approved",
        r"order placement approved", r"trading approved", r"autonomy approved", r"production behavior approved",
        r"generated data created", r"fixture data modified",
    ]
    for pattern in forbidden_positive_patterns:
        assert not re.search(pattern, text)
