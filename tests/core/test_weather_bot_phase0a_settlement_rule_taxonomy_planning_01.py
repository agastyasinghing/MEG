"""Static checks for Weather Bot Phase 0A settlement-rule taxonomy planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-TAXONOMY-PLANNING-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_settlement_rule_taxonomy_planning_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A settlement-rule taxonomy-planning assignments"
NEXT_TRACK = "weather_bot_phase0a_manual_review_checklist_planning"
CONDITIONAL_TRACK = "weather_bot_phase0a_settlement_rule_taxonomy_revision_if_scope_too_broad"

REQUIRED_SECTIONS = (
    "Status and scope", "Relationship to canonical identifier static audit self-review",
    "Taxonomy objective", "Current held/closed source-fetching posture",
    "No owner-decision revision boundary", "Settlement-rule taxonomy overview",
    "Settlement text fields", "Resolution-source taxonomy", "Weather measurement taxonomy",
    "Time-window taxonomy", "Location taxonomy", "Threshold and comparator taxonomy",
    "Outcome mapping taxonomy", "Ambiguity and manual-review taxonomy",
    "Static planning only boundary", "Canonical identifier posture",
    "Source-fetching track remains blocked", "Provider/source execution boundary",
    "Credential/config boundary", "Generated-data and fixture boundary",
    "Scoring/backtesting boundary", "Trading/autonomy/production boundary",
    "Audit report and export boundary", "Stage 2 runtime metadata posture",
    "Embedded self-review requirement", "Recommended next ticket", MACHINE_HEADING,
    "Acceptance criteria",
)
SETTLEMENT_FIELDS = {
    "resolution_source_text", "settlement_rule_text", "question_text", "measurement_type",
    "measurement_unit", "measurement_threshold", "measurement_comparator",
    "measurement_window_start", "measurement_window_end", "event_location",
    "reporting_authority", "fallback_resolution_rule", "ambiguous_resolution_trigger",
    "manual_review_reason", "operator_review_required", "outcome_label", "token_outcome_pair",
}
WEATHER_MEASUREMENTS = {
    "temperature", "precipitation", "snowfall", "rainfall", "wind_speed",
    "hurricane_category", "air_quality_index", "weather_alert_presence",
    "other_weather_measurement_requires_review",
}
COMPARATORS = {
    "greater_than", "greater_than_or_equal", "less_than", "less_than_or_equal",
    "equal_to", "within_range", "presence_absence", "ambiguous_comparator_requires_review",
}
MANUAL_REVIEW = {
    "missing_resolution_source", "ambiguous_location", "ambiguous_time_window",
    "ambiguous_measurement_unit", "ambiguous_threshold", "ambiguous_comparator",
    "conflicting_source_text", "unsupported_weather_measurement", "operator_review_required",
}
BLOCKED_WORK = {
    "owner_decision_revision", "source_fetching_runtime_implementation_plan",
    "source_fetching_implementation", "provider_connector_implementation",
    "provider_client_creation", "live_provider_source_fetching", "forecast_pull_execution",
    "api_call_execution", "scraping_execution", "file_download_execution",
    "provider_sdk_execution", "credentials_config_loading", "generated_data_creation",
    "fixture_data_modification", "settlement_rule_runtime_parser",
    "settlement_rule_runtime_classification", "scoring_implementation",
    "backtesting_implementation", "runtime_trading_behavior", "order_placement",
    "autonomy_behavior", "production_behavior", "audit_report_generation",
    "audit_output_persistence", "external_export_behavior", "standalone_self_review_prd_artifact",
}
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
    "weather bot planning stage": {"weather_bot_phase0a_settlement_rule_taxonomy_planning"},
    "settlement taxonomy status": {"docs_static_test_only", "settlement_rule_taxonomy_planning_only", "post_weather_bot_phase0a_canonical_identifier_static_audit_self_review"},
    "self review posture": {"embedded_secondary_prompt_only", "no_standalone_self_review_prd"},
    "owner decision posture": {"no_owner_decision_revision", "hold_source_fetching_runtime_track_preserved"},
    "source fetching track posture": {"closed_held", "no_source_fetching_implementation_plan", "no_source_fetching_implementation", "implementation_approval_not_granted"},
    "settlement taxonomy field": SETTLEMENT_FIELDS,
    "weather measurement category": WEATHER_MEASUREMENTS,
    "comparator category": COMPARATORS,
    "manual review category": MANUAL_REVIEW,
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "identifier relationship": {"token_outcome_pair_derived_relationship", "condition_token_outcome_preserved", "token_id_outcome_relationship_preserved"},
    "blocked work": BLOCKED_WORK,
    "stage2 runtime metadata artifact": {"source_identity_runtime_py", "retrieval_context_runtime_py", "provider_source_family_runtime_py", "manual_review_gate_runtime_py", "no_lookahead_metadata_runtime_py", "fail_closed_validation_runtime_py", "static_audit_surface_runtime_py"},
    "implementation posture": {"docs_static_test_only", "settlement_rule_taxonomy_planning_only", "no_runtime_code_change", "no_owner_decision_revision", "no_source_fetching", "no_source_fetching_plan", "no_provider_connector", "no_provider_client", "no_live_provider_fetching", "no_credential_config_loading", "no_generated_data", "no_fixture_change", "no_settlement_rule_runtime_parser", "no_scoring_backtesting", "no_trading_autonomy_production", "no_report_writing", "no_external_export", "no_persistence"},
    "recommended next track": {NEXT_TRACK},
    "conditional next track": {CONDITIONAL_TRACK},
    "evidence status": {"settlement_rule_taxonomy_planning_recorded"},
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
    r"fixture change " "is approved|settlement rule parser " "is approved|"
    r"settlement rule classification " "is approved|scoring " "is approved|backtesting " "is approved|"
    r"trading " "is approved|order placement " "is approved|autonomy " "is approved|"
    r"production behavior " "is approved|report writing " "is approved|external export " "is approved|"
    r"persistence " "is approved|silence " "is approval|continuation " "is approval|"
    r"non-interference " "is approval",
    re.IGNORECASE,
)


def _read() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, f"Missing section: {heading}"
    assert match.group("section").strip(), f"Section is empty: {heading}"
    return match.group("section")


def _assignment_pairs(text: str) -> set[tuple[str, str]]:
    section = _section(text, MACHINE_HEADING)
    return {(m.group("field"), m.group("value")) for m in ASSIGNMENT_RE.finditer(section)}


def test_document_exists_canonical_id_and_sections_are_non_empty() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert text.startswith(f"# {CANONICAL_ID} — Weather Bot Phase 0A Settlement Rule Taxonomy Planning")
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
        "docs/static-test-only/settlement-rule-taxonomy-planning-only",
        "This ticket does not modify `meg/`", "This ticket does not modify meta/handoff files",
        "does not revise the owner decision", "does not reopen source-fetching implementation planning",
        "does not fetch, create, or modify market data", "does not create fixtures or generated data",
        "does not parse settlement rules in runtime code", "does not implement scoring, backtesting, trading, or autonomy",
        "does not create a separate standalone self-review artifact",
        "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work",
        "source-fetching runtime track remains closed/held", "closed owner decision remains `hold_source_fetching_runtime_track`",
        "Source fetching remains not implemented", "Implementation approval remains not granted",
        "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
        "Provider connectors remain not approved", "Provider clients remain not created",
        "Live provider/source fetching remains not approved", "Credentials/config loading remains not approved",
        "Generated data and fixtures remain not approved", "Scoring/backtesting remains not approved",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
        "Silence, continuation, lack of objection, and non-interference are not approval",
    ]
    for phrase in required:
        assert phrase in text


def test_taxonomy_values_and_stage2_paths_appear() -> None:
    text = _read()
    for value in SETTLEMENT_FIELDS | WEATHER_MEASUREMENTS | COMPARATORS | MANUAL_REVIEW | BLOCKED_WORK | STAGE2_PATHS:
        assert value in text


def test_canonical_identifier_posture_is_preserved() -> None:
    section = _section(_read(), "Canonical identifier posture")
    assert "Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`" in section
    assert "Future reasoning must preserve all three canonical shared-rail identifiers" in section
    assert "Future reasoning must preserve the relationship between `token_id` and `outcome`" in section
    assert "`token_outcome_pair` remains a derived relationship, not a replacement for canonical fields" in section
    assert "`market_id` remains explicitly non-routing only" in section
    assert "No routing on `market_id` is introduced or approved" in section


def test_machine_assignments_are_section_scoped_complete_and_allowed() -> None:
    pairs = _assignment_pairs(_read())
    assert pairs == REQUIRED_ASSIGNMENTS
    by_field: dict[str, set[str]] = {}
    for field, value in pairs:
        by_field.setdefault(field, set()).add(value)
    assert by_field["canonical routing field"] == {"condition_id", "token_id", "outcome"}
    assert by_field["non routing field"] == {"market_id"}
    assert by_field["recommended next track"] == {NEXT_TRACK}
    assert by_field["conditional next track"] == {CONDITIONAL_TRACK}
    assert "self_review" not in NEXT_TRACK


def test_machine_assignment_parser_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        "## Machine-checkable Weather Bot Phase 0A settlement-rule taxonomy-planning assignments\n"
        "- label confidence: confirmed\n\n"
        "## Acceptance criteria\n"
        "- label confidence: invalid_after_next_heading\n"
    )
    assert _assignment_pairs(synthetic) == {("label confidence", "confirmed")}


def test_forbidden_approval_language_is_absent_and_regex_catches_unsafe_examples() -> None:
    combined = _read() + "\n" + TEST_PATH.read_text(encoding="utf-8")
    assert not FORBIDDEN_APPROVAL_RE.search(combined)
    unsafe_examples = [
        "revised " "owner decision",
        "source fetching implementation planning " "is approved",
        "settlement rule parser " "is approved",
        "trading " "is approved",
        "report writing " "is approved",
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
