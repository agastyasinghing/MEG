# Phase 0B-01 — DuckDB Historical Lake Plan

## Purpose

This document defines the **Phase 0B historical research data layer** for MEG.

The DuckDB historical lake is intended for:

- offline research,
- replay and analysis,
- feature/label iteration,
- and strategy hypothesis testing.

It is **not** part of the live execution rail.

### Boundary from runtime systems

The research lake is explicitly separate from operational runtime infrastructure:

- **Redis/Postgres rail** remains the system of record for live/paper operational flow (signals, proposals, approvals, execution, journaling).
- **DuckDB/Parquet lake** is the system of record for historical research analytics.

No Phase 0B-01 output in this ticket changes:

- Redis channels,
- Postgres operational schemas,
- Telegram approval flow,
- execution authority,
- or runtime order routing.

---

## Candidate Data Sources

Initial source families for Phase 0B historical lake planning:

1. **Historical Polymarket data**
   - markets, outcomes, lifecycle states
   - order/trade history where available
   - resolution metadata

2. **Historical Kalshi data**
   - market definitions and time series needed for cross-market research comparisons
   - venue-specific metadata required for harmonization

3. **Wallet / fill / trade data**
   - whale wallet activity streams
   - normalized fills and participant-level trade records
   - decoded transaction-linked fill evidence (where available)

4. **Market metadata**
   - category, subcategory, tags
   - creation/close/resolution timestamps
   - market description and contract context

5. **Price/odds snapshots**
   - snapshot or bar-based price states over time
   - liquidity/spread context when available

6. **External labels (optional, if available)**
   - manual or derived wallet cohort labels
   - event/classification tags
   - market quality annotations

---

## Proposed DuckDB Table Set

The following research tables are proposed as the first planning baseline.

## 1) `raw_trades`
Raw ingestion of trade/fill-like rows from source feeds before full normalization.

## 2) `raw_markets`
Raw market metadata from Polymarket/Kalshi exports and API captures.

## 3) `price_snapshots`
Time-indexed market price/odds snapshots (and optional liquidity/spread measures).

## 4) `wallet_labels`
Wallet-level labels/cohorts for research segmentation (manual + derived).

## 5) `normalized_fills`
Canonicalized research fill table aligned to MEG identifier contract.

## 6) `forward_returns`
Precomputed forward return labels (multi-horizon) anchored to event timestamps.

## 7) `signal_outcomes`
Research outcomes of signal hypotheses, including realized PnL proxies and decay diagnostics.

---

## Data Dictionary Draft (Phase 0B seed)

These fields form the initial dictionary spine across raw + normalized research tables.

- `condition_id` — canonical market condition identifier (primary routing identifier in MEG contracts).
- `token_id` — canonical outcome token identifier (venue-native execution key).
- `outcome` — normalized outcome label (`YES` / `NO`).
- `market_slug` — human-readable market slug (display and research context only).
- `market_id` (legacy) — retained only as optional compatibility/reference field; not a canonical routing key.
- `wallet_address` — participant wallet identifier.
- `timestamp_ms` — event timestamp in epoch milliseconds (UTC-based normalization target).
- `price` — trade/snapshot probability-like price in `[0,1]` convention where possible.
- `size_usdc` — notional size normalized to USDC terms where derivable.
- `side` — normalized side semantics (e.g., `BUY`/`SELL`, venue-mapped).
- `source` — provenance tag indicating data origin/ingestion path.

---

## Research View Layer (Initial)

Proposed Phase 0B analytical views:

1. `wallet_lead_lag`
   - wallet action timing vs subsequent market movement windows.

2. `wallet_forward_returns`
   - wallet-level cohort forward return summaries across multiple horizons.

3. `market_category_edges`
   - comparative edge statistics by market category/subcategory.

4. `signal_half_life`
   - decay curves and half-life estimates for signal persistence.

5. `cohort_performance`
   - cross-cohort behavior/performance diagnostics (e.g., whales, frequent traders, tagged cohorts).

---

## Query Goals

Phase 0B query pack should answer the following core research questions:

1. **Do whale trades lead subsequent price movement?**
   - quantify lead-lag effect sizes by horizon and category.

2. **What is the empirical signal half-life?**
   - estimate decay speed and practical execution windows.

3. **How do wallet cohorts compare?**
   - assess directional quality, hit-rate proxies, and return dispersion by cohort.

4. **How do market categories compare?**
   - identify where directional or structural edge appears stronger/weaker.

5. **Where do trap/crowding patterns appear?**
   - detect crowded entries, reversal regimes, and weakening follow-through.

---

## Non-goals (Strict)

This ticket is planning-only and explicitly excludes:

1. **No live trading implementation changes.**
2. **No autonomous execution authority.**
3. **No production Redis/Postgres schema/channel changes.**
4. **No strategy/scoring logic changes yet.**

---

## Implementation Roadmap (Phase 0B sequence)

## 0B-02 — Data inventory and import plan
- enumerate source endpoints/files,
- define bronze partitioning strategy,
- and specify ingestion cadence/retention assumptions.

## 0B-03 — Schema + data dictionary spec
- formalize table DDL,
- enforce canonical ID mapping rules,
- and document nullability/unit conventions.

## 0B-04 — First DuckDB loader skeleton
- implement minimal reproducible loaders for priority datasets,
- and validate deterministic ingest fingerprints/checksums.

## 0B-05 — First lead-lag query pack
- ship baseline wallet lead-lag and forward-return query set,
- and output reproducible summary artifacts for strategy research.

---

## Deferred Bookmarks (Intentionally parked)

The following tracks remain deferred and are included as bookmarks only:

1. **Polymarket bot repo feature-mining backlog**
   - backlog intake only; no implementation in this ticket.

2. **Swing bot / volatility sidecar**
   - exploratory track deferred beyond current Phase 0B-01 scope.

3. **Weather paper engine (later)**
   - explicitly out of scope for this ticket and deferred to later planned work.

---

## Acceptance Boundary for 0B-01

This ticket is complete when:

- one documentation artifact defines the DuckDB historical lake plan,
- the runtime execution rail remains unchanged,
- canonical identifier usage is preserved in planning language,
- and concrete next tickets (0B-02 through 0B-05) are enumerated.
