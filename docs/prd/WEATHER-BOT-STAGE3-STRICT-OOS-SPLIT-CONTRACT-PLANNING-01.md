# WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01

Canonical ID: WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01

## Status and scope

This artifact is docs/static-test-only/contract-planning-only for Weather Bot Stage 3 strict out-of-sample split assignments used by future retrospective probability scoring. It defines requirements only and executes no split.

This ticket creates no split files, datasets, probability records, scorers, metrics, evaluation runs, backtests, model training, fetching, corpus expansion, persistence, reports, simulation, trading, execution, autonomy, or production behavior. The weather bot planning stage is limited to `weather_bot_stage3_strict_oos_split_contract_planning`, and the ticket lifecycle statuses are `docs_static_test_only` and `contract_planning_only`.

## Immediate predecessor and merge verification

Predecessor gate verification was performed before editing using local repository history because no `origin` remote is configured in this container. Current history shows PR #359 merged as `8083a84 Merge pull request #359 from agastyasinghing/codex/define-static-contract-for-stage-3-probability`; the actual merge commit recorded for PR #359 is `8083a842e58da3e4b7573c2e1c7439254d275397`, not a preview merge SHA.

The current branch was verified as based on the local current main-equivalent history containing merge commit `8083a842e58da3e4b7573c2e1c7439254d275397` at HEAD before this ticket's edits. Repository history and controlling Weather Bot state files contained no newer Weather Bot PR merge and no newer controlling Weather Bot state superseding PR #359 for this strict OOS split-contract planning ticket. PR #359 remains the immediate merged predecessor as `pr_359`.

## Contract purpose and Stage 3 evidence gate

The contract purpose is to define the static requirements for future strict out-of-sample split assignments used in retrospective probability scoring. Evidence-ladder Stage 3 remains retrospective probability scoring on strict OOS splits; this document records the split requirements that must exist before future scoring can be considered.

The primary evidence design must be rolling-origin or walk-forward. This document is a planning contract only and does not grant scoring execution, split execution, backtesting, probability generation, model fitting, or production approval.

## Eligible-record preconditions

A future split may include only records that satisfy the probability-record contract; have exact canonical routing fields; target the exact venue-defined settlement rule; have legitimate prediction/input availability evidence; have compatible source, station, threshold, unit, comparator, window, and archive/finality posture; have a non-blocked compatible label; and are eligible as of the declared split cutoff.

Ineligible, conflicted, unavailable, or leakage-risk records must fail closed. Eligibility must not be inferred from generic weather similarity, final archives unavailable at prediction time, missing availability evidence, blocked labels, incompatible station/source posture, incompatible threshold/unit/comparator/window posture, or records outside the declared split cutoff.

## Split unit and leakage-group requirements

Future split assignments must define the split unit before assignment and must also define a leakage group. The leakage group must ensure related records for the same settlement event or overlapping target episode cannot be distributed across train, calibration, and test roles in a way that reveals the test label.

Canonical route identity alone must not be assumed to solve temporal leakage, event-level leakage, target-episode leakage, overlapping-window leakage, or delayed-publication leakage. This planning contract does not prescribe a database key, hash, UUID, or implementation for the split unit or leakage group.

## Split roles and temporal boundaries

The closed split roles are exactly:

| Split role | Requirement |
| --- | --- |
| train | fitting and feature-selection role using only information permitted before the applicable fold cutoff |
| calibration | separate calibration role when the method or diagnostic requires calibration, using only isolated permitted information |
| test | strict holdout role whose records are never used for fitting, feature selection, threshold selection, calibration tuning, hyperparameter tuning, bin selection, or split redesign |

Test targets must occur strictly after permitted fitting information for the fold. Fold boundaries, cutoffs, temporal windows, and role assignments must be predeclared before test outcomes are inspected.

## Primary rolling-origin or walk-forward contract

Primary Stage 3 evidence must use rolling-origin or walk-forward evaluation with monotonically advancing cutoffs; training information available before the fold cutoff; calibration information isolated where required; test targets occurring strictly after permitted fitting information; immutable, predeclared fold boundaries; no shuffled-random primary time-series split; and no post-hoc boundary changes based on test outcomes.

No numeric window size, fold count, fixed duration, or sample minimum is prescribed by this ticket. Later work must justify any concrete window, fold, or cutoff design from the target, availability, and sufficiency structure before execution.

## Secondary generalization-mode matrix

Secondary generalization modes supplement rather than replace the primary temporal split.

| Applicability mode | Exact applicability requirement |
| --- | --- |
| leave_station_out | required when claiming transfer to unseen stations or station contexts |
| leave_year_out | required when claiming interannual generalization and sufficient multi-year evidence exists |
| family_stratified | required when making market-family-specific or cross-family claims |
| season_or_regime_stratified | applicable only when supported by predeclared, sample-sufficient evidence |

These modes do not authorize shuffled-random primary splitting and do not weaken rolling-origin or walk-forward primacy.

## Training, calibration, tuning, and test isolation

Training and feature selection must use train records only unless a later predeclared method explicitly permits calibration-only diagnostics without touching test records. Calibration is separate when the method or diagnostic requires calibration.

Test records must never be used for fitting, feature selection, threshold selection, calibration tuning, hyperparameter tuning, bin selection, scorer choice, baseline choice, split redesign, fold-boundary changes, sufficiency-threshold changes, or post-hoc claim selection. Tuning posture is `train_or_calibration_only`.

## Overlap, gap, and embargo requirements

A predeclared gap or embargo is required when overlapping measurement windows, forecast horizons, delayed publication, revisions, or shared target episodes could leak information across roles. Later work must justify the gap or embargo from the target and availability structure.

This ticket does not fabricate a default gap duration, embargo duration, fold width, horizon bucket width, or numeric overlap tolerance.

## Stratification and sample-sufficiency requirements

Later work must predeclare sufficiency thresholds by fold, role, family, station/source posture, horizon, threshold bucket, and relevant stratum. Numeric minimums are not invented by this planning ticket.

Insufficient or empty strata must block claims rather than be silently pooled. Pooling, if ever proposed, requires a predeclared compatibility basis and cannot be used to rescue an otherwise unsupported claim after test outcomes are known.

## Baseline parity requirements

Future climatology and persistence baselines must use the same folds, cutoffs, availability rules, eligibility rules, and test records as candidate methods. Baseline parity posture is `same_folds_and_eligibility_required`.

This ticket does not define, calculate, implement, persist, or report climatology, persistence, or any other baseline calculations.

## Split identity, provenance, and immutability

A future split assignment must preserve split identity and version; fold identity; split role; cutoff and relevant temporal boundaries; eligible-record identity; leakage-group identity; applicability mode; exclusion/block reason where applicable; and provenance needed for audit.

Accepted split definitions and test assignments must be immutable. Corrections require a superseding version, not silent mutation. Split identity, fold identity, leakage-group identity, and provenance requirements are requirements only, not a storage schema or implementation prescription.

## Fail-closed and no-lookahead requirements

Missing required eligibility evidence, canonical routing mismatch, settlement-rule mismatch, incompatible source/station/threshold/unit/comparator/window/archive/finality posture, blocked labels, insufficient strata, leakage risk, unknown availability, or post-cutoff eligibility must fail closed.

No-lookahead requirements prohibit use of future inputs, final archives unavailable at the relevant as-of time, settlement labels before legitimate resolution availability, delayed publication knowledge before availability, revision knowledge before availability, or test outcomes during split design and tuning.

## Human-review and auditability requirements

Future split artifacts must remain human-reviewable and auditable. Reviewers must be able to inspect predecessor merge verification, split purpose, eligible-record preconditions, leakage grouping, fold boundaries, role assignments, gap or embargo rationale where required, stratification and sufficiency posture, baseline parity posture, exclusion/block reasons, provenance references, immutable version posture, no-lookahead posture, and non-approval boundaries.

This document creates no owner-decision capture, operator-decision execution, audit persistence, export writing, report generation, or production workflow.

## Explicit non-approvals

Split execution is not approved. Scoring execution is not approved. Backtesting is not approved. Probability generation is not approved. Model training is not approved. Dataset creation is not approved. Split-file creation is not approved. Corpus expansion is not approved. Fetching, provider connectors, API calls, scraping, downloads, live source fetching, credentials or secrets changes, persistence, metric storage, reports, exports, simulation, paper trading, trading, execution, autonomy, runtime observation, and production behavior are not approved.

This ticket does not modify `meg/`, fixtures, datasets, workflows, schemas, migrations, dependencies, configuration, secrets, generated artifacts, reports, or exports.

## Canonical routing posture

Canonical routing fields remain exactly:

- `condition_id`
- `token_id`
- `outcome`

`market_id` is non-routing only. `token_outcome_pair` is derived only. Canonical route identity is necessary for eligibility but is not sufficient by itself to prevent temporal, event-level, target-episode, or overlapping-window leakage.

## Recommended next ticket

Recommended next ticket: WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-PLANNING-01.

It must remain docs/static-test-only/planning-only and must not calculate baselines, create datasets, execute scoring, persist metrics, create split files, create probability records, run backtests, train models, fetch data, expand the corpus, or approve implementation.

## Machine-checkable assignments

Closed set for weather bot planning stage:
- weather_bot_stage3_strict_oos_split_contract_planning

Closed set for immediate predecessor pr:
- pr_359

Closed set for ticket lifecycle status:
- docs_static_test_only
- contract_planning_only

Closed set for split contract status:
- requirements_defined
- split_files_not_created

Closed set for primary split posture:
- rolling_origin_or_walk_forward_required

Closed set for random shuffle posture:
- primary_split_rejected

Closed set for split role:
- train
- calibration
- test

Closed set for test boundary posture:
- immutable

Closed set for tuning posture:
- train_or_calibration_only

Closed set for calibration posture:
- separate_when_required

Closed set for leakage group posture:
- settlement_event_or_target_episode_required

Closed set for overlap control posture:
- gap_or_embargo_when_required

Closed set for leave station posture:
- required_when_unseen_station_transfer_claimed

Closed set for leave year posture:
- required_when_interannual_claimed

Closed set for family stratification posture:
- required_for_family_claims

Closed set for sample sufficiency posture:
- insufficient_samples_block_claims

Closed set for baseline parity posture:
- same_folds_and_eligibility_required

Closed set for split execution posture:
- not_approved

Closed set for scoring execution posture:
- not_approved

Closed set for backtesting posture:
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
- stage3_baseline_contracts_planning

Closed set for evidence status:
- strict_oos_split_contract_planning_recorded

Closed set for label confidence:
- confirmed

Actual assignments:
- weather bot planning stage: weather_bot_stage3_strict_oos_split_contract_planning
- immediate predecessor pr: pr_359
- ticket lifecycle status: docs_static_test_only
- ticket lifecycle status: contract_planning_only
- split contract status: requirements_defined
- split contract status: split_files_not_created
- primary split posture: rolling_origin_or_walk_forward_required
- random shuffle posture: primary_split_rejected
- split role: train
- split role: calibration
- split role: test
- test boundary posture: immutable
- tuning posture: train_or_calibration_only
- calibration posture: separate_when_required
- leakage group posture: settlement_event_or_target_episode_required
- overlap control posture: gap_or_embargo_when_required
- leave station posture: required_when_unseen_station_transfer_claimed
- leave year posture: required_when_interannual_claimed
- family stratification posture: required_for_family_claims
- sample sufficiency posture: insufficient_samples_block_claims
- baseline parity posture: same_folds_and_eligibility_required
- split execution posture: not_approved
- scoring execution posture: not_approved
- backtesting posture: not_approved
- canonical routing field: condition_id
- canonical routing field: token_id
- canonical routing field: outcome
- non routing field: market_id
- derived identifier field: token_outcome_pair
- next ticket recommendation: stage3_baseline_contracts_planning
- evidence status: strict_oos_split_contract_planning_recorded
- label confidence: confirmed

Missing, hybrid, or custom values outside these closed sets are rejected.

## Acceptance criteria

- The document exists with canonical ID `WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01` and all required sections.
- The document records PR #359 actual merge commit `8083a842e58da3e4b7573c2e1c7439254d275397` and states it is not a preview merge SHA.
- The document defines eligible-record preconditions and fail-closed handling for ineligible, conflicted, unavailable, or leakage-risk records.
- The document defines exact split roles `train`, `calibration`, and `test`, plus the exact secondary generalization-mode matrix.
- The document requires rolling-origin or walk-forward primary evidence and rejects shuffled-random primary time-series splitting.
- The document requires immutable test boundaries, tuning isolation, leakage-group handling, conditional gap or embargo controls, no fabricated numeric windows, and no fabricated sample minimums.
- The document requires baseline parity, split identity/provenance/immutability, superseding-version corrections, fail-closed posture, no-lookahead posture, explicit non-approvals, exact machine-checkable assignments, canonical routing posture, and the exact next ticket `WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-PLANNING-01`.
