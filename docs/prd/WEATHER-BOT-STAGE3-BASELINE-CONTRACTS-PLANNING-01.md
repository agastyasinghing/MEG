# WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-PLANNING-01

Canonical ID: WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-PLANNING-01

## Status and scope

This artifact is docs/static-test-only/contract-planning-only for Weather Bot Stage 3 baseline contracts planning. It defines requirements only for future point-in-time climatology and persistence baselines used in strict OOS retrospective probability scoring. It calculates no baseline, creates no probability records, executes no splits or scoring, generates no datasets, trains no models, fetches no sources, expands no corpus, persists no metrics, creates no reports, simulates no markets, trades nothing, executes nothing, automates no decisions, and adds no production behavior.

Machine posture markers in this section are `weather_bot_stage3_baseline_contracts_planning`, `docs_static_test_only`, and `contract_planning_only`.

## Immediate predecessor and merge verification

PR #360 is the immediate predecessor for this planning ticket. Local repository history records PR #360 merged as actual merge commit `c0b892c7be00442cf167b09c4cd853605e7bd8a8`, not a preview merge SHA. The branch for this work is based on the local current main-equivalent history containing merge commit `c0b892c7be00442cf167b09c4cd853605e7bd8a8`. The read-first Weather Bot state and Stage 3 predecessor artifacts show no newer controlling Weather Bot state superseding PR #360 for this baseline-contract planning scope. The immediate merged predecessor is recorded as `pr_360`.

## Contract purpose and baseline role

The purpose is to define static contracts for future point-in-time climatology and persistence baselines used in strict OOS retrospective probability scoring. Both baselines must target the canonical venue-defined settlement outcome, satisfy the probability-record contract, and use the exact folds, cutoffs, eligibility rules, and test records defined by the strict OOS split contract. Baselines are comparative references only; no baseline is calculated or approved for execution here.

## Common baseline requirements

Every future baseline must:

- target the canonical venue-defined settlement outcome;
- preserve `condition_id`, `token_id`, and `outcome`;
- satisfy the probability-record contract;
- preserve `prediction_as_of` and legitimate input publication availability;
- preserve settlement-rule, source, station, threshold, unit, comparator, measurement-window, and archive/finality compatibility;
- preserve method identity, version, and provenance;
- use only information permitted by the applicable OOS fold;
- produce a representation compatible with the metric and candidate comparison;
- use the same fold, cutoff, eligibility rules, and test records as the candidate;
- fail closed when required compatible information is unavailable.

For binary-outcome scoring, a future baseline probability must be in [0, 1]. This ticket calculates no value.

## Exact baseline applicability matrix

| Baseline type | Required meaning | Fail-closed boundary |
| --- | --- | --- |
| climatology | as-of empirical reference for the canonical settlement outcome estimated only from permitted historical train records | block when compatible point-in-time history or a predeclared sufficient fallback is unavailable |
| persistence | latest legitimately available compatible prior state under one predeclared persisted quantity and conversion rule | block when no compatible prior state exists or the persisted quantity or conversion rule would change after test inspection |

## Climatology baseline contract

A future climatology baseline must require:

- only labels legitimately available before the applicable fold cutoff;
- train history only for estimation;
- exact canonical settlement target;
- source/station/threshold/unit/comparator/window/finality compatibility;
- any conditioning dimensions, smoothing, history window, hierarchy, or fallback declared before test evaluation;
- no test record, future label, unavailable revision, or final archive leakage;
- no numeric history window, smoothing constant, or sample minimum invented here.

If conditioned climatology is unavailable, use only a predeclared compatible fallback. Otherwise fail closed.

## Persistence baseline contract

A future persistence baseline must require:

- one exact persisted quantity and one conversion rule declared before evaluation;
- the latest legitimately available compatible prior state before `prediction_as_of`;
- exact target, source, station, unit, threshold, comparator, window, and finality compatibility;
- no hindsight switching among providers, stations, quantities, forecasts, observations, or conversion rules;
- no future state, unavailable revision, final archive, or test-label knowledge;
- fail closed when no compatible prior state exists.

This ticket does not decide the persisted quantity or conversion formula.

## Point-in-time availability and no-lookahead

Both baseline families must preserve `prediction_as_of`, legitimate input publication availability, fold cutoff availability, and availability evidence. They must not use future inputs, future labels, unavailable revisions, final archives unavailable at prediction time, or settlement outcomes before legitimate resolution availability. Forecast initialization time alone is insufficient evidence unless paired with legitimate publication availability.

## Split, eligibility, and test-record parity

Climatology, persistence, and candidate methods must use:

- the same split identity and version;
- the same fold and cutoff;
- the same eligibility and no-lookahead rules;
- the same compatible labels;
- the same test records for comparative claims.

A candidate-versus-baseline claim must use a common paired test-record set. Missing baseline records must not be silently dropped or replaced after test inspection. An unsupported paired comparison must be blocked or explicitly reported as unavailable.

## Fitting, tuning, and calibration isolation

Baseline estimation uses train data only. Any future selection of conditioning dimensions, smoothing, hierarchy, fallback, persistence quantity, or conversion rule must be predeclared using train or isolated calibration information only. Test records and test outcomes must never influence those choices. No test record may influence fitting, feature selection, threshold selection, calibration tuning, hyperparameter tuning, bin selection, fallback choice, persistence quantity choice, conversion-rule choice, or split redesign.

## Conditioning, fallback, and missingness

Conditioning dimensions, smoothing posture, history-window posture, hierarchy, fallback identity, persistence quantity, and conversion-rule identity must be predeclared before test evaluation. If required compatible information is missing, the future baseline must use only a predeclared compatible fallback or fail closed. Missingness must produce an exclusion/block reason and must not be silently imputed, replaced, or changed after test inspection.

## Probability-record output requirements

Any future baseline output used for scoring must satisfy the probability-record contract, including canonical target, `prediction_as_of`, availability evidence, method identity and version, provenance, representation, source/station/threshold/unit/comparator/window/finality compatibility, label-join readiness, and fail-closed mismatch posture. Binary-outcome probabilities must be in [0, 1], but this ticket calculates no probability value.

## Baseline identity, provenance, and immutability

A future baseline record or definition must preserve:

- baseline type;
- baseline identity and version;
- method identity and version;
- split and fold identity;
- `prediction_as_of`;
- availability evidence;
- conditioning or persisted-quantity definition;
- fallback or conversion-rule identity;
- canonical target and compatibility posture;
- provenance and exclusion/block reason.

Accepted baseline definitions and scored baseline records must be immutable. Corrections require a superseding version, not silent mutation.

## Paired comparison and claim requirements

Comparative claims must pair candidate, climatology, and persistence outputs on the same compatible test-record set when making candidate-versus-baseline claims. Missing baseline records must not be silently dropped, backfilled, or replaced after test inspection. If a common paired test-record set is unavailable, the comparison must be blocked or explicitly reported as unavailable. Claims must identify the metric, compatible representation, split identity and version, fold identity, cutoff, eligibility rules, test records, and baseline identity/version.

## Fail-closed requirements

Baselines must fail closed when compatible point-in-time history is unavailable, no predeclared compatible fallback exists, no compatible prior state exists, the persisted quantity or conversion rule would change after test inspection, source/station/threshold/unit/comparator/window/finality compatibility cannot be proven, availability evidence is missing, canonical target compatibility fails, probability-record requirements are unmet, or paired comparison requirements cannot be satisfied.

## Human-review and auditability

Future baseline definitions and records must preserve human-review evidence sufficient to audit target semantics, source/station compatibility, availability, no-lookahead posture, split parity, fallback or conversion-rule identity, exclusion/block reasons, provenance, immutable versioning, and non-approval boundaries. Human review is advisory and does not approve execution, scoring, storage persistence, trading, autonomy, or production behavior.

## Explicit non-approvals

This ticket does not approve baseline execution, scoring execution, probability generation, split execution, dataset generation, model training, source fetching, corpus expansion, metric persistence, storage persistence, report creation, market simulation, paper trading, trading, order placement, autonomy, production behavior, connectors, runtime behavior, or automated decisions. Market prices are not approved as climatology, persistence, or frictionless truth. Stage 4 market-price and executable-cost analysis remains outside scope.

## Canonical routing posture

Canonical routing fields remain exactly:

- `condition_id`
- `token_id`
- `outcome`

`market_id` is non-routing only.

`token_outcome_pair` is derived only.

## Recommended next ticket

Recommended next ticket: WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-CONTRACT-PLANNING-01.

It must remain docs/static-test-only/planning-only and must not calculate metrics, execute scoring, persist outputs, create reports, or approve implementation.

## Machine-checkable assignments

Closed sets:

Closed set for weather bot planning stage:
- weather_bot_stage3_baseline_contracts_planning

Closed set for immediate predecessor pr:
- pr_360

Closed set for ticket lifecycle status:
- docs_static_test_only
- contract_planning_only

Closed set for baseline contract status:
- requirements_defined
- calculations_not_created

Closed set for baseline type:
- climatology
- persistence

Closed set for scoring target posture:
- venue_defined_settlement_outcome

Closed set for climatology history posture:
- train_only_as_of_history

Closed set for persistence input posture:
- latest_legitimately_available_compatible_prior_state

Closed set for persistence definition posture:
- predeclared_quantity_and_conversion_required

Closed set for split parity posture:
- same_folds_cutoffs_eligibility_and_test_records_required

Closed set for paired comparison posture:
- common_test_record_set_required

Closed set for availability posture:
- point_in_time_required

Closed set for fallback posture:
- predeclared_compatible_or_fail_closed

Closed set for tuning posture:
- train_or_calibration_only

Closed set for output contract posture:
- probability_record_contract_required

Closed set for market price posture:
- not_approved_as_baseline

Closed set for baseline execution posture:
- not_approved

Closed set for scoring execution posture:
- not_approved

Closed set for storage persistence posture:
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
- stage3_scoring_and_diagnostics_contract_planning

Closed set for evidence status:
- baseline_contracts_planning_recorded

Closed set for label confidence:
- confirmed

Actual assignments:

- weather bot planning stage: weather_bot_stage3_baseline_contracts_planning
- immediate predecessor pr: pr_360
- ticket lifecycle status: docs_static_test_only
- ticket lifecycle status: contract_planning_only
- baseline contract status: requirements_defined
- baseline contract status: calculations_not_created
- baseline type: climatology
- baseline type: persistence
- scoring target posture: venue_defined_settlement_outcome
- climatology history posture: train_only_as_of_history
- persistence input posture: latest_legitimately_available_compatible_prior_state
- persistence definition posture: predeclared_quantity_and_conversion_required
- split parity posture: same_folds_cutoffs_eligibility_and_test_records_required
- paired comparison posture: common_test_record_set_required
- availability posture: point_in_time_required
- fallback posture: predeclared_compatible_or_fail_closed
- tuning posture: train_or_calibration_only
- output contract posture: probability_record_contract_required
- market price posture: not_approved_as_baseline
- baseline execution posture: not_approved
- scoring execution posture: not_approved
- storage persistence posture: not_approved
- canonical routing field: condition_id
- canonical routing field: token_id
- canonical routing field: outcome
- non routing field: market_id
- derived identifier field: token_outcome_pair
- next ticket recommendation: stage3_scoring_and_diagnostics_contract_planning
- evidence status: baseline_contracts_planning_recorded
- label confidence: confirmed

Missing, duplicate, hybrid, extra, or custom fields and values are rejected.

## Acceptance criteria

- This artifact records PR #360 actual merge commit `c0b892c7be00442cf167b09c4cd853605e7bd8a8` and no newer controlling Weather Bot state superseding PR #360.
- The exact baseline applicability matrix is present with the exact header, row order, and cell contents.
- Closed sets appear before Actual assignments and exactly match the machine-checkable assignments.
- Common, climatology, persistence, point-in-time, no-lookahead, split-parity, tuning-isolation, paired-comparison, immutability, fail-closed, market-price rejection, non-approval, and canonical-routing requirements are documented.
- No numeric history window, smoothing value, or sample minimum is invented here.
- The recommended next ticket is exactly WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-CONTRACT-PLANNING-01 and remains docs/static-test-only/planning-only.
