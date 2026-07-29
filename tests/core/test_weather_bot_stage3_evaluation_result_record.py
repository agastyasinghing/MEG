from __future__ import annotations

from collections.abc import Mapping
from dataclasses import FrozenInstanceError, fields
import inspect

import pytest

from meg.weather.stage3.baseline_contracts import BaselineType
from meg.weather.stage3.evaluation_result_record import (
    CalibrationBinResultPayload,
    DecompositionResultPayload,
    DistributionDiagnosticResultPayload,
    EnsembleDiagnosticResultPayload,
    EvaluationResultKind,
    EvaluationResultMethodRole,
    EvaluationResultRecord,
    EvaluationResultSupportStatus,
    EvaluationResultValidationCode,
    EvaluationResultValidationResult,
    EvaluationResultValidationSeverity,
    PairedComparisonResultPayload,
    ScalarScoreResultPayload,
    evaluation_result_record_from_mapping,
    validate_evaluation_result_record,
)
from meg.weather.stage3.scoring_and_diagnostics import (
    ScoringArtifact,
    ScoringPredictionRepresentation,
)


def _payload() -> ScalarScoreResultPayload:
    return ScalarScoreResultPayload(0.25, "lower_is_better", "artifact_specific_domain_validated")


def _values(**changes: object) -> dict[str, object]:
    values: dict[str, object] = {
        "evaluation_result_id": "result-1", "result_kind": EvaluationResultKind.SCALAR_SCORE_RESULT,
        "artifact_id": ScoringArtifact.BRIER_SCORE, "artifact_version": "1",
        "evaluation_definition_id": "definition-1", "evaluation_definition_version": "1",
        "evaluation_run_id": "run-1", "method_role": EvaluationResultMethodRole.CANDIDATE,
        "method_id": "method-1", "method_version": "1",
        "prediction_representation": ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        "target_posture": "venue_defined_settlement_outcome", "split_id": "split-1",
        "split_version": "1", "fold_id": "fold-1", "cutoff_identity": "cutoff-1",
        "paired_test_record_set_id": "set-1", "eligibility_policy_id": "eligible-1",
        "aggregation_rule_id": "aggregate-1", "weighting_rule_id": "weight-1",
        "stratum_id": "all", "eligible_record_count": 2, "excluded_record_count": 0,
        "blocked_record_count": 0, "total_considered_record_count": 2,
        "exclusion_block_reason_summary": (), "uncertainty_method_id": None,
        "uncertainty_level_id": None, "support_status": EvaluationResultSupportStatus.SUPPORTED,
        "result_payload": _payload(), "provenance": ("source-1",),
        "result_created_at": "2026-07-27T12:00:00Z",
        "supersedes_result_id_when_applicable": None,
    }
    values.update(changes)
    return values


def _codes(**changes: object) -> tuple[EvaluationResultValidationCode, ...]:
    return validate_evaluation_result_record(EvaluationResultRecord(**_values(**changes))).codes


def test_public_contract_and_frozen_shapes() -> None:
    import meg.weather.stage3.evaluation_result_record as module

    assert module.__all__ == (
        "EvaluationResultKind", "EvaluationResultSupportStatus", "EvaluationResultMethodRole",
        "EvaluationResultValidationSeverity", "EvaluationResultValidationCode",
        "ScalarScoreResultPayload", "CalibrationBinResultPayload", "DecompositionResultPayload",
        "DistributionDiagnosticResultPayload", "EnsembleDiagnosticResultPayload",
        "PairedComparisonResultPayload", "EvaluationResultRecord",
        "EvaluationResultValidationResult", "evaluation_result_record_from_mapping",
        "validate_evaluation_result_record",
    )
    assert len(EvaluationResultValidationCode) == 30
    assert tuple(member.value for member in EvaluationResultValidationCode) == tuple(
        name.lower() for name in (
            "MISSING_REQUIRED_FIELD", "UNEXPECTED_FIELD", "BLANK_REQUIRED_TEXT",
            "INVALID_RESULT_KIND", "INVALID_ARTIFACT", "INVALID_METHOD_ROLE",
            "INVALID_PREDICTION_REPRESENTATION", "INVALID_SUPPORT_STATUS",
            "INVALID_FIXED_POSTURE", "INVALID_RECORD_COUNT", "SAMPLE_ACCOUNTING_MISMATCH",
            "INVALID_REASON_SUMMARY", "MISSING_REQUIRED_REASON", "UNCERTAINTY_FIELDS_MISMATCH",
            "EMPTY_PROVENANCE", "INVALID_PROVENANCE_REF", "INVALID_RESULT_CREATED_AT",
            "RESULT_KIND_ARTIFACT_MISMATCH", "REPRESENTATION_MISMATCH", "METHOD_ROLE_MISMATCH",
            "INVALID_PAYLOAD_TYPE", "INVALID_SCALAR_SCORE_PAYLOAD",
            "INVALID_CALIBRATION_BIN_PAYLOAD", "INVALID_DECOMPOSITION_PAYLOAD",
            "INVALID_DISTRIBUTION_DIAGNOSTIC_PAYLOAD", "INVALID_ENSEMBLE_DIAGNOSTIC_PAYLOAD",
            "INVALID_PAIRED_COMPARISON_PAYLOAD", "PAIR_BASELINE_NOT_APPROVED",
            "PAIR_RESULT_IDENTITY_COLLISION", "SELF_SUPERSESSION",
        )
    )
    assert len(fields(EvaluationResultRecord)) == 33
    record = EvaluationResultRecord(**_values())
    with pytest.raises(FrozenInstanceError):
        record.method_id = "changed"  # type: ignore[misc]
    assert tuple(inspect.signature(evaluation_result_record_from_mapping).parameters) == ("mapping",)
    assert tuple(inspect.signature(validate_evaluation_result_record).parameters) == ("record",)


def test_validation_result_forces_invariants() -> None:
    passed = EvaluationResultValidationResult(EvaluationResultValidationSeverity.BLOCKED, False)
    blocked = EvaluationResultValidationResult(
        EvaluationResultValidationSeverity.PASSED, True,
        [EvaluationResultValidationCode.INVALID_ARTIFACT],  # type: ignore[arg-type]
    )
    assert (passed.severity, passed.passed, passed.codes) == (EvaluationResultValidationSeverity.PASSED, True, ())
    assert (blocked.severity, blocked.passed, blocked.codes) == (
        EvaluationResultValidationSeverity.BLOCKED, False,
        (EvaluationResultValidationCode.INVALID_ARTIFACT,),
    )


def test_valid_direct_and_mapping_records() -> None:
    record = EvaluationResultRecord(**_values())
    assert validate_evaluation_result_record(record).passed
    mapping = _values(result_kind="scalar_score_result", artifact_id="brier_score", method_role="candidate", prediction_representation="binary_outcome_probability", support_status="supported", exclusion_block_reason_summary=[], provenance=["source-1"])
    original = {key: value.copy() if type(value) is list else value for key, value in mapping.items()}
    adapted, result = evaluation_result_record_from_mapping(mapping)
    assert result.passed and adapted == record
    assert mapping == original


@pytest.mark.parametrize("root", [None, 1, [], object()])
def test_non_mapping_is_fail_closed(root: object) -> None:
    record, result = evaluation_result_record_from_mapping(root)
    assert record is None
    assert result.codes == (EvaluationResultValidationCode.MISSING_REQUIRED_FIELD,) * 32


class _DuplicateMapping(Mapping):
    def __getitem__(self, key: object) -> object:
        return "unused"

    def __iter__(self):
        return iter(())

    def __len__(self) -> int:
        return 2

    def items(self):
        return [("evaluation_result_id", "one"), ("evaluation_result_id", "two")]


class _BaseExceptionMapping(_DuplicateMapping):
    def items(self):
        raise KeyboardInterrupt


def test_duplicate_snapshot_is_unreadable_and_baseexception_propagates() -> None:
    assert evaluation_result_record_from_mapping(_DuplicateMapping())[1].codes == (
        EvaluationResultValidationCode.MISSING_REQUIRED_FIELD,
    ) * 32
    with pytest.raises(KeyboardInterrupt):
        evaluation_result_record_from_mapping(_BaseExceptionMapping())


def test_complete_group_order_and_repeated_codes() -> None:
    changes = _values(
        evaluation_result_id=" ", result_kind="bad", artifact_id="bad", method_role="bad",
        prediction_representation="bad", support_status="bad", target_posture=" ",
        eligible_record_count=-1, excluded_record_count=-1, blocked_record_count=-1,
        total_considered_record_count=-1, exclusion_block_reason_summary=("",),
        uncertainty_method_id="method", uncertainty_level_id=None, provenance=("", 1),
        result_created_at=" ", supersedes_result_id_when_applicable=" ",
    )
    _, result = evaluation_result_record_from_mapping(changes)
    assert result.codes == (
        EvaluationResultValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationResultValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationResultValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationResultValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationResultValidationCode.INVALID_RESULT_KIND,
        EvaluationResultValidationCode.INVALID_ARTIFACT,
        EvaluationResultValidationCode.INVALID_METHOD_ROLE,
        EvaluationResultValidationCode.INVALID_PREDICTION_REPRESENTATION,
        EvaluationResultValidationCode.INVALID_SUPPORT_STATUS,
        EvaluationResultValidationCode.INVALID_FIXED_POSTURE,
        EvaluationResultValidationCode.INVALID_RECORD_COUNT,
        EvaluationResultValidationCode.INVALID_RECORD_COUNT,
        EvaluationResultValidationCode.INVALID_RECORD_COUNT,
        EvaluationResultValidationCode.INVALID_RECORD_COUNT,
        EvaluationResultValidationCode.INVALID_REASON_SUMMARY,
        EvaluationResultValidationCode.UNCERTAINTY_FIELDS_MISMATCH,
        EvaluationResultValidationCode.INVALID_PROVENANCE_REF,
        EvaluationResultValidationCode.INVALID_PROVENANCE_REF,
        EvaluationResultValidationCode.INVALID_RESULT_CREATED_AT,
    )


@pytest.mark.parametrize("timestamp", ["2026-01-01T00:00:00Z", "2026-01-01T00:00:00+05:30", "2026-01-01T00:00:00-04:00"])
def test_timestamp_acceptance(timestamp: str) -> None:
    assert _codes(result_created_at=timestamp) == ()


@pytest.mark.parametrize("timestamp", ["2026-01-01", "2026-01-01T00:00:00", "2026-01-01 00:00:00Z", "", 1])
def test_timestamp_rejection(timestamp: object) -> None:
    expected = (EvaluationResultValidationCode.INVALID_RESULT_CREATED_AT,)
    if not (type(timestamp) is str and timestamp.strip()):
        expected = (EvaluationResultValidationCode.BLANK_REQUIRED_TEXT,) + expected
    assert _codes(result_created_at=timestamp) == expected


def test_counts_reasons_uncertainty_and_provenance() -> None:
    assert _codes(eligible_record_count=True) == (EvaluationResultValidationCode.INVALID_RECORD_COUNT,)
    assert _codes(total_considered_record_count=3) == (EvaluationResultValidationCode.SAMPLE_ACCOUNTING_MISMATCH,)
    assert _codes(excluded_record_count=1, total_considered_record_count=3) == (EvaluationResultValidationCode.MISSING_REQUIRED_REASON,)
    assert _codes(support_status=EvaluationResultSupportStatus.BLOCKED) == (EvaluationResultValidationCode.MISSING_REQUIRED_REASON,)
    assert _codes(exclusion_block_reason_summary=("same", "same")) == (EvaluationResultValidationCode.INVALID_REASON_SUMMARY,)
    assert _codes(uncertainty_method_id="bootstrap") == (EvaluationResultValidationCode.UNCERTAINTY_FIELDS_MISMATCH,)
    assert _codes(provenance=()) == (EvaluationResultValidationCode.EMPTY_PROVENANCE,)
    assert _codes(provenance=("", "ok", 1)) == (
        EvaluationResultValidationCode.INVALID_PROVENANCE_REF,
        EvaluationResultValidationCode.INVALID_PROVENANCE_REF,
    )


def test_compatibility_and_payload_boundaries() -> None:
    assert _codes(artifact_id=ScoringArtifact.LOG_SCORE) == ()
    assert _codes(artifact_id=ScoringArtifact.PIT_HISTOGRAM) == (
        EvaluationResultValidationCode.RESULT_KIND_ARTIFACT_MISMATCH,
        EvaluationResultValidationCode.REPRESENTATION_MISMATCH,
    )
    assert _codes(method_role=EvaluationResultMethodRole.PAIRED_COMPARISON) == (EvaluationResultValidationCode.METHOD_ROLE_MISMATCH,)
    assert _codes(result_payload=object()) == (EvaluationResultValidationCode.INVALID_PAYLOAD_TYPE,)
    assert _codes(result_payload=ScalarScoreResultPayload(float("nan"), "lower_is_better", "artifact_specific_domain_validated")) == (EvaluationResultValidationCode.INVALID_SCALAR_SCORE_PAYLOAD,)


def test_every_payload_kind_has_a_valid_boundary() -> None:
    cases = (
        (EvaluationResultKind.CALIBRATION_BIN_RESULT, ScoringArtifact.RELIABILITY_DIAGRAM, ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, CalibrationBinResultPayload("bin", 0, "policy", 2, 0.2, 0.5, "predeclared_order_required")),
        (EvaluationResultKind.DECOMPOSITION_RESULT, ScoringArtifact.BRIER_DECOMPOSITION, ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, DecompositionResultPayload("policy", 0.1, 0.2, 0.3, "reliability_resolution_uncertainty_required")),
        (EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT, ScoringArtifact.PIT_HISTOGRAM, ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, DistributionDiagnosticResultPayload("policy", ("a", "b"), (1, 1), "predeclared_order_required")),
        (EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT, ScoringArtifact.RANK_HISTOGRAM, ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE, EnsembleDiagnosticResultPayload("policy", ("a", "b"), (1, 1), "finite_comparable_ensemble_required", "predeclared_order_required")),
        (EvaluationResultKind.PAIRED_COMPARISON_RESULT, ScoringArtifact.BRIER_SCORE, ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, PairedComparisonResultPayload("candidate", "baseline", BaselineType.CLIMATOLOGY, "candidate_minus_baseline_lower_is_better", -0.1, "exact_common_test_record_set_required")),
    )
    for kind, artifact, representation, payload in cases:
        role = EvaluationResultMethodRole.PAIRED_COMPARISON if kind is EvaluationResultKind.PAIRED_COMPARISON_RESULT else EvaluationResultMethodRole.CANDIDATE
        assert _codes(result_kind=kind, artifact_id=artifact, prediction_representation=representation, method_role=role, result_payload=payload) == ()


def test_pair_and_supersession_identity_codes() -> None:
    payload = PairedComparisonResultPayload("same", "same", "climatology", "candidate_minus_baseline_lower_is_better", 0.0, "exact_common_test_record_set_required")  # type: ignore[arg-type]
    assert _codes(result_kind=EvaluationResultKind.PAIRED_COMPARISON_RESULT, method_role=EvaluationResultMethodRole.PAIRED_COMPARISON, result_payload=payload) == (
        EvaluationResultValidationCode.PAIR_BASELINE_NOT_APPROVED,
        EvaluationResultValidationCode.PAIR_RESULT_IDENTITY_COLLISION,
    )
    assert _codes(supersedes_result_id_when_applicable="result-1") == (EvaluationResultValidationCode.SELF_SUPERSESSION,)
