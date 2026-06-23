"""Static checks for Weather Bot source-fetching owner-disposition planning."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-PLANNING-01.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-PLANNING-01"
MACHINE_HEADING = "## Machine-checkable source-fetching approval-request owner-disposition planning assignments"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to meta refresh", "Relationship to hold checkpoint",
    "Relationship to draft closeout", "Relationship to source-fetching approval-request draft",
    "Relationship to source-fetching approval-request planning sequence",
    "Relationship to provider/source compatibility sequence",
    "Relationship to Weather Bot PRD and architecture alignment", "Owner-disposition planning objective",
    "Current state before owner disposition", "No default human-review posture",
    "Later owner-disposition artifact requirements", "Allowed owner-disposition decisions",
    "Disallowed owner-disposition decisions", "Approval posture", "Planning-only posture",
    "Canonical identifier posture", "Source identity and provenance posture",
    "Access-date and retrieval-context posture", "No-lookahead posture",
    "Provider/source compatibility posture", "Offline-ingestion boundary posture",
    "Credential/config posture", "Generated-data and fixture posture", "Test-scope posture",
    "Risk and failure-mode posture", "Explicit non-approval boundaries", "Blocked implementation work",
    "Recommended next ticket", "Machine-checkable source-fetching approval-request owner-disposition planning assignments",
    "Acceptance criteria",
)
RELATIONSHIP_IDS = {
    CANONICAL_ID,
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
ALLOWED_DECISIONS = {
    "remain_hold_checkpoint", "request_draft_revision", "request_additional_docs_only_evidence",
    "approve_narrow_source_fetching_planning_only", "reject_source_fetching_request",
}
DISALLOWED_DECISIONS = {
    "approve_source_fetching_implementation", "approve_provider_connector_implementation",
    "approve_forecast_pulls", "approve_api_calls", "approve_scraping",
    "approve_credentials_config_loading", "approve_generated_data", "approve_fixture_changes",
    "approve_scoring", "approve_backtesting", "approve_runtime_behavior", "approve_trading",
    "approve_autonomy", "approve_production_behavior",
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
    "weather bot planning stage": {"source_fetching_approval_request_owner_disposition_planning"},
    "owner disposition planning status": {"docs_static_test_only", "planning_only", "post_pr_248_meta_refresh"},
    "current state posture": {"hold_checkpoint", "draft_sequence_paused"},
    "human review posture": {"no_default_human_review_pending", "owner_disposition_required_for_next_gate"},
    "approval request posture": {"approval_not_granted", "source_fetching_not_approved", "implementation_not_approved", "later_explicit_approval_required"},
    "owner disposition posture": {"disposition_artifact_not_created", "disposition_options_planned_only"},
    "allowed owner disposition decision": ALLOWED_DECISIONS,
    "disallowed owner disposition decision": DISALLOWED_DECISIONS,
    "provider source posture": {"provider_connectors_not_approved", "source_fetching_not_approved", "forecast_pulls_not_approved", "api_calls_not_approved", "scraping_not_approved", "provider_source_planning_only"},
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "approval decision posture": {"approval_granted_pending_placeholder_only", "approved_scope_none", "implementation_allowed_no", "owner_disposition_required"},
    "implementation posture": {"owner_disposition_planning_only", "docs_static_test_only", "no_provider_connector", "no_source_fetching", "no_forecast_pull", "no_api_call", "no_scraping", "no_credentials_config_loading", "no_scoring_backtesting", "no_runtime_behavior", "no_trading_autonomy", "no_production_behavior", "no_generated_data", "no_fixture_change", "no_workflow_change", "no_dependency_change", "no_database_migration", "no_schema_change", "no_source_code_migration", "no_compatibility_shim"},
    "recommended next track": {"source_fetching_approval_request_owner_disposition"},
    "conditional next track": {"hold_checkpoint_if_owner_chooses_hold", "source_fetching_approval_request_draft_revision_if_owner_requests_revision", "additional_docs_only_evidence_if_owner_requests_evidence", "narrow_source_fetching_planning_request_if_owner_approves_planning_only"},
    "evidence status": {"not_applicable"},
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


def test_required_posture_and_non_approval_language() -> None:
    text = _read()
    required = [
        "owner-disposition planning only", "docs/static-test-only",
        "PR #248 is the latest completed meta-refresh predecessor",
        "current safe next state entering this ticket is `hold_checkpoint`",
        "no separate human-review ticket is pending by default",
        "plans a later owner-disposition artifact but is not that artifact",
        "does not grant approval", "does not approve source fetching", "does not approve implementation",
        "does not recommend implementation", "No approval has been granted",
        "Source fetching is not approved", "Implementation is not approved",
        "Weather Bot models the market settlement rule, not generic weather",
        "No routing on `market_id` is introduced or approved",
    ]
    for phrase in required:
        assert phrase in text
    for token in ("condition_id", "token_id", "outcome"):
        assert f"`{token}`" in text
    for value in CLOSED_SET_VALUES | NON_APPROVED_BEHAVIORS | ALLOWED_DECISIONS | DISALLOWED_DECISIONS:
        assert f"`{value}`" in text
    for phrase in (
        "provider connectors", "source fetching", "forecast pulls", "API calls", "scraping",
        "credentials/secrets/config loading", "scoring", "backtesting", "runtime behavior",
        "execution", "trading", "order placement", "autonomy", "production behavior",
        "generated data", "fixture data", "workflows", "dependencies", "DB migrations",
        "schema changes", "source-code migrations", "compatibility shims",
        "provider/source connector implementation", "real ingestion implementation",
        "live provider usage", "paper simulation", "runtime observation",
    ):
        assert phrase in text


def test_machine_assignments_are_section_scoped_and_allowed() -> None:
    assignments = _assignments(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, values in assignments.items():
        assert values <= ALLOWED_ASSIGNMENTS[field]
    assert assignments["recommended next track"] == {"source_fetching_approval_request_owner_disposition"}
    assert assignments["allowed owner disposition decision"] == ALLOWED_DECISIONS
    assert assignments["disallowed owner disposition decision"] == DISALLOWED_DECISIONS


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- recommended next track: source_fetching_approval_request_owner_disposition\n\n"
        "## Acceptance criteria\n"
        "- recommended next track: approve_source_fetching_implementation\n"
    )
    assert _assignments(synthetic) == {"recommended next track": {"source_fetching_approval_request_owner_disposition"}}


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
