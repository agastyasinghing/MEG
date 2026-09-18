"""Immutable Stage 3 evidence-gate decisions and pure boundary validation.

This module deliberately validates only the gate-visible, caller-supplied record.
It neither evaluates a substantive gate rule nor loads upstream result records.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import re

from meg.weather.stage3.scoring_and_diagnostics import ScoringPredictionRepresentation
from meg.weather.stage3.evaluation_claim import (
    EvaluationClaimClass,
    EvaluationClaimDisposition,
    EvaluationClaimRecord,
)

__all__ = (
    "EvidenceGateComponent",
    "EvidenceGateComponentOutcome",
    "EvidenceGateDisposition",
    "EvidenceGateValidationSeverity",
    "EvidenceGateValidationCode",
    "EvidenceGateDecisionRecord",
    "EvidenceGateValidationResult",
    "evidence_gate_decision_from_mapping",
    "validate_evidence_gate_decision",
)


class EvidenceGateComponent(StrEnum):
    CROSS_BASELINE_PREDICTIVE_SKILL = "cross_baseline_predictive_skill"
    REPRESENTATION_APPROPRIATE_CALIBRATION = "representation_appropriate_calibration"
    THRESHOLD_WEIGHTED_SKILL_WHEN_APPLICABLE = "threshold_weighted_skill_when_applicable"
    STRATUM_SPECIFIC_SKILL_WHEN_APPLICABLE = "stratum_specific_skill_when_applicable"
    SELECTION_SCOPE_AND_NO_LOOKAHEAD_INTEGRITY = "selection_scope_and_no_lookahead_integrity"
    OVERALL_STAGE3_EVIDENCE_GATE = "overall_stage3_evidence_gate"


class EvidenceGateComponentOutcome(StrEnum):
    COMPONENT_SATISFIED = "component_satisfied"
    COMPONENT_NOT_SATISFIED = "component_not_satisfied"
    COMPONENT_INSUFFICIENT = "component_insufficient"
    COMPONENT_BLOCKED = "component_blocked"
    COMPONENT_UNAVAILABLE = "component_unavailable"
    COMPONENT_NOT_APPLICABLE = "component_not_applicable"


class EvidenceGateDisposition(StrEnum):
    STAGE3_GATE_PASSED = "stage3_gate_passed"
    STAGE3_GATE_NOT_PASSED = "stage3_gate_not_passed"
    STAGE3_GATE_INSUFFICIENT = "stage3_gate_insufficient"
    STAGE3_GATE_BLOCKED = "stage3_gate_blocked"
    STAGE3_GATE_UNAVAILABLE = "stage3_gate_unavailable"


class EvidenceGateValidationSeverity(StrEnum):
    PASSED = "passed"
    BLOCKED = "blocked"


class EvidenceGateValidationCode(StrEnum):
    MISSING_REQUIRED_FIELD = "missing_required_field"
    UNEXPECTED_FIELD = "unexpected_field"
    BLANK_REQUIRED_TEXT = "blank_required_text"
    INVALID_GATE_COMPONENT = "invalid_gate_component"
    INVALID_COMPONENT_OUTCOME = "invalid_component_outcome"
    INVALID_GATE_DISPOSITION = "invalid_gate_disposition"
    INVALID_PREDICTION_REPRESENTATION = "invalid_prediction_representation"
    INVALID_CLAIM_CLASS = "invalid_claim_class"
    INVALID_FIXED_POSTURE = "invalid_fixed_posture"
    INVALID_TEXT_TUPLE = "invalid_text_tuple"
    INVALID_CLAIM_ID_TUPLE = "invalid_claim_id_tuple"
    INVALID_CLAIM_CLASS_TUPLE = "invalid_claim_class_tuple"
    INVALID_COMPONENT_TUPLE = "invalid_component_tuple"
    INVALID_COMPONENT_OUTCOME_TUPLE = "invalid_component_outcome_tuple"
    CLAIM_SET_PARTITION_MISMATCH = "claim_set_partition_mismatch"
    CLAIM_CLASS_SEQUENCE_MISMATCH = "claim_class_sequence_mismatch"
    APPLICABILITY_MISMATCH = "applicability_mismatch"
    INVALID_CLAIM_RECORD_CONTAINER = "invalid_claim_record_container"
    INVALID_CLAIM_RECORD = "invalid_claim_record"
    DUPLICATE_CONTEXT_CLAIM_ID = "duplicate_context_claim_id"
    OBSERVED_CLAIM_NOT_FOUND = "observed_claim_not_found"
    UNEXPECTED_CONTEXT_CLAIM = "unexpected_context_claim"
    CLAIM_DISPOSITION_UNUSABLE = "claim_disposition_unusable"
    CLAIM_CLASS_MISMATCH = "claim_class_mismatch"
    CANDIDATE_IDENTITY_MISMATCH = "candidate_identity_mismatch"
    REPRESENTATION_MISMATCH = "representation_mismatch"
    SPLIT_SCOPE_MISMATCH = "split_scope_mismatch"
    PAIRED_RECORD_SET_MISMATCH = "paired_record_set_mismatch"
    AGGREGATION_WEIGHTING_MISMATCH = "aggregation_weighting_mismatch"
    STRATUM_SCOPE_MISMATCH = "stratum_scope_mismatch"
    INHERITED_POLICY_MISMATCH = "inherited_policy_mismatch"
    PROVENANCE_TRACEABILITY_MISMATCH = "provenance_traceability_mismatch"
    CROSS_BASELINE_INCOMPLETE = "cross_baseline_incomplete"
    CALIBRATION_REQUIREMENT_MISMATCH = "calibration_requirement_mismatch"
    THRESHOLD_APPLICABILITY_MISMATCH = "threshold_applicability_mismatch"
    STRATUM_APPLICABILITY_MISMATCH = "stratum_applicability_mismatch"
    NO_LOOKAHEAD_INTEGRITY_MISMATCH = "no_lookahead_integrity_mismatch"
    COMPONENT_OUTCOME_MISMATCH = "component_outcome_mismatch"
    DISPOSITION_PRECEDENCE_MISMATCH = "disposition_precedence_mismatch"
    COMPLETE_RULE_REQUIRED = "complete_rule_required"
    INVALID_PROVENANCE = "invalid_provenance"
    EMPTY_PROVENANCE = "empty_provenance"
    INVALID_DECISION_CREATED_AT = "invalid_decision_created_at"
    SELF_SUPERSESSION = "self_supersession"
    INVALID_SUPERSESSION_LINK = "invalid_supersession_link"


@dataclass(frozen=True)
class EvidenceGateDecisionRecord:
    evidence_gate_decision_id: str
    evidence_gate_id: str
    evidence_gate_version: str
    gate_rule_id: str
    gate_rule_version: str
    gate_disposition: EvidenceGateDisposition
    gate_disposition_reason: str
    target_posture: str
    candidate_method_id: str
    candidate_method_version: str
    prediction_representation: ScoringPredictionRepresentation
    required_evaluation_claim_ids: tuple[str, ...]
    observed_evaluation_claim_ids: tuple[str, ...]
    missing_evaluation_claim_ids: tuple[str, ...]
    required_claim_classes: tuple[EvaluationClaimClass, ...]
    observed_claim_classes: tuple[EvaluationClaimClass, ...]
    applicable_gate_components: tuple[EvidenceGateComponent, ...]
    component_outcomes: tuple[tuple[EvidenceGateComponent, EvidenceGateComponentOutcome], ...]
    split_id: str
    split_version: str
    fold_scope: str
    cutoff_scope: str
    paired_test_record_set_id: str
    aggregation_rule_ids: tuple[str, ...]
    weighting_rule_ids: tuple[str, ...]
    stratum_scope: tuple[str | None, ...]
    uncertainty_policy_ids: tuple[str, ...]
    sample_support_rule_ids: tuple[str, ...]
    selection_control_policy_ids: tuple[str, ...]
    multiple_comparison_policy_ids: tuple[str | None, ...]
    no_lookahead_review_posture: str
    result_chain_traceability_posture: str
    subsequent_approval_request_eligibility_posture: str
    provenance: tuple[str, ...]
    decision_created_at: str
    supersedes_decision_id_when_applicable: str | None = None


@dataclass(frozen=True)
class EvidenceGateValidationResult:
    severity: EvidenceGateValidationSeverity
    passed: bool
    codes: tuple[EvidenceGateValidationCode, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "codes", tuple(self.codes))
        if self.codes:
            object.__setattr__(self, "severity", EvidenceGateValidationSeverity.BLOCKED)
            object.__setattr__(self, "passed", False)
        else:
            object.__setattr__(self, "severity", EvidenceGateValidationSeverity.PASSED)
            object.__setattr__(self, "passed", True)
            object.__setattr__(self, "codes", ())


_FIELDS = tuple(EvidenceGateDecisionRecord.__dataclass_fields__)
_REQUIRED = _FIELDS[:-1]
_OPTIONAL = _FIELDS[-1:]
_TEXT = _FIELDS[:5] + _FIELDS[6:10] + _FIELDS[18:23] + _FIELDS[30:33] + (_FIELDS[34],)
_TEXT_TUPLES = _FIELDS[23:30] + (_FIELDS[33],)
_NULLABLE_TUPLES = (_FIELDS[25], _FIELDS[29])
_ID_TUPLES = _FIELDS[11:14]
_CLASS_TUPLES = _FIELDS[14:16]
_LIST_FIELDS = _ID_TUPLES + _CLASS_TUPLES + (_FIELDS[16], _FIELDS[17]) + _TEXT_TUPLES
_COMPONENTS = tuple(EvidenceGateComponent)
_MANDATORY = (_COMPONENTS[0], _COMPONENTS[1], _COMPONENTS[4], _COMPONENTS[5])
_FIXED = (
    ("target_posture", "venue_defined_settlement_outcome"),
    ("no_lookahead_review_posture", "predeclared_point_in_time_review_completed"),
    ("result_chain_traceability_posture", "complete_immutable_result_chain_required"),
)
_ELIGIBILITY = {
    EvidenceGateDisposition.STAGE3_GATE_PASSED: "eligible_for_later_separate_readiness_or_approval_request_only",
    EvidenceGateDisposition.STAGE3_GATE_NOT_PASSED: "not_eligible_for_implementation_handoff",
    EvidenceGateDisposition.STAGE3_GATE_INSUFFICIENT: "not_eligible_for_implementation_handoff",
    EvidenceGateDisposition.STAGE3_GATE_BLOCKED: "not_eligible_for_implementation_handoff",
    EvidenceGateDisposition.STAGE3_GATE_UNAVAILABLE: "not_eligible_for_implementation_handoff",
}
_CALIBRATION = {
    ScoringPredictionRepresentation.BINARY_OUTCOME_PROBABILITY: EvaluationClaimClass.BINARY_CALIBRATION_BEHAVIOR,
    ScoringPredictionRepresentation.FULL_PREDICTIVE_DISTRIBUTION: EvaluationClaimClass.DISTRIBUTIONAL_CALIBRATION_BEHAVIOR,
    ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE: EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR,
}


def _result(codes: list[EvidenceGateValidationCode] | tuple[EvidenceGateValidationCode, ...]) -> EvidenceGateValidationResult:
    return EvidenceGateValidationResult(EvidenceGateValidationSeverity.BLOCKED, False, tuple(codes))


def _text(value: object) -> bool:
    return type(value) is str and bool(value.strip())


def _timestamp(value: object) -> bool:
    if type(value) is not str or "T" not in value:
        return False
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    if not value.endswith("Z") and re.search(r"[+-]\d{2}:\d{2}$", value) is None:
        return False
    try:
        return datetime.fromisoformat(candidate).utcoffset() is not None
    except (ValueError, OverflowError):
        return False


def _ordered_subsequence(needle: tuple[object, ...], haystack: tuple[object, ...]) -> bool:
    iterator = iter(haystack)
    return all(any(candidate == item for candidate in iterator) for item in needle)


def evidence_gate_decision_from_mapping(
    mapping: object,
    evaluation_claims: object,
) -> tuple[EvidenceGateDecisionRecord | None, EvidenceGateValidationResult]:
    code = EvidenceGateValidationCode
    unreadable = (code.MISSING_REQUIRED_FIELD,) * len(_REQUIRED)
    if not isinstance(mapping, Mapping):
        return None, _result(unreadable)
    try:
        items = tuple(mapping.items())
        keys: list[object] = []
        for item in items:
            key, unused = item
            if any(existing == key for existing in keys):
                return None, _result(unreadable)
            keys.append(key)
        for key in keys:
            hash(key)
        values = dict(items)
        exact_keys = tuple(key for key in keys if type(key) is str)
        adapted = {key: values[key] for key in exact_keys if key in _FIELDS}
        enum_fields = (
            ("gate_disposition", EvidenceGateDisposition),
            ("prediction_representation", ScoringPredictionRepresentation),
        )
        for field, enum_type in enum_fields:
            value = adapted.get(field)
            if type(value) is str:
                try:
                    adapted[field] = enum_type(value)
                except ValueError:
                    pass
        for field in _LIST_FIELDS:
            if type(adapted.get(field)) is list:
                adapted[field] = tuple(adapted[field])
        for field in _CLASS_TUPLES:
            value = adapted.get(field)
            if type(value) is tuple:
                adapted[field] = tuple(
                    EvaluationClaimClass(item) if type(item) is str and item in EvaluationClaimClass._value2member_map_ else item
                    for item in value
                )
        value = adapted.get("applicable_gate_components")
        if type(value) is tuple:
            adapted["applicable_gate_components"] = tuple(
                EvidenceGateComponent(item) if type(item) is str and item in EvidenceGateComponent._value2member_map_ else item
                for item in value
            )
        value = adapted.get("component_outcomes")
        if type(value) is tuple:
            pairs = []
            for pair in value:
                if type(pair) is list:
                    pair = tuple(pair)
                if type(pair) is tuple and len(pair) == 2:
                    component, outcome = pair
                    if type(component) is str and component in EvidenceGateComponent._value2member_map_:
                        component = EvidenceGateComponent(component)
                    if type(outcome) is str and outcome in EvidenceGateComponentOutcome._value2member_map_:
                        outcome = EvidenceGateComponentOutcome(outcome)
                    pair = (component, outcome)
                pairs.append(pair)
            adapted["component_outcomes"] = tuple(pairs)
    except Exception:
        return None, _result(unreadable)

    exact = set(exact_keys)
    codes = [code.MISSING_REQUIRED_FIELD for key in _REQUIRED if key not in exact]
    allowed = set(_FIELDS)
    codes += [code.UNEXPECTED_FIELD for key in sorted(key for key in exact_keys if key not in allowed)]
    codes += [code.UNEXPECTED_FIELD for key in keys if type(key) is not str]

    context = evaluation_claims
    if type(context) is list and all(type(item) is EvaluationClaimRecord for item in context):
        context = tuple(context)
    semantic = _validate_values(adapted, exact & allowed, context)
    combined = tuple(codes) + semantic
    if combined:
        return None, _result(combined)
    try:
        return EvidenceGateDecisionRecord(**adapted), _result(())
    except Exception:
        return None, _result(unreadable)


def _validate_values(values: Mapping[str, object], present: set[str], context: object) -> tuple[EvidenceGateValidationCode, ...]:
    code = EvidenceGateValidationCode
    codes: list[EvidenceGateValidationCode] = []

    # 4. required_and_nullable_text
    for field in _TEXT:
        if field in present and not _text(values.get(field)):
            codes.append(code.BLANK_REQUIRED_TEXT)
    supersedes = values.get("supersedes_decision_id_when_applicable")
    if "supersedes_decision_id_when_applicable" in present and supersedes is not None and not _text(supersedes):
        codes.append(code.BLANK_REQUIRED_TEXT)

    applicable = values.get("applicable_gate_components")
    pairs = values.get("component_outcomes")
    if type(applicable) is tuple:
        codes += [code.INVALID_GATE_COMPONENT for item in applicable if type(item) is not EvidenceGateComponent]
    if type(pairs) is tuple:
        for pair in pairs:
            if type(pair) is tuple and len(pair) == 2:
                if type(pair[0]) is not EvidenceGateComponent:
                    codes.append(code.INVALID_GATE_COMPONENT)
        for pair in pairs:
            if type(pair) is tuple and len(pair) == 2:
                if type(pair[1]) is not EvidenceGateComponentOutcome:
                    codes.append(code.INVALID_COMPONENT_OUTCOME)

    disposition_ok = "gate_disposition" in present and type(values.get("gate_disposition")) is EvidenceGateDisposition
    if "gate_disposition" in present and not disposition_ok:
        codes.append(code.INVALID_GATE_DISPOSITION)
    representation_ok = "prediction_representation" in present and type(values.get("prediction_representation")) is ScoringPredictionRepresentation
    if "prediction_representation" in present and not representation_ok:
        codes.append(code.INVALID_PREDICTION_REPRESENTATION)

    for field in _CLASS_TUPLES:
        value = values.get(field)
        if type(value) is tuple:
            codes += [code.INVALID_CLAIM_CLASS for item in value if type(item) is not EvaluationClaimClass]

    for field, expected in _FIXED:
        value = values.get(field)
        if field in present and _text(value) and value != expected:
            codes.append(code.INVALID_FIXED_POSTURE)
    if disposition_ok and _text(values.get("subsequent_approval_request_eligibility_posture")) and values.get("subsequent_approval_request_eligibility_posture") != _ELIGIBILITY[values["gate_disposition"]]:
        codes.append(code.INVALID_FIXED_POSTURE)

    tuple_valid: dict[str, bool] = {}
    for field in _TEXT_TUPLES:
        value = values.get(field)
        outer = field in present and type(value) is tuple
        tuple_valid[field] = outer and all(
            (item is None and field in _NULLABLE_TUPLES) or _text(item)
            for item in value
        )
        if field in present:
            if not outer:
                codes.append(code.INVALID_TEXT_TUPLE)
            else:
                for item in value:
                    if not ((item is None and field in _NULLABLE_TUPLES) or _text(item)):
                        codes.append(code.INVALID_TEXT_TUPLE)

    id_valid: dict[str, bool] = {}
    for field in _ID_TUPLES:
        value = values.get(field)
        valid = field in present and type(value) is tuple and all(_text(item) for item in value) and len(value) == len(set(value))
        id_valid[field] = valid
        if field in present and not valid:
            codes.append(code.INVALID_CLAIM_ID_TUPLE)

    class_valid: dict[str, bool] = {}
    for field in _CLASS_TUPLES:
        value = values.get(field)
        valid = field in present and type(value) is tuple and all(type(item) is EvaluationClaimClass for item in value)
        class_valid[field] = valid
        if field in present and not valid:
            codes.append(code.INVALID_CLAIM_CLASS_TUPLE)

    applicable_ok = (
        type(applicable) is tuple
        and all(type(item) is EvidenceGateComponent for item in applicable)
        and tuple(item for item in _COMPONENTS if item in applicable) == applicable
        and all(item in applicable for item in _MANDATORY)
        and len(applicable) in (4, 5, 6)
    )
    if "applicable_gate_components" in present and not applicable_ok:
        codes.append(code.INVALID_COMPONENT_TUPLE)
    pairs_ok = type(pairs) is tuple and len(pairs) == 6 and all(
        type(pair) is tuple and len(pair) == 2 and type(pair[0]) is EvidenceGateComponent
        and type(pair[1]) is EvidenceGateComponentOutcome and pair[0] is _COMPONENTS[index]
        for index, pair in enumerate(pairs)
    )
    if "component_outcomes" in present and not pairs_ok:
        codes.append(code.INVALID_COMPONENT_OUTCOME_TUPLE)

    required = values.get("required_evaluation_claim_ids")
    observed = values.get("observed_evaluation_claim_ids")
    missing = values.get("missing_evaluation_claim_ids")
    partition_ok = all(id_valid.values()) and (
        set(observed).isdisjoint(missing)
        and set(observed) | set(missing) == set(required)
        and tuple(item for item in required if item in observed) == observed
        and tuple(item for item in required if item in missing) == missing
    )
    if all(id_valid.values()) and not partition_ok:
        codes.append(code.CLAIM_SET_PARTITION_MISMATCH)

    required_classes = values.get("required_claim_classes")
    observed_classes = values.get("observed_claim_classes")
    required_alignment = id_valid[_ID_TUPLES[0]] and class_valid[_CLASS_TUPLES[0]] and len(required) == len(required_classes)
    if id_valid[_ID_TUPLES[0]] and class_valid[_CLASS_TUPLES[0]] and not required_alignment:
        codes.append(code.CLAIM_CLASS_SEQUENCE_MISMATCH)
    observed_alignment = id_valid[_ID_TUPLES[1]] and class_valid[_CLASS_TUPLES[1]] and len(observed) == len(observed_classes)
    expected_observed_classes = ()
    if required_alignment and id_valid[_ID_TUPLES[1]]:
        expected_observed_classes = tuple(required_classes[i] for i, identity in enumerate(required) if identity in observed)
    if id_valid[_ID_TUPLES[1]] and class_valid[_CLASS_TUPLES[1]] and (not observed_alignment or (required_alignment and observed_classes != expected_observed_classes)):
        codes.append(code.CLAIM_CLASS_SEQUENCE_MISMATCH)

    outcomes = dict(pairs) if pairs_ok else {}
    if applicable_ok and pairs_ok:
        for component in _COMPONENTS:
            outcome = outcomes[component]
            if component in _MANDATORY and outcome is EvidenceGateComponentOutcome.COMPONENT_NOT_APPLICABLE:
                codes.append(code.APPLICABILITY_MISMATCH)
            elif component in (_COMPONENTS[2], _COMPONENTS[3]) and ((component in applicable) == (outcome is EvidenceGateComponentOutcome.COMPONENT_NOT_APPLICABLE)):
                codes.append(code.APPLICABILITY_MISMATCH)

    context_ok = type(context) is tuple
    if not context_ok:
        codes.append(code.INVALID_CLAIM_RECORD_CONTAINER)
    exact_claims: list[EvaluationClaimRecord] = []
    if context_ok:
        for item in context:
            if type(item) is not EvaluationClaimRecord:
                codes.append(code.INVALID_CLAIM_RECORD)
            else:
                exact_claims.append(item)

    counts: dict[str, int] = {}
    usable_id_claims: list[EvaluationClaimRecord] = []
    if context_ok:
        for claim in exact_claims:
            if _text(claim.evaluation_claim_id):
                counts[claim.evaluation_claim_id] = counts.get(claim.evaluation_claim_id, 0) + 1
                if counts[claim.evaluation_claim_id] > 1:
                    codes.append(code.DUPLICATE_CONTEXT_CLAIM_ID)
                usable_id_claims.append(claim)
    resolved: dict[str, EvaluationClaimRecord] = {}
    if context_ok and id_valid[_ID_TUPLES[1]]:
        ordered_context_ids = tuple(
            claim.evaluation_claim_id
            for claim in exact_claims
            if _text(claim.evaluation_claim_id)
        )
        for identity in observed:
            matches = [claim for claim in usable_id_claims if claim.evaluation_claim_id == identity]
            position = observed.index(identity)
            in_required_position = (
                position < len(ordered_context_ids)
                and ordered_context_ids[position] == identity
            )
            if len(matches) != 1 or not in_required_position:
                codes.append(code.OBSERVED_CLAIM_NOT_FOUND)
            else:
                resolved[identity] = matches[0]
        for claim in usable_id_claims:
            if counts[claim.evaluation_claim_id] == 1 and claim.evaluation_claim_id not in observed:
                codes.append(code.UNEXPECTED_CONTEXT_CLAIM)

    usable_disposition: dict[str, EvaluationClaimDisposition] = {}
    if id_valid[_ID_TUPLES[1]]:
        for identity in observed:
            claim = resolved.get(identity)
            if claim is not None:
                if type(claim.claim_disposition) is not EvaluationClaimDisposition:
                    codes.append(code.CLAIM_DISPOSITION_UNUSABLE)
                else:
                    usable_disposition[identity] = claim.claim_disposition

    positions = {identity: index for index, identity in enumerate(required)} if id_valid[_ID_TUPLES[0]] else {}
    earlier_integrity_failure = False
    evidence_issues: set[str] = set()
    for identity in observed if id_valid[_ID_TUPLES[1]] else ():
        claim = resolved.get(identity)
        pos = positions.get(identity)
        if claim is None:
            continue
        if observed_alignment and required_alignment and pos is not None and (claim.claim_class is not observed_classes[observed.index(identity)] or claim.claim_class is not required_classes[pos]):
            codes.append(code.CLAIM_CLASS_MISMATCH)
            evidence_issues.add(identity)
        if _text(values.get("candidate_method_id")) and _text(values.get("candidate_method_version")) and (claim.candidate_method_id != values["candidate_method_id"] or claim.candidate_method_version != values["candidate_method_version"]):
            codes.append(code.CANDIDATE_IDENTITY_MISMATCH)
            evidence_issues.add(identity)
        if representation_ok and claim.prediction_representation is not values["prediction_representation"]:
            codes.append(code.REPRESENTATION_MISMATCH)
            evidence_issues.add(identity)
        if all(_text(values.get(field)) for field in ("split_id", "split_version", "fold_scope", "cutoff_scope")) and (
            claim.split_id != values["split_id"] or claim.split_version != values["split_version"]
            or claim.fold_scope != values["fold_scope"] or claim.cutoff_scope != values["cutoff_scope"]
        ):
            codes.append(code.SPLIT_SCOPE_MISMATCH)
            earlier_integrity_failure = True
            evidence_issues.add(identity)
        if _text(values.get("paired_test_record_set_id")) and claim.paired_test_record_set_id != values["paired_test_record_set_id"]:
            codes.append(code.PAIRED_RECORD_SET_MISMATCH)
            evidence_issues.add(identity)
        aggregation_usable = pos is not None and tuple_valid.get("aggregation_rule_ids") and tuple_valid.get("weighting_rule_ids")
        aggregation_mismatch = aggregation_usable and (
            len(values["aggregation_rule_ids"]) != len(required)
            or len(values["weighting_rule_ids"]) != len(required)
            or claim.aggregation_rule_id != values["aggregation_rule_ids"][pos]
            or claim.weighting_rule_id != values["weighting_rule_ids"][pos]
        )
        if aggregation_mismatch:
            codes.append(code.AGGREGATION_WEIGHTING_MISMATCH)
            evidence_issues.add(identity)
        stratum_usable = pos is not None and tuple_valid.get("stratum_scope")
        stratum_mismatch = stratum_usable and (
            len(values["stratum_scope"]) != len(required)
            or claim.stratum_id_when_applicable != values["stratum_scope"][pos]
        )
        if stratum_mismatch:
            codes.append(code.STRATUM_SCOPE_MISMATCH)
            evidence_issues.add(identity)
        policy_fields = (
            ("uncertainty_policy_ids", "uncertainty_policy_id"),
            ("sample_support_rule_ids", "sample_support_rule_id"),
            ("selection_control_policy_ids", "selection_control_policy_id"),
            ("multiple_comparison_policy_ids", "multiple_comparison_policy_id_when_applicable"),
        )
        for decision_field, claim_field in policy_fields:
            policy_mismatch = pos is not None and tuple_valid.get(decision_field) and (
                len(values[decision_field]) != len(required)
                or getattr(claim, claim_field) != values[decision_field][pos]
            )
            if policy_mismatch:
                codes.append(code.INHERITED_POLICY_MISMATCH)
                evidence_issues.add(identity)
                if decision_field == "selection_control_policy_ids":
                    earlier_integrity_failure = True

    provenance_ok = type(values.get("provenance")) is tuple and all(_text(item) for item in values.get("provenance", ()))
    traceability_failures: set[str] = set()
    if values.get("result_chain_traceability_posture") == _FIXED[2][1] and provenance_ok and id_valid[_ID_TUPLES[1]]:
        provenance = values["provenance"]
        for identity in observed:
            claim = resolved.get(identity)
            if claim is None:
                continue
            bad = identity not in provenance or type(claim.provenance) is not tuple or not _ordered_subsequence(claim.provenance, provenance)
            if type(claim.observed_evaluation_result_ids) is tuple:
                bad = bad or any(
                    result_id not in provenance
                    for result_id in claim.observed_evaluation_result_ids
                )
            else:
                bad = True
            if claim.claim_disposition in (EvaluationClaimDisposition.CLAIM_SUPPORTED, EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED):
                bad = bad or claim.observed_evaluation_result_ids != claim.required_evaluation_result_ids or claim.missing_evaluation_result_ids != ()
            if bad:
                codes.append(code.PROVENANCE_TRACEABILITY_MISMATCH)
                traceability_failures.add(identity)
                evidence_issues.add(identity)
                earlier_integrity_failure = True

    class_list = tuple(required_classes) if required_alignment else ()
    cross_class = EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES
    cross_bad = not required_alignment
    if required_alignment:
        cross_positions = [i for i, item in enumerate(class_list) if item is cross_class]
        cross_bad = len(cross_positions) != 1
        if len(cross_positions) == 1:
            identity = required[cross_positions[0]]
            claim = resolved.get(identity)
            cross_bad = claim is None or identity in traceability_failures or identity not in usable_disposition
            if claim is not None:
                cross_bad = cross_bad or type(claim.required_evaluation_result_ids) is not tuple or type(claim.observed_evaluation_result_ids) is not tuple or type(claim.missing_evaluation_result_ids) is not tuple
        if cross_bad:
            codes.append(code.CROSS_BASELINE_INCOMPLETE)
    calibration_bad = not (required_alignment and representation_ok)
    if required_alignment and representation_ok:
        selected = _CALIBRATION[values["prediction_representation"]]
        calibration_classes = set(_CALIBRATION.values())
        calibration_bad = class_list.count(selected) != 1 or any(item in calibration_classes and item is not selected for item in class_list)
        if calibration_bad:
            codes.append(code.CALIBRATION_REQUIREMENT_MISMATCH)

    threshold = _COMPONENTS[2]
    stratum = _COMPONENTS[3]
    threshold_bad = not (applicable_ok and pairs_ok and required_alignment)
    stratum_bad = threshold_bad
    if applicable_ok and pairs_ok and required_alignment:
        threshold_positions = [i for i, item in enumerate(class_list) if item is EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL]
        threshold_bad = (threshold in applicable) != bool(threshold_positions) or ((threshold in applicable) == (outcomes[threshold] is EvidenceGateComponentOutcome.COMPONENT_NOT_APPLICABLE))
        if threshold_bad:
            codes.append(code.THRESHOLD_APPLICABILITY_MISMATCH)
        stratum_positions = [i for i, item in enumerate(class_list) if item is EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL]
        scopes_ok = tuple_valid.get("stratum_scope") and len(values["stratum_scope"]) == len(required)
        relevant_scopes = [values["stratum_scope"][i] for i in stratum_positions] if scopes_ok else []
        stratum_bad = (stratum in applicable) != bool(stratum_positions) or (bool(stratum_positions) and (not scopes_ok or any(not _text(item) for item in relevant_scopes))) or ((stratum in applicable) == (outcomes[stratum] is EvidenceGateComponentOutcome.COMPONENT_NOT_APPLICABLE))
        if stratum_bad:
            codes.append(code.STRATUM_APPLICABILITY_MISMATCH)

    if values.get("no_lookahead_review_posture") == _FIXED[1][1] and pairs_ok and outcomes[_COMPONENTS[4]] is EvidenceGateComponentOutcome.COMPONENT_SATISFIED and earlier_integrity_failure:
        codes.append(code.NO_LOOKAHEAD_INTEGRITY_MISMATCH)

    component_claim_classes = {
        _COMPONENTS[0]: (EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES,),
        _COMPONENTS[1]: tuple(_CALIBRATION.values()),
        _COMPONENTS[2]: (EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL,),
        _COMPONENTS[3]: (EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL,),
    }
    strongest_rank = {
        EvaluationClaimDisposition.CLAIM_BLOCKED: 3,
        EvaluationClaimDisposition.CLAIM_UNAVAILABLE: 2,
        EvaluationClaimDisposition.CLAIM_INSUFFICIENT: 1,
    }
    expected_by_rank = {3: EvidenceGateComponentOutcome.COMPONENT_BLOCKED, 2: EvidenceGateComponentOutcome.COMPONENT_UNAVAILABLE, 1: EvidenceGateComponentOutcome.COMPONENT_INSUFFICIENT}
    if applicable_ok and pairs_ok and required_alignment:
        component_prerequisites = {
            _COMPONENTS[0]: not cross_bad,
            _COMPONENTS[1]: not calibration_bad,
            _COMPONENTS[2]: not threshold_bad,
            _COMPONENTS[3]: not stratum_bad,
        }
        for component, classes in component_claim_classes.items():
            if component not in applicable or not component_prerequisites[component]:
                continue
            relevant = [required[i] for i, item in enumerate(class_list) if item in classes]
            if not relevant or any(identity not in usable_disposition for identity in relevant):
                continue
            dispositions = [usable_disposition[identity] for identity in relevant]
            rank = max((strongest_rank.get(item, 0) for item in dispositions), default=0)
            outcome = outcomes[component]
            mismatch = rank and outcome is not expected_by_rank[rank]
            if not rank and EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED in dispositions and outcome is not EvidenceGateComponentOutcome.COMPONENT_NOT_SATISFIED:
                mismatch = True
            if not rank and outcome is EvidenceGateComponentOutcome.COMPONENT_SATISFIED and any(item is not EvaluationClaimDisposition.CLAIM_SUPPORTED for item in dispositions):
                mismatch = True
            if mismatch:
                codes.append(code.COMPONENT_OUTCOME_MISMATCH)

    complete = (
        partition_ok
        and not missing
        and id_valid[_ID_TUPLES[1]]
        and context_ok
        and len(resolved) == len(observed)
        and all(identity in usable_disposition for identity in observed)
        and not evidence_issues
        and required_alignment
        and observed_alignment
        and observed_classes == expected_observed_classes
        and applicable_ok
        and pairs_ok
        and not cross_bad
        and not calibration_bad
        and not threshold_bad
        and not stratum_bad
    )
    expected_outcome = None
    if applicable_ok and pairs_ok:
        structural = []
        for component in applicable:
            if component is _COMPONENTS[5]:
                continue
            outcome = outcomes[component]
            structural.append({EvidenceGateComponentOutcome.COMPONENT_BLOCKED: 3, EvidenceGateComponentOutcome.COMPONENT_UNAVAILABLE: 2, EvidenceGateComponentOutcome.COMPONENT_INSUFFICIENT: 1}.get(outcome, 0))
        structural.extend(strongest_rank.get(item, 0) for item in usable_disposition.values())
        rank = max(structural, default=0)
        overall_outcome = outcomes[_COMPONENTS[5]]
        expected_outcome = expected_by_rank.get(
            rank,
            overall_outcome
            if complete and overall_outcome in (
                EvidenceGateComponentOutcome.COMPONENT_SATISFIED,
                EvidenceGateComponentOutcome.COMPONENT_NOT_SATISFIED,
            )
            else None,
        )
        if rank and outcomes[_COMPONENTS[5]] is not expected_outcome:
            codes.append(code.COMPONENT_OUTCOME_MISMATCH)
        elif not rank and overall_outcome not in (
            EvidenceGateComponentOutcome.COMPONENT_SATISFIED,
            EvidenceGateComponentOutcome.COMPONENT_NOT_SATISFIED,
        ):
            codes.append(code.COMPONENT_OUTCOME_MISMATCH)

    expected_disposition = {
        EvidenceGateComponentOutcome.COMPONENT_BLOCKED: EvidenceGateDisposition.STAGE3_GATE_BLOCKED,
        EvidenceGateComponentOutcome.COMPONENT_UNAVAILABLE: EvidenceGateDisposition.STAGE3_GATE_UNAVAILABLE,
        EvidenceGateComponentOutcome.COMPONENT_INSUFFICIENT: EvidenceGateDisposition.STAGE3_GATE_INSUFFICIENT,
        EvidenceGateComponentOutcome.COMPONENT_SATISFIED: EvidenceGateDisposition.STAGE3_GATE_PASSED,
        EvidenceGateComponentOutcome.COMPONENT_NOT_SATISFIED: EvidenceGateDisposition.STAGE3_GATE_NOT_PASSED,
    }.get(expected_outcome)
    if disposition_ok and expected_disposition is not None and values["gate_disposition"] is not expected_disposition:
        codes.append(code.DISPOSITION_PRECEDENCE_MISMATCH)
    if disposition_ok and (values["gate_disposition"] in (EvidenceGateDisposition.STAGE3_GATE_PASSED, EvidenceGateDisposition.STAGE3_GATE_NOT_PASSED) and not complete or expected_disposition is None):
        codes.append(code.COMPLETE_RULE_REQUIRED)

    provenance = values.get("provenance")
    if "provenance" in present and type(provenance) is tuple:
        for item in provenance:
            if not _text(item):
                codes.append(code.INVALID_PROVENANCE)
        if not provenance:
            codes.append(code.EMPTY_PROVENANCE)
    if "decision_created_at" in present and not _timestamp(values.get("decision_created_at")):
        codes.append(code.INVALID_DECISION_CREATED_AT)
    if _text(values.get("evidence_gate_decision_id")) and _text(supersedes) and supersedes == values["evidence_gate_decision_id"]:
        codes.append(code.SELF_SUPERSESSION)
    if _text(supersedes) and _text(values.get("evidence_gate_decision_id")) and supersedes != values["evidence_gate_decision_id"] and provenance_ok and supersedes not in provenance:
        codes.append(code.INVALID_SUPERSESSION_LINK)
    return tuple(codes)


def validate_evidence_gate_decision(
    record: EvidenceGateDecisionRecord,
    evaluation_claims: tuple[EvaluationClaimRecord, ...],
) -> EvidenceGateValidationResult:
    values = {field: getattr(record, field) for field in _FIELDS}
    return _result(_validate_values(values, set(_FIELDS), evaluation_claims))
