"""Static checks for Weather Bot Phase 0A supplied market-contract input planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-SUPPLIED-MARKET-CONTRACT-INPUT-PLANNING-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_supplied_market_contract_input_planning_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A supplied-market-contract-input-planning assignments"
NEXT_TRACK = "weather_bot_phase0a_settlement_rule_interpreter_planning"
CONDITIONAL_TRACK = "weather_bot_phase0a_supplied_market_contract_input_revision_if_scope_too_broad"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to operator workflow planning", "Supplied input planning objective",
    "Current held/closed source-fetching posture", "No owner-decision revision boundary",
    "Supplied market-contract input readiness status", "Supplied input overview", "Required supplied contract fields",
    "Optional supplied contract context fields", "Canonical identifier supplied-input requirements",
    "Settlement-rule supplied-input requirements", "Resolution-source supplied-input requirements",
    "Time-window supplied-input requirements", "Location supplied-input requirements",
    "Outcome mapping supplied-input requirements", "Manual-review supplied-input requirements",
    "No-lookahead supplied-input requirements", "Fail-closed supplied-input requirements",
    "Stage 2 metadata supplied-input relationship", "Supplied input completeness gates",
    "Supplied input readiness blockers", "Static planning only boundary", "Canonical identifier posture",
    "Source-fetching track remains blocked", "Provider/source execution boundary", "Credential/config boundary",
    "Generated-data and fixture boundary", "Runtime ingestion and schema boundary", "Scoring/evaluation boundary",
    "Backtesting boundary", "Paper-trade boundary", "Operator workflow execution boundary",
    "Trading/autonomy/production boundary", "Audit report and export boundary", "Stage 2 runtime metadata posture",
    "Embedded self-review requirement", "Recommended next ticket", MACHINE_HEADING, "Acceptance criteria",
)
READINESS = {
    "not_supplied_input_ready", "docs_static_supplied_input_planning_only",
    "runtime_market_contract_ingestion_not_implemented", "runtime_supplied_input_loading_not_implemented",
    "runtime_supplied_input_validation_not_implemented", "schema_change_not_approved",
    "supplied_input_persistence_not_approved", "source_fetching_not_implemented", "paper_trade_execution_not_approved",
}
REQUIRED_FIELDS = {"condition_id", "token_id", "outcome", "question_text", "settlement_rule_text", "resolution_source_text", "outcome_label", "token_outcome_pair"}
OPTIONAL_FIELDS = {"market_slug", "market_title", "market_description", "open_time", "close_time", "resolution_time", "event_start_time", "event_end_time", "market_status", "operator_review_required", "manual_review_reason"}
GATES = {"gate_condition_id_present", "gate_token_id_present", "gate_outcome_present", "gate_token_outcome_pair_consistent", "gate_question_text_present", "gate_settlement_rule_text_present", "gate_resolution_source_text_present", "gate_outcome_label_present", "gate_time_window_context_reviewed", "gate_location_context_reviewed", "gate_manual_review_context_reviewed", "gate_no_lookahead_context_reviewed", "gate_fail_closed_context_reviewed", "gate_stage2_metadata_context_reviewed"}
BLOCKERS = {"block_runtime_market_contract_ingestion_missing", "block_runtime_supplied_input_loading_missing", "block_runtime_supplied_input_validation_missing", "block_schema_change_unapproved", "block_supplied_input_persistence_unapproved", "block_source_fetching_unapproved", "block_provider_execution_unapproved", "block_generated_fixture_data_unapproved", "block_operator_workflow_runtime_missing", "block_scoring_evaluation_unapproved", "block_backtesting_unapproved", "block_paper_trade_execution_not_approved", "block_trading_autonomy_production_not_approved", "block_audit_persistence_export_not_approved"}
STAGE2_PATHS = {"meg/weather/stage2/source_identity_runtime.py", "meg/weather/stage2/retrieval_context_runtime.py", "meg/weather/stage2/provider_source_family_runtime.py", "meg/weather/stage2/manual_review_gate_runtime.py", "meg/weather/stage2/no_lookahead_metadata_runtime.py", "meg/weather/stage2/fail_closed_validation_runtime.py", "meg/weather/stage2/static_audit_surface_runtime.py"}
STAGE2_ASSIGNMENTS = {"source_identity_runtime_py", "retrieval_context_runtime_py", "provider_source_family_runtime_py", "manual_review_gate_runtime_py", "no_lookahead_metadata_runtime_py", "fail_closed_validation_runtime_py", "static_audit_surface_runtime_py"}
BLOCKED_WORK = {"owner_decision_revision", "source_fetching_runtime_implementation_plan", "source_fetching_implementation", "provider_connector_implementation", "provider_client_creation", "live_provider_source_fetching", "forecast_pull_execution", "api_call_execution", "scraping_execution", "file_download_execution", "provider_sdk_execution", "credentials_config_loading", "generated_data_creation", "fixture_data_modification", "schema_change", "db_migration", "runtime_market_contract_ingestion", "runtime_supplied_input_loading", "runtime_supplied_input_validation", "supplied_input_persistence", "runtime_metadata_implementation", "stage2_runtime_module_modification", "fail_closed_runtime_enforcement", "runtime_error_handling", "no_lookahead_runtime_enforcement", "timestamp_runtime_validation", "settlement_rule_runtime_parser", "settlement_rule_runtime_classification", "manual_review_runtime_workflow", "manual_review_ui", "manual_review_persistence", "operator_decision_execution", "operator_decision_persistence", "scoring_implementation", "evaluation_execution", "metric_persistence", "backtesting_implementation", "paper_trade_execution", "paper_trade_readiness_runtime", "order_simulation", "runtime_trading_behavior", "order_placement", "autonomy_behavior", "production_behavior", "audit_report_generation", "audit_output_persistence", "external_export_behavior", "standalone_self_review_prd_artifact"}
IMPLEMENTATION_POSTURES = {"docs_static_test_only", "supplied_market_contract_input_planning_only", "no_runtime_code_change", "no_stage2_runtime_module_modification", "no_runtime_metadata_implementation", "no_owner_decision_revision", "no_source_fetching", "no_source_fetching_plan", "no_provider_connector", "no_provider_client", "no_live_provider_fetching", "no_credential_config_loading", "no_generated_data", "no_fixture_change", "no_schema_change", "no_db_migration", "no_runtime_market_contract_ingestion", "no_runtime_supplied_input_loading", "no_runtime_supplied_input_validation", "no_supplied_input_persistence", "no_fail_closed_runtime_enforcement", "no_runtime_error_handling", "no_no_lookahead_runtime_enforcement", "no_timestamp_runtime_validation", "no_settlement_rule_runtime_parser", "no_manual_review_runtime_workflow", "no_manual_review_ui", "no_manual_review_persistence", "no_operator_decision_execution", "no_operator_decision_persistence", "no_scoring_implementation", "no_evaluation_execution", "no_metric_persistence", "no_backtesting_implementation", "no_paper_trade_execution", "no_order_simulation", "no_trading_autonomy_production", "no_report_writing", "no_external_export", "no_persistence"}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_phase0a_supplied_market_contract_input_planning"},
    "supplied input status": {"docs_static_test_only", "supplied_market_contract_input_planning_only", "post_weather_bot_phase0a_operator_workflow_planning"},
    "supplied input readiness status": READINESS,
    "self review posture": {"embedded_secondary_prompt_only", "no_standalone_self_review_prd"},
    "owner decision posture": {"no_owner_decision_revision", "hold_source_fetching_runtime_track_preserved"},
    "source fetching track posture": {"closed_held", "no_source_fetching_implementation_plan", "no_source_fetching_implementation", "implementation_approval_not_granted"},
    "required supplied contract field": REQUIRED_FIELDS,
    "optional supplied contract context field": OPTIONAL_FIELDS,
    "supplied input completeness gate": GATES,
    "supplied input readiness blocker": BLOCKERS,
    "stage2 metadata artifact": STAGE2_ASSIGNMENTS,
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "identifier relationship": {"token_outcome_pair_derived_relationship", "condition_token_outcome_preserved", "token_id_outcome_relationship_preserved"},
    "fail closed canonical guard": {"market_identifier_routing_attempt"},
    "blocked work": BLOCKED_WORK,
    "implementation posture": IMPLEMENTATION_POSTURES,
    "recommended next track": {NEXT_TRACK},
    "conditional next track": {CONDITIONAL_TRACK},
    "evidence status": {"supplied_market_contract_input_planning_recorded"},
    "label confidence": {"confirmed"},
}
REQUIRED_ASSIGNMENTS = {(field, value) for field, values in ALLOWED_ASSIGNMENTS.items() for value in values}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
FORBIDDEN_APPROVAL_TERMS = (
    ('revised', 'owner', 'decision'),
    ('approve_narrow_source_fetching', '_runtime_implementation_plan'),
    ('provider', 'connector', 'is', 'approved'),
    ('provider', 'client', 'is', 'created'),
    ('source', 'fetching', 'is', 'approved'),
    ('source', 'fetching', 'implementation', 'is', 'approved'),
    ('source', 'fetching', 'implementation', 'planning', 'is', 'approved'),
    ('source', 'fetching', 'implementation', 'plan', 'is', 'approved'),
    ('live', 'provider', 'source', 'fetching', 'is', 'approved'),
    ('forecast', 'pull', 'is', 'approved'),
    ('api', 'call', 'is', 'approved'),
    ('scraping', 'is', 'approved'),
    ('file', 'download', 'is', 'approved'),
    ('provider', 'sdk', 'is', 'approved'),
    ('credentials.*loading', 'is', 'approved'),
    ('generated', 'data', 'is', 'approved'),
    ('fixture', 'change', 'is', 'approved'),
    ('schema', 'change', 'is', 'approved'),
    ('db', 'migration', 'is', 'approved'),
    ('market-contract', 'ingestion', 'is', 'approved'),
    ('market', 'contract', 'ingestion', 'is', 'approved'),
    ('supplied-input', 'loading', 'is', 'approved'),
    ('supplied', 'input', 'loading', 'is', 'approved'),
    ('supplied-input', 'validation', 'is', 'approved'),
    ('supplied', 'input', 'validation', 'is', 'approved'),
    ('supplied', 'input', 'persistence', 'is', 'approved'),
    ('runtime', 'metadata', 'implementation', 'is', 'approved'),
    ('stage2', 'runtime', 'module', 'modification', 'is', 'approved'),
    ('fail-closed', 'enforcement', 'is', 'approved'),
    ('fail', 'closed', 'enforcement', 'is', 'approved'),
    ('runtime', 'error', 'handling', 'is', 'approved'),
    ('no-lookahead', 'enforcement', 'is', 'approved'),
    ('no', 'lookahead', 'enforcement', 'is', 'approved'),
    ('timestamp', 'validation', 'is', 'approved'),
    ('settlement', 'rule', 'parser', 'is', 'approved'),
    ('settlement', 'rule', 'classification', 'is', 'approved'),
    ('manual', 'review', 'workflow', 'is', 'approved'),
    ('manual', 'review', 'ui', 'is', 'approved'),
    ('manual', 'review', 'persistence', 'is', 'approved'),
    ('operator', 'decision', 'execution', 'is', 'approved'),
    ('operator', 'decision', 'persistence', 'is', 'approved'),
    ('scoring', 'is', 'approved'),
    ('evaluation', 'execution', 'is', 'approved'),
    ('metric', 'persistence', 'is', 'approved'),
    ('backtesting', 'is', 'approved'),
    ('paper', 'trade', 'execution', 'is', 'approved'),
    ('paper', 'trade', 'readiness', 'runtime', 'is', 'approved'),
    ('order', 'simulation', 'is', 'approved'),
    ('trading', 'is', 'approved'),
    ('order', 'placement', 'is', 'approved'),
    ('autonomy', 'is', 'approved'),
    ('production', 'behavior', 'is', 'approved'),
    ('report', 'writing', 'is', 'approved'),
    ('external', 'export', 'is', 'approved'),
    ('persistence', 'is', 'approved'),
    ('silence', 'is', 'approval'),
    ('continuation', 'is', 'approval'),
    ('non-interference', 'is', 'approval'),
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
    assert text.startswith(f"# {CANONICAL_ID} — Weather Bot Phase 0A Supplied Market Contract Input Planning")
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
        "docs/static-test-only/supplied-market-contract-input-planning-only", "This ticket does not modify `meg/`",
        "This ticket does not modify meta/handoff files", "does not modify Stage 2 runtime metadata modules",
        "does not revise the owner decision", "does not reopen source-fetching implementation planning",
        "does not fetch, create, or modify market data", "does not create fixtures or generated data",
        "does not create or modify schemas", "does not implement runtime market-contract ingestion",
        "does not implement runtime supplied-input loading", "does not implement runtime supplied-input validation",
        "does not persist supplied input", "does not implement runtime metadata behavior",
        "does not implement runtime fail-closed enforcement", "does not implement runtime error handling",
        "does not implement runtime no-lookahead enforcement", "does not implement runtime timestamp validation",
        "does not implement runtime settlement-rule parsing or classification",
        "does not implement runtime manual-review workflow behavior", "does not implement operator decision execution",
        "does not implement manual-review UI or persistence", "does not implement scoring, evaluation execution, metric persistence, backtesting, paper trading, trading, or autonomy"[:80],
        "does not execute paper trades", "does not create simulated orders", "persisted supplied input",
        "does not create a separate standalone self-review artifact", "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work", "source-fetching runtime track remains closed/held",
        "closed owner decision remains `hold_source_fetching_runtime_track`", "Source fetching remains not implemented",
        "Implementation approval remains not granted", "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
        "Supplied market-contract input runtime behavior remains not implemented", "Operator workflow runtime behavior remains not implemented",
        "Paper-trade readiness remains not achieved", "Evaluation readiness remains not achieved", "Provider connectors remain not approved",
        "Provider clients remain not created", "Live provider/source fetching remains not approved", "Credentials/config loading remains not approved",
        "Generated data and fixtures remain not approved", "Scoring/evaluation execution remains not approved", "Backtesting remains not approved",
        "Paper-trade execution remains not approved", "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, metric persistence, supplied-input persistence, operator-decision persistence, and external export remain not approved",
        "Silence, continuation, lack of objection, and non-interference are not approval",
    ]
    for phrase in required:
        assert phrase in text


def test_values_paths_blocked_work_and_readiness_appear() -> None:
    text = _read()
    for value in READINESS | REQUIRED_FIELDS | OPTIONAL_FIELDS | GATES | BLOCKERS | STAGE2_PATHS | BLOCKED_WORK:
        assert value in text
    section = _section(text, "Supplied market-contract input readiness status")
    for status in READINESS:
        assert f"`{status}`" in section
    assert "`not_supplied_input_ready`" in section


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
        "Schema change and DB migration remain not approved", "does not implement runtime market-contract ingestion",
        "does not implement runtime supplied-input loading", "does not implement runtime supplied-input validation",
        "does not implement runtime metadata behavior", "does not modify Stage 2 runtime metadata modules",
        "does not implement runtime fail-closed enforcement", "does not implement runtime error handling",
        "does not implement runtime no-lookahead enforcement", "does not implement runtime timestamp validation",
        "does not implement runtime manual-review workflow behavior", "does not implement runtime settlement-rule parsing or classification",
        "does not implement operator decision execution", "does not implement manual-review UI or persistence",
        "Scoring/evaluation execution remains not approved", "Backtesting remains not approved", "Paper-trade execution remains not approved",
        "does not create simulated orders", "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, metric persistence, supplied-input persistence, operator-decision persistence, and external export remain not approved",
    ]
    for phrase in required:
        assert phrase in text


def test_embedded_self_review_and_recommended_next_track() -> None:
    text = _read()
    section = _section(text, "Embedded self-review requirement")
    assert "self-reviewed using the secondary self-review prompt" in section
    assert "self-review result must be summarized in the PR body" in section
    assert "Do not create a separate standalone self-review PRD artifact" in section
    next_section = _section(text, "Recommended next ticket")
    assert f"`{NEXT_TRACK}`" in next_section
    assert "standalone self-review" in next_section
    assert "runtime parsing/classification" in next_section


def test_machine_checkable_assignments_are_complete_and_allowed() -> None:
    pairs = _assignment_pairs(_read())
    assert pairs == REQUIRED_ASSIGNMENTS
    for field, value in pairs:
        assert field in ALLOWED_ASSIGNMENTS
        assert value in ALLOWED_ASSIGNMENTS[field]
    assert {value for field, value in pairs if field == "canonical routing field"} == {"condition_id", "token_id", "outcome"}
    assert ("non routing field", "market_id") in pairs
    assert ("fail closed canonical guard", "market_identifier_routing_attempt") in pairs
    assert ("identifier relationship", "token_outcome_pair_derived_relationship") in pairs
    assert ("recommended next track", NEXT_TRACK) in pairs
    assert ("conditional next track", CONDITIONAL_TRACK) in pairs
    assert not any(field == "recommended next track" and "self_review" in value for field, value in pairs)


def test_machine_checkable_parser_is_section_scoped() -> None:
    synthetic = _read() + "\n## Later heading\n- recommended next track: standalone_self_review_ticket\n- bogus field: bogus_value\n"
    assert _assignment_pairs(synthetic) == _assignment_pairs(_read())


def test_forbidden_approval_phrases_are_absent() -> None:
    assert not FORBIDDEN_APPROVAL_RE.search(_read())


def test_no_runtime_or_forbidden_paths_are_referenced_as_changes() -> None:
    text = _read()
    assert "This ticket does not modify `meg/`" in text
    assert "This ticket does not modify meta/handoff files" in text
    assert "This ticket does not modify `.env`, secrets, credentials, config, or config-loading behavior" in text
    assert "tests/fixtures/" not in text
