# MEG — Deferred TODOs

Items considered during planning and explicitly deferred. Each entry has enough
context to be picked up without re-reading the original planning session.

---

## [P1] Live order placement auth in clob_client

**What:** Implement `_get_clob_client()` in `meg/data_layer/clob_client.py` with real
py-clob-client authentication (API key + private key from env / AWS Secrets Manager).

**Why:** `place_order(paper_trading=False)` currently raises `NotImplementedError`.
This is the final blocker before MEG can submit any live order to the Polymarket CLOB.

**Pros:** Unblocks live trading. The lazy initializer hook (`_get_clob_client()`) is
already the designed extension point in the module.

**Cons:** Cannot be done until OQ-05 (private key custody) is resolved. Rushing this
risks storing private keys insecurely.

**Context:** `clob_client.place_order()` checks `config.risk.paper_trading` first — if
`True`, the paper path is taken and this code never runs. The live path raises
`NotImplementedError` with a message pointing here. To implement:
(1) Confirm Polymarket CLOB auth flow from py-clob-client docs (API key + L1/L2 key pair),
(2) Read credentials from env vars (never from config.yaml),
(3) Implement `_get_clob_client()` as a module-level lazy singleton,
(4) Wire it into `place_order()`, `cancel_order()`, `get_open_orders()`, `get_position()`.
See py-clob-client README for auth patterns.

**Effort:** S–M
**Priority:** P1
**Blocked by:** OQ-05 (private key custody decision), AWS Secrets Manager setup

---

## [P2] Limit→market order timeout conversion in order_router

**What:** Implement limit order timeout in `order_router.place()`: after
`config.entry.limit_timeout_seconds`, cancel the unfilled limit order and re-place
as an aggressive taker order (limit price at current ask for BUY, current bid for SELL).

**Why:** Unfilled limit orders leave capital allocated but undeployed, and the signal
edge may have already decayed by the time the limit fills (if it ever does). Forcing
a taker fill within the timeout window ensures execution happens while the signal is fresh.

**Pros:** Guarantees execution within `limit_timeout_seconds`. Reduces stranded capital.
The config param (`limit_timeout_seconds: 30`) is already wired and hot-reloadable.

**Cons:** Requires fill detection — polling `get_open_orders()` or a CLOB websocket.
Both are currently `NotImplementedError` stubs. Taker pricing needs careful definition
for Polymarket's binary market structure (buy at ask = aggressive fill).

**Context:** `config.entry.limit_timeout_seconds` is already in `EntryConfig` (added
Phase 7). A TODO comment in `order_router._place_with_retry()` marks the extension point.
To implement: (1) after `place_order()` returns an order_id, start an asyncio.Task that
polls `get_open_orders()` every 5s up to `limit_timeout_seconds`, (2) if still open,
`cancel_order()` + `place_order()` at aggressive price, (3) update position entry_price
with actual fill price. See `handle_fill()` stub in order_router.py.

**Effort:** M
**Priority:** P2
**Blocked by:** `handle_fill()` + `get_open_orders()` live mode (both `NotImplementedError`)

---

## [P2] Real orderbook depth slippage estimation in slippage_guard

**What:** Replace the `size_usdc / liquidity_usdc` proxy in `slippage_guard.estimate_slippage()`
with a full bid-side depth walk through the orderbook to get a true slippage estimate.

**Why:** The proxy overestimates slippage for small orders in deep markets (a 100 USDC order
in a 50k USDC book is estimated at 0.2% but actual impact is near zero) and underestimates
for large orders in thin markets (a 500 USDC order in a 1k book hits the proxy cap of 1.0 but
the real slippage at specific price levels could be lower). The difference matters as position
sizes grow in live trading.

**Pros:** Tighter, more accurate slippage estimate. Enables better entry decisions.
Allows higher `max_slippage_pct` threshold without fear of false positives.

**Cons:** Requires either (a) storing the full orderbook in Redis (significant memory,
requires a new CLOBMarketFeed write path) or (b) calling `get_orderbook()` live on every
check (adds latency on the hot path). Option (a) is preferred.

**Context:** `slippage_guard.estimate_slippage()` has a `TODO` comment pointing here.
`clob_client.get_orderbook()` is already stubbed — implement it first in the live auth
phase (see above). The depth walk should sum bid sizes from best bid downward until
`size_usdc` is consumed, then compute weighted average slippage from bid-ask spread at
each level.

**Effort:** M
**Priority:** P2
**Blocked by:** `get_orderbook()` live mode implementation; decision on Redis orderbook storage

---

## [P2] wallet_scores retention policy

**What:** Add a retention/pruning policy for the `wallet_scores` time-series table.

**Why:** `wallet_scores` is append-only — every score recompute writes a new row.
At 500 wallets x 4 rescores/day the table grows ~730k rows/year with no cleanup.
The dashboard's `/whales/{address}/scores/history` endpoint needs the full history,
so pruning must be selective (keep e.g. last 365 days or last N snapshots per wallet).

**Pros:** Bounded table growth. Faster index scans on score history queries.

**Cons:** Pruning logic adds complexity. Risk of accidentally deleting data needed
for model training. Requires deciding retention window (days? count per wallet?).

**Context:** See `meg/db/models.py` WalletScore class comment. At v1 scale,
unbounded growth is acceptable. Start here when query performance degrades or
table exceeds ~5M rows. Options: PostgreSQL cron via `pg_cron`, a Python background
task in agent_core, or migrate to TimescaleDB (best long-term, most infra change).

**Effort:** M (Python cron) or L (TimescaleDB migration)
**Priority:** P2
**Blocked by:** v1 stabilization (do not add until system is running and stable)

---

## [P1] Alembic drift check in CI

**What:** Add `alembic check` as a required CI step that fails if `models.py` has
drifted from the migration history (i.e., ORM models have columns not in migrations).

**Why:** The most common DB schema bug is: developer edits `models.py`, forgets to
generate a migration, tests pass locally (in-memory), prod fails on `alembic upgrade head`.
`alembic check` catches this at PR review time, not deploy time.

**Pros:** Zero-cost safety net. Catches the single most common DB schema mistake.
Gives confidence that `alembic upgrade head` in prod will match `models.py`.

**Cons:** Requires a live PG connection in CI (or a temporary one). Adds one CI step.
Must be run after `alembic upgrade head` to be meaningful.

**Context:** When CI pipeline is set up (planned post-dashboard), add to the DB test job:
```
alembic upgrade head
alembic check   # exits non-zero if models.py has unrepresented changes
```
The `alembic check` command was added in Alembic 1.9.0 — already satisfied by our
`alembic==1.13.1` pin.

**Effort:** S
**Priority:** P1
**Blocked by:** CI pipeline (no CI pipeline yet — planned after dashboard phase)

---

## [P1] resolved_pnl_usdc backfill job

**What:** Build a market-resolution listener that back-fills `positions.resolved_pnl_usdc`
and `signal_outcomes.resolved_pnl_usdc` when a Polymarket market resolves.

**Why:** Both tables have `resolved_pnl_usdc = NULL` until market resolution. Without
this backfill, the training data moat has signals but no outcome labels — you cannot
compute signal accuracy, whale attribution, or model performance over time. This is
what eventually trains the system to get better.

**Pros:** Enables signal performance analytics. Closes the feedback loop for reputation
decay (was a high-scoring signal actually right?). Enables dashboard P&L attribution.

**Cons:** Requires CLOB API polling for market resolution events. Adds a background
async task. Timing is non-trivial (markets can resolve days after the signal fires).

**Context:** Both `signal_outcomes.resolved_pnl_usdc` and `positions.resolved_pnl_usdc`
are explicitly nullable, with comments noting this is filled by the backfill job.
The listener should poll Polymarket CLOB for resolved markets, find matching positions
and signals, compute final P&L, and write it back. Start in `agent_core/` since it
has access to both position state and signal history.

**Effort:** M
**Priority:** P1
**Blocked by:** Execution layer (positions must exist before backfill is meaningful),
Data layer CLOB client (needs market resolution event feed)

---

## [P1] Polygon RPC gap-fill replay

**What:** When polygon_feed reconnects after a disconnect, replay transactions from the
last_processed_block to the current block to recover any missed whale trades.

**Why:** Currently, a disconnect (crash, RPC timeout, deploy restart) silently drops all
blocks between `last_processed_block` and the reconnect point. At 2 blocks/second on
Polygon, a 5-minute outage = ~600 missed blocks. A single whale trade in that window
is a missed signal with no recovery path.

**Pros:** Zero blind spots in trade history. Enables confident replay after restarts.
Reduces false negatives in signal detection during outages.

**Cons:** Requires fetching and filtering potentially hundreds of blocks on reconnect —
adds startup latency. Risk of re-emitting duplicate events if dedup is not airtight
(tx_hash UniqueConstraint in trades table provides this protection).

**Context:** polygon_feed._check_block_gap() already detects gaps and logs a WARNING
with gap size. The gap_fill replay should: (1) iterate block range [last+1, current],
(2) call _process_block() for each, (3) set last_processed_block at the end of replay.
Add a timeout (e.g. max 10 minutes of replay) to prevent stalling on very large gaps.
Consider building this as `PolygonFeed._replay_gap(from_block, to_block)`.

**Effort:** M
**Priority:** P1
**Blocked by:** polygon_feed must be stable in production before gap-fill adds complexity

---

## [P2] Wallet auto-discovery from on-chain data

**What:** Automatically identify and register new whale wallet candidates from
on-chain Polymarket CLOB transactions — without requiring manual bootstrap.

**Why:** bootstrap_wallets.py seeds the registry with known whales from Dune/Bitquery,
but new whales emerge continuously. Any wallet making large trades that is NOT in the
registry is invisible to MEG's signal engine. Auto-discovery fills this gap by
monitoring CLOB contract transactions and flagging wallets above a size/frequency
threshold for evaluation.

**Pros:** Self-growing registry. Captures emerging whales before competitors.
Removes dependency on periodic manual Dune queries.

**Cons:** Risk of polluting registry with noise (arbitrageurs, bots). Requires
qualification pipeline to evaluate new candidates — can't blindly trust any wallet
making a large trade. registry.register_if_new() is already built; this TODO is
about the scoring/qualification trigger for new registrations.

**Context:** polygon_feed._filter_whale_transaction() already calls register_if_new()
for unknown wallets to mark them as is_tracked=True. This TODO is the next step:
build a background job that evaluates is_tracked=True / is_qualified=False wallets
against historical on-chain data (Dune, Bitquery — see OQ-04) and promotes them to
is_qualified=True if they meet thresholds. Start in agent_core/ alongside the
reputation_decay system. See CLAUDE.md OQ-04 for data source options.

**Effort:** L
**Priority:** P2
**Blocked by:** Data layer stable + reputation decay system (signal_engine phase)

---

## [P1] Gate 1: resolution_source field and flagged_sources config

**What:** Add `resolution_source: str | None` to `MarketState`, write it from
`CLOBMarketFeed._fetch_market_state()`, add `flagged_sources: list[str]` to
`PreFilterConfig`, and implement the Gate 1 check:
`market.resolution_source not in config.pre_filter.flagged_sources`.

**Why:** PRD §9.1 Gate 1 includes this check to reject markets with non-standard
or unreliable resolution oracles — a documented failure mode (LinkedIn arb case,
PRD §10 threat model: "resolution divergence"). Without it, MEG may trade markets
that resolve off disputed or unusual data sources.

**Pros:** Closes the resolution-source risk gate. Gives operators a hot-config
list of oracle sources to blacklist (e.g. unverified admin wallets, obscure APIs).

**Cons:** Cannot implement until the Polymarket CLOB REST API field name for
resolution oracle is confirmed. Adding a field that always returns None provides
zero value and creates dead code. Also requires deciding which sources to flag
by default (empty list is safe — no markets blocked until configured).

**Context:** `days_to_resolution` was added to `MarketState` in the pre-filter
blocker sprint (2026-03-14, branch feat/db-schema). `resolution_source` was
explicitly deferred because the CLOB `/markets/{id}` response field name is
unconfirmed. To resume: (1) verify field name from Polymarket CLOB API docs
or a live `/markets/{id}` response, (2) add `resolution_source: str | None`
to `MarketState` in `meg/core/events.py`, (3) extract it in
`CLOBMarketFeed._fetch_market_state()` in `meg/data_layer/clob_client.py`,
(4) add `flagged_sources: list[str] = []` to `PreFilterConfig` in
`meg/core/config_loader.py`, (5) add the check in Gate 1 `market_quality.check()`.

**Depends on / blocked by:** Confirm Polymarket CLOB API field name for
resolution oracle. Candidate field names: `resolution_source`, `resolver`,
`oracle`, `resolution_criteria`. Check against live API or official docs.

**Effort:** S (once field name is confirmed)
**Priority:** P1

---

## [P2] Gate 2: hold-time arb heuristic (PRD §9.1 heuristic #2)

**What:** Add hold-time check to Gate 2: reject wallets whose `avg_hold_time_hours < 2`.

**Why:** PRD §9.1 specifies this as one of three arbitrage detection signals. Wallets
that hold positions for < 2 hours on average are exploiting price discrepancies, not
expressing directional views. The current Gate 2 only detects same-market both-sides
behavior (heuristic #1). This adds a complementary signal that catches single-sided
arb patterns (e.g. a wallet that buys YES on one platform and sells immediately after
the fill, never holding overnight).

**Pros:** Catches arb wallets that trade only one side (not detected by heuristic #1).
Small behavioral signal with high signal-to-noise for pure arb detection.

**Cons:** `avg_hold_time_hours` must be populated by the reputation_decay system before
this check is meaningful. Checking an un-populated field would false-positive on all
new wallets. Gate must remain conservative (skip check if field is NULL).

**Context:** `Wallet.avg_hold_time_hours` column exists in `meg/db/models.py`. The
check in `arbitrage_exclusion._is_arb_archetype()` or a new `_has_short_hold_time()`
helper would read `wallet:{addr}:data` JSON from Redis (already written by wallet_registry).
Add check only if `data["avg_hold_time_hours"] is not None`. See docstring in
`meg/pre_filter/arbitrage_exclusion.py` for v1 simplification rationale.

**Effort:** S (once avg_hold_time_hours is populated)
**Priority:** P2
**Blocked by:** reputation_decay system (signal_engine phase) must populate avg_hold_time_hours

---

## [P2] Gate 2: tight-spread volume concentration heuristic (PRD §9.1 heuristic #3)

**What:** Add volume-concentration check to Gate 2: reject wallets where >80% of their
observed volume is in markets with bid-ask spread < 0.02.

**Why:** Classic cross-market arb behavior concentrates volume in tight-spread markets
(high liquidity, low friction) rather than spreading across market categories. This
heuristic catches arb wallets that trade single-sided but exclusively in liquid markets.

**Pros:** Orthogonal to heuristics #1 and #2 — catches a distinct arb pattern.

**Cons:** Requires per-trade spread data at the time of trade entry, and an aggregate
query across wallet trade history. Neither is available at Gate 2 evaluation time without
significant additional storage. Requires a new field (e.g. `spread_at_trade` on trades)
or a materialized wallet aggregate.

**Context:** To implement: (1) add `spread_at_trade DECIMAL(6,4)` to Trade model,
(2) write it in polygon_feed / clob_client at trade detection time,
(3) add a wallet aggregate query in Gate 2 or a periodic batch job that computes
`pct_volume_tight_spread` per wallet, (4) read from `wallet:{addr}:data`.
This is a v1.5 enhancement — the current two-layer detection is sufficient for v1.
See docstring in `meg/pre_filter/arbitrage_exclusion.py` for full rationale.

**Effort:** M
**Priority:** P2
**Blocked by:** spread_at_trade field on trades (new migration) + wallet aggregate computation

---

---

## [P3] Gate 1: Redis pipeline optimization

**What:** Batch Gate 1's 5 Redis reads (last_updated_ms, liquidity, spread, participants,
days_to_resolution) into a single `redis.pipeline()` call instead of 5 serial awaits.

**Why:** Each serial read is a separate TCP round trip to Redis. At high event frequency
a 5x latency reduction per trade event could matter.

**Pros:** Reduces Gate 1 latency from ~5 * RTT to ~1 * RTT. No logic changes.

**Cons:** Slightly less readable — individual helper functions `_get_market_liquidity()`,
`_get_market_spread()` etc. become wrappers around a batched result rather than standalone
Redis calls. Requires restructuring `check()` to call pipeline internally.

**Context:** At v1 whale trade frequency (10s–100s/day), this is completely unmeasurable.
Profile first. If gate latency ever exceeds 50ms, this is the first optimization to make.
Implementation is in `meg/pre_filter/market_quality.py` — `check()` would batch all reads
via `redis.pipeline()`, then call individual helpers with the pre-fetched values.

**Effort:** S
**Priority:** P3
**Blocked by:** Gate 1 must be stable and tested before refactoring

---

## [P2] Behavioral state Redis cache for Gates 2/3

**What:** Maintain a Redis sorted set per wallet+market of recent trade outcomes
(`wallet:{addr}:{market_id}:recent_sides`, score=timestamp_ms, member=outcome+size).
Gate 2's `_has_simultaneous_both_sides()` and Gate 3's ladder/hedge detection would
read from Redis instead of querying the Trade table.

**Why:** Currently Gates 2 and 3 query the Trade table (authoritative but involves
a DB round trip). If whale trade frequency increases, these DB queries could become
a latency bottleneck. Redis O(log N) sorted set queries are ~1ms.

**Pros:** Eliminates Trade table round trips from the hot path. Sub-millisecond
behavioral lookups.

**Cons:** Only captures trades that passed Gate 1 (unqualified trades never reach
Gate 2, so the Redis set won't know about YES-side trades on thin markets). This is
a correctness tradeoff: a whale who bought YES on a low-quality market and then sells
NO on a qualified one would look like a SIGNAL, not a HEDGE. For v1, Trade table
is authoritative.

**Context:** Pipeline would write to the sorted set after each qualified trade
(post-Gate 3). Gates read from the set instead of the Trade table. Requires:
(1) new `RedisKeys.wallet_market_sides(addr, market_id)` key, (2) pipeline write
after emit, (3) gate read fallback to Trade table on cache miss.

**Effort:** M
**Priority:** P2
**Blocked by:** Gate 2/3 must be stable in production first; requires v1 load data to justify

---

## [P2] Pre-filter rejection analytics / dashboard metrics

**What:** Expose gate rejection rates as queryable metrics — how many trades are
filtered per gate per day, which markets/wallets are most frequently rejected, and
which gate is the tightest bottleneck.

**Why:** Without rejection analytics, there's no way to know if `min_market_liquidity_usdc`
is too aggressive, if a specific whale is being incorrectly labeled as an arb, or if
Gate 3's HEDGE/REBALANCE classification is swallowing valid signals. These are the
tuning knobs — you can't tune without measurement.

**Pros:** Enables threshold tuning with data. Surfaces misconfigured whales.
Provides operator visibility without requiring log aggregator setup.

**Cons:** Adds either (a) a dedicated `pre_filter_rejections` table (new migration),
(b) a metrics sink (e.g. statsd/CloudWatch), or (c) a structured log aggregation query.
Option (c) is available today via structlog + CloudWatch Insights — no code needed.

**Context:** Currently all rejections log via structlog with `filter_reason`, `gate_id`,
`market_id`, `wallet_address`, and `tx_hash`. This is sufficient for querying in any
log aggregator. The dashboard (Phase 9) could expose these metrics via a `/pre_filter/stats`
endpoint that aggregates structlog output or a lightweight `pre_filter_events` table.
Start with log aggregator approach — only build a DB table if the dashboard needs it.

**Effort:** S (log aggregator) or M (DB table + dashboard endpoint)
**Priority:** P2
**Blocked by:** Dashboard phase (Phase 9); structlog provides this today without a dashboard

---

## [P2] Per-signal-type half-life baselines (v1.5)

**What:** Calibrate a distinct `half_life_seconds` for each `SignalType` value:
`WHALE_REACTION`, `EVENT_CASCADE`, `BEHAVIORAL_DRIFT`, `RESOLUTION_ASYMMETRY`.

**Why:** v1 uses a single uniform half-life (config.signal_decay.half_life_seconds = 3600).
Different signal types decay at fundamentally different rates — a RESOLUTION_ASYMMETRY
signal (market nearing resolution) has a much shorter information window than a
BEHAVIORAL_DRIFT signal (structural wallet behavior shift). Uniform decay under-expires
slow signals and over-runs fast ones, leading to stale signals reaching agent_core.

**Pros:** More precise TTL per signal type. Reduces stale signal execution. Enables
signal_decay to act as a second-pass quality filter beyond score threshold.

**Cons:** Requires historical signal_outcomes data to calibrate baselines — these cannot
be guessed accurately. Building before data exists = arbitrary values. Requires new
config structure (per-type map, not a single scalar).

**Context:** `meg/signal_engine/signal_decay.py` docstring documents this TODO. The
`SignalType` Literal is defined in `meg/core/events.py`. Suggested starting baselines
(to validate against data): WHALE_REACTION=3600s, EVENT_CASCADE=1800s,
BEHAVIORAL_DRIFT=7200s, RESOLUTION_ASYMMETRY=900s. Config change needed in
`SignalDecayConfig` — add `per_type_half_life: dict[SignalType, int]` with fallback
to `half_life_seconds` when type is not in the map.

**Effort:** S (config + code), M (calibration from signal_outcomes)
**Priority:** P2
**Blocked by:** ~3 months of signal_outcomes data with `signal_type` populated; Signal Engine shipped first

---

## [P2] Composite score weight calibration from signal_outcomes

**What:** After accumulating signal_outcomes data (minimum 200 resolved signals),
run a weight optimization pass on `config.signal.composite_weights` using actual
P&L outcomes as the objective function.

**Why:** The current weights (lead_lag=0.35, consensus=0.30, kelly=0.20, divergence=0.15)
are set from PRD §9.3.9 defaults and engineering judgment. Real market data will show
whether lead_lag is truly the strongest predictor, or whether consensus or divergence
outperforms in practice. Un-calibrated weights = leaving alpha on the table.

**Pros:** Data-driven weight tuning replaces judgment-based defaults. Even small
improvements in weight allocation (e.g. +5% to the strongest predictor) improve
composite score accuracy across thousands of signals. signal_outcomes has both
FILTERED and EXECUTED labels — this is a labeled training dataset.

**Cons:** Requires resolved signals (pnl_usdc filled by backfill job). Requires the
resolved_pnl_usdc backfill job to be running first. Optimization can overfit on small
datasets — minimum 200 resolved signals before tuning.

**Context:** `config/config.yaml` composite_weights block is hot-reloadable, so
weight updates can be applied without restart once calibrated. The optimization can be
as simple as a grid search or as sophisticated as Bayesian optimization. Start with a
manual Pandas analysis of `signal_outcomes` data, then automate once the pattern is clear.
The JSONB `scores_json` field stores all component scores per signal — all features
are already captured for regression.

**Effort:** M (analysis + manual tuning), L (automated optimization loop)
**Priority:** P2
**Blocked by:** resolved_pnl_usdc backfill job (see above) + 200+ resolved signals

---

## [P2] pip-audit: dependency vulnerability scanning in CI

**What:** Add `pip-audit -r requirements.txt` as a required CI check on every PR.

**Why:** `requirements.txt` uses exact version pins for reproducibility, which
means security patches do not auto-apply. Without a scanner, a known CVE in a
pinned dependency could go unnoticed indefinitely.

**Pros:** Automated CVE gate. Catches dependency vulnerabilities before they
reach production. Zero false negatives on known CVEs in the advisory database.

**Cons:** Adds a CI step. Requires periodic manual version bumps when alerts
fire. May require triaging false positives on low-severity advisories.

**Context:** When CI is set up (planned post-dashboard phase), add:
```
pip-audit -r requirements.txt --fail-on-cvss 7.0
```
as a required check. Consider pairing with Dependabot or Renovate to auto-open
PRs for dependency updates.

**Effort:** S
**Priority:** P2
**Blocked by:** CI pipeline (no CI pipeline exists yet — planned for after dashboard phase)

---

## [P2] Full PRD saturation formula with 30-day baselines (v1.5)

**What:** Replace the simplified v1 saturation formula (price drift + liquidity ratio)
with the full PRD §9.4.3 formula using 30-day baseline data: price velocity spike
(vs 30-day avg velocity), order book thinning (vs baseline ask depth), and trade
frequency spike (vs 30-day avg trades per minute).

**Why:** v1 uses available data — price drift since whale entry and current liquidity
relative to config floor — but lacks the historical baselines needed for proper spike
detection. The full formula detects relative anomalies (this market is behaving
abnormally right now) rather than absolute thresholds (price moved X%).

**Pros:** More accurate saturation detection. Catches subtle crowding that absolute
thresholds miss. Market-specific baselines adapt to each market's normal behavior.

**Cons:** Requires new background jobs to compute 30-day rolling averages per market
(velocity, depth, frequency). New Redis sorted sets for baseline storage. Significant
infrastructure (~2 modules of work). Cannot be calibrated until 30 days of market
data has been accumulated.

**Context:** Current v1 formula in `meg/agent_core/saturation_monitor.py` uses two
signals: directional price drift (weight 0.60) and liquidity ratio (weight 0.40).
The PRD formula uses three signals with weights 0.40/0.35/0.25. To upgrade: (1) build
baseline accumulation jobs (30-day rolling averages per market), (2) add Redis keys for
baselines, (3) swap formula in `score()`. The config (`agent.saturation_threshold` and
`agent.saturation_size_reduction_sensitivity`) remains unchanged.

**Effort:** L
**Priority:** P2
**Blocked by:** 30 days of market data accumulation; data layer must be running in production

---

## [P3] Copy-follower wallet registry for crowding detection

**What:** Build a registry of known copy-follower wallets by analyzing on-chain behavior
— wallets that consistently trade the same markets within minutes of tracked whale trades.

**Why:** v1 crowding_detector uses price-based heuristics only (entry distance from whale
fill price). Wallet-level copy detection would catch crowding before price moves,
enabling earlier blocking of signals where copy bots have already entered.

**Pros:** Earlier crowding detection. More precise blocking. Enables volume-based crowding
metrics (how much copy-follower USDC has entered this market since the whale trade).

**Cons:** Requires on-chain behavioral analysis, a new DB table (copy_followers or similar),
and classification logic to distinguish copy bots from independent traders who happen to
trade the same market. Risk of false positives on legitimate independent traders.

**Context:** PRD references "copy followers" in the crowding problem description (§3)
but does not spec a registry. The `crowding_detector.get_copy_follower_volume()` stub
was originally designed for this but v1 implementation uses price-based detection instead.
To build: (1) analyze Trade table for wallets that trade within N minutes of tracked
whales at >50% frequency, (2) maintain a scored registry, (3) use in crowding_detector
for volume-based crowding alongside price-based checks.

**Effort:** L
**Priority:** P3
**Blocked by:** Trade table having 1000+ trades for behavioral analysis; data layer stable

---

## [P3] Shared test fixture deduplication across test directories

**What:** Extract common test fixtures (db_engine, db_session, mock_redis, factory helpers)
into a shared location to avoid copy-pasting between test directories.

**Why:** tests/pre_filter/conftest.py and tests/agent_core/conftest.py both define
db_engine, db_session, and mock_redis with identical implementations (~40 lines).
tests/signal_engine/ will need the same fixtures, creating a third copy.

**Pros:** DRY. Single source of truth for DB test setup. Changes to test infrastructure
propagate automatically.

**Cons:** Introduces a tests/conftest.py (root) or tests/helpers.py import pattern
not yet established in the codebase. May be premature with only 2-3 copies.

**Context:** Current project convention (Decision T-1 from Phase 6 eng review) is
independent test directories with their own conftest.py files. This works well for
isolation but creates duplication. Refactor to shared fixtures when the pattern
stabilizes after 3+ test directories use the same fixtures. Options: move to
tests/conftest.py (root), or create tests/fixtures.py as a shared import.

**Effort:** S
**Priority:** P3
**Blocked by:** Phase 7+ (wait until 3 test dirs duplicate the same fixtures)

---

## [P2] Saturation sensitivity default: 2.0 → 1.5 (PRD §15)

**What:** Change `AgentConfig.saturation_size_reduction_sensitivity` default from
`2.0` to `1.5` to match PRD §15 `saturation.size_reduction_sensitivity: 1.5`.

**Why:** At 2.0, the saturation size reduction curve is more aggressive than the PRD
specifies — e.g. at score 0.90, multiplier is 0.40 (2.0) vs 0.55 (1.5). The 2.0 value
hits the 0.25 floor at score ~0.97 while 1.5 reaches it at score ~1.10 (never in
practice). This over-reduces position size on moderately saturated markets.

**Effort:** S (one-line config change + update docstring)
**Priority:** P2
**Blocked by:** Nothing — safe to change at any time

---

## [P2] Trailing TP: add half_life_pct_remaining condition (PRD §9.4.4)

**What:** Add `signal_half_life_pct_remaining` field to `PositionState` and check
`> 0.25` before trailing the take-profit price in `position_manager._check_single_position()`.

**Why:** PRD §9.4.4 requires `half_life_remaining = position.signal_half_life_pct_remaining > 0.25`
as a condition for trailing TP. Without it, trailing TP can fire on signals whose information
edge has fully decayed — trailing on a stale signal risks holding into a reversion.

**Context:** `PositionState` needs: `signal_half_life_pct_remaining: float = 1.0`.
Must be set by the caller of `open_position()` using the signal's `estimated_half_life_minutes`
and `fired_at`. The monitor loop recalculates it each iteration from elapsed time.
Trailing TP is currently disabled (`trailing_tp_enabled=False`) so this is dormant.

**Effort:** S
**Priority:** P2
**Blocked by:** Nothing — but trailing TP is disabled in v1 so low urgency

---

## [P2] Trailing TP: use 1-hour price change instead of entry-relative drift (PRD §9.4.4)

**What:** Change trailing TP drift detection from `current_price > entry_price * 1.005`
to `market.price_change_pct(hours=1, direction=outcome) > 0.005`.

**Why:** PRD §9.4.4 checks 1-hour rolling price change, not total drift from entry.
The current implementation's entry-relative check becomes permanently True for positions
open >1 day with even modest drift, causing the trailing TP to trail unnecessarily on
flat markets. The 1-hour check captures recent momentum.

**Context:** Requires reading price_history sorted set from Redis (already available via
CLOBMarketFeed). Calculate 1h price change as `(current_mid - price_1h_ago) / price_1h_ago`.
Trailing TP is disabled in v1; implement before enabling.

**Effort:** S
**Priority:** P2
**Blocked by:** Nothing — but trailing TP is disabled in v1 so low urgency

---

## [P3] Position state machine: add PENDING_EXIT and WHALE_EXIT_FLAGGED states (PRD §9.4.4)

**What:** Add `PENDING_EXIT` and `WHALE_EXIT_FLAGGED` to `PositionState.status` Literal
and set them in `position_manager._check_single_position()` when TP/SL or whale exit
conditions are met.

**Why:** PRD §9.4.4 lifecycle shows TP/SL → `PENDING_EXIT` and whale exit → `WHALE_EXIT_FLAGGED`.
Currently TP/SL and whale exit only log warnings — status stays `OPEN`. The dashboard
approval queue (Phase 9) needs these states to show "awaiting exit decision" positions
distinctly from normal open positions.

**Context:** `PositionState.status` is `Literal["OPEN", "CLOSED", "EXITED"]`. Add
`"PENDING_EXIT"` and `"WHALE_EXIT_FLAGGED"`. In `_check_single_position()`, when `tp_hit`
or `sl_hit`: set `status = "PENDING_EXIT"`. When whale exit detected: set
`status = "WHALE_EXIT_FLAGGED"`. The DB `Position.status` enum (`PositionStatus`) also
needs these values. Requires a migration.

**Effort:** M
**Priority:** P3
**Blocked by:** Dashboard phase (Phase 9) — states only matter for UI display

---

## [P3] Decision agent gate ordering: circuit breaker before system_paused (PRD §9.4.1)

**What:** Move the daily loss / circuit breaker check before the system_paused check
in `decision_agent.evaluate()`.

**Why:** PRD §9.4.1 and §10 Gate 1 list circuit_breaker as the highest-priority check —
"Immediately halt ALL new signal processing." Currently `system_paused` is checked first.
If the system is not paused but daily loss has exceeded the threshold, the signal passes
through `system_paused` and `blacklisted_markets` checks before hitting the circuit breaker
in `risk_controller`. The circuit breaker should fire before any other check.

**Context:** In `decision_agent.evaluate()`, add a daily PnL read from Redis before
the system_paused check: `daily_pnl = float(await redis.get(RedisKeys.daily_pnl_usdc()) or "0")`.
If `daily_pnl < 0 and abs(daily_pnl) >= config.risk.max_daily_loss_usdc`: block immediately.
This duplicates the check from risk_controller but ensures correct priority ordering.
Alternatively, call risk_controller's daily loss gate first, then the hard blocks.

**Effort:** S
**Priority:** P3
**Blocked by:** Nothing — but practical impact at v1 is near-zero
