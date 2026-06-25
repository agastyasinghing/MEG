"""Static checks for Weather Bot narrow source-fetching runtime approval decision."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-APPROVAL-DECISION-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-fetching runtime approval-decision assignments"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to runtime approval request", "Relationship to static scaffold closeout",
    "Relationship to static scaffold", "Relationship to narrow implementation plan",
    "Relationship to Weather Bot PRD and architecture alignment", "Runtime approval decision objective",
    "Selected owner decision", "Approved future planning path", "Scope not implemented by this decision",
    "Scope not approved for execution", "Source identity runtime decision boundary",
    "Retrieval context runtime decision boundary", "Provider/source family runtime decision boundary",
    "Manual review gate runtime decision boundary", "No-lookahead metadata runtime decision boundary",
    "Fail-closed validation runtime decision boundary", "Static audit surface runtime decision boundary",
    "Provider/source execution boundary", "Credential/config boundary", "Generated-data and fixture boundary",
    "Trading/autonomy/production boundary", "Canonical identifier posture", "Provider/source compatibility posture",
    "Offline-ingestion boundary posture", "Test-scope posture", "Risk and failure-mode posture",
    "Explicit non-execution boundaries", "Blocked implementation work", "Recommended next ticket",
    "Machine-checkable source-fetching runtime approval-decision assignments", "Acceptance criteria",
)
RELATIONSHIP_IDS = {
    CANONICAL_ID,
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-APPROVAL-REQUEST-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLAN-01",
    "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01",
    "MEG-ARCH-ALIGN-08",
    "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD",
}
APPROVED_PATH = {
    "source_identity_recording_runtime_plan", "retrieval_context_recording_runtime_plan",
    "provider_source_family_recording_runtime_plan", "manual_review_gate_runtime_plan",
    "no_lookahead_metadata_gate_runtime_plan", "fail_closed_validation_gate_runtime_plan",
    "static_audit_surface_runtime_plan",
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
PROVIDER_POSTURE = {"provider_connectors_not_approved", "provider_clients_not_created", "live_provider_source_fetching_not_approved", "forecast_pulls_not_approved", "api_calls_not_approved", "scraping_not_approved", "runtime_decision_plan_only"}
IMPLEMENTATION_POSTURE = {"decision_only", "docs_static_test_only", "runtime_execution_not_approved", "no_runtime_source_fetching", "no_code_implementation", "no_provider_connector", "no_provider_client", "no_live_provider_fetching", "no_forecast_pull", "no_api_call", "no_scraping", "no_file_download", "no_provider_sdk", "no_credentials_config_loading", "no_scoring_backtesting", "no_runtime_trading", "no_order_placement", "no_autonomy", "no_production_behavior", "no_generated_data", "no_fixture_change", "no_workflow_change", "no_dependency_change", "no_database_migration", "no_schema_change", "no_source_code_migration", "no_compatibility_shim"}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_runtime_approval_decision"},
    "runtime approval decision status": {"docs_static_test_only", "decision_only", "post_pr_259_runtime_approval_request"},
    "current state posture": {"runtime_plan_approved_only", "runtime_execution_not_approved"},
    "selected owner decision": {"approve_narrow_source_fetching_runtime_implementation_plan"},
    "approved future planning path": APPROVED_PATH,
    "not executed scope": NOT_EXECUTED_SCOPE,
    "provider source posture": PROVIDER_POSTURE,
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "implementation posture": IMPLEMENTATION_POSTURE,
    "recommended next track": {"narrow_source_fetching_runtime_implementation_plan"},
    "conditional next track": {"hold_checkpoint_if_runtime_plan_not_desired", "decision_revision_if_scope_too_broad", "runtime_plan_revision_if_static_gap_found"},
    "evidence status": {"runtime_approval_decision_recorded"},
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


def test_required_decision_only_posture_and_non_approval_language() -> None:
    text = _read()
    required = [
        "runtime approval decision artifact", "docs/static-test-only", "decision-only",
        "PR #259 created `PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-APPROVAL-REQUEST-01`",
        "PR #259 recommended `narrow_source_fetching_runtime_approval_decision`",
        "selected owner decision is exactly `approve_narrow_source_fetching_runtime_implementation_plan`",
        "approves only a later narrow runtime implementation plan/scaffold path",
        "does not approve runtime execution itself", "does not itself implement runtime source fetching",
        "does not modify runtime code", "does not create provider connectors", "does not create provider clients",
        "does not call providers", "does not approve live provider/source fetching", "does not approve forecast pulls",
        "does not approve API calls", "does not approve scraping", "does not approve file downloads",
        "does not approve provider SDK usage", "does not approve credentials/secrets/config loading",
        "does not approve generated data", "does not approve fixture changes", "does not approve scoring",
        "does not approve backtesting", "does not approve runtime trading", "does not approve order placement",
        "does not approve autonomy", "does not approve production behavior",
        "Weather Bot models the market settlement rule, not generic weather",
        "No routing on `market_id` is introduced or approved", "Recommended next track: `narrow_source_fetching_runtime_implementation_plan`",
    ]
    for phrase in required:
        assert phrase in text
    for value in APPROVED_PATH | NOT_EXECUTED_SCOPE | SOURCE_FAMILIES | RETRIEVAL_MODES | ACCESS_METHODS:
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
    assert assignments["selected owner decision"] == {"approve_narrow_source_fetching_runtime_implementation_plan"}
    assert assignments["approved future planning path"] == APPROVED_PATH
    assert assignments["not executed scope"] == NOT_EXECUTED_SCOPE
    assert assignments["recommended next track"] == {"narrow_source_fetching_runtime_implementation_plan"}


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- recommended next track: narrow_source_fetching_runtime_implementation_plan\n"
        "## Later heading\n"
        "- recommended next track: runtime_source_fetching\n"
    )
    assert _assignments(synthetic) == {"recommended next track": {"narrow_source_fetching_runtime_implementation_plan"}}


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
