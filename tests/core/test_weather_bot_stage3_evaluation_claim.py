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
    "mapping_root_behavior": ("test_hostile_mapping_roots_and_baseexception",),
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
    "result_context": ("test_context_container_and_item_boundaries",),
    "duplicate_identities": ("test_context_container_and_item_boundaries",),
    "observed_resolution": ("test_valid_observed_claim",),
    "unexpected_context": ("test_valid_paired_claim_and_direct_references",),
    "paired_references": ("test_one_reference_suppresses_both_identity_comparisons",),
    "target_compatibility": ("test_semantic_parity_matrix",),
    "representation_compatibility": ("test_semantic_parity_matrix",),
    "scope_split_id": ("test_each_scope_component_independent_mismatch", "test_compatibility_prerequisite_exact_regressions"),
    "scope_split_version": ("test_each_scope_component_independent_mismatch", "test_compatibility_prerequisite_exact_regressions"),
    "scope_fold": ("test_each_scope_component_independent_mismatch", "test_compatibility_prerequisite_exact_regressions"),
    "scope_cutoff": ("test_each_scope_component_independent_mismatch", "test_compatibility_prerequisite_exact_regressions"),
    "scope_paired_set": ("test_each_scope_component_independent_mismatch", "test_compatibility_prerequisite_exact_regressions"),
    "scope_aggregation": ("test_each_scope_component_independent_mismatch", "test_compatibility_prerequisite_exact_regressions"),
    "scope_weighting": ("test_each_scope_component_independent_mismatch", "test_compatibility_prerequisite_exact_regressions"),
    "scope_stratum": ("test_scope_stratum_none_does_not_coerce_to_empty",),
    "metric_compatibility": ("test_valid_observed_claim",),
    "candidate_identity": ("test_one_reference_suppresses_both_identity_comparisons",),
    "baseline_identity": ("test_wrong_payload_baseline_family_is_classified_per_observed_pair",),
    "class_candidate_climatology": ("test_valid_paired_claim_and_direct_references",),
    "class_candidate_persistence": ("test_claim_class_claim_level_behavior",),
    "class_cross_baseline": ("test_claim_class_claim_level_behavior",),
    "class_binary_calibration": ("test_claim_class_claim_level_behavior",),
    "class_distributional_calibration": ("test_claim_class_claim_level_behavior",),
    "class_ensemble_calibration": ("test_valid_observed_claim",),
    "class_threshold_weighted": ("test_claim_class_claim_level_behavior",),
    "class_stratum_specific": ("test_claim_class_claim_level_behavior",),
    "baseline_requirements": ("test_present_aware_exact_regressions",),
    "cross_baseline_completeness": ("test_claim_class_claim_level_behavior",),
    "stratum_requirements": ("test_scope_stratum_none_does_not_coerce_to_empty",),
    "disposition_precedence": ("test_referenced_status_participates_in_precedence",),
    "supported_completeness": ("test_supported_completeness_includes_late_groups",),
    "evidence_gate_posture": ("test_evidence_gate_matrix",),
    "multiplicity": ("test_present_aware_exact_regressions",),
    "provenance": ("test_provenance_timestamp_supersession_matrix",),
    "timestamp": ("test_provenance_timestamp_supersession_matrix",),
    "supersession": ("test_provenance_timestamp_supersession_matrix",),
    "validation_groups": ("test_source_contract_and_purity",),
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
    assert all(names and set(names) <= test_names for names in COVERAGE_MANIFEST.values())
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


@pytest.mark.parametrize("index,expected", tuple(enumerate(ANNOTATIONS)))
def test_each_record_resolved_annotation_literal(index: int, expected: str) -> None:
    hints = typing.get_type_hints(EvaluationClaimRecord)
    field = dataclasses.fields(EvaluationClaimRecord)[index]
    assert hints[field.name] == ANNOTATION_TYPES[index]
    assert field.type == expected


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
