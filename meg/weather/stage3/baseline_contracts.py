"""Immutable Stage 3 baseline definitions and fail-closed validation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

__all__ = (
    "BaselineType",
    "BaselineDefinitionStatus",
    "BaselineValidationSeverity",
    "BaselineValidationCode",
    "BaselineContractDefinition",
    "BaselineContractValidationResult",
    "baseline_contract_definition_from_mapping",
    "validate_baseline_contract_definition",
)


class BaselineType(StrEnum):
    CLIMATOLOGY = "climatology"
    PERSISTENCE = "persistence"


class BaselineDefinitionStatus(StrEnum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class BaselineValidationSeverity(StrEnum):
    PASSED = "passed"
    BLOCKED = "blocked"


class BaselineValidationCode(StrEnum):
    MISSING_REQUIRED_FIELD = "missing_required_field"
    UNEXPECTED_FIELD = "unexpected_field"
    BLANK_REQUIRED_TEXT = "blank_required_text"
    INVALID_BASELINE_TYPE = "invalid_baseline_type"
    INVALID_DEFINITION_STATUS = "invalid_definition_status"
    INVALID_INTEGER_FIELD = "invalid_integer_field"
    INVALID_FIXED_POSTURE = "invalid_fixed_posture"
    INVALID_TIMESTAMP = "invalid_timestamp"
    INPUT_AVAILABLE_AFTER_PREDICTION = "input_available_after_prediction"
    PREDICTION_AFTER_FOLD_CUTOFF = "prediction_after_fold_cutoff"
    DEFINITION_DECLARED_AFTER_PREDICTION = "definition_declared_after_prediction"
    INVALID_CONDITIONING_DIMENSIONS = "invalid_conditioning_dimensions"
    EMPTY_AVAILABILITY_EVIDENCE_REFS = "empty_availability_evidence_refs"
    INVALID_AVAILABILITY_EVIDENCE_REF = "invalid_availability_evidence_ref"
    EMPTY_PROVENANCE_REFS = "empty_provenance_refs"
    INVALID_PROVENANCE_REF = "invalid_provenance_ref"
    CLIMATOLOGY_INVALID_INPUT_POSTURE = "climatology_invalid_input_posture"
    CLIMATOLOGY_MISSING_HISTORY_WINDOW = "climatology_missing_history_window"
    CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT = "climatology_persistence_fields_present"
    PERSISTENCE_INVALID_INPUT_POSTURE = "persistence_invalid_input_posture"
    PERSISTENCE_CONDITIONING_FIELDS_PRESENT = "persistence_conditioning_fields_present"
    PERSISTENCE_MISSING_QUANTITY = "persistence_missing_quantity"
    PERSISTENCE_MISSING_CONVERSION_RULE = "persistence_missing_conversion_rule"
    ACTIVE_WITH_EXCLUSION_REASON = "active_with_exclusion_reason"
    BLOCKED_WITHOUT_EXCLUSION_REASON = "blocked_without_exclusion_reason"
    SELF_SUPERSESSION = "self_supersession"


@dataclass(frozen=True)
class BaselineContractDefinition:
    baseline_definition_id: str
    baseline_type: BaselineType
    definition_status: BaselineDefinitionStatus
    baseline_version: str
    method_id: str
    method_version: str
    split_id: str
    split_version: str
    fold_id: str
    fold_index: int
    fold_cutoff: str
    prediction_as_of: str
    input_publication_available_at: str
    definition_declared_at: str
    condition_id: str
    token_id: str
    outcome: str
    settlement_rule_id: str
    settlement_rule_version: str
    source_compatibility_posture: str
    station_compatibility_posture: str
    threshold: str
    unit: str
    comparator: str
    measurement_window: str
    archive_finality_layer: str
    scoring_target_posture: str
    baseline_input_posture: str
    conditioning_dimensions: tuple[str, ...]
    smoothing_definition_id: str | None
    history_window_definition_id: str | None
    hierarchy_definition_id: str | None
    fallback_definition_id: str | None
    persisted_quantity_id: str | None
    conversion_rule_id: str | None
    split_parity_posture: str
    paired_comparison_posture: str
    availability_posture: str
    fallback_posture: str
    tuning_posture: str
    output_contract_posture: str
    market_price_posture: str
    baseline_execution_posture: str
    scoring_execution_posture: str
    storage_persistence_posture: str
    availability_evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    exclusion_reason: str | None
    supersedes_baseline_definition_id: str | None = None


@dataclass(frozen=True)
class BaselineContractValidationResult:
    severity: BaselineValidationSeverity
    passed: bool
    codes: tuple[BaselineValidationCode, ...] = ()

    def __post_init__(self) -> None:
        if self.codes:
            object.__setattr__(self, "severity", BaselineValidationSeverity.BLOCKED)
            object.__setattr__(self, "passed", False)
        else:
            object.__setattr__(self, "severity", BaselineValidationSeverity.PASSED)
            object.__setattr__(self, "passed", True)
            object.__setattr__(self, "codes", ())


_REQUIRED_MAPPING_KEYS = (
    "baseline_definition_id", "baseline_type", "definition_status", "baseline_version",
    "method_id", "method_version", "split_id", "split_version", "fold_id", "fold_index",
    "fold_cutoff", "prediction_as_of", "input_publication_available_at",
    "definition_declared_at", "condition_id", "token_id", "outcome", "settlement_rule_id",
    "settlement_rule_version", "source_compatibility_posture", "station_compatibility_posture",
    "threshold", "unit", "comparator", "measurement_window", "archive_finality_layer",
    "scoring_target_posture", "baseline_input_posture", "conditioning_dimensions",
    "smoothing_definition_id", "history_window_definition_id", "hierarchy_definition_id",
    "fallback_definition_id", "persisted_quantity_id", "conversion_rule_id",
    "split_parity_posture", "paired_comparison_posture", "availability_posture",
    "fallback_posture", "tuning_posture", "output_contract_posture", "market_price_posture",
    "baseline_execution_posture", "scoring_execution_posture", "storage_persistence_posture",
    "availability_evidence_refs", "provenance_refs", "exclusion_reason",
)
_OPTIONAL_MAPPING_KEYS = ("supersedes_baseline_definition_id",)
_REQUIRED_TEXT_FIELDS = (
    "baseline_definition_id", "baseline_version", "method_id", "method_version", "split_id",
    "split_version", "fold_id", "condition_id", "token_id", "outcome", "settlement_rule_id",
    "settlement_rule_version", "source_compatibility_posture", "station_compatibility_posture",
    "threshold", "unit", "comparator", "measurement_window", "archive_finality_layer",
    "scoring_target_posture", "baseline_input_posture", "split_parity_posture",
    "paired_comparison_posture", "availability_posture", "fallback_posture", "tuning_posture",
    "output_contract_posture", "market_price_posture", "baseline_execution_posture",
    "scoring_execution_posture", "storage_persistence_posture",
)
_NULLABLE_TEXT_FIELDS = (
    "smoothing_definition_id", "history_window_definition_id", "hierarchy_definition_id",
    "fallback_definition_id", "persisted_quantity_id", "conversion_rule_id", "exclusion_reason",
    "supersedes_baseline_definition_id",
)
_TIMESTAMP_FIELDS = (
    "fold_cutoff", "prediction_as_of", "input_publication_available_at", "definition_declared_at",
)
_FIXED_POSTURES = (
    ("scoring_target_posture", "venue_defined_settlement_outcome"),
    ("split_parity_posture", "same_folds_cutoffs_eligibility_and_test_records_required"),
    ("paired_comparison_posture", "common_test_record_set_required"),
    ("availability_posture", "point_in_time_required"),
    ("fallback_posture", "predeclared_compatible_or_fail_closed"),
    ("tuning_posture", "train_or_calibration_only"),
    ("output_contract_posture", "probability_record_contract_required"),
    ("market_price_posture", "not_approved_as_baseline"),
    ("baseline_execution_posture", "not_approved"),
    ("scoring_execution_posture", "not_approved"),
    ("storage_persistence_posture", "not_approved"),
)


def _result(codes: list[BaselineValidationCode] | tuple[BaselineValidationCode, ...]) -> BaselineContractValidationResult:
    values = tuple(codes)
    return BaselineContractValidationResult(
        BaselineValidationSeverity.BLOCKED if values else BaselineValidationSeverity.PASSED,
        not values,
        values,
    )


def _valid_text(value: object) -> bool:
    return type(value) is str and bool(value.strip())


def _parse_timestamp(value: object) -> datetime | None:
    if not _valid_text(value):
        return None
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            return None
        return parsed
    except (ValueError, OverflowError):
        return None


def _validate(values: Mapping[str, object], present: set[str]) -> list[BaselineValidationCode]:
    codes: list[BaselineValidationCode] = []
    for field in _REQUIRED_TEXT_FIELDS:
        if field in present and not _valid_text(values[field]):
            codes.append(BaselineValidationCode.BLANK_REQUIRED_TEXT)
    for field in _NULLABLE_TEXT_FIELDS:
        if field in present and values[field] is not None and not _valid_text(values[field]):
            codes.append(BaselineValidationCode.BLANK_REQUIRED_TEXT)

    baseline_type = values.get("baseline_type")
    valid_type = type(baseline_type) is BaselineType
    if "baseline_type" in present and not valid_type:
        codes.append(BaselineValidationCode.INVALID_BASELINE_TYPE)
    status = values.get("definition_status")
    valid_status = type(status) is BaselineDefinitionStatus
    if "definition_status" in present and not valid_status:
        codes.append(BaselineValidationCode.INVALID_DEFINITION_STATUS)
    if "fold_index" in present and (type(values["fold_index"]) is not int or values["fold_index"] < 0):
        codes.append(BaselineValidationCode.INVALID_INTEGER_FIELD)
    for field, expected in _FIXED_POSTURES:
        if field in present and (type(values[field]) is not str or values[field] != expected):
            codes.append(BaselineValidationCode.INVALID_FIXED_POSTURE)

    timestamps: dict[str, datetime | None] = {}
    for field in _TIMESTAMP_FIELDS:
        if field in present:
            timestamps[field] = _parse_timestamp(values[field])
            if timestamps[field] is None:
                codes.append(BaselineValidationCode.INVALID_TIMESTAMP)
    prediction = timestamps.get("prediction_as_of")
    available = timestamps.get("input_publication_available_at")
    cutoff = timestamps.get("fold_cutoff")
    declared = timestamps.get("definition_declared_at")
    if available is not None and prediction is not None and available > prediction:
        codes.append(BaselineValidationCode.INPUT_AVAILABLE_AFTER_PREDICTION)
    if prediction is not None and cutoff is not None and prediction > cutoff:
        codes.append(BaselineValidationCode.PREDICTION_AFTER_FOLD_CUTOFF)
    if declared is not None and prediction is not None and declared > prediction:
        codes.append(BaselineValidationCode.DEFINITION_DECLARED_AFTER_PREDICTION)

    conditioning_valid = False
    if "conditioning_dimensions" in present:
        conditioning = values["conditioning_dimensions"]
        conditioning_valid = type(conditioning) is tuple and all(_valid_text(item) for item in conditioning)
        if conditioning_valid:
            conditioning_valid = len(set(conditioning)) == len(conditioning)
        if not conditioning_valid:
            codes.append(BaselineValidationCode.INVALID_CONDITIONING_DIMENSIONS)

    for field, empty_code, invalid_code in (
        ("availability_evidence_refs", BaselineValidationCode.EMPTY_AVAILABILITY_EVIDENCE_REFS, BaselineValidationCode.INVALID_AVAILABILITY_EVIDENCE_REF),
        ("provenance_refs", BaselineValidationCode.EMPTY_PROVENANCE_REFS, BaselineValidationCode.INVALID_PROVENANCE_REF),
    ):
        if field not in present:
            continue
        refs = values[field]
        if type(refs) is not tuple:
            codes.append(invalid_code)
        elif not refs:
            codes.append(empty_code)
        else:
            for ref in refs:
                if not _valid_text(ref):
                    codes.append(invalid_code)

    if valid_type and baseline_type is BaselineType.CLIMATOLOGY:
        if "baseline_input_posture" in present and (type(values["baseline_input_posture"]) is not str or values["baseline_input_posture"] != "train_only_as_of_history"):
            codes.append(BaselineValidationCode.CLIMATOLOGY_INVALID_INPUT_POSTURE)
        if "history_window_definition_id" in present and not _valid_text(values["history_window_definition_id"]):
            codes.append(BaselineValidationCode.CLIMATOLOGY_MISSING_HISTORY_WINDOW)
        if any(field in present and values[field] is not None for field in ("persisted_quantity_id", "conversion_rule_id")):
            codes.append(BaselineValidationCode.CLIMATOLOGY_PERSISTENCE_FIELDS_PRESENT)
    elif valid_type and baseline_type is BaselineType.PERSISTENCE:
        if "baseline_input_posture" in present and (type(values["baseline_input_posture"]) is not str or values["baseline_input_posture"] != "latest_legitimately_available_compatible_prior_state"):
            codes.append(BaselineValidationCode.PERSISTENCE_INVALID_INPUT_POSTURE)
        if (("conditioning_dimensions" in present and conditioning_valid and bool(values["conditioning_dimensions"])) or
                any(field in present and values[field] is not None for field in ("smoothing_definition_id", "history_window_definition_id", "hierarchy_definition_id", "fallback_definition_id"))):
            codes.append(BaselineValidationCode.PERSISTENCE_CONDITIONING_FIELDS_PRESENT)
        if "persisted_quantity_id" in present and not _valid_text(values["persisted_quantity_id"]):
            codes.append(BaselineValidationCode.PERSISTENCE_MISSING_QUANTITY)
        if "conversion_rule_id" in present and not _valid_text(values["conversion_rule_id"]):
            codes.append(BaselineValidationCode.PERSISTENCE_MISSING_CONVERSION_RULE)

    if valid_status and status is BaselineDefinitionStatus.ACTIVE:
        if "exclusion_reason" in present and values["exclusion_reason"] is not None:
            codes.append(BaselineValidationCode.ACTIVE_WITH_EXCLUSION_REASON)
    elif valid_status and status is BaselineDefinitionStatus.BLOCKED:
        if "exclusion_reason" in present and not _valid_text(values["exclusion_reason"]):
            codes.append(BaselineValidationCode.BLOCKED_WITHOUT_EXCLUSION_REASON)
    if ("baseline_definition_id" in present and "supersedes_baseline_definition_id" in present
            and _valid_text(values["baseline_definition_id"])
            and _valid_text(values["supersedes_baseline_definition_id"])
            and values["baseline_definition_id"] == values["supersedes_baseline_definition_id"]):
        codes.append(BaselineValidationCode.SELF_SUPERSESSION)
    return codes


def baseline_contract_definition_from_mapping(
    mapping: object,
) -> tuple[BaselineContractDefinition | None, BaselineContractValidationResult]:
    if not isinstance(mapping, Mapping):
        return None, _result([BaselineValidationCode.MISSING_REQUIRED_FIELD] * 48)
    try:
        pairs = list(mapping.items())
        snapshot: dict[object, object] = {}
        ordered_keys: list[object] = []
        for pair in pairs:
            key, value = pair
            ordered_keys.append(key)
            snapshot[key] = value
    except Exception:
        return None, _result([BaselineValidationCode.MISSING_REQUIRED_FIELD] * 48)

    exact_keys = {key for key in snapshot if type(key) is str}
    present = exact_keys.intersection(_REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS)
    codes = [BaselineValidationCode.MISSING_REQUIRED_FIELD for key in _REQUIRED_MAPPING_KEYS if key not in present]
    unexpected_strings = sorted(key for key in exact_keys if key not in _REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS)
    codes.extend(BaselineValidationCode.UNEXPECTED_FIELD for _ in unexpected_strings)
    codes.extend(BaselineValidationCode.UNEXPECTED_FIELD for key in ordered_keys if type(key) is not str)

    values = {key: snapshot[key] for key in present}
    if "baseline_type" in present and type(values["baseline_type"]) is str:
        try:
            values["baseline_type"] = BaselineType(values["baseline_type"])
        except ValueError:
            pass
    if "definition_status" in present and type(values["definition_status"]) is str:
        try:
            values["definition_status"] = BaselineDefinitionStatus(values["definition_status"])
        except ValueError:
            pass
    for field in ("conditioning_dimensions", "availability_evidence_refs", "provenance_refs"):
        if field in present and type(values[field]) is list:
            values[field] = tuple(values[field])
    codes.extend(_validate(values, present))
    if codes:
        return None, _result(codes)
    definition = BaselineContractDefinition(**values)
    result = validate_baseline_contract_definition(definition)
    if not result.passed:
        return None, result
    return definition, result


def validate_baseline_contract_definition(
    definition: BaselineContractDefinition,
) -> BaselineContractValidationResult:
    values = {field: getattr(definition, field) for field in _REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS}
    return _result(_validate(values, set(values)))
