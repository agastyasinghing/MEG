"""Static checks for Weather Bot source-fetching approval-request draft.

These tests use only the Python standard library and validate a docs/static-test-only
non-approving draft artifact. They do not approve or implement provider connectors,
source fetching, forecast pulls, API calls, scraping, credentials/secrets/config
loading, scoring, backtesting, runtime behavior, trading, autonomy, production
behavior, generated data, fixture changes, workflows, dependencies, DB migrations,
schema changes, source-code migrations, or compatibility shims.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-01.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-01"
MACHINE_HEADING = "## Machine-checkable source-fetching approval-request draft assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to draft-planning artifact",
    "Relationship to source-fetching approval-request planning and closeout",
    "Relationship to provider/source compatibility planning and closeout",
    "Relationship to Weather Bot PRD and architecture alignment",
    "Draft request purpose",
    "Requested source family",
    "Requested source identity",
    "Requested source owner or publisher",
    "Requested source URL or citation",
    "Requested source access method",
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
    "Blocked implementation work",
    "Recommended next ticket",
    "Machine-checkable source-fetching approval-request draft assignments",
    "Acceptance criteria",
)

RELATIONSHIP_IDS = {
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-PLANNING-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-PLANNING-01",
    "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01",
    "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01",
    "MEG-ARCH-ALIGN-08",
    "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD",
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
CREDENTIAL_CONFIG_VALUES = {
    "none_required",
    "credentials_required_later",
    "config_required_later",
    "secrets_required_later",
    "unknown_requires_review",
}
GENERATED_DATA_FIXTURE_VALUES = {
    "no_generated_data",
    "no_fixture_change",
    "generated_data_requires_later_approval",
    "fixture_change_requires_later_approval",
    "unknown_requires_review",
}
APPROVAL_PLACEHOLDER_LINES = {
    "approval_requested: yes",
    "approval_granted: pending",
    "approved_scope: none",
    "implementation_allowed: no",
    "reviewer_notes: required",
}
APPROVAL_PLACEHOLDER_VALUES = {
    "approval_requested": {"yes", "no"},
    "approval_granted": {"pending", "yes", "no"},
    "approved_scope": {"none", "pending", "specific_scope_only"},
    "implementation_allowed": {"no", "pending", "yes_after_separate_approval"},
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
    "source_code_migration",
    "compatibility_shim",
}

ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_approval_request_draft"},
    "draft artifact posture": {"draft_packet_created", "docs_static_test_only", "human_review_only"},
    "approval request posture": {
        "approval_request_draft_only",
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
    "requested source family": SOURCE_FAMILY_VALUES,
    "requested retrieval mode": RETRIEVAL_MODE_VALUES,
    "requested source access method": ACCESS_METHOD_VALUES,
    "credential config posture": CREDENTIAL_CONFIG_VALUES,
    "generated data fixture posture": GENERATED_DATA_FIXTURE_VALUES,
    "approval decision posture": {
        "approval_requested_yes_placeholder_only",
        "approval_requested_no_placeholder_only",
        "approval_granted_pending_placeholder_only",
        "approved_scope_none",
        "implementation_allowed_no",
        "reviewer_notes_required",
    },
    "implementation posture": {
        "draft_only",
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
        "source_fetching_approval_request_draft_closeout",
        "source_fetching_approval_request_draft_revision",
        "stage2_active_state_refresh",
    },
    "evidence status": {"source_backed", "reviewer_inferred", "missing", "conflicting", "not_applicable"},
    "label confidence": {"confirmed", "unclear", "unknown"},
}

FORBIDDEN_NEXT_TICKET_TERMS = {
    "provider connector implementation",
    "source fetching implementation",
    "forecast pulls",
    "scoring",
    "backtesting",
    "runtime behavior",
    "trading",
    "autonomy",
    "production behavior",
    "generated data",
    "fixture changes",
    "workflows",
    "dependencies",
    "DB migrations",
    "schema changes",
    "source-code migrations",
    "compatibility shims",
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
    assert match, "Machine-checkable source-fetching approval-request draft section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable source-fetching approval-request draft section is empty"
    return section


def _assignments(text: str) -> dict[str, set[str]]:
    section = _machine_section(text)
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def test_draft_document_exists_and_canonical_id_appears() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read_artifact()
    assert CANONICAL_ID in text
    assert text.startswith("# PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-01 — Source-Fetching Approval Request Draft")


def test_all_required_sections_appear_and_are_non_empty() -> None:
    text = _read_artifact()
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_required_relationships_appear() -> None:
    text = _read_artifact()
    for relationship_id in RELATIONSHIP_IDS:
        assert relationship_id in text


def test_draft_only_docs_static_non_approval_non_implementation_posture() -> None:
    text = _read_artifact()
    required_phrases = {
        "This is a draft approval-request artifact for human review.",
        "This is docs/static-test-only.",
        "This does not submit a final approval decision.",
        "This does not grant approval.",
        "This does not create implementation permission.",
        "Approval placeholders are placeholders only and must be filled by human reviewers in a later explicit decision process.",
        "This draft is non-authoritative and non-approved.",
    }
    for phrase in required_phrases:
        assert phrase in text


def test_exact_non_approval_phrases_appear() -> None:
    text = _read_artifact()
    exact_phrases = {
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
        "No execution is implemented or approved.",
        "No trading is implemented or approved.",
        "No order placement is implemented or approved.",
        "No autonomy is implemented or approved.",
        "No production behavior is implemented or approved.",
        "No generated data is created.",
        "No fixture data is modified.",
        "No workflow or dependency change is approved.",
        "No DB migration or schema change is approved.",
        "No source-code migration is implemented or approved.",
        "No compatibility shim is implemented or approved.",
        "No provider/source connector implementation is implemented or approved.",
        "No real ingestion implementation is implemented or approved.",
        "No live provider usage is implemented or approved.",
        "No paper simulation is implemented or approved.",
        "No runtime observation is implemented or approved.",
    }
    for phrase in exact_phrases:
        assert phrase in text


def test_canonical_identifier_contract_preserved_without_market_id_routing() -> None:
    section = _section(_read_artifact(), "Canonical identifier contract")
    for identifier in ("condition_id", "token_id", "outcome"):
        assert identifier in section
    assert "No alternate routing identifiers are introduced." in section
    assert "must not propose routing on market_id" in section
    assert "market_id is not introduced as a routing identifier" in section
    assert "route on market_id" not in section.lower()


def test_weather_bot_models_market_settlement_rule_not_generic_weather() -> None:
    text = _read_artifact()
    assert "Weather Bot models the market settlement rule, not generic weather" in text


def test_closed_set_values_appear_in_relevant_sections() -> None:
    text = _read_artifact()
    checks = {
        "Requested source family": SOURCE_FAMILY_VALUES,
        "Requested source access method": ACCESS_METHOD_VALUES,
        "Requested retrieval mode": RETRIEVAL_MODE_VALUES,
        "Credential/config requirements": CREDENTIAL_CONFIG_VALUES,
        "Generated-data and fixture posture": GENERATED_DATA_FIXTURE_VALUES,
    }
    for heading, values in checks.items():
        section = _section(text, heading)
        for value in values:
            assert value in section
    placeholders = _section(text, "Approval decision placeholders")
    for field, values in APPROVAL_PLACEHOLDER_VALUES.items():
        assert field in placeholders
        for value in values:
            assert value in placeholders


def test_explicit_non_approved_behavior_list_appears() -> None:
    section = _section(_read_artifact(), "Explicit non-approved behaviors")
    for behavior in EXPLICIT_NON_APPROVED_BEHAVIORS:
        assert f"- {behavior}" in section


def test_approval_decision_placeholders_are_non_granting_by_default() -> None:
    section = _section(_read_artifact(), "Approval decision placeholders")
    for line in APPROVAL_PLACEHOLDER_LINES:
        assert line in section
    assert "approval_granted: yes" not in section
    assert "implementation_allowed: yes_after_separate_approval" not in section.split("Allowed implementation_allowed placeholder values:")[0]


def test_machine_checkable_parsing_is_section_scoped_and_assignments_allowed() -> None:
    text = _read_artifact()
    assignments = _assignments(text)
    assert set(ALLOWED_ASSIGNMENTS).issubset(assignments)
    for field, values in assignments.items():
        assert field in ALLOWED_ASSIGNMENTS, f"Unexpected assignment field: {field}"
        assert values <= ALLOWED_ASSIGNMENTS[field], f"Unexpected values for {field}: {values - ALLOWED_ASSIGNMENTS[field]}"


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"{MACHINE_HEADING}\n"
        "- weather bot planning stage: source_fetching_approval_request_draft\n"
        "## Acceptance criteria\n"
        "- weather bot planning stage: forbidden_after_heading\n"
    )
    assert _assignments(synthetic) == {"weather bot planning stage": {"source_fetching_approval_request_draft"}}


def test_recommended_next_ticket_is_static_closeout_not_forbidden_implementation() -> None:
    section = _section(_read_artifact(), "Recommended next ticket")
    assert "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-CLOSEOUT-01" in section
    assert "docs/static-test-only closeout/checkpoint" in section
    assert "must not recommend" in section
    negative_sentence = section.split("That ticket", 1)[1]
    for forbidden in FORBIDDEN_NEXT_TICKET_TERMS:
        assert forbidden in negative_sentence
