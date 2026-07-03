"""Static checks for Weather Bot Phase 0A settlement-rule interpreter planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-INTERPRETER-PLANNING-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_settlement_rule_interpreter_planning_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A settlement-rule-interpreter-planning assignments"
NEXT_TRACK = "weather_bot_phase0a_no_lookahead_validation_planning"
CONDITIONAL_TRACK = "weather_bot_phase0a_settlement_rule_interpreter_revision_if_scope_too_broad"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to supplied market-contract input planning", "Interpreter planning objective",
    "Current held/closed source-fetching posture", "No owner-decision revision boundary",
    "Settlement-rule interpreter readiness status", "Interpreter overview", "Interpreter input fields",
    "Interpreter output categories", "Measurement extraction planning categories",
    "Threshold and comparator planning categories", "Time-window planning categories", "Location planning categories",
    "Resolution-source planning categories", "Outcome mapping planning categories", "Ambiguity planning categories",
    "Manual-review handoff labels", "Fail-closed handoff labels", "No-lookahead relationship",
    "Stage 2 metadata relationship", "Interpreter readiness blockers", "Static planning only boundary",
    "Canonical identifier posture", "Source-fetching track remains blocked", "Provider/source execution boundary",
    "Credential/config boundary", "Generated-data and fixture boundary", "Runtime parser/classifier boundary",
    "Runtime ingestion and schema boundary", "Scoring/evaluation boundary", "Backtesting boundary", "Paper-trade boundary",
    "Operator workflow execution boundary", "Trading/autonomy/production boundary", "Audit report and export boundary",
    "Stage 2 runtime metadata posture", "Embedded self-review requirement", "Recommended next ticket", MACHINE_HEADING,
    "Acceptance criteria",
)
READINESS = {
    "not_interpreter_ready", "docs_static_interpreter_planning_only",
    "runtime_settlement_rule_parser_not_implemented", "runtime_settlement_rule_classifier_not_implemented",
    "runtime_settlement_rule_interpreter_not_implemented", "interpreter_output_persistence_not_approved",
    "source_fetching_not_implemented", "paper_trade_execution_not_approved",
}
INPUTS = {"condition_id", "token_id", "outcome", "question_text", "settlement_rule_text", "resolution_source_text", "outcome_label", "token_outcome_pair", "open_time", "close_time", "resolution_time", "event_start_time", "event_end_time", "operator_review_required", "manual_review_reason"}
OUTPUTS = {"interpreter_output_not_available", "interpreter_output_static_summary", "interpreter_output_requires_manual_review", "interpreter_output_requires_no_lookahead_review", "interpreter_output_requires_fail_closed", "interpreter_output_unsupported_measurement", "interpreter_output_ambiguous_rule", "interpreter_output_scope_revision_required"}
MEASUREMENTS = {"measurement_temperature", "measurement_precipitation", "measurement_snowfall", "measurement_rainfall", "measurement_wind_speed", "measurement_hurricane_category", "measurement_air_quality_index", "measurement_weather_alert_presence", "measurement_other_requires_review"}
THRESHOLDS = {"threshold_missing", "threshold_present", "threshold_ambiguous", "comparator_greater_than", "comparator_greater_than_or_equal", "comparator_less_than", "comparator_less_than_or_equal", "comparator_equal_to", "comparator_within_range", "comparator_presence_absence", "comparator_ambiguous_requires_review"}
TIME_WINDOWS = {"time_window_missing", "time_window_present", "time_window_ambiguous", "time_window_conflicts_with_market_close", "time_window_requires_no_lookahead_review"}
LOCATIONS = {"location_missing", "location_present", "location_ambiguous", "location_requires_manual_review"}
RESOLUTION_SOURCES = {"resolution_source_missing", "resolution_source_present", "resolution_source_ambiguous", "resolution_source_conflicting", "resolution_source_requires_future_source_fetching_approval"}
OUTCOME_MAPPINGS = {"outcome_mapping_preserved", "outcome_mapping_missing", "outcome_mapping_ambiguous", "outcome_mapping_token_outcome_mismatch", "outcome_mapping_requires_manual_review"}
AMBIGUITIES = {"ambiguity_missing_required_text", "ambiguity_conflicting_question_and_rule", "ambiguity_unsupported_measurement", "ambiguity_missing_threshold", "ambiguity_ambiguous_comparator", "ambiguity_ambiguous_time_window", "ambiguity_ambiguous_location", "ambiguity_conflicting_resolution_source", "ambiguity_identifier_mismatch", "ambiguity_requires_scope_revision"}
MANUAL_LABELS = {"handoff_manual_review_required", "handoff_operator_check_required", "handoff_identifier_check_required", "handoff_settlement_text_check_required", "handoff_resolution_source_check_required", "handoff_time_window_check_required", "handoff_location_check_required", "handoff_outcome_mapping_check_required"}
FAIL_LABELS = {"handoff_fail_closed_missing_required_field", "handoff_fail_closed_identifier_mismatch", "handoff_fail_closed_ambiguous_rule", "handoff_fail_closed_unsupported_measurement", "handoff_fail_closed_lookahead_uncertainty", "handoff_fail_closed_source_unapproved", "handoff_fail_closed_scope_violation"}
STAGE2_PATHS = {"meg/weather/stage2/source_identity_runtime.py", "meg/weather/stage2/retrieval_context_runtime.py", "meg/weather/stage2/provider_source_family_runtime.py", "meg/weather/stage2/manual_review_gate_runtime.py", "meg/weather/stage2/no_lookahead_metadata_runtime.py", "meg/weather/stage2/fail_closed_validation_runtime.py", "meg/weather/stage2/static_audit_surface_runtime.py"}
STAGE2_ASSIGNMENTS = {"source_identity_runtime_py", "retrieval_context_runtime_py", "provider_source_family_runtime_py", "manual_review_gate_runtime_py", "no_lookahead_metadata_runtime_py", "fail_closed_validation_runtime_py", "static_audit_surface_runtime_py"}
BLOCKED_WORK = set("""owner_decision_revision source_fetching_runtime_implementation_plan source_fetching_implementation provider_connector_implementation provider_client_creation live_provider_source_fetching forecast_pull_execution api_call_execution scraping_execution file_download_execution provider_sdk_execution credentials_config_loading generated_data_creation fixture_data_modification schema_change db_migration runtime_market_contract_ingestion runtime_supplied_input_loading runtime_supplied_input_validation supplied_input_persistence runtime_settlement_rule_parser runtime_settlement_rule_classifier runtime_settlement_rule_interpreter interpreter_output_persistence runtime_metadata_implementation stage2_runtime_module_modification fail_closed_runtime_enforcement runtime_error_handling no_lookahead_runtime_enforcement timestamp_runtime_validation manual_review_runtime_workflow manual_review_ui manual_review_persistence operator_decision_execution operator_decision_persistence scoring_implementation evaluation_execution metric_persistence backtesting_implementation paper_trade_execution paper_trade_readiness_runtime order_simulation runtime_trading_behavior order_placement autonomy_behavior production_behavior audit_report_generation audit_output_persistence external_export_behavior standalone_self_review_prd_artifact""".split())
IMPLEMENTATION_POSTURES = set("""docs_static_test_only settlement_rule_interpreter_planning_only no_runtime_code_change no_stage2_runtime_module_modification no_runtime_metadata_implementation no_owner_decision_revision no_source_fetching no_source_fetching_plan no_provider_connector no_provider_client no_live_provider_fetching no_credential_config_loading no_generated_data no_fixture_change no_schema_change no_db_migration no_runtime_market_contract_ingestion no_runtime_supplied_input_loading no_runtime_supplied_input_validation no_supplied_input_persistence no_runtime_settlement_rule_parser no_runtime_settlement_rule_classifier no_runtime_settlement_rule_interpreter no_interpreter_output_persistence no_fail_closed_runtime_enforcement no_runtime_error_handling no_no_lookahead_runtime_enforcement no_timestamp_runtime_validation no_manual_review_runtime_workflow no_manual_review_ui no_manual_review_persistence no_operator_decision_execution no_operator_decision_persistence no_scoring_implementation no_evaluation_execution no_metric_persistence no_backtesting_implementation no_paper_trade_execution no_order_simulation no_trading_autonomy_production no_report_writing no_external_export no_persistence""".split())
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_phase0a_settlement_rule_interpreter_planning"},
    "settlement rule interpreter status": {"docs_static_test_only", "settlement_rule_interpreter_planning_only", "post_weather_bot_phase0a_supplied_market_contract_input_planning"},
    "settlement rule interpreter readiness status": READINESS,
    "self review posture": {"embedded_secondary_prompt_only", "no_standalone_self_review_prd"},
    "owner decision posture": {"no_owner_decision_revision", "hold_source_fetching_runtime_track_preserved"},
    "source fetching track posture": {"closed_held", "no_source_fetching_implementation_plan", "no_source_fetching_implementation", "implementation_approval_not_granted"},
    "interpreter input field": INPUTS,
    "interpreter output category": OUTPUTS,
    "measurement planning category": MEASUREMENTS,
    "threshold comparator category": THRESHOLDS,
    "time window planning category": TIME_WINDOWS,
    "location planning category": LOCATIONS,
    "resolution source planning category": RESOLUTION_SOURCES,
    "outcome mapping planning category": OUTCOME_MAPPINGS,
    "ambiguity planning category": AMBIGUITIES,
    "manual review handoff label": MANUAL_LABELS,
    "fail closed handoff label": FAIL_LABELS,
    "stage2 metadata artifact": STAGE2_ASSIGNMENTS,
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "identifier relationship": {"token_outcome_pair_derived_relationship", "condition_token_outcome_preserved", "token_id_outcome_relationship_preserved"},
    "fail closed canonical guard": {"market_identifier_routing_attempt"},
    "blocked work": BLOCKED_WORK,
    "implementation posture": IMPLEMENTATION_POSTURES,
    "recommended next track": {NEXT_TRACK},
    "conditional next track": {CONDITIONAL_TRACK},
    "evidence status": {"settlement_rule_interpreter_planning_recorded"},
    "label confidence": {"confirmed"},
}
REQUIRED_ASSIGNMENTS = {(field, value) for field, values in ALLOWED_ASSIGNMENTS.items() for value in values}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
FORBIDDEN_APPROVAL_TERMS = (
    ("revised", "owner", "decision"),
    ("approve_narrow_source_fetching", "_runtime_implementation_plan"),
    ("source", "fetching", "is", "approved"),
    ("provider", "connector", "is", "approved"),
    ("settlement-rule", "interpreter", "is", "approved"),
    ("settlement", "rule", "interpreter", "is", "approved"),
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
    assert text.startswith(f"# {CANONICAL_ID} — Weather Bot Phase 0A Settlement Rule Interpreter Planning")
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
        "docs/static-test-only/settlement-rule-interpreter-planning-only", "This ticket does not modify `meg/`",
        "This ticket does not modify meta/handoff files", "does not modify Stage 2 runtime metadata modules",
        "does not revise the owner decision", "does not reopen source-fetching implementation planning",
        "does not fetch, create, or modify market data", "does not create fixtures or generated data",
        "does not create or modify schemas", "does not implement runtime market-contract ingestion",
        "does not implement runtime supplied-input loading", "does not implement runtime supplied-input validation",
        "does not persist supplied input", "does not implement runtime settlement-rule parsing",
        "does not implement runtime settlement-rule classification", "does not implement runtime settlement-rule interpretation",
        "does not persist interpreter output", "does not implement runtime metadata behavior",
        "does not implement runtime fail-closed enforcement", "does not implement runtime error handling",
        "does not implement runtime no-lookahead enforcement", "does not implement runtime timestamp validation",
        "does not implement runtime manual-review workflow behavior", "does not implement operator decision execution",
        "does not implement manual-review UI or persistence", "does not implement scoring, evaluation execution, backtesting, paper trading, trading, or autonomy",
        "does not execute paper trades", "does not create simulated orders", "persisted interpreter output",
        "does not create a separate standalone self-review artifact", "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work", "source-fetching runtime track remains closed/held",
        "closed owner decision remains `hold_source_fetching_runtime_track`", "Source fetching remains not implemented",
        "Implementation approval remains not granted", "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
        "Supplied market-contract input runtime behavior remains not implemented", "Settlement-rule interpreter runtime behavior remains not implemented",
        "Operator workflow runtime behavior remains not implemented", "Paper-trade readiness remains not achieved", "Evaluation readiness remains not achieved",
        "Provider connectors remain not approved", "Provider clients remain not created", "Live provider/source fetching remains not approved",
        "Credentials/config loading remains not approved", "Generated data and fixtures remain not approved", "Scoring/evaluation execution remains not approved",
        "Backtesting remains not approved", "Paper-trade execution remains not approved", "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, metric persistence, supplied-input persistence, interpreter-output persistence, operator-decision persistence, and external export remain not approved",
        "Silence, continuation, lack of objection, and non-interference are not approval",
    ]
    for phrase in required:
        assert phrase in text
    assert not any(FORBIDDEN_APPROVAL_RE.search(line) for line in text.splitlines())


def test_values_paths_blocked_work_and_readiness_appear() -> None:
    text = _read()
    for value in READINESS | INPUTS | OUTPUTS | MEASUREMENTS | THRESHOLDS | TIME_WINDOWS | LOCATIONS | RESOLUTION_SOURCES | OUTCOME_MAPPINGS | AMBIGUITIES | MANUAL_LABELS | FAIL_LABELS | STAGE2_PATHS | BLOCKED_WORK:
        assert value in text
    section = _section(text, "Settlement-rule interpreter readiness status")
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
        "Operator decision execution and persistence remain not approved", "Manual-review UI and persistence remain not approved",
        "Metric persistence remains not approved", "Report writing, persistence, and external export remain not approved",
        "Recommended next ticket: `weather_bot_phase0a_no_lookahead_validation_planning`",
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
    synthetic = (
        f"## {MACHINE_HEADING}\n"
        "- weather bot planning stage: weather_bot_phase0a_settlement_rule_interpreter_planning\n"
        "## Acceptance criteria\n"
        "- blocked work: forbidden_runtime_value\n"
    )
    assert _assignment_pairs(synthetic) == {("weather bot planning stage", "weather_bot_phase0a_settlement_rule_interpreter_planning")}
