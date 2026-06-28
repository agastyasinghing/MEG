"""Static checks for Source Fetching Runtime Hold Checkpoint."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "SOURCE-FETCHING-RUNTIME-HOLD-CHECKPOINT-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-fetching runtime hold-checkpoint assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to source-fetching runtime implementation approval request",
    "Hold checkpoint objective",
    "Owner decision posture",
    "Current state",
    "Held work",
    "Non-approval boundary",
    "Source fetching implementation boundary",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Audit report and export boundary",
    "Canonical identifier posture",
    "Blocked work during hold",
    "Conditions required to leave hold",
    "Recommended next ticket",
    "Machine-checkable source-fetching runtime hold-checkpoint assignments",
    "Acceptance criteria",
)

HELD_WORK = {
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
CONDITIONS_REQUIRED_TO_LEAVE_HOLD = {
    "approve_narrow_source_fetching_runtime_implementation_plan",
    "deny_source_fetching_runtime_implementation_plan",
    "request_revision_to_source_fetching_runtime_implementation_request",
    "hold_source_fetching_runtime_track",
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_runtime_hold_checkpoint"},
    "hold checkpoint status": {
        "docs_static_test_only",
        "hold_checkpoint_only",
        "post_source_fetching_runtime_implementation_approval_request",
    },
    "current state posture": {
        "source_fetching_runtime_implementation_approval_request_landed",
        "owner_decision_not_selected",
        "source_fetching_not_implemented",
        "implementation_approval_not_granted",
    },
    "owner decision posture": {
        "silence_is_not_approval",
        "continuation_is_not_approval",
        "non_interference_is_not_approval",
        "explicit_owner_decision_required",
    },
    "held work": HELD_WORK,
    "condition required to leave hold": CONDITIONS_REQUIRED_TO_LEAVE_HOLD,
    "blocked work during hold": HELD_WORK,
    "provider source posture": {
        "provider_connectors_not_approved",
        "provider_clients_not_created",
        "live_provider_source_fetching_not_approved",
        "hold_checkpoint_only",
    },
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "audit output posture": {"no_report_writing", "no_external_export", "no_persistence"},
    "implementation posture": {
        "docs_static_test_only",
        "hold_checkpoint_only",
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
    "recommended next track": {"source_fetching_runtime_owner_decision_record"},
    "conditional next track": {
        "source_fetching_hold_checkpoint_revision_if_scope_too_broad",
        "hold_checkpoint_refresh_if_owner_decision_still_missing",
    },
    "evidence status": {"hold_checkpoint_recorded"},
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
        "# SOURCE-FETCHING-RUNTIME-HOLD-CHECKPOINT-01 — "
        "Source Fetching Runtime Hold Checkpoint"
    )
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_docs_static_hold_checkpoint_scope_and_no_meg_modification_posture() -> None:
    text = _read()
    required_phrases = [
        "docs/static-test-only/hold-checkpoint-only",
        "This ticket does not modify `meg/`",
        "This ticket does not implement source fetching",
        "This ticket does not approve source-fetching implementation",
        "This ticket does not approve source-fetching implementation planning",
        "source-fetching runtime implementation track remains held",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_owner_decision_not_selected_and_non_approval_signals_rejected() -> None:
    text = _read()
    required_phrases = [
        "No owner decision has been selected in this ticket",
        "Silence, continuation, lack of objection, or non-interference must not be treated as approval",
        "Continuation of documentation work is not approval",
        "The absence of an objection is not approval",
        "Do not proceed to `source_fetching_runtime_implementation_plan` unless a later owner artifact explicitly selects `approve_narrow_source_fetching_runtime_implementation_plan`",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_held_work_conditions_and_blocked_work_values_appear() -> None:
    text = _read()
    for value in HELD_WORK | CONDITIONS_REQUIRED_TO_LEAVE_HOLD:
        assert value in text
    held_section = _section(text, "Held work")
    blocked_section = _section(text, "Blocked work during hold")
    for value in HELD_WORK:
        assert f"`{value}`" in held_section
        assert f"`{value}`" in blocked_section


def test_provider_source_execution_is_not_approved() -> None:
    text = _read()
    required_phrases = [
        "Provider connectors remain not approved",
        "Provider clients remain not created",
        "Live provider/source fetching remains not approved",
        "Forecast pulling, API calls, scraping, file downloads, and provider SDK usage remain not approved",
        "does not call providers",
        "does not fetch sources",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_credentials_generated_fixtures_scoring_trading_and_audit_not_approved() -> None:
    text = _read()
    required_phrases = [
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


def test_no_forbidden_execution_output_or_owner_approval_phrases() -> None:
    text = _read().lower()
    approval_suffix = " is " + "approved"
    created_suffix = " is " + "created"
    forbidden_patterns = [
        "provider connector" + approval_suffix,
        "provider client" + created_suffix,
        "source fetching" + approval_suffix,
        "source fetching implementation" + approval_suffix,
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
        assert not re.search(pattern, text), pattern


def test_canonical_identifier_contract_and_no_market_id_routing() -> None:
    canonical_section = _section(_read(), "Canonical identifier posture")
    for identifier in ("condition_id", "token_id", "outcome"):
        assert f"`{identifier}`" in canonical_section
    assert "No routing on `market_id` is introduced or approved" in canonical_section


def test_machine_checkable_assignments_are_complete_and_allowed() -> None:
    assignments = _assignments(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field] == allowed_values


def test_every_actual_machine_checkable_assignment_value_is_allowed() -> None:
    assignments = _assignments(_read())
    for field, values in assignments.items():
        assert field in ALLOWED_ASSIGNMENTS
        assert values <= ALLOWED_ASSIGNMENTS[field]


def test_machine_checkable_parser_is_section_scoped() -> None:
    text = _read()
    machine_section = _machine_section(text)
    assert "Acceptance criteria" not in machine_section

    synthetic = (
        "# Example\n\n"
        f"{MACHINE_HEADING}\n\n"
        "- evidence status: hold_checkpoint_recorded\n\n"
        "## Acceptance criteria\n\n"
        "- evidence status: forged_after_next_heading\n"
        "- recommended next track: source_fetching_runtime_implementation_plan\n"
    )
    assert _assignments(synthetic) == {"evidence status": {"hold_checkpoint_recorded"}}


def test_recommended_next_track_owner_decision_only_not_implementation() -> None:
    text = _read()
    recommended = _section(text, "Recommended next ticket")
    assert "Recommended next ticket: `source_fetching_runtime_owner_decision_record`" in recommended
    assert "should record an explicit owner decision only" in recommended
    assert "must not implement source fetching" in recommended
    assert "must not create provider connectors" in recommended
    assert _assignments(text)["recommended next track"] == {
        "source_fetching_runtime_owner_decision_record"
    }
