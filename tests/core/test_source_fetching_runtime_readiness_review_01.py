"""Static checks for Source Fetching Runtime Readiness Review."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "SOURCE-FETCHING-RUNTIME-READINESS-REVIEW-01"
ARTIFACT_PATH = REPO_ROOT / f"docs/prd/{CANONICAL_ID}.md"
MACHINE_HEADING = "## Machine-checkable source-fetching runtime readiness-review assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to Weather Bot PRD and architecture alignment",
    "Relationship to Stage 2 runtime closeout",
    "Readiness objective",
    "Landed metadata prerequisites",
    "Validation dependency chain readiness",
    "Source identity readiness",
    "Retrieval context readiness",
    "Provider/source-family readiness",
    "Manual review gate readiness",
    "No-lookahead metadata readiness",
    "Fail-closed validation readiness",
    "Static audit surface readiness",
    "Readiness findings",
    "Non-approval boundary",
    "Source fetching implementation boundary",
    "Provider/source execution boundary",
    "Credential/config boundary",
    "Generated-data and fixture boundary",
    "Scoring/backtesting boundary",
    "Trading/autonomy/production boundary",
    "Audit report and export boundary",
    "Canonical identifier posture",
    "Blocked work during readiness review",
    "Recommended next ticket",
    "Machine-checkable source-fetching runtime readiness-review assignments",
    "Acceptance criteria",
)
RUNTIME_MODULE_PATHS = {
    "meg/weather/stage2/source_identity_runtime.py",
    "meg/weather/stage2/retrieval_context_runtime.py",
    "meg/weather/stage2/provider_source_family_runtime.py",
    "meg/weather/stage2/manual_review_gate_runtime.py",
    "meg/weather/stage2/no_lookahead_metadata_runtime.py",
    "meg/weather/stage2/fail_closed_validation_runtime.py",
    "meg/weather/stage2/static_audit_surface_runtime.py",
}
VALIDATION_DEPENDENCY_ORDER = {
    "source_identity_runtime",
    "retrieval_context_runtime",
    "provider_source_family_runtime",
    "manual_review_gate_runtime",
    "no_lookahead_metadata_runtime",
    "fail_closed_validation_runtime",
    "static_audit_surface_runtime",
}
READINESS_FINDINGS = {
    "metadata_scaffold_sequence_landed",
    "validation_dependency_chain_documented",
    "fail_closed_posture_documented",
    "no_lookahead_posture_documented",
    "manual_review_gate_documented",
    "static_audit_surface_documented",
    "source_fetching_not_implemented",
    "provider_execution_not_approved",
    "implementation_approval_not_granted",
}
ALLOWED_FUTURE_CONSUMPTION_POSTURES = {
    "read_readiness_review_only",
    "require_separate_implementation_approval",
    "preserve_condition_id_token_id_outcome",
    "maintain_supplied_metadata_only_until_approval",
    "maintain_fail_closed_until_approval",
    "maintain_no_lookahead_until_approval",
    "no_source_fetching_implementation",
    "no_provider_execution",
    "no_live_fetching",
    "no_credentials_config_loading",
    "no_generated_data",
    "no_fixture_change",
    "no_scoring_backtesting",
    "no_trading_autonomy_production",
    "no_report_writing",
    "no_external_export",
    "no_persistence",
}
BLOCKED_WORK_DURING_READINESS_REVIEW = {
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
    "weather bot planning stage": {"source_fetching_runtime_readiness_review"},
    "readiness review status": {
        "docs_static_test_only",
        "readiness_review_only",
        "post_stage2_runtime_closeout_review",
    },
    "current state posture": {
        "stage2_runtime_metadata_scaffold_sequence_landed",
        "source_fetching_not_implemented",
        "implementation_approval_not_granted",
    },
    "landed runtime artifact": {
        "source_identity_runtime_py",
        "retrieval_context_runtime_py",
        "provider_source_family_runtime_py",
        "manual_review_gate_runtime_py",
        "no_lookahead_metadata_runtime_py",
        "fail_closed_validation_runtime_py",
        "static_audit_surface_runtime_py",
    },
    "validation dependency order": VALIDATION_DEPENDENCY_ORDER,
    "readiness finding": READINESS_FINDINGS,
    "allowed future consumption posture": ALLOWED_FUTURE_CONSUMPTION_POSTURES,
    "blocked work during readiness review": BLOCKED_WORK_DURING_READINESS_REVIEW,
    "provider source posture": {
        "provider_connectors_not_approved",
        "provider_clients_not_created",
        "live_provider_source_fetching_not_approved",
        "readiness_review_only",
    },
    "credential config posture": {"unknown_requires_review"},
    "generated data fixture posture": {"no_generated_data", "no_fixture_change"},
    "audit output posture": {"no_report_writing", "no_external_export", "no_persistence"},
    "implementation posture": {
        "docs_static_test_only",
        "readiness_review_only",
        "no_runtime_code_change",
        "no_source_fetching",
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
    "recommended next track": {"source_fetching_runtime_implementation_approval_request"},
    "conditional next track": {
        "source_fetching_readiness_revision_if_scope_too_broad",
        "hold_checkpoint_if_implementation_approval_not_desired",
    },
    "evidence status": {"readiness_review_recorded"},
    "label confidence": {"confirmed"},
}
ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)


def _read() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    assert match, f"Missing section: {heading}"
    assert match.group("section").strip(), f"Section is empty: {heading}"
    return match.group("section")


def _machine_section(text: str) -> str:
    return _section(text, MACHINE_HEADING.removeprefix("## "))


def _assignments(text: str) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(_machine_section(text)):
        result.setdefault(match.group("field"), set()).add(match.group("value"))
    return result


def test_document_exists_canonical_id_and_sections_are_non_empty() -> None:
    assert ARTIFACT_PATH.exists()
    text = _read()
    assert f"Canonical ID: {CANONICAL_ID}" in text
    assert text.startswith(
        "# SOURCE-FETCHING-RUNTIME-READINESS-REVIEW-01 — "
        "Source Fetching Runtime Readiness Review"
    )
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_docs_static_readiness_only_scope_and_no_meg_modification_posture() -> None:
    text = _read()
    required_phrases = [
        "docs/static-test-only/readiness-review-only",
        "does not modify `meg/`",
        "does not implement source fetching",
        "does not approve source-fetching implementation",
        "does not approve provider execution",
        "only evaluates readiness for a later, separately approved source-fetching runtime implementation approval request",
        "Weather Bot models the market settlement rule, not generic weather",
        "All landed Stage 2 runtime metadata artifacts remain supplied-metadata-only and fail-closed",
        "Source fetching remains not implemented",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_artifact_paths_dependency_order_findings_and_postures_appear() -> None:
    text = _read()
    for value in (
        RUNTIME_MODULE_PATHS
        | VALIDATION_DEPENDENCY_ORDER
        | READINESS_FINDINGS
        | ALLOWED_FUTURE_CONSUMPTION_POSTURES
        | BLOCKED_WORK_DURING_READINESS_REVIEW
    ):
        assert value in text


def test_provider_source_execution_is_not_approved() -> None:
    text = _read()
    required_phrases = [
        "Provider connectors remain not approved",
        "Provider clients remain not created",
        "Live provider/source fetching remains not approved",
        "Forecast pulling, API calls, scraping, file downloads, and provider SDK usage remain not approved",
        "does not approve provider execution",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_source_fetching_credentials_generated_data_and_fixture_boundaries() -> None:
    text = _read()
    required_phrases = [
        "Source fetching remains not implemented",
        "does not approve source-fetching implementation",
        "Credentials/config loading remains not approved",
        "does not modify `.env`, secrets, credentials, config, or config-loading behavior",
        "Generated data and fixtures remain not approved",
        "does not create generated data",
        "does not modify `tests/fixtures/`",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_scoring_trading_autonomy_production_and_audit_output_not_approved() -> None:
    text = _read()
    required_phrases = [
        "Scoring/backtesting remains not approved",
        "Runtime trading/order placement/autonomy/production remains not approved",
        "Report writing, audit output persistence, and external export remain not approved",
        "does not create audit reports",
        "persisted audit output",
        "external export behavior",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_no_forbidden_execution_or_output_approval_phrases() -> None:
    text = _read().lower()
    approved_suffix = " is " + "approved"
    created_suffix = " is " + "created"
    forbidden_patterns = [
        "provider connector" + approved_suffix,
        "provider client" + created_suffix,
        "source fetching" + approved_suffix,
        "source fetching implementation" + approved_suffix,
        "live provider source fetching" + approved_suffix,
        "forecast pull" + approved_suffix,
        "api call" + approved_suffix,
        "scraping" + approved_suffix,
        "file download" + approved_suffix,
        "provider sdk" + approved_suffix,
        "credentials.*loading" + approved_suffix,
        "generated data" + approved_suffix,
        "fixture change" + approved_suffix,
        "scoring" + approved_suffix,
        "backtesting" + approved_suffix,
        "trading" + approved_suffix,
        "order placement" + approved_suffix,
        "autonomy" + approved_suffix,
        "production behavior" + approved_suffix,
        "report writing" + approved_suffix,
        "external export" + approved_suffix,
        "persistence" + approved_suffix,
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text), pattern


def test_canonical_identifier_contract_and_no_market_id_routing() -> None:
    text = _read()
    canonical_section = _section(text, "Canonical identifier posture")
    for identifier in ("condition_id", "token_id", "outcome"):
        assert f"`{identifier}`" in canonical_section
    assert "No routing on `market_id` is introduced or approved" in canonical_section


def test_machine_checkable_assignments_are_complete_and_allowed() -> None:
    assignments = _assignments(_read())
    assert set(assignments) == set(ALLOWED_ASSIGNMENTS)
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert assignments[field] == allowed_values


def test_every_actual_machine_checkable_assignment_value_is_allowed() -> None:
    assignments = _assignments(_read())
    for field, values in assignments.items():
        assert field in ALLOWED_ASSIGNMENTS
        assert values <= ALLOWED_ASSIGNMENTS[field]


def test_machine_checkable_parser_is_section_scoped() -> None:
    text = _read()
    machine_section = _machine_section(text)
    assert "Acceptance criteria" not in machine_section

    synthetic = (
        "# Example\n\n"
        f"{MACHINE_HEADING}\n\n"
        "- evidence status: readiness_review_recorded\n\n"
        "## Acceptance criteria\n\n"
        "- evidence status: forged_after_next_heading\n"
        "- recommended next track: source_fetching_runtime_implementation\n"
    )
    parsed = _assignments(synthetic)
    assert parsed == {"evidence status": {"readiness_review_recorded"}}


def test_recommended_next_track_is_approval_request_only_not_implementation() -> None:
    text = _read()
    recommended = _section(text, "Recommended next ticket")
    assert "Recommended next track: `source_fetching_runtime_implementation_approval_request`" in recommended
    assert "approval request only, not implementation" in recommended
    assert "ask the owner whether to approve a narrow source-fetching runtime implementation plan" in recommended
    assert "must not itself implement source fetching" in recommended
    assignments = _assignments(text)
    assert assignments["recommended next track"] == {
        "source_fetching_runtime_implementation_approval_request"
    }
