# WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-TAXONOMY-PLANNING-01 — Weather Bot Phase 0A Settlement Rule Taxonomy Planning

Canonical ID: WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-TAXONOMY-PLANNING-01

## Status and scope

This is docs/static-test-only/settlement-rule-taxonomy-planning-only. This ticket does not modify `meg/`. This ticket does not modify meta/handoff files, including `docs/meta/MEG_ACTIVE_STATE.md`, `docs/meta/MEG_CHAT_HANDOFF.md`, or `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`. This ticket does not revise the owner decision. This ticket does not reopen source-fetching implementation planning. This ticket does not fetch, create, or modify market data. This ticket does not create fixtures or generated data. This ticket does not parse settlement rules in runtime code. This ticket does not implement scoring, backtesting, trading, or autonomy. This ticket does not create a separate standalone self-review artifact.

## Relationship to canonical identifier static audit self-review

This artifact follows `docs/prd/WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-SELF-REVIEW-01.md` and `tests/core/test_weather_bot_phase0a_canonical_identifier_static_audit_self_review_01.py` after merged PR #289. It preserves the canonical identifier self-review result while adding a narrow settlement-rule taxonomy planning layer only.

## Taxonomy objective

The objective is to define static planning categories Weather Bot may later use to reason about market settlement rules. Weather Bot models the market settlement rule, not generic weather. The taxonomy is not a parser, classifier, source-fetcher, scorer, backtester, trading mechanism, report writer, persistence path, or external export mechanism.

## Current held/closed source-fetching posture

Weather Bot Phase 0A remains held and closed for source-fetching runtime work. The source-fetching runtime track remains closed/held. The closed owner decision remains `hold_source_fetching_runtime_track`. Source fetching remains not implemented. Implementation approval remains not granted. Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed.

## No owner-decision revision boundary

No owner-decision revision is being made in this ticket. This ticket does not revise the owner decision, does not proceed to `source_fetching_runtime_implementation_plan`, and does not approve source-fetching implementation planning. Silence, continuation, lack of objection, and non-interference are not approval.

## Settlement-rule taxonomy overview

The static taxonomy records settlement-rule field categories, measurement categories, comparator categories, outcome mapping relationships, ambiguity triggers, and manual-review reasons. These are static planning categories only and do not create runtime behavior.

## Settlement text fields

The settlement text field categories are: `resolution_source_text`, `settlement_rule_text`, `question_text`. `resolution_source_text` captures the market-stated source text; `settlement_rule_text` captures rule text; `question_text` captures the market question text.

## Resolution-source taxonomy

`reporting_authority` records the named authority in the market rule. `fallback_resolution_rule` records stated fallback rule text. `ambiguous_resolution_trigger` records static triggers for manual review when source text conflicts or is incomplete. These categories do not fetch sources.

## Weather measurement taxonomy

Weather measurement categories are: `temperature`, `precipitation`, `snowfall`, `rainfall`, `wind_speed`, `hurricane_category`, `air_quality_index`, `weather_alert_presence`, `other_weather_measurement_requires_review`. Each is a static planning label only, and `other_weather_measurement_requires_review` is used for unsupported or unclear market-rule measurements.

## Time-window taxonomy

`measurement_window_start` and `measurement_window_end` describe the market-stated settlement window. Ambiguous or missing time windows require manual review and do not authorize source fetching or forecast pulling.

## Location taxonomy

`event_location` describes the market-stated location, station, region, or jurisdiction used by the settlement rule. Ambiguous locations require manual review and do not authorize API calls, scraping, or file downloads.

## Threshold and comparator taxonomy

`measurement_unit`, `measurement_threshold`, and `measurement_comparator` capture the market-stated unit, threshold, and comparator. Comparator categories are: `greater_than`, `greater_than_or_equal`, `less_than`, `less_than_or_equal`, `equal_to`, `within_range`, `presence_absence`, `ambiguous_comparator_requires_review`.

## Outcome mapping taxonomy

`outcome_label` records the market-facing label. `token_outcome_pair` records the derived relationship between `token_id` and `outcome`; it remains a derived relationship, not a replacement for canonical fields.

## Ambiguity and manual-review taxonomy

Manual-review categories are: `missing_resolution_source`, `ambiguous_location`, `ambiguous_time_window`, `ambiguous_measurement_unit`, `ambiguous_threshold`, `ambiguous_comparator`, `conflicting_source_text`, `unsupported_weather_measurement`, `operator_review_required`. `operator_review_required` remains a static manual-review flag and does not grant autonomy.

## Static planning only boundary

This ticket is docs/static-test-only/settlement-rule-taxonomy-planning-only. It does not modify runtime code, does not modify `meg/`, does not modify meta/handoff files, does not parse settlement rules in runtime code, and does not implement runtime settlement-rule classification.

## Canonical identifier posture

Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`. Future reasoning must preserve all three canonical shared-rail identifiers. Future reasoning must preserve the relationship between `token_id` and `outcome`. `token_outcome_pair` remains a derived relationship, not a replacement for canonical fields. `market_id` remains explicitly non-routing only. No routing on `market_id` is introduced or approved.

## Source-fetching track remains blocked

The following work remains blocked:

- `owner_decision_revision`
- `source_fetching_runtime_implementation_plan`
- `source_fetching_implementation`
- `provider_connector_implementation`
- `provider_client_creation`
- `live_provider_source_fetching`
- `forecast_pull_execution`
- `api_call_execution`
- `scraping_execution`
- `file_download_execution`
- `provider_sdk_execution`
- `credentials_config_loading`
- `generated_data_creation`
- `fixture_data_modification`
- `settlement_rule_runtime_parser`
- `settlement_rule_runtime_classification`
- `scoring_implementation`
- `backtesting_implementation`
- `runtime_trading_behavior`
- `order_placement`
- `autonomy_behavior`
- `production_behavior`
- `audit_report_generation`
- `audit_output_persistence`
- `external_export_behavior`
- `standalone_self_review_prd_artifact`

## Provider/source execution boundary

Provider connectors remain not approved. Provider clients remain not created. Live provider/source fetching remains not approved. Forecast pulls, API calls, scraping, file downloads, and provider SDK usage remain not approved.

## Credential/config boundary

Credentials/config loading remains not approved. This ticket does not modify `.env`, secrets, credentials, config, or config-loading behavior.

## Generated-data and fixture boundary

Generated data and fixtures remain not approved. This ticket does not fetch, create, or modify market data. This ticket does not create generated data, does not create fixtures, and does not modify `tests/fixtures/`.

## Scoring/backtesting boundary

Scoring/backtesting remains not approved. This ticket does not implement scoring, backtesting, model evaluation execution, or historical simulation.

## Trading/autonomy/production boundary

Runtime trading/order placement/autonomy/production remains not approved. This ticket does not implement trading, order placement, autonomy, or production behavior.

## Audit report and export boundary

Report writing, audit output persistence, and external export remain not approved. This ticket does not create audit reports, persisted audit output, export files, or external export behavior.

## Stage 2 runtime metadata posture

Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed. The existing Stage 2 runtime metadata artifacts remain: `meg/weather/stage2/source_identity_runtime.py`, `meg/weather/stage2/retrieval_context_runtime.py`, `meg/weather/stage2/provider_source_family_runtime.py`, `meg/weather/stage2/manual_review_gate_runtime.py`, `meg/weather/stage2/no_lookahead_metadata_runtime.py`, `meg/weather/stage2/fail_closed_validation_runtime.py`, `meg/weather/stage2/static_audit_surface_runtime.py`.

## Embedded self-review requirement

The PR must be self-reviewed using the secondary self-review prompt before asking for review. The self-review result must be summarized in the PR body. Do not create a separate standalone self-review PRD artifact for this ticket. Do not recommend a standalone self-review ticket as the next ticket.

## Recommended next ticket

Recommended next ticket: `weather_bot_phase0a_manual_review_checklist_planning`.

This next ticket is the next main safe lane from the non-source-fetching inventory. It must not revise the owner decision and must not implement source fetching. Do not recommend a standalone self-review ticket.

## Machine-checkable Weather Bot Phase 0A settlement-rule taxonomy-planning assignments

- weather bot planning stage: weather_bot_phase0a_settlement_rule_taxonomy_planning
- settlement taxonomy status: docs_static_test_only
- settlement taxonomy status: settlement_rule_taxonomy_planning_only
- settlement taxonomy status: post_weather_bot_phase0a_canonical_identifier_static_audit_self_review
- self review posture: embedded_secondary_prompt_only
- self review posture: no_standalone_self_review_prd
- owner decision posture: no_owner_decision_revision
- owner decision posture: hold_source_fetching_runtime_track_preserved
- source fetching track posture: closed_held
- source fetching track posture: no_source_fetching_implementation_plan
- source fetching track posture: no_source_fetching_implementation
- source fetching track posture: implementation_approval_not_granted
- settlement taxonomy field: resolution_source_text
- settlement taxonomy field: settlement_rule_text
- settlement taxonomy field: question_text
- settlement taxonomy field: measurement_type
- settlement taxonomy field: measurement_unit
- settlement taxonomy field: measurement_threshold
- settlement taxonomy field: measurement_comparator
- settlement taxonomy field: measurement_window_start
- settlement taxonomy field: measurement_window_end
- settlement taxonomy field: event_location
- settlement taxonomy field: reporting_authority
- settlement taxonomy field: fallback_resolution_rule
- settlement taxonomy field: ambiguous_resolution_trigger
- settlement taxonomy field: manual_review_reason
- settlement taxonomy field: operator_review_required
- settlement taxonomy field: outcome_label
- settlement taxonomy field: token_outcome_pair
- weather measurement category: temperature
- weather measurement category: precipitation
- weather measurement category: snowfall
- weather measurement category: rainfall
- weather measurement category: wind_speed
- weather measurement category: hurricane_category
- weather measurement category: air_quality_index
- weather measurement category: weather_alert_presence
- weather measurement category: other_weather_measurement_requires_review
- comparator category: greater_than
- comparator category: greater_than_or_equal
- comparator category: less_than
- comparator category: less_than_or_equal
- comparator category: equal_to
- comparator category: within_range
- comparator category: presence_absence
- comparator category: ambiguous_comparator_requires_review
- manual review category: missing_resolution_source
- manual review category: ambiguous_location
- manual review category: ambiguous_time_window
- manual review category: ambiguous_measurement_unit
- manual review category: ambiguous_threshold
- manual review category: ambiguous_comparator
- manual review category: conflicting_source_text
- manual review category: unsupported_weather_measurement
- manual review category: operator_review_required
- canonical routing field: condition_id
- canonical routing field: token_id
- canonical routing field: outcome
- non routing field: market_id
- identifier relationship: token_outcome_pair_derived_relationship
- identifier relationship: condition_token_outcome_preserved
- identifier relationship: token_id_outcome_relationship_preserved
- blocked work: owner_decision_revision
- blocked work: source_fetching_runtime_implementation_plan
- blocked work: source_fetching_implementation
- blocked work: provider_connector_implementation
- blocked work: provider_client_creation
- blocked work: live_provider_source_fetching
- blocked work: forecast_pull_execution
- blocked work: api_call_execution
- blocked work: scraping_execution
- blocked work: file_download_execution
- blocked work: provider_sdk_execution
- blocked work: credentials_config_loading
- blocked work: generated_data_creation
- blocked work: fixture_data_modification
- blocked work: settlement_rule_runtime_parser
- blocked work: settlement_rule_runtime_classification
- blocked work: scoring_implementation
- blocked work: backtesting_implementation
- blocked work: runtime_trading_behavior
- blocked work: order_placement
- blocked work: autonomy_behavior
- blocked work: production_behavior
- blocked work: audit_report_generation
- blocked work: audit_output_persistence
- blocked work: external_export_behavior
- blocked work: standalone_self_review_prd_artifact
- stage2 runtime metadata artifact: source_identity_runtime_py
- stage2 runtime metadata artifact: retrieval_context_runtime_py
- stage2 runtime metadata artifact: provider_source_family_runtime_py
- stage2 runtime metadata artifact: manual_review_gate_runtime_py
- stage2 runtime metadata artifact: no_lookahead_metadata_runtime_py
- stage2 runtime metadata artifact: fail_closed_validation_runtime_py
- stage2 runtime metadata artifact: static_audit_surface_runtime_py
- implementation posture: docs_static_test_only
- implementation posture: settlement_rule_taxonomy_planning_only
- implementation posture: no_runtime_code_change
- implementation posture: no_owner_decision_revision
- implementation posture: no_source_fetching
- implementation posture: no_source_fetching_plan
- implementation posture: no_provider_connector
- implementation posture: no_provider_client
- implementation posture: no_live_provider_fetching
- implementation posture: no_credential_config_loading
- implementation posture: no_generated_data
- implementation posture: no_fixture_change
- implementation posture: no_settlement_rule_runtime_parser
- implementation posture: no_scoring_backtesting
- implementation posture: no_trading_autonomy_production
- implementation posture: no_report_writing
- implementation posture: no_external_export
- implementation posture: no_persistence
- recommended next track: weather_bot_phase0a_manual_review_checklist_planning
- conditional next track: weather_bot_phase0a_settlement_rule_taxonomy_revision_if_scope_too_broad
- evidence status: settlement_rule_taxonomy_planning_recorded
- label confidence: confirmed

## Acceptance criteria

- The document exists with the required canonical ID and sections.
- The static test validates docs/static-test-only/settlement-rule-taxonomy-planning-only posture.
- The machine-checkable assignment values are section-scoped and closed-set.
- The embedded self-review posture is recorded without creating a standalone self-review PRD artifact.
- The recommended next ticket is `weather_bot_phase0a_manual_review_checklist_planning`.
