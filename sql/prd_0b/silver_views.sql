-- PRD-0B-IMPL-06 Silver view skeleton.

CREATE OR REPLACE VIEW silver_kalshi_events AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'kalshi' AS source_platform,
    'event' AS normalized_entity_type,
    'none' AS unresolved_status,
    source_dataset,
    source_relative_path,
    event_ticker_ref,
    ticker_ref
FROM bronze_kalshi_markets;

CREATE OR REPLACE VIEW silver_kalshi_markets AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'kalshi' AS source_platform,
    'market' AS normalized_entity_type,
    'none' AS unresolved_status,
    source_dataset,
    source_relative_path,
    ticker_ref,
    source_market_ref
FROM bronze_kalshi_markets;

CREATE OR REPLACE VIEW silver_kalshi_outcomes AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'kalshi' AS source_platform,
    'outcome' AS normalized_entity_type,
    'none' AS unresolved_status,
    source_dataset,
    source_relative_path,
    ticker_ref,
    outcome
FROM bronze_kalshi_markets;

CREATE OR REPLACE VIEW silver_kalshi_market_snapshots AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'kalshi' AS source_platform,
    'market_snapshot' AS normalized_entity_type,
    'none' AS unresolved_status,
    source_dataset,
    source_relative_path,
    ticker_ref,
    snapshot_ref
FROM bronze_kalshi_markets;

CREATE OR REPLACE VIEW silver_kalshi_fills AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'kalshi' AS source_platform,
    'fill' AS normalized_entity_type,
    CASE WHEN t.ticker_ref IS NULL THEN 'unresolved_ticker_ref' ELSE 'none' END AS unresolved_status,
    t.source_dataset,
    t.source_relative_path,
    t.transaction_ref,
    t.ticker_ref
FROM bronze_kalshi_trades t
LEFT JOIN bronze_kalshi_markets m
    ON t.ticker_ref = m.ticker_ref;

CREATE OR REPLACE VIEW silver_kalshi_results AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'kalshi' AS source_platform,
    'result' AS normalized_entity_type,
    'none' AS unresolved_status,
    source_dataset,
    source_relative_path,
    ticker_ref,
    result_ref
FROM bronze_kalshi_markets;

CREATE OR REPLACE VIEW silver_poly_markets AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'polymarket' AS source_platform,
    'market' AS normalized_entity_type,
    'none' AS unresolved_status,
    source_dataset,
    source_relative_path,
    condition_ref,
    source_market_ref
FROM bronze_poly_markets;

CREATE OR REPLACE VIEW silver_poly_outcomes AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'polymarket' AS source_platform,
    'outcome' AS normalized_entity_type,
    'none' AS unresolved_status,
    source_dataset,
    source_relative_path,
    condition_ref,
    outcome
FROM bronze_poly_markets;

CREATE OR REPLACE VIEW silver_poly_clob_tokens AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'polymarket' AS source_platform,
    'clob_token' AS normalized_entity_type,
    CASE WHEN token_ref IS NULL THEN 'unresolved_token_ref' ELSE 'none' END AS unresolved_status,
    source_dataset,
    source_relative_path,
    condition_ref,
    token_ref
FROM bronze_poly_markets;

CREATE OR REPLACE VIEW silver_poly_clob_fills AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'polymarket' AS source_platform,
    'clob_fill' AS normalized_entity_type,
    CASE WHEN b.block_ref IS NULL THEN 'unresolved_block_timestamp' ELSE 'none' END AS unresolved_status,
    t.source_dataset,
    t.source_relative_path,
    t.transaction_ref,
    COALESCE(m.condition_ref, t.condition_ref) AS condition_ref,
    t.block_ref
FROM bronze_poly_clob_trades t
LEFT JOIN bronze_poly_markets m
    ON t.condition_ref = m.condition_ref
LEFT JOIN bronze_poly_blocks b
    ON t.block_ref = b.block_ref;

CREATE OR REPLACE VIEW silver_poly_blocks AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'polymarket' AS source_platform,
    'block' AS normalized_entity_type,
    'none' AS unresolved_status,
    source_dataset,
    source_relative_path,
    block_ref
FROM bronze_poly_blocks;

CREATE OR REPLACE VIEW silver_poly_legacy_fpmm_fills AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'polymarket' AS source_platform,
    'legacy_fpmm_fill' AS normalized_entity_type,
    CASE WHEN c.collateral_asset_ref IS NULL THEN 'unresolved_collateral_ref' ELSE 'none' END AS unresolved_status,
    t.source_dataset,
    t.source_relative_path,
    t.fpmm_ref,
    c.collateral_asset_ref
FROM bronze_poly_legacy_fpmm_trades t
LEFT JOIN bronze_poly_fpmm_collateral_lookup c
    ON t.collateral_asset_ref = c.collateral_asset_ref;

CREATE OR REPLACE VIEW silver_poly_collateral_assets AS
SELECT
    'v0_skeleton' AS silver_view_version,
    'polymarket' AS source_platform,
    'collateral_asset' AS normalized_entity_type,
    'none' AS unresolved_status,
    source_dataset,
    source_relative_path,
    collateral_asset_ref
FROM bronze_poly_fpmm_collateral_lookup;
