"""Static checks for Weather Bot source-fetching approval-request meta refresh."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-META-REFRESH-01.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-META-REFRESH-01"
MACHINE_HEADING = "## Machine-checkable source-fetching approval-request meta-refresh assignments"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to hold checkpoint", "Relationship to draft closeout",
    "Relationship to draft artifact", "Relationship to source-fetching approval-request planning sequence",
    "Relationship to provider/source compatibility sequence", "Relationship to Weather Bot PRD and architecture alignment",
    "Meta refresh objective", "Refreshed active state", "Refreshed Weather Bot packet posture",
    "Refreshed chat handoff posture", "Refreshed bootstrap posture", "Phase ledger posture",
    "Current safe next state", "Explicitly disallowed next states", "Approval posture", "Human-review posture",
    "Canonical identifier posture", "Source identity and provenance posture", "Access-date and retrieval-context posture",
    "No-lookahead posture", "Provider/source compatibility posture", "Offline-ingestion boundary posture",
    "Credential/config posture", "Generated-data and fixture posture", "Test-scope posture",
    "Risk and failure-mode posture", "Explicit non-approval boundaries", "Blocked implementation work",
    "Recommended next ticket", "Machine-checkable source-fetching approval-request meta-refresh assignments",
    "Acceptance criteria",
)
RELATIONSHIP_IDS = {
    CANONICAL_ID,
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
    "weather bot planning stage": {"source_fetching_approval_request_meta_refresh"},
    "meta refresh status": {"docs_static_test_only", "handoff_meta_refresh_only", "post_pr_247_hold_checkpoint"},
    "active state posture": {"refreshed_to_hold_checkpoint"},
    "weather packet posture": {"refreshed_to_hold_checkpoint"},
    "chat handoff posture": {"refreshed_to_hold_checkpoint"},
    "bootstrap posture": {"refreshed_to_prefer_newer_pr_metadata"},
    "phase ledger posture": {"appended_if_present", "not_modified_if_absent_or_not_applicable"},
    "approval request posture": {"approval_not_granted", "implementation_not_approved", "later_explicit_approval_required"},
    "provider source posture": {"provider_connectors_not_approved", "source_fetching_not_approved", "forecast_pulls_not_approved", "api_calls_not_approved", "scraping_not_approved", "provider_source_planning_only"},
    "requested source family": {"unknown_source_family"},
    "requested retrieval mode": {"prohibited_until_explicit_approval"},
    "requested source access method": {"manual_review"},
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "approval decision posture": {"approval_granted_pending_placeholder_only", "approved_scope_none", "implementation_allowed_no", "reviewer_notes_not_required_by_default"},
    "implementation posture": {"meta_refresh_only", "docs_static_test_only", "no_provider_connector", "no_source_fetching", "no_forecast_pull", "no_api_call", "no_scraping", "no_credentials_config_loading", "no_scoring_backtesting", "no_runtime_behavior", "no_trading_autonomy", "no_production_behavior", "no_generated_data", "no_fixture_change", "no_workflow_change", "no_dependency_change", "no_database_migration", "no_schema_change", "no_source_code_migration", "no_compatibility_shim"},
    "recommended next track": {"hold_checkpoint"},
    "conditional next track": {"human_review_of_draft_if_explicitly_requested", "source_fetching_approval_request_draft_revision_if_explicitly_requested", "future_docs_static_test_only_meta_refresh_if_needed"},
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
        "meta/handoff refresh only", "docs/static-test-only", "PR #247 is the latest completed",
        "current safe next state is `hold_checkpoint`", "No human review is currently required",
        "This checkpoint is not a human approval decision", "No approval has been granted", "No implementation has been approved", "No implementation work is recommended",
        "source-fetching approval-request draft sequence is paused by default",
        "Weather Bot models the market settlement rule, not generic weather",
        "No routing on `market_id` is introduced or approved",
    ]
    for phrase in required:
        assert phrase in text
    for token in ("condition_id", "token_id", "outcome"):
        assert f"`{token}`" in text
    for value in CLOSED_SET_VALUES | NON_APPROVED_BEHAVIORS:
        assert f"`{value}`" in text
    for phrase in ("No provider connector is implemented", "No source fetching is implemented", "No forecast pull is implemented", "No API call is implemented", "No scraping is implemented", "No credentials/secrets/config loading is implemented", "No scoring is implemented", "No backtesting is implemented", "No runtime behavior is implemented", "No trading is implemented", "No autonomy is implemented", "No production behavior is implemented", "No generated data is created", "No fixture data is modified"):
        assert phrase in text


def test_machine_assignments_are_section_scoped_and_allowed() -> None:
    text = _read()
    assignments = _assignments(text)
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, values in assignments.items():
        assert values <= ALLOWED_ASSIGNMENTS[field]
    assert assignments["recommended next track"] == {"hold_checkpoint"}
    assert "hold_checkpoint" not in assignments.get("conditional next track", set())


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = f"{MACHINE_HEADING}\n- recommended next track: hold_checkpoint\n\n## Acceptance criteria\n- recommended next track: provider_connector\n"
    assert _assignments(synthetic) == {"recommended next track": {"hold_checkpoint"}}


def test_meta_files_reflect_post_pr_247_hold_checkpoint() -> None:
    active = _read(REPO_ROOT / "docs/meta/MEG_ACTIVE_STATE.md")
    for phrase in ("PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01", "hold_checkpoint", "source_fetching_not_approved", "implementation_not_approved", "prefer newer merged PRDs, closeout docs, checkpoint docs, and verified PR metadata over stale handoff state"):
        assert phrase in active
    packet = _read(REPO_ROOT / "docs/meta/domain_packets/WEATHER_BOT_PACKET.md")
    for phrase in ("PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01", "hold_checkpoint", "Weather Bot models the market settlement rule, not generic weather", "source_fetching_not_approved", "implementation_not_approved"):
        assert phrase in packet
    bootstrap = _read(REPO_ROOT / "docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md")
    for phrase in ("hold_checkpoint", "prefer newer merged PRDs/checkpoints/verified PR metadata over stale handoff state", "Do not generate provider/source implementation tickets without later explicit approval"):
        assert phrase in bootstrap
    handoff = _read(REPO_ROOT / "docs/meta/MEG_CHAT_HANDOFF.md")
    for phrase in ("PR #247", "hold_checkpoint", "implementation_not_approved", "source_fetching_not_approved"):
        assert phrase in handoff


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
