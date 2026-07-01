"""Static checks for Weather Bot Phase 0A canonical identifier static audit self-review."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-SELF-REVIEW-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_phase0a_canonical_identifier_static_audit_self_review_01.py"
MACHINE_HEADING = "Machine-checkable Weather Bot Phase 0A canonical-identifier static-audit self-review assignments"
NEXT_TRACK = "weather_bot_phase0a_canonical_identifier_static_audit_revision_if_scope_too_broad"
COMPLETE_TRACK = "weather_bot_phase0a_canonical_identifier_static_audit_self_review"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to canonical identifier static audit",
    "Self-review objective",
    "Scope verification",
    "Document verification",
    "Static test verification",
    "Safety and non-execution verification",
    "No owner-decision revision verification",
    "Source-fetching track posture",
    "Canonical identifier contract verification",
    "Identifier relationship verification",
    "Non-routing identifier verification",
    "Market contract field relationship verification",
    "Remaining blocked work",
    "Stage 2 runtime metadata posture",
    "Recommended next ticket",
    MACHINE_HEADING,
    "Acceptance criteria",
)
MARKET_CONTRACT_FIELDS = {
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
    "weather bot planning stage": {COMPLETE_TRACK},
    "self review status": {
        "docs_static_test_only",
        "self_review_pass_only",
        "post_weather_bot_phase0a_canonical_identifier_static_audit",
    },
    "reviewed artifact": {"weather_bot_phase0a_canonical_identifier_static_audit_01"},
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
    "identifier relationship verified": {
        "token_outcome_pair_derived_relationship",
        "condition_token_outcome_preserved",
        "token_id_outcome_relationship_preserved",
    },
    "market contract field relationship verified": MARKET_CONTRACT_FIELDS,
    "canonical routing field verified": {"condition_id", "token_id", "outcome"},
    "non routing field verified": {"market_id"},
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
        "self_review_pass_only",
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
    "conditional next track": {NEXT_TRACK},
    "evidence status": {"self_review_pass_recorded"},
    "label confidence": {"confirmed"},
}
REQUIRED_ASSIGNMENTS = {(field, value) for field, values in ALLOWED_ASSIGNMENTS.items() for value in values}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
FORBIDDEN_APPROVAL_RE = re.compile(
    r"revised " "owner decision|approve_narrow_source_fetching_runtime" "_implementation_plan|"
    r"provider connector " "is approved|provider client " "is created|source fetching " "is approved|"
    r"source fetching implementation " "is approved|source fetching implementation planning " "is approved|"
    r"source fetching implementation plan " "is approved|live provider source fetching " "is approved|"
    r"forecast pull " "is approved|api call " "is approved|scraping " "is approved|file download " "is approved|"
    r"provider sdk " "is approved|credentials.*loading " "is approved|generated data " "is approved|"
    r"fixture change " "is approved|scoring " "is approved|backtesting " "is approved|trading " "is approved|"
    r"order placement " "is approved|autonomy " "is approved|production behavior " "is approved|"
    r"report writing " "is approved|external export " "is approved|persistence " "is approved|"
    r"silence " "is approval|continuation " "is approval|non-interference " "is approval",
    re.IGNORECASE,
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
        "# WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-SELF-REVIEW-01 — "
        "Weather Bot Phase 0A Canonical Identifier Static Audit Self-Review"
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
    assert set(imports) <= {"__future__", "ast", "re", "pathlib"}
    assert all(not item.startswith("meg") for item in imports)


def test_required_posture_and_boundaries_are_present() -> None:
    text = _read()
    required_phrases = [
        "docs/static-test-only/self-review-pass-only",
        "This ticket does not modify `meg/`",
        "This ticket does not modify meta/handoff files",
        "reviews `WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-01`",
        "does not revise the owner decision",
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
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_market_contract_field_relationships_are_verified() -> None:
    text = _read()
    section = _section(text, "Market contract field relationship verification")
    assert "All market contract field relationship values were verified" in section
    for field in MARKET_CONTRACT_FIELDS:
        assert f"`{field}`" in section


def test_canonical_routing_and_identifier_relationships_are_preserved() -> None:
    text = _read()
    section = _section(text, "Canonical identifier contract verification")
    assert "Canonical routing fields were verified as exactly `condition_id`, `token_id`, and `outcome`" in section
    assert "Future routing must preserve all three canonical shared-rail identifiers" in section
    assert "Future reasoning must preserve the relationship between `token_id` and `outcome`" in section
    relationship_section = _section(text, "Identifier relationship verification")
    assert "`token_outcome_pair` remains a derived relationship, not a replacement for canonical fields" in relationship_section
    assert "The `condition_id`/`token_id`/`outcome` relationship is preserved" in relationship_section


def test_market_id_non_routing_boundary_is_preserved() -> None:
    section = _section(_read(), "Non-routing identifier verification")
    assert "`market_id` remains explicitly non-routing only" in section
    assert "No routing on `market_id` is introduced or approved" in section


def test_blocked_work_stage2_artifacts_and_no_execution_approvals_are_present() -> None:
    text = _read()
    for value in BLOCKED_WORK:
        assert f"`{value}`" in text
    for path in STAGE2_ARTIFACT_PATHS:
        assert f"`{path}`" in text
    required_non_approvals = [
        "Provider connectors remain not approved",
        "Provider clients remain not created",
        "Live provider/source fetching remains not approved",
        "Credentials/config loading remains not approved",
        "Generated data and fixtures remain not approved",
        "Scoring/backtesting remains not approved",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
        "Silence, continuation, lack of objection, and non-interference are not approval",
    ]
    for phrase in required_non_approvals:
        assert phrase in text
    assert FORBIDDEN_APPROVAL_RE.search(text) is None


def test_machine_checkable_assignments_are_section_scoped_and_allowed() -> None:
    assignments = _assignments_from(_read())
    actual_pairs = {(field, value) for field, values in assignments.items() for value in values}
    assert actual_pairs == REQUIRED_ASSIGNMENTS
    for field, values in assignments.items():
        assert field in ALLOWED_ASSIGNMENTS
        assert values <= ALLOWED_ASSIGNMENTS[field]


def test_machine_checkable_parser_ignores_assignments_after_next_heading() -> None:
    synthetic = (
        f"## {MACHINE_HEADING}\n"
        "- evidence status: self_review_pass_recorded\n"
        "## Acceptance criteria\n"
        "- evidence status: forbidden_after_next_heading\n"
    )
    assert _assignments_from(synthetic) == {"evidence status": {"self_review_pass_recorded"}}


def test_completion_and_recommended_next_track_are_conditional_and_safe() -> None:
    text = _read()
    section = _section(text, "Recommended next ticket")
    assert f"Recommended next ticket: `{NEXT_TRACK}`" in section
    assert f"conditional only if reviewers want another pass or identify scope issues" in section
    assert f"this pass completes `{COMPLETE_TRACK}`" in section
    assert "Do not proceed to owner-decision revision or source-fetching implementation planning" in section
    assert "not owner-decision revision and not source-fetching implementation planning" in section
    occurrences = re.findall(r"weather_bot_phase0a_canonical_identifier_static_audit_revision_if_scope_too_broad", section)
    assert occurrences == [NEXT_TRACK]
