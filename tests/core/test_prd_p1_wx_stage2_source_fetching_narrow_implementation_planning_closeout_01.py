"""Static checks for Weather Bot narrow source-fetching implementation-planning closeout."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-CLOSEOUT-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-fetching narrow implementation-planning closeout assignments"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to narrow implementation planning", "Relationship to narrow planning request",
    "Relationship to owner disposition", "Relationship to hold checkpoint", "Relationship to Weather Bot PRD and architecture alignment",
    "Closeout objective", "Closed planning layer", "Planning artifacts summarized", "Seam-planning closeout",
    "Source identity and provenance closeout", "Retrieval context closeout", "No-lookahead closeout",
    "Provider/source family closeout", "Fetch-boundary closeout", "Credential/config closeout",
    "Generated-data and fixture closeout", "Static validation closeout", "Fail-closed closeout", "Later approval gates",
    "Default next state", "Conditional next states", "Approval posture", "Planning-only posture",
    "Canonical identifier posture", "Provider/source compatibility posture", "Offline-ingestion boundary posture",
    "Test-scope posture", "Risk and failure-mode posture", "Explicit non-approval boundaries",
    "Blocked implementation work", "Recommended next ticket",
    "Machine-checkable source-fetching narrow implementation-planning closeout assignments", "Acceptance criteria",
)
RELATIONSHIP_IDS = {
    CANONICAL_ID, "PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-01",
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
SEAM = {"source_descriptor_in", "source_identity_record", "retrieval_context_record", "provider_source_family_record", "fetch_boundary_plan", "credential_config_boundary_plan", "generated_data_fixture_boundary_plan", "static_validation_audit_plan", "fail_closed_plan"}
SOURCE_REQ = {"source_identity_recorded_before_fetch_implementation", "source_family_recorded_before_fetch_implementation", "provider_source_provenance_recorded_before_fetch_implementation", "manual_review_before_known_source_family", "no_unreviewed_source_identity_in_probability_logic"}
RETRIEVAL_REQ = {"access_date_recorded", "retrieval_timestamp_recorded", "retrieval_context_recorded", "market_resolution_timing_relationship_recorded", "source_availability_timing_recorded", "no_source_without_access_date_context"}
NO_LOOKAHEAD = {"no_post_resolution_evidence_for_pre_resolution_labels", "no_unavailable_at_decision_time_source_use", "no_generated_labels_from_future_information", "no_settlement_leakage", "no_backfilled_source_data_without_access_date_context"}
FAMILIES = {"forecast_provider_family", "historical_observation_provider_family", "official_resolution_source_family", "market_metadata_source_family", "manual_human_review_source_family", "unsupported_source_family", "unknown_source_family"}
EXCLUSIONS = {"source_fetching_implementation", "provider_connector_implementation", "forecast_pull_execution", "api_call_execution", "scraping_execution", "file_download_execution", "provider_sdk_execution", "credentials_config_loading", "generated_data_creation", "fixture_data_modification", "scoring_implementation", "backtesting_implementation", "runtime_behavior", "trading_behavior", "autonomy_behavior", "production_behavior", "workflow_change", "dependency_change", "database_migration", "schema_change", "source_code_migration", "compatibility_shim"}
CLOSED_SET_VALUES = FAMILIES | {"manual_descriptor_only", "static_fixture_reference_only", "later_source_fetching_request", "later_provider_connector_request", "prohibited_until_explicit_approval", "unknown_requires_review", "manual_review", "static_reference", "api_call", "scraping", "file_download", "provider_sdk", "none_required", "credentials_required_later", "config_required_later", "secrets_required_later", "no_generated_data", "no_fixture_change", "generated_data_requires_later_approval", "fixture_change_requires_later_approval"}
NON_APPROVED_BEHAVIORS = {"provider_connector", "source_fetching", "forecast_pull", "api_call", "scraping", "credentials_secrets_config", "scoring_backtesting", "runtime_behavior", "trading_autonomy", "production_behavior", "generated_data", "fixture_change", "workflow_change", "dependency_change", "database_migration", "schema_change", "source_code_migration", "compatibility_shim"}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_narrow_implementation_planning_closeout"},
    "narrow implementation planning closeout status": {"docs_static_test_only", "closeout_only", "post_pr_252_narrow_implementation_planning"},
    "current state posture": {"hold_checkpoint", "implementation_not_approved"},
    "closed planning artifact": {"PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-01"},
    "closed seam component": SEAM,
    "closed source identity requirement": SOURCE_REQ,
    "closed retrieval context requirement": RETRIEVAL_REQ,
    "closed no lookahead requirement": NO_LOOKAHEAD,
    "closed provider source family": FAMILIES,
    "preserved exclusion": EXCLUSIONS,
    "approval posture": {"implementation_not_approved", "source_fetching_implementation_not_approved", "provider_connector_implementation_not_approved", "later_explicit_owner_approval_required"},
    "provider source posture": {"provider_connectors_not_approved", "source_fetching_implementation_not_approved", "forecast_pulls_not_approved", "api_calls_not_approved", "scraping_not_approved", "provider_source_planning_closed"},
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "implementation posture": {"closeout_only", "docs_static_test_only", "no_provider_connector", "no_source_fetching_implementation", "no_forecast_pull", "no_api_call", "no_scraping", "no_file_download", "no_provider_sdk", "no_credentials_config_loading", "no_scoring_backtesting", "no_runtime_behavior", "no_trading_autonomy", "no_production_behavior", "no_generated_data", "no_fixture_change", "no_workflow_change", "no_dependency_change", "no_database_migration", "no_schema_change", "no_source_code_migration", "no_compatibility_shim"},
    "recommended next track": {"hold_checkpoint"},
    "conditional next track": {"implementation_approval_request_only_after_explicit_owner_approval", "planning_revision_if_scope_exceeds_permission", "additional_docs_only_evidence_if_needed"},
    "evidence status": {"closeout_only"},
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
        "narrow implementation-planning closeout only", "docs/static-test-only", "PR #252 is the latest completed narrow implementation-planning predecessor",
        "PR #252 created `PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-01`",
        "closed at the docs/static-test-only planning level only", "does not approve implementation", "does not implement source fetching",
        "Source-fetching implementation is not approved", "Provider connector implementation is not approved", "Forecast pulls are not approved",
        "API calls are not approved", "Scraping is not approved", "File downloads are not approved", "Provider SDK usage is not approved",
        "Credentials/secrets/config loading is not approved", "Generated data is not approved or created", "Fixture changes are not approved or modified",
        "Scoring/backtesting/runtime/trading/autonomy/production behavior is not approved", "Actual implementation requires later separate explicit owner approval",
        "default next state is `hold_checkpoint`", "implementation approval request is conditional only after later explicit owner approval",
        "Weather Bot models the market settlement rule, not generic weather", "No routing on `market_id` is introduced or approved",
    ]
    for phrase in required:
        assert phrase in text
    for value in SEAM | SOURCE_REQ | RETRIEVAL_REQ | NO_LOOKAHEAD | FAMILIES | EXCLUSIONS | CLOSED_SET_VALUES | NON_APPROVED_BEHAVIORS:
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
    assert assignments["recommended next track"] == {"hold_checkpoint"}


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- recommended next track: hold_checkpoint\n\n"
        "## Acceptance criteria\n"
        "- recommended next track: approve_source_fetching_implementation\n"
    )
    assert _assignments(synthetic) == {"recommended next track": {"hold_checkpoint"}}


def test_document_does_not_recommend_disallowed_implementation_tracks() -> None:
    text = _read().lower()
    forbidden = [
        "recommend provider connector implementation", "recommend source fetching implementation", "recommend forecast pulls",
        "recommend api calls", "recommend scraping", "recommend file downloads", "recommend provider sdk use",
        "recommend scoring", "recommend backtesting", "recommend runtime behavior", "recommend trading",
        "recommend autonomy", "recommend production behavior", "recommend generated data", "recommend fixture changes",
        "recommend workflows", "recommend dependencies", "recommend db migrations", "recommend schema changes",
        "recommend source-code migrations", "recommend compatibility shims",
    ]
    for phrase in forbidden:
        assert phrase not in text
