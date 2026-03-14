# MEG — Deferred TODOs

Items considered during planning and explicitly deferred. Each entry has enough
context to be picked up without re-reading the original planning session.

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

## [P1] OPUS SESSION: Implement intent_classifier.py classify() and build_qualified_trade()

**What:** Implement the two NotImplementedError stubs in `meg/pre_filter/intent_classifier.py`:
`classify(trade, redis, config, session)` and `build_qualified_trade(trade, intent, redis)`.

**Why:** Gate 3 is the final pre-filter gate. Without it, the pipeline raises
NotImplementedError on every event and nothing reaches the signal engine. This is
the last blocker before pre_filter → signal_engine is end-to-end runnable.

**Pros:** Completes Phase 4. Enables signal engine work to begin.

**Cons:** Must be done with Opus + ultrathink — the classification logic directly
determines what reaches execution. Getting SIGNAL vs HEDGE/REBALANCE wrong means
either signal starvation (false HEDGE positives) or noise injection (REBALANCE
trades reaching the signal engine with real sizing).

**Context:** The test spec is fully written at `tests/pre_filter/test_intent_classifier.py`.
Read that file first — it defines the exact expected behaviour for all 14 test cases
(SIGNAL, SIGNAL_LADDER, HEDGE, REBALANCE, boundary conditions, edge cases).

Key implementation constraints:
- No import of meg.data_layer.wallet_registry (layer coupling violation)
- Read wallet data from Redis directly: wallet:{addr}:data (JSON blob),
  wallet:{addr}:score, wallet:{addr}:archetype
- Query Trade table via sqlalchemy (session param) for behavioral signals
- session=None: skip Trade queries, return SIGNAL conservatively
- build_qualified_trade returns None on any cache miss (never emit whale_score=0.0)
- The compound index ix_trades_wallet_market_time already exists for efficient queries

Config params available in config.pre_filter:
  ladder_window_hours: 6, ladder_min_trades: 2, min_signal_size_pct: 0.02,
  arb_detection_window_hours: 24

**Depends on / blocked by:** Nothing — test spec is ready. Start immediately
after any Opus context window is available.

**Effort:** M (Opus session ~1–2 hours with ultrathink)
**Priority:** P1

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
