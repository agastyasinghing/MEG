from __future__ import annotations

import ast
import dataclasses
import inspect
from collections.abc import Mapping
from dataclasses import FrozenInstanceError
from enum import Enum
from pathlib import Path

import pytest

from meg.weather.stage3.strict_oos_split import (
    OverlapControlPosture,
    SplitApplicabilityMode,
    SplitAssignmentStatus,
    SplitRole,
    SplitValidationCode,
    SplitValidationSeverity,
    StrictOOSSplitAssignment,
    StrictOOSSplitValidationResult,
    strict_oos_split_assignment_from_mapping,
    validate_strict_oos_split_assignment,
    validate_strict_oos_split_assignments,
)
import meg.weather.stage3.strict_oos_split as module

C = SplitValidationCode

REQUIRED_KEYS = (
    "split_assignment_id", "split_id", "split_version", "fold_id", "fold_index",
    "prediction_record_id", "condition_id", "token_id", "outcome", "settlement_rule_id",
    "settlement_rule_version", "split_role", "applicability_modes", "assignment_status",
    "fold_cutoff", "prediction_as_of", "input_publication_available_at", "target_start_at",
    "target_end_at", "label_available_at", "leakage_group_id", "overlap_control_posture",
    "primary_split_posture", "tuning_posture", "calibration_posture", "baseline_parity_posture",
    "exclusion_reason", "provenance_refs", "created_at",
)


def good(**overrides):
    data = {
        "split_assignment_id": "assign-1",
        "split_id": "split-1",
        "split_version": "v1",
        "fold_id": "fold-1",
        "fold_index": 0,
        "prediction_record_id": "pred-1",
        "condition_id": "cond-1",
        "token_id": "tok-1",
        "outcome": "yes",
        "settlement_rule_id": "rule-1",
        "settlement_rule_version": "rv1",
        "split_role": SplitRole.TEST,
        "applicability_modes": (SplitApplicabilityMode.PRIMARY_TEMPORAL, SplitApplicabilityMode.LEAVE_YEAR_OUT),
        "assignment_status": SplitAssignmentStatus.ASSIGNED,
        "fold_cutoff": "2025-01-01T00:00:00+00:00",
        "prediction_as_of": "2025-01-01T00:00:00+00:00",
        "input_publication_available_at": "2025-01-01T00:00:00+00:00",
        "target_start_at": "2025-01-02T00:00:00+00:00",
        "target_end_at": "2025-01-03T00:00:00+00:00",
        "label_available_at": None,
        "leakage_group_id": "lg-1",
        "overlap_control_posture": OverlapControlPosture.SATISFIED,
        "primary_split_posture": "rolling_origin_or_walk_forward_required",
        "tuning_posture": "train_or_calibration_only",
        "calibration_posture": "separate_when_required",
        "baseline_parity_posture": "same_folds_and_eligibility_required",
        "exclusion_reason": None,
        "provenance_refs": ("prd:369", "ticket:strict"),
        "created_at": "2025-01-01T00:00:00+00:00",
        "supersedes_split_assignment_id": None,
    }
    data.update(overrides)
    return StrictOOSSplitAssignment(**data)


def codes(result):
    return result.codes


def test_public_structure_and_private_contracts():
    assert module.__all__ == (
        "SplitRole", "SplitApplicabilityMode", "SplitAssignmentStatus", "OverlapControlPosture",
        "SplitValidationSeverity", "SplitValidationCode", "StrictOOSSplitAssignment",
        "StrictOOSSplitValidationResult", "strict_oos_split_assignment_from_mapping",
        "validate_strict_oos_split_assignment", "validate_strict_oos_split_assignments",
    )
    public = [n for n in module.__all__ if inspect.isclass(getattr(module, n)) or inspect.isfunction(getattr(module, n))]
    assert public == list(module.__all__)
    assert [(m.name, m.value) for m in SplitRole] == [("TRAIN", "train"), ("CALIBRATION", "calibration"), ("TEST", "test")]
    assert [(m.name, m.value) for m in SplitApplicabilityMode] == [("PRIMARY_TEMPORAL", "primary_temporal"), ("LEAVE_STATION_OUT", "leave_station_out"), ("LEAVE_YEAR_OUT", "leave_year_out"), ("FAMILY_STRATIFIED", "family_stratified"), ("SEASON_OR_REGIME_STRATIFIED", "season_or_regime_stratified")]
    assert [(m.name, m.value) for m in SplitValidationCode][-10:] == [("INVALID_ASSIGNMENT_COLLECTION_TYPE", "invalid_assignment_collection_type"), ("EMPTY_ASSIGNMENT_COLLECTION", "empty_assignment_collection"), ("DUPLICATE_ASSIGNMENT_ID", "duplicate_assignment_id"), ("DUPLICATE_FOLD_RECORD_ASSIGNMENT", "duplicate_fold_record_assignment"), ("DUPLICATE_TEST_RECORD", "duplicate_test_record"), ("INCONSISTENT_SPLIT_ID", "inconsistent_split_id"), ("INCONSISTENT_SPLIT_VERSION", "inconsistent_split_version"), ("INCONSISTENT_FOLD_DEFINITION", "inconsistent_fold_definition"), ("NON_MONOTONIC_FOLD_CUTOFF", "non_monotonic_fold_cutoff"), ("LEAKAGE_GROUP_ROLE_CONFLICT", "leakage_group_role_conflict")]
    assert [f.name for f in dataclasses.fields(StrictOOSSplitAssignment)] == list(REQUIRED_KEYS) + ["supersedes_split_assignment_id"]
    assert dataclasses.fields(StrictOOSSplitAssignment)[-1].default is None
    assert dataclasses.fields(StrictOOSSplitValidationResult)[2].default == ()
    assert dataclasses.is_dataclass(StrictOOSSplitAssignment)
    with pytest.raises(FrozenInstanceError):
        good().split_id = "x"
    assert inspect.signature(strict_oos_split_assignment_from_mapping).return_annotation == "tuple[StrictOOSSplitAssignment | None, StrictOOSSplitValidationResult]"
    assert module._REQUIRED_MAPPING_KEYS == REQUIRED_KEYS
    assert module._OPTIONAL_MAPPING_KEYS == ("supersedes_split_assignment_id",)
    assert module._TIMESTAMP_FIELDS == ("fold_cutoff", "prediction_as_of", "input_publication_available_at", "target_start_at", "target_end_at", "label_available_at", "created_at")
    assert module._FIXED_POSTURES == (("primary_split_posture", "rolling_origin_or_walk_forward_required"), ("tuning_posture", "train_or_calibration_only"), ("calibration_posture", "separate_when_required"), ("baseline_parity_posture", "same_folds_and_eligibility_required"))


def test_mapping_roots_shape_and_unknown_keys_fail_closed():
    expected_missing = (C.MISSING_REQUIRED_FIELD,) * 29
    for root in (None, "x", [], (), object()):
        record, result = strict_oos_split_assignment_from_mapping(root)
        assert record is None
        assert codes(result) == expected_missing

    class Hostile(Mapping):
        def __iter__(self):
            raise RuntimeError("boom")
        def __len__(self):
            return 1
        def __getitem__(self, key):
            raise RuntimeError("boom")

    assert strict_oos_split_assignment_from_mapping(Hostile())[1].codes == expected_missing
    assert strict_oos_split_assignment_from_mapping({})[1].codes == expected_missing
    base = good().__dict__.copy()
    for missing in REQUIRED_KEYS:
        d = dict(base)
        d.pop(missing)
        assert strict_oos_split_assignment_from_mapping(d)[1].codes[0] is C.MISSING_REQUIRED_FIELD
    bad_key = "mar" + "ket" + "_" + "id"
    record, result = strict_oos_split_assignment_from_mapping({**base, bad_key: "forbidden"})
    assert record is None
    assert result.codes == (C.UNEXPECTED_FIELD,)
    assert strict_oos_split_assignment_from_mapping({**base, "z": 1, "a": 2})[1].codes == (C.UNEXPECTED_FIELD, C.UNEXPECTED_FIELD)
    assert strict_oos_split_assignment_from_mapping({**base, 3: 1, (2,): 2})[1].codes == (C.UNEXPECTED_FIELD, C.UNEXPECTED_FIELD)

    class S(str):
        pass
    d = dict(base)
    d.pop("condition_id")
    d[S("condition_id")] = "x"
    assert strict_oos_split_assignment_from_mapping(d)[1].codes == (C.MISSING_REQUIRED_FIELD, C.UNEXPECTED_FIELD)


def test_mapping_adaptation_text_enums_integer_applicability_provenance():
    base = good().__dict__.copy()
    as_strings = dict(base, split_role="test", assignment_status="assigned", overlap_control_posture="satisfied", applicability_modes=["primary_temporal", "leave_year_out"], provenance_refs=["a", "a"])
    record, result = strict_oos_split_assignment_from_mapping(as_strings)
    assert result.passed
    assert record.split_role is SplitRole.TEST
    assert record.applicability_modes == (SplitApplicabilityMode.PRIMARY_TEMPORAL, SplitApplicabilityMode.LEAVE_YEAR_OUT)
    assert record.provenance_refs == ("a", "a")

    class S(str):
        pass
    class I(int):
        pass
    class Other(Enum):
        TEST = "test"
    invalid = dict(base, split_assignment_id=" ", split_role=S("test"), assignment_status=Other.TEST, overlap_control_posture=S("satisfied"), applicability_modes=("leave_year_out",), fold_index=True, provenance_refs=["", 4])
    assert strict_oos_split_assignment_from_mapping(invalid)[1].codes == (C.BLANK_REQUIRED_TEXT, C.INVALID_SPLIT_ROLE, C.INVALID_APPLICABILITY_MODES, C.INVALID_ASSIGNMENT_STATUS, C.INVALID_OVERLAP_CONTROL_POSTURE, C.INVALID_INTEGER_FIELD, C.INVALID_PROVENANCE_REF, C.INVALID_PROVENANCE_REF)
    for value in (False, I(1), -1, "1"):
        assert codes(validate_strict_oos_split_assignment(good(fold_index=value))) == (C.INVALID_INTEGER_FIELD,)
    for value in ([], ["primary_temporal", "primary_temporal"], ["leave_year_out"], (SplitApplicabilityMode.PRIMARY_TEMPORAL, "leave_year_out"), "primary_temporal"):
        assert codes(validate_strict_oos_split_assignment(good(applicability_modes=value))).count(C.INVALID_APPLICABILITY_MODES) == 1


def test_direct_temporal_role_status_order_and_timestamp_preservation():
    bad = good(
        split_role=SplitRole.TRAIN,
        target_end_at="2025-01-02T00:00:00+00:00",
        label_available_at="bad",
        input_publication_available_at="2025-01-01T00:00:01+00:00",
        prediction_as_of="2025-01-01T00:00:00+00:00",
        provenance_refs=(),
    )
    assert codes(validate_strict_oos_split_assignment(bad)) == (C.INVALID_TIMESTAMP, C.INPUT_AVAILABLE_AFTER_PREDICTION, C.TRAIN_OR_CALIBRATION_AFTER_CUTOFF, C.TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF, C.EMPTY_PROVENANCE_REFS)
    assert bad.label_available_at == "bad"
    assert validate_strict_oos_split_assignment(good(fold_cutoff="2024-12-31T22:00:00+00:00", prediction_as_of="2024-12-31T22:00:00+00:00", input_publication_available_at="2024-12-31T22:00:00+00:00", target_start_at="2025-01-01T00:00:00+01:00", target_end_at="2024-12-31T23:00:00+00:00")).passed
    combo = good(target_start_at="2025-01-01T00:00:00+00:00", label_available_at="2025-01-01T00:00:00+00:00", exclusion_reason="x", overlap_control_posture=OverlapControlPosture.UNSATISFIED)
    assert codes(validate_strict_oos_split_assignment(combo)) == (C.TEST_NOT_STRICTLY_AFTER_CUTOFF, C.TEST_LABEL_AVAILABLE_BY_CUTOFF, C.ASSIGNED_WITH_EXCLUSION_REASON, C.UNSATISFIED_OVERLAP_CONTROL_ASSIGNED)
    blocked = good(assignment_status=SplitAssignmentStatus.BLOCKED, exclusion_reason=None, overlap_control_posture=OverlapControlPosture.UNSATISFIED, target_start_at="2025-01-01T00:00:00+00:00")
    assert codes(validate_strict_oos_split_assignment(blocked)) == (C.BLOCKED_WITHOUT_EXCLUSION_REASON,)
    assert codes(validate_strict_oos_split_assignment(good(fold_cutoff="naive"))) == (C.INVALID_TIMESTAMP,)
    assert codes(validate_strict_oos_split_assignment(good(created_at=4))) == (C.INVALID_TIMESTAMP,)


def test_fixed_posture_nullable_text_provenance_and_supersession():
    record = good(primary_split_posture="", tuning_posture="bad", calibration_posture="bad", baseline_parity_posture="bad", exclusion_reason=" ", supersedes_split_assignment_id=" ", provenance_refs=["x"])
    assert codes(validate_strict_oos_split_assignment(record)) == (C.BLANK_REQUIRED_TEXT, C.BLANK_REQUIRED_TEXT, C.INVALID_FIXED_POSTURE, C.INVALID_FIXED_POSTURE, C.INVALID_FIXED_POSTURE, C.INVALID_FIXED_POSTURE, C.ASSIGNED_WITH_EXCLUSION_REASON, C.INVALID_PROVENANCE_REF)
    assert codes(validate_strict_oos_split_assignment(good(supersedes_split_assignment_id="assign-1"))) == (C.SELF_SUPERSESSION,)
    assert validate_strict_oos_split_assignment(good(supersedes_split_assignment_id="other")).passed
    assert validate_strict_oos_split_assignment(good(supersedes_split_assignment_id=None)).passed
    assert codes(validate_strict_oos_split_assignment(good(split_assignment_id=" ", supersedes_split_assignment_id=" "))) == (C.BLANK_REQUIRED_TEXT, C.BLANK_REQUIRED_TEXT)


def test_mapping_combined_order_and_no_partial_records():
    base = good().__dict__.copy()
    d = dict(base)
    d.pop("split_id")
    d.pop("fold_id")
    d.update({"z": 1, "a": 2, "split_assignment_id": "", "split_role": "bad"})
    record, result = strict_oos_split_assignment_from_mapping(d)
    assert record is None
    assert result.codes == (C.MISSING_REQUIRED_FIELD, C.MISSING_REQUIRED_FIELD, C.UNEXPECTED_FIELD, C.UNEXPECTED_FIELD, C.BLANK_REQUIRED_TEXT, C.INVALID_SPLIT_ROLE)
    d = dict(base, applicability_modes=[], fold_index=-1)
    assert strict_oos_split_assignment_from_mapping(d)[1].codes == (C.INVALID_APPLICABILITY_MODES, C.INVALID_INTEGER_FIELD)
    d = dict(base, fold_cutoff="bad", created_at="bad", provenance_refs=["", 1])
    assert strict_oos_split_assignment_from_mapping(d)[1].codes == (C.INVALID_PROVENANCE_REF, C.INVALID_PROVENANCE_REF)


def test_collection_validation_order_and_comparisons_are_deterministic():
    assert codes(validate_strict_oos_split_assignments([])) == (C.INVALID_ASSIGNMENT_COLLECTION_TYPE,)
    assert codes(validate_strict_oos_split_assignments(())) == (C.EMPTY_ASSIGNMENT_COLLECTION,)
    r1 = good(split_assignment_id="a1", fold_id="f1", fold_index=0, prediction_record_id="p1", split_role=SplitRole.TEST)
    r2 = good(split_assignment_id="a1", fold_id="f2", fold_index=1, prediction_record_id="p1", split_role=SplitRole.TEST, fold_cutoff="2025-01-02T00:00:00+00:00", target_start_at="2025-01-03T00:00:00+00:00", target_end_at="2025-01-04T00:00:00+00:00")
    r3 = good(split_assignment_id="a3", fold_id="f2", fold_index=1, prediction_record_id="p1", split_id="split-2", split_version="v2", split_role=SplitRole.TRAIN, fold_cutoff="2025-01-02T00:00:00+00:00", target_start_at="2025-01-01T00:00:00+00:00", target_end_at="2025-01-01T00:00:00+00:00", label_available_at="2025-01-01T00:00:00+00:00")
    result = validate_strict_oos_split_assignments(("bad", r1, r2, r3))
    assert result.codes == (C.INVALID_ASSIGNMENT_COLLECTION_TYPE, C.DUPLICATE_ASSIGNMENT_ID, C.DUPLICATE_FOLD_RECORD_ASSIGNMENT, C.DUPLICATE_TEST_RECORD, C.INCONSISTENT_SPLIT_ID, C.INCONSISTENT_SPLIT_VERSION, C.LEAKAGE_GROUP_ROLE_CONFLICT)
    assert validate_strict_oos_split_assignments(("bad", r1, r2, r3)).codes == result.codes
    rev = good(split_assignment_id="a4", fold_id="f3", fold_index=3, prediction_record_id="p4", fold_cutoff="2025-01-01T00:00:00+00:00", target_start_at="2025-01-04T00:00:00+00:00", target_end_at="2025-01-05T00:00:00+00:00")
    assert codes(validate_strict_oos_split_assignments((r1, rev))) == (C.NON_MONOTONIC_FOLD_CUTOFF,)
    conflict = good(split_assignment_id="a5", fold_id="f1", fold_index=2, prediction_record_id="p5", fold_cutoff="2025-01-01T00:00:00+01:00")
    assert C.INCONSISTENT_FOLD_DEFINITION in codes(validate_strict_oos_split_assignments((r1, conflict)))


def test_source_audit_and_purity():
    source = Path("meg/weather/stage3/strict_oos_split.py").read_text()
    assert "mar" + "ket" + "_" + "id" not in source
    tree = ast.parse(source)
    imports = []
    forbidden_calls = {"open", "exec", "eval", "compile", "__import__"}
    forbidden_attrs = {"now", "utcnow", "today"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            imports.append((node.module, tuple(alias.name for alias in node.names)))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_attrs
    assert imports == [("__future__", ("annotations",)), ("collections.abc", ("Mapping",)), ("dataclasses", ("dataclass",)), ("datetime", ("datetime",)), ("enum", ("StrEnum",))]
    d = good().__dict__.copy()
    before = dict(d)
    strict_oos_split_assignment_from_mapping(d)
    assert d == before
    assert StrictOOSSplitValidationResult(SplitValidationSeverity.PASSED, True).codes == ()
