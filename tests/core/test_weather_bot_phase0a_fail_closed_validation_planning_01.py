from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = ROOT / "docs/prd/WEATHER-BOT-PHASE0A-FAIL-CLOSED-VALIDATION-PLANNING-01.md"
TEST_PATH = ROOT / "tests/core/test_weather_bot_phase0a_fail_closed_validation_planning_01.py"
CANONICAL_ID = "WEATHER-BOT-PHASE0A-FAIL-CLOSED-VALIDATION-PLANNING-01"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A fail-closed-validation-planning assignments"
NEXT_TRACK = "weather_bot_phase0a_phase_summary_and_handoff_refresh"
CONDITIONAL_TRACK = "weather_bot_phase0a_fail_closed_validation_revision_if_scope_too_broad"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to no-lookahead validation planning",
    "Fail-closed validation planning objective", "Current held/closed source-fetching posture",
    "No owner-decision revision boundary", "Fail-closed validation readiness status", "Validation overview",
    "Fail-closed trigger categories", "Fail-closed status labels", "Validation blocker categories",
    "Manual-review handoff labels", "Operator decision relationship", "No-lookahead validation relationship",
    "Settlement-rule interpreter relationship", "Stage 2 metadata relationship", "Static planning only boundary",
    "Canonical identifier posture", "Source-fetching track remains blocked", "Provider/source execution boundary",
    "Credential/config boundary", "Generated-data and fixture boundary", "Runtime validation boundary",
    "Runtime parser/classifier boundary", "Runtime ingestion and schema boundary", "Scoring/evaluation boundary",
    "Backtesting boundary", "Paper-trade boundary", "Operator workflow execution boundary",
    "Trading/autonomy/production boundary", "Audit report and export boundary", "Stage 2 runtime metadata posture",
    "Embedded self-review requirement", "Recommended next ticket", MACHINE_HEADING, "Acceptance criteria",
)
READINESS = set("""not_fail_closed_validation_ready docs_static_fail_closed_validation_planning_only runtime_fail_closed_validation_not_implemented runtime_error_handling_not_implemented runtime_no_lookahead_validation_not_implemented runtime_evidence_time_comparison_not_implemented validation_output_persistence_not_approved source_fetching_not_implemented paper_trade_execution_not_approved""".split())
TRIGGERS = set("""trigger_missing_required_field trigger_identifier_mismatch trigger_token_outcome_mismatch trigger_ambiguous_settlement_rule trigger_unsupported_measurement trigger_ambiguous_threshold trigger_ambiguous_comparator trigger_ambiguous_time_window trigger_ambiguous_location trigger_resolution_source_missing trigger_resolution_source_conflict trigger_timestamp_missing trigger_timestamp_ambiguous trigger_lookahead_detected trigger_source_unapproved trigger_provider_unavailable trigger_scope_violation""".split())
STATUSES = set("""fail_closed_status_not_available fail_closed_status_static_planning_only fail_closed_status_requires_manual_review fail_closed_status_block_processing fail_closed_status_block_source_unapproved fail_closed_status_block_lookahead_detected fail_closed_status_block_identifier_mismatch fail_closed_status_block_ambiguous_rule fail_closed_status_block_scope_violation""".split())
BLOCKERS = set("""block_runtime_fail_closed_validation_missing block_runtime_error_handling_missing block_runtime_no_lookahead_validation_missing block_runtime_evidence_time_comparison_missing block_validation_output_persistence_unapproved block_source_fetching_unapproved block_provider_execution_unapproved block_generated_fixture_data_unapproved block_operator_workflow_runtime_missing block_scoring_evaluation_unapproved block_backtesting_unapproved block_paper_trade_execution_not_approved block_trading_autonomy_production_not_approved block_audit_persistence_export_not_approved""".split())
HANDOFFS = set("""handoff_manual_review_required handoff_fail_closed_reason_check_required handoff_identifier_check_required handoff_settlement_rule_check_required handoff_no_lookahead_check_required handoff_source_approval_check_required handoff_scope_revision_check_required""".split())
STAGE2_PATHS = set("""meg/weather/stage2/source_identity_runtime.py meg/weather/stage2/retrieval_context_runtime.py meg/weather/stage2/provider_source_family_runtime.py meg/weather/stage2/manual_review_gate_runtime.py meg/weather/stage2/no_lookahead_metadata_runtime.py meg/weather/stage2/fail_closed_validation_runtime.py meg/weather/stage2/static_audit_surface_runtime.py""".split())
STAGE2_ASSIGNMENTS = set("""source_identity_runtime_py retrieval_context_runtime_py provider_source_family_runtime_py manual_review_gate_runtime_py no_lookahead_metadata_runtime_py fail_closed_validation_runtime_py static_audit_surface_runtime_py""".split())
BLOCKED_WORK = set("""owner_decision_revision source_fetching_runtime_implementation_plan source_fetching_implementation provider_connector_implementation provider_client_creation live_provider_source_fetching forecast_pull_execution api_call_execution scraping_execution file_download_execution provider_sdk_execution credentials_config_loading generated_data_creation fixture_data_modification schema_change db_migration runtime_market_contract_ingestion runtime_supplied_input_loading runtime_supplied_input_validation supplied_input_persistence runtime_settlement_rule_parser runtime_settlement_rule_classifier runtime_settlement_rule_interpreter interpreter_output_persistence runtime_no_lookahead_validation runtime_timestamp_validation runtime_evidence_time_comparison runtime_fail_closed_validation runtime_error_handling validation_output_persistence runtime_metadata_implementation stage2_runtime_module_modification manual_review_runtime_workflow manual_review_ui manual_review_persistence operator_decision_execution operator_decision_persistence scoring_implementation evaluation_execution metric_persistence backtesting_implementation paper_trade_execution paper_trade_readiness_runtime order_simulation runtime_trading_behavior order_placement autonomy_behavior production_behavior audit_report_generation audit_output_persistence external_export_behavior standalone_self_review_prd_artifact""".split())
IMPLEMENTATION_POSTURES = set("""docs_static_test_only fail_closed_validation_planning_only no_runtime_code_change no_meg_modification no_meta_handoff_modification no_stage2_runtime_module_modification no_runtime_metadata_implementation no_owner_decision_revision no_source_fetching_reopen no_source_fetching no_source_fetching_plan no_provider_connector no_provider_client no_live_provider_fetching no_credential_config_loading no_generated_data no_fixture_change no_schema_change no_db_migration no_runtime_market_contract_ingestion no_runtime_supplied_input_loading no_runtime_supplied_input_validation no_supplied_input_persistence no_runtime_settlement_rule_parser no_runtime_settlement_rule_classifier no_runtime_settlement_rule_interpreter no_interpreter_output_persistence no_runtime_no_lookahead_validation no_runtime_timestamp_validation no_runtime_evidence_time_comparison no_runtime_fail_closed_validation no_runtime_error_handling no_validation_output_persistence no_manual_review_runtime_workflow no_manual_review_ui no_manual_review_persistence no_operator_decision_execution no_operator_decision_persistence no_scoring_implementation no_evaluation_execution no_metric_persistence no_backtesting_implementation no_paper_trade_execution no_order_simulation no_trading_autonomy_production no_report_writing no_external_export no_persistence""".split())
ALLOWED_ASSIGNMENTS = {
    "planning stage": {"weather_bot_phase0a_fail_closed_validation_planning"},
    "fail-closed validation status": {"docs_static_test_only", "fail_closed_validation_planning_only", "post_weather_bot_phase0a_no_lookahead_validation_planning"},
    "readiness status": READINESS,
    "fail-closed trigger category": TRIGGERS,
    "fail-closed status label": STATUSES,
    "validation blocker category": BLOCKERS,
    "manual-review handoff label": HANDOFFS,
    "Stage 2 metadata artifact": STAGE2_ASSIGNMENTS,
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non-routing market_id": {"market_id"},
    "identifier relationship": {"token_outcome_pair_derived_relationship", "condition_token_outcome_preserved", "token_id_outcome_relationship_preserved"},
    "fail-closed canonical guard": {"market_identifier_routing_attempt"},
    "blocked work": BLOCKED_WORK,
    "implementation posture": IMPLEMENTATION_POSTURES,
    "recommended next track": {NEXT_TRACK},
    "conditional next track": {CONDITIONAL_TRACK},
    "evidence status": {"fail_closed_validation_planning_recorded"},
    "label confidence": {"confirmed"},
}
REQUIRED_ASSIGNMENTS = {(field, value) for field, values in ALLOWED_ASSIGNMENTS.items() for value in values}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
FORBIDDEN_APPROVAL_TERMS = (
    ("owner", "decision", "is", "revised"),
    ("revised", "owner", "decision", "approved"),
    ("source", "fetching", "is", "approved"),
    ("source", "fetching", "implementation", "is", "approved"),
    ("provider", "connector", "is", "approved"),
    ("provider", "client", "is", "created"),
    ("live", "provider/source", "fetching", "is", "approved"),
    ("credentials/config", "loading", "is", "approved"),
    ("generated", "data", "is", "approved"),
    ("fixture", "changes", "are", "approved"),
    ("schema", "change", "is", "approved"),
    ("db", "migration", "is", "approved"),
    ("runtime", "fail-closed", "validation", "is", "approved"),
    ("runtime", "no-lookahead", "validation", "is", "approved"),
    ("runtime", "timestamp", "validation", "is", "approved"),
    ("runtime", "evidence-time", "comparison", "is", "approved"),
    ("settlement-rule", "interpreter", "is", "approved"),
    ("scoring", "is", "approved"),
    ("evaluation", "execution", "is", "approved"),
    ("backtesting", "is", "approved"),
    ("paper-trade", "execution", "is", "approved"),
    ("trading", "is", "approved"),
    ("autonomy", "is", "approved"),
    ("production", "behavior", "is", "approved"),
    ("persistence", "is", "approved"),
    ("export", "is", "approved"),
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
    assert text.startswith(f"# {CANONICAL_ID} — Weather Bot Phase 0A Fail-Closed Validation Planning")
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


def test_required_posture_boundaries_and_embedded_self_review_are_present() -> None:
    text = _read()
    required = [
        "docs/static-test-only/fail-closed-validation-planning-only", "This ticket does not modify `meg/`",
        "This ticket does not modify meta/handoff files", "does not revise the owner decision",
        "does not reopen source-fetching implementation planning", "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work",
        "source-fetching runtime track remains closed/held",
        "closed owner decision remains `hold_source_fetching_runtime_track`", "Source fetching remains not implemented",
        "Implementation approval remains not granted", "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
        "No-lookahead validation runtime behavior remains not implemented", "Fail-closed validation runtime behavior remains not implemented",
        "Settlement-rule interpreter runtime behavior remains not implemented", "Operator workflow runtime behavior remains not implemented",
        "Paper-trade readiness remains not achieved", "Evaluation readiness remains not achieved",
        "Provider connectors, provider clients, live provider/source fetching, credentials/config loading, generated data, fixtures, scoring/evaluation, backtesting, paper-trade execution, trading/autonomy/production, reports, persistence, and export remain not approved",
        "Silence, continuation, lack of objection, and non-interference are not approval",
        "embedded secondary self-review prompt", "Do not create a separate standalone self-review PRD artifact",
        "Do not recommend a standalone self-review ticket",
    ]
    for phrase in required:
        assert phrase in text
    assert not any(FORBIDDEN_APPROVAL_RE.search(line) for line in text.splitlines())
    assert " ".join(("owner", "decision", "is", "revised")) not in text.lower()
    assert " ".join(("revised", "owner", "decision", "approved")) not in text.lower()


def test_values_paths_blocked_work_and_readiness_appear() -> None:
    text = _read()
    for value in READINESS | TRIGGERS | STATUSES | BLOCKERS | HANDOFFS | STAGE2_PATHS | BLOCKED_WORK | IMPLEMENTATION_POSTURES:
        assert value in text
    section = _section(text, "Fail-closed validation readiness status")
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
    assert ("non-routing market_id", "market_id") in pairs
    assert ("fail-closed canonical guard", "market_identifier_routing_attempt") in pairs


def test_planning_boundaries_and_next_tracks_are_present() -> None:
    text = _read()
    required_phrases = [
        "Provider connector implementation", "Credentials/config loading remains not approved",
        "Generated data creation and fixture data modification remain not approved", "Schema change, DB migration",
        "Runtime fail-closed validation, runtime error handling, runtime no-lookahead validation",
        "Runtime settlement-rule parser, runtime settlement-rule classifier, runtime settlement-rule interpreter",
        "Scoring implementation, evaluation execution, metric persistence", "Backtesting implementation remains not approved",
        "Paper-trade execution, paper-trade readiness runtime, and order simulation", "Runtime trading behavior, order placement, autonomy behavior, and production behavior remain not approved",
        "Audit report generation, audit output persistence, external export behavior", f"Recommended next ticket: `{NEXT_TRACK}`",
        "docs/static-test-only/meta-handoff-refresh-only", "Do not recommend a standalone self-review ticket as the next ticket",
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
