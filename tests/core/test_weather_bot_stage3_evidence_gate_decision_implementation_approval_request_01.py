"""Static oracle for the Stage 3 evidence-gate approval request."""
from __future__ import annotations

import ast
import copy
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/prd/WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-IMPLEMENTATION-APPROVAL-REQUEST-01.md"
ALLOWLIST = Path(__file__).with_name("canonical_id_allowlist.py")
EXPECTED = {'title': 'WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-IMPLEMENTATION-APPROVAL-REQUEST-01',
 'canonical_id': 'WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-IMPLEMENTATION-APPROVAL-REQUEST-01',
 'status': 'request_prepared_implementation_not_approved',
 'actual_pr_378_merge_sha': '5bf865218c5187a9ccdb58d3c0c974d08610796d',
 'approved_pr_378_head': '1c4f731dda6d129923c87bb93d540ef4be3fd870',
 'base_sha': '5bf865218c5187a9ccdb58d3c0c974d08610796d',
 'pr_files': ['docs/prd/WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-IMPLEMENTATION-APPROVAL-REQUEST-01.md',
              'tests/core/test_weather_bot_stage3_evidence_gate_decision_implementation_approval_request_01.py',
              'tests/core/canonical_id_allowlist.py'],
 'future_files': ['meg/weather/stage3/evidence_gate_decision.py',
                  'tests/core/test_weather_bot_stage3_evidence_gate_decision.py'],
 'public_symbols': ['EvidenceGateComponent',
                    'EvidenceGateComponentOutcome',
                    'EvidenceGateDisposition',
                    'EvidenceGateValidationSeverity',
                    'EvidenceGateValidationCode',
                    'EvidenceGateDecisionRecord',
                    'EvidenceGateValidationResult',
                    'evidence_gate_decision_from_mapping',
                    'validate_evidence_gate_decision'],
 'permitted_imports': ['ScoringPredictionRepresentation',
                       'EvaluationClaimClass',
                       'EvaluationClaimDisposition',
                       'EvaluationClaimRecord',
                       'EvaluationClaimValidationResult',
                       'validate_evaluation_claim_record'],
 'enums': {'EvidenceGateComponent': [['CROSS_BASELINE_PREDICTIVE_SKILL', 'cross_baseline_predictive_skill'],
                                     ['REPRESENTATION_APPROPRIATE_CALIBRATION',
                                      'representation_appropriate_calibration'],
                                     ['THRESHOLD_WEIGHTED_SKILL_WHEN_APPLICABLE',
                                      'threshold_weighted_skill_when_applicable'],
                                     ['STRATUM_SPECIFIC_SKILL_WHEN_APPLICABLE',
                                      'stratum_specific_skill_when_applicable'],
                                     ['SELECTION_SCOPE_AND_NO_LOOKAHEAD_INTEGRITY',
                                      'selection_scope_and_no_lookahead_integrity'],
                                     ['OVERALL_STAGE3_EVIDENCE_GATE', 'overall_stage3_evidence_gate']],
           'EvidenceGateComponentOutcome': [['COMPONENT_SATISFIED', 'component_satisfied'],
                                            ['COMPONENT_NOT_SATISFIED', 'component_not_satisfied'],
                                            ['COMPONENT_INSUFFICIENT', 'component_insufficient'],
                                            ['COMPONENT_BLOCKED', 'component_blocked'],
                                            ['COMPONENT_UNAVAILABLE', 'component_unavailable'],
                                            ['COMPONENT_NOT_APPLICABLE', 'component_not_applicable']],
           'EvidenceGateDisposition': [['STAGE3_GATE_PASSED', 'stage3_gate_passed'],
                                       ['STAGE3_GATE_NOT_PASSED', 'stage3_gate_not_passed'],
                                       ['STAGE3_GATE_INSUFFICIENT', 'stage3_gate_insufficient'],
                                       ['STAGE3_GATE_BLOCKED', 'stage3_gate_blocked'],
                                       ['STAGE3_GATE_UNAVAILABLE', 'stage3_gate_unavailable']],
           'EvidenceGateValidationSeverity': [['PASSED', 'passed'], ['BLOCKED', 'blocked']],
           'EvidenceGateValidationCode': [['MISSING_REQUIRED_FIELD', 'missing_required_field'],
                                          ['UNEXPECTED_FIELD', 'unexpected_field'],
                                          ['BLANK_REQUIRED_TEXT', 'blank_required_text'],
                                          ['INVALID_GATE_COMPONENT', 'invalid_gate_component'],
                                          ['INVALID_COMPONENT_OUTCOME', 'invalid_component_outcome'],
                                          ['INVALID_GATE_DISPOSITION', 'invalid_gate_disposition'],
                                          ['INVALID_PREDICTION_REPRESENTATION', 'invalid_prediction_representation'],
                                          ['INVALID_CLAIM_CLASS', 'invalid_claim_class'],
                                          ['INVALID_FIXED_POSTURE', 'invalid_fixed_posture'],
                                          ['INVALID_TEXT_TUPLE', 'invalid_text_tuple'],
                                          ['INVALID_CLAIM_ID_TUPLE', 'invalid_claim_id_tuple'],
                                          ['INVALID_CLAIM_CLASS_TUPLE', 'invalid_claim_class_tuple'],
                                          ['INVALID_COMPONENT_TUPLE', 'invalid_component_tuple'],
                                          ['INVALID_COMPONENT_OUTCOME_TUPLE', 'invalid_component_outcome_tuple'],
                                          ['CLAIM_SET_PARTITION_MISMATCH', 'claim_set_partition_mismatch'],
                                          ['CLAIM_CLASS_SEQUENCE_MISMATCH', 'claim_class_sequence_mismatch'],
                                          ['APPLICABILITY_MISMATCH', 'applicability_mismatch'],
                                          ['INVALID_CLAIM_RECORD_CONTAINER', 'invalid_claim_record_container'],
                                          ['INVALID_CLAIM_RECORD', 'invalid_claim_record'],
                                          ['DUPLICATE_CONTEXT_CLAIM_ID', 'duplicate_context_claim_id'],
                                          ['OBSERVED_CLAIM_NOT_FOUND', 'observed_claim_not_found'],
                                          ['UNEXPECTED_CONTEXT_CLAIM', 'unexpected_context_claim'],
                                          ['CLAIM_DISPOSITION_UNUSABLE', 'claim_disposition_unusable'],
                                          ['CLAIM_CLASS_MISMATCH', 'claim_class_mismatch'],
                                          ['CANDIDATE_IDENTITY_MISMATCH', 'candidate_identity_mismatch'],
                                          ['REPRESENTATION_MISMATCH', 'representation_mismatch'],
                                          ['SPLIT_SCOPE_MISMATCH', 'split_scope_mismatch'],
                                          ['PAIRED_RECORD_SET_MISMATCH', 'paired_record_set_mismatch'],
                                          ['AGGREGATION_WEIGHTING_MISMATCH', 'aggregation_weighting_mismatch'],
                                          ['STRATUM_SCOPE_MISMATCH', 'stratum_scope_mismatch'],
                                          ['INHERITED_POLICY_MISMATCH', 'inherited_policy_mismatch'],
                                          ['PROVENANCE_TRACEABILITY_MISMATCH', 'provenance_traceability_mismatch'],
                                          ['CROSS_BASELINE_INCOMPLETE', 'cross_baseline_incomplete'],
                                          ['CALIBRATION_REQUIREMENT_MISMATCH', 'calibration_requirement_mismatch'],
                                          ['THRESHOLD_APPLICABILITY_MISMATCH', 'threshold_applicability_mismatch'],
                                          ['STRATUM_APPLICABILITY_MISMATCH', 'stratum_applicability_mismatch'],
                                          ['NO_LOOKAHEAD_INTEGRITY_MISMATCH', 'no_lookahead_integrity_mismatch'],
                                          ['COMPONENT_OUTCOME_MISMATCH', 'component_outcome_mismatch'],
                                          ['DISPOSITION_PRECEDENCE_MISMATCH', 'disposition_precedence_mismatch'],
                                          ['COMPLETE_RULE_REQUIRED', 'complete_rule_required'],
                                          ['INVALID_PROVENANCE', 'invalid_provenance'],
                                          ['EMPTY_PROVENANCE', 'empty_provenance'],
                                          ['INVALID_DECISION_CREATED_AT', 'invalid_decision_created_at'],
                                          ['SELF_SUPERSESSION', 'self_supersession'],
                                          ['INVALID_SUPERSESSION_LINK', 'invalid_supersession_link']]},
 'record_fields': [['evidence_gate_decision_id', 'str', None],
                   ['evidence_gate_id', 'str', None],
                   ['evidence_gate_version', 'str', None],
                   ['gate_rule_id', 'str', None],
                   ['gate_rule_version', 'str', None],
                   ['gate_disposition', 'EvidenceGateDisposition', None],
                   ['gate_disposition_reason', 'str', None],
                   ['target_posture', 'str', None],
                   ['candidate_method_id', 'str', None],
                   ['candidate_method_version', 'str', None],
                   ['prediction_representation', 'ScoringPredictionRepresentation', None],
                   ['required_evaluation_claim_ids', 'tuple[str, ...]', None],
                   ['observed_evaluation_claim_ids', 'tuple[str, ...]', None],
                   ['missing_evaluation_claim_ids', 'tuple[str, ...]', None],
                   ['required_claim_classes', 'tuple[EvaluationClaimClass, ...]', None],
                   ['observed_claim_classes', 'tuple[EvaluationClaimClass, ...]', None],
                   ['applicable_gate_components', 'tuple[EvidenceGateComponent, ...]', None],
                   ['component_outcomes',
                    'tuple[tuple[EvidenceGateComponent, EvidenceGateComponentOutcome], ...]',
                    None],
                   ['split_id', 'str', None],
                   ['split_version', 'str', None],
                   ['fold_scope', 'str', None],
                   ['cutoff_scope', 'str', None],
                   ['paired_test_record_set_id', 'str', None],
                   ['aggregation_rule_ids', 'tuple[str, ...]', None],
                   ['weighting_rule_ids', 'tuple[str, ...]', None],
                   ['stratum_scope', 'tuple[str | None, ...]', None],
                   ['uncertainty_policy_ids', 'tuple[str, ...]', None],
                   ['sample_support_rule_ids', 'tuple[str, ...]', None],
                   ['selection_control_policy_ids', 'tuple[str, ...]', None],
                   ['multiple_comparison_policy_ids', 'tuple[str | None, ...]', None],
                   ['no_lookahead_review_posture', 'str', None],
                   ['result_chain_traceability_posture', 'str', None],
                   ['subsequent_approval_request_eligibility_posture', 'str', None],
                   ['provenance', 'tuple[str, ...]', None],
                   ['decision_created_at', 'str', None],
                   ['supersedes_decision_id_when_applicable', 'str | None', 'None']],
 'validation_result_fields': [['severity', 'EvidenceGateValidationSeverity', None],
                              ['passed', 'bool', None],
                              ['codes', 'tuple[EvidenceGateValidationCode, ...]', '()']],
 'signatures': {'adapter': 'def evidence_gate_decision_from_mapping(\n'
                           '    mapping: object,\n'
                           '    evaluation_claims: object,\n'
                           ') -> tuple[EvidenceGateDecisionRecord | None, EvidenceGateValidationResult]:',
                'validator': 'def validate_evidence_gate_decision(\n'
                             '    record: EvidenceGateDecisionRecord,\n'
                             '    evaluation_claims: tuple[EvaluationClaimRecord, ...],\n'
                             ') -> EvidenceGateValidationResult:'},
 'required_mapping_keys': ['evidence_gate_decision_id',
                           'evidence_gate_id',
                           'evidence_gate_version',
                           'gate_rule_id',
                           'gate_rule_version',
                           'gate_disposition',
                           'gate_disposition_reason',
                           'target_posture',
                           'candidate_method_id',
                           'candidate_method_version',
                           'prediction_representation',
                           'required_evaluation_claim_ids',
                           'observed_evaluation_claim_ids',
                           'missing_evaluation_claim_ids',
                           'required_claim_classes',
                           'observed_claim_classes',
                           'applicable_gate_components',
                           'component_outcomes',
                           'split_id',
                           'split_version',
                           'fold_scope',
                           'cutoff_scope',
                           'paired_test_record_set_id',
                           'aggregation_rule_ids',
                           'weighting_rule_ids',
                           'stratum_scope',
                           'uncertainty_policy_ids',
                           'sample_support_rule_ids',
                           'selection_control_policy_ids',
                           'multiple_comparison_policy_ids',
                           'no_lookahead_review_posture',
                           'result_chain_traceability_posture',
                           'subsequent_approval_request_eligibility_posture',
                           'provenance',
                           'decision_created_at'],
 'optional_mapping_keys': ['supersedes_decision_id_when_applicable'],
 'list_to_tuple_fields': ['required_evaluation_claim_ids',
                          'observed_evaluation_claim_ids',
                          'missing_evaluation_claim_ids',
                          'required_claim_classes',
                          'observed_claim_classes',
                          'applicable_gate_components',
                          'component_outcomes',
                          'aggregation_rule_ids',
                          'weighting_rule_ids',
                          'stratum_scope',
                          'uncertainty_policy_ids',
                          'sample_support_rule_ids',
                          'selection_control_policy_ids',
                          'multiple_comparison_policy_ids',
                          'provenance'],
 'enum_adaptation': {'gate_disposition': 'EvidenceGateDisposition',
                     'prediction_representation': 'ScoringPredictionRepresentation',
                     'required_claim_classes': 'EvaluationClaimClass elements',
                     'observed_claim_classes': 'EvaluationClaimClass elements',
                     'applicable_gate_components': 'EvidenceGateComponent elements',
                     'component_outcomes': 'two-item actual list/tuple pairs; EvidenceGateComponent then '
                                           'EvidenceGateComponentOutcome'},
 'mapping_failure_contract': ['root must be an instance of Mapping; otherwise return no record and exactly 35 repeated '
                              'missing_required_field codes in required-key order',
                              'create the items iterator and snapshot tuple(mapping.items()) exactly once before '
                              'inspecting items; iterator creation failure or mid-iteration ordinary Exception makes '
                              'the root unreadable',
                              'every snapshotted item must unpack to exactly two values; malformed item shape or '
                              'unpacking ordinary Exception makes the root unreadable',
                              'duplicate detection compares each existing key to the incoming key only, as '
                              'existing_key == incoming_key, in snapshot order; it never performs the reverse '
                              'comparison',
                              'any truthy existing-to-incoming equality is a duplicate; asymmetric equality therefore '
                              'follows that one direction, and any ordinary Exception from equality makes the root '
                              'unreadable',
                              'hash every key after duplicate detection and before dictionary materialization; any '
                              'ordinary Exception from hashing makes the root unreadable',
                              'materialize exactly dict(items) once after successful snapshot, duplicate detection, '
                              'and hashing; any ordinary Exception during materialization, lookup, adaptation, or '
                              'record construction makes the root unreadable',
                              'exact readable keys require type(key) is str; string subclasses and non-string keys '
                              'each emit unexpected_field in snapshot order after exact-string unexpected keys sorted '
                              'lexically',
                              'an unreadable root returns no partial record and exactly one missing_required_field '
                              'occurrence for each of the 35 required keys in field order, with no unexpected or '
                              'semantic codes',
                              'catch ordinary Exception at the frozen mapping operations; never catch BaseException, '
                              'whose subclasses propagate unchanged',
                              'shape and semantic failures for a readable root aggregate in validation-group order; '
                              'repeated codes remain repeated and are never sorted or deduplicated'],
 'built_in_and_nullability': ['all non-enum text requires type(value) is str, nonblank under strip, and is never '
                              'stripped or rewritten',
                              'all direct-record tuple fields require type(value) is tuple; tuple subclasses and '
                              'arbitrary iterables fail',
                              'mapping adaptation converts only type(value) is list for declared tuple fields; nested '
                              'component pairs accept only exact two-item list or tuple',
                              'only supersedes_decision_id_when_applicable is nullable and optional; all other 35 keys '
                              'are required and non-null',
                              'enum adaptation accepts an exact enum member or type(value) is str matching exactly; '
                              'rejects string subclasses, unrelated enums, aliases, names, and case variants',
                              'decision_created_at is exact nonblank ISO-8601 text with T and explicit Z or numeric '
                              'UTC offset; it is never compared with the clock or rewritten',
                              'direct record __post_init__ performs no validation, normalization, adaptation, '
                              'evaluation, or mutation'],
 'claim_context_contract': {'accepted_container': 'direct validator: exact tuple; adapter: exact tuple or actual list '
                                                  'containing only exact EvaluationClaimRecord elements, adapted '
                                                  'without mutation',
                            'element_type': 'type(item) is EvaluationClaimRecord; subclasses and other items are '
                                            'invalid',
                            'invalid_items': 'one invalid_claim_record per offending item in context order; '
                                             'evidence-dependent checks for that item are suppressed',
                            'duplicate_identity': 'duplicate_context_claim_id for each later duplicate occurrence; '
                                                  'duplicate identities are unusable for resolution',
                            'identity_resolution': 'required IDs are ordered unique; observed and missing are ordered '
                                                   'unique, disjoint, and concatenate in required order to required '
                                                   'IDs; observed IDs resolve exactly once',
                            'unexpected_claims': 'context identities outside observed IDs are unexpected and rejected; '
                                                 'no extra context claims are consumed',
                            'order': 'context claim order must equal observed_evaluation_claim_ids; reordered or '
                                     'substituted claims fail closed',
                            'class_compatibility': 'required_claim_classes length equals required_evaluation_claim_ids '
                                                   'and is positionally aligned one-for-one; duplicates are permitted. '
                                                   'observed_claim_classes length equals '
                                                   'observed_evaluation_claim_ids, is positionally aligned '
                                                   'one-for-one, and equals the required-class subsequence at observed '
                                                   'required-ID positions. Each resolved claim class equals its '
                                                   'aligned observed class. No ordered-unique derivation and no '
                                                   'baseline-specific promotion is allowed.',
                            'disposition_compatibility': 'claim_blocked dominates; then claim_unavailable; then '
                                                         'claim_insufficient; claim_supported and claim_not_supported '
                                                         'are evaluable and component rules determine '
                                                         'satisfied/not_satisfied without inventing substantive rules',
                            'candidate_and_representation': 'every usable observed claim exactly matches candidate '
                                                            'method ID/version and ScoringPredictionRepresentation',
                            'scope': 'split_id, split_version, fold_scope to claim fold_scope, cutoff_scope, and '
                                     'paired_test_record_set_id match exactly',
                            'aggregation_weighting': 'claim aggregation_rule_id and weighting_rule_id must occur in '
                                                     'the corresponding ordered decision tuples; no substitution',
                            'stratum': 'claim stratum_id_when_applicable must match the predeclared stratum_scope and '
                                       'conditional applicability; no pooling or omission',
                            'inherited_policies': 'uncertainty_policy_id, sample_support_rule_id, '
                                                  'selection_control_policy_id, and applicable multiple-comparison '
                                                  'policy must occur in the corresponding decision tuples exactly',
                            'provenance_traceability': 'each claim must be individually valid, its ID must be in '
                                                       'provenance or otherwise linked by the explicit result-chain '
                                                       'posture, and no result/evidence is fetched or regenerated',
                            'dependent_suppression': 'missing, invalid, duplicated, or unresolved claims do not '
                                                     'fabricate unrelated class, compatibility, component, or '
                                                     'disposition failures',
                            'policy_alignment': 'aggregation_rule_ids, weighting_rule_ids, stratum_scope, '
                                                'uncertainty_policy_ids, sample_support_rule_ids, '
                                                'selection_control_policy_ids, and multiple_comparison_policy_ids each '
                                                'have exactly the required-claim-ID length and align one-for-one by '
                                                'required claim position. Values preserve the caller-predeclared '
                                                'required set, including repeated values and None only for '
                                                'stratum/multiple-comparison; there is no sorting, deduplication, '
                                                'inference, or observed-only shortening. Each usable observed claim '
                                                'must equal the values at its required-ID position.',
                            'independent_checks': 'after an invalid, duplicate, missing, or unresolved item is '
                                                  'excluded from evidence-dependent comparison, every structural or '
                                                  'compatibility check whose own prerequisites remain usable still '
                                                  'runs in validation-group order'},
 'gate_components': ['cross_baseline_predictive_skill',
                     'representation_appropriate_calibration',
                     'threshold_weighted_skill_when_applicable',
                     'stratum_specific_skill_when_applicable',
                     'selection_scope_and_no_lookahead_integrity',
                     'overall_stage3_evidence_gate'],
 'component_outcomes': ['component_satisfied',
                        'component_not_satisfied',
                        'component_insufficient',
                        'component_blocked',
                        'component_unavailable',
                        'component_not_applicable'],
 'gate_dispositions': ['stage3_gate_passed',
                       'stage3_gate_not_passed',
                       'stage3_gate_insufficient',
                       'stage3_gate_blocked',
                       'stage3_gate_unavailable'],
 'disposition_precedence': ['BLOCKED',
                            'UNAVAILABLE',
                            'INSUFFICIENT',
                            'PASSED_OR_NOT_PASSED_BY_COMPLETE_PREDECLARED_RULE'],
 'component_applicability': {'fixed_before': 'claim-disposition inspection',
                             'mandatory': ['cross_baseline_predictive_skill',
                                           'representation_appropriate_calibration',
                                           'selection_scope_and_no_lookahead_integrity',
                                           'overall_stage3_evidence_gate'],
                             'conditional': ['threshold_weighted_skill_when_applicable',
                                             'stratum_specific_skill_when_applicable'],
                             'rules': ['binary outcome probability requires binary_calibration_behavior',
                                       'full predictive distribution requires distributional_calibration_behavior',
                                       'finite comparable ensemble requires ensemble_calibration_behavior',
                                       'component_not_applicable is valid only for a conditionally predeclared '
                                       'inapplicable component',
                                       'no component may be changed, pooled, waived, or dropped after claim '
                                       'inspection'],
                             'roster': 'applicable_gate_components is exactly all six canonical components in '
                                       'canonical order for every record; the name preserves the planning semantic '
                                       'field, while each conditional component uses component_not_applicable only '
                                       'when predeclared inapplicable',
                             'outcome_alignment': 'component_outcomes has exactly six pairs; pair index and component '
                                                  'identity must match applicable_gate_components; mandatory '
                                                  'components and overall can never be component_not_applicable'},
 'required_claim_set': ['required, observed, and missing IDs are exact built-in-string tuples, ordered, unique, and '
                        'preserve the required partition',
                        'observed plus missing must reproduce required IDs in required order; extra, substituted, or '
                        'reordered IDs fail closed',
                        'passed and not_passed require zero missing IDs and a complete evaluable required set',
                        'claims are never inferred, regenerated, backfilled, replaced, selected, or repaired'],
 'cross_baseline_and_calibration': ['cross-baseline predictive skill requires complete climatology and persistence '
                                    'coverage',
                                    'a baseline-specific claim cannot be promoted into a cross-baseline claim',
                                    'binary outcome probability maps only to binary calibration',
                                    'full predictive distribution maps only to distributional calibration',
                                    'finite comparable ensemble maps only to ensemble calibration',
                                    'market price is not a baseline, settlement truth, calibration truth, or '
                                    'frictionless probability'],
 'predeclaration': ['gate and rule identity/version',
                    'candidate identity/version and representation',
                    'applicable components before claim inspection',
                    'required claim identities and classes; no runtime claim selection',
                    'component rules and complete overall rule',
                    'blocked then unavailable then insufficient precedence',
                    'complete evaluation scope and no-lookahead review',
                    'uncertainty, sample-support, selection-control, and multiple-comparison policies',
                    'missing, unavailable, insufficient, and blocked behavior',
                    'supersession requires new identity and explicit prior link'],
 'component_outcome_rules': ['component_blocked: one or more usable aligned claims are claim_blocked, or the mandatory '
                             'integrity checks identify a contract/no-lookahead block; it dominates every lower '
                             'outcome and cannot be downgraded',
                             'component_unavailable: no block applies and one or more usable aligned claims are '
                             'claim_unavailable; it dominates insufficient/not_satisfied/satisfied',
                             'component_insufficient: no block/unavailable applies and one or more usable aligned '
                             'claims are claim_insufficient; it dominates not_satisfied/satisfied',
                             'component_not_satisfied: the component is applicable and complete/evaluable, no '
                             'higher-precedence outcome applies, and at least one aligned claim is '
                             'claim_not_supported; this is not insufficiency',
                             'component_satisfied: the component is applicable, complete/evaluable, and every aligned '
                             'required claim is claim_supported; empty coverage never satisfies',
                             'component_not_applicable: allowed only for a conditional component predeclared '
                             'inapplicable before claim inspection; mandatory and overall components can never use it',
                             'each of all six canonical components appears exactly once in canonical order; no pair '
                             'can be missing, duplicated, extra, substituted, or reordered after inspection'],
 'disposition_rules': ['any of the first five component outcomes component_blocked -> overall component_blocked and '
                       'stage3_gate_blocked',
                       'otherwise any applicable first-five outcome component_unavailable -> overall '
                       'component_unavailable and stage3_gate_unavailable',
                       'otherwise any applicable first-five outcome component_insufficient -> overall '
                       'component_insufficient and stage3_gate_insufficient',
                       'otherwise any applicable first-five outcome component_not_satisfied -> overall '
                       'component_not_satisfied and stage3_gate_not_passed',
                       'otherwise every mandatory/applicable first-five outcome component_satisfied and every '
                       'inapplicable conditional outcome component_not_applicable -> overall component_satisfied and '
                       'stage3_gate_passed',
                       'stage3_gate_passed and stage3_gate_not_passed require an exact complete evaluable required '
                       'claim set with no missing claims',
                       'gate_disposition_reason is always required exact built-in nonblank text, is preserved '
                       'verbatim, is never generated or semantically parsed, and its presence/type requirement is '
                       'identical for all five dispositions because no textual reason vocabulary was approved'],
 'validation_groups': ['missing_keys',
                       'unexpected_exact_string_keys',
                       'unexpected_remaining_keys',
                       'required_and_nullable_text',
                       'gate_component_enum',
                       'component_outcome_enum',
                       'gate_disposition_enum',
                       'prediction_representation_enum',
                       'claim_class_enum',
                       'fixed_postures',
                       'text_tuple_structure',
                       'claim_identity_tuple_structure',
                       'claim_class_tuple_structure',
                       'component_tuple_structure',
                       'component_outcome_tuple_structure',
                       'claim_set_partition',
                       'claim_class_sequence',
                       'component_applicability',
                       'claim_context_container',
                       'individual_claim_validity',
                       'context_identity_uniqueness',
                       'observed_claim_resolution',
                       'unexpected_context_claims',
                       'claim_disposition_compatibility',
                       'claim_class_compatibility',
                       'candidate_identity_compatibility',
                       'representation_compatibility',
                       'split_fold_cutoff_compatibility',
                       'paired_record_set_compatibility',
                       'aggregation_weighting_compatibility',
                       'stratum_compatibility',
                       'inherited_policy_compatibility',
                       'provenance_result_chain_traceability',
                       'cross_baseline_completeness',
                       'calibration_requirement',
                       'threshold_applicability',
                       'stratum_applicability',
                       'no_lookahead_integrity',
                       'component_outcome_consistency',
                       'disposition_precedence',
                       'complete_rule_requirement',
                       'provenance',
                       'decision_created_timestamp',
                       'self_supersession',
                       'supersession_link'],
 'validation_occurrence': 'one code at each diagnosable occurrence in validation-group order; repeated codes remain '
                          'repeated; dependent groups run only with usable prerequisites; empty codes force '
                          'passed/true and nonempty codes force blocked/false',
 'fixed_assignments': {'target_posture': 'venue_defined_settlement_outcome',
                       'no_lookahead_review_posture': 'predeclared_point_in_time_review_completed',
                       'result_chain_traceability_posture': 'complete_immutable_result_chain_required',
                       'passed_eligibility': 'eligible_for_later_separate_readiness_or_approval_request_only',
                       'nonpassed_eligibility': 'not_eligible_for_implementation_handoff',
                       'canonical_routing_fields': ['condition_id', 'token_id', 'outcome'],
                       'non_routing_field': 'market&#95;id',
                       'derived_identifier': 'token_outcome_pair'},
 'immutability': ['both record types are frozen dataclasses; accepted tuple contents are immutable',
                  'provenance is nonempty exact tuple of exact nonblank built-in strings; order and duplicates are '
                  'preserved',
                  'correction requires a new decision ID, immutable record, explicit supersession link, and retained '
                  'prior provenance',
                  'self-supersession, blank/wrong-type supersession, and a supersession ID absent from provenance fail '
                  'closed; no overwrite or silent mutation; the pure boundary does not look up prior decisions'],
 'decision_options': ['approve_later_evidence_gate_decision_implementation_ticket',
                      'request_approval_request_revision',
                      'hold',
                      'block'],
 'successor_ticket': 'WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-IMPLEMENTATION-01',
 'non_goals': ['evidence-gate implementation',
               'evidence-gate decision creation',
               'execution over real evidence',
               'evidence-gate passage',
               'score/diagnostic/comparison calculation',
               'claim generation or substantive claim-rule evaluation',
               'probability generation',
               'split execution',
               'baseline execution',
               'model training/calibration',
               'source fetching',
               'provider connectors',
               'persistence or serialization',
               'database tables/migrations',
               'reports/exports',
               'backtesting/simulation',
               'market-price comparison execution',
               'economic-edge/executability findings',
               'paper trading',
               'trading',
               'order placement',
               'production runtime',
               'orchestration',
               'autonomy'],
 'approval_separation': 'stage3_gate_passed DOES NOT approve implementation; it means only that the exact predeclared '
                        'Stage 3 evidence-gate rule was satisfied for the exact recorded candidate and scope; only a '
                        'later separate readiness/approval sequence may proceed',
 'quantitative_policy': 'no numeric alpha, confidence level, correction threshold, effect threshold, sample minimum, '
                        'bin count, probability tolerance, weighting constant, resampling length, or economic-edge '
                        'threshold is introduced',
 'ambiguity_resolutions': ['the planning field prediction_representation uses the implemented '
                           'ScoringPredictionRepresentation type and its exact values, not a new alias',
                           'fold_scope maps exactly to EvaluationClaimRecord.fold_scope and cutoff_scope maps exactly '
                           'to EvaluationClaimRecord.cutoff_scope',
                           'plural decision policy fields are ordered tuples containing each compatible singular '
                           'EvaluationClaimRecord policy identity',
                           'required_claim_classes and observed_claim_classes use EvaluationClaimClass directly',
                           'component_outcomes is an ordered tuple of exact component/outcome pairs aligned one-to-one '
                           'with applicable_gate_components',
                           'required claim IDs are explicitly predeclared; deterministic selection-rule execution is '
                           'outside this minimal boundary',
                           'no semantic conflict requires modification of an existing upstream file',
                           'required and observed claim-class tuples are positional, permit repeated classes, and are '
                           'not ordered-unique derivations',
                           'plural policy and stratum tuples align positionally to required claim IDs, preserve '
                           'repeats and permitted None values, and are never sorted or deduplicated',
                           'all six components are always recorded in canonical order; conditional inapplicability is '
                           'expressed by the aligned component_not_applicable outcome',
                           'gate identifiers remain opaque metadata and the only executable semantics are the frozen '
                           'claim-disposition/component/disposition mappings; no general rule engine is approved',
                           'supersession validation is syntactic, self-link, and provenance-link-only because the '
                           'minimal API has no prior-decision context or registry'],
 'field_semantics': {'evidence_gate_decision_id': {'position': 1,
                                                   'annotation': 'str',
                                                   'mapping_key': 'required',
                                                   'nullable': False,
                                                   'mapping_adaptation': 'none',
                                                   'direct_record_requirement': 'exact declared annotation; no '
                                                                                'adaptation or normalization',
                                                   'validation_dependency': 'exact built-in nonblank text; fixed-value '
                                                                            'check where assigned; timestamp grammar '
                                                                            'additionally for decision_created_at',
                                                   'nullable_elements': False},
                     'evidence_gate_id': {'position': 2,
                                          'annotation': 'str',
                                          'mapping_key': 'required',
                                          'nullable': False,
                                          'mapping_adaptation': 'none',
                                          'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                       'normalization',
                                          'validation_dependency': 'exact built-in nonblank text; fixed-value check '
                                                                   'where assigned; timestamp grammar additionally for '
                                                                   'decision_created_at',
                                          'nullable_elements': False},
                     'evidence_gate_version': {'position': 3,
                                               'annotation': 'str',
                                               'mapping_key': 'required',
                                               'nullable': False,
                                               'mapping_adaptation': 'none',
                                               'direct_record_requirement': 'exact declared annotation; no adaptation '
                                                                            'or normalization',
                                               'validation_dependency': 'exact built-in nonblank text; fixed-value '
                                                                        'check where assigned; timestamp grammar '
                                                                        'additionally for decision_created_at',
                                               'nullable_elements': False},
                     'gate_rule_id': {'position': 4,
                                      'annotation': 'str',
                                      'mapping_key': 'required',
                                      'nullable': False,
                                      'mapping_adaptation': 'none',
                                      'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                   'normalization',
                                      'validation_dependency': 'exact built-in nonblank text; fixed-value check where '
                                                               'assigned; timestamp grammar additionally for '
                                                               'decision_created_at',
                                      'nullable_elements': False},
                     'gate_rule_version': {'position': 5,
                                           'annotation': 'str',
                                           'mapping_key': 'required',
                                           'nullable': False,
                                           'mapping_adaptation': 'none',
                                           'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                        'normalization',
                                           'validation_dependency': 'exact built-in nonblank text; fixed-value check '
                                                                    'where assigned; timestamp grammar additionally '
                                                                    'for decision_created_at',
                                           'nullable_elements': False},
                     'gate_disposition': {'position': 6,
                                          'annotation': 'EvidenceGateDisposition',
                                          'mapping_key': 'required',
                                          'nullable': False,
                                          'mapping_adaptation': 'exact string to exact enum member',
                                          'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                       'normalization',
                                          'validation_dependency': 'exact EvidenceGateDisposition and exact '
                                                                   'precedence/final-component consistency',
                                          'nullable_elements': False},
                     'gate_disposition_reason': {'position': 7,
                                                 'annotation': 'str',
                                                 'mapping_key': 'required',
                                                 'nullable': False,
                                                 'mapping_adaptation': 'none',
                                                 'direct_record_requirement': 'exact declared annotation; no '
                                                                              'adaptation or normalization',
                                                 'validation_dependency': 'exact built-in nonblank text; fixed-value '
                                                                          'check where assigned; timestamp grammar '
                                                                          'additionally for decision_created_at',
                                                 'nullable_elements': False},
                     'target_posture': {'position': 8,
                                        'annotation': 'str',
                                        'mapping_key': 'required',
                                        'nullable': False,
                                        'mapping_adaptation': 'none',
                                        'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                     'normalization',
                                        'validation_dependency': 'exact built-in nonblank text; fixed-value check '
                                                                 'where assigned; timestamp grammar additionally for '
                                                                 'decision_created_at',
                                        'nullable_elements': False},
                     'candidate_method_id': {'position': 9,
                                             'annotation': 'str',
                                             'mapping_key': 'required',
                                             'nullable': False,
                                             'mapping_adaptation': 'none',
                                             'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                          'normalization',
                                             'validation_dependency': 'exact built-in nonblank text; fixed-value check '
                                                                      'where assigned; timestamp grammar additionally '
                                                                      'for decision_created_at',
                                             'nullable_elements': False},
                     'candidate_method_version': {'position': 10,
                                                  'annotation': 'str',
                                                  'mapping_key': 'required',
                                                  'nullable': False,
                                                  'mapping_adaptation': 'none',
                                                  'direct_record_requirement': 'exact declared annotation; no '
                                                                               'adaptation or normalization',
                                                  'validation_dependency': 'exact built-in nonblank text; fixed-value '
                                                                           'check where assigned; timestamp grammar '
                                                                           'additionally for decision_created_at',
                                                  'nullable_elements': False},
                     'prediction_representation': {'position': 11,
                                                   'annotation': 'ScoringPredictionRepresentation',
                                                   'mapping_key': 'required',
                                                   'nullable': False,
                                                   'mapping_adaptation': 'exact string to exact enum member',
                                                   'direct_record_requirement': 'exact declared annotation; no '
                                                                                'adaptation or normalization',
                                                   'validation_dependency': 'exact ScoringPredictionRepresentation and '
                                                                            'representation-selected calibration '
                                                                            'compatibility',
                                                   'nullable_elements': False},
                     'required_evaluation_claim_ids': {'position': 12,
                                                       'annotation': 'tuple[str, ...]',
                                                       'mapping_key': 'required',
                                                       'nullable': False,
                                                       'mapping_adaptation': 'exact list to tuple',
                                                       'direct_record_requirement': 'exact declared annotation; no '
                                                                                    'adaptation or normalization',
                                                       'validation_dependency': 'exact tuple of ordered unique exact '
                                                                                'built-in nonblank strings; claim '
                                                                                'partition and resolution '
                                                                                'prerequisites',
                                                       'nullable_elements': False},
                     'observed_evaluation_claim_ids': {'position': 13,
                                                       'annotation': 'tuple[str, ...]',
                                                       'mapping_key': 'required',
                                                       'nullable': False,
                                                       'mapping_adaptation': 'exact list to tuple',
                                                       'direct_record_requirement': 'exact declared annotation; no '
                                                                                    'adaptation or normalization',
                                                       'validation_dependency': 'exact tuple of ordered unique exact '
                                                                                'built-in nonblank strings; claim '
                                                                                'partition and resolution '
                                                                                'prerequisites',
                                                       'nullable_elements': False},
                     'missing_evaluation_claim_ids': {'position': 14,
                                                      'annotation': 'tuple[str, ...]',
                                                      'mapping_key': 'required',
                                                      'nullable': False,
                                                      'mapping_adaptation': 'exact list to tuple',
                                                      'direct_record_requirement': 'exact declared annotation; no '
                                                                                   'adaptation or normalization',
                                                      'validation_dependency': 'exact tuple of ordered unique exact '
                                                                               'built-in nonblank strings; claim '
                                                                               'partition and resolution prerequisites',
                                                      'nullable_elements': False},
                     'required_claim_classes': {'position': 15,
                                                'annotation': 'tuple[EvaluationClaimClass, ...]',
                                                'mapping_key': 'required',
                                                'nullable': False,
                                                'mapping_adaptation': 'exact list to tuple',
                                                'direct_record_requirement': 'exact declared annotation; no adaptation '
                                                                             'or normalization',
                                                'validation_dependency': 'exact tuple of exact EvaluationClaimClass '
                                                                         'members; positionally aligned to its '
                                                                         'corresponding claim-ID tuple; duplicates '
                                                                         'permitted',
                                                'nullable_elements': False},
                     'observed_claim_classes': {'position': 16,
                                                'annotation': 'tuple[EvaluationClaimClass, ...]',
                                                'mapping_key': 'required',
                                                'nullable': False,
                                                'mapping_adaptation': 'exact list to tuple',
                                                'direct_record_requirement': 'exact declared annotation; no adaptation '
                                                                             'or normalization',
                                                'validation_dependency': 'exact tuple of exact EvaluationClaimClass '
                                                                         'members; positionally aligned to its '
                                                                         'corresponding claim-ID tuple; duplicates '
                                                                         'permitted',
                                                'nullable_elements': False},
                     'applicable_gate_components': {'position': 17,
                                                    'annotation': 'tuple[EvidenceGateComponent, ...]',
                                                    'mapping_key': 'required',
                                                    'nullable': False,
                                                    'mapping_adaptation': 'exact list to tuple',
                                                    'direct_record_requirement': 'exact declared annotation; no '
                                                                                 'adaptation or normalization',
                                                    'validation_dependency': 'exact six-component canonical roster in '
                                                                             'canonical order; conditional '
                                                                             'inapplicability is recorded only by its '
                                                                             'paired outcome',
                                                    'nullable_elements': False},
                     'component_outcomes': {'position': 18,
                                            'annotation': 'tuple[tuple[EvidenceGateComponent, '
                                                          'EvidenceGateComponentOutcome], ...]',
                                            'mapping_key': 'required',
                                            'nullable': False,
                                            'mapping_adaptation': 'exact list to tuple',
                                            'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                         'normalization',
                                            'validation_dependency': 'exact six canonical component/outcome pairs in '
                                                                     'canonical order; one pair per roster component; '
                                                                     'no missing, duplicate, extra, or reordered pair',
                                            'nullable_elements': False},
                     'split_id': {'position': 19,
                                  'annotation': 'str',
                                  'mapping_key': 'required',
                                  'nullable': False,
                                  'mapping_adaptation': 'none',
                                  'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                               'normalization',
                                  'validation_dependency': 'exact built-in nonblank text; fixed-value check where '
                                                           'assigned; timestamp grammar additionally for '
                                                           'decision_created_at',
                                  'nullable_elements': False},
                     'split_version': {'position': 20,
                                       'annotation': 'str',
                                       'mapping_key': 'required',
                                       'nullable': False,
                                       'mapping_adaptation': 'none',
                                       'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                    'normalization',
                                       'validation_dependency': 'exact built-in nonblank text; fixed-value check where '
                                                                'assigned; timestamp grammar additionally for '
                                                                'decision_created_at',
                                       'nullable_elements': False},
                     'fold_scope': {'position': 21,
                                    'annotation': 'str',
                                    'mapping_key': 'required',
                                    'nullable': False,
                                    'mapping_adaptation': 'none',
                                    'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                 'normalization',
                                    'validation_dependency': 'exact built-in nonblank text; fixed-value check where '
                                                             'assigned; timestamp grammar additionally for '
                                                             'decision_created_at',
                                    'nullable_elements': False},
                     'cutoff_scope': {'position': 22,
                                      'annotation': 'str',
                                      'mapping_key': 'required',
                                      'nullable': False,
                                      'mapping_adaptation': 'none',
                                      'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                   'normalization',
                                      'validation_dependency': 'exact built-in nonblank text; fixed-value check where '
                                                               'assigned; timestamp grammar additionally for '
                                                               'decision_created_at',
                                      'nullable_elements': False},
                     'paired_test_record_set_id': {'position': 23,
                                                   'annotation': 'str',
                                                   'mapping_key': 'required',
                                                   'nullable': False,
                                                   'mapping_adaptation': 'none',
                                                   'direct_record_requirement': 'exact declared annotation; no '
                                                                                'adaptation or normalization',
                                                   'validation_dependency': 'exact built-in nonblank text; fixed-value '
                                                                            'check where assigned; timestamp grammar '
                                                                            'additionally for decision_created_at',
                                                   'nullable_elements': False},
                     'aggregation_rule_ids': {'position': 24,
                                              'annotation': 'tuple[str, ...]',
                                              'mapping_key': 'required',
                                              'nullable': False,
                                              'mapping_adaptation': 'exact list to tuple',
                                              'direct_record_requirement': 'exact declared annotation; no adaptation '
                                                                           'or normalization',
                                              'validation_dependency': 'exact tuple positionally aligned to '
                                                                       'required_evaluation_claim_ids; values copied '
                                                                       'caller-side from each predeclared required '
                                                                       'claim identity; no sorting, deduplication, '
                                                                       'inference, or observed-only shortening',
                                              'nullable_elements': False},
                     'weighting_rule_ids': {'position': 25,
                                            'annotation': 'tuple[str, ...]',
                                            'mapping_key': 'required',
                                            'nullable': False,
                                            'mapping_adaptation': 'exact list to tuple',
                                            'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                         'normalization',
                                            'validation_dependency': 'exact tuple positionally aligned to '
                                                                     'required_evaluation_claim_ids; values copied '
                                                                     'caller-side from each predeclared required claim '
                                                                     'identity; no sorting, deduplication, inference, '
                                                                     'or observed-only shortening',
                                            'nullable_elements': False},
                     'stratum_scope': {'position': 26,
                                       'annotation': 'tuple[str | None, ...]',
                                       'mapping_key': 'required',
                                       'nullable': False,
                                       'mapping_adaptation': 'exact list to tuple',
                                       'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                    'normalization',
                                       'validation_dependency': 'exact tuple positionally aligned to '
                                                                'required_evaluation_claim_ids; values copied '
                                                                'caller-side from each predeclared required claim '
                                                                'identity; no sorting, deduplication, inference, or '
                                                                'observed-only shortening',
                                       'nullable_elements': True},
                     'uncertainty_policy_ids': {'position': 27,
                                                'annotation': 'tuple[str, ...]',
                                                'mapping_key': 'required',
                                                'nullable': False,
                                                'mapping_adaptation': 'exact list to tuple',
                                                'direct_record_requirement': 'exact declared annotation; no adaptation '
                                                                             'or normalization',
                                                'validation_dependency': 'exact tuple positionally aligned to '
                                                                         'required_evaluation_claim_ids; values copied '
                                                                         'caller-side from each predeclared required '
                                                                         'claim identity; no sorting, deduplication, '
                                                                         'inference, or observed-only shortening',
                                                'nullable_elements': False},
                     'sample_support_rule_ids': {'position': 28,
                                                 'annotation': 'tuple[str, ...]',
                                                 'mapping_key': 'required',
                                                 'nullable': False,
                                                 'mapping_adaptation': 'exact list to tuple',
                                                 'direct_record_requirement': 'exact declared annotation; no '
                                                                              'adaptation or normalization',
                                                 'validation_dependency': 'exact tuple positionally aligned to '
                                                                          'required_evaluation_claim_ids; values '
                                                                          'copied caller-side from each predeclared '
                                                                          'required claim identity; no sorting, '
                                                                          'deduplication, inference, or observed-only '
                                                                          'shortening',
                                                 'nullable_elements': False},
                     'selection_control_policy_ids': {'position': 29,
                                                      'annotation': 'tuple[str, ...]',
                                                      'mapping_key': 'required',
                                                      'nullable': False,
                                                      'mapping_adaptation': 'exact list to tuple',
                                                      'direct_record_requirement': 'exact declared annotation; no '
                                                                                   'adaptation or normalization',
                                                      'validation_dependency': 'exact tuple positionally aligned to '
                                                                               'required_evaluation_claim_ids; values '
                                                                               'copied caller-side from each '
                                                                               'predeclared required claim identity; '
                                                                               'no sorting, deduplication, inference, '
                                                                               'or observed-only shortening',
                                                      'nullable_elements': False},
                     'multiple_comparison_policy_ids': {'position': 30,
                                                        'annotation': 'tuple[str | None, ...]',
                                                        'mapping_key': 'required',
                                                        'nullable': False,
                                                        'mapping_adaptation': 'exact list to tuple',
                                                        'direct_record_requirement': 'exact declared annotation; no '
                                                                                     'adaptation or normalization',
                                                        'validation_dependency': 'exact tuple positionally aligned to '
                                                                                 'required_evaluation_claim_ids; '
                                                                                 'values copied caller-side from each '
                                                                                 'predeclared required claim identity; '
                                                                                 'no sorting, deduplication, '
                                                                                 'inference, or observed-only '
                                                                                 'shortening',
                                                        'nullable_elements': True},
                     'no_lookahead_review_posture': {'position': 31,
                                                     'annotation': 'str',
                                                     'mapping_key': 'required',
                                                     'nullable': False,
                                                     'mapping_adaptation': 'none',
                                                     'direct_record_requirement': 'exact declared annotation; no '
                                                                                  'adaptation or normalization',
                                                     'validation_dependency': 'exact built-in nonblank text; '
                                                                              'fixed-value check where assigned; '
                                                                              'timestamp grammar additionally for '
                                                                              'decision_created_at',
                                                     'nullable_elements': False},
                     'result_chain_traceability_posture': {'position': 32,
                                                           'annotation': 'str',
                                                           'mapping_key': 'required',
                                                           'nullable': False,
                                                           'mapping_adaptation': 'none',
                                                           'direct_record_requirement': 'exact declared annotation; no '
                                                                                        'adaptation or normalization',
                                                           'validation_dependency': 'exact built-in nonblank text; '
                                                                                    'fixed-value check where assigned; '
                                                                                    'timestamp grammar additionally '
                                                                                    'for decision_created_at',
                                                           'nullable_elements': False},
                     'subsequent_approval_request_eligibility_posture': {'position': 33,
                                                                         'annotation': 'str',
                                                                         'mapping_key': 'required',
                                                                         'nullable': False,
                                                                         'mapping_adaptation': 'none',
                                                                         'direct_record_requirement': 'exact declared '
                                                                                                      'annotation; no '
                                                                                                      'adaptation or '
                                                                                                      'normalization',
                                                                         'validation_dependency': 'exact built-in '
                                                                                                  'nonblank text; '
                                                                                                  'fixed-value check '
                                                                                                  'where assigned; '
                                                                                                  'timestamp grammar '
                                                                                                  'additionally for '
                                                                                                  'decision_created_at',
                                                                         'nullable_elements': False},
                     'provenance': {'position': 34,
                                    'annotation': 'tuple[str, ...]',
                                    'mapping_key': 'required',
                                    'nullable': False,
                                    'mapping_adaptation': 'exact list to tuple',
                                    'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                 'normalization',
                                    'validation_dependency': 'exact nonempty tuple of exact built-in nonblank strings; '
                                                             'order and duplicates preserved; result-chain linkage '
                                                             'checked',
                                    'nullable_elements': False},
                     'decision_created_at': {'position': 35,
                                             'annotation': 'str',
                                             'mapping_key': 'required',
                                             'nullable': False,
                                             'mapping_adaptation': 'none',
                                             'direct_record_requirement': 'exact declared annotation; no adaptation or '
                                                                          'normalization',
                                             'validation_dependency': 'exact built-in nonblank text; fixed-value check '
                                                                      'where assigned; timestamp grammar additionally '
                                                                      'for decision_created_at',
                                             'nullable_elements': False},
                     'supersedes_decision_id_when_applicable': {'position': 36,
                                                                'annotation': 'str | None',
                                                                'mapping_key': 'optional',
                                                                'nullable': True,
                                                                'mapping_adaptation': 'none',
                                                                'direct_record_requirement': 'exact declared '
                                                                                             'annotation; no '
                                                                                             'adaptation or '
                                                                                             'normalization',
                                                                'validation_dependency': 'None or exact built-in '
                                                                                         'nonblank string; omitted '
                                                                                         'adapts to None; self-link '
                                                                                         'fails; when present it must '
                                                                                         'occur in provenance as the '
                                                                                         'explicit prior-record link; '
                                                                                         'no prior-decision lookup or '
                                                                                         'registry',
                                                                'nullable_elements': False}},
 'gate_rule_execution_boundary': {'gate_rule_identity': 'evidence_gate_id/version and gate_rule_id/version are opaque '
                                                        'exact nonblank caller-supplied identifiers used only for '
                                                        'provenance and equality; they are not looked up, selected, '
                                                        'parsed, or executed',
                                  'validator_may': 'validate record/claim structure and compatibility; translate '
                                                   'caller-supplied claim dispositions into component outcomes by the '
                                                   'fixed rules below; validate the supplied six component outcomes, '
                                                   'overall outcome, final disposition, reason presence, and '
                                                   'eligibility posture against those fixed rules',
                                  'validator_must_not': 'implement a DSL, registry, expression evaluator, callback, '
                                                        'dynamic execution, threshold, configurable pass logic, '
                                                        'arbitrary rule engine, scoring, diagnostic calculation, claim '
                                                        'generation, or substantive evidence interpretation',
                                  'fixed_claim_to_component_rule': 'for each non-integrity evidence component, after '
                                                                   'complete compatible required claim coverage: any '
                                                                   'claim_blocked -> component_blocked; else any '
                                                                   'claim_unavailable -> component_unavailable; else '
                                                                   'any claim_insufficient -> component_insufficient; '
                                                                   'else any claim_not_supported -> '
                                                                   'component_not_satisfied; else all required claims '
                                                                   'claim_supported -> component_satisfied. Empty '
                                                                   'applicable claim coverage is incomplete, never '
                                                                   'satisfied.',
                                  'integrity_rule': 'selection_scope_and_no_lookahead_integrity is component_satisfied '
                                                    'only when all fixed postures, scope/policy alignments, '
                                                    'traceability, predeclaration, and no-lookahead validations pass; '
                                                    'any structural/policy/no-lookahead violation makes validation '
                                                    'fail and requires caller-supplied component_blocked, never a '
                                                    'repaired outcome',
                                  'overall_rule': 'derive the expected final disposition from the first five component '
                                                  'outcomes only: blocked, then unavailable, then insufficient; '
                                                  'otherwise any component_not_satisfied yields not_passed; otherwise '
                                                  'all applicable outcomes satisfied and valid conditional outcomes '
                                                  'not_applicable yields passed. The supplied overall component '
                                                  'outcome must respectively be blocked, unavailable, insufficient, '
                                                  'not_satisfied, or satisfied and the supplied gate disposition must '
                                                  'match.',
                                  'no_calculation_on_invalid_prerequisite': 'when prerequisites are unusable, do not '
                                                                            'fabricate an expected evidence outcome; '
                                                                            'emit only prerequisite diagnostics plus '
                                                                            'independently diagnosable structural '
                                                                            'errors'},
 'validation_code_semantics': [{'code': 'missing_required_field',
                                'group': 'missing_keys',
                                'condition_and_occurrence': 'once per absent required exact-string key, in '
                                                            'required-key order; unreadable root returns exactly all '
                                                            '35 occurrences and suppresses every other code',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'unexpected_field',
                                'group': 'unexpected_exact_string_keys',
                                'condition_and_occurrence': 'once per unexpected exact-string key in lexical order, '
                                                            'then once per string-subclass/non-string key in snapshot '
                                                            'order, only for readable root',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'blank_required_text',
                                'group': 'unexpected_remaining_keys',
                                'condition_and_occurrence': 'once per present required or non-None nullable text field '
                                                            'that is not exact built-in nonblank text, in record-field '
                                                            'order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_gate_component',
                                'group': 'required_and_nullable_text',
                                'condition_and_occurrence': 'once per non-exact EvidenceGateComponent element after a '
                                                            'usable outer component tuple/pair structure',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_component_outcome',
                                'group': 'gate_component_enum',
                                'condition_and_occurrence': 'once per non-exact EvidenceGateComponentOutcome element '
                                                            'after a usable pair structure',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_gate_disposition',
                                'group': 'component_outcome_enum',
                                'condition_and_occurrence': 'once when present disposition is not exact '
                                                            'EvidenceGateDisposition',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_prediction_representation',
                                'group': 'gate_disposition_enum',
                                'condition_and_occurrence': 'once when present representation is not exact '
                                                            'ScoringPredictionRepresentation',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_claim_class',
                                'group': 'prediction_representation_enum',
                                'condition_and_occurrence': 'once per non-exact EvaluationClaimClass element, required '
                                                            'classes then observed classes in tuple order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_fixed_posture',
                                'group': 'claim_class_enum',
                                'condition_and_occurrence': 'once per valid-text fixed posture whose value differs '
                                                            'from its frozen assignment, in field order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_text_tuple',
                                'group': 'fixed_postures',
                                'condition_and_occurrence': 'once per malformed policy/stratum/provenance tuple entry '
                                                            'or outer tuple, in record-field then entry order; '
                                                            'specialized identity tuples use their specialized codes',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_claim_id_tuple',
                                'group': 'text_tuple_structure',
                                'condition_and_occurrence': 'once for each malformed required/observed/missing '
                                                            'claim-ID tuple; duplicates within a tuple make that tuple '
                                                            'malformed',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_claim_class_tuple',
                                'group': 'claim_identity_tuple_structure',
                                'condition_and_occurrence': 'once for each malformed required/observed class outer '
                                                            'tuple; element enum errors additionally occur per invalid '
                                                            'element',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_component_tuple',
                                'group': 'claim_class_tuple_structure',
                                'condition_and_occurrence': 'once when applicable_gate_components is not an exact '
                                                            'tuple or not the exact six-component canonical roster',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_component_outcome_tuple',
                                'group': 'component_tuple_structure',
                                'condition_and_occurrence': 'once when component_outcomes is not an exact tuple of six '
                                                            'exact two-item tuple pairs in canonical component '
                                                            'alignment',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'claim_set_partition_mismatch',
                                'group': 'component_outcome_tuple_structure',
                                'condition_and_occurrence': 'once when usable unique ID tuples do not make observed '
                                                            'and missing disjoint subsequences whose merge in required '
                                                            'order is exactly required IDs',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'claim_class_sequence_mismatch',
                                'group': 'claim_set_partition',
                                'condition_and_occurrence': 'once for required class/ID length mismatch and once for '
                                                            'observed class/ID length or required-subsequence '
                                                            'mismatch, in that order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'applicability_mismatch',
                                'group': 'claim_class_sequence',
                                'condition_and_occurrence': 'once per component roster/outcome applicability violation '
                                                            'in canonical component order, including not_applicable on '
                                                            'mandatory/overall or non-not_applicable on '
                                                            'predeclared-inapplicable conditional',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_claim_record_container',
                                'group': 'component_applicability',
                                'condition_and_occurrence': 'once when direct context type is not exact tuple, or '
                                                            'adapter context is neither exact tuple nor an exact list '
                                                            'wholly eligible for adaptation',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_claim_record',
                                'group': 'claim_context_container',
                                'condition_and_occurrence': 'once per context item whose type is not exactly '
                                                            'EvaluationClaimRecord or whose direct upstream validation '
                                                            'has nonempty codes, in context order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'duplicate_context_claim_id',
                                'group': 'individual_claim_validity',
                                'condition_and_occurrence': 'once for each later exact-type individually-valid context '
                                                            'record repeating an earlier usable claim ID, in context '
                                                            'order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'observed_claim_not_found',
                                'group': 'context_identity_uniqueness',
                                'condition_and_occurrence': 'once per observed ID that does not resolve to exactly one '
                                                            'usable context claim, in observed-ID order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'unexpected_context_claim',
                                'group': 'observed_claim_resolution',
                                'condition_and_occurrence': 'once per usable unique context claim ID absent from '
                                                            'observed IDs, in context order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'claim_disposition_unusable',
                                'group': 'unexpected_context_claims',
                                'condition_and_occurrence': 'once per resolved usable claim whose disposition cannot '
                                                            'participate in the fixed closed-set mapping, in '
                                                            'observed-ID order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'claim_class_mismatch',
                                'group': 'claim_disposition_compatibility',
                                'condition_and_occurrence': 'once per resolved usable observed claim whose class '
                                                            'differs from its positionally aligned observed class or '
                                                            'required class, in observed-ID order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'candidate_identity_mismatch',
                                'group': 'claim_class_compatibility',
                                'condition_and_occurrence': 'once per resolved usable observed claim whose candidate '
                                                            'ID or version differs, in observed-ID order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'representation_mismatch',
                                'group': 'candidate_identity_compatibility',
                                'condition_and_occurrence': 'once per resolved usable observed claim whose '
                                                            'representation differs, in observed-ID order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'split_scope_mismatch',
                                'group': 'representation_compatibility',
                                'condition_and_occurrence': 'once per resolved usable observed claim with any split '
                                                            'ID/version, fold_scope, or cutoff_scope mismatch, in '
                                                            'observed-ID order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'paired_record_set_mismatch',
                                'group': 'split_fold_cutoff_compatibility',
                                'condition_and_occurrence': 'once per resolved usable observed claim with '
                                                            'paired_test_record_set_id mismatch, in observed-ID order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'aggregation_weighting_mismatch',
                                'group': 'paired_record_set_compatibility',
                                'condition_and_occurrence': 'once per resolved usable observed claim whose aggregation '
                                                            'or weighting identity differs from its required-position '
                                                            'value, in observed-ID order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'stratum_scope_mismatch',
                                'group': 'aggregation_weighting_compatibility',
                                'condition_and_occurrence': 'once per resolved usable observed claim whose nullable '
                                                            'stratum differs from its required-position value or '
                                                            'conditional scope, in observed-ID order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'inherited_policy_mismatch',
                                'group': 'stratum_compatibility',
                                'condition_and_occurrence': 'once per resolved usable observed claim per mismatching '
                                                            'uncertainty, sample-support, selection-control, then '
                                                            'multiple-comparison identity, in observed-ID then policy '
                                                            'order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'provenance_traceability_mismatch',
                                'group': 'inherited_policy_compatibility',
                                'condition_and_occurrence': 'once per resolved usable observed claim lacking the '
                                                            'frozen provenance/result-chain linkage, in observed-ID '
                                                            'order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'cross_baseline_incomplete',
                                'group': 'provenance_result_chain_traceability',
                                'condition_and_occurrence': 'once when usable aligned required classes lack the exact '
                                                            'cross-baseline class or its upstream-complete climatology '
                                                            'and persistence result chain',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'calibration_requirement_mismatch',
                                'group': 'cross_baseline_completeness',
                                'condition_and_occurrence': 'once when usable aligned required classes lack exactly '
                                                            'the representation-selected calibration class or include '
                                                            'a substituted calibration class',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'threshold_applicability_mismatch',
                                'group': 'calibration_requirement',
                                'condition_and_occurrence': 'once when threshold applicability, required class '
                                                            'coverage, outcome, or post-hoc selection conflicts after '
                                                            'usable applicability/class prerequisites',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'stratum_applicability_mismatch',
                                'group': 'threshold_applicability',
                                'condition_and_occurrence': 'once when stratum applicability, exact ordered '
                                                            'strata/class coverage, outcome, omission, or pooling '
                                                            'conflicts after usable prerequisites',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'no_lookahead_integrity_mismatch',
                                'group': 'stratum_applicability',
                                'condition_and_occurrence': 'once per independently diagnosable fixed no-lookahead, '
                                                            'selection-control, complete-scope, or '
                                                            'publication-availability violation in frozen check order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'component_outcome_mismatch',
                                'group': 'no_lookahead_integrity',
                                'condition_and_occurrence': 'once per non-overall component whose supplied outcome '
                                                            'differs from the fixed claim-to-component result, in '
                                                            'canonical order, then once if supplied overall outcome '
                                                            'differs from fixed first-five derivation',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'disposition_precedence_mismatch',
                                'group': 'component_outcome_consistency',
                                'condition_and_occurrence': 'once when supplied gate disposition differs from the '
                                                            'fixed overall outcome/precedence mapping',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'complete_rule_required',
                                'group': 'disposition_precedence',
                                'condition_and_occurrence': 'once when passed/not_passed is supplied without complete '
                                                            'evaluable required claims, or when no fixed complete '
                                                            'outcome can be derived but an evaluable disposition is '
                                                            'supplied',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_provenance',
                                'group': 'complete_rule_requirement',
                                'condition_and_occurrence': 'once per non-exact/nonblank provenance element after '
                                                            'exact tuple prerequisite, in provenance order',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'empty_provenance',
                                'group': 'provenance',
                                'condition_and_occurrence': 'once when provenance is an exact empty tuple',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_decision_created_at',
                                'group': 'decision_created_timestamp',
                                'condition_and_occurrence': 'once when present timestamp fails exact offset-aware '
                                                            'ISO-8601 grammar; blank/wrong-type text may also receive '
                                                            'BLANK_REQUIRED_TEXT earlier',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'self_supersession',
                                'group': 'self_supersession',
                                'condition_and_occurrence': 'once when usable supersession text equals usable '
                                                            'evidence_gate_decision_id',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'},
                               {'code': 'invalid_supersession_link',
                                'group': 'supersession_link',
                                'condition_and_occurrence': 'once when a present exact nonblank non-self supersession '
                                                            'ID is absent from the usable provenance tuple; no '
                                                            'prior-decision lookup, persistence, or registry is '
                                                            'permitted',
                                'prerequisite_and_suppression': 'run only when the condition text prerequisites are '
                                                                'usable; otherwise suppress this code while later '
                                                                'independent groups still run'}]}
HEADINGS = ['Verdict and decision boundary', 'Predecessor and exact base', 'Authority and reconciliation', 'Future two-file scope', 'Frozen API and record representation', 'Mapping and direct-validation contract', 'Caller-supplied evaluation-claim context', 'Applicability, completeness, and no-lookahead', 'Gate rule, component, and disposition semantics', 'Immutability, provenance, and supersession', 'Implementation-approval separation', 'Safety, routing, and explicit non-goals', 'Human decision and successor posture', 'Machine contract', 'Acceptance criteria']

def _read(text: str | None = None) -> str:
    return DOC.read_text(encoding="utf-8") if text is None else text

def _contract(text: str) -> dict[str, object]:
    matches = re.findall(r"```json\n(.*?)\n```", text, re.DOTALL)
    assert len(matches) == 1
    return json.loads(matches[0])

def _validate(text: str | None = None) -> None:
    doc = _read(text)
    lines = doc.splitlines()
    assert lines[:3] == [f"# {EXPECTED['title']}", "", f"Canonical ID: {EXPECTED['canonical_id']}"]
    assert doc.count("Canonical ID:") == 1
    assert re.findall(r"^## (.+)$", doc, re.MULTILINE) == HEADINGS
    actual = _contract(doc)
    assert actual == EXPECTED
    assert list(actual) == list(EXPECTED)
    assert len(actual["record_fields"]) == 36
    assert len(actual["required_mapping_keys"]) == 35
    assert len(actual["optional_mapping_keys"]) == 1
    assert len(actual["enums"]["EvidenceGateValidationCode"]) == 45
    assert len(actual["validation_groups"]) == 45
    assert actual["field_semantics"] == EXPECTED["field_semantics"]
    assert [entry["code"] for entry in actual["validation_code_semantics"]] == [entry[1] for entry in EXPECTED["enums"]["EvidenceGateValidationCode"]]
    assert [entry["group"] for entry in actual["validation_code_semantics"]] == EXPECTED["validation_groups"]
    assert actual["validation_code_semantics"] == EXPECTED["validation_code_semantics"]
    assert [x[1] for x in actual["enums"]["EvidenceGateComponent"]] == EXPECTED["gate_components"]
    assert [x[1] for x in actual["enums"]["EvidenceGateComponentOutcome"]] == EXPECTED["component_outcomes"]
    assert [x[1] for x in actual["enums"]["EvidenceGateDisposition"]] == EXPECTED["gate_dispositions"]
    assert actual["required_mapping_keys"] + actual["optional_mapping_keys"] == [x[0] for x in EXPECTED["record_fields"]]
    assert actual["decision_options"] == ["approve_later_evidence_gate_decision_implementation_ticket", "request_approval_request_revision", "hold", "block"]
    assert actual["fixed_assignments"]["canonical_routing_fields"] == ["condition_id", "token_id", "outcome"]
    assert actual["status"] == "request_prepared_implementation_not_approved"
    assert "DOES NOT approve implementation" in actual["approval_separation"]

def _allowlist() -> dict[str, int]:
    tree = ast.parse(ALLOWLIST.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "ALLOWED_MARKET_ID_OCCURRENCE_LINES":
            value = node.value.args[0] if isinstance(node.value, ast.Call) else node.value
            return ast.literal_eval(value)
    raise AssertionError("allowlist missing")

def _legacy_lines(path: Path) -> int:
    token = "market" + "_id"
    return sum(token in line for line in path.read_text(encoding="utf-8").splitlines())

def test_exact_approval_request_contract() -> None:
    _validate()

def test_direct_allowlist_occurrences() -> None:
    allowlist = _allowlist()
    for rel in EXPECTED["pr_files"][:2]:
        count = _legacy_lines(ROOT / rel)
        if count:
            assert allowlist[rel] == count
        else:
            assert rel not in allowlist

def test_literal_oracle_is_complete_and_independent() -> None:
    assert EXPECTED["actual_pr_378_merge_sha"] == "5bf865218c5187a9ccdb58d3c0c974d08610796d"
    assert EXPECTED["approved_pr_378_head"] == "1c4f731dda6d129923c87bb93d540ef4be3fd870"
    assert len(EXPECTED["gate_components"]) == len(EXPECTED["component_outcomes"]) == 6
    assert len(EXPECTED["gate_dispositions"]) == 5
    assert EXPECTED["disposition_precedence"] == ["BLOCKED", "UNAVAILABLE", "INSUFFICIENT", "PASSED_OR_NOT_PASSED_BY_COMPLETE_PREDECLARED_RULE"]
    assert EXPECTED["future_files"] == ["meg/weather/stage3/evidence_gate_decision.py", "tests/core/test_weather_bot_stage3_evidence_gate_decision.py"]

def test_meaningful_contract_mutations_are_rejected() -> None:
    original = _read()
    mutations = []
    replacements = [
        ("request_prepared_implementation_not_approved", "implementation_approved"),
        ("5bf865218c5187a9ccdb58d3c0c974d08610796d", "1c4f731dda6d129923c87bb93d540ef4be3fd870"),
        ('"cross_baseline_predictive_skill",\n    "representation_appropriate_calibration"', '"representation_appropriate_calibration",\n    "cross_baseline_predictive_skill"'),
        ('"BLOCKED",\n    "UNAVAILABLE"', '"UNAVAILABLE",\n    "BLOCKED"'),
        ('"evidence_gate_decision_id",\n      "str"', '"renamed_decision_id",\n      "str"'),
        ('"approve_later_evidence_gate_decision_implementation_ticket"', '"approve_now"'),
        ('"condition_id",\n      "token_id",\n      "outcome"', '"condition_id",\n      "outcome"'),
    ]
    for old, new in replacements:
        assert old in original
        mutations.append(original.replace(old, new))
    heading_swap = original.replace("## Future two-file scope", "## TEMP", 1).replace("## Frozen API and record representation", "## Future two-file scope", 1).replace("## TEMP", "## Frozen API and record representation", 1)
    mutations.append(heading_swap)
    for mutation in mutations:
        with pytest.raises(AssertionError):
            _validate(mutation)

def test_table_and_assignment_mutations_are_rejected() -> None:
    original = _read()
    parsed = _contract(original)
    mutations = []
    for path, value in [
        (("required_mapping_keys",), parsed["required_mapping_keys"][:-1]),
        (("validation_groups",), list(reversed(parsed["validation_groups"]))),
        (("claim_context_contract", "order"), "claims may be reordered"),
        (("claim_context_contract", "policy_alignment"), "policies may be deduplicated"),
        (("component_applicability", "mandatory"), parsed["component_applicability"]["mandatory"][:-1]),
        (("component_applicability", "outcome_alignment"), "pairs may be reordered"),
        (("gate_rule_execution_boundary", "validator_must_not"), "a rule registry is permitted"),
        (("validation_code_semantics",), parsed["validation_code_semantics"][:-1]),
        (("field_semantics", "component_outcomes", "validation_dependency"), "pairing is implementation-defined"),
        (("non_goals",), parsed["non_goals"][:-1]),
    ]:
        changed = copy.deepcopy(parsed)
        target = changed
        for key in path[:-1]: target = target[key]
        target[path[-1]] = value
        block = json.dumps(parsed, indent=2)
        replacement = json.dumps(changed, indent=2)
        mutations.append(original.replace(block, replacement, 1))
    for mutation in mutations:
        with pytest.raises(AssertionError):
            _validate(mutation)
