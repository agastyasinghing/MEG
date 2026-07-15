# WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-CONTRACT-PLANNING-01

Canonical ID: weather_bot_stage3_scoring_and_diagnostics_contract_planning_01

## Status and scope

This artifact is docs/static-test-only/contract-planning-only for Weather Bot evidence-ladder Stage 3 scoring-rule and diagnostic applicability contracts.

This ticket defines requirements only. It does not calculate scores, generate probability records, execute splits, perform evaluation, create datasets, fit or calibrate models, persist metrics, generate diagrams or reports, fetch sources, expand the corpus, simulate markets, trade, execute orders, automate decisions, or add production behavior.

## Immediate predecessor and merge verification

Immediate predecessor: pr_361.

PR #361 is recorded as merged by actual merge commit `9b0457495db3274ef957ab4c08e0e3cb6fb02fe3`.

The commit `9b0457495db3274ef957ab4c08e0e3cb6fb02fe3` is an actual merge commit with multiple parents, not a preview merge SHA.

This branch is based on current main containing `9b0457495db3274ef957ab4c08e0e3cb6fb02fe3`.

Current repository state was inspected for this ticket, and no newer controlling Weather Bot state supersedes PR #361 for this scoring-and-diagnostics contract-planning scope.

## Contract purpose and controlling target

Weather Bot scores and diagnoses probabilities for the venue-defined settlement outcome.

It does not score generic weather detached from the venue settlement rule.

Every score or diagnostic requires compatible probability-record, label, split, fold, availability, source/station, threshold, unit, comparator, measurement-window, and archive/finality posture.

Ineligible, blocked, conflicted, unavailable, unpaired, or representation-incompatible records fail closed.

Metric applicability is determined by the represented prediction object, not by convenience.

## Input eligibility and representation gates

A future scoring or diagnostic input is eligible only when the represented prediction object, compatible settlement label, split, fold, cutoff, point-in-time availability evidence, source/station compatibility, threshold, unit, comparator, measurement-window, and archive/finality posture are all compatible with the selected metric or diagnostic.

Representation mismatch blocks applicability. Binary-event probability artifacts do not imply full predictive distributions, and finite ensemble artifacts do not imply comparable distribution artifacts unless explicitly represented as such by a later approved contract.

Ineligible, blocked, conflicted, unavailable, unpaired, or representation-incompatible records must be represented as blocked rather than silently repaired.

## Exact scoring and diagnostic applicability matrix

| Artifact | Required representation | Required meaning | Direction or use | Fail-closed boundary |
| --- | --- | --- | --- | --- |
| brier_score | binary outcome probability | mean squared error between the probability assigned to the canonical binary settlement outcome and its compatible binary label | proper score; lower is better; aggregate only under one predeclared weighting rule | block when probability, label, canonical target, pairing, or aggregation compatibility is invalid |
| log_score | binary outcome probability | negative logarithmic score for the canonical binary settlement outcome and its compatible binary label | proper score; lower is better; probability-boundary handling must be predeclared without test-informed changes | block when the boundary policy is absent or probability, label, canonical target, or pairing compatibility is invalid |
| reliability_diagram | binary outcome probability | predeclared probability bins containing sample count, mean predicted probability, observed outcome frequency, and uncertainty | calibration diagnostic only; not a scalar ranking substitute | block unsupported claims for empty or insufficient bins and never silently merge bins after test inspection |
| brier_decomposition | binary outcome probability | reliability, resolution, and uncertainty components under one predeclared decomposition method | diagnostic decomposition only; not a replacement for the proper score and sample-sufficiency gated | block when the method, grouping, or sufficient compatible samples were not predeclared |
| crps | full predictive distribution | proper score comparing an explicitly represented predictive distribution with a compatible verifying observation | proper score; lower is better; applicable only to explicit full distributions | block when only a binary event probability or incomplete distribution is available |
| pit_histogram | continuous, discrete, or mixed full predictive distribution | probability-integral-transform diagnostic under one predeclared representation-compatible treatment | distributional calibration diagnostic only; not a scalar ranking substitute | block when the predictive representation or PIT treatment is incompatible or undeclared |
| rank_histogram | finite comparable ensemble | rank of the compatible verifying observation among explicit ensemble members under one predeclared tie treatment | ensemble calibration diagnostic only; not a scalar ranking substitute | block when members are not explicit and comparable or tie treatment is undeclared |
| threshold_weighted_crps | full predictive distribution with justified threshold weighting | proper distribution score using one predeclared threshold-weight function for a justified rare-event or near-threshold claim | proper score; lower is better; weighting must be fixed before test inspection | block when weighting, full-distribution representation, or claim justification is absent or post-hoc |

## Proper scoring-rule requirements

Brier score and log score apply only to compatible binary probability records and binary settlement labels.

CRPS and threshold-weighted CRPS require explicit full predictive distributions and compatible verifying observations.

Lower-is-better direction applies only to the proper-score rows.

Log-score boundary handling must be declared before evaluation.

This ticket does not choose a clipping epsilon, infinite-penalty policy, numeric probability tolerance, or other boundary constant.

Threshold-weight functions must be declared and justified before evaluation.

No score may be chosen after inspecting test outcomes.

## Calibration diagnostic requirements

Reliability bins, interval-closure convention, boundary handling, sample-support rule, and uncertainty method must be predeclared.

Each reliability bin must preserve count, mean predicted probability, observed outcome frequency, and uncertainty posture.

Brier decomposition must preserve reliability, resolution, and uncertainty under one declared method.

Diagnostics must not be misrepresented as scalar ranking scores.

No fabricated bin count, sample minimum, confidence level, clipping constant, or tie constant is approved.

## Distribution and ensemble diagnostic requirements

PIT treatment must be compatible with continuous, discrete, or mixed distributions.

Rank-histogram tie treatment and ensemble-member comparability must be declared.

Distribution and ensemble diagnostics must not be misrepresented as scalar ranking scores.

No fabricated bin count, sample minimum, confidence level, clipping constant, or tie constant is approved.

## Aggregation and weighting requirements

One predeclared aggregation and weighting rule is required before test inspection.

Candidate and baseline comparisons must use:

- the same split identity and version;
- the same fold and cutoff;
- the same eligible paired test-record set;
- the same compatible labels;
- the same metric version and applicability rule;
- the same aggregation and weighting rule;
- the same stratum definition.

Missing candidate or baseline records must not be silently dropped, replaced, backfilled, or imputed.

Score comparisons must preserve record counts, exclusions, and block reasons.

Do not prescribe a numeric weighting scheme in this ticket.

## Paired baseline comparison requirements

Paired comparisons are required against both:

- climatology;
- persistence.

The baselines must satisfy the merged baseline contract.

Market prices are not an approved baseline, calibration truth, or frictionless probability reference.

No economic-edge or trading claim may be inferred from a proper score or calibration diagnostic alone.

## Binning sparse-bucket and sample-sufficiency requirements

All bin definitions, grouping rules, sample-sufficiency thresholds, and pooling rules must be declared before test evaluation.

Empty or insufficient bins and strata must be represented as blocked or insufficient.

They must not be:

- silently removed;
- silently pooled;
- merged after test inspection;
- used for supported claims without sufficient evidence.

Do not invent a numeric minimum, fixed bin count, confidence level, or interval method.

## Stratification requirements

Future supported stratification axes are exactly:

- market_family
- threshold_distance
- forecast_horizon
- station_source_compatibility
- trap_category
- season_or_regime_when_supported
- archive_layer

An axis may be used only when predeclared, compatible, and sample-sufficient.

No post-hoc stratum selection is permitted.

## Uncertainty requirements

One predeclared uncertainty method and interval level is required.

The uncertainty method must be compatible with fold, temporal, event, and leakage-group dependence.

Sample counts and applicable block reasons must be preserved.

No naive independence assumption is permitted unless justified.

No test-informed interval-method selection is permitted.

Do not choose a bootstrap design, resampling block length, confidence level, or asymptotic method here.

## Metric identity provenance and immutability

Future score or diagnostic artifacts must preserve requirements for:

- metric or diagnostic identity and version;
- prediction representation;
- probability-record identity;
- compatible label identity;
- split identity and version;
- fold identity and cutoff;
- candidate or baseline method identity and version;
- paired test-record-set identity;
- aggregation and weighting rule;
- binning, decomposition, PIT, tie, or threshold-weight policy where applicable;
- stratum identity;
- sample count;
- uncertainty method and level;
- exclusion or block reason;
- provenance.

Accepted definitions and future results must be immutable. Corrections require a superseding version, not silent mutation.

## Fail-closed and no-lookahead requirements

Fail closed for:

- canonical-target mismatch;
- incompatible or blocked labels;
- invalid probability domain;
- missing publication-availability evidence;
- representation mismatch;
- split or fold mismatch;
- unpaired candidate and baseline records;
- undeclared metric policy;
- undeclared bin, tie, weighting, aggregation, or uncertainty policy;
- sparse or insufficient claims;
- final-archive or future-information leakage;
- test-informed selection or redesign.

## Human-review and claim boundaries

Calibration, ranking, economic edge, and executability are separate claim classes.

This ticket approves none of them.

Human review remains a claim-boundary safeguard and does not convert diagnostics into approval for ranking, economic edge, executability, trading, order placement, autonomy, runtime behavior, or production behavior.

## Explicit non-approvals

This ticket does not approve:

- scoring execution;
- diagnostic execution;
- probability generation;
- split execution;
- baseline execution;
- model training or calibration;
- dataset or corpus creation;
- source fetching;
- provider connectors;
- metric persistence;
- storage persistence;
- diagrams;
- reports or exports;
- backtesting;
- simulation;
- market-price comparison execution;
- paper trading;
- trading;
- order placement;
- autonomy;
- runtime behavior;
- production behavior.

## Canonical routing posture

Canonical routing fields remain exactly:

- condition_id
- token_id
- outcome

market_id is non-routing only.

token_outcome_pair is derived only.

## Recommended next ticket

Recommended next ticket: WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-CONTRACT-PLANNING-01.

It must remain docs/static-test-only/contract-planning-only and must not calculate, persist, report, or execute evaluation results.

## Machine-checkable assignments

Closed sets:

Closed set for weather bot planning stage:
- weather_bot_stage3_scoring_and_diagnostics_contract_planning

Closed set for immediate predecessor pr:
- pr_361

Closed set for ticket lifecycle status:
- docs_static_test_only
- contract_planning_only

Closed set for scoring contract status:
- requirements_defined
- calculations_not_created

Closed set for scoring target posture:
- venue_defined_settlement_outcome

Closed set for binary proper score:
- brier_score
- log_score

Closed set for full distribution proper score:
- crps

Closed set for conditional weighted score:
- threshold_weighted_crps

Closed set for calibration diagnostic:
- reliability_diagram
- brier_decomposition

Closed set for distribution diagnostic:
- pit_histogram

Closed set for ensemble diagnostic:
- rank_histogram

Closed set for proper score direction posture:
- lower_is_better

Closed set for metric applicability posture:
- representation_gated

Closed set for binning posture:
- predeclared_reproducible_bins_required

Closed set for sparse bucket posture:
- blocked_or_insufficient_not_silently_pooled

Closed set for uncertainty posture:
- predeclared_method_required

Closed set for comparison posture:
- paired_common_test_record_set_required

Closed set for baseline comparison posture:
- climatology_and_persistence_required

Closed set for stratification posture:
- predeclared_supported_axes_only

Closed set for tuning posture:
- train_or_calibration_only

Closed set for market price posture:
- not_approved_as_baseline_or_truth

Closed set for scoring execution posture:
- not_approved

Closed set for diagnostic execution posture:
- not_approved

Closed set for metric persistence posture:
- not_approved

Closed set for report export posture:
- not_approved

Closed set for canonical routing field:
- condition_id
- token_id
- outcome

Closed set for non routing field:
- market_id

Closed set for derived identifier field:
- token_outcome_pair

Closed set for next ticket recommendation:
- stage3_evaluation_result_record_contract_planning

Closed set for evidence status:
- scoring_and_diagnostics_contract_planning_recorded

Closed set for label confidence:
- confirmed

Actual assignments:

- weather bot planning stage: weather_bot_stage3_scoring_and_diagnostics_contract_planning
- immediate predecessor pr: pr_361
- ticket lifecycle status: docs_static_test_only
- ticket lifecycle status: contract_planning_only
- scoring contract status: requirements_defined
- scoring contract status: calculations_not_created
- scoring target posture: venue_defined_settlement_outcome
- binary proper score: brier_score
- binary proper score: log_score
- full distribution proper score: crps
- conditional weighted score: threshold_weighted_crps
- calibration diagnostic: reliability_diagram
- calibration diagnostic: brier_decomposition
- distribution diagnostic: pit_histogram
- ensemble diagnostic: rank_histogram
- proper score direction posture: lower_is_better
- metric applicability posture: representation_gated
- binning posture: predeclared_reproducible_bins_required
- sparse bucket posture: blocked_or_insufficient_not_silently_pooled
- uncertainty posture: predeclared_method_required
- comparison posture: paired_common_test_record_set_required
- baseline comparison posture: climatology_and_persistence_required
- stratification posture: predeclared_supported_axes_only
- tuning posture: train_or_calibration_only
- market price posture: not_approved_as_baseline_or_truth
- scoring execution posture: not_approved
- diagnostic execution posture: not_approved
- metric persistence posture: not_approved
- report export posture: not_approved
- canonical routing field: condition_id
- canonical routing field: token_id
- canonical routing field: outcome
- non routing field: market_id
- derived identifier field: token_outcome_pair
- next ticket recommendation: stage3_evaluation_result_record_contract_planning
- evidence status: scoring_and_diagnostics_contract_planning_recorded
- label confidence: confirmed

Missing, duplicate, hybrid, extra, or custom fields and values are rejected.

## Acceptance criteria

- The artifact remains docs/static-test-only/contract-planning-only.
- The applicability matrix is preserved exactly.
- Closed sets and Actual assignments remain synchronized and machine-checkable.
- Static tests use deterministic standard-library file and AST parsing and import no production modules.
- Changed-file scope is verified outside pytest.
- No runtime implementation, scorer, metric calculation, diagram generation, persistence, report, export, or production behavior is added.
