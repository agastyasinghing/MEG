"""Static checks for Weather Bot Phase 0A non-source-fetching scope inventory."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-NON-SOURCE-FETCHING-SCOPE-INVENTORY-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_non_source_fetching_scope_inventory_01.py"
MACHINE_HEADING = "## Machine-checkable Weather Bot Phase 0A non-source-fetching scope-inventory assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to Weather Bot Phase 0A meta-refresh self-review",
    "Inventory objective",
    "Current held/closed source-fetching posture",
    "No owner-decision revision boundary",
    "Non-source-fetching work allowed to inventory",
    "Non-source-fetching work not yet approved for implementation",
    "Source-fetching track remains blocked",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Audit report and export boundary",
    "Canonical identifier posture",
    "Stage 2 runtime metadata posture",
    "Recommended next ticket",
    "Machine-checkable Weather Bot Phase 0A non-source-fetching scope-inventory assignments",
    "Acceptance criteria",
)
SAFE_INVENTORY_LANES = {
    "market_contract_static_inventory",
    "canonical_identifier_static_audit",
    "settlement_rule_taxonomy_planning",
    "manual_review_checklist_planning",
    "no_lookahead_policy_documentation",
    "fail_closed_error_taxonomy_planning",
    "stage2_metadata_contract_documentation",
    "paper_trade_readiness_gap_inventory",
    "evaluation_metric_taxonomy_planning",
    "operator_review_workflow_planning",
}
BLOCKED_WORK = {
    "owner_decision_revision",
    "source_fetching_runtime_implementation_plan",
    "source_fetching_implementation",
    "provider_connector_implementation",
    "provider_client_creation",
    "live_provider_source_fetching",
    "forecast_pull_execution",
    "api_call_execution",
    "scraping_execution",
    "file_download_execution",
    "provider_sdk_execution",
    "credentials_config_loading",
    "generated_data_creation",
    "fixture_data_modification",
    "scoring_implementation",
    "backtesting_implementation",
    "runtime_trading_behavior",
    "order_placement",
    "autonomy_behavior",
    "production_behavior",
    "audit_report_generation",
    "audit_output_persistence",
    "external_export_behavior",
}
STAGE2_ARTIFACT_PATHS = {
    "meg/weather/stage2/source_identity_runtime.py",
    "meg/weather/stage2/retrieval_context_runtime.py",
    "meg/weather/stage2/provider_source_family_runtime.py",
    "meg/weather/stage2/manual_review_gate_runtime.py",
    "meg/weather/stage2/no_lookahead_metadata_runtime.py",
    "meg/weather/stage2/fail_closed_validation_runtime.py",
    "meg/weather/stage2/static_audit_surface_runtime.py",
}
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_phase0a_non_source_fetching_scope_inventory"},
    "scope inventory status": {
        "docs_static_test_only",
        "non_source_fetching_scope_inventory_only",
        "post_weather_bot_phase0a_meta_refresh_self_review",
    },
    "owner decision posture": {
        "no_owner_decision_revision",
        "hold_source_fetching_runtime_track_preserved",
    },
    "source fetching track posture": {
        "closed_held",
        "no_source_fetching_implementation_plan",
        "no_source_fetching_implementation",
        "implementation_approval_not_granted",
    },
    "safe inventory lane": SAFE_INVENTORY_LANES,
    "blocked work": BLOCKED_WORK,
    "stage2 runtime metadata artifact": {
        "source_identity_runtime_py",
        "retrieval_context_runtime_py",
        "provider_source_family_runtime_py",
        "manual_review_gate_runtime_py",
        "no_lookahead_metadata_runtime_py",
        "fail_closed_validation_runtime_py",
        "static_audit_surface_runtime_py",
    },
    "implementation posture": {
        "docs_static_test_only",
        "non_source_fetching_scope_inventory_only",
        "no_runtime_code_change",
        "no_owner_decision_revision",
        "no_source_fetching",
        "no_source_fetching_plan",
        "no_provider_connector",
        "no_provider_client",
        "no_live_provider_fetching",
        "no_credential_config_loading",
        "no_generated_data",
        "no_fixture_change",
        "no_scoring_backtesting",
        "no_trading_autonomy_production",
        "no_report_writing",
        "no_external_export",
        "no_persistence",
    },
    "recommended next track": {"weather_bot_phase0a_non_source_fetching_scope_inventory_self_review"},
    "conditional next track": {"weather_bot_phase0a_non_source_fetching_scope_inventory_revision_if_scope_too_broad"},
    "evidence status": {"non_source_fetching_scope_inventory_recorded"},
    "label confidence": {"confirmed"},
}
UNSAFE_APPROVAL_PATTERN_PARTS = (
    ("provider connector", "is approved"),
    ("provider client", "is created"),
    ("source fetching", "is approved"),
    ("source fetching implementation", "is approved"),
    ("source fetching implementation planning", "is approved"),
    ("source fetching implementation plan", "is approved"),
    ("live provider source fetching", "is approved"),
    ("forecast pull", "is approved"),
    ("api call", "is approved"),
    ("scraping", "is approved"),
    ("file download", "is approved"),
    ("provider sdk", "is approved"),
    ("credentials loading", "is approved"),
    ("credentials/config loading", "is approved"),
    ("generated data", "is approved"),
    ("fixture change", "is approved"),
    ("scoring", "is approved"),
    ("backtesting", "is approved"),
    ("trading", "is approved"),
    ("order placement", "is approved"),
    ("autonomy", "is approved"),
    ("production behavior", "is approved"),
    ("report writing", "is approved"),
    ("external export", "is approved"),
    ("persistence", "is approved"),
    ("silence", "is approval"),
    ("continuation", "is approval"),
    ("non-interference", "is approval"),
)
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)


def _read() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, f"Missing section: {heading}"
    assert match.group("section").strip(), f"Section is empty: {heading}"
    return match.group("section")


def _assignments_from(text: str) -> dict[str, set[str]]:
    section = _section(text, MACHINE_HEADING.removeprefix("## "))
    result: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        result.setdefault(match.group("field"), set()).add(match.group("value"))
    return result


def test_document_exists_canonical_id_and_sections_are_non_empty() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert text.startswith("# WEATHER-BOT-PHASE0A-NON-SOURCE-FETCHING-SCOPE-INVENTORY-01 — Weather Bot Phase 0A Non-Source-Fetching Scope Inventory")
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
    assert imports == ["__future__", "ast", "re", "pathlib"]
    assert all(not name.startswith("meg") for name in imports)


def test_docs_static_inventory_scope_and_no_forbidden_file_scope() -> None:
    text = _read()
    for phrase in [
        "docs/static-test-only/non-source-fetching-scope-inventory-only",
        "This ticket does not modify `meg/`",
        "This ticket does not modify meta/handoff files",
        "This ticket does not revise the owner decision",
        "This ticket does not reopen source-fetching implementation planning",
        "not an owner-decision revision",
    ]:
        assert phrase in text


def test_weather_bot_and_source_fetching_posture() -> None:
    text = _read()
    for phrase in [
        "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work",
        "source-fetching runtime track remains closed/held",
        "closed owner decision remains `hold_source_fetching_runtime_track`",
        "Source fetching remains not implemented",
        "Implementation approval remains not granted",
        "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
    ]:
        assert phrase in text


def test_stage2_runtime_metadata_artifact_paths_appear() -> None:
    text = _read()
    for path in STAGE2_ARTIFACT_PATHS:
        assert f"`{path}`" in text


def test_safe_inventory_lanes_and_blocked_work_are_complete() -> None:
    allowed_section = _section(_read(), "Non-source-fetching work allowed to inventory")
    blocked_section = _section(_read(), "Source-fetching track remains blocked")
    for value in SAFE_INVENTORY_LANES:
        assert f"`{value}`" in allowed_section
    for value in BLOCKED_WORK:
        assert f"`{value}`" in blocked_section
    assert "These are only inventory lanes. This ticket must not implement any of them." in allowed_section


def test_no_provider_source_credential_data_fixture_execution_is_approved() -> None:
    text = _read()
    lower_text = text.lower()
    for prefix, suffix in UNSAFE_APPROVAL_PATTERN_PARTS:
        assert f"{prefix} {suffix}" not in lower_text
    for phrase in [
        "Provider connectors remain not approved",
        "Provider clients remain not created",
        "Live provider/source fetching remains not approved",
        "Forecast pulls, API calls, scraping, file downloads, and provider SDK usage remain not approved",
        "Credentials/config loading remains not approved",
        "Generated data and fixtures remain not approved",
    ]:
        assert phrase in text


def test_no_scoring_backtesting_trading_report_persistence_export_is_approved() -> None:
    text = _read()
    for phrase in [
        "Scoring/backtesting remains not approved",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
    ]:
        assert phrase in text


def test_canonical_identifier_contract_and_no_market_id_routing() -> None:
    section = _section(_read(), "Canonical identifier posture")
    for value in ("`condition_id`", "`token_id`", "`outcome`"):
        assert value in section
    assert "No routing on `market_id` is introduced or approved" in section


def test_machine_checkable_assignments_are_section_scoped_and_allowed() -> None:
    assignments = _assignments_from(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, values in assignments.items():
        assert values == ALLOWED_ASSIGNMENTS[field]


def test_synthetic_parser_scoping_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        "## Machine-checkable Weather Bot Phase 0A non-source-fetching scope-inventory assignments\n"
        "- label confidence: confirmed\n"
        "## Acceptance criteria\n"
        "- label confidence: forbidden_after_heading\n"
    )
    assert _assignments_from(synthetic) == {"label confidence": {"confirmed"}}


def test_recommended_next_track_is_self_review_not_owner_revision_or_implementation() -> None:
    text = _read()
    section = _section(text, "Recommended next ticket")
    assert "`weather_bot_phase0a_non_source_fetching_scope_inventory_self_review`" in section
    assert "secondary docs/static-test-only self-review prompt/pass" in section
    assert "must not revise the owner decision" in section
    assert "must not implement source fetching" in section
    assert "must not approve source-fetching implementation planning" in section
    assignments = _assignments_from(text)
    assert assignments["recommended next track"] == {"weather_bot_phase0a_non_source_fetching_scope_inventory_self_review"}
