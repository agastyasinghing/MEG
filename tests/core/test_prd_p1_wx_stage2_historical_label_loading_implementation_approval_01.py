"""Static checks for the Stage 2 historical-label loading implementation approval request."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-APPROVAL-01_HISTORICAL_LABEL_LOADING_VALIDATION_IMPLEMENTATION_APPROVAL_REQUEST.md"
CANONICAL_ID = "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-APPROVAL-01"
ASSIGNMENT_HEADING = "## Machine-checkable historical-label loading implementation approval-request assignments"

ALLOWED_ASSIGNMENTS: dict[str, set[str]] = {
    "historical label loading implementation approval stage": {
        "stage_2_historical_label_loading_validation_implementation_approval_request",
    },
    "request status": {
        "request_prepared",
        "implementation_not_approved",
        "human_review_required",
        "blocked_pending_fix",
        "unclear",
    },
    "requested future implementation scope": {
        "static_loader_validator_skeleton_if_later_approved",
        "allowlisted_fixture_directory_reads_if_later_approved",
        "fail_closed_metadata_validation_if_later_approved",
        "synthetic_real_fixture_distinction_if_later_approved",
        "source_provenance_validation_if_later_approved",
        "no_lookahead_validation_if_later_approved",
        "reviewer_note_validation_if_later_approved",
        "closed_set_validation_if_later_approved",
        "tests_core_static_validation_if_later_approved",
        "no_ingestion_no_runtime_no_scoring",
    },
    "approval boundary status": {
        "not_approved",
        "separate_human_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "future ticket permission": {
        "may_request_historical_label_loading_implementation_ticket",
        "must_not_create_loader_now",
        "must_not_create_ingestion",
        "must_not_create_connectors",
        "must_not_create_runtime",
        "must_not_create_scoring",
        "must_not_create_backtesting",
        "must_not_create_trading",
        "blocked_until_human_decision",
    },
    "data posture": {
        "no_fixture_files_created",
        "no_fixture_files_modified",
        "no_historical_label_data_created",
        "no_generated_data_created",
        "no_loader_created",
        "no_runtime_data_access",
        "no_source_fetching",
    },
    "non-approval category": {
        "historical_label_loading_implementation",
        "real_historical_label_data_expansion",
        "generated_data",
        "ingestion",
        "provider_integration",
        "connectors",
        "external_api_calls",
        "credentials_secrets_config",
        "forecast_pulls",
        "model_scoring",
        "probability_scoring",
        "backtesting",
        "paper_simulation",
        "runtime_observation",
        "trading_order_autonomy",
        "production_behavior",
        "cplusplus_rust_runtime",
        "other_unclear",
    },
    "evidence status": {
        "source_backed",
        "reviewer_inferred",
        "missing",
        "conflicting",
        "not_applicable",
    },
    "label confidence": {
        "confirmed",
        "unclear",
        "unknown",
    },
}

FORBIDDEN_EXAMPLES = {
    "request_prepared/implementation_not_approved",
    "not_approved/separate_human_approval_required",
    "confirmed/unclear",
    "partial",
    "mixed",
    "likely_confirmed",
    "maybe",
    "approved",
    "configured",
    "available",
    "loader_ready",
    "data_ready",
    "ingestion_ready",
    "scoring_ready",
    "runtime_ready",
    "trading_ready",
    "production_ready",
    "provider_ready",
    "model_ready",
    "back" + "test_ready",
    "ready_for_loading",
    "ready_for_ingestion",
    "ready_for_scoring",
    "ready_for_runtime",
    "ready_for_trading",
    "approved_for_loading",
    "approved_for_ingestion",
    "approved_for_runtime",
    "approved_for_scoring",
    "approved_for_trading",
    "trade_ready",
    "auto" + "_execute",
    "aut" + "onomous",
    "live",
    "production",
}

FORBIDDEN_IMPLEMENTATION_FRAGMENTS = (
    "os." + "environ",
    "load_" + "dot" + "env",
    "dot" + "env",
    "requests" + ".",
    "http" + "x.",
    "aio" + "http",
    "urllib." + "request",
    "api_" + "key",
    "secret_" + "key",
    "weather_" + "api_" + "key",
    "fast" + "api",
    "fl" + "ask",
    "sql" + "alchemy",
    "pan" + "das",
    "pol" + "ars",
    "duck" + "db",
    "read_" + "csv",
    "to_" + "csv",
    "json." + "load",
    "json" + "lines",
    "par" + "quet",
    "pre" + "dict",
)


def _prd_text() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def _assignment_section(text: str) -> str:
    marker = ASSIGNMENT_HEADING + "\n"
    assert marker in text
    section_start = text.index(marker) + len(marker)
    next_heading = text.find("\n## ", section_start)
    if next_heading == -1:
        return text[section_start:]
    return text[section_start:next_heading]


def _parsed_assignments() -> dict[str, set[str]]:
    section = _assignment_section(_prd_text())
    parsed = {prefix: set() for prefix in ALLOWED_ASSIGNMENTS}
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        assert line.startswith("- "), line
        body = line[2:]
        prefix, separator, value = body.partition(": ")
        assert separator == ": ", line
        assert prefix in ALLOWED_ASSIGNMENTS, line
        assert value in ALLOWED_ASSIGNMENTS[prefix], line
        parsed[prefix].add(value)
    return parsed


def test_approval_request_prd_exists_with_canonical_id_and_required_references() -> None:
    assert PRD_PATH.is_file()
    text = _prd_text()
    for required in (
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "MEG_ACTIVE_STATE",
        "WEATHER_BOT_PACKET",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-01",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-APPROVAL-01",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01",
        "Stage 2 skeleton closeout",
    ):
        assert required in text


def test_required_sections_are_present_in_order() -> None:
    text = _prd_text()
    headings = [
        "## Status and scope",
        "## Strategic framing",
        "## Stage ladder position",
        "## Human approval context",
        "## Implementation approval-request boundary",
        "## Why a static loader/validator skeleton may be useful later",
        "## Requested future implementation scope",
        "## Explicitly excluded scope",
        "## Relationship to Stage 2 skeleton",
        "## Relationship to synthetic fixtures",
        "## Relationship to real source-backed fixtures",
        "## Relationship to historical-label loading planning",
        "## Relationship to ingestion",
        "## Relationship to scoring/backtesting",
        "## Relationship to runtime/trading",
        "## Human approval checklist",
        "## Approval decision options",
        "## Explicit non-approval boundaries",
        "## Closed historical-label loading implementation approval-request vocabulary",
        "## Forbidden historical-label loading implementation approval-request values",
        ASSIGNMENT_HEADING,
        "## Later-ticket handoff",
        "## Acceptance criteria",
    ]
    positions = [text.index(heading) for heading in headings]
    assert positions == sorted(positions)


def test_approval_request_only_scope_and_required_non_approval_language() -> None:
    text = _prd_text()
    required_phrases = (
        "This is a historical-label loading/validation implementation approval request only",
        "Historical-label loading implementation is not approved by this document",
        "Loader code is not created by this document",
        "No fixture JSON files are read by source/runtime code",
        "No fixture JSON files are created or modified",
        "No fixture README files are created or modified",
        "No historical-label data files are created",
        "No generated data is created",
        "Ingestion is not approved by this document",
        "Provider/API connectors are not approved by this document",
        "External API calls are not approved by this document",
        "Credentials/secrets/config loading is not approved by this document",
        "Forecast pulls are not approved by this document",
        "Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved",
        "Future implementation requires separate explicit human approval after this request",
        "Future ingestion requires a separate explicit approval request",
        "Future scoring/backtesting requires a separate explicit approval request",
        "Future runtime/trading requires a separate explicit approval request",
        "do not imply loader readiness, ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_requested_future_scope_is_narrow_static_test_oriented_and_fail_closed() -> None:
    text = _prd_text()
    for required in (
        "narrow static test-only loader/validator skeleton",
        "Reading only the existing allowlisted static fixture JSON directories in tests or explicit static-validation context",
        "Fail-closed validation for required metadata",
        "Strict synthetic-vs-real fixture distinction",
        "Source/provenance/no-lookahead/reviewer-note validation boundaries",
        "Closed-set validation for postures and statuses",
        "Static tests under `tests/core`",
        "No runtime market calls",
        "No external API calls",
        "No secrets/config loading",
        "No forecast pulls",
        "No ingestion pipeline",
        "No database writes",
        "No generated data",
        "No model/probability scoring",
        "No backtesting",
        "No paper simulation",
        "No runtime observation",
        "No trading/order/autonomy",
    ):
        assert required in text


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _prd_text()
    section = _assignment_section(text)
    assert section.strip()
    assert "## Later-ticket handoff" in text
    assert "## Later-ticket handoff" not in section
    for forbidden in FORBIDDEN_EXAMPLES:
        assert forbidden in text
        assert forbidden not in {value for values in _parsed_assignments().values() for value in values}


def test_closed_set_assignments_use_only_allowed_values_and_every_allowed_value_appears() -> None:
    parsed = _parsed_assignments()
    assert parsed == ALLOWED_ASSIGNMENTS


def test_forbidden_examples_are_documented_but_not_parsed_as_actual_values() -> None:
    text = _prd_text()
    section = _assignment_section(text)
    assert "Forbidden historical-label loading implementation approval-request values" in text
    parsed_values = {value for values in _parsed_assignments().values() for value in values}
    for forbidden in FORBIDDEN_EXAMPLES:
        assert forbidden in text
        assert forbidden not in parsed_values


def test_forbidden_implementation_fragments_are_absent_from_prd_and_test() -> None:
    combined = _prd_text() + "\n" + Path(__file__).read_text(encoding="utf-8")
    for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS:
        assert fragment not in combined
