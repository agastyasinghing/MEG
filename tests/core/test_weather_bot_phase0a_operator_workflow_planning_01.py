"""Static checks for Weather Bot Phase 0A operator workflow planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-OPERATOR-WORKFLOW-PLANNING-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_operator_workflow_planning_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A operator-workflow-planning assignments"
NEXT_TRACK = "weather_bot_phase0a_supplied_market_contract_input_planning"
CONDITIONAL_TRACK = "weather_bot_phase0a_operator_workflow_revision_if_scope_too_broad"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to evaluation metrics planning", "Operator workflow planning objective",
    "Current held/closed source-fetching posture", "No owner-decision revision boundary",
    "Operator workflow readiness status", "Operator workflow overview", "Operator intake states",
    "Operator review states", "Operator decision labels", "Operator handoff checkpoints",
    "Manual-review gate relationship", "No-lookahead review relationship", "Fail-closed review relationship",
    "Evaluation metrics relationship", "Operator workflow readiness blockers", "Static planning only boundary",
    "Canonical identifier posture", "Source-fetching track remains blocked", "Provider/source execution boundary",
    "Credential/config boundary", "Generated-data and fixture boundary", "Scoring/evaluation boundary",
    "Backtesting boundary", "Paper-trade boundary", "Operator workflow execution boundary",
    "Trading/autonomy/production boundary", "Audit report and export boundary", "Stage 2 runtime metadata posture",
    "Embedded self-review requirement", "Recommended next ticket", MACHINE_HEADING, "Acceptance criteria",
)
OPERATOR_WORKFLOW_READINESS = {
    "not_operator_workflow_ready", "docs_static_operator_workflow_planning_only",
    "runtime_manual_review_workflow_not_implemented", "operator_decision_execution_not_approved",
    "manual_review_ui_not_implemented", "operator_decision_persistence_not_approved",
    "source_fetching_not_implemented", "evaluation_execution_not_approved", "paper_trade_execution_not_approved",
}
INTAKE_STATES = {
    "operator_intake_pending", "operator_intake_requires_market_contract",
    "operator_intake_requires_canonical_identifiers", "operator_intake_requires_settlement_rule",
    "operator_intake_requires_stage2_metadata", "operator_intake_blocked_by_missing_source",
    "operator_intake_blocked_by_hold_state",
}
REVIEW_STATES = {
    "operator_review_not_started", "operator_review_in_progress", "operator_review_requires_manual_checklist",
    "operator_review_requires_no_lookahead_check", "operator_review_requires_fail_closed_check",
    "operator_review_requires_metric_context", "operator_review_blocked", "operator_review_complete_static_only",
}
DECISION_LABELS = {
    "operator_decision_not_available", "operator_decision_pass_static_review",
    "operator_decision_block_missing_required_field", "operator_decision_block_ambiguous_rule",
    "operator_decision_block_identifier_mismatch", "operator_decision_block_lookahead_uncertainty",
    "operator_decision_block_unsupported_measurement", "operator_decision_block_source_unapproved",
    "operator_decision_requires_scope_revision", "operator_decision_requires_future_approval",
}
HANDOFF_CHECKPOINTS = {
    "handoff_market_contract_checked", "handoff_canonical_identifiers_checked", "handoff_settlement_rule_checked",
    "handoff_manual_review_checklist_checked", "handoff_no_lookahead_checked", "handoff_fail_closed_checked",
    "handoff_stage2_metadata_checked", "handoff_metrics_context_checked", "handoff_blocked_work_checked",
    "handoff_next_scope_checked",
}
WORKFLOW_BLOCKERS = {
    "block_operator_workflow_runtime_missing", "block_operator_decision_execution_unapproved",
    "block_manual_review_ui_missing", "block_operator_decision_persistence_unapproved", "block_source_fetching_unapproved",
    "block_scoring_evaluation_unapproved", "block_backtesting_unapproved", "block_paper_trade_execution_not_approved",
    "block_trading_autonomy_production_not_approved", "block_audit_persistence_export_not_approved",
}
STAGE2_PATHS = {
    "meg/weather/stage2/source_identity_runtime.py", "meg/weather/stage2/retrieval_context_runtime.py",
    "meg/weather/stage2/provider_source_family_runtime.py", "meg/weather/stage2/manual_review_gate_runtime.py",
    "meg/weather/stage2/no_lookahead_metadata_runtime.py", "meg/weather/stage2/fail_closed_validation_runtime.py",
    "meg/weather/stage2/static_audit_surface_runtime.py",
}
STAGE2_ASSIGNMENTS = {
    "source_identity_runtime_py", "retrieval_context_runtime_py", "provider_source_family_runtime_py",
    "manual_review_gate_runtime_py", "no_lookahead_metadata_runtime_py", "fail_closed_validation_runtime_py",
    "static_audit_surface_runtime_py",
}
BLOCKED_WORK = {
    "owner_decision_revision", "source_fetching_runtime_implementation_plan", "source_fetching_implementation",
    "provider_connector_implementation", "provider_client_creation", "live_provider_source_fetching", "forecast_pull_execution",
    "api_call_execution", "scraping_execution", "file_download_execution", "provider_sdk_execution",
    "credentials_config_loading", "generated_data_creation", "fixture_data_modification", "runtime_metadata_implementation",
    "stage2_runtime_module_modification", "fail_closed_runtime_enforcement", "runtime_error_handling",
    "no_lookahead_runtime_enforcement", "timestamp_runtime_validation", "settlement_rule_runtime_parser",
    "settlement_rule_runtime_classification", "manual_review_runtime_workflow", "manual_review_ui",
    "manual_review_persistence", "operator_decision_execution", "operator_decision_persistence", "scoring_implementation",
    "evaluation_execution", "metric_persistence", "backtesting_implementation", "paper_trade_execution",
    "paper_trade_readiness_runtime", "order_simulation", "runtime_trading_behavior", "order_placement",
    "autonomy_behavior", "production_behavior", "audit_report_generation", "audit_output_persistence",
    "external_export_behavior", "standalone_self_review_prd_artifact",
}
IMPLEMENTATION_POSTURES = {
    "docs_static_test_only", "operator_workflow_planning_only", "no_runtime_code_change",
    "no_stage2_runtime_module_modification", "no_runtime_metadata_implementation", "no_owner_decision_revision",
    "no_source_fetching", "no_source_fetching_plan", "no_provider_connector", "no_provider_client",
    "no_live_provider_fetching", "no_credential_config_loading", "no_generated_data", "no_fixture_change",
    "no_fail_closed_runtime_enforcement", "no_runtime_error_handling", "no_no_lookahead_runtime_enforcement",
    "no_timestamp_runtime_validation", "no_settlement_rule_runtime_parser", "no_manual_review_runtime_workflow",
    "no_manual_review_ui", "no_manual_review_persistence", "no_operator_decision_execution",
    "no_operator_decision_persistence", "no_scoring_implementation", "no_evaluation_execution",
    "no_metric_persistence", "no_backtesting_implementation", "no_paper_trade_execution", "no_order_simulation",
    "no_trading_autonomy_production", "no_report_writing", "no_external_export", "no_persistence",
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_phase0a_operator_workflow_planning"},
    "operator workflow status": {"docs_static_test_only", "operator_workflow_planning_only", "post_weather_bot_phase0a_evaluation_metrics_planning"},
    "operator workflow readiness status": OPERATOR_WORKFLOW_READINESS,
    "self review posture": {"embedded_secondary_prompt_only", "no_standalone_self_review_prd"},
    "owner decision posture": {"no_owner_decision_revision", "hold_source_fetching_runtime_track_preserved"},
    "source fetching track posture": {"closed_held", "no_source_fetching_implementation_plan", "no_source_fetching_implementation", "implementation_approval_not_granted"},
    "operator intake state": INTAKE_STATES,
    "operator review state": REVIEW_STATES,
    "operator decision label": DECISION_LABELS,
    "operator handoff checkpoint": HANDOFF_CHECKPOINTS,
    "operator workflow blocker": WORKFLOW_BLOCKERS,
    "stage2 metadata artifact": STAGE2_ASSIGNMENTS,
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "identifier relationship": {"token_outcome_pair_derived_relationship", "condition_token_outcome_preserved", "token_id_outcome_relationship_preserved"},
    "fail closed canonical guard": {"market_identifier_routing_attempt"},
    "blocked work": BLOCKED_WORK,
    "implementation posture": IMPLEMENTATION_POSTURES,
    "recommended next track": {NEXT_TRACK},
    "conditional next track": {CONDITIONAL_TRACK},
    "evidence status": {"operator_workflow_planning_recorded"},
    "label confidence": {"confirmed"},
}
REQUIRED_ASSIGNMENTS = {(field, value) for field, values in ALLOWED_ASSIGNMENTS.items() for value in values}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
FORBIDDEN_APPROVAL_RE = re.compile(
    r"revised " "owner decision|approve_narrow_source_fetching_runtime" "_implementation_plan|"
    r"provider connector " "is approved|provider client " "is created|source fetching " "is approved|"
    r"source fetching implementation " "is approved|source fetching implementation planning " "is approved|"
    r"source fetching implementation plan " "is approved|live provider source fetching " "is approved|"
    r"forecast pull " "is approved|api call " "is approved|scraping " "is approved|file download " "is approved|"
    r"provider sdk " "is approved|credentials.*loading " "is approved|generated data " "is approved|"
    r"fixture change " "is approved|runtime metadata implementation " "is approved|"
    r"stage2 runtime module modification " "is approved|fail-closed enforcement " "is approved|"
    r"fail closed enforcement " "is approved|runtime error handling " "is approved|"
    r"no-lookahead enforcement " "is approved|no lookahead enforcement " "is approved|"
    r"timestamp validation " "is approved|settlement rule parser " "is approved|settlement rule classification " "is approved|"
    r"manual review workflow " "is approved|manual review ui " "is approved|manual review persistence " "is approved|"
    r"operator decision execution " "is approved|operator decision persistence " "is approved|scoring " "is approved|"
    r"evaluation execution " "is approved|metric persistence " "is approved|backtesting " "is approved|"
    r"paper trade execution " "is approved|paper trade readiness runtime " "is approved|order simulation " "is approved|"
    r"trading " "is approved|order placement " "is approved|autonomy " "is approved|production behavior " "is approved|"
    r"report writing " "is approved|external export " "is approved|persistence " "is approved|silence " "is approval|"
    r"continuation " "is approval|non-interference " "is approval",
    re.IGNORECASE,
)


def _read() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    assert match, heading
    assert match.group("section").strip(), heading
    return match.group("section")


def _assignment_pairs(text: str) -> set[tuple[str, str]]:
    return {(m.group("field"), m.group("value")) for m in ASSIGNMENT_RE.finditer(_section(text, MACHINE_HEADING))}


def test_document_exists_canonical_id_and_sections_are_non_empty() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert text.startswith(f"# {CANONICAL_ID} — Weather Bot Phase 0A Operator Workflow Planning")
    assert f"Canonical ID: {CANONICAL_ID}" in text
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_test_file_is_stdlib_only_and_does_not_import_production_modules() -> None:
    tree = ast.parse(TEST_PATH.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    assert set(imports) <= {"__future__", "ast", "re", "pathlib"}
    assert all(not item.startswith("meg") for item in imports)


def test_required_posture_and_non_execution_boundaries_are_present() -> None:
    text = _read()
    required = [
        "docs/static-test-only/operator-workflow-planning-only", "This ticket does not modify `meg/`",
        "This ticket does not modify meta/handoff files", "does not modify Stage 2 runtime metadata modules",
        "does not revise the owner decision", "does not reopen source-fetching implementation planning",
        "does not fetch, create, or modify market data", "does not create fixtures or generated data",
        "does not implement runtime metadata behavior", "does not implement runtime fail-closed enforcement",
        "does not implement runtime error handling", "does not implement runtime no-lookahead enforcement",
        "does not implement runtime timestamp validation", "does not implement runtime settlement-rule parsing or classification",
        "does not implement runtime manual-review workflow behavior", "does not implement operator decision execution",
        "does not implement manual-review UI or persistence",
        "does not implement scoring, evaluation execution, backtesting, paper trading, trading, or autonomy",
        "does not execute paper trades", "does not create simulated orders",
        "does not create reports, persisted metrics, persisted audit output, persisted operator decisions, or external exports",
        "does not create a separate standalone self-review artifact", "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work",
        "source-fetching runtime track remains closed/held", "closed owner decision remains `hold_source_fetching_runtime_track`",
        "Source fetching remains not implemented", "Implementation approval remains not granted",
        "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
        "Paper-trade readiness remains not achieved", "Evaluation readiness remains not achieved",
        "Operator workflow runtime behavior remains not implemented", "Provider connectors remain not approved",
        "Provider clients remain not created", "Live provider/source fetching remains not approved",
        "Credentials/config loading remains not approved", "Generated data and fixtures remain not approved",
        "Scoring/evaluation execution remains not approved", "Backtesting remains not approved",
        "Paper-trade execution remains not approved", "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, metric persistence, operator-decision persistence, and external export remain not approved",
        "Silence, continuation, lack of objection, and non-interference are not approval",
    ]
    for phrase in required:
        assert phrase in text


def test_values_paths_and_blocked_work_appear() -> None:
    text = _read()
    values = (OPERATOR_WORKFLOW_READINESS | INTAKE_STATES | REVIEW_STATES | DECISION_LABELS |
              HANDOFF_CHECKPOINTS | WORKFLOW_BLOCKERS | STAGE2_PATHS | BLOCKED_WORK)
    for value in values:
        assert value in text


def test_operator_workflow_readiness_is_not_ready() -> None:
    section = _section(_read(), "Operator workflow readiness status")
    for status in OPERATOR_WORKFLOW_READINESS:
        assert f"`{status}`" in section
    assert "`not_operator_workflow_ready`" in section


def test_canonical_identifier_posture_is_preserved() -> None:
    section = _section(_read(), "Canonical identifier posture")
    assert "Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`" in section
    assert "Future reasoning must preserve all three canonical shared-rail identifiers" in section
    assert "Future reasoning must preserve the relationship between `token_id` and `outcome`" in section
    assert "`token_outcome_pair` remains a derived relationship, not a replacement for canonical fields" in section
    assert "`market_id` remains explicitly non-routing only" in section
    assert "No routing on `market_id` is introduced or approved" in section
    assert "A `market_identifier_routing_attempt` remains fail-closed" in section


def test_execution_approval_boundaries_are_present() -> None:
    text = _read()
    required = [
        "Forecast pull execution, API call execution, scraping execution, file download execution, and provider SDK execution remain not approved",
        "Credentials/config loading remains not approved", "Generated data and fixtures remain not approved",
        "does not implement runtime metadata behavior", "does not modify Stage 2 runtime metadata modules",
        "does not implement runtime fail-closed enforcement", "does not implement runtime error handling",
        "does not implement runtime no-lookahead enforcement", "does not implement runtime timestamp validation",
        "does not implement runtime manual-review workflow behavior", "does not implement runtime settlement-rule parsing or classification",
        "does not implement operator decision execution", "does not implement manual-review UI or persistence",
        "Scoring/evaluation execution remains not approved", "Backtesting remains not approved",
        "Paper-trade execution remains not approved", "does not create simulated orders",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, metric persistence, operator-decision persistence, and external export remain not approved",
    ]
    for phrase in required:
        assert phrase in text


def test_machine_assignments_are_section_scoped_complete_and_allowed() -> None:
    pairs = _assignment_pairs(_read())
    assert pairs == REQUIRED_ASSIGNMENTS
    by_field: dict[str, set[str]] = {}
    for field, value in pairs:
        assert field in ALLOWED_ASSIGNMENTS
        assert value in ALLOWED_ASSIGNMENTS[field]
        by_field.setdefault(field, set()).add(value)
    assert by_field["canonical routing field"] == {"condition_id", "token_id", "outcome"}
    assert by_field["non routing field"] == {"market_id"}
    assert by_field["fail closed canonical guard"] == {"market_identifier_routing_attempt"}
    assert by_field["recommended next track"] == {NEXT_TRACK}
    assert "self_review" not in NEXT_TRACK
    assert by_field["conditional next track"] == {CONDITIONAL_TRACK}


def test_machine_assignment_parser_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        "## Machine-checkable Weather Bot Phase 0A operator-workflow-planning assignments\n"
        "- label confidence: confirmed\n\n"
        "## Acceptance criteria\n"
        "- label confidence: invalid_after_next_heading\n"
    )
    assert _assignment_pairs(synthetic) == {("label confidence", "confirmed")}


def test_embedded_self_review_and_next_ticket_are_not_standalone_review_track() -> None:
    text = _read()
    section = _section(text, "Embedded self-review requirement")
    assert "self-reviewed using the secondary self-review prompt" in section
    assert "self-review result must be summarized in the PR body" in section
    assert "Do not create a separate standalone self-review PRD artifact" in section
    assert "Do not recommend a standalone self-review ticket" in section
    recommended = _section(text, "Recommended next ticket")
    assert f"Recommended next ticket: `{NEXT_TRACK}`" in recommended
    assert "must not revise the owner decision" in recommended
    assert "must not implement source fetching" in recommended
    assert "Do not recommend a standalone self-review ticket" in recommended


def test_forbidden_approval_language_is_absent_and_regex_catches_unsafe_examples() -> None:
    combined = _read() + "\n" + TEST_PATH.read_text(encoding="utf-8")
    assert not FORBIDDEN_APPROVAL_RE.search(combined)
    unsafe_examples = [
        "revised " "owner decision", "source fetching " "is approved",
        "source fetching implementation planning " "is approved", "provider connector " "is approved",
        "runtime metadata implementation " "is approved", "stage2 runtime module modification " "is approved",
        "fail-closed enforcement " "is approved", "runtime error handling " "is approved",
        "no-lookahead enforcement " "is approved", "timestamp validation " "is approved",
        "settlement rule parser " "is approved", "manual review workflow " "is approved",
        "operator decision execution " "is approved", "operator decision persistence " "is approved",
        "evaluation execution " "is approved", "metric persistence " "is approved",
        "paper trade execution " "is approved", "order simulation " "is approved", "trading " "is approved",
        "report writing " "is approved", "persistence " "is approved", "silence " "is approval",
    ]
    for example in unsafe_examples:
        assert FORBIDDEN_APPROVAL_RE.search(example)
    allowed_negative_contexts = [
        "No owner-decision revision is being made in this ticket.",
        "This ticket does not revise the owner decision.",
        "Provider connectors remain not approved.",
        "Paper-trade execution remains not approved.",
        "Runtime trading/order placement/autonomy/production remains not approved.",
    ]
    for example in allowed_negative_contexts:
        assert not FORBIDDEN_APPROVAL_RE.search(example)
