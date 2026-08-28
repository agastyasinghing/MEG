# WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-IMPLEMENTATION-APPROVAL-REQUEST-01

Canonical ID: WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-IMPLEMENTATION-APPROVAL-REQUEST-01

## Verdict and decision boundary

This is approval-request-only documentation/static-test work. Its posture is `request_prepared_implementation_not_approved`. It asks for a separate human decision and neither implements nor approves the evidence gate.

## Predecessor and exact base

The exact base and actual PR #378 merge is `5bf865218c5187a9ccdb58d3c0c974d08610796d`; its approved implementation head is `1c4f731dda6d129923c87bb93d540ef4be3fd870`. The actual merge, never a preview merge SHA, is verified in current ancestry.

## Authority and reconciliation

The planning contract remains semantically controlling. The merged upstream APIs are reconciled by the explicit ambiguity resolutions below; they require no renaming, semantic-field removal, alias, or existing-file change.

## Future two-file scope

Only a later explicitly approved ticket may change exactly `meg/weather/stage3/evidence_gate_decision.py` and `tests/core/test_weather_bot_stage3_evidence_gate_decision.py`. It may create immutable caller-supplied records, adapt mappings, validate fail-closed, and apply only the already-predeclared rule semantics frozen here. It may not fetch, generate, repair, select, rank, persist, or report evidence.

## Frozen API and record representation

All enums are ordered `StrEnum` classes and both records are frozen dataclasses. The machine contract freezes every symbol, enum, annotation, field order, default, mapping key, list adaptation, and function signature. No convenience API or re-export is allowed. Both functions receive caller-supplied claim context explicitly; no separate collection validator is needed.

## Mapping and direct-validation contract

The machine contract is exhaustive. Mapping reads catch ordinary `Exception` but never `BaseException`; hostile/asymmetric key equality fails closed. Direct records are never adapted or mutated. Validation codes occur in the exact ordered groups and are neither sorted nor deduplicated.

## Caller-supplied evaluation-claim context

Only caller-supplied immutable `EvaluationClaimRecord` objects are consumed. The exact container, identity resolution, ordering, completeness, compatibility, invalid-item handling, and dependent-check suppression rules are frozen in the machine contract.

## Applicability, completeness, and no-lookahead

Applicability is predeclared before claim-disposition inspection. Cross-baseline, representation-selected calibration, selection/no-lookahead, and overall components are mandatory. Threshold and stratum components are conditional only under predeclared applicability. No unfavorable evidence may be dropped, pooled, or waived.

## Gate rule, component, and disposition semantics

Blocked precedes unavailable, which precedes insufficient, followed only by complete-rule passed/not-passed evaluation. Not-satisfied and not-passed are not insufficiency. The six components, six outcomes, five dispositions, structural precedence, caller-supplied predeclared overall-rule result, and fixed outcome-to-disposition consistency are literal closed sets below. Gate/rule identifiers are opaque metadata: no rule DSL, registry, callback, threshold engine, or arbitrary execution is approved.

## Immutability, provenance, and supersession

Accepted records and claim context are immutable. Corrections require a new decision identity and explicit supersession; self-supersession fails closed. Provenance and complete result-chain traceability are mandatory.

## Implementation-approval separation

`stage3_gate_passed` DOES NOT approve implementation. It records only satisfaction of the exact predeclared rule for the exact candidate and scope, and can support only a later separate readiness/approval sequence. No disposition authorizes deployment, runtime, simulation, paper trading, trading, orders, or autonomy.

## Safety, routing, and explicit non-goals

This PR creates no production code, schemas, fixtures, datasets, dependencies, workflows, migrations, runtime configuration, evidence, decision, persistence, serialization, report, export, or execution. Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`; market_id is non-routing and `token_outcome_pair` is derived only.

## Human decision and successor posture

The four ordered options are frozen below. Creation or merge implies no approval. Only explicit selection of `approve_later_evidence_gate_decision_implementation_ticket` after this request is merged allows the separate successor ticket to begin.

## Machine contract

The following JSON is the sole machine-assignment block. Array order is significant.

```json
{
  "title": "WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-IMPLEMENTATION-APPROVAL-REQUEST-01",
  "canonical_id": "WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-IMPLEMENTATION-APPROVAL-REQUEST-01",
  "status": "request_prepared_implementation_not_approved",
  "actual_pr_378_merge_sha": "5bf865218c5187a9ccdb58d3c0c974d08610796d",
  "approved_pr_378_head": "1c4f731dda6d129923c87bb93d540ef4be3fd870",
  "base_sha": "5bf865218c5187a9ccdb58d3c0c974d08610796d",
  "pr_files": [
    "docs/prd/WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-IMPLEMENTATION-APPROVAL-REQUEST-01.md",
    "tests/core/test_weather_bot_stage3_evidence_gate_decision_implementation_approval_request_01.py",
    "tests/core/canonical_id_allowlist.py"
  ],
  "future_files": [
    "meg/weather/stage3/evidence_gate_decision.py",
    "tests/core/test_weather_bot_stage3_evidence_gate_decision.py"
  ],
  "public_symbols": [
    "EvidenceGateComponent",
    "EvidenceGateComponentOutcome",
    "EvidenceGateDisposition",
    "EvidenceGateValidationSeverity",
    "EvidenceGateValidationCode",
    "EvidenceGateDecisionRecord",
    "EvidenceGateValidationResult",
    "evidence_gate_decision_from_mapping",
    "validate_evidence_gate_decision"
  ],
  "permitted_imports": [
    "ScoringPredictionRepresentation",
    "EvaluationClaimClass",
    "EvaluationClaimDisposition",
    "EvaluationClaimRecord"
  ],
  "enums": {
    "EvidenceGateComponent": [
      [
        "CROSS_BASELINE_PREDICTIVE_SKILL",
        "cross_baseline_predictive_skill"
      ],
      [
        "REPRESENTATION_APPROPRIATE_CALIBRATION",
        "representation_appropriate_calibration"
      ],
      [
        "THRESHOLD_WEIGHTED_SKILL_WHEN_APPLICABLE",
        "threshold_weighted_skill_when_applicable"
      ],
      [
        "STRATUM_SPECIFIC_SKILL_WHEN_APPLICABLE",
        "stratum_specific_skill_when_applicable"
      ],
      [
        "SELECTION_SCOPE_AND_NO_LOOKAHEAD_INTEGRITY",
        "selection_scope_and_no_lookahead_integrity"
      ],
      [
        "OVERALL_STAGE3_EVIDENCE_GATE",
        "overall_stage3_evidence_gate"
      ]
    ],
    "EvidenceGateComponentOutcome": [
      [
        "COMPONENT_SATISFIED",
        "component_satisfied"
      ],
      [
        "COMPONENT_NOT_SATISFIED",
        "component_not_satisfied"
      ],
      [
        "COMPONENT_INSUFFICIENT",
        "component_insufficient"
      ],
      [
        "COMPONENT_BLOCKED",
        "component_blocked"
      ],
      [
        "COMPONENT_UNAVAILABLE",
        "component_unavailable"
      ],
      [
        "COMPONENT_NOT_APPLICABLE",
        "component_not_applicable"
      ]
    ],
    "EvidenceGateDisposition": [
      [
        "STAGE3_GATE_PASSED",
        "stage3_gate_passed"
      ],
      [
        "STAGE3_GATE_NOT_PASSED",
        "stage3_gate_not_passed"
      ],
      [
        "STAGE3_GATE_INSUFFICIENT",
        "stage3_gate_insufficient"
      ],
      [
        "STAGE3_GATE_BLOCKED",
        "stage3_gate_blocked"
      ],
      [
        "STAGE3_GATE_UNAVAILABLE",
        "stage3_gate_unavailable"
      ]
    ],
    "EvidenceGateValidationSeverity": [
      [
        "PASSED",
        "passed"
      ],
      [
        "BLOCKED",
        "blocked"
      ]
    ],
    "EvidenceGateValidationCode": [
      [
        "MISSING_REQUIRED_FIELD",
        "missing_required_field"
      ],
      [
        "UNEXPECTED_FIELD",
        "unexpected_field"
      ],
      [
        "BLANK_REQUIRED_TEXT",
        "blank_required_text"
      ],
      [
        "INVALID_GATE_COMPONENT",
        "invalid_gate_component"
      ],
      [
        "INVALID_COMPONENT_OUTCOME",
        "invalid_component_outcome"
      ],
      [
        "INVALID_GATE_DISPOSITION",
        "invalid_gate_disposition"
      ],
      [
        "INVALID_PREDICTION_REPRESENTATION",
        "invalid_prediction_representation"
      ],
      [
        "INVALID_CLAIM_CLASS",
        "invalid_claim_class"
      ],
      [
        "INVALID_FIXED_POSTURE",
        "invalid_fixed_posture"
      ],
      [
        "INVALID_TEXT_TUPLE",
        "invalid_text_tuple"
      ],
      [
        "INVALID_CLAIM_ID_TUPLE",
        "invalid_claim_id_tuple"
      ],
      [
        "INVALID_CLAIM_CLASS_TUPLE",
        "invalid_claim_class_tuple"
      ],
      [
        "INVALID_COMPONENT_TUPLE",
        "invalid_component_tuple"
      ],
      [
        "INVALID_COMPONENT_OUTCOME_TUPLE",
        "invalid_component_outcome_tuple"
      ],
      [
        "CLAIM_SET_PARTITION_MISMATCH",
        "claim_set_partition_mismatch"
      ],
      [
        "CLAIM_CLASS_SEQUENCE_MISMATCH",
        "claim_class_sequence_mismatch"
      ],
      [
        "APPLICABILITY_MISMATCH",
        "applicability_mismatch"
      ],
      [
        "INVALID_CLAIM_RECORD_CONTAINER",
        "invalid_claim_record_container"
      ],
      [
        "INVALID_CLAIM_RECORD",
        "invalid_claim_record"
      ],
      [
        "DUPLICATE_CONTEXT_CLAIM_ID",
        "duplicate_context_claim_id"
      ],
      [
        "OBSERVED_CLAIM_NOT_FOUND",
        "observed_claim_not_found"
      ],
      [
        "UNEXPECTED_CONTEXT_CLAIM",
        "unexpected_context_claim"
      ],
      [
        "CLAIM_DISPOSITION_UNUSABLE",
        "claim_disposition_unusable"
      ],
      [
        "CLAIM_CLASS_MISMATCH",
        "claim_class_mismatch"
      ],
      [
        "CANDIDATE_IDENTITY_MISMATCH",
        "candidate_identity_mismatch"
      ],
      [
        "REPRESENTATION_MISMATCH",
        "representation_mismatch"
      ],
      [
        "SPLIT_SCOPE_MISMATCH",
        "split_scope_mismatch"
      ],
      [
        "PAIRED_RECORD_SET_MISMATCH",
        "paired_record_set_mismatch"
      ],
      [
        "AGGREGATION_WEIGHTING_MISMATCH",
        "aggregation_weighting_mismatch"
      ],
      [
        "STRATUM_SCOPE_MISMATCH",
        "stratum_scope_mismatch"
      ],
      [
        "INHERITED_POLICY_MISMATCH",
        "inherited_policy_mismatch"
      ],
      [
        "PROVENANCE_TRACEABILITY_MISMATCH",
        "provenance_traceability_mismatch"
      ],
      [
        "CROSS_BASELINE_INCOMPLETE",
        "cross_baseline_incomplete"
      ],
      [
        "CALIBRATION_REQUIREMENT_MISMATCH",
        "calibration_requirement_mismatch"
      ],
      [
        "THRESHOLD_APPLICABILITY_MISMATCH",
        "threshold_applicability_mismatch"
      ],
      [
        "STRATUM_APPLICABILITY_MISMATCH",
        "stratum_applicability_mismatch"
      ],
      [
        "NO_LOOKAHEAD_INTEGRITY_MISMATCH",
        "no_lookahead_integrity_mismatch"
      ],
      [
        "COMPONENT_OUTCOME_MISMATCH",
        "component_outcome_mismatch"
      ],
      [
        "DISPOSITION_PRECEDENCE_MISMATCH",
        "disposition_precedence_mismatch"
      ],
      [
        "COMPLETE_RULE_REQUIRED",
        "complete_rule_required"
      ],
      [
        "INVALID_PROVENANCE",
        "invalid_provenance"
      ],
      [
        "EMPTY_PROVENANCE",
        "empty_provenance"
      ],
      [
        "INVALID_DECISION_CREATED_AT",
        "invalid_decision_created_at"
      ],
      [
        "SELF_SUPERSESSION",
        "self_supersession"
      ],
      [
        "INVALID_SUPERSESSION_LINK",
        "invalid_supersession_link"
      ]
    ]
  },
  "record_fields": [
    [
      "evidence_gate_decision_id",
      "str",
      null
    ],
    [
      "evidence_gate_id",
      "str",
      null
    ],
    [
      "evidence_gate_version",
      "str",
      null
    ],
    [
      "gate_rule_id",
      "str",
      null
    ],
    [
      "gate_rule_version",
      "str",
      null
    ],
    [
      "gate_disposition",
      "EvidenceGateDisposition",
      null
    ],
    [
      "gate_disposition_reason",
      "str",
      null
    ],
    [
      "target_posture",
      "str",
      null
    ],
    [
      "candidate_method_id",
      "str",
      null
    ],
    [
      "candidate_method_version",
      "str",
      null
    ],
    [
      "prediction_representation",
      "ScoringPredictionRepresentation",
      null
    ],
    [
      "required_evaluation_claim_ids",
      "tuple[str, ...]",
      null
    ],
    [
      "observed_evaluation_claim_ids",
      "tuple[str, ...]",
      null
    ],
    [
      "missing_evaluation_claim_ids",
      "tuple[str, ...]",
      null
    ],
    [
      "required_claim_classes",
      "tuple[EvaluationClaimClass, ...]",
      null
    ],
    [
      "observed_claim_classes",
      "tuple[EvaluationClaimClass, ...]",
      null
    ],
    [
      "applicable_gate_components",
      "tuple[EvidenceGateComponent, ...]",
      null
    ],
    [
      "component_outcomes",
      "tuple[tuple[EvidenceGateComponent, EvidenceGateComponentOutcome], ...]",
      null
    ],
    [
      "split_id",
      "str",
      null
    ],
    [
      "split_version",
      "str",
      null
    ],
    [
      "fold_scope",
      "str",
      null
    ],
    [
      "cutoff_scope",
      "str",
      null
    ],
    [
      "paired_test_record_set_id",
      "str",
      null
    ],
    [
      "aggregation_rule_ids",
      "tuple[str, ...]",
      null
    ],
    [
      "weighting_rule_ids",
      "tuple[str, ...]",
      null
    ],
    [
      "stratum_scope",
      "tuple[str | None, ...]",
      null
    ],
    [
      "uncertainty_policy_ids",
      "tuple[str, ...]",
      null
    ],
    [
      "sample_support_rule_ids",
      "tuple[str, ...]",
      null
    ],
    [
      "selection_control_policy_ids",
      "tuple[str, ...]",
      null
    ],
    [
      "multiple_comparison_policy_ids",
      "tuple[str | None, ...]",
      null
    ],
    [
      "no_lookahead_review_posture",
      "str",
      null
    ],
    [
      "result_chain_traceability_posture",
      "str",
      null
    ],
    [
      "subsequent_approval_request_eligibility_posture",
      "str",
      null
    ],
    [
      "provenance",
      "tuple[str, ...]",
      null
    ],
    [
      "decision_created_at",
      "str",
      null
    ],
    [
      "supersedes_decision_id_when_applicable",
      "str | None",
      "None"
    ]
  ],
  "validation_result_fields": [
    [
      "severity",
      "EvidenceGateValidationSeverity",
      null
    ],
    [
      "passed",
      "bool",
      null
    ],
    [
      "codes",
      "tuple[EvidenceGateValidationCode, ...]",
      "()"
    ]
  ],
  "signatures": {
    "adapter": "def evidence_gate_decision_from_mapping(\n    mapping: object,\n    evaluation_claims: object,\n) -> tuple[EvidenceGateDecisionRecord | None, EvidenceGateValidationResult]:",
    "validator": "def validate_evidence_gate_decision(\n    record: EvidenceGateDecisionRecord,\n    evaluation_claims: tuple[EvaluationClaimRecord, ...],\n) -> EvidenceGateValidationResult:"
  },
  "required_mapping_keys": [
    "evidence_gate_decision_id",
    "evidence_gate_id",
    "evidence_gate_version",
    "gate_rule_id",
    "gate_rule_version",
    "gate_disposition",
    "gate_disposition_reason",
    "target_posture",
    "candidate_method_id",
    "candidate_method_version",
    "prediction_representation",
    "required_evaluation_claim_ids",
    "observed_evaluation_claim_ids",
    "missing_evaluation_claim_ids",
    "required_claim_classes",
    "observed_claim_classes",
    "applicable_gate_components",
    "component_outcomes",
    "split_id",
    "split_version",
    "fold_scope",
    "cutoff_scope",
    "paired_test_record_set_id",
    "aggregation_rule_ids",
    "weighting_rule_ids",
    "stratum_scope",
    "uncertainty_policy_ids",
    "sample_support_rule_ids",
    "selection_control_policy_ids",
    "multiple_comparison_policy_ids",
    "no_lookahead_review_posture",
    "result_chain_traceability_posture",
    "subsequent_approval_request_eligibility_posture",
    "provenance",
    "decision_created_at"
  ],
  "optional_mapping_keys": [
    "supersedes_decision_id_when_applicable"
  ],
  "list_to_tuple_fields": [
    "required_evaluation_claim_ids",
    "observed_evaluation_claim_ids",
    "missing_evaluation_claim_ids",
    "required_claim_classes",
    "observed_claim_classes",
    "applicable_gate_components",
    "component_outcomes",
    "aggregation_rule_ids",
    "weighting_rule_ids",
    "stratum_scope",
    "uncertainty_policy_ids",
    "sample_support_rule_ids",
    "selection_control_policy_ids",
    "multiple_comparison_policy_ids",
    "provenance"
  ],
  "enum_adaptation": {
    "gate_disposition": "EvidenceGateDisposition",
    "prediction_representation": "ScoringPredictionRepresentation",
    "required_claim_classes": "EvaluationClaimClass elements",
    "observed_claim_classes": "EvaluationClaimClass elements",
    "applicable_gate_components": "EvidenceGateComponent elements",
    "component_outcomes": "two-item actual list/tuple pairs; EvidenceGateComponent then EvidenceGateComponentOutcome"
  },
  "mapping_failure_contract": [
    "root must be an instance of Mapping; otherwise return no record and exactly 35 repeated missing_required_field codes in required-key order",
    "create the items iterator and snapshot tuple(mapping.items()) exactly once before inspecting items; iterator creation failure or mid-iteration ordinary Exception makes the root unreadable",
    "every snapshotted item must unpack to exactly two values; malformed item shape or unpacking ordinary Exception makes the root unreadable",
    "duplicate detection compares each existing key to the incoming key only, as existing_key == incoming_key, in snapshot order; it never performs the reverse comparison",
    "any truthy existing-to-incoming equality is a duplicate; asymmetric equality therefore follows that one direction, and any ordinary Exception from equality makes the root unreadable",
    "hash every key after duplicate detection and before dictionary materialization; any ordinary Exception from hashing makes the root unreadable",
    "materialize exactly dict(items) once after successful snapshot, duplicate detection, and hashing; any ordinary Exception during materialization, lookup, adaptation, or record construction makes the root unreadable",
    "exact readable keys require type(key) is str; string subclasses and non-string keys each emit unexpected_field in snapshot order after exact-string unexpected keys sorted lexically",
    "an unreadable root returns no partial record and exactly one missing_required_field occurrence for each of the 35 required keys in field order, with no unexpected or semantic codes",
    "catch ordinary Exception at the frozen mapping operations; never catch BaseException, whose subclasses propagate unchanged",
    "shape and semantic failures for a readable root aggregate in validation-group order; repeated codes remain repeated and are never sorted or deduplicated"
  ],
  "built_in_and_nullability": [
    "all non-enum text requires type(value) is str, nonblank under strip, and is never stripped or rewritten",
    "all direct-record tuple fields require type(value) is tuple; tuple subclasses and arbitrary iterables fail",
    "mapping adaptation converts only type(value) is list for declared tuple fields; nested component pairs accept only exact two-item list or tuple",
    "only supersedes_decision_id_when_applicable is nullable and optional; all other 35 keys are required and non-null",
    "enum adaptation accepts an exact enum member or type(value) is str matching exactly; rejects string subclasses, unrelated enums, aliases, names, and case variants",
    "decision_created_at is exact nonblank ISO-8601 text with T and explicit Z or numeric UTC offset; it is never compared with the clock or rewritten",
    "direct record __post_init__ performs no validation, normalization, adaptation, evaluation, or mutation"
  ],
  "claim_context_contract": {
    "accepted_container": "direct validator: exact tuple; adapter: exact tuple or actual list containing only exact EvaluationClaimRecord elements, adapted without mutation",
    "element_type": "type(item) is EvaluationClaimRecord; subclasses and other items are invalid",
    "invalid_items": "one invalid_claim_record per element whose type is not exactly EvaluationClaimRecord, in context order; exact-type claims are trusted as previously validated artifacts, while all gate-visible compatibility checks still run",
    "duplicate_identity": "duplicate_context_claim_id for each later duplicate occurrence; duplicate identities are unusable for resolution",
    "identity_resolution": "required, observed, and missing IDs are each ordered unique. observed and missing are disjoint and their set union equals required. Filtering required by observed membership must equal observed; filtering required by missing membership must equal missing. Each observed ID resolves exactly once.",
    "unexpected_claims": "context identities outside observed IDs are unexpected and rejected; no extra context claims are consumed",
    "order": "context claim order must equal observed_evaluation_claim_ids; reordered or substituted claims fail closed",
    "class_compatibility": "required_claim_classes length equals required_evaluation_claim_ids and aligns one-for-one. observed_claim_classes length equals observed_evaluation_claim_ids and equals required_claim_classes at the same required-ID positions selected by the ordered observed subsequence. Repeated classes are permitted; no ordered-unique derivation or baseline-specific promotion is allowed.",
    "disposition_compatibility": "claim_blocked dominates; then claim_unavailable; then claim_insufficient; claim_supported and claim_not_supported are evaluable and component rules determine satisfied/not_satisfied without inventing substantive rules",
    "candidate_and_representation": "every usable observed claim exactly matches candidate method ID/version and ScoringPredictionRepresentation",
    "scope": "split_id, split_version, fold_scope to claim fold_scope, cutoff_scope, and paired_test_record_set_id match exactly",
    "aggregation_weighting": "claim aggregation_rule_id and weighting_rule_id must occur in the corresponding ordered decision tuples; no substitution",
    "stratum": "claim stratum_id_when_applicable must match the predeclared stratum_scope and conditional applicability; no pooling or omission",
    "inherited_policies": "uncertainty_policy_id, sample_support_rule_id, selection_control_policy_id, and applicable multiple-comparison policy must occur in the corresponding decision tuples exactly",
    "provenance_traceability": "each exact claim must carry the previously validated artifact posture through explicit immutable provenance/result-chain references; the gate does not invoke upstream result-context validation and fetches or regenerates nothing",
    "dependent_suppression": "missing, invalid, duplicated, or unresolved claims do not fabricate unrelated class, compatibility, component, or disposition failures",
    "policy_alignment": "aggregation_rule_ids, weighting_rule_ids, stratum_scope, uncertainty_policy_ids, sample_support_rule_ids, selection_control_policy_ids, and multiple_comparison_policy_ids each have exactly the required-claim-ID length and align one-for-one by required claim position. Values preserve the caller-predeclared required set, including repeated values and None only for stratum/multiple-comparison; there is no sorting, deduplication, inference, or observed-only shortening. Each usable observed claim must equal the values at its required-ID position.",
    "independent_checks": "after an invalid, duplicate, missing, or unresolved item is excluded from evidence-dependent comparison, every structural or compatibility check whose own prerequisites remain usable still runs in validation-group order"
  },
  "gate_components": [
    "cross_baseline_predictive_skill",
    "representation_appropriate_calibration",
    "threshold_weighted_skill_when_applicable",
    "stratum_specific_skill_when_applicable",
    "selection_scope_and_no_lookahead_integrity",
    "overall_stage3_evidence_gate"
  ],
  "component_outcomes": [
    "component_satisfied",
    "component_not_satisfied",
    "component_insufficient",
    "component_blocked",
    "component_unavailable",
    "component_not_applicable"
  ],
  "gate_dispositions": [
    "stage3_gate_passed",
    "stage3_gate_not_passed",
    "stage3_gate_insufficient",
    "stage3_gate_blocked",
    "stage3_gate_unavailable"
  ],
  "disposition_precedence": [
    "BLOCKED",
    "UNAVAILABLE",
    "INSUFFICIENT",
    "PASSED_OR_NOT_PASSED_BY_COMPLETE_PREDECLARED_RULE"
  ],
  "component_applicability": {
    "fixed_before": "claim-disposition inspection",
    "mandatory": [
      "cross_baseline_predictive_skill",
      "representation_appropriate_calibration",
      "selection_scope_and_no_lookahead_integrity",
      "overall_stage3_evidence_gate"
    ],
    "conditional": [
      "threshold_weighted_skill_when_applicable",
      "stratum_specific_skill_when_applicable"
    ],
    "applicable_subset": "applicable_gate_components is the exact ordered subset of the canonical six components, retaining canonical relative order; it contains every mandatory component and includes each conditional component if and only if predeclared applicable",
    "outcome_alignment": "component_outcomes is always exactly six canonical component/outcome pairs in canonical order. A conditional component absent from applicable_gate_components must be component_not_applicable; a present conditional component must not be component_not_applicable. Mandatory and overall components are never absent or not_applicable.",
    "rules": [
      "binary outcome probability requires binary_calibration_behavior",
      "full predictive distribution requires distributional_calibration_behavior",
      "finite comparable ensemble requires ensemble_calibration_behavior",
      "no component may be added, removed, pooled, waived, substituted, or reordered after claim inspection"
    ]
  },
  "required_claim_set": [
    "required, observed, and missing IDs are exact built-in-string tuples, ordered, unique, and preserve the required partition",
    "tuple(identity for identity in required if identity in observed) equals observed; tuple(identity for identity in required if identity in missing) equals missing",
    "set(observed) is disjoint from set(missing), and their set union equals set(required)",
    "interleaving is valid: required (A, B, C), observed (A, C), missing (B); observed (C, A) or missing subsequences out of required order fail closed",
    "observed_claim_classes is the positional required_claim_classes subsequence selected by observed required-ID positions",
    "passed and not_passed require zero missing IDs and a complete evaluable required set",
    "claims are never inferred, regenerated, backfilled, replaced, selected, or repaired"
  ],
  "cross_baseline_and_calibration": [
    "cross-baseline predictive skill requires complete climatology and persistence coverage",
    "a baseline-specific claim cannot be promoted into a cross-baseline claim",
    "binary outcome probability maps only to binary calibration",
    "full predictive distribution maps only to distributional calibration",
    "finite comparable ensemble maps only to ensemble calibration",
    "market price is not a baseline, settlement truth, calibration truth, or frictionless probability"
  ],
  "predeclaration": [
    "gate and rule identity/version",
    "candidate identity/version and representation",
    "applicable components before claim inspection",
    "required claim identities and classes; no runtime claim selection",
    "component rules and complete overall rule",
    "blocked then unavailable then insufficient precedence",
    "complete evaluation scope and no-lookahead review",
    "uncertainty, sample-support, selection-control, and multiple-comparison policies",
    "missing, unavailable, insufficient, and blocked behavior",
    "supersession requires new identity and explicit prior link"
  ],
  "component_outcome_rules": [
    "component_blocked records a predeclared component block and cannot be downgraded by unavailable, insufficient, or substantive rule results",
    "component_unavailable records unavailable required input only when no blocked condition applies",
    "component_insufficient records insufficient evidence only when no blocked or unavailable condition applies",
    "component_not_satisfied records an evaluable predeclared component-rule result and is not insufficiency; it does not by itself determine the opaque overall rule result",
    "component_satisfied records an evaluable predeclared component-rule result; the validator does not recalculate substantive satisfaction",
    "component_not_applicable is required exactly for a conditional component absent from the predeclared applicable subset and forbidden otherwise",
    "each canonical component appears exactly once in component_outcomes in canonical order; no pair is missing, duplicated, extra, substituted, or reordered"
  ],
  "disposition_rules": [
    "any usable applicable claim/component blocked condition -> overall component_blocked and stage3_gate_blocked",
    "otherwise any usable applicable claim/component unavailable condition -> overall component_unavailable and stage3_gate_unavailable",
    "otherwise any usable applicable claim/component insufficient condition -> overall component_insufficient and stage3_gate_insufficient",
    "otherwise, with a complete evaluable required set, caller-supplied overall component_satisfied -> stage3_gate_passed and overall component_not_satisfied -> stage3_gate_not_passed according to the already-predeclared external overall rule result",
    "non-overall component_not_satisfied does not automatically prevent passage when the predeclared overall rule validly does not require its satisfaction",
    "stage3_gate_passed and stage3_gate_not_passed require an exact complete evaluable required claim set with no missing claims",
    "gate_disposition_reason is required exact built-in nonblank text for all dispositions, preserved verbatim, never generated, and never semantically parsed"
  ],
  "validation_groups": [
    "missing_keys",
    "unexpected_exact_string_keys",
    "unexpected_remaining_keys",
    "required_and_nullable_text",
    "gate_component_enum",
    "component_outcome_enum",
    "gate_disposition_enum",
    "prediction_representation_enum",
    "claim_class_enum",
    "fixed_postures",
    "text_tuple_structure",
    "claim_identity_tuple_structure",
    "claim_class_tuple_structure",
    "component_tuple_structure",
    "component_outcome_tuple_structure",
    "claim_set_partition",
    "claim_class_sequence",
    "component_applicability",
    "claim_context_container",
    "individual_claim_validity",
    "context_identity_uniqueness",
    "observed_claim_resolution",
    "unexpected_context_claims",
    "claim_disposition_compatibility",
    "claim_class_compatibility",
    "candidate_identity_compatibility",
    "representation_compatibility",
    "split_fold_cutoff_compatibility",
    "paired_record_set_compatibility",
    "aggregation_weighting_compatibility",
    "stratum_compatibility",
    "inherited_policy_compatibility",
    "provenance_result_chain_traceability",
    "cross_baseline_completeness",
    "calibration_requirement",
    "threshold_applicability",
    "stratum_applicability",
    "no_lookahead_integrity",
    "component_outcome_consistency",
    "disposition_precedence",
    "complete_rule_requirement",
    "provenance",
    "decision_created_timestamp",
    "self_supersession",
    "supersession_link"
  ],
  "validation_occurrence": "one code at each diagnosable occurrence in validation-group order; repeated codes remain repeated; dependent groups run only with usable prerequisites; empty codes force passed/true and nonempty codes force blocked/false",
  "fixed_assignments": {
    "target_posture": "venue_defined_settlement_outcome",
    "no_lookahead_review_posture": "predeclared_point_in_time_review_completed",
    "result_chain_traceability_posture": "complete_immutable_result_chain_required",
    "passed_eligibility": "eligible_for_later_separate_readiness_or_approval_request_only",
    "nonpassed_eligibility": "not_eligible_for_implementation_handoff",
    "canonical_routing_fields": [
      "condition_id",
      "token_id",
      "outcome"
    ],
    "non_routing_field": "market_id",
    "derived_identifier": "token_outcome_pair"
  },
  "immutability": [
    "both record types are frozen dataclasses; accepted tuple contents are immutable",
    "provenance is nonempty exact tuple of exact nonblank built-in strings; order and duplicates are preserved",
    "correction requires a new decision ID, immutable record, explicit supersession link, and retained prior provenance",
    "self-supersession, blank/wrong-type supersession, and a supersession ID absent from provenance fail closed; no overwrite or silent mutation; the pure boundary does not look up prior decisions"
  ],
  "decision_options": [
    "approve_later_evidence_gate_decision_implementation_ticket",
    "request_approval_request_revision",
    "hold",
    "block"
  ],
  "successor_ticket": "WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-IMPLEMENTATION-01",
  "non_goals": [
    "evidence-gate implementation",
    "evidence-gate decision creation",
    "execution over real evidence",
    "evidence-gate passage",
    "score/diagnostic/comparison calculation",
    "claim generation or substantive claim-rule evaluation",
    "probability generation",
    "split execution",
    "baseline execution",
    "model training/calibration",
    "source fetching",
    "provider connectors",
    "persistence or serialization",
    "database tables/migrations",
    "reports/exports",
    "backtesting/simulation",
    "market-price comparison execution",
    "economic-edge/executability findings",
    "paper trading",
    "trading",
    "order placement",
    "production runtime",
    "orchestration",
    "autonomy"
  ],
  "approval_separation": "stage3_gate_passed DOES NOT approve implementation; it means only that the exact predeclared Stage 3 evidence-gate rule was satisfied for the exact recorded candidate and scope; only a later separate readiness/approval sequence may proceed",
  "quantitative_policy": "no numeric alpha, confidence level, correction threshold, effect threshold, sample minimum, bin count, probability tolerance, weighting constant, resampling length, or economic-edge threshold is introduced",
  "ambiguity_resolutions": [
    "the planning field prediction_representation uses the implemented ScoringPredictionRepresentation type and its exact values, not a new alias",
    "fold_scope maps exactly to EvaluationClaimRecord.fold_scope and cutoff_scope maps exactly to EvaluationClaimRecord.cutoff_scope",
    "plural decision policy fields are ordered tuples containing each compatible singular EvaluationClaimRecord policy identity",
    "required_claim_classes and observed_claim_classes use EvaluationClaimClass directly",
    "component_outcomes is an exact six-pair canonical sequence independent of applicable_gate_components length; conditional components absent from the canonical-order applicable subset remain represented by component_not_applicable",
    "required claim IDs are explicitly predeclared; deterministic selection-rule execution is outside this minimal boundary",
    "no semantic conflict requires modification of an existing upstream file",
    "required and observed claim-class tuples are positional, permit repeated classes, and are not ordered-unique derivations",
    "plural policy and stratum tuples align positionally to required claim IDs, preserve repeats and permitted None values, and are never sorted or deduplicated",
    "applicable_gate_components remains the exact ordered applicable subset; component_outcomes separately preserves all six canonical pairs and explicit conditional not_applicable outcomes",
    "gate identifiers remain opaque metadata; only structural blocked/unavailable/insufficient precedence and overall-outcome/disposition consistency are executable, while substantive rule satisfaction remains caller-supplied from the predeclared external rule",
    "supersession validation is syntactic, self-link, and provenance-link-only because the minimal API has no prior-decision context or registry"
  ],
  "field_semantics": {
    "evidence_gate_decision_id": {
      "position": 1,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "evidence_gate_id": {
      "position": 2,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "evidence_gate_version": {
      "position": 3,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "gate_rule_id": {
      "position": 4,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "gate_rule_version": {
      "position": 5,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "gate_disposition": {
      "position": 6,
      "annotation": "EvidenceGateDisposition",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact string to exact enum member",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact EvidenceGateDisposition and exact precedence/final-component consistency",
      "nullable_elements": false
    },
    "gate_disposition_reason": {
      "position": 7,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "target_posture": {
      "position": 8,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "candidate_method_id": {
      "position": 9,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "candidate_method_version": {
      "position": 10,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "prediction_representation": {
      "position": 11,
      "annotation": "ScoringPredictionRepresentation",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact string to exact enum member",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact ScoringPredictionRepresentation and representation-selected calibration compatibility",
      "nullable_elements": false
    },
    "required_evaluation_claim_ids": {
      "position": 12,
      "annotation": "tuple[str, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple of ordered unique exact built-in nonblank strings; claim partition and resolution prerequisites",
      "nullable_elements": false
    },
    "observed_evaluation_claim_ids": {
      "position": 13,
      "annotation": "tuple[str, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple of ordered unique exact built-in nonblank strings; claim partition and resolution prerequisites",
      "nullable_elements": false
    },
    "missing_evaluation_claim_ids": {
      "position": 14,
      "annotation": "tuple[str, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple of ordered unique exact built-in nonblank strings; claim partition and resolution prerequisites",
      "nullable_elements": false
    },
    "required_claim_classes": {
      "position": 15,
      "annotation": "tuple[EvaluationClaimClass, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple of exact EvaluationClaimClass members; positionally aligned to its corresponding claim-ID tuple; duplicates permitted",
      "nullable_elements": false
    },
    "observed_claim_classes": {
      "position": 16,
      "annotation": "tuple[EvaluationClaimClass, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple of exact EvaluationClaimClass members; positionally aligned to its corresponding claim-ID tuple; duplicates permitted",
      "nullable_elements": false
    },
    "applicable_gate_components": {
      "position": 17,
      "annotation": "tuple[EvidenceGateComponent, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact canonical-order applicable subset containing all mandatory components; each conditional member is present iff predeclared applicable; no duplicates or extras",
      "nullable_elements": false
    },
    "component_outcomes": {
      "position": 18,
      "annotation": "tuple[tuple[EvidenceGateComponent, EvidenceGateComponentOutcome], ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact six canonical component/outcome pairs in canonical order; one pair per canonical component; conditional absence from applicable subset maps exactly to component_not_applicable",
      "nullable_elements": false
    },
    "split_id": {
      "position": 19,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "split_version": {
      "position": 20,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "fold_scope": {
      "position": 21,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "cutoff_scope": {
      "position": 22,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "paired_test_record_set_id": {
      "position": 23,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "aggregation_rule_ids": {
      "position": 24,
      "annotation": "tuple[str, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple positionally aligned to required_evaluation_claim_ids; values copied caller-side from each predeclared required claim identity; no sorting, deduplication, inference, or observed-only shortening",
      "nullable_elements": false
    },
    "weighting_rule_ids": {
      "position": 25,
      "annotation": "tuple[str, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple positionally aligned to required_evaluation_claim_ids; values copied caller-side from each predeclared required claim identity; no sorting, deduplication, inference, or observed-only shortening",
      "nullable_elements": false
    },
    "stratum_scope": {
      "position": 26,
      "annotation": "tuple[str | None, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple positionally aligned to required_evaluation_claim_ids; values copied caller-side from each predeclared required claim identity; no sorting, deduplication, inference, or observed-only shortening",
      "nullable_elements": true
    },
    "uncertainty_policy_ids": {
      "position": 27,
      "annotation": "tuple[str, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple positionally aligned to required_evaluation_claim_ids; values copied caller-side from each predeclared required claim identity; no sorting, deduplication, inference, or observed-only shortening",
      "nullable_elements": false
    },
    "sample_support_rule_ids": {
      "position": 28,
      "annotation": "tuple[str, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple positionally aligned to required_evaluation_claim_ids; values copied caller-side from each predeclared required claim identity; no sorting, deduplication, inference, or observed-only shortening",
      "nullable_elements": false
    },
    "selection_control_policy_ids": {
      "position": 29,
      "annotation": "tuple[str, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple positionally aligned to required_evaluation_claim_ids; values copied caller-side from each predeclared required claim identity; no sorting, deduplication, inference, or observed-only shortening",
      "nullable_elements": false
    },
    "multiple_comparison_policy_ids": {
      "position": 30,
      "annotation": "tuple[str | None, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact tuple positionally aligned to required_evaluation_claim_ids; values copied caller-side from each predeclared required claim identity; no sorting, deduplication, inference, or observed-only shortening",
      "nullable_elements": true
    },
    "no_lookahead_review_posture": {
      "position": 31,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "result_chain_traceability_posture": {
      "position": 32,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "subsequent_approval_request_eligibility_posture": {
      "position": 33,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text equal to eligibility_posture_matrix[gate_disposition]; mismatch emits INVALID_FIXED_POSTURE in fixed_postures after a usable exact disposition",
      "nullable_elements": false
    },
    "provenance": {
      "position": 34,
      "annotation": "tuple[str, ...]",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "exact list to tuple",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact nonempty tuple of exact built-in nonblank strings; order and duplicates preserved; result-chain linkage checked",
      "nullable_elements": false
    },
    "decision_created_at": {
      "position": 35,
      "annotation": "str",
      "mapping_key": "required",
      "nullable": false,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "exact built-in nonblank text; fixed-value check where assigned; timestamp grammar additionally for decision_created_at",
      "nullable_elements": false
    },
    "supersedes_decision_id_when_applicable": {
      "position": 36,
      "annotation": "str | None",
      "mapping_key": "optional",
      "nullable": true,
      "mapping_adaptation": "none",
      "direct_record_requirement": "exact declared annotation; no adaptation or normalization",
      "validation_dependency": "None or exact built-in nonblank string; omitted adapts to None; self-link fails; when present it must occur in provenance as the explicit prior-record link; no prior-decision lookup or registry",
      "nullable_elements": false
    }
  },
  "gate_rule_execution_boundary": {
    "gate_rule_identity": "evidence_gate_id/version and gate_rule_id/version are opaque exact nonblank caller-supplied identifiers used for provenance and equality; they are not looked up, selected, parsed, or executed",
    "structural_precedence": "the validator deterministically enforces BLOCKED, then UNAVAILABLE, then INSUFFICIENT from usable claim dispositions and applicable component outcomes before any complete-rule result is accepted",
    "substantive_rule_trust_boundary": "when no blocked/unavailable/insufficient condition applies and the required claim set is complete/evaluable, the caller-supplied overall_stage3_evidence_gate outcome is the recorded result of the already-predeclared substantive overall rule evaluated outside this minimal boundary",
    "not_satisfied_posture": "component_not_satisfied does not automatically force not_passed; passage remains permitted only when the opaque predeclared overall rule validly did not require that component to be satisfied",
    "validator_may": "validate completeness, applicability, fixed precedence, claim/component compatibility, overall outcome to final disposition consistency, reason presence, and eligibility posture; it does not independently prove substantive component or overall-rule satisfaction",
    "validator_must_not": "implement a DSL, rule registry, expression evaluator, callback, dynamic execution, threshold engine, configurable pass logic, scoring, diagnostics, claim generation, or arbitrary substantive rule evaluation",
    "final_mapping": "after structural precedence is clear, caller-supplied overall component_satisfied maps only to stage3_gate_passed and component_not_satisfied maps only to stage3_gate_not_passed; component_blocked/unavailable/insufficient map to their same-named gate dispositions; overall can never be component_not_applicable",
    "dependent_suppression": "when structural prerequisites are unusable, do not fabricate a substantive expected outcome; emit prerequisite diagnostics and independently diagnosable structural errors only"
  },
  "validation_code_semantics": [
    {
      "code": "missing_required_field",
      "condition_and_occurrence": "once per absent required exact-string key, in required-key order; unreadable root returns exactly all 35 occurrences and suppresses every other code",
      "prerequisite_and_suppression": "readable root: exact-string key absence; unreadable root: unconditional 35-code fallback; all semantic groups suppressed for unreadable root"
    },
    {
      "code": "unexpected_field",
      "condition_and_occurrence": "once per unexpected exact-string key in lexical order, then once per string-subclass/non-string key in snapshot order, only for readable root",
      "prerequisite_and_suppression": "readable successfully snapshotted/materialized root only; exact-string unexpected keys precede remaining-key occurrences"
    },
    {
      "code": "blank_required_text",
      "condition_and_occurrence": "once per present required or non-None nullable text field that is not exact built-in nonblank text, in record-field order",
      "prerequisite_and_suppression": "field is present; nullable field is checked only when non-None; enum and tuple fields are excluded"
    },
    {
      "code": "invalid_gate_component",
      "condition_and_occurrence": "once per non-exact EvidenceGateComponent element after a usable outer component tuple/pair structure",
      "prerequisite_and_suppression": "outer component tuple/pair location is structurally readable; repeat per invalid element"
    },
    {
      "code": "invalid_component_outcome",
      "condition_and_occurrence": "once per non-exact EvidenceGateComponentOutcome element after a usable pair structure",
      "prerequisite_and_suppression": "component pair is exact two-item tuple/list after allowed mapping adaptation; repeat per invalid outcome"
    },
    {
      "code": "invalid_gate_disposition",
      "condition_and_occurrence": "once when present disposition is not exact EvidenceGateDisposition",
      "prerequisite_and_suppression": "gate_disposition key/attribute is present; no disposition-dependent check runs until exact enum is usable"
    },
    {
      "code": "invalid_prediction_representation",
      "condition_and_occurrence": "once when present representation is not exact ScoringPredictionRepresentation",
      "prerequisite_and_suppression": "prediction_representation is present; calibration compatibility is suppressed until exact enum is usable"
    },
    {
      "code": "invalid_claim_class",
      "condition_and_occurrence": "once per non-exact EvaluationClaimClass element, required classes then observed classes in tuple order",
      "prerequisite_and_suppression": "corresponding class outer tuple is usable; repeat per non-exact enum element"
    },
    {
      "code": "invalid_fixed_posture",
      "condition_and_occurrence": "once per valid-text fixed posture whose value differs from its frozen assignment, in field order",
      "prerequisite_and_suppression": "relevant text and any controlling enum dependency are usable; eligibility check requires exact gate disposition"
    },
    {
      "code": "invalid_text_tuple",
      "condition_and_occurrence": "once per malformed policy/stratum/provenance tuple entry or outer tuple, in record-field then entry order; specialized identity tuples use their specialized codes",
      "prerequisite_and_suppression": "field is present; inspect entries only when outer value is exact tuple after allowed adapter conversion"
    },
    {
      "code": "invalid_claim_id_tuple",
      "condition_and_occurrence": "once for each malformed required/observed/missing claim-ID tuple; duplicates within a tuple make that tuple malformed",
      "prerequisite_and_suppression": "corresponding ID field is present; partition/resolution suppressed for each unusable tuple"
    },
    {
      "code": "invalid_claim_class_tuple",
      "condition_and_occurrence": "once for each malformed required/observed class outer tuple; element enum errors additionally occur per invalid element",
      "prerequisite_and_suppression": "corresponding class field is present; alignment suppressed for unusable outer tuple"
    },
    {
      "code": "invalid_component_tuple",
      "condition_and_occurrence": "once when applicable_gate_components is not an exact tuple, omits any mandatory component, includes a conditional component not predeclared applicable, omits a conditional component predeclared applicable, violates canonical relative order, or contains a duplicate, extra, or substituted component; valid subset lengths are four, five, or six",
      "prerequisite_and_suppression": "field is present; element enum diagnostics run for readable exact-tuple elements, while applicability and outcome-relationship checks are suppressed until the exact canonical-order applicable subset is usable"
    },
    {
      "code": "invalid_component_outcome_tuple",
      "condition_and_occurrence": "once when component_outcomes is not an exact tuple of six exact two-item tuple pairs in canonical component alignment",
      "prerequisite_and_suppression": "component_outcomes is present; outcome/applicability/precedence checks suppressed until usable six-pair structure"
    },
    {
      "code": "claim_set_partition_mismatch",
      "condition_and_occurrence": "once when usable unique ID tuples do not make observed and missing disjoint subsequences whose merge in required order is exactly required IDs",
      "prerequisite_and_suppression": "all three ID tuples are usable ordered-unique tuples; resolution may still run for independently usable observed IDs"
    },
    {
      "code": "claim_class_sequence_mismatch",
      "condition_and_occurrence": "once for required class/ID length mismatch and once for observed class/ID length or required-subsequence mismatch, in that order",
      "prerequisite_and_suppression": "relevant ID and class tuples are usable; evaluate required alignment then observed positional subsequence"
    },
    {
      "code": "applicability_mismatch",
      "condition_and_occurrence": "once per component roster/outcome applicability violation in canonical component order, including not_applicable on mandatory/overall or non-not_applicable on predeclared-inapplicable conditional",
      "prerequisite_and_suppression": "usable applicable subset and six-pair outcomes; repeat in canonical component order"
    },
    {
      "code": "invalid_claim_record_container",
      "condition_and_occurrence": "once when direct context type is not exact tuple, or adapter context is neither exact tuple nor an exact list wholly eligible for adaptation",
      "prerequisite_and_suppression": "context root is supplied; all item/resolution/compatibility checks suppressed if root unusable"
    },
    {
      "code": "invalid_claim_record",
      "condition_and_occurrence": "once per context item whose type is not exactly EvaluationClaimRecord, in context order; no upstream validator call occurs",
      "prerequisite_and_suppression": "context container usable; repeat per non-exact EvaluationClaimRecord; invalid items excluded downstream"
    },
    {
      "code": "duplicate_context_claim_id",
      "condition_and_occurrence": "once for each later exact-type individually-valid context record repeating an earlier usable claim ID, in context order",
      "prerequisite_and_suppression": "exact-type context items with usable exact nonblank IDs; repeat for each later duplicate; duplicate IDs unusable for resolution"
    },
    {
      "code": "observed_claim_not_found",
      "condition_and_occurrence": "once per observed ID that does not resolve to exactly one usable context claim, in observed-ID order",
      "prerequisite_and_suppression": "observed ID tuple usable and context root usable; repeat for IDs not resolving exactly once"
    },
    {
      "code": "unexpected_context_claim",
      "condition_and_occurrence": "once per usable unique context claim ID absent from observed IDs, in context order",
      "prerequisite_and_suppression": "usable unique exact-type context claims and observed tuple usable; repeat in context order"
    },
    {
      "code": "claim_disposition_unusable",
      "condition_and_occurrence": "once per resolved usable claim whose disposition cannot participate in the fixed closed-set mapping, in observed-ID order",
      "prerequisite_and_suppression": "observed claim resolves exactly once; disposition-dependent component checks suppressed for that claim"
    },
    {
      "code": "claim_class_mismatch",
      "condition_and_occurrence": "once per resolved usable observed claim whose class differs from its positionally aligned observed class or required class, in observed-ID order",
      "prerequisite_and_suppression": "claim resolves exactly once and aligned observed/required class position is usable"
    },
    {
      "code": "candidate_identity_mismatch",
      "condition_and_occurrence": "once per resolved usable observed claim whose candidate ID or version differs, in observed-ID order",
      "prerequisite_and_suppression": "claim resolves exactly once and decision candidate ID/version texts are usable"
    },
    {
      "code": "representation_mismatch",
      "condition_and_occurrence": "once per resolved usable observed claim whose representation differs, in observed-ID order",
      "prerequisite_and_suppression": "claim resolves exactly once and decision representation is exact enum"
    },
    {
      "code": "split_scope_mismatch",
      "condition_and_occurrence": "once per resolved usable observed claim with any split ID/version, fold_scope, or cutoff_scope mismatch, in observed-ID order",
      "prerequisite_and_suppression": "claim resolves exactly once and each compared decision scope text is usable; one occurrence per claim for any mismatch"
    },
    {
      "code": "paired_record_set_mismatch",
      "condition_and_occurrence": "once per resolved usable observed claim with paired_test_record_set_id mismatch, in observed-ID order",
      "prerequisite_and_suppression": "claim resolves exactly once and decision paired-set text is usable"
    },
    {
      "code": "aggregation_weighting_mismatch",
      "condition_and_occurrence": "once per resolved usable observed claim whose aggregation or weighting identity differs from its required-position value, in observed-ID order",
      "prerequisite_and_suppression": "claim resolves exactly once and positional policy tuples/required position are usable"
    },
    {
      "code": "stratum_scope_mismatch",
      "condition_and_occurrence": "once per resolved usable observed claim whose nullable stratum differs from its required-position value or conditional scope, in observed-ID order",
      "prerequisite_and_suppression": "claim resolves exactly once and positional nullable stratum tuple/required position are usable"
    },
    {
      "code": "inherited_policy_mismatch",
      "condition_and_occurrence": "once per resolved usable observed claim per mismatching uncertainty, sample-support, selection-control, then multiple-comparison identity, in observed-ID then policy order",
      "prerequisite_and_suppression": "claim resolves exactly once and corresponding positional policy tuple/required position is usable; repeat by claim then policy order"
    },
    {
      "code": "provenance_traceability_mismatch",
      "condition_and_occurrence": "once per uniquely resolved observed claim, in observed-ID order, when its evaluation_claim_id is absent from usable decision provenance or its trusted claim provenance is not a multiplicity-preserving ordered subsequence of decision provenance; both failures for one claim produce one occurrence",
      "prerequisite_and_suppression": "exact fixed result_chain_traceability_posture, usable decision provenance, and unique exact claim resolution; suppress for malformed posture (INVALID_FIXED_POSTURE only), unusable provenance, or unusable claim, while continuing independently usable claims"
    },
    {
      "code": "cross_baseline_incomplete",
      "condition_and_occurrence": "once when usable aligned required classes lack the exact cross-baseline class or its upstream-complete climatology and persistence result chain",
      "prerequisite_and_suppression": "required/class alignment and relevant resolved claims are usable; suppress when missing/invalid prerequisites prevent coverage determination"
    },
    {
      "code": "calibration_requirement_mismatch",
      "condition_and_occurrence": "once when usable aligned required classes lack exactly the representation-selected calibration class or include a substituted calibration class",
      "prerequisite_and_suppression": "representation, required/class alignment, and relevant claims are usable"
    },
    {
      "code": "threshold_applicability_mismatch",
      "condition_and_occurrence": "once when threshold applicability, required class coverage, outcome, or post-hoc selection conflicts after usable applicability/class prerequisites",
      "prerequisite_and_suppression": "applicable subset, outcomes, required/class alignment, and relevant claims are usable"
    },
    {
      "code": "stratum_applicability_mismatch",
      "condition_and_occurrence": "once when stratum applicability, exact ordered strata/class coverage, outcome, omission, or pooling conflicts after usable prerequisites",
      "prerequisite_and_suppression": "applicable subset, outcomes, stratum alignment, and relevant claims are usable"
    },
    {
      "code": "no_lookahead_integrity_mismatch",
      "condition_and_occurrence": "exactly once when the exact fixed no-lookahead posture and usable integrity pair claim component_satisfied while an earlier gate-visible split/fold/cutoff, selection-control-policy, or provenance/traceability diagnostic contradicts that satisfied attestation; never emitted solely for trusted upstream publication/finality facts",
      "prerequisite_and_suppression": "exact fixed no_lookahead_review_posture and usable selection_scope_and_no_lookahead_integrity pair; malformed posture emits INVALID_FIXED_POSTURE only; suppress when pair unusable or outcome is not component_satisfied"
    },
    {
      "code": "component_outcome_mismatch",
      "condition_and_occurrence": "once per structurally decisive blocked/unavailable/insufficient incompatibility in canonical order, then once if supplied overall outcome conflicts with structural precedence; substantive satisfied/not_satisfied outcomes are not recalculated",
      "prerequisite_and_suppression": "six-pair outcomes, applicability, and structurally decisive claim dispositions are usable; validator checks precedence/compatibility, not substantive rule satisfaction"
    },
    {
      "code": "disposition_precedence_mismatch",
      "condition_and_occurrence": "once when supplied gate disposition differs from the fixed overall outcome/precedence mapping",
      "prerequisite_and_suppression": "exact disposition and usable overall outcome/structural precedence inputs; substantive passed/not-passed result is caller supplied"
    },
    {
      "code": "complete_rule_required",
      "condition_and_occurrence": "once when passed/not_passed is supplied without complete evaluable required claims, or when no fixed complete outcome can be derived but an evaluable disposition is supplied",
      "prerequisite_and_suppression": "passed/not_passed or evaluable overall outcome is supplied; required partition, resolution, and applicability prerequisites are usable enough to diagnose incompleteness"
    },
    {
      "code": "invalid_provenance",
      "condition_and_occurrence": "once per non-exact/nonblank provenance element after exact tuple prerequisite, in provenance order",
      "prerequisite_and_suppression": "provenance field is present and outer tuple usable; repeat per invalid element in order"
    },
    {
      "code": "empty_provenance",
      "condition_and_occurrence": "once when provenance is an exact empty tuple",
      "prerequisite_and_suppression": "provenance is an exact empty tuple; may coexist with no element-level invalid_provenance codes"
    },
    {
      "code": "invalid_decision_created_at",
      "condition_and_occurrence": "once when present timestamp fails exact offset-aware ISO-8601 grammar; blank/wrong-type text may also receive BLANK_REQUIRED_TEXT earlier",
      "prerequisite_and_suppression": "timestamp field is present; blank/wrong type may also emit earlier blank_required_text"
    },
    {
      "code": "self_supersession",
      "condition_and_occurrence": "once when usable supersession text equals usable evidence_gate_decision_id",
      "prerequisite_and_suppression": "decision ID and non-None supersession are usable exact nonblank strings"
    },
    {
      "code": "invalid_supersession_link",
      "condition_and_occurrence": "once when a present exact nonblank non-self supersession ID is absent from the usable provenance tuple; no prior-decision lookup, persistence, or registry is permitted",
      "prerequisite_and_suppression": "non-None supersession is usable, not self, and provenance outer tuple/elements are usable"
    }
  ],
  "claim_validation_trust_boundary": {
    "posture": "previously_validated_immutable_evaluation_claim_artifacts",
    "reason": "the merged validate_evaluation_claim_record signature also requires tuple[EvaluationResultRecord, ...], while this minimal evidence-gate API intentionally receives only claim context",
    "exact_behavior": "require exact EvaluationClaimRecord elements and validate every gate-visible field and cross-claim relationship frozen here; do not call validate_evaluation_claim_record and do not claim to independently prove upstream result-level validity",
    "caller_responsibility": "caller supplies claims previously accepted by the merged claim boundary together with immutable provenance/result-chain references recording that validation",
    "prohibited_expansion": "no EvaluationResultRecord context, result resolver, result loader, additional public function, or production-file scope is added"
  },
  "eligibility_posture_matrix": {
    "stage3_gate_passed": "eligible_for_later_separate_readiness_or_approval_request_only",
    "stage3_gate_not_passed": "not_eligible_for_implementation_handoff",
    "stage3_gate_insufficient": "not_eligible_for_implementation_handoff",
    "stage3_gate_blocked": "not_eligible_for_implementation_handoff",
    "stage3_gate_unavailable": "not_eligible_for_implementation_handoff"
  },
  "validation_group_code_matrix": [
    [
      "missing_keys",
      [
        "missing_required_field"
      ]
    ],
    [
      "unexpected_exact_string_keys",
      [
        "unexpected_field"
      ]
    ],
    [
      "unexpected_remaining_keys",
      [
        "unexpected_field"
      ]
    ],
    [
      "required_and_nullable_text",
      [
        "blank_required_text"
      ]
    ],
    [
      "gate_component_enum",
      [
        "invalid_gate_component"
      ]
    ],
    [
      "component_outcome_enum",
      [
        "invalid_component_outcome"
      ]
    ],
    [
      "gate_disposition_enum",
      [
        "invalid_gate_disposition"
      ]
    ],
    [
      "prediction_representation_enum",
      [
        "invalid_prediction_representation"
      ]
    ],
    [
      "claim_class_enum",
      [
        "invalid_claim_class"
      ]
    ],
    [
      "fixed_postures",
      [
        "invalid_fixed_posture"
      ]
    ],
    [
      "text_tuple_structure",
      [
        "invalid_text_tuple"
      ]
    ],
    [
      "claim_identity_tuple_structure",
      [
        "invalid_claim_id_tuple"
      ]
    ],
    [
      "claim_class_tuple_structure",
      [
        "invalid_claim_class_tuple"
      ]
    ],
    [
      "component_tuple_structure",
      [
        "invalid_component_tuple"
      ]
    ],
    [
      "component_outcome_tuple_structure",
      [
        "invalid_component_outcome_tuple"
      ]
    ],
    [
      "claim_set_partition",
      [
        "claim_set_partition_mismatch"
      ]
    ],
    [
      "claim_class_sequence",
      [
        "claim_class_sequence_mismatch"
      ]
    ],
    [
      "component_applicability",
      [
        "applicability_mismatch"
      ]
    ],
    [
      "claim_context_container",
      [
        "invalid_claim_record_container"
      ]
    ],
    [
      "individual_claim_validity",
      [
        "invalid_claim_record"
      ]
    ],
    [
      "context_identity_uniqueness",
      [
        "duplicate_context_claim_id"
      ]
    ],
    [
      "observed_claim_resolution",
      [
        "observed_claim_not_found"
      ]
    ],
    [
      "unexpected_context_claims",
      [
        "unexpected_context_claim"
      ]
    ],
    [
      "claim_disposition_compatibility",
      [
        "claim_disposition_unusable"
      ]
    ],
    [
      "claim_class_compatibility",
      [
        "claim_class_mismatch"
      ]
    ],
    [
      "candidate_identity_compatibility",
      [
        "candidate_identity_mismatch"
      ]
    ],
    [
      "representation_compatibility",
      [
        "representation_mismatch"
      ]
    ],
    [
      "split_fold_cutoff_compatibility",
      [
        "split_scope_mismatch"
      ]
    ],
    [
      "paired_record_set_compatibility",
      [
        "paired_record_set_mismatch"
      ]
    ],
    [
      "aggregation_weighting_compatibility",
      [
        "aggregation_weighting_mismatch"
      ]
    ],
    [
      "stratum_compatibility",
      [
        "stratum_scope_mismatch"
      ]
    ],
    [
      "inherited_policy_compatibility",
      [
        "inherited_policy_mismatch"
      ]
    ],
    [
      "provenance_result_chain_traceability",
      [
        "provenance_traceability_mismatch"
      ]
    ],
    [
      "cross_baseline_completeness",
      [
        "cross_baseline_incomplete"
      ]
    ],
    [
      "calibration_requirement",
      [
        "calibration_requirement_mismatch"
      ]
    ],
    [
      "threshold_applicability",
      [
        "threshold_applicability_mismatch"
      ]
    ],
    [
      "stratum_applicability",
      [
        "stratum_applicability_mismatch"
      ]
    ],
    [
      "no_lookahead_integrity",
      [
        "no_lookahead_integrity_mismatch"
      ]
    ],
    [
      "component_outcome_consistency",
      [
        "component_outcome_mismatch"
      ]
    ],
    [
      "disposition_precedence",
      [
        "disposition_precedence_mismatch"
      ]
    ],
    [
      "complete_rule_requirement",
      [
        "complete_rule_required"
      ]
    ],
    [
      "provenance",
      [
        "invalid_provenance",
        "empty_provenance"
      ]
    ],
    [
      "decision_created_timestamp",
      [
        "invalid_decision_created_at"
      ]
    ],
    [
      "self_supersession",
      [
        "self_supersession"
      ]
    ],
    [
      "supersession_link",
      [
        "invalid_supersession_link"
      ]
    ]
  ],
  "gate_visible_attestation_contract": {
    "upstream_trust": "result-level source availability, publication timing, finality, and no-lookahead correctness are trusted from previously validated immutable EvaluationClaimRecord artifacts and are not independently inspected or recalculated",
    "traceability_inputs": "only observed_evaluation_claim_ids, resolved exact EvaluationClaimRecord.evaluation_claim_id, each resolved claim provenance tuple, decision provenance tuple, and the exact fixed result_chain_traceability_posture are gate-visible traceability inputs",
    "ordered_subsequence_definition": "claim provenance is linked when it is an ordered subsequence of decision provenance using left-to-right equality with multiplicity preserved; every observed claim ID must also occur at least once in decision provenance",
    "traceability_mismatch": "after exact fixed traceability posture, usable decision provenance, and unique observed resolution, emit PROVENANCE_TRACEABILITY_MISMATCH once per observed claim, in observed-ID order, when its ID is absent from decision provenance or its provenance is not an ordered subsequence of decision provenance; combine both failures for one claim into one occurrence",
    "traceability_suppression": "INVALID_FIXED_POSTURE alone handles a malformed result_chain_traceability_posture; suppress traceability mismatch for that posture, unusable decision provenance, or an unresolved/duplicate/invalid claim, while continuing other independently usable claims",
    "no_lookahead_inputs": "only the exact fixed no_lookahead_review_posture, the selection_scope_and_no_lookahead_integrity outcome pair, and already-diagnosed gate-visible split/fold/cutoff, selection-control policy, and provenance/traceability consistency are inspected",
    "no_lookahead_mismatch": "after exact fixed no-lookahead posture and a usable integrity outcome pair, emit NO_LOOKAHEAD_INTEGRITY_MISMATCH exactly once when that outcome is component_satisfied while any SPLIT_SCOPE_MISMATCH, INHERITED_POLICY_MISMATCH attributable to selection_control_policy_ids, or PROVENANCE_TRACEABILITY_MISMATCH occurred; no code is emitted merely for trusted result-level publication/finality facts",
    "no_lookahead_suppression": "INVALID_FIXED_POSTURE alone handles malformed no_lookahead_review_posture; suppress NO_LOOKAHEAD_INTEGRITY_MISMATCH when that posture or integrity pair is unusable, and do not emit it when the integrity outcome is not component_satisfied",
    "code_separation": "INVALID_FIXED_POSTURE validates exact posture text; PROVENANCE_TRACEABILITY_MISMATCH validates observable claim/provenance linkage; NO_LOOKAHEAD_INTEGRITY_MISMATCH validates the satisfied-integrity attestation against already-diagnosed gate-visible contradictions; the same malformed posture is never assigned to more than one code"
  }
}
```

## Acceptance criteria

Acceptance requires exact static agreement with this frozen contract, the three-file current scope, the two-file future scope, all safety boundaries, independent literal oracles, mutation rejection, and a separate human decision before implementation.
