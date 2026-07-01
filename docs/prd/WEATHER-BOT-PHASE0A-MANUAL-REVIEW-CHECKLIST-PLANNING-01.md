# WEATHER-BOT-PHASE0A-MANUAL-REVIEW-CHECKLIST-PLANNING-01 — Weather Bot Phase 0A Manual Review Checklist Planning

Canonical ID: WEATHER-BOT-PHASE0A-MANUAL-REVIEW-CHECKLIST-PLANNING-01

## Status and scope

This is docs/static-test-only/manual-review-checklist-planning-only. This ticket does not modify `meg/`. This ticket does not modify meta/handoff files, including `docs/meta/MEG_ACTIVE_STATE.md`, `docs/meta/MEG_CHAT_HANDOFF.md`, or `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`. This ticket does not revise the owner decision. This ticket does not reopen source-fetching implementation planning. This ticket does not fetch, create, or modify market data. This ticket does not create fixtures or generated data. This ticket does not implement runtime manual-review workflow behavior. This ticket does not implement runtime settlement-rule parsing or classification. This ticket does not implement scoring, backtesting, trading, or autonomy. This ticket does not create a separate standalone self-review artifact.

## Relationship to settlement-rule taxonomy planning

This artifact follows `docs/prd/WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-TAXONOMY-PLANNING-01.md` and `tests/core/test_weather_bot_phase0a_settlement_rule_taxonomy_planning_01.py` after merged PR #290. It converts the settlement-rule taxonomy and ambiguity categories into static operator-review checklist categories only. Weather Bot models the market settlement rule, not generic weather.

## Checklist objective

The objective is to define static checklist categories an operator would later use to review ambiguous Weather Bot Phase 0A settlement-rule cases. The checklist is planning vocabulary only and is not a runtime manual-review workflow, UI, persistence path, source-fetcher, parser, classifier, scorer, backtester, trading mechanism, audit report writer, or external export mechanism.

## Current held/closed source-fetching posture

Weather Bot Phase 0A remains held and closed for source-fetching runtime work. The source-fetching runtime track remains closed/held. The closed owner decision remains `hold_source_fetching_runtime_track`. Source fetching remains not implemented. Implementation approval remains not granted. Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed.

## No owner-decision revision boundary

No owner-decision revision is being made in this ticket. This ticket does not revise the owner decision, does not proceed to `source_fetching_runtime_implementation_plan`, and does not approve source-fetching implementation planning. Silence, continuation, lack of objection, and non-interference are not approval.

## Manual review checklist overview

The manual review checklist categories are static planning categories only. They describe later operator questions about source clarity, settlement text, weather measurement details, time windows, locations, thresholds, comparators, outcome mapping, canonical identifiers, and operator decision labels. They do not execute operator decisions.

## Settlement-rule review checklist

- `check_settlement_rule_text_present`: static check category for whether market settlement-rule text is present for operator review.
- `check_question_text_consistent`: static check category for whether the question text is consistent with the settlement-rule text.
- `check_fallback_rule_present_if_needed`: static check category for whether a fallback rule is stated when the settlement rule requires one.

## Resolution-source review checklist

- `check_resolution_source_present`: static check category for whether a settlement resolution source is stated.
- `check_resolution_source_unambiguous`: static check category for whether the stated resolution source is unambiguous.
- `check_reporting_authority_present`: static check category for whether the reporting authority is stated.

## Weather measurement review checklist

- `check_measurement_type_supported`: static check category for whether the market-rule measurement type is supported by the planning taxonomy.
- `check_measurement_unit_unambiguous`: static check category for whether the measurement unit is unambiguous.

## Time-window review checklist

- `check_time_window_present`: static check category for whether the market rule states the measurement time window.
- `check_time_window_unambiguous`: static check category for whether the time window is unambiguous.

## Location review checklist

- `check_location_present`: static check category for whether the market rule states the settlement location, station, region, or jurisdiction.
- `check_location_unambiguous`: static check category for whether the settlement location is unambiguous.

## Threshold and comparator review checklist

- `check_threshold_present`: static check category for whether the market rule states the threshold.
- `check_comparator_unambiguous`: static check category for whether the market-rule comparator is unambiguous.

## Outcome mapping review checklist

- `check_outcome_labels_match_tokens`: static check category for whether outcome labels match token-facing outcomes.
- `check_token_outcome_pair_preserved`: static check category for whether the derived relationship between `token_id` and `outcome` is preserved.
- `check_condition_token_outcome_preserved`: static check category for whether `condition_id`, `token_id`, and `outcome` are preserved together.

## Canonical identifier review checklist

- `check_operator_review_required_flag`: static check category for whether a market-rule ambiguity requires operator review.
- Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`.
- Future reasoning must preserve all three canonical shared-rail identifiers and the relationship between `token_id` and `outcome`.

## Operator decision checklist

Static operator decision labels are: `manual_review_pass`, `manual_review_blocked_missing_required_field`, `manual_review_blocked_ambiguous_rule`, `manual_review_blocked_identifier_mismatch`, `manual_review_blocked_unsupported_measurement`, `manual_review_requires_followup_planning`. These labels are planning values only and do not execute decisions.

## Manual-review reason taxonomy

Manual-review reason values are: `missing_resolution_source`, `ambiguous_resolution_source`, `missing_settlement_rule_text`, `question_rule_conflict`, `ambiguous_location`, `ambiguous_time_window`, `ambiguous_measurement_unit`, `ambiguous_threshold`, `ambiguous_comparator`, `conflicting_source_text`, `unsupported_weather_measurement`, `outcome_token_mismatch`, `operator_review_required`.

## Static planning only boundary

This ticket is docs/static-test-only/manual-review-checklist-planning-only. It does not modify runtime code, does not modify `meg/`, does not modify meta/handoff files, does not implement runtime manual-review workflow behavior, does not implement runtime settlement-rule parsing, and does not implement runtime settlement-rule classification.

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
- `manual_review_runtime_workflow`
- `manual_review_ui`
- `manual_review_persistence`
- `operator_decision_execution`
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

Recommended next ticket: `weather_bot_phase0a_no_lookahead_policy_documentation`.

This next ticket is the next main safe lane from the non-source-fetching inventory. It must not revise the owner decision and must not implement source fetching. Do not recommend a standalone self-review ticket.

## Machine-checkable Weather Bot Phase 0A manual-review checklist-planning assignments

- weather bot planning stage: weather_bot_phase0a_manual_review_checklist_planning
- manual review checklist status: docs_static_test_only
- manual review checklist status: manual_review_checklist_planning_only
- manual review checklist status: post_weather_bot_phase0a_settlement_rule_taxonomy_planning
- self review posture: embedded_secondary_prompt_only
- self review posture: no_standalone_self_review_prd
- owner decision posture: no_owner_decision_revision
- owner decision posture: hold_source_fetching_runtime_track_preserved
- source fetching track posture: closed_held
- source fetching track posture: no_source_fetching_implementation_plan
- source fetching track posture: no_source_fetching_implementation
- source fetching track posture: implementation_approval_not_granted
- manual review checklist item: check_resolution_source_present
- manual review checklist item: check_resolution_source_unambiguous
- manual review checklist item: check_settlement_rule_text_present
- manual review checklist item: check_question_text_consistent
- manual review checklist item: check_measurement_type_supported
- manual review checklist item: check_measurement_unit_unambiguous
- manual review checklist item: check_threshold_present
- manual review checklist item: check_comparator_unambiguous
- manual review checklist item: check_time_window_present
- manual review checklist item: check_time_window_unambiguous
- manual review checklist item: check_location_present
- manual review checklist item: check_location_unambiguous
- manual review checklist item: check_reporting_authority_present
- manual review checklist item: check_fallback_rule_present_if_needed
- manual review checklist item: check_outcome_labels_match_tokens
- manual review checklist item: check_token_outcome_pair_preserved
- manual review checklist item: check_condition_token_outcome_preserved
- manual review checklist item: check_operator_review_required_flag
- manual review reason: missing_resolution_source
- manual review reason: ambiguous_resolution_source
- manual review reason: missing_settlement_rule_text
- manual review reason: question_rule_conflict
- manual review reason: ambiguous_location
- manual review reason: ambiguous_time_window
- manual review reason: ambiguous_measurement_unit
- manual review reason: ambiguous_threshold
- manual review reason: ambiguous_comparator
- manual review reason: conflicting_source_text
- manual review reason: unsupported_weather_measurement
- manual review reason: outcome_token_mismatch
- manual review reason: operator_review_required
- operator decision label: manual_review_pass
- operator decision label: manual_review_blocked_missing_required_field
- operator decision label: manual_review_blocked_ambiguous_rule
- operator decision label: manual_review_blocked_identifier_mismatch
- operator decision label: manual_review_blocked_unsupported_measurement
- operator decision label: manual_review_requires_followup_planning
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
- blocked work: manual_review_runtime_workflow
- blocked work: manual_review_ui
- blocked work: manual_review_persistence
- blocked work: operator_decision_execution
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
- implementation posture: manual_review_checklist_planning_only
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
- implementation posture: no_manual_review_runtime_workflow
- implementation posture: no_scoring_backtesting
- implementation posture: no_trading_autonomy_production
- implementation posture: no_report_writing
- implementation posture: no_external_export
- implementation posture: no_persistence
- recommended next track: weather_bot_phase0a_no_lookahead_policy_documentation
- conditional next track: weather_bot_phase0a_manual_review_checklist_revision_if_scope_too_broad
- evidence status: manual_review_checklist_planning_recorded
- label confidence: confirmed

## Acceptance criteria

- The manual-review checklist planning artifact exists with this canonical ID.
- The artifact records checklist categories, reason taxonomy values, operator decision labels, canonical identifier posture, blocked work, and Stage 2 metadata artifact references.
- The artifact remains docs/static-test-only/manual-review-checklist-planning-only.
- The artifact does not modify `meg/`, meta/handoff files, fixtures, generated data, runtime manual-review workflow behavior, settlement-rule runtime parsing/classification, source fetching, provider/source execution, credentials/config loading, scoring/backtesting, trading/autonomy/production behavior, report writing, persistence, or external export.
- The embedded self-review requirement is satisfied and summarized in the PR body without creating a separate standalone self-review PRD artifact.
