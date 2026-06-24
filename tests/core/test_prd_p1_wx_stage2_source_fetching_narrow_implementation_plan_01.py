"""Static checks for Weather Bot narrow source-fetching implementation plan."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLAN-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-fetching narrow implementation-plan assignments"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to implementation approval decision",
    "Relationship to implementation approval request", "Relationship to narrow implementation-planning closeout",
    "Relationship to narrow implementation planning", "Relationship to Weather Bot PRD and architecture alignment",
    "Plan objective", "Approved narrow scope", "Planned future implementation surfaces",
    "Planned source identity recording", "Planned retrieval context recording",
    "Planned provider/source family recording", "Planned manual review gate",
    "Planned no-lookahead metadata gate", "Planned fail-closed validation gate", "Planned static audit surface",
    "Future file and module boundaries", "Future data model boundaries", "Future validation boundaries",
    "Future test boundaries", "Future rollout boundary", "Scope not implemented by this plan",
    "Scope not approved for runtime", "Credential/config boundary", "Generated-data and fixture boundary",
    "Canonical identifier posture", "Provider/source compatibility posture", "Offline-ingestion boundary posture",
    "Test-scope posture", "Risk and failure-mode posture", "Explicit non-implementation boundaries",
    "Blocked implementation work", "Recommended next ticket",
    "Machine-checkable source-fetching narrow implementation-plan assignments", "Acceptance criteria",
)
RELATIONSHIP_IDS = {
    CANONICAL_ID,
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-DECISION-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-REQUEST-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-PLANNING-REQUEST-01",
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
    "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01", "MEG-ARCH-ALIGN-08",
    "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD",
}
APPROVED_SCOPE = {"source_identity_recording", "retrieval_context_recording", "provider_source_family_recording", "manual_review_gate", "no_lookahead_metadata_gate", "fail_closed_validation_gate", "static_audit_surface"}
SURFACES = {"SourceIdentityRecord", "RetrievalContextRecord", "ProviderSourceFamilyRecord", "ManualReviewGate", "NoLookaheadMetadataGate", "FailClosedValidationGate", "StaticAuditSurface"}
FIELDS = {"source_id", "source_family", "source_uri_descriptor", "accessed_at_utc", "retrieved_at_utc", "available_at_utc", "market_resolution_time_utc", "decision_time_utc", "no_lookahead_verified", "manual_review_required", "review_status", "provenance_notes"}
FAILS = {"missing_source_identity", "unknown_source_family", "missing_access_time", "missing_retrieval_time", "missing_availability_time", "missing_decision_time", "missing_market_resolution_time", "missing_no_lookahead_verification", "manual_review_required_not_complete", "unsupported_source_family", "ambiguous_credential_config_posture", "ambiguous_generated_data_fixture_posture"}
NOT_IMPLEMENTED = {"source_fetching_implementation", "provider_connector_implementation", "live_provider_source_fetching", "forecast_pull_execution", "api_call_execution", "scraping_execution", "file_download_execution", "provider_sdk_execution", "credentials_config_loading", "generated_data_creation", "fixture_data_modification", "scoring_implementation", "backtesting_implementation", "runtime_trading_behavior", "autonomy_behavior", "production_behavior"}
SOURCE_FAMILIES = {"forecast_provider_family", "historical_observation_provider_family", "official_resolution_source_family", "market_metadata_source_family", "manual_human_review_source_family", "unsupported_source_family", "unknown_source_family"}
RETRIEVAL_MODES = {"manual_descriptor_only", "static_fixture_reference_only", "later_source_fetching_request", "later_provider_connector_request", "prohibited_until_explicit_approval", "unknown_requires_review"}
ACCESS_METHODS = {"manual_review", "static_reference", "api_call", "scraping", "file_download", "provider_sdk", "unknown_requires_review"}
CREDENTIAL_VALUES = {"none_required", "credentials_required_later", "config_required_later", "secrets_required_later", "unknown_requires_review"}
GENERATED_FIXTURE_VALUES = {"no_generated_data", "no_fixture_change", "generated_data_requires_later_approval", "fixture_change_requires_later_approval", "unknown_requires_review"}
NON_APPROVED_BEHAVIORS = {"provider_connector", "source_fetching", "forecast_pull", "api_call", "scraping", "credentials_secrets_config", "scoring_backtesting", "runtime_behavior", "trading_autonomy", "production_behavior", "generated_data", "fixture_change", "workflow_change", "dependency_change", "database_migration", "schema_change", "source_code_migration", "compatibility_shim"}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_narrow_implementation_plan"},
    "narrow implementation plan status": {"docs_static_test_only", "plan_only", "post_pr_255_approval_decision"},
    "current state posture": {"narrow_plan_approved_only", "runtime_not_approved"},
    "owner decision": {"approve_narrow_source_fetching_implementation_plan"},
    "approved narrow implementation scope": APPROVED_SCOPE,
    "planned future surface": SURFACES,
    "planned future field": FIELDS,
    "planned fail closed condition": FAILS,
    "not implemented scope": NOT_IMPLEMENTED,
    "provider source posture": {"provider_connectors_not_approved", "live_provider_source_fetching_not_approved", "forecast_pulls_not_approved", "api_calls_not_approved", "scraping_not_approved", "provider_source_plan_only"},
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "implementation posture": {"plan_only", "docs_static_test_only", "no_code_implementation", "no_provider_connector", "no_live_provider_fetching", "no_forecast_pull", "no_api_call", "no_scraping", "no_file_download", "no_provider_sdk", "no_credentials_config_loading", "no_scoring_backtesting", "no_runtime_trading", "no_autonomy", "no_production_behavior", "no_generated_data", "no_fixture_change", "no_workflow_change", "no_dependency_change", "no_database_migration", "no_schema_change", "no_source_code_migration", "no_compatibility_shim"},
    "recommended next track": {"narrow_source_fetching_static_scaffold"},
    "conditional next track": {"implementation_plan_revision_if_scope_too_broad", "hold_checkpoint_if_scope_violation_found", "runtime_approval_request_only_after_static_scaffold_lands"},
    "evidence status": {"plan_recorded"},
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


def test_required_posture_scope_and_non_approval_language() -> None:
    text = _read()
    required = [
        "narrow source-fetching implementation plan artifact only", "docs/static-test-only", "plan-only",
        "PR #255 is the latest completed approval-decision predecessor",
        "PR #255 selected owner decision exactly `approve_narrow_source_fetching_implementation_plan`",
        "does not implement source fetching", "does not modify runtime code", "does not approve live provider/source fetching",
        "does not approve provider connector implementation", "does not approve forecast pulls", "does not approve API calls",
        "does not approve scraping", "does not approve file downloads", "does not approve provider SDK usage",
        "does not approve credentials/secrets/config loading", "does not approve generated data", "does not approve fixture changes",
        "does not approve scoring", "does not approve backtesting", "does not approve runtime trading",
        "does not approve autonomy", "does not approve production behavior", "Weather Bot models the market settlement rule, not generic weather",
        "no routing on `market_id` is introduced or approved", "Recommended next track: `narrow_source_fetching_static_scaffold`",
    ]
    for phrase in required:
        assert phrase in text
    for value in APPROVED_SCOPE | SURFACES | FIELDS | FAILS | NOT_IMPLEMENTED | SOURCE_FAMILIES | RETRIEVAL_MODES | ACCESS_METHODS | CREDENTIAL_VALUES | GENERATED_FIXTURE_VALUES | NON_APPROVED_BEHAVIORS:
        assert value in text
    for identifier in ("condition_id", "token_id", "outcome"):
        assert f"`{identifier}`" in text


def test_machine_checkable_assignments_are_section_scoped_and_allowed() -> None:
    text = _read()
    assignments = _assignments(text)
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field]
        assert assignments[field] <= allowed_values
    assert assignments["owner decision"] == {"approve_narrow_source_fetching_implementation_plan"}
    assert assignments["approved narrow implementation scope"] == APPROVED_SCOPE
    assert assignments["planned future surface"] == SURFACES
    assert assignments["planned future field"] == FIELDS
    assert assignments["planned fail closed condition"] == FAILS
    assert assignments["not implemented scope"] == NOT_IMPLEMENTED
    assert assignments["recommended next track"] == {"narrow_source_fetching_static_scaffold"}


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- owner decision: approve_narrow_source_fetching_implementation_plan\n"
        "## Later heading\n"
        "- owner decision: runtime_behavior_approved\n"
    )
    assert _assignments(synthetic) == {"owner decision": {"approve_narrow_source_fetching_implementation_plan"}}


def test_document_does_not_assert_unsafe_approval() -> None:
    text = _read().lower()
    forbidden_positive_patterns = [
        r"runtime behavior is approved", r"live provider source fetching is approved", r"provider connectors are approved",
        r"trading is approved", r"autonomy is approved", r"production behavior is approved",
        r"generated data is approved", r"fixture changes are approved", r"code implementation is approved",
    ]
    for pattern in forbidden_positive_patterns:
        assert not re.search(pattern, text)
