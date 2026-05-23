-- PRD-0B-IMPL-06 Bronze view skeleton.
-- Unresolved-state taxonomy reference:
-- none, missing_source_record, missing_required_raw_field, malformed_raw_value,
-- unresolved_ticker_ref, unresolved_event_ref, unresolved_result, unresolved_taker_side,
-- unresolved_condition_ref, unresolved_token_ref, unresolved_token_outcome_mapping,
-- unresolved_block_timestamp, timestamp_mismatch, unresolved_legacy_fpmm_ref,
-- unresolved_collateral_ref, unsupported_source_shape

CREATE OR REPLACE VIEW bronze_kalshi_markets AS
SELECT
    *,
    'kalshi_markets' AS source_dataset,
    'data/kalshi/markets' AS source_relative_path,
    'v0_skeleton' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    'none' AS unresolved_status,
    COALESCE(CAST(ticker_ref AS VARCHAR), 'missing_source_record') AS source_record_ref
FROM source_kalshi_markets;

CREATE OR REPLACE VIEW bronze_kalshi_trades AS
SELECT
    *,
    'kalshi_trades' AS source_dataset,
    'data/kalshi/trades' AS source_relative_path,
    'v0_skeleton' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    'none' AS unresolved_status,
    COALESCE(CAST(trade_ref AS VARCHAR), 'missing_source_record') AS source_record_ref
FROM source_kalshi_trades;

CREATE OR REPLACE VIEW bronze_poly_markets AS
SELECT
    *,
    'poly_markets' AS source_dataset,
    'data/polymarket/markets' AS source_relative_path,
    'v0_skeleton' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    'none' AS unresolved_status,
    COALESCE(CAST(condition_ref AS VARCHAR), 'missing_source_record') AS source_record_ref
FROM source_poly_markets;

CREATE OR REPLACE VIEW bronze_poly_clob_trades AS
SELECT
    *,
    'poly_clob_trades' AS source_dataset,
    'data/polymarket/trades' AS source_relative_path,
    'v0_skeleton' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    'none' AS unresolved_status,
    COALESCE(CAST(transaction_ref AS VARCHAR), 'missing_source_record') AS source_record_ref
FROM source_poly_clob_trades;

CREATE OR REPLACE VIEW bronze_poly_blocks AS
SELECT
    *,
    'poly_blocks' AS source_dataset,
    'data/polymarket/blocks' AS source_relative_path,
    'v0_skeleton' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    'none' AS unresolved_status,
    COALESCE(CAST(block_ref AS VARCHAR), 'missing_source_record') AS source_record_ref
FROM source_poly_blocks;

CREATE OR REPLACE VIEW bronze_poly_legacy_fpmm_trades AS
SELECT
    *,
    'poly_legacy_fpmm_trades' AS source_dataset,
    'data/polymarket/legacy_trades' AS source_relative_path,
    'v0_skeleton' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    'none' AS unresolved_status,
    COALESCE(CAST(fpmm_ref AS VARCHAR), 'missing_source_record') AS source_record_ref
FROM source_poly_legacy_fpmm_trades;

CREATE OR REPLACE VIEW bronze_poly_fpmm_collateral_lookup AS
SELECT
    *,
    'poly_fpmm_collateral_lookup' AS source_dataset,
    'data/polymarket/fpmm_collateral_lookup.json' AS source_relative_path,
    'v0_skeleton' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    'none' AS unresolved_status,
    COALESCE(CAST(collateral_asset_ref AS VARCHAR), 'missing_source_record') AS source_record_ref
FROM source_poly_fpmm_collateral_lookup;
