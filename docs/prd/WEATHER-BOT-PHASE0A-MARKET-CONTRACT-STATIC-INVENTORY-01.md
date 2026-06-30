# WEATHER-BOT-PHASE0A-MARKET-CONTRACT-STATIC-INVENTORY-01 — Weather Bot Phase 0A Market Contract Static Inventory

Canonical ID: WEATHER-BOT-PHASE0A-MARKET-CONTRACT-STATIC-INVENTORY-01

## Status and scope

This is docs/static-test-only/market-contract-static-inventory-only. This ticket does not modify `meg/`. This ticket does not modify meta/handoff files. This ticket does not modify `docs/meta/MEG_ACTIVE_STATE.md`, `docs/meta/MEG_CHAT_HANDOFF.md`, or `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`. This ticket is not an owner-decision revision, not source-fetching implementation, not source-fetching implementation planning, and not approval of any implementation plan.

## Relationship to non-source-fetching scope inventory self-review

This artifact follows `docs/prd/WEATHER-BOT-PHASE0A-NON-SOURCE-FETCHING-SCOPE-INVENTORY-SELF-REVIEW-01.md` and `tests/core/test_weather_bot_phase0a_non_source_fetching_scope_inventory_self_review_01.py` after PR #285 landed. It narrows the previously recorded safe inventory lane `market_contract_static_inventory` into a docs/static-test-only market-contract field inventory. It does not revise the owner decision and does not reopen source-fetching implementation planning.

## Inventory objective

The objective is to identify static market-contract fields and contract-shape requirements Weather Bot must preserve and reason about later for settlement-rule-aware reasoning. Weather Bot models the market settlement rule, not generic weather. This ticket does not fetch, create, or modify market data, and it does not create fixtures or generated data.

## Current held/closed source-fetching posture

Weather Bot Phase 0A remains held and closed for source-fetching runtime work. The source-fetching runtime track remains closed/held. The closed owner decision remains `hold_source_fetching_runtime_track`. Source fetching remains not implemented. Implementation approval remains not granted. Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed.

## No owner-decision revision boundary

No owner-decision revision is being made in this ticket. This ticket does not revise the owner decision. Silence, continuation, lack of objection, and non-interference are not approval. This ticket does not proceed to `source_fetching_runtime_implementation_plan` and does not approve source-fetching implementation planning.

## Market contract fields to preserve

The static market-contract field categories to preserve are:

- `condition_id`
- `token_id`
- `outcome`
- `question_text`
- `market_slug`
- `market_title`
- `market_description`
- `resolution_source_text`
- `settlement_rule_text`
- `outcome_label`
- `token_outcome_pair`
- `open_time`
- `close_time`
- `resolution_time`
- `event_start_time`
- `event_end_time`
- `market_status`
- `operator_review_required`
- `manual_review_reason`

These field categories are static inventory only. They are not market-data fetching requirements and do not approve schema, fixture, connector, provider-client, or runtime code changes.

## Market contract fields not used for routing

`market_id` must not be used for routing. If `market_id` appears in Weather Bot planning, it may only be mentioned as a legacy/non-routing identifier in a negative boundary statement. This artifact does not introduce or approve routing on `market_id`.

## Settlement-rule contract fields

Settlement-rule-aware reasoning must preserve the market-facing contract text that defines what the market settles on, including `question_text`, `market_title`, `market_description`, `resolution_source_text`, and `settlement_rule_text`. Weather Bot models the market settlement rule, not generic weather, and this inventory does not fetch source records or pull forecasts.

## Outcome and token mapping fields

Outcome and token mapping must preserve `condition_id`, `token_id`, `outcome`, `outcome_label`, and `token_outcome_pair`. These fields support later operator-reviewed reasoning about the exact outcome-token relationship, but this ticket does not create mappings from live markets or generated examples.

## Timing and lifecycle fields

Timing and lifecycle inventory fields are `open_time`, `close_time`, `resolution_time`, `event_start_time`, `event_end_time`, and `market_status`. This ticket records these as contract-shape categories only and does not poll markets, download files, scrape pages, call APIs, or create fixtures.

## Operator-review fields

Operator review must preserve `operator_review_required` and `manual_review_reason`. These fields reinforce that later execution paths remain operator-reviewed and do not grant trading, order placement, autonomy, production behavior, report writing, persistence, or external export.

## Static inventory only boundary

This ticket is docs/static-test-only/market-contract-static-inventory-only. It does not fetch, create, or modify market data. It does not create fixtures or generated data. It does not modify `meg/`, meta/handoff files, runtime code, workflow files, dependency files, DB migrations, schemas, `.env`, secrets, credentials, config, or config-loading behavior.

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
- `scoring_implementation`
- `backtesting_implementation`
- `runtime_trading_behavior`
- `order_placement`
- `autonomy_behavior`
- `production_behavior`
- `audit_report_generation`
- `audit_output_persistence`
- `external_export_behavior`

## Provider/source execution boundary

Provider connectors remain not approved. Provider clients remain not created. Live provider/source fetching remains not approved. Forecast pulls, API calls, scraping, file downloads, and provider SDK usage remain not approved.

## Credential/config boundary

Credentials/config loading remains not approved. This ticket does not modify `.env`, secrets, credentials, config, or config-loading behavior.

## Generated-data and fixture boundary

Generated data and fixtures remain not approved. This ticket does not create generated data, does not create fixtures, and does not modify `tests/fixtures/`.

## Scoring/backtesting boundary

Scoring/backtesting remains not approved. This ticket does not create scoring logic, evaluation execution, historical backtests, or runtime model behavior.

## Trading/autonomy/production boundary

Runtime trading/order placement/autonomy/production remains not approved. This ticket does not approve trading, order placement, autonomous behavior, production jobs, queues, schedulers, or runtime execution.

## Audit report and export boundary

Report writing, audit output persistence, and external export remain not approved. This ticket does not create audit reports, export files, persisted audit output, or external export behavior.

## Canonical identifier posture

The canonical shared-rail routing fields are:

- `condition_id`
- `token_id`
- `outcome`

`condition_id`, `token_id`, and `outcome` are canonical shared-rail identifiers. `market_id` is explicitly non-routing only and must not be used for routing. No routing on `market_id` is introduced or approved.

## Stage 2 runtime metadata posture

Stage 2 runtime metadata scaffolds remain supplied-metadata-only and fail-closed. The Stage 2 runtime metadata artifact paths are:

- `meg/weather/stage2/source_identity_runtime.py`
- `meg/weather/stage2/retrieval_context_runtime.py`
- `meg/weather/stage2/provider_source_family_runtime.py`
- `meg/weather/stage2/manual_review_gate_runtime.py`
- `meg/weather/stage2/no_lookahead_metadata_runtime.py`
- `meg/weather/stage2/fail_closed_validation_runtime.py`
- `meg/weather/stage2/static_audit_surface_runtime.py`

## Recommended next ticket

Recommended next ticket: `weather_bot_phase0a_market_contract_static_inventory_self_review`.

This next ticket should be the secondary docs/static-test-only self-review prompt/pass for this market-contract static inventory PR. It must not revise the owner decision and must not implement source fetching. It must not approve source-fetching implementation planning.

## Machine-checkable Weather Bot Phase 0A market-contract static-inventory assignments

- weather bot planning stage: weather_bot_phase0a_market_contract_static_inventory
- market contract inventory status: docs_static_test_only
- market contract inventory status: market_contract_static_inventory_only
- market contract inventory status: post_weather_bot_phase0a_non_source_fetching_scope_inventory_self_review
- owner decision posture: no_owner_decision_revision
- owner decision posture: hold_source_fetching_runtime_track_preserved
- source fetching track posture: closed_held
- source fetching track posture: no_source_fetching_implementation_plan
- source fetching track posture: no_source_fetching_implementation
- source fetching track posture: implementation_approval_not_granted
- market contract field: condition_id
- market contract field: token_id
- market contract field: outcome
- market contract field: question_text
- market contract field: market_slug
- market contract field: market_title
- market contract field: market_description
- market contract field: resolution_source_text
- market contract field: settlement_rule_text
- market contract field: outcome_label
- market contract field: token_outcome_pair
- market contract field: open_time
- market contract field: close_time
- market contract field: resolution_time
- market contract field: event_start_time
- market contract field: event_end_time
- market contract field: market_status
- market contract field: operator_review_required
- market contract field: manual_review_reason
- canonical routing field: condition_id
- canonical routing field: token_id
- canonical routing field: outcome
- non routing field: market_id
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
- blocked work: scoring_implementation
- blocked work: backtesting_implementation
- blocked work: runtime_trading_behavior
- blocked work: order_placement
- blocked work: autonomy_behavior
- blocked work: production_behavior
- blocked work: audit_report_generation
- blocked work: audit_output_persistence
- blocked work: external_export_behavior
- stage2 runtime metadata artifact: source_identity_runtime_py
- stage2 runtime metadata artifact: retrieval_context_runtime_py
- stage2 runtime metadata artifact: provider_source_family_runtime_py
- stage2 runtime metadata artifact: manual_review_gate_runtime_py
- stage2 runtime metadata artifact: no_lookahead_metadata_runtime_py
- stage2 runtime metadata artifact: fail_closed_validation_runtime_py
- stage2 runtime metadata artifact: static_audit_surface_runtime_py
- implementation posture: docs_static_test_only
- implementation posture: market_contract_static_inventory_only
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
- implementation posture: no_scoring_backtesting
- implementation posture: no_trading_autonomy_production
- implementation posture: no_report_writing
- implementation posture: no_external_export
- implementation posture: no_persistence
- recommended next track: weather_bot_phase0a_market_contract_static_inventory_self_review
- conditional next track: weather_bot_phase0a_market_contract_static_inventory_revision_if_scope_too_broad
- evidence status: market_contract_static_inventory_recorded
- label confidence: confirmed

## Acceptance criteria

- Market-contract static inventory document exists with the required title, canonical ID, and all required sections.
- Static test validates this docs/static-test-only/market-contract-static-inventory-only posture without importing production runtime modules.
- This ticket does not modify `meg/` and does not modify meta/handoff files.
- This ticket does not revise the owner decision and does not reopen source-fetching implementation planning.
- Weather Bot models the market settlement rule, not generic weather.
- Source-fetching runtime work remains held, closed, not implemented, and not approved.
- The closed owner decision remains `hold_source_fetching_runtime_track`.
- All required market contract fields are inventoried as static field categories only.
- Canonical routing remains limited to `condition_id`, `token_id`, and `outcome`; `market_id` remains explicitly non-routing only.
- Provider/source execution, credentials/config loading, generated data, fixture changes, scoring/backtesting, trading/autonomy/production behavior, report writing, persistence, and external export remain not approved.
