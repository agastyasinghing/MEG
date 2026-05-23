-- PRD-0B-IMPL-07 Bronze semantic-hardening view contract.

CREATE OR REPLACE VIEW bronze_kalshi_markets AS
SELECT
    *,
    'kalshi_markets' AS source_dataset,
    'kalshi' AS source_platform,
    'data/kalshi/markets' AS source_relative_path,
    'v0_semantic_hardening' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    COALESCE(CAST(ticker_ref AS VARCHAR), 'missing_source_record') AS source_record_ref,
    CASE WHEN ticker_ref IS NULL THEN 'missing_required_raw_field' ELSE 'none' END AS bronze_unresolved_status,
    CASE WHEN ticker_ref IS NULL THEN 'missing' ELSE 'present' END AS required_field_status
FROM source_kalshi_markets;

CREATE OR REPLACE VIEW bronze_kalshi_trades AS
SELECT
    *, 'kalshi_trades' AS source_dataset, 'kalshi' AS source_platform,
    'data/kalshi/trades' AS source_relative_path, 'v0_semantic_hardening' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    COALESCE(CAST(trade_ref AS VARCHAR), 'missing_source_record') AS source_record_ref,
    CASE WHEN trade_ref IS NULL OR ticker_ref IS NULL THEN 'missing_required_raw_field' ELSE 'none' END AS bronze_unresolved_status,
    CASE WHEN trade_ref IS NULL OR ticker_ref IS NULL THEN 'missing' ELSE 'present' END AS required_field_status
FROM source_kalshi_trades;

CREATE OR REPLACE VIEW bronze_poly_markets AS
SELECT
    *, 'poly_markets' AS source_dataset, 'polymarket' AS source_platform,
    'data/polymarket/markets' AS source_relative_path, 'v0_semantic_hardening' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    COALESCE(CAST(condition_ref AS VARCHAR), 'missing_source_record') AS source_record_ref,
    CASE WHEN condition_ref IS NULL THEN 'missing_required_raw_field' ELSE 'none' END AS bronze_unresolved_status,
    CASE WHEN condition_ref IS NULL THEN 'missing' ELSE 'present' END AS required_field_status
FROM source_poly_markets;

CREATE OR REPLACE VIEW bronze_poly_clob_trades AS
SELECT
    *, 'poly_clob_trades' AS source_dataset, 'polymarket' AS source_platform,
    'data/polymarket/trades' AS source_relative_path, 'v0_semantic_hardening' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    COALESCE(CAST(transaction_ref AS VARCHAR), 'missing_source_record') AS source_record_ref,
    CASE WHEN transaction_ref IS NULL OR condition_ref IS NULL OR block_ref IS NULL THEN 'missing_required_raw_field' ELSE 'none' END AS bronze_unresolved_status,
    CASE WHEN transaction_ref IS NULL OR condition_ref IS NULL OR block_ref IS NULL THEN 'missing' ELSE 'present' END AS required_field_status
FROM source_poly_clob_trades;

CREATE OR REPLACE VIEW bronze_poly_blocks AS
SELECT
    *, 'poly_blocks' AS source_dataset, 'polymarket' AS source_platform,
    'data/polymarket/blocks' AS source_relative_path, 'v0_semantic_hardening' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    COALESCE(CAST(block_ref AS VARCHAR), 'missing_source_record') AS source_record_ref,
    CASE WHEN block_ref IS NULL THEN 'missing_required_raw_field' ELSE 'none' END AS bronze_unresolved_status,
    CASE WHEN block_ref IS NULL THEN 'missing' ELSE 'present' END AS required_field_status
FROM source_poly_blocks;

CREATE OR REPLACE VIEW bronze_poly_legacy_fpmm_trades AS
SELECT
    *, 'poly_legacy_fpmm_trades' AS source_dataset, 'polymarket' AS source_platform,
    'data/polymarket/legacy_trades' AS source_relative_path, 'v0_semantic_hardening' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    COALESCE(CAST(fpmm_ref AS VARCHAR), 'missing_source_record') AS source_record_ref,
    CASE WHEN fpmm_ref IS NULL OR collateral_asset_ref IS NULL THEN 'missing_required_raw_field' ELSE 'none' END AS bronze_unresolved_status,
    CASE WHEN fpmm_ref IS NULL OR collateral_asset_ref IS NULL THEN 'missing' ELSE 'present' END AS required_field_status
FROM source_poly_legacy_fpmm_trades;

CREATE OR REPLACE VIEW bronze_poly_fpmm_collateral_lookup AS
SELECT
    *, 'poly_fpmm_collateral_lookup' AS source_dataset, 'polymarket' AS source_platform,
    'data/polymarket/fpmm_collateral_lookup.json' AS source_relative_path, 'v0_semantic_hardening' AS bronze_view_version,
    CAST(NULL AS TIMESTAMP) AS raw_ingested_at,
    COALESCE(CAST(collateral_asset_ref AS VARCHAR), 'missing_source_record') AS source_record_ref,
    CASE WHEN collateral_asset_ref IS NULL THEN 'missing_required_raw_field' ELSE 'none' END AS bronze_unresolved_status,
    CASE WHEN collateral_asset_ref IS NULL THEN 'missing' ELSE 'present' END AS required_field_status
FROM source_poly_fpmm_collateral_lookup;
