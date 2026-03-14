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
