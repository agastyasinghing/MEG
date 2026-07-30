"""Immutable Stage 3 evaluation-result records and pure validation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import math
import re

from meg.weather.stage3.baseline_contracts import BaselineType
from meg.weather.stage3.scoring_and_diagnostics import (
    ScoringArtifact,
    ScoringPredictionRepresentation,
)

__all__ = (
    "EvaluationResultKind",
    "EvaluationResultSupportStatus",
    "EvaluationResultMethodRole",
    "EvaluationResultValidationSeverity",
    "EvaluationResultValidationCode",
    "ScalarScoreResultPayload",
    "CalibrationBinResultPayload",
    "DecompositionResultPayload",
    "DistributionDiagnosticResultPayload",
    "EnsembleDiagnosticResultPayload",
    "PairedComparisonResultPayload",
    "EvaluationResultRecord",
    "EvaluationResultValidationResult",
    "evaluation_result_record_from_mapping",
    "validate_evaluation_result_record",
)


class EvaluationResultKind(StrEnum):
    SCALAR_SCORE_RESULT = "scalar_score_result"
    CALIBRATION_BIN_RESULT = "calibration_bin_result"
    DECOMPOSITION_RESULT = "decomposition_result"
    DISTRIBUTION_DIAGNOSTIC_RESULT = "distribution_diagnostic_result"
    ENSEMBLE_DIAGNOSTIC_RESULT = "ensemble_diagnostic_result"
    PAIRED_COMPARISON_RESULT = "paired_comparison_result"


class EvaluationResultSupportStatus(StrEnum):
    SUPPORTED = "supported"
    INSUFFICIENT = "insufficient"
    BLOCKED = "blocked"
    UNAVAILABLE = "unavailable"


class EvaluationResultMethodRole(StrEnum):
    CANDIDATE = "candidate"
    CLIMATOLOGY_BASELINE = "climatology_baseline"
    PERSISTENCE_BASELINE = "persistence_baseline"
    PAIRED_COMPARISON = "paired_comparison"


class EvaluationResultValidationSeverity(StrEnum):
    PASSED = "passed"
    BLOCKED = "blocked"


class EvaluationResultValidationCode(StrEnum):
    MISSING_REQUIRED_FIELD = "missing_required_field"
    UNEXPECTED_FIELD = "unexpected_field"
    BLANK_REQUIRED_TEXT = "blank_required_text"
    INVALID_RESULT_KIND = "invalid_result_kind"
    INVALID_ARTIFACT = "invalid_artifact"
    INVALID_METHOD_ROLE = "invalid_method_role"
    INVALID_PREDICTION_REPRESENTATION = "invalid_prediction_representation"
    INVALID_SUPPORT_STATUS = "invalid_support_status"
    INVALID_FIXED_POSTURE = "invalid_fixed_posture"
    INVALID_RECORD_COUNT = "invalid_record_count"
    SAMPLE_ACCOUNTING_MISMATCH = "sample_accounting_mismatch"
    INVALID_REASON_SUMMARY = "invalid_reason_summary"
    MISSING_REQUIRED_REASON = "missing_required_reason"
    UNCERTAINTY_FIELDS_MISMATCH = "uncertainty_fields_mismatch"
    EMPTY_PROVENANCE = "empty_provenance"
    INVALID_PROVENANCE_REF = "invalid_provenance_ref"
    INVALID_RESULT_CREATED_AT = "invalid_result_created_at"
    RESULT_KIND_ARTIFACT_MISMATCH = "result_kind_artifact_mismatch"
    REPRESENTATION_MISMATCH = "representation_mismatch"
    METHOD_ROLE_MISMATCH = "method_role_mismatch"
    INVALID_PAYLOAD_TYPE = "invalid_payload_type"
    INVALID_SCALAR_SCORE_PAYLOAD = "invalid_scalar_score_payload"
    INVALID_CALIBRATION_BIN_PAYLOAD = "invalid_calibration_bin_payload"
    INVALID_DECOMPOSITION_PAYLOAD = "invalid_decomposition_payload"
    INVALID_DISTRIBUTION_DIAGNOSTIC_PAYLOAD = "invalid_distribution_diagnostic_payload"
    INVALID_ENSEMBLE_DIAGNOSTIC_PAYLOAD = "invalid_ensemble_diagnostic_payload"
    INVALID_PAIRED_COMPARISON_PAYLOAD = "invalid_paired_comparison_payload"
    PAIR_BASELINE_NOT_APPROVED = "pair_baseline_not_approved"
    PAIR_RESULT_IDENTITY_COLLISION = "pair_result_identity_collision"
    SELF_SUPERSESSION = "self_supersession"


@dataclass(frozen=True)
class ScalarScoreResultPayload:
    result_value: float
    score_direction: str
    result_domain_posture: str


@dataclass(frozen=True)
class CalibrationBinResultPayload:
    bin_id: str
    bin_index: int
    bin_boundary_policy_id: str
    sample_count: int
    mean_predicted_probability: float
    observed_outcome_frequency: float
    ordered_bin_posture: str


@dataclass(frozen=True)
class DecompositionResultPayload:
    decomposition_policy_id: str
    reliability_value: float
    resolution_value: float
    uncertainty_value: float
    component_posture: str


@dataclass(frozen=True)
class DistributionDiagnosticResultPayload:
    pit_treatment_policy_id: str
    ordered_bin_ids: tuple[str, ...]
    ordered_bin_counts: tuple[int, ...]
    ordered_content_posture: str


@dataclass(frozen=True)
class EnsembleDiagnosticResultPayload:
    tie_treatment_policy_id: str
    ordered_rank_ids: tuple[str, ...]
    ordered_rank_counts: tuple[int, ...]
    ensemble_comparability_posture: str
    ordered_content_posture: str


@dataclass(frozen=True)
class PairedComparisonResultPayload:
    candidate_result_id: str
    baseline_result_id: str
    baseline_type: BaselineType
    comparison_direction: str
    paired_comparison_value: float
    paired_scope_posture: str


@dataclass(frozen=True)
class EvaluationResultRecord:
    evaluation_result_id: str
    result_kind: EvaluationResultKind
    artifact_id: ScoringArtifact
    artifact_version: str
    evaluation_definition_id: str
    evaluation_definition_version: str
    evaluation_run_id: str
    method_role: EvaluationResultMethodRole
    method_id: str
    method_version: str
    prediction_representation: ScoringPredictionRepresentation
    target_posture: str
    split_id: str
    split_version: str
    fold_id: str
    cutoff_identity: str
    paired_test_record_set_id: str
    eligibility_policy_id: str
    aggregation_rule_id: str
    weighting_rule_id: str
    stratum_id: str
    eligible_record_count: int
    excluded_record_count: int
    blocked_record_count: int
    total_considered_record_count: int
    exclusion_block_reason_summary: tuple[str, ...]
    uncertainty_method_id: str | None
    uncertainty_level_id: str | None
    support_status: EvaluationResultSupportStatus
    result_payload: ScalarScoreResultPayload | CalibrationBinResultPayload | DecompositionResultPayload | DistributionDiagnosticResultPayload | EnsembleDiagnosticResultPayload | PairedComparisonResultPayload
    provenance: tuple[str, ...]
    result_created_at: str
    supersedes_result_id_when_applicable: str | None = None


@dataclass(frozen=True)
class EvaluationResultValidationResult:
    severity: EvaluationResultValidationSeverity
    passed: bool
    codes: tuple[EvaluationResultValidationCode, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "codes", tuple(self.codes))
        if self.codes:
            object.__setattr__(self, "severity", EvaluationResultValidationSeverity.BLOCKED)
            object.__setattr__(self, "passed", False)
        else:
            object.__setattr__(self, "severity", EvaluationResultValidationSeverity.PASSED)
            object.__setattr__(self, "passed", True)
            object.__setattr__(self, "codes", ())


_REQUIRED_MAPPING_KEYS = (
    "evaluation_result_id", "result_kind", "artifact_id", "artifact_version",
    "evaluation_definition_id", "evaluation_definition_version", "evaluation_run_id",
    "method_role", "method_id", "method_version", "prediction_representation",
    "target_posture", "split_id", "split_version", "fold_id", "cutoff_identity",
    "paired_test_record_set_id", "eligibility_policy_id", "aggregation_rule_id",
    "weighting_rule_id", "stratum_id", "eligible_record_count", "excluded_record_count",
    "blocked_record_count", "total_considered_record_count",
    "exclusion_block_reason_summary", "uncertainty_method_id", "uncertainty_level_id",
    "support_status", "result_payload", "provenance", "result_created_at",
)
_OPTIONAL_MAPPING_KEYS = ("supersedes_result_id_when_applicable",)
_REQUIRED_TEXT_FIELDS = (
    "evaluation_result_id", "artifact_version", "evaluation_definition_id",
    "evaluation_definition_version", "evaluation_run_id", "method_id", "method_version",
    "target_posture", "split_id", "split_version", "fold_id", "cutoff_identity",
    "paired_test_record_set_id", "eligibility_policy_id", "aggregation_rule_id",
    "weighting_rule_id", "stratum_id", "result_created_at",
)
_NULLABLE_TEXT_FIELDS = (
    "uncertainty_method_id", "uncertainty_level_id", "supersedes_result_id_when_applicable",
)
_COUNT_FIELDS = (
    "eligible_record_count", "excluded_record_count", "blocked_record_count",
    "total_considered_record_count",
)
_RESULT_KIND_ARTIFACT_PAYLOAD_MATRIX = {
    EvaluationResultKind.SCALAR_SCORE_RESULT: ((ScoringArtifact.BRIER_SCORE, ScoringArtifact.LOG_SCORE, ScoringArtifact.CRPS, ScoringArtifact.THRESHOLD_WEIGHTED_CRPS), ScalarScoreResultPayload),
    EvaluationResultKind.CALIBRATION_BIN_RESULT: ((ScoringArtifact.RELIABILITY_DIAGRAM,), CalibrationBinResultPayload),
    EvaluationResultKind.DECOMPOSITION_RESULT: ((ScoringArtifact.BRIER_DECOMPOSITION,), DecompositionResultPayload),
    EvaluationResultKind.DISTRIBUTION_DIAGNOSTIC_RESULT: ((ScoringArtifact.PIT_HISTOGRAM,), DistributionDiagnosticResultPayload),
    EvaluationResultKind.ENSEMBLE_DIAGNOSTIC_RESULT: ((ScoringArtifact.RANK_HISTOGRAM,), EnsembleDiagnosticResultPayload),
    EvaluationResultKind.PAIRED_COMPARISON_RESULT: ((ScoringArtifact.BRIER_SCORE, ScoringArtifact.LOG_SCORE, ScoringArtifact.CRPS, ScoringArtifact.THRESHOLD_WEIGHTED_CRPS), PairedComparisonResultPayload),
}
_REPRESENTATION_MATRIX = {
    ScoringArtifact.BRIER_SCORE: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
    ScoringArtifact.LOG_SCORE: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
    ScoringArtifact.RELIABILITY_DIAGRAM: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
    ScoringArtifact.BRIER_DECOMPOSITION: ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY,
    ScoringArtifact.CRPS: ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION,
    ScoringArtifact.PIT_HISTOGRAM: ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION,
    ScoringArtifact.RANK_HISTOGRAM: ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE,
    ScoringArtifact.THRESHOLD_WEIGHTED_CRPS: ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION,
}
_METHOD_ROLE_MATRIX = {
    kind: ((EvaluationResultMethodRole.PAIRED_COMPARISON,) if kind is EvaluationResultKind.PAIRED_COMPARISON_RESULT else (EvaluationResultMethodRole.CANDIDATE, EvaluationResultMethodRole.CLIMATOLOGY_BASELINE, EvaluationResultMethodRole.PERSISTENCE_BASELINE))
    for kind in EvaluationResultKind
}
_VALIDATION_GROUPS = (
    "missing keys", "unexpected exact-string keys", "unexpected non-string keys",
    "required and nullable text", "result kind", "artifact", "method role",
    "prediction representation", "support status", "fixed posture", "counts",
    "sample-accounting identity", "reason-summary structure",
    "required-reason consistency", "uncertainty pairing", "provenance",
    "result-created timestamp", "result-kind/artifact compatibility",
    "representation compatibility", "method-role compatibility", "payload type",
    "payload content", "paired baseline", "paired identity collision", "self-supersession",
)


def _result(codes: list[EvaluationResultValidationCode] | tuple[EvaluationResultValidationCode, ...]) -> EvaluationResultValidationResult:
    return EvaluationResultValidationResult(EvaluationResultValidationSeverity.BLOCKED, False, tuple(codes))


def _missing_result() -> EvaluationResultValidationResult:
    return _result((EvaluationResultValidationCode.MISSING_REQUIRED_FIELD,) * 32)


def _valid_text(value: object) -> bool:
    return type(value) is str and bool(value.strip())


def _valid_count(value: object) -> bool:
    return type(value) is int and value >= 0


def _valid_float(value: object) -> bool:
    return type(value) is float and math.isfinite(value)


def _valid_timestamp(value: object) -> bool:
    if type(value) is not str or "T" not in value:
        return False
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    if not value.endswith("Z") and re.search(r"[+-]\d{2}:\d{2}$", value) is None:
        return False
    try:
        parsed = datetime.fromisoformat(candidate)
        return parsed.utcoffset() is not None
    except (ValueError, OverflowError):
        return False


def _validate(values: Mapping[str, object], present: set[str]) -> list[EvaluationResultValidationCode]:
    code = EvaluationResultValidationCode
    codes: list[EvaluationResultValidationCode] = []
    for field in _REQUIRED_TEXT_FIELDS:
        if field in present and not _valid_text(values[field]):
            codes.append(code.BLANK_REQUIRED_TEXT)
    for field in _NULLABLE_TEXT_FIELDS:
        if field in present and values[field] is not None and not _valid_text(values[field]):
            codes.append(code.BLANK_REQUIRED_TEXT)

    kind = values.get("result_kind")
    valid_kind = type(kind) is EvaluationResultKind
    if "result_kind" in present and not valid_kind:
        codes.append(code.INVALID_RESULT_KIND)
    artifact = values.get("artifact_id")
    valid_artifact = type(artifact) is ScoringArtifact
    if "artifact_id" in present and not valid_artifact:
        codes.append(code.INVALID_ARTIFACT)
    role = values.get("method_role")
    valid_role = type(role) is EvaluationResultMethodRole
    if "method_role" in present and not valid_role:
        codes.append(code.INVALID_METHOD_ROLE)
    representation = values.get("prediction_representation")
    valid_representation = type(representation) is ScoringPredictionRepresentation
    if "prediction_representation" in present and not valid_representation:
        codes.append(code.INVALID_PREDICTION_REPRESENTATION)
    support = values.get("support_status")
    valid_support = type(support) is EvaluationResultSupportStatus
    if "support_status" in present and not valid_support:
        codes.append(code.INVALID_SUPPORT_STATUS)

    if "target_posture" in present and (type(values["target_posture"]) is not str or values["target_posture"] != "venue_defined_settlement_outcome"):
        codes.append(code.INVALID_FIXED_POSTURE)

    valid_counts = {field: field in present and _valid_count(values[field]) for field in _COUNT_FIELDS}
    for field in _COUNT_FIELDS:
        if field in present and not valid_counts[field]:
            codes.append(code.INVALID_RECORD_COUNT)
    if all(valid_counts.values()) and values["total_considered_record_count"] != values["eligible_record_count"] + values["excluded_record_count"] + values["blocked_record_count"]:
        codes.append(code.SAMPLE_ACCOUNTING_MISMATCH)

    reasons = values.get("exclusion_block_reason_summary")
    valid_reasons = "exclusion_block_reason_summary" in present and type(reasons) is tuple
    if valid_reasons:
        valid_reasons = all(_valid_text(item) for item in reasons) and len(set(reasons)) == len(reasons)
    if "exclusion_block_reason_summary" in present and not valid_reasons:
        codes.append(code.INVALID_REASON_SUMMARY)
    reason_prerequisites = valid_reasons and valid_counts["excluded_record_count"] and valid_counts["blocked_record_count"] and valid_support
    if reason_prerequisites and not reasons and (values["excluded_record_count"] > 0 or values["blocked_record_count"] > 0 or support in (EvaluationResultSupportStatus.INSUFFICIENT, EvaluationResultSupportStatus.BLOCKED, EvaluationResultSupportStatus.UNAVAILABLE)):
        codes.append(code.MISSING_REQUIRED_REASON)

    if "uncertainty_method_id" in present and "uncertainty_level_id" in present:
        method, level = values["uncertainty_method_id"], values["uncertainty_level_id"]
        if (method is None or _valid_text(method)) and (level is None or _valid_text(level)) and ((method is None) != (level is None)):
            codes.append(code.UNCERTAINTY_FIELDS_MISMATCH)

    if "provenance" in present:
        provenance = values["provenance"]
        if type(provenance) is not tuple:
            codes.append(code.INVALID_PROVENANCE_REF)
        elif not provenance:
            codes.append(code.EMPTY_PROVENANCE)
        else:
            codes.extend(code.INVALID_PROVENANCE_REF for ref in provenance if not _valid_text(ref))

    if "result_created_at" in present and not _valid_timestamp(values["result_created_at"]):
        codes.append(code.INVALID_RESULT_CREATED_AT)

    if valid_kind and valid_artifact and artifact not in _RESULT_KIND_ARTIFACT_PAYLOAD_MATRIX[kind][0]:
        codes.append(code.RESULT_KIND_ARTIFACT_MISMATCH)
    if valid_artifact and valid_representation and representation is not _REPRESENTATION_MATRIX[artifact]:
        codes.append(code.REPRESENTATION_MISMATCH)
    if valid_kind and valid_role and role not in _METHOD_ROLE_MATRIX[kind]:
        codes.append(code.METHOD_ROLE_MISMATCH)

    payload = values.get("result_payload")
    valid_payload = valid_kind and "result_payload" in present and type(payload) is _RESULT_KIND_ARTIFACT_PAYLOAD_MATRIX[kind][1]
    if valid_kind and "result_payload" in present and not valid_payload:
        codes.append(code.INVALID_PAYLOAD_TYPE)

    if valid_payload:
        eligible_valid = valid_counts["eligible_record_count"]
        if type(payload) is ScalarScoreResultPayload:
            valid = _valid_float(payload.result_value) and type(payload.score_direction) is str and payload.score_direction == "lower_is_better" and type(payload.result_domain_posture) is str and payload.result_domain_posture == "artifact_specific_domain_validated"
            if valid and valid_artifact and artifact in _RESULT_KIND_ARTIFACT_PAYLOAD_MATRIX[EvaluationResultKind.SCALAR_SCORE_RESULT][0]:
                valid = (0.0 <= payload.result_value <= 1.0) if artifact is ScoringArtifact.BRIER_SCORE else payload.result_value >= 0.0
            if not valid:
                codes.append(code.INVALID_SCALAR_SCORE_PAYLOAD)
        elif type(payload) is CalibrationBinResultPayload:
            valid = (_valid_text(payload.bin_id) and _valid_count(payload.bin_index) and _valid_text(payload.bin_boundary_policy_id) and _valid_count(payload.sample_count) and _valid_float(payload.mean_predicted_probability) and 0.0 <= payload.mean_predicted_probability <= 1.0 and _valid_float(payload.observed_outcome_frequency) and 0.0 <= payload.observed_outcome_frequency <= 1.0 and type(payload.ordered_bin_posture) is str and payload.ordered_bin_posture == "predeclared_order_required")
            if eligible_valid:
                valid = valid and payload.sample_count == values["eligible_record_count"]
            if not valid:
                codes.append(code.INVALID_CALIBRATION_BIN_PAYLOAD)
        elif type(payload) is DecompositionResultPayload:
            valid = _valid_text(payload.decomposition_policy_id) and all(_valid_float(item) and item >= 0.0 for item in (payload.reliability_value, payload.resolution_value, payload.uncertainty_value)) and type(payload.component_posture) is str and payload.component_posture == "reliability_resolution_uncertainty_required"
            if not valid:
                codes.append(code.INVALID_DECOMPOSITION_PAYLOAD)
        elif type(payload) is DistributionDiagnosticResultPayload:
            valid = _valid_text(payload.pit_treatment_policy_id) and type(payload.ordered_bin_ids) is tuple and type(payload.ordered_bin_counts) is tuple and bool(payload.ordered_bin_ids) and bool(payload.ordered_bin_counts) and len(payload.ordered_bin_ids) == len(payload.ordered_bin_counts) and all(_valid_text(item) for item in payload.ordered_bin_ids) and len(set(payload.ordered_bin_ids)) == len(payload.ordered_bin_ids) and all(_valid_count(item) for item in payload.ordered_bin_counts) and type(payload.ordered_content_posture) is str and payload.ordered_content_posture == "predeclared_order_required"
            if valid and eligible_valid:
                valid = sum(payload.ordered_bin_counts) == values["eligible_record_count"]
            if not valid:
                codes.append(code.INVALID_DISTRIBUTION_DIAGNOSTIC_PAYLOAD)
        elif type(payload) is EnsembleDiagnosticResultPayload:
            valid = _valid_text(payload.tie_treatment_policy_id) and type(payload.ordered_rank_ids) is tuple and type(payload.ordered_rank_counts) is tuple and bool(payload.ordered_rank_ids) and bool(payload.ordered_rank_counts) and len(payload.ordered_rank_ids) == len(payload.ordered_rank_counts) and all(_valid_text(item) for item in payload.ordered_rank_ids) and len(set(payload.ordered_rank_ids)) == len(payload.ordered_rank_ids) and all(_valid_count(item) for item in payload.ordered_rank_counts) and type(payload.ensemble_comparability_posture) is str and payload.ensemble_comparability_posture == "finite_comparable_ensemble_required" and type(payload.ordered_content_posture) is str and payload.ordered_content_posture == "predeclared_order_required"
            if valid and eligible_valid:
                valid = sum(payload.ordered_rank_counts) == values["eligible_record_count"]
            if not valid:
                codes.append(code.INVALID_ENSEMBLE_DIAGNOSTIC_PAYLOAD)
        else:
            candidate_valid = _valid_text(payload.candidate_result_id)
            baseline_valid = _valid_text(payload.baseline_result_id)
            valid = candidate_valid and baseline_valid and _valid_float(payload.paired_comparison_value) and type(payload.comparison_direction) is str and payload.comparison_direction == "candidate_minus_baseline_lower_is_better" and type(payload.paired_scope_posture) is str and payload.paired_scope_posture == "exact_common_test_record_set_required"
            if not valid:
                codes.append(code.INVALID_PAIRED_COMPARISON_PAYLOAD)

    if valid_payload and type(payload) is PairedComparisonResultPayload and type(payload.baseline_type) is not BaselineType:
        codes.append(code.PAIR_BASELINE_NOT_APPROVED)
    elif valid_payload and type(payload) is PairedComparisonResultPayload and payload.baseline_type not in (BaselineType.CLIMATOLOGY, BaselineType.PERSISTENCE):
        codes.append(code.PAIR_BASELINE_NOT_APPROVED)
    if valid_payload and type(payload) is PairedComparisonResultPayload and _valid_text(payload.candidate_result_id) and _valid_text(payload.baseline_result_id) and payload.candidate_result_id == payload.baseline_result_id:
        codes.append(code.PAIR_RESULT_IDENTITY_COLLISION)
    if "evaluation_result_id" in present and "supersedes_result_id_when_applicable" in present and _valid_text(values["evaluation_result_id"]) and _valid_text(values["supersedes_result_id_when_applicable"]) and values["evaluation_result_id"] == values["supersedes_result_id_when_applicable"]:
        codes.append(code.SELF_SUPERSESSION)
    return codes


def evaluation_result_record_from_mapping(
    mapping: object,
) -> tuple[
    EvaluationResultRecord | None,
    EvaluationResultValidationResult,
]:
    if not isinstance(mapping, Mapping):
        return None, _missing_result()
    try:
        items = list(mapping.items())
        seen: set[object] = set()
        for item in items:
            key, _ = item
            if key in seen:
                return None, _missing_result()
            seen.add(key)
        snapshot = dict(items)
        ordered_keys = [item[0] for item in items]
        values = {key: snapshot[key] for key in ordered_keys if type(key) is str and key in _REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS}
    except Exception:
        return None, _missing_result()

    present = set(values)
    codes = [EvaluationResultValidationCode.MISSING_REQUIRED_FIELD for key in _REQUIRED_MAPPING_KEYS if key not in present]
    unexpected_strings = sorted(key for key in ordered_keys if type(key) is str and key not in _REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS)
    codes.extend(EvaluationResultValidationCode.UNEXPECTED_FIELD for _ in unexpected_strings)
    codes.extend(EvaluationResultValidationCode.UNEXPECTED_FIELD for key in ordered_keys if type(key) is not str)
    for field, enum_type in (
        ("result_kind", EvaluationResultKind), ("artifact_id", ScoringArtifact),
        ("method_role", EvaluationResultMethodRole),
        ("prediction_representation", ScoringPredictionRepresentation),
        ("support_status", EvaluationResultSupportStatus),
    ):
        if field in present and type(values[field]) is str:
            try:
                values[field] = enum_type(values[field])
            except ValueError:
                pass
    for field in ("exclusion_block_reason_summary", "provenance"):
        if field in present and type(values[field]) is list:
            values[field] = tuple(values[field])
    codes.extend(_validate(values, present))
    if codes:
        return None, _result(codes)
    record = EvaluationResultRecord(**values)
    result = validate_evaluation_result_record(record)
    return (record if result.passed else None), result


def validate_evaluation_result_record(
    record: EvaluationResultRecord,
) -> EvaluationResultValidationResult:
    values = {field: getattr(record, field) for field in _REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS}
    return _result(_validate(values, set(values)))
