from pathlib import Path

import pytest

from meg.weather.stage2 import provider_source_family_runtime as psfr
from meg.weather.stage2 import retrieval_context_runtime as rcr
from meg.weather.stage2 import source_identity_runtime as sir


MODULE_PATH = Path("meg/weather/stage2/provider_source_family_runtime.py")
TEST_PATH = Path("tests/core/test_weather_provider_source_family_runtime.py")


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


def _valid_retrieval_context(
    source_identity: sir.SourceIdentityRecord | None = None, **overrides: object
) -> rcr.RetrievalContextRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": source_identity or _valid_source_identity(),
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


def _valid_retrieval_context_mapping(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": _valid_source_identity_mapping(),
        "retrieval_mode": "manual_descriptor_only",
        "retrieval_context_status": "retrieval_context_recorded",
        "retrieval_timing_status": "retrieval_timing_recorded",
        "accessed_at_utc": "2026-06-01T00:00:00Z",
        "retrieved_at_utc": "2026-06-01T00:00:00Z",
        "available_at_utc": "2026-05-31T23:00:00Z",
        "decision_time_utc": "2026-06-01T01:00:00Z",
        "runtime_gate_status": "runtime_gate_ready",
    }
    values.update(overrides)
    return values


def _valid_record(**overrides: object) -> psfr.ProviderSourceFamilyRecord:
    source_identity = overrides.get("source_identity")
    if not isinstance(source_identity, sir.SourceIdentityRecord):
        source_identity = _valid_source_identity()
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": source_identity,
        "retrieval_context": _valid_retrieval_context(source_identity),
        "source_family": "manual_human_review_source_family",
        "provider_source_family_status": (
            psfr.ProviderSourceFamilyStatus.PROVIDER_SOURCE_FAMILY_RECORDED
        ),
        "provider_execution_posture": psfr.ProviderExecutionPosture.NO_PROVIDER_EXECUTION,
        "source_family_compatibility_status": (
            psfr.SourceFamilyCompatibilityStatus.SOURCE_FAMILY_COMPATIBLE
        ),
        "runtime_gate_status": psfr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return psfr.ProviderSourceFamilyRecord(**values)


def _assert_blocked_with_reason(record: psfr.ProviderSourceFamilyRecord, reason: str) -> None:
    result = psfr.validate_provider_source_family_record(record)
    assert result.passed is False
    assert result.severity is psfr.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert psfr.ProviderSourceFamilyStatus.values() == frozenset(
        {
            "provider_source_family_recorded",
            "provider_source_family_missing",
            "provider_source_family_ambiguous",
            "provider_source_family_unsupported",
            "provider_source_family_unknown",
        }
    )
    assert psfr.ProviderExecutionPosture.values() == frozenset(
        {
            "no_provider_execution",
            "provider_execution_not_approved",
            "provider_connector_not_created",
            "provider_client_not_created",
            "live_provider_fetching_not_approved",
            "unknown_requires_review",
        }
    )
    assert psfr.SourceFamilyCompatibilityStatus.values() == frozenset(
        {
            "source_family_compatible",
            "source_family_incompatible",
            "source_family_requires_manual_review",
            "source_family_unknown",
        }
    )
    assert psfr.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert psfr.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    source_identity = _valid_source_identity()
    retrieval_context = _valid_retrieval_context(source_identity)
    record = _valid_record(
        source_identity=source_identity,
        retrieval_context=retrieval_context,
        provenance_notes="review note",
    )

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert record.source_identity is source_identity
    assert record.retrieval_context is retrieval_context
    assert record.source_family == "manual_human_review_source_family"
    assert record.provenance_notes == "review note"


def test_mapping_construction_with_nested_mappings_coerces_string_enums() -> None:
    record = psfr.provider_source_family_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "source_identity": _valid_source_identity_mapping(),
            "retrieval_context": _valid_retrieval_context_mapping(),
            "source_family": "manual_human_review_source_family",
            "provider_source_family_status": "provider_source_family_recorded",
            "provider_execution_posture": "no_provider_execution",
            "source_family_compatibility_status": "source_family_compatible",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "review note",
        }
    )

    assert isinstance(record.source_identity, sir.SourceIdentityRecord)
    assert isinstance(record.retrieval_context, rcr.RetrievalContextRecord)
    assert record.provider_source_family_status is (
        psfr.ProviderSourceFamilyStatus.PROVIDER_SOURCE_FAMILY_RECORDED
    )
    assert record.provider_execution_posture is psfr.ProviderExecutionPosture.NO_PROVIDER_EXECUTION
    assert record.source_family_compatibility_status is (
        psfr.SourceFamilyCompatibilityStatus.SOURCE_FAMILY_COMPATIBLE
    )
    assert record.runtime_gate_status is psfr.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "review note"


def test_mapping_construction_accepts_built_dependency_records() -> None:
    source_identity = _valid_source_identity()
    retrieval_context = _valid_retrieval_context(source_identity)

    record = psfr.provider_source_family_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "source_identity": source_identity,
            "retrieval_context": retrieval_context,
            "source_family": "manual_human_review_source_family",
            "provider_source_family_status": "provider_source_family_recorded",
            "provider_execution_posture": "no_provider_execution",
            "source_family_compatibility_status": "source_family_compatible",
            "runtime_gate_status": "runtime_gate_ready",
        }
    )

    assert record.source_identity is source_identity
    assert record.retrieval_context is retrieval_context


def test_minimal_valid_record_passes() -> None:
    result = psfr.validate_provider_source_family_record(_valid_record())

    assert result.passed is True
    assert result.severity is psfr.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("source_family", "source_family is missing"),
    ),
)
def test_blank_required_fields_fail_closed(field_name: str, reason: str) -> None:
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


@pytest.mark.parametrize(
    ("field_name", "value", "reason"),
    (
        ("condition_id", "other-condition", "condition_id does not match retrieval context"),
        ("token_id", "other-token", "token_id does not match retrieval context"),
        ("outcome", "No", "outcome does not match retrieval context"),
    ),
)
def test_canonical_field_mismatch_against_retrieval_context_fails_closed(
    field_name: str, value: str, reason: str
) -> None:
    retrieval_context = _valid_retrieval_context(**{field_name: value})
    _assert_blocked_with_reason(_valid_record(retrieval_context=retrieval_context), reason)


def test_invalid_nested_source_identity_fails_closed() -> None:
    source_identity = _valid_source_identity(source_id="  ")
    retrieval_context = _valid_retrieval_context(source_identity)

    _assert_blocked_with_reason(
        _valid_record(source_identity=source_identity, retrieval_context=retrieval_context),
        "source identity validation failed",
    )


def test_invalid_nested_retrieval_context_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_record(retrieval_context=_valid_retrieval_context(accessed_at_utc="  ")),
        "retrieval context validation failed",
    )


def test_source_family_mismatch_against_source_identity_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_record(source_family="official_resolution_source_family"),
        "source_family does not match source identity",
    )


@pytest.mark.parametrize(
    "status",
    (
        psfr.ProviderSourceFamilyStatus.PROVIDER_SOURCE_FAMILY_MISSING,
        psfr.ProviderSourceFamilyStatus.PROVIDER_SOURCE_FAMILY_AMBIGUOUS,
        psfr.ProviderSourceFamilyStatus.PROVIDER_SOURCE_FAMILY_UNSUPPORTED,
        psfr.ProviderSourceFamilyStatus.PROVIDER_SOURCE_FAMILY_UNKNOWN,
    ),
)
def test_non_recorded_provider_source_family_statuses_fail_closed(
    status: psfr.ProviderSourceFamilyStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(provider_source_family_status=status),
        f"provider source family status is {status.value}",
    )


@pytest.mark.parametrize(
    "posture",
    tuple(
        posture
        for posture in psfr.ProviderExecutionPosture
        if posture is not psfr.ProviderExecutionPosture.NO_PROVIDER_EXECUTION
    ),
)
def test_non_no_provider_execution_postures_fail_closed(
    posture: psfr.ProviderExecutionPosture,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(provider_execution_posture=posture),
        f"provider execution posture is {posture.value}",
    )


@pytest.mark.parametrize(
    "status",
    (
        psfr.SourceFamilyCompatibilityStatus.SOURCE_FAMILY_INCOMPATIBLE,
        psfr.SourceFamilyCompatibilityStatus.SOURCE_FAMILY_REQUIRES_MANUAL_REVIEW,
        psfr.SourceFamilyCompatibilityStatus.SOURCE_FAMILY_UNKNOWN,
    ),
)
def test_non_compatible_source_family_statuses_fail_closed(
    status: psfr.SourceFamilyCompatibilityStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(source_family_compatibility_status=status),
        f"source family compatibility status is {status.value}",
    )


@pytest.mark.parametrize(
    "status",
    (
        psfr.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        psfr.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        psfr.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(status: psfr.RuntimeGateStatus) -> None:
    _assert_blocked_with_reason(
        _valid_record(runtime_gate_status=status),
        f"runtime gate status is {status.value}",
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
