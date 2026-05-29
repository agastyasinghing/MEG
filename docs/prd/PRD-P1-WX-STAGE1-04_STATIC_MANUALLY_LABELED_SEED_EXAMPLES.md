# PRD-P1-WX-STAGE1-04: Static Manually Labeled Seed Examples

## 1. Status and scope

`PRD-P1-WX-STAGE1-04` is **Stage 1 only** static seed-example work for MEG Weather Bot planning. It builds on:

- `PRD-P1-WX-STAGE1-01` static canonical weather-event manual-label schema and example template.
- `PRD-P1-WX-STAGE1-02` static trap-label fixture/template.
- `PRD-P1-WX-STAGE1-03` reviewer checklist/adjudication protocol.
- The **standalone MEG Weather Bot PRD** (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`) as the source for the Stage ladder and strategic framing.

This document defines seed examples only. The examples are Markdown-only, static, reviewer-facing, and non-ingested. They are not live/current markets unless explicitly source-backed; the examples below are representative synthetic examples, not live market data.

This document does not create historical labels, JSON/YAML/CSV fixtures, provider integration, connectors, data ingestion, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy. It does not approve provider credentials, config loading, secret reading, external API calls, connector implementation, live weather API use, seed example data files, forecast modeling, trading strategy, position sizing, live market execution, or profitability claims.

## 2. Strategic framing

The standalone MEG Weather Bot PRD frames Weather Bot as a system for modeling prediction-market weather contracts as **source-defined settlement objects**, not as a generic weather API wrapper and not as a trading bot. The target is not simply `P(weather variable crosses threshold)`. The target is `P(the venue-defined source/station/window/threshold/revision/classification rule resolves Yes)`.

`PRD-P1-WX-STAGE1-01` supplies the manual-label schema for canonical weather-event mapping. `PRD-P1-WX-STAGE1-02` supplies the trap-label vocabulary for ambiguity, false-equivalence, and false-edge risks. `PRD-P1-WX-STAGE1-03` supplies the reviewer adjudication protocol that decides whether a proposed label should pass, be revised, be escalated, be blocked, or be deferred.

These static seed examples demonstrate how manual labels, trap labels, and reviewer adjudication work together on source-defined settlement objects. They are needed before historical labels, scoring, and backtesting because a later label or score is only meaningful if the contract object has been mapped to the correct venue-defined source, station or location, window, threshold, revision rule, and classification authority.

## 3. Stage ladder position

The standalone MEG Weather Bot PRD defines the Stage ladder:

- **Stage 0**: documentation and source-backed research only.
- **Stage 1**: static examples and manual labels.
- **Stage 2**: source-compatible historical labels with point-in-time provenance.
- **Stage 3**: retrospective probability scoring on strict OOS splits.
- **Stage 4**: trap-filtered paper simulation with executable quotes, fees, spreads, and depth assumptions.
- **Stage 5**: human-reviewed dry run with reviewer packets and override logs.
- **Stage 6**: runtime observation only under separate approval.
- **Stage 7**: execution/trading only after separate explicit approval.

This ticket is **Stage 1 only**. Stage 2 historical labels, Stage 3 scoring, Stage 4 paper simulation, Stage 5 dry run, Stage 6 runtime observation, and Stage 7 execution/trading remain unapproved and outside this document.

## 4. Seed-example purpose

The static seed examples are for reviewer training, future design discussion, and static documentation testing. They show how to read a weather-market question as a source-defined settlement object and how to keep one conservative closed-set value in each actual field while placing nuance in notes.

They are reviewer-facing examples, not data fixtures. They are for future review/design/testing only. They should teach future Codex tickets how to apply the Stage 1 manual-label schema, trap-label template, and adjudication protocol without creating runtime behavior, ingestion behavior, provider behavior, scoring behavior, or trading behavior.

## 5. Closed seed-example field vocabulary

No other actual values are allowed for the fields in this section. Hybrid, custom, and slash-combined values are forbidden as actual values. If a condition is mixed or partially supported, choose the single most conservative exact field value and place nuance in notes or prose.

### seed example stage

Allowed value:

- `stage_1_static_seed_example`

### market family

Allowed values:

- `temperature_threshold`
- `precipitation_threshold`
- `snowfall`
- `wind_gust`
- `storm_hurricane`
- `severe_extreme_weather`
- `daily_city_location_binary`
- `monthly_seasonal_aggregate`
- `source_dependent_resolution`
- `other_unclear`

### canonical mapping decision

Allowed values:

- `exact_equivalent`
- `near_equivalent`
- `related_non_equivalent`
- `incompatible`
- `unclear`

### resolver/source role

Allowed values:

- `official_resolver`
- `official_weather_source`
- `station_observation_source`
- `climate_archive_source`
- `forecast_model_provider`
- `historical_data_provider`
- `convenience_api`
- `venue_discretionary_resolver`
- `unknown`

### trap source

Allowed values:

- `market_wording`
- `resolution_source`
- `provider_source`
- `location_station`
- `time_window`
- `threshold_unit`
- `measurement_method`
- `data_revision`
- `venue_discretion`
- `external_event_classification`
- `market_microstructure`
- `validation_provenance`
- `other_unclear`

### trap severity

Allowed values:

- `caution`
- `blocking`

### false-edge risk

Allowed values:

- `none_identified`
- `possible_false_edge`
- `likely_false_edge`
- `blocking_false_edge`
- `unclear`

### canonical mapping impact

Allowed values:

- `no_material_impact`
- `mapping_unclear`
- `near_equivalence_only`
- `non_equivalent`
- `mapping_blocked`

### adjudication outcome

Allowed values:

- `accepted`
- `revised`
- `escalated`
- `blocked`
- `deferred`

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

### review posture

Allowed values:

- `informational`
- `review_only`
- `blocked`

### reviewer workflow state

Allowed values:

- `unreviewed`
- `caution_under_review`
- `blocking_under_review`
- `reviewed_pass`
- `reviewed_caution`
- `reviewed_block`

## 6. Forbidden seed-example values

The following strings are examples of forbidden actual values. They may appear only as forbidden examples in prose, not as actual machine-checkable field values:

- `confirmed/unclear`
- `caution/blocking`
- `accepted/revised`
- `source_backed/reviewer_inferred`
- `exact_equivalent/near_equivalent`
- `review_only/blocked`
- `possible_false_edge/likely_false_edge`
- `market_wording/resolution_source`
- `partial`
- `mixed`
- `likely`
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

## Machine-checkable seed-example field assignments

- seed example stage: stage_1_static_seed_example
- market family: temperature_threshold
- market family: precipitation_threshold
- market family: snowfall
- market family: wind_gust
- market family: storm_hurricane
- market family: severe_extreme_weather
- market family: daily_city_location_binary
- market family: monthly_seasonal_aggregate
- market family: source_dependent_resolution
- market family: other_unclear
- canonical mapping decision: exact_equivalent
- canonical mapping decision: near_equivalent
- canonical mapping decision: related_non_equivalent
- canonical mapping decision: incompatible
- canonical mapping decision: unclear
- resolver/source role: official_resolver
- resolver/source role: official_weather_source
- resolver/source role: station_observation_source
- resolver/source role: climate_archive_source
- resolver/source role: forecast_model_provider
- resolver/source role: historical_data_provider
- resolver/source role: convenience_api
- resolver/source role: venue_discretionary_resolver
- resolver/source role: unknown
- trap source: market_wording
- trap source: resolution_source
- trap source: provider_source
- trap source: location_station
- trap source: time_window
- trap source: threshold_unit
- trap source: measurement_method
- trap source: data_revision
- trap source: venue_discretion
- trap source: external_event_classification
- trap source: market_microstructure
- trap source: validation_provenance
- trap source: other_unclear
- trap severity: caution
- trap severity: blocking
- false-edge risk: none_identified
- false-edge risk: possible_false_edge
- false-edge risk: likely_false_edge
- false-edge risk: blocking_false_edge
- false-edge risk: unclear
- canonical mapping impact: no_material_impact
- canonical mapping impact: mapping_unclear
- canonical mapping impact: near_equivalence_only
- canonical mapping impact: non_equivalent
- canonical mapping impact: mapping_blocked
- adjudication outcome: accepted
- adjudication outcome: revised
- adjudication outcome: escalated
- adjudication outcome: blocked
- adjudication outcome: deferred
- evidence status: source_backed
- evidence status: reviewer_inferred
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown
- review posture: informational
- review posture: review_only
- review posture: blocked
- reviewer workflow state: unreviewed
- reviewer workflow state: caution_under_review
- reviewer workflow state: blocking_under_review
- reviewer workflow state: reviewed_pass
- reviewer workflow state: reviewed_caution
- reviewer workflow state: reviewed_block

## 8. Seed example format

Each seed example uses this Markdown-only structure:

- `seed_example_id`
- `representative_or_source_backed_status`
- `market family`
- `synthetic raw market wording`
- `source-defined settlement object summary`
- `manual-label summary`
- `trap-label summary`
- `reviewer adjudication summary`
- `closed-set values used`
- `human-review note`
- `non-approval reminder`
- `source notes or synthetic-example note`

The `closed-set values used` line in each example is reviewer-facing narrative, not an additional machine-checkable assignment block. Static tests parse actual field assignments only from the dedicated machine-checkable assignment section above.

## 9. Seed examples

### Seed example 1: temperature threshold with pinned station and daily high

- `seed_example_id`: `wx_seed_001_temperature_threshold`
- `representative_or_source_backed_status`: Representative synthetic example, not live market data.
- `market family`: `temperature_threshold`
- `synthetic raw market wording`: "Will the official daily high temperature at Station AAA reach at least 90 degrees F on the named local calendar date?"
- `source-defined settlement object summary`: The settlement object is the venue-defined official station observation for Station AAA, the local calendar-day maximum temperature window, the degrees-F threshold, and the named source's final or contract-specified report rule.
- `manual-label summary`: Stage1-01 concepts map the family, station, variable, comparator, unit, local-day window, source role, revision rule, and confidence. Because the synthetic wording pins one station and one unit, the manual label can be treated as an example of a safe exact mapping if the resolver source is truly the stated station product.
- `trap-label summary`: Stage1-02 concepts still flag threshold/unit and data-revision traps as cautionary because a daily climate report, an intraday observation, and a later archive can disagree near the threshold.
- `reviewer adjudication summary`: Stage1-03 review would accept the example for static teaching only after verifying that the source/station/window/threshold fields are all explicit in the wording.
- `closed-set values used`: `stage_1_static_seed_example`, `temperature_threshold`, `exact_equivalent`, `station_observation_source`, `threshold_unit`, `caution`, `possible_false_edge`, `no_material_impact`, `accepted`, `reviewer_inferred`, `unclear`, `review_only`, `reviewed_caution`.
- `human-review note`: Safe does not mean actionable; it means the synthetic text demonstrates a clear settlement-object mapping pattern.
- `non-approval reminder`: This example does not approve provider integration, connectors, external API calls, data ingestion, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.
- `source notes or synthetic-example note`: Representative synthetic example, not live market data; no external source was queried.

### Seed example 2: precipitation threshold with city wording and unspecified station

- `seed_example_id`: `wx_seed_002_precipitation_threshold`
- `representative_or_source_backed_status`: Representative synthetic example, not live market data.
- `market family`: `precipitation_threshold`
- `synthetic raw market wording`: "Will City BBB receive more than 1 inch of rain tomorrow?"
- `source-defined settlement object summary`: The settlement object is unclear because the city name, station, source product, local-day boundary, precipitation measurement method, trace handling, and revision/finality rule are not pinned.
- `manual-label summary`: Stage1-01 concepts would label this as a related weather question but not an exact source-defined settlement object. The reviewer should not infer a default airport station or convenience provider.
- `trap-label summary`: Stage1-02 concepts identify market wording, location/station, time-window, measurement-method, and provider-source traps. Convenience API precipitation totals would be especially unsafe if they are not the official resolver truth.
- `reviewer adjudication summary`: Stage1-03 review should block the mapping until the source, station/location, day boundary, and measurement rule are specified.
- `closed-set values used`: `stage_1_static_seed_example`, `precipitation_threshold`, `unclear`, `unknown`, `location_station`, `blocking`, `blocking_false_edge`, `mapping_blocked`, `blocked`, `missing`, `unknown`, `blocked`, `reviewed_block`.
- `human-review note`: The safest field choice is conservative blocking, with nuance captured here rather than with hybrid actual values.
- `non-approval reminder`: This example does not approve provider integration, connectors, external API calls, data ingestion, historical labels, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.
- `source notes or synthetic-example note`: Representative synthetic example, not live market data; no external source was queried.

### Seed example 3: snowfall accumulation with source and revision ambiguity

- `seed_example_id`: `wx_seed_003_snowfall`
- `representative_or_source_backed_status`: Representative synthetic example, not live market data.
- `market family`: `snowfall`
- `synthetic raw market wording`: "Will Location CCC record at least 6 inches of snowfall during the storm period?"
- `source-defined settlement object summary`: The settlement object depends on the venue-defined snowfall source, station or reporting area, storm-period start and end, accumulation method, trace and rounding rules, and whether revised climate archive values can change settlement.
- `manual-label summary`: Stage1-01 concepts can identify the candidate family and threshold but cannot safely finalize the mapping unless the source product, station/location, window, and revision rule are explicit.
- `trap-label summary`: Stage1-02 concepts flag time-window, measurement-method, location/station, and data-revision traps. Storm-period wording can hide non-equivalent windows across sources.
- `reviewer adjudication summary`: Stage1-03 review should revise or escalate if a reviewer can obtain source-backed wording; otherwise it remains a cautionary or blocked teaching example depending on missing fields.
- `closed-set values used`: `stage_1_static_seed_example`, `snowfall`, `near_equivalent`, `official_weather_source`, `time_window`, `caution`, `likely_false_edge`, `near_equivalence_only`, `revised`, `reviewer_inferred`, `unclear`, `review_only`, `caution_under_review`.
- `human-review note`: The example demonstrates that a near-equivalent weather event is not necessarily the same source-defined settlement object.
- `non-approval reminder`: This example does not approve provider integration, connectors, external API calls, provider credentials, config loading, secret reading, data ingestion, historical labels, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.
- `source notes or synthetic-example note`: Representative synthetic example, not live market data; no external source was queried.

### Seed example 4: wind gust threshold with measurement-method mismatch

- `seed_example_id`: `wx_seed_004_wind_gust`
- `representative_or_source_backed_status`: Representative synthetic example, not live market data.
- `market family`: `wind_gust`
- `synthetic raw market wording`: "Will the official airport station report a wind gust of 50 mph or higher during the event window?"
- `source-defined settlement object summary`: The settlement object is the specified airport station's official wind-gust observation, the event window, mph threshold, gust measurement method, and the contract's publication/finality rule.
- `manual-label summary`: Stage1-01 concepts can map source, station, variable, threshold, unit, and time window if the contract names the official station and source product.
- `trap-label summary`: Stage1-02 concepts flag measurement-method and validation-provenance traps because a nearby mesonet, convenience API, or forecast-provider gust value may be related but non-equivalent to the official station observation.
- `reviewer adjudication summary`: Stage1-03 review accepts the teaching pattern only if the example stays review-only and rejects convenience-provider substitution.
- `closed-set values used`: `stage_1_static_seed_example`, `wind_gust`, `related_non_equivalent`, `station_observation_source`, `measurement_method`, `caution`, `possible_false_edge`, `non_equivalent`, `accepted`, `reviewer_inferred`, `unclear`, `review_only`, `reviewed_caution`.
- `human-review note`: This is a source-compatibility lesson: a higher nearby gust does not settle the contract unless the venue-defined source says so.
- `non-approval reminder`: This example does not approve provider integration, connectors, external API calls, data ingestion, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.
- `source notes or synthetic-example note`: Representative synthetic example, not live market data; no external source was queried.

### Seed example 5: storm/hurricane classification tied to advisory authority

- `seed_example_id`: `wx_seed_005_storm_hurricane`
- `representative_or_source_backed_status`: Representative synthetic example, not live market data.
- `market family`: `storm_hurricane`
- `synthetic raw market wording`: "Will Storm DDD be classified as a hurricane by the named official advisory center before the deadline?"
- `source-defined settlement object summary`: The settlement object is the venue-defined classification authority, advisory product, deadline, storm identity, and whether real-time advisory status or later reanalysis controls resolution.
- `manual-label summary`: Stage1-01 concepts identify the family, classification authority, time cutoff, and revision/finality rule as load-bearing fields.
- `trap-label summary`: Stage1-02 concepts flag external-event-classification and data-revision traps because advisory-time classification and later best-track-style reanalysis can be related but incompatible settlement objects.
- `reviewer adjudication summary`: Stage1-03 review escalates unless the wording clearly specifies the advisory authority, cutoff, and finality rule.
- `closed-set values used`: `stage_1_static_seed_example`, `storm_hurricane`, `incompatible`, `official_resolver`, `external_event_classification`, `blocking`, `blocking_false_edge`, `mapping_blocked`, `escalated`, `conflicting`, `unknown`, `blocked`, `blocking_under_review`.
- `human-review note`: This example teaches that event classification is a resolver object, not just a meteorological description.
- `non-approval reminder`: This example does not approve provider integration, connectors, external API calls, data ingestion, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.
- `source notes or synthetic-example note`: Representative synthetic example, not live market data; no external source was queried.

## 10. Cross-example lessons

- Source, station, window, threshold, unit, measurement method, revision rule, and classification authority are settlement-object fields, not optional metadata.
- False equivalence is dangerous because two weather questions can be intuitively similar while resolving from different sources, stations, windows, reports, or classification authorities.
- Provider convenience data is not resolver truth unless the venue-defined settlement rule makes that provider the official resolver source.
- Traps may make a mapping cautionary or blocked even when the raw weather concept is easy to understand.
- Static seed examples are not historical labels, backtests, model inputs, probability claims, executable signals, or paper-trade records.

## 11. Non-approval boundaries for seed examples

Seed examples do not approve:

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
- seed example data files
- forecast pulls
- forecast modeling
- model scoring
- probability modeling
- probability scoring
- backtesting
- paper simulation
- runtime observation
- trading strategy
- position sizing
- trading
- order placement
- live market execution
- autonomy
- profitability claims

## 12. Later-ticket handoff

- Additional Stage 1 seed examples may be added only in later Stage 1 expansion tickets if needed.
- Stage 2 source-compatible historical labels belong to a future Stage 2 ticket only after Stage 1 is complete and explicitly gated.
- Probability scoring and backtesting belong to later stages only after the required gates and source-compatible label design exist.
- Any implementation-adjacent work belongs to later stages only after explicit approval; this document is not that approval.

## 13. Acceptance criteria

This document is complete only if:

- [x] `PRD-P1-WX-STAGE1-04` canonical ID is present.
- [x] The standalone Weather Bot PRD is referenced.
- [x] `PRD-P1-WX-STAGE1-01` is referenced.
- [x] `PRD-P1-WX-STAGE1-02` is referenced.
- [x] `PRD-P1-WX-STAGE1-03` is referenced.
- [x] Stage 1 scope is explicit.
- [x] The source-defined settlement object thesis is preserved.
- [x] Seed examples are Markdown-only and static.
- [x] Examples are labeled representative synthetic unless source-backed.
- [x] 4 to 6 seed examples are included.
- [x] Required market families are covered.
- [x] Manual-label, trap-label, and adjudication summaries are included.
- [x] All closed sets are listed exactly.
- [x] Machine-checkable assignment section exists.
- [x] Actual machine-checkable assignments use only allowed values.
- [x] Forbidden examples are documented without being used as actual field values.
- [x] Non-approval boundaries are explicit.
- [x] Later-ticket handoff is clear.
- [x] No implementation behavior is introduced.
