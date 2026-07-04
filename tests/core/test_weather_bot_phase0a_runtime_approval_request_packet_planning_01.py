from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-RUNTIME-APPROVAL-REQUEST-PACKET-PLANNING-01"
PRD = ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST = ROOT / "tests/core/test_weather_bot_phase0a_runtime_approval_request_packet_planning_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A runtime-approval request assignments"
REQUIRED_TITLE = f"# {CANONICAL_ID} — Weather Bot Phase 0A Runtime Approval Request Packet Planning"
REQUIRED_CANONICAL = f"Canonical ID: {CANONICAL_ID}"
REQUIRED_SECTIONS = (
    "Status and scope", "Predecessor and stop condition", "Purpose", "Source-of-truth relationship",
    "Non-goals and non-approval boundaries", "Runtime approval request packet overview",
    "Planned request packet field groups", "Canonical identifier posture",
    "Phase 0A closeout inventory relationship", "Runtime readiness summary",
    "Non-owner runtime gate hold representation", "Explicit non-approval representation",
    "Source-fetching and provider approval posture", "Paper-trade evaluation and trading approval posture",
    "Manual-review and operator runtime posture", "Blocker taxonomy", "Future handoff boundaries",
    "Static-test expectations", MACHINE_HEADING, "Embedded self-review requirement",
    "PR body completion requirement", "Acceptance criteria", "Recommended next ticket",
)
ASSIGNMENT_RE = re.compile(r"^- (?P<category>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
CLOSED_SETS = {'request packet field group': ['blocker_summary', 'canonical_identifier_summary', 'explicit_non_approval_summary', 'future_gate_summary', 'manual_review_operator_posture', 'non_owner_gate_options', 'packet_identity', 'paper_trade_evaluation_trading_posture', 'phase0a_closeout_inventory_reference', 'pr_body_completion_summary', 'runtime_readiness_summary', 'source_fetching_provider_posture'], 'request packet lifecycle status': ['docs_static_test_only', 'not_executable', 'not_exported', 'not_persisted_schema', 'not_report_output', 'not_runtime_contract', 'paper_trade_approval_not_granted', 'planning_only', 'provider_source_approval_not_granted', 'runtime_approval_not_granted', 'source_fetching_approval_not_granted'], 'canonical routing field': ['condition_id', 'outcome', 'token_id'], 'derived identifier field': ['token_outcome_pair'], 'non routing field': ['market_id'], 'phase0a closeout relationship': ['closeout_inventory_not_runtime_contract', 'closeout_inventory_planning_only', 'closeout_inventory_runtime_approval_not_granted', 'future_runtime_gate_required', 'phase_closeout_inventory_predecessor'], 'non owner gate option': ['approve_paper_trade_planning_only', 'approve_provider_planning_only', 'approve_runtime_planning_only', 'approve_source_fetching_planning_only', 'defer_decision', 'hold_runtime_track', 'request_revision_before_decision'], 'approval posture': ['runtime_gate_required', 'paper_trade_approval_not_granted', 'production_approval_not_granted', 'provider_source_approval_not_granted', 'runtime_approval_not_granted', 'source_fetching_approval_not_granted', 'trading_approval_not_granted'], 'runtime readiness status': ['blocked', 'manual_review_runtime_not_implemented', 'not_evaluation_ready', 'not_paper_trade_ready', 'not_runtime_ready', 'operator_decision_execution_not_implemented', 'operator_decision_persistence_not_implemented', 'provider_implementation_not_approved', 'runtime_approval_not_granted', 'source_fetching_not_approved'], 'source provider posture': ['api_calls_not_implemented', 'closed_held', 'credentials_config_loading_not_implemented', 'forecast_pulls_not_implemented', 'provider_client_not_implemented', 'provider_connector_not_implemented', 'provider_implementation_not_approved', 'source_fetching_not_approved', 'source_fetching_not_implemented'], 'validation runtime posture': ['fail_closed_validation_runtime_not_implemented', 'no_lookahead_validation_runtime_not_implemented', 'runtime_ingestion_not_implemented', 'runtime_loading_not_implemented', 'runtime_parser_interpreter_not_implemented', 'runtime_validation_not_implemented', 'settlement_rule_interpreter_runtime_not_implemented'], 'trading readiness posture': ['backtesting_not_implemented', 'metric_persistence_not_implemented', 'order_simulation_not_implemented', 'paper_trading_not_implemented', 'scoring_evaluation_execution_not_implemented', 'trading_autonomy_production_not_implemented'], 'manual operator posture': ['manual_review_runtime_not_implemented', 'manual_review_ui_not_implemented', 'operator_decision_execution_not_implemented', 'operator_decision_persistence_not_implemented', 'operator_workflow_runtime_not_implemented'], 'blocker class': ['audit_output_not_approved', 'evaluation_not_approved', 'export_not_approved', 'fail_closed_validation_not_implemented', 'manual_review_runtime_not_implemented', 'no_lookahead_validation_not_implemented', 'operator_decision_execution_not_approved', 'operator_decision_persistence_not_approved', 'operator_workflow_runtime_not_implemented', 'paper_trading_not_approved', 'persistence_not_approved', 'production_not_approved', 'provider_implementation_not_approved', 'reports_not_approved', 'runtime_approval_not_granted', 'runtime_ingestion_not_approved', 'runtime_validation_not_approved', 'scoring_not_approved', 'settlement_rule_interpreter_not_implemented', 'source_fetching_not_approved', 'trading_not_approved'], 'implementation posture': ['no_api_call', 'no_audit_output', 'no_backtesting', 'no_credentials_config_loading', 'no_db_migration', 'no_export', 'no_file_download', 'no_fixture_change', 'no_forecast_pull', 'no_generated_data', 'no_manual_review_runtime_workflow', 'no_manual_review_ui', 'no_meg_modification', 'no_metric_persistence', 'no_operator_decision_execution', 'no_operator_decision_persistence', 'no_order_simulation', 'no_runtime_gate_revision', 'no_paper_trade_approval_granted', 'no_paper_trading', 'no_persistence', 'no_provider_client', 'no_provider_connector', 'no_provider_source_approval_granted', 'no_reports', 'no_runtime_approval_granted', 'no_runtime_code_change', 'no_runtime_ingestion', 'no_runtime_loading', 'no_runtime_parser_interpreter', 'no_runtime_validation', 'no_schema_change', 'no_scoring_evaluation_execution', 'no_scraping', 'no_sdk_usage', 'no_source_fetching', 'no_source_fetching_approval_granted', 'no_trading_autonomy_production'], 'recommended next track': ['weather_bot_phase0a_non_owner_runtime_gate_hold_refresh_planning'], 'conditional next track': ['weather_bot_phase0a_runtime_approval_request_packet_revision_if_scope_too_broad'], 'pr body completion status': ['changed_file_scope_audit_required', 'embedded_self_review_summary_required', 'exact_commands_must_be_reported', 'final_merge_recommendation_required', 'post_pr_creation_body_update_required', 'pr_body_must_be_fixed_before_review', 'process_light_pr_body_blocked', 'recommended_next_ticket_required', 'required_headings_must_be_present', 'return_must_confirm_pr_body_complete', 'safety_non_execution_summary_required', 'targeted_safety_audit_required']}
REQUIRED_ASSIGNMENTS = {('pr body completion status', 'targeted_safety_audit_required'), ('manual operator posture', 'manual_review_runtime_not_implemented'), ('blocker class', 'runtime_ingestion_not_approved'), ('runtime readiness status', 'runtime_approval_not_granted'), ('source provider posture', 'credentials_config_loading_not_implemented'), ('runtime readiness status', 'source_fetching_not_approved'), ('canonical routing field', 'token_id'), ('source provider posture', 'provider_connector_not_implemented'), ('implementation posture', 'no_fixture_change'), ('implementation posture', 'no_source_fetching'), ('implementation posture', 'no_paper_trade_approval_granted'), ('validation runtime posture', 'runtime_validation_not_implemented'), ('pr body completion status', 'pr_body_must_be_fixed_before_review'), ('readiness status', 'source_fetching_approval_not_granted'), ('request packet lifecycle status', 'not_runtime_contract'), ('blocker class', 'evaluation_not_approved'), ('readiness status', 'no_lookahead_validation_runtime_not_implemented'), ('trading readiness posture', 'metric_persistence_not_implemented'), ('validation runtime posture', 'runtime_parser_interpreter_not_implemented'), ('trading readiness posture', 'order_simulation_not_implemented'), ('readiness status', 'evaluation_readiness_not_achieved'), ('implementation posture', 'no_manual_review_ui'), ('implementation posture', 'no_persistence'), ('validation runtime posture', 'settlement_rule_interpreter_runtime_not_implemented'), ('implementation posture', 'no_runtime_code_change'), ('request packet field group', 'blocker_summary'), ('excluded predecessor pr', 'pr_283_unmerged'), ('source provider posture', 'provider_implementation_not_approved'), ('trading readiness posture', 'scoring_evaluation_execution_not_implemented'), ('implementation posture', 'no_credentials_config_loading'), ('readiness status', 'manual_review_runtime_not_implemented'), ('request packet field group', 'manual_review_operator_posture'), ('request packet lifecycle status', 'runtime_approval_not_granted'), ('readiness status', 'operator_workflow_runtime_not_implemented'), ('predecessor artifact', 'phase_closeout_runtime_approval_readiness_inventory'), ('implementation posture', 'no_manual_review_runtime_workflow'), ('blocker class', 'persistence_not_approved'), ('implementation posture', 'no_runtime_loading'), ('implementation posture', 'no_reports'), ('implementation posture', 'no_operator_decision_persistence'), ('implementation posture', 'no_db_migration'), ('validation runtime posture', 'fail_closed_validation_runtime_not_implemented'), ('blocker class', 'runtime_approval_not_granted'), ('implementation posture', 'no_provider_connector'), ('implementation posture', 'no_source_fetching_approval_granted'), ('runtime readiness status', 'not_runtime_ready'), ('blocker class', 'source_fetching_not_approved'), ('implementation posture', 'no_backtesting'), ('validation runtime posture', 'runtime_loading_not_implemented'), ('implementation posture', 'no_scoring_evaluation_execution'), ('implementation posture', 'no_provider_source_approval_granted'), ('blocker class', 'audit_output_not_approved'), ('request packet lifecycle status', 'not_executable'), ('manual operator posture', 'operator_workflow_runtime_not_implemented'), ('runtime readiness status', 'blocked'), ('trading readiness posture', 'paper_trading_not_implemented'), ('request packet field group', 'non_owner_gate_options'), ('blocker class', 'runtime_validation_not_approved'), ('request packet lifecycle status', 'provider_source_approval_not_granted'), ('pr body completion status', 'safety_non_execution_summary_required'), ('implementation posture', 'no_runtime_validation'), ('non owner gate option', 'approve_source_fetching_planning_only'), ('pr body completion status', 'embedded_self_review_summary_required'), ('blocker class', 'fail_closed_validation_not_implemented'), ('canonical routing field', 'outcome'), ('runtime readiness status', 'manual_review_runtime_not_implemented'), ('readiness status', 'fail_closed_validation_runtime_not_implemented'), ('source provider posture', 'forecast_pulls_not_implemented'), ('implementation posture', 'no_trading_autonomy_production'), ('blocker class', 'no_lookahead_validation_not_implemented'), ('trading readiness posture', 'trading_autonomy_production_not_implemented'), ('runtime readiness status', 'provider_implementation_not_approved'), ('readiness status', 'operator_decision_persistence_not_implemented'), ('blocker class', 'production_not_approved'), ('phase0a closeout relationship', 'future_runtime_gate_required'), ('runtime readiness status', 'not_paper_trade_ready'), ('request packet field group', 'source_fetching_provider_posture'), ('implementation posture', 'no_order_simulation'), ('pr body completion status', 'post_pr_creation_body_update_required'), ('request packet lifecycle status', 'paper_trade_approval_not_granted'), ('validation runtime posture', 'runtime_ingestion_not_implemented'), ('approval posture', 'paper_trade_approval_not_granted'), ('request packet lifecycle status', 'source_fetching_approval_not_granted'), ('non owner gate option', 'request_revision_before_decision'), ('blocker class', 'paper_trading_not_approved'), ('source fetching track posture', 'implementation_approval_not_granted'), ('approval posture', 'source_fetching_approval_not_granted'), ('implementation posture', 'no_metric_persistence'), ('source fetching track posture', 'source_fetching_not_implemented'), ('implementation posture', 'no_api_call'), ('source fetching track posture', 'closed_held'), ('approval posture', 'runtime_approval_not_granted'), ('manual operator posture', 'operator_decision_persistence_not_implemented'), ('phase0a closeout relationship', 'phase_closeout_inventory_predecessor'), ('implementation posture', 'no_runtime_parser_interpreter'), ('pr body completion status', 'required_headings_must_be_present'), ('implementation posture', 'no_file_download'), ('readiness status', 'settlement_rule_interpreter_runtime_not_implemented'), ('non owner gate option', 'hold_runtime_track'), ('implementation posture', 'no_audit_output'), ('readiness status', 'paper_trade_readiness_not_achieved'), ('canonical routing field', 'condition_id'), ('phase0a closeout relationship', 'closeout_inventory_runtime_approval_not_granted'), ('implementation posture', 'no_generated_data'), ('blocker class', 'scoring_not_approved'), ('source provider posture', 'source_fetching_not_implemented'), ('source provider posture', 'closed_held'), ('blocker class', 'reports_not_approved'), ('approval posture', 'trading_approval_not_granted'), ('runtime readiness status', 'operator_decision_persistence_not_implemented'), ('recommended next track', 'weather_bot_phase0a_non_owner_runtime_gate_hold_refresh_planning'), ('request packet field group', 'pr_body_completion_summary'), ('implementation posture', 'no_forecast_pull'), ('readiness status', 'operator_decision_execution_not_implemented'), ('non owner gate option', 'defer_decision'), ('source provider posture', 'provider_client_not_implemented'), ('approval posture', 'provider_source_approval_not_granted'), ('phase0a closeout relationship', 'closeout_inventory_not_runtime_contract'), ('runtime readiness status', 'not_evaluation_ready'), ('approval posture', 'production_approval_not_granted'), ('blocker class', 'manual_review_runtime_not_implemented'), ('weather bot scope', 'market_settlement_rule_not_generic_weather'), ('label confidence', 'confirmed'), ('request packet lifecycle status', 'not_persisted_schema'), ('pr body completion status', 'final_merge_recommendation_required'), ('pr body completion status', 'recommended_next_ticket_required'), ('request packet field group', 'paper_trade_evaluation_trading_posture'), ('request packet field group', 'phase0a_closeout_inventory_reference'), ('blocker class', 'operator_workflow_runtime_not_implemented'), ('blocker class', 'operator_decision_persistence_not_approved'), ('blocker class', 'trading_not_approved'), ('manual operator posture', 'manual_review_ui_not_implemented'), ('blocker class', 'export_not_approved'), ('request packet field group', 'packet_identity'), ('implementation posture', 'no_meg_modification'), ('non owner gate option', 'approve_paper_trade_planning_only'), ('manual operator posture', 'operator_decision_execution_not_implemented'), ('implementation posture', 'no_runtime_gate_revision'), ('source provider posture', 'api_calls_not_implemented'), ('predecessor pr', 'pr_305'), ('pr body completion status', 'return_must_confirm_pr_body_complete'), ('implementation posture', 'no_paper_trading'), ('request packet field group', 'explicit_non_approval_summary'), ('request packet lifecycle status', 'not_report_output'), ('implementation posture', 'no_runtime_approval_granted'), ('pr body completion status', 'exact_commands_must_be_reported'), ('trading readiness posture', 'backtesting_not_implemented'), ('non owner gate option', 'approve_provider_planning_only'), ('readiness status', 'paper_trade_approval_not_granted'), ('request packet field group', 'future_gate_summary'), ('request packet field group', 'runtime_readiness_summary'), ('implementation posture', 'no_provider_client'), ('request packet field group', 'canonical_identifier_summary'), ('source provider posture', 'source_fetching_not_approved'), ('implementation posture', 'no_sdk_usage'), ('pr body completion status', 'changed_file_scope_audit_required'), ('readiness status', 'runtime_approval_not_granted'), ('weather bot planning stage', 'weather_bot_phase0a_runtime_approval_request_packet_planning'), ('runtime readiness status', 'operator_decision_execution_not_implemented'), ('approval posture', 'runtime_gate_required'), ('blocker class', 'settlement_rule_interpreter_not_implemented'), ('pr body completion status', 'process_light_pr_body_blocked'), ('non routing field', 'market_id'), ('blocker class', 'operator_decision_execution_not_approved'), ('derived identifier field', 'token_outcome_pair'), ('phase0a closeout relationship', 'closeout_inventory_planning_only'), ('conditional next track', 'weather_bot_phase0a_runtime_approval_request_packet_revision_if_scope_too_broad'), ('implementation posture', 'no_scraping'), ('implementation posture', 'no_operator_decision_execution'), ('blocker class', 'provider_implementation_not_approved'), ('request packet lifecycle status', 'docs_static_test_only'), ('readiness status', 'provider_source_approval_not_granted'), ('validation runtime posture', 'no_lookahead_validation_runtime_not_implemented'), ('implementation posture', 'no_runtime_ingestion'), ('non owner gate option', 'approve_runtime_planning_only'), ('request packet lifecycle status', 'planning_only'), ('implementation posture', 'no_export'), ('implementation posture', 'no_schema_change'), ('request packet lifecycle status', 'not_exported')}
REQUIRED_SOURCE_AREAS = (
    "phase closeout runtime approval readiness inventory",
    "manual-review decision record planning",
    "validation output packet planning",
    "operator workflow planning",
    "canonical identifier static audit",
    "Stage 2 metadata contract documentation",
    "no-lookahead validation planning",
    "fail-closed validation planning",
    "settlement-rule interpreter planning",
    "supplied market contract input planning",
    "evaluation metrics planning",
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
        assert actual == set(allowed), category


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


def test_predecessor_exclusion_non_approvals_and_next_tracks_are_recorded() -> None:
    pairs = _pairs(_read())
    assert ("predecessor pr", "pr_305") in pairs
    assert ("predecessor artifact", "phase_closeout_runtime_approval_readiness_inventory") in pairs
    assert ("excluded predecessor pr", "pr_283_unmerged") in pairs
    for value in (
        "runtime_approval_not_granted",
        "source_fetching_approval_not_granted",
        "provider_source_approval_not_granted",
        "paper_trade_approval_not_granted",
    ):
        assert ("approval posture", value) in pairs
        assert ("request packet lifecycle status", value) in pairs
    gate_options = {value for field, value in pairs if field == "non owner gate option"}
    assert gate_options == set(CLOSED_SETS["non owner gate option"])
    assert not any("implementation" in value or "execute" in value for value in gate_options)
    for value in CLOSED_SETS["implementation posture"]:
        assert ("implementation posture", value) in pairs
    next_values = [value for field, value in pairs if field in {"recommended next track", "conditional next track"}]
    assert next_values == [
        "weather_bot_phase0a_non_owner_runtime_gate_hold_refresh_planning",
        "weather_bot_phase0a_runtime_approval_request_packet_revision_if_scope_too_broad",
    ]
    for value in next_values:
        assert not any(fragment in value for fragment in SELF_REVIEW_FRAGMENTS)


def test_pr_body_completion_statuses_are_recorded() -> None:
    pairs = _pairs(_read())
    for value in CLOSED_SETS["pr body completion status"]:
        assert ("pr body completion status", value) in pairs
    for value in (
        "process_light_pr_body_blocked",
        "pr_body_must_be_fixed_before_review",
        "post_pr_creation_body_update_required",
        "return_must_confirm_pr_body_complete",
    ):
        assert ("pr body completion status", value) in pairs


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
