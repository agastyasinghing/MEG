# Phase 0B-22 — Kalshi Normalized Fills/Markets Mapping Plan (Docs-Only)

## 1) Purpose and posture

This ticket is **documentation-only**.

This document defines a **Kalshi normalization design plan** for future MEG historical-research normalization work.

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
- related Polymarket normalization doc: `docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md`

Local archive folders/files in scope:

- `data/kalshi/markets`
- `data/kalshi/trades`

File handling rule:

- AppleDouble metadata files prefixed with `._` must be ignored.

## 3) Core normalization problem

Kalshi market rows and trade rows are not automatically analysis-safe as one flat table.

Observed shape separation:

- Market rows include ticker/event-ticker/title/subtitle/status/result/timing context plus snapshot-like price/liquidity fields.
- Trade rows include trade reference, ticker, count, yes/no price, taker side, and trade-time fields.

MEG normalization planning needs:

- deterministic ticker-based linking from trades to markets,
- event-ticker-based grouping from markets to event-like groupings,
- normalized yes/no outcome entities so yes/no prices and result semantics are interpreted consistently,
- explicit preservation of raw price/count values until scale/units are handled by a future approved rule set.

Cross-platform boundary:

- MEG must not infer cross-platform equivalence from title/subtitle/ticker fields alone.

## 4) Proposed Bronze/Silver/Gold model (planning-only)

The following are planned entities only, not implemented tables.

### Bronze (raw landing targets)

- `bronze_kalshi_markets_raw`
- `bronze_kalshi_trades_raw`

### Silver (normalized targets)

- `silver_kalshi_events`
- `silver_kalshi_markets`
- `silver_kalshi_outcomes`
- `silver_kalshi_market_snapshots`
- `silver_kalshi_fills`
- `silver_kalshi_results`

### Gold (analysis-ready targets)

- `gold_kalshi_market_flow`
- `gold_kalshi_taker_side_flow`
- `gold_kalshi_calibration_ev_inputs`
- `gold_kalshi_resolution_outcome_inputs`
- `gold_kalshi_cross_platform_matching_inputs`

## 5) Proposed normalized entities and fields (planning-only)

### A) `kalshi_event`

Suggested fields:

- `source_platform`
- `event_ticker_ref`
- `event_title_inferred`
- `market_count_observed`
- `first_market_open_time`
- `last_market_close_time`
- `first_fetched_at`
- `last_fetched_at`
- `event_mapping_status`
- `source_record_hash`
- `parser_version`

### B) `kalshi_market`

Suggested fields:

- `source_platform`
- `ticker_ref`
- `event_ticker_ref`
- `market_type`
- `title`
- `yes_sub_title`
- `no_sub_title`
- `status`
- `result_raw`
- `created_time`
- `open_time`
- `close_time`
- `fetched_at`
- `source_record_hash`
- `parser_version`

### C) `kalshi_outcome`

Suggested fields:

- `source_platform`
- `ticker_ref`
- `event_ticker_ref`
- `outcome_side`
- `outcome_label`
- `result_raw`
- `result_side_normalized`
- `outcome_mapping_status`
- `source_record_hash`
- `parser_version`

### D) `kalshi_market_snapshot`

Suggested fields:

- `source_platform`
- `ticker_ref`
- `event_ticker_ref`
- `fetched_at`
- `yes_bid_raw`
- `yes_ask_raw`
- `no_bid_raw`
- `no_ask_raw`
- `last_price_raw`
- `volume_raw`
- `volume_24h_raw`
- `open_interest_raw`
- `price_scale_status`
- `price_consistency_status`
- `source_record_hash`
- `parser_version`

### E) `kalshi_fill`

Suggested fields:

- `source_platform`
- `trade_ref`
- `ticker_ref`
- `event_ticker_ref`
- `count_raw`
- `yes_price_raw`
- `no_price_raw`
- `taker_side_raw`
- `taker_side_normalized`
- `created_time`
- `fetched_at`
- `yes_no_direction_status`
- `linked_market_status`
- `source_record_hash`
- `parser_version`

### F) `kalshi_result`

Suggested fields:

- `source_platform`
- `ticker_ref`
- `event_ticker_ref`
- `result_raw`
- `result_side_normalized`
- `close_time`
- `fetched_at`
- `result_parse_status`
- `source_record_hash`
- `parser_version`

## 6) Ticker/event mapping strategy

Deterministic planned strategy:

- Treat `ticker_ref` as the primary Kalshi market-level native reference.
- Treat `event_ticker_ref` as the event grouping reference.
- Build market-to-event grouping by `event_ticker_ref`, not title parsing.
- If source `event_ticker` is missing, keep the market row and mark `event_mapping_status = unresolved_event_ref`.
- Link trade/fill rows to market rows by `ticker_ref`.
- If a trade ticker does not map to a known market ticker, preserve the fill row and mark `linked_market_status = unresolved_ticker_ref`.
- Do not drop unresolved rows.
- Do not infer event grouping from title alone.
- Do not infer cross-platform equivalence from ticker alone.

## 7) Yes/no outcome and result normalization

Planned normalization constraints:

- Kalshi markets are binary yes/no style propositions.
- `yes_sub_title` and `no_sub_title` should be preserved as outcome labels when present.
- `yes_bid`, `yes_ask`, `no_bid`, `no_ask`, and `last_price` remain raw until explicit price-scale rules are approved.
- `yes_price` and `no_price` in trade rows remain raw until explicit price-scale rules are approved.
- `result_raw` must be preserved.
- `result_side_normalized` should be assigned only when `result_raw` maps safely under explicit mapping rules.
- If a result cannot be safely mapped, preserve `result_raw` and mark `result_parse_status = unresolved_result`.
- Do not infer final result from price alone.
- Do not infer final result from title/subtitle alone.
- Do not infer result before market resolution/finalization unless a future approved source-status rule allows it.

## 8) Fill/trade direction and taker-side semantics

Planning constraints:

- `trade_id` is the trade-level source reference and maps into `trade_ref`.
- `ticker` links fills to markets through `ticker_ref`.
- `count` is a raw size/count field and needs explicit scale interpretation before economic analysis.
- `yes_price` and `no_price` are raw price fields.
- `taker_side` must be preserved raw before normalization.
- `taker_side_normalized` should use an explicit allowed-value mapping only after observed values are reviewed.
- yes/no direction should be derived only after taker-side and yes/no price semantics are validated.
- Do not classify taker behavior or EV without resolved direction semantics.
- Do not use unresolved taker-side rows for calibration or EV claims.

## 9) Market snapshot and price consistency normalization

Planning constraints:

- Kalshi market rows include snapshot-like fields observed at `_fetched_at`.
- Future normalization should treat `yes_bid`, `yes_ask`, `no_bid`, `no_ask`, `last_price`, `volume`, `volume_24h`, and `open_interest` as market snapshot fields.
- Preserve all raw price/liquidity/count fields.
- Future implementation should validate yes/no complementary relationships where appropriate.
- If yes/no prices appear inconsistent or malformed, preserve the row and flag `price_consistency_status`.
- Do not silently rewrite complementary prices.
- Do not use display/snapshot fields as guaranteed execution prices without later orderbook-specific design.

## 10) Time normalization

Planned time-handling constraints:

- Preserve `created_time`, `open_time`, `close_time`, and `_fetched_at` values from source rows.
- Trade `created_time` and market open/close windows should become comparable after timezone normalization.
- Future normalization should flag trades outside known market open/close windows.
- If timestamps disagree or are missing, preserve raw timestamps and mark `timestamp_status`.
- Do not silently overwrite source timestamps.
- Record source timezone/format assumptions as explicit parser metadata.

## 11) Validation and unresolved-state taxonomy

Planned validation statuses:

- `parsed`
- `unresolved_ticker_ref`
- `unresolved_event_ref`
- `duplicate_trade_ref`
- `duplicate_market_ref`
- `missing_ticker_ref`
- `missing_event_ticker_ref`
- `malformed_yes_price`
- `malformed_no_price`
- `malformed_bid_ask`
- `inconsistent_yes_no_price`
- `missing_taker_side`
- `unsupported_taker_side`
- `unresolved_direction`
- `unresolved_result`
- `unsupported_market_type`
- `missing_open_time`
- `missing_close_time`
- `trade_outside_market_window`
- `timestamp_mismatch`
- `unsupported_market_shape`

## 12) Cross-platform matching implications

Kalshi normalized outputs needed by 0B-20C planning include:

- `ticker_ref`
- `event_ticker_ref`
- `title`
- `yes_sub_title`
- `no_sub_title`
- `market_type`
- `status`
- `result_raw`
- `open_time`
- `close_time`
- yes/no outcome labels
- price/liquidity snapshot fields
- `fetched_at`

Research implications:

- Kalshi title/subtitle/ticker/event-ticker fields support semantic matching against Polymarket question/slug/outcomes.
- Kalshi result and timing fields support calibration/EV research framing.
- Kalshi fill normalization supports market-flow and taker-side analysis.
- Unresolved Kalshi mappings should block cross-platform opportunity claims.
- Cross-platform opportunity labels remain research-only and human-reviewed.

## 13) Future fixture implications

Future tiny fixtures should include:

- `3 to 5` Kalshi market rows with populated ticker/event-ticker/title/subtitle values where possible,
- `3 to 5` Kalshi trade rows where ticker maps to known market rows where possible,
- at least one market row with populated result where available,
- at least one market row with populated open/close time where available,
- at least one trade row with populated taker side where available.

Boundary reminder:

- This document does not approve deriving or committing fixtures.
- Fixture derivation remains dependent on Phase 0B-23 or a later explicit approval.

## 14) Future tests/preflight implications

Planned static/preflight test candidates:

- schema field presence tests for planned normalized entities,
- ticker/event mapping fixture-shape tests,
- yes/no outcome mapping shape tests,
- result-normalization status taxonomy tests,
- taker-side allowed-value guard tests,
- price-consistency status shape tests,
- timestamp window reconciliation shape tests,
- no-auto-drop unresolved row tests,
- no cross-platform opportunity label when ticker/event/result mapping is unresolved.

## 15) Recommended next tickets

Recommended sequence:

- **Phase 0B-23:** approved tiny-fixture derivation script plan; still no fixture commit unless explicitly approved.
- **Phase 0B-24:** cross-platform candidate-pair schema fixture tests, static/preflight only.
- **Phase 0B-25:** semantic-matching rejection-reason taxonomy tests, static/preflight only.
- **Phase 0B-26:** integration/rate-limit/fee source appendix maintenance plan.
- **Phase 1 candidate:** approved local fixture generation and Bronze schema implementation, only after Phase 0B closure.

## 16) Explicit non-approvals

This plan explicitly does not approve:

- data import,
- fixture derivation,
- fixture commit,
- loader implementation,
- query engine,
- connector implementation,
- order placement,
- live trading,
- autonomous execution.

## 17) Static canonical-ID guard

Canonical-ID guard for this document:

- avoid the literal legacy token for historical market routing identifiers,
- prefer `ticker_ref`, `source_market_ref`, native market reference, source market identifier, or legacy market identifier prose,
- if the literal legacy token ever becomes unavoidable in a future edit, update `tests/core/canonical_id_allowlist.py` exactly and narrowly,
- do not increase legacy identifier counts casually.
