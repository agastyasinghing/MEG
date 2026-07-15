# WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-CONTRACT-PLANNING-01

Canonical ID: WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-CONTRACT-PLANNING-01

## Status and scope


Status: docs_static_test_only and contract_planning_only. This artifact defines requirements only for future immutable Weather Bot Stage 3 evaluation result records and creates no runtime behavior.

## Immediate predecessor and merge verification


Immediate predecessor: pr_362. ACTUAL_PR_362_MERGE_SHA: 1073494197c5c2e527ee1e8c5b2b66a2dfbb96e6. Local history shows this is a two-parent GitHub merge commit on current main, not preview merge SHA d33a247d730b3358be92d2fc0e983a34aabecc3b. No newer controlling Weather Bot state supersedes PR #362 for this scope.

## Contract purpose and result boundary


An evaluation result record is an immutable audit artifact describing one future score, diagnostic, diagnostic component, or paired comparison under one exact evaluation scope.

A result record is not a probability record, split definition, baseline definition, evaluation implementation, report, claim approval, evidence-gate passage, or trading approval. The target remains the venue-defined settlement outcome, not generic weather. Result applicability is inherited from the scoring-and-diagnostics contract. Result records must link to compatible upstream probability-record, label, split, baseline, metric, and diagnostic definitions. Unknown, incomplete, incompatible, unpaired, unsupported, or provenance-deficient results fail closed.

## Upstream contract dependencies


Compatible upstream dependencies are the Weather Bot PRD, research validation packet, readiness inventory, retrospective scoring requirements, probability-record contract, strict OOS split contract, baseline contracts, and scoring-and-diagnostics contract. Definitions and versions must match before any future result is accepted.

## Exact evaluation result-kind matrix


| Result kind | Applies to | Required result content | Required linkage | Fail-closed boundary |
| --- | --- | --- | --- | --- |
| scalar_score_result | brier_score, log_score, crps, threshold_weighted_crps | one metric identity and version, one result value, direction, sample accounting, and uncertainty or support posture as applicable | method role and version, representation, split, fold, cutoff, paired test-record set, aggregation, weighting, and stratum | block when applicability, result domain, linkage, provenance, or sample accounting is invalid |
| calibration_bin_result | reliability_diagram | ordered predeclared bin identity, boundary policy, sample count, mean predicted probability, observed outcome frequency, and uncertainty or support status | reliability definition and version, method identity, split scope, paired test-record set, aggregation, weighting, and stratum | block when bin policy, ordering, compatible support, or required linkage is absent |
| decomposition_result | brier_decomposition | declared decomposition method and component values for reliability, resolution, and uncertainty with sample accounting | decomposition definition and version, method identity, binary representation, split scope, paired test-record set, aggregation, weighting, and stratum | block when the decomposition method, representation, support, or linkage is incompatible |
| distribution_diagnostic_result | pit_histogram | declared PIT treatment, ordered bin definitions and counts, sample accounting, and uncertainty or support status | PIT definition and version, full-distribution representation, method identity, split scope, paired test-record set, aggregation, weighting, and stratum | block when PIT treatment, representation, ordered content, support, or linkage is incompatible |
| ensemble_diagnostic_result | rank_histogram | declared tie treatment, ordered ranks or bins and counts, ensemble comparability, sample accounting, and uncertainty or support status | rank-histogram definition and version, ensemble representation, method identity, split scope, paired test-record set, aggregation, weighting, and stratum | block when members, tie treatment, ordered content, support, or linkage are incompatible |
| paired_comparison_result | candidate versus climatology or persistence under one applicable proper score | candidate result identity, baseline result identity, comparison direction, paired comparison payload, and shared sample accounting | the same metric and version, representation, split, fold, cutoff, paired test-record set, aggregation, weighting, and stratum | block when the scope is not exactly paired or the baseline and scoring contracts are not satisfied |

## Exact result-support status matrix


| Support status | Required meaning | Claim posture |
| --- | --- | --- |
| supported | the result satisfies its upstream contracts and its predeclared sample-support rule | eligible only for later claim review; no claim is approved here |
| insufficient | the result is otherwise contract-compatible but does not satisfy its predeclared sample-support rule | claim use is blocked |
| blocked | a contract, compatibility, leakage, pairing, accounting, immutability, or provenance requirement failed | result is invalid for claims |
| unavailable | a required permitted input or result artifact does not exist | no substitution, backfill, inference, or claim is allowed |

No custom, hybrid, or additional support status is allowed.

## Common result-record requirements


Include exactly this ordered semantic-field list:

- evaluation_result_id
- result_kind
- artifact_id
- artifact_version
- evaluation_definition_id
- evaluation_definition_version
- evaluation_run_id
- method_role
- method_id
- method_version
- prediction_representation
- target_posture
- split_id
- split_version
- fold_id
- cutoff_identity
- paired_test_record_set_id
- eligibility_policy_id
- aggregation_rule_id
- weighting_rule_id
- stratum_id
- eligible_record_count
- excluded_record_count
- blocked_record_count
- total_considered_record_count
- exclusion_block_reason_summary
- uncertainty_method_id
- uncertainty_level_id
- support_status
- result_payload
- provenance
- result_created_at
- supersedes_result_id_when_applicable

These are future semantic requirements only.

This ticket must not create a dataclass, runtime schema, serialization implementation, database table, migration, SQL, JSON schema, Pydantic model, persistence adapter, or API contract.

## Scalar score result requirements


Scalar score results must preserve applicable score identity and version; result direction; result-domain validation posture; common scope; sample accounting; uncertainty or support posture; and no inferred economic meaning.

## Calibration and decomposition result requirements


Calibration and decomposition results must preserve ordered component or bin identity; all applicable policies and versions; counts and support status; no silent bin pooling; and no scalar-ranking substitution.

## Distribution and ensemble diagnostic result requirements


Distribution and ensemble diagnostic results must preserve ordered payload identity; representation compatibility; PIT or tie treatment; sample accounting; and no scalar-ranking substitution.

## Paired comparison result requirements


Paired comparison results must preserve candidate result identity; baseline result identity; baseline type; identical paired scope; comparison direction; shared sample accounting; no market-price baseline; and no economic-edge inference.

## Scope identity and sample accounting


Require one exact scope per result. The scope must preserve target posture; prediction representation; metric or diagnostic version; method role and version; split and fold identity; cutoff; paired test-record-set identity; eligibility policy; aggregation and weighting rules; and stratum. Eligible, excluded, and blocked records must be mutually exclusive terminal categories.

Require exactly:

total_considered_record_count =
eligible_record_count + excluded_record_count + blocked_record_count

Every excluded or blocked category must have a declared reason. Silent dropping, double counting, reclassification after test inspection, count fabrication, hidden pooling, and scope substitution are prohibited. Do not invent actual counts or numeric thresholds.

## Uncertainty and support-status requirements


Support status must be selected only from the exact support-status matrix. Require predeclared uncertainty method and level where applicable; compatibility with temporal, event, fold, and leakage-group dependence; sample-support rule identity; explicit insufficient, blocked, or unavailable reasons; no test-informed uncertainty-method selection; and no fabricated confidence level, sample minimum, bin count, resampling length, or tolerance.

## Exclusion block and missingness requirements


Missingness, exclusions, and blocks must be represented explicitly with declared reason summaries. Unknown permitted inputs are unavailable, incompatible inputs are blocked, and insufficient sample support is insufficient; no substitution, backfill, inference, pooling, or silent omission is allowed.

## Identity provenance and immutability


Require preservation of all common semantic fields; upstream definition identities and versions; source and label compatibility posture; result-content policy identities; exclusion and block reasons; complete provenance; and supersession linkage where applicable. Accepted result records must be immutable. Corrections require a new result identity and explicit supersedes linkage. Silent mutation, overwrite, deletion-based correction, or version reuse is prohibited.

## Claim separation and interpretation boundaries


A result record is not a claim; supported does not mean evidence-gate passage; a lower score does not by itself establish ranking superiority; calibration diagnostics do not establish economic edge; paired baseline improvement does not establish executability; no result approves trading, implementation, autonomy, or production behavior; later claim review must consume immutable result records under a separate contract.

## Fail-closed requirements


Fail closed for unknown result kind; unknown support status; missing or duplicate required semantic fields; metric or representation mismatch; invalid result domain; missing identity or version; split, fold, cutoff, stratum, aggregation, or weighting mismatch; unpaired comparison scope; sample-accounting mismatch; overlapping terminal count categories; missing reason for excluded, blocked, insufficient, or unavailable posture; missing required uncertainty policy; missing provenance; hidden record dropping or pooling; final-archive or future-information leakage; test-informed definition changes; mutation without superseding version; and market price treated as baseline, truth, or frictionless probability.

## Explicit non-approvals


This ticket does not approve or create result calculation; scoring execution; diagnostic execution; evaluation execution; probability generation; split execution; baseline execution; model training or calibration; data acquisition; corpus or dataset creation; source fetching; provider connectors; runtime schemas; dataclasses; serialization; persistence; database tables; migrations; reports; exports; diagrams; backtesting; simulation; market-price comparison execution; paper trading; trading; order placement; autonomy; runtime behavior; or production behavior.

## Canonical routing posture


Canonical routing fields remain exactly:

- condition_id
- token_id
- outcome

market_id is non-routing only.

token_outcome_pair is derived only.

## Recommended next ticket


WEATHER-BOT-STAGE3-EVALUATION-CLAIM-CONTRACT-PLANNING-01

It must remain docs/static-test-only/contract-planning-only and must not calculate results, execute evaluation, persist records, create reports, approve claims, or approve implementation.

## Machine-checkable assignments


Declared closed sets:

- weather bot planning stage:
  - weather_bot_stage3_evaluation_result_record_contract_planning
- immediate predecessor pr:
  - pr_362
- ticket lifecycle status:
  - docs_static_test_only
  - contract_planning_only
- result record contract status:
  - requirements_defined
  - runtime_schema_not_created
  - result_values_not_created
- scoring target posture:
  - venue_defined_settlement_outcome
- result kind:
  - scalar_score_result
  - calibration_bin_result
  - decomposition_result
  - distribution_diagnostic_result
  - ensemble_diagnostic_result
  - paired_comparison_result
- result support status:
  - supported
  - insufficient
  - blocked
  - unavailable
- scope identity posture:
  - exact_single_scope_required
- sample accounting posture:
  - eligible_excluded_blocked_total_identity_required
- terminal category posture:
  - mutually_exclusive_required
- exclusion block posture:
  - explicit_reason_required
- uncertainty posture:
  - predeclared_method_level_and_support_rule_required
- paired comparison posture:
  - exact_common_test_record_set_required
- baseline comparison posture:
  - climatology_or_persistence_only
- market price posture:
  - not_approved_as_baseline_or_truth
- immutability posture:
  - superseding_result_version_required
- claim posture:
  - result_records_do_not_approve_claims
- result calculation posture:
  - not_approved
- persistence posture:
  - not_approved
- report export posture:
  - not_approved
- canonical routing field:
  - condition_id
  - token_id
  - outcome
- non routing field:
  - market_id
- derived identifier field:
  - token_outcome_pair
- next ticket recommendation:
  - stage3_evaluation_claim_contract_planning
- evidence status:
  - evaluation_result_record_contract_planning_recorded
- label confidence:
  - confirmed

Actual assignments:

- weather bot planning stage: weather_bot_stage3_evaluation_result_record_contract_planning
- immediate predecessor pr: pr_362
- ticket lifecycle status: docs_static_test_only
- ticket lifecycle status: contract_planning_only
- result record contract status: requirements_defined
- result record contract status: runtime_schema_not_created
- result record contract status: result_values_not_created
- scoring target posture: venue_defined_settlement_outcome
- result kind: scalar_score_result
- result kind: calibration_bin_result
- result kind: decomposition_result
- result kind: distribution_diagnostic_result
- result kind: ensemble_diagnostic_result
- result kind: paired_comparison_result
- result support status: supported
- result support status: insufficient
- result support status: blocked
- result support status: unavailable
- scope identity posture: exact_single_scope_required
- sample accounting posture: eligible_excluded_blocked_total_identity_required
- terminal category posture: mutually_exclusive_required
- exclusion block posture: explicit_reason_required
- uncertainty posture: predeclared_method_level_and_support_rule_required
- paired comparison posture: exact_common_test_record_set_required
- baseline comparison posture: climatology_or_persistence_only
- market price posture: not_approved_as_baseline_or_truth
- immutability posture: superseding_result_version_required
- claim posture: result_records_do_not_approve_claims
- result calculation posture: not_approved
- persistence posture: not_approved
- report export posture: not_approved
- canonical routing field: condition_id
- canonical routing field: token_id
- canonical routing field: outcome
- non routing field: market_id
- derived identifier field: token_outcome_pair
- next ticket recommendation: stage3_evaluation_claim_contract_planning
- evidence status: evaluation_result_record_contract_planning_recorded
- label confidence: confirmed

Missing, duplicate, hybrid, reordered, extra, or custom fields and values are rejected.

## Acceptance criteria


Acceptance requires the exact title and Canonical ID, required headings, exact matrices, exact semantic-field list, exact assignments, predecessor merge SHA, successor ticket, routing posture, allowlist counts, deterministic static tests, mutation tests, validation commands, and no runtime schema, calculation, persistence, report, export, or production behavior.
