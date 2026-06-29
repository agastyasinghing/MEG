"""Static checks for Weather Bot Phase 0A Hold State Refresh."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-HOLD-STATE-REFRESH-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable Weather Bot Phase 0A hold-state-refresh assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to Weather Bot PRD and architecture alignment",
    "Relationship to Stage 2 runtime metadata sequence",
    "Relationship to source-fetching runtime track hold closeout",
    "Held-state refresh objective",
    "Current Phase 0A held state",
    "Source-fetching track state",
    "Stage 2 runtime metadata state",
    "Blocked work",
    "Non-approval boundary",
    "Source fetching implementation boundary",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Audit report and export boundary",
    "Canonical identifier posture",
    "Conditions required to reopen source-fetching track",
    "Recommended next ticket",
    "Machine-checkable Weather Bot Phase 0A hold-state-refresh assignments",
    "Acceptance criteria",
)

STAGE2_ARTIFACT_PATHS = {
    "meg/weather/stage2/source_identity_runtime.py",
    "meg/weather/stage2/retrieval_context_runtime.py",
    "meg/weather/stage2/provider_source_family_runtime.py",
    "meg/weather/stage2/manual_review_gate_runtime.py",
    "meg/weather/stage2/no_lookahead_metadata_runtime.py",
    "meg/weather/stage2/fail_closed_validation_runtime.py",
    "meg/weather/stage2/static_audit_surface_runtime.py",
}
BLOCKED_WORK = {
    "source_fetching_runtime_implementation_plan",
    "source_fetching_implementation",
    "provider_connector_implementation",
    "provider_client_creation",
    "live_provider_source_fetching",
    "forecast_pull_execution",
    "api_call_execution",
    "scraping_execution",
    "file_download_execution",
    "provider_sdk_execution",
    "credentials_config_loading",
    "generated_data_creation",
    "fixture_data_modification",
    "scoring_implementation",
    "backtesting_implementation",
    "runtime_trading_behavior",
    "order_placement",
    "autonomy_behavior",
    "production_behavior",
    "audit_report_generation",
    "audit_output_persistence",
    "external_export_behavior",
}
CONDITIONS_REQUIRED_TO_REOPEN = {
    "approve_narrow_source_fetching_runtime_implementation_plan",
    "deny_source_fetching_runtime_implementation_plan",
    "request_revision_to_source_fetching_runtime_implementation_request",
    "hold_source_fetching_runtime_track",
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_phase0a_hold_state_refresh"},
    "held state refresh status": {
        "docs_static_test_only",
        "held_state_refresh_only",
        "post_source_fetching_runtime_track_hold_closeout",
    },
    "current phase0a posture": {
        "weather_bot_phase0a_held",
        "source_fetching_runtime_track_closed_held",
        "source_fetching_not_implemented",
        "implementation_approval_not_granted",
        "stage2_runtime_metadata_supplied_only",
        "stage2_runtime_metadata_fail_closed",
    },
    "source fetching track state": {
        "hold_source_fetching_runtime_track",
        "future_reopen_requires_owner_decision_revision",
        "no_source_fetching_implementation_plan",
        "no_source_fetching_implementation",
    },
    "stage2 runtime metadata artifact": {
        "source_identity_runtime_py",
        "retrieval_context_runtime_py",
        "provider_source_family_runtime_py",
        "manual_review_gate_runtime_py",
        "no_lookahead_metadata_runtime_py",
        "fail_closed_validation_runtime_py",
        "static_audit_surface_runtime_py",
    },
    "blocked work": BLOCKED_WORK,
    "condition required to reopen source fetching track": CONDITIONS_REQUIRED_TO_REOPEN,
    "provider source posture": {
        "provider_connectors_not_approved",
        "provider_clients_not_created",
        "live_provider_source_fetching_not_approved",
        "held_state_refresh_only",
    },
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "audit output posture": {"no_report_writing", "no_external_export", "no_persistence"},
    "implementation posture": {
        "docs_static_test_only",
        "held_state_refresh_only",
        "no_runtime_code_change",
        "no_source_fetching",
        "no_source_fetching_plan",
        "no_provider_connector",
        "no_provider_client",
        "no_live_provider_fetching",
        "no_credential_config_loading",
        "no_generated_data",
        "no_fixture_change",
        "no_scoring_backtesting",
        "no_trading_autonomy_production",
        "no_report_writing",
        "no_external_export",
        "no_persistence",
    },
    "recommended next track": {"weather_bot_phase0a_hold_state_closeout"},
    "conditional next track": {
        "weather_bot_phase0a_hold_state_refresh_revision_if_scope_too_broad",
        "source_fetching_runtime_owner_decision_revision_if_owner_changes_decision",
    },
    "evidence status": {"held_state_refresh_recorded"},
    "label confidence": {"confirmed"},
}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)


def _read() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
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


def test_document_exists_canonical_id_and_sections_are_non_empty() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert f"Canonical ID: {CANONICAL_ID}" in text
    assert text.startswith(
        "# WEATHER-BOT-PHASE0A-HOLD-STATE-REFRESH-01 — "
        "Weather Bot Phase 0A Hold State Refresh"
    )
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_docs_static_held_state_refresh_scope_and_no_meg_modification() -> None:
    text = _read()
    required_phrases = [
        "docs/static-test-only/held-state-refresh-only",
        "This ticket does not modify `meg/`",
        "refreshes the broader Weather Bot Phase 0A held-state context",
        "This ticket does not implement source fetching",
        "This ticket does not approve source-fetching implementation",
        "This ticket does not approve source-fetching implementation planning",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_weather_bot_models_market_settlement_rule_not_generic_weather() -> None:
    text = _read()
    assert "Weather Bot models the market settlement rule, not generic weather" in text


def test_source_fetching_track_closed_held_owner_decision_and_current_state() -> None:
    text = _read()
    assert "The source-fetching runtime track is closed/held" in text
    assert "Closed owner decision: hold_source_fetching_runtime_track" in _section(
        text, "Source-fetching track state"
    )
    required_phrases = [
        "Source fetching remains not implemented",
        "Implementation approval remains not granted",
        "does not proceed to `source_fetching_runtime_implementation_plan`",
        "does not approve source-fetching implementation planning",
        "future implementation-plan ticket remains blocked",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_stage2_runtime_metadata_supplied_only_fail_closed_and_paths() -> None:
    text = _read()
    assert "supplied-metadata-only and fail-closed" in text
    stage2_section = _section(text, "Stage 2 runtime metadata state")
    assert "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed" in stage2_section
    for path in STAGE2_ARTIFACT_PATHS:
        assert f"`{path}`" in stage2_section


def test_blocked_work_and_reopen_conditions_appear() -> None:
    text = _read()
    blocked_section = _section(text, "Blocked work")
    for value in BLOCKED_WORK:
        assert f"`{value}`" in blocked_section
    reopen_section = _section(text, "Conditions required to reopen source-fetching track")
    for value in CONDITIONS_REQUIRED_TO_REOPEN:
        assert f"`{value}`" in reopen_section
    assert "Only `approve_narrow_source_fetching_runtime_implementation_plan` may unlock" in reopen_section
    assert "other decisions must route to continued hold, closeout, or revision" in reopen_section


def test_provider_credentials_generated_scoring_trading_and_audit_not_approved() -> None:
    text = _read()
    required_phrases = [
        "Provider connectors remain not approved",
        "Provider clients remain not created",
        "Live provider/source fetching remains not approved",
        "Forecast pulling, API calls, scraping, file downloads, and provider SDK usage remain not approved",
        "does not call providers",
        "does not fetch sources",
        "does not execute API calls",
        "Credentials/config loading remains not approved",
        "does not modify `.env`, secrets, credentials, config, or config-loading behavior",
        "Generated data and fixtures remain not approved",
        "does not modify `tests/fixtures/`",
        "Scoring/backtesting remains not approved",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
        "does not create audit reports, persisted audit output, export files, external export behavior",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_non_approval_signals_and_no_forbidden_approval_phrases() -> None:
    text = _read()
    assert "Silence, continuation, lack of objection, and non-interference are not approval" in text
    lower_text = text.lower()
    approval_suffix = " is " + "approved"
    created_suffix = " is " + "created"
    forbidden_patterns = [
        "provider connector" + approval_suffix,
        "provider client" + created_suffix,
        "source fetching" + approval_suffix,
        "source fetching implementation" + approval_suffix,
        "source fetching implementation planning" + approval_suffix,
        "source fetching implementation plan" + approval_suffix,
        "live provider source fetching" + approval_suffix,
        "forecast pull" + approval_suffix,
        "api call" + approval_suffix,
        "scraping" + approval_suffix,
        "file download" + approval_suffix,
        "provider sdk" + approval_suffix,
        r"credentials.*loading" + approval_suffix,
        "generated data" + approval_suffix,
        "fixture change" + approval_suffix,
        "scoring" + approval_suffix,
        "backtesting" + approval_suffix,
        "trading" + approval_suffix,
        "order placement" + approval_suffix,
        "autonomy" + approval_suffix,
        "production behavior" + approval_suffix,
        "report writing" + approval_suffix,
        "external export" + approval_suffix,
        "persistence" + approval_suffix,
        "silence" + approval_suffix,
        "continuation" + approval_suffix,
        "non-interference" + approval_suffix,
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, lower_text), pattern


def test_canonical_identifier_contract_and_no_legacy_market_routing() -> None:
    canonical_section = _section(_read(), "Canonical identifier posture")
    for identifier in ("condition_id", "token_id", "outcome"):
        assert f"`{identifier}`" in canonical_section
    legacy_identifier = "market" + "_id"
    assert f"No routing on `{legacy_identifier}` is introduced or approved" in canonical_section


def test_machine_checkable_assignments_are_section_scoped_complete_and_allowed() -> None:
    text = _read()
    assignments = _assignments(text)
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field] == allowed_values
    assert "Acceptance criteria" not in _machine_section(text)


def test_every_actual_machine_checkable_assignment_value_is_allowed() -> None:
    assignments = _assignments(_read())
    for field, values in assignments.items():
        assert field in ALLOWED_ASSIGNMENTS
        assert values <= ALLOWED_ASSIGNMENTS[field]


def test_machine_checkable_parser_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        "# Example\n\n"
        f"{MACHINE_HEADING}\n\n"
        "- evidence status: held_state_refresh_recorded\n\n"
        "## Acceptance criteria\n\n"
        "- evidence status: forged_after_next_heading\n"
        "- recommended next track: source_fetching_runtime_implementation_plan\n"
    )
    assert _assignments(synthetic) == {"evidence status": {"held_state_refresh_recorded"}}


def test_recommended_next_track_hold_closeout_only_not_implementation() -> None:
    text = _read()
    recommended = _section(text, "Recommended next ticket")
    assert "Recommended next ticket: `weather_bot_phase0a_hold_state_closeout`" in recommended
    assert "docs/static-test-only held-state closeout" in recommended
    assert "It must not implement source fetching" in recommended
    assert "must not create provider connectors" in recommended
    assert _assignments(text)["recommended next track"] == {"weather_bot_phase0a_hold_state_closeout"}
