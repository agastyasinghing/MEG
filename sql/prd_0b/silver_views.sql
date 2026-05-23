-- PRD-0B-IMPL-07 Silver semantic-hardening view contract.

CREATE OR REPLACE VIEW silver_kalshi_events AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'kalshi' AS source_platform,
    'event' AS normalized_entity_type,
    source_dataset,
    source_relative_path,
    source_record_ref,
    bronze_unresolved_status AS unresolved_status,
    'not_required' AS dependency_status,
    event_ticker_ref,
    ticker_ref
FROM bronze_kalshi_markets;

CREATE OR REPLACE VIEW silver_kalshi_markets AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'kalshi' AS source_platform,
    'market' AS normalized_entity_type,
    source_dataset,
    source_relative_path,
    source_record_ref,
    bronze_unresolved_status AS unresolved_status,
    'not_required' AS dependency_status,
    ticker_ref,
    source_market_ref
FROM bronze_kalshi_markets;

CREATE OR REPLACE VIEW silver_kalshi_outcomes AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'kalshi' AS source_platform,
    'outcome' AS normalized_entity_type,
    source_dataset,
    source_relative_path,
    source_record_ref,
    bronze_unresolved_status AS unresolved_status,
    'not_required' AS dependency_status,
    ticker_ref,
    outcome
FROM bronze_kalshi_markets;

CREATE OR REPLACE VIEW silver_kalshi_market_snapshots AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'kalshi' AS source_platform,
    'market_snapshot' AS normalized_entity_type,
    source_dataset,
    source_relative_path,
    source_record_ref,
    bronze_unresolved_status AS unresolved_status,
    'not_required' AS dependency_status,
    ticker_ref,
    snapshot_ref
FROM bronze_kalshi_markets;

CREATE OR REPLACE VIEW silver_kalshi_fills AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'kalshi' AS source_platform,
    'fill' AS normalized_entity_type,
    t.source_dataset,
    t.source_relative_path,
    t.source_record_ref,
    CASE
        WHEN t.bronze_unresolved_status <> 'none' THEN t.bronze_unresolved_status
        WHEN m.ticker_ref IS NULL THEN 'missing_dependency'
        ELSE 'none'
    END AS unresolved_status,
    CASE
        WHEN m.ticker_ref IS NULL THEN 'missing_dependency'
        ELSE 'matched_dependency'
    END AS dependency_status,
    t.transaction_ref,
    t.ticker_ref
FROM bronze_kalshi_trades t
LEFT JOIN bronze_kalshi_markets m
    ON t.ticker_ref = m.ticker_ref;

CREATE OR REPLACE VIEW silver_kalshi_results AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'kalshi' AS source_platform,
    'result' AS normalized_entity_type,
    source_dataset,
    source_relative_path,
    source_record_ref,
    bronze_unresolved_status AS unresolved_status,
    'not_required' AS dependency_status,
    ticker_ref,
    result_ref
FROM bronze_kalshi_markets;

CREATE OR REPLACE VIEW silver_poly_markets AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'polymarket' AS source_platform,
    'market' AS normalized_entity_type,
    source_dataset,
    source_relative_path,
    source_record_ref,
    bronze_unresolved_status AS unresolved_status,
    'not_required' AS dependency_status,
    condition_ref,
    source_market_ref
FROM bronze_poly_markets;

CREATE OR REPLACE VIEW silver_poly_outcomes AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'polymarket' AS source_platform,
    'outcome' AS normalized_entity_type,
    source_dataset,
    source_relative_path,
    source_record_ref,
    bronze_unresolved_status AS unresolved_status,
    'not_required' AS dependency_status,
    condition_ref,
    outcome
FROM bronze_poly_markets;

CREATE OR REPLACE VIEW silver_poly_clob_tokens AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'polymarket' AS source_platform,
    'clob_token' AS normalized_entity_type,
    source_dataset,
    source_relative_path,
    source_record_ref,
    CASE
        WHEN bronze_unresolved_status <> 'none' THEN bronze_unresolved_status
        WHEN token_ref IS NULL THEN 'missing_required_raw_field'
        ELSE 'none'
    END AS unresolved_status,
    'not_required' AS dependency_status,
    condition_ref,
    token_ref
FROM bronze_poly_markets;

CREATE OR REPLACE VIEW silver_poly_clob_fills AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'polymarket' AS source_platform,
    'clob_fill' AS normalized_entity_type,
    t.source_dataset,
    t.source_relative_path,
    t.source_record_ref,
    CASE
        WHEN t.bronze_unresolved_status <> 'none' THEN t.bronze_unresolved_status
        WHEN m.condition_ref IS NULL AND b.block_ref IS NULL THEN 'missing_market_and_block_dependency'
        WHEN m.condition_ref IS NULL THEN 'missing_market_dependency'
        WHEN b.block_ref IS NULL THEN 'missing_block_dependency'
        ELSE 'none'
    END AS unresolved_status,
    CASE
        WHEN m.condition_ref IS NULL OR b.block_ref IS NULL THEN 'missing_dependency'
        ELSE 'matched_dependency'
    END AS dependency_status,
    CASE
        WHEN m.condition_ref IS NULL THEN 'missing_dependency'
        ELSE 'matched_dependency'
    END AS market_dependency_status,
    CASE
        WHEN b.block_ref IS NULL THEN 'missing_dependency'
        ELSE 'matched_dependency'
    END AS block_dependency_status,
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
    'v0_semantic_hardening' AS silver_view_version,
    'polymarket' AS source_platform,
    'block' AS normalized_entity_type,
    source_dataset,
    source_relative_path,
    source_record_ref,
    bronze_unresolved_status AS unresolved_status,
    'not_required' AS dependency_status,
    block_ref
FROM bronze_poly_blocks;

CREATE OR REPLACE VIEW silver_poly_legacy_fpmm_fills AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'polymarket' AS source_platform,
    'legacy_fpmm_fill' AS normalized_entity_type,
    t.source_dataset,
    t.source_relative_path,
    t.source_record_ref,
    CASE
        WHEN t.bronze_unresolved_status <> 'none' THEN t.bronze_unresolved_status
        WHEN c.collateral_asset_ref IS NULL THEN 'missing_collateral_dependency'
        ELSE 'none'
    END AS unresolved_status,
    CASE
        WHEN c.collateral_asset_ref IS NULL THEN 'missing_dependency'
        ELSE 'matched_dependency'
    END AS dependency_status,
    t.fpmm_ref,
    c.collateral_asset_ref
FROM bronze_poly_legacy_fpmm_trades t
LEFT JOIN bronze_poly_fpmm_collateral_lookup c
    ON t.collateral_asset_ref = c.collateral_asset_ref;

CREATE OR REPLACE VIEW silver_poly_collateral_assets AS
SELECT
    'v0_semantic_hardening' AS silver_view_version,
    'polymarket' AS source_platform,
    'collateral_asset' AS normalized_entity_type,
    source_dataset,
    source_relative_path,
    source_record_ref,
    bronze_unresolved_status AS unresolved_status,
    'not_required' AS dependency_status,
    collateral_asset_ref
FROM bronze_poly_fpmm_collateral_lookup;
