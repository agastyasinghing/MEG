# PRD-0B-IMPL-03 Data Dictionary Contract (Static Preflight)

## 1) Purpose and posture
- This document is **PRD-0B-IMPL-03** data dictionary generation plan/static contract.
- This ticket is **docs/static-preflight only**.
- This ticket does **not generate a data dictionary**.
- This ticket does **not read archive payloads**.
- This ticket does **not run DuckDB**.
- This ticket does **not implement Bronze/Silver views, loaders, query engines, connectors, API calls, order routing, live trading, or autonomy**.
- This document is a contract for a future generator.

## 2) PRD Phase 0B alignment
The master PRD requires Phase 0B research lake setup with DuckDB + Parquet + Becker archive posture, Bronze/Silver normalization views, data dictionary, seven sanity queries, and query latency gate. PRD-0B-IMPL-01 covered local research-lake smoke. PRD-0B-IMPL-02 covered the seven sanity-query harness. PRD-0B-IMPL-03 covers only the data dictionary static contract, not generation.

## 3) Required dataset coverage (exactly seven families)
Unless changed by later approved PRD update, future dictionary coverage must include exactly:
1. kalshi_markets
2. kalshi_trades
3. poly_markets
4. poly_clob_trades
5. poly_blocks
6. poly_legacy_fpmm_trades
7. poly_fpmm_collateral_lookup

Each dataset maps to:
- source_platform
- source_kind (parquet_family or json_sidecar)
- source_relative_path
- related_sanity_check_name (from PRD-0B-IMPL-02)
- related_bronze_schema (from Phase 1R Bronze contracts)
- related_normalization_plan

## 3A) Dataset family mapping table
| dataset_ref | source_platform | source_kind | source_relative_path | related_sanity_check_name | related_bronze_schema | related_normalization_plan |
|---|---|---|---|---|---|---|
| kalshi_markets | kalshi | parquet_family | data/kalshi/markets | kalshi_markets_schema_count_sample | bronze_kalshi_market | docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md |
| kalshi_trades | kalshi | parquet_family | data/kalshi/trades | kalshi_trades_schema_count_sample | bronze_kalshi_trade | docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md |
| poly_markets | polymarket | parquet_family | data/polymarket/markets | poly_markets_schema_count_sample | bronze_poly_market | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md |
| poly_clob_trades | polymarket | parquet_family | data/polymarket/trades | poly_clob_trades_schema_count_sample | bronze_poly_clob_trade | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md |
| poly_blocks | polymarket | parquet_family | data/polymarket/blocks | poly_blocks_schema_count_sample | bronze_poly_block | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md |
| poly_legacy_fpmm_trades | polymarket | parquet_family | data/polymarket/legacy_trades | poly_legacy_fpmm_trades_schema_count_sample | bronze_poly_legacy_fpmm_trade | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md |
| poly_fpmm_collateral_lookup | polymarket | json_sidecar | data/polymarket/fpmm_collateral_lookup.json | poly_fpmm_collateral_lookup_presence | bronze_poly_fpmm_collateral_lookup | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md |

## 4) Data dictionary top-level shape
Required top-level fields:
- dictionary_ref
- schema_version
- phase
- dictionary_status
- created_by
- created_at
- source_manifest_ref
- source_repo_ref
- source_repo_commit
- source_archive_ref
- generation_mode
- dataset_entries
- global_posture
- artifact_hygiene
- reviewer_envelope

`dictionary_status` allowlist:
- planned_contract_only
- generated_pending_review
- committed_reviewed_dictionary

For this ticket: only `planned_contract_only` is allowed.

`generation_mode` allowlist:
- static_contract
- local_generated_from_sanity_harness

For this ticket: only `static_contract` is allowed.

## 5) global_posture contract
Required fields:
- research_only
- local_only
- archive_payload_read_allowed
- duckdb_execution_allowed
- generated_output_allowed
- committed_data_allowed
- fixture_commit_allowed
- bronze_silver_view_creation_allowed
- loader_execution_allowed
- connector_import_allowed
- api_calls_allowed
- order_routing_allowed
- live_trading_allowed
- autonomous_execution_allowed

For this static contract:
- research_only = true
- local_only = true
- all other allowed flags = false

## 6) artifact_hygiene contract
Required fields:
- no_archive_payload_reads
- no_generated_dictionary_file
- no_duckdb_artifacts
- no_generated_reports
- no_committed_archive_data
- no_fixture_outputs
- no_external_repo_files
- no_secret_material
- no_absolute_archive_paths

All artifact_hygiene fields are true for this ticket.

## 7) Dataset entry shape
Each dataset entry must include:
- dataset_ref
- source_platform
- source_kind
- source_relative_path
- related_sanity_check_name
- related_bronze_schema
- related_normalization_plan
- expected_columns
- primary_reference_fields
- temporal_fields
- numeric_fields
- boolean_fields
- json_fields
- provenance_fields
- unresolved_state_fields
- known_raw_field_aliases
- future_dictionary_status
- notes

## 8) Column metadata shape
Future column metadata entry shape:
- column_name
- source_name
- logical_role
- raw_type_observed
- normalized_type_target
- nullable_status
- semantic_notes
- validation_notes
- pii_or_secret_status
- used_for_joining
- used_for_time_filtering
- used_for_price_or_size
- used_for_resolution_or_result
- used_for_wallet_or_actor
- unresolved_handling

Raw-type observation status placeholders allowed in this static contract:
- not_observed_static_contract
- planned_from_inspection_notes
- requires_future_generation

## 9) Dataset-specific expected columns
### A) kalshi_markets
- ticker
- event_ticker
- market_type
- title
- yes_sub_title
- no_sub_title
- status
- yes_bid
- yes_ask
- no_bid
- no_ask
- last_price
- volume
- volume_24h
- open_interest
- result
- created_time
- open_time
- close_time
- _fetched_at

### B) kalshi_trades
- trade_id
- ticker
- count
- yes_price
- no_price
- taker_side
- created_time
- _fetched_at

### C) poly_markets
- id
- condition_id
- question
- slug
- outcomes
- outcome_prices
- clob_token_ids
- volume
- liquidity
- active
- closed
- end_date
- created_at
- market_maker_address
- _fetched_at

### D) poly_clob_trades
- block_number
- transaction_hash
- log_index
- order_hash
- maker
- taker
- maker_asset_id
- taker_asset_id
- maker_amount
- taker_amount
- fee
- timestamp
- _fetched_at
- _contract

### E) poly_blocks
- block_number
- timestamp

### F) poly_legacy_fpmm_trades
- block_number
- transaction_hash
- log_index
- fpmm_address
- trader
- amount
- fee_amount
- outcome_index
- outcome_tokens
- is_buy
- timestamp
- _fetched_at

### G) poly_fpmm_collateral_lookup
- fpmm_or_contract_ref
- collateral_token
- collateral_symbol
- collateral_decimals

## 10) Status taxonomy
`future_dictionary_status` allowlist:
- planned_only
- generated_from_local_archive
- reviewed
- stale_needs_regeneration
- rejected

For this ticket, all dataset entries are `planned_only`.

`pii_or_secret_status` allowlist:
- no_private_pii_expected
- public_chain_address_or_actor_ref
- unknown_needs_review
- secret_disallowed

## 11) Future generation rules
Future generator must:
- run only after explicit approval
- use local archive root only
- use PRD-0B-IMPL-02 sanity harness results as input where possible
- use DuckDB only if dependency posture is approved
- write only to explicitly approved dictionary output path
- never commit archive data
- never embed absolute local archive paths
- never include secrets/API keys/private PII
- preserve source_relative_path only
- record source repo/ref/checksum metadata
- record generated timestamp and reviewer reference
- fail closed if required datasets or columns are missing
- never imply execution readiness

## 12) Relationship to Bronze/Silver
- Data dictionary is not Bronze/Silver view implementation.
- It supports future Bronze/Silver view implementation planning.
- It maps raw fields to logical roles and future target types.
- Silver normalization remains a later ticket.
- Cross-platform opportunity labeling remains out of scope.

## 13) Recommended next tickets
- PRD-0B-IMPL-04 Bronze/Silver view implementation plan
- PRD-0B-IMPL-05 data dictionary local generator (only after explicit approval and dependency posture decision)
- PRD-0A-AUDIT-01 shared rail implementation gap audit (parallel)
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved

## 14) Explicit non-approvals
- no data dictionary generation
- no archive reads
- no DuckDB execution
- no generated outputs
- no .duckdb files
- no fixture derivation
- no fixture commit
- no data import
- no Bronze/Silver view implementation
- no loader implementation
- no query engine service
- no connector implementation
- no API calls
- no order placement
- no live trading
- no autonomous execution
- no weather implementation
