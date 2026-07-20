"""Binary outcome probability record boundary for Weather Bot Stage 3."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum

__all__ = (
    "PredictionRepresentation",
    "ProbabilityRecordValidationSeverity",
    "ProbabilityRecordValidationCode",
    "BinaryOutcomeProbabilityRecord",
    "ProbabilityRecordValidationResult",
    "binary_outcome_probability_record_from_mapping",
    "validate_binary_outcome_probability_record",
)


class _StringEnum(StrEnum):
    pass


class PredictionRepresentation(_StringEnum):
    BINARY_OUTCOME_PROBABILITY = "binary_outcome_probability"


class ProbabilityRecordValidationSeverity(_StringEnum):
    PASSED = "passed"
    BLOCKED = "blocked"


class ProbabilityRecordValidationCode(_StringEnum):
    MISSING_REQUIRED_FIELD = "missing_required_field"
    UNEXPECTED_FIELD = "unexpected_field"
    BLANK_REQUIRED_TEXT = "blank_required_text"
    INVALID_PREDICTION_REPRESENTATION = "invalid_prediction_representation"
    INVALID_PROBABILITY_TYPE = "invalid_probability_type"
    NON_FINITE_PROBABILITY = "non_finite_probability"
    PROBABILITY_OUT_OF_RANGE = "probability_out_of_range"
    INVALID_TIMESTAMP = "invalid_timestamp"
    INPUT_AVAILABLE_AFTER_PREDICTION = "input_available_after_prediction"
    CREATED_BEFORE_PREDICTION = "created_before_prediction"
    EMPTY_PROVENANCE_REFS = "empty_provenance_refs"
    INVALID_PROVENANCE_REF = "invalid_provenance_ref"
    SELF_SUPERSESSION = "self_supersession"


@dataclass(frozen=True)
class BinaryOutcomeProbabilityRecord:
    prediction_record_id: str
    condition_id: str
    token_id: str
    outcome: str
    settlement_rule_id: str
    settlement_rule_version: str
    prediction_as_of: str
    input_publication_available_at: str
    market_family: str
    threshold: str
    unit: str
    comparator: str
    measurement_window: str
    source_compatibility_posture: str
    station_compatibility_posture: str
    archive_finality_layer: str
    prediction_representation: PredictionRepresentation
    probability: Decimal
    method_id: str
    method_version: str
    provenance_refs: tuple[str, ...]
    created_at: str
    record_version: str
    supersedes_prediction_record_id: str | None = None


@dataclass(frozen=True)
class ProbabilityRecordValidationResult:
    severity: ProbabilityRecordValidationSeverity
    passed: bool
    codes: tuple[ProbabilityRecordValidationCode, ...] = ()


_REQUIRED_KEYS = (
    "prediction_record_id", "condition_id", "token_id", "outcome",
    "settlement_rule_id", "settlement_rule_version", "prediction_as_of",
    "input_publication_available_at", "market_family", "threshold", "unit",
    "comparator", "measurement_window", "source_compatibility_posture",
    "station_compatibility_posture", "archive_finality_layer",
    "prediction_representation", "probability", "method_id", "method_version",
    "provenance_refs", "created_at", "record_version",
)
_OPTIONAL_KEYS = ("supersedes_prediction_record_id",)
_TEXT_FIELDS = (
    "prediction_record_id", "condition_id", "token_id", "outcome",
    "settlement_rule_id", "settlement_rule_version", "market_family", "threshold",
    "unit", "comparator", "measurement_window", "source_compatibility_posture",
    "station_compatibility_posture", "archive_finality_layer", "method_id",
    "method_version", "record_version",
)
_TIMESTAMP_FIELDS = ("prediction_as_of", "input_publication_available_at", "created_at")
_ZERO = Decimal("0")
_ONE = Decimal("1")


def _result(codes: list[ProbabilityRecordValidationCode]) -> ProbabilityRecordValidationResult:
    if codes:
        return ProbabilityRecordValidationResult(
            ProbabilityRecordValidationSeverity.BLOCKED, False, tuple(codes)
        )
    return ProbabilityRecordValidationResult(ProbabilityRecordValidationSeverity.PASSED, True)


def _is_nonblank_text(value: object) -> bool:
    return type(value) is str and bool(value.strip())


def _is_ascii_canonical_decimal_text(value: str) -> bool:
    index = 1 if value.startswith("-") else 0
    integer_start = index
    while index < len(value) and "0" <= value[index] <= "9":
        index += 1
    integer = value[integer_start:index]
    if integer == "":
        return False
    if len(integer) > 1 and integer.startswith("0"):
        return False
    if index < len(value) and value[index] == ".":
        index += 1
        fraction_start = index
        while index < len(value) and "0" <= value[index] <= "9":
            index += 1
        if fraction_start == index:
            return False
    return index == len(value)


def _parse_timestamp(value: object) -> datetime | None:
    if not _is_nonblank_text(value):
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _append_timestamp_codes(
    codes: list[ProbabilityRecordValidationCode],
    timestamps: dict[str, datetime | None],
) -> None:
    for field in _TIMESTAMP_FIELDS:
        if timestamps[field] is None:
            codes.append(ProbabilityRecordValidationCode.INVALID_TIMESTAMP)
    prediction = timestamps["prediction_as_of"]
    input_available = timestamps["input_publication_available_at"]
    created = timestamps["created_at"]
    if prediction is not None and input_available is not None and input_available > prediction:
        codes.append(ProbabilityRecordValidationCode.INPUT_AVAILABLE_AFTER_PREDICTION)
    if prediction is not None and created is not None and created < prediction:
        codes.append(ProbabilityRecordValidationCode.CREATED_BEFORE_PREDICTION)


def _adapt_mapping_representation(value: object) -> PredictionRepresentation | None:
    if value is PredictionRepresentation.BINARY_OUTCOME_PROBABILITY:
        return value
    if type(value) is str and value == PredictionRepresentation.BINARY_OUTCOME_PROBABILITY.value:
        return PredictionRepresentation.BINARY_OUTCOME_PROBABILITY
    return None


def _adapt_mapping_probability(value: object) -> tuple[Decimal | None, ProbabilityRecordValidationCode | None]:
    if isinstance(value, Decimal):
        probability = value
    elif type(value) is str:
        try:
            probability = Decimal(value)
        except InvalidOperation:
            return None, ProbabilityRecordValidationCode.INVALID_PROBABILITY_TYPE
        if probability.is_finite() and not _is_ascii_canonical_decimal_text(value):
            return None, ProbabilityRecordValidationCode.INVALID_PROBABILITY_TYPE
    else:
        return None, ProbabilityRecordValidationCode.INVALID_PROBABILITY_TYPE
    if not probability.is_finite():
        return None, ProbabilityRecordValidationCode.NON_FINITE_PROBABILITY
    if probability < _ZERO or probability > _ONE:
        return None, ProbabilityRecordValidationCode.PROBABILITY_OUT_OF_RANGE
    return probability, None


def _append_mapping_provenance_codes(
    codes: list[ProbabilityRecordValidationCode], value: object
) -> tuple[str, ...] | None:
    if not isinstance(value, (tuple, list)):
        codes.append(ProbabilityRecordValidationCode.INVALID_PROVENANCE_REF)
        return None
    if not value:
        codes.append(ProbabilityRecordValidationCode.EMPTY_PROVENANCE_REFS)
        return None
    for entry in value:
        if not _is_nonblank_text(entry):
            codes.append(ProbabilityRecordValidationCode.INVALID_PROVENANCE_REF)
    if codes and codes[-1] is ProbabilityRecordValidationCode.INVALID_PROVENANCE_REF:
        return None
    return tuple(value)


def _append_direct_provenance_codes(
    codes: list[ProbabilityRecordValidationCode], value: object
) -> None:
    if not isinstance(value, tuple):
        codes.append(ProbabilityRecordValidationCode.INVALID_PROVENANCE_REF)
        return
    if not value:
        codes.append(ProbabilityRecordValidationCode.EMPTY_PROVENANCE_REFS)
        return
    for entry in value:
        if not _is_nonblank_text(entry):
            codes.append(ProbabilityRecordValidationCode.INVALID_PROVENANCE_REF)


def binary_outcome_probability_record_from_mapping(mapping: object) -> tuple[BinaryOutcomeProbabilityRecord | None, ProbabilityRecordValidationResult]:
    if not isinstance(mapping, Mapping):
        return None, _result([ProbabilityRecordValidationCode.MISSING_REQUIRED_FIELD for _ in _REQUIRED_KEYS])

    codes: list[ProbabilityRecordValidationCode] = []
    present: dict[str, object] = {}
    for key in _REQUIRED_KEYS:
        if key in mapping:
            present[key] = mapping[key]
        else:
            codes.append(ProbabilityRecordValidationCode.MISSING_REQUIRED_FIELD)
    optional_supersedes_present = "supersedes_prediction_record_id" in mapping
    if optional_supersedes_present:
        present["supersedes_prediction_record_id"] = mapping["supersedes_prediction_record_id"]
    else:
        present["supersedes_prediction_record_id"] = None

    allowed_keys = _REQUIRED_KEYS + _OPTIONAL_KEYS
    unexpected_keys = [key for key in mapping.keys() if key not in allowed_keys]
    for _key in sorted(unexpected_keys, key=lambda item: item if type(item) is str else repr(item)):
        codes.append(ProbabilityRecordValidationCode.UNEXPECTED_FIELD)

    for field in _TEXT_FIELDS:
        if field in present and not _is_nonblank_text(present[field]):
            codes.append(ProbabilityRecordValidationCode.BLANK_REQUIRED_TEXT)
    supersedes = present["supersedes_prediction_record_id"]
    if optional_supersedes_present and supersedes is not None and not _is_nonblank_text(supersedes):
        codes.append(ProbabilityRecordValidationCode.BLANK_REQUIRED_TEXT)

    adapted: dict[str, object] = {}
    if "prediction_representation" in present:
        representation = _adapt_mapping_representation(present["prediction_representation"])
        if representation is None:
            codes.append(ProbabilityRecordValidationCode.INVALID_PREDICTION_REPRESENTATION)
        else:
            adapted["prediction_representation"] = representation

    if "probability" in present:
        probability, probability_code = _adapt_mapping_probability(present["probability"])
        if probability_code is not None:
            codes.append(probability_code)
        else:
            adapted["probability"] = probability

    timestamps = {
        field: _parse_timestamp(present[field]) if field in present else None
        for field in _TIMESTAMP_FIELDS
    }
    for field in _TIMESTAMP_FIELDS:
        if field in present and timestamps[field] is None:
            codes.append(ProbabilityRecordValidationCode.INVALID_TIMESTAMP)
    prediction = timestamps["prediction_as_of"]
    input_available = timestamps["input_publication_available_at"]
    created = timestamps["created_at"]
    if prediction is not None and input_available is not None and input_available > prediction:
        codes.append(ProbabilityRecordValidationCode.INPUT_AVAILABLE_AFTER_PREDICTION)
    if prediction is not None and created is not None and created < prediction:
        codes.append(ProbabilityRecordValidationCode.CREATED_BEFORE_PREDICTION)

    if "provenance_refs" in present:
        provenance_refs = _append_mapping_provenance_codes(codes, present["provenance_refs"])
        if provenance_refs is not None:
            adapted["provenance_refs"] = provenance_refs

    prediction_id_valid = "prediction_record_id" in present and _is_nonblank_text(present["prediction_record_id"])
    supersedes_valid = supersedes is not None and _is_nonblank_text(supersedes)
    if prediction_id_valid and supersedes_valid and supersedes == present["prediction_record_id"]:
        codes.append(ProbabilityRecordValidationCode.SELF_SUPERSESSION)

    if codes:
        return None, _result(codes)

    record_values = {key: present[key] for key in _REQUIRED_KEYS}
    record_values["supersedes_prediction_record_id"] = present["supersedes_prediction_record_id"]
    record_values.update(adapted)
    record = BinaryOutcomeProbabilityRecord(**record_values)
    validation = validate_binary_outcome_probability_record(record)
    if not validation.passed:
        return None, validation
    return record, validation


def validate_binary_outcome_probability_record(record: BinaryOutcomeProbabilityRecord) -> ProbabilityRecordValidationResult:
    codes: list[ProbabilityRecordValidationCode] = []
    for field in _TEXT_FIELDS:
        if not _is_nonblank_text(getattr(record, field)):
            codes.append(ProbabilityRecordValidationCode.BLANK_REQUIRED_TEXT)
    supersedes = record.supersedes_prediction_record_id
    if supersedes is not None and not _is_nonblank_text(supersedes):
        codes.append(ProbabilityRecordValidationCode.BLANK_REQUIRED_TEXT)

    if record.prediction_representation is not PredictionRepresentation.BINARY_OUTCOME_PROBABILITY:
        codes.append(ProbabilityRecordValidationCode.INVALID_PREDICTION_REPRESENTATION)

    probability = record.probability
    if not isinstance(probability, Decimal):
        codes.append(ProbabilityRecordValidationCode.INVALID_PROBABILITY_TYPE)
    elif not probability.is_finite():
        codes.append(ProbabilityRecordValidationCode.NON_FINITE_PROBABILITY)
    elif probability < _ZERO or probability > _ONE:
        codes.append(ProbabilityRecordValidationCode.PROBABILITY_OUT_OF_RANGE)

    timestamps = {field: _parse_timestamp(getattr(record, field)) for field in _TIMESTAMP_FIELDS}
    _append_timestamp_codes(codes, timestamps)
    _append_direct_provenance_codes(codes, record.provenance_refs)
    if _is_nonblank_text(record.prediction_record_id) and _is_nonblank_text(supersedes):
        if supersedes == record.prediction_record_id:
            codes.append(ProbabilityRecordValidationCode.SELF_SUPERSESSION)
    return _result(codes)
