# Phase 0B-23 — Tiny Fixture Derivation Script Plan (Documentation-Only)

## 1) Purpose and posture

This ticket is **documentation-only**.

This ticket defines a **future script plan only**.

This ticket does **not** create a script, does **not** derive fixtures, and does **not** commit fixture data.

This ticket does **not** approve import, loaders, query engines, connector use, order routing, live trading, or autonomous execution.

All fixture derivation remains blocked until a later ticket grants explicit approval.

## 2) Source and dependency anchors

This planning document is anchored to the following Phase 0B records:

- source manifest entry: `local_poly_kalshi_historical_archive_placeholder`
- origin source: `jon_becker_prediction_market_analysis_snapshot`
- archive inspection doc: `docs/phase0b/reviews/JON_BECKER_LOCAL_ARCHIVE_REVIEW_PENDING.md`
- fixture candidate plan: `docs/phase0b/0B-19_TINY_FIXTURE_CANDIDATE_SELECTION_PLAN.md`
- cross-platform research plan: `docs/phase0b/0B-20C_CROSS_PLATFORM_SEMANTIC_MATCHING_RESEARCH_PLAN.md`
- Polymarket normalization plan: `docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md`
- Kalshi normalization plan: `docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md`

## 3) Future script scope

Future work may introduce a local-only, operator-run, deterministic fixture candidate extractor.

Future script scope requirements:

- read only from explicitly approved local archive paths,
- ignore AppleDouble files prefixed with `._`,
- never scan arbitrary user paths,
- never write into `data/` or external archive directories,
- write only to a future explicitly approved fixture output directory,
- support dry-run mode,
- support manifest/provenance output,
- support checksum capture,
- refuse to run unless explicit approval flags/config are present in a future ticket,
- never upload data,
- never call APIs,
- never access network,
- never use secrets,
- never use trading connectors,
- never create `.duckdb` files unless a future ticket explicitly approves them,
- never create generated report outputs unless explicitly approved.

## 4) Candidate fixture groups

Carry forward the seven groups from 0B-19. Suggested tiny output size for each group is `3 to 5` rows or objects.

| Group | Source file path (from 0B-19) | Stable keys (required) | Minimum required non-null fields | Future fixture family | Dependency anchor |
|---|---|---|---|---|---|
| A. Kalshi markets | `data/kalshi/markets/markets_0_10000.parquet` | `ticker_ref/ticker`, `event_ticker_ref/event_ticker`, `fetched_at/_fetched_at` | `ticker`, `event_ticker`, `title`, `status`, `_fetched_at` | `kalshi_markets_tiny` | 0B-22 |
| B. Kalshi trades | `data/kalshi/trades/trades_0_10000.parquet` | `trade_ref/trade_id`, `ticker_ref/ticker`, `created_time` | `trade_id`, `ticker`, `taker_side`, `created_time` | `kalshi_trades_tiny` | 0B-22 |
| C. Polymarket markets | `data/polymarket/markets/markets_0_10000.parquet` | `condition_id`, `source_market_ref/id`, `fetched_at/_fetched_at` | `condition_id`, `id`, `question`, `outcomes`, `_fetched_at` | `poly_markets_tiny` | 0B-21 |
| D. Polymarket CLOB trades | `data/polymarket/trades/trades_0_10000.parquet` | `transaction_hash`, `log_index`, `order_hash` | `transaction_hash`, `log_index`, `order_hash`, `timestamp` | `poly_clob_trades_tiny` | 0B-21 |
| E. Polymarket blocks | `data/polymarket/blocks/blocks_10000000_10100000.parquet` | `block_number` | `block_number`, `timestamp` | `poly_blocks_tiny` | 0B-21 |
| F. Polymarket legacy FPMM trades | `data/polymarket/legacy_trades/trades_0_10000.parquet` | `transaction_hash`, `log_index`, `fpmm_address` | `transaction_hash`, `log_index`, `fpmm_address`, `timestamp` | `poly_legacy_fpmm_trades_tiny` | 0B-21 |
| G. FPMM collateral lookup JSON | `data/polymarket/fpmm_collateral_lookup.json` | `address/key` sorted lexicographically | `collateral_token`, `collateral_symbol`, `collateral_decimals` | `poly_fpmm_collateral_lookup_tiny` | 0B-21 |

Cross-platform use of any tiny fixture outputs depends on 0B-20C.

## 5) Deterministic selection rules

Future script behavior must be deterministic and fail closed:

- use fixed source file paths,
- filter out files prefixed with `._`,
- sort by stable keys before selecting rows or objects,
- select only rows with required key fields populated,
- include time fields where available,
- include price and amount fields where available,
- avoid selecting rows based on profitability or outcome attractiveness,
- avoid cherry-picking specific resolved outcomes,
- produce exactly bounded tiny output sizes,
- preserve raw source values,
- do not normalize fields inside fixture derivation unless explicitly approved,
- record unresolved or missing fields instead of dropping rows silently,
- fail closed when deterministic selection is impossible.

## 6) Suggested stable keys

Use the following stable key plan in the future script:

- Kalshi markets: `ticker_ref/ticker`, `event_ticker_ref/event_ticker`, `fetched_at/_fetched_at`
- Kalshi trades: `trade_ref/trade_id`, `ticker_ref/ticker`, `created_time`
- Polymarket markets: `condition_id`, `source_market_ref/id`, `fetched_at/_fetched_at`
- Polymarket CLOB trades: `transaction_hash`, `log_index`, `order_hash`
- Polymarket blocks: `block_number`
- Polymarket legacy FPMM trades: `transaction_hash`, `log_index`, `fpmm_address`
- FPMM collateral lookup JSON: `address/key` sorted lexicographically

## 7) Provenance and checksum requirements

Future script manifest output must record:

- source manifest ID,
- source repo ID,
- source repo commit inspected,
- local archive path,
- source file relative path,
- source file checksum,
- extraction date or inspection date if known,
- row-selection rule,
- selected row/object count,
- selected stable keys,
- generated fixture file path,
- generated fixture checksum,
- script version,
- parser version,
- operator/reviewer approval reference,
- timestamp of derivation,
- explicit note that fixture is tiny and deterministic.

## 8) Output shape planning

Future candidate output paths (planning only; do not create in this ticket):

- `fixtures/phase0b/kalshi_markets_tiny.json`
- `fixtures/phase0b/kalshi_trades_tiny.json`
- `fixtures/phase0b/poly_markets_tiny.json`
- `fixtures/phase0b/poly_clob_trades_tiny.json`
- `fixtures/phase0b/poly_blocks_tiny.json`
- `fixtures/phase0b/poly_legacy_fpmm_trades_tiny.json`
- `fixtures/phase0b/poly_fpmm_collateral_lookup_tiny.json`
- `fixtures/phase0b/fixture_manifest.json`

These are future candidate paths only and must not be created by this documentation ticket.

## 9) Safety gates and refusal behavior

Future script should refuse to run if any of the following applies:

- source manifest status is not approved for fixture derivation,
- license/provenance status is unresolved or not explicitly approved,
- checksum strategy is missing,
- output directory is not explicitly approved,
- requested row/object count exceeds approved tiny limits,
- source path is outside approved archive root,
- source file is AppleDouble metadata,
- source file path is absolute when relative path is required,
- generated output would overwrite existing fixture without explicit flag,
- network access is requested,
- secrets are present,
- connector/trading module import is attempted,
- `.duckdb` file creation is attempted without approval,
- generated report output is attempted without approval.

## 10) Privacy, security, and compliance gates

Before fixture derivation is approved in a future ticket, reviewers must confirm:

- public wallet/address field handling is approved,
- no private user PII is included,
- no secrets are included,
- no API keys are included,
- no full local archive absolute paths are embedded inside fixture payloads,
- no ToS/redistribution conflict exists,
- no jurisdiction-sensitive operational claim is introduced,
- no trading/execution implication is implied by fixture content.

## 11) Platform-specific notes

### Polymarket

- preserve raw `outcomes` and `clob_token_ids` before parsing,
- do not infer outcome from price, wallet, title, or slug alone,
- preserve unresolved token mappings,
- keep CLOB and legacy FPMM paths separate,
- preserve block/timestamp fields for later reconciliation.

### Kalshi

- preserve raw `ticker`, `event_ticker`, `title`, `subtitle`, `result`, `taker_side`, and price fields,
- do not infer result from price, title, or subtitle alone,
- preserve unresolved ticker/event/taker-side/result mappings,
- do not treat snapshot fields as executable orderbook prices.

## 12) Future test implications

Later static/preflight tickets should add tests for:

- fixture manifest shape,
- source provenance field presence,
- checksum field presence,
- row count bounds,
- no absolute archive path in fixture payloads,
- no AppleDouble source file use,
- no `.duckdb` artifact creation,
- no generated report artifact creation,
- no network/API/secret dependency,
- per-group required field shape,
- unresolved-state preservation.

## 13) Recommended next tickets

- Phase 0B-24: cross-platform candidate-pair schema fixture tests (static/preflight only)
- Phase 0B-25: semantic matching rejection-reason taxonomy tests (static/preflight only)
- Phase 0B-26: integration/rate-limit/fee source appendix maintenance plan
- Phase 1 candidate: approved local fixture generation and Bronze schema implementation, only after Phase 0B closes

## 14) Explicit non-approvals

This ticket explicitly does **not** approve:

- script implementation,
- fixture derivation,
- fixture commit,
- data import,
- loader implementation,
- query engine implementation,
- connector implementation,
- order placement,
- live trading,
- autonomous execution.

## 15) Static canonical-ID guard

Canonical-ID guard posture for this document:

- avoid the literal legacy identifier term;
- use `source_market_ref`, `ticker_ref`, native market reference, source market identifier, or legacy market identifier prose;
- if a future change requires a literal legacy identifier token, update `tests/core/canonical_id_allowlist.py` exactly and narrowly in that future change only.
