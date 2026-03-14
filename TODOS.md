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
