"""Static checks for Weather Bot Phase 0A fail-closed error taxonomy planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-FAIL-CLOSED-ERROR-TAXONOMY-PLANNING-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_fail_closed_error_taxonomy_planning_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A fail-closed error-taxonomy-planning assignments"
NEXT_TRACK = "weather_bot_phase0a_stage2_metadata_contract_documentation"
CONDITIONAL_TRACK = "weather_bot_phase0a_fail_closed_error_taxonomy_revision_if_scope_too_broad"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to no-lookahead policy documentation", "Taxonomy objective",
    "Current held/closed source-fetching posture", "No owner-decision revision boundary",
    "Fail-closed taxonomy overview", "Source and provider error categories",
    "Timestamp and no-lookahead error categories", "Settlement-rule ambiguity error categories",
    "Canonical identifier error categories", "Manual-review gate error categories",
    "Generated-data and fixture error categories", "Scoring and backtesting error categories",
    "Trading and production error categories", "Operator decision error categories",
    "Fail-closed action labels", "Static taxonomy only boundary", "Canonical identifier posture",
    "Source-fetching track remains blocked", "Provider/source execution boundary", "Credential/config boundary",
    "Generated-data and fixture boundary", "Scoring/backtesting boundary", "Paper-trade boundary",
    "Trading/autonomy/production boundary", "Audit report and export boundary",
    "Stage 2 runtime metadata posture", "Embedded self-review requirement", "Recommended next ticket",
    MACHINE_HEADING, "Acceptance criteria",
)
FAIL_CLOSED_ERROR_CATEGORIES = {'settlement_rule_ambiguous', 'condition_id_missing', 'source_ambiguous', 'timestamp_conflict', 'production_behavior_attempted', 'backtesting_attempted', 'outcome_missing', 'market_identifier_routing_attempt', 'timestamp_ambiguous', 'timestamp_missing', 'settlement_rule_conflict', 'location_ambiguous', 'measurement_unit_ambiguous', 'provider_unavailable', 'paper_trade_attempted', 'trading_attempted', 'token_outcome_pair_mismatch', 'source_missing', 'provider_unapproved', 'settlement_rule_missing', 'operator_decision_ambiguous', 'external_export_attempted', 'token_id_missing', 'lookahead_status_unknown', 'generated_data_detected', 'credential_config_required', 'lookahead_violation_detected', 'manual_review_required', 'fixture_data_detected', 'operator_decision_missing', 'threshold_ambiguous', 'comparator_ambiguous', 'source_conflict', 'unsupported_weather_measurement', 'scoring_attempted', 'time_window_ambiguous'}
FAIL_CLOSED_ACTION_LABELS = {'reject_scoring_backtesting_trading', 'preserve_hold_state', 'require_runtime_implementation_approval', 'reject_generated_or_fixture_data', 'reject_market_identifier_routing', 'block_processing', 'require_scope_revision', 'reject_lookahead_evidence', 'require_source_fetching_approval', 'reject_external_export', 'require_manual_review'}
BLOCKED_WORK = {'scoring_implementation', 'file_download_execution', 'production_behavior', 'provider_client_creation', 'source_fetching_runtime_implementation_plan', 'operator_decision_execution', 'provider_sdk_execution', 'provider_connector_implementation', 'forecast_pull_execution', 'owner_decision_revision', 'generated_data_creation', 'manual_review_ui', 'order_placement', 'no_lookahead_runtime_enforcement', 'settlement_rule_runtime_parser', 'manual_review_runtime_workflow', 'fail_closed_runtime_enforcement', 'fixture_data_modification', 'standalone_self_review_prd_artifact', 'autonomy_behavior', 'audit_output_persistence', 'api_call_execution', 'live_provider_source_fetching', 'credentials_config_loading', 'manual_review_persistence', 'timestamp_runtime_validation', 'audit_report_generation', 'runtime_error_handling', 'settlement_rule_runtime_classification', 'source_fetching_implementation', 'runtime_trading_behavior', 'backtesting_implementation', 'external_export_behavior', 'paper_trade_execution', 'scraping_execution'}
STAGE2_PATHS = {
    "meg/weather/stage2/source_identity_runtime.py",
    "meg/weather/stage2/retrieval_context_runtime.py",
    "meg/weather/stage2/provider_source_family_runtime.py",
    "meg/weather/stage2/manual_review_gate_runtime.py",
    "meg/weather/stage2/no_lookahead_metadata_runtime.py",
    "meg/weather/stage2/fail_closed_validation_runtime.py",
    "meg/weather/stage2/static_audit_surface_runtime.py",
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_phase0a_fail_closed_error_taxonomy_planning"},
    "fail closed taxonomy status": {"docs_static_test_only", "fail_closed_error_taxonomy_planning_only", "post_weather_bot_phase0a_no_lookahead_policy_documentation"},
    "self review posture": {"embedded_secondary_prompt_only", "no_standalone_self_review_prd"},
    "owner decision posture": {"no_owner_decision_revision", "hold_source_fetching_runtime_track_preserved"},
    "source fetching track posture": {"closed_held", "no_source_fetching_implementation_plan", "no_source_fetching_implementation", "implementation_approval_not_granted"},
    "fail closed error category": FAIL_CLOSED_ERROR_CATEGORIES,
    "fail closed action label": FAIL_CLOSED_ACTION_LABELS,
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "identifier relationship": {"token_outcome_pair_derived_relationship", "condition_token_outcome_preserved", "token_id_outcome_relationship_preserved"},
    "blocked work": BLOCKED_WORK,
    "stage2 runtime metadata artifact": {"source_identity_runtime_py", "retrieval_context_runtime_py", "provider_source_family_runtime_py", "manual_review_gate_runtime_py", "no_lookahead_metadata_runtime_py", "fail_closed_validation_runtime_py", "static_audit_surface_runtime_py"},
    "implementation posture": {'fail_closed_error_taxonomy_planning_only', 'no_timestamp_runtime_validation', 'no_provider_connector', 'no_settlement_rule_runtime_parser', 'no_generated_data', 'no_fail_closed_runtime_enforcement', 'no_runtime_code_change', 'no_trading_autonomy_production', 'no_scoring_backtesting', 'no_runtime_error_handling', 'no_persistence', 'no_provider_client', 'no_manual_review_runtime_workflow', 'no_source_fetching_plan', 'no_credential_config_loading', 'no_live_provider_fetching', 'no_paper_trade_execution', 'no_source_fetching', 'no_report_writing', 'no_no_lookahead_runtime_enforcement', 'docs_static_test_only', 'no_fixture_change', 'no_external_export', 'no_owner_decision_revision'},
    "recommended next track": {NEXT_TRACK},
    "conditional next track": {CONDITIONAL_TRACK},
    "evidence status": {"fail_closed_error_taxonomy_planning_recorded"},
    "label confidence": {"confirmed"},
}
REQUIRED_ASSIGNMENTS = {(k, v) for k, values in ALLOWED_ASSIGNMENTS.items() for v in values}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
FORBIDDEN_APPROVAL_RE = re.compile(
    r"revised " "owner decision|approve_narrow_source_fetching_runtime" "_implementation_plan|"
    r"provider connector " "is approved|provider client " "is created|source fetching " "is approved|"
    r"source fetching implementation " "is approved|source fetching implementation planning " "is approved|"
    r"source fetching implementation plan " "is approved|live provider source fetching " "is approved|"
    r"forecast pull " "is approved|api call " "is approved|scraping " "is approved|file download " "is approved|"
    r"provider sdk " "is approved|credentials.*loading " "is approved|generated data " "is approved|"
    r"fixture change " "is approved|fail-closed enforcement " "is approved|fail closed enforcement " "is approved|"
    r"runtime error handling " "is approved|no-lookahead enforcement " "is approved|no lookahead enforcement " "is approved|"
    r"timestamp validation " "is approved|settlement rule parser " "is approved|"
    r"settlement rule classification " "is approved|manual review workflow " "is approved|"
    r"manual review ui " "is approved|manual review persistence " "is approved|operator decision execution " "is approved|"
    r"paper trade execution " "is approved|scoring " "is approved|backtesting " "is approved|trading " "is approved|"
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
    section = _section(text, MACHINE_HEADING)
    return {(m.group("field"), m.group("value")) for m in ASSIGNMENT_RE.finditer(section)}


def test_document_exists_canonical_id_and_sections_are_non_empty() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert text.startswith(f"# {CANONICAL_ID} — Weather Bot Phase 0A Fail-Closed Error Taxonomy Planning")
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
        "docs/static-test-only/fail-closed-error-taxonomy-planning-only",
        "This ticket does not modify `meg/`", "This ticket does not modify meta/handoff files",
        "does not revise the owner decision", "does not reopen source-fetching implementation planning",
        "does not fetch, create, or modify market data", "does not create fixtures or generated data",
        "does not implement runtime fail-closed enforcement", "does not implement runtime error handling",
        "does not implement runtime no-lookahead enforcement", "does not implement runtime timestamp validation",
        "does not implement runtime settlement-rule parsing or classification",
        "does not implement runtime manual-review workflow behavior",
        "does not implement scoring, backtesting, paper trading, trading, or autonomy",
        "does not create a separate standalone self-review artifact",
        "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work",
        "source-fetching runtime track remains closed/held", "closed owner decision remains `hold_source_fetching_runtime_track`",
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


def test_taxonomy_values_action_labels_blocked_work_and_stage2_paths_appear() -> None:
    text = _read()
    for value in FAIL_CLOSED_ERROR_CATEGORIES | FAIL_CLOSED_ACTION_LABELS | BLOCKED_WORK | STAGE2_PATHS:
        assert value in text


def test_execution_approval_boundaries_are_present() -> None:
    text = _read()
    required = [
        "Provider connectors remain not approved", "Provider clients remain not created",
        "Forecast pull execution, API call execution, scraping execution, file download execution, and provider SDK execution remain not approved",
        "Credentials/config loading remains not approved", "Generated data and fixtures remain not approved",
        "does not implement runtime fail-closed enforcement", "does not implement runtime error handling",
        "Scoring/backtesting remains not approved", "Paper-trade execution remains not approved",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
    ]
    for phrase in required:
        assert phrase in text


def test_canonical_identifier_posture_is_preserved() -> None:
    section = _section(_read(), "Canonical identifier posture")
    assert "Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`" in section
    assert "Future reasoning must preserve all three canonical shared-rail identifiers" in section
    assert "Future reasoning must preserve the relationship between `token_id` and `outcome`" in section
    assert "`token_outcome_pair` remains a derived relationship, not a replacement for canonical fields" in section
    assert "`market_id` remains explicitly non-routing only" in section
    assert "No routing on `market_id` is introduced or approved" in section
    assert "`market_identifier_routing_attempt` must be documented as fail-closed" in section


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
    assert by_field["recommended next track"] == {NEXT_TRACK}
    assert by_field["conditional next track"] == {CONDITIONAL_TRACK}
    assert "self_review" not in NEXT_TRACK
    assert by_field["conditional next track"] == {"weather_bot_phase0a_fail_closed_error_taxonomy_revision_if_scope_too_broad"}


def test_machine_assignment_parser_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        "## Machine-checkable Weather Bot Phase 0A fail-closed error-taxonomy-planning assignments\n"
        "- label confidence: confirmed\n\n"
        "## Acceptance criteria\n"
        "- label confidence: invalid_after_next_heading\n"
    )
    assert _assignment_pairs(synthetic) == {("label confidence", "confirmed")}


def test_forbidden_approval_language_is_absent_and_regex_catches_unsafe_examples() -> None:
    combined = _read() + "\n" + TEST_PATH.read_text(encoding="utf-8")
    assert not FORBIDDEN_APPROVAL_RE.search(combined)
    unsafe_examples = [
        "revised " "owner decision", "source fetching implementation planning " "is approved",
        "fail-closed enforcement " "is approved", "runtime error handling " "is approved",
        "no-lookahead enforcement " "is approved", "timestamp validation " "is approved",
        "manual review workflow " "is approved", "settlement rule parser " "is approved",
        "paper trade execution " "is approved", "trading " "is approved", "report writing " "is approved",
        "silence " "is approval",
    ]
    for example in unsafe_examples:
        assert FORBIDDEN_APPROVAL_RE.search(example)
    allowed_negative_contexts = [
        "No owner-decision revision is being made in this ticket.",
        "This ticket does not revise the owner decision.",
        "Provider connectors remain not approved.",
        "Runtime trading/order placement/autonomy/production remains not approved.",
    ]
    for example in allowed_negative_contexts:
        assert not FORBIDDEN_APPROVAL_RE.search(example)
