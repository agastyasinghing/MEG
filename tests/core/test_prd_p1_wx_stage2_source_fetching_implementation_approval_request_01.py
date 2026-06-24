"""Static checks for Weather Bot source-fetching implementation approval request."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-REQUEST-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-fetching implementation approval-request assignments"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to narrow implementation-planning closeout",
    "Relationship to narrow implementation planning", "Relationship to narrow planning request",
    "Relationship to owner disposition", "Relationship to hold checkpoint",
    "Relationship to Weather Bot PRD and architecture alignment", "Approval-request objective",
    "Owner continuation signal", "Requested approval path", "Requested narrow implementation scope",
    "Scope still not approved by this request", "Required later owner approval decision",
    "Proposed implementation boundaries for later approval", "Source identity and provenance requirements",
    "Retrieval context requirements", "No-lookahead requirements", "Provider/source family requirements",
    "Fetch-boundary requirements", "Credential/config requirements", "Generated-data and fixture requirements",
    "Static validation requirements", "Fail-closed requirements", "Approval posture", "Request-only posture",
    "Canonical identifier posture", "Provider/source compatibility posture", "Offline-ingestion boundary posture",
    "Test-scope posture", "Risk and failure-mode posture", "Explicit non-approval boundaries",
    "Blocked implementation work", "Recommended next ticket",
    "Machine-checkable source-fetching implementation approval-request assignments", "Acceptance criteria",
)
RELATIONSHIP_IDS = {
    CANONICAL_ID,
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
REQUESTED_SCOPE = {"source_identity_recording", "retrieval_context_recording", "provider_source_family_recording", "manual_review_gate", "no_lookahead_metadata_gate", "fail_closed_validation_gate", "static_audit_surface"}
EXCLUDED_APPROVALS = {"source_fetching_implementation_approved", "provider_connector_implementation_approved", "forecast_pull_execution_approved", "api_call_execution_approved", "scraping_execution_approved", "file_download_execution_approved", "provider_sdk_execution_approved", "credentials_config_loading_approved", "generated_data_creation_approved", "fixture_data_modification_approved", "scoring_implementation_approved", "backtesting_implementation_approved", "runtime_behavior_approved", "trading_behavior_approved", "autonomy_behavior_approved", "production_behavior_approved"}
SOURCE_FAMILIES = {"forecast_provider_family", "historical_observation_provider_family", "official_resolution_source_family", "market_metadata_source_family", "manual_human_review_source_family", "unsupported_source_family", "unknown_source_family"}
RETRIEVAL_MODES = {"manual_descriptor_only", "static_fixture_reference_only", "later_source_fetching_request", "later_provider_connector_request", "prohibited_until_explicit_approval", "unknown_requires_review"}
ACCESS_METHODS = {"manual_review", "static_reference", "api_call", "scraping", "file_download", "provider_sdk", "unknown_requires_review"}
CREDENTIAL_VALUES = {"none_required", "credentials_required_later", "config_required_later", "secrets_required_later", "unknown_requires_review"}
GENERATED_FIXTURE_VALUES = {"no_generated_data", "no_fixture_change", "generated_data_requires_later_approval", "fixture_change_requires_later_approval", "unknown_requires_review"}
NON_APPROVED_BEHAVIORS = {"provider_connector", "source_fetching", "forecast_pull", "api_call", "scraping", "credentials_secrets_config", "scoring_backtesting", "runtime_behavior", "trading_autonomy", "production_behavior", "generated_data", "fixture_change", "workflow_change", "dependency_change", "database_migration", "schema_change", "source_code_migration", "compatibility_shim"}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_implementation_approval_request"},
    "implementation approval request status": {"docs_static_test_only", "request_only", "post_pr_253_closeout"},
    "current state posture": {"post_closeout_hold_checkpoint", "implementation_not_approved"},
    "owner continuation posture": {"owner_requested_continue_beyond_hold"},
    "approval request posture": {"approval_request_only", "approval_decision_not_recorded", "implementation_not_approved_by_request", "later_owner_approval_decision_required"},
    "requested approval path": {"implementation_approval_request_only_after_explicit_owner_approval"},
    "requested narrow implementation scope": REQUESTED_SCOPE,
    "excluded approval": EXCLUDED_APPROVALS,
    "provider source posture": {"provider_connectors_not_approved", "source_fetching_implementation_not_approved", "forecast_pulls_not_approved", "api_calls_not_approved", "scraping_not_approved", "provider_source_approval_request_only"},
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "implementation posture": {"request_only", "docs_static_test_only", "no_provider_connector", "no_source_fetching_implementation", "no_forecast_pull", "no_api_call", "no_scraping", "no_file_download", "no_provider_sdk", "no_credentials_config_loading", "no_scoring_backtesting", "no_runtime_behavior", "no_trading_autonomy", "no_production_behavior", "no_generated_data", "no_fixture_change", "no_workflow_change", "no_dependency_change", "no_database_migration", "no_schema_change", "no_source_code_migration", "no_compatibility_shim"},
    "recommended next track": {"source_fetching_implementation_approval_decision"},
    "conditional next track": {"hold_checkpoint_if_approval_denied", "implementation_planning_revision_if_scope_too_broad", "narrow_source_fetching_implementation_plan_if_owner_approves"},
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
        "source-fetching implementation approval request only", "docs/static-test-only",
        "post-PR #253 narrow implementation-planning closeout state", "PR #253 defaulted to `hold_checkpoint`",
        "owner has explicitly requested to continue the gated path rather than remain at hold",
        "opens the `implementation_approval_request_only_after_explicit_owner_approval` path",
        "not an approval decision", "does not approve implementation by itself", "does not implement source fetching",
        "Source-fetching implementation is not approved by this artifact", "Provider connector implementation is not approved by this artifact",
        "Forecast pulls are not approved", "API calls are not approved", "Scraping is not approved", "File downloads are not approved",
        "Provider SDK usage is not approved", "Credentials/secrets/config loading is not approved",
        "Generated data is not approved or created", "Fixture changes are not approved or modified",
        "Scoring/backtesting/runtime/trading/autonomy/production behavior is not approved",
        "later separate explicit owner approval decision artifact", "Weather Bot models the market settlement rule, not generic weather",
        "No routing on `market_id` is introduced or approved",
    ]
    for phrase in required:
        assert phrase in text
    for value in REQUESTED_SCOPE | EXCLUDED_APPROVALS | SOURCE_FAMILIES | RETRIEVAL_MODES | ACCESS_METHODS | CREDENTIAL_VALUES | GENERATED_FIXTURE_VALUES | NON_APPROVED_BEHAVIORS:
        assert f"`{value}`" in text
    for token in ("condition_id", "token_id", "outcome"):
        assert f"`{token}`" in text
    for phrase in ("provider/source connector implementation", "real ingestion implementation", "live provider usage", "paper simulation", "runtime observation"):
        assert phrase in text


def test_machine_assignments_are_section_scoped_and_allowed() -> None:
    assignments = _assignments(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, values in assignments.items():
        assert values <= ALLOWED_ASSIGNMENTS[field]
        assert values, field
    for field, expected in ALLOWED_ASSIGNMENTS.items():
        assert expected <= assignments[field]
    assert assignments["recommended next track"] == {"source_fetching_implementation_approval_decision"}


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- recommended next track: source_fetching_implementation_approval_decision\n\n"
        "## Acceptance criteria\n"
        "- recommended next track: source_fetching_implementation_approved\n"
    )
    assert _assignments(synthetic) == {"recommended next track": {"source_fetching_implementation_approval_decision"}}


def test_document_does_not_assert_implementation_already_approved() -> None:
    text = _read().lower()
    forbidden = [
        "implementation has been approved", "implementation is approved by this request", "source-fetching implementation is approved",
        "provider connector implementation is approved", "forecast pulls are approved", "api calls are approved",
        "scraping is approved", "file downloads are approved", "provider sdk usage is approved",
        "credentials/secrets/config loading is approved", "generated data is approved", "fixture changes are approved",
        "scoring is approved", "backtesting is approved", "runtime behavior is approved", "trading is approved",
        "autonomy is approved", "production behavior is approved", "recommend provider connector implementation",
        "recommend source fetching implementation", "recommend forecast pulls", "recommend api calls", "recommend scraping",
        "recommend file downloads", "recommend provider sdk usage", "recommend generated data", "recommend fixture changes",
    ]
    for phrase in forbidden:
        assert phrase not in text
