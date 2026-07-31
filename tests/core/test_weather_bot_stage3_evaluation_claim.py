from __future__ import annotations

import dataclasses
import inspect

import pytest

from meg.weather.stage3.baseline_contracts import BaselineType
from meg.weather.stage3.evaluation_claim import (
    EvaluationClaimClass,
    EvaluationClaimDisposition,
    EvaluationClaimRecord,
    EvaluationClaimValidationCode,
    EvaluationClaimValidationResult,
    EvaluationClaimValidationSeverity,
    evaluation_claim_record_from_mapping,
    validate_evaluation_claim_record,
)
from meg.weather.stage3.scoring_and_diagnostics import ScoringPredictionRepresentation


PUBLIC = (
    "EvaluationClaimClass", "EvaluationClaimDisposition",
    "EvaluationClaimValidationSeverity", "EvaluationClaimValidationCode",
    "EvaluationClaimRecord", "EvaluationClaimValidationResult",
    "evaluation_claim_record_from_mapping", "validate_evaluation_claim_record",
)
FIELDS = (
    "evaluation_claim_id", "claim_class", "claim_rule_id", "claim_rule_version",
    "claim_disposition", "claim_disposition_reason", "target_posture",
    "candidate_method_id", "candidate_method_version", "baseline_type_when_applicable",
    "baseline_method_id_when_applicable", "baseline_method_version_when_applicable",
    "prediction_representation", "metric_or_diagnostic_ids",
    "metric_or_diagnostic_versions", "required_evaluation_result_ids",
    "observed_evaluation_result_ids", "missing_evaluation_result_ids", "split_id",
    "split_version", "fold_scope", "cutoff_scope", "paired_test_record_set_id",
    "aggregation_rule_id", "weighting_rule_id", "stratum_id_when_applicable",
    "uncertainty_policy_id", "sample_support_rule_id", "selection_control_policy_id",
    "multiple_comparison_policy_id_when_applicable", "evidence_gate_eligibility_posture",
    "provenance", "claim_created_at", "supersedes_claim_id_when_applicable",
)


def _mapping() -> dict[str, object]:
    return {
        "evaluation_claim_id": "claim-1",
        "claim_class": EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR,
        "claim_rule_id": "rule", "claim_rule_version": "v1",
        "claim_disposition": EvaluationClaimDisposition.CLAIM_UNAVAILABLE,
        "claim_disposition_reason": "result unavailable",
        "target_posture": "venue_defined_settlement_outcome",
        "candidate_method_id": "candidate", "candidate_method_version": "v1",
        "baseline_type_when_applicable": None,
        "baseline_method_id_when_applicable": None,
        "baseline_method_version_when_applicable": None,
        "prediction_representation": ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE,
        "metric_or_diagnostic_ids": ("rank_histogram",),
        "metric_or_diagnostic_versions": ("v1",),
        "required_evaluation_result_ids": ("result-1",),
        "observed_evaluation_result_ids": (),
        "missing_evaluation_result_ids": ("result-1",),
        "split_id": "split", "split_version": "v1", "fold_scope": "fold-1",
        "cutoff_scope": "2025-01-01T00:00:00Z", "paired_test_record_set_id": "test-set",
        "aggregation_rule_id": "aggregate", "weighting_rule_id": "weight",
        "stratum_id_when_applicable": None, "uncertainty_policy_id": "uncertainty",
        "sample_support_rule_id": "support", "selection_control_policy_id": "selection",
        "multiple_comparison_policy_id_when_applicable": None,
        "evidence_gate_eligibility_posture": "no_substitution_or_evidence_gate_use",
        "provenance": ("source:fixture",), "claim_created_at": "2025-01-01T00:00:00Z",
    }


def test_public_surface_enums_and_frozen_records_are_exact() -> None:
    import meg.weather.stage3.evaluation_claim as module

    assert module.__all__ == PUBLIC
    assert tuple(member.value for member in EvaluationClaimClass) == (
        "candidate_vs_climatology_predictive_skill", "candidate_vs_persistence_predictive_skill",
        "candidate_predictive_skill_across_required_baselines", "binary_calibration_behavior",
        "distributional_calibration_behavior", "ensemble_calibration_behavior",
        "threshold_weighted_distribution_skill", "stratum_specific_predictive_skill",
    )
    assert tuple(member.value for member in EvaluationClaimDisposition) == (
        "claim_supported", "claim_not_supported", "claim_insufficient", "claim_blocked", "claim_unavailable",
    )
    assert len(EvaluationClaimValidationCode) == 38
    assert tuple(field.name for field in dataclasses.fields(EvaluationClaimRecord)) == FIELDS
    assert EvaluationClaimRecord.__dataclass_params__.frozen
    assert EvaluationClaimValidationResult.__dataclass_params__.frozen


def test_signatures_are_frozen() -> None:
    assert tuple(inspect.signature(evaluation_claim_record_from_mapping).parameters) == ("mapping", "result_records")
    assert tuple(inspect.signature(validate_evaluation_claim_record).parameters) == ("record", "result_records")


def test_validation_result_invariant_preserves_repetition() -> None:
    passed = EvaluationClaimValidationResult(EvaluationClaimValidationSeverity.BLOCKED, False)
    assert (passed.severity, passed.passed, passed.codes) == (EvaluationClaimValidationSeverity.PASSED, True, ())
    repeated = (EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,) * 2
    blocked = EvaluationClaimValidationResult(EvaluationClaimValidationSeverity.PASSED, True, repeated)
    assert (blocked.severity, blocked.passed, blocked.codes) == (EvaluationClaimValidationSeverity.BLOCKED, False, repeated)


@pytest.mark.parametrize("root", [None, (), [], "mapping"])
def test_unreadable_roots_fail_with_exact_missing_sequence(root: object) -> None:
    record, result = evaluation_claim_record_from_mapping(root, ())
    assert record is None
    assert result.codes == (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,) * 33


def test_mapping_adapts_only_approved_values_without_mutation() -> None:
    values = _mapping()
    values["claim_class"] = "ensemble_calibration_behavior"
    values["claim_disposition"] = "claim_unavailable"
    values["prediction_representation"] = "finite_comparable_ensemble"
    values["metric_or_diagnostic_ids"] = ["rank_histogram"]
    original = list(values["metric_or_diagnostic_ids"])
    record, result = evaluation_claim_record_from_mapping(values, [])
    assert result.codes == ()
    assert record is not None
    assert record.claim_class is EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR
    assert record.metric_or_diagnostic_ids == ("rank_histogram",)
    assert values["metric_or_diagnostic_ids"] == original


def test_mapping_shape_codes_precede_value_codes() -> None:
    values = _mapping()
    del values["evaluation_claim_id"]
    values["zzz"] = 1
    values[1] = "unexpected"
    values["claim_rule_id"] = " "
    record, result = evaluation_claim_record_from_mapping(values, ())
    assert record is None
    assert result.codes == (
        EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,
        EvaluationClaimValidationCode.UNEXPECTED_FIELD,
        EvaluationClaimValidationCode.UNEXPECTED_FIELD,
        EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
    )


def test_direct_validation_is_pure_and_reports_timestamp_provenance_and_supersession() -> None:
    values = _mapping()
    values["claim_created_at"] = " "
    values["provenance"] = ("", "valid", "")
    values["supersedes_claim_id_when_applicable"] = "claim-1"
    record = EvaluationClaimRecord(**values)
    result = validate_evaluation_claim_record(record, ())
    assert result.codes == (
        EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationClaimValidationCode.INVALID_PROVENANCE_REF,
        EvaluationClaimValidationCode.INVALID_PROVENANCE_REF,
        EvaluationClaimValidationCode.INVALID_CLAIM_CREATED_AT,
        EvaluationClaimValidationCode.SELF_SUPERSESSION,
    )
    assert record.claim_created_at == " "


def test_direct_validation_rejects_tuple_subclasses_and_is_deterministic() -> None:
    class TupleSubclass(tuple):
        pass

    record = EvaluationClaimRecord(**_mapping())
    first = validate_evaluation_claim_record(record, TupleSubclass())
    second = validate_evaluation_claim_record(record, TupleSubclass())
    assert first == second
    assert first.codes == (EvaluationClaimValidationCode.INVALID_RESULT_RECORD_CONTAINER,)


def test_frozen_claim_cannot_be_mutated() -> None:
    record = EvaluationClaimRecord(**_mapping())
    with pytest.raises(dataclasses.FrozenInstanceError):
        record.evaluation_claim_id = "changed"  # type: ignore[misc]
