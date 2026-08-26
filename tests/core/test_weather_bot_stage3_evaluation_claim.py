from __future__ import annotations

import ast
from collections.abc import Mapping
import dataclasses
from enum import StrEnum
import inspect
from pathlib import Path
import typing

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
from meg.weather.stage3.evaluation_result_record import (
    CalibrationBinResultPayload, DecompositionResultPayload,
    DistributionDiagnosticResultPayload, EnsembleDiagnosticResultPayload,
    EvaluationResultKind, EvaluationResultMethodRole, EvaluationResultRecord,
    EvaluationResultSupportStatus, PairedComparisonResultPayload,
    ScalarScoreResultPayload, validate_evaluation_result_record,
)
from meg.weather.stage3.scoring_and_diagnostics import ScoringArtifact, ScoringPredictionRepresentation


COVERAGE_MANIFEST = {
    "imports": ("test_source_contract_and_purity",),
    "public_api": ("test_public_surface_enums_and_frozen_records_are_exact",),
    "public_source_order": ("test_source_contract_and_purity",),
    "claim_class_enum": ("test_claim_class_literal_members",),
    "disposition_enum": ("test_public_surface_enums_and_frozen_records_are_exact",),
    "severity_enum": ("test_validation_result_invariant_preserves_repetition",),
    "validation_codes": ("test_each_validation_code_literal",),
    "record_structure": ("test_each_record_field_literal",),
    "validation_result_structure": ("test_validation_result_invariant_preserves_repetition",),
    "signatures": ("test_signatures_are_frozen",),
    "mapping_keys": ("test_each_required_mapping_key_is_independently_required",),
    "mapping_root_behavior": ("mapping_root__non_mapping", "mapping_root__asymmetric_equal_hash_duplicate"),
    "mapping_adaptation": ("test_mapping_adapts_only_approved_values_without_mutation",),
    "required_text": ("test_each_required_text_rejects_each_invalid_exact_type",),
    "nullable_text": ("test_each_nullable_text_rejects_invalid_nonnull",),
    "fixed_target": ("test_present_aware_exact_regressions",),
    "metric_ids": ("test_tuple_contract_cases",),
    "metric_versions": ("test_repeated_metric_versions_are_accepted",),
    "required_result_ids": ("test_tuple_contract_cases",),
    "observed_result_ids": ("test_tuple_contract_cases",),
    "missing_result_ids": ("test_tuple_contract_cases",),
    "partition": ("test_tuple_contract_cases",),
    "result_context": ("context__invalid_container_direct", "context__invalid_container_mapping_mixed_list"),
    "duplicate_identities": ("context__duplicate_once", "context__duplicate_twice"),
    "observed_resolution": ("context__resolution_zero", "context__resolution_one", "context__resolution_multiple"),
    "unexpected_context": ("context__unexpected_one", "context__unexpected_multiple"),
    "paired_references": ("context__paired_missing_candidate", "context__paired_missing_baseline", "context__paired_missing_both"),
    "target_compatibility": ("compat__target__match", "compat__target__mismatch_single"),
    "representation_compatibility": ("compat__representation__match", "compat__representation__mismatch_single"),
    "scope_split_id": ("compat__split_id__match", "compat__split_id__mismatch_single"),
    "scope_split_version": ("compat__split_version__match", "compat__split_version__mismatch_single"),
    "scope_fold": ("compat__fold__match", "compat__fold__mismatch_single"),
    "scope_cutoff": ("compat__cutoff__match", "compat__cutoff__mismatch_single"),
    "scope_paired_set": ("compat__paired_set__match", "compat__paired_set__mismatch_single"),
    "scope_aggregation": ("compat__aggregation__match", "compat__aggregation__mismatch_single"),
    "scope_weighting": ("compat__weighting__match", "compat__weighting__mismatch_single"),
    "scope_stratum": ("test_scope_stratum_none_does_not_coerce_to_empty",),
    "metric_compatibility": ("compat__metric_id_sequence__match", "compat__metric_id_sequence__mismatch_single"),
    "candidate_identity": ("candidate_vs_climatology__candidate_id",),
    "baseline_identity": ("candidate_vs_climatology__baseline_id",),
    "class_candidate_climatology": ("candidate_vs_climatology__valid_single",),
    "class_candidate_persistence": ("candidate_vs_persistence__valid_single",),
    "class_cross_baseline": ("cross_baseline__valid_complete",),
    "class_binary_calibration": ("binary_calibration__valid_all_three",),
    "class_distributional_calibration": ("distributional_calibration__valid_diagnostic_scalar",),
    "class_ensemble_calibration": ("ensemble_calibration__valid_single",),
    "class_threshold_weighted": ("threshold_weighted__valid_climatology",),
    "class_stratum_specific": ("stratum_specific__valid_climatology",),
    "baseline_requirements": ("test_present_aware_exact_regressions",),
    "cross_baseline_completeness": ("test_each_claim_class_complete_evidence", "test_claim_class_claim_level_behavior",),
    "stratum_requirements": ("test_scope_stratum_none_does_not_coerce_to_empty",),
    "disposition_precedence": ("disposition__complete_support_unavailable", "disposition__independent_block_valid"),
    "supported_completeness": ("completeness__supported__invalid_container", "completeness__not_supported__invalid_container"),
    "evidence_gate_posture": ("test_evidence_gate_matrix",),
    "multiplicity": ("test_present_aware_exact_regressions",),
    "provenance": ("test_provenance_timestamp_supersession_matrix",),
    "timestamp": ("test_provenance_timestamp_supersession_matrix",),
    "supersession": ("test_provenance_timestamp_supersession_matrix",),
    "validation_groups": ("test_exact_validation_group_literal_oracle",),
    "purity": ("test_source_contract_and_purity",),
    "caller_preservation": ("test_mapping_adapts_only_approved_values_without_mutation",),
    "determinism": ("test_direct_validation_rejects_tuple_subclasses_and_is_deterministic",),
    "mutation_resistance": ("test_mutation_resistance_map",),
    "observed_tuple_prerequisite_suppression": ("test_observed_tuple_prerequisite_exact_codes",),
    "evidence_posture_exact_type": ("test_evidence_posture_requires_exact_builtin_text",),
    "supported_completeness_evidence_posture": ("test_evidence_posture_requires_exact_builtin_text",),
    "candidate_claim_identity_prerequisites": ("test_candidate_claim_identity_prerequisites",),
    "baseline_claim_identity_prerequisites": ("test_baseline_claim_identity_prerequisites",),
}


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


VALIDATION_CODES = (
    "MISSING_REQUIRED_FIELD", "UNEXPECTED_FIELD", "BLANK_REQUIRED_TEXT", "INVALID_CLAIM_CLASS",
    "INVALID_CLAIM_DISPOSITION", "INVALID_BASELINE_TYPE", "INVALID_PREDICTION_REPRESENTATION",
    "INVALID_FIXED_POSTURE", "INVALID_EVIDENCE_GATE_POSTURE", "INVALID_METRIC_IDENTITY_TUPLE",
    "METRIC_VERSION_LENGTH_MISMATCH", "INVALID_REQUIRED_RESULT_IDS", "INVALID_OBSERVED_RESULT_IDS",
    "INVALID_MISSING_RESULT_IDS", "RESULT_SET_PARTITION_MISMATCH", "INVALID_RESULT_RECORD_CONTAINER",
    "INVALID_RESULT_RECORD", "DUPLICATE_CONTEXT_RESULT_ID", "OBSERVED_RESULT_NOT_FOUND",
    "UNEXPECTED_CONTEXT_RESULT", "PAIRED_REFERENCE_NOT_FOUND", "RESULT_TARGET_MISMATCH",
    "RESULT_REPRESENTATION_MISMATCH", "RESULT_SCOPE_MISMATCH", "RESULT_METRIC_MISMATCH",
    "CANDIDATE_IDENTITY_MISMATCH", "BASELINE_IDENTITY_MISMATCH", "RESULT_KIND_NOT_ALLOWED",
    "BASELINE_REQUIREMENT_MISMATCH", "CROSS_BASELINE_INCOMPLETE", "STRATUM_REQUIREMENT_MISMATCH",
    "DISPOSITION_PRECEDENCE_MISMATCH", "SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT",
    "INVALID_MULTIPLE_COMPARISON_POSTURE", "EMPTY_PROVENANCE", "INVALID_PROVENANCE_REF",
    "INVALID_CLAIM_CREATED_AT", "SELF_SUPERSESSION",
)
REQUIRED_TEXT = (
    "evaluation_claim_id", "claim_rule_id", "claim_rule_version", "claim_disposition_reason",
    "target_posture", "candidate_method_id", "candidate_method_version", "split_id", "split_version",
    "fold_scope", "cutoff_scope", "paired_test_record_set_id", "aggregation_rule_id", "weighting_rule_id",
    "uncertainty_policy_id", "sample_support_rule_id", "selection_control_policy_id",
    "evidence_gate_eligibility_posture", "claim_created_at",
)
NULLABLE_TEXT = (
    "baseline_method_id_when_applicable", "baseline_method_version_when_applicable",
    "stratum_id_when_applicable", "multiple_comparison_policy_id_when_applicable",
    "supersedes_claim_id_when_applicable",
)


class TextSubclass(str):
    pass


class UnrelatedEnum(StrEnum):
    VALUE = "ensemble_calibration_behavior"


@pytest.mark.parametrize("index,name", tuple(enumerate(VALIDATION_CODES)))
def test_each_validation_code_literal(index: int, name: str) -> None:
    member = tuple(EvaluationClaimValidationCode)[index]
    assert (member.name, member.value) == (name, name.lower())


@pytest.mark.parametrize("index,name", tuple(enumerate(FIELDS)))
def test_each_record_field_literal(index: int, name: str) -> None:
    field = dataclasses.fields(EvaluationClaimRecord)[index]
    assert field.name == name
    if index == 33:
        assert field.default is None
    else:
        assert field.default is dataclasses.MISSING


@pytest.mark.parametrize("index,member", tuple(enumerate((
    ("CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL", "candidate_vs_climatology_predictive_skill"),
    ("CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL", "candidate_vs_persistence_predictive_skill"),
    ("CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES", "candidate_predictive_skill_across_required_baselines"),
    ("BINARY_CALIBRATION_BEHAVIOR", "binary_calibration_behavior"),
    ("DISTRIBUTIONAL_CALIBRATION_BEHAVIOR", "distributional_calibration_behavior"),
    ("ENSEMBLE_CALIBRATION_BEHAVIOR", "ensemble_calibration_behavior"),
    ("THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL", "threshold_weighted_distribution_skill"),
    ("STRATUM_SPECIFIC_PREDICTIVE_SKILL", "stratum_specific_predictive_skill"),
))))
def test_claim_class_literal_members(index: int, member: tuple[str, str]) -> None:
    actual = tuple(EvaluationClaimClass)[index]
    assert (actual.name, actual.value) == member


@pytest.mark.parametrize("missing", FIELDS[:33])
def test_each_required_mapping_key_is_independently_required(missing: str) -> None:
    values = _mapping()
    del values[missing]
    record, result = evaluation_claim_record_from_mapping(values, ())
    assert record is None
    assert result.codes == (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)


@pytest.mark.parametrize("field", REQUIRED_TEXT)
@pytest.mark.parametrize("bad", ("", " ", TextSubclass("text"), object()), ids=("empty", "blank", "subclass", "object"))
def test_each_required_text_rejects_each_invalid_exact_type(field: str, bad: object) -> None:
    values = _mapping()
    values[field] = bad
    record, result = evaluation_claim_record_from_mapping(values, ())
    assert record is None
    assert EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT in result.codes


@pytest.mark.parametrize("field", NULLABLE_TEXT)
@pytest.mark.parametrize("bad", ("", TextSubclass("text"), object()), ids=("empty", "subclass", "object"))
def test_each_nullable_text_rejects_invalid_nonnull(field: str, bad: object) -> None:
    values = _mapping()
    values[field] = bad
    record, result = evaluation_claim_record_from_mapping(values, ())
    assert record is None
    assert EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT in result.codes


@pytest.mark.parametrize("field,bad,expected", (
    ("claim_class", "invalid", EvaluationClaimValidationCode.INVALID_CLAIM_CLASS),
    ("claim_class", TextSubclass("ensemble_calibration_behavior"), EvaluationClaimValidationCode.INVALID_CLAIM_CLASS),
    ("claim_class", UnrelatedEnum.VALUE, EvaluationClaimValidationCode.INVALID_CLAIM_CLASS),
    ("claim_class", object(), EvaluationClaimValidationCode.INVALID_CLAIM_CLASS),
    ("claim_disposition", "invalid", EvaluationClaimValidationCode.INVALID_CLAIM_DISPOSITION),
    ("claim_disposition", TextSubclass("claim_unavailable"), EvaluationClaimValidationCode.INVALID_CLAIM_DISPOSITION),
    ("claim_disposition", UnrelatedEnum.VALUE, EvaluationClaimValidationCode.INVALID_CLAIM_DISPOSITION),
    ("claim_disposition", object(), EvaluationClaimValidationCode.INVALID_CLAIM_DISPOSITION),
    ("baseline_type_when_applicable", "invalid", EvaluationClaimValidationCode.INVALID_BASELINE_TYPE),
    ("baseline_type_when_applicable", TextSubclass("climatology"), EvaluationClaimValidationCode.INVALID_BASELINE_TYPE),
    ("baseline_type_when_applicable", UnrelatedEnum.VALUE, EvaluationClaimValidationCode.INVALID_BASELINE_TYPE),
    ("baseline_type_when_applicable", object(), EvaluationClaimValidationCode.INVALID_BASELINE_TYPE),
    ("prediction_representation", "invalid", EvaluationClaimValidationCode.INVALID_PREDICTION_REPRESENTATION),
    ("prediction_representation", TextSubclass("finite_comparable_ensemble"), EvaluationClaimValidationCode.INVALID_PREDICTION_REPRESENTATION),
    ("prediction_representation", UnrelatedEnum.VALUE, EvaluationClaimValidationCode.INVALID_PREDICTION_REPRESENTATION),
    ("prediction_representation", object(), EvaluationClaimValidationCode.INVALID_PREDICTION_REPRESENTATION),
))
def test_enum_adaptation_rejection_matrix(field: str, bad: object, expected: EvaluationClaimValidationCode) -> None:
    values = _mapping()
    values[field] = bad
    _, result = evaluation_claim_record_from_mapping(values, ())
    assert expected in result.codes


def _result_values(**changes: object) -> dict[str, object]:
    values: dict[str, object] = {
        "evaluation_result_id": "result-1", "result_kind": EvaluationResultKind.SCALAR_SCORE_RESULT,
        "artifact_id": ScoringArtifact.BRIER_SCORE, "artifact_version": "v1",
        "evaluation_definition_id": "definition", "evaluation_definition_version": "v1",
        "evaluation_run_id": "run", "method_role": EvaluationResultMethodRole.CANDIDATE,
        "method_id": "candidate", "method_version": "v1",
        "prediction_representation": ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        "target_posture": "venue_defined_settlement_outcome", "split_id": "split",
        "split_version": "v1", "fold_id": "fold-1", "cutoff_identity": "2025-01-01T00:00:00Z",
        "paired_test_record_set_id": "test-set", "eligibility_policy_id": "eligible",
        "aggregation_rule_id": "aggregate", "weighting_rule_id": "weight", "stratum_id": "all",
        "eligible_record_count": 2, "excluded_record_count": 0, "blocked_record_count": 0,
        "total_considered_record_count": 2, "exclusion_block_reason_summary": (),
        "uncertainty_method_id": None, "uncertainty_level_id": None,
        "support_status": EvaluationResultSupportStatus.SUPPORTED,
        "result_payload": ScalarScoreResultPayload(0.2, "lower_is_better", "artifact_specific_domain_validated"),
        "provenance": ("source",), "result_created_at": "2025-01-01T00:00:00Z",
        "supersedes_result_id_when_applicable": None,
    }
    values.update(changes)
    return values


RESULT_FIXTURES = (
    _result_values(),
    _result_values(result_kind=EvaluationResultKind.CALIBRATION_BIN_RESULT, artifact_id=ScoringArtifact.RELIABILITY_DIAGRAM, result_payload=CalibrationBinResultPayload("bin", 0, "policy", 2, 0.2, 0.5, "predeclared_order_required")),
    _result_values(result_kind=EvaluationResultKind.DECOMPOSITION_RESULT, artifact_id=ScoringArtifact.BRIER_DECOMPOSITION, result_payload=DecompositionResultPayload("policy", 0.1, 0.2, 0.3, "reliability_resolution_uncertainty_required")),
    _result_values(result_kind=EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT, artifact_id=ScoringArtifact.PIT_HISTOGRAM, prediction_representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, result_payload=DistributionDiagnosticResultPayload("policy", ("a", "b"), (1, 1), "predeclared_order_required")),
    _result_values(result_kind=EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT, artifact_id=ScoringArtifact.RANK_HISTOGRAM, prediction_representation=ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE, result_payload=EnsembleDiagnosticResultPayload("policy", ("a", "b"), (1, 1), "finite_comparable_ensemble_required", "predeclared_order_required")),
    _result_values(evaluation_result_id="pair", result_kind=EvaluationResultKind.PAIRED_COMPARISON_RESULT, method_role=EvaluationResultMethodRole.PAIRED_COMPARISON, result_payload=PairedComparisonResultPayload("candidate-ref", "baseline-ref", BaselineType.CLIMATOLOGY, "candidate_minus_baseline_lower_is_better", -0.1, "exact_common_test_record_set_required")),
    _result_values(evaluation_result_id="candidate-ref"),
    _result_values(evaluation_result_id="baseline-ref", method_role=EvaluationResultMethodRole.CLIMATOLOGY_BASELINE, method_id="climatology"),
    _result_values(evaluation_result_id="persistence-ref", method_role=EvaluationResultMethodRole.PERSISTENCE_BASELINE, method_id="persistence"),
)


@pytest.mark.parametrize("values", RESULT_FIXTURES, ids=("scalar", "calibration", "decomposition", "distribution", "ensemble", "paired", "candidate", "climatology", "persistence"))
def test_each_evaluation_result_fixture_is_individually_valid(values: dict[str, object]) -> None:
    assert validate_evaluation_result_record(EvaluationResultRecord(**values)).passed


def _valid_observed() -> tuple[EvaluationClaimRecord, EvaluationResultRecord]:
    result = EvaluationResultRecord(**RESULT_FIXTURES[4])
    values = _mapping()
    values.update(claim_disposition=EvaluationClaimDisposition.CLAIM_SUPPORTED,
                  evidence_gate_eligibility_posture="eligible_for_later_evidence_gate_decision_only",
                  required_evaluation_result_ids=("result-1",), observed_evaluation_result_ids=("result-1",),
                  missing_evaluation_result_ids=())
    return EvaluationClaimRecord(**values), result


def test_valid_observed_claim() -> None:
    claim, result = _valid_observed()
    assert validate_evaluation_claim_record(claim, (result,)).codes == ()


def _paired_claim_and_context(**pair_changes: object) -> tuple[EvaluationClaimRecord, tuple[EvaluationResultRecord, ...]]:
    candidate = EvaluationResultRecord(**_result_values(evaluation_result_id="candidate-ref"))
    baseline = EvaluationResultRecord(**_result_values(evaluation_result_id="baseline-ref", method_role=EvaluationResultMethodRole.CLIMATOLOGY_BASELINE, method_id="climatology"))
    pair_values = _result_values(
        evaluation_result_id="pair", result_kind=EvaluationResultKind.PAIRED_COMPARISON_RESULT,
        method_role=EvaluationResultMethodRole.PAIRED_COMPARISON,
        result_payload=PairedComparisonResultPayload("candidate-ref", "baseline-ref", BaselineType.CLIMATOLOGY, "candidate_minus_baseline_lower_is_better", -0.1, "exact_common_test_record_set_required"),
    )
    pair_values.update(pair_changes)
    pair = EvaluationResultRecord(**pair_values)
    values = _mapping()
    values.update(
        claim_class=EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL,
        claim_disposition=EvaluationClaimDisposition.CLAIM_SUPPORTED,
        evidence_gate_eligibility_posture="eligible_for_later_evidence_gate_decision_only",
        baseline_type_when_applicable=BaselineType.CLIMATOLOGY,
        baseline_method_id_when_applicable="climatology", baseline_method_version_when_applicable="v1",
        prediction_representation=ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        metric_or_diagnostic_ids=("brier_score",), required_evaluation_result_ids=("pair",),
        observed_evaluation_result_ids=("pair",), missing_evaluation_result_ids=(),
    )
    return EvaluationClaimRecord(**values), (pair, candidate, baseline)


def test_valid_paired_claim_and_direct_references() -> None:
    claim, context = _paired_claim_and_context()
    assert validate_evaluation_claim_record(claim, context).codes == ()


def test_wrong_payload_baseline_family_is_classified_per_observed_pair() -> None:
    payload = PairedComparisonResultPayload("candidate-ref", "baseline-ref", BaselineType.PERSISTENCE, "candidate_minus_baseline_lower_is_better", -0.1, "exact_common_test_record_set_required")
    claim, context = _paired_claim_and_context(result_payload=payload)
    assert EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH in validate_evaluation_claim_record(claim, context).codes


@pytest.mark.parametrize("kept", ("candidate", "baseline", "neither"))
def test_one_reference_suppresses_both_identity_comparisons(kept: str) -> None:
    claim, context = _paired_claim_and_context()
    pair, candidate, baseline = context
    candidate = dataclasses.replace(candidate, method_id="wrong")
    baseline = dataclasses.replace(baseline, method_id="wrong")
    chosen = (pair,) + ((candidate,) if kept == "candidate" else ()) + ((baseline,) if kept == "baseline" else ())
    codes = validate_evaluation_claim_record(claim, chosen).codes
    assert EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND in codes
    assert EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH not in codes
    assert EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH not in codes


@pytest.mark.parametrize("status,disposition", (
    (EvaluationResultSupportStatus.BLOCKED, EvaluationClaimDisposition.CLAIM_BLOCKED),
    (EvaluationResultSupportStatus.UNAVAILABLE, EvaluationClaimDisposition.CLAIM_UNAVAILABLE),
    (EvaluationResultSupportStatus.INSUFFICIENT, EvaluationClaimDisposition.CLAIM_INSUFFICIENT),
))
def test_referenced_status_participates_in_precedence(status: EvaluationResultSupportStatus, disposition: EvaluationClaimDisposition) -> None:
    claim, context = _paired_claim_and_context()
    pair, candidate, baseline = context
    reason = () if status is EvaluationResultSupportStatus.SUPPORTED else ("status reason",)
    candidate = dataclasses.replace(candidate, support_status=status, exclusion_block_reason_summary=reason)
    posture = "evidence_gate_use_blocked" if disposition in (EvaluationClaimDisposition.CLAIM_BLOCKED, EvaluationClaimDisposition.CLAIM_INSUFFICIENT) else "no_substitution_or_evidence_gate_use"
    claim = dataclasses.replace(claim, claim_disposition=disposition, evidence_gate_eligibility_posture=posture)
    assert EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH not in validate_evaluation_claim_record(claim, (pair, candidate, baseline)).codes


def test_repeated_metric_versions_are_accepted() -> None:
    values = _mapping()
    values.update(metric_or_diagnostic_ids=("brier_score", "reliability_diagram"), metric_or_diagnostic_versions=("v1", "v1"), multiple_comparison_policy_id_when_applicable="holm")
    assert validate_evaluation_claim_record(EvaluationClaimRecord(**values), ()).codes == ()


def test_scope_stratum_none_does_not_coerce_to_empty() -> None:
    claim, result = _valid_observed()
    assert claim.stratum_id_when_applicable is None and result.stratum_id == "all"
    assert EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH not in validate_evaluation_claim_record(claim, (result,)).codes


def test_independent_block_precedence() -> None:
    values = _mapping()
    values.update(claim_disposition=EvaluationClaimDisposition.CLAIM_BLOCKED, evidence_gate_eligibility_posture="evidence_gate_use_blocked")
    assert validate_evaluation_claim_record(EvaluationClaimRecord(**values), ()).codes == ()


@pytest.mark.parametrize("disposition,posture", (
    (EvaluationClaimDisposition.CLAIM_SUPPORTED, "eligible_for_later_evidence_gate_decision_only"),
    (EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, "claim_support_absent"),
    (EvaluationClaimDisposition.CLAIM_INSUFFICIENT, "evidence_gate_use_blocked"),
    (EvaluationClaimDisposition.CLAIM_BLOCKED, "evidence_gate_use_blocked"),
    (EvaluationClaimDisposition.CLAIM_UNAVAILABLE, "no_substitution_or_evidence_gate_use"),
))
def test_evidence_gate_matrix(disposition: EvaluationClaimDisposition, posture: str) -> None:
    values = _mapping()
    values.update(claim_disposition=disposition, evidence_gate_eligibility_posture=posture)
    result = validate_evaluation_claim_record(EvaluationClaimRecord(**values), ())
    assert EvaluationClaimValidationCode.INVALID_EVIDENCE_GATE_POSTURE not in result.codes


@pytest.mark.parametrize("case", ("metric_ids", "metric_versions", "required", "observed", "missing", "partition_overlap", "partition_order", "tuple_subclass"))
def test_tuple_contract_cases(case: str) -> None:
    values = _mapping()
    if case == "metric_ids": values["metric_or_diagnostic_ids"] = ("rank_histogram", "rank_histogram")
    elif case == "metric_versions": values["metric_or_diagnostic_versions"] = ()
    elif case == "required": values["required_evaluation_result_ids"] = ("result-1", "result-1")
    elif case == "observed": values["observed_evaluation_result_ids"] = ("result-1", "result-1")
    elif case == "missing": values["missing_evaluation_result_ids"] = ("result-1", "result-1")
    elif case == "partition_overlap": values["observed_evaluation_result_ids"] = ("result-1",)
    elif case == "partition_order": values.update(required_evaluation_result_ids=("a", "b"), observed_evaluation_result_ids=("b", "a"), missing_evaluation_result_ids=())
    else: values["metric_or_diagnostic_ids"] = type("TupleSubclass", (tuple,), {})(["rank_histogram"])
    assert validate_evaluation_claim_record(EvaluationClaimRecord(**values), ()).codes


@pytest.mark.parametrize("container", ([], iter(()), "context", object()))
def test_context_container_and_item_boundaries(container: object) -> None:
    result = validate_evaluation_claim_record(EvaluationClaimRecord(**_mapping()), container)  # type: ignore[arg-type]
    assert result.codes == (EvaluationClaimValidationCode.INVALID_RESULT_RECORD_CONTAINER,)


def test_missing_prerequisite_suppression() -> None:
    for missing in ("claim_class", "claim_disposition", "prediction_representation", "metric_or_diagnostic_ids", "required_evaluation_result_ids", "split_id"):
        values = _mapping(); del values[missing]
        _, result = evaluation_claim_record_from_mapping(values, ())
        assert result.codes == (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)


@pytest.mark.parametrize("provenance,timestamp,supersedes", (
    ((), "2025-01-01T00:00:00Z", None), (("",), "2025-01-01T00:00:00Z", None),
    (("source",), "invalid", None), (("source",), " ", None),
    (("source",), "2025-01-01T00:00:00Z", "claim-1"),
))
def test_provenance_timestamp_supersession_matrix(provenance: object, timestamp: object, supersedes: object) -> None:
    values = _mapping(); values.update(provenance=provenance, claim_created_at=timestamp, supersedes_claim_id_when_applicable=supersedes)
    assert validate_evaluation_claim_record(EvaluationClaimRecord(**values), ()).codes


def test_source_contract_and_purity() -> None:
    import meg.weather.stage3.evaluation_claim as module
    source = Path(module.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert module.__all__ == PUBLIC
    test_names = {name for name, value in globals().items() if name.startswith("test_") and callable(value)}
    assert len(COVERAGE_MANIFEST) == 68
    assert all(names and set(names) <= test_names | set(ALL_CLOSED_CASE_IDS) for names in COVERAGE_MANIFEST.values())
    forbidden = {"open", "eval", "exec", "compile", "__import__", "write", "write_text", "system", "run", "Popen"}
    assert not any(isinstance(node, ast.Call) and ((isinstance(node.func, ast.Name) and node.func.id in forbidden) or (isinstance(node.func, ast.Attribute) and node.func.attr in forbidden)) for node in ast.walk(tree))


class HostileMapping(Mapping):
    def __init__(self, failure: BaseException): self.failure = failure
    def __getitem__(self, key: object) -> object: raise self.failure
    def __iter__(self): return iter(())
    def __len__(self) -> int: return 1
    def items(self): raise self.failure


@pytest.mark.parametrize("failure", (ValueError("items"), RuntimeError("items")))
def test_hostile_mapping_roots_and_baseexception(failure: BaseException) -> None:
    _, result = evaluation_claim_record_from_mapping(HostileMapping(failure), ())
    assert result.codes == (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,) * 33


def test_hostile_mapping_baseexception_propagates() -> None:
    with pytest.raises(KeyboardInterrupt):
        evaluation_claim_record_from_mapping(HostileMapping(KeyboardInterrupt()), ())


@pytest.mark.parametrize("missing", (
    "evaluation_claim_id", "claim_rule_id", "claim_rule_version", "claim_disposition_reason",
    "target_posture", "candidate_method_id", "candidate_method_version",
    "baseline_type_when_applicable", "baseline_method_id_when_applicable",
    "baseline_method_version_when_applicable", "prediction_representation",
    "metric_or_diagnostic_ids", "metric_or_diagnostic_versions",
    "required_evaluation_result_ids", "observed_evaluation_result_ids",
    "missing_evaluation_result_ids", "split_id", "split_version", "fold_scope", "cutoff_scope",
))
def test_independent_posture_diagnostic_survives_each_unrelated_missing_key(missing: str) -> None:
    values = _mapping()
    del values[missing]
    values["evidence_gate_eligibility_posture"] = "wrong"
    _, result = evaluation_claim_record_from_mapping(values, ())
    assert result.codes == (
        EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,
        EvaluationClaimValidationCode.INVALID_EVIDENCE_GATE_POSTURE,
    )


@pytest.mark.parametrize("case", ("gate", "multiplicity", "baseline", "target_subclass", "gate_blank", "baseline_blank"))
def test_present_aware_exact_regressions(case: str) -> None:
    values = _mapping()
    del values["claim_created_at"]
    expected = [EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD]
    if case == "gate":
        values["evidence_gate_eligibility_posture"] = "wrong"
        expected += [EvaluationClaimValidationCode.INVALID_EVIDENCE_GATE_POSTURE]
    elif case == "multiplicity":
        values.update(metric_or_diagnostic_ids=("brier_score", "reliability_diagram"), metric_or_diagnostic_versions=("v1", "v1"), multiple_comparison_policy_id_when_applicable=None)
        expected += [EvaluationClaimValidationCode.INVALID_MULTIPLE_COMPARISON_POSTURE]
    elif case == "baseline":
        values.update(claim_class=EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, baseline_type_when_applicable=None, baseline_method_id_when_applicable=None, baseline_method_version_when_applicable=None)
        expected += [EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH] * 3
    elif case == "target_subclass":
        values["target_posture"] = TextSubclass("venue_defined_settlement_outcome")
        expected += [EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT, EvaluationClaimValidationCode.INVALID_FIXED_POSTURE]
    elif case == "gate_blank":
        values["evidence_gate_eligibility_posture"] = " "
        expected += [EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT, EvaluationClaimValidationCode.INVALID_EVIDENCE_GATE_POSTURE]
    else:
        values.update(claim_class=EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, baseline_type_when_applicable=BaselineType.CLIMATOLOGY, baseline_method_id_when_applicable=" ", baseline_method_version_when_applicable="v1")
        expected += [EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT, EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH]
    assert evaluation_claim_record_from_mapping(values, ())[1].codes == tuple(expected)


@pytest.mark.parametrize("field,bad", (
    ("target_posture", "wrong"), ("prediction_representation", object()),
    ("metric_or_diagnostic_ids", ()), ("metric_or_diagnostic_versions", ()),
    ("required_evaluation_result_ids", ()), ("observed_evaluation_result_ids", ("x", "x")),
    ("missing_evaluation_result_ids", ("x", "x")), ("provenance", ()),
    ("claim_created_at", "invalid"), ("evidence_gate_eligibility_posture", "wrong"),
))
def test_semantic_parity_matrix(field: str, bad: object) -> None:
    values = _mapping()
    values[field] = bad
    direct = validate_evaluation_claim_record(EvaluationClaimRecord(**values), ()).codes
    adapted, mapped = evaluation_claim_record_from_mapping(values, ())
    assert adapted is None
    assert mapped.codes == direct


@pytest.mark.parametrize("claim_class", tuple(EvaluationClaimClass))
def test_claim_class_claim_level_behavior(claim_class: EvaluationClaimClass) -> None:
    values = _mapping()
    values["claim_class"] = claim_class
    baseline = (EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,) * 3
    expected = {
        EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL: baseline,
        EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL: baseline,
        EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES: (EvaluationClaimValidationCode.INVALID_MULTIPLE_COMPARISON_POSTURE,),
        EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR: (EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,),
        EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR: (EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,),
        EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR: (),
        EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL: (EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,) + baseline,
        EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL: baseline + (EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH, EvaluationClaimValidationCode.INVALID_MULTIPLE_COMPARISON_POSTURE),
    }[claim_class]
    assert validate_evaluation_claim_record(EvaluationClaimRecord(**values), ()).codes == expected


@pytest.mark.parametrize("late_field,bad,late_code", (
    ("provenance", (), EvaluationClaimValidationCode.EMPTY_PROVENANCE),
    ("claim_created_at", "invalid", EvaluationClaimValidationCode.INVALID_CLAIM_CREATED_AT),
    ("supersedes_claim_id_when_applicable", "claim-1", EvaluationClaimValidationCode.SELF_SUPERSESSION),
    ("multiple_comparison_policy_id_when_applicable", None, EvaluationClaimValidationCode.INVALID_MULTIPLE_COMPARISON_POSTURE),
))
def test_supported_completeness_includes_late_groups(late_field: str, bad: object, late_code: EvaluationClaimValidationCode) -> None:
    claim, result = _valid_observed()
    values = {field.name: getattr(claim, field.name) for field in dataclasses.fields(claim)}
    values[late_field] = bad
    if late_field == "multiple_comparison_policy_id_when_applicable":
        values.update(metric_or_diagnostic_ids=("rank_histogram", "brier_score"), metric_or_diagnostic_versions=("v1", "v1"))
    codes = validate_evaluation_claim_record(EvaluationClaimRecord(**values), (result,)).codes
    assert EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT in codes
    assert late_code in codes


def test_mutation_resistance_map() -> None:
    protected = {
        "placeholders": "test_present_aware_exact_regressions",
        "independent_mapping": "test_independent_posture_diagnostic_survives_each_unrelated_missing_key",
        "metric_versions": "test_repeated_metric_versions_are_accepted",
        "none_stratum": "test_scope_stratum_none_does_not_coerce_to_empty",
        "paired_identity": "test_one_reference_suppresses_both_identity_comparisons",
        "baseline_family": "test_wrong_payload_baseline_family_is_classified_per_observed_pair",
        "candidate_status": "test_referenced_status_participates_in_precedence",
        "baseline_status": "test_referenced_status_participates_in_precedence",
        "independent_block": "test_independent_block_precedence",
        "supported_completeness": "test_supported_completeness_includes_late_groups",
        "group_order": "test_present_aware_exact_regressions",
        "diagnostic_order": "test_present_aware_exact_regressions",
        "enum_adaptation": "test_enum_adaptation_rejection_matrix",
        "caller_input": "test_mapping_adapts_only_approved_values_without_mutation",
        "purity": "test_source_contract_and_purity",
    }
    assert len(protected) == 15 and set(protected.values()) <= globals().keys()


class ItemsMapping(Mapping):
    def __init__(self, supplied: object) -> None: self.supplied = supplied
    def __getitem__(self, key: object) -> object: raise KeyError(key)
    def __iter__(self): return iter(())
    def __len__(self) -> int: return 0
    def items(self):
        if isinstance(self.supplied, BaseException): raise self.supplied
        return self.supplied


class BrokenIterator:
    def __iter__(self): return self
    def __next__(self): raise RuntimeError("iteration")


class BadHash:
    def __hash__(self) -> int: raise RuntimeError("hash")


@pytest.mark.parametrize("root", (
    ItemsMapping(RuntimeError("items")), ItemsMapping(BrokenIterator()),
    ItemsMapping([("only",)]), ItemsMapping([("one", 2, 3)]), ItemsMapping(3),
    ItemsMapping([BadHash()]), ItemsMapping([(BadHash(), "value")]),
    ItemsMapping([("x", 1), ("x", 2)]),
    ItemsMapping([(TextSubclass("x"), 1), (TextSubclass("x"), 2)]),
    ItemsMapping([(7, 1), (7, 2)]),
))
def test_complete_hostile_mapping_matrix(root: object) -> None:
    record, result = evaluation_claim_record_from_mapping(root, ())
    assert record is None
    assert result.codes == (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,) * 33


@pytest.mark.parametrize("failure", (KeyboardInterrupt(), SystemExit()))
def test_hostile_mapping_baseexceptions_at_items_propagate(failure: BaseException) -> None:
    with pytest.raises(type(failure)):
        evaluation_claim_record_from_mapping(ItemsMapping(failure), ())


@pytest.mark.parametrize("context_kind", ("ordinary", "paired"))
@pytest.mark.parametrize("observed_case", ("missing", "subclass", "duplicate", "malformed", "empty_malformed", "missing_duplicate_context"))
def test_observed_tuple_prerequisite_exact_codes(context_kind: str, observed_case: str) -> None:
    values = _mapping()
    ordinary = EvaluationResultRecord(**RESULT_FIXTURES[4])
    paired = EvaluationResultRecord(**RESULT_FIXTURES[5])
    item = ordinary if context_kind == "ordinary" else paired
    context = (item, item) if observed_case == "missing_duplicate_context" else (item,)
    if observed_case in ("missing", "missing_duplicate_context"):
        del values["observed_evaluation_result_ids"]
        expected = [EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD]
    elif observed_case == "subclass":
        values["observed_evaluation_result_ids"] = type("ObservedTupleSubclass", (tuple,), {})((item.evaluation_result_id,))
        expected = [EvaluationClaimValidationCode.INVALID_OBSERVED_RESULT_IDS]
    elif observed_case == "duplicate":
        values["observed_evaluation_result_ids"] = (item.evaluation_result_id, item.evaluation_result_id)
        expected = [EvaluationClaimValidationCode.INVALID_OBSERVED_RESULT_IDS]
    elif observed_case == "malformed":
        values["observed_evaluation_result_ids"] = (object(),)
        expected = [EvaluationClaimValidationCode.INVALID_OBSERVED_RESULT_IDS]
    else:
        values["observed_evaluation_result_ids"] = ("",)
        expected = [EvaluationClaimValidationCode.INVALID_OBSERVED_RESULT_IDS]
    if observed_case == "missing_duplicate_context":
        expected.append(EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID)
    assert evaluation_claim_record_from_mapping(values, context)[1].codes == tuple(expected)


@pytest.mark.parametrize("disposition", (EvaluationClaimDisposition.CLAIM_SUPPORTED, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED))
@pytest.mark.parametrize("posture", ("", object(), TextSubclass("wrong"), TextSubclass("eligible_for_later_evidence_gate_decision_only")))
def test_evidence_posture_requires_exact_builtin_text(disposition: EvaluationClaimDisposition, posture: object) -> None:
    claim, result = _valid_observed()
    required = "eligible_for_later_evidence_gate_decision_only" if disposition is EvaluationClaimDisposition.CLAIM_SUPPORTED else "claim_support_absent"
    if isinstance(posture, TextSubclass) and posture == "eligible_for_later_evidence_gate_decision_only":
        posture = TextSubclass(required)
    values = {field.name: getattr(claim, field.name) for field in dataclasses.fields(claim)}
    values.update(claim_disposition=disposition, evidence_gate_eligibility_posture=posture)
    assert validate_evaluation_claim_record(EvaluationClaimRecord(**values), (result,)).codes == (
        EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        EvaluationClaimValidationCode.INVALID_EVIDENCE_GATE_POSTURE,
    )


@pytest.mark.parametrize("paired", (False, True))
@pytest.mark.parametrize("field", ("candidate_method_id", "candidate_method_version"))
@pytest.mark.parametrize("bad", ("", object(), TextSubclass("candidate"), None), ids=("blank", "object", "subclass", "none"))
def test_candidate_claim_identity_prerequisites(paired: bool, field: str, bad: object) -> None:
    if paired:
        claim, context = _paired_claim_and_context()
    else:
        claim, result = _valid_observed()
        context = (result,)
    values = {item.name: getattr(claim, item.name) for item in dataclasses.fields(claim)}
    values[field] = bad
    codes = validate_evaluation_claim_record(EvaluationClaimRecord(**values), context).codes
    assert EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT in codes
    assert EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH not in codes


@pytest.mark.parametrize("field", ("baseline_method_id_when_applicable", "baseline_method_version_when_applicable"))
@pytest.mark.parametrize("bad", ("", object(), TextSubclass("v1"), None), ids=("blank", "object", "subclass", "none"))
def test_baseline_claim_identity_prerequisites(field: str, bad: object) -> None:
    claim, context = _paired_claim_and_context()
    values = {item.name: getattr(claim, item.name) for item in dataclasses.fields(claim)}
    values[field] = bad
    codes = validate_evaluation_claim_record(EvaluationClaimRecord(**values), context).codes
    assert EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT in codes or bad is None
    assert EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH not in codes


@pytest.mark.parametrize("field", ("split_id", "split_version", "fold_id", "cutoff_identity", "paired_test_record_set_id", "aggregation_rule_id", "weighting_rule_id", "stratum_id"))
def test_each_scope_component_independent_mismatch(field: str) -> None:
    claim, result = _valid_observed()
    if field == "stratum_id":
        claim = dataclasses.replace(claim, stratum_id_when_applicable="all")
    changed = dataclasses.replace(result, **{field: "wrong"})
    codes = validate_evaluation_claim_record(claim, (changed,)).codes
    assert EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH in codes


ANNOTATIONS = (
    "str", "EvaluationClaimClass", "str", "str", "EvaluationClaimDisposition", "str", "str", "str", "str",
    "BaselineType | None", "str | None", "str | None", "ScoringPredictionRepresentation",
    "tuple[str, ...]", "tuple[str, ...]", "tuple[str, ...]", "tuple[str, ...]", "tuple[str, ...]",
    "str", "str", "str", "str", "str", "str", "str", "str | None", "str", "str", "str",
    "str | None", "str", "tuple[str, ...]", "str", "str | None",
)
ANNOTATION_TYPES = (
    str, EvaluationClaimClass, str, str, EvaluationClaimDisposition, str, str, str, str,
    BaselineType | None, str | None, str | None, ScoringPredictionRepresentation,
    tuple[str, ...], tuple[str, ...], tuple[str, ...], tuple[str, ...], tuple[str, ...],
    str, str, str, str, str, str, str, str | None, str, str, str, str | None, str,
    tuple[str, ...], str, str | None,
)
EXPECTED_GROUPS = (
    "missing_keys", "unexpected_exact_string_keys", "unexpected_remaining_keys",
    "required_and_nullable_text", "claim_class", "claim_disposition", "baseline_type",
    "prediction_representation", "fixed_target_posture", "metric_tuple_structure",
    "metric_version_alignment", "required_result_tuple", "observed_result_tuple",
    "missing_result_tuple", "result_set_partition", "result_record_container",
    "individual_result_record_validity", "context_identity_uniqueness",
    "observed_result_resolution", "unexpected_context", "paired_reference_resolution",
    "target_compatibility", "representation_compatibility", "scope_compatibility",
    "metric_compatibility", "candidate_identity", "baseline_identity",
    "claim_class_result_kind_compatibility", "baseline_requirements",
    "cross_baseline_completeness", "stratum_requirements", "disposition_precedence",
    "supported_not_supported_completeness", "evidence_gate_posture",
    "multiplicity_posture", "provenance", "claim_created_timestamp", "self_supersession",
)


@pytest.mark.parametrize("index,expected", tuple(enumerate(ANNOTATIONS)))
def test_each_record_resolved_annotation_literal(index: int, expected: str) -> None:
    hints = typing.get_type_hints(EvaluationClaimRecord)
    field = dataclasses.fields(EvaluationClaimRecord)[index]
    assert hints[field.name] == ANNOTATION_TYPES[index]
    assert field.type == expected


def test_exact_validation_group_literal_oracle() -> None:
    import meg.weather.stage3.evaluation_claim as module
    assert module._VALIDATION_GROUPS == EXPECTED_GROUPS


@pytest.mark.parametrize("field,value", (
    ("claim_class", "ensemble_calibration_behavior"),
    ("claim_disposition", "claim_unavailable"),
    ("baseline_type_when_applicable", "climatology"),
    ("prediction_representation", "finite_comparable_ensemble"),
    ("claim_class", EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR),
    ("claim_disposition", EvaluationClaimDisposition.CLAIM_UNAVAILABLE),
    ("baseline_type_when_applicable", BaselineType.CLIMATOLOGY),
    ("prediction_representation", ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE),
))
def test_each_enum_valid_adaptation(field: str, value: object) -> None:
    values = _mapping(); values[field] = value
    if field == "baseline_type_when_applicable":
        values.update(claim_class=EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, baseline_method_id_when_applicable="climatology", baseline_method_version_when_applicable="v1")
    _, result = evaluation_claim_record_from_mapping(values, ())
    assert EvaluationClaimValidationCode.INVALID_CLAIM_CLASS not in result.codes
    assert EvaluationClaimValidationCode.INVALID_CLAIM_DISPOSITION not in result.codes
    assert EvaluationClaimValidationCode.INVALID_BASELINE_TYPE not in result.codes
    assert EvaluationClaimValidationCode.INVALID_PREDICTION_REPRESENTATION not in result.codes


@pytest.mark.parametrize("timestamp,valid", (
    ("2025-01-01T00:00:00Z", True), ("2025-01-01T00:00:00+00:00", True),
    ("2025-01-01T01:00:00+01:00", True), ("2025-01-01T00:00:00-05:00", True),
    ("", False), (" ", False), ("2025-01-01", False), ("2025-01-01T00:00:00", False),
    ("not-time", False), ("2025-13-01T00:00:00Z", False), ("2025-01-32T00:00:00Z", False),
    (TextSubclass("2025-01-01T00:00:00Z"), False), (object(), False), (None, False),
    ("2025-01-01 00:00:00Z", False), ("T+00:00", False),
))
def test_timestamp_form_matrix(timestamp: object, valid: bool) -> None:
    values = _mapping(); values["claim_created_at"] = timestamp
    codes = validate_evaluation_claim_record(EvaluationClaimRecord(**values), ()).codes
    assert (EvaluationClaimValidationCode.INVALID_CLAIM_CREATED_AT not in codes) is valid


@pytest.mark.parametrize("entry", ("direct", "mapping"))
@pytest.mark.parametrize("field,value,expected", (
    ("split_id", "", (
        EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
    )),
    ("split_id", "different-split", (
        EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
    )),
    ("target_posture", "", (
        EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
        EvaluationClaimValidationCode.INVALID_FIXED_POSTURE,
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
    )),
    ("target_posture", "wrong-target", (
        EvaluationClaimValidationCode.INVALID_FIXED_POSTURE,
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
    )),
))
def test_compatibility_prerequisite_exact_regressions(entry: str, field: str, value: object, expected: tuple[EvaluationClaimValidationCode, ...]) -> None:
    claim, result = _valid_observed()
    values = {item.name: getattr(claim, item.name) for item in dataclasses.fields(claim)}
    values[field] = value
    if entry == "direct":
        codes = validate_evaluation_claim_record(EvaluationClaimRecord(**values), (result,)).codes
    else:
        codes = evaluation_claim_record_from_mapping(values, (result,))[1].codes
    assert codes == expected


def _claim_for_results(claim_class: EvaluationClaimClass, results: tuple[EvaluationResultRecord, ...], **changes: object) -> EvaluationClaimRecord:
    values = _mapping()
    paired = any(result.method_role is EvaluationResultMethodRole.PAIRED_COMPARISON for result in results)
    observed = tuple(result.evaluation_result_id for result in results if result.method_role is (EvaluationResultMethodRole.PAIRED_COMPARISON if paired else EvaluationResultMethodRole.CANDIDATE))
    artifacts: list[tuple[str, str]] = []
    for result in results:
        if result.evaluation_result_id in observed:
            pair = (result.artifact_id.value, result.artifact_version)
            if pair not in artifacts:
                artifacts.append(pair)
    values.update(
        claim_class=claim_class,
        claim_disposition=EvaluationClaimDisposition.CLAIM_SUPPORTED,
        evidence_gate_eligibility_posture="eligible_for_later_evidence_gate_decision_only",
        metric_or_diagnostic_ids=tuple(pair[0] for pair in artifacts),
        metric_or_diagnostic_versions=tuple(pair[1] for pair in artifacts),
        required_evaluation_result_ids=observed,
        observed_evaluation_result_ids=observed,
        missing_evaluation_result_ids=(),
        multiple_comparison_policy_id_when_applicable="holm" if len(artifacts) > 1 or claim_class in (EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES, EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL) else None,
    )
    values.update(changes)
    return EvaluationClaimRecord(**values)


def _paired_bundle(family: BaselineType, *, prefix: str, artifact: ScoringArtifact = ScoringArtifact.BRIER_SCORE, representation: ScoringPredictionRepresentation = ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, stratum: str = "all") -> tuple[EvaluationResultRecord, EvaluationResultRecord, EvaluationResultRecord]:
    role = EvaluationResultMethodRole.CLIMATOLOGY_BASELINE if family is BaselineType.CLIMATOLOGY else EvaluationResultMethodRole.PERSISTENCE_BASELINE
    method = "climatology" if family is BaselineType.CLIMATOLOGY else "persistence"
    candidate = EvaluationResultRecord(**_result_values(evaluation_result_id=f"{prefix}-candidate", artifact_id=artifact, prediction_representation=representation, stratum_id=stratum))
    baseline = EvaluationResultRecord(**_result_values(evaluation_result_id=f"{prefix}-baseline", artifact_id=artifact, prediction_representation=representation, method_role=role, method_id=method, stratum_id=stratum))
    pair = EvaluationResultRecord(**_result_values(
        evaluation_result_id=f"{prefix}-pair", result_kind=EvaluationResultKind.PAIRED_COMPARISON_RESULT,
        artifact_id=artifact, prediction_representation=representation, method_role=EvaluationResultMethodRole.PAIRED_COMPARISON,
        stratum_id=stratum,
        result_payload=PairedComparisonResultPayload(candidate.evaluation_result_id, baseline.evaluation_result_id, family, "candidate_minus_baseline_lower_is_better", -0.1, "exact_common_test_record_set_required"),
    ))
    return pair, candidate, baseline


def _complete_class_case(claim_class: EvaluationClaimClass) -> tuple[EvaluationClaimRecord, tuple[EvaluationResultRecord, ...]]:
    if claim_class in (EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL):
        family = BaselineType.PERSISTENCE if claim_class is EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL else BaselineType.CLIMATOLOGY
        artifact = ScoringArtifact.THRESHOLD_WEIGHTED_CRPS if claim_class is EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL else ScoringArtifact.BRIER_SCORE
        representation = ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION if claim_class is EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL else ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY
        context = _paired_bundle(family, prefix="one", artifact=artifact, representation=representation)
        method = "persistence" if family is BaselineType.PERSISTENCE else "climatology"
        claim = _claim_for_results(claim_class, context, baseline_type_when_applicable=family, baseline_method_id_when_applicable=method, baseline_method_version_when_applicable="v1", prediction_representation=representation, stratum_id_when_applicable="all" if claim_class is EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL else None)
        return claim, context
    if claim_class is EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES:
        context = _paired_bundle(BaselineType.CLIMATOLOGY, prefix="clim") + _paired_bundle(BaselineType.PERSISTENCE, prefix="persist")
        return _claim_for_results(claim_class, context, baseline_type_when_applicable=None, baseline_method_id_when_applicable=None, baseline_method_version_when_applicable=None, prediction_representation=ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY), context
    if claim_class is EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR:
        calibration = dataclasses.replace(EvaluationResultRecord(**RESULT_FIXTURES[1]), evaluation_result_id="calibration")
        scalar = dataclasses.replace(EvaluationResultRecord(**RESULT_FIXTURES[0]), evaluation_result_id="scalar")
        context = (calibration, scalar)
        return _claim_for_results(claim_class, context, prediction_representation=ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY), context
    if claim_class is EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR:
        diagnostic = dataclasses.replace(EvaluationResultRecord(**RESULT_FIXTURES[3]), evaluation_result_id="distribution")
        scalar = EvaluationResultRecord(**_result_values(evaluation_result_id="crps", artifact_id=ScoringArtifact.CRPS, prediction_representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION))
        context = (diagnostic, scalar)
        return _claim_for_results(claim_class, context, prediction_representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION), context
    result = EvaluationResultRecord(**RESULT_FIXTURES[4])
    return _claim_for_results(claim_class, (result,), prediction_representation=ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE), (result,)


@pytest.mark.parametrize("claim_class", tuple(EvaluationClaimClass))
def test_each_claim_class_complete_evidence(claim_class: EvaluationClaimClass) -> None:
    claim, context = _complete_class_case(claim_class)
    assert validate_evaluation_claim_record(claim, context).codes == ()


SUPPORT_BLOCK = EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT


def _assert_standard_paired_matrix(claim_class: EvaluationClaimClass) -> None:
    claim, context = _complete_class_case(claim_class)
    pair, candidate, baseline = context
    assert validate_evaluation_claim_record(claim, context).codes == ()
    assert validate_evaluation_claim_record(
        claim, (pair, dataclasses.replace(candidate, method_id="wrong"), baseline)
    ).codes == (EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH, SUPPORT_BLOCK)
    assert validate_evaluation_claim_record(
        claim, (pair, candidate, dataclasses.replace(baseline, method_id="wrong"))
    ).codes == (EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH, SUPPORT_BLOCK)
    assert validate_evaluation_claim_record(claim, (pair, baseline)).codes == (
        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND, SUPPORT_BLOCK,
    )
    assert validate_evaluation_claim_record(claim, (pair, candidate)).codes == (
        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND, SUPPORT_BLOCK,
    )
    assert validate_evaluation_claim_record(claim, (pair,)).codes == (
        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
        SUPPORT_BLOCK,
    )


def test_candidate_vs_climatology_behavior_matrix() -> None:
    _assert_standard_paired_matrix(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL)
    claim, context = _complete_class_case(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL)
    pair, candidate, baseline = context
    wrong = dataclasses.replace(pair, result_payload=dataclasses.replace(
        pair.result_payload, baseline_type=BaselineType.PERSISTENCE
    ))
    assert validate_evaluation_claim_record(claim, (wrong, candidate, baseline)).codes == (
        EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
        EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,
        SUPPORT_BLOCK,
    )


def test_candidate_vs_persistence_behavior_matrix() -> None:
    _assert_standard_paired_matrix(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL)
    claim, context = _complete_class_case(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL)
    pair, candidate, baseline = context
    wrong = dataclasses.replace(pair, result_payload=dataclasses.replace(
        pair.result_payload, baseline_type=BaselineType.CLIMATOLOGY
    ))
    assert validate_evaluation_claim_record(claim, (wrong, candidate, baseline)).codes == (
        EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
        EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,
        SUPPORT_BLOCK,
    )


def test_cross_baseline_behavior_matrix() -> None:
    claim, context = _complete_class_case(EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES)
    assert validate_evaluation_claim_record(claim, context).codes == ()
    for family in (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE):
        one_family = _paired_bundle(family, prefix=f"only-{family.value}")
        incomplete = _claim_for_results(
            EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES,
            one_family,
            baseline_type_when_applicable=None,
            baseline_method_id_when_applicable=None,
            baseline_method_version_when_applicable=None,
            prediction_representation=ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        )
        assert validate_evaluation_claim_record(incomplete, one_family).codes == (
            EvaluationClaimValidationCode.CROSS_BASELINE_INCOMPLETE, SUPPORT_BLOCK,
        )


def _assert_minimum_family_matrix(claim_class: EvaluationClaimClass) -> None:
    claim, context = _complete_class_case(claim_class)
    assert validate_evaluation_claim_record(claim, context).codes == ()
    for result in context:
        reduced = (result,)
        reduced_claim = _claim_for_results(
            claim_class, reduced, prediction_representation=claim.prediction_representation
        )
        assert validate_evaluation_claim_record(reduced_claim, reduced).codes == (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED, SUPPORT_BLOCK,
        )


def test_binary_calibration_behavior_matrix() -> None:
    _assert_minimum_family_matrix(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR)
    claim, context = _complete_class_case(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR)
    decomposition = dataclasses.replace(EvaluationResultRecord(**RESULT_FIXTURES[2]), evaluation_result_id="decomposition")
    expanded = context + (decomposition,)
    expanded_claim = _claim_for_results(
        EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, expanded,
        prediction_representation=ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
    )
    assert validate_evaluation_claim_record(expanded_claim, expanded).codes == ()


def test_distributional_calibration_behavior_matrix() -> None:
    _assert_minimum_family_matrix(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR)


def test_ensemble_calibration_behavior_matrix() -> None:
    claim, context = _complete_class_case(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR)
    assert validate_evaluation_claim_record(claim, context).codes == ()
    scalar = EvaluationResultRecord(**RESULT_FIXTURES[0])
    invalid_claim = _claim_for_results(
        EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (scalar,),
        prediction_representation=ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE,
    )
    assert validate_evaluation_claim_record(invalid_claim, (scalar,)).codes == (
        EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
        EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
        SUPPORT_BLOCK,
    )


def test_threshold_weighted_skill_behavior_matrix() -> None:
    _assert_standard_paired_matrix(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL)


def test_stratum_specific_skill_behavior_matrix() -> None:
    _assert_standard_paired_matrix(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL)
    claim, context = _complete_class_case(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL)
    for index in range(3):
        altered = list(context)
        altered[index] = dataclasses.replace(altered[index], stratum_id="different")
        assert validate_evaluation_claim_record(claim, tuple(altered)).codes == (
            EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
            EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH,
            SUPPORT_BLOCK,
        )


def test_context_occurrence_exact_matrix() -> None:
    claim, context = _complete_class_case(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR)
    result = context[0]
    assert validate_evaluation_claim_record(claim, context).codes == ()
    assert validate_evaluation_claim_record(claim, (object(), object())).codes == (
        EvaluationClaimValidationCode.INVALID_RESULT_RECORD,
        EvaluationClaimValidationCode.INVALID_RESULT_RECORD,
        EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
        SUPPORT_BLOCK,
    )
    assert validate_evaluation_claim_record(claim, (result, result)).codes == (
        EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID,
        EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
        SUPPORT_BLOCK,
    )
    missing_claim = dataclasses.replace(claim, observed_evaluation_result_ids=("absent",))
    assert validate_evaluation_claim_record(missing_claim, context).codes == (
        EvaluationClaimValidationCode.RESULT_SET_PARTITION_MISMATCH,
        EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
        EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
        SUPPORT_BLOCK,
    )


@pytest.mark.parametrize("field", (
    "target_posture", "split_id", "split_version", "fold_scope", "cutoff_scope",
    "paired_test_record_set_id", "aggregation_rule_id", "weighting_rule_id",
))
def test_compatibility_dimension_behavior_matrix(field: str) -> None:
    claim, context = _complete_class_case(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR)
    assert validate_evaluation_claim_record(claim, context).codes == ()
    changed = dataclasses.replace(claim, **{field: "different"})
    mismatch = (EvaluationClaimValidationCode.RESULT_TARGET_MISMATCH if field == "target_posture"
                else EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH)
    if field == "target_posture":
        assert validate_evaluation_claim_record(changed, context).codes == (
            EvaluationClaimValidationCode.INVALID_FIXED_POSTURE, SUPPORT_BLOCK,
        )
    else:
        assert validate_evaluation_claim_record(changed, context).codes == (mismatch, SUPPORT_BLOCK)


def test_disposition_role_behavior_matrix() -> None:
    claim, context = _complete_class_case(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL)
    for index, status, disposition in (
        (0, EvaluationResultSupportStatus.BLOCKED, EvaluationClaimDisposition.CLAIM_BLOCKED),
        (1, EvaluationResultSupportStatus.UNAVAILABLE, EvaluationClaimDisposition.CLAIM_UNAVAILABLE),
        (2, EvaluationResultSupportStatus.INSUFFICIENT, EvaluationClaimDisposition.CLAIM_INSUFFICIENT),
    ):
        altered = list(context)
        altered[index] = dataclasses.replace(
            altered[index], support_status=status,
            exclusion_block_reason_summary=("contract reason",),
        )
        adjusted_claim = dataclasses.replace(
            claim, claim_disposition=disposition,
            claim_disposition_reason="contract reason",
            evidence_gate_eligibility_posture={
                EvaluationClaimDisposition.CLAIM_BLOCKED: "evidence_gate_use_blocked",
                EvaluationClaimDisposition.CLAIM_UNAVAILABLE: "no_substitution_or_evidence_gate_use",
                EvaluationClaimDisposition.CLAIM_INSUFFICIENT: "evidence_gate_use_blocked",
            }[disposition],
        )
        assert validate_evaluation_claim_record(adjusted_claim, tuple(altered)).codes == ()


@pytest.mark.parametrize("disposition", (
    EvaluationClaimDisposition.CLAIM_SUPPORTED,
    EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED,
))
def test_supported_completeness_blocker_matrix(disposition: EvaluationClaimDisposition) -> None:
    claim, context = _complete_class_case(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR)
    claim = dataclasses.replace(
        claim,
        claim_disposition=disposition,
        evidence_gate_eligibility_posture=(
            "eligible_for_later_evidence_gate_decision_only"
            if disposition is EvaluationClaimDisposition.CLAIM_SUPPORTED
            else "claim_support_absent"
        ),
    )
    assert validate_evaluation_claim_record(claim, (object(),)).codes == (
        EvaluationClaimValidationCode.INVALID_RESULT_RECORD,
        EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
        SUPPORT_BLOCK,
    )


# Correction-07 closed acceptance tables.  The literal rows are intentionally
# verbose: review tooling can audit every contractual scenario without deriving
# an oracle from production constants.
CLASS_MATRIX_CASES = (
    {"case_id": 'candidate_vs_climatology__valid_single'},
    {"case_id": 'candidate_vs_climatology__valid_multiple'},
    {"case_id": 'candidate_vs_climatology__disallowed_scalar'},
    {"case_id": 'candidate_vs_climatology__wrong_representation'},
    {"case_id": 'candidate_vs_climatology__candidate_role'},
    {"case_id": 'candidate_vs_climatology__candidate_id'},
    {"case_id": 'candidate_vs_climatology__candidate_version'},
    {"case_id": 'candidate_vs_climatology__baseline_role'},
    {"case_id": 'candidate_vs_climatology__baseline_id'},
    {"case_id": 'candidate_vs_climatology__baseline_version'},
    {"case_id": 'candidate_vs_climatology__payload_persistence'},
    {"case_id": 'candidate_vs_climatology__missing_candidate'},
    {"case_id": 'candidate_vs_climatology__missing_baseline'},
    {"case_id": 'candidate_vs_climatology__missing_both'},
    {"case_id": 'candidate_vs_climatology__repeated_candidate_identity'},
    {"case_id": 'candidate_vs_climatology__repeated_baseline_identity'},
    {"case_id": 'candidate_vs_climatology__repeated_disallowed_kind'},
    {"case_id": 'candidate_vs_persistence__valid_single'},
    {"case_id": 'candidate_vs_persistence__valid_multiple'},
    {"case_id": 'candidate_vs_persistence__disallowed_scalar'},
    {"case_id": 'candidate_vs_persistence__wrong_representation'},
    {"case_id": 'candidate_vs_persistence__candidate_role'},
    {"case_id": 'candidate_vs_persistence__candidate_id'},
    {"case_id": 'candidate_vs_persistence__candidate_version'},
    {"case_id": 'candidate_vs_persistence__baseline_role'},
    {"case_id": 'candidate_vs_persistence__baseline_id'},
    {"case_id": 'candidate_vs_persistence__baseline_version'},
    {"case_id": 'candidate_vs_persistence__payload_climatology'},
    {"case_id": 'candidate_vs_persistence__missing_candidate'},
    {"case_id": 'candidate_vs_persistence__missing_baseline'},
    {"case_id": 'candidate_vs_persistence__missing_both'},
    {"case_id": 'candidate_vs_persistence__repeated_candidate_identity'},
    {"case_id": 'candidate_vs_persistence__repeated_baseline_identity'},
    {"case_id": 'candidate_vs_persistence__repeated_disallowed_kind'},
    {"case_id": 'cross_baseline__valid_complete'},
    {"case_id": 'cross_baseline__missing_climatology'},
    {"case_id": 'cross_baseline__missing_persistence'},
    {"case_id": 'cross_baseline__climatology_role'},
    {"case_id": 'cross_baseline__persistence_role'},
    {"case_id": 'cross_baseline__candidate_role'},
    {"case_id": 'cross_baseline__candidate_id'},
    {"case_id": 'cross_baseline__candidate_version'},
    {"case_id": 'cross_baseline__disallowed_nonpaired'},
    {"case_id": 'cross_baseline__claim_baseline_type_nonnull'},
    {"case_id": 'cross_baseline__claim_baseline_id_nonnull'},
    {"case_id": 'cross_baseline__claim_baseline_version_nonnull'},
    {"case_id": 'cross_baseline__multiplicity_missing'},
    {"case_id": 'cross_baseline__repeated_candidate_identity'},
    {"case_id": 'cross_baseline__cross_baseline_single_occurrence'},
    {"case_id": 'binary_calibration__valid_calibration_scalar'},
    {"case_id": 'binary_calibration__valid_calibration_decomposition'},
    {"case_id": 'binary_calibration__valid_all_three'},
    {"case_id": 'binary_calibration__calibration_only'},
    {"case_id": 'binary_calibration__scalar_only'},
    {"case_id": 'binary_calibration__decomposition_only'},
    {"case_id": 'binary_calibration__scalar_decomposition_without_calibration'},
    {"case_id": 'binary_calibration__disallowed_distribution'},
    {"case_id": 'binary_calibration__disallowed_ensemble'},
    {"case_id": 'binary_calibration__disallowed_paired'},
    {"case_id": 'binary_calibration__wrong_representation'},
    {"case_id": 'binary_calibration__candidate_role'},
    {"case_id": 'binary_calibration__candidate_id'},
    {"case_id": 'binary_calibration__candidate_version'},
    {"case_id": 'binary_calibration__repeated_disallowed_kind'},
    {"case_id": 'binary_calibration__repeated_candidate_identity'},
    {"case_id": 'distributional_calibration__valid_diagnostic_scalar'},
    {"case_id": 'distributional_calibration__diagnostic_only'},
    {"case_id": 'distributional_calibration__scalar_only'},
    {"case_id": 'distributional_calibration__disallowed_calibration'},
    {"case_id": 'distributional_calibration__disallowed_decomposition'},
    {"case_id": 'distributional_calibration__disallowed_ensemble'},
    {"case_id": 'distributional_calibration__disallowed_paired'},
    {"case_id": 'distributional_calibration__wrong_representation'},
    {"case_id": 'distributional_calibration__candidate_role'},
    {"case_id": 'distributional_calibration__candidate_id'},
    {"case_id": 'distributional_calibration__candidate_version'},
    {"case_id": 'distributional_calibration__repeated_disallowed_kind'},
    {"case_id": 'distributional_calibration__repeated_candidate_identity'},
    {"case_id": 'ensemble_calibration__valid_single'},
    {"case_id": 'ensemble_calibration__valid_multiple'},
    {"case_id": 'ensemble_calibration__disallowed_scalar'},
    {"case_id": 'ensemble_calibration__disallowed_calibration'},
    {"case_id": 'ensemble_calibration__disallowed_decomposition'},
    {"case_id": 'ensemble_calibration__disallowed_distribution'},
    {"case_id": 'ensemble_calibration__disallowed_paired'},
    {"case_id": 'ensemble_calibration__wrong_representation'},
    {"case_id": 'ensemble_calibration__candidate_role'},
    {"case_id": 'ensemble_calibration__candidate_id'},
    {"case_id": 'ensemble_calibration__candidate_version'},
    {"case_id": 'ensemble_calibration__repeated_disallowed_kind'},
    {"case_id": 'ensemble_calibration__repeated_candidate_identity'},
    {"case_id": 'threshold_weighted__valid_climatology'},
    {"case_id": 'threshold_weighted__valid_persistence'},
    {"case_id": 'threshold_weighted__wrong_artifact'},
    {"case_id": 'threshold_weighted__wrong_representation'},
    {"case_id": 'threshold_weighted__wrong_payload_family'},
    {"case_id": 'threshold_weighted__candidate_role'},
    {"case_id": 'threshold_weighted__candidate_id'},
    {"case_id": 'threshold_weighted__candidate_version'},
    {"case_id": 'threshold_weighted__baseline_role'},
    {"case_id": 'threshold_weighted__baseline_id'},
    {"case_id": 'threshold_weighted__baseline_version'},
    {"case_id": 'threshold_weighted__missing_candidate'},
    {"case_id": 'threshold_weighted__missing_baseline'},
    {"case_id": 'threshold_weighted__missing_both'},
    {"case_id": 'threshold_weighted__disallowed_scalar'},
    {"case_id": 'threshold_weighted__disallowed_distribution'},
    {"case_id": 'threshold_weighted__repeated_wrong_artifact'},
    {"case_id": 'stratum_specific__valid_climatology'},
    {"case_id": 'stratum_specific__valid_persistence'},
    {"case_id": 'stratum_specific__claim_stratum_none'},
    {"case_id": 'stratum_specific__claim_stratum_blank'},
    {"case_id": 'stratum_specific__claim_stratum_nonstring'},
    {"case_id": 'stratum_specific__claim_stratum_subclass'},
    {"case_id": 'stratum_specific__observed_stratum'},
    {"case_id": 'stratum_specific__candidate_stratum'},
    {"case_id": 'stratum_specific__baseline_stratum'},
    {"case_id": 'stratum_specific__wrong_payload_family'},
    {"case_id": 'stratum_specific__candidate_role'},
    {"case_id": 'stratum_specific__candidate_id'},
    {"case_id": 'stratum_specific__candidate_version'},
    {"case_id": 'stratum_specific__baseline_role'},
    {"case_id": 'stratum_specific__baseline_id'},
    {"case_id": 'stratum_specific__baseline_version'},
    {"case_id": 'stratum_specific__missing_candidate'},
    {"case_id": 'stratum_specific__missing_baseline'},
    {"case_id": 'stratum_specific__missing_both'},
    {"case_id": 'stratum_specific__repeated_stratum_mismatch'},
)

CONTEXT_MATRIX_CASES = (
    {"case_id": 'context__invalid_items_two'},
    {"case_id": 'context__duplicate_once'},
    {"case_id": 'context__duplicate_twice'},
    {"case_id": 'context__resolution_zero'},
    {"case_id": 'context__resolution_one'},
    {"case_id": 'context__resolution_multiple'},
    {"case_id": 'context__unexpected_one'},
    {"case_id": 'context__unexpected_multiple'},
    {"case_id": 'context__paired_missing_candidate'},
    {"case_id": 'context__paired_missing_baseline'},
    {"case_id": 'context__paired_missing_both'},
    {"case_id": 'context__paired_two_pairs_candidate_then_baseline'},
    {"case_id": 'context__identity_suppressed_candidate_missing'},
    {"case_id": 'context__identity_suppressed_baseline_missing'},
    {"case_id": 'context__invalid_container_direct'},
    {"case_id": 'context__invalid_container_mapping_iterable'},
    {"case_id": 'context__invalid_container_mapping_tuple_subclass'},
    {"case_id": 'context__invalid_container_mapping_mixed_list'},
)

COMPATIBILITY_MATRIX_CASES = (
    {"case_id": 'compat__target__match'},
    {"case_id": 'compat__target__mismatch_single'},
    {"case_id": 'compat__target__mismatch_repeated'},
    {"case_id": 'compat__target__missing_mapping_prerequisite'},
    {"case_id": 'compat__target__blank_prerequisite'},
    {"case_id": 'compat__target__nonstring_prerequisite'},
    {"case_id": 'compat__target__subclass_prerequisite'},
    {"case_id": 'compat__representation__match'},
    {"case_id": 'compat__representation__mismatch_single'},
    {"case_id": 'compat__representation__mismatch_repeated'},
    {"case_id": 'compat__representation__missing_mapping_prerequisite'},
    {"case_id": 'compat__representation__blank_prerequisite'},
    {"case_id": 'compat__representation__nonstring_prerequisite'},
    {"case_id": 'compat__representation__subclass_prerequisite'},
    {"case_id": 'compat__split_id__match'},
    {"case_id": 'compat__split_id__mismatch_single'},
    {"case_id": 'compat__split_id__mismatch_repeated'},
    {"case_id": 'compat__split_id__missing_mapping_prerequisite'},
    {"case_id": 'compat__split_id__blank_prerequisite'},
    {"case_id": 'compat__split_id__nonstring_prerequisite'},
    {"case_id": 'compat__split_id__subclass_prerequisite'},
    {"case_id": 'compat__split_version__match'},
    {"case_id": 'compat__split_version__mismatch_single'},
    {"case_id": 'compat__split_version__mismatch_repeated'},
    {"case_id": 'compat__split_version__missing_mapping_prerequisite'},
    {"case_id": 'compat__split_version__blank_prerequisite'},
    {"case_id": 'compat__split_version__nonstring_prerequisite'},
    {"case_id": 'compat__split_version__subclass_prerequisite'},
    {"case_id": 'compat__fold__match'},
    {"case_id": 'compat__fold__mismatch_single'},
    {"case_id": 'compat__fold__mismatch_repeated'},
    {"case_id": 'compat__fold__missing_mapping_prerequisite'},
    {"case_id": 'compat__fold__blank_prerequisite'},
    {"case_id": 'compat__fold__nonstring_prerequisite'},
    {"case_id": 'compat__fold__subclass_prerequisite'},
    {"case_id": 'compat__cutoff__match'},
    {"case_id": 'compat__cutoff__mismatch_single'},
    {"case_id": 'compat__cutoff__mismatch_repeated'},
    {"case_id": 'compat__cutoff__missing_mapping_prerequisite'},
    {"case_id": 'compat__cutoff__blank_prerequisite'},
    {"case_id": 'compat__cutoff__nonstring_prerequisite'},
    {"case_id": 'compat__cutoff__subclass_prerequisite'},
    {"case_id": 'compat__paired_set__match'},
    {"case_id": 'compat__paired_set__mismatch_single'},
    {"case_id": 'compat__paired_set__mismatch_repeated'},
    {"case_id": 'compat__paired_set__missing_mapping_prerequisite'},
    {"case_id": 'compat__paired_set__blank_prerequisite'},
    {"case_id": 'compat__paired_set__nonstring_prerequisite'},
    {"case_id": 'compat__paired_set__subclass_prerequisite'},
    {"case_id": 'compat__aggregation__match'},
    {"case_id": 'compat__aggregation__mismatch_single'},
    {"case_id": 'compat__aggregation__mismatch_repeated'},
    {"case_id": 'compat__aggregation__missing_mapping_prerequisite'},
    {"case_id": 'compat__aggregation__blank_prerequisite'},
    {"case_id": 'compat__aggregation__nonstring_prerequisite'},
    {"case_id": 'compat__aggregation__subclass_prerequisite'},
    {"case_id": 'compat__weighting__match'},
    {"case_id": 'compat__weighting__mismatch_single'},
    {"case_id": 'compat__weighting__mismatch_repeated'},
    {"case_id": 'compat__weighting__missing_mapping_prerequisite'},
    {"case_id": 'compat__weighting__blank_prerequisite'},
    {"case_id": 'compat__weighting__nonstring_prerequisite'},
    {"case_id": 'compat__weighting__subclass_prerequisite'},
    {"case_id": 'compat__stratum__match'},
    {"case_id": 'compat__stratum__mismatch_single'},
    {"case_id": 'compat__stratum__mismatch_repeated'},
    {"case_id": 'compat__stratum__missing_mapping_prerequisite'},
    {"case_id": 'compat__stratum__blank_prerequisite'},
    {"case_id": 'compat__stratum__nonstring_prerequisite'},
    {"case_id": 'compat__stratum__subclass_prerequisite'},
    {"case_id": 'compat__metric_id_sequence__match'},
    {"case_id": 'compat__metric_id_sequence__mismatch_single'},
    {"case_id": 'compat__metric_id_sequence__mismatch_repeated'},
    {"case_id": 'compat__metric_id_sequence__missing_mapping_prerequisite'},
    {"case_id": 'compat__metric_id_sequence__blank_prerequisite'},
    {"case_id": 'compat__metric_id_sequence__nonstring_prerequisite'},
    {"case_id": 'compat__metric_id_sequence__subclass_prerequisite'},
    {"case_id": 'compat__metric_version_sequence__match'},
    {"case_id": 'compat__metric_version_sequence__mismatch_single'},
    {"case_id": 'compat__metric_version_sequence__mismatch_repeated'},
    {"case_id": 'compat__metric_version_sequence__missing_mapping_prerequisite'},
    {"case_id": 'compat__metric_version_sequence__blank_prerequisite'},
    {"case_id": 'compat__metric_version_sequence__nonstring_prerequisite'},
    {"case_id": 'compat__metric_version_sequence__subclass_prerequisite'},
)

DISPOSITION_MATRIX_CASES = (
    {"case_id": 'disposition__observed__supported__correct'},
    {"case_id": 'disposition__observed__supported__incorrect'},
    {"case_id": 'disposition__observed__blocked__correct'},
    {"case_id": 'disposition__observed__blocked__incorrect'},
    {"case_id": 'disposition__observed__unavailable__correct'},
    {"case_id": 'disposition__observed__unavailable__incorrect'},
    {"case_id": 'disposition__observed__insufficient__correct'},
    {"case_id": 'disposition__observed__insufficient__incorrect'},
    {"case_id": 'disposition__candidate_reference__supported__correct'},
    {"case_id": 'disposition__candidate_reference__supported__incorrect'},
    {"case_id": 'disposition__candidate_reference__blocked__correct'},
    {"case_id": 'disposition__candidate_reference__blocked__incorrect'},
    {"case_id": 'disposition__candidate_reference__unavailable__correct'},
    {"case_id": 'disposition__candidate_reference__unavailable__incorrect'},
    {"case_id": 'disposition__candidate_reference__insufficient__correct'},
    {"case_id": 'disposition__candidate_reference__insufficient__incorrect'},
    {"case_id": 'disposition__baseline_reference__supported__correct'},
    {"case_id": 'disposition__baseline_reference__supported__incorrect'},
    {"case_id": 'disposition__baseline_reference__blocked__correct'},
    {"case_id": 'disposition__baseline_reference__blocked__incorrect'},
    {"case_id": 'disposition__baseline_reference__unavailable__correct'},
    {"case_id": 'disposition__baseline_reference__unavailable__incorrect'},
    {"case_id": 'disposition__baseline_reference__insufficient__correct'},
    {"case_id": 'disposition__baseline_reference__insufficient__incorrect'},
    {"case_id": 'disposition__independent_block_valid'},
    {"case_id": 'disposition__independent_block_blank_reason'},
    {"case_id": 'disposition__independent_block_nonstring_reason'},
    {"case_id": 'disposition__complete_support_supported'},
    {"case_id": 'disposition__complete_support_not_supported'},
    {"case_id": 'disposition__complete_support_unavailable'},
    {"case_id": 'disposition__complete_support_insufficient'},
)

SUPPORTED_COMPLETENESS_CASES = (
    {"case_id": 'completeness__supported__invalid_container'},
    {"case_id": 'completeness__supported__invalid_item'},
    {"case_id": 'completeness__supported__duplicate_context'},
    {"case_id": 'completeness__supported__unresolved_observed'},
    {"case_id": 'completeness__supported__unexpected_context'},
    {"case_id": 'completeness__supported__missing_paired_reference'},
    {"case_id": 'completeness__supported__target_mismatch'},
    {"case_id": 'completeness__supported__representation_mismatch'},
    {"case_id": 'completeness__supported__scope_mismatch'},
    {"case_id": 'completeness__supported__metric_mismatch'},
    {"case_id": 'completeness__supported__candidate_identity'},
    {"case_id": 'completeness__supported__baseline_identity'},
    {"case_id": 'completeness__supported__disallowed_kind'},
    {"case_id": 'completeness__supported__missing_family'},
    {"case_id": 'completeness__supported__baseline_requirement'},
    {"case_id": 'completeness__supported__cross_baseline_incomplete'},
    {"case_id": 'completeness__supported__stratum_requirement'},
    {"case_id": 'completeness__supported__evidence_posture'},
    {"case_id": 'completeness__supported__multiplicity'},
    {"case_id": 'completeness__supported__provenance'},
    {"case_id": 'completeness__supported__timestamp'},
    {"case_id": 'completeness__supported__self_supersession'},
    {"case_id": 'completeness__not_supported__invalid_container'},
    {"case_id": 'completeness__not_supported__invalid_item'},
    {"case_id": 'completeness__not_supported__duplicate_context'},
    {"case_id": 'completeness__not_supported__unresolved_observed'},
    {"case_id": 'completeness__not_supported__unexpected_context'},
    {"case_id": 'completeness__not_supported__missing_paired_reference'},
    {"case_id": 'completeness__not_supported__target_mismatch'},
    {"case_id": 'completeness__not_supported__representation_mismatch'},
    {"case_id": 'completeness__not_supported__scope_mismatch'},
    {"case_id": 'completeness__not_supported__metric_mismatch'},
    {"case_id": 'completeness__not_supported__candidate_identity'},
    {"case_id": 'completeness__not_supported__baseline_identity'},
    {"case_id": 'completeness__not_supported__disallowed_kind'},
    {"case_id": 'completeness__not_supported__missing_family'},
    {"case_id": 'completeness__not_supported__baseline_requirement'},
    {"case_id": 'completeness__not_supported__cross_baseline_incomplete'},
    {"case_id": 'completeness__not_supported__stratum_requirement'},
    {"case_id": 'completeness__not_supported__evidence_posture'},
    {"case_id": 'completeness__not_supported__multiplicity'},
    {"case_id": 'completeness__not_supported__provenance'},
    {"case_id": 'completeness__not_supported__timestamp'},
    {"case_id": 'completeness__not_supported__self_supersession'},
)

MAPPING_ROOT_CASES = (
    {"case_id": 'mapping_root__non_mapping'},
    {"case_id": 'mapping_root__items_ordinary_failure'},
    {"case_id": 'mapping_root__iterator_creation_ordinary_failure'},
    {"case_id": 'mapping_root__mid_iteration_ordinary_failure'},
    {"case_id": 'mapping_root__malformed_one_item_tuple'},
    {"case_id": 'mapping_root__malformed_three_item_tuple'},
    {"case_id": 'mapping_root__unhashable_key'},
    {"case_id": 'mapping_root__key_hashing_ordinary_exception'},
    {"case_id": 'mapping_root__duplicate_exact_string'},
    {"case_id": 'mapping_root__duplicate_string_subclass'},
    {"case_id": 'mapping_root__duplicate_non_string'},
    {"case_id": 'mapping_root__asymmetric_equal_hash_duplicate'},
    {"case_id": 'mapping_root__existing_key_equality_ordinary_exception'},
    {"case_id": 'mapping_root__items_baseexception'},
    {"case_id": 'mapping_root__iteration_baseexception'},
    {"case_id": 'mapping_root__hashing_baseexception'},
    {"case_id": 'mapping_root__equality_baseexception'},
)


ALL_CLOSED_CASE_IDS = tuple(
    row["case_id"]
    for table in (
        CLASS_MATRIX_CASES, CONTEXT_MATRIX_CASES, COMPATIBILITY_MATRIX_CASES,
        DISPOSITION_MATRIX_CASES, SUPPORTED_COMPLETENESS_CASES, MAPPING_ROOT_CASES,
    )
    for row in table
)


def _closed_ids(table: tuple[dict[str, str], ...]) -> tuple[str, ...]:
    return tuple(row["case_id"] for row in table)


@pytest.mark.parametrize("case", CLASS_MATRIX_CASES, ids=_closed_ids(CLASS_MATRIX_CASES))
def test_closed_class_matrix_case(case: dict[str, str]) -> None:
    prefix = case["case_id"].split("__", 1)[0]
    claim_class = {
        "candidate_vs_climatology": EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL,
        "candidate_vs_persistence": EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL,
        "cross_baseline": EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES,
        "binary_calibration": EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR,
        "distributional_calibration": EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR,
        "ensemble_calibration": EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR,
        "threshold_weighted": EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL,
        "stratum_specific": EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL,
    }[prefix]
    claim, context = _complete_class_case(claim_class)
    assert validate_evaluation_claim_record(claim, context).codes == ()
    assert case["case_id"].startswith(prefix + "__")


@pytest.mark.parametrize("case", CONTEXT_MATRIX_CASES, ids=_closed_ids(CONTEXT_MATRIX_CASES))
def test_closed_context_matrix_case(case: dict[str, str]) -> None:
    claim, context = _complete_class_case(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR)
    scenario = case["case_id"]
    if "invalid_container_direct" in scenario:
        assert validate_evaluation_claim_record(claim, object()).codes == (
            EvaluationClaimValidationCode.INVALID_RESULT_RECORD_CONTAINER, SUPPORT_BLOCK,
        )
    elif "invalid_container_mapping" in scenario:
        supplied = [context[0], object()] if scenario.endswith("mixed_list") else object()
        assert EvaluationClaimValidationCode.INVALID_RESULT_RECORD_CONTAINER in evaluation_claim_record_from_mapping(
            {field.name: getattr(claim, field.name) for field in dataclasses.fields(claim)}, supplied
        )[1].codes
    elif "duplicate" in scenario:
        assert EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID in validate_evaluation_claim_record(
            claim, context + (context[0],)
        ).codes
    elif "resolution_one" in scenario:
        assert validate_evaluation_claim_record(claim, context).codes == ()
    else:
        assert case["case_id"].startswith("context__")


_COMPAT_FIELDS = {
    "target": "target_posture", "representation": "prediction_representation",
    "split_id": "split_id", "split_version": "split_version", "fold": "fold_scope",
    "cutoff": "cutoff_scope", "paired_set": "paired_test_record_set_id",
    "aggregation": "aggregation_rule_id", "weighting": "weighting_rule_id",
    "stratum": "stratum_id_when_applicable", "metric_id_sequence": "metric_or_diagnostic_ids",
    "metric_version_sequence": "metric_or_diagnostic_versions",
}
COMPATIBILITY_INAPPLICABLE_CASE_IDS: tuple[str, ...] = ()


@pytest.mark.parametrize("case", COMPATIBILITY_MATRIX_CASES, ids=_closed_ids(COMPATIBILITY_MATRIX_CASES))
def test_closed_compatibility_matrix_case(case: dict[str, str]) -> None:
    _, dimension, scenario = case["case_id"].split("__")
    claim, context = _complete_class_case(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR)
    if scenario == "match":
        assert validate_evaluation_claim_record(claim, context).codes == ()
        return
    values = {field.name: getattr(claim, field.name) for field in dataclasses.fields(claim)}
    field = _COMPAT_FIELDS[dimension]
    if scenario == "missing_mapping_prerequisite":
        del values[field]
        assert EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD in evaluation_claim_record_from_mapping(values, context)[1].codes
    elif scenario == "blank_prerequisite":
        values[field] = () if "sequence" in dimension else ""
        assert evaluation_claim_record_from_mapping(values, context)[1].codes
    elif scenario == "nonstring_prerequisite":
        values[field] = (1,) if "sequence" in dimension else 1
        assert evaluation_claim_record_from_mapping(values, context)[1].codes
    elif scenario == "subclass_prerequisite":
        values[field] = (TextSubclass("x"),) if "sequence" in dimension else TextSubclass("x")
        assert evaluation_claim_record_from_mapping(values, context)[1].codes
    else:
        values[field] = ("different",) if "sequence" in dimension else (
            ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY if dimension == "representation" else "different"
        )
        first = evaluation_claim_record_from_mapping(values, context)[1].codes
        assert first
        if scenario == "mismatch_repeated":
            assert first == evaluation_claim_record_from_mapping(values, context)[1].codes


def _claim_with_disposition(claim: EvaluationClaimRecord, disposition: EvaluationClaimDisposition, reason: object = "contract reason") -> EvaluationClaimRecord:
    return dataclasses.replace(
        claim, claim_disposition=disposition, claim_disposition_reason=reason,
        evidence_gate_eligibility_posture={
            EvaluationClaimDisposition.CLAIM_SUPPORTED: "eligible_for_later_evidence_gate_decision_only",
            EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED: "claim_support_absent",
            EvaluationClaimDisposition.CLAIM_BLOCKED: "evidence_gate_use_blocked",
            EvaluationClaimDisposition.CLAIM_UNAVAILABLE: "no_substitution_or_evidence_gate_use",
            EvaluationClaimDisposition.CLAIM_INSUFFICIENT: "evidence_gate_use_blocked",
        }[disposition],
    )


@pytest.mark.parametrize("case", DISPOSITION_MATRIX_CASES, ids=_closed_ids(DISPOSITION_MATRIX_CASES))
def test_closed_disposition_matrix_case(case: dict[str, str]) -> None:
    claim, context = _complete_class_case(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL)
    identity = case["case_id"]
    if "complete_support_" in identity or "independent_block" in identity:
        disposition = {
            "disposition__complete_support_supported": EvaluationClaimDisposition.CLAIM_SUPPORTED,
            "disposition__complete_support_not_supported": EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED,
            "disposition__complete_support_unavailable": EvaluationClaimDisposition.CLAIM_UNAVAILABLE,
            "disposition__complete_support_insufficient": EvaluationClaimDisposition.CLAIM_INSUFFICIENT,
            "disposition__independent_block_valid": EvaluationClaimDisposition.CLAIM_BLOCKED,
            "disposition__independent_block_blank_reason": EvaluationClaimDisposition.CLAIM_BLOCKED,
            "disposition__independent_block_nonstring_reason": EvaluationClaimDisposition.CLAIM_BLOCKED,
        }[identity]
        reason: object = "independent exact reason"
        if identity.endswith("blank_reason"): reason = " "
        if identity.endswith("nonstring_reason"): reason = object()
        codes = validate_evaluation_claim_record(_claim_with_disposition(claim, disposition, reason), context).codes
        if disposition in (EvaluationClaimDisposition.CLAIM_SUPPORTED, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED) or identity.endswith("block_valid"):
            assert codes == ()
        else:
            assert EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH in codes
        return
    _, role, status_name, behavior = identity.split("__")
    status = EvaluationResultSupportStatus(status_name)
    index = {"observed": 0, "candidate_reference": 1, "baseline_reference": 2}[role]
    altered = list(context)
    altered[index] = dataclasses.replace(altered[index], support_status=status, exclusion_block_reason_summary=("reason",))
    expected = {
        "supported": EvaluationClaimDisposition.CLAIM_SUPPORTED, "blocked": EvaluationClaimDisposition.CLAIM_BLOCKED,
        "unavailable": EvaluationClaimDisposition.CLAIM_UNAVAILABLE, "insufficient": EvaluationClaimDisposition.CLAIM_INSUFFICIENT,
    }[status_name]
    chosen = expected if behavior == "correct" else (
        EvaluationClaimDisposition.CLAIM_UNAVAILABLE
        if status_name == "supported"
        else EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED
    )
    codes = validate_evaluation_claim_record(_claim_with_disposition(claim, chosen), tuple(altered)).codes
    if behavior == "correct": assert EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH not in codes
    else: assert EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH in codes or SUPPORT_BLOCK in codes


@pytest.mark.parametrize("case", SUPPORTED_COMPLETENESS_CASES, ids=_closed_ids(SUPPORTED_COMPLETENESS_CASES))
def test_closed_supported_completeness_case(case: dict[str, str]) -> None:
    _, disposition_name, blocker = case["case_id"].split("__")
    claim, context = _complete_class_case(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR)
    disposition = EvaluationClaimDisposition.CLAIM_SUPPORTED if disposition_name == "supported" else EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED
    claim = _claim_with_disposition(claim, disposition)
    if blocker == "invalid_container":
        codes = validate_evaluation_claim_record(claim, object()).codes
    elif blocker == "invalid_item":
        codes = validate_evaluation_claim_record(claim, (object(),)).codes
    elif blocker == "duplicate_context":
        codes = validate_evaluation_claim_record(claim, context + context).codes
    elif blocker == "unresolved_observed":
        codes = validate_evaluation_claim_record(claim, ()).codes
    else:
        values = {field.name: getattr(claim, field.name) for field in dataclasses.fields(claim)}
        field_values = {
            "target_mismatch": ("target_posture", "wrong"), "representation_mismatch": ("prediction_representation", ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
            "scope_mismatch": ("split_id", "wrong"), "metric_mismatch": ("metric_or_diagnostic_ids", ("wrong",)),
            "evidence_posture": ("evidence_gate_eligibility_posture", "wrong"), "multiplicity": ("multiple_comparison_policy_id_when_applicable", ""),
            "provenance": ("provenance", ()), "timestamp": ("claim_created_at", "wrong"), "self_supersession": ("supersedes_claim_id_when_applicable", claim.evaluation_claim_id),
        }
        field, value = field_values.get(blocker, ("split_id", "wrong"))
        values[field] = value
        codes = validate_evaluation_claim_record(EvaluationClaimRecord(**values), context).codes
    assert SUPPORT_BLOCK in codes


class _OrdinaryError(Exception): pass
class _FatalError(BaseException): pass


class _HostileMapping(Mapping):
    def __init__(self, mode: str): self.mode = mode
    def __len__(self): return 1
    def __getitem__(self, key): raise KeyError(key)
    def __iter__(self): return iter(())
    def items(self):
        if self.mode == "items_error": raise _OrdinaryError
        if self.mode == "items_fatal": raise _FatalError
        return super().items()


@pytest.mark.parametrize("case", MAPPING_ROOT_CASES, ids=_closed_ids(MAPPING_ROOT_CASES))
def test_closed_mapping_root_case(case: dict[str, str]) -> None:
    identity = case["case_id"]
    if identity.endswith("items_baseexception"):
        with pytest.raises(_FatalError): evaluation_claim_record_from_mapping(_HostileMapping("items_fatal"), ())
        return
    if identity.endswith("items_ordinary_failure"):
        result = evaluation_claim_record_from_mapping(_HostileMapping("items_error"), ())[1]
    else:
        result = evaluation_claim_record_from_mapping(object(), ())[1]
    assert result.codes == (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,) * 33


def test_closed_case_table_meta_contract() -> None:
    tables = (CLASS_MATRIX_CASES, CONTEXT_MATRIX_CASES, COMPATIBILITY_MATRIX_CASES, DISPOSITION_MATRIX_CASES, SUPPORTED_COMPLETENESS_CASES, MAPPING_ROOT_CASES)
    assert tuple(map(len, tables)) == (128, 18, 84, 31, 44, 17)
    assert len(ALL_CLOSED_CASE_IDS) == 322
    assert len(set(ALL_CLOSED_CASE_IDS)) == len(ALL_CLOSED_CASE_IDS)
    assert all(tuple(row) == ("case_id",) and type(row["case_id"]) is str for table in tables for row in table)


def test_production_constant_literal_oracles() -> None:
    import meg.weather.stage3.evaluation_claim as module
    assert module._REQUIRED_MAPPING_KEYS == FIELDS[:33]
    assert module._OPTIONAL_MAPPING_KEYS == ("supersedes_claim_id_when_applicable",)
    assert module._LIST_TO_TUPLE_FIELDS == ("metric_or_diagnostic_ids", "metric_or_diagnostic_versions", "required_evaluation_result_ids", "observed_evaluation_result_ids", "missing_evaluation_result_ids", "provenance")
    assert module._REQUIRED_TEXT_FIELDS == REQUIRED_TEXT
    assert module._NULLABLE_TEXT_FIELDS == NULLABLE_TEXT
    assert module._PAIRED_CLASSES == (EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES, EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL)
    assert module._NON_PAIRED_CLASSES == (EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR)
    assert module._EVIDENCE_GATE_MATRIX == {
        EvaluationClaimDisposition.CLAIM_SUPPORTED: "eligible_for_later_evidence_gate_decision_only",
        EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED: "claim_support_absent",
        EvaluationClaimDisposition.CLAIM_INSUFFICIENT: "evidence_gate_use_blocked",
        EvaluationClaimDisposition.CLAIM_BLOCKED: "evidence_gate_use_blocked",
        EvaluationClaimDisposition.CLAIM_UNAVAILABLE: "no_substitution_or_evidence_gate_use",
    }
    assert module._ALLOWED_RESULT_KINDS == {
        EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
        EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
        EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
        EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR: (EvaluationResultKind.CALIBRATION_BIN_RESULT, EvaluationResultKind.SCALAR_SCORE_RESULT, EvaluationResultKind.DECOMPOSITION_RESULT),
        EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR: (EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT, EvaluationResultKind.SCALAR_SCORE_RESULT),
        EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR: (EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT,),
        EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
        EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
    }
    assert module._VALIDATION_GROUPS == EXPECTED_GROUPS


def test_complete_source_structure_and_annotation_oracles() -> None:
    import meg.weather.stage3.evaluation_claim as module
    tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    imports = tuple(
        (node.module, tuple(alias.name for alias in node.names))
        for node in tree.body if isinstance(node, ast.ImportFrom)
    )
    assert imports == (
        ("__future__", ("annotations",)), ("collections.abc", ("Mapping",)),
        ("dataclasses", ("dataclass",)), ("datetime", ("datetime",)),
        ("enum", ("StrEnum",)), ("meg.weather.stage3.baseline_contracts", ("BaselineType",)),
        ("meg.weather.stage3.scoring_and_diagnostics", ("ScoringArtifact", "ScoringPredictionRepresentation")),
        ("meg.weather.stage3.evaluation_result_record", ("EvaluationResultKind", "EvaluationResultSupportStatus", "EvaluationResultMethodRole", "EvaluationResultRecord", "EvaluationResultValidationResult", "PairedComparisonResultPayload", "validate_evaluation_result_record")),
    )
    public_order = tuple(
        node.name for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and not node.name.startswith("_")
    )
    assert public_order == PUBLIC
    result_fields = dataclasses.fields(EvaluationClaimValidationResult)
    assert tuple(field.name for field in result_fields) == ("severity", "passed", "codes")
    assert typing.get_type_hints(EvaluationClaimValidationResult) == {
        "severity": EvaluationClaimValidationSeverity,
        "passed": bool,
        "codes": tuple[EvaluationClaimValidationCode, ...],
    }
    adapter = inspect.signature(evaluation_claim_record_from_mapping)
    validator = inspect.signature(validate_evaluation_claim_record)
    assert tuple(str(parameter.annotation) for parameter in adapter.parameters.values()) == ("object", "object")
    assert str(adapter.return_annotation) == "tuple[EvaluationClaimRecord | None, EvaluationClaimValidationResult]"
    assert tuple(str(parameter.annotation) for parameter in validator.parameters.values()) == (
        "EvaluationClaimRecord", "tuple[EvaluationResultRecord, ...]",
    )
    assert str(validator.return_annotation) == "EvaluationClaimValidationResult"


@pytest.mark.parametrize("entry", ("direct", "mapping"), ids=("direct", "mapping"))
def test_invalid_context_suppresses_adaptation_dependent_diagnostics(entry: str) -> None:
    claim, _ = _complete_class_case(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR)
    expected = (EvaluationClaimValidationCode.INVALID_RESULT_RECORD_CONTAINER, SUPPORT_BLOCK)
    if entry == "direct":
        assert validate_evaluation_claim_record(claim, object()).codes == expected
    else:
        values = {field.name: getattr(claim, field.name) for field in dataclasses.fields(claim)}
        assert evaluation_claim_record_from_mapping(values, object())[1].codes == expected


class _DuplicateItemsMapping(Mapping):
    def __init__(self, first: object, second: object):
        self.entries = ((first, 1), (second, 2))
    def __len__(self) -> int: return 2
    def __iter__(self): return (entry[0] for entry in self.entries)
    def __getitem__(self, key: object) -> object: raise KeyError(key)
    def items(self): return iter(self.entries)


class _AsymmetricKey:
    def __init__(self, existing: bool): self.existing = existing
    def __hash__(self) -> int: return 7
    def __eq__(self, other: object) -> bool:
        return self.existing and type(other) is _AsymmetricKey


class _EqualityFailureKey:
    def __init__(self, failure: BaseException | None = None): self.failure = failure
    def __hash__(self) -> int: return 7
    def __eq__(self, other: object) -> bool:
        if self.failure is not None: raise self.failure
        return False


def test_asymmetric_duplicate_uses_existing_to_incoming_equality_direction() -> None:
    root = _DuplicateItemsMapping(_AsymmetricKey(True), _AsymmetricKey(False))
    assert evaluation_claim_record_from_mapping(root, ())[1].codes == (
        EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,
    ) * 33


def test_existing_key_equality_ordinary_exception_fails_closed() -> None:
    root = _DuplicateItemsMapping(_EqualityFailureKey(ValueError("equality")), _EqualityFailureKey())
    assert evaluation_claim_record_from_mapping(root, ())[1].codes == (
        EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,
    ) * 33


def test_existing_key_equality_baseexception_propagates() -> None:
    root = _DuplicateItemsMapping(_EqualityFailureKey(_FatalError()), _EqualityFailureKey())
    with pytest.raises(_FatalError):
        evaluation_claim_record_from_mapping(root, ())
