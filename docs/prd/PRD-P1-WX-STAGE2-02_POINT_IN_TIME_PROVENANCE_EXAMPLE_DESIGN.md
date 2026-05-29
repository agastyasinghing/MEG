# PRD-P1-WX-STAGE2-02: Point-in-Time Provenance Example Design

## 1. Status and scope

- Canonical ID: **PRD-P1-WX-STAGE2-02**.
- This is **Stage 2 point-in-time provenance example design only**.
- This follows `PRD-P1-WX-STAGE2-01`, the source-compatible historical-label design contract.
- This document defines representative provenance example designs only.
- This document does **not** create historical labels.
- This document does **not** create JSON/YAML/CSV/Parquet fixtures, seed example data, archive outputs, generated data, or provider output.
- This document does **not** approve provider integration, connectors, data ingestion, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, live market execution, or autonomy.
- This document does **not** approve provider credentials, external API calls, config loading, secret reading, historical label implementation, production behavior, profitability claims, or C++/Rust runtime components.
- The only implementation-like artifact paired with this document is a lightweight Python standard-library static validation test for this Markdown contract.

## 2. Strategic framing

The controlling source for the Weather Bot stage ladder and evidence gates is the **standalone MEG Weather Bot PRD** (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`). `PRD-P1-WX-STAGE1-CLOSEOUT-01` confirms that Stage 1 static/manual-labeling artifacts can hand off into Stage 2 design work without approving ingestion or scoring. `PRD-P1-WX-STAGE2-01` defines the source-compatible historical-label design contract that this ticket makes more concrete through representative point-in-time provenance example design patterns.

Weather Bot is not a generic weather API wrapper and is not a trading bot. It models prediction-market weather contracts as **source-defined settlement objects**. The future target remains:

`P(the venue-defined source/station/window/threshold/revision/classification rule resolves Yes)`

It is not:

`P(weather variable crosses threshold)`

Point-in-time provenance protects the source-defined settlement object from lookahead leakage. A future historical label must prove what information was available at the claimed decision time, what information was unavailable, and whether any source, station, forecast cycle, archive revision, or reviewer action happened after the decision point. This document provides representative designs only. It does not create real labels, real examples from live or historical markets, or source-backed historical observations.

## 3. Stage ladder position

The standalone MEG Weather Bot PRD defines the Weather Bot stage ladder as follows:

| Stage | Scope | Status in this ticket |
| --- | --- | --- |
| Stage 0 | Documentation and source-backed research only. | Completed before this ticket. |
| Stage 1 | Static examples and manual labels. | Closed by `PRD-P1-WX-STAGE1-CLOSEOUT-01`. |
| Stage 2 | Source-compatible historical labels with point-in-time provenance. | **This ticket is Stage 2 design only.** |
| Stage 3 | Retrospective probability scoring on strict OOS splits. | Unapproved. |
| Stage 4 | Trap-filtered paper simulation with executable quotes, fees, spreads, and depth assumptions. | Unapproved. |
| Stage 5 | Human-reviewed dry run with reviewer packets and override logs. | Unapproved. |
| Stage 6 | Runtime observation only under separate approval. | Unapproved. |
| Stage 7 | Execution/trading only after separate explicit approval. | Unapproved. |

Historical-label implementation, Stage 3 scoring, Stage 4 paper simulation, Stage 5 dry run, Stage 6 runtime observation, and Stage 7 execution/trading remain unapproved.

## 4. Provenance example design purpose

Representative point-in-time provenance examples are static reasoning aids for later Stage 2 work. They show how future labels should reason about timestamps, source availability, observation availability, archive revisions, station selection, reviewer timing, and label usability. They clarify what “available as of decision time” means without creating any historical-label row.

These examples are not data fixtures. They are not historical labels. They are not ingestion, provider, scoring, probability modeling, runtime, connector, or trading designs. They are Markdown-only planning templates that help future tickets decide whether a proposed label is usable, blocked pending provenance, blocked pending source match, or blocked pending adjudication.

## 5. Closed Stage 2 provenance example vocabulary

No other actual values are allowed for the machine-checkable fields below. Hybrid values, custom values, slash-combined values, and implementation-readiness terms are forbidden as actual values. If a scenario is nuanced, mixed, or partially supported, the conservative exact field value must be selected and the nuance must be written in reviewer notes or prose.

### provenance example design stage

Allowed values:

- `stage_2_provenance_example_design`

### provenance example type

Allowed values:

- `source_availability`
- `observation_availability`
- `market_timing`
- `archive_revision`
- `station_selection`
- `forecast_publication_time`
- `advisory_publication_time`
- `reviewer_label_time`
- `as_of_join`
- `finality_revision`
- `other_unclear`

### timestamp role

Allowed values:

- `decision_time`
- `market_open_time`
- `market_close_time`
- `resolution_time`
- `source_publication_time`
- `observation_valid_time`
- `observation_available_time`
- `archive_revision_time`
- `station_selection_time`
- `reviewer_label_time`
- `not_applicable`

### point-in-time availability status

Allowed values:

- `available_as_of`
- `unavailable_as_of`
- `ambiguous_as_of`
- `not_applicable`
- `design_only`

### leakage risk

Allowed values:

- `none_identified`
- `possible`
- `likely`
- `blocking`
- `unknown`

### provenance blocking reason

Allowed values:

- `none_identified`
- `missing_source_timestamp`
- `missing_observation_availability`
- `missing_archive_revision_record`
- `hindsight_station_selection`
- `final_archive_leakage`
- `future_forecast_cycle`
- `post_resolution_label_leakage`
- `unresolved_source_conflict`
- `other_unclear`

### label usability posture

Allowed values from `PRD-P1-WX-STAGE2-01`:

- `design_only`
- `usable_after_stage_2_approval`
- `blocked_pending_source_match`
- `blocked_pending_provenance`
- `blocked_pending_adjudication`

### evidence status

Allowed values:

- `source_backed`
- `reviewer_inferred`
- `missing`
- `conflicting`
- `not_applicable`

### label confidence

Allowed values:

- `confirmed`
- `unclear`
- `unknown`

## 6. Forbidden Stage 2 provenance example values

The following examples may appear only as forbidden examples in prose. They must not be used as actual machine-checkable field values:

- `available_as_of/unavailable_as_of`
- `possible/likely`
- `source_backed/reviewer_inferred`
- `confirmed/unclear`
- `design_only/usable_after_stage_2_approval`
- `missing_source_timestamp/final_archive_leakage`
- `partial`
- `mixed`
- `likely_confirmed`
- `maybe`
- `approved`
- `configured`
- `available`
- `trade_ready`
- `auto_execute`
- `autonomous`
- `live`
- `production`
- `provider_ready`
- `model_ready`
- `backtest_ready`
- `ready_for_ingestion`
- `ready_for_scoring`
- `ready_for_runtime`
- `ready_for_trading`
- `implementation_ready`
- `ingestion_ready`

## Machine-checkable Stage 2 provenance example assignments

- provenance example design stage: stage_2_provenance_example_design
- provenance example type: source_availability
- provenance example type: observation_availability
- provenance example type: market_timing
- provenance example type: archive_revision
- provenance example type: station_selection
- provenance example type: forecast_publication_time
- provenance example type: advisory_publication_time
- provenance example type: reviewer_label_time
- provenance example type: as_of_join
- provenance example type: finality_revision
- provenance example type: other_unclear
- timestamp role: decision_time
- timestamp role: market_open_time
- timestamp role: market_close_time
- timestamp role: resolution_time
- timestamp role: source_publication_time
- timestamp role: observation_valid_time
- timestamp role: observation_available_time
- timestamp role: archive_revision_time
- timestamp role: station_selection_time
- timestamp role: reviewer_label_time
- timestamp role: not_applicable
- point-in-time availability status: available_as_of
- point-in-time availability status: unavailable_as_of
- point-in-time availability status: ambiguous_as_of
- point-in-time availability status: not_applicable
- point-in-time availability status: design_only
- leakage risk: none_identified
- leakage risk: possible
- leakage risk: likely
- leakage risk: blocking
- leakage risk: unknown
- provenance blocking reason: none_identified
- provenance blocking reason: missing_source_timestamp
- provenance blocking reason: missing_observation_availability
- provenance blocking reason: missing_archive_revision_record
- provenance blocking reason: hindsight_station_selection
- provenance blocking reason: final_archive_leakage
- provenance blocking reason: future_forecast_cycle
- provenance blocking reason: post_resolution_label_leakage
- provenance blocking reason: unresolved_source_conflict
- provenance blocking reason: other_unclear
- label usability posture: design_only
- label usability posture: usable_after_stage_2_approval
- label usability posture: blocked_pending_source_match
- label usability posture: blocked_pending_provenance
- label usability posture: blocked_pending_adjudication
- evidence status: source_backed
- evidence status: reviewer_inferred
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown

## 8. Provenance timestamp model

The provenance timestamp model defines the timing roles future Stage 2 labels must be able to reason about before they can be used beyond design review:

- `decision_time`: the claimed as-of time for a hypothetical later decision, review, replay, or evaluation join. Evidence after this time cannot support an as-of claim for this time.
- `market_open_time`: the time the venue contract first becomes relevant for a future replay or label join.
- `market_close_time`: the time the contract stops accepting relevant decisions for the window being evaluated.
- `resolution_time`: the time the venue resolves, cancels, voids, or otherwise finalizes the contract outcome.
- `source_publication_time`: the time the resolver source publishes the relevant report, advisory, page, bulletin, or official value.
- `observation_valid_time`: the time or interval the weather observation represents.
- `observation_available_time`: the time the observation could actually have been inspected from the relevant source by a reviewer or future system.
- `archive_revision_time`: the time an archive, final report, quality-control layer, post-analysis product, or corrected source layer changes the value or status.
- `station_selection_time`: the time the station, source page, geographic proxy, or fallback station was specified for the contract or label.
- `reviewer_label_time`: the time a human reviewer records or updates a label judgment.
- `not_applicable`: used only when a timestamp role is not relevant to the representative design.

Valid time is not the same as available time: an observation can describe a past hour or day while being unavailable until later. Publication time is not the same as observation time: a daily, monthly, advisory, or final report can be published after the period it describes. Archive revision time must not be treated as original availability time because revised archives can reveal facts unavailable at the claimed decision time. Reviewer label time is not evidence availability time because a reviewer may label after resolution using evidence that did or did not exist earlier. Station selection time matters because hindsight station selection can leak outcome knowledge when a later reviewer chooses the station that best matches a desired outcome rather than the station specified before the result was known.

## 9. Representative provenance example format

Use this Markdown-only conceptual template for later representative examples. This is not a JSON schema, YAML schema, CSV fixture, Parquet fixture, data file, provider schema, loader contract, or ingestion script.

```text
provenance_example_id: human-readable Markdown identifier only
representative_or_source_backed_status: representative synthetic scenario, not historical label data
linked_stage2_design_concept: short reference to the Stage2-01 concept being illustrated
provenance example type: one exact allowed value

timeline summary:
- decision_time: conceptual as-of moment
- relevant timestamp roles: conceptual ordering only

timestamp roles used:
- one or more exact timestamp role values

point-in-time availability status: one exact allowed value
leakage risk: one exact allowed value
provenance blocking reason: one exact allowed value
label usability posture: one exact allowed value
evidence status: one exact allowed value
label confidence: one exact allowed value

reviewer notes: prose nuance and conservative interpretation
source notes or synthetic-example note: state whether the example is synthetic; no real source row is created
non-approval reminder: no ingestion, scoring, runtime, paper simulation, trading, order placement, or autonomy
```

## 10. Representative provenance scenarios

The scenarios below are representative synthetic scenario designs, not historical label data. They show how future labels should reason about provenance. They do not create source-backed rows, fixtures, or market labels.

### Representative provenance scenario 1: source_availability before decision time

- Label: **Representative synthetic scenario, not historical label data**.
- provenance example type: `source_availability`.
- Timeline summary: a venue rule says resolution depends on a named official source page. The conceptual `source_publication_time` occurs before the conceptual `decision_time`, and the future reviewer can document that the source page was already available at that as-of moment.
- Timestamp roles involved: `source_publication_time`, `decision_time`, `resolution_time`, `reviewer_label_time`.
- point-in-time availability status: `available_as_of`.
- leakage risk: `none_identified`.
- provenance blocking reason: `none_identified`.
- label usability posture: `usable_after_stage_2_approval`.
- evidence status: `source_backed`.
- label confidence: `confirmed`.
- What would block future label use: missing proof of source publication time, an unresolved source mismatch, or inability to show that the source was available before decision time.
- Non-approval reminder: this scenario does not approve provider integration, connectors, external API calls, ingestion, historical label implementation, scoring, runtime observation, trading, order placement, or autonomy.

### Representative provenance scenario 2: observation_availability lags observation_valid_time

- Label: **Representative synthetic scenario, not historical label data**.
- provenance example type: `observation_availability`.
- Timeline summary: an observation has an `observation_valid_time` before `decision_time`, but its `observation_available_time` is after `decision_time`. A future label cannot treat the valid time as evidence availability.
- Timestamp roles involved: `observation_valid_time`, `observation_available_time`, `decision_time`, `market_close_time`.
- point-in-time availability status: `unavailable_as_of`.
- leakage risk: `likely`.
- provenance blocking reason: `missing_observation_availability`.
- label usability posture: `blocked_pending_provenance`.
- evidence status: `missing`.
- label confidence: `unknown`.
- What would block future label use: lack of a source-backed availability timestamp showing when the observation could have been inspected.
- Non-approval reminder: this scenario does not approve data ingestion, forecast pulls, provider credentials, model scoring, probability scoring, backtesting, paper simulation, runtime observation, or trading.

### Representative provenance scenario 3: archive_revision changes the apparent value

- Label: **Representative synthetic scenario, not historical label data**.
- provenance example type: `archive_revision`.
- Timeline summary: the first posted source layer appears before `decision_time`, but a later final archive layer at `archive_revision_time` changes or confirms the settlement value after `market_close_time`. A future label must not use the later final archive as if it were available at decision time.
- Timestamp roles involved: `source_publication_time`, `decision_time`, `market_close_time`, `archive_revision_time`, `resolution_time`.
- point-in-time availability status: `ambiguous_as_of`.
- leakage risk: `blocking`.
- provenance blocking reason: `final_archive_leakage`.
- label usability posture: `blocked_pending_provenance`.
- evidence status: `conflicting`.
- label confidence: `unclear`.
- What would block future label use: no record distinguishing first-posted values from revised archive values, or no archive revision record.
- Non-approval reminder: this scenario does not create archive data, JSON/YAML/CSV/Parquet fixtures, data loaders, backtesting, paper simulation, runtime behavior, or order placement.

### Representative provenance scenario 4: station_selection after outcome knowledge

- Label: **Representative synthetic scenario, not historical label data**.
- provenance example type: `station_selection`.
- Timeline summary: a contract headline describes a city, but the station is selected by a future reviewer only after the outcome is known. Without a pre-result `station_selection_time`, the station choice can encode hindsight.
- Timestamp roles involved: `station_selection_time`, `decision_time`, `resolution_time`, `reviewer_label_time`.
- point-in-time availability status: `ambiguous_as_of`.
- leakage risk: `blocking`.
- provenance blocking reason: `hindsight_station_selection`.
- label usability posture: `blocked_pending_source_match`.
- evidence status: `reviewer_inferred`.
- label confidence: `unclear`.
- What would block future label use: station not specified by the venue rule, no source-backed station metadata at decision time, or reviewer-selected proxy station after resolution.
- Non-approval reminder: this scenario does not approve a provider connector, convenience API source mapping, ingestion, scoring, live market execution, or autonomy.

### Representative provenance scenario 5: forecast_publication_time after market close

- Label: **Representative synthetic scenario, not historical label data**.
- provenance example type: `forecast_publication_time`.
- Timeline summary: a forecast cycle is initialized before `market_close_time`, but the public forecast product is not published until after `market_close_time`. The initialization time alone does not prove as-of availability.
- Timestamp roles involved: `decision_time`, `market_close_time`, `source_publication_time`, `not_applicable`.
- point-in-time availability status: `unavailable_as_of`.
- leakage risk: `possible`.
- provenance blocking reason: `future_forecast_cycle`.
- label usability posture: `blocked_pending_provenance`.
- evidence status: `missing`.
- label confidence: `unknown`.
- What would block future label use: missing publication timestamp, use of a future forecast cycle, or failure to prove the forecast was public before the decision point.
- Non-approval reminder: this scenario does not approve forecast pulls, forecast modeling, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.

## 11. No-lookahead leakage examples

- **Final archive leakage:** a future label uses a final official archive value as if it had been available at `decision_time`. This is dangerous because archive quality control or post-analysis can revise preliminary values. Future labels must prove whether the venue rule uses first-posted, final archive, or another finality layer, and must record `archive_revision_time` when revision matters.
- **Future forecast cycle leakage:** a future label or scoring replay uses a forecast product that was issued or published after the claimed as-of moment. This is dangerous because it imports information unavailable to the market participant or reviewer. Future labels must prove `source_publication_time`, not only cycle initialization or valid time.
- **Post-resolution label leakage:** a reviewer records a label after `resolution_time` and accidentally treats the post-resolution result as if it were available before close. This is dangerous because it collapses settlement outcome into the decision-time evidence set. Future labels must distinguish `reviewer_label_time` from `source_publication_time` and `observation_available_time`.
- **Hindsight station selection:** a reviewer selects the station or source page after seeing which station crosses a threshold. This is dangerous because station choice becomes outcome-dependent. Future labels must prove the `station_selection_time` and source rule before the outcome was known.
- **Source publication timestamp missing:** a future label has a source value but no source publication timestamp. This is dangerous because the value may have appeared after the as-of claim. Future labels must prove source availability or remain blocked pending provenance.
- **Observation valid time mistaken for availability time:** a label treats a timestamp describing the measurement window as the time the evidence could be inspected. This is dangerous because valid observations can be posted, corrected, or archived later. Future labels must separately record `observation_valid_time` and `observation_available_time`.

## 12. Relationship to Stage 2 historical-label design

`PRD-P1-WX-STAGE2-01` defines the historical-label design contract. This ticket defines representative provenance examples/templates that explain how to apply that contract to availability, timestamp, revision, station, and reviewer-timing questions. Future labels must link provenance evidence to label usability posture.

No labels are created here. No ingestion is created here. No data files are created here. No JSON/YAML/CSV/Parquet fixtures are created here. No provider integration, connector behavior, scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy is created here.

## 13. Relationship to future Stage 3 scoring

Stage 3 scoring remains unapproved. Future scoring requires source-compatible historical labels. Source-compatible historical labels require point-in-time provenance. Scoring without point-in-time provenance risks lookahead leakage because it can evaluate decisions using facts, revisions, station choices, or final outcomes that were unavailable at the claimed time.

This ticket only prepares provenance design examples for later review. It does not approve Stage 3 probability scoring, model scoring, forecast modeling, backtesting, paper simulation, runtime observation, trading, position sizing, order placement, or autonomy.

## 14. Language/tooling posture

Stage 2 provenance example design remains Markdown plus Python standard-library static tests only. No C++/Rust or other performance-oriented language is appropriate at this stage. Python remains the default for future design/static validation because the work is document validation, not runtime computation. Any C++/Rust consideration requires a later approved implementation stage, profiling evidence, a proven hot path, and a separate approval gate. This ticket adds no C++/Rust runtime components.

## 15. Non-approval boundaries for provenance examples

Stage 2 provenance example design does not approve:

- provider integration
- connectors
- connector implementation
- provider credentials
- external API calls
- live weather API use
- config loading
- secret reading
- data ingestion
- historical labels
- historical label implementation
- JSON/YAML/CSV/Parquet fixtures
- JSON/YAML/CSV/Parquet fixture creation
- forecast pulls
- forecast modeling
- model scoring
- probability modeling
- probability scoring
- backtesting
- paper simulation
- runtime observation
- trading
- trading strategy
- position sizing
- order placement
- live market execution
- autonomy
- profitability claims
- C++/Rust runtime components

## 16. Later-ticket handoff

Later tickets may address the following only after explicit approval and within their own allowed scope:

- Future Stage 2 historical-label schema refinement only if needed.
- Future point-in-time provenance static example expansion only if needed.
- Future historical-label implementation or fixture creation only after separate approval.
- Future ingestion design only after separate approval.
- Future Stage 3 probability scoring only after Stage 2 labels exist and pass gates.
- Any implementation-adjacent work to later stages only after explicit approval.

## 17. Acceptance criteria

This document is complete only if:

- [x] `PRD-P1-WX-STAGE2-02` canonical ID is present.
- [x] Standalone Weather Bot PRD is referenced.
- [x] `PRD-P1-WX-STAGE1-CLOSEOUT-01` is referenced.
- [x] `PRD-P1-WX-STAGE2-01` is referenced.
- [x] Stage 2 design scope is explicit.
- [x] Provenance timestamp model is included.
- [x] Representative provenance example format is included.
- [x] 4 to 6 representative synthetic provenance scenarios are included.
- [x] Required scenarios are covered: `source_availability`, `observation_availability`, `archive_revision`, and `station_selection`.
- [x] No-lookahead leakage examples are included.
- [x] Relationship to Stage 2 historical-label design is defined.
- [x] Relationship to Stage 3 scoring is defined without approving scoring.
- [x] Language/tooling posture is included.
- [x] All closed sets are listed exactly.
- [x] Machine-checkable assignment section exists.
- [x] Actual machine-checkable assignments use only allowed values.
- [x] Forbidden examples are documented without being used as actual field values.
- [x] Non-approval boundaries are explicit.
- [x] Later-ticket handoff is clear.
- [x] No implementation behavior is introduced.
