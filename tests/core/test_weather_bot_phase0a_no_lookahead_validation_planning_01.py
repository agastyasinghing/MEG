"""Static checks for Weather Bot Phase 0A no-lookahead validation planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-VALIDATION-PLANNING-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_no_lookahead_validation_planning_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A no-lookahead-validation-planning assignments"
NEXT_TRACK = "weather_bot_phase0a_fail_closed_validation_planning"
CONDITIONAL_TRACK = "weather_bot_phase0a_no_lookahead_validation_revision_if_scope_too_broad"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to settlement-rule interpreter planning", "No-lookahead validation planning objective",
    "Current held/closed source-fetching posture", "No owner-decision revision boundary", "No-lookahead validation readiness status",
    "Validation overview", "Timestamp input fields", "Evidence-time comparison categories", "Validation status labels",
    "Validation blocker categories", "Manual-review handoff labels", "Fail-closed handoff labels",
    "Settlement-rule interpreter relationship", "Stage 2 metadata relationship", "Static planning only boundary",
    "Canonical identifier posture", "Source-fetching track remains blocked", "Provider/source execution boundary",
    "Credential/config boundary", "Generated-data and fixture boundary", "Runtime validation boundary",
    "Runtime parser/classifier boundary", "Runtime ingestion and schema boundary", "Scoring/evaluation boundary",
    "Backtesting boundary", "Paper-trade boundary", "Operator workflow execution boundary",
    "Trading/autonomy/production boundary", "Audit report and export boundary", "Stage 2 runtime metadata posture",
    "Embedded self-review requirement", "Recommended next ticket", MACHINE_HEADING, "Acceptance criteria",
)
READINESS = set("""not_no_lookahead_validation_ready docs_static_no_lookahead_validation_planning_only runtime_no_lookahead_validation_not_implemented runtime_timestamp_validation_not_implemented runtime_evidence_time_comparison_not_implemented validation_output_persistence_not_approved source_fetching_not_implemented paper_trade_execution_not_approved""".split())
TIMESTAMPS = set("""decision_time evidence_available_time evidence_observed_time forecast_issue_time observation_valid_time resolution_time settlement_time market_close_time market_resolution_source_time operator_review_time latest_allowed_information_time""".split())
COMPARISONS = set("""comparison_not_available comparison_evidence_before_decision comparison_evidence_at_decision comparison_evidence_after_decision comparison_forecast_issue_after_decision comparison_observation_valid_after_decision comparison_resolution_after_decision comparison_settlement_after_decision comparison_source_time_conflict comparison_timestamp_missing comparison_timestamp_ambiguous""".split())
STATUSES = set("""validation_status_not_available validation_status_static_planning_only validation_status_requires_manual_review validation_status_pass_candidate validation_status_block_lookahead_detected validation_status_block_timestamp_missing validation_status_block_timestamp_ambiguous validation_status_block_source_time_conflict validation_status_block_scope_violation""".split())
BLOCKERS = set("""block_runtime_no_lookahead_validation_missing block_runtime_timestamp_validation_missing block_runtime_evidence_time_comparison_missing block_validation_output_persistence_unapproved block_source_fetching_unapproved block_provider_execution_unapproved block_generated_fixture_data_unapproved block_operator_workflow_runtime_missing block_scoring_evaluation_unapproved block_backtesting_unapproved block_paper_trade_execution_not_approved block_trading_autonomy_production_not_approved block_audit_persistence_export_not_approved""".split())
MANUAL = set("""handoff_manual_review_required handoff_timestamp_check_required handoff_decision_time_check_required handoff_evidence_available_time_check_required handoff_forecast_issue_time_check_required handoff_observation_valid_time_check_required handoff_resolution_time_check_required handoff_source_time_conflict_check_required""".split())
FAIL = set("""handoff_fail_closed_lookahead_detected handoff_fail_closed_timestamp_missing handoff_fail_closed_timestamp_ambiguous handoff_fail_closed_source_time_conflict handoff_fail_closed_validation_unavailable handoff_fail_closed_scope_violation""".split())
STAGE2_PATHS = set("""meg/weather/stage2/source_identity_runtime.py meg/weather/stage2/retrieval_context_runtime.py meg/weather/stage2/provider_source_family_runtime.py meg/weather/stage2/manual_review_gate_runtime.py meg/weather/stage2/no_lookahead_metadata_runtime.py meg/weather/stage2/fail_closed_validation_runtime.py meg/weather/stage2/static_audit_surface_runtime.py""".split())
STAGE2_ASSIGNMENTS = set("""source_identity_runtime_py retrieval_context_runtime_py provider_source_family_runtime_py manual_review_gate_runtime_py no_lookahead_metadata_runtime_py fail_closed_validation_runtime_py static_audit_surface_runtime_py""".split())
BLOCKED_WORK = set("""owner_decision_revision source_fetching_runtime_implementation_plan source_fetching_implementation provider_connector_implementation provider_client_creation live_provider_source_fetching forecast_pull_execution api_call_execution scraping_execution file_download_execution provider_sdk_execution credentials_config_loading generated_data_creation fixture_data_modification schema_change db_migration runtime_market_contract_ingestion runtime_supplied_input_loading runtime_supplied_input_validation supplied_input_persistence runtime_settlement_rule_parser runtime_settlement_rule_classifier runtime_settlement_rule_interpreter interpreter_output_persistence runtime_no_lookahead_validation runtime_timestamp_validation runtime_evidence_time_comparison validation_output_persistence runtime_metadata_implementation stage2_runtime_module_modification fail_closed_runtime_enforcement runtime_error_handling manual_review_runtime_workflow manual_review_ui manual_review_persistence operator_decision_execution operator_decision_persistence scoring_implementation evaluation_execution metric_persistence backtesting_implementation paper_trade_execution paper_trade_readiness_runtime order_simulation runtime_trading_behavior order_placement autonomy_behavior production_behavior audit_report_generation audit_output_persistence external_export_behavior standalone_self_review_prd_artifact""".split())
IMPLEMENTATION_POSTURES = set("""docs_static_test_only no_lookahead_validation_planning_only no_runtime_code_change no_stage2_runtime_module_modification no_runtime_metadata_implementation no_owner_decision_revision no_source_fetching no_source_fetching_plan no_provider_connector no_provider_client no_live_provider_fetching no_credential_config_loading no_generated_data no_fixture_change no_schema_change no_db_migration no_runtime_market_contract_ingestion no_runtime_supplied_input_loading no_runtime_supplied_input_validation no_supplied_input_persistence no_runtime_settlement_rule_parser no_runtime_settlement_rule_classifier no_runtime_settlement_rule_interpreter no_interpreter_output_persistence no_runtime_no_lookahead_validation no_runtime_timestamp_validation no_runtime_evidence_time_comparison no_validation_output_persistence no_fail_closed_runtime_enforcement no_runtime_error_handling no_manual_review_runtime_workflow no_manual_review_ui no_manual_review_persistence no_operator_decision_execution no_operator_decision_persistence no_scoring_implementation no_evaluation_execution no_metric_persistence no_backtesting_implementation no_paper_trade_execution no_order_simulation no_trading_autonomy_production no_report_writing no_external_export no_persistence""".split())
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_phase0a_no_lookahead_validation_planning"},
    "no lookahead validation status": {"docs_static_test_only", "no_lookahead_validation_planning_only", "post_weather_bot_phase0a_settlement_rule_interpreter_planning"},
    "no lookahead validation readiness status": READINESS,
    "self review posture": {"embedded_secondary_prompt_only", "no_standalone_self_review_prd"},
    "owner decision posture": {"no_owner_decision_revision", "hold_source_fetching_runtime_track_preserved"},
    "source fetching track posture": {"closed_held", "no_source_fetching_implementation_plan", "no_source_fetching_implementation", "implementation_approval_not_granted"},
    "timestamp input field": TIMESTAMPS, "evidence time comparison category": COMPARISONS,
    "validation status label": STATUSES, "validation blocker category": BLOCKERS,
    "manual review handoff label": MANUAL, "fail closed handoff label": FAIL,
    "stage2 metadata artifact": STAGE2_ASSIGNMENTS,
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "identifier relationship": {"token_outcome_pair_derived_relationship", "condition_token_outcome_preserved", "token_id_outcome_relationship_preserved"},
    "fail closed canonical guard": {"market_identifier_routing_attempt"},
    "blocked work": BLOCKED_WORK, "implementation posture": IMPLEMENTATION_POSTURES,
    "recommended next track": {NEXT_TRACK}, "conditional next track": {CONDITIONAL_TRACK},
    "evidence status": {"no_lookahead_validation_planning_recorded"}, "label confidence": {"confirmed"},
}
REQUIRED_ASSIGNMENTS = {(field, value) for field, values in ALLOWED_ASSIGNMENTS.items() for value in values}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
FORBIDDEN_APPROVAL_TERMS = (
    ("revised", "owner", "decision"),
    ("approve_narrow_source_fetching", "_runtime_implementation_plan"),
    ("source", "fetching", "is", "approved"),
    ("source", "fetching", "implementation", "is", "approved"),
    ("source", "fetching", "implementation", "planning", "is", "approved"),
    ("provider", "connector", "is", "approved"),
    ("provider", "client", "is", "created"),
    ("live", "provider", "source", "fetching", "is", "approved"),
    ("forecast", "pull", "is", "approved"),
    ("api", "call", "is", "approved"),
    ("scraping", "is", "approved"),
    ("file", "download", "is", "approved"),
    ("provider", "sdk", "is", "approved"),
    ("credentials", ".*loading", "is", "approved"),
    ("generated", "data", "is", "approved"),
    ("fixture", "change", "is", "approved"),
    ("schema", "change", "is", "approved"),
    ("db", "migration", "is", "approved"),
    ("market-contract", "ingestion", "is", "approved"),
    ("supplied-input", "loading", "is", "approved"),
    ("supplied-input", "validation", "is", "approved"),
    ("supplied", "input", "persistence", "is", "approved"),
    ("settlement-rule", "parser", "is", "approved"),
    ("settlement-rule", "classifier", "is", "approved"),
    ("settlement-rule", "interpreter", "is", "approved"),
    ("interpreter", "output", "persistence", "is", "approved"),
    ("no-lookahead", "validation", "is", "approved"),
    ("timestamp", "validation", "is", "approved"),
    ("evidence-time", "comparison", "is", "approved"),
    ("validation", "output", "persistence", "is", "approved"),
    ("runtime", "metadata", "implementation", "is", "approved"),
    ("stage2", "runtime", "module", "modification", "is", "approved"),
    ("fail-closed", "enforcement", "is", "approved"),
    ("runtime", "error", "handling", "is", "approved"),
    ("manual", "review", "workflow", "is", "approved"),
    ("manual", "review", "ui", "is", "approved"),
    ("manual", "review", "persistence", "is", "approved"),
    ("operator", "decision", "execution", "is", "approved"),
    ("operator", "decision", "persistence", "is", "approved"),
    ("scoring", "is", "approved"),
    ("evaluation", "execution", "is", "approved"),
    ("metric", "persistence", "is", "approved"),
    ("backtesting", "is", "approved"),
    ("paper", "trade", "execution", "is", "approved"),
    ("order", "simulation", "is", "approved"),
    ("trading", "is", "approved"),
    ("order", "placement", "is", "approved"),
    ("autonomy", "is", "approved"),
    ("production", "behavior", "is", "approved"),
    ("report", "writing", "is", "approved"),
    ("external", "export", "is", "approved"),
    ("persistence", "is", "approved"),
    ("silence", "is", "approval"),
    ("continuation", "is", "approval"),
    ("non-interference", "is", "approval"),
)
FORBIDDEN_APPROVAL_RE = re.compile(
    "|".join(r"\s+".join(parts) for parts in FORBIDDEN_APPROVAL_TERMS),
    re.IGNORECASE,
)

def _read() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, heading
    assert match.group("section").strip(), heading
    return match.group("section")


def _assignment_pairs(text: str) -> set[tuple[str, str]]:
    return {(m.group("field"), m.group("value")) for m in ASSIGNMENT_RE.finditer(_section(text, MACHINE_HEADING))}


def test_document_exists_canonical_id_and_sections_are_non_empty() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert text.startswith(f"# {CANONICAL_ID} — Weather Bot Phase 0A No-Lookahead Validation Planning")
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
        "docs/static-test-only/no-lookahead-validation-planning-only", "This ticket does not modify `meg/`",
        "This ticket does not modify meta/handoff files", "does not modify Stage 2 runtime metadata modules",
        "does not revise the owner decision", "does not reopen source-fetching implementation planning",
        "does not fetch, create, or modify market data", "does not create fixtures or generated data",
        "does not create or modify schemas", "does not implement runtime market-contract ingestion",
        "does not implement runtime supplied-input loading", "does not implement runtime supplied-input validation",
        "does not persist supplied input", "does not implement runtime no-lookahead validation",
        "does not implement runtime timestamp validation", "does not implement runtime evidence-time comparison",
        "does not persist validation output", "does not implement runtime settlement-rule parsing",
        "does not implement runtime settlement-rule classification", "does not implement runtime settlement-rule interpretation",
        "does not persist interpreter output", "does not implement runtime metadata behavior",
        "does not implement runtime fail-closed enforcement", "does not implement runtime error handling",
        "does not implement runtime manual-review workflow behavior", "does not implement operator decision execution",
        "does not implement manual-review UI or persistence", "does not implement scoring, evaluation execution, backtesting, paper trading, trading, or autonomy",
        "does not execute paper trades", "does not create simulated orders", "persisted validation output",
        "does not create a separate standalone self-review artifact", "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work", "source-fetching runtime track remains closed/held",
        "closed owner decision remains `hold_source_fetching_runtime_track`", "Source fetching remains not implemented",
        "Implementation approval remains not granted", "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
        "Supplied market-contract input runtime behavior remains not implemented", "Settlement-rule interpreter runtime behavior remains not implemented",
        "No-lookahead validation runtime behavior remains not implemented", "Operator workflow runtime behavior remains not implemented",
        "Paper-trade readiness remains not achieved", "Evaluation readiness remains not achieved", "Provider connectors remain not approved",
        "Provider clients remain not created", "Live provider/source fetching remains not approved", "Credentials/config loading remains not approved",
        "Generated data and fixtures remain not approved", "Scoring/evaluation execution remains not approved", "Backtesting remains not approved",
        "Paper-trade execution remains not approved", "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, metric persistence, supplied-input persistence, interpreter-output persistence, validation-output persistence, operator-decision persistence, and external export remain not approved",
        "Silence, continuation, lack of objection, and non-interference are not approval",
    ]
    for phrase in required:
        assert phrase in text
    assert not any(FORBIDDEN_APPROVAL_RE.search(line) for line in text.splitlines())


def test_values_paths_blocked_work_and_readiness_appear() -> None:
    text = _read()
    for value in READINESS | TIMESTAMPS | COMPARISONS | STATUSES | BLOCKERS | MANUAL | FAIL | STAGE2_PATHS | BLOCKED_WORK:
        assert value in text
    section = _section(text, "No-lookahead validation readiness status")
    for status in READINESS:
        assert f"`{status}`" in section


def test_canonical_identifier_posture_is_preserved() -> None:
    section = _section(_read(), "Canonical identifier posture")
    assert "Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`" in section
    assert "Future reasoning must preserve all three canonical shared-rail identifiers" in section
    assert "Future reasoning must preserve the relationship between `token_id` and `outcome`" in section
    assert "`token_outcome_pair` remains a derived relationship, not a replacement for canonical fields" in section
    assert "`market_id` remains explicitly non-routing only" in section
    assert "No routing on `market_id` is introduced or approved" in section
    assert "`market_identifier_routing_attempt` remains fail-closed" in section
    pairs = _assignment_pairs(_read())
    assert {value for field, value in pairs if field == "canonical routing field"} == {"condition_id", "token_id", "outcome"}


def test_planning_boundaries_and_next_tracks_are_present() -> None:
    text = _read()
    required_phrases = [
        "Provider/source execution remains not approved", "Credentials/config loading remains not approved",
        "Generated data and fixture changes remain not approved", "Schema change and DB migration remain not approved",
        "Runtime market-contract ingestion, supplied-input loading, supplied-input validation, and supplied-input persistence remain not approved",
        "Runtime settlement-rule parser, runtime settlement-rule classifier, runtime settlement-rule interpreter, and interpreter-output persistence remain not approved",
        "Runtime no-lookahead validation, runtime timestamp validation, runtime evidence-time comparison, and validation-output persistence remain not approved",
        "runtime metadata behavior", "Operator decision execution and persistence remain not approved",
        "Manual-review UI and persistence remain not approved", "Metric persistence remains not approved",
        "Report writing, persistence, and external export remain not approved", f"Recommended next ticket: `{NEXT_TRACK}`",
        "Do not recommend a standalone self-review ticket as the next ticket",
    ]
    for phrase in required_phrases:
        assert phrase in text
    pairs = _assignment_pairs(text)
    assert ("recommended next track", NEXT_TRACK) in pairs
    assert {value for field, value in pairs if field == "conditional next track"} == {CONDITIONAL_TRACK}
    assert "standalone_self_review" not in NEXT_TRACK


def test_machine_checkable_assignments_are_section_scoped_complete_and_closed_set() -> None:
    pairs = _assignment_pairs(_read())
    assert REQUIRED_ASSIGNMENTS <= pairs
    assert pairs == REQUIRED_ASSIGNMENTS
    for field, value in pairs:
        assert field in ALLOWED_ASSIGNMENTS
        assert value in ALLOWED_ASSIGNMENTS[field]


def test_machine_checkable_parser_ignores_assignments_after_next_heading() -> None:
    synthetic = f"## {MACHINE_HEADING}\n- label confidence: confirmed\n\n## Acceptance criteria\n- label confidence: invalid_after_heading\n"
    assert _assignment_pairs(synthetic) == {("label confidence", "confirmed")}
