"""Binary outcome probability record boundary for Weather Bot Stage 3."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum
import re

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
_PROBABILITY_TEXT_RE = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?\Z")
_ZERO = Decimal("0")
_ONE = Decimal("1")


def _result(codes: list[ProbabilityRecordValidationCode]) -> ProbabilityRecordValidationResult:
    if codes:
        return ProbabilityRecordValidationResult(
            ProbabilityRecordValidationSeverity.BLOCKED, False, tuple(codes)
        )
    return ProbabilityRecordValidationResult(ProbabilityRecordValidationSeverity.PASSED, True)


def _is_nonblank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


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


def _adapt_representation(value: object) -> PredictionRepresentation | None:
    if value is PredictionRepresentation.BINARY_OUTCOME_PROBABILITY:
        return value
    if type(value) is str and value == PredictionRepresentation.BINARY_OUTCOME_PROBABILITY.value:
        return PredictionRepresentation.BINARY_OUTCOME_PROBABILITY
    return None


def _adapt_probability(value: object) -> tuple[Decimal | None, ProbabilityRecordValidationCode | None]:
    if isinstance(value, Decimal):
        probability = value
    elif isinstance(value, str):
        try:
            probability = Decimal(value)
        except InvalidOperation:
            return None, ProbabilityRecordValidationCode.INVALID_PROBABILITY_TYPE
        if probability.is_finite() and _PROBABILITY_TEXT_RE.fullmatch(value) is None:
            return None, ProbabilityRecordValidationCode.INVALID_PROBABILITY_TYPE
    else:
        return None, ProbabilityRecordValidationCode.INVALID_PROBABILITY_TYPE
    if not probability.is_finite():
        return None, ProbabilityRecordValidationCode.NON_FINITE_PROBABILITY
    if probability < _ZERO or probability > _ONE:
        return None, ProbabilityRecordValidationCode.PROBABILITY_OUT_OF_RANGE
    return probability, None


def _adapt_provenance(value: object) -> tuple[tuple[str, ...] | None, list[ProbabilityRecordValidationCode]]:
    if not isinstance(value, (tuple, list)):
        return None, [ProbabilityRecordValidationCode.INVALID_PROVENANCE_REF]
    if not value:
        return None, [ProbabilityRecordValidationCode.EMPTY_PROVENANCE_REFS]
    codes: list[ProbabilityRecordValidationCode] = []
    for entry in value:
        if not _is_nonblank_text(entry):
            codes.append(ProbabilityRecordValidationCode.INVALID_PROVENANCE_REF)
    if codes:
        return None, codes
    return tuple(value), []


def _validate_values(values: Mapping[str, object]) -> tuple[list[ProbabilityRecordValidationCode], dict[str, object]]:
    adapted: dict[str, object] = {}
    codes: list[ProbabilityRecordValidationCode] = []
    for field in _TEXT_FIELDS:
        if not _is_nonblank_text(values[field]):
            codes.append(ProbabilityRecordValidationCode.BLANK_REQUIRED_TEXT)
    supersedes = values.get("supersedes_prediction_record_id")
    if supersedes is not None and not _is_nonblank_text(supersedes):
        codes.append(ProbabilityRecordValidationCode.BLANK_REQUIRED_TEXT)

    representation = _adapt_representation(values["prediction_representation"])
    if representation is None:
        codes.append(ProbabilityRecordValidationCode.INVALID_PREDICTION_REPRESENTATION)
    else:
        adapted["prediction_representation"] = representation

    probability, probability_code = _adapt_probability(values["probability"])
    if probability_code is not None:
        codes.append(probability_code)
    else:
        adapted["probability"] = probability

    timestamps = {field: _parse_timestamp(values[field]) for field in _TIMESTAMP_FIELDS}
    for field in _TIMESTAMP_FIELDS:
        if timestamps[field] is None:
            codes.append(ProbabilityRecordValidationCode.INVALID_TIMESTAMP)
    if timestamps["prediction_as_of"] is not None and timestamps["input_publication_available_at"] is not None:
        if timestamps["input_publication_available_at"] > timestamps["prediction_as_of"]:
            codes.append(ProbabilityRecordValidationCode.INPUT_AVAILABLE_AFTER_PREDICTION)
    if timestamps["prediction_as_of"] is not None and timestamps["created_at"] is not None:
        if timestamps["created_at"] < timestamps["prediction_as_of"]:
            codes.append(ProbabilityRecordValidationCode.CREATED_BEFORE_PREDICTION)

    provenance_refs, provenance_codes = _adapt_provenance(values["provenance_refs"])
    codes.extend(provenance_codes)
    if provenance_refs is not None:
        adapted["provenance_refs"] = provenance_refs

    if supersedes is not None and supersedes == values["prediction_record_id"]:
        codes.append(ProbabilityRecordValidationCode.SELF_SUPERSESSION)
    return codes, adapted


def binary_outcome_probability_record_from_mapping(mapping: object) -> tuple[BinaryOutcomeProbabilityRecord | None, ProbabilityRecordValidationResult]:
    if not isinstance(mapping, Mapping):
        codes = [ProbabilityRecordValidationCode.MISSING_REQUIRED_FIELD for _ in _REQUIRED_KEYS]
        return None, _result(codes)
    allowed_keys = _REQUIRED_KEYS + _OPTIONAL_KEYS
    codes: list[ProbabilityRecordValidationCode] = []
    for key in _REQUIRED_KEYS:
        if key not in mapping:
            codes.append(ProbabilityRecordValidationCode.MISSING_REQUIRED_FIELD)
    unexpected_keys = [key for key in mapping.keys() if key not in allowed_keys]
    for _key in sorted(unexpected_keys, key=lambda item: item if isinstance(item, str) else repr(item)):
        codes.append(ProbabilityRecordValidationCode.UNEXPECTED_FIELD)
    if codes:
        return None, _result(codes)

    values = {key: mapping[key] for key in _REQUIRED_KEYS}
    if "supersedes_prediction_record_id" in mapping:
        values["supersedes_prediction_record_id"] = mapping["supersedes_prediction_record_id"]
    else:
        values["supersedes_prediction_record_id"] = None
    value_codes, adapted = _validate_values(values)
    if value_codes:
        return None, _result(value_codes)

    record_values = dict(values)
    record_values.update(adapted)
    record = BinaryOutcomeProbabilityRecord(**record_values)
    validation = validate_binary_outcome_probability_record(record)
    if not validation.passed:
        return None, validation
    return record, validation


def validate_binary_outcome_probability_record(record: BinaryOutcomeProbabilityRecord) -> ProbabilityRecordValidationResult:
    values = {field: getattr(record, field) for field in _REQUIRED_KEYS}
    values["supersedes_prediction_record_id"] = record.supersedes_prediction_record_id
    codes, _adapted = _validate_values(values)
    if not isinstance(record.prediction_representation, PredictionRepresentation):
        if ProbabilityRecordValidationCode.INVALID_PREDICTION_REPRESENTATION not in codes:
            insert_at = sum(1 for code in codes if code is ProbabilityRecordValidationCode.BLANK_REQUIRED_TEXT)
            codes.insert(insert_at, ProbabilityRecordValidationCode.INVALID_PREDICTION_REPRESENTATION)
    if not isinstance(record.probability, Decimal):
        codes = [c for c in codes if c is not ProbabilityRecordValidationCode.INVALID_PROBABILITY_TYPE]
        insert_at = 0
        ordered_before = {ProbabilityRecordValidationCode.BLANK_REQUIRED_TEXT, ProbabilityRecordValidationCode.INVALID_PREDICTION_REPRESENTATION}
        while insert_at < len(codes) and codes[insert_at] in ordered_before:
            insert_at += 1
        codes.insert(insert_at, ProbabilityRecordValidationCode.INVALID_PROBABILITY_TYPE)
    if not isinstance(record.provenance_refs, tuple):
        codes = [c for c in codes if c is not ProbabilityRecordValidationCode.EMPTY_PROVENANCE_REFS]
        if ProbabilityRecordValidationCode.INVALID_PROVENANCE_REF not in codes:
            insert_at = len(codes)
            if codes and codes[-1] is ProbabilityRecordValidationCode.SELF_SUPERSESSION:
                insert_at -= 1
            codes.insert(insert_at, ProbabilityRecordValidationCode.INVALID_PROVENANCE_REF)
    return _result(codes)
