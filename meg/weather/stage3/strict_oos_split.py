from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

__all__ = (
    "SplitRole",
    "SplitApplicabilityMode",
    "SplitAssignmentStatus",
    "OverlapControlPosture",
    "SplitValidationSeverity",
    "SplitValidationCode",
    "StrictOOSSplitAssignment",
    "StrictOOSSplitValidationResult",
    "strict_oos_split_assignment_from_mapping",
    "validate_strict_oos_split_assignment",
    "validate_strict_oos_split_assignments",
)


class SplitRole(StrEnum):
    TRAIN = "train"
    CALIBRATION = "calibration"
    TEST = "test"


class SplitApplicabilityMode(StrEnum):
    PRIMARY_TEMPORAL = "primary_temporal"
    LEAVE_STATION_OUT = "leave_station_out"
    LEAVE_YEAR_OUT = "leave_year_out"
    FAMILY_STRATIFIED = "family_stratified"
    SEASON_OR_REGIME_STRATIFIED = "season_or_regime_stratified"


class SplitAssignmentStatus(StrEnum):
    ASSIGNED = "assigned"
    BLOCKED = "blocked"


class OverlapControlPosture(StrEnum):
    NOT_REQUIRED = "not_required"
    SATISFIED = "satisfied"
    UNSATISFIED = "unsatisfied"


class SplitValidationSeverity(StrEnum):
    PASSED = "passed"
    BLOCKED = "blocked"


class SplitValidationCode(StrEnum):
    MISSING_REQUIRED_FIELD = "missing_required_field"
    UNEXPECTED_FIELD = "unexpected_field"
    BLANK_REQUIRED_TEXT = "blank_required_text"
    INVALID_SPLIT_ROLE = "invalid_split_role"
    INVALID_APPLICABILITY_MODES = "invalid_applicability_modes"
    INVALID_ASSIGNMENT_STATUS = "invalid_assignment_status"
    INVALID_OVERLAP_CONTROL_POSTURE = "invalid_overlap_control_posture"
    INVALID_INTEGER_FIELD = "invalid_integer_field"
    INVALID_FIXED_POSTURE = "invalid_fixed_posture"
    INVALID_TIMESTAMP = "invalid_timestamp"
    INPUT_AVAILABLE_AFTER_PREDICTION = "input_available_after_prediction"
    PREDICTION_AFTER_FOLD_CUTOFF = "prediction_after_fold_cutoff"
    INVALID_TARGET_WINDOW = "invalid_target_window"
    TRAIN_OR_CALIBRATION_AFTER_CUTOFF = "train_or_calibration_after_cutoff"
    TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF = "train_or_calibration_label_unavailable_by_cutoff"
    TEST_NOT_STRICTLY_AFTER_CUTOFF = "test_not_strictly_after_cutoff"
    TEST_LABEL_AVAILABLE_BY_CUTOFF = "test_label_available_by_cutoff"
    ASSIGNED_WITH_EXCLUSION_REASON = "assigned_with_exclusion_reason"
    BLOCKED_WITHOUT_EXCLUSION_REASON = "blocked_without_exclusion_reason"
    UNSATISFIED_OVERLAP_CONTROL_ASSIGNED = "unsatisfied_overlap_control_assigned"
    EMPTY_PROVENANCE_REFS = "empty_provenance_refs"
    INVALID_PROVENANCE_REF = "invalid_provenance_ref"
    SELF_SUPERSESSION = "self_supersession"
    INVALID_ASSIGNMENT_COLLECTION_TYPE = "invalid_assignment_collection_type"
    EMPTY_ASSIGNMENT_COLLECTION = "empty_assignment_collection"
    DUPLICATE_ASSIGNMENT_ID = "duplicate_assignment_id"
    DUPLICATE_FOLD_RECORD_ASSIGNMENT = "duplicate_fold_record_assignment"
    DUPLICATE_TEST_RECORD = "duplicate_test_record"
    INCONSISTENT_SPLIT_ID = "inconsistent_split_id"
    INCONSISTENT_SPLIT_VERSION = "inconsistent_split_version"
    INCONSISTENT_FOLD_DEFINITION = "inconsistent_fold_definition"
    NON_MONOTONIC_FOLD_CUTOFF = "non_monotonic_fold_cutoff"
    LEAKAGE_GROUP_ROLE_CONFLICT = "leakage_group_role_conflict"


@dataclass(frozen=True)
class StrictOOSSplitAssignment:
    split_assignment_id: str
    split_id: str
    split_version: str
    fold_id: str
    fold_index: int
    prediction_record_id: str
    condition_id: str
    token_id: str
    outcome: str
    settlement_rule_id: str
    settlement_rule_version: str
    split_role: SplitRole
    applicability_modes: tuple[SplitApplicabilityMode, ...]
    assignment_status: SplitAssignmentStatus
    fold_cutoff: str
    prediction_as_of: str
    input_publication_available_at: str
    target_start_at: str
    target_end_at: str
    label_available_at: str | None
    leakage_group_id: str
    overlap_control_posture: OverlapControlPosture
    primary_split_posture: str
    tuning_posture: str
    calibration_posture: str
    baseline_parity_posture: str
    exclusion_reason: str | None
    provenance_refs: tuple[str, ...]
    created_at: str
    supersedes_split_assignment_id: str | None = None


@dataclass(frozen=True)
class StrictOOSSplitValidationResult:
    severity: SplitValidationSeverity
    passed: bool
    codes: tuple[SplitValidationCode, ...] = ()

    def __post_init__(self) -> None:
        if self.codes:
            object.__setattr__(self, "severity", SplitValidationSeverity.BLOCKED)
            object.__setattr__(self, "passed", False)
        else:
            object.__setattr__(self, "severity", SplitValidationSeverity.PASSED)
            object.__setattr__(self, "passed", True)
            object.__setattr__(self, "codes", ())


_REQUIRED_MAPPING_KEYS = (
    "split_assignment_id", "split_id", "split_version", "fold_id", "fold_index",
    "prediction_record_id", "condition_id", "token_id", "outcome", "settlement_rule_id",
    "settlement_rule_version", "split_role", "applicability_modes", "assignment_status",
    "fold_cutoff", "prediction_as_of", "input_publication_available_at", "target_start_at",
    "target_end_at", "label_available_at", "leakage_group_id", "overlap_control_posture",
    "primary_split_posture", "tuning_posture", "calibration_posture", "baseline_parity_posture",
    "exclusion_reason", "provenance_refs", "created_at",
)
_OPTIONAL_MAPPING_KEYS = ("supersedes_split_assignment_id",)
_REQUIRED_TEXT_FIELDS = (
    "split_assignment_id", "split_id", "split_version", "fold_id", "prediction_record_id",
    "condition_id", "token_id", "outcome", "settlement_rule_id", "settlement_rule_version",
    "leakage_group_id", "primary_split_posture", "tuning_posture", "calibration_posture",
    "baseline_parity_posture",
)
_NULLABLE_TEXT_FIELDS = ("exclusion_reason", "supersedes_split_assignment_id")
_TIMESTAMP_FIELDS = (
    "fold_cutoff", "prediction_as_of", "input_publication_available_at", "target_start_at",
    "target_end_at", "label_available_at", "created_at",
)
_FIXED_POSTURES = (
    ("primary_split_posture", "rolling_origin_or_walk_forward_required"),
    ("tuning_posture", "train_or_calibration_only"),
    ("calibration_posture", "separate_when_required"),
    ("baseline_parity_posture", "same_folds_and_eligibility_required"),
)


def _result(codes: tuple[SplitValidationCode, ...]) -> StrictOOSSplitValidationResult:
    if codes:
        return StrictOOSSplitValidationResult(SplitValidationSeverity.BLOCKED, False, codes)
    return StrictOOSSplitValidationResult(SplitValidationSeverity.PASSED, True, ())


def _missing_result() -> StrictOOSSplitValidationResult:
    return _result((SplitValidationCode.MISSING_REQUIRED_FIELD,) * len(_REQUIRED_MAPPING_KEYS))


def _valid_text(value: object) -> bool:
    return type(value) is str and value.strip() != ""


def _valid_fixed_text(value: object, expected: str) -> bool:
    return type(value) is str and value == expected


def _parse_time(value: object):
    if type(value) is not str or value.strip() == "":
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except Exception:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _enum_value(value: object, enum_type: type[StrEnum]):
    if type(value) is enum_type:
        return value
    if type(value) is str:
        for member in enum_type:
            if value == member.value:
                return member
    return None


def _adapt_modes(value: object):
    if type(value) not in (tuple, list) or len(value) == 0:
        return None
    adapted = []
    for item in value:
        member = _enum_value(item, SplitApplicabilityMode)
        if member is None:
            return None
        adapted.append(member)
    if adapted[0] is not SplitApplicabilityMode.PRIMARY_TEMPORAL:
        return None
    seen = []
    for item in adapted:
        if item in seen:
            return None
        seen.append(item)
    return tuple(adapted)


def _valid_modes(value: object) -> bool:
    if type(value) is not tuple or len(value) == 0:
        return False
    seen = []
    for item in value:
        if type(item) is not SplitApplicabilityMode or item in seen:
            return False
        seen.append(item)
    return value[0] is SplitApplicabilityMode.PRIMARY_TEMPORAL


def _valid_role(value: object) -> bool:
    return type(value) is SplitRole


def _valid_status(value: object) -> bool:
    return type(value) is SplitAssignmentStatus


def _valid_overlap(value: object) -> bool:
    return type(value) is OverlapControlPosture


def _append_value_codes(values: Mapping, present: tuple[str, ...], codes: list[SplitValidationCode], adapt_enums: bool) -> dict:
    parsed = {}
    for field in _REQUIRED_TEXT_FIELDS:
        if field in present and not _valid_text(values[field]):
            codes.append(SplitValidationCode.BLANK_REQUIRED_TEXT)
    for field in _NULLABLE_TEXT_FIELDS:
        if field in present and values[field] is not None and not _valid_text(values[field]):
            codes.append(SplitValidationCode.BLANK_REQUIRED_TEXT)
    if "split_role" in present and ((adapt_enums and _enum_value(values["split_role"], SplitRole) is None) or (not adapt_enums and not _valid_role(values["split_role"]))):
        codes.append(SplitValidationCode.INVALID_SPLIT_ROLE)
    if "applicability_modes" in present and ((adapt_enums and _adapt_modes(values["applicability_modes"]) is None) or (not adapt_enums and not _valid_modes(values["applicability_modes"]))):
        codes.append(SplitValidationCode.INVALID_APPLICABILITY_MODES)
    if "assignment_status" in present and ((adapt_enums and _enum_value(values["assignment_status"], SplitAssignmentStatus) is None) or (not adapt_enums and not _valid_status(values["assignment_status"]))):
        codes.append(SplitValidationCode.INVALID_ASSIGNMENT_STATUS)
    if "overlap_control_posture" in present and ((adapt_enums and _enum_value(values["overlap_control_posture"], OverlapControlPosture) is None) or (not adapt_enums and not _valid_overlap(values["overlap_control_posture"]))):
        codes.append(SplitValidationCode.INVALID_OVERLAP_CONTROL_POSTURE)
    if "fold_index" in present and (type(values["fold_index"]) is not int or values["fold_index"] < 0):
        codes.append(SplitValidationCode.INVALID_INTEGER_FIELD)
    for field, expected in _FIXED_POSTURES:
        if field in present and not _valid_fixed_text(values[field], expected):
            codes.append(SplitValidationCode.INVALID_FIXED_POSTURE)
    for field in _TIMESTAMP_FIELDS:
        if field not in present:
            continue
        value = values[field]
        if field == "label_available_at" and value is None:
            parsed[field] = None
            continue
        parsed[field] = _parse_time(value)
        if parsed[field] is None:
            codes.append(SplitValidationCode.INVALID_TIMESTAMP)
    if parsed.get("input_publication_available_at") is not None and parsed.get("prediction_as_of") is not None:
        if parsed["input_publication_available_at"] > parsed["prediction_as_of"]:
            codes.append(SplitValidationCode.INPUT_AVAILABLE_AFTER_PREDICTION)
    if parsed.get("prediction_as_of") is not None and parsed.get("fold_cutoff") is not None:
        if parsed["prediction_as_of"] > parsed["fold_cutoff"]:
            codes.append(SplitValidationCode.PREDICTION_AFTER_FOLD_CUTOFF)
    if parsed.get("target_start_at") is not None and parsed.get("target_end_at") is not None:
        if parsed["target_start_at"] > parsed["target_end_at"]:
            codes.append(SplitValidationCode.INVALID_TARGET_WINDOW)
    role = _enum_value(values["split_role"], SplitRole) if adapt_enums and "split_role" in present else (values["split_role"] if "split_role" in present and _valid_role(values["split_role"]) else None)
    status = _enum_value(values["assignment_status"], SplitAssignmentStatus) if adapt_enums and "assignment_status" in present else (values["assignment_status"] if "assignment_status" in present and _valid_status(values["assignment_status"]) else None)
    overlap = _enum_value(values["overlap_control_posture"], OverlapControlPosture) if adapt_enums and "overlap_control_posture" in present else (values["overlap_control_posture"] if "overlap_control_posture" in present and _valid_overlap(values["overlap_control_posture"]) else None)
    if status is SplitAssignmentStatus.ASSIGNED and role is not None:
        cutoff = parsed.get("fold_cutoff")
        if role in (SplitRole.TRAIN, SplitRole.CALIBRATION):
            if parsed.get("target_end_at") is not None and cutoff is not None and parsed["target_end_at"] > cutoff:
                codes.append(SplitValidationCode.TRAIN_OR_CALIBRATION_AFTER_CUTOFF)
            label = parsed.get("label_available_at")
            if "label_available_at" in present and (values["label_available_at"] is None or label is None or (cutoff is not None and label > cutoff)):
                codes.append(SplitValidationCode.TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF)
        if role is SplitRole.TEST:
            if parsed.get("target_start_at") is not None and cutoff is not None and parsed["target_start_at"] <= cutoff:
                codes.append(SplitValidationCode.TEST_NOT_STRICTLY_AFTER_CUTOFF)
            label = parsed.get("label_available_at")
            if label is not None and cutoff is not None and label <= cutoff:
                codes.append(SplitValidationCode.TEST_LABEL_AVAILABLE_BY_CUTOFF)
    if status is SplitAssignmentStatus.ASSIGNED and "exclusion_reason" in present and values["exclusion_reason"] is not None:
        codes.append(SplitValidationCode.ASSIGNED_WITH_EXCLUSION_REASON)
    if status is SplitAssignmentStatus.BLOCKED and "exclusion_reason" in present and not _valid_text(values["exclusion_reason"]):
        codes.append(SplitValidationCode.BLOCKED_WITHOUT_EXCLUSION_REASON)
    if status is SplitAssignmentStatus.ASSIGNED and overlap is OverlapControlPosture.UNSATISFIED:
        codes.append(SplitValidationCode.UNSATISFIED_OVERLAP_CONTROL_ASSIGNED)
    if "provenance_refs" in present:
        prov = values["provenance_refs"]
        if (adapt_enums and type(prov) not in (tuple, list)) or (not adapt_enums and type(prov) is not tuple):
            codes.append(SplitValidationCode.INVALID_PROVENANCE_REF)
        elif len(prov) == 0:
            codes.append(SplitValidationCode.EMPTY_PROVENANCE_REFS)
        else:
            for ref in prov:
                if not _valid_text(ref):
                    codes.append(SplitValidationCode.INVALID_PROVENANCE_REF)
    if "split_assignment_id" in present and "supersedes_split_assignment_id" in present:
        if _valid_text(values["split_assignment_id"]) and _valid_text(values["supersedes_split_assignment_id"]) and values["split_assignment_id"] == values["supersedes_split_assignment_id"]:
            codes.append(SplitValidationCode.SELF_SUPERSESSION)
    return parsed


def _mapping_snapshot(mapping: Mapping):
    snapshot = []
    for entry in mapping.items():
        key, value = entry
        snapshot.append((key, value))
    return tuple(snapshot)


def strict_oos_split_assignment_from_mapping(mapping: object) -> tuple[StrictOOSSplitAssignment | None, StrictOOSSplitValidationResult]:
    if not isinstance(mapping, Mapping):
        return None, _missing_result()
    try:
        items = _mapping_snapshot(mapping)
    except Exception:
        return None, _missing_result()
    exact = {}
    unexpected_strings = []
    unexpected_other = []
    try:
        for key, value in items:
            if type(key) is str:
                exact[key] = value
            if type(key) is str:
                if key not in _REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS:
                    unexpected_strings.append(key)
            else:
                unexpected_other.append(key)
    except Exception:
        return None, _missing_result()
    codes = []
    for key in _REQUIRED_MAPPING_KEYS:
        if key not in exact:
            codes.append(SplitValidationCode.MISSING_REQUIRED_FIELD)
    for _key in sorted(unexpected_strings):
        codes.append(SplitValidationCode.UNEXPECTED_FIELD)
    for _key in unexpected_other:
        codes.append(SplitValidationCode.UNEXPECTED_FIELD)
    present = tuple(key for key in _REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS if key in exact)
    _append_value_codes(exact, present, codes, True)
    if codes:
        return None, _result(tuple(codes))
    adapted = dict(exact)
    adapted["split_role"] = _enum_value(adapted["split_role"], SplitRole)
    adapted["applicability_modes"] = _adapt_modes(adapted["applicability_modes"])
    adapted["assignment_status"] = _enum_value(adapted["assignment_status"], SplitAssignmentStatus)
    adapted["overlap_control_posture"] = _enum_value(adapted["overlap_control_posture"], OverlapControlPosture)
    if type(adapted["provenance_refs"]) is list:
        adapted["provenance_refs"] = tuple(adapted["provenance_refs"])
    record = StrictOOSSplitAssignment(**adapted)
    result = validate_strict_oos_split_assignment(record)
    if result.passed:
        return record, result
    return None, result


def validate_strict_oos_split_assignment(record: StrictOOSSplitAssignment) -> StrictOOSSplitValidationResult:
    values = {
        "split_assignment_id": record.split_assignment_id,
        "split_id": record.split_id,
        "split_version": record.split_version,
        "fold_id": record.fold_id,
        "fold_index": record.fold_index,
        "prediction_record_id": record.prediction_record_id,
        "condition_id": record.condition_id,
        "token_id": record.token_id,
        "outcome": record.outcome,
        "settlement_rule_id": record.settlement_rule_id,
        "settlement_rule_version": record.settlement_rule_version,
        "split_role": record.split_role,
        "applicability_modes": record.applicability_modes,
        "assignment_status": record.assignment_status,
        "fold_cutoff": record.fold_cutoff,
        "prediction_as_of": record.prediction_as_of,
        "input_publication_available_at": record.input_publication_available_at,
        "target_start_at": record.target_start_at,
        "target_end_at": record.target_end_at,
        "label_available_at": record.label_available_at,
        "leakage_group_id": record.leakage_group_id,
        "overlap_control_posture": record.overlap_control_posture,
        "primary_split_posture": record.primary_split_posture,
        "tuning_posture": record.tuning_posture,
        "calibration_posture": record.calibration_posture,
        "baseline_parity_posture": record.baseline_parity_posture,
        "exclusion_reason": record.exclusion_reason,
        "provenance_refs": record.provenance_refs,
        "created_at": record.created_at,
        "supersedes_split_assignment_id": record.supersedes_split_assignment_id,
    }
    codes = []
    _append_value_codes(values, _REQUIRED_MAPPING_KEYS + _OPTIONAL_MAPPING_KEYS, codes, False)
    return _result(tuple(codes))


def _eligible_text(value: object) -> bool:
    return _valid_text(value)


def validate_strict_oos_split_assignments(assignments: tuple[StrictOOSSplitAssignment, ...]) -> StrictOOSSplitValidationResult:
    if type(assignments) is not tuple:
        return _result((SplitValidationCode.INVALID_ASSIGNMENT_COLLECTION_TYPE,))
    if len(assignments) == 0:
        return _result((SplitValidationCode.EMPTY_ASSIGNMENT_COLLECTION,))
    codes = []
    records = []
    for record in assignments:
        if type(record) is not StrictOOSSplitAssignment:
            codes.append(SplitValidationCode.INVALID_ASSIGNMENT_COLLECTION_TYPE)
        else:
            records.append(record)
            codes.extend(validate_strict_oos_split_assignment(record).codes)
    seen_ids = []
    for record in records:
        if _eligible_text(record.split_assignment_id):
            if record.split_assignment_id in seen_ids:
                codes.append(SplitValidationCode.DUPLICATE_ASSIGNMENT_ID)
            else:
                seen_ids.append(record.split_assignment_id)
    seen_fold_records = []
    for record in records:
        if _eligible_text(record.fold_id) and _eligible_text(record.prediction_record_id):
            key = (record.fold_id, record.prediction_record_id)
            if key in seen_fold_records:
                codes.append(SplitValidationCode.DUPLICATE_FOLD_RECORD_ASSIGNMENT)
            else:
                seen_fold_records.append(key)
    seen_test = []
    for record in records:
        if _valid_status(record.assignment_status) and record.assignment_status is SplitAssignmentStatus.ASSIGNED and _valid_role(record.split_role) and record.split_role is SplitRole.TEST and _eligible_text(record.fold_id) and _eligible_text(record.prediction_record_id):
            conflict = False
            for fold_id, prediction_record_id in seen_test:
                if prediction_record_id == record.prediction_record_id and fold_id != record.fold_id:
                    conflict = True
            if conflict:
                codes.append(SplitValidationCode.DUPLICATE_TEST_RECORD)
            seen_test.append((record.fold_id, record.prediction_record_id))
    baseline = None
    for record in records:
        if _eligible_text(record.split_id):
            if baseline is None:
                baseline = record.split_id
            elif record.split_id != baseline:
                codes.append(SplitValidationCode.INCONSISTENT_SPLIT_ID)
    baseline = None
    for record in records:
        if _eligible_text(record.split_version):
            if baseline is None:
                baseline = record.split_version
            elif record.split_version != baseline:
                codes.append(SplitValidationCode.INCONSISTENT_SPLIT_VERSION)
    by_fold = {}
    by_index = {}
    definitions = []
    for record in records:
        cutoff = _parse_time(record.fold_cutoff)
        if _eligible_text(record.fold_id) and type(record.fold_index) is int and record.fold_index >= 0 and cutoff is not None:
            definition = (record.fold_index, record.fold_id, record.fold_cutoff, cutoff)
            fold_def = (record.fold_index, record.fold_cutoff)
            index_def = (record.fold_id, record.fold_cutoff)
            conflict = (record.fold_id in by_fold and by_fold[record.fold_id] != fold_def) or (record.fold_index in by_index and by_index[record.fold_index] != index_def)
            if conflict:
                codes.append(SplitValidationCode.INCONSISTENT_FOLD_DEFINITION)
            else:
                if record.fold_id not in by_fold and record.fold_index not in by_index:
                    definitions.append(definition)
                by_fold.setdefault(record.fold_id, fold_def)
                by_index.setdefault(record.fold_index, index_def)
    previous = None
    for definition in sorted(definitions, key=lambda item: item[0]):
        if previous is not None and definition[3] <= previous[3]:
            codes.append(SplitValidationCode.NON_MONOTONIC_FOLD_CUTOFF)
        previous = definition
    seen_roles = {}
    for record in records:
        if _valid_status(record.assignment_status) and record.assignment_status is SplitAssignmentStatus.ASSIGNED and _valid_role(record.split_role) and _eligible_text(record.fold_id) and _eligible_text(record.leakage_group_id):
            key = (record.fold_id, record.leakage_group_id)
            if key in seen_roles and seen_roles[key] is not record.split_role:
                codes.append(SplitValidationCode.LEAKAGE_GROUP_ROLE_CONFLICT)
            else:
                seen_roles.setdefault(key, record.split_role)
    return _result(tuple(codes))
