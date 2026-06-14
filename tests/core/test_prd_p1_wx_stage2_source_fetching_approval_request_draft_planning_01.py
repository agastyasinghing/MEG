"""Static checks for Weather Bot source-fetching approval-request draft planning.

These tests use only the Python standard library and validate a docs/static-test-only
planning artifact. They do not approve or implement provider connectors, source
fetching, forecast pulls, API calls, scraping, credentials/secrets/config loading,
scoring, backtesting, runtime behavior, trading, autonomy, production behavior,
generated data, fixture changes, workflows, dependencies, migrations, source-code
migrations, schema changes, or compatibility shims.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-PLANNING-01.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-PLANNING-01"
MACHINE_HEADING = "## Machine-checkable source-fetching approval-request draft-planning assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to source-fetching approval-request closeout",
    "Relationship to source-fetching approval-request planning",
    "Draft-planning objective",
    "Future approval-request draft outline",
    "Required draft sections",
    "Required source identity evidence",
    "Required provenance evidence",
    "Required access-date and retrieval-context evidence",
    "Required no-lookahead evidence",
    "Required provider/source compatibility evidence",
    "Required offline-ingestion boundary evidence",
    "Required risk and failure-mode evidence",
    "Required test-scope evidence",
    "Required explicit non-approval statement",
    "Reviewer checklist for future draft",
    "Blocked implementation work",
    "Recommended next ticket",
    "Machine-checkable source-fetching approval-request draft-planning assignments",
    "Acceptance criteria",
)

RELATIONSHIP_IDS = {
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-PLANNING-01",
    "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01",
    "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01",
    "MEG-ARCH-ALIGN-08",
}

FUTURE_DRAFT_OUTLINE = {
    "Request status and scope",
    "Requested source family",
    "Requested source identity",
    "Requested source owner or publisher",
    "Requested source URL or citation",
    "Requested access method",
    "Requested retrieval mode",
    "Intended weather-market use",
    "Forecast or resolution target",
    "Canonical identifier contract",
    "Descriptor field requirements",
    "Source identity and provenance evidence",
    "Access-date and retrieval-context evidence",
    "No-lookahead control plan",
    "Provider/source compatibility mapping",
    "Offline-ingestion boundary mapping",
    "Credential/config requirements",
    "Generated-data and fixture posture",
    "Proposed test scope",
    "Risk and failure-mode analysis",
    "Explicit non-approved behaviors",
    "Human-review checklist",
    "Approval decision placeholders",
}

APPROVAL_PLACEHOLDERS = {
    "approval_requested: yes/no",
    "approval_granted: pending/yes/no",
    "approved_scope: none/pending/specific_scope_only",
    "implementation_allowed: no/pending/yes_after_separate_approval",
    "reviewer_notes: required",
}

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
}

SOURCE_FAMILY_VALUES = {
    "forecast_provider_family",
    "historical_observation_provider_family",
    "official_resolution_source_family",
    "market_metadata_source_family",
    "manual_human_review_source_family",
    "unsupported_source_family",
    "unknown_source_family",
}
RETRIEVAL_MODE_VALUES = {
    "manual_descriptor_only",
    "static_fixture_reference_only",
    "later_source_fetching_request",
    "later_provider_connector_request",
    "prohibited_until_explicit_approval",
    "unknown_requires_review",
}
ACCESS_METHOD_VALUES = {
    "manual_review",
    "static_reference",
    "api_call",
    "scraping",
    "file_download",
    "provider_sdk",
    "unknown_requires_review",
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
    "weather bot planning stage": {"source_fetching_approval_request_draft_planning"},
    "draft planning posture": {
        "draft_outline_defined",
        "reviewer_checklist_defined",
        "evidence_checklist_defined",
        "non_approval_language_defined",
        "approval_decision_placeholders_defined",
    },
    "approval request posture": {
        "approval_request_not_created",
        "approval_request_not_submitted",
        "approval_not_granted",
        "implementation_not_approved",
        "later_explicit_approval_required",
    },
    "provider source posture": {
        "provider_connectors_not_approved",
        "source_fetching_not_approved",
        "forecast_pulls_not_approved",
        "api_calls_not_approved",
        "scraping_not_approved",
        "provider_source_planning_only",
    },
    "requested retrieval mode": RETRIEVAL_MODE_VALUES,
    "requested source family": SOURCE_FAMILY_VALUES,
    "requested source access method": ACCESS_METHOD_VALUES,
    "approval decision posture": {
        "approval_requested_placeholder_only",
        "approval_granted_pending_placeholder_only",
        "approved_scope_none",
        "implementation_allowed_no",
        "reviewer_notes_required",
    },
    "implementation posture": {
        "draft_planning_only",
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
        "source_fetching_approval_request_draft_artifact",
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
    match = re.search(
        rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, f"Missing section: {heading}"
    section = match.group("section")
    assert section.strip(), f"Section is empty: {heading}"
    return section


def _machine_section(text: str) -> str:
    match = re.search(
        rf"^{re.escape(MACHINE_HEADING)}\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, "Machine-checkable source-fetching approval-request draft-planning section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable source-fetching approval-request draft-planning section is empty"
    return section


def _assignments(text: str) -> dict[str, set[str]]:
    section = _machine_section(text)
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def test_draft_planning_document_exists_and_canonical_id_appears() -> None:
    assert ARTIFACT_PATH.exists()
    assert CANONICAL_ID in _read_artifact()


def test_all_required_sections_appear() -> None:
    text = _read_artifact()
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_required_relationships_appear() -> None:
    text = _read_artifact()
    relationship_text = "\n".join(
        (
            _section(text, "Relationship to source-fetching approval-request closeout"),
            _section(text, "Relationship to source-fetching approval-request planning"),
        )
    )
    for relationship_id in RELATIONSHIP_IDS:
        assert relationship_id in relationship_text


def test_draft_planning_and_non_approval_scope_are_stated() -> None:
    text = _read_artifact()
    required_phrases = (
        "This is draft planning only.",
        "This is docs/static-test-only.",
        "This is not the approval request itself.",
        "This does not submit an approval request.",
        "This does not grant approval.",
        "This does not create implementation permission.",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_future_draft_outline_and_approval_decision_placeholders_appear() -> None:
    section = _section(_read_artifact(), "Future approval-request draft outline")
    for outline_item in FUTURE_DRAFT_OUTLINE:
        assert f"- {outline_item}" in section
    for placeholder in APPROVAL_PLACEHOLDERS:
        assert f"- {placeholder}" in section


def test_all_required_template_fields_and_closed_set_values_appear() -> None:
    section = _section(_read_artifact(), "Required draft sections")
    for field in TEMPLATE_FIELDS:
        assert f"- {field}" in section
    for value in SOURCE_FAMILY_VALUES | RETRIEVAL_MODE_VALUES | ACCESS_METHOD_VALUES | EXPLICIT_NON_APPROVED_BEHAVIORS:
        assert value in section


def test_non_approved_provider_runtime_trading_and_data_work_is_stated() -> None:
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
        "No generated data is created.",
        "No fixture data is modified.",
        "No workflow or dependency change is approved.",
        "No DB migration or schema change is approved.",
        "No source-code migration is implemented or approved.",
        "No compatibility shim is implemented or approved.",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_later_work_requires_separate_explicit_approval() -> None:
    text = _read_artifact()
    assert "Any later source-fetching/provider connector/forecast pull/API/scraping/credential/config work requires a separate explicit approval request." in text
    assert "Any later scoring/backtesting/runtime/trading/autonomy/production work requires a separate explicit approval request." in text


def test_recommended_next_ticket_is_draft_artifact_only_and_not_implementation() -> None:
    section = _section(_read_artifact(), "Recommended next ticket")
    assert "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-01" in section
    assert "docs/static-test-only draft artifact for human review, not implementation" in section
    assert "should not approve provider connector implementation" in section
    prohibited_recommendations = (
        "source fetching implementation",
        "forecast pulls",
        "scoring",
        "backtesting",
        "runtime behavior",
        "trading",
        "autonomy",
        "production behavior",
    )
    for phrase in prohibited_recommendations:
        assert phrase in section


def test_machine_checkable_section_exists_and_parser_is_section_scoped() -> None:
    text = _read_artifact()
    section = _machine_section(text)
    assert "## Acceptance criteria" not in section
    assert "- weather bot planning stage: source_fetching_approval_request_draft_planning" in section

    synthetic_text = (
        f"{MACHINE_HEADING}\n"
        "- weather bot planning stage: source_fetching_approval_request_draft_planning\n"
        "## Acceptance criteria\n"
        "- weather bot planning stage: unapproved_actual_value\n"
    )
    assert _assignments(synthetic_text) == {
        "weather bot planning stage": {"source_fetching_approval_request_draft_planning"}
    }


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
