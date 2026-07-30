# WEATHER-BOT-STAGE3-EVALUATION-CLAIM-IMPLEMENTATION-APPROVAL-REQUEST-01

Canonical ID: WEATHER-BOT-STAGE3-EVALUATION-CLAIM-IMPLEMENTATION-APPROVAL-REQUEST-01

## Verdict and decision boundary

This is an approval-request-only, documentation/static-test change. Its current status is `request_prepared_implementation_not_approved`. It does not implement evaluation claims, create claim records, evaluate claim rules, generate dispositions, make an evidence-gate decision, or approve the later implementation. The ordered human decision options and every frozen contract detail are in the machine contract below.

## Predecessor and exact base

`ACTUAL_PR_376_MERGE_SHA = e20f6d6755188043c50bfbd00c003f8200ef2d1a` and `BASE_SHA = e20f6d6755188043c50bfbd00c003f8200ef2d1a`. The actual commit is a two-parent merge. Approved head `b53a379b0aadfa9c76ec3f624c93ef68dade66f5` is its second parent and therefore its ancestor; the merge commit is the exact current-main base from which this branch was created. No preview merge SHA is used.

## Authority and requested future scope

The merged evaluation-claim planning artifact remains authoritative for the eight classes, five dispositions, 34 semantic fields, predeclaration, complete result sets, precedence, immutability, evidence-gate separation, fail-closed behavior, and non-approvals. The merged evaluation-result record, scoring/diagnostics, and baseline contracts and their focused tests define the referenced types and compatibility vocabulary.

Only after separate human approval may a later ticket create the two `future_files` in the machine contract, modifying no existing file. That future slice is limited to immutable caller-supplied claim records, deterministic mapping adaptation, pure validation against immutable evaluation-result records, and fail-closed disposition/scope consistency. It may not calculate results, metrics, diagnostics, comparisons, uncertainty, rule satisfaction, or dispositions; select or alter rules; decide an evidence gate; approve anything; persist; or report.

## Frozen API, records, and adaptation

Every enum is a `StrEnum`; both records are `@dataclass(frozen=True)`. The public surface, allowed imports, enum members/values, exact annotations, field order/defaults, and signatures are frozen structurally below. Imported result/scoring/baseline names are not re-exported. No collection validator, evaluator, registry, loader, or persistence helper is approved. No field is generated. `EvaluationClaimRecord.__post_init__` performs no validation, normalization, rule evaluation, or disposition calculation.

The adapter accepts only exact members or exact built-in matching strings for its four enum fields. It rejects string subclasses, unrelated enums, invalid strings, and other values. It adapts actual lists only for the six declared tuple fields and may adapt an actual list containing only exact evaluation-result records for context. Direct validation requires exact tuples and performs no adaptation. Caller inputs are never mutated.

Readable keys count only when `type(key) is str`. Nullable fields among the first 33 remain required and only supersession is optional. Shape failures aggregate and do not return early. Duplicate keys of any type, or any ordinary exception during snapshot, duplicate detection, hashing, unpacking, value snapshotting, or materialization, make the root unreadable and produce exactly the declared 33 missing-field codes. Catch `Exception`, not `BaseException`; never return a partial record.

## Text, tuples, timestamp, and provenance

Required and nullable text uses exact built-in, nonblank strings without stripping or rewriting. Target posture is exactly `venue_defined_settlement_outcome`. Text-invalid timestamps receive both `BLANK_REQUIRED_TEXT` and later `INVALID_CLAIM_CREATED_AT`; timestamps are never compared with the clock or rewritten. Tuple entries use exact nonblank built-in strings, preserve order, reject tuple subclasses/arbitrary iterables, and obey the exact uniqueness and partition rules below.

Provenance accepts exact tuple/list in mapping adaptation and exact tuple in direct validation. It preserves valid order and duplicates. It never resolves, fetches, sorts, generates, or deduplicates. Supersession corrections require a new identity and explicit link.

## Result context, class matrix, and compatibility

Context records must be exact, immutable, individually valid evaluation-result records with unique identities. Observed identities resolve exactly once. Extra records are permitted solely when an observed exact paired payload directly references them. Nothing is fetched, generated, repaired, recalculated, substituted, averaged, voted, or used as fallback.

Every observed result must match all declared compatibility fields. Its ordered unique artifact/version sequence in observed-ID order must exactly equal the two metric identity tuples. Paired candidate/baseline references must resolve and preserve candidate identity, applicable approved baseline identity/type, and exact compatible scope. No paired comparison is calculated or recomputed.

The class matrix below is exact. Cross-baseline evidence includes both climatology and persistence without omission. Calibration classes preserve their exact representation and allowed result kinds. Threshold-weighted evidence uses only threshold-weighted CRPS in its declared scope. Stratum evidence preserves one exact declared stratum.

## Disposition and evidence-gate separation

Precedence is machine-checkable and ordered. Supported/not-supported merely validates structural eligibility of a caller-supplied disposition after complete supported evidence; the validator never decides whether a rule is substantively satisfied. A blocked disposition may represent another predeclared contract failure stated in its nonblank reason. Evidence-gate posture must match the exact disposition matrix. A supported claim does not pass an evidence gate.

Multiplicity policy is required for every declared trigger and otherwise may be null or valid nonblank text; the validator neither selects nor interprets a method. No numeric alpha, confidence level, sample minimum, effect threshold, tolerance, correction threshold, bin count, resampling length, or weighting constant is prescribed.

## Exact validation behavior

Validation aggregates every diagnosable present-value failure, suppressing only checks whose prerequisites are absent or unusable. The 38-code `StrEnum` and 38 group order are closed and exact. Repeated codes remain repeated; codes are neither sorted nor deduplicated. Empty codes force passed/true and nonempty codes force blocked/false. No partial claim record is returned.

## Safety, routing, and non-goals

All explicit non-goals in the machine contract are denied. This request changes no production module and creates no runtime schema or behavior. It leaves Phase 0A shared rails and both jobs unchanged and leaves Phase 0B DuckDB/Parquet historical-research boundaries unchanged. Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`; market&#95;id is non-routing, and `token_outcome_pair` is derived only. It does not approve connectors, paper trading, trading, order placement, orchestration, autonomy, or production behavior.

## Machine contract

The following JSON is the sole machine-assignment block. Order is significant for every array.

```json
{
  "title": "WEATHER-BOT-STAGE3-EVALUATION-CLAIM-IMPLEMENTATION-APPROVAL-REQUEST-01",
  "canonical_id": "WEATHER-BOT-STAGE3-EVALUATION-CLAIM-IMPLEMENTATION-APPROVAL-REQUEST-01",
  "actual_pr_376_merge_sha": "e20f6d6755188043c50bfbd00c003f8200ef2d1a",
  "base_sha": "e20f6d6755188043c50bfbd00c003f8200ef2d1a",
  "approved_pr_376_head": "b53a379b0aadfa9c76ec3f624c93ef68dade66f5",
  "pr_files": [
    "docs/prd/WEATHER-BOT-STAGE3-EVALUATION-CLAIM-IMPLEMENTATION-APPROVAL-REQUEST-01.md",
    "tests/core/test_weather_bot_stage3_evaluation_claim_implementation_approval_request_01.py",
    "tests/core/canonical_id_allowlist.py"
  ],
  "future_files": [
    "meg/weather/stage3/evaluation_claim.py",
    "tests/core/test_weather_bot_stage3_evaluation_claim.py"
  ],
  "public_symbols": [
    "EvaluationClaimClass",
    "EvaluationClaimDisposition",
    "EvaluationClaimValidationSeverity",
    "EvaluationClaimValidationCode",
    "EvaluationClaimRecord",
    "EvaluationClaimValidationResult",
    "evaluation_claim_record_from_mapping",
    "validate_evaluation_claim_record"
  ],
  "permitted_imports": [
    "BaselineType",
    "ScoringArtifact",
    "ScoringPredictionRepresentation",
    "EvaluationResultKind",
    "EvaluationResultSupportStatus",
    "EvaluationResultMethodRole",
    "EvaluationResultRecord",
    "EvaluationResultValidationResult",
    "PairedComparisonResultPayload",
    "validate_evaluation_result_record"
  ],
  "enums": {
    "EvaluationClaimClass": [
      [
        "CANDIDATE_VS_CLIMATOLOGY_PREDICTIVE_SKILL",
        "candidate_vs_climatology_predictive_skill"
      ],
      [
        "CANDIDATE_VS_PERSISTENCE_PREDICTIVE_SKILL",
        "candidate_vs_persistence_predictive_skill"
      ],
      [
        "CANDIDATE_PREDICTIVE_SKILL_ACROSS_REQUIRED_BASELINES",
        "candidate_predictive_skill_across_required_baselines"
      ],
      [
        "BINARY_CALIBRATION_BEHAVIOR",
        "binary_calibration_behavior"
      ],
      [
        "DISTRIBUTIONAL_CALIBRATION_BEHAVIOR",
        "distributional_calibration_behavior"
      ],
      [
        "ENSEMBLE_CALIBRATION_BEHAVIOR",
        "ensemble_calibration_behavior"
      ],
      [
        "THRESHOLD_WEIGHTED_DISTRIBUTION_SKILL",
        "threshold_weighted_distribution_skill"
      ],
      [
        "STRATUM_SPECIFIC_PREDICTIVE_SKILL",
        "stratum_specific_predictive_skill"
      ]
    ],
    "EvaluationClaimDisposition": [
      [
        "CLAIM_SUPPORTED",
        "claim_supported"
      ],
      [
        "CLAIM_NOT_SUPPORTED",
        "claim_not_supported"
      ],
      [
        "CLAIM_INSUFFICIENT",
        "claim_insufficient"
      ],
      [
        "CLAIM_BLOCKED",
        "claim_blocked"
      ],
      [
        "CLAIM_UNAVAILABLE",
        "claim_unavailable"
      ]
    ],
    "EvaluationClaimValidationSeverity": [
      [
        "PASSED",
        "passed"
      ],
      [
        "BLOCKED",
        "blocked"
      ]
    ],
    "EvaluationClaimValidationCode": [
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
        "INVALID_CLAIM_CLASS",
        "invalid_claim_class"
      ],
      [
        "INVALID_CLAIM_DISPOSITION",
        "invalid_claim_disposition"
      ],
      [
        "INVALID_BASELINE_TYPE",
        "invalid_baseline_type"
      ],
      [
        "INVALID_PREDICTION_REPRESENTATION",
        "invalid_prediction_representation"
      ],
      [
        "INVALID_FIXED_POSTURE",
        "invalid_fixed_posture"
      ],
      [
        "INVALID_EVIDENCE_GATE_POSTURE",
        "invalid_evidence_gate_posture"
      ],
      [
        "INVALID_METRIC_IDENTITY_TUPLE",
        "invalid_metric_identity_tuple"
      ],
      [
        "METRIC_VERSION_LENGTH_MISMATCH",
        "metric_version_length_mismatch"
      ],
      [
        "INVALID_REQUIRED_RESULT_IDS",
        "invalid_required_result_ids"
      ],
      [
        "INVALID_OBSERVED_RESULT_IDS",
        "invalid_observed_result_ids"
      ],
      [
        "INVALID_MISSING_RESULT_IDS",
        "invalid_missing_result_ids"
      ],
      [
        "RESULT_SET_PARTITION_MISMATCH",
        "result_set_partition_mismatch"
      ],
      [
        "INVALID_RESULT_RECORD_CONTAINER",
        "invalid_result_record_container"
      ],
      [
        "INVALID_RESULT_RECORD",
        "invalid_result_record"
      ],
      [
        "DUPLICATE_CONTEXT_RESULT_ID",
        "duplicate_context_result_id"
      ],
      [
        "OBSERVED_RESULT_NOT_FOUND",
        "observed_result_not_found"
      ],
      [
        "UNEXPECTED_CONTEXT_RESULT",
        "unexpected_context_result"
      ],
      [
        "PAIRED_REFERENCE_NOT_FOUND",
        "paired_reference_not_found"
      ],
      [
        "RESULT_TARGET_MISMATCH",
        "result_target_mismatch"
      ],
      [
        "RESULT_REPRESENTATION_MISMATCH",
        "result_representation_mismatch"
      ],
      [
        "RESULT_SCOPE_MISMATCH",
        "result_scope_mismatch"
      ],
      [
        "RESULT_METRIC_MISMATCH",
        "result_metric_mismatch"
      ],
      [
        "CANDIDATE_IDENTITY_MISMATCH",
        "candidate_identity_mismatch"
      ],
      [
        "BASELINE_IDENTITY_MISMATCH",
        "baseline_identity_mismatch"
      ],
      [
        "RESULT_KIND_NOT_ALLOWED",
        "result_kind_not_allowed"
      ],
      [
        "BASELINE_REQUIREMENT_MISMATCH",
        "baseline_requirement_mismatch"
      ],
      [
        "CROSS_BASELINE_INCOMPLETE",
        "cross_baseline_incomplete"
      ],
      [
        "STRATUM_REQUIREMENT_MISMATCH",
        "stratum_requirement_mismatch"
      ],
      [
        "DISPOSITION_PRECEDENCE_MISMATCH",
        "disposition_precedence_mismatch"
      ],
      [
        "SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT",
        "supported_or_not_supported_without_complete_support"
      ],
      [
        "INVALID_MULTIPLE_COMPARISON_POSTURE",
        "invalid_multiple_comparison_posture"
      ],
      [
        "EMPTY_PROVENANCE",
        "empty_provenance"
      ],
      [
        "INVALID_PROVENANCE_REF",
        "invalid_provenance_ref"
      ],
      [
        "INVALID_CLAIM_CREATED_AT",
        "invalid_claim_created_at"
      ],
      [
        "SELF_SUPERSESSION",
        "self_supersession"
      ]
    ]
  },
  "record_fields": [
    [
      "evaluation_claim_id",
      "str",
      null
    ],
    [
      "claim_class",
      "EvaluationClaimClass",
      null
    ],
    [
      "claim_rule_id",
      "str",
      null
    ],
    [
      "claim_rule_version",
      "str",
      null
    ],
    [
      "claim_disposition",
      "EvaluationClaimDisposition",
      null
    ],
    [
      "claim_disposition_reason",
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
      "baseline_type_when_applicable",
      "BaselineType | None",
      null
    ],
    [
      "baseline_method_id_when_applicable",
      "str | None",
      null
    ],
    [
      "baseline_method_version_when_applicable",
      "str | None",
      null
    ],
    [
      "prediction_representation",
      "ScoringPredictionRepresentation",
      null
    ],
    [
      "metric_or_diagnostic_ids",
      "tuple[str, ...]",
      null
    ],
    [
      "metric_or_diagnostic_versions",
      "tuple[str, ...]",
      null
    ],
    [
      "required_evaluation_result_ids",
      "tuple[str, ...]",
      null
    ],
    [
      "observed_evaluation_result_ids",
      "tuple[str, ...]",
      null
    ],
    [
      "missing_evaluation_result_ids",
      "tuple[str, ...]",
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
      "aggregation_rule_id",
      "str",
      null
    ],
    [
      "weighting_rule_id",
      "str",
      null
    ],
    [
      "stratum_id_when_applicable",
      "str | None",
      null
    ],
    [
      "uncertainty_policy_id",
      "str",
      null
    ],
    [
      "sample_support_rule_id",
      "str",
      null
    ],
    [
      "selection_control_policy_id",
      "str",
      null
    ],
    [
      "multiple_comparison_policy_id_when_applicable",
      "str | None",
      null
    ],
    [
      "evidence_gate_eligibility_posture",
      "str",
      null
    ],
    [
      "provenance",
      "tuple[str, ...]",
      null
    ],
    [
      "claim_created_at",
      "str",
      null
    ],
    [
      "supersedes_claim_id_when_applicable",
      "str | None",
      "None"
    ]
  ],
  "validation_result_fields": [
    [
      "severity",
      "EvaluationClaimValidationSeverity",
      null
    ],
    [
      "passed",
      "bool",
      null
    ],
    [
      "codes",
      "tuple[EvaluationClaimValidationCode, ...]",
      "()"
    ]
  ],
  "signatures": {
    "adapter": "def evaluation_claim_record_from_mapping(\n    mapping: object,\n    result_records: object,\n) -> tuple[\n    EvaluationClaimRecord | None,\n    EvaluationClaimValidationResult,\n]:",
    "validator": "def validate_evaluation_claim_record(\n    record: EvaluationClaimRecord,\n    result_records: tuple[EvaluationResultRecord, ...],\n) -> EvaluationClaimValidationResult:"
  },
  "required_mapping_keys": [
    "evaluation_claim_id",
    "claim_class",
    "claim_rule_id",
    "claim_rule_version",
    "claim_disposition",
    "claim_disposition_reason",
    "target_posture",
    "candidate_method_id",
    "candidate_method_version",
    "baseline_type_when_applicable",
    "baseline_method_id_when_applicable",
    "baseline_method_version_when_applicable",
    "prediction_representation",
    "metric_or_diagnostic_ids",
    "metric_or_diagnostic_versions",
    "required_evaluation_result_ids",
    "observed_evaluation_result_ids",
    "missing_evaluation_result_ids",
    "split_id",
    "split_version",
    "fold_scope",
    "cutoff_scope",
    "paired_test_record_set_id",
    "aggregation_rule_id",
    "weighting_rule_id",
    "stratum_id_when_applicable",
    "uncertainty_policy_id",
    "sample_support_rule_id",
    "selection_control_policy_id",
    "multiple_comparison_policy_id_when_applicable",
    "evidence_gate_eligibility_posture",
    "provenance",
    "claim_created_at"
  ],
  "optional_mapping_keys": [
    "supersedes_claim_id_when_applicable"
  ],
  "list_to_tuple_fields": [
    "metric_or_diagnostic_ids",
    "metric_or_diagnostic_versions",
    "required_evaluation_result_ids",
    "observed_evaluation_result_ids",
    "missing_evaluation_result_ids",
    "provenance"
  ],
  "result_context_list_adaptation": "actual list of exact EvaluationResultRecord objects only",
  "required_text": [
    "evaluation_claim_id",
    "claim_rule_id",
    "claim_rule_version",
    "claim_disposition_reason",
    "target_posture",
    "candidate_method_id",
    "candidate_method_version",
    "split_id",
    "split_version",
    "fold_scope",
    "cutoff_scope",
    "paired_test_record_set_id",
    "aggregation_rule_id",
    "weighting_rule_id",
    "uncertainty_policy_id",
    "sample_support_rule_id",
    "selection_control_policy_id",
    "evidence_gate_eligibility_posture",
    "claim_created_at"
  ],
  "nullable_text": [
    "baseline_method_id_when_applicable",
    "baseline_method_version_when_applicable",
    "stratum_id_when_applicable",
    "multiple_comparison_policy_id_when_applicable",
    "supersedes_claim_id_when_applicable"
  ],
  "fixed_target_posture": "venue_defined_settlement_outcome",
  "class_matrix": {
    "candidate_vs_climatology_predictive_skill": [
      "paired_comparison_result_only",
      "paired_baseline_climatology",
      "claim_baseline_climatology",
      "nonblank_baseline_method_identity_and_version",
      "exact_candidate_and_baseline_references"
    ],
    "candidate_vs_persistence_predictive_skill": [
      "paired_comparison_result_only",
      "paired_baseline_persistence",
      "claim_baseline_persistence",
      "nonblank_baseline_method_identity_and_version",
      "exact_candidate_and_baseline_references"
    ],
    "candidate_predictive_skill_across_required_baselines": [
      "paired_comparison_result_only",
      "at_least_one_climatology",
      "at_least_one_persistence",
      "no_silent_baseline_omission",
      "claim_baseline_fields_none",
      "compatible_candidate_identity_and_exact_scope"
    ],
    "binary_calibration_behavior": [
      "binary_outcome_probability",
      "at_least_one_calibration_bin_result",
      "at_least_one_scalar_score_or_decomposition_result",
      "no_other_result_kind",
      "claim_baseline_fields_none"
    ],
    "distributional_calibration_behavior": [
      "full_predictive_distribution",
      "at_least_one_distribution_diagnostic_result",
      "at_least_one_scalar_score_result",
      "no_other_result_kind",
      "claim_baseline_fields_none"
    ],
    "ensemble_calibration_behavior": [
      "finite_comparable_ensemble",
      "at_least_one_ensemble_diagnostic_result",
      "no_incompatible_result_kind",
      "claim_baseline_fields_none"
    ],
    "threshold_weighted_distribution_skill": [
      "paired_comparison_result_only",
      "artifact_threshold_weighted_crps_only",
      "claim_baseline_climatology_or_persistence",
      "matching_baseline_method_identity_and_version",
      "exact_threshold_focused_scope"
    ],
    "stratum_specific_predictive_skill": [
      "paired_comparison_result_only",
      "nonnull_valid_stratum",
      "claim_baseline_climatology_or_persistence",
      "matching_baseline_method_identity_and_version",
      "exact_declared_stratum_preserved"
    ]
  },
  "compatibility_fields": [
    "target_posture",
    "prediction_representation",
    "split_id_and_version",
    "fold_scope",
    "cutoff_scope",
    "paired_test_record_set_id",
    "aggregation_rule_id",
    "weighting_rule_id",
    "applicable_stratum"
  ],
  "result_context_requirements": [
    "direct_exact_tuple",
    "exact_EvaluationResultRecord_items",
    "reject_record_and_payload_subclasses",
    "each_result_passes_validator",
    "unique_context_result_ids",
    "each_observed_id_resolves_exactly_once",
    "extras_only_if_direct_paired_candidate_or_baseline_reference",
    "no_fetch_generate_repair_recalculate_or_substitute"
  ],
  "disposition_precedence": [
    "blocked_consumed_result_requires_claim_blocked",
    "otherwise_missing_or_unavailable_requires_claim_unavailable_unless_independent_block",
    "otherwise_insufficient_requires_claim_insufficient_unless_blocked",
    "supported_or_not_supported_only_with_complete_all_supported_structurally_valid_evidence"
  ],
  "evidence_gate_matrix": {
    "claim_supported": "eligible_for_later_evidence_gate_decision_only",
    "claim_not_supported": "claim_support_absent",
    "claim_insufficient": "evidence_gate_use_blocked",
    "claim_blocked": "evidence_gate_use_blocked",
    "claim_unavailable": "no_substitution_or_evidence_gate_use"
  },
  "multiplicity_triggers": [
    "more_than_one_metric_or_diagnostic_identity",
    "candidate_predictive_skill_across_required_baselines",
    "stratum_specific_predictive_skill"
  ],
  "provenance_rules": [
    "wrong_container_one_INVALID_PROVENANCE_REF",
    "empty_accepted_container_one_EMPTY_PROVENANCE",
    "malformed_entry_one_INVALID_PROVENANCE_REF_in_order",
    "valid_duplicates_allowed_and_preserved",
    "empty_and_malformed_codes_mutually_exclusive",
    "no_resolve_fetch_sort_generate_or_deduplicate"
  ],
  "timestamp_procedure": [
    "exact_builtin_str",
    "contains_T_separator",
    "terminal_Z_converts_to_plus_00_00_for_parsing_only",
    "otherwise_explicit_terminal_numeric_offset",
    "datetime_fromisoformat",
    "non_none_utc_offset"
  ],
  "validation_codes": [
    "MISSING_REQUIRED_FIELD",
    "UNEXPECTED_FIELD",
    "BLANK_REQUIRED_TEXT",
    "INVALID_CLAIM_CLASS",
    "INVALID_CLAIM_DISPOSITION",
    "INVALID_BASELINE_TYPE",
    "INVALID_PREDICTION_REPRESENTATION",
    "INVALID_FIXED_POSTURE",
    "INVALID_EVIDENCE_GATE_POSTURE",
    "INVALID_METRIC_IDENTITY_TUPLE",
    "METRIC_VERSION_LENGTH_MISMATCH",
    "INVALID_REQUIRED_RESULT_IDS",
    "INVALID_OBSERVED_RESULT_IDS",
    "INVALID_MISSING_RESULT_IDS",
    "RESULT_SET_PARTITION_MISMATCH",
    "INVALID_RESULT_RECORD_CONTAINER",
    "INVALID_RESULT_RECORD",
    "DUPLICATE_CONTEXT_RESULT_ID",
    "OBSERVED_RESULT_NOT_FOUND",
    "UNEXPECTED_CONTEXT_RESULT",
    "PAIRED_REFERENCE_NOT_FOUND",
    "RESULT_TARGET_MISMATCH",
    "RESULT_REPRESENTATION_MISMATCH",
    "RESULT_SCOPE_MISMATCH",
    "RESULT_METRIC_MISMATCH",
    "CANDIDATE_IDENTITY_MISMATCH",
    "BASELINE_IDENTITY_MISMATCH",
    "RESULT_KIND_NOT_ALLOWED",
    "BASELINE_REQUIREMENT_MISMATCH",
    "CROSS_BASELINE_INCOMPLETE",
    "STRATUM_REQUIREMENT_MISMATCH",
    "DISPOSITION_PRECEDENCE_MISMATCH",
    "SUPPORTED_OR_NOT_SUPPORTED_WITHOUT_COMPLETE_SUPPORT",
    "INVALID_MULTIPLE_COMPARISON_POSTURE",
    "EMPTY_PROVENANCE",
    "INVALID_PROVENANCE_REF",
    "INVALID_CLAIM_CREATED_AT",
    "SELF_SUPERSESSION"
  ],
  "validation_groups": [
    "missing_keys",
    "unexpected_exact_string_keys",
    "unexpected_remaining_keys",
    "required_and_nullable_text",
    "claim_class",
    "claim_disposition",
    "baseline_type",
    "prediction_representation",
    "fixed_target_posture",
    "metric_tuple_structure",
    "metric_version_alignment",
    "required_result_tuple",
    "observed_result_tuple",
    "missing_result_tuple",
    "result_set_partition",
    "result_record_container",
    "individual_result_record_validity",
    "context_identity_uniqueness",
    "observed_result_resolution",
    "unexpected_context",
    "paired_reference_resolution",
    "target_compatibility",
    "representation_compatibility",
    "scope_compatibility",
    "metric_compatibility",
    "candidate_identity",
    "baseline_identity",
    "claim_class_result_kind_compatibility",
    "baseline_requirements",
    "cross_baseline_completeness",
    "stratum_requirements",
    "disposition_precedence",
    "supported_not_supported_completeness",
    "evidence_gate_posture",
    "multiplicity_posture",
    "provenance",
    "claim_created_timestamp",
    "self_supersession"
  ],
  "decision_options": [
    "approve_later_evaluation_claim_implementation_ticket",
    "request_approval_request_revision",
    "hold",
    "block"
  ],
  "current_status": "request_prepared_implementation_not_approved",
  "next_ticket": "WEATHER-BOT-STAGE3-EVALUATION-CLAIM-IMPLEMENTATION-01",
  "machine_assignments": {
    "ticket_kind": "approval_request_only",
    "implementation_approval": "not_approved",
    "claim_record_creation": "not_approved",
    "claim_rule_evaluation": "not_approved",
    "evidence_gate_decision": "not_approved",
    "phase_0a": "shared_rail_infrastructure_unchanged",
    "phase_0a_job_1": "unchanged",
    "phase_0a_job_2": "unchanged",
    "phase_0b": "duckdb_parquet_historical_research_unchanged",
    "canonical_routing_fields": [
      "condition_id",
      "token_id",
      "outcome"
    ],
    "non_routing_field": "market\u005fid",
    "derived_identifier": "token_outcome_pair"
  },
  "non_goals": [
    "result_calculation",
    "score_or_diagnostic_calculation",
    "comparison_calculation",
    "uncertainty_calculation",
    "claim_rule_selection",
    "claim_rule_evaluation",
    "claim_disposition_generation",
    "evidence_gate_evaluation",
    "evidence_gate_passage",
    "implementation_approval",
    "probability_generation",
    "label_joining",
    "split_or_baseline_execution",
    "model_training_or_calibration",
    "data_acquisition",
    "source_fetching",
    "provider_connectors",
    "runtime_schemas",
    "serialization",
    "persistence",
    "database_tables_or_migrations",
    "reports_or_exports",
    "backtesting_or_simulation",
    "market_price_comparison_execution",
    "economic_edge_findings",
    "executability_findings",
    "paper_trading",
    "trading",
    "order_placement",
    "orchestration",
    "autonomy",
    "production_behavior"
  ],
  "numeric_policy": "no_numeric_alpha_confidence_sample_effect_tolerance_correction_bin_resampling_or_weight_constants",
  "mapping_root_failure": {
    "record": null,
    "severity": "blocked",
    "codes": [
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD",
      "MISSING_REQUIRED_FIELD"
    ],
    "catch": "Exception_not_BaseException"
  },
  "validation_result_invariant": {
    "empty_codes": [
      "passed",
      true
    ],
    "nonempty_codes": [
      "blocked",
      false
    ],
    "repeated_codes": "preserved"
  },
  "shape_order": [
    "missing_required_in_field_order",
    "unexpected_exact_builtin_strings_lexical",
    "remaining_keys_mapping_iteration_order"
  ],
  "tuple_partition_rules": [
    "metric_ids_nonempty_unique",
    "metric_versions_nonempty_same_length",
    "required_ids_nonempty_unique",
    "observed_and_missing_each_unique",
    "subsets_disjoint_required_order_exact_partition"
  ],
  "supersession": "SELF_SUPERSESSION_once_only_for_two_valid_equal_exact_nonblank_ids",
  "public_non_exports": [
    "permitted_imports",
    "collection_validator",
    "claim_evaluator",
    "evidence_gate_evaluator",
    "claim_rule_registry",
    "result_loader",
    "persistence_helper"
  ]
}
```

## Acceptance and later ticket boundary

Acceptance requires exact three-file PR scope, deterministic standard-library-only static validation, independent literal oracles, mutation rejection, clean focused/full tests, and unchanged production files. This document is a request, not human approval. The next ticket may be `WEATHER-BOT-STAGE3-EVALUATION-CLAIM-IMPLEMENTATION-01` only after a separate human selects the approval option; otherwise revise, hold, or block in the declared order. Do not merge or enable auto-merge on this request.
