"""Static checks for Source Fetching Runtime Owner Decision Revision 01."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "SOURCE-FETCHING-RUNTIME-OWNER-DECISION-REVISION-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_source_fetching_runtime_owner_decision_revision_01.py"
MACHINE_HEADING = "## Machine-checkable source-fetching runtime owner-decision revision assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to Weather Bot Phase 0A meta-refresh self-review",
    "Owner-decision revision objective",
    "Previous owner decision",
    "Revised owner decision",
    "Revision rationale",
    "Scope unlocked by this revision",
    "Scope still blocked by this revision",
    "Non-approval boundary",
    "Source fetching implementation boundary",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Audit report and export boundary",
    "Canonical identifier posture",
    "Stage 2 runtime metadata posture",
    "Recommended next ticket",
    "Machine-checkable source-fetching runtime owner-decision revision assignments",
    "Acceptance criteria",
)
STAGE2_ARTIFACT_PATHS = {
    "meg/weather/stage2/source_identity_runtime.py",
    "meg/weather/stage2/retrieval_context_runtime.py",
    "meg/weather/stage2/provider_source_family_runtime.py",
    "meg/weather/stage2/manual_review_gate_runtime.py",
    "meg/weather/stage2/no_lookahead_metadata_runtime.py",
    "meg/weather/stage2/fail_closed_validation_runtime.py",
    "meg/weather/stage2/static_audit_surface_runtime.py",
}
UNLOCKED_SCOPE = {
    "source_fetching_runtime_implementation_plan_ticket",
    "docs_static_test_only_implementation_planning",
    "provider_source_boundary_planning",
    "credential_config_boundary_planning",
    "generated_data_fixture_boundary_planning",
    "scoring_backtesting_boundary_planning",
    "audit_output_boundary_planning",
    "acceptance_criteria_planning",
}
BLOCKED_SCOPE = {
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
    "weather bot planning stage": {"source_fetching_runtime_owner_decision_revision"},
    "owner decision revision status": {"docs_static_test_only", "owner_decision_revision_only", "post_weather_bot_phase0a_meta_refresh_self_review"},
    "previous owner decision": {"hold_source_fetching_runtime_track"},
    "revised owner decision": {"approve_narrow_source_fetching_runtime_implementation_plan"},
    "revision rationale": {"weather_bot_phase0a_meta_refresh_self_review_complete", "source_fetching_track_previously_closed_held", "owner_explicitly_revises_decision", "implementation_plan_needed_before_any_runtime_work", "narrow_planning_only_unlock_selected", "source_fetching_implementation_still_blocked", "provider_execution_still_blocked", "trading_autonomy_production_still_blocked"},
    "unlocked scope": UNLOCKED_SCOPE,
    "blocked scope": BLOCKED_SCOPE,
    "stage2 runtime metadata artifact": {"source_identity_runtime_py", "retrieval_context_runtime_py", "provider_source_family_runtime_py", "manual_review_gate_runtime_py", "no_lookahead_metadata_runtime_py", "fail_closed_validation_runtime_py", "static_audit_surface_runtime_py"},
    "implementation posture": {"docs_static_test_only", "owner_decision_revision_only", "no_runtime_code_change", "no_source_fetching", "no_source_fetching_implementation", "no_provider_connector", "no_provider_client", "no_live_provider_fetching", "no_credential_config_loading", "no_generated_data", "no_fixture_change", "no_scoring_backtesting", "no_trading_autonomy_production", "no_report_writing", "no_external_export", "no_persistence"},
    "recommended next track": {"source_fetching_runtime_owner_decision_revision_self_review"},
    "conditional next track": {"source_fetching_runtime_owner_decision_revision_if_scope_too_broad"},
    "evidence status": {"owner_decision_revision_recorded"},
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
    assert text.startswith("# SOURCE-FETCHING-RUNTIME-OWNER-DECISION-REVISION-01 — Source Fetching Runtime Owner Decision Revision")
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


def test_docs_static_owner_decision_revision_scope_and_no_forbidden_file_posture() -> None:
    text = _read()
    for phrase in [
        "docs/static-test-only/owner-decision-revision-only",
        "This ticket does not modify `meg/`",
        "This ticket does not modify meta/handoff files",
        "records an owner-decision revision after `WEATHER-BOT-PHASE0A-META-REFRESH-SELF-REVIEW-01`",
        "not source-fetching implementation planning",
    ]:
        assert phrase in text


def test_weather_bot_previous_and_revised_owner_decision() -> None:
    text = _read()
    for phrase in [
        "Weather Bot models the market settlement rule, not generic weather",
        "previous owner decision was `hold_source_fetching_runtime_track`",
        "Revised owner decision: approve_narrow_source_fetching_runtime_implementation_plan",
        "only unlocks a future docs/static-test-only implementation-plan ticket",
        "Source fetching remains not implemented",
        "Implementation remains not performed",
        "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
    ]:
        assert phrase in text


def test_no_unsafe_implementation_execution_or_approval_is_recorded() -> None:
    text = _read()
    lower_text = text.lower()
    for prefix, suffix in UNSAFE_APPROVAL_PATTERN_PARTS:
        assert f"{prefix} {suffix}" not in lower_text
    for phrase in [
        "It does not approve source-fetching implementation",
        "Provider connectors remain not created and not approved",
        "Provider clients remain not created",
        "Live provider/source fetching remains not executed and not approved",
        "Forecast pulls, API calls, scraping, file downloads, and provider SDK usage remain not approved and not performed",
        "Credentials/config loading remains not approved",
        "Generated data and fixtures remain not approved",
        "Scoring/backtesting remains not approved",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
        "Silence, continuation, lack of objection, and non-interference are not approval",
    ]:
        assert phrase in text


def test_stage2_artifact_paths_and_metadata_posture() -> None:
    text = _read()
    for path in STAGE2_ARTIFACT_PATHS:
        assert f"`{path}`" in text
    assert "supplied-metadata-only and fail-closed" in _section(text, "Stage 2 runtime metadata posture")


def test_unlocked_scope_is_complete_and_limited_to_planning_only_values() -> None:
    section = _section(_read(), "Scope unlocked by this revision")
    listed_values = set(re.findall(r"^- `([^`]+)`$", section, re.MULTILINE))
    assert listed_values == UNLOCKED_SCOPE
    assert all(
        value.endswith("_planning")
        or value == "source_fetching_runtime_implementation_plan_ticket"
        for value in listed_values
    )


def test_blocked_scope_is_complete() -> None:
    section = _section(_read(), "Scope still blocked by this revision")
    for value in BLOCKED_SCOPE:
        assert f"`{value}`" in section


def test_canonical_identifier_contract_and_no_legacy_market_routing() -> None:
    section = _section(_read(), "Canonical identifier posture")
    for value in ("`condition_id`", "`token_id`", "`outcome`"):
        assert value in section
    assert "No routing on `" + "market_" + "id" + "` is introduced or approved" in section


def test_machine_assignments_are_section_scoped_complete_and_allowed() -> None:
    assignments = _assignments_from(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    assert assignments == ALLOWED_ASSIGNMENTS


def test_machine_assignment_parser_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        "# doc\n\n## Machine-checkable source-fetching runtime owner-decision revision assignments\n\n"
        "- label confidence: confirmed\n\n## Acceptance criteria\n\n"
        "- label confidence: forbidden_after_next_heading\n"
    )
    assert _assignments_from(synthetic) == {"label confidence": {"confirmed"}}


def test_recommended_next_track_is_docs_static_self_review_not_implementation() -> None:
    section = _section(_read(), "Recommended next ticket")
    assert "`source_fetching_runtime_owner_decision_revision_self_review`" in section
    assert "docs/static-test-only self-review and not implementation" in section
    assert "must not implement source fetching" in section
