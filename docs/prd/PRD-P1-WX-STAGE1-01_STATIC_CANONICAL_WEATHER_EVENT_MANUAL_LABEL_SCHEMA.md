# PRD-P1-WX-STAGE1-01: Static Canonical Weather-Event Manual-Label Schema

## 1. Status and scope
- This ticket is **Stage 1 only** and begins Stage 1 after the standalone MEG Weather Bot PRD Stage 0 posture.
- This document is **static examples/manual labels only**.
- This document defines a **manual-label schema and example template only** for canonical weather-event mapping.
- This document does **not** approve provider integration, connectors, provider credentials, external API calls, config loading, secret reading, data ingestion, historical labels, forecast pulls, model scoring, probability modeling, backtesting, runtime observation, trading strategy, position sizing, order placement, live market execution, autonomy, or profitability claims.

## 2. Strategic framing
- Controlling Stage-0 synthesis reference: **standalone MEG Weather Bot PRD** (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`).
- Core thesis preserved: weather markets are **source-defined settlement objects**.
- The target is not `P(weather variable crosses threshold)`.
- The target is `P(the venue-defined source/station/window/threshold/revision/classification rule resolves Yes)`.
- The target is the venue-defined source/station/window/threshold/revision/classification rule resolution object.
- Manual labels are required before Stage 2 historical labels, Stage 3 scoring, or Stage 4 backtesting/paper simulation because the canonical weather-event mapping contract must be unambiguous first.

## 3. Stage ladder position
- Stage 0: documentation and source-backed research only.
- **Stage 1: static examples and manual labels (this ticket).**
- Stage 2: source-compatible historical labels with point-in-time provenance.
- Stage 3: retrospective probability scoring on strict OOS splits.
- Stage 4: trap-filtered paper simulation with executable quotes, fees, spreads, and depth assumptions.
- Stage 5: human-reviewed dry run with reviewer packets and override logs.
- Stage 6: runtime observation only under separate approval.
- Stage 7: execution/trading only after separate explicit approval.

Stage 2 through Stage 7 remain unapproved in this ticket.

## 4. Manual-label schema purpose
- Define a static manual-label schema for reviewer-authored examples.
- Ensure labels are static reviewer-created examples and not ingested historical data.
- Help reviewers map raw market wording into canonical weather-event fields.
- Provide a stable documentation and static-test contract for later review/design/testing tickets.

## 5. Closed manual-label field vocabulary
No other actual values are allowed for closed-set machine-checkable assignments.

- manual label stage: `stage_1_static_manual_label`
- market family: `temperature_threshold`, `precipitation_threshold`, `snowfall`, `wind_gust`, `storm_hurricane`, `severe_extreme_weather`, `daily_city_location_binary`, `monthly_seasonal_aggregate`, `source_dependent_resolution`, `other_unclear`
- canonical mapping decision: `exact_equivalent`, `near_equivalent`, `related_non_equivalent`, `incompatible`, `unclear`
- resolver/source role: `official_resolver`, `official_weather_source`, `station_observation_source`, `climate_archive_source`, `forecast_model_provider`, `historical_data_provider`, `convenience_api`, `venue_discretionary_resolver`, `unknown`
- label confidence: `confirmed`, `unclear`, `unknown`
- trap severity: `caution`, `blocking`
- review posture: `informational`, `review_only`, `blocked`
- reviewer workflow state: `unreviewed`, `caution_under_review`, `blocking_under_review`, `reviewed_pass`, `reviewed_caution`, `reviewed_block`

Hybrid/custom/slash values are forbidden as actual field assignments. Nuance belongs in notes/prose fields.

## 6. Forbidden manual-label values
Forbidden examples may appear only as forbidden examples in prose, not as actual field values:
- `confirmed/unclear`
- `exact_equivalent/near_equivalent`
- `caution/blocking`
- `review_only/blocked`
- `station_observation_source/convenience_api`
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

## Machine-checkable manual-label field assignments
- manual label stage: stage_1_static_manual_label
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
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown
- trap severity: caution
- trap severity: blocking
- review posture: informational
- review posture: review_only
- review posture: blocked
- reviewer workflow state: unreviewed
- reviewer workflow state: caution_under_review
- reviewer workflow state: blocking_under_review
- reviewer workflow state: reviewed_pass
- reviewer workflow state: reviewed_caution
- reviewer workflow state: reviewed_block

## 8. Static manual-label schema
- `label_id`
- `manual_label_stage`
- `reviewer_workflow_state`
- `review_posture`
- `raw_market_title`
- `raw_market_rules_excerpt`
- `venue_name`
- `venue_market_url_or_reference`
- `market_family`
- `canonical_mapping_decision`
- `canonical_event_summary`
- `venue_defined_settlement_rule`
- `resolver/source_role`
- `resolver/source_name`
- `resolver/source_url_or_reference`
- `location_text`
- `station_or_observation_point`
- `geographic_precision_note`
- `weather_variable`
- `threshold_value`
- `threshold_unit`
- `comparator`
- `measurement_window_text`
- `timezone_or_local_day_rule`
- `aggregation_method`
- `revision_or_finality_rule`
- `classification_authority`
- `source_compatibility_notes`
- `trap_flags`
- `primary_trap_severity`
- `label_confidence`
- `ambiguity_notes`
- `reviewer_notes`
- `non_approval_notes`
- `source_notes`

## 9. Field definitions
Each field is required unless explicitly marked optional by reviewer judgment. Uncertainty is recorded in `ambiguity_notes`, `reviewer_notes`, `source_compatibility_notes`, and `source_notes` while closed-set fields keep one exact allowed value.

- `label_id`: reviewer-managed identifier for the static label template row.
- `manual_label_stage`: must use closed set `stage_1_static_manual_label`.
- `reviewer_workflow_state`: review lifecycle state; closed set applies.
- `review_posture`: WX-04-aligned review posture closed set applies.
- `raw_market_title`: exact venue headline text excerpt.
- `raw_market_rules_excerpt`: exact settlement-relevant rule snippet.
- `venue_name`: market venue identity.
- `venue_market_url_or_reference`: non-runtime reference link/string.
- `market_family`: family classification; closed set applies.
- `canonical_mapping_decision`: mapping relationship decision; closed set applies.
- `canonical_event_summary`: plain-English canonical event interpretation.
- `venue_defined_settlement_rule`: normalized settlement-rule summary.
- `resolver/source_role`: source-role classification; closed set applies.
- `resolver/source_name`: named resolver/source artifact.
- `resolver/source_url_or_reference`: citation/reference to the resolver source.
- `location_text`: venue location wording.
- `station_or_observation_point`: station/point controlling settlement if specified.
- `geographic_precision_note`: notes for city vs station vs region ambiguity.
- `weather_variable`: measured variable name.
- `threshold_value`: threshold literal used by settlement rule.
- `threshold_unit`: unit used by threshold.
- `comparator`: comparator token (e.g., above, below, at least).
- `measurement_window_text`: explicit settlement time window.
- `timezone_or_local_day_rule`: local-day or timezone definition.
- `aggregation_method`: max/min/sum/occurrence method when present.
- `revision_or_finality_rule`: first-posted/final-revision/fallback behavior.
- `classification_authority`: authority for event classification, if applicable.
- `source_compatibility_notes`: rationale for compatibility / incompatibility.
- `trap_flags`: listed trap labels relevant to review.
- `primary_trap_severity`: closed set `{caution, blocking}`.
- `label_confidence`: closed set `{confirmed, unclear, unknown}`.
- `ambiguity_notes`: unresolved interpretation details.
- `reviewer_notes`: adjudicator notes and rationale.
- `non_approval_notes`: explicit reminder this label is not implementation approval.
- `source_notes`: references and evidence notes backing label choices.

## 10. Example manual-label template
**Template only (static example). Not live/current ingested data.**

- label_id: [label_id]
- manual_label_stage: stage_1_static_manual_label
- reviewer_workflow_state: unreviewed
- review_posture: review_only
- raw_market_title: [raw_market_title]
- raw_market_rules_excerpt: [raw_market_rules_excerpt]
- venue_name: [venue_name]
- venue_market_url_or_reference: [venue_market_url_or_reference]
- market_family: precipitation_threshold
- canonical_mapping_decision: unclear
- canonical_event_summary: [canonical_event_summary]
- venue_defined_settlement_rule: [venue_defined_settlement_rule]
- resolver/source_role: official_weather_source
- resolver/source_name: [resolver/source_name]
- resolver/source_url_or_reference: [resolver/source_url_or_reference]
- location_text: [location_text]
- station_or_observation_point: [station_or_observation_point]
- geographic_precision_note: [geographic_precision_note]
- weather_variable: [weather_variable]
- threshold_value: [threshold_value]
- threshold_unit: [threshold_unit]
- comparator: [comparator]
- measurement_window_text: [measurement_window_text]
- timezone_or_local_day_rule: [timezone_or_local_day_rule]
- aggregation_method: [aggregation_method]
- revision_or_finality_rule: [revision_or_finality_rule]
- classification_authority: [classification_authority]
- source_compatibility_notes: [source_compatibility_notes]
- trap_flags: [trap_flags]
- primary_trap_severity: caution
- label_confidence: unknown
- ambiguity_notes: [ambiguity_notes]
- reviewer_notes: [reviewer_notes]
- non_approval_notes: [non_approval_notes]
- source_notes: [source_notes]

## 11. Source-defined settlement object checklist
- What exactly resolves?
- Which venue wording controls?
- Which source or authority resolves?
- Which station/location controls?
- Which measurement window controls?
- Which threshold/comparator/unit controls?
- Which revision/finality rule controls?
- Which classification authority controls, if applicable?
- Which traps are present?
- What remains unknown or unclear?

## 12. Non-approval boundaries for labels
Manual labels do not approve:
- provider integration
- connectors
- provider credentials
- external API calls
- config loading
- secret reading
- data ingestion
- historical labels
- forecast pulls
- model scoring
- probability modeling
- backtesting
- runtime observation
- trading strategy
- position sizing
- order placement
- live market execution
- autonomy
- profitability claims

## 13. Later-ticket handoff
- Static trap-label fixture/template: **PRD-P1-WX-STAGE1-02**.
- Reviewer checklist/adjudication protocol expansion: **PRD-P1-WX-STAGE1-03**.
- Small manually labeled seed examples: **PRD-P1-WX-STAGE1-04**.
- Stage 2 source-compatible historical labels move to a future Stage 2 ticket only after Stage 1 completion.
- Probability scoring/backtesting remain later-stage work only after required gates.

## 14. Acceptance criteria
- [x] Canonical ID `PRD-P1-WX-STAGE1-01` is present exactly.
- [x] Standalone Weather Bot PRD is referenced.
- [x] Stage 1 scope is explicit.
- [x] Source-defined settlement object thesis is preserved.
- [x] Manual-label schema is defined.
- [x] Example template is included.
- [x] All closed sets are listed exactly.
- [x] Machine-checkable assignment section exists.
- [x] Machine-checkable assignments use only allowed values.
- [x] Forbidden examples are documented without being used as actual field values.
- [x] Non-approval boundaries are explicit.
- [x] Later-ticket handoff is explicit.
- [x] No implementation behavior is introduced.
