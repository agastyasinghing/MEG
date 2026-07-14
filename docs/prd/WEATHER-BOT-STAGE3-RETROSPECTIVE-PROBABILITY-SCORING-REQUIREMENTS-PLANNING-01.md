# WEATHER-BOT-STAGE3-RETROSPECTIVE-PROBABILITY-SCORING-REQUIREMENTS-PLANNING-01

Canonical ID: WEATHER-BOT-STAGE3-RETROSPECTIVE-PROBABILITY-SCORING-REQUIREMENTS-PLANNING-01

## Status and scope

This artifact is docs/static-test-only/requirements-planning-only for Weather Bot Stage 3 retrospective probability scoring requirements. It records a static requirements contract for later evidence-ladder Stage 3 design and creates no executable scorer, probability generator, model training path, scoring run, evaluation execution, backtest, data acquisition, corpus expansion, source fetch, persistence layer, report, paper simulation, runtime observation path, trading path, execution path, autonomy, or production behavior.

The weather bot planning stage is limited to `weather_bot_stage3_retrospective_probability_scoring_requirements_planning`. The ticket lifecycle statuses are `docs_static_test_only` and `requirements_planning_only`.

## Immediate predecessor and merge verification

Predecessor gate verification was performed before editing using local repository history because no `origin` remote or `gh` CLI is configured in this container. Current history shows PR #357 merged as `3ede1b5 Merge pull request #357 from agastyasinghing/codex/create-stage-3-readiness-inventory`; the actual merge commit recorded for PR #357 is `3ede1b5e2eb019e3195ff3abf023442a69a3f23b`, not a preview merge SHA.

The current branch is based on the local current main-equivalent history containing merge commit `3ede1b5e2eb019e3195ff3abf023442a69a3f23b` at HEAD before this ticket's edits. Repository history after PR #357 contained no newer Weather Bot PR merge and no newer controlling Weather Bot state superseding PR #357. PR #357 remains the immediate merged predecessor as `pr_357` for this requirements-planning ticket.

## Controlling settlement-probability target

Weather Bot scores the probability of the venue-defined settlement outcome represented by the canonical token/outcome route. It does not score generic weather, generic meteorological exceedance, or a provider-native weather target detached from the venue settlement rule.

The target posture is `venue_defined_settlement_outcome`; `generic_weather_target_rejected` is an explicit negative boundary. The evidence-ladder Stage 3 gate definition controls sequencing as `retrospective_probability_scoring_strict_oos`. Quantitative-roadmap methods such as EMOS, BMA, analog ensembles, and distributional regression remain unapproved candidates and do not override the evidence-ladder gate.

## Stage 3 prediction-record requirements

A future prediction record must preserve, at minimum, these requirements-only fields:

- `condition_id`
- `token_id`
- `outcome`
- prediction as-of timestamp
- target settlement-rule identity
- market family
- source and station compatibility
- threshold, unit, comparator, and measurement window
- archive/finality layer
- forecast or input publication availability
- probability value and the outcome it refers to
- method/version identity
- provenance needed for later scoring

These are planning requirements only. This ticket does not create a runtime schema, dataclass, persistence table, serialization contract, or production validation path.

## Source-compatible label requirements

Future labels must be source-compatible with the venue resolver, resolver-accurate, archive-layer explicit, revision-aware, and unavailable before their legitimate publication or resolution time. Labels must preserve source identity, station identity where applicable, finality/archive layer, revision status, measurement window, unit, threshold, comparator, and the settlement outcome represented by the canonical route.

Blocked/conflicted labels must fail closed; blocked, conflicted, unresolved, source-incompatible, station-incompatible, or resolver-incompatible labels must fail closed and must not be scored as ordinary usable labels.

## Point-in-time and availability requirements

Future replay must use as-of joins and forecast/input publication time rather than forecast initialization time. Availability must be represented as the time at which an input was legitimately obtainable by the evaluator, including delayed releases and revisions.

Future work must prohibit future forecast cycles, final-archive leakage, hindsight station/source/provider selection, and use of labels or forecasts before their legitimate publication, availability, or settlement-resolution time.

## Strict OOS split requirements

Future scoring design must require strict out-of-sample evaluation using rolling-origin or walk-forward OOS evaluation. Where applicable, it must include leave-station-out validation, leave-year-out validation, family-stratified evaluation, immutable train/calibration/test boundaries, and predeclared split and tuning rules.

Shuffled random validation is rejected as the primary time-series split. Test-split threshold tuning, test-split calibration tuning, and post-hoc split changes are prohibited. This ticket creates no split files and executes no split.

## Baseline requirements

Future evaluation must include source-compatible, as-of baselines for climatology and persistence. Baselines must obey the same venue-target, publication-availability, source/station compatibility, archive-layer, and no-lookahead constraints as candidate methods.

Market prices must not be treated as frictionless truth. This ticket does not introduce Stage 4 executable-cost analysis, market-microstructure execution analysis, or paper-simulation behavior.

## Scoring-rule applicability matrix

The deterministic planning matrix is conditional on prediction representation:

| Prediction representation | Applicable future diagnostics | Applicability boundary |
| --- | --- | --- |
| binary outcome probabilities | Brier score, log score, reliability diagrams | Applies only when the prediction is a probability for the canonical venue-defined binary settlement outcome. |
| binary calibration analysis | Brier decomposition | Applies only to binary probability records with enough predeclared samples for decomposition claims. |
| full predictive distributions | CRPS and PIT diagnostics | Applies only when a full predictive distribution is explicitly represented. |
| finite ensembles | rank histograms where appropriate | Applies only when finite ensemble members are represented and comparable to the verifying observation. |
| rare-event or near-threshold distributional evaluation | threshold-weighted CRPS where justified | Applies only when the future design justifies rare-event or near-threshold weighting before evaluation. |

Not every metric applies to every prediction representation. No metric may be calculated by this ticket, and scoring output remains not approved.

## Calibration and diagnostic requirements

Future diagnostics must specify reproducible bins, sample counts, uncertainty intervals, and declared handling for empty or sparse buckets. Calibration claims must distinguish reliability, resolution, uncertainty, and representation-specific applicability.

Diagnostics must preserve the target outcome, split identity, baseline identity, method/version identity, availability posture, and label compatibility posture needed for later audit.

## Threshold-bucket and stratification requirements

Future planning must cover stratification by market family, threshold distance, forecast horizon, station/source compatibility, trap category, season/regime when supported, and archive layer.

Threshold buckets and other strata must be reproducibly declared before evaluation. Sparse or empty strata must be reported as blocked or insufficient rather than silently pooled into broader claims.

## Sample-sufficiency and uncertainty requirements

Later work must predeclare sample-sufficiency thresholds and uncertainty-interval methods before evaluation. This document deliberately fabricates no numeric minimum sample threshold and authorizes no default minimum.

Insufficient samples must block claims rather than be silently pooled. Uncertainty reporting must be tied to the split, stratum, metric applicability, and label/finality layer.

## Fail-closed and no-lookahead requirements

Future design must fail closed for missing canonical identifiers, incompatible labels, unavailable inputs, revision ambiguity, final-archive leakage risk, future forecast cycles, hindsight provider/source/station selection, blocked/conflicted labels, and split-boundary violations.

No-lookahead requirements prohibit using future forecast cycles, final archive information unavailable as of prediction time, shuffled random validation as primary time-series evidence, test-split threshold or calibration tuning, and scoring blocked or conflicted labels as ordinary usable labels.

## Human-review and auditability requirements

Future scoring design must preserve human-review and auditability requirements for target identity, source/station compatibility, publication availability, archive/finality layer, method/version identity, split identity, baseline identity, metric applicability, sparse-bucket handling, and fail-closed exclusions.

This ticket does not approve owner-decision capture, operator-decision execution, Telegram approval queue behavior, runtime observation, reporting, persistence, or production audit output.

## Explicit non-approvals

This ticket does not approve probability generation, model training, scoring, evaluation execution, backtesting, data acquisition, corpus expansion, source fetching, persistence, reporting, paper simulation, runtime observation, trading, execution, autonomy, production behavior, runtime schemas, dataclasses, split files, metrics, diagrams, datasets, or reports.

EMOS, BMA, analog ensembles, distributional regression, and any other quantitative-roadmap method remain unapproved candidates for later planning only.

## Canonical routing posture

Canonical routing fields remain exactly:

- `condition_id`
- `token_id`
- `outcome`

`market_id` is non-routing only. `token_outcome_pair` is derived only and is not an input replacement for `condition_id`, `token_id`, and `outcome`.

## Recommended next ticket

Recommended next ticket: WEATHER-BOT-STAGE3-PROBABILITY-RECORD-CONTRACT-PLANNING-01

The recommended next ticket must remain docs/static-test-only/planning-only and must not create runtime code, probabilities, scoring runs, datasets, persistence, reports, implementation approval, trading, execution, autonomy, or production behavior.

## Machine-checkable assignments

Closed sets:

- weather bot planning stage: weather_bot_stage3_retrospective_probability_scoring_requirements_planning
- immediate predecessor pr: pr_357
- ticket lifecycle status: docs_static_test_only, requirements_planning_only
- scoring target posture: venue_defined_settlement_outcome, generic_weather_target_rejected
- stage3 gate definition: retrospective_probability_scoring_strict_oos
- prediction record status: requirements_defined, runtime_schema_not_created
- label requirement status: source_compatible_point_in_time_required
- split requirement status: rolling_origin_or_walk_forward_required, random_shuffle_primary_split_rejected
- baseline requirement: climatology, persistence
- scoring execution posture: not_approved
- probability generation posture: not_approved
- backtesting posture: not_approved
- persistence posture: not_approved
- canonical routing field: condition_id, token_id, outcome
- non routing field: market_id
- derived identifier field: token_outcome_pair
- next ticket recommendation: stage3_probability_record_contract_planning
- evidence status: requirements_planning_recorded
- label confidence: confirmed

Actual assignments:

- weather bot planning stage: weather_bot_stage3_retrospective_probability_scoring_requirements_planning
- immediate predecessor pr: pr_357
- ticket lifecycle status: docs_static_test_only
- ticket lifecycle status: requirements_planning_only
- scoring target posture: venue_defined_settlement_outcome
- scoring target posture: generic_weather_target_rejected
- stage3 gate definition: retrospective_probability_scoring_strict_oos
- prediction record status: requirements_defined
- prediction record status: runtime_schema_not_created
- label requirement status: source_compatible_point_in_time_required
- split requirement status: rolling_origin_or_walk_forward_required
- split requirement status: random_shuffle_primary_split_rejected
- baseline requirement: climatology
- baseline requirement: persistence
- scoring execution posture: not_approved
- probability generation posture: not_approved
- backtesting posture: not_approved
- persistence posture: not_approved
- canonical routing field: condition_id
- canonical routing field: token_id
- canonical routing field: outcome
- non routing field: market_id
- derived identifier field: token_outcome_pair
- next ticket recommendation: stage3_probability_record_contract_planning
- evidence status: requirements_planning_recorded
- label confidence: confirmed

Hybrid/custom values and missing required assignments are rejected.

## Acceptance criteria

- The PRD exists at the canonical path and contains every required section.
- The actual PR #357 merge commit is recorded as `3ede1b5e2eb019e3195ff3abf023442a69a3f23b`.
- The target is venue-defined settlement outcome probability, not generic weather.
- Prediction-record fields are requirements only and no runtime schema or dataclass is created.
- Label, availability, revision, source compatibility, and no-lookahead rules are recorded.
- Strict OOS split and as-of baseline requirements are complete.
- Scoring-rule applicability is conditional by prediction representation and no metric is calculated.
- Calibration, uncertainty, sample-sufficiency, and stratification requirements are recorded without fabricated sample minimums.
- Scoring, probability generation, backtesting, persistence, runtime behavior, trading, execution, autonomy, and production behavior remain not approved.
- Machine-checkable assignments are section-scoped, exact, complete, and closed.
- Canonical routing posture remains exactly `condition_id`, `token_id`, and `outcome`; `market_id` is non-routing only; `token_outcome_pair` is derived only.
- Recommended next ticket is exactly `WEATHER-BOT-STAGE3-PROBABILITY-RECORD-CONTRACT-PLANNING-01`.
