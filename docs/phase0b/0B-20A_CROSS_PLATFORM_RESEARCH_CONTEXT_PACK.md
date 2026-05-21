# Phase 0B-20A — Cross-Platform Research Context Pack (Fresh-Chat Input)

## 1) Purpose and boundary

This document is a **fresh-chat research context pack** for **Phase 0B-20B**.

It is designed to be pasted into a new ChatGPT/web-research session so a researcher can produce a detailed, cited research document.

This document is:

- not the final Phase 0B-20B research output,
- not implementation,
- not fixture derivation,
- not data import approval,
- not live trading approval,
- not autonomous execution approval.

## 2) MEG strategic scope (for research framing)

- MEG is a broad prediction-market intelligence engine.
- Kalshi and Polymarket are both first-class research targets.
- Long-term direction includes both platform-native strategies and cross-platform opportunities.
- Cross-platform opportunity detection scope includes:
  - arbitrage,
  - mispricing,
  - stale-price divergence,
  - liquidity gaps,
  - event-resolution mismatches,
  - market-structure inefficiencies.
- MEG may eventually support autonomous trading in later phases, but **Phase 0B does not approve**:
  - trading,
  - order placement,
  - connector implementation,
  - autonomous execution authority.

## 3) Phase 0B constraints (must remain explicit)

Phase 0B posture for this work is strictly:

- research/planning only,
- no runtime implementation,
- no connector implementation,
- no order routing,
- no live trading,
- no autonomous execution,
- no fixture derivation,
- no data import,
- no legal/ToS assumption should be treated as approved,
- all cross-platform matching must be conservative and reviewable.

## 4) Archive/source context from local inspection

Use the following local-inspection context as a starting point:

- `source_id`: `local_poly_kalshi_historical_archive_placeholder`
- repo source: `jon_becker_prediction_market_analysis_snapshot`
- inspection doc: `docs/phase0b/reviews/JON_BECKER_LOCAL_ARCHIVE_REVIEW_PENDING.md`
- archive path inspected: `/e/meg_source_review/repos/prediction-market-analysis/data`
- total files: `78732`
- parquet files: `78723`
- AppleDouble metadata files: `29245` (ignore files prefixed with `._`)

Platform folders observed in local archive:

- Kalshi:
  - `data/kalshi/markets`
  - `data/kalshi/trades`
- Polymarket:
  - `data/polymarket/blocks`
  - `data/polymarket/markets`
  - `data/polymarket/trades`
  - `data/polymarket/legacy_trades`
- JSON:
  - `data/polymarket/fpmm_collateral_lookup.json`

## 5) Concise schema fingerprints

### Kalshi markets

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
- `_fetched_at`

### Kalshi trades

- `trade_id`
- `ticker`
- `count`
- `yes_price`
- `no_price`
- `taker_side`
- `created_time`
- `_fetched_at`

### Polymarket markets

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

### Polymarket CLOB trades

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

### Polymarket blocks

- `block_number`
- `timestamp`

### Polymarket legacy FPMM trades

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

### FPMM collateral lookup JSON

- object mapping FPMM/contract-like addresses to:
  - `collateral_token`
  - `collateral_symbol`
  - `collateral_decimals`

## 6) Research mission for Phase 0B-20B (fresh chat)

The fresh-chat researcher should produce a **detailed, cited research document** for:

- Kalshi/Polymarket semantic matching,
- cross-platform opportunity detection.

Research expectations:

- Use current public sources where needed.
- Prioritize primary/official sources when possible:
  - Kalshi docs,
  - Polymarket docs,
  - API docs,
  - fee pages,
  - rules pages,
  - ToS/legal pages,
  - market examples,
  - platform help docs,
  - settlement/resolution docs.
- Use secondary sources only when helpful and clearly label them as secondary.
- Surface uncertainties rather than guessing.

## 7) Open-ended research posture

The following research lanes are **guides, not hard limits**.

- Go beyond these lanes if you find additional relevant issues, risks, opportunities, platform mechanics, API constraints, market-structure details, or design implications.
- Do not treat this list as exhaustive.
- Add unexpected findings and propose new follow-up tickets where useful.

## 8) Guiding research lanes (non-exhaustive)

### Lane A — Platform mechanics

- How Kalshi markets are structured.
- How Polymarket markets are structured.
- How each platform defines outcomes, contracts, tickers/questions, close times, settlement, and resolution.
- How fees, price units, order books, liquidity, and settlement differ.

### Lane B — Semantic market matching

- What fields can help match equivalent or near-equivalent markets.
- Kalshi `title`/subtitle/`ticker`/`event_ticker` versus Polymarket `question`/`slug`/`outcomes`/`condition_id`/`clob_token_ids`.
- Why similar wording is insufficient.
- How to compare resolution criteria, event scope, time windows, settlement logic, and edge cases.
- Possible scoring model for match confidence.
- Human-review thresholds for equivalence.

### Lane C — Cross-platform opportunity types

- True arbitrage candidates.
- Mispricing and probability divergence.
- Stale-price divergence.
- Liquidity-gap opportunities.
- Latency-sensitive opportunities.
- Market-resolution mismatch opportunities.
- Fee/slippage-adjusted opportunities.
- Risk-free versus risk-adjusted opportunities.

### Lane D — Data/model implications for MEG

- What normalized entities MEG needs.
- Candidate schemas for cross-platform pairs.
- Features needed for match confidence.
- Features needed for arbitrage/mispricing scoring.
- Where Polymarket token/outcome normalization intersects with cross-platform matching.
- Where Kalshi normalized market/fill mapping intersects with cross-platform matching.

### Lane E — Risk and compliance

- ToS/jurisdiction caveats.
- CFTC/regulatory implications at high level.
- Platform restrictions.
- Data redistribution concerns.
- Live trading restrictions.
- Why Phase 0B must remain research-only.

### Lane F — Implementation planning (still no implementation)

- Suggested docs-only deliverables.
- Future fixture needs.
- Future tests.
- Future manual review gates.
- Future connector boundaries.
- Suggested follow-up tickets.

## 9) Required output format for Phase 0B-20B research deliverable

The fresh-chat research output should include:

- Executive summary
- Source list with citations
- Platform mechanics comparison
- Semantic matching framework
- Cross-platform opportunity taxonomy
- Fee/liquidity/slippage caveats
- Resolution/settlement caveats
- API/data implications
- MEG architecture implications
- Conservative acceptance criteria
- “Do not implement yet” boundaries
- Open questions
- Recommended follow-up tickets

## 10) Explicit safety and posture requirements

- No instructions to place trades.
- No evasion of platform rules.
- No bypassing KYC, geo, API, or legal restrictions.
- No assumption that arbitrage is risk-free.
- No claim that similar markets are equivalent without resolution review.
- No autonomy until future phases add controls, kill switches, monitoring, audit logs, and explicit approval.

## 11) Paste-ready prompt block for fresh-chat research

```text
You are assisting with MEG Phase 0B-20B research.

Context and purpose:
- This is a research/planning task only.
- Produce a detailed, cited research document for Kalshi/Polymarket semantic matching and cross-platform opportunity detection.
- This is not implementation, not fixture derivation, not data import, and not live-trading/autonomous approval.

MEG strategic scope:
- MEG is a broad prediction-market intelligence engine.
- Kalshi and Polymarket are first-class research targets.
- Long-term scope includes both platform-native strategies and cross-platform opportunities.
- Cross-platform opportunity categories include arbitrage, mispricing, stale-price divergence, liquidity gaps, event-resolution mismatches, and market-structure inefficiencies.
- Phase 0B does not approve trading, order placement, connector implementation, or autonomy.

Phase 0B constraints:
- research/planning only
- no runtime implementation
- no connector implementation
- no order routing
- no live trading
- no autonomous execution
- no fixture derivation
- no data import
- no legal/ToS assumption should be treated as approved
- all cross-platform matching must be conservative and reviewable

Local archive/schema context from prior inspection:
- source_id: local_poly_kalshi_historical_archive_placeholder
- repo source: jon_becker_prediction_market_analysis_snapshot
- inspection doc: docs/phase0b/reviews/JON_BECKER_LOCAL_ARCHIVE_REVIEW_PENDING.md
- archive path inspected: /e/meg_source_review/repos/prediction-market-analysis/data
- total files: 78732
- parquet files: 78723
- AppleDouble metadata files: 29245 (ignore files prefixed with ._)
- Kalshi folders: data/kalshi/markets, data/kalshi/trades
- Polymarket folders: data/polymarket/blocks, data/polymarket/markets, data/polymarket/trades, data/polymarket/legacy_trades
- JSON: data/polymarket/fpmm_collateral_lookup.json

Schema fingerprints:
- Kalshi markets: ticker, event_ticker, market_type, title, yes_sub_title, no_sub_title, status, yes_bid, yes_ask, no_bid, no_ask, last_price, volume, volume_24h, open_interest, result, created_time, open_time, close_time, _fetched_at
- Kalshi trades: trade_id, ticker, count, yes_price, no_price, taker_side, created_time, _fetched_at
- Polymarket markets: id, condition_id, question, slug, outcomes, outcome_prices, clob_token_ids, volume, liquidity, active, closed, end_date, created_at, market_maker_address, _fetched_at
- Polymarket CLOB trades: block_number, transaction_hash, log_index, order_hash, maker, taker, maker_asset_id, taker_asset_id, maker_amount, taker_amount, fee, timestamp, _fetched_at, _contract
- Polymarket blocks: block_number, timestamp
- Polymarket legacy FPMM trades: block_number, transaction_hash, log_index, fpmm_address, trader, amount, fee_amount, outcome_index, outcome_tokens, is_buy, timestamp, _fetched_at
- FPMM collateral lookup JSON: object mapping FPMM/contract-like addresses to collateral_token, collateral_symbol, collateral_decimals

Research-source requirements:
- Perform web research with citations.
- Prefer official/primary sources whenever possible (platform docs, API docs, fee pages, rules pages, settlement/resolution pages, ToS/legal pages, help docs, and concrete market examples).
- Use secondary sources only when helpful; label them clearly as secondary.
- Flag uncertainty and open issues instead of guessing.

Research lanes (guides, not hard limits; do not treat as exhaustive):
A) Platform mechanics
B) Semantic market matching
C) Cross-platform opportunity types
D) Data/model implications for MEG
E) Risk and compliance
F) Implementation planning (still no implementation)

Go beyond these lanes if you find relevant additional issues, risks, opportunities, platform mechanics, API constraints, market-structure details, or design implications. Include unexpected findings and propose follow-up tickets when useful.

Required output format:
1) Executive summary
2) Source list with citations
3) Platform mechanics comparison
4) Semantic matching framework
5) Cross-platform opportunity taxonomy
6) Fee/liquidity/slippage caveats
7) Resolution/settlement caveats
8) API/data implications
9) MEG architecture implications
10) Conservative acceptance criteria
11) “Do not implement yet” boundaries
12) Open questions
13) Recommended follow-up tickets

Safety/posture constraints:
- No instructions to place trades.
- No evasion of platform rules.
- No bypassing KYC, geo, API, or legal restrictions.
- Do not assume arbitrage is risk-free.
- Do not claim similar markets are equivalent without explicit resolution review.
- No autonomy recommendations until future phases add controls, kill switches, monitoring, audit logs, and explicit approval.
```
