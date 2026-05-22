# PRD-0B-IMPL-04 Bronze/Silver View Implementation Plan (Static Preflight Contract)

## 1) Purpose and posture
- This document is **PRD-0B-IMPL-04 Bronze/Silver view implementation plan**.
- This ticket is **docs/static-preflight only**.
- This ticket does **not implement DuckDB views**.
- This ticket does **not run DuckDB**.
- This ticket does **not read archive payloads**.
- This ticket does **not create SQL files, .duckdb files, generated reports, fixtures, loaders, query engines, connectors, API calls, order routing, live trading, autonomy, or weather implementation**.
- This document is a contract for a future implementation ticket.

## 2) PRD Phase 0B alignment
The master PRD requires Phase 0B research lake setup with DuckDB + Parquet + Becker posture, Bronze/Silver normalization views, data dictionary, seven sanity queries, and query latency gate. PRD-0B-IMPL-01 covered local research-lake smoke. PRD-0B-IMPL-02 covered the seven sanity-query harness. PRD-0B-IMPL-03 covered the data dictionary static contract. This ticket covers the Bronze/Silver view implementation plan only, not implementation.

## 3) Implementation prerequisites
Before actual view implementation:
- PRD-0B-IMPL-01 merged and green.
- PRD-0B-IMPL-02 merged and green.
- PRD-0B-IMPL-03 merged and green.
- DuckDB dependency posture approved or optional local DuckDB execution gate defined.
- Approved local archive root or approved committed tiny fixtures.
- Data dictionary generated or reviewed enough for view implementation.
- No absolute local archive paths embedded in committed artifacts.
- No generated data outputs committed without approval.
- No full archive import.
- No production loader dependency.

## 4) Bronze view principles
Bronze views must:
- Preserve raw source fields.
- Add source/provenance metadata.
- Add parser/schema version metadata where applicable.
- Not perform Silver normalization.
- Not infer outcomes from title/price/wallet alone.
- Preserve unresolved/malformed rows instead of dropping them.
- Expose `source_relative_path`, `source_record_hash`, and `source_file_checksum` when available.
- Not imply execution readiness.

## 5) Silver view principles
Silver views must:
- Normalize platform-specific identifiers into stable references.
- Parse and validate outcome/token/ticker/event relationships.
- Retain unresolved-state flags.
- Preserve raw field references where practical.
- Separate Polymarket CLOB and legacy FPMM paths.
- Separate Kalshi market/event/outcome/fill/result/snapshot paths.
- Not create cross-platform equivalence claims.
- Not create opportunity labels.
- Not imply trading/execution readiness.

## 6) Planned Bronze views (exactly seven)
| planned_bronze_view | source_dataset | source_path | related_dictionary_dataset | related_bronze_contract | planned_raw_field_family |
|---|---|---|---|---|---|
| bronze_kalshi_markets | kalshi_markets | data/kalshi/markets | kalshi_markets | bronze_kalshi_market | Kalshi market metadata/snapshot fields |
| bronze_kalshi_trades | kalshi_trades | data/kalshi/trades | kalshi_trades | bronze_kalshi_trade | Kalshi trade/fill fields |
| bronze_poly_markets | poly_markets | data/polymarket/markets | poly_markets | bronze_poly_market | Polymarket market/outcome/token metadata |
| bronze_poly_clob_trades | poly_clob_trades | data/polymarket/trades | poly_clob_trades | bronze_poly_clob_trade | Polymarket CLOB trade/fill fields |
| bronze_poly_blocks | poly_blocks | data/polymarket/blocks | poly_blocks | bronze_poly_block | Polygon/Polymarket block timestamp fields |
| bronze_poly_legacy_fpmm_trades | poly_legacy_fpmm_trades | data/polymarket/legacy_trades | poly_legacy_fpmm_trades | bronze_poly_legacy_fpmm_trade | Polymarket legacy FPMM trade fields |
| bronze_poly_fpmm_collateral_lookup | poly_fpmm_collateral_lookup | data/polymarket/fpmm_collateral_lookup.json | poly_fpmm_collateral_lookup | bronze_poly_fpmm_collateral_lookup | FPMM collateral metadata |

## 7) Planned Silver views
Planned names only; no views are created in this ticket.

### Kalshi Silver
- silver_kalshi_events
- silver_kalshi_markets
- silver_kalshi_outcomes
- silver_kalshi_market_snapshots
- silver_kalshi_fills
- silver_kalshi_results

### Polymarket Silver
- silver_poly_markets
- silver_poly_outcomes
- silver_poly_clob_tokens
- silver_poly_clob_fills
- silver_poly_blocks
- silver_poly_legacy_fpmm_fills
- silver_poly_collateral_assets

## 8) Bronze-to-Silver dependency map
| silver_view | depends_on_bronze_views | normalization_plan_ref | primary_join_or_mapping_logic | unresolved_state_policy |
|---|---|---|---|---|
| silver_kalshi_events | bronze_kalshi_markets | docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md | Group by event_ticker/ticker_ref from market metadata to event-level references. | Preserve unresolved_event_ref as flagged rows; no drop policy. |
| silver_kalshi_markets | bronze_kalshi_markets | docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md | Normalize source market identifier and ticker_ref mapping from raw market records. | Preserve missing_required_raw_field and malformed_raw_value rows. |
| silver_kalshi_outcomes | bronze_kalshi_markets | docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md | Parse yes/no outcome references from raw Kalshi market payload fields. | Preserve unresolved_result/unresolved_ticker_ref rows. |
| silver_kalshi_market_snapshots | bronze_kalshi_markets | docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md | Derive snapshot timeline rows from market metadata + temporal fields. | Preserve unresolved_block_timestamp/timestamp_mismatch flags. |
| silver_kalshi_fills | bronze_kalshi_trades, bronze_kalshi_markets | docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md | Join trade ticker_ref to market ticker_ref for normalized fill references. | Preserve unresolved_taker_side and unresolved_ticker_ref rows. |
| silver_kalshi_results | bronze_kalshi_markets | docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md | Normalize result fields from market-level outcome/result metadata. | Preserve unresolved_result rows. |
| silver_poly_markets | bronze_poly_markets | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md | Normalize source market identifier and condition_id relationship. | Preserve unresolved_condition_ref/missing_required_raw_field rows. |
| silver_poly_outcomes | bronze_poly_markets | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md | Parse outcomes arrays aligned to outcome_prices and condition_id. | Preserve unresolved_token_outcome_mapping rows. |
| silver_poly_clob_tokens | bronze_poly_markets | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md | Normalize clob_token_ids to condition_id + outcome references. | Preserve unresolved_token_ref/unresolved_token_outcome_mapping rows. |
| silver_poly_clob_fills | bronze_poly_clob_trades, bronze_poly_markets, bronze_poly_blocks | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md | Map maker_asset_id/taker_asset_id via token reference joins and block timestamp linkage. | Preserve unresolved_token_ref/unresolved_block_timestamp rows. |
| silver_poly_blocks | bronze_poly_blocks | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md | Normalize block_number and timestamp reference shape. | Preserve malformed_raw_value/timestamp_mismatch rows. |
| silver_poly_legacy_fpmm_fills | bronze_poly_legacy_fpmm_trades, bronze_poly_fpmm_collateral_lookup | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md | Map legacy trade collateral + outcome references using lookup sidecar. | Preserve unresolved_legacy_fpmm_ref/unresolved_collateral_ref rows. |
| silver_poly_collateral_assets | bronze_poly_fpmm_collateral_lookup | docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md | Normalize collateral assets from sidecar lookup records. | Preserve unsupported_source_shape/unresolved_collateral_ref rows. |

## 9) Unresolved-state taxonomy
- none
- missing_source_record
- missing_required_raw_field
- malformed_raw_value
- unresolved_ticker_ref
- unresolved_event_ref
- unresolved_result
- unresolved_taker_side
- unresolved_condition_ref
- unresolved_token_ref
- unresolved_token_outcome_mapping
- unresolved_block_timestamp
- timestamp_mismatch
- unresolved_legacy_fpmm_ref
- unresolved_collateral_ref
- unsupported_source_shape

## 10) Planned implementation files (future only)
Future implementation may add:
- `sql/prd_0b/bronze_views.sql`
- `sql/prd_0b/silver_views.sql`
- `scripts/prd_0b/run_view_smoke.py`
- `tests/core/test_prd_0b_bronze_silver_views.py`

This ticket must not create these files.

## 11) View implementation safety rules
Future implementation must:
- Use read-only local archive inputs or approved tiny fixtures.
- Use in-memory DuckDB or explicitly approved output database path.
- Avoid committing .duckdb files.
- Avoid committing generated query outputs/reports.
- Fail closed on missing expected datasets.
- Preserve unresolved rows.
- Not infer outcomes from title/price/wallet alone.
- Not produce cross-platform opportunity labels.
- Not connect to APIs.
- Not invoke trading connectors.
- Not rely on 0A runtime rails.
- Record dependency on data dictionary version.

## 12) Query latency gate planning
- Master PRD requires query latency gate.
- This ticket does not implement latency testing.
- Future view smoke should record local query timing for bounded sanity queries.
- No performance claims are made in this ticket.
- Query latency gate must be separate from correctness gate.

## 13) Relationship to PRD-0A
- Bronze/Silver view planning does not satisfy Phase 0A shared rail.
- Runtime proposals, paper execution, Telegram queue, Postgres journal, Redis rails, heartbeat, and risk envelopes still require PRD-0A-AUDIT-01 and follow-up repair tickets.
- Weather paper engine remains blocked until 0A/0B readiness is resolved.

## 14) Recommended next tickets
- PRD-0B-IMPL-05 data dictionary local generator, only after explicit approval and dependency posture decision.
- PRD-0B-IMPL-06 Bronze/Silver DuckDB view skeleton, only after dependency posture and source gating.
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel.
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved.

## 15) Explicit non-approvals
- No DuckDB view implementation.
- No DuckDB execution.
- No archive reads.
- No SQL file generation.
- No generated outputs.
- No .duckdb files.
- No fixture derivation.
- No fixture commit.
- No data import.
- No loader implementation.
- No query engine service.
- No connector implementation.
- No API calls.
- No order placement.
- No live trading.
- No autonomous execution.
- No weather implementation.
