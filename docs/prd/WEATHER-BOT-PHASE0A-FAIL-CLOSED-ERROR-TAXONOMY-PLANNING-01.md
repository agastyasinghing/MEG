# WEATHER-BOT-PHASE0A-FAIL-CLOSED-ERROR-TAXONOMY-PLANNING-01 — Weather Bot Phase 0A Fail-Closed Error Taxonomy Planning

Canonical ID: WEATHER-BOT-PHASE0A-FAIL-CLOSED-ERROR-TAXONOMY-PLANNING-01

## Status and scope

This is docs/static-test-only/fail-closed-error-taxonomy-planning-only. This ticket does not modify `meg/`. This ticket does not modify meta/handoff files, including `docs/meta/MEG_ACTIVE_STATE.md`, `docs/meta/MEG_CHAT_HANDOFF.md`, or `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`. This ticket does not revise the owner decision. This ticket does not reopen source-fetching implementation planning. This ticket does not fetch, create, or modify market data. This ticket does not create fixtures or generated data. This ticket does not implement runtime fail-closed enforcement. This ticket does not implement runtime error handling. This ticket does not implement runtime no-lookahead enforcement. This ticket does not implement runtime timestamp validation. This ticket does not implement runtime settlement-rule parsing or classification. This ticket does not implement runtime manual-review workflow behavior. This ticket does not implement scoring, backtesting, paper trading, trading, or autonomy. This ticket does not create a separate standalone self-review artifact.

## Relationship to no-lookahead policy documentation

This artifact follows `docs/prd/WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-POLICY-DOCUMENTATION-01.md` and `tests/core/test_weather_bot_phase0a_no_lookahead_policy_documentation_01.py` after merged PR #292. It narrows that no-lookahead policy posture into static fail-closed error taxonomy vocabulary. Weather Bot models the market settlement rule, not generic weather.

## Taxonomy objective

The objective is to define static fail-closed error categories Weather Bot must preserve so later planning and implementation work can block uncertain, incomplete, ambiguous, conflicting, or unsafe evidence states. These categories are planning vocabulary only and do not enforce runtime behavior.

## Current held/closed source-fetching posture

Weather Bot Phase 0A remains held and closed for source-fetching runtime work. The source-fetching runtime track remains closed/held. The closed owner decision remains `hold_source_fetching_runtime_track`. Source fetching remains not implemented. Implementation approval remains not granted. Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed.

## No owner-decision revision boundary

No owner-decision revision is being made in this ticket. This ticket does not proceed to `source_fetching_runtime_implementation_plan`, does not approve source-fetching implementation, and does not approve source-fetching implementation planning. Silence, continuation, lack of objection, and non-interference are not approval.

## Fail-closed taxonomy overview

All fail-closed error category values in this artifact are static taxonomy categories only. They describe future blocking reasons, not runtime validation, runtime error handling, runtime no-lookahead enforcement, runtime timestamp validation, runtime settlement-rule parsing or classification, runtime manual-review workflow behavior, scoring, backtesting, paper trading, trading, persistence, report writing, or external export behavior.

- `source_missing`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `source_ambiguous`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `source_conflict`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `provider_unavailable`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `provider_unapproved`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `credential_config_required`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `timestamp_missing`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `timestamp_ambiguous`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `timestamp_conflict`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `lookahead_status_unknown`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `lookahead_violation_detected`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `settlement_rule_missing`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `settlement_rule_ambiguous`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `settlement_rule_conflict`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `unsupported_weather_measurement`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `measurement_unit_ambiguous`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `threshold_ambiguous`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `comparator_ambiguous`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `location_ambiguous`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `time_window_ambiguous`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `condition_id_missing`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `token_id_missing`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `outcome_missing`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `token_outcome_pair_mismatch`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `market_identifier_routing_attempt`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `manual_review_required`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `operator_decision_missing`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `operator_decision_ambiguous`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `generated_data_detected`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `fixture_data_detected`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `scoring_attempted`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `backtesting_attempted`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `paper_trade_attempted`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `trading_attempted`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `production_behavior_attempted`: static taxonomy category only; future work must treat this as a fail-closed planning reason.
- `external_export_attempted`: static taxonomy category only; future work must treat this as a fail-closed planning reason.

## Source and provider error categories

- `source_missing`: static fail-closed source/provider category only.
- `source_ambiguous`: static fail-closed source/provider category only.
- `source_conflict`: static fail-closed source/provider category only.
- `provider_unavailable`: static fail-closed source/provider category only.
- `provider_unapproved`: static fail-closed source/provider category only.
- `credential_config_required`: static fail-closed source/provider category only.

Provider connectors remain not approved. Provider clients remain not created. Live provider/source fetching remains not approved. Forecast pull execution, API call execution, scraping execution, file download execution, and provider SDK execution remain not approved.

## Timestamp and no-lookahead error categories

- `timestamp_missing`: static fail-closed timestamp/no-lookahead category only.
- `timestamp_ambiguous`: static fail-closed timestamp/no-lookahead category only.
- `timestamp_conflict`: static fail-closed timestamp/no-lookahead category only.
- `lookahead_status_unknown`: static fail-closed timestamp/no-lookahead category only.
- `lookahead_violation_detected`: static fail-closed timestamp/no-lookahead category only.

This ticket does not implement runtime no-lookahead enforcement or runtime timestamp validation.

## Settlement-rule ambiguity error categories

- `settlement_rule_missing`: static fail-closed settlement-rule ambiguity category only.
- `settlement_rule_ambiguous`: static fail-closed settlement-rule ambiguity category only.
- `settlement_rule_conflict`: static fail-closed settlement-rule ambiguity category only.
- `unsupported_weather_measurement`: static fail-closed settlement-rule ambiguity category only.
- `measurement_unit_ambiguous`: static fail-closed settlement-rule ambiguity category only.
- `threshold_ambiguous`: static fail-closed settlement-rule ambiguity category only.
- `comparator_ambiguous`: static fail-closed settlement-rule ambiguity category only.
- `location_ambiguous`: static fail-closed settlement-rule ambiguity category only.
- `time_window_ambiguous`: static fail-closed settlement-rule ambiguity category only.

Weather Bot models the market settlement rule, not generic weather. This ticket does not implement runtime settlement-rule parsing or classification.

## Canonical identifier error categories

- `condition_id_missing`: static fail-closed canonical identifier category only.
- `token_id_missing`: static fail-closed canonical identifier category only.
- `outcome_missing`: static fail-closed canonical identifier category only.
- `token_outcome_pair_mismatch`: static fail-closed canonical identifier category only.
- `market_identifier_routing_attempt`: static fail-closed canonical identifier category only.

A `market_identifier_routing_attempt` must be documented as fail-closed in future planning.

## Manual-review gate error categories

- `manual_review_required`: static fail-closed manual-review/operator category only.
- `operator_decision_missing`: static fail-closed manual-review/operator category only.
- `operator_decision_ambiguous`: static fail-closed manual-review/operator category only.

This ticket does not implement runtime manual-review workflow behavior or operator decision execution.

## Generated-data and fixture error categories

- `generated_data_detected`: static fail-closed generated-data/fixture category only.
- `fixture_data_detected`: static fail-closed generated-data/fixture category only.

Generated data and fixtures remain not approved.

## Scoring and backtesting error categories

- `scoring_attempted`: static fail-closed scoring/backtesting category only.
- `backtesting_attempted`: static fail-closed scoring/backtesting category only.

Scoring/backtesting remains not approved.

## Trading and production error categories

- `paper_trade_attempted`: static fail-closed trading/production category only.
- `trading_attempted`: static fail-closed trading/production category only.
- `production_behavior_attempted`: static fail-closed trading/production category only.

Paper-trade execution remains not approved. Runtime trading/order placement/autonomy/production remains not approved.

## Operator decision error categories

- `operator_decision_missing`: static fail-closed category for missing future operator decision evidence.
- `operator_decision_ambiguous`: static fail-closed category for ambiguous future operator decision evidence.

Silence, continuation, lack of objection, and non-interference are not approval.

## Fail-closed action labels

Fail-closed action labels are static planning labels only:

- `block_processing`
- `require_manual_review`
- `require_scope_revision`
- `require_source_fetching_approval`
- `require_runtime_implementation_approval`
- `reject_lookahead_evidence`
- `reject_market_identifier_routing`
- `reject_generated_or_fixture_data`
- `reject_scoring_backtesting_trading`
- `reject_external_export`
- `preserve_hold_state`

## Static taxonomy only boundary

This artifact is static taxonomy and a static test only. It does not modify runtime code, does not modify `meg/`, does not modify meta/handoff files, does not implement runtime fail-closed enforcement, does not implement runtime error handling, does not implement runtime no-lookahead enforcement, does not implement runtime timestamp validation, does not implement runtime settlement-rule parsing or classification, and does not implement runtime manual-review workflow behavior.

## Canonical identifier posture

Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`. Future reasoning must preserve all three canonical shared-rail identifiers. Future reasoning must preserve the relationship between `token_id` and `outcome`. `token_outcome_pair` remains a derived relationship, not a replacement for canonical fields. `market_id` remains explicitly non-routing only. No routing on `market_id` is introduced or approved. A `market_identifier_routing_attempt` must be documented as fail-closed in future planning.

## Source-fetching track remains blocked

The following blocked work remains blocked:

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
- `fail_closed_runtime_enforcement`
- `runtime_error_handling`
- `no_lookahead_runtime_enforcement`
- `timestamp_runtime_validation`
- `settlement_rule_runtime_parser`
- `settlement_rule_runtime_classification`
- `manual_review_runtime_workflow`
- `manual_review_ui`
- `manual_review_persistence`
- `operator_decision_execution`
- `scoring_implementation`
- `backtesting_implementation`
- `paper_trade_execution`
- `runtime_trading_behavior`
- `order_placement`
- `autonomy_behavior`
- `production_behavior`
- `audit_report_generation`
- `audit_output_persistence`
- `external_export_behavior`
- `standalone_self_review_prd_artifact`

## Provider/source execution boundary

Provider connectors remain not approved. Provider clients remain not created. Live provider/source fetching remains not approved. Forecast pull execution, API call execution, scraping execution, file download execution, and provider SDK execution remain not approved.

## Credential/config boundary

Credentials/config loading remains not approved. This ticket does not modify `.env`, secrets, credentials, config, or config-loading behavior.

## Generated-data and fixture boundary

Generated data and fixtures remain not approved. This ticket does not fetch, create, or modify market data. This ticket does not create generated data, does not create fixtures, and does not modify `tests/fixtures/`.

## Scoring/backtesting boundary

Scoring/backtesting remains not approved. This ticket does not implement scoring, backtesting, model evaluation execution, or historical simulation.

## Paper-trade boundary

Paper-trade execution remains not approved. This ticket does not implement paper trading, paper-trade readiness execution, simulated order placement, or operational journaling for trades.

## Trading/autonomy/production boundary

Runtime trading/order placement/autonomy/production remains not approved. This ticket does not implement trading, order placement, autonomous behavior, production behavior, or any production execution path.

## Audit report and export boundary

Report writing, audit output persistence, and external export remain not approved. This ticket does not create report writing, audit reports, persisted audit output, export files, persistence, or external export behavior.

## Stage 2 runtime metadata posture

Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed. This ticket mentions existing artifacts only and does not modify them:

- `meg/weather/stage2/source_identity_runtime.py`
- `meg/weather/stage2/retrieval_context_runtime.py`
- `meg/weather/stage2/provider_source_family_runtime.py`
- `meg/weather/stage2/manual_review_gate_runtime.py`
- `meg/weather/stage2/no_lookahead_metadata_runtime.py`
- `meg/weather/stage2/fail_closed_validation_runtime.py`
- `meg/weather/stage2/static_audit_surface_runtime.py`

## Embedded self-review requirement

The PR must be self-reviewed using the secondary self-review prompt before asking for review. The self-review result must be summarized in the PR body. Do not create a separate standalone self-review PRD artifact for this ticket. Do not recommend a standalone self-review ticket as the next ticket.

## Recommended next ticket

Recommended next ticket: `weather_bot_phase0a_stage2_metadata_contract_documentation`. This is the next main safe lane from the non-source-fetching inventory. It must not revise the owner decision and must not implement source fetching. Do not recommend a standalone self-review ticket.

## Machine-checkable Weather Bot Phase 0A fail-closed error-taxonomy-planning assignments

- weather bot planning stage: weather_bot_phase0a_fail_closed_error_taxonomy_planning
- fail closed taxonomy status: docs_static_test_only
- fail closed taxonomy status: fail_closed_error_taxonomy_planning_only
- fail closed taxonomy status: post_weather_bot_phase0a_no_lookahead_policy_documentation
- self review posture: embedded_secondary_prompt_only
- self review posture: no_standalone_self_review_prd
- owner decision posture: no_owner_decision_revision
- owner decision posture: hold_source_fetching_runtime_track_preserved
- source fetching track posture: closed_held
- source fetching track posture: no_source_fetching_implementation_plan
- source fetching track posture: no_source_fetching_implementation
- source fetching track posture: implementation_approval_not_granted
- fail closed error category: source_missing
- fail closed error category: source_ambiguous
- fail closed error category: source_conflict
- fail closed error category: provider_unavailable
- fail closed error category: provider_unapproved
- fail closed error category: credential_config_required
- fail closed error category: timestamp_missing
- fail closed error category: timestamp_ambiguous
- fail closed error category: timestamp_conflict
- fail closed error category: lookahead_status_unknown
- fail closed error category: lookahead_violation_detected
- fail closed error category: settlement_rule_missing
- fail closed error category: settlement_rule_ambiguous
- fail closed error category: settlement_rule_conflict
- fail closed error category: unsupported_weather_measurement
- fail closed error category: measurement_unit_ambiguous
- fail closed error category: threshold_ambiguous
- fail closed error category: comparator_ambiguous
- fail closed error category: location_ambiguous
- fail closed error category: time_window_ambiguous
- fail closed error category: condition_id_missing
- fail closed error category: token_id_missing
- fail closed error category: outcome_missing
- fail closed error category: token_outcome_pair_mismatch
- fail closed error category: market_identifier_routing_attempt
- fail closed error category: manual_review_required
- fail closed error category: operator_decision_missing
- fail closed error category: operator_decision_ambiguous
- fail closed error category: generated_data_detected
- fail closed error category: fixture_data_detected
- fail closed error category: scoring_attempted
- fail closed error category: backtesting_attempted
- fail closed error category: paper_trade_attempted
- fail closed error category: trading_attempted
- fail closed error category: production_behavior_attempted
- fail closed error category: external_export_attempted
- fail closed action label: block_processing
- fail closed action label: require_manual_review
- fail closed action label: require_scope_revision
- fail closed action label: require_source_fetching_approval
- fail closed action label: require_runtime_implementation_approval
- fail closed action label: reject_lookahead_evidence
- fail closed action label: reject_market_identifier_routing
- fail closed action label: reject_generated_or_fixture_data
- fail closed action label: reject_scoring_backtesting_trading
- fail closed action label: reject_external_export
- fail closed action label: preserve_hold_state
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
- blocked work: fail_closed_runtime_enforcement
- blocked work: runtime_error_handling
- blocked work: no_lookahead_runtime_enforcement
- blocked work: timestamp_runtime_validation
- blocked work: settlement_rule_runtime_parser
- blocked work: settlement_rule_runtime_classification
- blocked work: manual_review_runtime_workflow
- blocked work: manual_review_ui
- blocked work: manual_review_persistence
- blocked work: operator_decision_execution
- blocked work: scoring_implementation
- blocked work: backtesting_implementation
- blocked work: paper_trade_execution
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
- implementation posture: fail_closed_error_taxonomy_planning_only
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
- implementation posture: no_fail_closed_runtime_enforcement
- implementation posture: no_runtime_error_handling
- implementation posture: no_no_lookahead_runtime_enforcement
- implementation posture: no_timestamp_runtime_validation
- implementation posture: no_settlement_rule_runtime_parser
- implementation posture: no_manual_review_runtime_workflow
- implementation posture: no_scoring_backtesting
- implementation posture: no_paper_trade_execution
- implementation posture: no_trading_autonomy_production
- implementation posture: no_report_writing
- implementation posture: no_external_export
- implementation posture: no_persistence
- recommended next track: weather_bot_phase0a_stage2_metadata_contract_documentation
- conditional next track: weather_bot_phase0a_fail_closed_error_taxonomy_revision_if_scope_too_broad
- evidence status: fail_closed_error_taxonomy_planning_recorded
- label confidence: confirmed

## Acceptance criteria

- The artifact remains docs/static-test-only/fail-closed-error-taxonomy-planning-only.
- The static test validates document existence, canonical ID, required sections, posture, taxonomy values, action labels, canonical identifier posture, blocked work, Stage 2 artifact references, machine-checkable assignments, and recommended next ticket.
- No runtime, source-fetching, generated-data, fixture, scoring, backtesting, paper-trade, trading, persistence, report-writing, or external export behavior is created or approved.
