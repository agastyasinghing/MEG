# MEG Master PRD

**Polymarket trading and research system**
**Version:** 4.0 (supersedes v3.0)
**Status:** Frozen master spec — child phase docs derive from this
**Owner:** Krishna · Co-owner: Agastya
**Last reviewed:** May 2026

---

## 0. Document purpose and scope

This is the canonical product requirements document for the MEG trading and research system. It supersedes the v3.0 PRD by repositioning v3.0's components (information half-life framework, dynamic TTL decay, contract-design edge taxonomy, cross-market arbitrage, signal versioning) as deliverables for Phases 3-6 rather than the initial build target. The v3.0 architecture is preserved as the destination spec; this PRD is the path that earns the right to build it.

This document specifies what the system does, how it is sequenced, what its data and risk contracts look like, and what each implementation phase must produce before the next begins. It does not contain implementation code. Code-level guidance lives in child documents (`PHASE_0A_SHARED_RAIL.md`, `PHASE_0B_MEG_REPAIR.md`, `WEATHER_STRATEGY_SPEC.md`, `DATA_MODEL.md`, `TESTING_STRATEGY.md`, `AGENTS.md`) that Codex generates from this PRD and implements one ticket at a time.

The intended reader is an implementation agent (Codex or a human engineer) with access to the existing MEG repo and the donor repos referenced below. This PRD assumes familiarity with Polymarket's CLOB V2, the MEG repo structure, and the May 2026 production-readiness audit.

---

## 1. Executive summary

The MEG repository in its current state is an architectural scaffold with a broken spine. The May 2026 audit found that `main.py` does not start a signal-engine worker, `signal_aggregator` is launched without the database session it explicitly requires, `clob_client.place_order()` still raises `NotImplementedError` in live mode, and the Polygon whale parser fabricates market identifiers from transaction hash prefixes. The v3.0 PRD adds architectural sophistication (half-life decay, TTL frameworks, edge taxonomies) on top of a base that has never executed end-to-end. This is the wrong sequencing.

The correct sequencing is rail-first, weather-first, MEG-second. Build a shared Polymarket execution and research rail that any strategy can plug into. Validate that rail by running a tightly scoped weather strategy through it — weather is the cleanest calibration problem on Polymarket because resolution rules are explicit (named airport stations, Weather Underground finalization), data is free (NWS, Open-Meteo, HRRR, GEFS), and the market template repeats daily across dozens of cities. Only after the rail is proven on weather does the MEG whale lead-lag thesis get bolted on as the second strategy module on the same rail.

Three architectural decisions govern the entire system. First, all execution flows through a Telegram operator approval queue; no strategy gets autonomous execution authority in any phase covered by this PRD. Second, historical research lives in a DuckDB-over-Parquet lakehouse seeded by the Jon Becker prediction-market-analysis dataset and extended with the system's own captures; Postgres is used exclusively for operational journaling (proposals, executions, fills, positions, audit). Third, every strategy is a sidecar producing normalized `TradeProposal` objects on a single proposal bus; MEG itself is the control plane, not a strategy.

Capital and timeline assumptions. Starting bankroll is $350. Realistic build timeline is sixteen weeks of part-time effort, accounting for a 1.4-1.7x debugging multiplier on optimistic estimates. The system is designed to make the first live dollar in Phase 2 (weeks 5-7) with tiny per-position sizing, and to keep that strategy running while subsequent phases instrument the whale thesis. Profit maximization at this capital level is principally a function of compounding the validated rail; absolute dollar profit in early phases will be small.

---

## 2. System overview

The MEG system is a paper-and-canary trading platform for Polymarket prediction markets, organized around a control plane (MEG itself) and three execution surfaces (weather strategy, whale lead-lag strategy, and a research lab).

```
                         ┌──────────────────────────────┐
                         │   Operator (Telegram bot)    │
                         └───────────────┬──────────────┘
                                         │ approvals
                                         ▼
 ┌──────────────────────────────────────────────────────────┐
 │                    MEG control plane                     │
 │   pre-filters · risk gates · proposal bus · journal     │
 └────────┬────────────────────┬───────────────────┬────────┘
          │                    │                   │
          ▼                    ▼                   ▼
 ┌──────────────────┐  ┌────────────────┐  ┌────────────────┐
 │ Weather strategy │  │ Whale strategy │  │   Research lab │
 │   (Phase 1-2)    │  │   (Phase 3-5)  │  │  (Phase 0+)    │
 └────────┬─────────┘  └────────┬───────┘  └────────┬───────┘
          │                     │                   │
          ▼                     ▼                   ▼
 ┌─────────────────────────────────────┐  ┌───────────────────┐
 │       Polymarket execution rail     │  │ DuckDB + Parquet  │
 │  CLOB V2 · deposit wallet · POLY_   │  │  research lake    │
 │  1271 · user channel · reconciler   │  │                   │
 └─────────────────────┬───────────────┘  └───────────────────┘
                       │ fills/acks
                       ▼
            ┌─────────────────────┐
            │  Postgres journal   │
            │ proposals · trades  │
            │ positions · audit   │
            └─────────────────────┘
```

The control plane (everything in the MEG repo) owns event contracts, the Redis bus, pre-filter gates, risk controls, the approval queue, the journal, and the heartbeat. Each strategy is a separate module that consumes from upstream Redis channels and produces `TradeProposal` objects. The execution rail is the only path to Polymarket; it is shared across strategies. The research lake is read-only at runtime and write-mostly during offline study sessions.

---

## 3. Goals and non-goals

### 3.1 Goals

The system must produce a Polymarket execution adapter compatible with the CLOB V2 deposit-wallet flow, validated against live canary tests on the actual wallet path the operator intends to use. The adapter must support GTC, GTD, FOK, and FAK order types and must reconcile every order through the authenticated user WebSocket channel.

The system must run a calibrated weather forecasting strategy across a defined city set, generating probabilistic distributions over Polymarket temperature buckets that demonstrably outperform raw model output on Brier score. The weather strategy must trade through the operator approval queue with explicit per-position and per-day risk caps.

The system must run a whale lead-lag strategy that ingests authoritative Polymarket fill events (decoded from on-chain receipts, not heuristics) and produces signal events scored against measured forward returns. The strategy must respect TTL decay calibrated on the system's own historical signal data.

The system must journal every proposal, approval, execution, fill, and position change to Postgres in a form that allows end-to-end reconciliation. The system must run a deterministic replay harness over the DuckDB historical lake that simulates the full proposal-to-resolution path under historical conditions.

The system must enforce a defined risk envelope (per-position cap, daily exposure cap, daily loss limit, drawdown limit) and must halt automatically when limits are breached. The system must emit a structured operational heartbeat suitable for human review.

### 3.2 Non-goals

The system will not perform autonomous live trading without operator approval in any phase covered by this PRD. The system will not implement cross-venue arbitrage (Polymarket-Kalshi) until Phase 6; the pair registry and Kalshi adapter are explicit Phase 6 deliverables only.

The system will not implement a full custom weather machine learning model. The weather forecasting stack uses ensemble post-processing (EMOS or equivalent) over publicly available numerical weather prediction outputs. GraphCast, GenCast, and similar frontier ML weather systems are out of scope.

The system will not implement passive market-making or maker rebate harvesting in any phase covered by this PRD. At $350 capital the inventory and adverse-selection profile of market making is incompatible with the available bankroll.

The system will not implement social-media sentiment scraping, news-feed parsing, or natural-language signal extraction from external sources in any phase covered by this PRD.

The system will not trade on markets with mid prices above 0.85 or below 0.15 except by explicit operator override. Favorite-longshot bias and Kalshi-style research findings indicate poor expected returns for taker fills in these regions.

The system will not operate outside the Polymarket geoblock policy. The operator is responsible for confirming local jurisdictional compliance before any live deployment.

---

## 4. Architecture

### 4.1 Control plane (MEG repo)

The MEG repository hosts the control plane. Its responsibilities are: event contracts and schema definitions, the Redis event bus, pre-filter gates, the risk control layer, the proposal bus, the Telegram approval workflow, the operational journal writers, and the runtime supervisor that starts and supervises every long-running task.

The control plane does not generate signals. Signal generation is delegated to strategy modules (weather, whale) that subscribe to upstream events and publish `TradeProposal` objects to a single normalized proposal channel.

The control plane does not place orders. Order placement is delegated to the execution rail, which is the sole module authorized to interact with Polymarket's CLOB.

### 4.2 Execution rail

The execution rail is a single module that wraps the Polymarket CLOB V2 client and exposes a deliberately narrow interface: `submit_order`, `cancel_order`, `get_position`, and `reconcile_fills`. The rail handles authentication (L1 wallet signing to obtain L2 API credentials), order signing (POLY_1271 with deposit wallet as both maker and signer), acknowledgment correlation, user-channel WebSocket reconciliation, and retry semantics for ambiguous transport failures.

The rail is the only module aware of token IDs, condition IDs, tick sizes, negRisk settings, and Polymarket-specific order parameters. Strategies request fills in terms of `(condition_id, outcome, side, notional, price_constraint)` and the rail handles the translation to venue-native parameters.

### 4.3 Data planes

There are two distinct data planes with non-overlapping responsibilities.

The research lake is DuckDB over Parquet, seeded by the Jon Becker prediction-market-analysis dataset (approximately 36 GiB compressed) and extended over time with the system's own market WebSocket captures, user-channel fill exports, and Polygon receipt-decoded whale fills. The research lake is read-only at runtime; it is written only by offline ingestion jobs. Bronze layer is raw Parquet partitions. Silver layer is normalized views (`poly_trades`, `poly_quotes`, `poly_markets`, `wallet_labels`, `paired_markets`). Gold layer is feature tables generated for strategy research (forward returns, half-life curves, edge taxonomies, wallet cohort labels).

The operational journal is Postgres. It holds the live and paper signal stream, the proposal queue, the execution log, the position book, and the audit trail. The journal does not store raw market data, raw quote streams, raw fill streams, or anything that could be reconstructed from the research lake. The journal is the source of truth for "what did the system do and what did it cost"; the lake is the source of truth for "what would the system have done if it had been running."

### 4.4 Redis event bus

Redis is the in-process event bus for the live system. Channels are:

| Channel | Producer | Consumer | Payload |
|---|---|---|---|
| `raw_whale_trades` | Polygon fill decoder | Pre-filter pipeline | `RawWhaleFill` events |
| `qualified_whale_trades` | Pre-filter pipeline | Whale signal worker | `QualifiedWhaleFill` events |
| `signal_events` | Strategy signal workers | Decision agent | `Signal` events with TTL |
| `trade_proposals` | Decision agent | Telegram bot, dashboard | `TradeProposal` objects |
| `execution_requests` | Telegram approval handler | Execution rail | Approved trades |
| `fills.user` | Polymarket user WebSocket | Reconciler, journal writer | Authoritative fills |
| `bot_alerts` | Any module | Telegram bot | Operator alerts |
| `market:{token_id}:*` | CLOB market-state feed | Pre-filter, execution, monitoring | Bid/ask/spread/liquidity |
| `replay.clock` | Replay harness | All services in test mode | Deterministic time |

Strategy modules subscribe to upstream channels and publish to downstream channels. No module shall write to a channel it does not own per the table above.

### 4.5 Approval plane

Every proposal flows through Telegram. The proposal message contains the signal identifier, the market (condition_id and human-readable slug), the side, the proposed size in pUSD, the model probability, the market probability, the estimated edge, the proposal expiry timestamp, and the strategy of origin. The operator approves, rejects, or defers; defer requeues for re-evaluation by the strategy.

Approved proposals proceed to the execution rail. Expired proposals are dropped and journaled with the elapsed approval latency, which feeds back into the TTL decay measurements in Phase 4.

---

## 5. Canonical data model

### 5.1 Identifier convention

The system uses three identifiers across all event schemas, Redis payloads, and database tables: `condition_id` (hex string identifying the market), `token_id` (numeric string identifying the specific outcome token), and `outcome` (literal "YES" or "NO" derived from token metadata). The legacy `market_id` field is deprecated and removed in Phase 0. Where a human-readable slug is available, `market_slug` is included as an optional field for operator displays only; it is never used for routing or matching.

The reason for this strictness is that Polymarket's order book and order placement are keyed by `tokenID`, not by any generic market identifier. The current MEG code path overloads `market_id` and fabricates values from transaction hash prefixes, which is a hard blocker for both backtesting correctness and execution correctness. Phase 0 removes this overloading entirely.

### 5.2 Event schemas

`RawWhaleFill` is the authoritative decoded fill event produced by the Polygon receipt decoder.

```json
{
  "event_type": "raw_whale_fill",
  "venue": "polymarket",
  "ts_event_ms": 1762819205123,
  "block_number": 73123456,
  "tx_hash": "0x...",
  "condition_id": "0x...",
  "token_id": "12345678901234567890",
  "market_slug": "will-btc-be-above-120k-on-june-30",
  "outcome": "YES",
  "wallet_address": "0xwallet",
  "maker_address": "0xmaker",
  "aggressor_side": "BUY",
  "price": 0.63,
  "size_shares": 720.0,
  "notional_pusd": 453.60,
  "fee_pusd": 0.18,
  "neg_risk": false,
  "source": "polygon_receipt+user_ws"
}
```

`QualifiedWhaleFill` is the same shape with additional fields appended by the pre-filter pipeline: `passed_gates` (list of gate identifiers cleared), `wallet_label` (looked up from `wallet_labels`), `market_quality_score`, and `pre_filter_timestamp_ms`.

`Signal` is the output of any strategy signal worker. It carries strategy-of-origin, score, forward horizon, decay parameters, and an explicit TTL.

```json
{
  "event_type": "signal",
  "signal_id": "uuid",
  "strategy_id": "whale_lead_lag" | "weather_temperature" | ...,
  "ts_emitted_ms": 1762819210000,
  "ts_expires_ms": 1762819510000,
  "condition_id": "0x...",
  "token_id": "12345678901234567890",
  "outcome": "YES",
  "side": "BUY",
  "model_probability": 0.71,
  "score_breakdown": {...},
  "half_life_seconds": 240,
  "metadata": {...}
}
```

`TradeProposal` is the normalized output of the decision agent, suitable for operator approval. It carries the signal it derives from, the proposed order parameters, the risk envelope it consumes, and a human-readable summary string.

`ExecutionRequest` is what the Telegram approval handler emits when a proposal is approved. It carries the proposal identifier, the final approved parameters (which may differ from proposed if the operator modified), and the approval latency.

### 5.3 Postgres operational schema

The operational journal contains five tables. Full DDL lives in `DATA_MODEL.md`; the column inventory is summarized here.

`signal_journal` — every signal emitted by any strategy, with score breakdown, TTL, and downstream proposal linkage. Indexed by `signal_id`, `strategy_id`, `condition_id`, `ts_emitted`.

`proposal_audit` — every proposal created, approved, rejected, deferred, expired, with timestamps for each state transition. Indexed by `proposal_id`, `signal_id`, `state`, `created_at`.

`trade_journal` — every execution attempt, with intended and realized parameters, fees, slippage, state, wallet path, CLOB order ID, trade IDs, and reject reasons where applicable. This is the central reconciliation table. Indexed by `execution_id`, `proposal_id`, `token_id`, `state`, `created_at`, `mode` (replay/paper/live).

`position_lots` — open position tracking by lot, with entry price, current mark, P&L attribution, and exit linkage. Indexed by `condition_id`, `token_id`, `mode`, `closed_at`.

`daily_strategy_stats` — rollup table populated by a nightly job: trades, hit rate, gross P&L, fees, net P&L, max position size, max drawdown, by strategy and date.

A `wallet_registry` table is added in Phase 3 holding wallet labels, cohort assignments, and historical edge measurements by category.

### 5.4 DuckDB research views

The DuckDB lake exposes normalized views over Bronze Parquet partitions:

- `poly_trades` — historical Polymarket fills with canonical identifiers, derived from Becker dataset and own captures
- `poly_quotes_1s` — one-second-aggregated mid prices, bid/ask, and spread, per token
- `poly_markets` — market metadata including resolution rules, category, neg_risk, tick size
- `kalshi_trades` — historical Kalshi fills for cross-venue research (Phase 6 only)
- `wallet_labels` — wallet identifiers with cohort and category-edge labels
- `paired_markets` — registry mapping equivalent markets across venues (Phase 6 only)

Bronze partition layout follows the Becker convention; Phase 0 includes a data dictionary generation step that documents the exact raw schema names before normalization.

---

## 6. Phase roadmap with exit gates

Each phase has a fixed scope, an exit gate (criteria that must be met before the next phase begins), and a kill criterion (a condition under which the phase is abandoned and the plan is revised). Phases do not overlap; the next phase begins when the current phase's exit gate is cleared.

### 6.1 Phase 0 — Correctness foundation (weeks 1-3, ~40h budgeted, realistic 56-68h)

**Scope.** Repair the broken MEG spine and establish the research lake. No strategy work, no new features, no live trading.

**Deliverables.**
1. Polygon receipt decoder: replaces `_filter_whale_transaction` heuristics. Decodes OrderFilled logs against the exchange contract ABI. Extracts authoritative `condition_id`, `token_id`, `outcome`, `aggressor_side`, fill price, share quantity, fee, and block timestamp. Produces `RawWhaleFill` events to `raw_whale_trades`.
2. Canonical identifier migration: all event schemas, Redis payloads, and Postgres tables migrated to `condition_id` + `token_id` + `outcome`. Legacy `market_id` removed.
3. `signal_engine/runner.py`: new module subscribing to `qualified_whale_trades`, scoring with `composite_scorer`, opening per-event DB sessions, writing to `signal_outcomes`, and publishing `Signal` events to `signal_events`. Wired into `main.py` TaskGroup.
4. `signal_aggregator` session fix: replace `session=None` launch path with per-event `async with get_session()` inside the routing loop.
5. CLOB market-state and user-stream services started as first-class long-running tasks in `main.py`, with health checks and staleness alarms exposed via the heartbeat.
6. DuckDB lake initialization: Becker dataset downloaded, extracted, indexed. Data dictionary written documenting raw schema. Bronze-Silver normalization views created for `poly_trades`, `poly_quotes_1s`, `poly_markets`.

**Exit gates.**
- Polygon receipt decoder produces canonical `RawWhaleFill` events for ten known historical Polymarket fills, with all canonical fields matching block-explorer ground truth.
- Sample signal flow demonstrated: a mock `qualified_whale_trade` published to Redis results in a journaled `Signal` event in Postgres within five seconds, with correct DB session lifecycle.
- DuckDB lake queryable: a defined set of seven sanity queries (volume by market, daily fill count, top wallets, spread distribution) return results matching independent block-explorer counts within 2%.
- All Phase 0 unit tests passing (target: 80%+ line coverage on `signal_engine`, `data_layer`, `db`).
- Heartbeat emits successfully every 60 seconds with all health indicators populated.

**Kill criterion.** If the Polygon receipt decoder cannot be verified against ground truth within 60 hours of focused work, escalate. The most likely cause is an ABI mismatch or unfamiliarity with the Polymarket exchange contract event layout; the recovery path is to consult NautilusTrader's Polymarket adapter for reference rather than continuing to debug in isolation.

**Profit state.** Zero. This phase produces no trading activity.

### 6.2 Phase 1 — Weather paper engine (weeks 3-5, ~30h budgeted, realistic 42-51h)

**Scope.** Implement the weather forecasting strategy as the first strategy module on the rail. Paper trading only; every proposal generates a journaled trade with simulated execution against historical book snapshots from the market-state cache.

**Deliverables.**
1. Weather forecast pipeline: pulls GEFS and HRRR ensemble forecasts via Open-Meteo's free tier. Performs station-specific bias correction using historical METAR observations from the past 365 days. Produces calibrated probabilistic distributions over Polymarket temperature buckets.
2. EMOS calibration module: ensemble model output statistics applied to ensemble spread to produce well-calibrated probabilities. Trained on archived forecasts (Open-Meteo archive API) against METAR ground truth.
3. Resolution source registry: a configuration file mapping every traded weather market to its exact resolution source (Weather Underground page, NOAA monthly summary, NWS forecast office), measurement precision, finalization rule, and named station identifier (e.g. KLGA for LaGuardia, KSEA for Seattle-Tacoma).
4. Weather strategy module: subscribes to a weather signal channel produced by the forecast pipeline, evaluates edge against market mid prices, emits `Signal` events when edge thresholds are met.
5. Telegram approval workflow hardening: proposal expiry timer, defer-and-requeue logic, approval-latency tracking, structured proposal message format with all required fields.
6. Trade journal Postgres schema and writers: `trade_journal`, `proposal_audit`, `signal_journal`, `position_lots`, `daily_strategy_stats` tables created and exercised end-to-end in paper mode.
7. Anomaly veto: if observation at a tracked station diverges from forecast ensemble by more than 3°F without atmospheric cause (frontal passage, thunderstorm) in the past 60 minutes, suspend new proposals for that station. Manual reset only.

**Exit gates.**
- Forecast pipeline produces calibrated probability distributions for at least five cities daily, with EMOS-calibrated Brier score at least 5% lower than raw ensemble-count Brier score over a 14-day rolling window.
- At least 50 paper trades journaled end-to-end (proposed → approved/rejected → simulated execution → simulated settlement) with zero unreconciled state.
- Proposal expiry, defer, and rejection paths each exercised at least 10 times with correct journal state transitions.
- Anomaly veto fires correctly on a synthetic test (injected anomalous observation triggers suspension within 60 seconds).
- Paper P&L attribution matches independent recomputation from journal records within 0.1%.

**Kill criterion.** If EMOS-calibrated Brier score exceeds 0.25 across the target city set after Phase 1 deliverables are complete, the model is too miscalibrated to trade with. The recovery path is either (a) station-specific bias correction was insufficient and needs longer training history, or (b) the target cities have intrinsic forecast uncertainty too high for the Polymarket bucket widths. Either response is acceptable; proceeding to Phase 2 with an uncalibrated model is not.

**Profit state.** Zero. Paper only.

### 6.3 Phase 2 — Weather live canary (weeks 5-7, ~25h budgeted, realistic 35-43h)

**Scope.** Transition weather strategy from paper to live. Tiny size, strict caps, full reconciliation. First real dollars.

**Deliverables.**
1. Deposit-wallet execution adapter: implementation of the Polymarket V2 deposit wallet flow per the official `trading/deposit-wallets` and `trading/quickstart` documentation. Deposit wallet created, funded with pUSD, allowances approved from the deposit wallet itself, balance/allowance synced with `signatureType = 3`. All orders place `maker` and `signer` set to the deposit wallet using `POLY_1271` signing.
2. Live canary test suite: a defined sequence of five canary operations (auth handshake, place tiny GTC, cancel tiny GTC, place tiny FOK at unfillable price, place tiny FOK at fillable price) with explicit assertions on every acknowledgment and user-channel reconciliation event. Run before any strategy is enabled in live mode.
3. Reconciliation engine: on every venue event (order ack, partial fill, full fill, rejection, cancellation), update the journal state machine and surface mismatches as alerts.
4. Live risk envelope enforcement: per-position cap, daily exposure cap, daily loss limit, drawdown limit, all enforced at the rail level (the rail refuses to submit orders that breach limits regardless of what the strategy or operator requested).
5. Kill switch: operator command `/halt` immediately cancels all open orders and blocks new submissions until `/resume`. Halt state journaled with timestamp and reason.

**Exit gates.**
- Live canary test suite passes end-to-end with zero unreconciled state across five sequential runs.
- At least 25 live trades executed across at least 4 weeks of live operation, with every trade fully reconciled (proposal → approval → ack → fill → settlement → journal close).
- Net P&L after fees and slippage positive over the 4-week window, OR a written postmortem identifying the specific cause of underperformance and a defined remediation path.
- Anomaly veto fired at least once in live conditions and prevented at least one suspect trade (or, if no anomaly occurred, the synthetic test continues to pass weekly).
- Maximum drawdown over any rolling 7-day window stays within the defined limit.

**Kill criterion.** If net P&L after fees is worse than -$50 over four consecutive weeks of live operation AND no specific model issue has been identified (e.g. calibration error, station-mapping bug, fee miscalculation), pause Phase 2 live trading and run a root-cause analysis before either resuming or pivoting. Continuing to bleed capital while debugging in production is not acceptable at this bankroll level.

**Profit state.** First live dollars. Realistic outcome on $350 over 4 weeks: between -$30 and +$80 net, with the sign of P&L being more informative than the magnitude.

### 6.4 Phase 3 — MEG data layer and lead-lag studies (weeks 7-10, ~35h budgeted, realistic 49-60h)

**Scope.** Build the data and research infrastructure for the whale lead-lag thesis. No live whale trading yet; weather continues running in production.

**Deliverables.**
1. Wallet identifier ingestion: every distinct wallet appearing as taker or maker in the historical fill stream is registered in `wallet_registry` with a stable label, first-seen timestamp, fill count, total notional, and most-active categories.
2. Wallet cohort labeling: cohort assignment by historical pattern — `early_buyer` (consistently enters before price moves), `news_reactor` (concentrated activity around resolution events), `large_taker` (notional > $5000 in single fills), and so on. Cohort definitions live in a versioned configuration file.
3. Lead-lag DuckDB studies: SQL studies of forward returns across 1h, 4h, 12h, and 24h horizons, by wallet cohort, market category, and entry price bucket. Studies include statistical confidence (sample size, standard error, win rate stability across rolling windows).
4. Information half-life framework (first v3.0 element folded in): for each wallet cohort and market category, fit an exponential decay model to forward returns by signal age. Half-life parameters stored in `wallet_registry` and consumed by the whale strategy in Phase 4.
5. Edge survival analysis: for each cohort, compute forward returns net of estimated fees, spreads, and median proposal latency (taken from Phase 1-2 Telegram approval data). Only cohorts with positive net edge survive to Phase 4.

**Exit gates.**
- At least 90 days of historical wallet activity ingested and labeled, with cohort assignments stable across two-week rolling re-labeling (no cohort flips by more than 10% week-to-week).
- Lead-lag SQL studies executed across at least 50 markets in at least 4 categories, with at least one cohort showing forward return signal exceeding twice its standard error.
- Information half-life curves fitted for at least the top three cohorts with R² > 0.4 and a defined plausible decay regime (half-life between 30 minutes and 12 hours).
- Edge survival analysis documents which cohorts retain positive net edge after fees, spreads, and approval latency. The set of surviving cohorts defines the Phase 4 strategy scope.

**Kill criterion.** If no wallet cohort shows positive net edge after fees over the 90-day backtest, the whale lead-lag thesis does not survive contact with reality. The recovery path is to pivot away from the whale strategy and add `live_swing_reversal` (the audit's second-priority strategy) as the second module instead. v3.0's whale-specific components (TTL decay, edge taxonomy in the whale context) would also be deferred indefinitely.

**Profit state.** Weather P&L only.

### 6.5 Phase 4 — MEG whale paper engine (weeks 10-12, ~25h budgeted, realistic 35-43h)

**Scope.** Implement the whale lead-lag strategy as the second module on the rail. Paper trading only.

**Deliverables.**
1. Whale strategy module: subscribes to `qualified_whale_trades`, evaluates against the Phase 3 cohort labels and half-life parameters, emits `Signal` events when conditions are met.
2. Dynamic TTL decay (second v3.0 element folded in): every signal carries a TTL derived from its cohort's measured half-life and the current proposal latency distribution. Decision agent re-scores signals continuously until execution or expiry.
3. Approval latency telemetry: median, 95th-percentile, and worst-case proposal-to-approval latency tracked by hour of day, exposed in heartbeat, used as input to TTL decay calculations.
4. Strategy A/B telemetry: paper P&L tracked independently for weather and whale strategies, with shared cost attribution (slippage models, fee curves).
5. Whale-specific risk gates: no whale signal trades a market with mid > 0.85 or < 0.15 (favorite/longshot exclusion); no whale signal trades a market with spread > 0.04; no whale signal trades a market with under $500 of liquidity within $0.02 of mid.

**Exit gates.**
- At least 30 paper trades from the whale strategy journaled end-to-end with full TTL decay accounting.
- Paper net edge (after simulated fees, spreads, and approval latency) statistically distinguishable from zero across at least three surviving cohorts.
- Dynamic TTL decay demonstrably affects execution decisions (proposals re-scored downward and dropped when stale).
- No whale strategy trade violates the favorite/longshot or spread/liquidity gates.
- Weather strategy continues running in live mode throughout Phase 4 with no degradation in journal reconciliation or risk envelope compliance.

**Kill criterion.** If paper net edge is statistically indistinguishable from zero across all cohorts after 30+ trades, the whale strategy is not viable at this capital level. Pivot to `live_swing_reversal` or extend the data layer for further study.

**Profit state.** Weather live P&L continues; whale strategy paper only.

### 6.6 Phase 5 — MEG whale live canary (weeks 12-16, ~30h budgeted, realistic 42-51h)

**Scope.** Transition whale strategy from paper to live, on top of the now-proven rail. Tiny size scaling toward measured edge.

**Deliverables.**
1. Whale strategy live enablement: gated on the surviving cohort set from Phases 3-4 only. No general whale strategy; only cohorts with statistically validated positive net edge.
2. Contract-design edge taxonomy (third v3.0 element folded in): markets classified by structural properties (binary resolution clarity, oracle vulnerability, liquidity profile, time-to-resolution). Whale signals routed only to taxonomy buckets where the cohort has historical edge.
3. Per-cohort risk caps: per-position cap and daily exposure cap defined per cohort based on measured edge variance, with conservative initial scaling.
4. Two-strategy reconciliation: dashboard or heartbeat view showing weather and whale exposure, P&L, fill quality, and risk envelope utilization side by side.
5. Strategy comparison report: monthly automated report comparing weather vs whale on net P&L, edge capture, drawdown, fill quality, and capital efficiency.

**Exit gates.**
- At least 20 live whale trades executed across at least 4 weeks with full reconciliation.
- Live net edge (after fees) matches paper net edge within 50%, OR a documented postmortem explains the gap.
- Combined weather + whale exposure never exceeds 50% of bankroll across any rolling 24-hour window.
- Contract-design taxonomy routes whale signals correctly (verified: no whale trade outside its cohort's taxonomy bucket).
- Strategy comparison report generated and reviewed at least once.

**Kill criterion.** If live net edge underperforms paper net edge by more than 50% AND the gap cannot be attributed to a fixable rail issue (fee miscalculation, latency spike, missed reconciliation), pause whale live and revert to weather-only operation.

**Profit state.** Weather plus whale, two strategies live.

### 6.7 Phase 6 — v3.0 full rollout (weeks 16+, open scope)

**Scope.** With the rail proven and two strategies in production, the remaining v3.0 elements become legitimate build targets: cross-market arbitrage modules, five-track signal versioning, and additional sidecar strategies. This phase is scoped per-feature; this PRD does not pre-commit to a Phase 6 timeline.

**Candidate deliverables (each independently scoped at Phase 6 kickoff).**
1. Polymarket-Kalshi pair registry and Kalshi adapter (research-only initially, given the audit's caution on cross-venue execution friction at small capital).
2. BTC15m sidecar strategy as a third module on the rail.
3. `live_swing_reversal` as a fourth module on the rail.
4. Five-track signal versioning: A/B/C/D/E versioning of strategy code with shadow comparison and gradual rollout.
5. Capacity analysis: at what capital size does each strategy's edge degrade significantly, and what's the optimal allocation across strategies?

**Phase 6 entry criterion.** Phases 0-5 exit gates all cleared, with weather and whale strategies running in production for at least 8 weeks combined, generating positive net P&L (or a documented and accepted negative-net-P&L learning outcome).

---

## 7. Strategy specifications

### 7.1 Weather temperature strategy (Phase 1-2)

**Market scope.** Daily temperature markets at the following stations, in priority order: KLGA (NYC LaGuardia), KSEA (Seattle-Tacoma), KORD (Chicago O'Hare), KATL (Atlanta Hartsfield), KDEN (Denver), KLAX (Los Angeles), KBOS (Boston), KMIA (Miami), KDFW (Dallas-Fort Worth), KPHX (Phoenix). The resolution source registry maps each market explicitly; markets that resolve on different stations (e.g. central park vs LaGuardia for NYC) are tracked as separate entries.

**Forecast inputs.** GEFS (Global Ensemble Forecast System, 30 members at 0.5° resolution, 6h cadence) and HRRR (High-Resolution Rapid Refresh, 3km resolution, 1h cadence for the US) via Open-Meteo's free tier. Open-Meteo's archive API used for training-period historical forecasts. METAR observations from each station pulled directly from NWS for ground truth and bias correction.

**Signal generation.**
1. At each forecast refresh, pull the latest ensemble for the target station and forecast horizon.
2. Apply station-specific bias correction trained on 365-day rolling METAR ground truth.
3. Apply EMOS calibration to produce a probability density over a 1°F-resolution temperature grid.
4. Integrate the density over each Polymarket bucket to produce bucket probabilities.
5. Compare to current market mid prices.

**Entry conditions.** Trade only when all of:
- |model_p - market_p| > 0.08 in the target bucket
- model_p in the target bucket > 0.20 (avoid longshots)
- market liquidity > $1000 within $0.02 of mid in the target bucket
- time-to-resolution < 18 hours (avoid extended capital lockup)
- market_p in (0.15, 0.85) (avoid favorite/longshot bias zones)
- anomaly veto not active for this station

**Sizing.** Kelly fraction times 0.25 (quarter-Kelly) on the modeled edge, capped at $20 per position in Phase 2. Sizing is recomputed every minute on resting orders; if the modeled edge falls below 0.04 after entry, exit at next available price.

**Exit conditions.** Hold to resolution OR exit if model probability moves against the position by more than 0.10 from entry OR exit if anomaly veto fires for the relevant station.

**Resolution source registry entry (example).**
```yaml
market: "highest-temperature-in-nyc-on-may-18-2026"
condition_id: "0x..."
buckets:
  - {label: "60-64", token_id: "...", lower: 60, upper: 64}
  - {label: "65-69", token_id: "...", lower: 65, upper: 69}
  - ...
station: "KLGA"
station_name: "LaGuardia Airport"
resolution_source: "wunderground"
resolution_url_pattern: "https://www.wunderground.com/history/daily/us/ny/new-york-city/KLGA/date/{date}"
measurement: "highest_temperature_fahrenheit"
precision: 1
finalization_rule: "first_finalized_value_after_resolution_date"
revisions_policy: "ignored_after_finalization"
```

### 7.2 Whale lead-lag strategy (Phase 4-5)

**Definition of whale.** Cohort-dependent. The whale definition is not a single threshold but a label assigned by `wallet_registry` based on observed historical behavior. The general filter for `qualified_whale_trade` admission is a single fill with notional > $500 OR cumulative 7-day notional > $5000 from a wallet with at least 30 days of activity.

**Signal generation.**
1. On every `RawWhaleFill`, look up `wallet_label` in `wallet_registry`.
2. If wallet is in a surviving cohort (Phase 3 output), look up the cohort's measured half-life and category-edge mapping.
3. If the market category is one where this cohort has positive historical edge, emit a `Signal` event with TTL = 1.5 × half-life.
4. Score the signal using the composite scorer (whale recency, fill notional relative to wallet history, market category fit, price entry quality).

**Entry conditions.** Trade only when all of:
- signal score above defined threshold (cohort-specific, validated in Phase 4 paper)
- signal age < 1.5 × half-life at decision time
- market_p in (0.15, 0.85)
- market spread < 0.04
- market liquidity > $500 within $0.02 of mid
- no existing position in the same condition_id

**Sizing.** $10-30 per position in Phase 5 initial deployment, scaling with measured cohort edge variance.

**Exit conditions.** Hold to resolution OR exit if mark moves against position by 0.08 from entry OR exit at half-life-derived stop-time (default 4 hours from entry, cohort-specific).

### 7.3 Future strategies (Phase 6+)

`live_swing_reversal`, `btc15m_sidecar`, and `polymarket_kalshi_arb` are documented in their own specification files at Phase 6 kickoff. They share the same rail, proposal bus, journal, and risk envelope as weather and whale.

---

## 8. Polymarket venue specifics

### 8.1 CLOB V2 and deposit wallet flow

The system targets Polymarket's production CLOB V2 endpoint. The integration uses the deposit wallet authentication pattern documented in the official `trading/deposit-wallets` and `trading/quickstart` guides as of May 2026.

The deposit wallet is a proxy contract owned by the operator's externally owned account (EOA). It holds pUSD, executes approvals, and signs orders under the `POLY_1271` flow. Critically, both `maker` and `signer` fields on every order must be set to the deposit wallet address. `signatureType` is `3` for balance and allowance sync calls.

Authentication is a two-level model. Level 1 (L1) is a one-time EIP-712 signature from the EOA to derive Level 2 (L2) API credentials. The L2 credentials are then included as `POLY_*` HTTP headers on every trading endpoint request. Public market data endpoints require no authentication.

The system holds L2 credentials in environment variables only, never in committed configuration. L2 credentials are rotated on operator command via a defined rotation procedure.

### 8.2 Order types and parameters

The system uses GTC (Good-Til-Cancelled) for resting taker orders that we intend to leave on the book, GTD (Good-Til-Date) for time-bounded resting orders, FOK (Fill-Or-Kill) for aggressive immediate fills with no partial acceptance, and FAK (Fill-And-Kill) for aggressive immediate fills with partial acceptance allowed.

Every order specifies `tokenID`, `side` (BUY or SELL), `size`, `price`, and `orderType`. The execution rail is responsible for translating strategy intent ("BUY $15 of YES in market X at no worse than 0.65") into venue-native parameters including correct tick size rounding and negRisk market handling.

The system does not place orders on negRisk markets in Phase 0-5 unless explicitly enabled per-market in the resolution source registry. NegRisk markets have different execution semantics (constrained spreads, automatic re-pricing) that require additional rail logic.

### 8.3 Fee mechanics

Polymarket charges takers a protocol fee using the formula `fee = collateral × feeRate × p × (1 − p)`, where `feeRate` is category-specific and `p` is the order's executed price. Makers pay zero protocol fee. For weather markets the `feeRate` is 0.05.

Fee implications for strategy:
- The fee is highest near the 0.5 midpoint, which is exactly where many tradeable signals sit. A 100-share weather trade at 0.50 incurs $1.25 in protocol fee against $50 notional, or 2.5%. Edge thresholds must be set with this in mind.
- The maker rebate program redistributes 25% of fee-enabled weather taker fees daily to makers. The system is not a maker in Phase 0-5; this is informational only.
- All strategy edge calculations include the realized fee, not a fee-free expected return. The pre-filter pipeline rejects proposals whose modeled edge does not exceed (estimated fee + estimated half-spread + a defined safety buffer).

### 8.4 Market data sources

Public market data comes from three layers: the Gamma API for market discovery and metadata, the CLOB REST endpoints for order books and historical prices, and the public market WebSocket for streaming order-book and trade events. None of these require authentication.

Authenticated data (user fills, account state) comes from the user WebSocket channel. This is the source of truth for fill confirmation; the system does not trust order acknowledgments alone for position tracking.

The CLOB market-state cache writer (Phase 0 deliverable) subscribes to a watch list of active markets in `meg:active_markets` Redis key and continuously publishes bid/ask/spread/liquidity/volume/category/last-update fields to `market:{token_id}:*` keys. Pre-filter and execution modules read from this cache rather than calling the REST API directly.

### 8.5 Resolution and the UMA Optimistic Oracle

Polymarket resolves markets via the UMA Optimistic Oracle. The proposer posts a bond (currently $750 pUSD), there is a 2-hour challenge period, and disputes escalate to UMA's Data Verification Mechanism. Winning tokens redeem 1:1 against pUSD; losing tokens go to zero.

The system does not interact with the resolution process directly; positions are held until tokens resolve, and the journal is updated when the user channel reports token redemption. The system does not attempt to participate in dispute or proposal activity.

### 8.6 Geoblock and legal posture

The Polymarket geoblock policy is enforced by the venue. The system does not attempt to bypass it (VPN use is explicitly prohibited by venue terms). The operator confirms local jurisdictional compliance before any live deployment; this PRD makes no claim about the legal status of trading on Polymarket in any specific jurisdiction.

---

## 9. Risk controls

### 9.1 Position and exposure limits

| Limit | Phase 2 value | Phase 5 value | Enforcement |
|---|---|---|---|
| Per-position cap | $20 | $30 | Execution rail refuses orders exceeding cap |
| Per-strategy daily exposure | $50 | $80 | Strategy module respects allocation |
| Total daily exposure | $70 | $150 | Pre-filter checks cumulative open exposure |
| Daily loss limit (kill switch) | $30 | $50 | Halt all new orders on breach |
| Rolling 7-day drawdown limit | 8% of bankroll | 8% of bankroll | Halt and require operator review |
| Single-market concentration | 30% of bankroll | 30% of bankroll | Pre-filter rejection |

Limits are enforced at the rail level, meaning the execution rail will refuse to submit an order that would breach them regardless of what any upstream module requested. This is intentional: it makes risk a guarantee of the rail, not a contract that each strategy must independently honor.

### 9.2 Market and execution gates

The pre-filter pipeline rejects proposals that fail any of:
- Market liquidity within $0.02 of mid is below the strategy's defined floor.
- Market spread exceeds the strategy's defined ceiling.
- Market mid is outside (0.15, 0.85) unless the strategy explicitly allows extremes.
- Market state cache is stale (last update > 30 seconds ago).
- Market resolution date is within 30 minutes (avoid race conditions with resolution).

### 9.3 Anomaly veto (weather-specific)

For weather strategy, an independent anomaly monitor watches each tracked station's METAR observations. If observed temperature diverges from the ensemble forecast by more than 3°F over the past 60 minutes without correspondence to documented atmospheric events (frontal passage, thunderstorm log entry), the veto fires for that station. Vetoed stations stop generating new proposals; existing positions are held to resolution unless manual override.

The Paris CDG sensor incident in April 2026 is the proximate cause of this control. A weather strategy with an automated veto would have refused to enter the affected markets.

### 9.4 Approval workflow gates

Every proposal expires within 5 minutes by default; the strategy may specify shorter expiries. Expired proposals are dropped, not auto-approved. Operator approval latency is journaled per proposal and used to recalibrate TTL decay parameters in Phase 4.

The operator has explicit halt and resume commands via Telegram. Halt cancels all open orders and blocks new submissions until resume. Halt events are journaled with timestamp and operator-provided reason.

### 9.5 Reconciliation guarantees

Every order submitted to the venue must reach one of four terminal states in the journal: filled, partially filled and closed out, cancelled, or rejected. Orders that remain in `posted` state for more than 60 seconds without venue acknowledgment trigger a reconciliation alert.

The end-of-session reconciliation job (run nightly) compares the journal's open position book against the user channel's reported balances. Any discrepancy is surfaced as a high-priority alert and blocks the next session's startup until resolved.

---

## 10. Testing strategy

The system uses five testing tiers, in order of cost and confidence.

### 10.1 Unit tests

Every module exposes a unit test suite covering its pure logic. Target line coverage: 80% on `signal_engine`, `data_layer`, `db`, `pre_filter`; 90% on `execution` and `risk` modules. Unit tests run on every commit via CI.

### 10.2 Contract tests

Contract tests validate the system's behavior against official venue semantics. For Polymarket: identifier handling (token_id and condition_id parsed and round-tripped correctly), fee calculation (matches published formula across price/size grid), order parameter validation (tick size, negRisk, signatureType correctly set per market), WebSocket event parsing (all documented event types correctly deserialized).

Contract tests are run before any phase exit gate.

### 10.3 Replay tests

The replay harness drives the full pipeline (pre-filter → signal → decision → proposal → simulated execution → journal) against historical data from the DuckDB lake. Replay runs are deterministic: same input data and same configuration produce identical journal output. The replay clock advances by event timestamp, not wall-clock.

Replay tests are run for each strategy across at least three fixed historical windows: a high-volatility week, a low-volatility week, and a resolution-event week.

### 10.4 Paper trading shadow

In paper mode, every signal generates a journaled proposal that flows through the full approval and execution pipeline, but the execution rail simulates orders against historical book snapshots from the market-state cache. Paper trading runs continuously alongside live trading once Phase 2 ships, providing a continuous A/B between live and counterfactual paper P&L.

Paper trades are journaled with `mode = "paper"` and are excluded from live P&L reports but included in strategy A/B comparisons.

### 10.5 Live canary

Live canary tests are scoped to specific high-risk integration points: deposit-wallet auth, order submission, fill reconciliation, and order cancellation. The canary suite uses tiny sizes (5 shares, ~$3 notional) and predefined markets known to be active. Canary runs are mandatory before any phase enables live execution.

Canary tests are not run continuously in production; they are pre-deployment gates.

---

## 11. Operational runbook

### 11.1 Heartbeat

The system emits a structured heartbeat to Telegram every 5 minutes during active hours and on every strategy state change. The heartbeat format is:

```
MEG heartbeat | YYYY-MM-DD HH:MM UTC
Mode: paper | live | mixed | halted
Approval-first: ON | OFF
Paused: NO | YES (reason)

Signals (last 60m): N raw -> N qualified -> N proposed -> N approved -> N filled
Top strategy: <strategy_id> | Net PnL today: $XX.XX | Open exposure: $XX.XX / $cap

Latency:
  detect p50/p95 = X.XXs / X.XXs
  proposal->approval p50/p95 = XXs / XXs
  submit->ack p50/p95 = X.XXs / X.XXs

Health:
  poly market ws OK | poly user ws OK | gamma OK | redis OK | postgres OK | replay lag 0s

Guardrails:
  max drawdown X.X% | slippage p95 XX bps | stale market cache N | rejected orders N
```

A heartbeat with any health indicator in non-OK state escalates to a priority alert.

### 11.2 Daily reconciliation

A nightly job runs at 04:00 UTC and:
1. Pulls all fills from the user channel for the past 24 hours.
2. Compares against journal records.
3. Reports any discrepancies, missing entries, or state inconsistencies.
4. Computes the `daily_strategy_stats` rollup.
5. Emits a daily summary to Telegram.

If the reconciliation job finds any discrepancy, the next session's startup is blocked until the operator acknowledges the report.

### 11.3 Halt and resume

The operator can issue `/halt <reason>` via Telegram at any time. Halt cancels all open orders, blocks new submissions, and journals the event. The operator issues `/resume` to lift the halt; resume requires a typed confirmation.

Automatic halts trigger on: daily loss limit breach, drawdown limit breach, reconciliation error, or stale market cache exceeding 5 minutes.

### 11.4 Incident response

For any unreconciled state, the operator's first action is `/halt` and the second action is to run the reconciliation job manually. The runbook for common incidents lives in `OPERATIONS.md` (Phase 0 deliverable).

---

## 12. Implementation ticket structure

Tickets are ordered by phase. Each ticket has a priority (P0 = blocking, P1 = required for phase exit, P2 = nice-to-have within phase), an effort estimate (in hours of focused work), a defined acceptance criterion, and an explicit dependency list.

Acceptance criteria are written in the form "when X is true, the ticket is done." Codex must verify acceptance before requesting review.

### 12.1 Phase 0 tickets

| # | Priority | Ticket | Effort | Dependencies | Acceptance |
|---|---|---|---|---|---|
| 1 | P0 | Polygon receipt decoder | 12h | None | 10 known historical fills decoded with all canonical fields matching block-explorer ground truth |
| 2 | P0 | Canonical identifier migration | 8h | 1 | All event schemas, Redis payloads, Postgres tables use `condition_id` + `token_id` + `outcome`; legacy `market_id` removed |
| 3 | P0 | `signal_engine/runner.py` | 6h | 2 | Module subscribes to `qualified_whale_trades`, scores with `composite_scorer`, publishes to `signal_events`; wired into `main.py` TaskGroup |
| 4 | P0 | `signal_aggregator` session fix | 4h | 2 | Replace `session=None` launch path with per-event `async with get_session()` |
| 5 | P0 | CLOB market-state and user-stream services | 8h | 2 | Both services start in `main.py` as long-running tasks with health checks and staleness alarms |
| 6 | P0 | DuckDB lake setup and Becker normalization | 12h | None | Becker dataset extracted; `poly_trades`, `poly_quotes_1s`, `poly_markets` views queryable; seven sanity queries match block-explorer counts within 2% |
| 7 | P1 | Phase 0 unit test pass | 4h | 1-6 | 80% line coverage on `signal_engine`, `data_layer`, `db` |
| 8 | P1 | Heartbeat emitter | 4h | 5 | Heartbeat publishes every 60s with all health indicators populated |

Phase 0 total budget: 58h. Realistic estimate with 1.4x debug multiplier: 81h.

### 12.2 Phase 1 tickets

| # | Priority | Ticket | Effort | Dependencies | Acceptance |
|---|---|---|---|---|---|
| 9 | P0 | Weather forecast pipeline | 15h | 6 | GEFS + HRRR pulled via Open-Meteo; station-specific bias correction over 365-day METAR history; produces probability density over temperature buckets |
| 10 | P0 | EMOS calibration module | 10h | 9 | Calibrated Brier score at least 5% lower than raw ensemble Brier over 14-day rolling window |
| 11 | P0 | Resolution source registry | 6h | 2 | YAML registry covers 10 cities with station, source URL pattern, measurement, precision, finalization rule |
| 12 | P0 | Weather strategy module | 12h | 9-11 | Emits `Signal` events meeting all defined entry conditions |
| 13 | P0 | Telegram approval workflow hardening | 8h | 3 | Proposal expiry, defer/requeue, approval-latency tracking all working with journal records |
| 14 | P0 | Trade journal Postgres schema and writers | 8h | 4 | All five tables created; end-to-end paper trade journaled with zero unreconciled state |
| 15 | P1 | Anomaly veto | 6h | 11 | Synthetic test (injected anomalous observation) triggers suspension within 60s |

Phase 1 total budget: 65h. Realistic estimate: 91h.

### 12.3 Phase 2 tickets

| # | Priority | Ticket | Effort | Dependencies | Acceptance |
|---|---|---|---|---|---|
| 16 | P0 | Deposit-wallet execution adapter | 16h | 14 | Deposit wallet created, funded, allowances approved; all orders use deposit wallet as maker and signer with POLY_1271 |
| 17 | P0 | Live canary test suite | 10h | 16 | Five canary operations pass with full reconciliation across five sequential runs |
| 18 | P0 | Reconciliation engine | 8h | 16 | Every venue event updates journal state; mismatches surface as alerts |
| 19 | P0 | Live risk envelope enforcement | 6h | 14 | All risk limits enforced at rail level; orders exceeding limits refused |
| 20 | P0 | Kill switch (`/halt`, `/resume`) | 4h | 13 | Halt cancels open orders and blocks submissions until resume; events journaled |

Phase 2 total budget: 44h. Realistic estimate: 62h.

### 12.4 Phase 3 tickets

| # | Priority | Ticket | Effort | Dependencies | Acceptance |
|---|---|---|---|---|---|
| 21 | P0 | `wallet_registry` Postgres table and ingestion | 6h | 6 | Every distinct wallet from past 90 days registered with stable label, first-seen, fill count, total notional |
| 22 | P0 | Wallet cohort labeling | 8h | 21 | Cohort definitions versioned; cohort assignments stable across two-week rolling re-labeling |
| 23 | P0 | Lead-lag DuckDB studies | 14h | 22 | Studies executed across 50+ markets in 4+ categories; at least one cohort shows signal > 2× standard error |
| 24 | P1 | Information half-life framework | 10h | 23 | Half-life curves fitted for top three cohorts with R² > 0.4 and plausible decay regime |
| 25 | P1 | Edge survival analysis | 6h | 23-24 | Per-cohort net edge after fees, spreads, latency documented; surviving cohort set defined |

Phase 3 total budget: 44h. Realistic estimate: 62h.

### 12.5 Phase 4 tickets

| # | Priority | Ticket | Effort | Dependencies | Acceptance |
|---|---|---|---|---|---|
| 26 | P0 | Whale strategy module | 12h | 24-25 | Subscribes to `qualified_whale_trades`, scores against cohort+half-life, emits `Signal` events meeting entry conditions |
| 27 | P0 | Dynamic TTL decay | 8h | 24 | Every signal carries TTL derived from cohort half-life and proposal latency; decision agent re-scores continuously |
| 28 | P0 | Approval latency telemetry | 4h | 13 | Median, p95, worst-case latency tracked by hour of day; exposed in heartbeat |
| 29 | P1 | Strategy A/B telemetry | 6h | 14 | Paper P&L tracked independently per strategy with shared cost attribution |
| 30 | P1 | Whale-specific risk gates | 4h | 19 | Favorite/longshot, spread, liquidity gates enforced at pre-filter level |

Phase 4 total budget: 34h. Realistic estimate: 48h.

### 12.6 Phase 5 tickets

| # | Priority | Ticket | Effort | Dependencies | Acceptance |
|---|---|---|---|---|---|
| 31 | P0 | Whale strategy live enablement | 6h | 17, 26 | Live whale trading gated on surviving cohort set only |
| 32 | P0 | Contract-design edge taxonomy | 8h | 23 | Markets classified by binary clarity, oracle vulnerability, liquidity profile, time-to-resolution; whale signals routed only to taxonomy buckets where cohort has edge |
| 33 | P0 | Per-cohort risk caps | 4h | 19, 32 | Caps defined per cohort based on edge variance |
| 34 | P1 | Two-strategy reconciliation view | 6h | 29 | Dashboard or heartbeat shows weather + whale exposure, P&L, fill quality, risk envelope side by side |
| 35 | P1 | Strategy comparison report | 6h | 34 | Monthly automated report covering net P&L, edge capture, drawdown, fill quality, capital efficiency |

Phase 5 total budget: 30h. Realistic estimate: 42h.

### 12.7 Phase 6 tickets

Phase 6 tickets are not enumerated in this PRD. Each Phase 6 deliverable (Polymarket-Kalshi pair registry, BTC15m sidecar, `live_swing_reversal`, signal versioning, capacity analysis) is scoped in its own specification at Phase 6 kickoff, after Phase 5 exit gates clear.

---

## 13. Known risks and failure modes

### 13.1 Thesis risk

The whale lead-lag thesis may not survive contact with reality. Phase 3's edge survival analysis is explicitly designed to detect this; if no cohort retains positive net edge after fees, the kill criterion fires and the system pivots to `live_swing_reversal` as the second strategy. This is not a failure of the system; it is the system functioning as intended.

The weather thesis is more robust (information is cleaner, data is free, resolution is precise) but is not risk-free. Calibration drift, oracle source changes, or category-wide liquidity collapse on Polymarket would all impair it.

### 13.2 Operational risk

The Polymarket V2 Python client has open issues around deposit-wallet flows (maker address not allowed, signer/funder mismatches, phantom fills) as of May 2026. The execution rail isolates these by maintaining a thin adapter that can be replaced if the upstream client's behavior changes. Live canary tests are mandatory before any phase enables live execution precisely because upstream behavior is volatile.

Unreconciled state is the most dangerous operational failure mode. The system's defense is daily reconciliation with hard startup blocks on discrepancy.

### 13.3 Capital risk

At $350 bankroll, the system has no room for catastrophic execution errors. The risk envelope is calibrated for this bankroll. If capital changes, the envelope is re-derived; it does not auto-scale.

The execution rail enforces limits independently of strategy code, so a strategy bug cannot bypass risk caps. This is structural, not a discipline question.

### 13.4 Oracle source manipulation

The Paris CDG temperature sensor incident in April 2026 demonstrates that physical-sensor-resolved markets carry oracle vulnerability. The weather strategy's anomaly veto is a partial defense. The more general defense is to avoid trading large positions on any single-source-resolved market when the market has recently exhibited anomalous activity.

For whale strategy, the analog risk is wallet-cohort manipulation: an adversary could spoof "whale" activity to draw signals. The defense is cohort labeling stability (a wallet must demonstrate consistent behavior over 30+ days before being labeled) and the per-cohort risk caps.

### 13.5 Legal and jurisdictional risk

The system makes no claim about the legality of Polymarket trading in any specific jurisdiction. The operator is solely responsible for jurisdictional compliance, KYC/AML, and tax treatment. The system does not facilitate or encourage bypass of the venue's geoblock policy.

### 13.6 Build sequence risk

The most common sequence failure mode is "scope creep into v3.0." If during Phase 1-2 the team starts implementing v3.0 elements (half-life, TTL decay, edge taxonomy) before their dependencies exist, the system reverts to the pre-audit state of architectural sophistication without working execution. Phase exit gates are the structural defense; the cultural defense is treating this PRD as frozen and resisting elaboration until Phase 5 ships.

---

## 14. Glossary

**Aggressor side.** The side of a fill that crossed the spread to initiate the trade. The aggressor pays the protocol fee.

**Approval-first.** A workflow constraint in which every order requires explicit operator approval through Telegram before submission to the venue.

**Becker dataset.** Jon Becker's `prediction-market-analysis` repository, a pre-collected ~36 GiB Parquet archive of historical Polymarket and Kalshi data used as the seed for the research lake.

**Bronze / Silver / Gold.** Lakehouse data tiers. Bronze is raw immutable Parquet, Silver is normalized cleaned views, Gold is feature-engineered tables for strategy research.

**Canary.** A tiny live-mode test sequence used to validate an execution path before allowing strategy traffic. Canaries use minimal size (5 shares) and predefined markets.

**Composite scorer.** The whale signal scoring function combining whale recency, fill notional, market category fit, and entry price quality into a single score.

**Condition ID.** The Polymarket identifier for a market. A market has one condition_id and typically two token_ids (one for YES, one for NO).

**Contract-design edge taxonomy.** A classification of markets by structural properties (binary clarity, oracle vulnerability, liquidity profile, time-to-resolution) used to route strategy signals to favorable bucket types. v3.0 PRD origin; folded in at Phase 5.

**Deposit wallet.** A Polygon proxy contract owned by the operator's EOA that holds pUSD, executes approvals, and signs orders under POLY_1271. Required by Polymarket's current API user flow.

**EMOS.** Ensemble Model Output Statistics. A meteorological post-processing technique that calibrates ensemble forecast spread into well-calibrated probabilistic distributions.

**Half-life.** The time over which a signal's expected forward return decays by 50%. v3.0 PRD origin; folded in at Phase 3.

**Kelly fraction.** The capital fraction maximizing expected log-wealth given an estimated edge and odds. The system uses 0.25 × Kelly (quarter-Kelly) as the default sizing to reduce variance.

**Maker / taker.** A maker posts a resting order on the book; a taker crosses the spread to fill against a resting order. Polymarket charges takers a protocol fee and pays makers zero protocol fee plus daily rebates.

**NegRisk.** A Polymarket market type with constrained spreads and automatic re-pricing. Out of scope for Phase 0-5.

**Operator.** The human in the loop who approves or rejects proposals via Telegram. In current scope: Krishna.

**POLY_1271.** Polymarket's deposit-wallet signing scheme conforming to EIP-1271 for smart-contract wallet signatures.

**Proposal.** A structured object representing the system's intent to place a specific order, awaiting operator approval. See `TradeProposal` schema.

**Quarter-Kelly.** See Kelly fraction.

**Rail.** The shared execution infrastructure (control plane + execution adapter + journal + risk envelope) that any strategy plugs into. Strategies are sidecars; the rail is the constant.

**Signal.** A scored, time-bounded prediction emitted by a strategy module. Signals are consumed by the decision agent to produce proposals.

**TTL.** Time-to-live. The maximum age a signal can have before it is considered stale and discarded. In Phase 4, TTL is cohort-specific and derived from measured half-life.

**Token ID.** The Polymarket identifier for a specific outcome token within a market. Order placement is keyed by token_id.

**Wallet cohort.** A group of wallets sharing observed behavioral patterns (early_buyer, news_reactor, large_taker, etc.) used as the unit of analysis for whale strategy.

---

## 15. Child documents derived from this PRD

This master PRD is intended to be split into the following child documents for Codex implementation:

- `PHASE_0A_SHARED_RAIL.md` — Phase 0 deliverables 1-8: receipt decoder, identifiers, signal runner, session fix, CLOB services, heartbeat
- `PHASE_0B_MEG_REPAIR.md` — Phase 0 deliverable 6 specifically: DuckDB lake setup and Becker normalization
- `WEATHER_STRATEGY_SPEC.md` — Phase 1 deliverables: forecast pipeline, EMOS calibration, resolution registry, weather strategy module, anomaly veto
- `EXECUTION_RAIL_SPEC.md` — Phase 2 deliverables: deposit-wallet adapter, canary suite, reconciliation engine, risk enforcement, kill switch
- `WHALE_STRATEGY_SPEC.md` — Phase 3-5 deliverables: wallet registry, cohort labeling, lead-lag studies, half-life framework, dynamic TTL, whale strategy module
- `DATA_MODEL.md` — Full DDL for Postgres tables, full schema for DuckDB views, all event payload definitions
- `TESTING_STRATEGY.md` — Full unit/contract/replay/paper/canary test specifications
- `OPERATIONS.md` — Runbook for heartbeat, reconciliation, halt/resume, incident response
- `AGENTS.md` — Codex implementation conventions, ticket workflow, review cadence, commit and branching rules

Each child document references this master PRD as its source of truth. Conflicts between a child document and this PRD are resolved in favor of this PRD until the master is explicitly revised.

---

## 16. Revision policy

This master PRD is frozen at v4.0 as of May 2026. Revisions require:
1. A documented reason for change.
2. An assessment of which child documents are affected.
3. An explicit version bump.
4. A diff committed to the repo.

Bug fixes and clarifications during phase implementation are not revisions and do not require version bumps; they go in the child documents.

The most likely sources of legitimate future revision are: Polymarket V2 client behavior changes that affect the execution rail, Becker dataset schema changes that affect the research lake, and Phase 3 kill criterion firing (which would trigger a substantive replan of Phases 4-6).

End of master PRD.
