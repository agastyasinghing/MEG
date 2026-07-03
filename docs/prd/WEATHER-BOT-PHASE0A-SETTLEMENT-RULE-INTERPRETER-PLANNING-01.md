# WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-INTERPRETER-PLANNING-01 — Weather Bot Phase 0A Settlement Rule Interpreter Planning


Canonical ID: WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-INTERPRETER-PLANNING-01


## Status and scope

This artifact is docs/static-test-only/settlement-rule-interpreter-planning-only. This ticket does not modify `meg/`. This ticket does not modify meta/handoff files. This ticket does not revise the owner decision. This ticket does not reopen source-fetching implementation planning. This ticket does not fetch, create, or modify market data. This ticket does not create fixtures or generated data. This ticket does not create or modify schemas. Weather Bot models the market settlement rule, not generic weather. This ticket does not create a separate standalone self-review artifact.

## Relationship to supplied market-contract input planning

This follows `docs/prd/WEATHER-BOT-PHASE0A-SUPPLIED-MARKET-CONTRACT-INPUT-PLANNING-01.md` and `tests/core/test_weather_bot_phase0a_supplied_market_contract_input_planning_01.py` after merged PR #298. Supplied market-contract input runtime behavior remains not implemented. Settlement-rule interpreter runtime behavior remains not implemented.

## Interpreter planning objective

Define future interpreter input vocabulary, interpreter output categories, ambiguity categories, and manual-review/fail-closed handoff labels for the market settlement rule. This artifact does not implement a parser, classifier, interpreter, runtime validation, source fetching, scoring, backtesting, paper trading, trading, persistence, reports, or exports.

## Current held/closed source-fetching posture

Weather Bot Phase 0A remains held and closed for source-fetching runtime work. The source-fetching runtime track remains closed/held. The closed owner decision remains `hold_source_fetching_runtime_track`. Source fetching remains not implemented. Implementation approval remains not granted. Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed. Supplied market-contract input runtime behavior remains not implemented. Settlement-rule interpreter runtime behavior remains not implemented. Paper-trade readiness remains not achieved. Evaluation readiness remains not achieved. Operator workflow runtime behavior remains not implemented.

## No owner-decision revision boundary

No owner-decision revision is being made in this ticket. This ticket does not revise the owner decision and does not proceed to `source_fetching_runtime_implementation_plan`. Silence, continuation, lack of objection, and non-interference are not approval.

## Settlement-rule interpreter readiness status

Current readiness is:
- `not_interpreter_ready`
- `docs_static_interpreter_planning_only`
- `runtime_settlement_rule_parser_not_implemented`
- `runtime_settlement_rule_classifier_not_implemented`
- `runtime_settlement_rule_interpreter_not_implemented`
- `interpreter_output_persistence_not_approved`
- `source_fetching_not_implemented`
- `paper_trade_execution_not_approved`

## Interpreter overview

A future interpreter may summarize supplied settlement-rule text only after a later approved implementation gate. This ticket records static vocabulary only and keeps runtime settlement-rule parser, runtime settlement-rule classifier, runtime settlement-rule interpreter, and interpreter output persistence not implemented or not approved.

## Interpreter input fields

- `condition_id`
- `token_id`
- `outcome`
- `question_text`
- `settlement_rule_text`
- `resolution_source_text`
- `outcome_label`
- `token_outcome_pair`
- `open_time`
- `close_time`
- `resolution_time`
- `event_start_time`
- `event_end_time`
- `operator_review_required`
- `manual_review_reason`

## Interpreter output categories

- `interpreter_output_not_available`
- `interpreter_output_static_summary`
- `interpreter_output_requires_manual_review`
- `interpreter_output_requires_no_lookahead_review`
- `interpreter_output_requires_fail_closed`
- `interpreter_output_unsupported_measurement`
- `interpreter_output_ambiguous_rule`
- `interpreter_output_scope_revision_required`

## Measurement extraction planning categories

- `measurement_temperature`
- `measurement_precipitation`
- `measurement_snowfall`
- `measurement_rainfall`
- `measurement_wind_speed`
- `measurement_hurricane_category`
- `measurement_air_quality_index`
- `measurement_weather_alert_presence`
- `measurement_other_requires_review`

## Threshold and comparator planning categories

- `threshold_missing`
- `threshold_present`
- `threshold_ambiguous`
- `comparator_greater_than`
- `comparator_greater_than_or_equal`
- `comparator_less_than`
- `comparator_less_than_or_equal`
- `comparator_equal_to`
- `comparator_within_range`
- `comparator_presence_absence`
- `comparator_ambiguous_requires_review`

## Time-window planning categories

- `time_window_missing`
- `time_window_present`
- `time_window_ambiguous`
- `time_window_conflicts_with_market_close`
- `time_window_requires_no_lookahead_review`

## Location planning categories

- `location_missing`
- `location_present`
- `location_ambiguous`
- `location_requires_manual_review`

## Resolution-source planning categories

- `resolution_source_missing`
- `resolution_source_present`
- `resolution_source_ambiguous`
- `resolution_source_conflicting`
- `resolution_source_requires_future_source_fetching_approval`

## Outcome mapping planning categories

- `outcome_mapping_preserved`
- `outcome_mapping_missing`
- `outcome_mapping_ambiguous`
- `outcome_mapping_token_outcome_mismatch`
- `outcome_mapping_requires_manual_review`

## Ambiguity planning categories

- `ambiguity_missing_required_text`
- `ambiguity_conflicting_question_and_rule`
- `ambiguity_unsupported_measurement`
- `ambiguity_missing_threshold`
- `ambiguity_ambiguous_comparator`
- `ambiguity_ambiguous_time_window`
- `ambiguity_ambiguous_location`
- `ambiguity_conflicting_resolution_source`
- `ambiguity_identifier_mismatch`
- `ambiguity_requires_scope_revision`

## Manual-review handoff labels

- `handoff_manual_review_required`
- `handoff_operator_check_required`
- `handoff_identifier_check_required`
- `handoff_settlement_text_check_required`
- `handoff_resolution_source_check_required`
- `handoff_time_window_check_required`
- `handoff_location_check_required`
- `handoff_outcome_mapping_check_required`

## Fail-closed handoff labels

- `handoff_fail_closed_missing_required_field`
- `handoff_fail_closed_identifier_mismatch`
- `handoff_fail_closed_ambiguous_rule`
- `handoff_fail_closed_unsupported_measurement`
- `handoff_fail_closed_lookahead_uncertainty`
- `handoff_fail_closed_source_unapproved`
- `handoff_fail_closed_scope_violation`

## No-lookahead relationship

Future interpreter planning must preserve no-lookahead review labels, but this ticket does not implement runtime no-lookahead enforcement or runtime timestamp validation.

## Stage 2 metadata relationship

Existing Stage 2 metadata runtime artifacts are documentation references only; this ticket does not modify Stage 2 runtime metadata modules:
- `meg/weather/stage2/source_identity_runtime.py`
- `meg/weather/stage2/retrieval_context_runtime.py`
- `meg/weather/stage2/provider_source_family_runtime.py`
- `meg/weather/stage2/manual_review_gate_runtime.py`
- `meg/weather/stage2/no_lookahead_metadata_runtime.py`
- `meg/weather/stage2/fail_closed_validation_runtime.py`
- `meg/weather/stage2/static_audit_surface_runtime.py`

## Interpreter readiness blockers

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
- `schema_change`
- `db_migration`
- `runtime_market_contract_ingestion`
- `runtime_supplied_input_loading`
- `runtime_supplied_input_validation`
- `supplied_input_persistence`
- `runtime_settlement_rule_parser`
- `runtime_settlement_rule_classifier`
- `runtime_settlement_rule_interpreter`
- `interpreter_output_persistence`
- `runtime_metadata_implementation`
- `stage2_runtime_module_modification`
- `fail_closed_runtime_enforcement`
- `runtime_error_handling`
- `no_lookahead_runtime_enforcement`
- `timestamp_runtime_validation`
- `manual_review_runtime_workflow`
- `manual_review_ui`
- `manual_review_persistence`
- `operator_decision_execution`
- `operator_decision_persistence`
- `scoring_implementation`
- `evaluation_execution`
- `metric_persistence`
- `backtesting_implementation`
- `paper_trade_execution`
- `paper_trade_readiness_runtime`
- `order_simulation`
- `runtime_trading_behavior`
- `order_placement`
- `autonomy_behavior`
- `production_behavior`
- `audit_report_generation`
- `audit_output_persistence`
- `external_export_behavior`
- `standalone_self_review_prd_artifact`

## Static planning only boundary

This ticket does not implement runtime market-contract ingestion. This ticket does not implement runtime supplied-input loading. This ticket does not implement runtime supplied-input validation. This ticket does not persist supplied input. This ticket does not implement runtime settlement-rule parsing. This ticket does not implement runtime settlement-rule classification. This ticket does not implement runtime settlement-rule interpretation. This ticket does not persist interpreter output. This ticket does not implement runtime metadata behavior. This ticket does not modify Stage 2 runtime metadata modules. This ticket does not implement runtime fail-closed enforcement. This ticket does not implement runtime error handling. This ticket does not implement runtime no-lookahead enforcement. This ticket does not implement runtime timestamp validation. This ticket does not implement runtime manual-review workflow behavior. This ticket does not implement operator decision execution. This ticket does not implement manual-review UI or persistence. This ticket does not implement scoring, evaluation execution, backtesting, paper trading, trading, or autonomy. This ticket does not execute paper trades. This ticket does not create simulated orders. This ticket does not create reports, persisted metrics, persisted audit output, persisted supplied input, persisted interpreter output, persisted operator decisions, or external exports.

## Canonical identifier posture

Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`. Future reasoning must preserve all three canonical shared-rail identifiers. Future reasoning must preserve the relationship between `token_id` and `outcome`. `token_outcome_pair` remains a derived relationship, not a replacement for canonical fields. `market_id` remains explicitly non-routing only. No routing on `market_id` is introduced or approved. A `market_identifier_routing_attempt` remains fail-closed.

## Source-fetching track remains blocked

Source-fetching runtime track remains closed/held. Source fetching remains not implemented. Implementation approval remains not granted. Source-fetching implementation planning remains blocked and no source-fetching implementation is approved.

## Provider/source execution boundary

Provider connectors remain not approved. Provider clients remain not created. Live provider/source fetching remains not approved. Forecast pull execution, API call execution, scraping execution, file download execution, and provider SDK execution remain not approved. Provider/source execution remains not approved.

## Credential/config boundary

Credentials/config loading remains not approved. This ticket does not modify `.env`, secrets, credentials, config, or config-loading behavior. Credentials/config loading remains not approved.

## Generated-data and fixture boundary

Generated data and fixtures remain not approved. This ticket does not create fixtures or generated data. Generated data and fixture changes remain not approved.

## Runtime parser/classifier boundary

Runtime settlement-rule parser, runtime settlement-rule classifier, runtime settlement-rule interpreter, and interpreter-output persistence remain not approved and not implemented.

## Runtime ingestion and schema boundary

Schema change and DB migration remain not approved. This ticket does not create or modify schemas. Schema change and DB migration remain not approved. Runtime market-contract ingestion, supplied-input loading, supplied-input validation, and supplied-input persistence remain not approved.

## Scoring/evaluation boundary

Scoring/evaluation execution remains not approved. This ticket does not implement scoring, evaluation execution, metric persistence, backtesting, paper trading, trading, or autonomy. Evaluation readiness remains not achieved. Metric persistence remains not approved.

## Backtesting boundary

Backtesting remains not approved. This ticket does not implement backtesting.

## Paper-trade boundary

Paper-trade readiness remains not achieved. Paper-trade execution remains not approved. This ticket does not execute paper trades. This ticket does not create simulated orders.

## Operator workflow execution boundary

Operator workflow runtime behavior remains not implemented. This ticket does not implement runtime manual-review workflow behavior. This ticket does not implement operator decision execution. This ticket does not implement manual-review UI or persistence. Operator decision execution and persistence remain not approved. Manual-review UI and persistence remain not approved.

## Trading/autonomy/production boundary

Runtime trading/order placement/autonomy/production remains not approved. This ticket does not implement trading, order placement, autonomy behavior, or production behavior.

## Audit report and export boundary

Report writing, audit output persistence, metric persistence, supplied-input persistence, interpreter-output persistence, operator-decision persistence, and external export remain not approved. This ticket does not create reports, persisted metrics, persisted audit output, persisted supplied input, persisted interpreter output, persisted operator decisions, or external exports. Report writing, persistence, and external export remain not approved.

## Stage 2 runtime metadata posture

Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed. This ticket does not implement runtime metadata behavior and does not modify Stage 2 runtime metadata modules. Documentation references only:
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

Recommended next ticket: `weather_bot_phase0a_no_lookahead_validation_planning`. This next ticket should be the next main safe lane. It must not revise the owner decision and must not implement source fetching, runtime no-lookahead validation, runtime timestamp validation, provider execution, scoring, backtesting, paper trading, trading, persistence, or export behavior. It should remain static planning only. Do not recommend a standalone self-review ticket.

## Machine-checkable Weather Bot Phase 0A settlement-rule-interpreter-planning assignments

- weather bot planning stage: weather_bot_phase0a_settlement_rule_interpreter_planning

- settlement rule interpreter status: docs_static_test_only

- settlement rule interpreter status: settlement_rule_interpreter_planning_only

- settlement rule interpreter status: post_weather_bot_phase0a_supplied_market_contract_input_planning

- settlement rule interpreter readiness status: not_interpreter_ready

- settlement rule interpreter readiness status: docs_static_interpreter_planning_only

- settlement rule interpreter readiness status: runtime_settlement_rule_parser_not_implemented

- settlement rule interpreter readiness status: runtime_settlement_rule_classifier_not_implemented

- settlement rule interpreter readiness status: runtime_settlement_rule_interpreter_not_implemented

- settlement rule interpreter readiness status: interpreter_output_persistence_not_approved

- settlement rule interpreter readiness status: source_fetching_not_implemented

- settlement rule interpreter readiness status: paper_trade_execution_not_approved

- self review posture: embedded_secondary_prompt_only

- self review posture: no_standalone_self_review_prd

- owner decision posture: no_owner_decision_revision

- owner decision posture: hold_source_fetching_runtime_track_preserved

- source fetching track posture: closed_held

- source fetching track posture: no_source_fetching_implementation_plan

- source fetching track posture: no_source_fetching_implementation

- source fetching track posture: implementation_approval_not_granted

- interpreter input field: condition_id

- interpreter input field: token_id

- interpreter input field: outcome

- interpreter input field: question_text

- interpreter input field: settlement_rule_text

- interpreter input field: resolution_source_text

- interpreter input field: outcome_label

- interpreter input field: token_outcome_pair

- interpreter input field: open_time

- interpreter input field: close_time

- interpreter input field: resolution_time

- interpreter input field: event_start_time

- interpreter input field: event_end_time

- interpreter input field: operator_review_required

- interpreter input field: manual_review_reason

- interpreter output category: interpreter_output_not_available

- interpreter output category: interpreter_output_static_summary

- interpreter output category: interpreter_output_requires_manual_review

- interpreter output category: interpreter_output_requires_no_lookahead_review

- interpreter output category: interpreter_output_requires_fail_closed

- interpreter output category: interpreter_output_unsupported_measurement

- interpreter output category: interpreter_output_ambiguous_rule

- interpreter output category: interpreter_output_scope_revision_required

- measurement planning category: measurement_temperature

- measurement planning category: measurement_precipitation

- measurement planning category: measurement_snowfall

- measurement planning category: measurement_rainfall

- measurement planning category: measurement_wind_speed

- measurement planning category: measurement_hurricane_category

- measurement planning category: measurement_air_quality_index

- measurement planning category: measurement_weather_alert_presence

- measurement planning category: measurement_other_requires_review

- threshold comparator category: threshold_missing

- threshold comparator category: threshold_present

- threshold comparator category: threshold_ambiguous

- threshold comparator category: comparator_greater_than

- threshold comparator category: comparator_greater_than_or_equal

- threshold comparator category: comparator_less_than

- threshold comparator category: comparator_less_than_or_equal

- threshold comparator category: comparator_equal_to

- threshold comparator category: comparator_within_range

- threshold comparator category: comparator_presence_absence

- threshold comparator category: comparator_ambiguous_requires_review

- time window planning category: time_window_missing

- time window planning category: time_window_present

- time window planning category: time_window_ambiguous

- time window planning category: time_window_conflicts_with_market_close

- time window planning category: time_window_requires_no_lookahead_review

- location planning category: location_missing

- location planning category: location_present

- location planning category: location_ambiguous

- location planning category: location_requires_manual_review

- resolution source planning category: resolution_source_missing

- resolution source planning category: resolution_source_present

- resolution source planning category: resolution_source_ambiguous

- resolution source planning category: resolution_source_conflicting

- resolution source planning category: resolution_source_requires_future_source_fetching_approval

- outcome mapping planning category: outcome_mapping_preserved

- outcome mapping planning category: outcome_mapping_missing

- outcome mapping planning category: outcome_mapping_ambiguous

- outcome mapping planning category: outcome_mapping_token_outcome_mismatch

- outcome mapping planning category: outcome_mapping_requires_manual_review

- ambiguity planning category: ambiguity_missing_required_text

- ambiguity planning category: ambiguity_conflicting_question_and_rule

- ambiguity planning category: ambiguity_unsupported_measurement

- ambiguity planning category: ambiguity_missing_threshold

- ambiguity planning category: ambiguity_ambiguous_comparator

- ambiguity planning category: ambiguity_ambiguous_time_window

- ambiguity planning category: ambiguity_ambiguous_location

- ambiguity planning category: ambiguity_conflicting_resolution_source

- ambiguity planning category: ambiguity_identifier_mismatch

- ambiguity planning category: ambiguity_requires_scope_revision

- manual review handoff label: handoff_manual_review_required

- manual review handoff label: handoff_operator_check_required

- manual review handoff label: handoff_identifier_check_required

- manual review handoff label: handoff_settlement_text_check_required

- manual review handoff label: handoff_resolution_source_check_required

- manual review handoff label: handoff_time_window_check_required

- manual review handoff label: handoff_location_check_required

- manual review handoff label: handoff_outcome_mapping_check_required

- fail closed handoff label: handoff_fail_closed_missing_required_field

- fail closed handoff label: handoff_fail_closed_identifier_mismatch

- fail closed handoff label: handoff_fail_closed_ambiguous_rule

- fail closed handoff label: handoff_fail_closed_unsupported_measurement

- fail closed handoff label: handoff_fail_closed_lookahead_uncertainty

- fail closed handoff label: handoff_fail_closed_source_unapproved

- fail closed handoff label: handoff_fail_closed_scope_violation

- stage2 metadata artifact: source_identity_runtime_py

- stage2 metadata artifact: retrieval_context_runtime_py

- stage2 metadata artifact: provider_source_family_runtime_py

- stage2 metadata artifact: manual_review_gate_runtime_py

- stage2 metadata artifact: no_lookahead_metadata_runtime_py

- stage2 metadata artifact: fail_closed_validation_runtime_py

- stage2 metadata artifact: static_audit_surface_runtime_py

- canonical routing field: condition_id

- canonical routing field: token_id

- canonical routing field: outcome

- non routing field: market_id

- identifier relationship: token_outcome_pair_derived_relationship

- identifier relationship: condition_token_outcome_preserved

- identifier relationship: token_id_outcome_relationship_preserved

- fail closed canonical guard: market_identifier_routing_attempt

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

- blocked work: schema_change

- blocked work: db_migration

- blocked work: runtime_market_contract_ingestion

- blocked work: runtime_supplied_input_loading

- blocked work: runtime_supplied_input_validation

- blocked work: supplied_input_persistence

- blocked work: runtime_settlement_rule_parser

- blocked work: runtime_settlement_rule_classifier

- blocked work: runtime_settlement_rule_interpreter

- blocked work: interpreter_output_persistence

- blocked work: runtime_metadata_implementation

- blocked work: stage2_runtime_module_modification

- blocked work: fail_closed_runtime_enforcement

- blocked work: runtime_error_handling

- blocked work: no_lookahead_runtime_enforcement

- blocked work: timestamp_runtime_validation

- blocked work: manual_review_runtime_workflow

- blocked work: manual_review_ui

- blocked work: manual_review_persistence

- blocked work: operator_decision_execution

- blocked work: operator_decision_persistence

- blocked work: scoring_implementation

- blocked work: evaluation_execution

- blocked work: metric_persistence

- blocked work: backtesting_implementation

- blocked work: paper_trade_execution

- blocked work: paper_trade_readiness_runtime

- blocked work: order_simulation

- blocked work: runtime_trading_behavior

- blocked work: order_placement

- blocked work: autonomy_behavior

- blocked work: production_behavior

- blocked work: audit_report_generation

- blocked work: audit_output_persistence

- blocked work: external_export_behavior

- blocked work: standalone_self_review_prd_artifact

- implementation posture: docs_static_test_only

- implementation posture: settlement_rule_interpreter_planning_only

- implementation posture: no_runtime_code_change

- implementation posture: no_stage2_runtime_module_modification

- implementation posture: no_runtime_metadata_implementation

- implementation posture: no_owner_decision_revision

- implementation posture: no_source_fetching

- implementation posture: no_source_fetching_plan

- implementation posture: no_provider_connector

- implementation posture: no_provider_client

- implementation posture: no_live_provider_fetching

- implementation posture: no_credential_config_loading

- implementation posture: no_generated_data

- implementation posture: no_fixture_change

- implementation posture: no_schema_change

- implementation posture: no_db_migration

- implementation posture: no_runtime_market_contract_ingestion

- implementation posture: no_runtime_supplied_input_loading

- implementation posture: no_runtime_supplied_input_validation

- implementation posture: no_supplied_input_persistence

- implementation posture: no_runtime_settlement_rule_parser

- implementation posture: no_runtime_settlement_rule_classifier

- implementation posture: no_runtime_settlement_rule_interpreter

- implementation posture: no_interpreter_output_persistence

- implementation posture: no_fail_closed_runtime_enforcement

- implementation posture: no_runtime_error_handling

- implementation posture: no_no_lookahead_runtime_enforcement

- implementation posture: no_timestamp_runtime_validation

- implementation posture: no_manual_review_runtime_workflow

- implementation posture: no_manual_review_ui

- implementation posture: no_manual_review_persistence

- implementation posture: no_operator_decision_execution

- implementation posture: no_operator_decision_persistence

- implementation posture: no_scoring_implementation

- implementation posture: no_evaluation_execution

- implementation posture: no_metric_persistence

- implementation posture: no_backtesting_implementation

- implementation posture: no_paper_trade_execution

- implementation posture: no_order_simulation

- implementation posture: no_trading_autonomy_production

- implementation posture: no_report_writing

- implementation posture: no_external_export

- implementation posture: no_persistence

- recommended next track: weather_bot_phase0a_no_lookahead_validation_planning

- conditional next track: weather_bot_phase0a_settlement_rule_interpreter_revision_if_scope_too_broad

- evidence status: settlement_rule_interpreter_planning_recorded

- label confidence: confirmed

## Acceptance criteria

This artifact is accepted when the static document exists, the stdlib-only static test validates the section-scoped machine-checkable assignments, all required safety boundaries remain explicit, embedded self-review is summarized in the PR body, and no runtime, metadata, source-fetching, provider, persistence, reporting, export, scoring, backtesting, paper-trading, trading, autonomy, schema, migration, fixture, generated-data, or `meg/` change is made.
