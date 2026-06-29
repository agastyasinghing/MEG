"""Static checks for Weather Bot Phase 0A Meta Refresh Self-Review."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-META-REFRESH-SELF-REVIEW-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_meta_refresh_self_review_01.py"
MACHINE_HEADING = "## Machine-checkable Weather Bot Phase 0A meta-refresh self-review assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to Weather Bot Phase 0A meta refresh",
    "Self-review objective",
    "Scope verification",
    "Meta file verification",
    "Document verification",
    "Static test verification",
    "Validation verification",
    "Safety and non-execution verification",
    "Canonical identifier verification",
    "Source-fetching track posture",
    "Stage 2 runtime metadata posture",
    "Remaining blocked work",
    "Non-approval boundary",
    "Recommended next ticket",
    "Machine-checkable Weather Bot Phase 0A meta-refresh self-review assignments",
    "Acceptance criteria",
)
META_FILES = {
    "docs/meta/MEG_ACTIVE_STATE.md",
    "docs/meta/MEG_CHAT_HANDOFF.md",
    "docs/meta/domain_packets/WEATHER_BOT_PACKET.md",
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
BLOCKED_WORK = {
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
ALLOWED_ASSIGNMENTS = {
    "weather bot planning stage": {"weather_bot_phase0a_meta_refresh_self_review"},
    "self review status": {"docs_static_test_only", "self_review_pass_only", "post_weather_bot_phase0a_meta_refresh"},
    "reviewed artifact": {"weather_bot_phase0a_meta_refresh_01"},
    "reviewed meta file": {"meg_active_state_md", "meg_chat_handoff_md", "weather_bot_packet_md"},
    "scope verification": {"no_meg_modification", "no_meta_file_modification", "no_runtime_code_change", "no_source_fetching_module", "no_provider_connector", "no_provider_client", "no_fixture_change", "no_generated_data", "no_workflow_change", "no_dependency_change", "no_schema_migration_change", "no_credentials_config_change", "no_scoring_backtesting_change", "no_trading_autonomy_production_change", "no_report_export_persistence_change"},
    "document verification": {"title_and_canonical_id_confirmed", "required_sections_confirmed", "weather_bot_settlement_rule_confirmed", "source_fetching_track_closed_held_confirmed", "hold_source_fetching_runtime_track_confirmed", "stage2_metadata_supplied_only_confirmed", "stage2_metadata_fail_closed_confirmed"},
    "static test verification": {"stdlib_only_except_pytest", "no_production_imports", "parser_section_scoped", "closed_set_assignments", "unsafe_approvals_rejected"},
    "source fetching track state": {"source_fetching_runtime_track_closed_held", "hold_source_fetching_runtime_track", "source_fetching_not_implemented", "implementation_approval_not_granted", "future_reopen_requires_owner_decision_revision"},
    "stage2 runtime metadata artifact": {"source_identity_runtime_py", "retrieval_context_runtime_py", "provider_source_family_runtime_py", "manual_review_gate_runtime_py", "no_lookahead_metadata_runtime_py", "fail_closed_validation_runtime_py", "static_audit_surface_runtime_py"},
    "implementation posture": {"docs_static_test_only", "self_review_pass_only", "no_runtime_code_change", "no_source_fetching", "no_source_fetching_plan", "no_provider_connector", "no_provider_client", "no_live_provider_fetching", "no_credential_config_loading", "no_generated_data", "no_fixture_change", "no_scoring_backtesting", "no_trading_autonomy_production", "no_report_writing", "no_external_export", "no_persistence"},
    "recommended next track": {"weather_bot_phase0a_meta_refresh_revision_if_scope_too_broad"},
    "conditional next track": {"source_fetching_runtime_owner_decision_revision_if_owner_changes_decision"},
    "evidence status": {"self_review_pass_recorded"},
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
    assert text.startswith("# WEATHER-BOT-PHASE0A-META-REFRESH-SELF-REVIEW-01 — Weather Bot Phase 0A Meta Refresh Self-Review")
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


def test_docs_static_self_review_scope_and_predecessor_recorded() -> None:
    text = _read()
    for phrase in [
        "docs/static-test-only/self-review-pass-only",
        "This ticket does not modify `meg/`",
        "This ticket does not modify meta/handoff files",
        "records a self-review pass for `WEATHER-BOT-PHASE0A-META-REFRESH-01`",
        "safe to complete as this pass",
        "This pass completes `weather_bot_phase0a_meta_refresh_self_review`",
    ]:
        assert phrase in text


def test_weather_bot_and_phase0a_source_fetching_posture() -> None:
    text = _read()
    for phrase in [
        "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work",
        "source-fetching runtime track is closed/held",
        "closed owner decision is `hold_source_fetching_runtime_track`",
        "Source fetching remains not implemented",
        "Implementation approval remains not granted",
        "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
    ]:
        assert phrase in text


def test_meta_files_and_stage2_artifacts_are_verified() -> None:
    text = _read()
    for path in META_FILES:
        assert f"`{path}`" in text
    for path in STAGE2_ARTIFACT_PATHS:
        assert f"`{path}`" in text


def test_remaining_blocked_work_is_complete() -> None:
    section = _section(_read(), "Remaining blocked work")
    for value in BLOCKED_WORK:
        assert f"`{value}`" in section


def test_no_unsafe_implementation_or_execution_is_approved() -> None:
    text = _read()
    lower_text = text.lower()
    for prefix, suffix in UNSAFE_APPROVAL_PATTERN_PARTS:
        assert f"{prefix} {suffix}" not in lower_text
    for phrase in [
        "does not approve source-fetching implementation or implementation planning",
        "does not approve provider/source execution",
        "credentials/config loading",
        "generated data, fixture changes",
        "scoring, backtesting, trading, order placement, autonomy, production behavior",
        "report writing, persistence, or external export",
    ]:
        assert phrase in text


def test_canonical_identifier_contract_and_no_market_id_routing() -> None:
    section = _section(_read(), "Canonical identifier verification")
    for value in ("`condition_id`", "`token_id`", "`outcome`"):
        assert value in section
    assert "No routing on `market_id` is introduced or approved" in section


def test_machine_assignments_are_section_scoped_complete_and_allowed() -> None:
    assignments = _assignments_from(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    assert assignments == ALLOWED_ASSIGNMENTS


def test_machine_assignment_parser_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        "# doc\n\n## Machine-checkable Weather Bot Phase 0A meta-refresh self-review assignments\n\n"
        "- label confidence: confirmed\n\n## Acceptance criteria\n\n"
        "- label confidence: forbidden_after_next_heading\n"
    )
    assert _assignments_from(synthetic) == {"label confidence": {"confirmed"}}


def test_recommended_next_track_is_conditional_and_only_revision_if_scope_too_broad() -> None:
    text = _read()
    section = _section(text, "Recommended next ticket")
    expected = "weather_bot_phase0a_meta_refresh_revision_if_scope_too_broad"
    assert f"`{expected}`" in section
    assert "conditional only if reviewers want another pass or identify scope issues" in section
    assert "Otherwise, the meta-refresh self-review is complete as this pass" in section
    assert "Do not proceed to `source_fetching_runtime_implementation_plan`" in section
    assignments = _assignments_from(text)
    assert assignments["recommended next track"] == {expected}
