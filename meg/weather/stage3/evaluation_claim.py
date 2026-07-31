"""Immutable Stage 3 evaluation claims and pure boundary validation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import re

from meg.weather.stage3.baseline_contracts import BaselineType
from meg.weather.stage3.scoring_and_diagnostics import (
    ScoringArtifact,
    ScoringPredictionRepresentation,
)
from meg.weather.stage3.evaluation_result_record import (
    EvaluationResultKind,
    EvaluationResultSupportStatus,
    EvaluationResultMethodRole,
    EvaluationResultRecord,
    EvaluationResultValidationResult,
    PairedComparisonResultPayload,
    validate_evaluation_result_record,
)

__all__ = (
    "EvaluationClaimClass",
    "EvaluationClaimDisposition",
    "EvaluationClaimValidationSeverity",
    "EvaluationClaimValidationCode",
    "EvaluationClaimRecord",
    "EvaluationClaimValidationResult",
    "evaluation_claim_record_from_mapping",
    "validate_evaluation_claim_record",
)


class EvaluationClaimClass(StrEnum):
    CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL = "candidate_vs_climatology_predictive_skill"
    CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL = "candidate_vs_persistence_predictive_skill"
    CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES = "candidate_predictive_skill_across_required_baselines"
    BINARY_CALIBRATION_BEHAVIOR = "binary_calibration_behavior"
    DISTRIBUTIONAL_CALIBRATION_BEHAVIOR = "distributional_calibration_behavior"
    ENSEMBLE_CALIBRATION_BEHAVIOR = "ensemble_calibration_behavior"
    THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL = "threshold_weighted_distribution_skill"
    STRATUM_SPECIFIC_PREDICTIVE_SKILL = "stratum_specific_predictive_skill"


class EvaluationClaimDisposition(StrEnum):
    CLAIM_SUPPORTED = "claim_supported"
    CLAIM_NOT_SUPPORTED = "claim_not_supported"
    CLAIM_INSUFFICIENT = "claim_insufficient"
    CLAIM_BLOCKED = "claim_blocked"
    CLAIM_UNAVAILABLE = "claim_unavailable"


class EvaluationClaimValidationSeverity(StrEnum):
    PASSED = "passed"
    BLOCKED = "blocked"


class EvaluationClaimValidationCode(StrEnum):
    MISSING_REQUIRED_FIELD = "missing_required_field"
    UNEXPECTED_FIELD = "unexpected_field"
    BLANK_REQUIRED_TEXT = "blank_required_text"
    INVALID_CLAIM_CLASS = "invalid_claim_class"
    INVALID_CLAIM_DISPOSITION = "invalid_claim_disposition"
    INVALID_BASELINE_TYPE = "invalid_baseline_type"
    INVALID_PREDICTION_REPRESENTATION = "invalid_prediction_representation"
    INVALID_FIXED_POSTURE = "invalid_fixed_posture"
    INVALID_EVIDENCE_GATE_POSTURE = "invalid_evidence_gate_posture"
    INVALID_METRIC_IDENTITY_TUPLE = "invalid_metric_identity_tuple"
    METRIC_VERSION_LENGTH_MISMATCH = "metric_version_length_mismatch"
    INVALID_REQUIRED_RESULT_IDS = "invalid_required_result_ids"
    INVALID_OBSERVED_RESULT_IDS = "invalid_observed_result_ids"
    INVALID_MISSING_RESULT_IDS = "invalid_missing_result_ids"
    RESULT_SET_PARTITION_MISMATCH = "result_set_partition_mismatch"
    INVALID_RESULT_RECORD_CONTAINER = "invalid_result_record_container"
    INVALID_RESULT_RECORD = "invalid_result_record"
    DUPLICATE_CONTEXT_RESULT_ID = "duplicate_context_result_id"
    OBSERVED_RESULT_NOT_FOUND = "observed_result_not_found"
    UNEXPECTED_CONTEXT_RESULT = "unexpected_context_result"
    PAIRED_REFERENCE_NOT_FOUND = "paired_reference_not_found"
    RESULT_TARGET_MISMATCH = "result_target_mismatch"
    RESULT_REPRESENTATION_MISMATCH = "result_representation_mismatch"
    RESULT_SCOPE_MISMATCH = "result_scope_mismatch"
    RESULT_METRIC_MISMATCH = "result_metric_mismatch"
    CANDIDATE_IDENTITY_MISMATCH = "candidate_identity_mismatch"
    BASELINE_IDENTITY_MISMATCH = "baseline_identity_mismatch"
    RESULT_KIND_NOT_ALLOWED = "result_kind_not_allowed"
    BASELINE_REQUIREMENT_MISMATCH = "baseline_requirement_mismatch"
    CROSS_BASELINE_INCOMPLETE = "cross_baseline_incomplete"
    STRATUM_REQUIREMENT_MISMATCH = "stratum_requirement_mismatch"
    DISPOSITION_PRECEDENCE_MISMATCH = "disposition_precedence_mismatch"
    SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT = "supported_or_not_supported_without_complete_support"
    INVALID_MULTIPLE_COMPARISON_POSTURE = "invalid_multiple_comparison_posture"
    EMPTY_PROVENANCE = "empty_provenance"
    INVALID_PROVENANCE_REF = "invalid_provenance_ref"
    INVALID_CLAIM_CREATED_AT = "invalid_claim_created_at"
    SELF_SUPERSESSION = "self_supersession"


@dataclass(frozen=True)
class EvaluationClaimRecord:
    evaluation_claim_id: str
    claim_class: EvaluationClaimClass
    claim_rule_id: str
    claim_rule_version: str
    claim_disposition: EvaluationClaimDisposition
    claim_disposition_reason: str
    target_posture: str
    candidate_method_id: str
    candidate_method_version: str
    baseline_type_when_applicable: BaselineType | None
    baseline_method_id_when_applicable: str | None
    baseline_method_version_when_applicable: str | None
    prediction_representation: ScoringPredictionRepresentation
    metric_or_diagnostic_ids: tuple[str, ...]
    metric_or_diagnostic_versions: tuple[str, ...]
    required_evaluation_result_ids: tuple[str, ...]
    observed_evaluation_result_ids: tuple[str, ...]
    missing_evaluation_result_ids: tuple[str, ...]
    split_id: str
    split_version: str
    fold_scope: str
    cutoff_scope: str
    paired_test_record_set_id: str
    aggregation_rule_id: str
    weighting_rule_id: str
    stratum_id_when_applicable: str | None
    uncertainty_policy_id: str
    sample_support_rule_id: str
    selection_control_policy_id: str
    multiple_comparison_policy_id_when_applicable: str | None
    evidence_gate_eligibility_posture: str
    provenance: tuple[str, ...]
    claim_created_at: str
    supersedes_claim_id_when_applicable: str | None = None


@dataclass(frozen=True)
class EvaluationClaimValidationResult:
    severity: EvaluationClaimValidationSeverity
    passed: bool
    codes: tuple[EvaluationClaimValidationCode, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "codes", tuple(self.codes))
        if self.codes:
            object.__setattr__(self, "severity", EvaluationClaimValidationSeverity.BLOCKED)
            object.__setattr__(self, "passed", False)
        else:
            object.__setattr__(self, "severity", EvaluationClaimValidationSeverity.PASSED)
            object.__setattr__(self, "passed", True)
            object.__setattr__(self, "codes", ())


_REQUIRED_MAPPING_KEYS = (
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
    "provenance", "claim_created_at",
)
_OPTIONAL_MAPPING_KEYS = ("supersedes_claim_id_when_applicable",)
_LIST_TO_TUPLE_FIELDS = (
    "metric_or_diagnostic_ids", "metric_or_diagnostic_versions",
    "required_evaluation_result_ids", "observed_evaluation_result_ids",
    "missing_evaluation_result_ids", "provenance",
)
_REQUIRED_TEXT_FIELDS = (
    "evaluation_claim_id", "claim_rule_id", "claim_rule_version",
    "claim_disposition_reason", "target_posture", "candidate_method_id",
    "candidate_method_version", "split_id", "split_version", "fold_scope",
    "cutoff_scope", "paired_test_record_set_id", "aggregation_rule_id",
    "weighting_rule_id", "uncertainty_policy_id", "sample_support_rule_id",
    "selection_control_policy_id", "evidence_gate_eligibility_posture",
    "claim_created_at",
)
_NULLABLE_TEXT_FIELDS = (
    "baseline_method_id_when_applicable", "baseline_method_version_when_applicable",
    "stratum_id_when_applicable", "multiple_comparison_policy_id_when_applicable",
    "supersedes_claim_id_when_applicable",
)
_FIXED_TARGET_POSTURE = "venue_defined_settlement_outcome"
_EVIDENCE_GATE_MATRIX = {
    EvaluationClaimDisposition.CLAIM_SUPPORTED: "eligible_for_later_evidence_gate_decision_only",
    EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED: "claim_support_absent",
    EvaluationClaimDisposition.CLAIM_INSUFFICIENT: "evidence_gate_use_blocked",
    EvaluationClaimDisposition.CLAIM_BLOCKED: "evidence_gate_use_blocked",
    EvaluationClaimDisposition.CLAIM_UNAVAILABLE: "no_substitution_or_evidence_gate_use",
}
_PAIRED_CLASSES = (
    EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL,
    EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL,
    EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES,
    EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL,
    EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL,
)
_NON_PAIRED_CLASSES = (
    EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR,
    EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR,
    EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR,
)
_ALLOWED_RESULT_KINDS = {
    EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
    EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
    EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
    EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR: (EvaluationResultKind.CALIBRATION_BIN_RESULT, EvaluationResultKind.SCALAR_SCORE_RESULT, EvaluationResultKind.DECOMPOSITION_RESULT),
    EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR: (EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT, EvaluationResultKind.SCALAR_SCORE_RESULT),
    EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR: (EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT,),
    EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
    EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL: (EvaluationResultKind.PAIRED_COMPARISON_RESULT,),
}
_VALIDATION_GROUPS = (
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


def _result(codes: list[EvaluationClaimValidationCode] | tuple[EvaluationClaimValidationCode, ...]) -> EvaluationClaimValidationResult:
    return EvaluationClaimValidationResult(EvaluationClaimValidationSeverity.BLOCKED, False, tuple(codes))


def _valid_text(value: object) -> bool:
    return type(value) is str and bool(value.strip())


def _valid_unique_text_tuple(value: object, *, nonempty: bool) -> bool:
    return type(value) is tuple and (not nonempty or bool(value)) and all(_valid_text(item) for item in value) and len(value) == len(set(value))


def _valid_metric_versions(value: object) -> bool:
    return type(value) is tuple and bool(value) and all(_valid_text(item) for item in value)


def _valid_timestamp(value: object) -> bool:
    if type(value) is not str or "T" not in value:
        return False
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    if not value.endswith("Z") and re.search(r"[+-]\d{2}:\d{2}$", value) is None:
        return False
    try:
        return datetime.fromisoformat(candidate).utcoffset() is not None
    except (ValueError, OverflowError):
        return False


def _scope_matches(values: Mapping[str, object], present: set[str], result: EvaluationResultRecord) -> bool:
    required = {"split_id", "split_version", "fold_scope", "cutoff_scope", "paired_test_record_set_id", "aggregation_rule_id", "weighting_rule_id"}
    if not required <= present:
        return True
    return (
        result.split_id == values.get("split_id")
        and result.split_version == values.get("split_version")
        and result.fold_id == values.get("fold_scope")
        and result.cutoff_identity == values.get("cutoff_scope")
        and result.paired_test_record_set_id == values.get("paired_test_record_set_id")
        and result.aggregation_rule_id == values.get("aggregation_rule_id")
        and result.weighting_rule_id == values.get("weighting_rule_id")
        and ("stratum_id_when_applicable" not in present or values.get("stratum_id_when_applicable") is None or result.stratum_id == values.get("stratum_id_when_applicable"))
    )


def evaluation_claim_record_from_mapping(
    mapping: object,
    result_records: object,
) -> tuple[
    EvaluationClaimRecord | None,
    EvaluationClaimValidationResult,
]:
    code = EvaluationClaimValidationCode
    missing = (code.MISSING_REQUIRED_FIELD,) * len(_REQUIRED_MAPPING_KEYS)
    if not isinstance(mapping, Mapping):
        return None, _result(missing)
    try:
        items = tuple(mapping.items())
        keys: list[object] = []
        for item in items:
            key, value = item
            hash(key)
            if any(key == prior for prior in keys):
                return None, _result(missing)
            keys.append(key)
            hash(value) if False else None
        values = dict(items)
    except Exception:
        return None, _result(missing)

    exact = {key for key in keys if type(key) is str}
    codes: list[EvaluationClaimValidationCode] = [code.MISSING_REQUIRED_FIELD for key in _REQUIRED_MAPPING_KEYS if key not in exact]
    allowed = set(_REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS)
    codes.extend(code.UNEXPECTED_FIELD for key in sorted(key for key in exact if key not in allowed))
    codes.extend(code.UNEXPECTED_FIELD for key in keys if type(key) is not str)

    adapted = {key: values[key] for key in exact if key in allowed}
    enum_fields = (
        ("claim_class", EvaluationClaimClass, code.INVALID_CLAIM_CLASS),
        ("claim_disposition", EvaluationClaimDisposition, code.INVALID_CLAIM_DISPOSITION),
        ("baseline_type_when_applicable", BaselineType, code.INVALID_BASELINE_TYPE),
        ("prediction_representation", ScoringPredictionRepresentation, code.INVALID_PREDICTION_REPRESENTATION),
    )
    for field, enum_type, invalid_code in enum_fields:
        if field not in adapted or (field == "baseline_type_when_applicable" and adapted[field] is None):
            continue
        value = adapted[field]
        if type(value) is enum_type:
            continue
        if type(value) is str:
            try:
                adapted[field] = enum_type(value)
                continue
            except ValueError:
                pass
    for field in _LIST_TO_TUPLE_FIELDS:
        if field in adapted and type(adapted[field]) is list:
            adapted[field] = tuple(adapted[field])

    context = result_records
    context_invalid = False
    if type(context) is list:
        if all(type(item) is EvaluationResultRecord for item in context):
            context = tuple(context)
        else:
            context_invalid = True
    elif type(context) is not tuple:
        context_invalid = True

    semantic = _validate_claim_values(adapted, set(adapted), context if not context_invalid else object())
    combined = tuple(codes) + semantic
    if context_invalid and code.INVALID_RESULT_RECORD_CONTAINER not in combined:
        combined += (code.INVALID_RESULT_RECORD_CONTAINER,)
    if combined:
        return None, _result(combined)
    record = EvaluationClaimRecord(**adapted)
    return record, _result(())


def _validate_claim_values(
    values: Mapping[str, object],
    present: set[str],
    result_records: object,
) -> tuple[EvaluationClaimValidationCode, ...]:
    code = EvaluationClaimValidationCode
    codes: list[EvaluationClaimValidationCode] = []

    for field in _REQUIRED_TEXT_FIELDS:
        if field in present and not _valid_text(values.get(field)):
            codes.append(code.BLANK_REQUIRED_TEXT)
    for field in _NULLABLE_TEXT_FIELDS:
        value = values.get(field)
        if field in present and value is not None and not _valid_text(value):
            codes.append(code.BLANK_REQUIRED_TEXT)

    valid_class = "claim_class" in present and type(values.get("claim_class")) is EvaluationClaimClass
    if "claim_class" in present and not valid_class:
        codes.append(code.INVALID_CLAIM_CLASS)
    valid_disposition = "claim_disposition" in present and type(values.get("claim_disposition")) is EvaluationClaimDisposition
    if "claim_disposition" in present and not valid_disposition:
        codes.append(code.INVALID_CLAIM_DISPOSITION)
    valid_baseline = "baseline_type_when_applicable" in present and (values.get("baseline_type_when_applicable") is None or type(values.get("baseline_type_when_applicable")) is BaselineType)
    if "baseline_type_when_applicable" in present and not valid_baseline:
        codes.append(code.INVALID_BASELINE_TYPE)
    valid_representation = "prediction_representation" in present and type(values.get("prediction_representation")) is ScoringPredictionRepresentation
    if "prediction_representation" in present and not valid_representation:
        codes.append(code.INVALID_PREDICTION_REPRESENTATION)
    if "target_posture" in present and (type(values.get("target_posture")) is not str or values.get("target_posture") != _FIXED_TARGET_POSTURE):
        codes.append(code.INVALID_FIXED_POSTURE)

    ids_valid = "metric_or_diagnostic_ids" in present and _valid_unique_text_tuple(values.get("metric_or_diagnostic_ids"), nonempty=True)
    versions_valid = "metric_or_diagnostic_versions" in present and _valid_metric_versions(values.get("metric_or_diagnostic_versions"))
    if "metric_or_diagnostic_ids" in present and not ids_valid:
        codes.append(code.INVALID_METRIC_IDENTITY_TUPLE)
    if "metric_or_diagnostic_versions" in present and not versions_valid:
        codes.append(code.INVALID_METRIC_IDENTITY_TUPLE)
    if ids_valid and versions_valid and len(values.get("metric_or_diagnostic_ids")) != len(values.get("metric_or_diagnostic_versions")):
        codes.append(code.METRIC_VERSION_LENGTH_MISMATCH)
    required_valid = "required_evaluation_result_ids" in present and _valid_unique_text_tuple(values.get("required_evaluation_result_ids"), nonempty=True)
    observed_valid = "observed_evaluation_result_ids" in present and _valid_unique_text_tuple(values.get("observed_evaluation_result_ids"), nonempty=False)
    missing_valid = "missing_evaluation_result_ids" in present and _valid_unique_text_tuple(values.get("missing_evaluation_result_ids"), nonempty=False)
    if "required_evaluation_result_ids" in present and not required_valid:
        codes.append(code.INVALID_REQUIRED_RESULT_IDS)
    if "observed_evaluation_result_ids" in present and not observed_valid:
        codes.append(code.INVALID_OBSERVED_RESULT_IDS)
    if "missing_evaluation_result_ids" in present and not missing_valid:
        codes.append(code.INVALID_MISSING_RESULT_IDS)
    partition_valid = False
    if required_valid and observed_valid and missing_valid:
        required = values.get("required_evaluation_result_ids")
        observed = values.get("observed_evaluation_result_ids")
        missing_ids = values.get("missing_evaluation_result_ids")
        partition_valid = (
            tuple(item for item in required if item in observed) == observed
            and tuple(item for item in required if item in missing_ids) == missing_ids
            and set(observed).isdisjoint(missing_ids)
            and set(observed) | set(missing_ids) == set(required)
        )
        if not partition_valid:
            codes.append(code.RESULT_SET_PARTITION_MISMATCH)

    context_valid = type(result_records) is tuple
    valid_context: list[EvaluationResultRecord] = []
    if not context_valid:
        codes.append(code.INVALID_RESULT_RECORD_CONTAINER)
    else:
        for item in result_records:
            if type(item) is not EvaluationResultRecord or not validate_evaluation_result_record(item).passed:
                codes.append(code.INVALID_RESULT_RECORD)
            else:
                valid_context.append(item)

    by_id: dict[str, list[EvaluationResultRecord]] = {}
    for item in valid_context:
        bucket = by_id.setdefault(item.evaluation_result_id, [])
        if bucket:
            codes.append(code.DUPLICATE_CONTEXT_RESULT_ID)
        bucket.append(item)

    resolved: list[EvaluationResultRecord] = []
    if observed_valid:
        for identity in values.get("observed_evaluation_result_ids"):
            matches = by_id.get(identity, ())
            if len(matches) != 1:
                codes.append(code.OBSERVED_RESULT_NOT_FOUND)
            else:
                resolved.append(matches[0])

    referenced_ids: set[str] = set()
    for item in resolved:
        if item.result_kind is EvaluationResultKind.PAIRED_COMPARISON_RESULT and type(item.result_payload) is PairedComparisonResultPayload:
            referenced_ids.add(item.result_payload.candidate_result_id)
            referenced_ids.add(item.result_payload.baseline_result_id)
    observed_set = set(values.get("observed_evaluation_result_ids")) if observed_valid else set()
    for item in valid_context:
        if item.evaluation_result_id not in observed_set and item.evaluation_result_id not in referenced_ids:
            codes.append(code.UNEXPECTED_CONTEXT_RESULT)

    paired_refs: list[tuple[EvaluationResultRecord, EvaluationResultRecord | None, EvaluationResultRecord | None]] = []
    for item in resolved:
        if item.result_kind is not EvaluationResultKind.PAIRED_COMPARISON_RESULT or item.method_role is not EvaluationResultMethodRole.PAIRED_COMPARISON or type(item.result_payload) is not PairedComparisonResultPayload:
            continue
        candidate_matches = by_id.get(item.result_payload.candidate_result_id, ())
        baseline_matches = by_id.get(item.result_payload.baseline_result_id, ())
        candidate = candidate_matches[0] if len(candidate_matches) == 1 else None
        baseline = baseline_matches[0] if len(baseline_matches) == 1 else None
        if candidate is None:
            codes.append(code.PAIRED_REFERENCE_NOT_FOUND)
        if baseline is None:
            codes.append(code.PAIRED_REFERENCE_NOT_FOUND)
        paired_refs.append((item, candidate, baseline))

    for item in resolved:
        if "target_posture" in present and item.target_posture != values.get("target_posture"):
            codes.append(code.RESULT_TARGET_MISMATCH)
    for item in resolved:
        if valid_representation and item.prediction_representation is not values.get("prediction_representation"):
            codes.append(code.RESULT_REPRESENTATION_MISMATCH)
    if valid_class and valid_representation:
        required_representation = {
            EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
            EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR: ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION,
            EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR: ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE,
            EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL: ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION,
        }.get(values.get("claim_class"))
        if required_representation is not None and values.get("prediction_representation") is not required_representation:
            codes.append(code.RESULT_REPRESENTATION_MISMATCH)
    refs_by_observed = {id(item): (candidate, baseline) for item, candidate, baseline in paired_refs}
    for item in resolved:
        if not _scope_matches(values, present, item):
            codes.append(code.RESULT_SCOPE_MISMATCH)
        candidate, baseline = refs_by_observed.get(id(item), (None, None))
        if candidate is not None and not _scope_matches(values, present, candidate):
            codes.append(code.RESULT_SCOPE_MISMATCH)
        if baseline is not None and not _scope_matches(values, present, baseline):
            codes.append(code.RESULT_SCOPE_MISMATCH)

    artifacts: list[tuple[str, str]] = []
    for item in resolved:
        pair = (item.artifact_id.value, item.artifact_version)
        if pair not in artifacts:
            artifacts.append(pair)
    if resolved and ids_valid and versions_valid and (
        tuple(pair[0] for pair in artifacts) != values.get("metric_or_diagnostic_ids")
        or tuple(pair[1] for pair in artifacts) != values.get("metric_or_diagnostic_versions")
    ):
        codes.append(code.RESULT_METRIC_MISMATCH)

    candidate_identity_present = {"candidate_method_id", "candidate_method_version"} <= present
    if valid_class and candidate_identity_present and values.get("claim_class") in _NON_PAIRED_CLASSES:
        for item in resolved:
            if item.method_role is not EvaluationResultMethodRole.CANDIDATE or item.method_id != values.get("candidate_method_id") or item.method_version != values.get("candidate_method_version"):
                codes.append(code.CANDIDATE_IDENTITY_MISMATCH)
    if valid_class and candidate_identity_present and values.get("claim_class") in _PAIRED_CLASSES:
        for item, candidate, baseline in paired_refs:
            if candidate is not None and baseline is not None and (candidate.method_role is not EvaluationResultMethodRole.CANDIDATE or candidate.method_id != values.get("candidate_method_id") or candidate.method_version != values.get("candidate_method_version")):
                codes.append(code.CANDIDATE_IDENTITY_MISMATCH)
    if valid_class and values.get("claim_class") in _PAIRED_CLASSES:
        for item, candidate, baseline in paired_refs:
            if candidate is None or baseline is None:
                continue
            payload = item.result_payload
            expected_role = EvaluationResultMethodRole.CLIMATOLOGY_BASELINE if payload.baseline_type is BaselineType.CLIMATOLOGY else EvaluationResultMethodRole.PERSISTENCE_BASELINE
            if (
                baseline.method_role is not expected_role
                or (values.get("claim_class") is not EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES and "baseline_method_id_when_applicable" in present and baseline.method_id != values.get("baseline_method_id_when_applicable"))
                or (values.get("claim_class") is not EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES and "baseline_method_version_when_applicable" in present and baseline.method_version != values.get("baseline_method_version_when_applicable"))
            ):
                codes.append(code.BASELINE_IDENTITY_MISMATCH)

    if valid_class:
        allowed = _ALLOWED_RESULT_KINDS[values.get("claim_class")]
        for item in resolved:
            if item.result_kind not in allowed:
                codes.append(code.RESULT_KIND_NOT_ALLOWED)
        kinds = tuple(item.result_kind for item in resolved)
        if resolved and values.get("claim_class") is EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR and (
            EvaluationResultKind.CALIBRATION_BIN_RESULT not in kinds
            or not any(kind in (EvaluationResultKind.SCALAR_SCORE_RESULT, EvaluationResultKind.DECOMPOSITION_RESULT) for kind in kinds)
        ):
            codes.append(code.RESULT_KIND_NOT_ALLOWED)
        if resolved and values.get("claim_class") is EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR and (
            EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT not in kinds or EvaluationResultKind.SCALAR_SCORE_RESULT not in kinds
        ):
            codes.append(code.RESULT_KIND_NOT_ALLOWED)
        if values.get("claim_class") is EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL:
            for item in resolved:
                if item.artifact_id is not ScoringArtifact.THRESHOLD_WEIGHTED_CRPS:
                    codes.append(code.RESULT_KIND_NOT_ALLOWED)

    if valid_class:
        absent = values.get("claim_class") in (
            EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES,
            *_NON_PAIRED_CLASSES,
        )
        if absent:
            if valid_baseline and values.get("baseline_type_when_applicable") is not None:
                codes.append(code.BASELINE_REQUIREMENT_MISMATCH)
            if "baseline_method_id_when_applicable" in present and values.get("baseline_method_id_when_applicable") is not None and _valid_text(values.get("baseline_method_id_when_applicable")):
                codes.append(code.BASELINE_REQUIREMENT_MISMATCH)
            if "baseline_method_version_when_applicable" in present and values.get("baseline_method_version_when_applicable") is not None and _valid_text(values.get("baseline_method_version_when_applicable")):
                codes.append(code.BASELINE_REQUIREMENT_MISMATCH)
        else:
            expected_type = None
            if values.get("claim_class") is EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL:
                expected_type = BaselineType.CLIMATOLOGY
            elif values.get("claim_class") is EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL:
                expected_type = BaselineType.PERSISTENCE
            if valid_baseline and (values.get("baseline_type_when_applicable") is None or (expected_type is not None and values.get("baseline_type_when_applicable") is not expected_type)):
                codes.append(code.BASELINE_REQUIREMENT_MISMATCH)
            if "baseline_method_id_when_applicable" in present and not _valid_text(values.get("baseline_method_id_when_applicable")):
                codes.append(code.BASELINE_REQUIREMENT_MISMATCH)
            if "baseline_method_version_when_applicable" in present and not _valid_text(values.get("baseline_method_version_when_applicable")):
                codes.append(code.BASELINE_REQUIREMENT_MISMATCH)
        for item, _, _ in paired_refs:
            payload_type = item.result_payload.baseline_type
            expected_family = None
            if values.get("claim_class") is EvaluationClaimClass.CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL:
                expected_family = BaselineType.CLIMATOLOGY
            elif values.get("claim_class") is EvaluationClaimClass.CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL:
                expected_family = BaselineType.PERSISTENCE
            elif values.get("claim_class") in (EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL, EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL) and valid_baseline:
                expected_family = values.get("baseline_type_when_applicable")
            if expected_family is not None and payload_type is not expected_family:
                codes.append(code.BASELINE_REQUIREMENT_MISMATCH)

    baseline_families = {
        item.result_payload.baseline_type for item, _, _ in paired_refs
        if type(item.result_payload) is PairedComparisonResultPayload
    }
    if valid_class and values.get("claim_class") is EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES and paired_refs and baseline_families != {BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE}:
        codes.append(code.CROSS_BASELINE_INCOMPLETE)

    if valid_class and values.get("claim_class") is EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL:
        if "stratum_id_when_applicable" in present and not _valid_text(values.get("stratum_id_when_applicable")):
            codes.append(code.STRATUM_REQUIREMENT_MISMATCH)
        elif "stratum_id_when_applicable" in present and (any(item.stratum_id != values.get("stratum_id_when_applicable") for item in resolved) or any(
            ref is not None and ref.stratum_id != values.get("stratum_id_when_applicable")
            for _, candidate, baseline in paired_refs for ref in (candidate, baseline)
        )):
            codes.append(code.STRATUM_REQUIREMENT_MISMATCH)

    consumed: list[EvaluationResultRecord] = list(resolved)
    for _, candidate, baseline in paired_refs:
        for referenced in (candidate, baseline):
            if referenced is not None and referenced not in consumed:
                consumed.append(referenced)
    statuses = tuple(item.support_status for item in consumed)
    if valid_disposition:
        expected = None
        if EvaluationResultSupportStatus.BLOCKED in statuses:
            expected = EvaluationClaimDisposition.CLAIM_BLOCKED
        elif values.get("claim_disposition") is EvaluationClaimDisposition.CLAIM_BLOCKED and _valid_text(values.get("claim_disposition_reason")):
            expected = EvaluationClaimDisposition.CLAIM_BLOCKED
        elif (missing_valid and bool(values.get("missing_evaluation_result_ids"))) or EvaluationResultSupportStatus.UNAVAILABLE in statuses:
            expected = EvaluationClaimDisposition.CLAIM_UNAVAILABLE
        elif EvaluationResultSupportStatus.INSUFFICIENT in statuses:
            expected = EvaluationClaimDisposition.CLAIM_INSUFFICIENT
        if expected is not None and values.get("claim_disposition") is not expected:
            codes.append(code.DISPOSITION_PRECEDENCE_MISMATCH)
        if values.get("claim_disposition") in (EvaluationClaimDisposition.CLAIM_SUPPORTED, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED):
            complete_support = partition_valid and not values.get("missing_evaluation_result_ids") and len(resolved) == len(values.get("observed_evaluation_result_ids")) and all(status is EvaluationResultSupportStatus.SUPPORTED for status in statuses)
            multiplicity_will_fail = valid_class and ids_valid and (len(values.get("metric_or_diagnostic_ids")) > 1 or values.get("claim_class") in (EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES, EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL)) and "multiple_comparison_policy_id_when_applicable" in present and not _valid_text(values.get("multiple_comparison_policy_id_when_applicable"))
            provenance_will_fail = "provenance" in present and (type(values.get("provenance")) is not tuple or not values.get("provenance") or any(not _valid_text(item) for item in values.get("provenance") if type(values.get("provenance")) is tuple))
            timestamp_will_fail = "claim_created_at" in present and not _valid_timestamp(values.get("claim_created_at"))
            supersession_will_fail = {"evaluation_claim_id", "supersedes_claim_id_when_applicable"} <= present and _valid_text(values.get("evaluation_claim_id")) and _valid_text(values.get("supersedes_claim_id_when_applicable")) and values.get("evaluation_claim_id") == values.get("supersedes_claim_id_when_applicable")
            if not complete_support or bool(codes) or multiplicity_will_fail or provenance_will_fail or timestamp_will_fail or supersession_will_fail:
                codes.append(code.SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT)
        if "evidence_gate_eligibility_posture" in present and values.get("evidence_gate_eligibility_posture") != _EVIDENCE_GATE_MATRIX[values.get("claim_disposition")]:
            codes.append(code.INVALID_EVIDENCE_GATE_POSTURE)

    multiplicity_required = valid_class and ids_valid and (
        len(values.get("metric_or_diagnostic_ids")) > 1
        or values.get("claim_class") is EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES
        or values.get("claim_class") is EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL
    )
    if multiplicity_required and "multiple_comparison_policy_id_when_applicable" in present and not _valid_text(values.get("multiple_comparison_policy_id_when_applicable")):
        codes.append(code.INVALID_MULTIPLE_COMPARISON_POSTURE)

    if "provenance" in present and type(values.get("provenance")) is not tuple:
        codes.append(code.INVALID_PROVENANCE_REF)
    elif "provenance" in present and not values.get("provenance"):
        codes.append(code.EMPTY_PROVENANCE)
    elif "provenance" in present:
        for value in values.get("provenance"):
            if not _valid_text(value):
                codes.append(code.INVALID_PROVENANCE_REF)
    if "claim_created_at" in present and not _valid_timestamp(values.get("claim_created_at")):
        codes.append(code.INVALID_CLAIM_CREATED_AT)
    if {"evaluation_claim_id", "supersedes_claim_id_when_applicable"} <= present and _valid_text(values.get("evaluation_claim_id")) and _valid_text(values.get("supersedes_claim_id_when_applicable")) and values.get("evaluation_claim_id") == values.get("supersedes_claim_id_when_applicable"):
        codes.append(code.SELF_SUPERSESSION)
    return tuple(codes)


def validate_evaluation_claim_record(
    record: EvaluationClaimRecord,
    result_records: tuple[EvaluationResultRecord, ...],
) -> EvaluationClaimValidationResult:
    field_names = _REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS
    values = {field: getattr(record, field) for field in field_names}
    return _result(_validate_claim_values(values, set(field_names), result_records))
