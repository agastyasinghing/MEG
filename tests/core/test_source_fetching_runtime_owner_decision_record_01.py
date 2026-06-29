"""Static checks for Source Fetching Runtime Owner Decision Record."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "SOURCE-FETCHING-RUNTIME-OWNER-DECISION-RECORD-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-fetching runtime owner-decision-record assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to source-fetching runtime hold checkpoint",
    "Owner decision objective",
    "Recorded owner decision",
    "Decision rationale",
    "Current state",
    "Held work after decision",
    "Non-approval boundary",
    "Source fetching implementation boundary",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Audit report and export boundary",
    "Canonical identifier posture",
    "Blocked work after owner decision",
    "Conditions required to revisit decision",
    "Recommended next ticket",
    "Machine-checkable source-fetching runtime owner-decision-record assignments",
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
CONDITIONS_REQUIRED_TO_REVISIT = {
    "approve_narrow_source_fetching_runtime_implementation_plan",
    "deny_source_fetching_runtime_implementation_plan",
    "request_revision_to_source_fetching_runtime_implementation_request",
    "hold_source_fetching_runtime_track",
}
RATIONALE = {
    "source_fetching_runtime_implementation_approval_request_landed",
    "source_fetching_runtime_hold_checkpoint_landed",
    "explicit_approval_not_selected",
    "silence_is_not_approval",
    "continuation_is_not_approval",
    "non_interference_is_not_approval",
    "hold_selected_for_safety",
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_runtime_owner_decision_record"},
    "owner decision record status": {
        "docs_static_test_only",
        "owner_decision_record_only",
        "post_source_fetching_runtime_hold_checkpoint",
    },
    "recorded owner decision": {"hold_source_fetching_runtime_track"},
    "decision rationale": RATIONALE,
    "current state posture": {
        "owner_decision_recorded",
        "source_fetching_not_implemented",
        "implementation_approval_not_granted",
        "source_fetching_runtime_track_held",
    },
    "held work after decision": HELD_WORK,
    "condition required to revisit decision": CONDITIONS_REQUIRED_TO_REVISIT,
    "blocked work after owner decision": HELD_WORK,
    "provider source posture": {
        "provider_connectors_not_approved",
        "provider_clients_not_created",
        "live_provider_source_fetching_not_approved",
        "owner_decision_record_only",
    },
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "audit output posture": {"no_report_writing", "no_external_export", "no_persistence"},
    "implementation posture": {
        "docs_static_test_only",
        "owner_decision_record_only",
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
    "recommended next track": {"source_fetching_runtime_track_hold_closeout"},
    "conditional next track": {
        "source_fetching_owner_decision_record_revision_if_scope_too_broad",
        "source_fetching_runtime_owner_decision_revision_if_owner_changes_decision",
    },
    "evidence status": {"owner_decision_recorded"},
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
        "# SOURCE-FETCHING-RUNTIME-OWNER-DECISION-RECORD-01 — "
        "Source Fetching Runtime Owner Decision Record"
    )
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_docs_static_owner_decision_scope_and_no_meg_modification_posture() -> None:
    text = _read()
    required_phrases = [
        "docs/static-test-only/owner-decision-record-only",
        "This ticket does not modify `meg/`",
        "This ticket records `hold_source_fetching_runtime_track`",
        "This ticket does not implement source fetching",
        "This ticket does not approve source-fetching implementation",
        "This ticket does not approve source-fetching implementation planning",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_recorded_owner_decision_exact_and_non_approval_signals_rejected() -> None:
    text = _read()
    assert "Recorded owner decision: hold_source_fetching_runtime_track" in _section(
        text, "Recorded owner decision"
    )
    required_phrases = [
        "Silence, continuation, lack of objection, and non-interference are not approval",
        "Landing PR #275, landing PR #276, continuing documentation work, lacking objection, and not interfering with this ticket are not approval",
        "does not proceed to `source_fetching_runtime_implementation_plan`",
        "does not approve source-fetching implementation and does not approve source-fetching implementation planning",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_current_state_and_rationale_values_appear() -> None:
    text = _read()
    for value in RATIONALE:
        assert value in _section(text, "Decision rationale")
    required_phrases = [
        "Source fetching remains not implemented",
        "Implementation approval remains not granted",
        "Provider connectors remain not approved",
        "Provider clients remain not created",
        "Live provider/source fetching remains not approved",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_held_work_conditions_and_blocked_work_values_appear() -> None:
    text = _read()
    held_section = _section(text, "Held work after decision")
    blocked_section = _section(text, "Blocked work after owner decision")
    revisit_section = _section(text, "Conditions required to revisit decision")
    for value in HELD_WORK:
        assert f"`{value}`" in held_section
        assert f"`{value}`" in blocked_section
    for value in CONDITIONS_REQUIRED_TO_REVISIT:
        assert f"`{value}`" in revisit_section
    assert "Only `approve_narrow_source_fetching_runtime_implementation_plan` may unlock" in revisit_section


def test_provider_source_execution_is_not_approved() -> None:
    text = _read()
    required_phrases = [
        "Provider connectors remain not approved",
        "Provider clients remain not created",
        "Live provider/source fetching remains not approved",
        "Forecast pulling, API calls, scraping, file downloads, and provider SDK usage remain not approved",
        "does not call providers",
        "does not fetch sources",
        "does not pull forecasts",
        "does not execute API calls",
        "does not scrape",
        "does not download files",
        "does not use provider SDKs",
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


def test_no_forbidden_execution_output_or_approval_phrases() -> None:
    text = _read().lower()
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
        assert not re.search(pattern, text), pattern


def test_canonical_identifier_contract_and_no_legacy_market_routing() -> None:
    canonical_section = _section(_read(), "Canonical identifier posture")
    for identifier in ("condition_id", "token_id", "outcome"):
        assert f"`{identifier}`" in canonical_section
    assert "No routing on `" + "market" + "_id" + "` is introduced or approved" in canonical_section


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
        "- evidence status: owner_decision_recorded\n\n"
        "## Acceptance criteria\n\n"
        "- evidence status: forged_after_next_heading\n"
        "- recommended next track: source_fetching_runtime_implementation_plan\n"
    )
    assert _assignments(synthetic) == {"evidence status": {"owner_decision_recorded"}}


def test_recommended_next_track_closeout_only_not_implementation() -> None:
    text = _read()
    recommended = _section(text, "Recommended next ticket")
    assert "Recommended next ticket: `source_fetching_runtime_track_hold_closeout`" in recommended
    assert "should close out the held track as docs/static-test-only" in recommended
    assert "It must not implement source fetching" in recommended
    assert "must not create provider connectors" in recommended
    assert _assignments(text)["recommended next track"] == {
        "source_fetching_runtime_track_hold_closeout"
    }
