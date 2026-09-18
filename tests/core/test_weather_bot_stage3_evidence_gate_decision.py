"""Independent adversarial oracle for the Stage 3 evidence-gate boundary."""

from __future__ import annotations

from collections.abc import Mapping
import ast
import copy
import dataclasses
from dataclasses import replace
import inspect
from pathlib import Path

import pytest

from meg.weather.stage3.evaluation_claim import (
    EvaluationClaimClass,
    EvaluationClaimDisposition,
    EvaluationClaimRecord,
)
from meg.weather.stage3.scoring_and_diagnostics import ScoringPredictionRepresentation
from meg.weather.stage3.evidence_gate_decision import (
    EvidenceGateComponent,
    EvidenceGateComponentOutcome,
    EvidenceGateDecisionRecord,
    EvidenceGateDisposition,
    EvidenceGateValidationCode,
    EvidenceGateValidationResult,
    EvidenceGateValidationSeverity,
    evidence_gate_decision_from_mapping,
    validate_evidence_gate_decision,
)


PUBLIC = (
    "EvidenceGateComponent", "EvidenceGateComponentOutcome", "EvidenceGateDisposition",
    "EvidenceGateValidationSeverity", "EvidenceGateValidationCode",
    "EvidenceGateDecisionRecord", "EvidenceGateValidationResult",
    "evidence_gate_decision_from_mapping", "validate_evidence_gate_decision",
)
COMPONENT_VALUES = (
    "cross_baseline_predictive_skill", "representation_appropriate_calibration",
    "threshold_weighted_skill_when_applicable", "stratum_specific_skill_when_applicable",
    "selection_scope_and_no_lookahead_integrity", "overall_stage3_evidence_gate",
)
OUTCOME_VALUES = (
    "component_satisfied", "component_not_satisfied", "component_insufficient",
    "component_blocked", "component_unavailable", "component_not_applicable",
)
DISPOSITION_VALUES = (
    "stage3_gate_passed", "stage3_gate_not_passed", "stage3_gate_insufficient",
    "stage3_gate_blocked", "stage3_gate_unavailable",
)
CODE_VALUES = (
    "missing_required_field", "unexpected_field", "blank_required_text",
    "invalid_gate_component", "invalid_component_outcome", "invalid_gate_disposition",
    "invalid_prediction_representation", "invalid_claim_class", "invalid_fixed_posture",
    "invalid_text_tuple", "invalid_claim_id_tuple", "invalid_claim_class_tuple",
    "invalid_component_tuple", "invalid_component_outcome_tuple",
    "claim_set_partition_mismatch", "claim_class_sequence_mismatch",
    "applicability_mismatch", "invalid_claim_record_container", "invalid_claim_record",
    "duplicate_context_claim_id", "observed_claim_not_found", "unexpected_context_claim",
    "claim_disposition_unusable", "claim_class_mismatch", "candidate_identity_mismatch",
    "representation_mismatch", "split_scope_mismatch", "paired_record_set_mismatch",
    "aggregation_weighting_mismatch", "stratum_scope_mismatch",
    "inherited_policy_mismatch", "provenance_traceability_mismatch",
    "cross_baseline_incomplete", "calibration_requirement_mismatch",
    "threshold_applicability_mismatch", "stratum_applicability_mismatch",
    "no_lookahead_integrity_mismatch", "component_outcome_mismatch",
    "disposition_precedence_mismatch", "complete_rule_required", "invalid_provenance",
    "empty_provenance", "invalid_decision_created_at", "self_supersession",
    "invalid_supersession_link",
)
FIELDS = (
    "evidence_gate_decision_id", "evidence_gate_id", "evidence_gate_version",
    "gate_rule_id", "gate_rule_version", "gate_disposition", "gate_disposition_reason",
    "target_posture", "candidate_method_id", "candidate_method_version",
    "prediction_representation", "required_evaluation_claim_ids",
    "observed_evaluation_claim_ids", "missing_evaluation_claim_ids",
    "required_claim_classes", "observed_claim_classes", "applicable_gate_components",
    "component_outcomes", "split_id", "split_version", "fold_scope", "cutoff_scope",
    "paired_test_record_set_id", "aggregation_rule_ids", "weighting_rule_ids",
    "stratum_scope", "uncertainty_policy_ids", "sample_support_rule_ids",
    "selection_control_policy_ids", "multiple_comparison_policy_ids",
    "no_lookahead_review_posture", "result_chain_traceability_posture",
    "subsequent_approval_request_eligibility_posture", "provenance",
    "decision_created_at", "supersedes_decision_id_when_applicable",
)
COVERAGE_MANIFEST = {
    "public_api": "test_public_contract_is_literal_and_frozen",
    "all_validation_codes": "test_public_contract_is_literal_and_frozen",
    "mapping_root_and_baseexception": "test_mapping_catches_exception_but_propagates_baseexception",
    "asymmetric_equality": "test_duplicate_comparison_direction_is_existing_to_incoming",
    "mapping_shape_order": "test_each_required_key_and_unexpected_key_order",
    "adaptation_and_preservation": "test_adapter_exact_adaptation_and_caller_preservation",
    "direct_no_adaptation": "test_direct_validation_does_not_adapt_lists",
    "applicability_4_5_6": "test_all_applicability_combinations_and_always_six_outcomes",
    "context_trust_boundary": "test_context_exact_type_order_duplicates_and_unexpected_claims",
    "partition_and_classes": "test_partition_interleaving_and_repeated_classes_are_valid",
    "structural_precedence": "test_structural_precedence",
    "supported_floor": "test_not_supported_floor_but_supported_does_not_force_satisfaction",
    "traceability_no_lookahead": "test_traceability_and_no_lookahead_codes_are_separate_and_ordered",
    "diagnostic_repetition": "test_repeated_validation_codes_keep_group_and_occurrence_order",
    "provenance_timestamp_supersession": "test_supersession_timestamp_and_provenance_rules",
    "purity_and_safety": "test_source_has_no_forbidden_trust_or_execution_dependencies",
}


def _claim(identity: str, claim_class: EvaluationClaimClass, *, stratum: str | None = None) -> EvaluationClaimRecord:
    result_id = f"result-{identity}"
    return EvaluationClaimRecord(
        evaluation_claim_id=identity, claim_class=claim_class, claim_rule_id="claim-rule",
        claim_rule_version="v1", claim_disposition=EvaluationClaimDisposition.CLAIM_SUPPORTED,
        claim_disposition_reason="supported", target_posture="venue_defined_settlement_outcome",
        candidate_method_id="candidate", candidate_method_version="v1",
        baseline_type_when_applicable=None, baseline_method_id_when_applicable=None,
        baseline_method_version_when_applicable=None,
        prediction_representation=ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE,
        metric_or_diagnostic_ids=("metric",), metric_or_diagnostic_versions=("v1",),
        required_evaluation_result_ids=(result_id,), observed_evaluation_result_ids=(result_id,),
        missing_evaluation_result_ids=(), split_id="split", split_version="v1",
        fold_scope="fold", cutoff_scope="cutoff", paired_test_record_set_id="paired",
        aggregation_rule_id="aggregate", weighting_rule_id="weight", stratum_id_when_applicable=stratum,
        uncertainty_policy_id="uncertainty", sample_support_rule_id="support",
        selection_control_policy_id="selection",
        multiple_comparison_policy_id_when_applicable=None,
        evidence_gate_eligibility_posture="eligible_for_later_evidence_gate_decision_only",
        provenance=(f"source-{identity}", result_id), claim_created_at="2025-01-01T00:00:00Z",
    )


def _fixture(*, threshold: bool = False, stratum: bool = False) -> tuple[EvidenceGateDecisionRecord, tuple[EvaluationClaimRecord, ...]]:
    claims = [
        _claim("cross", EvaluationClaimClass.CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES),
        _claim("calibration", EvaluationClaimClass.ENSEMBLE_CALIBRATION_BEHAVIOR),
    ]
    if threshold:
        claims.append(_claim("threshold", EvaluationClaimClass.THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL))
    if stratum:
        claims.append(_claim("stratum", EvaluationClaimClass.STRATUM_SPECIFIC_PREDICTIVE_SKILL, stratum="coastal"))
    context = tuple(claims)
    ids = tuple(claim.evaluation_claim_id for claim in context)
    classes = tuple(claim.claim_class for claim in context)
    conditional = {
        EvidenceGateComponent.THRESHOLD_WEIGHTED_SKILL_WHEN_APPLICABLE: threshold,
        EvidenceGateComponent.STRATUM_SPECIFIC_SKILL_WHEN_APPLICABLE: stratum,
    }
    applicable = tuple(
        component for component in EvidenceGateComponent
        if component not in conditional or conditional[component]
    )
    outcomes = tuple(
        (component, EvidenceGateComponentOutcome.COMPONENT_NOT_APPLICABLE)
        if component in conditional and not conditional[component]
        else (component, EvidenceGateComponentOutcome.COMPONENT_SATISFIED)
        for component in EvidenceGateComponent
    )
    provenance = tuple(
        reference
        for claim in context
        for reference in (claim.evaluation_claim_id, *claim.provenance)
    )
    record = EvidenceGateDecisionRecord(
        evidence_gate_decision_id="decision", evidence_gate_id="gate",
        evidence_gate_version="v1", gate_rule_id="rule", gate_rule_version="v1",
        gate_disposition=EvidenceGateDisposition.STAGE3_GATE_PASSED,
        gate_disposition_reason="complete rule satisfied",
        target_posture="venue_defined_settlement_outcome", candidate_method_id="candidate",
        candidate_method_version="v1",
        prediction_representation=ScoringPredictionRepresentation.FINITE_COMPARABLE_ENSEMBLE,
        required_evaluation_claim_ids=ids, observed_evaluation_claim_ids=ids,
        missing_evaluation_claim_ids=(), required_claim_classes=classes,
        observed_claim_classes=classes, applicable_gate_components=applicable,
        component_outcomes=outcomes, split_id="split", split_version="v1",
        fold_scope="fold", cutoff_scope="cutoff", paired_test_record_set_id="paired",
        aggregation_rule_ids=("aggregate",) * len(context),
        weighting_rule_ids=("weight",) * len(context),
        stratum_scope=tuple(claim.stratum_id_when_applicable for claim in context),
        uncertainty_policy_ids=("uncertainty",) * len(context),
        sample_support_rule_ids=("support",) * len(context),
        selection_control_policy_ids=("selection",) * len(context),
        multiple_comparison_policy_ids=(None,) * len(context),
        no_lookahead_review_posture="predeclared_point_in_time_review_completed",
        result_chain_traceability_posture="complete_immutable_result_chain_required",
        subsequent_approval_request_eligibility_posture="eligible_for_later_separate_readiness_or_approval_request_only",
        provenance=provenance, decision_created_at="2025-01-01T00:00:00Z",
    )
    return record, context


def _mapping(record: EvidenceGateDecisionRecord) -> dict[str, object]:
    return {field.name: getattr(record, field.name) for field in dataclasses.fields(record)}


def _outcomes(record: EvidenceGateDecisionRecord, **changes: EvidenceGateComponentOutcome) -> tuple[tuple[EvidenceGateComponent, EvidenceGateComponentOutcome], ...]:
    return tuple((component, changes.get(component.name, outcome)) for component, outcome in record.component_outcomes)


def test_public_contract_is_literal_and_frozen() -> None:
    import meg.weather.stage3.evidence_gate_decision as module

    assert module.__all__ == PUBLIC
    assert tuple(item.value for item in EvidenceGateComponent) == COMPONENT_VALUES
    assert tuple(item.value for item in EvidenceGateComponentOutcome) == OUTCOME_VALUES
    assert tuple(item.value for item in EvidenceGateDisposition) == DISPOSITION_VALUES
    assert tuple(item.value for item in EvidenceGateValidationSeverity) == ("passed", "blocked")
    assert tuple(item.value for item in EvidenceGateValidationCode) == CODE_VALUES
    assert tuple(field.name for field in dataclasses.fields(EvidenceGateDecisionRecord)) == FIELDS
    assert EvidenceGateDecisionRecord.__dataclass_params__.frozen
    assert EvidenceGateValidationResult.__dataclass_params__.frozen
    assert "__post_init__" not in EvidenceGateDecisionRecord.__dict__
    assert tuple(inspect.signature(evidence_gate_decision_from_mapping).parameters) == ("mapping", "evaluation_claims")
    assert tuple(inspect.signature(validate_evidence_gate_decision).parameters) == ("record", "evaluation_claims")


def test_validation_result_invariant_preserves_repetition() -> None:
    assert EvidenceGateValidationResult(EvidenceGateValidationSeverity.BLOCKED, False).codes == ()
    repeated = (EvidenceGateValidationCode.INVALID_PROVENANCE,) * 2
    result = EvidenceGateValidationResult(EvidenceGateValidationSeverity.PASSED, True, repeated)
    assert (result.severity, result.passed, result.codes) == (EvidenceGateValidationSeverity.BLOCKED, False, repeated)


@pytest.mark.parametrize("root", [None, (), [], "mapping", object()])
def test_unreadable_mapping_has_exact_fail_closed_result(root: object) -> None:
    record, result = evidence_gate_decision_from_mapping(root, ())
    assert record is None
    assert result.codes == (EvidenceGateValidationCode.MISSING_REQUIRED_FIELD,) * 35


class _HostileMapping(Mapping):
    def __init__(self, error: BaseException): self.error = error
    def __len__(self): return 1
    def __iter__(self): raise self.error
    def __getitem__(self, key): raise KeyError(key)
    def items(self): raise self.error


def test_mapping_catches_exception_but_propagates_baseexception() -> None:
    assert evidence_gate_decision_from_mapping(_HostileMapping(RuntimeError("ordinary")), ())[0] is None
    with pytest.raises(KeyboardInterrupt, match="base"):
        evidence_gate_decision_from_mapping(_HostileMapping(KeyboardInterrupt("base")), ())


def test_duplicate_comparison_direction_is_existing_to_incoming() -> None:
    calls: list[str] = []
    class Key:
        def __init__(self, name: str): self.name = name
        def __hash__(self): return id(self)
        def __eq__(self, other): calls.append(self.name); return self.name == "existing"
    class Pairs(Mapping):
        def __len__(self): return 2
        def __iter__(self): return iter(())
        def __getitem__(self, key): raise KeyError(key)
        def items(self): return ((Key("existing"), 1), (Key("incoming"), 2))
    _, result = evidence_gate_decision_from_mapping(Pairs(), ())
    assert calls == ["existing"]
    assert result.codes == (EvidenceGateValidationCode.MISSING_REQUIRED_FIELD,) * 35


def test_equality_baseexception_propagates() -> None:
    class Key:
        def __hash__(self): return id(self)
        def __eq__(self, other): raise SystemExit("equality-base")
    class Pairs(Mapping):
        def __len__(self): return 2
        def __iter__(self): return iter(())
        def __getitem__(self, key): raise KeyError(key)
        def items(self): return ((Key(), 1), (Key(), 2))
    with pytest.raises(SystemExit, match="equality-base"):
        evidence_gate_decision_from_mapping(Pairs(), ())


def test_each_required_key_and_unexpected_key_order() -> None:
    record, context = _fixture()
    values = _mapping(record)
    values.pop("supersedes_decision_id_when_applicable")
    for key in FIELDS[:-1]:
        candidate = dict(values)
        del candidate[key]
        _, result = evidence_gate_decision_from_mapping(candidate, context)
        assert result.codes[0] is EvidenceGateValidationCode.MISSING_REQUIRED_FIELD
    values["zzz"] = 1
    values["aaa"] = 2
    values[3] = 3
    _, result = evidence_gate_decision_from_mapping(values, context)
    assert result.codes[:3] == (EvidenceGateValidationCode.UNEXPECTED_FIELD,) * 3


def test_adapter_exact_adaptation_and_caller_preservation() -> None:
    record, context = _fixture(threshold=True, stratum=True)
    values = _mapping(record)
    values.pop("supersedes_decision_id_when_applicable")
    values["gate_disposition"] = "stage3_gate_passed"
    values["prediction_representation"] = "finite_comparable_ensemble"
    for field in (
        "required_evaluation_claim_ids", "observed_evaluation_claim_ids",
        "missing_evaluation_claim_ids", "required_claim_classes", "observed_claim_classes",
        "applicable_gate_components", "aggregation_rule_ids", "weighting_rule_ids",
        "stratum_scope", "uncertainty_policy_ids", "sample_support_rule_ids",
        "selection_control_policy_ids", "multiple_comparison_policy_ids", "provenance",
    ):
        values[field] = [item.value if hasattr(item, "value") else item for item in values[field]]
    values["component_outcomes"] = [[component.value, outcome.value] for component, outcome in record.component_outcomes]
    before = copy.deepcopy(values)
    adapted, result = evidence_gate_decision_from_mapping(values, list(context))
    assert result.codes == ()
    assert adapted == record
    assert values == before


@pytest.mark.parametrize("threshold,stratum,length", [(False, False, 4), (True, False, 5), (False, True, 5), (True, True, 6)])
def test_all_applicability_combinations_and_always_six_outcomes(threshold: bool, stratum: bool, length: int) -> None:
    record, context = _fixture(threshold=threshold, stratum=stratum)
    assert len(record.applicable_gate_components) == length
    assert len(record.component_outcomes) == 6
    assert validate_evidence_gate_decision(record, context).codes == ()


def test_direct_validation_does_not_adapt_lists() -> None:
    record, context = _fixture()
    malformed = replace(record, required_evaluation_claim_ids=list(record.required_evaluation_claim_ids))
    assert validate_evidence_gate_decision(malformed, context).codes[0] is EvidenceGateValidationCode.INVALID_CLAIM_ID_TUPLE


def test_context_exact_type_order_duplicates_and_unexpected_claims() -> None:
    record, context = _fixture()
    assert validate_evidence_gate_decision(record, list(context)).codes[0] is EvidenceGateValidationCode.INVALID_CLAIM_RECORD_CONTAINER
    reordered = validate_evidence_gate_decision(record, tuple(reversed(context))).codes
    assert reordered[:2] == (EvidenceGateValidationCode.OBSERVED_CLAIM_NOT_FOUND,) * 2
    duplicate = validate_evidence_gate_decision(record, context + (context[0],)).codes
    assert EvidenceGateValidationCode.DUPLICATE_CONTEXT_CLAIM_ID in duplicate
    extra = replace(context[0], evaluation_claim_id="extra")
    unexpected = validate_evidence_gate_decision(record, context + (extra,)).codes
    assert EvidenceGateValidationCode.UNEXPECTED_CONTEXT_CLAIM in unexpected


def test_partition_interleaving_and_repeated_classes_are_valid() -> None:
    record, context = _fixture(threshold=True)
    partial = replace(
        record,
        gate_disposition=EvidenceGateDisposition.STAGE3_GATE_UNAVAILABLE,
        subsequent_approval_request_eligibility_posture="not_eligible_for_implementation_handoff",
        observed_evaluation_claim_ids=(record.required_evaluation_claim_ids[0], record.required_evaluation_claim_ids[2]),
        missing_evaluation_claim_ids=(record.required_evaluation_claim_ids[1],),
        observed_claim_classes=(record.required_claim_classes[0], record.required_claim_classes[2]),
        component_outcomes=_outcomes(
            record,
            REPRESENTATION_APPROPRIATE_CALIBRATION=EvidenceGateComponentOutcome.COMPONENT_UNAVAILABLE,
            OVERALL_STAGE3_EVIDENCE_GATE=EvidenceGateComponentOutcome.COMPONENT_UNAVAILABLE,
        ),
    )
    partial_context = (context[0], context[2])
    codes = validate_evidence_gate_decision(partial, partial_context).codes
    assert EvidenceGateValidationCode.CLAIM_SET_PARTITION_MISMATCH not in codes
    repeated = replace(record, required_claim_classes=(record.required_claim_classes[0],) * len(context))
    assert EvidenceGateValidationCode.INVALID_CLAIM_CLASS_TUPLE not in validate_evidence_gate_decision(repeated, context).codes


@pytest.mark.parametrize(
    "claim_disposition,component_outcome,overall_outcome,gate_disposition",
    [
        (EvaluationClaimDisposition.CLAIM_BLOCKED, EvidenceGateComponentOutcome.COMPONENT_BLOCKED, EvidenceGateComponentOutcome.COMPONENT_BLOCKED, EvidenceGateDisposition.STAGE3_GATE_BLOCKED),
        (EvaluationClaimDisposition.CLAIM_UNAVAILABLE, EvidenceGateComponentOutcome.COMPONENT_UNAVAILABLE, EvidenceGateComponentOutcome.COMPONENT_UNAVAILABLE, EvidenceGateDisposition.STAGE3_GATE_UNAVAILABLE),
        (EvaluationClaimDisposition.CLAIM_INSUFFICIENT, EvidenceGateComponentOutcome.COMPONENT_INSUFFICIENT, EvidenceGateComponentOutcome.COMPONENT_INSUFFICIENT, EvidenceGateDisposition.STAGE3_GATE_INSUFFICIENT),
    ],
)
def test_structural_precedence(
    claim_disposition: EvaluationClaimDisposition,
    component_outcome: EvidenceGateComponentOutcome,
    overall_outcome: EvidenceGateComponentOutcome,
    gate_disposition: EvidenceGateDisposition,
) -> None:
    record, context = _fixture()
    context = (replace(context[0], claim_disposition=claim_disposition), context[1])
    changed = replace(
        record, gate_disposition=gate_disposition,
        subsequent_approval_request_eligibility_posture="not_eligible_for_implementation_handoff",
        component_outcomes=_outcomes(
            record, CROSS_BASELINE_PREDICTIVE_SKILL=component_outcome,
            OVERALL_STAGE3_EVIDENCE_GATE=overall_outcome,
        ),
    )
    assert validate_evidence_gate_decision(changed, context).codes == ()


def test_not_supported_floor_but_supported_does_not_force_satisfaction() -> None:
    record, context = _fixture()
    not_supported = (replace(context[0], claim_disposition=EvaluationClaimDisposition.CLAIM_NOT_SUPPORTED), context[1])
    invalid = validate_evidence_gate_decision(record, not_supported).codes
    assert EvidenceGateValidationCode.COMPONENT_OUTCOME_MISMATCH in invalid
    external_not_satisfied = replace(
        record, gate_disposition=EvidenceGateDisposition.STAGE3_GATE_NOT_PASSED,
        subsequent_approval_request_eligibility_posture="not_eligible_for_implementation_handoff",
        component_outcomes=_outcomes(
            record, CROSS_BASELINE_PREDICTIVE_SKILL=EvidenceGateComponentOutcome.COMPONENT_NOT_SATISFIED,
            OVERALL_STAGE3_EVIDENCE_GATE=EvidenceGateComponentOutcome.COMPONENT_NOT_SATISFIED,
        ),
    )
    assert validate_evidence_gate_decision(external_not_satisfied, context).codes == ()


def test_traceability_and_no_lookahead_codes_are_separate_and_ordered() -> None:
    record, context = _fixture()
    bad_scope_context = (replace(context[0], fold_scope="other"), context[1])
    codes = validate_evidence_gate_decision(record, bad_scope_context).codes
    assert codes.index(EvidenceGateValidationCode.SPLIT_SCOPE_MISMATCH) < codes.index(EvidenceGateValidationCode.NO_LOOKAHEAD_INTEGRITY_MISMATCH)
    bad_provenance = replace(record, provenance=tuple(item for item in record.provenance if item != "result-cross"))
    codes = validate_evidence_gate_decision(bad_provenance, context).codes
    assert EvidenceGateValidationCode.INVALID_FIXED_POSTURE not in codes
    assert EvidenceGateValidationCode.PROVENANCE_TRACEABILITY_MISMATCH in codes
    assert EvidenceGateValidationCode.NO_LOOKAHEAD_INTEGRITY_MISMATCH in codes
    bad_posture = replace(record, result_chain_traceability_posture="wrong")
    codes = validate_evidence_gate_decision(bad_posture, context).codes
    assert EvidenceGateValidationCode.INVALID_FIXED_POSTURE in codes
    assert EvidenceGateValidationCode.PROVENANCE_TRACEABILITY_MISMATCH not in codes


def test_repeated_validation_codes_keep_group_and_occurrence_order() -> None:
    record, context = _fixture()
    malformed = replace(record, provenance=("", "valid", ""), decision_created_at="no-offset")
    assert validate_evidence_gate_decision(malformed, context).codes == (
        EvidenceGateValidationCode.INVALID_TEXT_TUPLE,
        EvidenceGateValidationCode.INVALID_TEXT_TUPLE,
        EvidenceGateValidationCode.INVALID_PROVENANCE,
        EvidenceGateValidationCode.INVALID_PROVENANCE,
        EvidenceGateValidationCode.INVALID_DECISION_CREATED_AT,
    )


def test_supersession_timestamp_and_provenance_rules() -> None:
    record, context = _fixture()
    self_link = replace(record, supersedes_decision_id_when_applicable="decision")
    assert validate_evidence_gate_decision(self_link, context).codes[-1] is EvidenceGateValidationCode.SELF_SUPERSESSION
    absent_link = replace(record, supersedes_decision_id_when_applicable="prior")
    assert validate_evidence_gate_decision(absent_link, context).codes[-1] is EvidenceGateValidationCode.INVALID_SUPERSESSION_LINK
    linked = replace(absent_link, provenance=record.provenance + ("prior",))
    assert validate_evidence_gate_decision(linked, context).codes == ()
    assert EvidenceGateValidationCode.INVALID_DECISION_CREATED_AT in validate_evidence_gate_decision(replace(record, decision_created_at="2025-01-01T00:00:00"), context).codes


def test_source_has_no_forbidden_trust_or_execution_dependencies() -> None:
    source = Path(inspect.getsourcefile(EvidenceGateDecisionRecord)).read_text()
    tree = ast.parse(source)
    imports = {alias.name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) for alias in node.names}
    assert imports & {"EvaluationResultRecord", "validate_evaluation_claim_record"} == set()
    calls = {node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert calls & {"open", "eval", "exec", "compile", "__import__"} == set()
    forbidden = ("requests.", "socket.", "subprocess.", "market" + "_id", "token" + "_outcome_pair")
    assert all(term not in source for term in forbidden)
