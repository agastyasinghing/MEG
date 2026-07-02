# WEATHER-BOT-PHASE0A-STAGE2-METADATA-CONTRACT-DOCUMENTATION-01 — Weather Bot Phase 0A Stage 2 Metadata Contract Documentation

Canonical ID: WEATHER-BOT-PHASE0A-STAGE2-METADATA-CONTRACT-DOCUMENTATION-01

## Status and scope

This ticket is docs/static-test-only/stage2-metadata-contract-documentation-only. This ticket does not modify `meg/`. This ticket does not modify meta/handoff files. This ticket does not modify Stage 2 runtime metadata modules. This ticket does not revise the owner decision. This ticket does not reopen source-fetching implementation planning. This ticket does not fetch, create, or modify market data. This ticket does not create fixtures or generated data. This ticket does not implement runtime metadata behavior. This ticket does not implement runtime fail-closed enforcement. This ticket does not implement runtime error handling. This ticket does not implement runtime no-lookahead enforcement. This ticket does not implement runtime timestamp validation. This ticket does not implement runtime settlement-rule parsing or classification. This ticket does not implement runtime manual-review workflow behavior. This ticket does not implement scoring, backtesting, paper trading, trading, or autonomy. This ticket does not create a separate standalone self-review artifact. Weather Bot models the market settlement rule, not generic weather.

## Relationship to fail-closed error taxonomy planning

This artifact follows `docs/prd/WEATHER-BOT-PHASE0A-FAIL-CLOSED-ERROR-TAXONOMY-PLANNING-01.md` and its static test as the immediate predecessor. It records the Stage 2 metadata contract that future planning must preserve after the fail-closed taxonomy, without adding runtime behavior.

## Contract objective

The objective is to document the expected static metadata surfaces, supplied-metadata-only posture, fail-closed behavior, canonical identifier contract, no-lookahead metadata contract, manual-review metadata contract, and audit-surface metadata contract for future planning. It is not an implementation plan and grants no execution approval.

## Current held/closed source-fetching posture

Weather Bot Phase 0A remains held and closed for source-fetching runtime work. The source-fetching runtime track remains closed/held. The closed owner decision remains `hold_source_fetching_runtime_track`. Source fetching remains not implemented. Implementation approval remains not granted. Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed. Silence, continuation, lack of objection, and non-interference are not approval.

## No owner-decision revision boundary

No owner-decision revision is being made in this ticket. The closed owner decision remains `hold_source_fetching_runtime_track`; this artifact does not proceed to `source_fetching_runtime_implementation_plan` and does not approve source-fetching implementation planning.

## Stage 2 metadata contract overview

Existing Stage 2 runtime metadata artifacts are documentation references only for this ticket:
- `meg/weather/stage2/source_identity_runtime.py` — existing supplied-metadata-only fail-closed scaffold; referenced, not modified.
- `meg/weather/stage2/retrieval_context_runtime.py` — existing supplied-metadata-only fail-closed scaffold; referenced, not modified.
- `meg/weather/stage2/provider_source_family_runtime.py` — existing supplied-metadata-only fail-closed scaffold; referenced, not modified.
- `meg/weather/stage2/manual_review_gate_runtime.py` — existing supplied-metadata-only fail-closed scaffold; referenced, not modified.
- `meg/weather/stage2/no_lookahead_metadata_runtime.py` — existing supplied-metadata-only fail-closed scaffold; referenced, not modified.
- `meg/weather/stage2/fail_closed_validation_runtime.py` — existing supplied-metadata-only fail-closed scaffold; referenced, not modified.
- `meg/weather/stage2/static_audit_surface_runtime.py` — existing supplied-metadata-only fail-closed scaffold; referenced, not modified.

Static documentation fields only:
- `source_identity_status` — static contract field documented for future planning, not runtime implementation.
- `source_identity_label` — static contract field documented for future planning, not runtime implementation.
- `retrieval_context_status` — static contract field documented for future planning, not runtime implementation.
- `retrieval_context_label` — static contract field documented for future planning, not runtime implementation.
- `provider_source_family_status` — static contract field documented for future planning, not runtime implementation.
- `provider_source_family_label` — static contract field documented for future planning, not runtime implementation.
- `manual_review_gate_status` — static contract field documented for future planning, not runtime implementation.
- `manual_review_gate_reason` — static contract field documented for future planning, not runtime implementation.
- `no_lookahead_status` — static contract field documented for future planning, not runtime implementation.
- `no_lookahead_reason` — static contract field documented for future planning, not runtime implementation.
- `fail_closed_validation_status` — static contract field documented for future planning, not runtime implementation.
- `fail_closed_reason` — static contract field documented for future planning, not runtime implementation.
- `static_audit_surface_status` — static contract field documented for future planning, not runtime implementation.
- `static_audit_surface_label` — static contract field documented for future planning, not runtime implementation.
- `supplied_metadata_only` — static contract field documented for future planning, not runtime implementation.
- `metadata_missing_requires_fail_closed` — static contract field documented for future planning, not runtime implementation.
- `metadata_ambiguous_requires_manual_review` — static contract field documented for future planning, not runtime implementation.
- `metadata_conflict_requires_fail_closed` — static contract field documented for future planning, not runtime implementation.

Stage 2 contract posture values:
- `supplied_metadata_only`
- `fail_closed_by_default`
- `manual_review_required_on_ambiguity`
- `no_runtime_fetching`
- `no_provider_execution`
- `no_credentials_required`
- `no_generated_data_required`
- `no_fixture_required`
- `no_scoring_required`
- `no_trading_required`
- `no_export_required`

## Source identity metadata contract

This section documents `source identity metadata contract` as a static planning contract only. Missing metadata requires fail-closed handling; ambiguous metadata requires manual review; conflicting metadata requires fail-closed handling. No runtime metadata behavior is implemented here.

## Retrieval context metadata contract

This section documents `retrieval context metadata contract` as a static planning contract only. Missing metadata requires fail-closed handling; ambiguous metadata requires manual review; conflicting metadata requires fail-closed handling. No runtime metadata behavior is implemented here.

## Provider source family metadata contract

This section documents `provider source family metadata contract` as a static planning contract only. Missing metadata requires fail-closed handling; ambiguous metadata requires manual review; conflicting metadata requires fail-closed handling. No runtime metadata behavior is implemented here.

## Manual-review gate metadata contract

This section documents `manual-review gate metadata contract` as a static planning contract only. Missing metadata requires fail-closed handling; ambiguous metadata requires manual review; conflicting metadata requires fail-closed handling. No runtime metadata behavior is implemented here.

## No-lookahead metadata contract

This section documents `no-lookahead metadata contract` as a static planning contract only. Missing metadata requires fail-closed handling; ambiguous metadata requires manual review; conflicting metadata requires fail-closed handling. No runtime metadata behavior is implemented here.

## Fail-closed validation metadata contract

This section documents `fail-closed validation metadata contract` as a static planning contract only. Missing metadata requires fail-closed handling; ambiguous metadata requires manual review; conflicting metadata requires fail-closed handling. No runtime metadata behavior is implemented here.

## Static audit surface metadata contract

This section documents `static audit surface metadata contract` as a static planning contract only. Missing metadata requires fail-closed handling; ambiguous metadata requires manual review; conflicting metadata requires fail-closed handling. No runtime metadata behavior is implemented here.

## Canonical identifier posture

Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`. Future reasoning must preserve all three canonical shared-rail identifiers. Future reasoning must preserve the relationship between `token_id` and `outcome`. `token_outcome_pair` remains a derived relationship, not a replacement for canonical fields. `market_id` remains explicitly non-routing only. No routing on `market_id` is introduced or approved. A `market_identifier_routing_attempt` remains fail-closed.

## Supplied-metadata-only boundary

The contract posture is `supplied_metadata_only`: future planning may reason about caller-supplied metadata fields, but this ticket creates no provider/source retrieval, generated data, fixture data, or runtime metadata implementation.

## Fail-closed contract boundary

The contract posture is `fail_closed_by_default`: metadata missing requires fail-closed, metadata conflict requires fail-closed, and metadata ambiguity requires manual review. This is documentation only and does not implement runtime fail-closed enforcement or runtime error handling.

## Static documentation only boundary

This artifact is static documentation and a static test only. It does not modify `meg/`, workflow files, dependency files, schemas, migrations, secrets, credentials, environment files, config, or config-loading behavior.

## Source-fetching track remains blocked

The source-fetching runtime track remains closed/held. Source fetching remains not implemented. Implementation approval remains not granted. `source_fetching_runtime_implementation_plan`, `source_fetching_implementation`, and owner-decision revision remain blocked work.

## Provider/source execution boundary

Provider connectors remain not approved. Provider clients remain not created. Live provider/source fetching remains not approved. Forecast pull execution, API call execution, scraping execution, file download execution, and provider SDK execution remain not approved.

## Credential/config boundary

Credentials/config loading remains not approved. This ticket does not modify `.env`, secrets, credentials, config, or config-loading behavior.

## Generated-data and fixture boundary

Generated data and fixtures remain not approved. This ticket does not create fixtures or generated data and does not modify `tests/fixtures/`.

## Scoring/backtesting boundary

Scoring/backtesting remains not approved. This ticket does not implement scoring or backtesting.

## Paper-trade boundary

Paper-trade execution remains not approved. This ticket does not implement paper-trade execution.

## Trading/autonomy/production boundary

Runtime trading/order placement/autonomy/production remains not approved. This ticket does not implement trading, order placement, autonomy, or production behavior.

## Audit report and export boundary

Report writing, audit output persistence, and external export remain not approved. This ticket does not create audit reports, export files, persisted audit output, or external export behavior.

## Stage 2 runtime metadata posture

Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed. The existing runtime metadata modules are referenced only and are not modified by this documentation ticket.

## Embedded self-review requirement

The PR must be self-reviewed using the secondary self-review prompt before asking for review. The self-review result must be summarized in the PR body. Do not create a separate standalone self-review PRD artifact for this ticket. Do not recommend a standalone self-review ticket as the next ticket.

## Recommended next ticket

Recommended next ticket: `weather_bot_phase0a_paper_trade_readiness_gap_inventory`. This is the next main safe lane from the non-source-fetching inventory; it must not revise the owner decision and must not implement source fetching. Do not recommend a standalone self-review ticket.

## Machine-checkable Weather Bot Phase 0A stage2-metadata-contract-documentation assignments

- weather bot planning stage: weather_bot_phase0a_stage2_metadata_contract_documentation
- stage2 metadata contract status: docs_static_test_only
- stage2 metadata contract status: stage2_metadata_contract_documentation_only
- stage2 metadata contract status: post_weather_bot_phase0a_fail_closed_error_taxonomy_planning
- self review posture: embedded_secondary_prompt_only
- self review posture: no_standalone_self_review_prd
- owner decision posture: no_owner_decision_revision
- owner decision posture: hold_source_fetching_runtime_track_preserved
- source fetching track posture: closed_held
- source fetching track posture: no_source_fetching_implementation_plan
- source fetching track posture: no_source_fetching_implementation
- source fetching track posture: implementation_approval_not_granted
- stage2 metadata artifact: source_identity_runtime_py
- stage2 metadata artifact: retrieval_context_runtime_py
- stage2 metadata artifact: provider_source_family_runtime_py
- stage2 metadata artifact: manual_review_gate_runtime_py
- stage2 metadata artifact: no_lookahead_metadata_runtime_py
- stage2 metadata artifact: fail_closed_validation_runtime_py
- stage2 metadata artifact: static_audit_surface_runtime_py
- stage2 metadata contract field: source_identity_status
- stage2 metadata contract field: source_identity_label
- stage2 metadata contract field: retrieval_context_status
- stage2 metadata contract field: retrieval_context_label
- stage2 metadata contract field: provider_source_family_status
- stage2 metadata contract field: provider_source_family_label
- stage2 metadata contract field: manual_review_gate_status
- stage2 metadata contract field: manual_review_gate_reason
- stage2 metadata contract field: no_lookahead_status
- stage2 metadata contract field: no_lookahead_reason
- stage2 metadata contract field: fail_closed_validation_status
- stage2 metadata contract field: fail_closed_reason
- stage2 metadata contract field: static_audit_surface_status
- stage2 metadata contract field: static_audit_surface_label
- stage2 metadata contract field: supplied_metadata_only
- stage2 metadata contract field: metadata_missing_requires_fail_closed
- stage2 metadata contract field: metadata_ambiguous_requires_manual_review
- stage2 metadata contract field: metadata_conflict_requires_fail_closed
- stage2 contract posture: supplied_metadata_only
- stage2 contract posture: fail_closed_by_default
- stage2 contract posture: manual_review_required_on_ambiguity
- stage2 contract posture: no_runtime_fetching
- stage2 contract posture: no_provider_execution
- stage2 contract posture: no_credentials_required
- stage2 contract posture: no_generated_data_required
- stage2 contract posture: no_fixture_required
- stage2 contract posture: no_scoring_required
- stage2 contract posture: no_trading_required
- stage2 contract posture: no_export_required
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
- blocked work: runtime_metadata_implementation
- blocked work: stage2_runtime_module_modification
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
- implementation posture: docs_static_test_only
- implementation posture: stage2_metadata_contract_documentation_only
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
- recommended next track: weather_bot_phase0a_paper_trade_readiness_gap_inventory
- conditional next track: weather_bot_phase0a_stage2_metadata_contract_revision_if_scope_too_broad
- evidence status: stage2_metadata_contract_documentation_recorded
- label confidence: confirmed

## Acceptance criteria

- The documentation artifact exists with the required canonical ID and all required sections.
- Static tests validate posture, boundaries, machine-checkable assignments, and recommended next ticket.
- Only docs/static-test files are changed; no runtime modules or meta/handoff files are modified.
