"""Static checks for Weather Bot Phase 0A paper-trade readiness gap inventory."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-PAPER-TRADE-READINESS-GAP-INVENTORY-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_paper_trade_readiness_gap_inventory_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A paper-trade-readiness gap-inventory assignments"
NEXT_TRACK = "weather_bot_phase0a_evaluation_metrics_planning"
CONDITIONAL_TRACK = "weather_bot_phase0a_paper_trade_readiness_gap_inventory_revision_if_scope_too_broad"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to Stage 2 metadata contract documentation", "Gap inventory objective",
    "Current held/closed source-fetching posture", "No owner-decision revision boundary",
    "Paper-trade readiness definition", "Current readiness status", "Market contract readiness gaps",
    "Canonical identifier readiness gaps", "Settlement-rule readiness gaps", "Manual-review readiness gaps",
    "No-lookahead readiness gaps", "Fail-closed readiness gaps", "Stage 2 metadata readiness gaps",
    "Source-fetching readiness gaps", "Provider and credential readiness gaps", "Data and fixture readiness gaps",
    "Scoring and evaluation readiness gaps", "Backtesting readiness gaps", "Paper-trade execution readiness gaps",
    "Operator workflow readiness gaps", "Audit, reporting, persistence, and export readiness gaps",
    "Static inventory only boundary", "Canonical identifier posture", "Source-fetching track remains blocked",
    "Provider/source execution boundary", "Credential/config boundary", "Generated-data and fixture boundary",
    "Scoring/backtesting boundary", "Paper-trade boundary", "Trading/autonomy/production boundary",
    "Audit report and export boundary", "Stage 2 runtime metadata posture", "Embedded self-review requirement",
    "Recommended next ticket", MACHINE_HEADING, "Acceptance criteria",
)
READINESS_CURRENT_STATUS = {
    "not_paper_trade_ready", "docs_static_inventory_only", "paper_trade_execution_not_approved",
    "source_fetching_not_implemented", "scoring_not_implemented", "backtesting_not_implemented",
    "operator_workflow_not_implemented", "audit_persistence_not_implemented",
}
READINESS_GAPS = {
    "gap_market_contract_input_source", "gap_canonical_identifier_runtime_contract",
    "gap_settlement_rule_runtime_interpreter", "gap_manual_review_runtime_workflow",
    "gap_no_lookahead_runtime_enforcement", "gap_fail_closed_runtime_enforcement",
    "gap_stage2_metadata_runtime_integration", "gap_source_fetching_approval",
    "gap_provider_connector_strategy", "gap_credential_config_strategy", "gap_generated_data_policy",
    "gap_fixture_policy", "gap_scoring_methodology", "gap_backtesting_methodology",
    "gap_paper_trade_execution_design", "gap_order_simulation_boundary", "gap_operator_decision_workflow",
    "gap_audit_report_strategy", "gap_persistence_strategy", "gap_external_export_strategy",
}
READINESS_BLOCKERS = {
    "block_owner_decision_hold", "block_source_fetching_unapproved", "block_runtime_metadata_not_implemented",
    "block_runtime_validation_not_implemented", "block_scoring_not_implemented", "block_backtesting_not_implemented",
    "block_paper_trade_execution_not_approved", "block_trading_autonomy_production_not_approved",
    "block_audit_persistence_export_not_approved",
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
    "provider_connector_implementation", "provider_client_creation", "live_provider_source_fetching",
    "forecast_pull_execution", "api_call_execution", "scraping_execution", "file_download_execution",
    "provider_sdk_execution", "credentials_config_loading", "generated_data_creation", "fixture_data_modification",
    "runtime_metadata_implementation", "stage2_runtime_module_modification", "fail_closed_runtime_enforcement",
    "runtime_error_handling", "no_lookahead_runtime_enforcement", "timestamp_runtime_validation",
    "settlement_rule_runtime_parser", "settlement_rule_runtime_classification", "manual_review_runtime_workflow",
    "manual_review_ui", "manual_review_persistence", "operator_decision_execution", "scoring_implementation",
    "backtesting_implementation", "paper_trade_execution", "paper_trade_readiness_runtime", "order_simulation",
    "runtime_trading_behavior", "order_placement", "autonomy_behavior", "production_behavior",
    "audit_report_generation", "audit_output_persistence", "external_export_behavior",
    "standalone_self_review_prd_artifact",
}
IMPLEMENTATION_POSTURES = {
    "docs_static_test_only", "paper_trade_readiness_gap_inventory_only", "no_runtime_code_change",
    "no_stage2_runtime_module_modification", "no_runtime_metadata_implementation", "no_owner_decision_revision",
    "no_source_fetching", "no_source_fetching_plan", "no_provider_connector", "no_provider_client",
    "no_live_provider_fetching", "no_credential_config_loading", "no_generated_data", "no_fixture_change",
    "no_fail_closed_runtime_enforcement", "no_runtime_error_handling", "no_no_lookahead_runtime_enforcement",
    "no_timestamp_runtime_validation", "no_settlement_rule_runtime_parser", "no_manual_review_runtime_workflow",
    "no_scoring_backtesting", "no_paper_trade_execution", "no_order_simulation",
    "no_trading_autonomy_production", "no_report_writing", "no_external_export", "no_persistence",
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_phase0a_paper_trade_readiness_gap_inventory"},
    "paper trade readiness status": {
        "docs_static_test_only", "paper_trade_readiness_gap_inventory_only",
        "post_weather_bot_phase0a_stage2_metadata_contract_documentation", "not_paper_trade_ready",
        "paper_trade_execution_not_approved",
    },
    "self review posture": {"embedded_secondary_prompt_only", "no_standalone_self_review_prd"},
    "owner decision posture": {"no_owner_decision_revision", "hold_source_fetching_runtime_track_preserved"},
    "source fetching track posture": {
        "closed_held", "no_source_fetching_implementation_plan", "no_source_fetching_implementation",
        "implementation_approval_not_granted",
    },
    "readiness current status": READINESS_CURRENT_STATUS,
    "readiness gap": READINESS_GAPS,
    "readiness blocker": READINESS_BLOCKERS,
    "stage2 metadata artifact": STAGE2_ASSIGNMENTS,
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "identifier relationship": {
        "token_outcome_pair_derived_relationship", "condition_token_outcome_preserved",
        "token_id_outcome_relationship_preserved",
    },
    "fail closed canonical guard": {"market_identifier_routing_attempt"},
    "blocked work": BLOCKED_WORK,
    "implementation posture": IMPLEMENTATION_POSTURES,
    "recommended next track": {NEXT_TRACK},
    "conditional next track": {CONDITIONAL_TRACK},
    "evidence status": {"paper_trade_readiness_gap_inventory_recorded"},
    "label confidence": {"confirmed"},
}
REQUIRED_ASSIGNMENTS = {(field, value) for field, values in ALLOWED_ASSIGNMENTS.items() for value in values}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
FORBIDDEN_APPROVAL_RE = re.compile(
    r"revised " "owner decision|"
    r"approve_narrow_source_fetching_runtime" "_implementation_plan|"
    r"provider connector " "is approved|provider client " "is created|"
    r"source fetching " "is approved|source fetching implementation " "is approved|"
    r"source fetching implementation planning " "is approved|"
    r"source fetching implementation plan " "is approved|live provider source fetching " "is approved|"
    r"forecast pull " "is approved|api call " "is approved|scraping " "is approved|"
    r"file download " "is approved|provider sdk " "is approved|credentials.*loading " "is approved|"
    r"generated data " "is approved|fixture change " "is approved|runtime metadata implementation " "is approved|"
    r"stage2 runtime module modification " "is approved|fail-closed enforcement " "is approved|"
    r"fail closed enforcement " "is approved|runtime error handling " "is approved|"
    r"no-lookahead enforcement " "is approved|no lookahead enforcement " "is approved|"
    r"timestamp validation " "is approved|settlement rule parser " "is approved|"
    r"settlement rule classification " "is approved|manual review workflow " "is approved|"
    r"manual review ui " "is approved|manual review persistence " "is approved|"
    r"operator decision execution " "is approved|paper trade execution " "is approved|"
    r"paper trade readiness runtime " "is approved|order simulation " "is approved|"
    r"scoring " "is approved|backtesting " "is approved|trading " "is approved|"
    r"order placement " "is approved|autonomy " "is approved|production behavior " "is approved|"
    r"report writing " "is approved|external export " "is approved|persistence " "is approved|"
    r"silence " "is approval|continuation " "is approval|non-interference " "is approval",
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
    assert text.startswith(f"# {CANONICAL_ID} — Weather Bot Phase 0A Paper-Trade Readiness Gap Inventory")
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
        "docs/static-test-only/paper-trade-readiness-gap-inventory-only",
        "This ticket does not modify `meg/`", "This ticket does not modify meta/handoff files",
        "does not modify Stage 2 runtime metadata modules", "does not revise the owner decision",
        "does not reopen source-fetching implementation planning", "does not fetch, create, or modify market data",
        "does not create fixtures or generated data", "does not implement runtime metadata behavior",
        "does not implement runtime fail-closed enforcement", "does not implement runtime error handling",
        "does not implement runtime no-lookahead enforcement", "does not implement runtime timestamp validation",
        "does not implement runtime settlement-rule parsing or classification",
        "does not implement runtime manual-review workflow behavior",
        "does not implement scoring, backtesting, paper trading, trading, or autonomy",
        "does not execute paper trades", "does not create simulated orders",
        "does not create a separate standalone self-review artifact",
        "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work",
        "source-fetching runtime track remains closed/held",
        "closed owner decision remains `hold_source_fetching_runtime_track`",
        "Source fetching remains not implemented", "Implementation approval remains not granted",
        "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
        "Provider connectors remain not approved", "Provider clients remain not created",
        "Live provider/source fetching remains not approved", "Credentials/config loading remains not approved",
        "Generated data and fixtures remain not approved", "Scoring/backtesting remains not approved",
        "Paper-trade execution remains not approved", "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
        "Silence, continuation, lack of objection, and non-interference are not approval",
    ]
    for phrase in required:
        assert phrase in text


def test_readiness_values_blockers_paths_and_blocked_work_appear() -> None:
    text = _read()
    for value in READINESS_CURRENT_STATUS | READINESS_GAPS | READINESS_BLOCKERS | STAGE2_PATHS | BLOCKED_WORK:
        assert value in text


def test_paper_trade_readiness_definition_contains_required_future_criteria_only() -> None:
    section = _section(_read(), "Paper-trade readiness definition")
    required = [
        "trusted market contract input", "preserved canonical identifiers", "settlement-rule interpretation plan",
        "no-lookahead policy enforcement", "fail-closed validation", "manual-review workflow",
        "source-fetching approval if live or source-backed data is required",
        "provider and credential strategy if providers are required", "scoring/evaluation plan", "backtesting plan",
        "paper-trade execution design", "audit/reporting/persistence strategy",
        "not implementation permission",
    ]
    for phrase in required:
        assert phrase in section


def test_current_readiness_status_is_not_paper_trade_ready() -> None:
    section = _section(_read(), "Current readiness status")
    for status in READINESS_CURRENT_STATUS:
        assert f"`{status}`" in section
    assert "`not_paper_trade_ready`" in section


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
        "Provider connectors remain not approved", "Provider clients remain not created",
        "Live provider/source fetching remains not approved",
        "Forecast pull execution, API call execution, scraping execution, file download execution, and provider SDK execution remain not approved",
        "Credentials/config loading remains not approved", "Generated data and fixtures remain not approved",
        "does not implement runtime metadata behavior", "does not modify Stage 2 runtime metadata modules",
        "does not implement runtime fail-closed enforcement", "does not implement runtime error handling",
        "does not implement runtime no-lookahead enforcement", "does not implement runtime timestamp validation",
        "does not implement runtime manual-review workflow behavior",
        "does not implement runtime settlement-rule parsing or classification",
        "Scoring/backtesting remains not approved", "Paper-trade execution remains not approved",
        "does not create simulated orders", "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
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
        "## Machine-checkable Weather Bot Phase 0A paper-trade-readiness gap-inventory assignments\n"
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
        "paper trade execution " "is approved", "order simulation " "is approved",
        "trading " "is approved", "report writing " "is approved", "persistence " "is approved",
        "silence " "is approval",
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
