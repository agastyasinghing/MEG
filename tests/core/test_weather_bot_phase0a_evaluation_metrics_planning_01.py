"""Static checks for Weather Bot Phase 0A evaluation metrics planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-EVALUATION-METRICS-PLANNING-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_evaluation_metrics_planning_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A evaluation-metrics-planning assignments"
NEXT_TRACK = "weather_bot_phase0a_operator_workflow_planning"
CONDITIONAL_TRACK = "weather_bot_phase0a_evaluation_metrics_revision_if_scope_too_broad"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to paper-trade readiness gap inventory", "Metrics planning objective",
    "Current held/closed source-fetching posture", "No owner-decision revision boundary",
    "Evaluation readiness status", "Evaluation metrics overview", "Market contract metrics",
    "Canonical identifier metrics", "Settlement-rule metrics", "Manual-review metrics", "No-lookahead metrics",
    "Fail-closed metrics", "Stage 2 metadata metrics", "Source and provider metrics", "Scoring metric candidates",
    "Backtesting metric candidates", "Paper-trade readiness metric candidates", "Auditability metric candidates",
    "Metric readiness blockers", "Static planning only boundary", "Canonical identifier posture",
    "Source-fetching track remains blocked", "Provider/source execution boundary", "Credential/config boundary",
    "Generated-data and fixture boundary", "Scoring/evaluation boundary", "Backtesting boundary", "Paper-trade boundary",
    "Trading/autonomy/production boundary", "Audit report and export boundary", "Stage 2 runtime metadata posture",
    "Embedded self-review requirement", "Recommended next ticket", MACHINE_HEADING, "Acceptance criteria",
)
EVALUATION_READINESS = {
    "not_evaluation_ready", "docs_static_metrics_planning_only", "scoring_not_implemented",
    "evaluation_execution_not_approved", "backtesting_not_implemented", "paper_trade_execution_not_approved",
    "source_fetching_not_implemented", "audit_metric_persistence_not_approved",
}
METRIC_CANDIDATES = {
    "metric_market_contract_coverage", "metric_canonical_identifier_preservation",
    "metric_token_outcome_pair_preservation", "metric_settlement_rule_interpretability",
    "metric_manual_review_required_rate", "metric_manual_review_reason_coverage",
    "metric_no_lookahead_policy_coverage", "metric_timestamp_availability_coverage",
    "metric_fail_closed_block_rate", "metric_fail_closed_reason_coverage",
    "metric_stage2_metadata_completeness", "metric_stage2_metadata_conflict_rate",
    "metric_provider_status_coverage", "metric_source_identity_coverage",
    "metric_scoring_candidate_brier_score", "metric_scoring_candidate_log_loss",
    "metric_scoring_candidate_calibration_error", "metric_scoring_candidate_resolution_accuracy",
    "metric_backtesting_candidate_sample_coverage", "metric_backtesting_candidate_no_lookahead_compliance",
    "metric_paper_trade_readiness_gap_count", "metric_paper_trade_blocker_count",
    "metric_auditability_field_coverage", "metric_export_blocker_coverage",
}
METRIC_BLOCKERS = {
    "block_source_fetching_unapproved", "block_scoring_not_implemented",
    "block_evaluation_execution_not_approved", "block_backtesting_not_implemented",
    "block_paper_trade_execution_not_approved", "block_no_lookahead_runtime_not_implemented",
    "block_fail_closed_runtime_not_implemented", "block_manual_review_runtime_not_implemented",
    "block_runtime_metadata_not_implemented", "block_metric_persistence_not_approved",
    "block_external_export_not_approved",
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
    "evaluation_execution", "metric_persistence", "backtesting_implementation", "paper_trade_execution",
    "paper_trade_readiness_runtime", "order_simulation", "runtime_trading_behavior", "order_placement",
    "autonomy_behavior", "production_behavior", "audit_report_generation", "audit_output_persistence",
    "external_export_behavior", "standalone_self_review_prd_artifact",
}
IMPLEMENTATION_POSTURES = {
    "docs_static_test_only", "evaluation_metrics_planning_only", "no_runtime_code_change",
    "no_stage2_runtime_module_modification", "no_runtime_metadata_implementation", "no_owner_decision_revision",
    "no_source_fetching", "no_source_fetching_plan", "no_provider_connector", "no_provider_client",
    "no_live_provider_fetching", "no_credential_config_loading", "no_generated_data", "no_fixture_change",
    "no_fail_closed_runtime_enforcement", "no_runtime_error_handling", "no_no_lookahead_runtime_enforcement",
    "no_timestamp_runtime_validation", "no_settlement_rule_runtime_parser", "no_manual_review_runtime_workflow",
    "no_scoring_implementation", "no_evaluation_execution", "no_metric_persistence", "no_backtesting_implementation",
    "no_paper_trade_execution", "no_order_simulation", "no_trading_autonomy_production", "no_report_writing",
    "no_external_export", "no_persistence",
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_phase0a_evaluation_metrics_planning"},
    "evaluation metrics status": {
        "docs_static_test_only", "evaluation_metrics_planning_only",
        "post_weather_bot_phase0a_paper_trade_readiness_gap_inventory",
    },
    "evaluation readiness status": EVALUATION_READINESS,
    "self review posture": {"embedded_secondary_prompt_only", "no_standalone_self_review_prd"},
    "owner decision posture": {"no_owner_decision_revision", "hold_source_fetching_runtime_track_preserved"},
    "source fetching track posture": {
        "closed_held", "no_source_fetching_implementation_plan", "no_source_fetching_implementation",
        "implementation_approval_not_granted",
    },
    "evaluation metric candidate": METRIC_CANDIDATES,
    "metric readiness blocker": METRIC_BLOCKERS,
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
    "evidence status": {"evaluation_metrics_planning_recorded"},
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
    r"operator decision execution " "is approved|scoring " "is approved|"
    r"evaluation execution " "is approved|metric persistence " "is approved|backtesting " "is approved|"
    r"paper trade execution " "is approved|paper trade readiness runtime " "is approved|"
    r"order simulation " "is approved|trading " "is approved|order placement " "is approved|"
    r"autonomy " "is approved|production behavior " "is approved|report writing " "is approved|"
    r"external export " "is approved|persistence " "is approved|silence " "is approval|"
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
    assert text.startswith(f"# {CANONICAL_ID} — Weather Bot Phase 0A Evaluation Metrics Planning")
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
        "docs/static-test-only/evaluation-metrics-planning-only",
        "This ticket does not modify `meg/`", "This ticket does not modify meta/handoff files",
        "does not modify Stage 2 runtime metadata modules", "does not revise the owner decision",
        "does not reopen source-fetching implementation planning", "does not fetch, create, or modify market data",
        "does not create fixtures or generated data", "does not implement runtime metadata behavior",
        "does not implement runtime fail-closed enforcement", "does not implement runtime error handling",
        "does not implement runtime no-lookahead enforcement", "does not implement runtime timestamp validation",
        "does not implement runtime settlement-rule parsing or classification",
        "does not implement runtime manual-review workflow behavior",
        "does not implement scoring, evaluation execution, backtesting, paper trading, trading, or autonomy",
        "does not execute paper trades", "does not create simulated orders",
        "does not create reports, persisted metrics, persisted audit output, or external exports",
        "does not create a separate standalone self-review artifact",
        "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work",
        "source-fetching runtime track remains closed/held",
        "closed owner decision remains `hold_source_fetching_runtime_track`",
        "Source fetching remains not implemented", "Implementation approval remains not granted",
        "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
        "Paper-trade readiness remains not achieved", "Provider connectors remain not approved",
        "Provider clients remain not created", "Live provider/source fetching remains not approved",
        "Credentials/config loading remains not approved", "Generated data and fixtures remain not approved",
        "Scoring/evaluation execution remains not approved", "Backtesting remains not approved",
        "Paper-trade execution remains not approved", "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, metric persistence, and external export remain not approved",
        "Silence, continuation, lack of objection, and non-interference are not approval",
    ]
    for phrase in required:
        assert phrase in text


def test_values_paths_and_blocked_work_appear() -> None:
    text = _read()
    for value in EVALUATION_READINESS | METRIC_CANDIDATES | METRIC_BLOCKERS | STAGE2_PATHS | BLOCKED_WORK:
        assert value in text


def test_evaluation_readiness_is_not_ready() -> None:
    section = _section(_read(), "Evaluation readiness status")
    for status in EVALUATION_READINESS:
        assert f"`{status}`" in section
    assert "`not_evaluation_ready`" in section


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
        "Scoring/evaluation execution remains not approved", "Backtesting remains not approved",
        "Paper-trade execution remains not approved", "does not create simulated orders",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, metric persistence, and external export remain not approved",
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
        "## Machine-checkable Weather Bot Phase 0A evaluation-metrics-planning assignments\n"
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
        "evaluation execution " "is approved", "metric persistence " "is approved",
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
