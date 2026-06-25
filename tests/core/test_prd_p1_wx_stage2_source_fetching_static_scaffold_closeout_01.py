"""Static checks for Weather Bot narrow source-fetching static scaffold closeout."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-CLOSEOUT-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-fetching static-scaffold closeout assignments"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to static scaffold", "Relationship to narrow implementation plan",
    "Relationship to implementation approval decision", "Relationship to Weather Bot PRD and architecture alignment", "Closeout objective",
    "Closed static scaffold scope", "Closed static scaffold surfaces", "Closed future static module names",
    "Closed future static test names", "Closed future static field names", "Closed fail-closed expectations",
    "Closed no-lookahead and provenance expectations", "Runtime boundary closeout", "Provider/source execution boundary closeout",
    "Credential/config boundary closeout", "Generated-data and fixture boundary closeout", "Canonical identifier posture",
    "Provider/source compatibility posture", "Offline-ingestion boundary posture", "Test-scope posture",
    "Risk and failure-mode posture", "Explicit non-execution boundaries", "Blocked implementation work",
    "Recommended next ticket", "Machine-checkable source-fetching static-scaffold closeout assignments", "Acceptance criteria",
)
RELATIONSHIP_IDS = {
    CANONICAL_ID,
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLAN-01",
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
CLOSED_SCOPE = {"source_identity_recording", "retrieval_context_recording", "provider_source_family_recording", "manual_review_gate", "no_lookahead_metadata_gate", "fail_closed_validation_gate", "static_audit_surface"}
SURFACES = {"SourceIdentityRecord", "RetrievalContextRecord", "ProviderSourceFamilyRecord", "ManualReviewGate", "NoLookaheadMetadataGate", "FailClosedValidationGate", "StaticAuditSurface"}
MODULES = {"source_identity_static", "retrieval_context_static", "provider_source_family_static", "manual_review_gate_static", "no_lookahead_gate_static", "fail_closed_validation_static", "static_audit_surface"}
TESTS = {"test_source_identity_static", "test_retrieval_context_static", "test_provider_source_family_static", "test_manual_review_gate_static", "test_no_lookahead_gate_static", "test_fail_closed_validation_static", "test_static_audit_surface"}
FIELDS = {"source_id", "source_family", "source_uri_descriptor", "accessed_at_utc", "retrieved_at_utc", "available_at_utc", "market_resolution_time_utc", "decision_time_utc", "no_lookahead_verified", "manual_review_required", "review_status", "provenance_notes"}
FAILS = {"missing_source_identity", "unknown_source_family", "missing_access_time", "missing_retrieval_time", "missing_availability_time", "missing_decision_time", "missing_market_resolution_time", "missing_no_lookahead_verification", "manual_review_required_not_complete", "unsupported_source_family", "ambiguous_credential_config_posture", "ambiguous_generated_data_fixture_posture"}
NOT_EXECUTED = {"runtime_source_fetching", "source_fetching_implementation", "provider_connector_implementation", "provider_client_creation", "live_provider_source_fetching", "forecast_pull_execution", "api_call_execution", "scraping_execution", "file_download_execution", "provider_sdk_execution", "credentials_config_loading", "generated_data_creation", "fixture_data_modification", "scoring_implementation", "backtesting_implementation", "runtime_trading_behavior", "autonomy_behavior", "production_behavior"}
SOURCE_FAMILIES = {"forecast_provider_family", "historical_observation_provider_family", "official_resolution_source_family", "market_metadata_source_family", "manual_human_review_source_family", "unsupported_source_family", "unknown_source_family"}
RETRIEVAL_MODES = {"manual_descriptor_only", "static_fixture_reference_only", "later_source_fetching_request", "later_provider_connector_request", "prohibited_until_explicit_approval", "unknown_requires_review"}
ACCESS_METHODS = {"manual_review", "static_reference", "api_call", "scraping", "file_download", "provider_sdk", "unknown_requires_review"}
CREDENTIAL_VALUES = {"none_required", "credentials_required_later", "config_required_later", "secrets_required_later", "unknown_requires_review"}
GENERATED_FIXTURE_VALUES = {"no_generated_data", "no_fixture_change", "generated_data_requires_later_approval", "fixture_change_requires_later_approval", "unknown_requires_review"}
NON_APPROVED_BEHAVIORS = {"provider_connector", "source_fetching", "forecast_pull", "api_call", "scraping", "credentials_secrets_config", "scoring_backtesting", "runtime_behavior", "trading_autonomy", "production_behavior", "generated_data", "fixture_change", "workflow_change", "dependency_change", "database_migration", "schema_change", "source_code_migration", "compatibility_shim"}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_static_scaffold_closeout"},
    "static scaffold closeout status": {"docs_static_test_only", "closeout_only", "post_pr_257_static_scaffold"},
    "current state posture": {"static_scaffold_closed", "runtime_not_approved"},
    "closed static scaffold scope": CLOSED_SCOPE,
    "closed static scaffold surface": SURFACES,
    "closed future static module": MODULES,
    "closed future static test": TESTS,
    "closed future static field": FIELDS,
    "closed fail closed expectation": FAILS,
    "not executed scope": NOT_EXECUTED,
    "provider source posture": {"provider_connectors_not_approved", "provider_clients_not_created", "live_provider_source_fetching_not_approved", "forecast_pulls_not_approved", "api_calls_not_approved", "scraping_not_approved", "provider_source_static_scaffold_closed"},
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "implementation posture": {"closeout_only", "docs_static_test_only", "no_runtime_source_fetching", "no_code_implementation", "no_provider_connector", "no_provider_client", "no_live_provider_fetching", "no_forecast_pull", "no_api_call", "no_scraping", "no_file_download", "no_provider_sdk", "no_credentials_config_loading", "no_scoring_backtesting", "no_runtime_trading", "no_autonomy", "no_production_behavior", "no_generated_data", "no_fixture_change", "no_workflow_change", "no_dependency_change", "no_database_migration", "no_schema_change", "no_source_code_migration", "no_compatibility_shim"},
    "recommended next track": {"narrow_source_fetching_runtime_approval_request"},
    "conditional next track": {"hold_checkpoint_if_runtime_approval_not_requested", "scaffold_revision_if_scope_gap_found", "runtime_approval_request_only_after_static_scaffold_closeout"},
    "evidence status": {"closeout_recorded"},
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


def test_required_static_scaffold_posture_and_non_approval_language() -> None:
    text = _read()
    required = [
        "narrow source-fetching static scaffold closeout artifact only", "docs/static-test-only/closeout-only",
        "PR #257 is the latest completed static-scaffold predecessor",
        "PR #257 recommended `narrow_source_fetching_static_scaffold_closeout`", "does not implement runtime source fetching",
        "does not modify runtime code", "does not create provider connectors",
        "does not create provider clients", "does not call providers", "does not approve live provider/source fetching",
        "does not approve forecast pulls", "does not approve API calls", "does not approve scraping",
        "does not approve file downloads", "does not approve provider SDK usage",
        "does not approve credentials/secrets/config loading", "does not approve generated data",
        "does not approve fixture changes", "does not approve scoring", "does not approve backtesting",
        "does not approve runtime trading", "does not approve autonomy", "does not approve production behavior",
        "Weather Bot models the market settlement rule, not generic weather",
        "no routing on `market_id` is introduced or approved",
        "Recommended next track: `narrow_source_fetching_runtime_approval_request`",
    ]
    for phrase in required:
        assert phrase in text
    for value in (CLOSED_SCOPE | SURFACES | MODULES | TESTS | FIELDS | FAILS | NOT_EXECUTED | SOURCE_FAMILIES |
                  RETRIEVAL_MODES | ACCESS_METHODS | CREDENTIAL_VALUES | GENERATED_FIXTURE_VALUES | NON_APPROVED_BEHAVIORS):
        assert value in text
    for identifier in ("condition_id", "token_id", "outcome"):
        assert f"`{identifier}`" in text


def test_machine_checkable_assignments_are_section_scoped_and_allowed() -> None:
    assignments = _assignments(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field]
        assert assignments[field] <= allowed_values
    assert assignments["closed static scaffold scope"] == CLOSED_SCOPE
    assert assignments["closed static scaffold surface"] == SURFACES
    assert assignments["closed future static module"] == MODULES
    assert assignments["closed future static test"] == TESTS
    assert assignments["closed future static field"] == FIELDS
    assert assignments["closed fail closed expectation"] == FAILS
    assert assignments["not executed scope"] == NOT_EXECUTED
    assert assignments["recommended next track"] == {"narrow_source_fetching_runtime_approval_request"}


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- recommended next track: narrow_source_fetching_runtime_approval_request\n"
        "## Later heading\n"
        "- recommended next track: runtime_behavior_approved\n"
    )
    assert _assignments(synthetic) == {"recommended next track": {"narrow_source_fetching_runtime_approval_request"}}


def test_document_does_not_assert_unsafe_approval() -> None:
    text = _read().lower()
    forbidden_positive_patterns = [
        r"runtime source fetching approved", r"source fetching implementation approved",
        r"provider connector implementation approved", r"provider clients created",
        r"live provider source fetching approved", r"forecast pulls approved", r"api calls approved",
        r"scraping approved", r"file downloads approved", r"provider sdk usage approved",
        r"credentials/secrets/config loading approved", r"generated data approved", r"fixture changes approved",
        r"scoring approved", r"backtesting approved", r"runtime trading approved", r"trading approved",
        r"autonomy approved", r"production behavior approved", r"generated data created", r"fixture data modified",
    ]
    for pattern in forbidden_positive_patterns:
        assert not re.search(pattern, text)
