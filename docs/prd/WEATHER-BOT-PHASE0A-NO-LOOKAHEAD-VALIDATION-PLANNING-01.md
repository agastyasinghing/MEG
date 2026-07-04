# WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-VALIDATION-PLANNING-01 — Weather Bot Phase 0A No-Lookahead Validation Planning

Canonical ID: WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-VALIDATION-PLANNING-01

## Status and scope

This artifact is docs/static-test-only/no-lookahead-validation-planning-only. This ticket does not modify `meg/`. This ticket does not modify meta/handoff files. This ticket does not modify Stage 2 runtime metadata modules. This ticket does not revise the owner decision. This ticket does not reopen source-fetching implementation planning. This ticket does not fetch, create, or modify market data. This ticket does not create fixtures or generated data. This ticket does not create or modify schemas. This ticket does not implement runtime market-contract ingestion. This ticket does not implement runtime supplied-input loading. This ticket does not implement runtime supplied-input validation. This ticket does not persist supplied input. This ticket does not implement runtime no-lookahead validation. This ticket does not implement runtime timestamp validation. This ticket does not implement runtime evidence-time comparison. This ticket does not persist validation output. This ticket does not implement runtime settlement-rule parsing. This ticket does not implement runtime settlement-rule classification. This ticket does not implement runtime settlement-rule interpretation. This ticket does not persist interpreter output. This ticket does not implement runtime metadata behavior. This ticket does not implement runtime fail-closed enforcement. This ticket does not implement runtime error handling. This ticket does not implement runtime manual-review workflow behavior. This ticket does not implement operator decision execution. This ticket does not implement manual-review UI or persistence. This ticket does not implement scoring, evaluation execution, backtesting, paper trading, trading, or autonomy. This ticket does not execute paper trades. This ticket does not create simulated orders. This ticket does not create reports, persisted metrics, persisted audit output, persisted supplied input, persisted interpreter output, persisted validation output, persisted operator decisions, or external exports. This ticket does not create a separate standalone self-review artifact. Weather Bot models the market settlement rule, not generic weather. Weather Bot Phase 0A remains held and closed for source-fetching runtime work. The source-fetching runtime track remains closed/held. The closed owner decision remains `hold_source_fetching_runtime_track`. Source fetching remains not implemented. Implementation approval remains not granted. Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed. Supplied market-contract input runtime behavior remains not implemented. Settlement-rule interpreter runtime behavior remains not implemented. No-lookahead validation runtime behavior remains not implemented. Operator workflow runtime behavior remains not implemented. Paper-trade readiness remains not achieved. Evaluation readiness remains not achieved. Provider connectors remain not approved. Provider clients remain not created. Live provider/source fetching remains not approved. Credentials/config loading remains not approved. Generated data and fixtures remain not approved. Scoring/evaluation execution remains not approved. Backtesting remains not approved. Paper-trade execution remains not approved. Runtime trading/order placement/autonomy/production remains not approved. Report writing, audit output persistence, metric persistence, supplied-input persistence, interpreter-output persistence, validation-output persistence, operator-decision persistence, and external export remain not approved. Silence, continuation, lack of objection, and non-interference are not approval.

## Relationship to settlement-rule interpreter planning

This follows `docs/prd/WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-INTERPRETER-PLANNING-01.md` and `tests/core/test_weather_bot_phase0a_settlement_rule_interpreter_planning_01.py` after merged PR #299. Settlement-rule interpreter runtime behavior remains not implemented; this artifact only records future no-lookahead validation vocabulary.

## No-lookahead validation planning objective

Define future timestamp fields, validation statuses, validation blockers, evidence-time comparison categories, and fail-closed/manual-review handoff labels for the market settlement rule. This artifact does not implement runtime validation, timestamp comparison, source fetching, parsing/classification, scoring, backtesting, paper trading, trading, persistence, reports, or exports.

## Current held/closed source-fetching posture

Weather Bot models the market settlement rule, not generic weather. Weather Bot Phase 0A remains held and closed for source-fetching runtime work. The source-fetching runtime track remains closed/held. The closed owner decision remains `hold_source_fetching_runtime_track`. Source fetching remains not implemented. Implementation approval remains not granted. Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed. Supplied market-contract input runtime behavior remains not implemented. Settlement-rule interpreter runtime behavior remains not implemented. No-lookahead validation runtime behavior remains not implemented. Operator workflow runtime behavior remains not implemented. Paper-trade readiness remains not achieved. Evaluation readiness remains not achieved. Provider connectors remain not approved. Provider clients remain not created. Live provider/source fetching remains not approved. Credentials/config loading remains not approved. Generated data and fixtures remain not approved. Scoring/evaluation execution remains not approved. Backtesting remains not approved. Paper-trade execution remains not approved. Runtime trading/order placement/autonomy/production remains not approved. Report writing, audit output persistence, metric persistence, supplied-input persistence, interpreter-output persistence, validation-output persistence, operator-decision persistence, and external export remain not approved. Silence, continuation, lack of objection, and non-interference are not approval.

## No owner-decision revision boundary

No owner-decision revision is being made in this ticket. This ticket does not revise the owner decision and does not proceed to `source_fetching_runtime_implementation_plan`. This ticket does not approve source-fetching implementation or source-fetching implementation planning. Silence, continuation, lack of objection, and non-interference are not approval.

## No-lookahead validation readiness status

Current readiness is:
- `not_no_lookahead_validation_ready`
- `docs_static_no_lookahead_validation_planning_only`
- `runtime_no_lookahead_validation_not_implemented`
- `runtime_timestamp_validation_not_implemented`
- `runtime_evidence_time_comparison_not_implemented`
- `validation_output_persistence_not_approved`
- `source_fetching_not_implemented`
- `paper_trade_execution_not_approved`

## Validation overview

A future no-lookahead validator may compare supplied timestamps only after a later approved implementation gate. This ticket records static labels only and keeps runtime no-lookahead validation, runtime timestamp validation, runtime evidence-time comparison, and validation output persistence not implemented or not approved.

## Timestamp input fields

- `decision_time`
- `evidence_available_time`
- `evidence_observed_time`
- `forecast_issue_time`
- `observation_valid_time`
- `resolution_time`
- `settlement_time`
- `market_close_time`
- `market_resolution_source_time`
- `operator_review_time`
- `latest_allowed_information_time`

## Evidence-time comparison categories

- `comparison_not_available`
- `comparison_evidence_before_decision`
- `comparison_evidence_at_decision`
- `comparison_evidence_after_decision`
- `comparison_forecast_issue_after_decision`
- `comparison_observation_valid_after_decision`
- `comparison_resolution_after_decision`
- `comparison_settlement_after_decision`
- `comparison_source_time_conflict`
- `comparison_timestamp_missing`
- `comparison_timestamp_ambiguous`

## Validation status labels

- `validation_status_not_available`
- `validation_status_static_planning_only`
- `validation_status_requires_manual_review`
- `validation_status_pass_candidate`
- `validation_status_block_lookahead_detected`
- `validation_status_block_timestamp_missing`
- `validation_status_block_timestamp_ambiguous`
- `validation_status_block_source_time_conflict`
- `validation_status_block_scope_violation`

## Validation blocker categories

- `block_runtime_no_lookahead_validation_missing`
- `block_runtime_timestamp_validation_missing`
- `block_runtime_evidence_time_comparison_missing`
- `block_validation_output_persistence_unapproved`
- `block_source_fetching_unapproved`
- `block_provider_execution_unapproved`
- `block_generated_fixture_data_unapproved`
- `block_operator_workflow_runtime_missing`
- `block_scoring_evaluation_unapproved`
- `block_backtesting_unapproved`
- `block_paper_trade_execution_not_approved`
- `block_trading_autonomy_production_not_approved`
- `block_audit_persistence_export_not_approved`

## Manual-review handoff labels

- `handoff_manual_review_required`
- `handoff_timestamp_check_required`
- `handoff_decision_time_check_required`
- `handoff_evidence_available_time_check_required`
- `handoff_forecast_issue_time_check_required`
- `handoff_observation_valid_time_check_required`
- `handoff_resolution_time_check_required`
- `handoff_source_time_conflict_check_required`

## Fail-closed handoff labels

- `handoff_fail_closed_lookahead_detected`
- `handoff_fail_closed_timestamp_missing`
- `handoff_fail_closed_timestamp_ambiguous`
- `handoff_fail_closed_source_time_conflict`
- `handoff_fail_closed_validation_unavailable`
- `handoff_fail_closed_scope_violation`

## Settlement-rule interpreter relationship

Weather Bot models the market settlement rule, not generic weather. Future no-lookahead validation must reason from settlement-rule meaning only after a separately approved interpreter implementation exists; runtime settlement-rule parsing, classification, and interpretation remain not implemented.

## Stage 2 metadata relationship

Existing Stage 2 metadata runtime artifacts are documentation references only; this ticket does not modify Stage 2 runtime metadata modules:
- `meg/weather/stage2/source_identity_runtime.py` documents supplied source identity posture only.
- `meg/weather/stage2/retrieval_context_runtime.py` documents supplied retrieval context posture only.
- `meg/weather/stage2/provider_source_family_runtime.py` documents supplied provider/source family posture only.
- `meg/weather/stage2/manual_review_gate_runtime.py` documents supplied manual-review gate posture only.
- `meg/weather/stage2/no_lookahead_metadata_runtime.py` documents supplied no-lookahead metadata posture only.
- `meg/weather/stage2/fail_closed_validation_runtime.py` documents supplied fail-closed validation posture only.
- `meg/weather/stage2/static_audit_surface_runtime.py` documents supplied static audit surface posture only.

## Static planning only boundary

This ticket is docs/static-test-only/no-lookahead-validation-planning-only and makes no runtime code change. This ticket does not modify `meg/`. This ticket does not modify meta/handoff files. This ticket does not modify Stage 2 runtime metadata modules. This ticket does not revise the owner decision. This ticket does not reopen source-fetching implementation planning. This ticket does not fetch, create, or modify market data. This ticket does not create fixtures or generated data. This ticket does not create or modify schemas. This ticket does not implement runtime market-contract ingestion. This ticket does not implement runtime supplied-input loading. This ticket does not implement runtime supplied-input validation. This ticket does not persist supplied input. This ticket does not implement runtime no-lookahead validation. This ticket does not implement runtime timestamp validation. This ticket does not implement runtime evidence-time comparison. This ticket does not persist validation output. This ticket does not implement runtime settlement-rule parsing. This ticket does not implement runtime settlement-rule classification. This ticket does not implement runtime settlement-rule interpretation. This ticket does not persist interpreter output. This ticket does not implement runtime metadata behavior. This ticket does not implement runtime fail-closed enforcement. This ticket does not implement runtime error handling. This ticket does not implement runtime manual-review workflow behavior. This ticket does not implement operator decision execution. This ticket does not implement manual-review UI or persistence. This ticket does not implement scoring, evaluation execution, backtesting, paper trading, trading, or autonomy. This ticket does not execute paper trades. This ticket does not create simulated orders. This ticket does not create reports, persisted metrics, persisted audit output, persisted supplied input, persisted interpreter output, persisted validation output, persisted operator decisions, or external exports. This ticket does not create a separate standalone self-review artifact.

## Canonical identifier posture

Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`. Future reasoning must preserve all three canonical shared-rail identifiers. Future reasoning must preserve the relationship between `token_id` and `outcome`. `token_outcome_pair` remains a derived relationship, not a replacement for canonical fields. `market_id` remains explicitly non-routing only. No routing on `market_id` is introduced or approved. A `market_identifier_routing_attempt` remains fail-closed.

## Source-fetching track remains blocked

The source-fetching runtime track remains closed/held. The closed owner decision remains `hold_source_fetching_runtime_track`. Source fetching remains not implemented. Implementation approval remains not granted. Do not proceed to `source_fetching_runtime_implementation_plan`.

## Provider/source execution boundary

Provider/source execution remains not approved. Provider connectors remain not approved; provider clients remain not created; live provider/source fetching, forecast pulling, API calls, scraping, file downloads, and provider SDK usage remain not approved.

## Credential/config boundary

Credentials/config loading remains not approved. This ticket does not modify `.env`, secrets, credentials, config, or config-loading behavior.

## Generated-data and fixture boundary

Generated data and fixture changes remain not approved. This ticket does not create fixtures, generated data, market data, reports, persisted audit output, or exports.

## Runtime validation boundary

Runtime no-lookahead validation, runtime timestamp validation, runtime evidence-time comparison, and validation-output persistence remain not approved and not implemented.

## Runtime parser/classifier boundary

Runtime settlement-rule parser, runtime settlement-rule classifier, runtime settlement-rule interpreter, and interpreter-output persistence remain not approved and not implemented.

## Runtime ingestion and schema boundary

Schema change and DB migration remain not approved. Runtime market-contract ingestion, supplied-input loading, supplied-input validation, and supplied-input persistence remain not approved and not implemented.

## Scoring/evaluation boundary

Scoring/evaluation execution remains not approved. This ticket does not implement scoring or evaluation execution. Metric persistence remains not approved. Evaluation readiness remains not achieved.

## Backtesting boundary

Backtesting remains not approved. This ticket does not implement backtesting.

## Paper-trade boundary

Paper-trade execution remains not approved. Paper-trade readiness remains not achieved. This ticket does not execute paper trades or create simulated orders.

## Operator workflow execution boundary

Operator workflow runtime behavior remains not implemented. Operator decision execution and persistence remain not approved. Manual-review UI and persistence remain not approved.

## Trading/autonomy/production boundary

Runtime trading/order placement/autonomy/production remains not approved. This ticket does not implement trading, order placement, autonomy, or production behavior.

## Audit report and export boundary

Report writing, persistence, and external export remain not approved. This ticket does not create reports, persisted metrics, persisted audit output, persisted supplied input, persisted interpreter output, persisted validation output, persisted operator decisions, or external exports.

## Stage 2 runtime metadata posture

Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed. This ticket does not implement runtime metadata behavior and does not modify Stage 2 runtime metadata modules.

## Embedded self-review requirement

The PR must be self-reviewed using the secondary self-review prompt before asking for review. The self-review result must be summarized in the PR body. Do not create a separate standalone self-review PRD artifact for this ticket. Do not recommend a standalone self-review ticket as the next ticket.

## Recommended next ticket

Recommended next ticket: `weather_bot_phase0a_fail_closed_validation_planning`. This next ticket should be the next main safe lane. It must not revise the owner decision and must not implement source fetching, runtime fail-closed validation, runtime no-lookahead validation, runtime timestamp validation, provider execution, scoring, backtesting, paper trading, trading, persistence, or export behavior. It should remain static planning only. Do not recommend a standalone self-review ticket.

## Machine-checkable Weather Bot Phase 0A no-lookahead-validation-planning assignments

- weather bot planning stage: weather_bot_phase0a_no_lookahead_validation_planning
- no lookahead validation status: docs_static_test_only
- no lookahead validation status: no_lookahead_validation_planning_only
- no lookahead validation status: post_weather_bot_phase0a_settlement_rule_interpreter_planning
- no lookahead validation readiness status: not_no_lookahead_validation_ready
- no lookahead validation readiness status: docs_static_no_lookahead_validation_planning_only
- no lookahead validation readiness status: runtime_no_lookahead_validation_not_implemented
- no lookahead validation readiness status: runtime_timestamp_validation_not_implemented
- no lookahead validation readiness status: runtime_evidence_time_comparison_not_implemented
- no lookahead validation readiness status: validation_output_persistence_not_approved
- no lookahead validation readiness status: source_fetching_not_implemented
- no lookahead validation readiness status: paper_trade_execution_not_approved
- self review posture: embedded_secondary_prompt_only
- self review posture: no_standalone_self_review_prd
- owner decision posture: no_owner_decision_revision
- owner decision posture: hold_source_fetching_runtime_track_preserved
- source fetching track posture: closed_held
- source fetching track posture: no_source_fetching_implementation_plan
- source fetching track posture: no_source_fetching_implementation
- source fetching track posture: implementation_approval_not_granted
- timestamp input field: decision_time
- timestamp input field: evidence_available_time
- timestamp input field: evidence_observed_time
- timestamp input field: forecast_issue_time
- timestamp input field: observation_valid_time
- timestamp input field: resolution_time
- timestamp input field: settlement_time
- timestamp input field: market_close_time
- timestamp input field: market_resolution_source_time
- timestamp input field: operator_review_time
- timestamp input field: latest_allowed_information_time
- evidence time comparison category: comparison_not_available
- evidence time comparison category: comparison_evidence_before_decision
- evidence time comparison category: comparison_evidence_at_decision
- evidence time comparison category: comparison_evidence_after_decision
- evidence time comparison category: comparison_forecast_issue_after_decision
- evidence time comparison category: comparison_observation_valid_after_decision
- evidence time comparison category: comparison_resolution_after_decision
- evidence time comparison category: comparison_settlement_after_decision
- evidence time comparison category: comparison_source_time_conflict
- evidence time comparison category: comparison_timestamp_missing
- evidence time comparison category: comparison_timestamp_ambiguous
- validation status label: validation_status_not_available
- validation status label: validation_status_static_planning_only
- validation status label: validation_status_requires_manual_review
- validation status label: validation_status_pass_candidate
- validation status label: validation_status_block_lookahead_detected
- validation status label: validation_status_block_timestamp_missing
- validation status label: validation_status_block_timestamp_ambiguous
- validation status label: validation_status_block_source_time_conflict
- validation status label: validation_status_block_scope_violation
- validation blocker category: block_runtime_no_lookahead_validation_missing
- validation blocker category: block_runtime_timestamp_validation_missing
- validation blocker category: block_runtime_evidence_time_comparison_missing
- validation blocker category: block_validation_output_persistence_unapproved
- validation blocker category: block_source_fetching_unapproved
- validation blocker category: block_provider_execution_unapproved
- validation blocker category: block_generated_fixture_data_unapproved
- validation blocker category: block_operator_workflow_runtime_missing
- validation blocker category: block_scoring_evaluation_unapproved
- validation blocker category: block_backtesting_unapproved
- validation blocker category: block_paper_trade_execution_not_approved
- validation blocker category: block_trading_autonomy_production_not_approved
- validation blocker category: block_audit_persistence_export_not_approved
- manual review handoff label: handoff_manual_review_required
- manual review handoff label: handoff_timestamp_check_required
- manual review handoff label: handoff_decision_time_check_required
- manual review handoff label: handoff_evidence_available_time_check_required
- manual review handoff label: handoff_forecast_issue_time_check_required
- manual review handoff label: handoff_observation_valid_time_check_required
- manual review handoff label: handoff_resolution_time_check_required
- manual review handoff label: handoff_source_time_conflict_check_required
- fail closed handoff label: handoff_fail_closed_lookahead_detected
- fail closed handoff label: handoff_fail_closed_timestamp_missing
- fail closed handoff label: handoff_fail_closed_timestamp_ambiguous
- fail closed handoff label: handoff_fail_closed_source_time_conflict
- fail closed handoff label: handoff_fail_closed_validation_unavailable
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
- blocked work: runtime_no_lookahead_validation
- blocked work: runtime_timestamp_validation
- blocked work: runtime_evidence_time_comparison
- blocked work: validation_output_persistence
- blocked work: runtime_metadata_implementation
- blocked work: stage2_runtime_module_modification
- blocked work: fail_closed_runtime_enforcement
- blocked work: runtime_error_handling
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
- implementation posture: no_lookahead_validation_planning_only
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
- implementation posture: no_runtime_no_lookahead_validation
- implementation posture: no_runtime_timestamp_validation
- implementation posture: no_runtime_evidence_time_comparison
- implementation posture: no_validation_output_persistence
- implementation posture: no_fail_closed_runtime_enforcement
- implementation posture: no_runtime_error_handling
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
- recommended next track: weather_bot_phase0a_fail_closed_validation_planning
- conditional next track: weather_bot_phase0a_no_lookahead_validation_revision_if_scope_too_broad
- evidence status: no_lookahead_validation_planning_recorded
- label confidence: confirmed

## Acceptance criteria

- The document exists with the canonical ID and required sections.
- The static test validates section-scoped machine-checkable assignments.
- The artifact remains docs/static-test-only/no-lookahead-validation-planning-only.
- Blocked work remains blocked:
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
- `runtime_no_lookahead_validation`
- `runtime_timestamp_validation`
- `runtime_evidence_time_comparison`
- `validation_output_persistence`
- `runtime_metadata_implementation`
- `stage2_runtime_module_modification`
- `fail_closed_runtime_enforcement`
- `runtime_error_handling`
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
