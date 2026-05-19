# Phase 0B-03 — Schema + Data Dictionary Spec

## 1) Purpose and boundaries

This ticket defines a **documentation-only schema and data dictionary specification** for the first MEG DuckDB/Parquet historical research lake.

Boundary statements:

- This is a **schema spec only** ticket.
- This applies to the **historical research lake only**.
- This remains separate from the live shared rail (Redis channels, Telegram approval queue, and Postgres operational journal).
- This ticket introduces **no execution or trading behavior changes**.
- This ticket introduces **no dependency install, loader code, or data file ingestion**.

## 2) Naming and identifier rules

Canonical identifier contract (must hold across all research tables):

1. `condition_id` is the canonical market/condition identifier.
2. `token_id` is the canonical outcome token identifier.
3. `outcome` is the normalized outcome label (`YES` / `NO`).
4. `market_slug` is display/research context only and is never a routing key.
5. Legacy market identifier fields may be retained only for source compatibility/reference.
6. Source and provenance fields must be preserved so every row can be traced to origin.
7. Legacy identifiers must not be used as canonical matching or routing keys.

## 3) Proposed table schemas

## 3.1 `raw_trades` (Bronze)

- **Purpose:** Immutable source-level trade/fill-like records before normalization.
- **Grain / primary row meaning:** One raw source trade/fill event.
- **Key fields:** `source`, `source_trade_id` (or `tx_hash` + source event index fallback), `timestamp_ms`.
- **Required fields:** `source`, `timestamp_ms`, at least one canonical mapping anchor (`condition_id` or `token_id`), `price` when provided by source.
- **Nullable fields:** `condition_id`, `token_id`, `outcome`, `wallet_address`, `size_usdc`, `tx_hash`, `block_number`, `market_slug`, legacy market identifier.
- **Timestamp fields:** `timestamp_ms` (event time), `ingested_at_ms` (ingestion lineage).
- **Provenance fields:** `source`, `source_file`, `source_trade_id`, `ingest_run_id`, `raw_payload_hash`.
- **Validation checks:**
  - `timestamp_ms > 0`.
  - `price` in `[0,1]` when populated.
  - At least one of `condition_id`, `token_id`, or legacy market identifier present.
  - Duplicate detection on (`source`, `source_trade_id`) where source IDs exist.

## 3.2 `raw_markets` (Bronze)

- **Purpose:** Immutable source market metadata snapshots.
- **Grain / primary row meaning:** One source market metadata record at capture time.
- **Key fields:** `source`, `source_market_ref`, `captured_at_ms`.
- **Required fields:** `source`, `captured_at_ms`, `source_market_ref`, and any available canonical mapping fields.
- **Nullable fields:** `condition_id`, `market_slug`, `market_category`, `liquidity_usdc`, resolution timestamps, legacy market identifier.
- **Timestamp fields:** `captured_at_ms`, `open_timestamp_ms`, `close_timestamp_ms`, `resolution_timestamp_ms`.
- **Provenance fields:** `source`, `source_file`, `ingest_run_id`, `raw_payload_hash`.
- **Validation checks:**
  - `captured_at_ms > 0`.
  - Lifecycle timestamps monotonically consistent when present.
  - Canonical mapping coverage tracked (percent with `condition_id`).

## 3.3 `price_snapshots` (Bronze/Silver bridge)

- **Purpose:** Time-indexed probability and microstructure state.
- **Grain / primary row meaning:** One `(token_id, timestamp_ms, source)` snapshot.
- **Key fields:** `token_id`, `timestamp_ms`, `source`.
- **Required fields:** `timestamp_ms`, `source`, and one of `token_id` / `condition_id`; `price`.
- **Nullable fields:** `condition_id`, `outcome`, `market_slug`, `liquidity_usdc`, `spread`, `bid_price`, `ask_price`.
- **Timestamp fields:** `timestamp_ms`, `ingested_at_ms`.
- **Provenance fields:** `source`, `source_file`, `ingest_run_id`.
- **Validation checks:**
  - `price` in `[0,1]`.
  - `spread >= 0` when present.
  - `liquidity_usdc >= 0` when present.
  - No duplicate (`token_id`, `timestamp_ms`, `source`) rows.

## 3.4 `wallet_labels` (Silver reference)

- **Purpose:** Wallet cohort/label enrichment for research segmentation.
- **Grain / primary row meaning:** One label assignment per wallet and label source/version.
- **Key fields:** `wallet_address`, `label_source`, `label_name`.
- **Required fields:** `wallet_address`, `label_source`, `label_name`, `label_confidence` or equivalent quality marker.
- **Nullable fields:** `valid_from_ms`, `valid_to_ms`, label notes.
- **Timestamp fields:** `assigned_at_ms`, `valid_from_ms`, `valid_to_ms`.
- **Provenance fields:** `label_source`, `source`, `ingest_run_id`, `reviewed_by`.
- **Validation checks:**
  - `wallet_address` normalized (lowercase hex format).
  - `label_confidence` in `[0,1]` when present.
  - At most one active row per (`wallet_address`, `label_source`, `label_name`) at a timestamp.

## 3.5 `normalized_fills` (Silver)

- **Purpose:** Canonicalized fill/trade table aligned to MEG identifier contract.
- **Grain / primary row meaning:** One normalized fill event.
- **Key fields:** `source`, `source_fill_id` (or deterministic surrogate), `timestamp_ms`, `token_id`.
- **Required fields:** `condition_id`, `token_id`, `outcome`, `timestamp_ms`, `source`, `price`, `side`.
- **Nullable fields:** `wallet_address`, `size_usdc`, `tx_hash`, `block_number`, `market_slug`, fees.
- **Timestamp fields:** `timestamp_ms`, `ingested_at_ms`.
- **Provenance fields:** `source`, `source_fill_id`, `source_file`, `ingest_run_id`, `normalization_version`.
- **Validation checks:**
  - Canonical ID triple present (`condition_id`, `token_id`, `outcome`).
  - `side` in (`BUY`, `SELL`).
  - `price` in `[0,1]`.
  - Duplicate-key check on normalized unique event key.

## 3.6 `forward_returns` (Gold label table)

- **Purpose:** Precomputed forward-return labels for research windows.
- **Grain / primary row meaning:** One anchor event and one forward horizon.
- **Key fields:** `token_id`, `timestamp_ms`, `horizon_seconds`, `source`.
- **Required fields:** `condition_id`, `token_id`, `outcome`, `timestamp_ms`, `horizon_seconds`, `forward_return_bps`, `source`.
- **Nullable fields:** `market_slug`, anchor/forward prices if not available for specific horizon.
- **Timestamp fields:** `timestamp_ms` (anchor), `forward_timestamp_ms`.
- **Provenance fields:** `source`, `return_calc_version`, `ingest_run_id`.
- **Validation checks:**
  - `horizon_seconds > 0`.
  - Anchor and forward timestamps are ordered.
  - Return reproducibility for deterministic fixtures.

## 3.7 `signal_outcomes` (Gold research output)

- **Purpose:** Research join between signal hypotheses and realized outcomes.
- **Grain / primary row meaning:** One `signal_id` evaluated at one horizon.
- **Key fields:** `signal_id`, `horizon_seconds`, `label_source`.
- **Required fields:** `signal_id`, `condition_id`, `token_id`, `outcome`, `timestamp_ms`, `horizon_seconds`, `label_source`.
- **Nullable fields:** `forward_return_bps`, realized proxy metrics, notes.
- **Timestamp fields:** `timestamp_ms` (signal time), `evaluated_at_ms`.
- **Provenance fields:** `label_source`, `source`, `signal_generation_version`, `evaluation_version`.
- **Validation checks:**
  - One row per (`signal_id`, `horizon_seconds`, `label_source`).
  - Canonical ID triple present.
  - Horizon/value completeness metrics reported.

## 4) Field-level data dictionary

| Field | Description | Type guidance | Unit convention | Nullability guidance |
|---|---|---|---|---|
| `condition_id` | Canonical market condition identifier. | `TEXT` hex-like string. | N/A. | Required in normalized/gold tables; nullable in raw only when source lacks mapping. |
| `token_id` | Canonical outcome token identifier. | `TEXT` numeric string (avoid integer overflow risk). | N/A. | Required in normalized/gold; nullable in early raw capture. |
| `outcome` | Normalized outcome label. | `TEXT` enum-like (`YES`,`NO`). | N/A. | Required after normalization. |
| `market_slug` | Human-readable market context field. | `TEXT`. | N/A. | Optional everywhere; never routing-critical. |
| Legacy market identifier | Source-compatibility identifier from upstream systems. | `TEXT`. | N/A. | Optional; compatibility/reference only. |
| `wallet_address` | Trader/participant wallet address. | `TEXT` lowercase hex string. | N/A. | Nullable when unavailable or intentionally redacted. |
| `timestamp_ms` | Event or anchor timestamp. | `BIGINT`. | Epoch milliseconds UTC. | Required in all listed tables. |
| `source` | Origin tag for provenance. | `TEXT` (controlled vocabulary recommended). | N/A. | Required in all listed tables. |
| `price` | Probability-like trade/snapshot price. | `DOUBLE` or `DECIMAL(9,6)`. | Fraction in `[0,1]`. | Required where price-bearing rows are expected; otherwise nullable by table purpose. |
| `size_usdc` | Notional size normalized to USDC-equivalent. | `DOUBLE` or `DECIMAL(18,6)`. | USDC notional. | Nullable if source cannot provide reliable sizing. |
| `side` | Trade side after normalization. | `TEXT` enum-like (`BUY`,`SELL`). | N/A. | Required in `normalized_fills`; optional in some raw sources. |
| `tx_hash` | Transaction hash for chain-linked events. | `TEXT`. | N/A. | Nullable for non-chain or aggregate sources. |
| `block_number` | Chain block height associated with event. | `BIGINT`. | Block number integer. | Nullable when not chain-derived. |
| `market_category` | Research grouping/category. | `TEXT`. | N/A. | Nullable until category mapping exists. |
| `liquidity_usdc` | Liquidity estimate near snapshot time. | `DOUBLE` or `DECIMAL(18,6)`. | USDC-equivalent. | Nullable when source omits liquidity fields. |
| `spread` | Bid-ask spread at snapshot time. | `DOUBLE` or `DECIMAL(9,6)`. | Fractional probability points. | Nullable if bid/ask unavailable. |
| `forward_return_bps` | Forward return from anchor to horizon. | `DOUBLE`. | Basis points. | Required in `forward_returns`; optional in partially evaluated `signal_outcomes`. |
| `horizon_seconds` | Forward evaluation horizon. | `INTEGER`. | Seconds. | Required in `forward_returns` and `signal_outcomes`. |
| `signal_id` | Stable signal identifier for research joins. | `TEXT`/UUID string. | N/A. | Required in `signal_outcomes`; absent elsewhere. |
| `label_source` | Origin of labels/outcome mapping logic. | `TEXT`. | N/A. | Required where labels/outcomes are derived (`wallet_labels`, `signal_outcomes`). |

## 5) Bronze / Silver / Gold mapping

- **Bronze (raw):** `raw_trades`, `raw_markets`.
- **Bronze/Silver bridge:** `price_snapshots` (raw captures with normalization-ready keys).
- **Silver (normalized/reference):** `normalized_fills`, `wallet_labels`.
- **Gold (research outputs/labels):** `forward_returns`, `signal_outcomes`.

## 6) Fixture-first acceptance criteria

Before any full historical dataset load, a tiny deterministic fixture must prove:

1. Deterministic row counts per table across repeated runs.
2. Stable schema fingerprint (column names/order/types hash).
3. Timestamp range checks (expected min/max in fixture window).
4. Canonical identifier coverage checks (`condition_id`, `token_id`, `outcome`) for normalized/gold tables.
5. Duplicate-key check passes for declared table keys/grains.
6. Source provenance is present (`source`, run identifier, and source reference fields).
7. No large data committed (fixture remains tiny and repository-safe).

## 7) Non-goals

This ticket explicitly does **not** include:

- DuckDB dependency installation,
- loader implementation,
- data file commits,
- strategy/scoring logic changes,
- live execution integration,
- external repository vendoring.

## 8) Recommended next ticket

**Phase 0B-04: First DuckDB Loader Skeleton**

Expected focus for 0B-04:

- implement minimal loader skeletons against tiny deterministic fixtures,
- enforce schema fingerprint and provenance assertions,
- keep runtime execution rail fully untouched.
