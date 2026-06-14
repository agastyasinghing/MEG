"""Static checks for Weather Bot provider/source compatibility planning.

These tests use only the Python standard library and validate a docs/static-test-only
planning artifact. They do not approve or implement provider connectors, source
fetching, forecast pulls, API calls, scraping, credentials/secrets/config loading,
scoring, backtesting, runtime behavior, trading, autonomy, production behavior,
generated data, fixture changes, workflows, dependencies, or migrations.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01"
MACHINE_HEADING = "## Machine-checkable provider/source compatibility assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to Weather Bot return-to-planning checkpoint",
    "Planning objective",
    "Provider/source compatibility taxonomy",
    "Forecast source families",
    "Historical observation source families",
    "Market-resolution source families",
    "Human-reviewed descriptor compatibility",
    "Offline real-ingestion compatibility",
    "Source identity and provenance requirements",
    "Access-date and retrieval-context requirements",
    "No-lookahead requirements",
    "Provider/API connector boundary",
    "Source-fetching boundary",
    "Forecast-pull boundary",
    "Credentials/secrets/config boundary",
    "Scoring/backtesting/runtime/trading boundary",
    "Candidate compatibility matrix format",
    "Future approval-request requirements",
    "Recommended next ticket",
    "Machine-checkable provider/source compatibility assignments",
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
    "weather bot planning stage": {"provider_source_compatibility_planning"},
    "architecture alignment status": {
        "meg_arch_align_08_complete",
        "weather_bot_return_checkpoint_complete",
        "canonical_id_posture_recorded",
        "market_id_compatibility_posture_recorded",
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
        "planning_only",
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
    },
    "recommended next track": {
        "provider_source_compatibility_closeout",
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
    assert match, "Machine-checkable provider/source compatibility assignment section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable provider/source compatibility assignment section is empty"
    return section


def _assignments(text: str) -> dict[str, set[str]]:
    section = _machine_section(text)
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def test_planning_document_exists_and_canonical_id_appears() -> None:
    assert ARTIFACT_PATH.exists()
    assert CANONICAL_ID in _read_artifact()


def test_all_required_sections_appear() -> None:
    text = _read_artifact()
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_relationship_to_weather_bot_return_to_planning_checkpoint_appears() -> None:
    section = _section(_read_artifact(), "Relationship to Weather Bot return-to-planning checkpoint")
    assert "PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01" in section
    assert "MEG-ARCH-ALIGN-08" in section
    assert "gated planning/approval work" in section


def test_planning_only_and_docs_static_test_only_scope_are_stated() -> None:
    text = _read_artifact()
    assert "planning only" in text
    assert "docs/static-test-only" in text
    assert "compatibility only as a planning artifact" in text


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
        "No generated data is created.",
        "No fixture data is modified.",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_source_family_categories_appear() -> None:
    text = _read_artifact()
    for value in SOURCE_FAMILY_CATEGORIES:
        assert value in text


def test_official_resolution_source_family_is_defined_as_planning_only() -> None:
    section = _section(_read_artifact(), "Market-resolution source families")
    assert "Official resolution source families are limited to planning descriptors" in section
    assert "They do not approve fetching the official source" in section
    assert "adding runtime resolution behavior" in section


def test_candidate_compatibility_matrix_schema_and_allowed_values_appear() -> None:
    section = _section(_read_artifact(), "Candidate compatibility matrix format")
    for field in MATRIX_SCHEMA_FIELDS:
        assert field in section
    for allowed_values in (
        ALLOWED_ASSIGNMENTS["offline compatibility status"],
        ALLOWED_ASSIGNMENTS["approval required before use"],
        ALLOWED_ASSIGNMENTS["prohibited until approval"],
    ):
        for value in allowed_values:
            assert value in section


def test_future_approval_request_requirements_appear() -> None:
    section = _section(_read_artifact(), "Future approval-request requirements")
    assert "Any later provider connector or source-fetching work requires a separate explicit approval request." in section
    assert "Any later scoring/backtesting/runtime/trading work requires a separate explicit approval request." in section
    assert "schema change" in section
    assert "no-lookahead controls" in section


def test_machine_checkable_section_exists_and_parser_is_section_scoped() -> None:
    text = _read_artifact()
    section = _machine_section(text)
    assert "## Acceptance criteria" not in section
    assert "- weather bot planning stage: provider_source_compatibility_planning" in section

    synthetic_text = (
        f"{MACHINE_HEADING}\n"
        "- weather bot planning stage: provider_source_compatibility_planning\n"
        "## Acceptance criteria\n"
        "- weather bot planning stage: unapproved_actual_value\n"
    )
    assert _assignments(synthetic_text) == {
        "weather bot planning stage": {"provider_source_compatibility_planning"}
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


def test_recommended_next_ticket_does_not_recommend_implementation_work() -> None:
    section = _section(_read_artifact(), "Recommended next ticket")
    assert "PROVIDER-SOURCE-COMPATIBILITY-CLOSEOUT" in section
    assert "SOURCE-FETCHING-APPROVAL-REQUEST-PLANNING" in section
    prohibited_recommendations = (
        "provider connector implementation",
        "source fetching implementation",
        "forecast pulls",
        "scoring",
        "backtesting",
        "runtime behavior",
        "trading",
        "autonomy",
        "production behavior",
    )
    assert "Neither recommendation approves" in section
    for phrase in prohibited_recommendations:
        assert phrase in section
