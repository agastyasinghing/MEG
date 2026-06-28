from pathlib import Path

import pytest

from meg.weather.stage2 import manual_review_gate_runtime as mrgr
from meg.weather.stage2 import no_lookahead_metadata_runtime as nlmr
from meg.weather.stage2 import provider_source_family_runtime as psfr
from meg.weather.stage2 import retrieval_context_runtime as rcr
from meg.weather.stage2 import source_identity_runtime as sir


MODULE_PATH = Path("meg/weather/stage2/no_lookahead_metadata_runtime.py")
TEST_PATH = Path("tests/core/test_weather_no_lookahead_metadata_runtime.py")


def _text(path: Path) -> str:
    return getattr(path, "read" + "_text")()


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
    source_identity = source_identity or _valid_source_identity()
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": source_identity,
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


def _valid_manual_review_gate(
    source_identity: sir.SourceIdentityRecord | None = None,
    retrieval_context: rcr.RetrievalContextRecord | None = None,
    provider_source_family: psfr.ProviderSourceFamilyRecord | None = None,
    **overrides: object,
) -> mrgr.ManualReviewGateRecord:
    source_identity = source_identity or _valid_source_identity()
    retrieval_context = retrieval_context or _valid_retrieval_context(source_identity)
    provider_source_family = provider_source_family or _valid_provider_source_family(
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


def _valid_manual_review_gate_mapping(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
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
    }
    values.update(overrides)
    return values


def _valid_record(**overrides: object) -> nlmr.NoLookaheadMetadataRecord:
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
    manual_review_gate = overrides.get("manual_review_gate")
    if not isinstance(manual_review_gate, mrgr.ManualReviewGateRecord):
        manual_review_gate = _valid_manual_review_gate(
            source_identity, retrieval_context, provider_source_family
        )
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": source_identity,
        "retrieval_context": retrieval_context,
        "provider_source_family": provider_source_family,
        "manual_review_gate": manual_review_gate,
        "available_at_utc": "2026-05-31T23:00:00Z",
        "decision_time_utc": "2026-06-01T01:00:00Z",
        "no_lookahead_verification_status": (
            nlmr.NoLookaheadVerificationStatus.NO_LOOKAHEAD_VERIFIED
        ),
        "availability_timing_status": (
            nlmr.AvailabilityTimingStatus.AVAILABILITY_BEFORE_DECISION
        ),
        "decision_timing_status": nlmr.DecisionTimingStatus.DECISION_TIME_RECORDED,
        "runtime_gate_status": nlmr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return nlmr.NoLookaheadMetadataRecord(**values)


def _assert_blocked_with_reason(record: nlmr.NoLookaheadMetadataRecord, reason: str) -> None:
    result = nlmr.validate_no_lookahead_metadata_record(record)
    assert result.passed is False
    assert result.severity is nlmr.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert nlmr.NoLookaheadVerificationStatus.values() == frozenset(
        {
            "no_lookahead_verified",
            "no_lookahead_missing",
            "no_lookahead_ambiguous",
            "no_lookahead_failed",
            "no_lookahead_unknown",
        }
    )
    assert nlmr.AvailabilityTimingStatus.values() == frozenset(
        {
            "availability_before_decision",
            "availability_at_decision",
            "availability_after_decision",
            "availability_missing",
            "availability_ambiguous",
            "availability_unknown",
        }
    )
    assert nlmr.DecisionTimingStatus.values() == frozenset(
        {
            "decision_time_recorded",
            "decision_time_missing",
            "decision_time_ambiguous",
            "decision_time_unknown",
        }
    )
    assert nlmr.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert nlmr.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_record(provenance_notes="no-lookahead note")

    assert record.condition_id == "condition-1"
    assert isinstance(record.source_identity, sir.SourceIdentityRecord)
    assert isinstance(record.retrieval_context, rcr.RetrievalContextRecord)
    assert isinstance(record.provider_source_family, psfr.ProviderSourceFamilyRecord)
    assert isinstance(record.manual_review_gate, mrgr.ManualReviewGateRecord)
    assert record.provenance_notes == "no-lookahead note"


def test_mapping_construction_with_nested_mappings_coerces_string_enums() -> None:
    record = nlmr.no_lookahead_metadata_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "source_identity": _valid_source_identity_mapping(),
            "retrieval_context": _valid_retrieval_context_mapping(),
            "provider_source_family": _valid_provider_source_family_mapping(),
            "manual_review_gate": _valid_manual_review_gate_mapping(),
            "available_at_utc": "2026-05-31T23:00:00Z",
            "decision_time_utc": "2026-06-01T01:00:00Z",
            "no_lookahead_verification_status": "no_lookahead_verified",
            "availability_timing_status": "availability_at_decision",
            "decision_timing_status": "decision_time_recorded",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "no-lookahead note",
        }
    )

    assert isinstance(record.source_identity, sir.SourceIdentityRecord)
    assert isinstance(record.retrieval_context, rcr.RetrievalContextRecord)
    assert isinstance(record.provider_source_family, psfr.ProviderSourceFamilyRecord)
    assert isinstance(record.manual_review_gate, mrgr.ManualReviewGateRecord)
    assert record.availability_timing_status is nlmr.AvailabilityTimingStatus.AVAILABILITY_AT_DECISION
    assert record.provenance_notes == "no-lookahead note"


def test_mapping_construction_accepts_already_built_records() -> None:
    source_identity = _valid_source_identity()
    retrieval_context = _valid_retrieval_context(source_identity)
    provider_source_family = _valid_provider_source_family(source_identity, retrieval_context)
    manual_review_gate = _valid_manual_review_gate(
        source_identity, retrieval_context, provider_source_family
    )

    record = nlmr.no_lookahead_metadata_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "Yes",
            "source_identity": source_identity,
            "retrieval_context": retrieval_context,
            "provider_source_family": provider_source_family,
            "manual_review_gate": manual_review_gate,
            "available_at_utc": "2026-05-31T23:00:00Z",
            "decision_time_utc": "2026-06-01T01:00:00Z",
            "no_lookahead_verification_status": "no_lookahead_verified",
            "availability_timing_status": "availability_before_decision",
            "decision_timing_status": "decision_time_recorded",
            "runtime_gate_status": "runtime_gate_ready",
        }
    )

    assert record.source_identity is source_identity
    assert record.retrieval_context is retrieval_context
    assert record.provider_source_family is provider_source_family
    assert record.manual_review_gate is manual_review_gate


@pytest.mark.parametrize(
    "availability_timing_status",
    [
        nlmr.AvailabilityTimingStatus.AVAILABILITY_BEFORE_DECISION,
        nlmr.AvailabilityTimingStatus.AVAILABILITY_AT_DECISION,
    ],
)
def test_minimal_valid_records_pass(availability_timing_status: nlmr.AvailabilityTimingStatus) -> None:
    result = nlmr.validate_no_lookahead_metadata_record(
        _valid_record(availability_timing_status=availability_timing_status)
    )

    assert result.passed is True
    assert result.severity is nlmr.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    [
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("available_at_utc", "available_at_utc is missing"),
        ("decision_time_utc", "decision_time_utc is missing"),
    ],
)
def test_blank_top_level_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_record(**{field_name: " "}), reason)


@pytest.mark.parametrize(
    ("nested_factory", "field_name", "reason"),
    [
        (_valid_source_identity, "condition_id", "condition_id does not match source identity"),
        (_valid_source_identity, "token_id", "token_id does not match source identity"),
        (_valid_source_identity, "outcome", "outcome does not match source identity"),
        (_valid_retrieval_context, "condition_id", "condition_id does not match retrieval context"),
        (_valid_retrieval_context, "token_id", "token_id does not match retrieval context"),
        (_valid_retrieval_context, "outcome", "outcome does not match retrieval context"),
        (_valid_provider_source_family, "condition_id", "condition_id does not match provider source family"),
        (_valid_provider_source_family, "token_id", "token_id does not match provider source family"),
        (_valid_provider_source_family, "outcome", "outcome does not match provider source family"),
        (_valid_manual_review_gate, "condition_id", "condition_id does not match manual review gate"),
        (_valid_manual_review_gate, "token_id", "token_id does not match manual review gate"),
        (_valid_manual_review_gate, "outcome", "outcome does not match manual review gate"),
    ],
)
def test_canonical_mismatches_against_nested_records_fail_closed(
    nested_factory: object, field_name: str, reason: str
) -> None:
    nested_record = nested_factory(**{field_name: f"different-{field_name}"})
    if isinstance(nested_record, sir.SourceIdentityRecord):
        record = _valid_record(source_identity=nested_record)
    elif isinstance(nested_record, rcr.RetrievalContextRecord):
        record = _valid_record(retrieval_context=nested_record)
    elif isinstance(nested_record, psfr.ProviderSourceFamilyRecord):
        record = _valid_record(provider_source_family=nested_record)
    else:
        record = _valid_record(manual_review_gate=nested_record)

    _assert_blocked_with_reason(record, reason)


def test_available_at_mismatch_against_retrieval_context_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_record(available_at_utc="2026-05-31T22:00:00Z"),
        "available_at_utc does not match retrieval context",
    )


def test_decision_time_mismatch_against_retrieval_context_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_record(decision_time_utc="2026-06-01T02:00:00Z"),
        "decision_time_utc does not match retrieval context",
    )


def test_invalid_nested_source_identity_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_record(source_identity=_valid_source_identity(source_id="")),
        "source identity validation failed",
    )


def test_invalid_nested_retrieval_context_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_record(retrieval_context=_valid_retrieval_context(accessed_at_utc="")),
        "retrieval context validation failed",
    )


def test_invalid_nested_provider_source_family_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_record(provider_source_family=_valid_provider_source_family(source_family="")),
        "provider source family validation failed",
    )


def test_invalid_nested_manual_review_gate_fails_closed() -> None:
    _assert_blocked_with_reason(
        _valid_record(manual_review_gate=_valid_manual_review_gate(reviewer_id="")),
        "manual review gate validation failed",
    )


@pytest.mark.parametrize(
    "status",
    [
        nlmr.NoLookaheadVerificationStatus.NO_LOOKAHEAD_MISSING,
        nlmr.NoLookaheadVerificationStatus.NO_LOOKAHEAD_AMBIGUOUS,
        nlmr.NoLookaheadVerificationStatus.NO_LOOKAHEAD_FAILED,
        nlmr.NoLookaheadVerificationStatus.NO_LOOKAHEAD_UNKNOWN,
    ],
)
def test_non_verified_no_lookahead_statuses_fail_closed(
    status: nlmr.NoLookaheadVerificationStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(no_lookahead_verification_status=status),
        f"no-lookahead verification status is {status.value}",
    )


@pytest.mark.parametrize(
    "status",
    [
        nlmr.AvailabilityTimingStatus.AVAILABILITY_AFTER_DECISION,
        nlmr.AvailabilityTimingStatus.AVAILABILITY_MISSING,
        nlmr.AvailabilityTimingStatus.AVAILABILITY_AMBIGUOUS,
        nlmr.AvailabilityTimingStatus.AVAILABILITY_UNKNOWN,
    ],
)
def test_disallowed_availability_timing_statuses_fail_closed(
    status: nlmr.AvailabilityTimingStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(availability_timing_status=status),
        f"availability timing status is {status.value}",
    )


@pytest.mark.parametrize(
    "status",
    [
        nlmr.DecisionTimingStatus.DECISION_TIME_MISSING,
        nlmr.DecisionTimingStatus.DECISION_TIME_AMBIGUOUS,
        nlmr.DecisionTimingStatus.DECISION_TIME_UNKNOWN,
    ],
)
def test_non_recorded_decision_timing_statuses_fail_closed(
    status: nlmr.DecisionTimingStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(decision_timing_status=status),
        f"decision timing status is {status.value}",
    )


@pytest.mark.parametrize(
    "status",
    [
        nlmr.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        nlmr.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        nlmr.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ],
)
def test_non_ready_runtime_gate_statuses_fail_closed(status: nlmr.RuntimeGateStatus) -> None:
    _assert_blocked_with_reason(
        _valid_record(runtime_gate_status=status),
        f"runtime gate status is {status.value}",
    )


def test_changed_files_do_not_contain_legacy_identifier_text() -> None:
    forbidden = "market" + "_id"
    assert forbidden not in _text(MODULE_PATH)
    assert forbidden not in _text(TEST_PATH)


def test_module_source_does_not_contain_forbidden_execution_terms() -> None:
    module_source = _text(MODULE_PATH)
    forbidden_terms = (
        "req" + "uests",
        "htt" + "px",
        "url" + "lib",
        "aio" + "http",
        "bo" + "to3",
        "poly" + "market",
        "sub" + "process",
        "open" + "(",
        ".read" + "_text(",
        ".write" + "_text(",
        "sock" + "et",
        "os" + ".environ",
        "dot" + "env",
    )

    for term in forbidden_terms:
        assert term not in module_source
