"""Static checks for Weather Bot Phase 0A canonical identifier static audit."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_canonical_identifier_static_audit_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A canonical-identifier static-audit assignments"
NEXT_TRACK = "weather_bot_phase0a_canonical_identifier_static_audit_self_review"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to market-contract static inventory self-review",
    "Audit objective",
    "Current held/closed source-fetching posture",
    "No owner-decision revision boundary",
    "Canonical identifier contract",
    "Condition identifier audit",
    "Token identifier audit",
    "Outcome identifier audit",
    "Outcome-token pairing audit",
    "Non-routing identifier boundary",
    "Market contract field relationship",
    "Static audit only boundary",
    "Source-fetching track remains blocked",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Audit report and export boundary",
    "Stage 2 runtime metadata posture",
    "Recommended next ticket",
    MACHINE_HEADING,
    "Acceptance criteria",
)
MARKET_CONTRACT_FIELD_RELATIONSHIPS = {
    "condition_id",
    "token_id",
    "outcome",
    "outcome_label",
    "token_outcome_pair",
    "question_text",
    "settlement_rule_text",
    "resolution_source_text",
    "operator_review_required",
    "manual_review_reason",
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
    "weather bot planning stage": {"weather_bot_phase0a_canonical_identifier_static_audit"},
    "canonical identifier audit status": {
        "docs_static_test_only",
        "canonical_identifier_static_audit_only",
        "post_weather_bot_phase0a_market_contract_static_inventory_self_review",
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
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "identifier relationship": {
        "token_outcome_pair_derived_relationship",
        "condition_token_outcome_preserved",
        "token_id_outcome_relationship_preserved",
    },
    "market contract field relationship": MARKET_CONTRACT_FIELD_RELATIONSHIPS,
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
        "canonical_identifier_static_audit_only",
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
    "recommended next track": {NEXT_TRACK},
    "conditional next track": {"weather_bot_phase0a_canonical_identifier_static_audit_revision_if_scope_too_broad"},
    "evidence status": {"canonical_identifier_static_audit_recorded"},
    "label confidence": {"confirmed"},
}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
UNSAFE_APPROVAL_PATTERN_PARTS = (
    ("revised " "owner decision", ""),
    ("approve_narrow_source_fetching_runtime" "_implementation_plan", ""),
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


def _read() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, f"Missing section: {heading}"
    assert match.group("section").strip(), f"Section is empty: {heading}"
    return match.group("section")


def _assignments_from(text: str) -> dict[str, set[str]]:
    section = _section(text, MACHINE_HEADING)
    result: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        result.setdefault(match.group("field"), set()).add(match.group("value"))
    return result


def test_document_exists_canonical_id_and_sections_are_non_empty() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert text.startswith(
        "# WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-01 — "
        "Weather Bot Phase 0A Canonical Identifier Static Audit"
    )
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


def test_required_static_audit_posture_and_scope_boundaries_are_present() -> None:
    text = _read()
    for phrase in [
        "docs/static-test-only/canonical-identifier-static-audit-only",
        "This ticket does not modify `meg/`",
        "This ticket does not modify meta/handoff files",
        "This ticket does not revise the owner decision",
        "does not reopen source-fetching implementation planning",
        "does not fetch, create, or modify market data",
        "does not create fixtures or generated data",
        "Weather Bot models the market settlement rule, not generic weather",
        "Weather Bot Phase 0A remains held and closed for source-fetching runtime work",
        "source-fetching runtime track remains closed/held",
        "closed owner decision remains `hold_source_fetching_runtime_track`",
        "Source fetching remains not implemented",
        "Implementation approval remains not granted",
        "Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed",
    ]:
        assert phrase in text


def test_canonical_routing_fields_are_exact_and_relationships_are_preserved() -> None:
    text = _read()
    contract = _section(text, "Canonical identifier contract")
    pairing = _section(text, "Outcome-token pairing audit")
    assignments = _assignments_from(text)
    assert assignments["canonical routing field"] == {"condition_id", "token_id", "outcome"}
    for phrase in [
        "`condition_id` identifies the prediction-market condition",
        "`token_id` identifies the tradable outcome token",
        "`outcome` identifies the human-readable outcome side",
        "`condition_id`, `token_id`, and `outcome` are the canonical shared-rail identifiers",
        "Future routing must preserve all three",
        "Future reasoning must preserve the relationship between `token_id` and `outcome`",
        "`token_outcome_pair` as a derived relationship, not a replacement for the canonical fields",
    ]:
        assert phrase in contract
    assert "The `condition_id`/`token_id`/`outcome` relationship is preserved" in pairing


def test_market_id_is_non_routing_only_and_not_approved_for_routing() -> None:
    text = _read()
    contract = _section(text, "Canonical identifier contract")
    boundary = _section(text, "Non-routing identifier boundary")
    assignments = _assignments_from(text)
    assert assignments["non routing field"] == {"market_id"}
    assert "`market_id` must not be used for routing" in contract
    assert "legacy/non-routing identifier in a negative boundary statement" in contract
    assert "Do not introduce or approve routing on `market_id`" in contract
    assert "`market_id` is explicitly non-routing only" in boundary
    assert "no routing on `market_id` is introduced or approved" in boundary


def test_market_contract_field_relationship_values_are_present() -> None:
    section = _section(_read(), "Market contract field relationship")
    for value in MARKET_CONTRACT_FIELD_RELATIONSHIPS:
        assert f"`{value}`" in section


def test_blocked_work_stage2_artifacts_and_no_execution_approvals_are_present() -> None:
    text = _read()
    blocked_section = _section(text, "Source-fetching track remains blocked")
    for value in BLOCKED_WORK:
        assert f"`{value}`" in blocked_section
    for path in STAGE2_ARTIFACT_PATHS:
        assert f"`{path}`" in text
    for phrase in [
        "Provider connectors remain not approved",
        "Provider clients remain not created",
        "Live provider/source fetching remains not approved",
        "Forecast pulls, API calls, scraping, file downloads, and provider SDK usage remain not approved",
        "Credentials/config loading remains not approved",
        "Generated data and fixtures remain not approved",
        "Scoring/backtesting remains not approved",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
        "Silence, continuation, lack of objection, and non-interference are not approval",
    ]:
        assert phrase in text


def test_no_forbidden_approval_language_is_present() -> None:
    lower_text = _read().lower()
    for prefix, suffix in UNSAFE_APPROVAL_PATTERN_PARTS:
        assert f"{prefix} {suffix}".strip() not in lower_text


def test_machine_checkable_assignments_are_section_scoped_and_allowed() -> None:
    assignments = _assignments_from(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field] == values


def test_machine_parser_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"## {MACHINE_HEADING}\n"
        "- weather bot planning stage: weather_bot_phase0a_canonical_identifier_static_audit\n"
        "## Acceptance criteria\n"
        "- blocked work: source_fetching_implementation\n"
    )
    assert _assignments_from(synthetic) == {
        "weather bot planning stage": {"weather_bot_phase0a_canonical_identifier_static_audit"}
    }


def test_recommended_next_ticket_is_self_review_not_revision_or_implementation() -> None:
    section = _section(_read(), "Recommended next ticket")
    assert f"Recommended next ticket: `{NEXT_TRACK}`" in section
    assert "secondary docs/static-test-only self-review prompt/pass" in section
    assert "must not revise the owner decision" in section
    assert "must not implement source fetching" in section
    assert "must not approve source-fetching implementation planning" in section
    assert _assignments_from(_read())["recommended next track"] == {NEXT_TRACK}
