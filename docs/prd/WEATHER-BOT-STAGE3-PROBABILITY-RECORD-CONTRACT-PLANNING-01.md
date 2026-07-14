# WEATHER-BOT-STAGE3-PROBABILITY-RECORD-CONTRACT-PLANNING-01

Canonical ID: WEATHER-BOT-STAGE3-PROBABILITY-RECORD-CONTRACT-PLANNING-01

## Status and scope

This artifact is docs/static-test-only/contract-planning-only for a future immutable Weather Bot Stage 3 probability-prediction record contract. It defines requirements only and creates no probability generation, runtime schema, dataclass, record instance, scoring, evaluation execution, backtesting, model training, source fetching, corpus expansion, persistence, reporting, simulation, trading, execution, autonomy, or production behavior.

The weather bot planning stage is limited to `weather_bot_stage3_probability_record_contract_planning`. The ticket lifecycle statuses are `docs_static_test_only` and `contract_planning_only`.

## Immediate predecessor and merge verification

Predecessor gate verification was performed before editing using local repository history because no `origin` remote or `gh` CLI is configured in this container. Current history shows PR #358 merged as `786a723 Merge pull request #358 from agastyasinghing/codex/document-requirements-for-scoring-contract`; the actual merge commit recorded for PR #358 is `786a72353bfbdb6e27365c7f6ff6066481a440b5`, not a preview merge SHA.

The current branch is based on the local current main-equivalent history containing merge commit `786a72353bfbdb6e27365c7f6ff6066481a440b5` at HEAD before this ticket's edits. Repository history after PR #358 contained no newer Weather Bot PR merge and no newer controlling Weather Bot state superseding PR #358. PR #358 remains the immediate merged predecessor as `pr_358` for this contract-planning ticket.

## Contract purpose and target semantics

The future record must target the venue-defined settlement outcome represented by the canonical route. It records a prediction about the market settlement rule, not generic weather, not provider-native weather, and not a detached meteorological event.

## Common required record fields

A future record must preserve prediction record identity; `condition_id`; `token_id`; `outcome`; venue-defined settlement-rule identity and version where applicable; prediction as-of timestamp; forecast/input publication-availability timestamp or evidence; market family; threshold, unit, comparator, and measurement window where applicable; source and station compatibility posture; archive/finality layer expected for verification; prediction representation; method identity and version; provenance references required for audit; and creation/version metadata needed to establish immutability. These are requirements only, not a Python or storage schema.

## Canonical routing and settlement-rule identity

Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`. `market_id` is non-routing only. `token_outcome_pair` is derived only and cannot replace the canonical fields. Record identity must not replace canonical routing identity. The record must identify the exact venue-defined settlement-rule target and settlement-rule version where applicable.

## Temporal and availability fields

A future record must require `prediction_as_of`, legitimate input publication availability, forecast-cycle identity where applicable, and target measurement window. No future input relative to `prediction_as_of` is allowed. No final-archive information unavailable at prediction time is allowed. No settlement labels may be used before legitimate resolution availability. Forecast initialization time alone must not prove availability.

## Source, station, and target compatibility fields

A future record must preserve source compatibility, station compatibility where applicable, target threshold, target unit, comparator, measurement window, and archive/finality layer expected for verification. These fields must be compatible with the venue resolver and later labels before scoring readiness can be claimed.

## Prediction-representation applicability matrix

| Prediction representation | Conditional required fields | Later metric applicability metadata |
| --- | --- | --- |
| binary_outcome_probability | probability value in the closed interval [0, 1] and explicit identification of the canonical outcome it represents | sufficient to determine binary Brier/log-score/reliability applicability for the canonical venue-defined binary settlement outcome |
| full_predictive_distribution | explicit distribution representation, support/units, method/version identity | sufficient metadata for later CRPS/PIT applicability |
| finite_ensemble | explicit member representation, member count, units, method/version identity | sufficient metadata for later rank-histogram applicability |

Do not require one representation's fields for another representation. This ticket does not calculate, normalize, generate, or validate an actual probability.

## Probability-value requirements

For `binary_outcome_probability`, the future probability value must be in the closed interval [0, 1] and must identify the canonical outcome it represents. This planning artifact does not compute, normalize, generate, validate, store, or score any actual probability.

## Method, version, and provenance fields

A future record must preserve method identity and version, input/source provenance references, forecast-cycle identity where applicable, publication-availability evidence, settlement-rule provenance, and audit references sufficient for later human review. Candidate methods are not approved by this ticket.

## Record identity and immutability requirements

A future prediction record must be immutable after accepted creation. Corrections must create a new version or superseding record rather than silently mutating the scored record. Record identity is required for audit and de-duplication, but record identity must not replace canonical routing identity. This ticket does not prescribe a database, hash algorithm, UUID implementation, serialization format, or persistence mechanism.

## Label-join and scoring-readiness requirements

A later scoring join must verify exact canonical route; exact settlement-rule target; compatible threshold/unit/comparator/window; source/station compatibility; archive/finality compatibility; prediction timestamp before legitimate label availability; representation-specific metric applicability; and non-blocked prediction and label posture. Any mismatch must fail closed.

## Missingness and fail-closed requirements

Missing required fields, hybrid values, custom values, blocked prediction posture, blocked label posture, incompatible canonical route, incompatible settlement-rule target, incompatible source/station posture, incompatible archive/finality posture, unavailable input evidence, future input leakage, or label lookahead must fail closed and must not be scored as ordinary usable records.

## Human-review and auditability requirements

The future contract must preserve human-review evidence, provenance references, creation/version metadata, correction/supersession links where applicable, and audit context sufficient to explain what target was predicted, what information was legitimately available, and why a later label join was accepted or blocked.

## Explicit non-approvals

This artifact does not approve probability generation, schemas, dataclasses, scoring, evaluation execution, backtesting, model training, source fetching, corpus expansion, persistence, reporting, simulation, trading, execution, autonomy, production behavior, runtime validation, metric calculation, split creation, dataset creation, or implementation work.

## Recommended next ticket

Recommend exactly `WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01`. It must remain docs/static-test-only/planning-only and must not create split files, datasets, scoring runs, runtime code, persistence, reports, or implementation approval.

## Machine-checkable assignments

Closed sets:

- weather bot planning stage: weather_bot_stage3_probability_record_contract_planning
- immediate predecessor pr: pr_358
- ticket lifecycle status: docs_static_test_only, contract_planning_only
- record contract status: requirements_defined, runtime_schema_not_created
- scoring target posture: venue_defined_settlement_outcome
- record immutability posture: immutable_after_accepted_creation_required
- correction posture: superseding_record_required
- probability domain: closed_unit_interval
- prediction representation: binary_outcome_probability, full_predictive_distribution, finite_ensemble
- time availability posture: prediction_as_of_required, input_publication_availability_required
- label join posture: canonical_route_and_target_rule_required
- mismatch posture: fail_closed
- scoring execution posture: not_approved
- probability generation posture: not_approved
- persistence posture: not_approved
- canonical routing field: condition_id, token_id, outcome
- non routing field: market_id
- derived identifier field: token_outcome_pair
- next ticket recommendation: stage3_strict_oos_split_contract_planning
- evidence status: probability_record_contract_planning_recorded
- label confidence: confirmed

Actual assignments:

- weather bot planning stage: weather_bot_stage3_probability_record_contract_planning
- immediate predecessor pr: pr_358
- ticket lifecycle status: docs_static_test_only
- ticket lifecycle status: contract_planning_only
- record contract status: requirements_defined
- record contract status: runtime_schema_not_created
- scoring target posture: venue_defined_settlement_outcome
- record immutability posture: immutable_after_accepted_creation_required
- correction posture: superseding_record_required
- probability domain: closed_unit_interval
- prediction representation: binary_outcome_probability
- prediction representation: full_predictive_distribution
- prediction representation: finite_ensemble
- time availability posture: prediction_as_of_required
- time availability posture: input_publication_availability_required
- label join posture: canonical_route_and_target_rule_required
- mismatch posture: fail_closed
- scoring execution posture: not_approved
- probability generation posture: not_approved
- persistence posture: not_approved
- canonical routing field: condition_id
- canonical routing field: token_id
- canonical routing field: outcome
- non routing field: market_id
- derived identifier field: token_outcome_pair
- next ticket recommendation: stage3_strict_oos_split_contract_planning
- evidence status: probability_record_contract_planning_recorded
- label confidence: confirmed

Hybrid/custom values are rejected. Missing assignments are rejected. Values outside the closed sets above are rejected.

## Acceptance criteria

- The artifact records PR #358 as the actual merged predecessor and records no superseding Weather Bot state.
- The future probability-prediction record common required fields are defined as requirements only.
- The prediction-representation matrix is conditional and representation-specific.
- Binary probability domain is the closed interval [0, 1].
- Temporal availability, no-lookahead, immutability, correction, label-join, missingness, and fail-closed requirements are explicit.
- Canonical routing remains exactly `condition_id`, `token_id`, and `outcome`; `market_id` remains non-routing only; `token_outcome_pair` remains derived only.
- The exact recommended next ticket is `WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01`.
