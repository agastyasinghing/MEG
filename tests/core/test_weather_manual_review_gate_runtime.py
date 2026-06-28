from pathlib import Path

import pytest

from meg.weather.stage2 import manual_review_gate_runtime as mrgr
from meg.weather.stage2 import provider_source_family_runtime as psfr
from meg.weather.stage2 import retrieval_context_runtime as rcr
from meg.weather.stage2 import source_identity_runtime as sir


MODULE_PATH = Path("meg/weather/stage2/manual_review_gate_runtime.py")
TEST_PATH = Path("tests/core/test_weather_manual_review_gate_runtime.py")


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


def _valid_provider_source_family(
    source_identity: sir.SourceIdentityRecord | None = None,
    retrieval_context: rcr.RetrievalContextRecord | None = None,
    **overrides: object,
) -> psfr.ProviderSourceFamilyRecord:
    source_identity = source_identity or _valid_source_identity()
    retrieval_context = retrieval_context or _valid_retrieval_context(source_identity)
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": source_identity,
        "retrieval_context": retrieval_context,
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


def _valid_provider_source_family_mapping(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
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
    }
    values.update(overrides)
    return values


def _valid_record(**overrides: object) -> mrgr.ManualReviewGateRecord:
    source_identity = overrides.get("source_identity")
    if not isinstance(source_identity, sir.SourceIdentityRecord):
        source_identity = _valid_source_identity()
    retrieval_context = overrides.get("retrieval_context")
    if not isinstance(retrieval_context, rcr.RetrievalContextRecord):
        retrieval_context = _valid_retrieval_context(source_identity)
    provider_source_family = overrides.get("provider_source_family")
    if not isinstance(provider_source_family, psfr.ProviderSourceFamilyRecord):
        provider_source_family = _valid_provider_source_family(
            source_identity, retrieval_context
        )
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": source_identity,
        "retrieval_context": retrieval_context,
        "provider_source_family": provider_source_family,
        "manual_review_status": mrgr.ManualReviewStatus.MANUAL_REVIEW_COMPLETED,
        "reviewer_authority_status": (
            mrgr.ReviewerAuthorityStatus.REVIEWER_AUTHORITY_CONFIRMED
        ),
        "manual_review_decision": mrgr.ManualReviewDecision.APPROVED_FOR_METADATA_USE,
        "reviewer_id": "reviewer-1",
        "reviewed_at_utc": "2026-06-01T02:00:00Z",
        "runtime_gate_status": mrgr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return mrgr.ManualReviewGateRecord(**values)


def _assert_blocked_with_reason(record: mrgr.ManualReviewGateRecord, reason: str) -> None:
    result = mrgr.validate_manual_review_gate_record(record)
    assert result.passed is False
    assert result.severity is mrgr.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert mrgr.ManualReviewStatus.values() == frozenset(
        {
            "manual_review_completed",
            "manual_review_required",
            "manual_review_missing",
            "manual_review_ambiguous",
            "manual_review_rejected",
            "manual_review_unknown",
        }
    )
    assert mrgr.ReviewerAuthorityStatus.values() == frozenset(
        {
            "reviewer_authority_confirmed",
            "reviewer_authority_missing",
            "reviewer_authority_ambiguous",
            "reviewer_authority_unknown",
        }
    )
    assert mrgr.ManualReviewDecision.values() == frozenset(
        {
            "approved_for_metadata_use",
            "rejected_for_metadata_use",
            "requires_revision",
            "not_decided",
            "unknown_requires_review",
        }
    )
    assert mrgr.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert mrgr.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_record(provenance_notes="manual gate note")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert isinstance(record.source_identity, sir.SourceIdentityRecord)
    assert isinstance(record.retrieval_context, rcr.RetrievalContextRecord)
    assert isinstance(record.provider_source_family, psfr.ProviderSourceFamilyRecord)
    assert record.reviewer_id == "reviewer-1"
    assert record.reviewed_at_utc == "2026-06-01T02:00:00Z"
    assert record.provenance_notes == "manual gate note"


def test_mapping_construction_with_nested_mappings_coerces_string_enums() -> None:
    record = mrgr.manual_review_gate_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "source_identity": _valid_source_identity_mapping(),
            "retrieval_context": _valid_retrieval_context_mapping(),
            "provider_source_family": _valid_provider_source_family_mapping(),
            "manual_review_status": "manual_review_completed",
            "reviewer_authority_status": "reviewer_authority_confirmed",
            "manual_review_decision": "approved_for_metadata_use",
            "reviewer_id": "reviewer-1",
            "reviewed_at_utc": "2026-06-01T02:00:00Z",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "manual gate note",
        }
    )

    assert isinstance(record.source_identity, sir.SourceIdentityRecord)
    assert isinstance(record.retrieval_context, rcr.RetrievalContextRecord)
    assert isinstance(record.provider_source_family, psfr.ProviderSourceFamilyRecord)
    assert record.manual_review_status is mrgr.ManualReviewStatus.MANUAL_REVIEW_COMPLETED
    assert record.reviewer_authority_status is (
        mrgr.ReviewerAuthorityStatus.REVIEWER_AUTHORITY_CONFIRMED
    )
    assert record.manual_review_decision is mrgr.ManualReviewDecision.APPROVED_FOR_METADATA_USE
    assert record.runtime_gate_status is mrgr.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "manual gate note"


def test_mapping_construction_accepts_built_dependency_records() -> None:
    source_identity = _valid_source_identity()
    retrieval_context = _valid_retrieval_context(source_identity)
    provider_source_family = _valid_provider_source_family(source_identity, retrieval_context)

    record = mrgr.manual_review_gate_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "source_identity": source_identity,
            "retrieval_context": retrieval_context,
            "provider_source_family": provider_source_family,
            "manual_review_status": "manual_review_completed",
            "reviewer_authority_status": "reviewer_authority_confirmed",
            "manual_review_decision": "approved_for_metadata_use",
            "reviewer_id": "reviewer-1",
            "reviewed_at_utc": "2026-06-01T02:00:00Z",
            "runtime_gate_status": "runtime_gate_ready",
        }
    )

    assert record.source_identity is source_identity
    assert record.retrieval_context is retrieval_context
    assert record.provider_source_family is provider_source_family


def test_minimal_valid_record_passes() -> None:
    result = mrgr.validate_manual_review_gate_record(_valid_record())

    assert result.passed is True
    assert result.severity is mrgr.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("reviewer_id", "reviewer_id is missing"),
        ("reviewed_at_utc", "reviewed_at_utc is missing"),
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
    source_identity = _valid_source_identity()
    retrieval_context = _valid_retrieval_context(source_identity, **{field_name: value})
    provider_source_family = _valid_provider_source_family(source_identity)
    _assert_blocked_with_reason(
        _valid_record(
            retrieval_context=retrieval_context,
            provider_source_family=provider_source_family,
        ),
        reason,
    )


@pytest.mark.parametrize(
    ("field_name", "value", "reason"),
    (
        (
            "condition_id",
            "other-condition",
            "condition_id does not match provider source family",
        ),
        ("token_id", "other-token", "token_id does not match provider source family"),
        ("outcome", "No", "outcome does not match provider source family"),
    ),
)
def test_canonical_field_mismatch_against_provider_source_family_fails_closed(
    field_name: str, value: str, reason: str
) -> None:
    provider_source_family = _valid_provider_source_family(**{field_name: value})
    _assert_blocked_with_reason(
        _valid_record(provider_source_family=provider_source_family), reason
    )


def test_invalid_nested_source_identity_fails_closed() -> None:
    source_identity = _valid_source_identity(source_id="  ")
    retrieval_context = _valid_retrieval_context(source_identity)
    provider_source_family = _valid_provider_source_family(source_identity, retrieval_context)

    _assert_blocked_with_reason(
        _valid_record(
            source_identity=source_identity,
            retrieval_context=retrieval_context,
            provider_source_family=provider_source_family,
        ),
        "source identity validation failed",
    )


def test_invalid_nested_retrieval_context_fails_closed() -> None:
    source_identity = _valid_source_identity()
    retrieval_context = _valid_retrieval_context(source_identity, accessed_at_utc="  ")
    provider_source_family = _valid_provider_source_family(source_identity)

    _assert_blocked_with_reason(
        _valid_record(
            retrieval_context=retrieval_context,
            provider_source_family=provider_source_family,
        ),
        "retrieval context validation failed",
    )


def test_invalid_nested_provider_source_family_fails_closed() -> None:
    provider_source_family = _valid_provider_source_family(
        provider_execution_posture=psfr.ProviderExecutionPosture.PROVIDER_EXECUTION_NOT_APPROVED
    )

    _assert_blocked_with_reason(
        _valid_record(provider_source_family=provider_source_family),
        "provider source family validation failed",
    )


@pytest.mark.parametrize(
    "status",
    tuple(
        status
        for status in mrgr.ManualReviewStatus
        if status is not mrgr.ManualReviewStatus.MANUAL_REVIEW_COMPLETED
    ),
)
def test_non_completed_manual_review_statuses_fail_closed(
    status: mrgr.ManualReviewStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(manual_review_status=status),
        f"manual review status is {status.value}",
    )


@pytest.mark.parametrize(
    "status",
    tuple(
        status
        for status in mrgr.ReviewerAuthorityStatus
        if status is not mrgr.ReviewerAuthorityStatus.REVIEWER_AUTHORITY_CONFIRMED
    ),
)
def test_non_confirmed_reviewer_authority_statuses_fail_closed(
    status: mrgr.ReviewerAuthorityStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(reviewer_authority_status=status),
        f"reviewer authority status is {status.value}",
    )


@pytest.mark.parametrize(
    "decision",
    tuple(
        decision
        for decision in mrgr.ManualReviewDecision
        if decision is not mrgr.ManualReviewDecision.APPROVED_FOR_METADATA_USE
    ),
)
def test_non_approved_manual_review_decisions_fail_closed(
    decision: mrgr.ManualReviewDecision,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(manual_review_decision=decision),
        f"manual review decision is {decision.value}",
    )


@pytest.mark.parametrize(
    "status",
    (
        mrgr.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        mrgr.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        mrgr.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(status: mrgr.RuntimeGateStatus) -> None:
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
