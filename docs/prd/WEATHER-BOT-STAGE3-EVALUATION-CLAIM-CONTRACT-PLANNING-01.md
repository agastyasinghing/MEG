# WEATHER-BOT-STAGE3-EVALUATION-CLAIM-CONTRACT-PLANNING-01

Canonical ID: WEATHER-BOT-STAGE3-EVALUATION-CLAIM-CONTRACT-PLANNING-01

## Status and scope

This artifact is docs/static-test-only and contract-planning-only for Weather Bot Stage 3 evaluation claim requirements. It defines future semantic requirements only and creates no claim records, decisions, schemas, persistence, reports, runtime behavior, or production behavior.

## Immediate predecessor and merge verification

Immediate predecessor: pr_363.

ACTUAL_PR_363_MERGE_SHA: ba641e2b73cc5108b5506861e1924260d4516e1f.

The repository history contains this actual merge commit with two parents for PR #363. It is not the preview merge SHA e7f7f68f824e419989d7b2a1780b87ac4113c805. Current local HEAD contains the predecessor merge commit, and no newer controlling Weather Bot state in the read-first artifacts supersedes PR #363 for this claim-contract scope.

## Contract purpose and claim boundary

- An evaluation claim is a narrowly scoped, versioned interpretation of a complete ordered set of immutable evaluation-result records under one predeclared claim rule.
- A claim is not an evaluation result, metric, diagnostic, report, evidence-gate decision, implementation approval, economic-edge finding, executability finding, or trading approval.
- The target remains the venue-defined settlement outcome, not generic weather.
- Every future claim must consume immutable result records satisfying the evaluation-result-record contract.
- Claim class, required result identities, scope, comparator, rule, selection controls, and uncertainty posture must be fixed before test-result inspection.
- Unknown, incomplete, incompatible, post-hoc, provenance-deficient, or boundary-violating claims fail closed.

## Upstream result-record dependencies

Every future evaluation claim depends on immutable evaluation-result records that satisfy the evaluation-result-record contract, including exact result identity, kind, support status, method identity, target posture, representation, split, fold, cutoff, paired test-record set, aggregation, weighting, stratum, sample accounting, provenance, and supersession posture. Unsupported substitutions, mutable result payloads, or result records outside the predeclared scope cannot support a claim.

## Exact evaluation claim-class matrix

| Claim class | Required immutable result records | Required scope or comparator | Allowed future conclusion | Forbidden inference |
| --- | --- | --- | --- | --- |
| candidate_vs_climatology_predictive_skill | one or more predeclared paired_comparison_result records under applicable proper scores | candidate versus climatology under one exact paired scope | whether the predeclared candidate-versus-climatology claim rule is satisfied for the exact metrics and scope | overall superiority, calibration, economic edge, executability, implementation approval, or trading approval |
| candidate_vs_persistence_predictive_skill | one or more predeclared paired_comparison_result records under applicable proper scores | candidate versus persistence under one exact paired scope | whether the predeclared candidate-versus-persistence claim rule is satisfied for the exact metrics and scope | overall superiority, calibration, economic edge, executability, implementation approval, or trading approval |
| candidate_predictive_skill_across_required_baselines | the complete predeclared paired_comparison_result set against both climatology and persistence | identical candidate definition with both required baselines and compatible exact scopes | whether the predeclared cross-baseline predictive-skill rule is satisfied | universal superiority, robustness outside the declared scope, economic edge, executability, implementation approval, or trading approval |
| binary_calibration_behavior | calibration_bin_result plus every compatible scalar_score_result or decomposition_result required by the predeclared claim rule | one compatible binary representation, split scope, aggregation, weighting, and stratum | whether the predeclared binary-calibration claim rule is satisfied for the exact scope | predictive-skill superiority, economic edge, executability, implementation approval, or trading approval |
| distributional_calibration_behavior | distribution_diagnostic_result plus every compatible scalar_score_result required by the predeclared claim rule | one compatible full-distribution representation and exact scope | whether the predeclared distributional-calibration claim rule is satisfied | scalar-ranking superiority, economic edge, executability, implementation approval, or trading approval |
| ensemble_calibration_behavior | ensemble_diagnostic_result and every supporting result required by the predeclared claim rule | one compatible finite-ensemble representation, tie treatment, and exact scope | whether the predeclared ensemble-calibration claim rule is satisfied | scalar-ranking superiority, economic edge, executability, implementation approval, or trading approval |
| threshold_weighted_distribution_skill | paired_comparison_result under threshold_weighted_crps with its declared threshold-weight policy | one justified threshold-focused scope and approved climatology or persistence comparator | whether the predeclared threshold-weighted skill rule is satisfied for the exact threshold-focused scope | general predictive superiority, economic edge, executability, implementation approval, or trading approval |
| stratum_specific_predictive_skill | the complete predeclared paired_comparison_result set for one exact supported stratum | one declared stratum and approved climatology or persistence comparator | whether the predeclared stratum-specific skill rule is satisfied | generalization beyond the stratum, post-hoc subgroup discovery, economic edge, executability, implementation approval, or trading approval |

Do not add, remove, reorder, abbreviate, merge, or paraphrase rows.

## Exact claim-disposition matrix

| Claim disposition | Required meaning | Evidence-gate posture |
| --- | --- | --- |
| claim_supported | every required result is supported, the exact result set is complete, and the predeclared claim rule is satisfied | eligible only for a later evidence-gate decision; no gate passage is approved here |
| claim_not_supported | every required result is supported and complete but the predeclared claim rule is not satisfied | evidence-gate support from this claim is absent |
| claim_insufficient | no blocking or unavailable condition applies, but one or more required results or the claim-level support rule is insufficient | evidence-gate use is blocked |
| claim_blocked | a required result is blocked or a contract, leakage, scope, selection, accounting, immutability, or provenance requirement failed | claim is invalid for evidence-gate use |
| claim_unavailable | no blocking condition applies, but one or more required permitted result records do not exist or are unavailable | no substitution, inference, backfill, or evidence-gate use is allowed |

No custom, hybrid, pending, partial, or additional claim disposition is allowed.

## Common claim-record requirements

Include exactly this ordered semantic-field list:

- evaluation_claim_id
- claim_class
- claim_rule_id
- claim_rule_version
- claim_disposition
- claim_disposition_reason
- target_posture
- candidate_method_id
- candidate_method_version
- baseline_type_when_applicable
- baseline_method_id_when_applicable
- baseline_method_version_when_applicable
- prediction_representation
- metric_or_diagnostic_ids
- metric_or_diagnostic_versions
- required_evaluation_result_ids
- observed_evaluation_result_ids
- missing_evaluation_result_ids
- split_id
- split_version
- fold_scope
- cutoff_scope
- paired_test_record_set_id
- aggregation_rule_id
- weighting_rule_id
- stratum_id_when_applicable
- uncertainty_policy_id
- sample_support_rule_id
- selection_control_policy_id
- multiple_comparison_policy_id_when_applicable
- evidence_gate_eligibility_posture
- provenance
- claim_created_at
- supersedes_claim_id_when_applicable

These are future semantic requirements only.

This ticket must not create:

- a dataclass;
- Pydantic model;
- JSON schema;
- runtime validation schema;
- serializer;
- database table;
- migration;
- persistence adapter;
- API model;
- claim engine;
- result loader;
- report generator.

## Claim-rule predeclaration requirements

Require every future claim rule to declare before test-result inspection:

- claim class;
- exact ordered required result identities or deterministic result-selection rule;
- candidate identity and version;
- comparator identity and version where applicable;
- metric and diagnostic identities and versions;
- result-support requirements;
- exact split, fold, cutoff, paired-record, aggregation, weighting, and stratum scope;
- claim-direction convention;
- uncertainty and sample-support policy;
- selection-control policy;
- multiple-comparison policy when applicable;
- deterministic claim-disposition logic;
- missing, insufficient, unavailable, and blocked handling;
- supersession behavior.

No claim rule may be selected, altered, narrowed, broadened, or substituted after inspecting test results.

## Candidate-versus-climatology claim requirements

Candidate-versus-climatology claims must consume paired_comparison_result records, preserve the exact same candidate definition, preserve the applicable proper score and version, preserve the exact paired test-record set, preserve aggregation, weighting, split, fold, cutoff, representation, and stratum, preserve sample accounting, identify only climatology as the declared baseline, and remain separate claims unless a cross-baseline rule was predeclared. Market price is not an approved baseline, calibration truth, settlement truth, or frictionless probability.

## Candidate-versus-persistence claim requirements

Candidate-versus-persistence claims must consume paired_comparison_result records, preserve the exact same candidate definition, preserve the applicable proper score and version, preserve the exact paired test-record set, preserve aggregation, weighting, split, fold, cutoff, representation, and stratum, preserve sample accounting, identify only persistence as the declared baseline, and remain separate claims unless a cross-baseline rule was predeclared. Market price is not an approved baseline, calibration truth, settlement truth, or frictionless probability.

## Cross-baseline predictive-skill claim requirements

A cross-baseline predictive-skill claim requires:

- both climatology and persistence;
- the complete predeclared result set;
- compatible candidate identity and version;
- compatible metrics and result directions;
- compatible exact scopes;
- no silent metric or baseline omission;
- no substitution of one baseline for the other;
- a predeclared synthesis rule.

A baseline-specific pass cannot be silently promoted into a cross-baseline claim.

## Binary calibration claim requirements

Binary calibration claims require exact binary representation compatibility, exact result-record identities, declared bin or decomposition policy where applicable, ordered diagnostic payload preservation, support-status compatibility, exact scope and sample accounting, no conversion of a diagnostic into a scalar-ranking score, no conversion of calibration behavior into predictive-skill superiority, and no conversion into economic-edge or executability claims.

## Distribution and ensemble diagnostic claim requirements

Distribution and ensemble diagnostic claims require exact representation compatibility, exact result-record identities, declared PIT or tie policy where applicable, ordered diagnostic payload preservation, support-status compatibility, exact scope and sample accounting, no conversion of a diagnostic into a scalar-ranking score, no conversion of calibration behavior into predictive-skill superiority, and no conversion into economic-edge or executability claims.

## Threshold-weighted and stratified claim requirements

Require:

- threshold-weighted claims to preserve the declared threshold-weight function and justification;
- stratum-specific claims to identify one exact predeclared supported stratum;
- no post-hoc threshold, regime, season, trap category, horizon, market family, or source-compatibility selection;
- no generalization outside the exact threshold-focused or stratified scope;
- no pooling after test inspection;
- no silent removal of unfavorable strata.

## Multiple-testing and selection-control requirements

Require predeclaration of:

- claim families;
- metrics;
- diagnostics;
- comparators;
- strata;
- threshold-focused analyses;
- selection-control method;
- multiple-comparison policy when applicable;
- interpretation rule.

Prohibit:

- cherry-picking;
- winner-only reporting;
- metric shopping;
- baseline shopping;
- stratum shopping;
- cutoff shopping;
- uncertainty-method shopping;
- post-hoc claim-family creation;
- selective omission;
- silent multiplicity;
- test-informed rule revision.

Do not prescribe a numeric alpha, confidence level, correction threshold, minimum sample size, effect-size cutoff, tolerance, bin count, resampling length, or weighting constant.

## Scope identity and result-set completeness

Require:

- one exact claim scope;
- required_evaluation_result_ids fixed before test inspection;
- observed_evaluation_result_ids to equal the required list for claim_supported or claim_not_supported;
- no duplicate result identity;
- no result identity outside the required list;
- missing_evaluation_result_ids to be exact;
- every consumed result to have compatible target, representation, metric, method, split, fold, cutoff, paired-record set, aggregation, weighting, and stratum;
- no hidden result dropping;
- no result substitution;
- no scope broadening or narrowing;
- no final-archive or future-information leakage.

## Claim-disposition precedence and reason requirements

Require exactly this precedence order:

1. claim_blocked
2. claim_unavailable
3. claim_insufficient
4. evaluate the predeclared rule as claim_supported or claim_not_supported

Explain semantically:

- Any blocking contract condition produces claim_blocked.
- Otherwise, any missing or unavailable required result produces claim_unavailable.
- Otherwise, any insufficient required result or insufficient claim-level support produces claim_insufficient.
- Only when every required result is supported and complete may the predeclared rule produce claim_supported or claim_not_supported.

No averaging, voting, fallback, or custom precedence is allowed.

Do not place numeric constants in this section.

## Identity provenance and immutability

Require preservation of:

- every common semantic field;
- claim-rule identity and version;
- all required and observed result-record identities;
- upstream method and baseline identities;
- exact scope;
- selection-control and multiplicity policy identities;
- claim disposition and reason;
- complete provenance;
- supersession linkage.

Accepted claim records must be immutable.

Corrections require a new claim identity and explicit supersedes linkage.

Silent mutation, overwrite, deletion-based correction, result-list substitution, or version reuse is prohibited.

## Evidence-gate separation and interpretation boundaries

A claim record is not an evidence-gate decision; claim_supported does not mean the Stage 3 evidence gate passed; claim_not_supported does not by itself reject implementation permanently; calibration, predictive skill, economic edge, executability, implementation approval, and trading approval remain separate claim or decision classes; no claim record approves runtime implementation, persistence, reports, autonomy, production behavior, paper trading, trading, or order placement; only a later separately contracted evidence-gate decision may consume immutable claim records.

## Fail-closed requirements

Fail closed for:

- unknown claim class;
- unknown claim disposition;
- missing or duplicate common semantic field;
- missing claim-rule identity or version;
- missing, duplicated, unexpected, or reordered required result identity;
- incompatible result kind or support status;
- candidate, baseline, metric, representation, or scope mismatch;
- incomplete cross-baseline result set;
- undeclared claim direction;
- undeclared uncertainty or sample-support policy;
- undeclared selection-control policy;
- undeclared multiplicity policy when applicable;
- sample-accounting incompatibility;
- post-hoc metric, baseline, threshold, stratum, cutoff, or claim selection;
- hidden result dropping or substitution;
- missing provenance;
- final-archive or future-information leakage;
- mutation without a superseding version;
- market price treated as baseline, truth, or frictionless probability;
- claim interpretation expanded beyond the exact contract.

## Explicit non-approvals

This ticket does not approve or create result calculation; evaluation execution; claim evaluation; claim records; claim approval; evidence-gate decisions; evidence-gate passage; implementation approval; probability generation; split execution; baseline execution; model training or calibration; data acquisition; source fetching; provider connectors; runtime schemas; dataclasses; serialization; persistence; database tables; migrations; reports; exports; diagrams; backtesting; simulation; market-price comparison execution; economic-edge findings; executability findings; paper trading; trading; order placement; autonomy; runtime behavior; or production behavior.

## Canonical routing posture

Canonical routing fields remain exactly:

- condition_id
- token_id
- outcome

market_id is non-routing only.

token_outcome_pair is derived only.

## Recommended next ticket

WEATHER-BOT-STAGE3-EVIDENCE-GATE-DECISION-RECORD-CONTRACT-PLANNING-01

It must remain docs/static-test-only/contract-planning-only and must not calculate results, evaluate claims, make an evidence-gate decision, approve implementation, persist records, create reports, or add runtime behavior.

## Machine-checkable assignments

Declared closed sets:

- weather bot planning stage:
  - weather_bot_stage3_evaluation_claim_contract_planning
- immediate predecessor pr:
  - pr_363
- ticket lifecycle status:
  - docs_static_test_only
  - contract_planning_only
- claim contract status:
  - requirements_defined
  - claim_records_not_created
  - claim_decisions_not_created
- scoring target posture:
  - venue_defined_settlement_outcome
- claim class:
  - candidate_vs_climatology_predictive_skill
  - candidate_vs_persistence_predictive_skill
  - candidate_predictive_skill_across_required_baselines
  - binary_calibration_behavior
  - distributional_calibration_behavior
  - ensemble_calibration_behavior
  - threshold_weighted_distribution_skill
  - stratum_specific_predictive_skill
- claim disposition:
  - claim_supported
  - claim_not_supported
  - claim_insufficient
  - claim_blocked
  - claim_unavailable
- disposition precedence:
  - blocked_then_unavailable_then_insufficient_then_rule_evaluation
- result dependency posture:
  - immutable_evaluation_result_records_required
- claim rule posture:
  - predeclared_versioned_exact_scope_required
- result completeness posture:
  - exact_required_result_list_required
- selection control posture:
  - no_post_hoc_metric_stratum_comparator_or_rule_selection
- multiple comparison posture:
  - predeclared_policy_required_when_applicable
- baseline-specific posture:
  - climatology_and_persistence_claims_remain_distinct
- cross-baseline posture:
  - both_climatology_and_persistence_required
- market price posture:
  - not_approved_as_baseline_or_truth
- evidence gate posture:
  - claim_disposition_does_not_pass_evidence_gate
- immutability posture:
  - superseding_claim_version_required
- claim evaluation posture:
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
  - stage3_evidence_gate_decision_record_contract_planning
- evidence status:
  - evaluation_claim_contract_planning_recorded
- label confidence:
  - confirmed

Actual assignments:

- weather bot planning stage: weather_bot_stage3_evaluation_claim_contract_planning
- immediate predecessor pr: pr_363
- ticket lifecycle status: docs_static_test_only
- ticket lifecycle status: contract_planning_only
- claim contract status: requirements_defined
- claim contract status: claim_records_not_created
- claim contract status: claim_decisions_not_created
- scoring target posture: venue_defined_settlement_outcome
- claim class: candidate_vs_climatology_predictive_skill
- claim class: candidate_vs_persistence_predictive_skill
- claim class: candidate_predictive_skill_across_required_baselines
- claim class: binary_calibration_behavior
- claim class: distributional_calibration_behavior
- claim class: ensemble_calibration_behavior
- claim class: threshold_weighted_distribution_skill
- claim class: stratum_specific_predictive_skill
- claim disposition: claim_supported
- claim disposition: claim_not_supported
- claim disposition: claim_insufficient
- claim disposition: claim_blocked
- claim disposition: claim_unavailable
- disposition precedence: blocked_then_unavailable_then_insufficient_then_rule_evaluation
- result dependency posture: immutable_evaluation_result_records_required
- claim rule posture: predeclared_versioned_exact_scope_required
- result completeness posture: exact_required_result_list_required
- selection control posture: no_post_hoc_metric_stratum_comparator_or_rule_selection
- multiple comparison posture: predeclared_policy_required_when_applicable
- baseline-specific posture: climatology_and_persistence_claims_remain_distinct
- cross-baseline posture: both_climatology_and_persistence_required
- market price posture: not_approved_as_baseline_or_truth
- evidence gate posture: claim_disposition_does_not_pass_evidence_gate
- immutability posture: superseding_claim_version_required
- claim evaluation posture: not_approved
- persistence posture: not_approved
- report export posture: not_approved
- canonical routing field: condition_id
- canonical routing field: token_id
- canonical routing field: outcome
- non routing field: market_id
- derived identifier field: token_outcome_pair
- next ticket recommendation: stage3_evidence_gate_decision_record_contract_planning
- evidence status: evaluation_claim_contract_planning_recorded
- label confidence: confirmed

Missing, duplicate, hybrid, reordered, extra, or custom fields and values are rejected.

## Acceptance criteria

Acceptance requires the document to keep the exact title, Canonical ID, section order, matrices, common semantic fields, disposition precedence, closed sets, assignments, predecessor merge SHA, routing posture, successor ticket, evidence-gate separation, explicit non-approvals, fail-closed posture, and static-test-only scope. The companion static test must use independent expectations, parse the document structurally, exercise in-memory mutation rejection, verify allowlist counts, avoid production imports and repository-history assertions, and confirm no claim engine, runtime schema, persistence, report, decision, or production behavior is added.
