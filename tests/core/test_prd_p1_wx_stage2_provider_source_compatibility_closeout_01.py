"""Static checks for Weather Bot provider/source compatibility closeout.

These tests use only the Python standard library and validate a docs/static-test-only
closeout artifact. They do not approve or implement provider connectors, source
fetching, forecast pulls, API calls, scraping, credentials/secrets/config loading,
scoring, backtesting, runtime behavior, trading, autonomy, production behavior,
generated data, fixture changes, workflows, dependencies, migrations, schema
changes, source-code migrations, or compatibility shims.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT-01.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT-01"
PLANNING_ID = "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01"
NEXT_TICKET = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-PLANNING-01"
MACHINE_HEADING = "## Machine-checkable provider/source compatibility closeout assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to provider/source compatibility planning",
    "Closeout objective",
    "Completed planning summary",
    "Provider/source taxonomy closeout",
    "Compatibility matrix schema closeout",
    "Offline descriptor compatibility closeout",
    "Source identity and provenance closeout",
    "Access-date and no-lookahead closeout",
    "Explicit non-approval boundaries",
    "Blocked implementation work",
    "Remaining planning risks",
    "Recommended next ticket",
    "Machine-checkable provider/source compatibility closeout assignments",
    "Acceptance criteria",
)

SOURCE_FAMILY_CATEGORIES = {
    "forecast_provider_family",
    "historical_observation_provider_family",
    "official_resolution_source_family",
    "market_metadata_source_family",
    "manual_human_review_source_family",
    "unsupported_source_family",
    "unknown_source_family",
}

MATRIX_SCHEMA_FIELDS = {
    "source_family",
    "example_source_type",
    "intended_use",
    "required_descriptor_fields",
    "offline_compatibility_status",
    "approval_required_before_use",
    "prohibited_until_approval",
    "risk_notes",
}

ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"provider_source_compatibility_closeout"},
    "closeout status": {
        "compatibility_planning_complete",
        "taxonomy_defined",
        "matrix_schema_defined",
        "provenance_requirements_defined",
        "no_lookahead_requirements_defined",
        "future_approval_requirements_defined",
    },
    "provider source posture": {
        "provider_source_planning_only",
        "provider_connectors_not_approved",
        "source_fetching_not_approved",
        "forecast_pulls_not_approved",
        "api_calls_not_approved",
        "scraping_not_approved",
    },
    "source family category": SOURCE_FAMILY_CATEGORIES,
    "offline compatibility status": {
        "compatible_as_human_reviewed_descriptor_only",
        "compatible_as_static_fixture_reference_only",
        "requires_later_source_fetching_approval",
        "requires_later_provider_connector_approval",
        "prohibited_until_explicit_approval",
        "unknown_requires_review",
    },
    "approval required before use": {
        "no_new_approval_for_manual_descriptor_only",
        "source_fetching_approval_required",
        "provider_connector_approval_required",
        "credentials_config_approval_required",
        "scoring_backtesting_approval_required",
        "runtime_trading_approval_required",
        "human_review_required",
    },
    "prohibited until approval": {
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
        "none_for_manual_descriptor_only",
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
    },
    "recommended next track": {
        "source_fetching_approval_request_planning",
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
    assert match, "Machine-checkable provider/source compatibility closeout section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable provider/source compatibility closeout section is empty"
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


def test_relationship_to_provider_source_compatibility_planning_appears() -> None:
    section = _section(_read_artifact(), "Relationship to provider/source compatibility planning")
    assert PLANNING_ID in section
    assert "planning-level completion" in section
    assert "descriptor and matrix-schema level only" in section


def test_closeout_checkpoint_and_docs_static_test_only_scope_are_stated() -> None:
    text = _read_artifact()
    assert "closeout/checkpoint only" in text
    assert "docs/static-test-only" in text
    assert "Provider/source compatibility planning is complete at the planning level" in text
    assert "compatibility remains planning-only" in text


def test_completed_planning_summary_appears() -> None:
    section = _section(_read_artifact(), "Completed planning summary")
    for value in SOURCE_FAMILY_CATEGORIES:
        assert value in section
    assert "candidate compatibility matrix schema" in section
    assert "source identity and provenance requirements" in section
    assert "access-date and retrieval-context requirements" in section
    assert "no-lookahead requirements" in section
    assert "future approval-request requirements" in section


def test_provider_source_taxonomy_values_appear() -> None:
    section = _section(_read_artifact(), "Provider/source taxonomy closeout")
    for value in SOURCE_FAMILY_CATEGORIES:
        assert value in section
    assert "labels, not implementation approval" in section


def test_compatibility_matrix_schema_closeout_appears() -> None:
    section = _section(_read_artifact(), "Compatibility matrix schema closeout")
    for field in MATRIX_SCHEMA_FIELDS:
        assert field in section
    assert "planning guidance only" in section
    assert "does not create provider connectors" in section


def test_provenance_access_date_and_no_lookahead_closeout_appears() -> None:
    provenance_section = _section(_read_artifact(), "Source identity and provenance closeout")
    access_section = _section(_read_artifact(), "Access-date and no-lookahead closeout")
    assert "Source identity and provenance requirements" in provenance_section
    assert "condition_id, token_id, and outcome" in provenance_section
    assert "Access-date and retrieval-context requirements" in access_section
    assert "No-lookahead requirements" in access_section
    assert "prevents post-resolution or post-target information" in access_section


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


def test_no_data_workflow_dependency_db_schema_source_migration_or_shim_work_is_approved() -> None:
    section = _section(_read_artifact(), "Explicit non-approval boundaries")
    required_phrases = (
        "No generated data is created.",
        "No fixture data is modified.",
        "No workflow or dependency change is approved.",
        "No DB migration or schema change is approved.",
        "No source-code migration is implemented or approved.",
        "No compatibility shim is implemented or approved.",
    )
    for phrase in required_phrases:
        assert phrase in section


def test_recommended_next_ticket_is_planning_approval_request_only_and_not_implementation() -> None:
    section = _section(_read_artifact(), "Recommended next ticket")
    assert NEXT_TICKET in section
    assert "planning/approval-request only" in section
    assert "must not approve provider connector implementation" in section
    for phrase in (
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
    assert "- weather bot planning stage: provider_source_compatibility_closeout" in section

    synthetic_text = (
        f"{MACHINE_HEADING}\n"
        "- weather bot planning stage: provider_source_compatibility_closeout\n"
        "## Acceptance criteria\n"
        "- weather bot planning stage: unapproved_actual_value\n"
    )
    assert _assignments(synthetic_text) == {
        "weather bot planning stage": {"provider_source_compatibility_closeout"}
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
