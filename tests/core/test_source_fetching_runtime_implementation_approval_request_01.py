"""Static checks for Source Fetching Runtime Implementation Approval Request."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "SOURCE-FETCHING-RUNTIME-IMPLEMENTATION-APPROVAL-REQUEST-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = (
    "## Machine-checkable source-fetching runtime implementation "
    "approval-request assignments"
)
OWNER_QUESTION = (
    "Should MEG proceed to a narrow source-fetching runtime implementation plan "
    "after this approval request, limited to supplied-control-plane metadata, "
    "validation gates, and non-production source retrieval scaffolding, with no "
    "trading, autonomy, scoring, backtesting, generated data, fixtures, or "
    "production behavior?"
)

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to Weather Bot PRD and architecture alignment",
    "Relationship to source-fetching runtime readiness review",
    "Approval request objective",
    "Current state",
    "Approval question for owner",
    "Proposed future implementation scope if approved",
    "Proposed future non-goals if approved",
    "Required future controls if approved",
    "Required future validation chain if approved",
    "Required future source identity boundary",
    "Required future retrieval context boundary",
    "Required future provider/source-family boundary",
    "Required future manual review gate boundary",
    "Required future no-lookahead boundary",
    "Required future fail-closed validation boundary",
    "Required future static audit boundary",
    "Non-approval boundary",
    "Source fetching implementation boundary",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Audit report and export boundary",
    "Canonical identifier posture",
    "Owner decision options",
    "Blocked work during approval request",
    "Recommended next ticket",
    "Machine-checkable source-fetching runtime implementation approval-request assignments",
    "Acceptance criteria",
)
OWNER_DECISION_OPTIONS = {
    "approve_narrow_source_fetching_runtime_implementation_plan",
    "deny_source_fetching_runtime_implementation_plan",
    "request_revision_to_source_fetching_runtime_implementation_request",
    "hold_source_fetching_runtime_track",
}
PROPOSED_FUTURE_IMPLEMENTATION_SCOPE = {
    "source_retrieval_intent_metadata",
    "source_retrieval_request_record",
    "source_retrieval_result_metadata",
    "retrieval_attempt_status_metadata",
    "provider_execution_posture_metadata",
    "no_lookahead_verification_metadata",
    "manual_review_gate_consumption",
    "fail_closed_validation_consumption",
    "static_audit_surface_consumption",
}
PROPOSED_FUTURE_NON_GOALS = {
    "production_provider_connector",
    "production_provider_client",
    "live_trading_runtime",
    "order_placement",
    "autonomous_execution",
    "scoring_model",
    "backtesting_engine",
    "generated_dataset_creation",
    "fixture_data_expansion",
    "credential_secret_management",
    "external_export_pipeline",
    "audit_report_writer",
}
REQUIRED_FUTURE_CONTROLS = {
    "manual_review_required_before_runtime_use",
    "no_lookahead_required_before_runtime_use",
    "fail_closed_validation_required",
    "static_audit_surface_required",
    "condition_id_token_id_outcome_required",
    "provider_execution_posture_explicit",
    "source_access_method_explicit",
    "decision_time_and_availability_metadata_required",
    "no_production_behavior_without_separate_approval",
}
ALLOWED_FUTURE_CONSUMPTION_POSTURES = {
    "read_approval_request_only",
    "require_owner_decision_before_plan",
    "preserve_condition_id_token_id_outcome",
    "maintain_supplied_metadata_only_until_approval",
    "maintain_fail_closed_until_approval",
    "maintain_no_lookahead_until_approval",
    "no_source_fetching_implementation_in_this_ticket",
    "no_provider_execution_in_this_ticket",
    "no_live_fetching_in_this_ticket",
    "no_credentials_config_loading_in_this_ticket",
    "no_generated_data_in_this_ticket",
    "no_fixture_change_in_this_ticket",
    "no_scoring_backtesting_in_this_ticket",
    "no_trading_autonomy_production_in_this_ticket",
    "no_report_writing_in_this_ticket",
    "no_external_export_in_this_ticket",
    "no_persistence_in_this_ticket",
}
BLOCKED_WORK_DURING_APPROVAL_REQUEST = {
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
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"source_fetching_runtime_implementation_approval_request"},
    "approval request status": {
        "docs_static_test_only",
        "approval_request_only",
        "post_source_fetching_runtime_readiness_review",
    },
    "current state posture": {
        "source_fetching_runtime_readiness_review_landed",
        "stage2_runtime_metadata_scaffold_sequence_landed",
        "source_fetching_not_implemented",
        "implementation_approval_not_granted_before_this_request",
        "provider_connectors_not_approved",
        "provider_clients_not_created",
        "credentials_config_loading_not_approved",
        "generated_data_not_approved",
        "fixtures_not_approved",
        "scoring_backtesting_not_approved",
        "trading_autonomy_production_not_approved",
    },
    "approval question": {"narrow_source_fetching_runtime_implementation_plan_owner_decision"},
    "owner decision option": OWNER_DECISION_OPTIONS,
    "proposed future implementation scope": PROPOSED_FUTURE_IMPLEMENTATION_SCOPE,
    "proposed future non-goal": PROPOSED_FUTURE_NON_GOALS,
    "required future control": REQUIRED_FUTURE_CONTROLS,
    "allowed future consumption posture": ALLOWED_FUTURE_CONSUMPTION_POSTURES,
    "blocked work during approval request": BLOCKED_WORK_DURING_APPROVAL_REQUEST,
    "provider source posture": {
        "provider_connectors_not_approved",
        "provider_clients_not_created",
        "live_provider_source_fetching_not_approved",
        "approval_request_only",
    },
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "audit output posture": {"no_report_writing", "no_external_export", "no_persistence"},
    "implementation posture": {
        "docs_static_test_only",
        "approval_request_only",
        "no_runtime_code_change",
        "no_source_fetching",
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
    "recommended next track if approved": {"source_fetching_runtime_implementation_plan"},
    "recommended next track if denied_or_held": {"source_fetching_runtime_hold_checkpoint"},
    "recommended next track if revision_requested": {
        "source_fetching_runtime_implementation_approval_request_revision"
    },
    "evidence status": {"approval_request_recorded"},
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
        "# SOURCE-FETCHING-RUNTIME-IMPLEMENTATION-APPROVAL-REQUEST-01 — "
        "Source Fetching Runtime Implementation Approval Request"
    )
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_docs_static_approval_only_scope_and_no_meg_modification_posture() -> None:
    text = _read()
    required_phrases = [
        "docs/static-test-only/approval-request-only",
        "This ticket does not modify `meg/`",
        "This ticket does not implement source fetching",
        "This ticket does not approve source-fetching implementation by itself",
        "This ticket only asks the owner whether to approve a later narrow source-fetching runtime implementation plan",
        "Weather Bot models the market settlement rule, not generic weather",
        "All landed Stage 2 runtime metadata artifacts remain supplied-metadata-only and fail-closed",
        "Source fetching remains not implemented",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_owner_question_options_scope_non_goals_and_controls_appear() -> None:
    text = _read()
    assert OWNER_QUESTION in text
    for value in (
        OWNER_DECISION_OPTIONS
        | PROPOSED_FUTURE_IMPLEMENTATION_SCOPE
        | PROPOSED_FUTURE_NON_GOALS
        | REQUIRED_FUTURE_CONTROLS
        | ALLOWED_FUTURE_CONSUMPTION_POSTURES
        | BLOCKED_WORK_DURING_APPROVAL_REQUEST
    ):
        assert value in text


def test_provider_source_execution_is_not_approved() -> None:
    text = _read()
    required_phrases = [
        "Provider connectors remain not approved",
        "Provider clients remain not created",
        "Live provider/source fetching remains not approved",
        "Forecast pulling, API calls, scraping, file downloads, and provider SDK usage remain not approved",
        "It may not create provider connectors or live source fetching",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_credentials_generated_data_fixtures_scoring_trading_and_audit_not_approved() -> None:
    text = _read()
    required_phrases = [
        "Credentials/config loading remains not approved",
        "does not modify `.env`, secrets, credentials, config, or config-loading behavior",
        "Generated data and fixtures remain not approved",
        "does not modify `tests/fixtures/`",
        "Scoring/backtesting remains not approved",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
        "does not create audit reports, persisted audit output, export files, or external export behavior",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_no_forbidden_execution_or_output_approval_phrases() -> None:
    text = _read().lower()
    approved_suffix = " is " + "approved"
    created_suffix = " is " + "created"
    forbidden_patterns = [
        "provider connector" + approved_suffix,
        "provider client" + created_suffix,
        "source fetching" + approved_suffix,
        "source fetching implementation" + approved_suffix,
        "live provider source fetching" + approved_suffix,
        "forecast pull" + approved_suffix,
        "api call" + approved_suffix,
        "scraping" + approved_suffix,
        "file download" + approved_suffix,
        "provider sdk" + approved_suffix,
        "credentials.*loading" + approved_suffix,
        "generated data" + approved_suffix,
        "fixture change" + approved_suffix,
        "scoring" + approved_suffix,
        "backtesting" + approved_suffix,
        "trading" + approved_suffix,
        "order placement" + approved_suffix,
        "autonomy" + approved_suffix,
        "production behavior" + approved_suffix,
        "report writing" + approved_suffix,
        "external export" + approved_suffix,
        "persistence" + approved_suffix,
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text), pattern


def test_canonical_identifier_contract_and_no_market_id_routing() -> None:
    text = _read()
    canonical_section = _section(text, "Canonical identifier posture")
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
        "- evidence status: approval_request_recorded\n\n"
        "## Acceptance criteria\n\n"
        "- evidence status: forged_after_next_heading\n"
        "- recommended next track if approved: source_fetching_runtime_implementation\n"
    )
    parsed = _assignments(synthetic)
    assert parsed == {"evidence status": {"approval_request_recorded"}}


def test_recommended_next_tracks_and_later_plan_framing() -> None:
    text = _read()
    recommended = _section(text, "Recommended next ticket")
    assert "If owner approves: `source_fetching_runtime_implementation_plan`" in recommended
    assert "If owner denies or holds: `source_fetching_runtime_hold_checkpoint`" in recommended
    assert (
        "If owner requests revision: `source_fetching_runtime_implementation_approval_request_revision`"
        in recommended
    )
    assert "must itself be a later plan, not implementation inside this approval request" in recommended
    assert "This approval request must not itself implement source fetching" in recommended
    assignments = _assignments(text)
    assert assignments["recommended next track if approved"] == {
        "source_fetching_runtime_implementation_plan"
    }
    assert assignments["recommended next track if denied_or_held"] == {
        "source_fetching_runtime_hold_checkpoint"
    }
    assert assignments["recommended next track if revision_requested"] == {
        "source_fetching_runtime_implementation_approval_request_revision"
    }
