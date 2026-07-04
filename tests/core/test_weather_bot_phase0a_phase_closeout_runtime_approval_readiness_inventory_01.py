from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-PHASE-CLOSEOUT-AND-RUNTIME-APPROVAL-READINESS-INVENTORY-01"
PRD = ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST = ROOT / "tests/core/test_weather_bot_phase0a_phase_closeout_runtime_approval_readiness_inventory_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A phase-closeout readiness assignments"
REQUIRED_TITLE = f"# {CANONICAL_ID} — Weather Bot Phase 0A Phase Closeout and Runtime Approval Readiness Inventory"
REQUIRED_CANONICAL = f"Canonical ID: {CANONICAL_ID}"
REQUIRED_SECTIONS = (
    "Status and scope", "Predecessor and stop condition", "Purpose", "Source-of-truth relationship",
    "Non-goals and non-approval boundaries", "Phase 0A closeout inventory overview",
    "Completed static-planning artifact inventory", "Canonical identifier posture", "Stage 2 metadata posture",
    "Settlement-rule interpreter posture", "No-lookahead validation posture", "Fail-closed validation posture",
    "Validation output packet posture", "Manual-review decision record posture", "Operator workflow posture",
    "Runtime approval readiness inventory", "Source-fetching and provider posture",
    "Paper-trade evaluation and trading posture", "Owner-decision gate inventory", "Blocker taxonomy",
    "Future handoff boundaries", "Static-test expectations", MACHINE_HEADING, "Embedded self-review requirement",
    "PR body validation requirement", "Acceptance criteria", "Recommended next ticket",
)
ASSIGNMENT_RE = re.compile(r"^- (?P<category>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
CLOSED_SETS = {
    "closeout inventory group": {
        "artifact_chain_inventory", "canonical_identifier_inventory", "stage2_metadata_inventory",
        "settlement_rule_interpreter_inventory", "no_lookahead_validation_inventory",
        "fail_closed_validation_inventory", "validation_output_packet_inventory",
        "manual_review_decision_record_inventory", "operator_workflow_inventory",
        "runtime_approval_readiness_inventory", "source_fetching_provider_inventory",
        "paper_trade_evaluation_trading_inventory", "owner_decision_gate_inventory", "non_approval_summary",
    },
    "closeout lifecycle status": {
        "planning_only", "docs_static_test_only", "not_runtime_contract", "not_persisted_schema",
        "not_executable", "not_exported", "not_report_output", "runtime_approval_not_granted",
    },
    "phase0a artifact status": {
        "static_planning_artifact_present", "static_test_guard_present", "planning_chain_inventory_only",
        "not_runtime_implementation", "future_gate_required",
    },
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "derived identifier field": {"token_outcome_pair"},
    "non routing field": {"market_id"},
    "runtime readiness status": {
        "not_runtime_ready", "not_paper_trade_ready", "not_evaluation_ready", "runtime_approval_not_granted",
        "source_fetching_not_approved", "provider_implementation_not_approved",
        "manual_review_runtime_not_implemented", "operator_decision_execution_not_implemented",
        "operator_decision_persistence_not_implemented", "blocked",
    },
    "source fetching posture": {
        "closed_held", "source_fetching_not_implemented", "implementation_approval_not_granted",
        "provider_connector_not_implemented", "provider_client_not_implemented", "api_calls_not_implemented",
        "forecast_pulls_not_implemented", "credentials_config_loading_not_implemented",
    },
    "validation runtime posture": {
        "settlement_rule_interpreter_runtime_not_implemented", "no_lookahead_validation_runtime_not_implemented",
        "fail_closed_validation_runtime_not_implemented", "runtime_ingestion_not_implemented",
        "runtime_loading_not_implemented", "runtime_validation_not_implemented",
        "runtime_parser_interpreter_not_implemented",
    },
    "trading readiness posture": {
        "scoring_evaluation_execution_not_implemented", "metric_persistence_not_implemented",
        "backtesting_not_implemented", "paper_trading_not_implemented", "order_simulation_not_implemented",
        "trading_autonomy_production_not_implemented",
    },
    "owner decision gate": {
        "runtime_approval_owner_decision_required", "source_fetching_owner_decision_required",
        "provider_connector_owner_decision_required", "paper_trade_owner_decision_required",
        "trading_owner_decision_required", "production_owner_decision_required",
    },
    "blocker class": {
        "runtime_approval_not_granted", "source_fetching_not_approved", "provider_implementation_not_approved",
        "runtime_ingestion_not_approved", "runtime_validation_not_approved",
        "settlement_rule_interpreter_not_implemented", "no_lookahead_validation_not_implemented",
        "fail_closed_validation_not_implemented", "manual_review_runtime_not_implemented",
        "operator_workflow_runtime_not_implemented", "operator_decision_execution_not_approved",
        "operator_decision_persistence_not_approved", "scoring_not_approved", "evaluation_not_approved",
        "paper_trading_not_approved", "trading_not_approved", "production_not_approved", "reports_not_approved",
        "persistence_not_approved", "audit_output_not_approved", "export_not_approved",
    },
    "implementation posture": {
        "no_runtime_code_change", "no_meg_modification", "no_source_fetching", "no_provider_connector",
        "no_provider_client", "no_api_call", "no_scraping", "no_file_download", "no_forecast_pull",
        "no_sdk_usage", "no_credentials_config_loading", "no_generated_data", "no_fixture_change",
        "no_schema_change", "no_db_migration", "no_runtime_ingestion", "no_runtime_loading",
        "no_runtime_validation", "no_runtime_parser_interpreter", "no_manual_review_runtime_workflow",
        "no_manual_review_ui", "no_operator_decision_execution", "no_operator_decision_persistence",
        "no_scoring_evaluation_execution", "no_metric_persistence", "no_backtesting", "no_paper_trading",
        "no_order_simulation", "no_trading_autonomy_production", "no_reports", "no_persistence",
        "no_audit_output", "no_export", "no_owner_decision_revision", "no_runtime_approval_granted",
    },
    "recommended next track": {"weather_bot_phase0a_runtime_approval_request_packet_planning"},
    "conditional next track": {"weather_bot_phase0a_closeout_inventory_revision_if_scope_too_broad"},
    "pr body validation status": {
        "required_headings_must_be_present", "exact_commands_must_be_reported",
        "embedded_self_review_summary_required", "safety_non_execution_summary_required",
        "changed_file_scope_audit_required", "targeted_safety_audit_required",
        "final_merge_recommendation_required", "recommended_next_ticket_required",
        "process_light_pr_body_blocked", "pr_body_must_be_fixed_before_review",
    },
}
REQUIRED_ASSIGNMENTS = {(category, value) for category, values in CLOSED_SETS.items() for value in values} | {
    ("weather bot planning stage", "weather_bot_phase0a_phase_closeout_and_runtime_approval_readiness_inventory"),
    ("predecessor pr", "pr_304"),
    ("predecessor artifact", "manual_review_decision_record_planning"),
    ("excluded predecessor pr", "pr_283_unmerged"),
    ("weather bot scope", "market_settlement_rule_not_generic_weather"),
    ("source fetching track posture", "closed_held"),
    ("source fetching track posture", "source_fetching_not_implemented"),
    ("source fetching track posture", "implementation_approval_not_granted"),
    ("readiness status", "paper_trade_readiness_not_achieved"),
    ("readiness status", "evaluation_readiness_not_achieved"),
    ("readiness status", "settlement_rule_interpreter_runtime_not_implemented"),
    ("readiness status", "no_lookahead_validation_runtime_not_implemented"),
    ("readiness status", "fail_closed_validation_runtime_not_implemented"),
    ("readiness status", "operator_workflow_runtime_not_implemented"),
    ("readiness status", "manual_review_runtime_not_implemented"),
    ("readiness status", "operator_decision_execution_not_implemented"),
    ("readiness status", "operator_decision_persistence_not_implemented"),
    ("readiness status", "runtime_approval_not_granted"),
    ("label confidence", "confirmed"),
}
REQUIRED_SOURCE_AREAS = (
    "manual-review decision record planning", "validation output packet planning", "operator workflow planning",
    "canonical identifier static audit", "Stage 2 metadata contract documentation",
    "no-lookahead validation planning", "fail-closed validation planning", "settlement-rule interpreter planning",
    "supplied market contract input planning", "evaluation metrics planning",
)
SELF_REVIEW_FRAGMENTS = ("self_review", "self-review", "standalone_self_review", "standalone-self-review")


def _read(path: Path = PRD) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<body>.*?)(?:\n## |\Z)", text, re.S | re.M)
    assert match, heading
    assert match.group("body").strip(), heading
    return match.group("body")


def _pairs_from_section(section: str) -> list[tuple[str, str]]:
    pairs = []
    for line in section.splitlines():
        if line.startswith("- "):
            match = ASSIGNMENT_RE.match(line)
            assert match, line
            pairs.append((match.group("category"), match.group("value")))
    return pairs


def _pairs(text: str) -> list[tuple[str, str]]:
    return _pairs_from_section(_section(text, MACHINE_HEADING))


def _assert_closed_sets(pairs: list[tuple[str, str]]) -> None:
    for category, allowed in CLOSED_SETS.items():
        actual = {value for field, value in pairs if field == category}
        assert actual == allowed, category


def test_prd_exists_title_canonical_id_and_required_sections() -> None:
    text = _read()
    assert text.startswith(REQUIRED_TITLE)
    assert REQUIRED_CANONICAL in text
    assert text.count(f"## {MACHINE_HEADING}") == 1
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_test_file_uses_only_standard_library_imports() -> None:
    tree = ast.parse(TEST.read_text(encoding="utf-8"))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    assert set(imports) <= {"__future__", "ast", "re", "pathlib"}


def test_machine_checkable_assignments_are_complete_and_closed_set_exact() -> None:
    pairs = _pairs(_read())
    assert set(pairs) == REQUIRED_ASSIGNMENTS
    _assert_closed_sets(pairs)


def test_canonical_market_and_token_outcome_assignments_are_scoped_correctly() -> None:
    pairs = _pairs(_read())
    assert {value for field, value in pairs if field == "canonical routing field"} == {"condition_id", "token_id", "outcome"}
    assert ("non routing field", "market_id") in pairs
    assert ("canonical routing field", "market_id") not in pairs
    assert ("derived identifier field", "token_outcome_pair") in pairs
    assert ("canonical routing field", "token_outcome_pair") not in pairs


def test_predecessor_exclusion_runtime_approval_and_next_tracks_are_recorded() -> None:
    pairs = _pairs(_read())
    assert ("predecessor pr", "pr_304") in pairs
    assert ("predecessor artifact", "manual_review_decision_record_planning") in pairs
    assert ("excluded predecessor pr", "pr_283_unmerged") in pairs
    assert ("closeout lifecycle status", "runtime_approval_not_granted") in pairs
    assert ("runtime readiness status", "runtime_approval_not_granted") in pairs
    assert ("blocker class", "runtime_approval_not_granted") in pairs
    assert ("implementation posture", "no_runtime_approval_granted") in pairs
    assert ("readiness status", "runtime_approval_not_granted") in pairs
    for value in CLOSED_SETS["implementation posture"]:
        assert ("implementation posture", value) in pairs
    next_values = [value for field, value in pairs if field in {"recommended next track", "conditional next track"}]
    assert next_values == [
        "weather_bot_phase0a_runtime_approval_request_packet_planning",
        "weather_bot_phase0a_closeout_inventory_revision_if_scope_too_broad",
    ]
    for value in next_values:
        assert not any(fragment in value for fragment in SELF_REVIEW_FRAGMENTS)


def test_pr_body_validation_statuses_are_recorded() -> None:
    pairs = _pairs(_read())
    for value in CLOSED_SETS["pr body validation status"]:
        assert ("pr body validation status", value) in pairs
    assert ("pr body validation status", "process_light_pr_body_blocked") in pairs
    assert ("pr body validation status", "pr_body_must_be_fixed_before_review") in pairs


def test_parser_rejects_artificial_hybrid_custom_assignment_values() -> None:
    sample = "- canonical routing field: condition_id_market_id_hybrid\n"
    sample_pairs = _pairs_from_section(sample)
    try:
        _assert_closed_sets(sample_pairs)
    except AssertionError:
        return
    raise AssertionError("hybrid/custom assignment value was accepted")


def test_required_predecessor_planning_source_areas_are_named() -> None:
    text = _read()
    for source_area in REQUIRED_SOURCE_AREAS:
        assert source_area in text
