from pathlib import Path

import pytest

from meg.weather.stage2 import manual_review_gate_runtime as mrgr
from meg.weather.stage2 import fail_closed_validation_runtime as fcvr
from meg.weather.stage2 import static_audit_surface_runtime as sasr
from meg.weather.stage2 import no_lookahead_metadata_runtime as nlmr
from meg.weather.stage2 import provider_source_family_runtime as psfr
from meg.weather.stage2 import retrieval_context_runtime as rcr
from meg.weather.stage2 import source_identity_runtime as sir


MODULE_PATH = Path("meg/weather/stage2/static_audit_surface_runtime.py")
TEST_PATH = Path("tests/core/test_weather_static_audit_surface_runtime.py")


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


def _valid_no_lookahead_metadata(**overrides: object) -> nlmr.NoLookaheadMetadataRecord:
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


def _valid_no_lookahead_metadata_mapping(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
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
        "availability_timing_status": "availability_before_decision",
        "decision_timing_status": "decision_time_recorded",
        "runtime_gate_status": "runtime_gate_ready",
    }
    values.update(overrides)
    return values


def _valid_record(**overrides: object) -> fcvr.FailClosedValidationRecord:
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
    no_lookahead_metadata = overrides.get("no_lookahead_metadata")
    if not isinstance(no_lookahead_metadata, nlmr.NoLookaheadMetadataRecord):
        no_lookahead_metadata = _valid_no_lookahead_metadata(
            source_identity=source_identity,
            retrieval_context=retrieval_context,
            provider_source_family=provider_source_family,
            manual_review_gate=manual_review_gate,
        )
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": source_identity,
        "retrieval_context": retrieval_context,
        "provider_source_family": provider_source_family,
        "manual_review_gate": manual_review_gate,
        "no_lookahead_metadata": no_lookahead_metadata,
        "aggregate_validation_status": fcvr.AggregateValidationStatus.AGGREGATE_VALIDATION_PASSED,
        "dependency_validation_status": fcvr.DependencyValidationStatus.ALL_DEPENDENCIES_VALIDATED,
        "fail_closed_posture": fcvr.FailClosedPosture.FAIL_CLOSED_ENFORCED,
        "runtime_gate_status": fcvr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return fcvr.FailClosedValidationRecord(**values)


def _valid_mapping(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": _valid_source_identity_mapping(),
        "retrieval_context": _valid_retrieval_context_mapping(),
        "provider_source_family": _valid_provider_source_family_mapping(),
        "manual_review_gate": _valid_manual_review_gate_mapping(),
        "no_lookahead_metadata": _valid_no_lookahead_metadata_mapping(),
        "aggregate_validation_status": "aggregate_validation_passed",
        "dependency_validation_status": "all_dependencies_validated",
        "fail_closed_posture": "fail_closed_enforced",
        "runtime_gate_status": "runtime_gate_ready",
    }
    values.update(overrides)
    return values


def _assert_blocked_with_reason(
    record: fcvr.FailClosedValidationRecord, reason: str
) -> None:
    result = fcvr.validate_fail_closed_validation_record(record)
    assert result.passed is False
    assert result.severity is fcvr.ValidationSeverity.BLOCKED
    assert reason in result.reasons




def _valid_fail_closed_validation(**overrides: object) -> fcvr.FailClosedValidationRecord:
    return _valid_record(**overrides)


def _valid_fail_closed_validation_mapping(**overrides: object) -> dict[str, object]:
    return _valid_mapping(**overrides)


def _valid_static_record(**overrides: object) -> sasr.StaticAuditSurfaceRecord:
    source_identity = overrides.get("source_identity")
    if not isinstance(source_identity, sir.SourceIdentityRecord):
        source_identity = _valid_source_identity()
    retrieval_context = overrides.get("retrieval_context")
    if not isinstance(retrieval_context, rcr.RetrievalContextRecord):
        retrieval_context = _valid_retrieval_context(source_identity)
    provider_source_family = overrides.get("provider_source_family")
    if not isinstance(provider_source_family, psfr.ProviderSourceFamilyRecord):
        provider_source_family = _valid_provider_source_family(source_identity, retrieval_context)
    manual_review_gate = overrides.get("manual_review_gate")
    if not isinstance(manual_review_gate, mrgr.ManualReviewGateRecord):
        manual_review_gate = _valid_manual_review_gate(source_identity, retrieval_context, provider_source_family)
    no_lookahead_metadata = overrides.get("no_lookahead_metadata")
    if not isinstance(no_lookahead_metadata, nlmr.NoLookaheadMetadataRecord):
        no_lookahead_metadata = _valid_no_lookahead_metadata(
            source_identity=source_identity,
            retrieval_context=retrieval_context,
            provider_source_family=provider_source_family,
            manual_review_gate=manual_review_gate,
        )
    fail_closed_validation = overrides.get("fail_closed_validation")
    if not isinstance(fail_closed_validation, fcvr.FailClosedValidationRecord):
        fail_closed_validation = _valid_fail_closed_validation(
            source_identity=source_identity,
            retrieval_context=retrieval_context,
            provider_source_family=provider_source_family,
            manual_review_gate=manual_review_gate,
            no_lookahead_metadata=no_lookahead_metadata,
        )
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": source_identity,
        "retrieval_context": retrieval_context,
        "provider_source_family": provider_source_family,
        "manual_review_gate": manual_review_gate,
        "no_lookahead_metadata": no_lookahead_metadata,
        "fail_closed_validation": fail_closed_validation,
        "static_audit_surface_status": sasr.StaticAuditSurfaceStatus.STATIC_AUDIT_SURFACE_RECORDED,
        "audit_presentation_mode": sasr.AuditPresentationMode.READ_ONLY_SUMMARY,
        "audit_evidence_status": sasr.AuditEvidenceStatus.ALL_REQUIRED_METADATA_VALIDATED,
        "runtime_gate_status": sasr.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return sasr.StaticAuditSurfaceRecord(**values)


def _valid_static_mapping(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_identity": _valid_source_identity_mapping(),
        "retrieval_context": _valid_retrieval_context_mapping(),
        "provider_source_family": _valid_provider_source_family_mapping(),
        "manual_review_gate": _valid_manual_review_gate_mapping(),
        "no_lookahead_metadata": _valid_no_lookahead_metadata_mapping(),
        "fail_closed_validation": _valid_fail_closed_validation_mapping(),
        "static_audit_surface_status": "static_audit_surface_recorded",
        "audit_presentation_mode": "read_only_summary",
        "audit_evidence_status": "all_required_metadata_validated",
        "runtime_gate_status": "runtime_gate_ready",
    }
    values.update(overrides)
    return values


def _assert_blocked_with_reason(record: sasr.StaticAuditSurfaceRecord, reason: str) -> None:
    result = sasr.validate_static_audit_surface_record(record)
    assert result.passed is False
    assert result.severity is sasr.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert sasr.StaticAuditSurfaceStatus.values() == frozenset({
        "static_audit_surface_recorded", "static_audit_surface_missing",
        "static_audit_surface_ambiguous", "static_audit_surface_unknown",
    })
    assert sasr.AuditPresentationMode.values() == frozenset({
        "read_only_summary", "read_only_detail", "write_report_not_approved",
        "external_export_not_approved", "unknown_requires_review",
    })
    assert sasr.AuditEvidenceStatus.values() == frozenset({
        "all_required_metadata_validated", "metadata_validation_failed",
        "metadata_validation_missing", "metadata_validation_unknown",
    })
    assert sasr.RuntimeGateStatus.values() == frozenset({
        "runtime_gate_ready", "runtime_gate_blocked",
        "runtime_gate_requires_manual_review", "runtime_gate_unknown",
    })
    assert sasr.ValidationSeverity.values() == frozenset({"passed", "caution", "failed", "blocked"})


def test_dataclass_construction_and_valid_record_passes() -> None:
    record = _valid_static_record(provenance_notes="supplied metadata only")
    assert record.provenance_notes == "supplied metadata only"
    assert sasr.validate_static_audit_surface_record(record) == sasr.StaticAuditSurfaceValidationResult(
        severity=sasr.ValidationSeverity.PASSED, passed=True
    )


@pytest.mark.parametrize("mode", [sasr.AuditPresentationMode.READ_ONLY_SUMMARY, sasr.AuditPresentationMode.READ_ONLY_DETAIL])
def test_minimal_valid_static_audit_records_pass_for_read_only_modes(mode: sasr.AuditPresentationMode) -> None:
    result = sasr.validate_static_audit_surface_record(_valid_static_record(audit_presentation_mode=mode))
    assert result.passed is True


def test_mapping_construction_with_nested_mappings() -> None:
    record = sasr.static_audit_surface_record_from_mapping(_valid_static_mapping())
    assert isinstance(record.source_identity, sir.SourceIdentityRecord)
    assert isinstance(record.retrieval_context, rcr.RetrievalContextRecord)
    assert isinstance(record.provider_source_family, psfr.ProviderSourceFamilyRecord)
    assert isinstance(record.manual_review_gate, mrgr.ManualReviewGateRecord)
    assert isinstance(record.no_lookahead_metadata, nlmr.NoLookaheadMetadataRecord)
    assert isinstance(record.fail_closed_validation, fcvr.FailClosedValidationRecord)
    assert record.static_audit_surface_status is sasr.StaticAuditSurfaceStatus.STATIC_AUDIT_SURFACE_RECORDED


def test_mapping_construction_accepts_built_dependency_records() -> None:
    source_identity = _valid_source_identity()
    retrieval_context = _valid_retrieval_context(source_identity)
    provider_source_family = _valid_provider_source_family(source_identity, retrieval_context)
    manual_review_gate = _valid_manual_review_gate(source_identity, retrieval_context, provider_source_family)
    no_lookahead_metadata = _valid_no_lookahead_metadata(
        source_identity=source_identity, retrieval_context=retrieval_context,
        provider_source_family=provider_source_family, manual_review_gate=manual_review_gate,
    )
    fail_closed_validation = _valid_fail_closed_validation(
        source_identity=source_identity, retrieval_context=retrieval_context,
        provider_source_family=provider_source_family, manual_review_gate=manual_review_gate,
        no_lookahead_metadata=no_lookahead_metadata,
    )
    record = sasr.static_audit_surface_record_from_mapping(_valid_static_mapping(
        source_identity=source_identity, retrieval_context=retrieval_context,
        provider_source_family=provider_source_family, manual_review_gate=manual_review_gate,
        no_lookahead_metadata=no_lookahead_metadata, fail_closed_validation=fail_closed_validation,
    ))
    assert record.source_identity is source_identity
    assert record.retrieval_context is retrieval_context
    assert record.provider_source_family is provider_source_family
    assert record.manual_review_gate is manual_review_gate
    assert record.no_lookahead_metadata is no_lookahead_metadata
    assert record.fail_closed_validation is fail_closed_validation


def test_static_audit_summary_is_deterministic_read_only_tuple() -> None:
    summary = sasr.static_audit_summary(_valid_static_record())
    assert summary == (
        "condition_id=condition-1", "token_id=token-1", "outcome=Yes",
        "static_audit_surface_status=static_audit_surface_recorded",
        "audit_presentation_mode=read_only_summary",
        "audit_evidence_status=all_required_metadata_validated",
        "runtime_gate_status=runtime_gate_ready",
    )


@pytest.mark.parametrize(("field_name", "reason"), [
    ("condition_id", "condition_id is missing"),
    ("token_id", "token_id is missing"),
    ("outcome", "outcome is missing"),
])
def test_blank_canonical_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_static_record(**{field_name: " "}), reason)


@pytest.mark.parametrize(("dependency_name", "record", "reason"), [
    ("source_identity", _valid_source_identity(condition_id="other"), "condition_id does not match source identity"),
    ("retrieval_context", _valid_retrieval_context(condition_id="other"), "condition_id does not match retrieval context"),
    ("provider_source_family", _valid_provider_source_family(condition_id="other"), "condition_id does not match provider source family"),
    ("manual_review_gate", _valid_manual_review_gate(condition_id="other"), "condition_id does not match manual review gate"),
    ("no_lookahead_metadata", _valid_no_lookahead_metadata(condition_id="other"), "condition_id does not match no-lookahead metadata"),
    ("fail_closed_validation", _valid_fail_closed_validation(condition_id="other"), "condition_id does not match fail-closed validation"),
])
def test_canonical_condition_mismatches_fail_closed(dependency_name: str, record: object, reason: str) -> None:
    _assert_blocked_with_reason(_valid_static_record(**{dependency_name: record}), reason)


@pytest.mark.parametrize(("dependency_name", "record", "reason"), [
    ("source_identity", _valid_source_identity(source_id=" "), "source identity validation failed"),
    ("retrieval_context", _valid_retrieval_context(accessed_at_utc=" "), "retrieval context validation failed"),
    ("provider_source_family", _valid_provider_source_family(source_family=" "), "provider source family validation failed"),
    ("manual_review_gate", _valid_manual_review_gate(reviewer_id=" "), "manual review gate validation failed"),
    ("no_lookahead_metadata", _valid_no_lookahead_metadata(available_at_utc=" "), "no-lookahead metadata validation failed"),
    ("fail_closed_validation", _valid_fail_closed_validation(fail_closed_posture=fcvr.FailClosedPosture.FAIL_CLOSED_MISSING), "fail-closed validation failed"),
])
def test_invalid_nested_dependency_records_fail_closed(dependency_name: str, record: object, reason: str) -> None:
    _assert_blocked_with_reason(_valid_static_record(**{dependency_name: record}), reason)


@pytest.mark.parametrize("status", [s for s in sasr.StaticAuditSurfaceStatus if s is not sasr.StaticAuditSurfaceStatus.STATIC_AUDIT_SURFACE_RECORDED])
def test_non_recorded_static_audit_surface_statuses_fail_closed(status: sasr.StaticAuditSurfaceStatus) -> None:
    _assert_blocked_with_reason(_valid_static_record(static_audit_surface_status=status), f"static audit surface status is {status.value}")


@pytest.mark.parametrize("mode", [
    sasr.AuditPresentationMode.WRITE_REPORT_NOT_APPROVED,
    sasr.AuditPresentationMode.EXTERNAL_EXPORT_NOT_APPROVED,
    sasr.AuditPresentationMode.UNKNOWN_REQUIRES_REVIEW,
])
def test_disallowed_audit_presentation_modes_fail_closed(mode: sasr.AuditPresentationMode) -> None:
    _assert_blocked_with_reason(_valid_static_record(audit_presentation_mode=mode), f"audit presentation mode is {mode.value}")


@pytest.mark.parametrize("status", [s for s in sasr.AuditEvidenceStatus if s is not sasr.AuditEvidenceStatus.ALL_REQUIRED_METADATA_VALIDATED])
def test_non_validated_audit_evidence_statuses_fail_closed(status: sasr.AuditEvidenceStatus) -> None:
    _assert_blocked_with_reason(_valid_static_record(audit_evidence_status=status), f"audit evidence status is {status.value}")


@pytest.mark.parametrize("status", [
    sasr.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
    sasr.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
    sasr.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
])
def test_non_ready_runtime_gate_statuses_fail_closed(status: sasr.RuntimeGateStatus) -> None:
    _assert_blocked_with_reason(_valid_static_record(runtime_gate_status=status), f"runtime gate status is {status.value}")


def test_new_files_do_not_contain_disallowed_identifier() -> None:
    assert "market" + "_id" not in _text(MODULE_PATH)
    assert "market" + "_id" not in _text(TEST_PATH)


def test_module_does_not_contain_forbidden_calls_or_imports() -> None:
    text = _text(MODULE_PATH)
    forbidden_terms = (
        "requests", "httpx", "urllib", "aiohttp", "boto3", "polymarket",
        "subprocess", "open(", ".read" + "_text(", ".write" + "_text(",
        "socket", "os.environ", "dotenv",
    )
    for term in forbidden_terms:
        assert term not in text
