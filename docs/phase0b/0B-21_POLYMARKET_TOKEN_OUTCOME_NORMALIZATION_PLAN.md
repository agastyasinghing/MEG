# Phase 0B-21 — Polymarket Token/Outcome Normalization Plan (Docs-Only)

## 1) Purpose and posture

This ticket is **documentation-only**.

This document defines a **Polymarket normalization design plan** for future MEG historical-research normalization work.

This document does **not** implement normalization logic and does **not** approve:

- data import,
- fixture derivation,
- fixture commits,
- loader implementation,
- query-engine implementation,
- connector use/implementation,
- order routing,
- order placement,
- live trading,
- autonomous execution.

All normalized entities named in this document are **planning targets only**, not implemented artifacts.

## 2) Source and schema anchors

Planning anchors for this design:

- source manifest entry: `local_poly_kalshi_historical_archive_placeholder`
- origin source: `jon_becker_prediction_market_analysis_snapshot`
- inspection doc: `docs/phase0b/reviews/JON_BECKER_LOCAL_ARCHIVE_REVIEW_PENDING.md`
- related cross-platform doc: `docs/phase0b/0B-20C_CROSS_PLATFORM_SEMANTIC_MATCHING_RESEARCH_PLAN.md`

Local archive folders/files in scope:

- `data/polymarket/blocks`
- `data/polymarket/markets`
- `data/polymarket/trades`
- `data/polymarket/legacy_trades`
- `data/polymarket/fpmm_collateral_lookup.json`

File handling rule:

- AppleDouble metadata files prefixed with `._` must be ignored.

## 3) Core normalization problem

Polymarket market metadata, token references, and CLOB trade records are not automatically usable as one flat, analysis-safe dataset.

Core mismatch:

- CLOB trades expose `maker_asset_id` and `taker_asset_id`.
- Market metadata exposes `clob_token_ids` and `outcomes` (plus `outcome_prices`).

MEG needs a deterministic mapping from trade asset references to normalized token/outcome entities.

Canonical anchor expectations:

- `condition_id` should anchor market-level identity.
- `clob_token_ids` should anchor tradable token/outcome identity where available.
- `outcomes` and `outcome_prices` require careful parse-and-alignment behavior.

Legacy FPMM path difference:

- Legacy records use `fpmm_address`, `outcome_index`, `outcome_tokens`, and `is_buy`.
- Legacy FPMM normalization must follow a separate branch from CLOB normalization.

## 4) Proposed Bronze/Silver/Gold model (planning-only)

The following are planned entities only, not implemented tables.

### Bronze (raw landing targets)

- `bronze_poly_markets_raw`
- `bronze_poly_clob_trades_raw`
- `bronze_poly_blocks_raw`
- `bronze_poly_legacy_fpmm_trades_raw`
- `bronze_poly_fpmm_collateral_lookup_raw`

### Silver (normalized targets)

- `silver_poly_markets`
- `silver_poly_outcomes`
- `silver_poly_clob_tokens`
- `silver_poly_clob_fills`
- `silver_poly_blocks`
- `silver_poly_legacy_fpmm_markets`
- `silver_poly_legacy_fpmm_fills`
- `silver_poly_collateral_assets`

### Gold (analysis-ready targets)

- `gold_poly_wallet_activity`
- `gold_poly_market_flow`
- `gold_poly_token_outcome_flow`
- `gold_poly_whale_lead_lag_candidates`
- `gold_poly_cross_platform_matching_inputs`

## 5) Proposed normalized entities and fields (planning-only)

### A) `poly_market`

Suggested fields:

- `source_platform`
- `source_market_ref`
- `condition_id`
- `question`
- `slug`
- `outcomes_raw`
- `outcome_prices_raw`
- `clob_token_ids_raw`
- `volume`
- `liquidity`
- `active`
- `closed`
- `end_date`
- `created_at`
- `market_maker_address`
- `fetched_at`
- `source_record_hash`
- `parser_version`

### B) `poly_outcome`

Suggested fields:

- `source_platform`
- `condition_id`
- `source_market_ref`
- `outcome_index`
- `outcome_label`
- `outcome_price_raw`
- `clob_token_ref`
- `is_yes_no_binary`
- `is_parsed_from_clob_token_ids`
- `source_record_hash`
- `parser_version`

### C) `poly_clob_token`

Suggested fields:

- `source_platform`
- `condition_id`
- `source_market_ref`
- `clob_token_ref`
- `outcome_index`
- `outcome_label`
- `token_side`
- `token_parse_status`
- `source_record_hash`
- `parser_version`

### D) `poly_clob_fill`

Suggested fields:

- `source_platform`
- `block_number`
- `block_timestamp`
- `transaction_hash`
- `log_index`
- `order_hash`
- `maker_ref`
- `taker_ref`
- `maker_asset_ref`
- `taker_asset_ref`
- `maker_amount_raw`
- `taker_amount_raw`
- `fee_raw`
- `trade_timestamp`
- `fetched_at`
- `contract_ref`
- `maker_token_outcome_ref`
- `taker_token_outcome_ref`
- `token_mapping_status`
- `source_record_hash`
- `parser_version`

### E) `poly_block`

Suggested fields:

- `source_platform`
- `block_number`
- `block_timestamp`
- `source_record_hash`
- `parser_version`

### F) `poly_legacy_fpmm_fill`

Suggested fields:

- `source_platform`
- `block_number`
- `block_timestamp`
- `transaction_hash`
- `log_index`
- `fpmm_ref`
- `trader_ref`
- `amount_raw`
- `fee_amount_raw`
- `outcome_index`
- `outcome_tokens_raw`
- `is_buy`
- `trade_timestamp`
- `fetched_at`
- `collateral_token_ref`
- `collateral_symbol`
- `collateral_decimals`
- `legacy_mapping_status`
- `source_record_hash`
- `parser_version`

### G) `poly_collateral_asset`

Suggested fields:

- `source_platform`
- `fpmm_or_contract_ref`
- `collateral_token_ref`
- `collateral_symbol`
- `collateral_decimals`
- `source_record_hash`
- `parser_version`

## 6) CLOB token/outcome mapping strategy (deterministic plan)

Planned deterministic strategy:

1. Parse `outcomes` and `clob_token_ids` from market metadata.
2. Preserve raw source values before parsing.
3. Validate compatible lengths between parsed outcomes and parsed token IDs.
4. Assign `outcome_index` deterministically by array order only after validation.
5. Map each `clob_token_ref` to `condition_id`, `source_market_ref`, `outcome_index`, and `outcome_label`.
6. For each CLOB trade, map `maker_asset_ref` and `taker_asset_ref` to known `clob_token_ref` values.
7. If both sides map, populate `maker_token_outcome_ref` and `taker_token_outcome_ref`.
8. If one or both sides fail to map, preserve the raw fill row and mark `token_mapping_status=unresolved`.
9. Never auto-drop unresolved mapping rows; preserve for audit/reconciliation.
10. Do not infer outcome from price alone.
11. Do not infer outcome from wallet address alone.
12. Do not infer outcome from title/slug alone.

## 7) CLOB fill direction and wallet semantics

Planned interpretation constraints:

- `maker_ref` and `taker_ref` are wallet-like actors.
- `maker_asset_ref` and `taker_asset_ref` represent exchanged assets, not direct YES/NO semantics until mapped.
- `maker_amount_raw` and `taker_amount_raw` require explicit decimal/scale handling before economic interpretation.
- `fee_raw` requires explicit scale/asset interpretation.
- Directional interpretation must be derived only after token mapping is known.
- Wallet/lead-lag analysis should rely on mapped token/outcome flows, not raw asset IDs alone.
- Whale behavior classification should not be performed on unresolved token mappings.

## 8) Block timestamp normalization

Planned timestamp normalization:

- CLOB trades include `block_number` and `timestamp`.
- Blocks records include `block_number` and `timestamp`.
- Future normalization should use `block_number` joins to attach canonical `block_timestamp` where available.
- If trade timestamp and block timestamp disagree, preserve both and flag `timestamp_reconciliation_status`.
- Source timestamps must not be silently overwritten.
- Timestamp normalization must record source timezone/format assumptions.

## 9) Legacy FPMM separate path

Legacy-path planning requirements:

- Legacy FPMM records must not be forced into the CLOB model.
- Legacy fields include `fpmm_address`, `trader`, `outcome_index`, `outcome_tokens`, `is_buy`, `amount`, and `fee_amount`.
- Future normalization should first produce dedicated legacy FPMM entities.
- `fpmm_collateral_lookup.json` can enrich FPMM/contract refs with collateral metadata.
- CLOB and legacy FPMM paths may be reconciled only later, after separate mapping/reconciliation design.
- Legacy unresolved mapping states must be preserved.

## 10) Validation and unresolved-state taxonomy

Planned validation statuses:

- `parsed`
- `unresolved_token_ref`
- `unresolved_condition_ref`
- `malformed_outcomes`
- `malformed_clob_token_ids`
- `outcome_token_length_mismatch`
- `duplicate_token_ref`
- `missing_condition_id`
- `missing_trade_asset_ref`
- `missing_block_timestamp`
- `timestamp_mismatch`
- `legacy_unresolved_fpmm_ref`
- `legacy_unresolved_collateral_ref`
- `unsupported_market_shape`

## 11) Cross-platform matching implications

Polymarket normalized outputs needed by Phase 0B-20C include:

- `condition_id`
- `source_market_ref`
- `question`
- `slug`
- outcome labels
- `clob_token_refs`
- active/closed status flags
- `end_date`
- `liquidity`
- `volume`
- rule/resolution metadata where available

Implications:

- CLOB fill normalization is a prerequisite for reliable wallet/lead-lag and whale-flow research.
- Token/outcome normalization supports cross-platform semantic matching by providing stable Polymarket outcome candidates for comparison with Kalshi titles/subtitles/tickers.
- Unresolved Polymarket mappings should block cross-platform opportunity claims.
- Cross-platform opportunity labels remain research-only and human-reviewed.

## 12) Future fixture implications

Future tiny fixtures should include:

- 3 to 5 Polymarket market rows with parseable `outcomes`/`clob_token_ids`
- 3 to 5 CLOB trade rows where `maker_asset_id`/`taker_asset_id` map to known `clob_token_ids` if possible
- 3 to 5 block rows for timestamp joins
- 3 to 5 legacy FPMM trade rows
- 3 to 5 FPMM collateral lookup JSON entries

Boundary:

- This document does not approve deriving or committing those fixtures.
- Fixture derivation remains dependent on Phase 0B-23 or later explicit approval.

## 13) Future tests/preflight implications

Static/preflight test candidates:

- schema field-presence tests for planned normalized entities
- token/outcome mapping fixture-shape tests
- unresolved-state taxonomy tests
- CLOB fill direction guard tests
- block timestamp reconciliation shape tests
- legacy FPMM separate-path tests
- no-auto-drop unresolved rows tests
- no cross-platform opportunity claims when token mapping is unresolved

## 14) Recommended next tickets

- **Phase 0B-22**: Kalshi normalized fills/markets mapping plan.
- **Phase 0B-23**: approved tiny fixture derivation script plan, still no fixture commit unless explicitly approved.
- **Phase 0B-24**: cross-platform candidate-pair schema fixture tests (static/preflight only).
- **Phase 0B-25**: semantic matching rejection-reason taxonomy tests (static/preflight only).
- **Phase 0B-26**: integration/rate-limit/fee source appendix maintenance plan.
- **Phase 1 candidate**: approved local fixture generation and Bronze schema implementation, only after Phase 0B closes.

## 15) Explicit non-approvals

This document explicitly does **not** approve:

- data import,
- fixture derivation,
- fixture commit,
- loader implementation,
- query engine implementation,
- connector implementation,
- order placement,
- live trading,
- autonomous execution.

## 16) Static canonical-ID guard

Canonical identifier guard for this document:

- avoid literal legacy market identifier term usage,
- use `source_market_ref`, native market reference, source market identifier, or legacy market identifier wording instead,
- if literal legacy market identifier term becomes unavoidable in a future revision, update `tests/core/canonical_id_allowlist.py` narrowly and explicitly,
- do not casually increase legacy identifier footprint.
