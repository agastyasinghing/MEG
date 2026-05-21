# Phase 0B-17 — Jon-Becker Local Archive Metadata Inspection (Documentation-Only)

## 1) Inspection status and decision posture

This ticket records **completed local metadata/schema inspection findings** for the Jon-Becker source repo and its local extracted archive.

Status for this ticket:

- local archive inspection: **completed**,
- import decision: **hold**,
- fixture derivation decision: **pending / no approval**,
- license/provenance decision for dataset/archive: **pending**,
- data imported into MEG: **none**,
- data committed to MEG: **none**.

Boundary posture remains documentation-only:

- no loader implementation,
- no runtime or execution-path changes,
- no live-trading or connector-use approval,
- no autonomous execution authority.

## 2) Source metadata and archive metadata

| Field | Finding |
|---|---|
| Source repository URL | `https://github.com/Jon-Becker/prediction-market-analysis` |
| Source repository remote | `https://github.com/Jon-Becker/prediction-market-analysis.git` |
| Commit inspected | `f3ab641264d9acbedb72b5db9040bc9d078d5ff0` |
| Local repo path inspected | `/e/meg_source_review/repos/prediction-market-analysis` |
| Archive path inspected | `/e/meg_source_review/repos/prediction-market-analysis/data` |
| Compressed archive presence | `data/data.tar.zst` present |
| Compressed archive size observed | `34G` |
| Extracted sentinel | `data/.download_complete` present |
| Disk free after extraction | `about 699G on E:` |

### 2.1 File-format and count summary (completed scan)

| Metric | Value |
|---|---:|
| Total files | 78732 |
| Parquet files | 78723 |
| CSV files | 0 |
| JSON files | 1 |
| JSONL files | 0 |

### 2.2 Top-level extracted layout

- `data/kalshi/markets`
- `data/kalshi/trades`
- `data/polymarket/blocks`
- `data/polymarket/legacy_trades`
- `data/polymarket/markets`
- `data/polymarket/trades`

### 2.3 Non-AppleDouble file counts by folder

| Folder | Non-AppleDouble file count |
|---|---:|
| `kalshi/markets` | 769 |
| `kalshi/trades` | 7214 |
| `polymarket/blocks` | 785 |
| `polymarket/markets` | 41 |
| `polymarket/trades` | 40454 |
| `polymarket/legacy_trades` | 221 |

### 2.4 AppleDouble artifact findings

- AppleDouble metadata files observed: **29245**.
- Files starting with `._` are extraction/metadata artifacts and should be ignored for inspection/import logic.
- These AppleDouble files are not usable Parquet research payloads.

## 3) Platform coverage confirmation

The inspected archive indicates both platforms are materially represented:

- Kalshi coverage present:
  - markets (`data/kalshi/markets`),
  - trades (`data/kalshi/trades`).
- Polymarket coverage present:
  - blocks (`data/polymarket/blocks`),
  - markets (`data/polymarket/markets`),
  - trades (`data/polymarket/trades`),
  - legacy trades (`data/polymarket/legacy_trades`).
- Additional Polymarket metadata file present:
  - `data/polymarket/fpmm_collateral_lookup.json`.

## 4) Representative non-AppleDouble sample files and row counts

| Sample key | Sample file | Representative rows |
|---|---|---:|
| `kalshi_markets` | `data/kalshi/markets/markets_0_10000.parquet` | 10000 |
| `kalshi_trades` | `data/kalshi/trades/trades_0_10000.parquet` | 10000 |
| `polymarket_blocks` | `data/polymarket/blocks/blocks_10000000_10100000.parquet` | 100000 |
| `polymarket_markets` | `data/polymarket/markets/markets_0_10000.parquet` | 10000 |
| `polymarket_trades` | `data/polymarket/trades/trades_0_10000.parquet` | 10000 |
| `polymarket_legacy_trades` | `data/polymarket/legacy_trades/trades_0_10000.parquet` | 10000 |

## 5) Schema findings

## 5.1 Kalshi markets schema

- `ticker VARCHAR`
- `event_ticker VARCHAR`
- `market_type VARCHAR`
- `title VARCHAR`
- `yes_sub_title VARCHAR`
- `no_sub_title VARCHAR`
- `status VARCHAR`
- `yes_bid BIGINT`
- `yes_ask BIGINT`
- `no_bid BIGINT`
- `no_ask BIGINT`
- `last_price BIGINT`
- `volume BIGINT`
- `volume_24h BIGINT`
- `open_interest BIGINT`
- `result VARCHAR`
- `created_time TIMESTAMP WITH TIME ZONE`
- `open_time TIMESTAMP WITH TIME ZONE`
- `close_time TIMESTAMP WITH TIME ZONE`
- `_fetched_at TIMESTAMP_NS`

## 5.2 Kalshi trades schema

- `trade_id VARCHAR`
- `ticker VARCHAR`
- `count BIGINT`
- `yes_price BIGINT`
- `no_price BIGINT`
- `taker_side VARCHAR`
- `created_time TIMESTAMP WITH TIME ZONE`
- `_fetched_at TIMESTAMP_NS`

## 5.3 Polymarket blocks schema

- `block_number BIGINT`
- `timestamp VARCHAR`

## 5.4 Polymarket markets schema

- `id VARCHAR`
- `condition_id VARCHAR`
- `question VARCHAR`
- `slug VARCHAR`
- `outcomes VARCHAR`
- `outcome_prices VARCHAR`
- `clob_token_ids VARCHAR`
- `volume DOUBLE`
- `liquidity DOUBLE`
- `active BOOLEAN`
- `closed BOOLEAN`
- `end_date TIMESTAMP WITH TIME ZONE`
- `created_at TIMESTAMP WITH TIME ZONE`
- `market_maker_address VARCHAR`
- `_fetched_at TIMESTAMP_NS`

## 5.5 Polymarket trades schema

- `block_number BIGINT`
- `transaction_hash VARCHAR`
- `log_index BIGINT`
- `order_hash VARCHAR`
- `maker VARCHAR`
- `taker VARCHAR`
- `maker_asset_id VARCHAR`
- `taker_asset_id VARCHAR`
- `maker_amount BIGINT`
- `taker_amount BIGINT`
- `fee BIGINT`
- `timestamp INTEGER`
- `_fetched_at TIMESTAMP_NS`
- `_contract VARCHAR`

## 5.6 Polymarket legacy trades schema

- `block_number BIGINT`
- `transaction_hash VARCHAR`
- `log_index BIGINT`
- `fpmm_address VARCHAR`
- `trader VARCHAR`
- `amount VARCHAR`
- `fee_amount VARCHAR`
- `outcome_index BIGINT`
- `outcome_tokens VARCHAR`
- `is_buy BOOLEAN`
- `timestamp INTEGER`
- `_fetched_at TIMESTAMP_NS`

## 5.7 FPMM collateral lookup JSON shape

File:

- `data/polymarket/fpmm_collateral_lookup.json`

Observed shape:

- object mapping FPMM/contract-like addresses to collateral metadata.

Observed fields:

- `collateral_token`
- `collateral_symbol`
- `collateral_decimals`

Observed symbol examples:

- `USDC`
- `GNT`
- `USDT0`

## 6) Research implications (planning-only)

## 6.1 Kalshi implications

- Kalshi should be treated as a first-class research target alongside Polymarket.
- Kalshi market/trade calibration and EV-style analysis appears feasible using:
  - `ticker` joins between trades and markets,
  - price fields (`yes_price`, `no_price`, `last_price`),
  - outcome/result context (`result`),
  - taker-side style behavior context through `taker_side`.
- Kalshi `title`, `yes_sub_title`, `no_sub_title`, `ticker`, and `event_ticker` are useful for future semantic matching.
- These fields can help map Kalshi markets to comparable Polymarket questions/slugs/outcomes for cross-platform opportunity research.
- This matching must remain conservative and reviewable.

## 6.2 Polymarket implications

- Polymarket should also be treated as a first-class research target.
- Lead-lag, wallet-flow, and whale-behavior analysis appears feasible through:
  - maker/taker wallet fields,
  - token-facing trade fields (`maker_asset_id`, `taker_asset_id`).
- Market normalization likely requires joining trade asset identifiers to market metadata token lists:
  - `maker_asset_id` / `taker_asset_id` -> `clob_token_ids`,
  - then map into canonical `condition_id` and `outcome`.
- Legacy FPMM trades require a separate normalization path from CLOB trades.
- `fpmm_address`, `trader`, `outcome_index`, `outcome_tokens`, `is_buy`, `amount`, and `fee_amount` should not be forced into the CLOB trade model without a separate mapping/reconciliation plan.
- Future work should treat CLOB trades and legacy FPMM trades as separate Bronze/Silver normalization branches before combining them into higher-level analysis.

## 6.3 Cross-platform implications

- Cross-platform Polymarket-Kalshi opportunity detection appears promising for future research.
- Candidate analysis areas include:
  - arbitrage,
  - mispricing,
  - stale-price divergence,
  - liquidity-gap assessment.
- This must remain conservative and gated because equivalent-market alignment requires:
  - semantic matching,
  - explicit resolution-criteria comparison before treating two markets as equivalent,
  - event-scope comparison,
  - close/end-time comparison,
  - settlement-logic comparison,
  - fee assumptions,
  - liquidity assumptions,
  - platform restrictions and platform-rule checks,
  - ToS/jurisdiction review.
- Similar titles/questions are not enough for equivalence decisions.
- Future matching should compare resolution rules, event scope, close/end times, settlement logic, fees, liquidity, and platform restrictions before allowing any candidate pair.

## 7) Tooling notes from inspection

- Python `duckdb` was available and used successfully for schema inspection.
- DuckDB CLI was unavailable in the inspection environment.
- Initial schema attempts failed with Git Bash `/e` paths and AppleDouble `._*` artifacts.
- Successful schema inspection used Windows-style `E:/...` paths and explicit ignore behavior for `._*` files.

## 8) Hygiene and import posture rules

Hard constraints remain:

- never commit `data.tar.zst`,
- never commit extracted archive payload files,
- ignore `._*` AppleDouble metadata files,
- do not commit `.duckdb` files,
- do not commit generated reports,
- no import into MEG research tables from this ticket,
- no fixture derivation approval from this ticket.

Future fixture derivation must be:

- tiny,
- deterministic,
- regenerable from approved source/provenance,
- separately reviewed and approved in a dedicated follow-up ticket.

## 9) Candidate follow-up tickets

- **Phase 0B-18:** local archive source manifest update placeholders.
- **Phase 0B-19:** tiny fixture candidate selection plan (no fixture commit yet).
- **Phase 0B-20:** Kalshi/Polymarket semantic matching and cross-platform opportunity research plan.
- **Phase 0B-21:** Polymarket token/outcome normalization plan.
- **Phase 0B-22:** Kalshi normalized fills/markets mapping plan.

## 10) Decision summary

| Decision item | Status | Notes |
|---|---|---|
| Local metadata inspection completion | `yes` | Completed from manual external-drive inspection record. |
| Import approval | `no` | Explicit hold remains in effect. |
| Fixture derivation approval | `no` | Pending separate review and explicit approval. |
| License/provenance completion for archive | `pending` | Keep local-inspection-only posture until resolved. |
| Live trading / connector execution approval | `no` | Not approved by this ticket. |
| Autonomous execution approval | `no` | Not approved by this ticket. |
