from __future__ import annotations

import ast
from collections.abc import Mapping
import dataclasses
from enum import StrEnum
import inspect
from pathlib import Path
import typing
from collections.abc import Callable

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
    'imports': ('test_source_contract_and_purity',),
    'public_api': ('test_public_surface_enums_and_frozen_records_are_exact',),
    'public_source_order': ('test_source_contract_and_purity',),
    'claim_class_enum': ('test_claim_class_literal_members',),
    'disposition_enum': ('test_public_surface_enums_and_frozen_records_are_exact',),
    'severity_enum': ('test_validation_result_invariant_preserves_repetition',),
    'validation_codes': ('test_each_validation_code_literal',),
    'record_structure': ('test_each_record_field_literal',),
    'validation_result_structure': ('test_validation_result_invariant_preserves_repetition',),
    'signatures': ('test_signatures_are_frozen',),
    'mapping_keys': ('test_each_required_mapping_key_is_independently_required',),
    'mapping_root_behavior': ('mapping_root__asymmetric_equal_hash_duplicate', 'mapping_root__equality_baseexception'),
    'mapping_adaptation': ('test_mapping_adapts_only_approved_values_without_mutation',),
    'required_text': ('test_each_required_text_rejects_each_invalid_exact_type',),
    'nullable_text': ('test_each_nullable_text_rejects_invalid_nonnull',),
    'fixed_target': ('test_present_aware_exact_regressions',),
    'metric_ids': ('test_tuple_contract_cases',),
    'metric_versions': ('test_repeated_metric_versions_are_accepted',),
    'required_result_ids': ('test_tuple_contract_cases',),
    'observed_result_ids': ('test_tuple_contract_cases',),
    'missing_result_ids': ('test_tuple_contract_cases',),
    'partition': ('test_tuple_contract_cases',),
    'result_context': ('context__invalid_container_direct', 'context__invalid_items_two'),
    'duplicate_identities': ('context__duplicate_once', 'context__duplicate_twice'),
    'observed_resolution': ('context__resolution_zero', 'context__resolution_multiple'),
    'unexpected_context': ('context__unexpected_one', 'context__unexpected_multiple'),
    'paired_references': ('context__paired_missing_candidate', 'context__paired_missing_both'),
    'target_compatibility': ('compat__target__mismatch_single', 'compat__target__mismatch_repeated'),
    'representation_compatibility': ('compat__representation__mismatch_single', 'compat__representation__mismatch_repeated'),
    'scope_split_id': ('compat__split_id__mismatch_single', 'compat__split_id__mismatch_repeated'),
    'scope_split_version': ('compat__split_version__mismatch_single', 'compat__split_version__mismatch_repeated'),
    'scope_fold': ('compat__fold__mismatch_single', 'compat__fold__mismatch_repeated'),
    'scope_cutoff': ('compat__cutoff__mismatch_single', 'compat__cutoff__mismatch_repeated'),
    'scope_paired_set': ('compat__paired_set__mismatch_single', 'compat__paired_set__mismatch_repeated'),
    'scope_aggregation': ('compat__aggregation__mismatch_single', 'compat__aggregation__mismatch_repeated'),
    'scope_weighting': ('compat__weighting__mismatch_single', 'compat__weighting__mismatch_repeated'),
    'scope_stratum': ('compat__stratum__mismatch_single', 'compat__stratum__mismatch_repeated'),
    'metric_compatibility': ('compat__metric_id_sequence__mismatch_single', 'compat__metric_version_sequence__mismatch_repeated'),
    'candidate_identity': ('candidate_vs_climatology__candidate_id', 'completeness__supported__candidate_identity'),
    'baseline_identity': ('candidate_vs_climatology__baseline_id', 'completeness__supported__baseline_identity'),
    'class_candidate_climatology': ('candidate_vs_climatology__valid_single', 'candidate_vs_climatology__repeated_disallowed_kind'),
    'class_candidate_persistence': ('candidate_vs_persistence__valid_single', 'candidate_vs_persistence__repeated_disallowed_kind'),
    'class_cross_baseline': ('cross_baseline__valid_complete', 'cross_baseline__cross_baseline_single_occurrence'),
    'class_binary_calibration': ('binary_calibration__valid_all_three', 'binary_calibration__scalar_only'),
    'class_distributional_calibration': ('distributional_calibration__valid_diagnostic_scalar', 'distributional_calibration__diagnostic_only'),
    'class_ensemble_calibration': ('ensemble_calibration__valid_single', 'ensemble_calibration__repeated_disallowed_kind'),
    'class_threshold_weighted': ('threshold_weighted__valid_climatology', 'threshold_weighted__repeated_wrong_artifact'),
    'class_stratum_specific': ('stratum_specific__valid_climatology', 'stratum_specific__repeated_stratum_mismatch'),
    'baseline_requirements': ('test_present_aware_exact_regressions',),
    'cross_baseline_completeness': ('test_each_claim_class_complete_evidence', 'test_claim_class_claim_level_behavior'),
    'stratum_requirements': ('test_scope_stratum_none_does_not_coerce_to_empty',),
    'disposition_precedence': ('disposition__candidate_reference__blocked__correct', 'disposition__complete_support_unavailable'),
    'supported_completeness': ('completeness__supported__invalid_container', 'completeness__not_supported__self_supersession'),
    'evidence_gate_posture': ('test_evidence_gate_matrix',),
    'multiplicity': ('test_present_aware_exact_regressions',),
    'provenance': ('test_provenance_timestamp_supersession_matrix',),
    'timestamp': ('test_provenance_timestamp_supersession_matrix',),
    'supersession': ('test_provenance_timestamp_supersession_matrix',),
    'validation_groups': ('test_exact_validation_group_literal_oracle',),
    'purity': ('test_source_contract_and_purity',),
    'caller_preservation': ('test_mapping_adapts_only_approved_values_without_mutation',),
    'determinism': ('test_direct_validation_rejects_tuple_subclasses_and_is_deterministic',),
    'mutation_resistance': ('test_mutation_resistance_map',),
    'observed_tuple_prerequisite_suppression': ('test_observed_tuple_prerequisite_exact_codes',),
    'evidence_posture_exact_type': ('test_evidence_posture_requires_exact_builtin_text',),
    'supported_completeness_evidence_posture': ('test_evidence_posture_requires_exact_builtin_text',),
    'candidate_claim_identity_prerequisites': ('test_candidate_claim_identity_prerequisites',),
    'baseline_claim_identity_prerequisites': ('test_baseline_claim_identity_prerequisites',),
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
    reason = ("status reason",)
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
    closed_ids = {case.case_id for case in ALL_CLOSED_CASES}
    assert len(COVERAGE_MANIFEST) == 68
    assert all(names and set(names) <= test_names | closed_ids for names in COVERAGE_MANIFEST.values())
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


class EqualityKey:
    def __init__(self, result: object) -> None:
        self.result = result

    def __hash__(self) -> int:
        return 7

    def __eq__(self, other: object) -> object:
        if isinstance(self.result, BaseException):
            raise self.result
        return self.result


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


def test_duplicate_equality_uses_existing_to_incoming_direction() -> None:
    existing = EqualityKey(True)
    incoming = EqualityKey(False)
    record, result = evaluation_claim_record_from_mapping(
        ItemsMapping(((existing, 1), (incoming, 2))), (),
    )
    assert record is None
    assert result.codes == (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,) * 33


def test_existing_key_ordinary_equality_failure_fails_closed() -> None:
    root = ItemsMapping(((EqualityKey(RuntimeError("equality")), 1), (EqualityKey(False), 2)))
    assert evaluation_claim_record_from_mapping(root, ())[1].codes == (
        EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,
    ) * 33


def test_existing_key_baseexception_equality_failure_propagates() -> None:
    root = ItemsMapping(((EqualityKey(KeyboardInterrupt()), 1), (EqualityKey(False), 2)))
    with pytest.raises(KeyboardInterrupt):
        evaluation_claim_record_from_mapping(root, ())


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
        EvaluationClaimValidationCode.RESULT_TARGET_MISMATCH,
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
            EvaluationClaimValidationCode.INVALID_FIXED_POSTURE,
            EvaluationClaimValidationCode.RESULT_TARGET_MISMATCH,
            SUPPORT_BLOCK,
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


@dataclasses.dataclass(frozen=True)
class ClosedCase:
    """One independently executable row in a closed behavioral matrix."""

    case_id: str
    build: Callable[[], tuple[EvaluationClaimRecord, object]]
    expected_codes: tuple[EvaluationClaimValidationCode, ...]


@dataclasses.dataclass(frozen=True)
class MappingAdapterContext:
    mapping: object


@dataclasses.dataclass(frozen=True)
class MappingRootCase:
    case_id: str
    build: Callable[[], object]
    expected_codes: tuple[EvaluationClaimValidationCode, ...] | None
    expected_exception: type[BaseException] | None = None


def _closed_result(fixture_index: int, result_id: str, **changes: object) -> EvaluationResultRecord:
    values = dict(RESULT_FIXTURES[fixture_index])
    values.update(evaluation_result_id=result_id, **changes)
    return EvaluationResultRecord(**values)


def _closed_nonpaired(
    claim_class: EvaluationClaimClass,
    fixtures: tuple[int, ...],
    representation: ScoringPredictionRepresentation,
    *,
    claim_changes: Mapping[str, object] | None = None,
    result_changes: Mapping[int, Mapping[str, object]] | None = None,
) -> Callable[[], tuple[EvaluationClaimRecord, object]]:
    frozen_claim = dict(claim_changes or {})
    frozen_results = {index: dict(change) for index, change in (result_changes or {}).items()}

    def build() -> tuple[EvaluationClaimRecord, object]:
        results = tuple(
            _closed_result(fixture, f"closed-result-{index}", **frozen_results.get(index, {}))
            for index, fixture in enumerate(fixtures)
        )
        return _claim_for_results(
            claim_class, results, prediction_representation=representation, **frozen_claim,
        ), results

    return build


def _closed_paired(
    claim_class: EvaluationClaimClass,
    family: BaselineType,
    *,
    count: int = 1,
    artifact: ScoringArtifact = ScoringArtifact.BRIER_SCORE,
    representation: ScoringPredictionRepresentation = ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
    claim_representation: ScoringPredictionRepresentation | None = None,
    claim_changes: Mapping[str, object] | None = None,
    pair_changes: Mapping[int, Mapping[str, object]] | None = None,
    candidate_changes: Mapping[int, Mapping[str, object]] | None = None,
    baseline_changes: Mapping[int, Mapping[str, object]] | None = None,
    omit_candidates: tuple[int, ...] = (),
    omit_baselines: tuple[int, ...] = (),
) -> Callable[[], tuple[EvaluationClaimRecord, object]]:
    claim_updates = dict(claim_changes or {})
    pair_updates = {index: dict(change) for index, change in (pair_changes or {}).items()}
    candidate_updates = {index: dict(change) for index, change in (candidate_changes or {}).items()}
    baseline_updates = {index: dict(change) for index, change in (baseline_changes or {}).items()}

    def build() -> tuple[EvaluationClaimRecord, object]:
        context: list[EvaluationResultRecord] = []
        for index in range(count):
            pair, candidate, baseline = _paired_bundle(
                family, prefix=f"closed-{index}", artifact=artifact,
                representation=representation, stratum="all",
            )
            pair = dataclasses.replace(pair, **pair_updates.get(index, {}))
            candidate = dataclasses.replace(candidate, **candidate_updates.get(index, {}))
            baseline = dataclasses.replace(baseline, **baseline_updates.get(index, {}))
            context.append(pair)
            if index not in omit_candidates:
                context.append(candidate)
            if index not in omit_baselines:
                context.append(baseline)
        method = "climatology" if family is BaselineType.CLIMATOLOGY else "persistence"
        values: dict[str, object] = {
            "baseline_type_when_applicable": family,
            "baseline_method_id_when_applicable": method,
            "baseline_method_version_when_applicable": "v1",
            "prediction_representation": claim_representation or representation,
            "stratum_id_when_applicable": "all" if claim_class is EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL else None,
        }
        values.update(claim_updates)
        return _claim_for_results(claim_class, tuple(context), **values), tuple(context)

    return build


def _closed_paired_scalars(
    claim_class: EvaluationClaimClass, family: BaselineType, count: int = 1,
) -> Callable[[], tuple[EvaluationClaimRecord, object]]:
    def build() -> tuple[EvaluationClaimRecord, object]:
        results = tuple(_closed_result(0, f"closed-scalar-{index}") for index in range(count))
        method = "climatology" if family is BaselineType.CLIMATOLOGY else "persistence"
        return _claim_for_results(
            claim_class, results, baseline_type_when_applicable=family,
            baseline_method_id_when_applicable=method,
            baseline_method_version_when_applicable="v1",
            prediction_representation=ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        ), results
    return build


def _closed_cross(
    families: tuple[BaselineType, ...] = (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE),
    *,
    claim_changes: Mapping[str, object] | None = None,
    candidate_changes: Mapping[int, Mapping[str, object]] | None = None,
    baseline_changes: Mapping[int, Mapping[str, object]] | None = None,
) -> Callable[[], tuple[EvaluationClaimRecord, object]]:
    claim_updates = dict(claim_changes or {})
    candidate_updates = {index: dict(change) for index, change in (candidate_changes or {}).items()}
    baseline_updates = {index: dict(change) for index, change in (baseline_changes or {}).items()}

    def build() -> tuple[EvaluationClaimRecord, object]:
        context: list[EvaluationResultRecord] = []
        for index, family in enumerate(families):
            pair, candidate, baseline = _paired_bundle(family, prefix=f"cross-{index}")
            candidate = dataclasses.replace(candidate, **candidate_updates.get(index, {}))
            baseline = dataclasses.replace(baseline, **baseline_updates.get(index, {}))
            context.extend((pair, candidate, baseline))
        values: dict[str, object] = {
            "baseline_type_when_applicable": None,
            "baseline_method_id_when_applicable": None,
            "baseline_method_version_when_applicable": None,
            "prediction_representation": ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        }
        values.update(claim_updates)
        return _claim_for_results(
            EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES,
            tuple(context), **values,
        ), tuple(context)
    return build


def _closed_cross_nonpaired() -> tuple[EvaluationClaimRecord, object]:
    result = _closed_result(0, "cross-scalar")
    return _claim_for_results(
        EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES,
        (result,), baseline_type_when_applicable=None,
        baseline_method_id_when_applicable=None,
        baseline_method_version_when_applicable=None,
        prediction_representation=ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
        multiple_comparison_policy_id_when_applicable="holm",
    ), (result,)


REQUIRED_CLASS_CASE_IDS = (
    'candidate_vs_climatology__valid_single',
    'candidate_vs_climatology__valid_multiple',
    'candidate_vs_climatology__disallowed_scalar',
    'candidate_vs_climatology__wrong_representation',
    'candidate_vs_climatology__candidate_role',
    'candidate_vs_climatology__candidate_id',
    'candidate_vs_climatology__candidate_version',
    'candidate_vs_climatology__baseline_role',
    'candidate_vs_climatology__baseline_id',
    'candidate_vs_climatology__baseline_version',
    'candidate_vs_climatology__payload_persistence',
    'candidate_vs_climatology__missing_candidate',
    'candidate_vs_climatology__missing_baseline',
    'candidate_vs_climatology__missing_both',
    'candidate_vs_climatology__repeated_candidate_identity',
    'candidate_vs_climatology__repeated_baseline_identity',
    'candidate_vs_climatology__repeated_disallowed_kind',
    'candidate_vs_persistence__valid_single',
    'candidate_vs_persistence__valid_multiple',
    'candidate_vs_persistence__disallowed_scalar',
    'candidate_vs_persistence__wrong_representation',
    'candidate_vs_persistence__candidate_role',
    'candidate_vs_persistence__candidate_id',
    'candidate_vs_persistence__candidate_version',
    'candidate_vs_persistence__baseline_role',
    'candidate_vs_persistence__baseline_id',
    'candidate_vs_persistence__baseline_version',
    'candidate_vs_persistence__payload_climatology',
    'candidate_vs_persistence__missing_candidate',
    'candidate_vs_persistence__missing_baseline',
    'candidate_vs_persistence__missing_both',
    'candidate_vs_persistence__repeated_candidate_identity',
    'candidate_vs_persistence__repeated_baseline_identity',
    'candidate_vs_persistence__repeated_disallowed_kind',
    'cross_baseline__valid_complete',
    'cross_baseline__missing_climatology',
    'cross_baseline__missing_persistence',
    'cross_baseline__climatology_role',
    'cross_baseline__persistence_role',
    'cross_baseline__candidate_role',
    'cross_baseline__candidate_id',
    'cross_baseline__candidate_version',
    'cross_baseline__disallowed_nonpaired',
    'cross_baseline__claim_baseline_type_nonnull',
    'cross_baseline__claim_baseline_id_nonnull',
    'cross_baseline__claim_baseline_version_nonnull',
    'cross_baseline__multiplicity_missing',
    'cross_baseline__repeated_candidate_identity',
    'cross_baseline__cross_baseline_single_occurrence',
    'binary_calibration__valid_calibration_scalar',
    'binary_calibration__valid_calibration_decomposition',
    'binary_calibration__valid_all_three',
    'binary_calibration__calibration_only',
    'binary_calibration__scalar_only',
    'binary_calibration__decomposition_only',
    'binary_calibration__scalar_decomposition_without_calibration',
    'binary_calibration__disallowed_distribution',
    'binary_calibration__disallowed_ensemble',
    'binary_calibration__disallowed_paired',
    'binary_calibration__wrong_representation',
    'binary_calibration__candidate_role',
    'binary_calibration__candidate_id',
    'binary_calibration__candidate_version',
    'binary_calibration__repeated_disallowed_kind',
    'binary_calibration__repeated_candidate_identity',
    'distributional_calibration__valid_diagnostic_scalar',
    'distributional_calibration__diagnostic_only',
    'distributional_calibration__scalar_only',
    'distributional_calibration__disallowed_calibration',
    'distributional_calibration__disallowed_decomposition',
    'distributional_calibration__disallowed_ensemble',
    'distributional_calibration__disallowed_paired',
    'distributional_calibration__wrong_representation',
    'distributional_calibration__candidate_role',
    'distributional_calibration__candidate_id',
    'distributional_calibration__candidate_version',
    'distributional_calibration__repeated_disallowed_kind',
    'distributional_calibration__repeated_candidate_identity',
    'ensemble_calibration__valid_single',
    'ensemble_calibration__valid_multiple',
    'ensemble_calibration__disallowed_scalar',
    'ensemble_calibration__disallowed_calibration',
    'ensemble_calibration__disallowed_decomposition',
    'ensemble_calibration__disallowed_distribution',
    'ensemble_calibration__disallowed_paired',
    'ensemble_calibration__wrong_representation',
    'ensemble_calibration__candidate_role',
    'ensemble_calibration__candidate_id',
    'ensemble_calibration__candidate_version',
    'ensemble_calibration__repeated_disallowed_kind',
    'ensemble_calibration__repeated_candidate_identity',
    'threshold_weighted__valid_climatology',
    'threshold_weighted__valid_persistence',
    'threshold_weighted__wrong_artifact',
    'threshold_weighted__wrong_representation',
    'threshold_weighted__wrong_payload_family',
    'threshold_weighted__candidate_role',
    'threshold_weighted__candidate_id',
    'threshold_weighted__candidate_version',
    'threshold_weighted__baseline_role',
    'threshold_weighted__baseline_id',
    'threshold_weighted__baseline_version',
    'threshold_weighted__missing_candidate',
    'threshold_weighted__missing_baseline',
    'threshold_weighted__missing_both',
    'threshold_weighted__disallowed_scalar',
    'threshold_weighted__disallowed_distribution',
    'threshold_weighted__repeated_wrong_artifact',
    'stratum_specific__valid_climatology',
    'stratum_specific__valid_persistence',
    'stratum_specific__claim_stratum_none',
    'stratum_specific__claim_stratum_blank',
    'stratum_specific__claim_stratum_nonstring',
    'stratum_specific__claim_stratum_subclass',
    'stratum_specific__observed_stratum',
    'stratum_specific__candidate_stratum',
    'stratum_specific__baseline_stratum',
    'stratum_specific__wrong_payload_family',
    'stratum_specific__candidate_role',
    'stratum_specific__candidate_id',
    'stratum_specific__candidate_version',
    'stratum_specific__baseline_role',
    'stratum_specific__baseline_id',
    'stratum_specific__baseline_version',
    'stratum_specific__missing_candidate',
    'stratum_specific__missing_baseline',
    'stratum_specific__missing_both',
    'stratum_specific__repeated_stratum_mismatch',
)

CLASS_MATRIX_CASES = (
    ClosedCase(
        'candidate_vs_climatology__valid_single',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY),
        (),
    ),
    ClosedCase(
        'candidate_vs_climatology__valid_multiple',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, count=2),
        (),
    ),
    ClosedCase(
        'candidate_vs_climatology__disallowed_scalar',
        _closed_paired_scalars(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__wrong_representation',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, claim_representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__candidate_role',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, candidate_changes={0: {"method_role": EvaluationResultMethodRole.CLIMATOLOGY_BASELINE}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__candidate_id',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, candidate_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__candidate_version',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, candidate_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__baseline_role',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, baseline_changes={0: {"method_role": EvaluationResultMethodRole.CANDIDATE}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__baseline_id',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, baseline_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__baseline_version',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, baseline_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__payload_persistence',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, pair_changes={0: {"result_payload": PairedComparisonResultPayload("closed-0-candidate", "closed-0-baseline", BaselineType.PERSISTENCE, "candidate_minus_baseline_lower_is_better", -0.1, "exact_common_test_record_set_required")}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__missing_candidate',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, omit_candidates=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__missing_baseline',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, omit_baselines=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__missing_both',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, omit_candidates=(0,), omit_baselines=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__repeated_candidate_identity',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, count=2, candidate_changes={0: {"method_id": "wrong"}, 1: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__repeated_baseline_identity',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, count=2, baseline_changes={0: {"method_id": "wrong"}, 1: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_climatology__repeated_disallowed_kind',
        _closed_paired_scalars(EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, 2),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__valid_single',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE),
        (),
    ),
    ClosedCase(
        'candidate_vs_persistence__valid_multiple',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, count=2),
        (),
    ),
    ClosedCase(
        'candidate_vs_persistence__disallowed_scalar',
        _closed_paired_scalars(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__wrong_representation',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, claim_representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__candidate_role',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, candidate_changes={0: {"method_role": EvaluationResultMethodRole.CLIMATOLOGY_BASELINE}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__candidate_id',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, candidate_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__candidate_version',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, candidate_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__baseline_role',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, baseline_changes={0: {"method_role": EvaluationResultMethodRole.CANDIDATE}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__baseline_id',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, baseline_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__baseline_version',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, baseline_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__payload_climatology',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, pair_changes={0: {"result_payload": PairedComparisonResultPayload("closed-0-candidate", "closed-0-baseline", BaselineType.CLIMATOLOGY, "candidate_minus_baseline_lower_is_better", -0.1, "exact_common_test_record_set_required")}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__missing_candidate',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, omit_candidates=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__missing_baseline',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, omit_baselines=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__missing_both',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, omit_candidates=(0,), omit_baselines=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__repeated_candidate_identity',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, count=2, candidate_changes={0: {"method_id": "wrong"}, 1: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__repeated_baseline_identity',
        _closed_paired(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, count=2, baseline_changes={0: {"method_id": "wrong"}, 1: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'candidate_vs_persistence__repeated_disallowed_kind',
        _closed_paired_scalars(EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, BaselineType.PERSISTENCE, 2),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__valid_complete',
        _closed_cross(),
        (),
    ),
    ClosedCase(
        'cross_baseline__missing_climatology',
        _closed_cross((BaselineType.PERSISTENCE,)),
        (
            EvaluationClaimValidationCode.CROSS_BASELINE_INCOMPLETE,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__missing_persistence',
        _closed_cross((BaselineType.CLIMATOLOGY,)),
        (
            EvaluationClaimValidationCode.CROSS_BASELINE_INCOMPLETE,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__climatology_role',
        _closed_cross(baseline_changes={0: {"method_role": EvaluationResultMethodRole.CANDIDATE}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__persistence_role',
        _closed_cross(baseline_changes={1: {"method_role": EvaluationResultMethodRole.CANDIDATE}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__candidate_role',
        _closed_cross(candidate_changes={0: {"method_role": EvaluationResultMethodRole.CLIMATOLOGY_BASELINE}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__candidate_id',
        _closed_cross(candidate_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__candidate_version',
        _closed_cross(candidate_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__disallowed_nonpaired',
        _closed_cross_nonpaired,
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__claim_baseline_type_nonnull',
        _closed_cross(claim_changes={"baseline_type_when_applicable": BaselineType.CLIMATOLOGY}),
        (
            EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__claim_baseline_id_nonnull',
        _closed_cross(claim_changes={"baseline_method_id_when_applicable": "climatology"}),
        (
            EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__claim_baseline_version_nonnull',
        _closed_cross(claim_changes={"baseline_method_version_when_applicable": "v1"}),
        (
            EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__multiplicity_missing',
        _closed_cross(claim_changes={"multiple_comparison_policy_id_when_applicable": None}),
        (
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
            EvaluationClaimValidationCode.INVALID_MULTIPLE_COMPARISON_POSTURE,
        ),
    ),
    ClosedCase(
        'cross_baseline__repeated_candidate_identity',
        _closed_cross(candidate_changes={0: {"method_id": "wrong"}, 1: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'cross_baseline__cross_baseline_single_occurrence',
        _closed_cross((BaselineType.CLIMATOLOGY, BaselineType.CLIMATOLOGY)),
        (
            EvaluationClaimValidationCode.CROSS_BASELINE_INCOMPLETE,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__valid_calibration_scalar',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (1, 0), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (),
    ),
    ClosedCase(
        'binary_calibration__valid_calibration_decomposition',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (1, 2), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (),
    ),
    ClosedCase(
        'binary_calibration__valid_all_three',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (1, 0, 2), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (),
    ),
    ClosedCase(
        'binary_calibration__calibration_only',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (1,), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__scalar_only',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (0,), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__decomposition_only',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (2,), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__scalar_decomposition_without_calibration',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (0, 2), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__disallowed_distribution',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (3,), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__disallowed_ensemble',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (4,), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__disallowed_paired',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (5,), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__wrong_representation',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (1, 0), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__candidate_role',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (1, 0), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, result_changes={0: {"method_role": EvaluationResultMethodRole.CLIMATOLOGY_BASELINE}}),
        (
            EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__candidate_id',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (1, 0), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, result_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__candidate_version',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (1, 0), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, result_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__repeated_disallowed_kind',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (3, 3), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'binary_calibration__repeated_candidate_identity',
        _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (1, 0), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY, result_changes={0: {"method_id": "wrong"}, 1: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__valid_diagnostic_scalar',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (3, 0), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, result_changes={1: {"artifact_id": ScoringArtifact.CRPS, "prediction_representation": ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION}}),
        (),
    ),
    ClosedCase(
        'distributional_calibration__diagnostic_only',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (3,), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__scalar_only',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (0,), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, result_changes={0: {"artifact_id": ScoringArtifact.CRPS, "prediction_representation": ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION}}),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__disallowed_calibration',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (1,), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__disallowed_decomposition',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (2,), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__disallowed_ensemble',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (4,), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__disallowed_paired',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (5,), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__wrong_representation',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (3, 0), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__candidate_role',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (3, 0), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, result_changes={0: {"method_role": EvaluationResultMethodRole.CLIMATOLOGY_BASELINE}}),
        (
            EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__candidate_id',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (3, 0), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, result_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__candidate_version',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (3, 0), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, result_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__repeated_disallowed_kind',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (1, 1), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'distributional_calibration__repeated_candidate_identity',
        _closed_nonpaired(EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, (3, 0), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, result_changes={0: {"method_id": "wrong"}, 1: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'ensemble_calibration__valid_single',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (4,), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE),
        (),
    ),
    ClosedCase(
        'ensemble_calibration__valid_multiple',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (4, 4), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE),
        (),
    ),
    ClosedCase(
        'ensemble_calibration__disallowed_scalar',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (0,), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'ensemble_calibration__disallowed_calibration',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (1,), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'ensemble_calibration__disallowed_decomposition',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (2,), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'ensemble_calibration__disallowed_distribution',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (3,), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'ensemble_calibration__disallowed_paired',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (5,), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'ensemble_calibration__wrong_representation',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (4,), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'ensemble_calibration__candidate_role',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (4,), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE, result_changes={0: {"method_role": EvaluationResultMethodRole.CLIMATOLOGY_BASELINE}}),
        (
            EvaluationClaimValidationCode.INVALID_METRIC_IDENTITY_TUPLE,
            EvaluationClaimValidationCode.INVALID_METRIC_IDENTITY_TUPLE,
            EvaluationClaimValidationCode.INVALID_REQUIRED_RESULT_IDS,
            EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'ensemble_calibration__candidate_id',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (4,), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE, result_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'ensemble_calibration__candidate_version',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (4,), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE, result_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'ensemble_calibration__repeated_disallowed_kind',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (0, 0), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'ensemble_calibration__repeated_candidate_identity',
        _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (4, 4), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE, result_changes={0: {"method_id": "wrong"}, 1: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__valid_climatology',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (),
    ),
    ClosedCase(
        'threshold_weighted__valid_persistence',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.PERSISTENCE, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (),
    ),
    ClosedCase(
        'threshold_weighted__wrong_artifact',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__wrong_representation',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, claim_representation=ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__wrong_payload_family',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, pair_changes={0: {"result_payload": PairedComparisonResultPayload("closed-0-candidate", "closed-0-baseline", BaselineType.PERSISTENCE, "candidate_minus_baseline_lower_is_better", -0.1, "exact_common_test_record_set_required")}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__candidate_role',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, candidate_changes={0: {"method_role": EvaluationResultMethodRole.CLIMATOLOGY_BASELINE}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__candidate_id',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, candidate_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__candidate_version',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, candidate_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__baseline_role',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, baseline_changes={0: {"method_role": EvaluationResultMethodRole.CANDIDATE}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__baseline_id',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, baseline_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__baseline_version',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, baseline_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__missing_candidate',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, omit_candidates=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__missing_baseline',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, omit_baselines=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__missing_both',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, artifact=ScoringArtifact.THRESHOLD_WEIGHTED_CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, omit_candidates=(0,), omit_baselines=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__disallowed_scalar',
        _closed_nonpaired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, (0,), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, claim_changes={ "baseline_type_when_applicable": BaselineType.CLIMATOLOGY, "baseline_method_id_when_applicable": "climatology", "baseline_method_version_when_applicable": "v1" }),
        (
            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__disallowed_distribution',
        _closed_nonpaired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, (3,), ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION, claim_changes={ "baseline_type_when_applicable": BaselineType.CLIMATOLOGY, "baseline_method_id_when_applicable": "climatology", "baseline_method_version_when_applicable": "v1" }),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'threshold_weighted__repeated_wrong_artifact',
        _closed_paired(EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, BaselineType.CLIMATOLOGY, count=2, artifact=ScoringArtifact.CRPS, representation=ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION),
        (
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__valid_climatology',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY),
        (),
    ),
    ClosedCase(
        'stratum_specific__valid_persistence',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.PERSISTENCE),
        (),
    ),
    ClosedCase(
        'stratum_specific__claim_stratum_none',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, claim_changes={"stratum_id_when_applicable": None}),
        (
            EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__claim_stratum_blank',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, claim_changes={"stratum_id_when_applicable": " "}),
        (
            EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
            EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__claim_stratum_nonstring',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, claim_changes={"stratum_id_when_applicable": 7}),
        (
            EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
            EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__claim_stratum_subclass',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, claim_changes={"stratum_id_when_applicable": TextSubclass("all")}),
        (
            EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
            EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__observed_stratum',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, pair_changes={0: {"stratum_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
            EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__candidate_stratum',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, candidate_changes={0: {"stratum_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
            EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__baseline_stratum',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, baseline_changes={0: {"stratum_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
            EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__wrong_payload_family',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, pair_changes={0: {"result_payload": PairedComparisonResultPayload("closed-0-candidate", "closed-0-baseline", BaselineType.PERSISTENCE, "candidate_minus_baseline_lower_is_better", -0.1, "exact_common_test_record_set_required")}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__candidate_role',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, candidate_changes={0: {"method_role": EvaluationResultMethodRole.CLIMATOLOGY_BASELINE}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__candidate_id',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, candidate_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__candidate_version',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, candidate_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__baseline_role',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, baseline_changes={0: {"method_role": EvaluationResultMethodRole.CANDIDATE}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__baseline_id',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, baseline_changes={0: {"method_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__baseline_version',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, baseline_changes={0: {"method_version": "wrong"}}),
        (
            EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__missing_candidate',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, omit_candidates=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__missing_baseline',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, omit_baselines=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__missing_both',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, omit_candidates=(0,), omit_baselines=(0,)),
        (
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
    ClosedCase(
        'stratum_specific__repeated_stratum_mismatch',
        _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, count=2, pair_changes={0: {"stratum_id": "wrong"}, 1: {"stratum_id": "wrong"}}),
        (
            EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
            EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
            EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH,
            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
        ),
    ),
)

def _build_complete_ensemble() -> tuple[EvaluationClaimRecord, object]:
    return _complete_class_case(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR)


def _build_invalid_direct_context() -> tuple[EvaluationClaimRecord, object]:
    claim, _ = _build_complete_ensemble()
    return claim, object()


def _build_complete_unavailable() -> tuple[EvaluationClaimRecord, object]:
    claim, context = _build_complete_ensemble()
    return dataclasses.replace(claim, claim_disposition=EvaluationClaimDisposition.CLAIM_UNAVAILABLE, evidence_gate_eligibility_posture="no_substitution_or_evidence_gate_use"), context


def _build_complete_insufficient() -> tuple[EvaluationClaimRecord, object]:
    claim, context = _build_complete_ensemble()
    return dataclasses.replace(claim, claim_disposition=EvaluationClaimDisposition.CLAIM_INSUFFICIENT, evidence_gate_eligibility_posture="evidence_gate_use_blocked"), context


def _build_complete_blank_block() -> tuple[EvaluationClaimRecord, object]:
    claim, context = _build_complete_ensemble()
    return dataclasses.replace(claim, claim_disposition=EvaluationClaimDisposition.CLAIM_BLOCKED, claim_disposition_reason=" ", evidence_gate_eligibility_posture="evidence_gate_use_blocked"), context


def _build_complete_independent_block() -> tuple[EvaluationClaimRecord, object]:
    claim, context = _build_complete_ensemble()
    return dataclasses.replace(claim, claim_disposition=EvaluationClaimDisposition.CLAIM_BLOCKED, claim_disposition_reason="independent contract block", evidence_gate_eligibility_posture="evidence_gate_use_blocked"), context


def _claim_mapping(record: EvaluationClaimRecord) -> dict[str, object]:
    return {field.name: getattr(record, field.name) for field in dataclasses.fields(record)}


def _closed_ensemble_context(
    context_factory: Callable[[EvaluationResultRecord], object],
    *,
    claim_changes: Mapping[str, object] | None = None,
    adapter: bool = False,
) -> Callable[[], tuple[EvaluationClaimRecord | MappingAdapterContext, object]]:
    updates = dict(claim_changes or {})

    def build() -> tuple[EvaluationClaimRecord | MappingAdapterContext, object]:
        claim, context = _build_complete_ensemble()
        claim = dataclasses.replace(claim, **updates)
        subject: EvaluationClaimRecord | MappingAdapterContext = (
            MappingAdapterContext(_claim_mapping(claim)) if adapter else claim
        )
        return subject, context_factory(context[0])

    return build


def _closed_paired_context(
    *, count: int = 1, omit_candidates: tuple[int, ...] = (),
    omit_baselines: tuple[int, ...] = (), claim_changes: Mapping[str, object] | None = None,
) -> Callable[[], tuple[EvaluationClaimRecord, object]]:
    return _closed_paired(
        EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL,
        BaselineType.CLIMATOLOGY, count=count, omit_candidates=omit_candidates,
        omit_baselines=omit_baselines, claim_changes=claim_changes,
    )


class ContextIterable:
    def __iter__(self):
        return iter(())


class ContextTupleSubclass(tuple):
    pass


REQUIRED_CONTEXT_CASE_IDS = (
    "context__invalid_items_two",
    "context__duplicate_once",
    "context__duplicate_twice",
    "context__resolution_zero",
    "context__resolution_one",
    "context__resolution_multiple",
    "context__unexpected_one",
    "context__unexpected_multiple",
    "context__paired_missing_candidate",
    "context__paired_missing_baseline",
    "context__paired_missing_both",
    "context__paired_two_pairs_candidate_then_baseline",
    "context__identity_suppressed_candidate_missing",
    "context__identity_suppressed_baseline_missing",
    "context__invalid_container_direct",
    "context__invalid_container_mapping_iterable",
    "context__invalid_container_mapping_tuple_subclass",
    "context__invalid_container_mapping_mixed_list",
)


CONTEXT_MATRIX_CASES = (
    ClosedCase("context__invalid_items_two", _closed_ensemble_context(lambda result: (object(), object())), (
                                                                                                                EvaluationClaimValidationCode.INVALID_RESULT_RECORD,
                                                                                                                EvaluationClaimValidationCode.INVALID_RESULT_RECORD,
                                                                                                                EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
                                                                                                                EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                            )),
    ClosedCase("context__duplicate_once", _closed_ensemble_context(lambda result: (result, dataclasses.replace(result, evaluation_result_id="extra"), dataclasses.replace(result, evaluation_result_id="extra"))), (
                                                                                                                                                                                                                       EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID,
                                                                                                                                                                                                                       EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
                                                                                                                                                                                                                       EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
                                                                                                                                                                                                                       EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                   )),
    ClosedCase("context__duplicate_twice", _closed_ensemble_context(lambda result: (result, dataclasses.replace(result, evaluation_result_id="extra"), dataclasses.replace(result, evaluation_result_id="extra"), dataclasses.replace(result, evaluation_result_id="extra"))), (
                                                                                                                                                                                                                                                                                   EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID,
                                                                                                                                                                                                                                                                                   EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID,
                                                                                                                                                                                                                                                                                   EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
                                                                                                                                                                                                                                                                                   EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
                                                                                                                                                                                                                                                                                   EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
                                                                                                                                                                                                                                                                                   EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                               )),
    ClosedCase("context__resolution_zero", _closed_ensemble_context(lambda result: ()), (
                                                                                            EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
                                                                                            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                        )),
    ClosedCase("context__resolution_one", _closed_ensemble_context(lambda result: (result,)), ()),
    ClosedCase("context__resolution_multiple", _closed_ensemble_context(lambda result: (result, result)), (
                                                                                                              EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID,
                                                                                                              EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
                                                                                                              EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                          )),
    ClosedCase("context__unexpected_one", _closed_ensemble_context(lambda result: (result, dataclasses.replace(result, evaluation_result_id="extra-1"))), (
                                                                                                                                                              EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
                                                                                                                                                              EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                          )),
    ClosedCase("context__unexpected_multiple", _closed_ensemble_context(lambda result: (result, dataclasses.replace(result, evaluation_result_id="extra-1"), dataclasses.replace(result, evaluation_result_id="extra-2"))), (
                                                                                                                                                                                                                                EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
                                                                                                                                                                                                                                EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
                                                                                                                                                                                                                                EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                            )),
    ClosedCase("context__paired_missing_candidate", _closed_paired_context(omit_candidates=(0,)), (
                                                                                                      EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                      EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                  )),
    ClosedCase("context__paired_missing_baseline", _closed_paired_context(omit_baselines=(0,)), (
                                                                                                    EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                    EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                )),
    ClosedCase("context__paired_missing_both", _closed_paired_context(omit_candidates=(0,), omit_baselines=(0,)), (
                                                                                                                      EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                                      EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                                      EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                  )),
    ClosedCase("context__paired_two_pairs_candidate_then_baseline", _closed_paired_context(count=2, omit_candidates=(0, 1), omit_baselines=(0, 1)), (
                                                                                                                                                        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                                                                        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                                                                        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                                                                        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                                                                        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                    )),
    ClosedCase("context__identity_suppressed_candidate_missing", _closed_paired_context(omit_candidates=(0,), claim_changes={"candidate_method_id": "otherwise-wrong"}), (
                                                                                                                                                                             EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                         )),
    ClosedCase("context__identity_suppressed_baseline_missing", _closed_paired_context(omit_baselines=(0,), claim_changes={"baseline_method_id_when_applicable": "otherwise-wrong"}), (
                                                                                                                                                                                          EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                                                                                                          EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                      )),
    ClosedCase("context__invalid_container_direct", _closed_ensemble_context(lambda result: object()), (
                                                                                                           EvaluationClaimValidationCode.INVALID_RESULT_RECORD_CONTAINER,
                                                                                                           EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                       )),
    ClosedCase("context__invalid_container_mapping_iterable", _closed_ensemble_context(lambda result: ContextIterable(), adapter=True), (
                                                                                                                                            EvaluationClaimValidationCode.INVALID_RESULT_RECORD_CONTAINER,
                                                                                                                                            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                        )),
    ClosedCase("context__invalid_container_mapping_tuple_subclass", _closed_ensemble_context(lambda result: ContextTupleSubclass((result,)), adapter=True), (
                                                                                                                                                                EvaluationClaimValidationCode.INVALID_RESULT_RECORD_CONTAINER,
                                                                                                                                                                EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                            )),
    ClosedCase("context__invalid_container_mapping_mixed_list", _closed_ensemble_context(lambda result: [result, object()], adapter=True), (
                                                                                                                                               EvaluationClaimValidationCode.INVALID_RESULT_RECORD_CONTAINER,
                                                                                                                                               EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                           )),
)


def _compat_mapping_delete(field: str) -> Callable[[dict[str, object]], None]:
    def mutate(values: dict[str, object]) -> None:
        del values[field]
    return mutate


def _compat_mapping_set(field: str, value: object) -> Callable[[dict[str, object]], None]:
    def mutate(values: dict[str, object]) -> None:
        values[field] = value
    return mutate


def _compat_ensemble_builder(
    *,
    count: int = 1,
    claim_changes: Mapping[str, object] | None = None,
    result_changes: Mapping[str, object] | None = None,
    mapping_mutation: Callable[[dict[str, object]], None] | None = None,
) -> Callable[[], tuple[EvaluationClaimRecord | MappingAdapterContext, object]]:
    frozen_claim = dict(claim_changes or {})
    frozen_result = dict(result_changes or {})

    def build() -> tuple[EvaluationClaimRecord | MappingAdapterContext, object]:
        results = tuple(
            _closed_result(4, f"compat-ensemble-{index}", **frozen_result)
            for index in range(count)
        )
        claim_values = dict(frozen_claim)
        claim_representation = claim_values.pop(
            "prediction_representation",
            ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE,
        )
        claim = _claim_for_results(
            EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR,
            results,
            prediction_representation=claim_representation,
            **claim_values,
        )
        if mapping_mutation is None:
            return claim, results
        values = _claim_mapping(claim)
        mapping_mutation(values)
        return MappingAdapterContext(values), results

    return build


def _compat_metric_repeated_builder(
    *, version: bool,
) -> Callable[[], tuple[EvaluationClaimRecord, object]]:
    def build() -> tuple[EvaluationClaimRecord, object]:
        claim, context = _complete_class_case(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR)
        changes = (
            {"metric_or_diagnostic_versions": ("wrong-1", "wrong-2")}
            if version
            else {"metric_or_diagnostic_ids": ("wrong-1", "wrong-2")}
        )
        return dataclasses.replace(claim, **changes), context
    return build


REQUIRED_COMPATIBILITY_CASE_IDS = (
    'compat__target__match',
    'compat__target__mismatch_single',
    'compat__target__mismatch_repeated',
    'compat__target__missing_mapping_prerequisite',
    'compat__target__blank_prerequisite',
    'compat__target__nonstring_prerequisite',
    'compat__target__subclass_prerequisite',
    'compat__representation__match',
    'compat__representation__mismatch_single',
    'compat__representation__mismatch_repeated',
    'compat__representation__missing_mapping_prerequisite',
    'compat__representation__blank_prerequisite',
    'compat__representation__nonstring_prerequisite',
    'compat__representation__subclass_prerequisite',
    'compat__split_id__match',
    'compat__split_id__mismatch_single',
    'compat__split_id__mismatch_repeated',
    'compat__split_id__missing_mapping_prerequisite',
    'compat__split_id__blank_prerequisite',
    'compat__split_id__nonstring_prerequisite',
    'compat__split_id__subclass_prerequisite',
    'compat__split_version__match',
    'compat__split_version__mismatch_single',
    'compat__split_version__mismatch_repeated',
    'compat__split_version__missing_mapping_prerequisite',
    'compat__split_version__blank_prerequisite',
    'compat__split_version__nonstring_prerequisite',
    'compat__split_version__subclass_prerequisite',
    'compat__fold__match',
    'compat__fold__mismatch_single',
    'compat__fold__mismatch_repeated',
    'compat__fold__missing_mapping_prerequisite',
    'compat__fold__blank_prerequisite',
    'compat__fold__nonstring_prerequisite',
    'compat__fold__subclass_prerequisite',
    'compat__cutoff__match',
    'compat__cutoff__mismatch_single',
    'compat__cutoff__mismatch_repeated',
    'compat__cutoff__missing_mapping_prerequisite',
    'compat__cutoff__blank_prerequisite',
    'compat__cutoff__nonstring_prerequisite',
    'compat__cutoff__subclass_prerequisite',
    'compat__paired_set__match',
    'compat__paired_set__mismatch_single',
    'compat__paired_set__mismatch_repeated',
    'compat__paired_set__missing_mapping_prerequisite',
    'compat__paired_set__blank_prerequisite',
    'compat__paired_set__nonstring_prerequisite',
    'compat__paired_set__subclass_prerequisite',
    'compat__aggregation__match',
    'compat__aggregation__mismatch_single',
    'compat__aggregation__mismatch_repeated',
    'compat__aggregation__missing_mapping_prerequisite',
    'compat__aggregation__blank_prerequisite',
    'compat__aggregation__nonstring_prerequisite',
    'compat__aggregation__subclass_prerequisite',
    'compat__weighting__match',
    'compat__weighting__mismatch_single',
    'compat__weighting__mismatch_repeated',
    'compat__weighting__missing_mapping_prerequisite',
    'compat__weighting__blank_prerequisite',
    'compat__weighting__nonstring_prerequisite',
    'compat__weighting__subclass_prerequisite',
    'compat__stratum__match',
    'compat__stratum__mismatch_single',
    'compat__stratum__mismatch_repeated',
    'compat__stratum__missing_mapping_prerequisite',
    'compat__stratum__blank_prerequisite',
    'compat__stratum__nonstring_prerequisite',
    'compat__stratum__subclass_prerequisite',
    'compat__metric_id_sequence__match',
    'compat__metric_id_sequence__mismatch_single',
    'compat__metric_id_sequence__mismatch_repeated',
    'compat__metric_id_sequence__missing_mapping_prerequisite',
    'compat__metric_id_sequence__blank_prerequisite',
    'compat__metric_id_sequence__nonstring_prerequisite',
    'compat__metric_id_sequence__subclass_prerequisite',
    'compat__metric_version_sequence__match',
    'compat__metric_version_sequence__mismatch_single',
    'compat__metric_version_sequence__mismatch_repeated',
    'compat__metric_version_sequence__missing_mapping_prerequisite',
    'compat__metric_version_sequence__blank_prerequisite',
    'compat__metric_version_sequence__nonstring_prerequisite',
    'compat__metric_version_sequence__subclass_prerequisite',
)

COMPATIBILITY_MATRIX_CASES = (
    ClosedCase('compat__target__match', _compat_ensemble_builder(claim_changes={"target_posture": 'venue_defined_settlement_outcome'}, result_changes={"target_posture": 'venue_defined_settlement_outcome'}), ()),
    ClosedCase('compat__target__mismatch_single', _compat_ensemble_builder(claim_changes={"target_posture": 'other-target'}), (
        EvaluationClaimValidationCode.INVALID_FIXED_POSTURE,
        EvaluationClaimValidationCode.RESULT_TARGET_MISMATCH,
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
    )),
    ClosedCase('compat__target__mismatch_repeated', _compat_ensemble_builder(count=2, claim_changes={"target_posture": 'other-target'}), (
        EvaluationClaimValidationCode.INVALID_FIXED_POSTURE,
        EvaluationClaimValidationCode.RESULT_TARGET_MISMATCH,
        EvaluationClaimValidationCode.RESULT_TARGET_MISMATCH,
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
    )),
    ClosedCase('compat__target__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("target_posture")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__target__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("target_posture", '')), (
                                                                                                                                               EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                               EvaluationClaimValidationCode.INVALID_FIXED_POSTURE,
                                                                                                                                               EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                           )),
    ClosedCase('compat__target__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("target_posture", 7)), (
                                                                                                                                                  EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                  EvaluationClaimValidationCode.INVALID_FIXED_POSTURE,
                                                                                                                                                  EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                              )),
    ClosedCase('compat__target__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("target_posture", TextSubclass("venue_defined_settlement_outcome"))), (
                                                                                                                                                                                                EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                                                                EvaluationClaimValidationCode.INVALID_FIXED_POSTURE,
                                                                                                                                                                                                EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                            )),
    ClosedCase('compat__representation__match', _compat_ensemble_builder(
        claim_changes={"prediction_representation": ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE},
        result_changes={"prediction_representation": ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE},
    ), ()),
    ClosedCase('compat__representation__mismatch_single', _compat_ensemble_builder(
        claim_changes={"prediction_representation": ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY},
    ), (
        EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
        EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
    )),
    ClosedCase('compat__representation__mismatch_repeated', _compat_ensemble_builder(
        count=2,
        claim_changes={"prediction_representation": ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY},
    ), (
        EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
        EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
        EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
    )),
    ClosedCase('compat__representation__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("prediction_representation")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__representation__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("prediction_representation", '')), (
                                                                                                                                                                  EvaluationClaimValidationCode.INVALID_PREDICTION_REPRESENTATION,
                                                                                                                                                                  EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                              )),
    ClosedCase('compat__representation__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("prediction_representation", 7)), (
                                                                                                                                                                     EvaluationClaimValidationCode.INVALID_PREDICTION_REPRESENTATION,
                                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                 )),
    ClosedCase('compat__representation__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("prediction_representation", TextSubclass("finite_comparable_ensemble"))), (
                                                                                                                                                                                                             EvaluationClaimValidationCode.INVALID_PREDICTION_REPRESENTATION,
                                                                                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                         )),
    ClosedCase('compat__split_id__match', _compat_ensemble_builder(claim_changes={"split_id": 'split'}, result_changes={"split_id": 'split'}), ()),
    ClosedCase('compat__split_id__mismatch_single', _compat_ensemble_builder(result_changes={"split_id": 'other'}), (
                                                                                                                        EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                    )),
    ClosedCase('compat__split_id__mismatch_repeated', _compat_ensemble_builder(count=2, result_changes={"split_id": 'other'}), (
                                                                                                                                   EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                   EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                   EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                               )),
    ClosedCase('compat__split_id__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("split_id")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__split_id__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("split_id", '')), (
                                                                                                                                           EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                           EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                       )),
    ClosedCase('compat__split_id__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("split_id", 7)), (
                                                                                                                                              EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                              EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                          )),
    ClosedCase('compat__split_id__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("split_id", TextSubclass("split"))), (
                                                                                                                                                                 EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                                 EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                             )),
    ClosedCase('compat__split_version__match', _compat_ensemble_builder(claim_changes={"split_version": 'v1'}, result_changes={"split_version": 'v1'}), ()),
    ClosedCase('compat__split_version__mismatch_single', _compat_ensemble_builder(result_changes={"split_version": 'other'}), (
                                                                                                                                  EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                  EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                              )),
    ClosedCase('compat__split_version__mismatch_repeated', _compat_ensemble_builder(count=2, result_changes={"split_version": 'other'}), (
                                                                                                                                             EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                             EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                         )),
    ClosedCase('compat__split_version__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("split_version")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__split_version__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("split_version", '')), (
                                                                                                                                                     EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                 )),
    ClosedCase('compat__split_version__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("split_version", 7)), (
                                                                                                                                                        EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                    )),
    ClosedCase('compat__split_version__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("split_version", TextSubclass("v1"))), (
                                                                                                                                                                        EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                                        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                    )),
    ClosedCase('compat__fold__match', _compat_ensemble_builder(claim_changes={"fold_scope": 'fold-1'}, result_changes={"fold_id": 'fold-1'}), ()),
    ClosedCase('compat__fold__mismatch_single', _compat_ensemble_builder(result_changes={"fold_id": 'other'}), (
                                                                                                                   EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                   EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                               )),
    ClosedCase('compat__fold__mismatch_repeated', _compat_ensemble_builder(count=2, result_changes={"fold_id": 'other'}), (
                                                                                                                              EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                              EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                              EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                          )),
    ClosedCase('compat__fold__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("fold_scope")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__fold__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("fold_scope", '')), (
                                                                                                                                         EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                         EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                     )),
    ClosedCase('compat__fold__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("fold_scope", 7)), (
                                                                                                                                            EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                        )),
    ClosedCase('compat__fold__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("fold_scope", TextSubclass("fold-1"))), (
                                                                                                                                                                EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                                EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                            )),
    ClosedCase('compat__cutoff__match', _compat_ensemble_builder(claim_changes={"cutoff_scope": '2025-01-01T00:00:00Z'}, result_changes={"cutoff_identity": '2025-01-01T00:00:00Z'}), ()),
    ClosedCase('compat__cutoff__mismatch_single', _compat_ensemble_builder(result_changes={"cutoff_identity": 'other'}), (
                                                                                                                             EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                         )),
    ClosedCase('compat__cutoff__mismatch_repeated', _compat_ensemble_builder(count=2, result_changes={"cutoff_identity": 'other'}), (
                                                                                                                                        EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                        EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                    )),
    ClosedCase('compat__cutoff__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("cutoff_scope")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__cutoff__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("cutoff_scope", '')), (
                                                                                                                                             EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                         )),
    ClosedCase('compat__cutoff__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("cutoff_scope", 7)), (
                                                                                                                                                EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                            )),
    ClosedCase('compat__cutoff__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("cutoff_scope", TextSubclass("2025-01-01T00:00:00Z"))), (
                                                                                                                                                                                  EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                                                  EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                              )),
    ClosedCase('compat__paired_set__match', _compat_ensemble_builder(claim_changes={"paired_test_record_set_id": 'test-set'}, result_changes={"paired_test_record_set_id": 'test-set'}), ()),
    ClosedCase('compat__paired_set__mismatch_single', _compat_ensemble_builder(result_changes={"paired_test_record_set_id": 'other'}), (
                                                                                                                                           EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                           EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                       )),
    ClosedCase('compat__paired_set__mismatch_repeated', _compat_ensemble_builder(count=2, result_changes={"paired_test_record_set_id": 'other'}), (
                                                                                                                                                      EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                                      EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                                      EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                  )),
    ClosedCase('compat__paired_set__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("paired_test_record_set_id")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__paired_set__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("paired_test_record_set_id", '')), (
                                                                                                                                                              EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                              EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                          )),
    ClosedCase('compat__paired_set__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("paired_test_record_set_id", 7)), (
                                                                                                                                                                 EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                                 EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                             )),
    ClosedCase('compat__paired_set__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("paired_test_record_set_id", TextSubclass("test-set"))), (
                                                                                                                                                                                       EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                                                       EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                   )),
    ClosedCase('compat__aggregation__match', _compat_ensemble_builder(claim_changes={"aggregation_rule_id": 'aggregate'}, result_changes={"aggregation_rule_id": 'aggregate'}), ()),
    ClosedCase('compat__aggregation__mismatch_single', _compat_ensemble_builder(result_changes={"aggregation_rule_id": 'other'}), (
                                                                                                                                      EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                      EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                  )),
    ClosedCase('compat__aggregation__mismatch_repeated', _compat_ensemble_builder(count=2, result_changes={"aggregation_rule_id": 'other'}), (
                                                                                                                                                 EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                                 EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                                 EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                             )),
    ClosedCase('compat__aggregation__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("aggregation_rule_id")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__aggregation__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("aggregation_rule_id", '')), (
                                                                                                                                                         EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                         EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                     )),
    ClosedCase('compat__aggregation__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("aggregation_rule_id", 7)), (
                                                                                                                                                            EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                        )),
    ClosedCase('compat__aggregation__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("aggregation_rule_id", TextSubclass("aggregate"))), (
                                                                                                                                                                                   EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                                                   EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                               )),
    ClosedCase('compat__weighting__match', _compat_ensemble_builder(claim_changes={"weighting_rule_id": 'weight'}, result_changes={"weighting_rule_id": 'weight'}), ()),
    ClosedCase('compat__weighting__mismatch_single', _compat_ensemble_builder(result_changes={"weighting_rule_id": 'other'}), (
                                                                                                                                  EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                  EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                              )),
    ClosedCase('compat__weighting__mismatch_repeated', _compat_ensemble_builder(count=2, result_changes={"weighting_rule_id": 'other'}), (
                                                                                                                                             EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                             EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                         )),
    ClosedCase('compat__weighting__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("weighting_rule_id")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__weighting__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("weighting_rule_id", '')), (
                                                                                                                                                     EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                 )),
    ClosedCase('compat__weighting__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("weighting_rule_id", 7)), (
                                                                                                                                                        EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                    )),
    ClosedCase('compat__weighting__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("weighting_rule_id", TextSubclass("weight"))), (
                                                                                                                                                                            EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                                            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                        )),
    ClosedCase('compat__stratum__match', _compat_ensemble_builder(claim_changes={"stratum_id_when_applicable": 'all'}, result_changes={"stratum_id": 'all'}), ()),
    ClosedCase('compat__stratum__mismatch_single', _compat_ensemble_builder(claim_changes={"stratum_id_when_applicable": "all"}, result_changes={"stratum_id": 'other'}), (
        EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
    )),
    ClosedCase('compat__stratum__mismatch_repeated', _compat_ensemble_builder(count=2, claim_changes={"stratum_id_when_applicable": "all"}, result_changes={"stratum_id": 'other'}), (
        EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
        EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
    )),
    ClosedCase('compat__stratum__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("stratum_id_when_applicable")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__stratum__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("stratum_id_when_applicable", '')), (
                                                                                                                                                            EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                        )),
    ClosedCase('compat__stratum__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("stratum_id_when_applicable", 7)), (
                                                                                                                                                               EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                               EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                           )),
    ClosedCase('compat__stratum__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("stratum_id_when_applicable", TextSubclass("all"))), (
                                                                                                                                                                                EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                                                EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                            )),
    ClosedCase('compat__metric_id_sequence__match', _compat_ensemble_builder(claim_changes={"metric_or_diagnostic_ids": ("rank_histogram",)}), ()),
    ClosedCase('compat__metric_id_sequence__mismatch_single', _compat_ensemble_builder(claim_changes={"metric_or_diagnostic_ids": ("wrong",)}), (
                                                                                                                                                    EvaluationClaimValidationCode.RESULT_METRIC_MISMATCH,
                                                                                                                                                    EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                )),
    ClosedCase('compat__metric_id_sequence__mismatch_repeated', _compat_metric_repeated_builder(version=False), (
                                                                                                                    EvaluationClaimValidationCode.RESULT_METRIC_MISMATCH,
                                                                                                                    EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                )),
    ClosedCase('compat__metric_id_sequence__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("metric_or_diagnostic_ids")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__metric_id_sequence__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("metric_or_diagnostic_ids", ("",))), (
                                                                                                                                                                        EvaluationClaimValidationCode.INVALID_METRIC_IDENTITY_TUPLE,
                                                                                                                                                                        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                    )),
    ClosedCase('compat__metric_id_sequence__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("metric_or_diagnostic_ids", (7,))), (
                                                                                                                                                                           EvaluationClaimValidationCode.INVALID_METRIC_IDENTITY_TUPLE,
                                                                                                                                                                           EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                       )),
    ClosedCase('compat__metric_id_sequence__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("metric_or_diagnostic_ids", (TextSubclass("rank_histogram"),))), (
                                                                                                                                                                                                       EvaluationClaimValidationCode.INVALID_METRIC_IDENTITY_TUPLE,
                                                                                                                                                                                                       EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                   )),
    ClosedCase('compat__metric_version_sequence__match', _compat_ensemble_builder(claim_changes={"metric_or_diagnostic_versions": ("v1",)}), ()),
    ClosedCase('compat__metric_version_sequence__mismatch_single', _compat_ensemble_builder(claim_changes={"metric_or_diagnostic_versions": ("wrong",)}), (
                                                                                                                                                              EvaluationClaimValidationCode.RESULT_METRIC_MISMATCH,
                                                                                                                                                              EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                          )),
    ClosedCase('compat__metric_version_sequence__mismatch_repeated', _compat_metric_repeated_builder(version=True), (
                                                                                                                        EvaluationClaimValidationCode.RESULT_METRIC_MISMATCH,
                                                                                                                        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                    )),
    ClosedCase('compat__metric_version_sequence__missing_mapping_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_delete("metric_or_diagnostic_versions")), (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,)),
    ClosedCase('compat__metric_version_sequence__blank_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("metric_or_diagnostic_versions", ("",))), (
                                                                                                                                                                                  EvaluationClaimValidationCode.INVALID_METRIC_IDENTITY_TUPLE,
                                                                                                                                                                                  EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                              )),
    ClosedCase('compat__metric_version_sequence__nonstring_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("metric_or_diagnostic_versions", (7,))), (
                                                                                                                                                                                     EvaluationClaimValidationCode.INVALID_METRIC_IDENTITY_TUPLE,
                                                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                 )),
    ClosedCase('compat__metric_version_sequence__subclass_prerequisite', _compat_ensemble_builder(mapping_mutation=_compat_mapping_set("metric_or_diagnostic_versions", (TextSubclass("v1"),))), (
                                                                                                                                                                                                     EvaluationClaimValidationCode.INVALID_METRIC_IDENTITY_TUPLE,
                                                                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                 )),
)
def _disposition_posture(disposition: EvaluationClaimDisposition) -> str:
    return {
        EvaluationClaimDisposition.CLAIM_SUPPORTED: "eligible_for_later_evidence_gate_decision_only",
        EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED: "claim_support_absent",
        EvaluationClaimDisposition.CLAIM_BLOCKED: "evidence_gate_use_blocked",
        EvaluationClaimDisposition.CLAIM_UNAVAILABLE: "no_substitution_or_evidence_gate_use",
        EvaluationClaimDisposition.CLAIM_INSUFFICIENT: "evidence_gate_use_blocked",
    }[disposition]


def _disposition_role_builder(
    role_index: int,
    status: EvaluationResultSupportStatus,
    caller: EvaluationClaimDisposition,
) -> Callable[[], tuple[EvaluationClaimRecord, object]]:
    def build() -> tuple[EvaluationClaimRecord, object]:
        claim, context = _closed_paired(
            EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL,
            BaselineType.CLIMATOLOGY,
        )()
        altered = list(context)
        altered[role_index] = dataclasses.replace(
            altered[role_index], support_status=status,
            exclusion_block_reason_summary={
                EvaluationResultSupportStatus.SUPPORTED: (),
                EvaluationResultSupportStatus.BLOCKED: ("contract reason",),
                EvaluationResultSupportStatus.UNAVAILABLE: ("contract reason",),
                EvaluationResultSupportStatus.INSUFFICIENT: ("contract reason",),
            }[status],
        )
        return dataclasses.replace(
            claim, claim_disposition=caller,
            claim_disposition_reason="contract reason",
            evidence_gate_eligibility_posture=_disposition_posture(caller),
        ), tuple(altered)
    return build


def _complete_disposition_builder(
    disposition: EvaluationClaimDisposition,
    reason: object = "contract reason",
) -> Callable[[], tuple[EvaluationClaimRecord, object]]:
    def build() -> tuple[EvaluationClaimRecord, object]:
        claim, context = _build_complete_ensemble()
        return dataclasses.replace(
            claim, claim_disposition=disposition,
            claim_disposition_reason=reason,
            evidence_gate_eligibility_posture=_disposition_posture(disposition),
        ), context
    return build


def _completion_builder(
    base: Callable[[], tuple[EvaluationClaimRecord, object]],
    disposition: EvaluationClaimDisposition,
    *,
    claim_changes: Mapping[str, object] | None = None,
    context_change: Callable[[object], object] | None = None,
) -> Callable[[], tuple[EvaluationClaimRecord, object]]:
    frozen_changes = dict(claim_changes or {})

    def build() -> tuple[EvaluationClaimRecord, object]:
        claim, context = base()
        claim = dataclasses.replace(
            claim, claim_disposition=disposition,
            evidence_gate_eligibility_posture=_disposition_posture(disposition),
        )
        claim = dataclasses.replace(claim, **frozen_changes)
        return claim, context_change(context) if context_change is not None else context
    return build


def _completion_ensemble() -> tuple[EvaluationClaimRecord, object]:
    return _build_complete_ensemble()


def _completion_paired(**kwargs: object) -> Callable[[], tuple[EvaluationClaimRecord, object]]:
    return _closed_paired(
        EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL,
        BaselineType.CLIMATOLOGY, **kwargs,
    )


REQUIRED_DISPOSITION_CASE_IDS = (
    'disposition__observed__supported__correct',
    'disposition__observed__supported__incorrect',
    'disposition__observed__blocked__correct',
    'disposition__observed__blocked__incorrect',
    'disposition__observed__unavailable__correct',
    'disposition__observed__unavailable__incorrect',
    'disposition__observed__insufficient__correct',
    'disposition__observed__insufficient__incorrect',
    'disposition__candidate_reference__supported__correct',
    'disposition__candidate_reference__supported__incorrect',
    'disposition__candidate_reference__blocked__correct',
    'disposition__candidate_reference__blocked__incorrect',
    'disposition__candidate_reference__unavailable__correct',
    'disposition__candidate_reference__unavailable__incorrect',
    'disposition__candidate_reference__insufficient__correct',
    'disposition__candidate_reference__insufficient__incorrect',
    'disposition__baseline_reference__supported__correct',
    'disposition__baseline_reference__supported__incorrect',
    'disposition__baseline_reference__blocked__correct',
    'disposition__baseline_reference__blocked__incorrect',
    'disposition__baseline_reference__unavailable__correct',
    'disposition__baseline_reference__unavailable__incorrect',
    'disposition__baseline_reference__insufficient__correct',
    'disposition__baseline_reference__insufficient__incorrect',
    'disposition__independent_block_valid',
    'disposition__independent_block_blank_reason',
    'disposition__independent_block_nonstring_reason',
    'disposition__complete_support_supported',
    'disposition__complete_support_not_supported',
    'disposition__complete_support_unavailable',
    'disposition__complete_support_insufficient',
)

DISPOSITION_MATRIX_CASES = (
    ClosedCase('disposition__observed__supported__correct', _disposition_role_builder(0, EvaluationResultSupportStatus.SUPPORTED, EvaluationClaimDisposition.CLAIM_SUPPORTED), ()),
    ClosedCase('disposition__observed__supported__incorrect', _disposition_role_builder(0, EvaluationResultSupportStatus.SUPPORTED, EvaluationClaimDisposition.CLAIM_UNAVAILABLE), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__observed__blocked__correct', _disposition_role_builder(0, EvaluationResultSupportStatus.BLOCKED, EvaluationClaimDisposition.CLAIM_BLOCKED), ()),
    ClosedCase('disposition__observed__blocked__incorrect', _disposition_role_builder(0, EvaluationResultSupportStatus.BLOCKED, EvaluationClaimDisposition.CLAIM_INSUFFICIENT), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__observed__unavailable__correct', _disposition_role_builder(0, EvaluationResultSupportStatus.UNAVAILABLE, EvaluationClaimDisposition.CLAIM_UNAVAILABLE), ()),
    ClosedCase('disposition__observed__unavailable__incorrect', _disposition_role_builder(0, EvaluationResultSupportStatus.UNAVAILABLE, EvaluationClaimDisposition.CLAIM_INSUFFICIENT), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__observed__insufficient__correct', _disposition_role_builder(0, EvaluationResultSupportStatus.INSUFFICIENT, EvaluationClaimDisposition.CLAIM_INSUFFICIENT), ()),
    ClosedCase('disposition__observed__insufficient__incorrect', _disposition_role_builder(0, EvaluationResultSupportStatus.INSUFFICIENT, EvaluationClaimDisposition.CLAIM_UNAVAILABLE), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__candidate_reference__supported__correct', _disposition_role_builder(1, EvaluationResultSupportStatus.SUPPORTED, EvaluationClaimDisposition.CLAIM_SUPPORTED), ()),
    ClosedCase('disposition__candidate_reference__supported__incorrect', _disposition_role_builder(1, EvaluationResultSupportStatus.SUPPORTED, EvaluationClaimDisposition.CLAIM_UNAVAILABLE), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__candidate_reference__blocked__correct', _disposition_role_builder(1, EvaluationResultSupportStatus.BLOCKED, EvaluationClaimDisposition.CLAIM_BLOCKED), ()),
    ClosedCase('disposition__candidate_reference__blocked__incorrect', _disposition_role_builder(1, EvaluationResultSupportStatus.BLOCKED, EvaluationClaimDisposition.CLAIM_INSUFFICIENT), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__candidate_reference__unavailable__correct', _disposition_role_builder(1, EvaluationResultSupportStatus.UNAVAILABLE, EvaluationClaimDisposition.CLAIM_UNAVAILABLE), ()),
    ClosedCase('disposition__candidate_reference__unavailable__incorrect', _disposition_role_builder(1, EvaluationResultSupportStatus.UNAVAILABLE, EvaluationClaimDisposition.CLAIM_INSUFFICIENT), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__candidate_reference__insufficient__correct', _disposition_role_builder(1, EvaluationResultSupportStatus.INSUFFICIENT, EvaluationClaimDisposition.CLAIM_INSUFFICIENT), ()),
    ClosedCase('disposition__candidate_reference__insufficient__incorrect', _disposition_role_builder(1, EvaluationResultSupportStatus.INSUFFICIENT, EvaluationClaimDisposition.CLAIM_UNAVAILABLE), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__baseline_reference__supported__correct', _disposition_role_builder(2, EvaluationResultSupportStatus.SUPPORTED, EvaluationClaimDisposition.CLAIM_SUPPORTED), ()),
    ClosedCase('disposition__baseline_reference__supported__incorrect', _disposition_role_builder(2, EvaluationResultSupportStatus.SUPPORTED, EvaluationClaimDisposition.CLAIM_UNAVAILABLE), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__baseline_reference__blocked__correct', _disposition_role_builder(2, EvaluationResultSupportStatus.BLOCKED, EvaluationClaimDisposition.CLAIM_BLOCKED), ()),
    ClosedCase('disposition__baseline_reference__blocked__incorrect', _disposition_role_builder(2, EvaluationResultSupportStatus.BLOCKED, EvaluationClaimDisposition.CLAIM_INSUFFICIENT), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__baseline_reference__unavailable__correct', _disposition_role_builder(2, EvaluationResultSupportStatus.UNAVAILABLE, EvaluationClaimDisposition.CLAIM_UNAVAILABLE), ()),
    ClosedCase('disposition__baseline_reference__unavailable__incorrect', _disposition_role_builder(2, EvaluationResultSupportStatus.UNAVAILABLE, EvaluationClaimDisposition.CLAIM_INSUFFICIENT), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__baseline_reference__insufficient__correct', _disposition_role_builder(2, EvaluationResultSupportStatus.INSUFFICIENT, EvaluationClaimDisposition.CLAIM_INSUFFICIENT), ()),
    ClosedCase('disposition__baseline_reference__insufficient__incorrect', _disposition_role_builder(2, EvaluationResultSupportStatus.INSUFFICIENT, EvaluationClaimDisposition.CLAIM_UNAVAILABLE), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__independent_block_valid', _complete_disposition_builder(EvaluationClaimDisposition.CLAIM_BLOCKED, "independent block"), ()),
    ClosedCase('disposition__independent_block_blank_reason', _complete_disposition_builder(EvaluationClaimDisposition.CLAIM_BLOCKED, " "), (
                                                                                                                                                EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,
                                                                                                                                            )),
    ClosedCase('disposition__independent_block_nonstring_reason', _complete_disposition_builder(EvaluationClaimDisposition.CLAIM_BLOCKED, 7), (
                                                                                                                                                  EvaluationClaimValidationCode.BLANK_REQUIRED_TEXT,
                                                                                                                                                  EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,
                                                                                                                                              )),
    ClosedCase('disposition__complete_support_supported', _complete_disposition_builder(EvaluationClaimDisposition.CLAIM_SUPPORTED), ()),
    ClosedCase('disposition__complete_support_not_supported', _complete_disposition_builder(EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED), ()),
    ClosedCase('disposition__complete_support_unavailable', _complete_disposition_builder(EvaluationClaimDisposition.CLAIM_UNAVAILABLE), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
    ClosedCase('disposition__complete_support_insufficient', _complete_disposition_builder(EvaluationClaimDisposition.CLAIM_INSUFFICIENT), (EvaluationClaimValidationCode.DISPOSITION_PRECEDENCE_MISMATCH,)),
)

REQUIRED_SUPPORTED_COMPLETENESS_CASE_IDS = (
    'completeness__supported__invalid_container',
    'completeness__supported__invalid_item',
    'completeness__supported__duplicate_context',
    'completeness__supported__unresolved_observed',
    'completeness__supported__unexpected_context',
    'completeness__supported__missing_paired_reference',
    'completeness__supported__target_mismatch',
    'completeness__supported__representation_mismatch',
    'completeness__supported__scope_mismatch',
    'completeness__supported__metric_mismatch',
    'completeness__supported__candidate_identity',
    'completeness__supported__baseline_identity',
    'completeness__supported__disallowed_kind',
    'completeness__supported__missing_family',
    'completeness__supported__baseline_requirement',
    'completeness__supported__cross_baseline_incomplete',
    'completeness__supported__stratum_requirement',
    'completeness__supported__evidence_posture',
    'completeness__supported__multiplicity',
    'completeness__supported__provenance',
    'completeness__supported__timestamp',
    'completeness__supported__self_supersession',
    'completeness__not_supported__invalid_container',
    'completeness__not_supported__invalid_item',
    'completeness__not_supported__duplicate_context',
    'completeness__not_supported__unresolved_observed',
    'completeness__not_supported__unexpected_context',
    'completeness__not_supported__missing_paired_reference',
    'completeness__not_supported__target_mismatch',
    'completeness__not_supported__representation_mismatch',
    'completeness__not_supported__scope_mismatch',
    'completeness__not_supported__metric_mismatch',
    'completeness__not_supported__candidate_identity',
    'completeness__not_supported__baseline_identity',
    'completeness__not_supported__disallowed_kind',
    'completeness__not_supported__missing_family',
    'completeness__not_supported__baseline_requirement',
    'completeness__not_supported__cross_baseline_incomplete',
    'completeness__not_supported__stratum_requirement',
    'completeness__not_supported__evidence_posture',
    'completeness__not_supported__multiplicity',
    'completeness__not_supported__provenance',
    'completeness__not_supported__timestamp',
    'completeness__not_supported__self_supersession',
)

SUPPORTED_COMPLETENESS_CASES = (
    ClosedCase('completeness__supported__invalid_container', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=lambda context: object()), (
                                                                                                                                                                                                                     EvaluationClaimValidationCode.INVALID_RESULT_RECORD_CONTAINER,
                                                                                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                 )),
    ClosedCase('completeness__supported__invalid_item', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=lambda context: (object(),)), (
                                                                                                                                                                                                                   EvaluationClaimValidationCode.INVALID_RESULT_RECORD,
                                                                                                                                                                                                                   EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
                                                                                                                                                                                                                   EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                               )),
    ClosedCase('completeness__supported__duplicate_context', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=lambda context: (context[0], context[0])), (
                                                                                                                                                                                                                                     EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID,
                                                                                                                                                                                                                                     EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
                                                                                                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                 )),
    ClosedCase('completeness__supported__unresolved_observed', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=lambda context: ()), (
                                                                                                                                                                                                                 EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
                                                                                                                                                                                                                 EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                             )),
    ClosedCase('completeness__supported__unexpected_context', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=lambda context: (context[0], dataclasses.replace(context[0], evaluation_result_id="extra"))), (
                                                                                                                                                                                                                                                                                         EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
                                                                                                                                                                                                                                                                                         EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                                     )),
    ClosedCase('completeness__supported__missing_paired_reference', _completion_builder(_completion_paired(omit_candidates=(0,)), EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                            EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                                                                                                                                            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                        )),
    ClosedCase('completeness__supported__target_mismatch', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes={"target_posture": "other-target"}, context_change=None), (
                                                                                                                                                                                                                             EvaluationClaimValidationCode.INVALID_FIXED_POSTURE,
                                                                                                                                                                                                                             EvaluationClaimValidationCode.RESULT_TARGET_MISMATCH,
                                                                                                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                         )),
    ClosedCase('completeness__supported__representation_mismatch', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes={"prediction_representation": ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY}, context_change=None), (
                                                                                                                                                                                                                                                                                            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
                                                                                                                                                                                                                                                                                            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
                                                                                                                                                                                                                                                                                            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                                        )),
    ClosedCase('completeness__supported__scope_mismatch', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes={"split_id": "other-split"}, context_change=None), (
                                                                                                                                                                                                                     EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                 )),
    ClosedCase('completeness__supported__metric_mismatch', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes={"metric_or_diagnostic_ids": ("wrong",)}, context_change=None), (
                                                                                                                                                                                                                                   EvaluationClaimValidationCode.RESULT_METRIC_MISMATCH,
                                                                                                                                                                                                                                   EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                               )),
    ClosedCase('completeness__supported__candidate_identity', _completion_builder(_completion_paired(candidate_changes={0: {"method_id": "wrong"}}), EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                               EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
                                                                                                                                                                                                                                               EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                           )),
    ClosedCase('completeness__supported__baseline_identity', _completion_builder(_completion_paired(baseline_changes={0: {"method_id": "wrong"}}), EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                             EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
                                                                                                                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                         )),
    ClosedCase('completeness__supported__disallowed_kind', _completion_builder(lambda: _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (0,), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE)(), EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                                                                                                            EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
                                                                                                                                                                                                                                                                                                                            EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
                                                                                                                                                                                                                                                                                                                            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                                                                        )),
    ClosedCase('completeness__supported__missing_family', _completion_builder(lambda: _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (1,), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY)(), EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                                                                                                         EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
                                                                                                                                                                                                                                                                                                                         EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                                                                     )),
    ClosedCase('completeness__supported__baseline_requirement', _completion_builder(_completion_paired(claim_changes={"baseline_type_when_applicable": BaselineType.PERSISTENCE}), EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                                                             EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,
                                                                                                                                                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                         )),
    ClosedCase('completeness__supported__cross_baseline_incomplete', _completion_builder(lambda: _closed_cross((BaselineType.CLIMATOLOGY,))(), EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                         EvaluationClaimValidationCode.CROSS_BASELINE_INCOMPLETE,
                                                                                                                                                                                                                                         EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                     )),
    ClosedCase('completeness__supported__stratum_requirement', _completion_builder(lambda: _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, claim_changes={"stratum_id_when_applicable": None})(), EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                                                                                                                             EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH,
                                                                                                                                                                                                                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                                                                                         )),
    ClosedCase('completeness__supported__evidence_posture', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes={"evidence_gate_eligibility_posture": "wrong"}, context_change=None), (
                                                                                                                                                                                                                                          EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                          EvaluationClaimValidationCode.INVALID_EVIDENCE_GATE_POSTURE,
                                                                                                                                                                                                                                      )),
    ClosedCase('completeness__supported__multiplicity', _completion_builder(lambda: _closed_cross()(), EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes={"multiple_comparison_policy_id_when_applicable": None}, context_change=None), (
                                                                                                                                                                                                                                                    EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                    EvaluationClaimValidationCode.INVALID_MULTIPLE_COMPARISON_POSTURE,
                                                                                                                                                                                                                                                )),
    ClosedCase('completeness__supported__provenance', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes={"provenance": ()}, context_change=None), (
                                                                                                                                                                                                        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                        EvaluationClaimValidationCode.EMPTY_PROVENANCE,
                                                                                                                                                                                                    )),
    ClosedCase('completeness__supported__timestamp', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes={"claim_created_at": "invalid"}, context_change=None), (
                                                                                                                                                                                                                    EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                    EvaluationClaimValidationCode.INVALID_CLAIM_CREATED_AT,
                                                                                                                                                                                                                )),
    ClosedCase('completeness__supported__self_supersession', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_SUPPORTED, claim_changes={"supersedes_claim_id_when_applicable": "claim-1"}, context_change=None), (
                                                                                                                                                                                                                                               EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                               EvaluationClaimValidationCode.SELF_SUPERSESSION,
                                                                                                                                                                                                                                           )),
    ClosedCase('completeness__not_supported__invalid_container', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=lambda context: object()), (
                                                                                                                                                                                                                             EvaluationClaimValidationCode.INVALID_RESULT_RECORD_CONTAINER,
                                                                                                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                         )),
    ClosedCase('completeness__not_supported__invalid_item', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=lambda context: (object(),)), (
                                                                                                                                                                                                                           EvaluationClaimValidationCode.INVALID_RESULT_RECORD,
                                                                                                                                                                                                                           EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
                                                                                                                                                                                                                           EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                       )),
    ClosedCase('completeness__not_supported__duplicate_context', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=lambda context: (context[0], context[0])), (
                                                                                                                                                                                                                                             EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID,
                                                                                                                                                                                                                                             EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
                                                                                                                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                         )),
    ClosedCase('completeness__not_supported__unresolved_observed', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=lambda context: ()), (
                                                                                                                                                                                                                         EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
                                                                                                                                                                                                                         EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                     )),
    ClosedCase('completeness__not_supported__unexpected_context', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=lambda context: (context[0], dataclasses.replace(context[0], evaluation_result_id="extra"))), (
                                                                                                                                                                                                                                                                                                 EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT,
                                                                                                                                                                                                                                                                                                 EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                                             )),
    ClosedCase('completeness__not_supported__missing_paired_reference', _completion_builder(_completion_paired(omit_candidates=(0,)), EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                    EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
                                                                                                                                                                                                                                    EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                )),
    ClosedCase('completeness__not_supported__target_mismatch', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes={"target_posture": "other-target"}, context_change=None), (
                                                                                                                                                                                                                                     EvaluationClaimValidationCode.INVALID_FIXED_POSTURE,
                                                                                                                                                                                                                                     EvaluationClaimValidationCode.RESULT_TARGET_MISMATCH,
                                                                                                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                 )),
    ClosedCase('completeness__not_supported__representation_mismatch', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes={"prediction_representation": ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY}, context_change=None), (
                                                                                                                                                                                                                                                                                                    EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
                                                                                                                                                                                                                                                                                                    EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
                                                                                                                                                                                                                                                                                                    EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                                                )),
    ClosedCase('completeness__not_supported__scope_mismatch', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes={"split_id": "other-split"}, context_change=None), (
                                                                                                                                                                                                                             EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
                                                                                                                                                                                                                             EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                         )),
    ClosedCase('completeness__not_supported__metric_mismatch', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes={"metric_or_diagnostic_ids": ("wrong",)}, context_change=None), (
                                                                                                                                                                                                                                           EvaluationClaimValidationCode.RESULT_METRIC_MISMATCH,
                                                                                                                                                                                                                                           EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                       )),
    ClosedCase('completeness__not_supported__candidate_identity', _completion_builder(_completion_paired(candidate_changes={0: {"method_id": "wrong"}}), EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                                       EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
                                                                                                                                                                                                                                                       EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                   )),
    ClosedCase('completeness__not_supported__baseline_identity', _completion_builder(_completion_paired(baseline_changes={0: {"method_id": "wrong"}}), EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                                     EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
                                                                                                                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                 )),
    ClosedCase('completeness__not_supported__disallowed_kind', _completion_builder(lambda: _closed_nonpaired(EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR, (0,), ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE)(), EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                                                                                                                    EvaluationClaimValidationCode.RESULT_REPRESENTATION_MISMATCH,
                                                                                                                                                                                                                                                                                                                                    EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
                                                                                                                                                                                                                                                                                                                                    EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                                                                                )),
    ClosedCase('completeness__not_supported__missing_family', _completion_builder(lambda: _closed_nonpaired(EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, (1,), ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY)(), EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                                                                                                                 EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
                                                                                                                                                                                                                                                                                                                                 EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                                                                             )),
    ClosedCase('completeness__not_supported__baseline_requirement', _completion_builder(_completion_paired(claim_changes={"baseline_type_when_applicable": BaselineType.PERSISTENCE}), EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                                                                     EvaluationClaimValidationCode.BASELINE_REQUIREMENT_MISMATCH,
                                                                                                                                                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                                 )),
    ClosedCase('completeness__not_supported__cross_baseline_incomplete', _completion_builder(lambda: _closed_cross((BaselineType.CLIMATOLOGY,))(), EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                                 EvaluationClaimValidationCode.CROSS_BASELINE_INCOMPLETE,
                                                                                                                                                                                                                                                 EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                             )),
    ClosedCase('completeness__not_supported__stratum_requirement', _completion_builder(lambda: _closed_paired(EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, BaselineType.CLIMATOLOGY, claim_changes={"stratum_id_when_applicable": None})(), EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes=None, context_change=None), (
                                                                                                                                                                                                                                                                                                                                                     EvaluationClaimValidationCode.STRATUM_REQUIREMENT_MISMATCH,
                                                                                                                                                                                                                                                                                                                                                     EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                                                                                                                 )),
    ClosedCase('completeness__not_supported__evidence_posture', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes={"evidence_gate_eligibility_posture": "wrong"}, context_change=None), (
                                                                                                                                                                                                                                                  EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                  EvaluationClaimValidationCode.INVALID_EVIDENCE_GATE_POSTURE,
                                                                                                                                                                                                                                              )),
    ClosedCase('completeness__not_supported__multiplicity', _completion_builder(lambda: _closed_cross()(), EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes={"multiple_comparison_policy_id_when_applicable": None}, context_change=None), (
                                                                                                                                                                                                                                                            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                            EvaluationClaimValidationCode.INVALID_MULTIPLE_COMPARISON_POSTURE,
                                                                                                                                                                                                                                                        )),
    ClosedCase('completeness__not_supported__provenance', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes={"provenance": ()}, context_change=None), (
                                                                                                                                                                                                                EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                EvaluationClaimValidationCode.EMPTY_PROVENANCE,
                                                                                                                                                                                                            )),
    ClosedCase('completeness__not_supported__timestamp', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes={"claim_created_at": "invalid"}, context_change=None), (
                                                                                                                                                                                                                            EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                            EvaluationClaimValidationCode.INVALID_CLAIM_CREATED_AT,
                                                                                                                                                                                                                        )),
    ClosedCase('completeness__not_supported__self_supersession', _completion_builder(_completion_ensemble, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED, claim_changes={"supersedes_claim_id_when_applicable": "claim-1"}, context_change=None), (
                                                                                                                                                                                                                                                       EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT,
                                                                                                                                                                                                                                                       EvaluationClaimValidationCode.SELF_SUPERSESSION,
                                                                                                                                                                                                                                                   )),
)


class IteratorCreationFailure:
    def __iter__(self):
        raise RuntimeError("iterator creation")


class MidIterationFailure:
    def __iter__(self):
        yield ("first", 1)
        raise RuntimeError("mid iteration")


class MidIterationBaseFailure:
    def __iter__(self):
        yield ("first", 1)
        raise KeyboardInterrupt()


class BaseHashKey:
    def __hash__(self) -> int:
        raise KeyboardInterrupt()


_MISSING_ROOT_CODES = (EvaluationClaimValidationCode.MISSING_REQUIRED_FIELD,) * 33

REQUIRED_MAPPING_ROOT_CASE_IDS = (
    "mapping_root__non_mapping",
    "mapping_root__items_ordinary_failure",
    "mapping_root__iterator_creation_ordinary_failure",
    "mapping_root__mid_iteration_ordinary_failure",
    "mapping_root__malformed_one_item_tuple",
    "mapping_root__malformed_three_item_tuple",
    "mapping_root__unhashable_key",
    "mapping_root__key_hashing_ordinary_exception",
    "mapping_root__duplicate_exact_string",
    "mapping_root__duplicate_string_subclass",
    "mapping_root__duplicate_non_string",
    "mapping_root__asymmetric_equal_hash_duplicate",
    "mapping_root__existing_key_equality_ordinary_exception",
    "mapping_root__items_baseexception",
    "mapping_root__iteration_baseexception",
    "mapping_root__hashing_baseexception",
    "mapping_root__equality_baseexception",
)

MAPPING_ROOT_CASES = (
    MappingRootCase("mapping_root__non_mapping", lambda: object(), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__items_ordinary_failure", lambda: ItemsMapping(RuntimeError("items")), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__iterator_creation_ordinary_failure", lambda: ItemsMapping(IteratorCreationFailure()), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__mid_iteration_ordinary_failure", lambda: ItemsMapping(MidIterationFailure()), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__malformed_one_item_tuple", lambda: ItemsMapping((("only",),)), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__malformed_three_item_tuple", lambda: ItemsMapping((("one", 2, 3),)), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__unhashable_key", lambda: ItemsMapping(((["unhashable"], 1),)), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__key_hashing_ordinary_exception", lambda: ItemsMapping(((BadHash(), 1),)), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__duplicate_exact_string", lambda: ItemsMapping((("same", 1), ("same", 2))), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__duplicate_string_subclass", lambda: ItemsMapping(((TextSubclass("same"), 1), (TextSubclass("same"), 2))), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__duplicate_non_string", lambda: ItemsMapping(((7, 1), (7, 2))), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__asymmetric_equal_hash_duplicate", lambda: ItemsMapping(((EqualityKey(True), 1), (EqualityKey(False), 2))), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__existing_key_equality_ordinary_exception", lambda: ItemsMapping(((EqualityKey(RuntimeError("equality")), 1), (EqualityKey(False), 2))), _MISSING_ROOT_CODES),
    MappingRootCase("mapping_root__items_baseexception", lambda: ItemsMapping(KeyboardInterrupt()), None, KeyboardInterrupt),
    MappingRootCase("mapping_root__iteration_baseexception", lambda: ItemsMapping(MidIterationBaseFailure()), None, KeyboardInterrupt),
    MappingRootCase("mapping_root__hashing_baseexception", lambda: ItemsMapping(((BaseHashKey(), 1),)), None, KeyboardInterrupt),
    MappingRootCase("mapping_root__equality_baseexception", lambda: ItemsMapping(((EqualityKey(KeyboardInterrupt()), 1), (EqualityKey(False), 2))), None, KeyboardInterrupt),
)


@pytest.mark.parametrize("case", CLASS_MATRIX_CASES, ids=lambda case: case.case_id)
def test_closed_class_matrix(case: ClosedCase) -> None:
    claim, context = case.build()
    assert validate_evaluation_claim_record(claim, context).codes == case.expected_codes


def test_closed_class_matrix_inventory_is_exact() -> None:
    assert tuple(case.case_id for case in CLASS_MATRIX_CASES) == REQUIRED_CLASS_CASE_IDS
    assert len(CLASS_MATRIX_CASES) == 128
    assert len(set(REQUIRED_CLASS_CASE_IDS)) == 128
    assert all(callable(case.build) for case in CLASS_MATRIX_CASES)
    assert all(type(case.expected_codes) is tuple for case in CLASS_MATRIX_CASES)
    assert all(
        type(code) is EvaluationClaimValidationCode
        for case in CLASS_MATRIX_CASES
        for code in case.expected_codes
    )


def test_closed_class_repeated_cases_have_repeated_diagnostics() -> None:
    repeated = {
        "candidate_vs_climatology__repeated_candidate_identity": EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
        "candidate_vs_climatology__repeated_baseline_identity": EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
        "candidate_vs_climatology__repeated_disallowed_kind": EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
        "candidate_vs_persistence__repeated_candidate_identity": EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
        "candidate_vs_persistence__repeated_baseline_identity": EvaluationClaimValidationCode.BASELINE_IDENTITY_MISMATCH,
        "candidate_vs_persistence__repeated_disallowed_kind": EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
        "cross_baseline__repeated_candidate_identity": EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
        "binary_calibration__repeated_disallowed_kind": EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
        "binary_calibration__repeated_candidate_identity": EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
        "distributional_calibration__repeated_disallowed_kind": EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
        "distributional_calibration__repeated_candidate_identity": EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
        "ensemble_calibration__repeated_disallowed_kind": EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
        "ensemble_calibration__repeated_candidate_identity": EvaluationClaimValidationCode.CANDIDATE_IDENTITY_MISMATCH,
        "threshold_weighted__repeated_wrong_artifact": EvaluationClaimValidationCode.RESULT_KIND_NOT_ALLOWED,
        "stratum_specific__repeated_stratum_mismatch": EvaluationClaimValidationCode.RESULT_SCOPE_MISMATCH,
    }
    expected = {case.case_id: case.expected_codes for case in CLASS_MATRIX_CASES}
    assert set(repeated) <= set(expected)
    for case_id, code in repeated.items():
        assert expected[case_id].count(code) >= 2


@pytest.mark.parametrize("case", CONTEXT_MATRIX_CASES, ids=lambda case: case.case_id)
def test_closed_context_matrix(case: ClosedCase) -> None:
    subject, context = case.build()
    if type(subject) is MappingAdapterContext:
        actual = evaluation_claim_record_from_mapping(subject.mapping, context)[1]
    else:
        actual = validate_evaluation_claim_record(subject, context)
    assert actual.codes == case.expected_codes


def test_closed_context_matrix_inventory_is_exact() -> None:
    assert tuple(case.case_id for case in CONTEXT_MATRIX_CASES) == REQUIRED_CONTEXT_CASE_IDS
    assert len(CONTEXT_MATRIX_CASES) == 18
    assert len(set(REQUIRED_CONTEXT_CASE_IDS)) == 18
    assert all(callable(case.build) for case in CONTEXT_MATRIX_CASES)
    assert all(type(case.expected_codes) is tuple for case in CONTEXT_MATRIX_CASES)
    assert all(
        type(code) is EvaluationClaimValidationCode
        for case in CONTEXT_MATRIX_CASES
        for code in case.expected_codes
    )


def test_closed_context_occurrence_expectations_are_exact() -> None:
    expected = {case.case_id: case.expected_codes for case in CONTEXT_MATRIX_CASES}
    assert expected["context__invalid_items_two"].count(
        EvaluationClaimValidationCode.INVALID_RESULT_RECORD
    ) == 2
    assert expected["context__duplicate_once"].count(
        EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID
    ) == 1
    assert expected["context__duplicate_twice"].count(
        EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID
    ) == 2
    assert expected["context__resolution_multiple"][:2] == (
        EvaluationClaimValidationCode.DUPLICATE_CONTEXT_RESULT_ID,
        EvaluationClaimValidationCode.OBSERVED_RESULT_NOT_FOUND,
    )
    assert expected["context__unexpected_multiple"].count(
        EvaluationClaimValidationCode.UNEXPECTED_CONTEXT_RESULT
    ) == 2
    assert expected["context__paired_missing_both"][:2] == (
        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
    )
    assert expected["context__paired_two_pairs_candidate_then_baseline"][:4] == (
        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
        EvaluationClaimValidationCode.PAIRED_REFERENCE_NOT_FOUND,
    )


@pytest.mark.parametrize("case", COMPATIBILITY_MATRIX_CASES, ids=lambda case: case.case_id)
def test_closed_compatibility_matrix(case: ClosedCase) -> None:
    subject, context = case.build()
    if type(subject) is MappingAdapterContext:
        actual = evaluation_claim_record_from_mapping(subject.mapping, context)[1]
    else:
        actual = validate_evaluation_claim_record(subject, context)
    assert actual.codes == case.expected_codes


def test_closed_compatibility_matrix_inventory_is_exact() -> None:
    assert tuple(case.case_id for case in COMPATIBILITY_MATRIX_CASES) == REQUIRED_COMPATIBILITY_CASE_IDS
    assert len(COMPATIBILITY_MATRIX_CASES) == 84
    assert len(set(REQUIRED_COMPATIBILITY_CASE_IDS)) == 84
    assert all(callable(case.build) for case in COMPATIBILITY_MATRIX_CASES)
    assert all(type(case.expected_codes) is tuple for case in COMPATIBILITY_MATRIX_CASES)
    assert all(
        type(code) is EvaluationClaimValidationCode
        for case in COMPATIBILITY_MATRIX_CASES
        for code in case.expected_codes
    )


def test_closed_compatibility_fixture_postures_are_executable() -> None:
    groups = tuple(
        COMPATIBILITY_MATRIX_CASES[index:index + 7]
        for index in range(0, len(COMPATIBILITY_MATRIX_CASES), 7)
    )
    assert len(groups) == 12
    for match, single, repeated, missing, blank, nonstring, subclass in groups:
        assert match.expected_codes == ()
        assert len(single.build()[1]) == 1
        assert len(repeated.build()[1]) >= 2
        assert all(
            type(case.build()[0]) is MappingAdapterContext
            for case in (missing, blank, nonstring, subclass)
        )


@pytest.mark.parametrize("case", DISPOSITION_MATRIX_CASES, ids=lambda case: case.case_id)
def test_closed_disposition_matrix(case: ClosedCase) -> None:
    claim, context = case.build()
    assert validate_evaluation_claim_record(claim, context).codes == case.expected_codes


def test_closed_disposition_matrix_inventory_and_role_status_facts_are_exact() -> None:
    assert tuple(case.case_id for case in DISPOSITION_MATRIX_CASES) == REQUIRED_DISPOSITION_CASE_IDS
    assert len(DISPOSITION_MATRIX_CASES) == 31
    assert len(set(REQUIRED_DISPOSITION_CASE_IDS)) == 31
    assert all(callable(case.build) for case in DISPOSITION_MATRIX_CASES)
    assert all(type(case.expected_codes) is tuple for case in DISPOSITION_MATRIX_CASES)
    facts = tuple(
        (role_index, status)
        for role_index in (0, 1, 2)
        for status in (
            EvaluationResultSupportStatus.SUPPORTED,
            EvaluationResultSupportStatus.BLOCKED,
            EvaluationResultSupportStatus.UNAVAILABLE,
            EvaluationResultSupportStatus.INSUFFICIENT,
        )
    )
    for case, (role_index, status) in zip(DISPOSITION_MATRIX_CASES[:24:2], facts):
        _, context = case.build()
        assert context[role_index].support_status is status
        assert all(
            record.support_status is EvaluationResultSupportStatus.SUPPORTED
            for index, record in enumerate(context)
            if index != role_index
        )


@pytest.mark.parametrize("case", SUPPORTED_COMPLETENESS_CASES, ids=lambda case: case.case_id)
def test_closed_supported_completeness_matrix(case: ClosedCase) -> None:
    claim, context = case.build()
    assert validate_evaluation_claim_record(claim, context).codes == case.expected_codes


def test_closed_supported_completeness_inventory_and_facts_are_exact() -> None:
    assert tuple(case.case_id for case in SUPPORTED_COMPLETENESS_CASES) == REQUIRED_SUPPORTED_COMPLETENESS_CASE_IDS
    assert len(SUPPORTED_COMPLETENESS_CASES) == 44
    assert len(set(REQUIRED_SUPPORTED_COMPLETENESS_CASE_IDS)) == 44
    assert len({id(case.build) for case in SUPPORTED_COMPLETENESS_CASES}) == 44
    assert all(callable(case.build) for case in SUPPORTED_COMPLETENESS_CASES)
    assert all(type(case.expected_codes) is tuple for case in SUPPORTED_COMPLETENESS_CASES)
    assert all(
        type(code) is EvaluationClaimValidationCode
        for case in SUPPORTED_COMPLETENESS_CASES
        for code in case.expected_codes
    )
    assert all(
        EvaluationClaimValidationCode.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT
        in case.expected_codes
        for case in SUPPORTED_COMPLETENESS_CASES
    )


@pytest.mark.parametrize("case", MAPPING_ROOT_CASES, ids=lambda case: case.case_id)
def test_closed_mapping_root_matrix(case: MappingRootCase) -> None:
    root = case.build()
    if case.expected_exception is not None:
        with pytest.raises(case.expected_exception):
            evaluation_claim_record_from_mapping(root, ())
    else:
        assert evaluation_claim_record_from_mapping(root, ())[1].codes == case.expected_codes


def test_closed_mapping_root_inventory_is_exact() -> None:
    assert tuple(case.case_id for case in MAPPING_ROOT_CASES) == REQUIRED_MAPPING_ROOT_CASE_IDS
    assert len(MAPPING_ROOT_CASES) == 17
    assert len(set(REQUIRED_MAPPING_ROOT_CASE_IDS)) == 17
    assert all(callable(case.build) for case in MAPPING_ROOT_CASES)
    normal = MAPPING_ROOT_CASES[:13]
    propagation = MAPPING_ROOT_CASES[13:]
    assert all(type(case.expected_codes) is tuple for case in normal)
    assert all(case.expected_codes == _MISSING_ROOT_CODES for case in normal)
    assert all(case.expected_exception is None for case in normal)
    assert all(case.expected_codes is None for case in propagation)
    assert all(case.expected_exception is KeyboardInterrupt for case in propagation)
    assert type(normal[0].build()) is object
    assert all(isinstance(case.build(), Mapping) for case in normal[1:])
    assert all(isinstance(case.build(), Mapping) for case in propagation)


ALL_CLOSED_CASES = (
    CLASS_MATRIX_CASES + CONTEXT_MATRIX_CASES + COMPATIBILITY_MATRIX_CASES
    + DISPOSITION_MATRIX_CASES + SUPPORTED_COMPLETENESS_CASES + MAPPING_ROOT_CASES
)


def test_closed_case_data_is_immutable_executable_and_unique() -> None:
    assert len({case.case_id for case in ALL_CLOSED_CASES}) == len(ALL_CLOSED_CASES)
    for case in ALL_CLOSED_CASES:
        assert callable(case.build)
        if type(case) is MappingRootCase:
            assert tuple(field.name for field in dataclasses.fields(case)) == (
                "case_id", "build", "expected_codes", "expected_exception",
            )
            assert type(case.expected_codes) is tuple or case.expected_exception is KeyboardInterrupt
        else:
            assert tuple(field.name for field in dataclasses.fields(case)) == (
                "case_id", "build", "expected_codes",
            )
            assert type(case.expected_codes) is tuple
            assert all(type(item) is EvaluationClaimValidationCode for item in case.expected_codes)


@pytest.mark.parametrize("field", dataclasses.fields(EvaluationClaimRecord), ids=lambda field: field.name)
def test_each_claim_field_resolved_annotation(field: dataclasses.Field[object]) -> None:
    expected = {
        "evaluation_claim_id": str, "claim_class": EvaluationClaimClass,
        "claim_rule_id": str, "claim_rule_version": str,
        "claim_disposition": EvaluationClaimDisposition, "claim_disposition_reason": str,
        "target_posture": str, "candidate_method_id": str, "candidate_method_version": str,
        "baseline_type_when_applicable": BaselineType | None,
        "baseline_method_id_when_applicable": str | None,
        "baseline_method_version_when_applicable": str | None,
        "prediction_representation": ScoringPredictionRepresentation,
        "metric_or_diagnostic_ids": tuple[str, ...],
        "metric_or_diagnostic_versions": tuple[str, ...],
        "required_evaluation_result_ids": tuple[str, ...],
        "observed_evaluation_result_ids": tuple[str, ...],
        "missing_evaluation_result_ids": tuple[str, ...],
        "split_id": str, "split_version": str, "fold_scope": str, "cutoff_scope": str,
        "paired_test_record_set_id": str, "aggregation_rule_id": str,
        "weighting_rule_id": str, "stratum_id_when_applicable": str | None,
        "uncertainty_policy_id": str, "sample_support_rule_id": str,
        "selection_control_policy_id": str,
        "multiple_comparison_policy_id_when_applicable": str | None,
        "evidence_gate_eligibility_posture": str, "provenance": tuple[str, ...],
        "claim_created_at": str, "supersedes_claim_id_when_applicable": str | None,
    }
    assert typing.get_type_hints(EvaluationClaimRecord)[field.name] == expected[field.name]


@pytest.mark.parametrize("index,group", tuple(enumerate((
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
))))
def test_each_validation_group_is_independently_frozen(index: int, group: str) -> None:
    import meg.weather.stage3.evaluation_claim as module

    assert module._VALIDATION_GROUPS[index] == group


@pytest.mark.parametrize("index,name", tuple(enumerate(PUBLIC)))
def test_each_public_definition_order_entry(index: int, name: str) -> None:
    import meg.weather.stage3.evaluation_claim as module

    assert module.__all__[index] == name


@pytest.mark.parametrize("claim_class", tuple(EvaluationClaimClass))
def test_each_allowed_kind_matrix_entry_is_literal(claim_class: EvaluationClaimClass) -> None:
    import meg.weather.stage3.evaluation_claim as module

    expected = {
        EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
        EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
        EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
        EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR: (EvaluationResultKind.CALIBRATION_BIN_RESULT, EvaluationResultKind.SCALAR_SCORE_RESULT, EvaluationResultKind.DECOMPOSITION_RESULT),
        EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR: (EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT, EvaluationResultKind.SCALAR_SCORE_RESULT),
        EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR: (EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT,),
        EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
        EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
    }
    assert module._ALLOWED_RESULT_KINDS[claim_class] == expected[claim_class]


@pytest.mark.parametrize("disposition", tuple(EvaluationClaimDisposition))
def test_each_evidence_gate_matrix_entry_is_literal(disposition: EvaluationClaimDisposition) -> None:
    import meg.weather.stage3.evaluation_claim as module

    expected = {
        EvaluationClaimDisposition.CLAIM_SUPPORTED: "eligible_for_later_evidence_gate_decision_only",
        EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED: "claim_support_absent",
        EvaluationClaimDisposition.CLAIM_INSUFFICIENT: "evidence_gate_use_blocked",
        EvaluationClaimDisposition.CLAIM_BLOCKED: "evidence_gate_use_blocked",
        EvaluationClaimDisposition.CLAIM_UNAVAILABLE: "no_substitution_or_evidence_gate_use",
    }
    assert module._EVIDENCE_GATE_MATRIX[disposition] == expected[disposition]


@pytest.mark.parametrize("claim_class", tuple(EvaluationClaimClass))
def test_each_class_partition_entry_is_literal(claim_class: EvaluationClaimClass) -> None:
    import meg.weather.stage3.evaluation_claim as module

    expected_paired = claim_class in (
        EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL,
        EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL,
        EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES,
        EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL,
        EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL,
    )
    assert (claim_class in module._PAIRED_CLASSES) is expected_paired
    assert (claim_class in module._NON_PAIRED_CLASSES) is not expected_paired


@pytest.mark.parametrize("field_name,annotation", (
    ("severity", EvaluationClaimValidationSeverity),
    ("passed", bool),
    ("codes", tuple[EvaluationClaimValidationCode, ...]),
))
def test_each_validation_result_field_annotation(field_name: str, annotation: object) -> None:
    assert typing.get_type_hints(EvaluationClaimValidationResult)[field_name] == annotation


REQUIRED_COVERAGE_MANIFEST_KEYS = ('imports', 'public_api', 'public_source_order', 'claim_class_enum', 'disposition_enum', 'severity_enum', 'validation_codes', 'record_structure', 'validation_result_structure', 'signatures', 'mapping_keys', 'mapping_root_behavior', 'mapping_adaptation', 'required_text', 'nullable_text', 'fixed_target', 'metric_ids', 'metric_versions', 'required_result_ids', 'observed_result_ids', 'missing_result_ids', 'partition', 'result_context', 'duplicate_identities', 'observed_resolution', 'unexpected_context', 'paired_references', 'target_compatibility', 'representation_compatibility', 'scope_split_id', 'scope_split_version', 'scope_fold', 'scope_cutoff', 'scope_paired_set', 'scope_aggregation', 'scope_weighting', 'scope_stratum', 'metric_compatibility', 'candidate_identity', 'baseline_identity', 'class_candidate_climatology', 'class_candidate_persistence', 'class_cross_baseline', 'class_binary_calibration', 'class_distributional_calibration', 'class_ensemble_calibration', 'class_threshold_weighted', 'class_stratum_specific', 'baseline_requirements', 'cross_baseline_completeness', 'stratum_requirements', 'disposition_precedence', 'supported_completeness', 'evidence_gate_posture', 'multiplicity', 'provenance', 'timestamp', 'supersession', 'validation_groups', 'purity', 'caller_preservation', 'determinism', 'mutation_resistance', 'observed_tuple_prerequisite_suppression', 'evidence_posture_exact_type', 'supported_completeness_evidence_posture', 'candidate_claim_identity_prerequisites', 'baseline_claim_identity_prerequisites')


def test_final_structural_literal_contract_is_exact() -> None:
    import meg.weather.stage3.evaluation_claim as module

    tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.append(("import", None, tuple(alias.name for alias in node.names), 0))
        elif isinstance(node, ast.ImportFrom):
            imports.append(("from", node.module, tuple(alias.name for alias in node.names), node.level))
    assert tuple(imports) == (
        ("from", "__future__", ("annotations",), 0),
        ("from", "collections.abc", ("Mapping",), 0),
        ("from", "dataclasses", ("dataclass",), 0),
        ("from", "datetime", ("datetime",), 0),
        ("from", "enum", ("StrEnum",), 0),
        ("import", None, ("re",), 0),
        ("from", "meg.weather.stage3.baseline_contracts", ("BaselineType",), 0),
        ("from", "meg.weather.stage3.scoring_and_diagnostics", ("ScoringArtifact", "ScoringPredictionRepresentation"), 0),
        ("from", "meg.weather.stage3.evaluation_result_record", (
            "EvaluationResultKind", "EvaluationResultSupportStatus", "EvaluationResultMethodRole",
            "EvaluationResultRecord", "EvaluationResultValidationResult",
            "PairedComparisonResultPayload", "validate_evaluation_result_record",
        ), 0),
    )
    assert module.__all__ == (
        "EvaluationClaimClass", "EvaluationClaimDisposition",
        "EvaluationClaimValidationSeverity", "EvaluationClaimValidationCode",
        "EvaluationClaimRecord", "EvaluationClaimValidationResult",
        "evaluation_claim_record_from_mapping", "validate_evaluation_claim_record",
    )
    assert tuple(
        node.name for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and not node.name.startswith("_")
    ) == module.__all__
    assert tuple((member.name, member.value) for member in EvaluationClaimClass) == (
        ("CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL", "candidate_vs_climatology_predictive_skill"),
        ("CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL", "candidate_vs_persistence_predictive_skill"),
        ("CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES", "candidate_predictive_skill_across_required_baselines"),
        ("BINARY_CALIBRATION_BEHAVIOR", "binary_calibration_behavior"),
        ("DISTRIBUTIONAL_CALIBRATION_BEHAVIOR", "distributional_calibration_behavior"),
        ("ENSEMBLE_CALIBRATION_BEHAVIOR", "ensemble_calibration_behavior"),
        ("THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL", "threshold_weighted_distribution_skill"),
        ("STRATUM_SPECIFIC_PREDICTIVE_SKILL", "stratum_specific_predictive_skill"),
    )
    assert tuple((member.name, member.value) for member in EvaluationClaimDisposition) == (
        ("CLAIM_SUPPORTED", "claim_supported"), ("CLAIM_NOT_SUPPORTED", "claim_not_supported"),
        ("CLAIM_INSUFFICIENT", "claim_insufficient"), ("CLAIM_BLOCKED", "claim_blocked"),
        ("CLAIM_UNAVAILABLE", "claim_unavailable"),
    )
    assert tuple((member.name, member.value) for member in EvaluationClaimValidationSeverity) == (
        ("PASSED", "passed"), ("BLOCKED", "blocked"),
    )
    assert tuple((member.name, member.value) for member in EvaluationClaimValidationCode) == (('MISSING_REQUIRED_FIELD', 'missing_required_field'), ('UNEXPECTED_FIELD', 'unexpected_field'), ('BLANK_REQUIRED_TEXT', 'blank_required_text'), ('INVALID_CLAIM_CLASS', 'invalid_claim_class'), ('INVALID_CLAIM_DISPOSITION', 'invalid_claim_disposition'), ('INVALID_BASELINE_TYPE', 'invalid_baseline_type'), ('INVALID_PREDICTION_REPRESENTATION', 'invalid_prediction_representation'), ('INVALID_FIXED_POSTURE', 'invalid_fixed_posture'), ('INVALID_EVIDENCE_GATE_POSTURE', 'invalid_evidence_gate_posture'), ('INVALID_METRIC_IDENTITY_TUPLE', 'invalid_metric_identity_tuple'), ('METRIC_VERSION_LENGTH_MISMATCH', 'metric_version_length_mismatch'), ('INVALID_REQUIRED_RESULT_IDS', 'invalid_required_result_ids'), ('INVALID_OBSERVED_RESULT_IDS', 'invalid_observed_result_ids'), ('INVALID_MISSING_RESULT_IDS', 'invalid_missing_result_ids'), ('RESULT_SET_PARTITION_MISMATCH', 'result_set_partition_mismatch'), ('INVALID_RESULT_RECORD_CONTAINER', 'invalid_result_record_container'), ('INVALID_RESULT_RECORD', 'invalid_result_record'), ('DUPLICATE_CONTEXT_RESULT_ID', 'duplicate_context_result_id'), ('OBSERVED_RESULT_NOT_FOUND', 'observed_result_not_found'), ('UNEXPECTED_CONTEXT_RESULT', 'unexpected_context_result'), ('PAIRED_REFERENCE_NOT_FOUND', 'paired_reference_not_found'), ('RESULT_TARGET_MISMATCH', 'result_target_mismatch'), ('RESULT_REPRESENTATION_MISMATCH', 'result_representation_mismatch'), ('RESULT_SCOPE_MISMATCH', 'result_scope_mismatch'), ('RESULT_METRIC_MISMATCH', 'result_metric_mismatch'), ('CANDIDATE_IDENTITY_MISMATCH', 'candidate_identity_mismatch'), ('BASELINE_IDENTITY_MISMATCH', 'baseline_identity_mismatch'), ('RESULT_KIND_NOT_ALLOWED', 'result_kind_not_allowed'), ('BASELINE_REQUIREMENT_MISMATCH', 'baseline_requirement_mismatch'), ('CROSS_BASELINE_INCOMPLETE', 'cross_baseline_incomplete'), ('STRATUM_REQUIREMENT_MISMATCH', 'stratum_requirement_mismatch'), ('DISPOSITION_PRECEDENCE_MISMATCH', 'disposition_precedence_mismatch'), ('SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT', 'supported_or_not_supported_without_complete_support'), ('INVALID_MULTIPLE_COMPARISON_POSTURE', 'invalid_multiple_comparison_posture'), ('EMPTY_PROVENANCE', 'empty_provenance'), ('INVALID_PROVENANCE_REF', 'invalid_provenance_ref'), ('INVALID_CLAIM_CREATED_AT', 'invalid_claim_created_at'), ('SELF_SUPERSESSION', 'self_supersession'))
    assert tuple(field.name for field in dataclasses.fields(EvaluationClaimRecord)) == FIELDS
    assert typing.get_type_hints(EvaluationClaimRecord) == {
        "evaluation_claim_id": str, "claim_class": EvaluationClaimClass, "claim_rule_id": str,
        "claim_rule_version": str, "claim_disposition": EvaluationClaimDisposition,
        "claim_disposition_reason": str, "target_posture": str, "candidate_method_id": str,
        "candidate_method_version": str, "baseline_type_when_applicable": BaselineType | None,
        "baseline_method_id_when_applicable": str | None, "baseline_method_version_when_applicable": str | None,
        "prediction_representation": ScoringPredictionRepresentation, "metric_or_diagnostic_ids": tuple[str, ...],
        "metric_or_diagnostic_versions": tuple[str, ...], "required_evaluation_result_ids": tuple[str, ...],
        "observed_evaluation_result_ids": tuple[str, ...], "missing_evaluation_result_ids": tuple[str, ...],
        "split_id": str, "split_version": str, "fold_scope": str, "cutoff_scope": str,
        "paired_test_record_set_id": str, "aggregation_rule_id": str, "weighting_rule_id": str,
        "stratum_id_when_applicable": str | None, "uncertainty_policy_id": str,
        "sample_support_rule_id": str, "selection_control_policy_id": str,
        "multiple_comparison_policy_id_when_applicable": str | None,
        "evidence_gate_eligibility_posture": str, "provenance": tuple[str, ...],
        "claim_created_at": str, "supersedes_claim_id_when_applicable": str | None,
    }
    assert tuple(field.name for field in dataclasses.fields(EvaluationClaimValidationResult)) == ("severity", "passed", "codes")
    assert typing.get_type_hints(EvaluationClaimValidationResult) == {
        "severity": EvaluationClaimValidationSeverity, "passed": bool,
        "codes": tuple[EvaluationClaimValidationCode, ...],
    }
    assert str(inspect.signature(evaluation_claim_record_from_mapping)) == "(mapping: 'object', result_records: 'object') -> 'tuple[EvaluationClaimRecord | None, EvaluationClaimValidationResult]'"
    assert str(inspect.signature(validate_evaluation_claim_record)) == "(record: 'EvaluationClaimRecord', result_records: 'tuple[EvaluationResultRecord, ...]') -> 'EvaluationClaimValidationResult'"
    assert module._REQUIRED_MAPPING_KEYS == FIELDS[:33]
    assert module._OPTIONAL_MAPPING_KEYS == ("supersedes_claim_id_when_applicable",)
    assert module._LIST_TO_TUPLE_FIELDS == ("metric_or_diagnostic_ids", "metric_or_diagnostic_versions", "required_evaluation_result_ids", "observed_evaluation_result_ids", "missing_evaluation_result_ids", "provenance")
    assert module._REQUIRED_TEXT_FIELDS == ("evaluation_claim_id", "claim_rule_id", "claim_rule_version", "claim_disposition_reason", "target_posture", "candidate_method_id", "candidate_method_version", "split_id", "split_version", "fold_scope", "cutoff_scope", "paired_test_record_set_id", "aggregation_rule_id", "weighting_rule_id", "uncertainty_policy_id", "sample_support_rule_id", "selection_control_policy_id", "evidence_gate_eligibility_posture", "claim_created_at")
    assert module._NULLABLE_TEXT_FIELDS == ("baseline_method_id_when_applicable", "baseline_method_version_when_applicable", "stratum_id_when_applicable", "multiple_comparison_policy_id_when_applicable", "supersedes_claim_id_when_applicable")
    assert module._EVIDENCE_GATE_MATRIX == {
        EvaluationClaimDisposition.CLAIM_SUPPORTED: "eligible_for_later_evidence_gate_decision_only",
        EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED: "claim_support_absent",
        EvaluationClaimDisposition.CLAIM_INSUFFICIENT: "evidence_gate_use_blocked",
        EvaluationClaimDisposition.CLAIM_BLOCKED: "evidence_gate_use_blocked",
        EvaluationClaimDisposition.CLAIM_UNAVAILABLE: "no_substitution_or_evidence_gate_use",
    }
    assert module._PAIRED_CLASSES == (EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL, EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL, EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES, EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL)
    assert module._NON_PAIRED_CLASSES == (EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR, EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR, EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR)
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


def test_final_closed_inventory_and_manifest_are_exact() -> None:
    required = (REQUIRED_CLASS_CASE_IDS + REQUIRED_CONTEXT_CASE_IDS + REQUIRED_COMPATIBILITY_CASE_IDS + REQUIRED_DISPOSITION_CASE_IDS + REQUIRED_SUPPORTED_COMPLETENESS_CASE_IDS + REQUIRED_MAPPING_ROOT_CASE_IDS)
    assert (len(CLASS_MATRIX_CASES), len(CONTEXT_MATRIX_CASES), len(COMPATIBILITY_MATRIX_CASES), len(DISPOSITION_MATRIX_CASES), len(SUPPORTED_COMPLETENESS_CASES), len(MAPPING_ROOT_CASES)) == (128, 18, 84, 31, 44, 17)
    assert len(ALL_CLOSED_CASES) == 322
    assert tuple(case.case_id for case in ALL_CLOSED_CASES) == required
    assert len(set(required)) == 322
    assert tuple(COVERAGE_MANIFEST) == REQUIRED_COVERAGE_MANIFEST_KEYS
    assert all(COVERAGE_MANIFEST.values())
    test_names = {name for name, value in globals().items() if name.startswith("test_") and callable(value)}
    closed_ids = {case.case_id for case in ALL_CLOSED_CASES}
    assert all(set(references) <= test_names | closed_ids for references in COVERAGE_MANIFEST.values())
    behavioral = ("mapping_root_behavior", "result_context", "duplicate_identities", "observed_resolution", "unexpected_context", "paired_references", "target_compatibility", "representation_compatibility", "scope_split_id", "scope_split_version", "scope_fold", "scope_cutoff", "scope_paired_set", "scope_aggregation", "scope_weighting", "scope_stratum", "metric_compatibility", "candidate_identity", "baseline_identity", "class_candidate_climatology", "class_candidate_persistence", "class_cross_baseline", "class_binary_calibration", "class_distributional_calibration", "class_ensemble_calibration", "class_threshold_weighted", "class_stratum_specific", "disposition_precedence", "supported_completeness")
    assert all(set(COVERAGE_MANIFEST[key]) <= closed_ids for key in behavioral)
