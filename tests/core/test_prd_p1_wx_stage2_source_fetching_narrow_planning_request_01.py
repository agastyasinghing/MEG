"""Static checks for Weather Bot narrow source-fetching planning request."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-PLANNING-REQUEST-01.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-PLANNING-REQUEST-01"
MACHINE_HEADING = "## Machine-checkable source-fetching narrow planning-request assignments"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to owner disposition", "Relationship to owner-disposition planning",
    "Relationship to meta refresh", "Relationship to hold checkpoint",
    "Relationship to source-fetching approval-request draft",
    "Relationship to source-fetching approval-request planning sequence",
    "Relationship to provider/source compatibility sequence",
    "Relationship to Weather Bot PRD and architecture alignment", "Narrow planning-request objective",
    "Current permitted next track", "Requested later planning artifact", "Proposed narrow planning scope",
    "Explicitly excluded scope", "Planning artifact requirements",
    "Source identity and provenance planning requirements",
    "Access-date and retrieval-context planning requirements", "No-lookahead planning requirements",
    "Provider/source family planning requirements", "Fetch-boundary planning requirements",
    "Credential/config planning requirements", "Generated-data and fixture planning requirements",
    "Static validation planning requirements", "Fail-closed planning requirements", "Approval posture",
    "Planning-only posture", "Canonical identifier posture", "Provider/source compatibility posture",
    "Offline-ingestion boundary posture", "Test-scope posture", "Risk and failure-mode posture",
    "Explicit non-approval boundaries", "Blocked implementation work", "Recommended next ticket",
    "Machine-checkable source-fetching narrow planning-request assignments", "Acceptance criteria",
)
RELATIONSHIP_IDS = {
    CANONICAL_ID,
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-PLANNING-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-META-REFRESH-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-PLANNING-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-PLANNING-01",
    "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01",
    "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01",
    "MEG-ARCH-ALIGN-08", "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD",
}
REQUESTED_SCOPE = {
    "source_identity_and_provenance_planning", "access_date_and_retrieval_context_planning",
    "no_lookahead_boundary_planning", "provider_source_family_selection_planning",
    "fetch_boundary_design_planning", "credential_config_boundary_planning",
    "generated_data_fixture_boundary_planning", "static_validation_audit_planning",
    "fail_closed_behavior_planning",
}
EXCLUDED_SCOPE = {
    "source_fetching_implementation", "provider_connector_implementation", "forecast_pull_execution",
    "api_call_execution", "scraping_execution", "credentials_config_loading", "generated_data_creation",
    "fixture_data_modification", "scoring_implementation", "backtesting_implementation",
    "runtime_behavior", "trading_behavior", "autonomy_behavior", "production_behavior",
    "workflow_change", "dependency_change", "database_migration", "schema_change",
    "source_code_migration", "compatibility_shim",
}
CLOSED_SET_VALUES = {
    "forecast_provider_family", "historical_observation_provider_family", "official_resolution_source_family",
    "market_metadata_source_family", "manual_human_review_source_family", "unsupported_source_family",
    "unknown_source_family", "manual_descriptor_only", "static_fixture_reference_only",
    "later_source_fetching_request", "later_provider_connector_request", "prohibited_until_explicit_approval",
    "unknown_requires_review", "manual_review", "static_reference", "api_call", "scraping", "file_download",
    "provider_sdk", "none_required", "credentials_required_later", "config_required_later",
    "secrets_required_later", "no_generated_data", "no_fixture_change",
    "generated_data_requires_later_approval", "fixture_change_requires_later_approval",
}
NON_APPROVED_BEHAVIORS = {
    "provider_connector", "source_fetching", "forecast_pull", "api_call", "scraping",
    "credentials_secrets_config", "scoring_backtesting", "runtime_behavior", "trading_autonomy",
    "production_behavior", "generated_data", "fixture_change", "workflow_change", "dependency_change",
    "database_migration", "schema_change", "source_code_migration", "compatibility_shim",
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_narrow_planning_request"},
    "narrow planning request status": {"docs_static_test_only", "request_only", "post_pr_250_owner_disposition"},
    "current state posture": {"hold_checkpoint", "narrow_planning_request_allowed"},
    "owner disposition posture": {"approve_narrow_source_fetching_planning_only"},
    "requested planning scope": REQUESTED_SCOPE,
    "excluded scope": EXCLUDED_SCOPE,
    "approval request posture": {"narrow_implementation_planning_request_only", "source_fetching_implementation_not_approved", "provider_connector_implementation_not_approved", "later_explicit_implementation_approval_required"},
    "provider source posture": {"provider_connectors_not_approved", "source_fetching_implementation_not_approved", "forecast_pulls_not_approved", "api_calls_not_approved", "scraping_not_approved", "provider_source_planning_only"},
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "implementation posture": {"narrow_planning_request_only", "docs_static_test_only", "no_provider_connector", "no_source_fetching_implementation", "no_forecast_pull", "no_api_call", "no_scraping", "no_credentials_config_loading", "no_scoring_backtesting", "no_runtime_behavior", "no_trading_autonomy", "no_production_behavior", "no_generated_data", "no_fixture_change", "no_workflow_change", "no_dependency_change", "no_database_migration", "no_schema_change", "no_source_code_migration", "no_compatibility_shim"},
    "recommended next track": {"narrow_source_fetching_implementation_planning"},
    "conditional next track": {"hold_checkpoint_if_scope_blocker_found", "owner_disposition_revision_if_scope_exceeds_permission", "additional_docs_only_evidence_if_needed"},
    "evidence status": {"request_only"},
    "label confidence": {"confirmed"},
}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)


def _read(path: Path = ARTIFACT_PATH) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, f"Missing section: {heading}"
    assert match.group("section").strip(), f"Section is empty: {heading}"
    return match.group("section")


def _machine_section(text: str) -> str:
    match = re.search(rf"^{re.escape(MACHINE_HEADING)}\n(?P<section>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, "Machine-checkable section is missing"
    return match.group("section")


def _assignments(text: str) -> dict[str, set[str]]:
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(_machine_section(text)):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def test_document_exists_canonical_sections_and_relationships() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert f"Canonical ID: {CANONICAL_ID}" in text
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)
    for relationship_id in RELATIONSHIP_IDS:
        assert relationship_id in text


def test_required_posture_scope_and_non_approval_language() -> None:
    text = _read()
    required = [
        "narrow source-fetching implementation-planning request only", "docs/static-test-only",
        "PR #250 is merged", "latest completed owner-disposition predecessor",
        "owner disposition selected `approve_narrow_source_fetching_planning_only`",
        "current permitted next track `narrow_source_fetching_planning_request`",
        "requests a later implementation-planning artifact", "does not itself create that implementation-planning artifact",
        "later planning artifact must not implement source fetching", "Actual implementation requires a later separate explicit approval",
        "does not approve source-fetching implementation", "does not approve provider connector implementation",
        "does not approve forecast pulls", "does not approve API calls", "does not approve scraping",
        "does not approve credentials/secrets/config loading", "does not approve generated data",
        "does not approve fixture changes", "does not approve scoring", "does not approve backtesting",
        "does not approve runtime behavior", "does not approve trading, order placement, autonomy, or production behavior",
        "Weather Bot models the market settlement rule, not generic weather", "No routing on `market_id` is introduced or approved",
    ]
    for phrase in required:
        assert phrase in text
    for value in REQUESTED_SCOPE | EXCLUDED_SCOPE | CLOSED_SET_VALUES | NON_APPROVED_BEHAVIORS:
        assert f"`{value}`" in text
    for token in ("condition_id", "token_id", "outcome"):
        assert f"`{token}`" in text
    for phrase in (
        "provider connectors", "source fetching implementation", "forecast pulls", "API calls", "scraping",
        "credentials/secrets/config loading", "scoring", "backtesting", "runtime behavior", "execution",
        "trading", "order placement", "autonomy", "production behavior", "generated data", "fixture data",
        "workflows", "dependencies", "DB migrations", "schema changes", "source-code migrations",
        "compatibility shims", "provider/source connector implementation", "real ingestion implementation",
        "live provider usage", "paper simulation", "runtime observation",
    ):
        assert phrase in text


def test_machine_assignments_are_section_scoped_and_allowed() -> None:
    assignments = _assignments(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, values in assignments.items():
        assert values <= ALLOWED_ASSIGNMENTS[field]
        assert values, field
    assert assignments["requested planning scope"] == REQUESTED_SCOPE
    assert assignments["excluded scope"] == EXCLUDED_SCOPE
    assert assignments["owner disposition posture"] == {"approve_narrow_source_fetching_planning_only"}
    assert assignments["recommended next track"] == {"narrow_source_fetching_implementation_planning"}


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- recommended next track: narrow_source_fetching_implementation_planning\n\n"
        "## Acceptance criteria\n"
        "- recommended next track: approve_source_fetching_implementation\n"
    )
    assert _assignments(synthetic) == {"recommended next track": {"narrow_source_fetching_implementation_planning"}}


def test_document_does_not_recommend_disallowed_implementation_tracks() -> None:
    text = _read().lower()
    forbidden = [
        "recommend provider connector implementation", "recommend source fetching implementation",
        "recommend forecast pulls", "recommend scoring", "recommend backtesting", "recommend runtime behavior",
        "recommend trading", "recommend autonomy", "recommend production behavior", "recommend generated data",
        "recommend fixture changes", "recommend workflows", "recommend dependencies", "recommend db migrations",
        "recommend schema changes", "recommend source-code migrations", "recommend compatibility shims",
    ]
    for phrase in forbidden:
        assert phrase not in text
