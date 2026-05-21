# Phase 1-06 — Bronze Schema Definitions (Docs + Static/Preflight Only)

## 1) Purpose and posture

This is the **Phase 1-06 Bronze schema definition document**.

This ticket is **documentation + static/preflight only**.

This ticket does **not** generate, derive, or commit fixtures.

This ticket does **not** read archive payloads (no Parquet/JSON archive row reads).

This ticket does **not** implement DuckDB, loaders, query engines, connectors, API calls, order routing, live trading, or autonomous execution.

These Bronze schemas are planning contracts for future fixture-backed records.

## 2) PRD alignment note

The frozen master PRD states that the real Phase 1 target is the **weather paper engine**.

The repository sequence used here is a conservative fixture/Bronze foundation that must exist before local research-lake workflow expansion.

This ticket does **not** implement the weather paper engine.

Future phase realignment must map this fixture/Bronze foundation back to the master PRD roadmap.

## 3) Bronze layer principles

- Bronze preserves raw source fields as faithfully as possible.
- Bronze adds provenance and parser metadata.
- Bronze does not perform Silver normalization.
- Bronze does not infer outcomes from titles, prices, or wallet fields alone.
- Bronze preserves unresolved/malformed states instead of dropping rows.
- Bronze records are tiny-fixture-compatible first.
- Bronze records must not include absolute local archive paths.
- Bronze records must not include secrets, API keys, or private PII.
- Bronze records must not imply execution readiness.

## 4) Common Bronze metadata fields

All Bronze fixture-backed records must include:

- `fixture_ref`
- `fixture_family`
- `source_platform`
- `source_manifest_ref`
- `source_repo_ref`
- `source_repo_commit`
- `source_archive_ref`
- `source_relative_path`
- `source_file_checksum`
- `source_record_index`
- `source_record_hash`
- `parser_version`
- `schema_version`
- `ingestion_mode`
- `record_status`
- `unresolved_reasons`
- `created_from_fixture`
- `execution_allowed`
- `live_trading_allowed`
- `autonomous_execution_allowed`

Rules:

- `ingestion_mode` allowlist:
  - `tiny_fixture`
  - `dry_run_contract`
- `record_status` allowlist:
  - `raw_preserved`
  - `parsed_with_warnings`
  - `malformed_preserved`
  - `unresolved_preserved`
- `created_from_fixture` is true for committed tiny fixtures and false for dry-run examples.
- `execution_allowed`, `live_trading_allowed`, and `autonomous_execution_allowed` must remain false.

## 5) Seven Bronze record contracts

### A) `bronze_kalshi_market`

Raw fields:

- `ticker`
- `event_ticker`
- `market_type`
- `title`
- `yes_sub_title`
- `no_sub_title`
- `status`
- `yes_bid`
- `yes_ask`
- `no_bid`
- `no_ask`
- `last_price`
- `volume`
- `volume_24h`
- `open_interest`
- `result`
- `created_time`
- `open_time`
- `close_time`
- `fetched_at`

Additional Bronze fields:

- `price_fields_preserved`
- `result_preserved`
- `event_grouping_unresolved`

### B) `bronze_kalshi_trade`

Raw fields:

- `trade_id`
- `ticker`
- `count`
- `yes_price`
- `no_price`
- `taker_side`
- `created_time`
- `fetched_at`

Additional Bronze fields:

- `linked_market_unresolved`
- `taker_side_preserved`
- `price_fields_preserved`

### C) `bronze_poly_market`

Raw fields:

- `source_market_ref`
- `condition_id`
- `question`
- `slug`
- `outcomes`
- `outcome_prices`
- `clob_token_ids`
- `volume`
- `liquidity`
- `active`
- `closed`
- `end_date`
- `created_at`
- `market_maker_address`
- `fetched_at`

Additional Bronze fields:

- `outcomes_preserved`
- `clob_token_ids_preserved`
- `token_mapping_unresolved`

### D) `bronze_poly_clob_trade`

Raw fields:

- `block_number`
- `transaction_hash`
- `log_index`
- `order_hash`
- `maker`
- `taker`
- `maker_asset_id`
- `taker_asset_id`
- `maker_amount`
- `taker_amount`
- `fee`
- `timestamp`
- `fetched_at`
- `contract_ref`

Additional Bronze fields:

- `maker_asset_preserved`
- `taker_asset_preserved`
- `token_mapping_unresolved`
- `direction_unresolved`

### E) `bronze_poly_block`

Raw fields:

- `block_number`
- `timestamp`

Additional Bronze fields:

- `block_timestamp_preserved`

### F) `bronze_poly_legacy_fpmm_trade`

Raw fields:

- `block_number`
- `transaction_hash`
- `log_index`
- `fpmm_address`
- `trader`
- `amount`
- `fee_amount`
- `outcome_index`
- `outcome_tokens`
- `is_buy`
- `timestamp`
- `fetched_at`

Additional Bronze fields:

- `legacy_fpmm_path`
- `outcome_tokens_preserved`
- `collateral_mapping_unresolved`

### G) `bronze_poly_fpmm_collateral_lookup`

Raw fields:

- `fpmm_or_contract_ref`
- `collateral_token`
- `collateral_symbol`
- `collateral_decimals`

Additional Bronze fields:

- `collateral_lookup_preserved`

## 6) Unresolved reason taxonomy

Bronze unresolved reason allowlist:

- `none`
- `missing_required_raw_field`
- `malformed_raw_value`
- `missing_source_provenance`
- `unresolved_event_grouping`
- `unresolved_ticker_link`
- `unresolved_token_mapping`
- `unresolved_direction`
- `unresolved_block_timestamp`
- `unresolved_legacy_fpmm_mapping`
- `unresolved_collateral_mapping`
- `unsupported_fixture_family`
- `unsupported_source_shape`

## 7) Fixture family to Bronze schema mapping

- `kalshi_markets_tiny` -> `bronze_kalshi_market`
- `kalshi_trades_tiny` -> `bronze_kalshi_trade`
- `poly_markets_tiny` -> `bronze_poly_market`
- `poly_clob_trades_tiny` -> `bronze_poly_clob_trade`
- `poly_blocks_tiny` -> `bronze_poly_block`
- `poly_legacy_fpmm_trades_tiny` -> `bronze_poly_legacy_fpmm_trade`
- `poly_fpmm_collateral_lookup_tiny` -> `bronze_poly_fpmm_collateral_lookup`

## 8) Relation to future Silver normalization

Bronze does not create `silver_kalshi_markets`, `silver_kalshi_fills`, `silver_poly_markets`, `silver_poly_outcomes`, or `silver_poly_clob_fills`.

Bronze only preserves raw source records with provenance.

Silver normalization must be a later phase/ticket after tiny fixture commit and Bronze validation.

Cross-platform equivalence/opportunity labels remain blocked at Bronze.

## 9) Future implementation notes

Future implementation may:

- define these schemas as dataclasses/Pydantic/TypedDict/etc. in a later ticket,
- load committed tiny JSON fixtures only after fixture commit approval,
- validate Bronze records against these contracts,
- build Bronze-to-Silver normalization only after Phase 1 closeout/readiness review.
