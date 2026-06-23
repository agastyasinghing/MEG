"""Static checks for Weather Bot source-fetching approval-request hold checkpoint."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01"
MACHINE_HEADING = "## Machine-checkable source-fetching approval-request hold-checkpoint assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to draft closeout",
    "Relationship to draft artifact",
    "Relationship to draft-planning artifact",
    "Relationship to source-fetching approval-request planning and closeout",
    "Relationship to provider/source compatibility planning and closeout",
    "Relationship to Weather Bot PRD and architecture alignment",
    "Hold checkpoint objective",
    "Current hold state",
    "Allowed next tracks",
    "Explicitly disallowed next tracks",
    "Human-review posture",
    "Approval posture",
    "Canonical identifier posture",
    "Source identity and provenance posture",
    "Access-date and retrieval-context posture",
    "No-lookahead posture",
    "Provider/source compatibility posture",
    "Offline-ingestion boundary posture",
    "Credential/config posture",
    "Generated-data and fixture posture",
    "Test-scope posture",
    "Risk and failure-mode posture",
    "Explicit non-approval boundaries",
    "Blocked implementation work",
    "Recommended next ticket",
    "Machine-checkable source-fetching approval-request hold-checkpoint assignments",
    "Acceptance criteria",
)

RELATIONSHIP_IDS = {
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01",
    "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-01",
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
    "weather bot planning stage": {"source_fetching_approval_request_hold_checkpoint"},
    "hold checkpoint status": {"hold_checkpoint", "docs_static_test_only", "checkpoint_only"},
    "draft sequence posture": {"draft_artifact_exists", "draft_closeout_exists", "draft_sequence_paused", "human_review_only"},
    "approval request posture": {"approval_not_granted", "implementation_not_approved", "later_explicit_approval_required"},
    "provider source posture": {
        "provider_connectors_not_approved",
        "source_fetching_not_approved",
        "forecast_pulls_not_approved",
        "api_calls_not_approved",
        "scraping_not_approved",
        "provider_source_planning_only",
    },
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "approval decision posture": {
        "approval_granted_pending_placeholder_only",
        "approved_scope_none",
        "implementation_allowed_no",
        "reviewer_notes_required",
    },
    "implementation posture": {
        "hold_only",
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
        "hold_checkpoint",
    },
    "conditional next track": {
        "human_review_of_draft_if_explicitly_requested",
        "source_fetching_approval_request_draft_revision_if_explicitly_requested",
    },
    "evidence status": {"missing", "not_applicable"},
    "label confidence": {"unknown"},
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
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(_machine_section(text)):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def test_document_exists_and_canonical_id_appears() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read_artifact()
    assert CANONICAL_ID in text
    assert f"Canonical ID: {CANONICAL_ID}" in text


def test_all_required_sections_appear_and_are_non_empty() -> None:
    text = _read_artifact()
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_required_relationship_ids_appear() -> None:
    text = _read_artifact()
    for relationship_id in RELATIONSHIP_IDS:
        assert relationship_id in text


def test_hold_checkpoint_static_human_review_and_non_approval_posture() -> None:
    text = _read_artifact()
    required_phrases = (
        "This is hold/checkpoint only.",
        "This is docs/static-test-only.",
        "The default next state is `hold_checkpoint`.",
        "The draft artifact exists.",
        "The draft closeout exists.",
        "This checkpoint is not a human approval decision.",
        "Approval was not granted.",
        "Implementation was not approved.",
        "This checkpoint does not grant approval",
        "does not create implementation permission",
        "does not recommend implementation work",
        "Later explicit approval is required before any source fetching, provider connector, forecast pull, API call, scraping, credential/config, generated-data, fixture, scoring, backtesting, runtime, trading, autonomy, or production work.",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_weather_bot_settlement_rule_and_canonical_identifier_posture() -> None:
    text = _read_artifact()
    assert "Weather Bot models the market settlement rule, not generic weather." in text
    identifier_section = _section(text, "Canonical identifier posture")
    for identifier in ("condition_id", "token_id", "outcome"):
        assert identifier in identifier_section
    assert "No routing on market_id is introduced or approved." in identifier_section


def test_closed_set_values_appear() -> None:
    text = _read_artifact()
    for values in (
        SOURCE_FAMILY_VALUES,
        RETRIEVAL_MODE_VALUES,
        ACCESS_METHOD_VALUES,
        CREDENTIAL_CONFIG_VALUES,
        GENERATED_DATA_FIXTURE_VALUES,
    ):
        for value in values:
            assert value in text


def test_explicit_non_approved_behavior_values_appear() -> None:
    section = _section(_read_artifact(), "Explicit non-approval boundaries")
    for behavior in EXPLICIT_NON_APPROVED_BEHAVIORS:
        assert f"- {behavior}" in section


def test_exact_non_approval_phrases_appear() -> None:
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


def test_machine_checkable_parser_is_section_scoped() -> None:
    section = _machine_section(_read_artifact())
    assert "## Acceptance criteria" not in section
    assert "- weather bot planning stage: source_fetching_approval_request_hold_checkpoint" in section
    synthetic_text = (
        f"{MACHINE_HEADING}\n"
        "- weather bot planning stage: source_fetching_approval_request_hold_checkpoint\n"
        "## Acceptance criteria\n"
        "- weather bot planning stage: implementation_approved\n"
    )
    assert _assignments(synthetic_text) == {"weather bot planning stage": {"source_fetching_approval_request_hold_checkpoint"}}


def test_every_actual_machine_checkable_assignment_value_is_allowed() -> None:
    assignments = _assignments(_read_artifact())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, actual_values in assignments.items():
        assert actual_values <= ALLOWED_ASSIGNMENTS[field]
        assert actual_values == ALLOWED_ASSIGNMENTS[field]


def test_recommended_next_tracks_are_safe_and_non_implementation() -> None:
    section = _section(_read_artifact(), "Recommended next ticket")
    for safe_track in ALLOWED_ASSIGNMENTS["recommended next track"]:
        assert safe_track in section
    for conditional_track in ("human_review_of_draft_if_explicitly_requested", "source_fetching_approval_request_draft_revision_if_explicitly_requested"):
        assert conditional_track in _machine_section(_read_artifact())
    assert "recommends no implementation work" in section
    forbidden_positive_recommendations = (
        "Recommended next track: provider connector implementation",
        "Recommended next track: source fetching implementation",
        "Recommended next track: forecast pulls",
        "Recommended next track: scoring",
        "Recommended next track: backtesting",
        "Recommended next track: runtime behavior",
        "Recommended next track: trading",
        "Recommended next track: autonomy",
        "Recommended next track: production behavior",
        "Recommended next track: generated data",
        "Recommended next track: fixture changes",
        "Recommended next track: workflows",
        "Recommended next track: dependencies",
        "Recommended next track: DB migrations",
        "Recommended next track: schema changes",
        "Recommended next track: source-code migrations",
        "Recommended next track: compatibility shims",
    )
    for phrase in forbidden_positive_recommendations:
        assert phrase not in section
