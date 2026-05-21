# Phase 0B-19 — Tiny Fixture Candidate Selection Plan (Documentation-Only)

## 1) Ticket posture and explicit non-approvals

This ticket is **documentation-only**.

This ticket provides a **fixture candidate selection plan only**.

This ticket explicitly does **not** approve:

- importing any archive data into MEG,
- committing any fixture data,
- deriving fixtures,
- fixture derivation approval,
- import approval,
- loader implementation,
- query-engine implementation,
- live trading,
- autonomous execution.

No fixture files, fixture payloads, data imports, loader code, or runtime behavior changes are included in this ticket.

## 2) Source references and inspection anchors

This plan is scoped to the previously inspected local archive metadata and schema findings.

Primary source references:

- source manifest entry: `local_poly_kalshi_historical_archive_placeholder`,
- origin repository source: `jon_becker_prediction_market_analysis_snapshot`,
- inspection doc: `docs/phase0b/reviews/JON_BECKER_LOCAL_ARCHIVE_REVIEW_PENDING.md`,
- archive path inspected: `/e/meg_source_review/repos/prediction-market-analysis/data`.

Inspection facts carried forward from prior docs:

- compressed archive observed: `data/data.tar.zst`,
- extracted sentinel observed: `data/.download_complete`,
- file counts observed:
  - `total_files: 78732`,
  - `parquet_files: 78723`,
  - `json_files: 1`,
  - `appledouble_metadata_files: 29245`,
- AppleDouble files prefixed with `._` must be ignored.

Available inspected folders and files include:

- `data/kalshi/markets`,
- `data/kalshi/trades`,
- `data/polymarket/blocks`,
- `data/polymarket/markets`,
- `data/polymarket/trades`,
- `data/polymarket/legacy_trades`,
- `data/polymarket/fpmm_collateral_lookup.json`.

## 3) Global fixture-candidate selection rules (future derivation only)

Any future fixture derivation must satisfy all of the following:

1. fixtures must be tiny,
2. fixtures must be deterministic,
3. fixtures must be regenerable,
4. derivation must occur only after separate explicit approval,
5. source path must be recorded,
6. source commit must be recorded,
7. source manifest ID must be recorded,
8. deterministic row-selection/object-selection rule must be recorded,
9. source checksum must be recorded before committing any derived fixture,
10. generated fixture checksum must be recorded after derivation,
11. files prefixed with `._` (AppleDouble) must never be used,
12. full local archive absolute paths must not be embedded in fixture payload content,
13. generated reports must not be committed,
14. `.duckdb` artifacts must not be committed,
15. large data must not be committed,
16. external repo vendoring must not be introduced.

## 4) Candidate fixture groups (planning only; do not create in this ticket)

## Group A — Kalshi markets tiny fixture candidate

- Purpose:
  - market metadata,
  - title/subtitle semantic matching inputs,
  - price/result field coverage.
- Source: `data/kalshi/markets/markets_0_10000.parquet`.
- Suggested tiny row count: `3 to 5` rows.
- Candidate fields:
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
  - `open_interest`
  - `result`
  - `open_time`
  - `close_time`
  - `_fetched_at`
- Future use:
  - Kalshi normalized market mapping,
  - semantic matching against Polymarket question/slug/outcomes,
  - calibration/EV planning.

## Group B — Kalshi trades tiny fixture candidate

- Source: `data/kalshi/trades/trades_0_10000.parquet`.
- Suggested tiny row count: `3 to 5` rows.
- Candidate fields:
  - `trade_id`
  - `ticker`
  - `count`
  - `yes_price`
  - `no_price`
  - `taker_side`
  - `created_time`
  - `_fetched_at`
- Future use:
  - Kalshi normalized fills/trades mapping,
  - price/side analysis,
  - event/ticker joins to Kalshi markets.

## Group C — Polymarket markets tiny fixture candidate

- Source: `data/polymarket/markets/markets_0_10000.parquet`.
- Suggested tiny row count: `3 to 5` rows.
- Candidate fields:
  - `id`
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
  - `_fetched_at`
- Future use:
  - condition/outcome/token mapping,
  - semantic matching against Kalshi title/subtitle fields,
  - cross-platform opportunity planning.

## Group D — Polymarket CLOB trades tiny fixture candidate

- Source: `data/polymarket/trades/trades_0_10000.parquet`.
- Suggested tiny row count: `3 to 5` rows.
- Candidate fields:
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
  - `_fetched_at`
  - `_contract`
- Future use:
  - wallet/lead-lag/whale behavior research,
  - CLOB trade normalization,
  - token/outcome mapping via `clob_token_ids`.

## Group E — Polymarket blocks tiny fixture candidate

- Source: `data/polymarket/blocks/blocks_10000000_10100000.parquet`.
- Suggested tiny row count: `3 to 5` rows.
- Candidate fields:
  - `block_number`
  - `timestamp`
- Future use:
  - block timestamp joins for Polymarket trades,
  - chronological normalization.

## Group F — Polymarket legacy FPMM trades tiny fixture candidate

- Source: `data/polymarket/legacy_trades/trades_0_10000.parquet`.
- Suggested tiny row count: `3 to 5` rows.
- Candidate fields:
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
  - `_fetched_at`
- Future use:
  - separate legacy FPMM normalization path,
  - FPMM address/outcome-token mapping,
  - legacy trade compatibility research.

## Group G — FPMM collateral lookup JSON tiny fixture candidate

- Source: `data/polymarket/fpmm_collateral_lookup.json`.
- Suggested tiny object count: `3 to 5` entries.
- Candidate fields:
  - `fpmm_or_contract_ref`
  - `collateral_token`
  - `collateral_symbol`
  - `collateral_decimals`
- Future use:
  - collateral normalization,
  - FPMM legacy trade reconciliation.

## 5) Deterministic row/object selection rules for future derivation

Future tiny fixture derivation should follow these deterministic rules:

1. use non-AppleDouble files only,
2. use a fixed source file path per fixture group,
3. sort by stable keys where possible,
4. choose rows with non-null key fields,
5. include at least one row with populated time fields where possible,
6. include at least one row with populated price/amount fields where possible,
7. do not select rows based on profitability/outcomes (avoid cherry-picking),
8. record source file checksum before deriving fixtures,
9. record generated fixture checksum after derivation.

## 6) Suggested stable keys by fixture group

- Kalshi markets: `ticker`, `event_ticker`, `_fetched_at`.
- Kalshi trades: `trade_id`, `ticker`, `created_time`.
- Polymarket markets: `condition_id`, `id`, `_fetched_at`.
- Polymarket CLOB trades: `transaction_hash`, `log_index`, `order_hash`.
- Polymarket blocks: `block_number`.
- Polymarket legacy trades: `transaction_hash`, `log_index`, `fpmm_address`.
- FPMM collateral lookup JSON: address/key sorted lexicographically.

## 7) Future approval gates required before any fixture creation

Before deriving any fixture payloads from this archive, all of the following should be explicitly reviewed and approved:

1. source manifest status reviewed,
2. license/provenance status resolved or explicitly approved for fixture derivation,
3. checksum strategy completed,
4. tiny fixture row/object counts approved,
5. privacy/security review completed for public wallet/address fields,
6. no ToS or redistribution conflict,
7. canonical identifier guard reviewed,
8. cross-platform semantic matching fixtures reviewed separately before use in equivalence/arbitrage tests.

## 8) Explicit scope boundaries reiterated

This plan does **not** approve:

- importing any archive data into MEG,
- committing any fixture data,
- deriving fixtures,
- adding loaders,
- adding query engines,
- enabling live trading,
- enabling autonomous execution.

## 9) Strategic cross-platform support summary (planning)

This plan intentionally covers both Kalshi and Polymarket as first-class research targets.

Planned fixture candidates are structured to support future research in:

- Polymarket token/outcome normalization,
- Polymarket wallet/lead-lag/whale behavior,
- Polymarket legacy FPMM normalization,
- Kalshi market/trade mapping,
- Kalshi calibration and EV analysis,
- Kalshi/Polymarket semantic matching and cross-platform opportunity detection research.

Any equivalence or arbitrage interpretation remains out of scope until separate semantic/resolution/fees/liquidity/ToS review gates are passed.

## 10) Recommended next tickets

1. **Phase 0B-20A**: prepare fresh-chat research context pack for Kalshi/Polymarket semantic matching and cross-platform opportunity research.
2. **Phase 0B-20B**: external cited research document for Kalshi/Polymarket matching, fees, rules, resolution criteria, liquidity, and ToS/jurisdiction caveats.
3. **Phase 0B-20C**: docs-only cross-platform semantic matching research plan PR.
4. **Phase 0B-21**: Polymarket token/outcome normalization plan.
5. **Phase 0B-22**: Kalshi normalized fills/markets mapping plan.
6. **Phase 0B-23**: approved tiny fixture derivation script plan, still no fixture commit unless explicitly approved.
