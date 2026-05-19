# Phase 0B-02 — Data and Repo Inventory Plan

## 1) Purpose

Phase 0B-02 is a **documentation-only planning ticket** with the rule: inventory first, implementation later.

This plan is explicitly separate from live execution. It defines what to inventory and how to evaluate future imports before any implementation work.

Boundaries for this ticket:

- no runtime Redis/Postgres contract or schema changes,
- no execution-path changes,
- no strategy/scoring changes,
- no DuckDB dependency installation yet,
- no loader implementation yet,
- no external repo cloning/vendoring in this ticket.

## 2) Historical Data Inventory

| Source/category | Expected contents | Expected format | Expected size/volume (if known) | Access method | Freshness | Licensing/terms concern | Priority | Phase 0B use |
|---|---|---|---|---|---|---|---|---|
| Jon-Becker/prediction-market-analysis (candidate dataset/framework source) | Historical prediction-market research dataset patterns, transforms, and analysis framing for Polymarket/Kalshi-like studies | Repo assets, notebooks/scripts, parquet/csv patterns (to validate per source review) | Unknown in this repo-only phase; historically associated with large research corpus contexts | Manual source review and later controlled ingest design | Depends on upstream snapshots/releases | Must review repository license and dataset rights before reuse/import | P0 | Seed fixture shape ideas, schema planning, and ingestion acceptance criteria |
| Local Polymarket/Kalshi historical archive (if available) | Multi-venue historical markets/trades/time series/snapshots for backfill | Parquet/CSV/JSON bundles (to inventory exactly first) | ~36 GiB class dataset (if present) | Local filesystem inventory + manifesting | Static point-in-time unless refreshed | Confirm provenance and redistribution constraints | P0 | Main medium-term backfill candidate after fixture-first validation |
| Polymarket market metadata | Market definitions, outcomes, lifecycle timestamps, tags, resolution context | JSON/CSV/API exports | Medium | API/export capture plan (future ticket) | Medium | API terms, retention, and use constraints must be validated | P0 | Canonical identifier mapping tests + metadata normalization |
| Polymarket trade/fill history | Trade/fill rows with timestamp, side, price, size, wallet references where available | JSON/CSV/Parquet extracts | High row count likely | Historical export/capture jobs (future ticket) | Medium/high | Participant-data handling and source terms review needed | P0 | Lead-lag and forward-return research inputs |
| Kalshi market/time-series data | Market metadata + venue-specific time series for comparative research | CSV/JSON/API exports | Medium/high | API/export pipeline design (future ticket) | Medium | Must validate Kalshi terms/licensing for archival research storage | P1 | Cross-market normalization and comparison studies |
| CLOB/order-book snapshots | Bid/ask ladders, spread, depth, quote-state timelines | JSONL/Parquet snapshots | High (especially high-frequency captures) | Snapshot archives/WebSocket capture outputs (future ticket) | High when captured; static once archived | Storage/retention policy and terms checks required | P1 | Microstructure context and slippage/spread research |
| Wallet-level trade activity | Wallet-centric trade timelines and behavior cohorts | CSV/JSON/Parquet normalized rows | Medium/high | Derived from fill/trade joins + enrichment | Medium | Privacy/compliance posture and labeling governance needed | P1 | Cohort analytics and wallet behavior features |
| Manual wallet labels | Curated labels/notes/provenance for known wallets/cohorts | CSV/YAML/small parquet reference tables | Small | Manually maintained internal artifacts | Slow-changing | Provenance tracking and review discipline required | P2 | Segmentation and cohort-level performance slicing |
| External outcome/resolution metadata | Supplemental resolution references and outcome context | CSV/JSON/reference tables | Small/medium | Public refs + curated mappings | Low | Validate external source terms and attribution needs | P2 | Resolution QA and reconciliation checks |

## 3) Reference Repo Feature-Mining Inventory

Feature-mining principle: **mine ideas, not code**.

| Repo | Category | Likely useful ideas | What NOT to copy | Possible MEG phase | Priority |
|---|---|---|---|---|---|
| Polymarket/agents | agent architecture | Agent decomposition patterns, orchestration interfaces, tool boundaries | Direct strategy logic or execution assumptions that bypass MEG approval model | Phase 3+ architecture refinement | P1 |
| skharchikov/polymarket-bot | bot execution/trading system patterns | Bot lifecycle management, config patterns, exchange adapter boundaries | Blind reuse of order logic/risk assumptions/license-bound code | Phase 2/3 backlog inspiration | P1 |
| Drakkar-Software/OctoBot-Prediction-Market | bot execution/trading system patterns | Plugin-style bot modularity, signal plumbing concepts | Vendor-style import of framework internals | Phase 3+ modularity ideas | P2 |
| ImMike/polymarket-arbitrage | arbitrage/cross-market logic | Opportunity detection framing, spread/path evaluation concepts | Any autonomous execution shortcuts or non-MEG risk controls | Phase 6 (explicit arbitrage phase) | P2 |
| aulekator/Polymarket-BTC-15-Minute-Trading-Bot | bot execution/trading system patterns | Short-horizon signal framing and evaluation checkpoints | Hardcoded strategy rules and capital assumptions | Phase 3+ research inspiration | P3 |
| nautechsystems/nautilus_trader | production trading engine architecture | Robust engine architecture patterns: event flow, replay discipline, adapters | Large framework vendoring or incompatible abstractions | Phase 4/5 infra-hardening ideas | P1 |
| HKUDS/AI-Trader | swarm/agent inspiration | Multi-agent research workflow ideas and experiment orchestration | Copying model prompts/weights/pipelines without fit/license review | Phase 5+ experimentation framework ideas | P3 |
| Jon-Becker/prediction-market-analysis | historical dataset/research framework | Data-modeling patterns, query framing, reproducible research structure | Direct dataset/code import without provenance/license review | Phase 0B core planning input | P0 |
| 666ghj/MiroFish | swarm/agent inspiration | Agent coordination metaphors and task decomposition ideas | Unreviewed integration of third-party agent runtime code | Phase 5+ ideation only | P3 |

## 4) Copy/Learn Rules

1. Mine ideas, not code.
2. No blind copying from external repositories.
3. No vendor imports in Phase 0B planning tickets.
4. No license-risk code adoption without explicit legal/license review.
5. Convert useful findings into scoped MEG tickets only after source review.
6. Keep data/research ideas separated from live execution ideas.

## 5) Import Staging Model

Future implementation tickets should stage imports in three layers:

1. **Bronze (raw immutable files)**
   - preserve source bytes/records as acquired,
   - keep immutable partitions and provenance manifests.

2. **Silver (normalized tables)**
   - normalize identifiers and field semantics,
   - standardize timestamps/units/types,
   - attach quality/provenance flags.

3. **Gold (research views)**
   - produce derived analytical views for lead-lag, forward returns, cohorts, and decay studies.

The DuckDB/Parquet lake is a **research-only data plane**, separate from live execution and operational journaling.

## 6) Proposed Local Directory/Artifact Layout

- `data/raw/` — immutable source drops + manifests.
- `data/staged/` — normalized intermediate artifacts.
- `data/duckdb/` — local DuckDB files/metadata.
- `data/exports/` — reproducible query outputs.
- `data/fixtures/` — tiny deterministic fixtures for test/dev validation.

Rules:

- large data files should not be committed,
- `.duckdb` files should not be committed,
- only tiny fixtures should live in the repository,
- future `.gitignore` review may be needed to enforce these boundaries consistently.

## 7) First Import Priority

Start with the **smallest high-value import** that validates end-to-end ingest behavior.

Recommended first priority:

1. tiny sample fixture derived from Jon-Becker/prediction-market-analysis style data if available, **or**
2. small Polymarket market metadata/trade sample.

Do **not** start by loading the full ~36 GiB historical corpus.

## 8) Validation Checks for Future Import Tickets

Every import ticket should include:

1. row-count reconciliation,
2. schema fingerprint capture,
3. null-rate checks for critical fields,
4. timestamp min/max and timezone normalization checks,
5. duplicate-key checks on expected unique keys,
6. sample canonical identifier checks (`condition_id`, `token_id`, `outcome`),
7. source provenance check (origin + acquisition metadata),
8. small fixture checksum verification.

## 9) Non-goals

Phase 0B-02 excludes:

- live trading changes,
- autonomous execution,
- runtime Redis/Postgres changes,
- strategy/scoring changes,
- DuckDB dependency installation,
- loader implementation,
- external repo vendoring,
- large dataset commits.

## 10) Recommended Next Ticket

**Phase 0B-03: Schema + Data Dictionary Spec**

Minimum expected output for 0B-03:

- formal table-level schema specs,
- field-level data dictionary (types, nullability, units),
- canonical identifier mapping and validation rules,
- fixture-first ingestion acceptance criteria.
