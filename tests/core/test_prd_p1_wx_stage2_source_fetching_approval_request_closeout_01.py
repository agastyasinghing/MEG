"""Static checks for Weather Bot source-fetching approval-request closeout."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-CLOSEOUT-01.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-CLOSEOUT-01"
MACHINE_HEADING = "## Machine-checkable source-fetching approval-request closeout assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to source-fetching approval-request planning",
    "Relationship to provider/source compatibility closeout",
    "Closeout objective",
    "Completed planning summary",
    "Approval-request template closeout",
    "Source identity and provenance closeout",
    "Access-date and retrieval-context closeout",
    "No-lookahead control closeout",
    "Provider/source compatibility reference closeout",
    "Offline-ingestion boundary closeout",
    "Risk and failure-mode closeout",
    "Test-scope closeout",
    "Explicit non-approval boundaries",
    "Blocked implementation work",
    "Recommended next ticket",
    "Machine-checkable source-fetching approval-request closeout assignments",
    "Acceptance criteria",
)

TEMPLATE_FIELDS = {
    "requested_source_family",
    "requested_source_name",
    "requested_source_owner_or_publisher",
    "requested_source_identity",
    "requested_source_url_or_citation",
    "requested_source_access_method",
    "requested_retrieval_mode",
    "intended_weather_market_use",
    "intended_forecast_or_resolution_target",
    "required_descriptor_fields",
    "required_identifier_contract",
    "access_date_policy",
    "retrieval_context_policy",
    "no_lookahead_control_plan",
    "provenance_capture_plan",
    "credential_or_config_requirement",
    "generated_data_or_fixture_plan",
    "test_scope_plan",
    "risk_and_failure_mode_summary",
    "explicit_non_approved_behaviors",
    "condition_id",
    "token_id",
    "outcome",
}

EXPLICIT_NON_APPROVED_BEHAVIORS = {
    "provider_connector",
    "source_fetching",
    "forecast_pull",
    "api_call",
    "scraping",
    "credentials_secrets_config",
    "scoring_backtesting",
    "runtime_behavior",
    "trading_autonomy",
    "production_behavior",
    "generated_data",
    "fixture_change",
    "workflow_change",
    "dependency_change",
    "database_migration",
    "schema_change",
}

ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_approval_request_closeout"},
    "closeout status": {
        "approval_request_planning_complete",
        "template_defined",
        "source_identity_requirements_defined",
        "provenance_requirements_defined",
        "access_date_requirements_defined",
        "no_lookahead_requirements_defined",
        "risk_requirements_defined",
        "test_scope_requirements_defined",
    },
    "approval request posture": {
        "approval_request_not_submitted",
        "approval_not_granted",
        "implementation_not_approved",
        "later_explicit_approval_required",
        "closeout_only",
    },
    "provider source posture": {
        "provider_connectors_not_approved",
        "source_fetching_not_approved",
        "forecast_pulls_not_approved",
        "api_calls_not_approved",
        "scraping_not_approved",
        "provider_source_planning_only",
    },
    "requested retrieval mode": {
        "manual_descriptor_only",
        "static_fixture_reference_only",
        "later_source_fetching_request",
        "later_provider_connector_request",
        "prohibited_until_explicit_approval",
        "unknown_requires_review",
    },
    "requested source family": {
        "forecast_provider_family",
        "historical_observation_provider_family",
        "official_resolution_source_family",
        "market_metadata_source_family",
        "manual_human_review_source_family",
        "unsupported_source_family",
        "unknown_source_family",
    },
    "requested source access method": {
        "manual_review",
        "static_reference",
        "api_call",
        "scraping",
        "file_download",
        "provider_sdk",
        "unknown_requires_review",
    },
    "implementation posture": {
        "closeout_only",
        "docs_static_test_only",
        "no_provider_connector",
        "no_source_fetching",
        "no_forecast_pull",
        "no_api_call",
        "no_scraping",
        "no_credentials_config_loading",
        "no_scoring_backtesting",
        "no_runtime_behavior",
        "no_trading_autonomy",
        "no_production_behavior",
        "no_generated_data",
        "no_fixture_change",
        "no_workflow_change",
        "no_dependency_change",
        "no_database_migration",
        "no_schema_change",
        "no_source_code_migration",
        "no_compatibility_shim",
    },
    "recommended next track": {
        "source_fetching_approval_request_draft_planning",
        "forecast_resolution_source_mapping_planning",
        "scoring_backtesting_approval_request_planning",
        "stage2_active_state_refresh",
    },
    "evidence status": {"source_backed", "reviewer_inferred", "missing", "conflicting", "not_applicable"},
    "label confidence": {"confirmed", "unclear", "unknown"},
}

ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)


def _read_artifact() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, f"Missing section: {heading}"
    section = match.group("section")
    assert section.strip(), f"Section is empty: {heading}"
    return section


def _machine_section(text: str) -> str:
    match = re.search(rf"^{re.escape(MACHINE_HEADING)}\n(?P<section>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, "Machine-checkable section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable section is empty"
    return section


def _assignments(text: str) -> dict[str, set[str]]:
    section = _machine_section(text)
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def test_closeout_document_exists_and_canonical_id_appears() -> None:
    assert ARTIFACT_PATH.exists()
    assert CANONICAL_ID in _read_artifact()


def test_all_required_sections_appear() -> None:
    text = _read_artifact()
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_required_relationships_appear() -> None:
    text = _read_artifact()
    assert "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-PLANNING-01" in _section(text, "Relationship to source-fetching approval-request planning")
    relationship = _section(text, "Relationship to provider/source compatibility closeout")
    assert "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT-01" in relationship
    assert "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01" in relationship
    assert "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01" in relationship
    assert "MEG-ARCH-ALIGN-08" in relationship


def test_closeout_docs_static_and_planning_complete_scope_are_stated() -> None:
    text = _read_artifact()
    assert "This is closeout/checkpoint only." in text
    assert "This is docs/static-test-only." in text
    assert "Source-fetching approval-request planning is complete at the planning level only." in text
    assert "This closeout is not an approval request." in text
    assert "This closeout does not submit an approval request." in text
    assert "This closeout does not grant approval." in text


def test_approval_request_template_fields_appear() -> None:
    section = _section(_read_artifact(), "Completed planning summary")
    for field in TEMPLATE_FIELDS:
        assert field in section


def test_closed_set_values_appear() -> None:
    text = _read_artifact()
    for field in ("requested source family", "requested retrieval mode", "requested source access method"):
        for value in ALLOWED_ASSIGNMENTS[field]:
            assert value in text


def test_explicit_non_approved_behaviors_appear() -> None:
    section = _section(_read_artifact(), "Explicit non-approval boundaries")
    for behavior in EXPLICIT_NON_APPROVED_BEHAVIORS:
        assert f"- {behavior}" in section


def test_no_provider_source_runtime_or_trading_work_is_implemented_or_approved() -> None:
    text = _read_artifact()
    required_phrases = (
        "No provider connector is implemented.",
        "No provider connector is approved.",
        "No source fetching is implemented.",
        "No source fetching is approved.",
        "No forecast pull is implemented.",
        "No forecast pull is approved.",
        "No API call is implemented.",
        "No API call is approved.",
        "No scraping is implemented.",
        "No scraping is approved.",
        "No credentials/secrets/config loading is implemented.",
        "No credentials/secrets/config loading is approved.",
        "No scoring is implemented or approved.",
        "No backtesting is implemented or approved.",
        "No runtime behavior is implemented or approved.",
        "No trading is implemented or approved.",
        "No autonomy is implemented or approved.",
        "No production behavior is implemented or approved.",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_no_data_fixture_workflows_dependencies_migrations_or_shims_are_approved() -> None:
    text = _read_artifact()
    required_phrases = (
        "No generated data is created.",
        "No fixture data is modified.",
        "No workflow or dependency change is approved.",
        "No DB migration or schema change is approved.",
        "No source-code migration is implemented or approved.",
        "No compatibility shim is implemented or approved.",
        "No generated data, fixture changes, workflows, dependencies, DB migrations, schema changes, source-code migrations, or compatibility shims are implemented or approved.",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_later_work_requires_separate_explicit_approval() -> None:
    text = _read_artifact()
    assert "Any later source-fetching/provider connector/forecast pull/API/scraping/credential/config work requires a separate explicit approval request." in text
    assert "Any later scoring/backtesting/runtime/trading/autonomy/production work requires a separate explicit approval request." in text


def test_recommended_next_ticket_is_draft_planning_only_and_does_not_approve() -> None:
    section = _section(_read_artifact(), "Recommended next ticket")
    assert "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-PLANNING-01" in section
    assert "docs/static-test-only draft planning for a future approval-request artifact" in section
    assert "does not approve implementation" in section
    for phrase in (
        "provider connector implementation",
        "source fetching implementation",
        "forecast pulls",
        "scoring",
        "backtesting",
        "runtime behavior",
        "trading",
        "autonomy",
        "production behavior",
    ):
        assert phrase in section


def test_machine_checkable_section_exists_and_parser_is_section_scoped() -> None:
    text = _read_artifact()
    section = _machine_section(text)
    assert "## Acceptance criteria" not in section
    assert "- weather bot planning stage: source_fetching_approval_request_closeout" in section
    synthetic_text = (
        f"{MACHINE_HEADING}\n"
        "- weather bot planning stage: source_fetching_approval_request_closeout\n"
        "## Acceptance criteria\n"
        "- weather bot planning stage: unapproved_actual_value\n"
    )
    assert _assignments(synthetic_text) == {"weather bot planning stage": {"source_fetching_approval_request_closeout"}}


def test_every_allowed_closed_set_machine_checkable_value_appears() -> None:
    assignments = _assignments(_read_artifact())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field] == allowed_values


def test_no_unapproved_actual_assignment_values_appear() -> None:
    assignments = _assignments(_read_artifact())
    for field, actual_values in assignments.items():
        assert field in ALLOWED_ASSIGNMENTS
        assert actual_values <= ALLOWED_ASSIGNMENTS[field]
