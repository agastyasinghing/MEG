from pathlib import Path

import pytest

from meg.weather.stage2 import retrieval_context_runtime as rcr
from meg.weather.stage2 import source_identity_runtime as sir


MODULE_PATH = Path("meg/weather/stage2/retrieval_context_runtime.py")
TEST_PATH = Path("tests/core/test_weather_retrieval_context_runtime.py")


def _valid_source_identity(**overrides: object) -> sir.SourceIdentityRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_id": "reviewed-source-1",
        "source_family": sir.SourceFamily.MANUAL_HUMAN_REVIEW_SOURCE_FAMILY,
        "source_uri_descriptor": "human-reviewed static source descriptor",
        "source_access_method": sir.SourceAccessMethod.MANUAL_REVIEW,
        "source_identity_status": sir.SourceIdentityStatus.SOURCE_IDENTITY_RECORDED,
        "runtime_gate_status": sir.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return sir.SourceIdentityRecord(**values)


def _valid_source_identity_mapping(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_id": "reviewed-source-1",
        "source_family": "manual_human_review_source_family",
        "source_uri_descriptor": "human-reviewed static source descriptor",
        "source_access_method": "manual_review",
        "source_identity_status": "source_identity_recorded",
        "runtime_gate_status": "runtime_gate_ready",
    }
    values.update(overrides)
    return values


def _valid_record(**overrides: object) -> rcr.RetrievalContextRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": _valid_source_identity(),
        "retrieval_mode": rcr.RetrievalMode.MANUAL_DESCRIPTOR_ONLY,
        "retrieval_context_status": rcr.RetrievalContextStatus.RETRIEVAL_CONTEXT_RECORDED,
        "retrieval_timing_status": rcr.RetrievalTimingStatus.RETRIEVAL_TIMING_RECORDED,
        "accessed_at_utc": "2026-06-01T00:00:00Z",
        "retrieved_at_utc": "2026-06-01T00:00:00Z",
        "available_at_utc": "2026-05-31T23:00:00Z",
        "decision_time_utc": "2026-06-01T01:00:00Z",
        "runtime_gate_status": rcr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return rcr.RetrievalContextRecord(**values)


def _assert_blocked_with_reason(record: rcr.RetrievalContextRecord, reason: str) -> None:
    result = rcr.validate_retrieval_context_record(record)
    assert result.passed is False
    assert result.severity is rcr.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert rcr.RetrievalMode.values() == frozenset(
        {
            "manual_descriptor_only",
            "static_reference",
            "later_source_fetching_request",
            "later_provider_connector_request",
            "prohibited_until_explicit_approval",
            "unknown_requires_review",
        }
    )
    assert rcr.RetrievalContextStatus.values() == frozenset(
        {
            "retrieval_context_recorded",
            "retrieval_context_missing",
            "retrieval_context_ambiguous",
            "retrieval_context_unsupported",
            "retrieval_context_unknown",
        }
    )
    assert rcr.RetrievalTimingStatus.values() == frozenset(
        {
            "retrieval_timing_recorded",
            "retrieval_timing_missing",
            "retrieval_timing_ambiguous",
            "retrieval_timing_after_decision",
            "retrieval_timing_unknown",
        }
    )
    assert rcr.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert rcr.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    source_identity = _valid_source_identity()
    record = _valid_record(source_identity=source_identity, provenance_notes="review note")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert record.source_identity is source_identity
    assert record.retrieval_mode is rcr.RetrievalMode.MANUAL_DESCRIPTOR_ONLY
    assert record.provenance_notes == "review note"


def test_mapping_construction_with_nested_mapping_coerces_string_enums() -> None:
    record = rcr.retrieval_context_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "source_identity": _valid_source_identity_mapping(),
            "retrieval_mode": "static_reference",
            "retrieval_context_status": "retrieval_context_recorded",
            "retrieval_timing_status": "retrieval_timing_recorded",
            "accessed_at_utc": "2026-06-01T00:00:00Z",
            "retrieved_at_utc": "2026-06-01T00:00:00Z",
            "available_at_utc": "2026-05-31T23:00:00Z",
            "decision_time_utc": "2026-06-01T01:00:00Z",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "review note",
        }
    )

    assert isinstance(record.source_identity, sir.SourceIdentityRecord)
    assert record.retrieval_mode is rcr.RetrievalMode.STATIC_REFERENCE
    assert record.retrieval_context_status is rcr.RetrievalContextStatus.RETRIEVAL_CONTEXT_RECORDED
    assert record.retrieval_timing_status is rcr.RetrievalTimingStatus.RETRIEVAL_TIMING_RECORDED
    assert record.runtime_gate_status is rcr.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "review note"


def test_mapping_construction_accepts_built_source_identity_record() -> None:
    source_identity = _valid_source_identity()

    record = rcr.retrieval_context_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "source_identity": source_identity,
            "retrieval_mode": "manual_descriptor_only",
            "retrieval_context_status": "retrieval_context_recorded",
            "retrieval_timing_status": "retrieval_timing_recorded",
            "accessed_at_utc": "2026-06-01T00:00:00Z",
            "retrieved_at_utc": "2026-06-01T00:00:00Z",
            "available_at_utc": "2026-05-31T23:00:00Z",
            "decision_time_utc": "2026-06-01T01:00:00Z",
            "runtime_gate_status": "runtime_gate_ready",
        }
    )

    assert record.source_identity is source_identity


@pytest.mark.parametrize(
    "retrieval_mode",
    (rcr.RetrievalMode.MANUAL_DESCRIPTOR_ONLY, rcr.RetrievalMode.STATIC_REFERENCE),
)
def test_minimal_valid_records_pass(retrieval_mode: rcr.RetrievalMode) -> None:
    result = rcr.validate_retrieval_context_record(_valid_record(retrieval_mode=retrieval_mode))

    assert result.passed is True
    assert result.severity is rcr.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
    ),
)
def test_blank_canonical_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_record(**{field_name: "  "}), reason)


@pytest.mark.parametrize(
    ("field_name", "value", "reason"),
    (
        ("condition_id", "other-condition", "condition_id does not match source identity"),
        ("token_id", "other-token", "token_id does not match source identity"),
        ("outcome", "No", "outcome does not match source identity"),
    ),
)
def test_canonical_field_mismatch_against_source_identity_fails_closed(
    field_name: str, value: str, reason: str
) -> None:
    _assert_blocked_with_reason(_valid_record(**{field_name: value}), reason)


def test_invalid_nested_source_identity_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_record(source_identity=_valid_source_identity(source_id="  ")),
        "source identity validation failed",
    )


@pytest.mark.parametrize(
    "retrieval_mode",
    (
        rcr.RetrievalMode.LATER_SOURCE_FETCHING_REQUEST,
        rcr.RetrievalMode.LATER_PROVIDER_CONNECTOR_REQUEST,
        rcr.RetrievalMode.PROHIBITED_UNTIL_EXPLICIT_APPROVAL,
        rcr.RetrievalMode.UNKNOWN_REQUIRES_REVIEW,
    ),
)
def test_non_static_retrieval_modes_fail_closed(retrieval_mode: rcr.RetrievalMode) -> None:
    _assert_blocked_with_reason(
        _valid_record(retrieval_mode=retrieval_mode),
        f"retrieval mode is {retrieval_mode.value}",
    )


@pytest.mark.parametrize(
    "context_status",
    (
        rcr.RetrievalContextStatus.RETRIEVAL_CONTEXT_MISSING,
        rcr.RetrievalContextStatus.RETRIEVAL_CONTEXT_AMBIGUOUS,
        rcr.RetrievalContextStatus.RETRIEVAL_CONTEXT_UNSUPPORTED,
        rcr.RetrievalContextStatus.RETRIEVAL_CONTEXT_UNKNOWN,
    ),
)
def test_non_recorded_retrieval_context_statuses_fail_closed(
    context_status: rcr.RetrievalContextStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(retrieval_context_status=context_status),
        f"retrieval context status is {context_status.value}",
    )


@pytest.mark.parametrize(
    "timing_status",
    (
        rcr.RetrievalTimingStatus.RETRIEVAL_TIMING_MISSING,
        rcr.RetrievalTimingStatus.RETRIEVAL_TIMING_AMBIGUOUS,
        rcr.RetrievalTimingStatus.RETRIEVAL_TIMING_AFTER_DECISION,
        rcr.RetrievalTimingStatus.RETRIEVAL_TIMING_UNKNOWN,
    ),
)
def test_non_recorded_retrieval_timing_statuses_fail_closed(
    timing_status: rcr.RetrievalTimingStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(retrieval_timing_status=timing_status),
        f"retrieval timing status is {timing_status.value}",
    )


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("accessed_at_utc", "accessed_at_utc is missing"),
        ("retrieved_at_utc", "retrieved_at_utc is missing"),
        ("available_at_utc", "available_at_utc is missing"),
        ("decision_time_utc", "decision_time_utc is missing"),
    ),
)
def test_blank_timing_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_record(**{field_name: "  "}), reason)


@pytest.mark.parametrize(
    "gate_status",
    (
        rcr.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        rcr.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        rcr.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(gate_status: rcr.RuntimeGateStatus) -> None:
    _assert_blocked_with_reason(
        _valid_record(runtime_gate_status=gate_status),
        f"runtime gate status is {gate_status.value}",
    )


def test_new_files_do_not_contain_noncanonical_identifier_string() -> None:
    forbidden = "market" "_id"

    assert forbidden not in MODULE_PATH.read_bytes().decode("utf-8")
    assert forbidden not in TEST_PATH.read_bytes().decode("utf-8")


def test_module_source_has_no_network_provider_execution_or_file_io_calls() -> None:
    source_text = MODULE_PATH.read_bytes().decode("utf-8")
    forbidden_terms = (
        "req" "uests",
        "ht" "tpx",
        "url" "lib",
        "aio" "http",
        "bo" "to3",
        "poly" "market",
        "sub" "process",
        "open" "(",
        ".read" "_text(",
        ".write" "_text(",
        "sock" "et",
        "os" ".environ",
        "dot" "env",
    )

    for term in forbidden_terms:
        assert term not in source_text
