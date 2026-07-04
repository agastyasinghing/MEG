from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-PHASE-SUMMARY-AND-HANDOFF-REFRESH-01"
PRD = ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST = ROOT / "tests/core/test_weather_bot_phase0a_phase_summary_and_handoff_refresh_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A phase-summary-and-handoff-refresh assignments"
META_DOCS = (
    ROOT / "docs/meta/MEG_ACTIVE_STATE.md",
    ROOT / "docs/meta/MEG_CHAT_HANDOFF.md",
    ROOT / "docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md",
    ROOT / "docs/meta/domain_packets/WEATHER_BOT_PACKET.md",
)
REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to PR #301 fail-closed validation planning", "Phase 0A planning chain summary",
    "Current held/closed source-fetching posture", "No owner-decision revision boundary", "Current Weather Bot readiness snapshot",
    "Completed Phase 0A planning artifacts", "Current canonical identifier posture", "Current Stage 2 metadata posture",
    "Current non-source-fetching boundaries", "Current blocked runtime scopes", "Current next-chat bootstrap instructions",
    "Handoff docs refreshed", "Static documentation only boundary", "Source-fetching track remains blocked",
    "Provider/source execution boundary", "Credential/config boundary", "Generated-data and fixture boundary",
    "Runtime validation boundary", "Runtime parser/interpreter boundary", "Runtime ingestion and schema boundary",
    "Scoring/evaluation boundary", "Backtesting boundary", "Paper-trade boundary", "Operator workflow execution boundary",
    "Trading/autonomy/production boundary", "Audit report and export boundary", "Embedded self-review requirement",
    "Recommended next ticket", MACHINE_HEADING, "Acceptance criteria",
)
ARTIFACTS = tuple("""WEATHER-BOT-PHASE0A-NON-SOURCE-FETCHING-SCOPE-INVENTORY-01 WEATHER-BOT-PHASE0A-MARKET-CONTRACT-STATIC-INVENTORY-01 WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-01 WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-POLICY-DOCUMENTATION-01 WEATHER-BOT-PHASE0A-FAIL-CLOSED-ERROR-TAXONOMY-PLANNING-01 WEATHER-BOT-PHASE0A-STAGE2-METADATA-CONTRACT-DOCUMENTATION-01 WEATHER-BOT-PHASE0A-PAPER-TRADE-READINESS-GAP-INVENTORY-01 WEATHER-BOT-PHASE0A-EVALUATION-METRICS-PLANNING-01 WEATHER-BOT-PHASE0A-OPERATOR-WORKFLOW-PLANNING-01 WEATHER-BOT-PHASE0A-SUPPLIED-MARKET-CONTRACT-INPUT-PLANNING-01 WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-INTERPRETER-PLANNING-01 WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-VALIDATION-PLANNING-01 WEATHER-BOT-PHASE0A-FAIL-CLOSED-VALIDATION-PLANNING-01""".split())
BLOCKED = set("""owner_decision_revision source_fetching_runtime_implementation_plan source_fetching_implementation provider_connector_implementation provider_client_creation live_provider_source_fetching forecast_pull_execution api_call_execution scraping_execution file_download_execution provider_sdk_execution credentials_config_loading generated_data_creation fixture_data_modification schema_change db_migration runtime_market_contract_ingestion runtime_supplied_input_loading runtime_supplied_input_validation supplied_input_persistence runtime_settlement_rule_parser runtime_settlement_rule_classifier runtime_settlement_rule_interpreter interpreter_output_persistence runtime_no_lookahead_validation runtime_timestamp_validation runtime_evidence_time_comparison runtime_fail_closed_validation runtime_error_handling validation_output_persistence runtime_metadata_implementation stage2_runtime_module_modification manual_review_runtime_workflow manual_review_ui manual_review_persistence operator_decision_execution operator_decision_persistence scoring_implementation evaluation_execution metric_persistence backtesting_implementation paper_trade_execution paper_trade_readiness_runtime order_simulation runtime_trading_behavior order_placement autonomy_behavior production_behavior audit_report_generation audit_output_persistence external_export_behavior""".split())
IMPLEMENTATION = set("""docs_static_test_only meta_handoff_refresh_only no_runtime_code_change no_meg_modification no_stage2_runtime_module_modification no_owner_decision_revision no_source_fetching no_source_fetching_plan no_provider_connector no_provider_client no_live_provider_fetching no_credential_config_loading no_generated_data no_fixture_change no_schema_change no_db_migration no_runtime_validation no_runtime_parser_interpreter no_scoring_evaluation no_backtesting no_paper_trade_execution no_order_simulation no_trading_autonomy_production no_report_writing no_external_export no_persistence""".split())
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
ALLOWED = {
    "weather bot planning stage": {"weather_bot_phase0a_phase_summary_and_handoff_refresh"},
    "handoff refresh status": {"docs_static_test_only", "meta_handoff_refresh_only", "post_weather_bot_phase0a_fail_closed_validation_planning"},
    "latest merged pr": {"pr_301"}, "excluded predecessor pr": {"pr_283_unmerged"},
    "owner decision posture": {"no_owner_decision_revision", "hold_source_fetching_runtime_track_preserved"},
    "source fetching track posture": {"closed_held", "source_fetching_not_implemented", "implementation_approval_not_granted"},
    "weather bot scope": {"market_settlement_rule_not_generic_weather"},
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "identifier relationship": {"token_outcome_pair_derived_relationship", "condition_token_outcome_preserved", "token_id_outcome_relationship_preserved"},
    "stage2 metadata posture": {"supplied_metadata_only", "fail_closed"},
    "readiness status": {"paper_trade_readiness_not_achieved", "evaluation_readiness_not_achieved", "operator_workflow_runtime_not_implemented", "supplied_market_contract_runtime_not_implemented", "settlement_rule_interpreter_runtime_not_implemented", "no_lookahead_validation_runtime_not_implemented", "fail_closed_validation_runtime_not_implemented"},
    "refreshed handoff file": {"meg_active_state_md", "meg_chat_handoff_md", "meg_next_chat_bootstrap_prompt_md", "weather_bot_packet_md"},
    "completed phase0a artifact": {"non_source_fetching_scope_inventory", "market_contract_static_inventory", "canonical_identifier_static_audit", "no_lookahead_policy_documentation", "fail_closed_error_taxonomy_planning", "stage2_metadata_contract_documentation", "paper_trade_readiness_gap_inventory", "evaluation_metrics_planning", "operator_workflow_planning", "supplied_market_contract_input_planning", "settlement_rule_interpreter_planning", "no_lookahead_validation_planning", "fail_closed_validation_planning"},
    "blocked work": BLOCKED, "implementation posture": IMPLEMENTATION,
    "recommended next track": {"weather_bot_phase0a_next_chat_bootstrap_or_hold"},
    "conditional next track": {"weather_bot_phase0a_handoff_refresh_revision_if_scope_too_broad"},
    "evidence status": {"phase_summary_and_handoff_refresh_recorded"}, "label confidence": {"confirmed"},
}
REQUIRED_ASSIGNMENTS = {(field, value) for field, values in ALLOWED.items() for value in values}
FORBIDDEN_APPROVAL = re.compile(r"(source fetching is approved|provider connector is approved|runtime validation is approved|trading is approved|autonomy is approved|production behavior is approved|owner decision is revised|silence is approval|continuation is approval|non-interference is approval)", re.I)


def _read(path: Path = PRD) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<body>.*?)(?:\n## |\Z)", text, re.S | re.M)
    assert match, heading
    assert match.group("body").strip(), heading
    return match.group("body")


def _pairs(text: str) -> set[tuple[str, str]]:
    return {(m.group("field"), m.group("value")) for m in ASSIGNMENT_RE.finditer(_section(text, MACHINE_HEADING))}


def test_prd_exists_canonical_id_and_required_sections_are_non_empty() -> None:
    assert PRD.exists()
    text = _read()
    assert text.startswith(f"# {CANONICAL_ID} — Weather Bot Phase 0A Phase Summary and Handoff Refresh")
    assert f"Canonical ID: {CANONICAL_ID}" in text
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_test_is_stdlib_only_and_no_production_imports() -> None:
    tree = ast.parse(TEST.read_text(encoding="utf-8"))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    assert set(imports) <= {"__future__", "ast", "re", "pathlib"}
    assert all(not name.startswith("meg") for name in imports)


def test_static_scope_no_meg_runtime_owner_revision_or_pr283_predecessor() -> None:
    text = _read()
    for phrase in [
        "docs/static-test-only/meta-handoff-refresh-only", "This ticket does not modify `meg/`",
        "This ticket does not modify runtime code", "does not revise the owner decision",
        "does not reopen source-fetching implementation planning", "PR #283 remains excluded unless explicitly merged",
        "Source fetching remains not implemented", "Implementation approval remains not granted",
    ]:
        assert phrase in text
    assert not FORBIDDEN_APPROVAL.search(text)
    assert "modified `meg/`" not in text


def test_post_pr301_controls_all_refreshed_handoff_docs_and_bootstrap_safety() -> None:
    for path in META_DOCS:
        text = _read(path)
        assert "Post-PR #301" in text
        assert text.index("Post-PR #301") < text.find("Post-PR #280") if "Post-PR #280" in text else True
        assert "PR #283 remains excluded unless explicitly merged" in text
    boot = _read(ROOT / "docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md")
    assert "Do not create tickets until the user asks" in boot
    for phrase in ["source fetching", "provider connectors", "runtime validation", "scoring", "backtesting", "paper trading", "trading", "autonomy", "production", "persistence", "reports", "export"]:
        assert phrase in boot


def test_artifacts_blocked_values_canonical_stage2_and_refreshed_docs_are_recorded() -> None:
    text = _read()
    for artifact in ARTIFACTS:
        assert artifact in text
    for value in BLOCKED:
        assert value in text
    pairs = _pairs(text)
    assert {v for f, v in pairs if f == "canonical routing field"} == {"condition_id", "token_id", "outcome"}
    assert ("non routing field", "market_id") in pairs
    assert ("identifier relationship", "token_outcome_pair_derived_relationship") in pairs
    assert {v for f, v in pairs if f == "stage2 metadata posture"} == {"supplied_metadata_only", "fail_closed"}
    assert {v for f, v in pairs if f == "refreshed handoff file"} == {"meg_active_state_md", "meg_chat_handoff_md", "meg_next_chat_bootstrap_prompt_md", "weather_bot_packet_md"}


def test_machine_checkable_assignments_are_section_scoped_complete_and_allowed() -> None:
    pairs = _pairs(_read())
    assert pairs == REQUIRED_ASSIGNMENTS
    for field, value in pairs:
        assert field in ALLOWED
        assert value in ALLOWED[field]


def test_machine_checkable_parser_ignores_assignments_after_next_heading() -> None:
    synthetic = f"## {MACHINE_HEADING}\n- label confidence: confirmed\n\n## Acceptance criteria\n- label confidence: invalid_after_heading\n"
    assert _pairs(synthetic) == {("label confidence", "confirmed")}


def test_next_tracks_are_not_standalone_self_review() -> None:
    pairs = _pairs(_read())
    assert ("recommended next track", "weather_bot_phase0a_next_chat_bootstrap_or_hold") in pairs
    assert {v for f, v in pairs if f == "conditional next track"} == {"weather_bot_phase0a_handoff_refresh_revision_if_scope_too_broad"}
    assert all("self_review" not in value and "self-review" not in value for field, value in pairs if field in {"recommended next track", "conditional next track"})
