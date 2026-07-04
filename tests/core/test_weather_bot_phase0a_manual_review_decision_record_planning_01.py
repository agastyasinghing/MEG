from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-MANUAL-REVIEW-DECISION-RECORD-PLANNING-01"
PRD = ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST = ROOT / "tests/core/test_weather_bot_phase0a_manual_review_decision_record_planning_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A manual-review decision-record assignments"
REQUIRED_TITLE = f"# {CANONICAL_ID} — Weather Bot Phase 0A Manual Review Decision Record Planning"
REQUIRED_CANONICAL = f"Canonical ID: {CANONICAL_ID}"
REQUIRED_SECTIONS = (
    "Status and scope", "Predecessor and stop condition", "Purpose", "Source-of-truth relationship",
    "Non-goals and non-approval boundaries", "Manual-review decision record planning overview",
    "Planned record field groups", "Canonical identifier representation", "Validation output packet relationship",
    "Stage 2 metadata representation", "Manual-review trigger representation", "Operator review posture representation",
    "Future decision category representation", "Decision rationale representation", "Blocker taxonomy",
    "No-lookahead and fail-closed posture", "Future handoff boundaries", "Static-test expectations",
    MACHINE_HEADING, "Embedded self-review requirement", "PR body validation requirement", "Acceptance criteria",
    "Recommended next ticket",
)
ASSIGNMENT_RE = re.compile(r"^- (?P<category>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
CLOSED_SETS = {
    "decision record field group": {
        "record_identity", "canonical_routing_identifiers", "derived_identifier_relationships",
        "non_routing_market_reference", "validation_output_packet_reference", "stage2_metadata_summary",
        "manual_review_trigger_summary", "operator_review_posture", "future_decision_category",
        "decision_rationale_summary", "blocker_summary", "no_lookahead_posture", "fail_closed_posture",
        "non_approval_summary",
    },
    "decision record lifecycle status": {
        "planning_only", "docs_static_test_only", "not_runtime_contract", "not_persisted_schema",
        "not_executable", "not_exported", "not_report_output", "not_operator_action_record",
    },
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "derived identifier field": {"token_outcome_pair"},
    "non routing field": {"market_id"},
    "validation packet relationship": {
        "validation_output_packet_planning_predecessor", "packet_not_runtime_contract", "packet_not_persisted",
        "packet_not_executable", "packet_not_exported",
    },
    "manual review trigger status": {
        "manual_review_required", "missing_required_metadata", "invalid_closed_set_value",
        "settlement_rule_interpreter_not_implemented", "no_lookahead_validation_not_implemented",
        "fail_closed_validation_not_implemented", "operator_workflow_runtime_not_implemented",
        "source_fetching_not_approved",
    },
    "operator review posture": {
        "not_implemented", "planning_only_handoff", "operator_decision_not_executed",
        "operator_decision_not_persisted", "manual_review_runtime_not_implemented", "blocked",
    },
    "future decision category": {
        "approve_for_future_manual_followup", "reject_for_missing_metadata", "reject_for_no_lookahead_uncertainty",
        "reject_for_fail_closed_uncertainty", "reject_for_identifier_issue", "reject_for_unapproved_runtime_scope",
        "defer_to_owner_decision", "blocked",
    },
    "decision rationale field": {
        "human_readable_summary", "canonical_identifier_summary", "validation_packet_summary", "blocker_summary",
        "non_approval_summary", "future_gate_required_summary",
    },
    "blocker class": {
        "missing_condition_id", "missing_token_id", "missing_outcome", "market_id_used_for_routing",
        "missing_validation_output_packet", "validation_output_packet_not_runtime_contract", "missing_stage2_metadata",
        "invalid_stage2_metadata", "settlement_rule_interpreter_not_implemented",
        "no_lookahead_validation_not_implemented", "fail_closed_validation_not_implemented",
        "manual_review_runtime_not_implemented", "operator_decision_execution_not_approved",
        "operator_decision_persistence_not_approved", "source_fetching_not_approved", "runtime_ingestion_not_approved",
        "runtime_validation_not_approved", "scoring_not_approved", "paper_trading_not_approved", "trading_not_approved",
    },
    "no lookahead posture": {"not_implemented", "planning_only", "no_lookahead_unvalidated", "manual_review_required", "blocked"},
    "fail closed posture": {"not_implemented", "planning_only", "fail_closed_unvalidated", "manual_review_required", "blocked"},
    "handoff target": {
        "manual_review_planning_packet", "operator_review_future_gate", "hold_source_fetching_runtime_track",
        "weather_bot_phase0a_hold", "owner_decision_required_for_future_runtime",
    },
    "implementation posture": {
        "no_runtime_code_change", "no_meg_modification", "no_source_fetching", "no_provider_connector",
        "no_provider_client", "no_api_call", "no_scraping", "no_file_download", "no_forecast_pull",
        "no_sdk_usage", "no_credentials_config_loading", "no_generated_data", "no_fixture_change",
        "no_schema_change", "no_db_migration", "no_runtime_ingestion", "no_runtime_loading",
        "no_runtime_validation", "no_runtime_parser_interpreter", "no_manual_review_runtime_workflow",
        "no_manual_review_ui", "no_operator_decision_execution", "no_operator_decision_persistence",
        "no_scoring_evaluation_execution", "no_backtesting", "no_paper_trading", "no_order_simulation",
        "no_trading_autonomy_production", "no_reports", "no_persistence", "no_audit_output", "no_export",
        "no_owner_decision_revision",
    },
    "recommended next track": {"weather_bot_phase0a_phase_closeout_and_runtime_approval_readiness_inventory"},
    "conditional next track": {"weather_bot_phase0a_manual_review_decision_record_revision_if_scope_too_broad"},
    "pr body validation status": {
        "required_headings_must_be_present", "exact_commands_must_be_reported",
        "embedded_self_review_summary_required", "safety_non_execution_summary_required",
        "final_merge_recommendation_required", "recommended_next_ticket_required", "process_light_pr_body_blocked",
    },
}
REQUIRED_ASSIGNMENTS = {(category, value) for category, values in CLOSED_SETS.items() for value in values} | {
    ("weather bot planning stage", "weather_bot_phase0a_manual_review_decision_record_planning"),
    ("predecessor pr", "pr_303"),
    ("predecessor artifact", "validation_output_packet_planning"),
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
    ("label confidence", "confirmed"),
}
REQUIRED_SOURCE_AREAS = (
    "validation output packet planning", "operator workflow planning", "canonical identifier static audit",
    "Stage 2 metadata contract documentation", "no-lookahead validation planning", "fail-closed validation planning",
    "settlement-rule interpreter planning",
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
    for category in CLOSED_SETS:
        actual = {value for field, value in pairs if field == category}
        assert actual == CLOSED_SETS[category], category


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


def test_predecessor_exclusion_non_approval_and_next_tracks_are_recorded() -> None:
    pairs = _pairs(_read())
    assert ("predecessor pr", "pr_303") in pairs
    assert ("predecessor artifact", "validation_output_packet_planning") in pairs
    assert ("excluded predecessor pr", "pr_283_unmerged") in pairs
    for value in CLOSED_SETS["implementation posture"]:
        assert ("implementation posture", value) in pairs
    next_values = [value for field, value in pairs if field in {"recommended next track", "conditional next track"}]
    assert next_values == [
        "weather_bot_phase0a_phase_closeout_and_runtime_approval_readiness_inventory",
        "weather_bot_phase0a_manual_review_decision_record_revision_if_scope_too_broad",
    ]
    for value in next_values:
        assert not any(fragment in value for fragment in SELF_REVIEW_FRAGMENTS)


def test_pr_body_validation_statuses_are_recorded() -> None:
    pairs = _pairs(_read())
    for value in CLOSED_SETS["pr body validation status"]:
        assert ("pr body validation status", value) in pairs
    assert ("pr body validation status", "process_light_pr_body_blocked") in pairs


def test_parser_rejects_artificial_hybrid_custom_assignment_values() -> None:
    sample = "- canonical routing field: condition_id_market_id_hybrid\n"
    sample_pairs = _pairs_from_section(sample)
    try:
        _assert_closed_sets(sample_pairs)
    except AssertionError:
        return
    raise AssertionError("hybrid/custom assignment values must be rejected")


def test_prd_names_all_required_predecessor_planning_source_areas() -> None:
    text = _read()
    for phrase in REQUIRED_SOURCE_AREAS:
        assert phrase in text


def test_machine_parser_is_section_scoped() -> None:
    synthetic = (
        f"## {MACHINE_HEADING}\n"
        "- canonical routing field: condition_id\n"
        "\n## Acceptance criteria\n"
        "- canonical routing field: market_id\n"
    )
    assert _pairs(synthetic) == [("canonical routing field", "condition_id")]
