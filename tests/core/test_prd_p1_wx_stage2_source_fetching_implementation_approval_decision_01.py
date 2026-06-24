"""Static checks for Weather Bot source-fetching implementation approval decision."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-DECISION-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-fetching implementation approval-decision assignments"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to implementation approval request",
    "Relationship to narrow implementation-planning closeout", "Relationship to narrow implementation planning",
    "Relationship to owner disposition", "Relationship to Weather Bot PRD and architecture alignment",
    "Decision objective", "Owner decision", "Approved narrow scope", "Scope not approved by this decision",
    "Required next implementation plan", "Required implementation boundaries", "Source identity and provenance requirements",
    "Retrieval context requirements", "No-lookahead requirements", "Provider/source family requirements",
    "Fetch-boundary requirements", "Credential/config requirements", "Generated-data and fixture requirements",
    "Static validation requirements", "Fail-closed requirements", "Approval posture", "Decision-only posture",
    "Canonical identifier posture", "Provider/source compatibility posture", "Offline-ingestion boundary posture",
    "Test-scope posture", "Risk and failure-mode posture", "Explicit non-approval boundaries",
    "Blocked implementation work", "Recommended next ticket",
    "Machine-checkable source-fetching implementation approval-decision assignments", "Acceptance criteria",
)
RELATIONSHIP_IDS = {
    CANONICAL_ID,
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
NOT_APPROVED_SCOPE = {"broad_source_fetching_implementation", "provider_connector_implementation", "live_provider_source_fetching", "forecast_pull_execution", "api_call_execution", "scraping_execution", "file_download_execution", "provider_sdk_execution", "credentials_config_loading", "generated_data_creation", "fixture_data_modification", "scoring_implementation", "backtesting_implementation", "runtime_trading_behavior", "autonomy_behavior", "production_behavior"}
SOURCE_FAMILIES = {"forecast_provider_family", "historical_observation_provider_family", "official_resolution_source_family", "market_metadata_source_family", "manual_human_review_source_family", "unsupported_source_family", "unknown_source_family"}
RETRIEVAL_MODES = {"manual_descriptor_only", "static_fixture_reference_only", "later_source_fetching_request", "later_provider_connector_request", "prohibited_until_explicit_approval", "unknown_requires_review"}
ACCESS_METHODS = {"manual_review", "static_reference", "api_call", "scraping", "file_download", "provider_sdk", "unknown_requires_review"}
CREDENTIAL_VALUES = {"none_required", "credentials_required_later", "config_required_later", "secrets_required_later", "unknown_requires_review"}
GENERATED_FIXTURE_VALUES = {"no_generated_data", "no_fixture_change", "generated_data_requires_later_approval", "fixture_change_requires_later_approval", "unknown_requires_review"}
NON_APPROVED_BEHAVIORS = {"provider_connector", "source_fetching", "forecast_pull", "api_call", "scraping", "credentials_secrets_config", "scoring_backtesting", "runtime_behavior", "trading_autonomy", "production_behavior", "generated_data", "fixture_change", "workflow_change", "dependency_change", "database_migration", "schema_change", "source_code_migration", "compatibility_shim"}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_implementation_approval_decision"},
    "implementation approval decision status": {"docs_static_test_only", "decision_only", "post_pr_254_approval_request"},
    "current state posture": {"implementation_plan_approved_only", "runtime_not_approved"},
    "owner decision": {"approve_narrow_source_fetching_implementation_plan"},
    "approved narrow implementation scope": APPROVED_SCOPE,
    "not approved scope": NOT_APPROVED_SCOPE,
    "provider source posture": {"provider_connectors_not_approved", "live_provider_source_fetching_not_approved", "forecast_pulls_not_approved", "api_calls_not_approved", "scraping_not_approved", "provider_source_decision_narrow_plan_only"},
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "implementation posture": {"decision_only", "docs_static_test_only", "narrow_plan_approved_only", "no_provider_connector", "no_live_provider_fetching", "no_forecast_pull", "no_api_call", "no_scraping", "no_file_download", "no_provider_sdk", "no_credentials_config_loading", "no_scoring_backtesting", "no_runtime_trading", "no_autonomy", "no_production_behavior", "no_generated_data", "no_fixture_change", "no_workflow_change", "no_dependency_change", "no_database_migration", "no_schema_change", "no_source_code_migration", "no_compatibility_shim"},
    "recommended next track": {"narrow_source_fetching_implementation_plan"},
    "conditional next track": {"implementation_planning_revision_if_scope_too_broad", "hold_checkpoint_if_scope_violation_found", "runtime_approval_request_only_after_static_plan_lands"},
    "evidence status": {"decision_recorded"},
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
        "source-fetching implementation approval decision artifact", "docs/static-test-only", "decision-only",
        "PR #254 is the latest completed approval-request predecessor",
        "PR #254", "created `PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-REQUEST-01`",
        "selected owner decision is exactly `approve_narrow_source_fetching_implementation_plan`",
        "permits only a later narrow source-fetching implementation plan/ticket", "does not itself implement source fetching",
        "does not approve broad source-fetching implementation", "does not approve provider connector implementation",
        "does not approve live provider/source fetching yet", "does not approve forecast pulls yet",
        "does not approve API calls yet", "does not approve scraping yet", "does not approve file downloads yet",
        "does not approve provider SDK usage yet", "does not approve credentials/secrets/config loading yet",
        "does not approve generated data", "does not approve fixture changes", "does not approve scoring",
        "does not approve backtesting", "does not approve trading, order placement, autonomy, or production behavior",
        "static validation, no-lookahead, provenance, and fail-closed gates", "Weather Bot models the market settlement rule, not generic weather",
        "No routing on `market_id` is introduced or approved",
    ]
    for phrase in required:
        assert phrase in text
    for value in APPROVED_SCOPE | NOT_APPROVED_SCOPE | SOURCE_FAMILIES | RETRIEVAL_MODES | ACCESS_METHODS | CREDENTIAL_VALUES | GENERATED_FIXTURE_VALUES | NON_APPROVED_BEHAVIORS:
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
    assert assignments["owner decision"] == {"approve_narrow_source_fetching_implementation_plan"}
    assert assignments["recommended next track"] == {"narrow_source_fetching_implementation_plan"}


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- recommended next track: narrow_source_fetching_implementation_plan\n\n"
        "## Acceptance criteria\n"
        "- recommended next track: live_provider_source_fetching\n"
    )
    assert _assignments(synthetic) == {"recommended next track": {"narrow_source_fetching_implementation_plan"}}


def test_document_does_not_assert_runtime_or_broad_approval() -> None:
    text = _read().lower()
    forbidden = [
        "broad source-fetching implementation is approved", "provider connector implementation is approved",
        "live provider/source fetching is approved", "forecast pulls are approved", "api calls are approved",
        "scraping is approved", "file downloads are approved", "provider sdk usage is approved",
        "credentials/secrets/config loading is approved", "generated data is approved", "fixture changes are approved",
        "scoring is approved", "backtesting is approved", "runtime behavior is approved", "trading is approved",
        "autonomy is approved", "production behavior is approved", "runtime behavior, live provider fetching, trading, autonomy, or production behavior is approved",
        "recommend provider connector implementation", "recommend broad source fetching implementation", "recommend forecast pulls",
        "recommend api calls", "recommend scraping", "recommend file downloads", "recommend provider sdk usage",
        "recommend generated data", "recommend fixture changes",
    ]
    for phrase in forbidden:
        assert phrase not in text
