# MEG — Claude Code Project Instructions
### Megalodon: Market Intelligence Engine
**Last Updated:** March 2026  
**Team:** Krishna · Bowen · Agastya

---

## What Is MEG

MEG (Megalodon) is a prediction market intelligence engine and automated trading bot for Polymarket. It detects, scores, and executes trades by extracting actionable signal from the on-chain behavior of statistically proven whale traders — not by blindly copying them.

MEG is NOT a copy bot. It is an intelligence layer that sits in the gap between when a high-quality whale enters a position and when retail copy traders react. Everything in this codebase exists to exploit that window with precision.

**Current Phase:** v1 — Paper Trading / Semi-Autonomous  
**Status:** Pre-code. Greenfield build.

---

## Architecture Overview (5 Layers)

```
DATA LAYER
  Polygon RPC (on-chain feed) · Polymarket CLOB API · Whale Wallet Registry
        ↓ raw_whale_trade_event
PRE-FILTER GATES
  Market Quality Filter · Arbitrage Whale Exclusion · Intent Classifier
        ↓ qualified_whale_trade_event
SIGNAL ENGINE
  Lead-Lag Scorer · Reputation Decay · Conviction Ratio · Kelly Sizer
  Consensus Filter · Contrarian Detector · Entry Ladder Detector
  Archetype Weighter · Signal Decay Timer
        ↓ signal_event (scored + sized)
AGENT CORE
  Signal Aggregator · Decision Agent · Position Manager
  Risk Controller · Whale Trap Detector · Market Saturation Monitor · Signal Crowding Detector
        ↓ trade_proposal (PENDING_APPROVAL in v1)
EXECUTION LAYER
  Entry Distance Filter · Slippage Guard · Order Router · Position Exit Manager
        ↓
  Dashboard (FastAPI + React/TS) · Telegram Bot
```

Layers communicate via Redis pub/sub event bus. No layer has a direct dependency on another's implementation. All layers are independently testable.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Core bot | Python 3.11+ async (asyncio) |
| Dashboard | FastAPI (API) + React + TypeScript (UI) |
| Database | PostgreSQL (persistent) + Redis (cache + event bus) |
| On-chain feed | web3.py websocket → Polygon RPC (Alchemy preferred) |
| Polymarket execution | py-clob-client (official SDK) |
| Notifications | Telegram Bot API (python-telegram-bot) |
| Infrastructure | Docker (local) → AWS EC2 + RDS + ElastiCache (prod) |
| Config | YAML hot config (no restart required for param changes) |

**Python style:** Type hints on everything. Async/await throughout. Pydantic models for all event schemas. No bare `except`. No hardcoded credentials — all secrets via env vars or AWS Secrets Manager.

---

## Repo Structure

```
meg/
├── data_layer/
│   ├── polygon_feed.py          # Polygon RPC websocket, raw event emission
│   ├── clob_client.py           # Polymarket CLOB API wrapper
│   └── wallet_registry.py       # Wallet DB reads/writes, score queries
├── pre_filter/
│   ├── market_quality.py        # Gate 1: liquidity/spread/participant checks
│   ├── arbitrage_exclusion.py   # Gate 2: arb whale detection
│   └── intent_classifier.py    # Gate 3: SIGNAL / HEDGE / REBALANCE
├── signal_engine/
│   ├── lead_lag_scorer.py       # Lead-lag scoring + reputation decay
│   ├── conviction_ratio.py      # bet_size / wallet_capital weighting
│   ├── kelly_sizer.py           # Kelly criterion position sizing
│   ├── consensus_filter.py      # Multi-whale agreement check
│   ├── contrarian_detector.py   # Against-order-flow detection
│   ├── ladder_detector.py       # Escalating position pattern detection
│   ├── archetype_weighter.py    # INFORMATION / MOMENTUM / ARBITRAGE weighting
│   ├── signal_decay.py          # TTL management on signals
│   └── composite_scorer.py     # Combine all module scores → final score
├── agent_core/
│   ├── signal_aggregator.py     # Collect scored signals
│   ├── decision_agent.py        # Gate signals against risk rules
│   ├── position_manager.py      # Track open positions
│   ├── risk_controller.py       # 5-gate risk framework
│   ├── trap_detector.py         # Whale pump-and-exit pattern detection
│   ├── saturation_monitor.py    # Market crowding detection
│   └── crowding_detector.py    # Entry distance / copy follower detection
├── execution/
│   ├── entry_filter.py          # Entry distance re-check before order
│   ├── slippage_guard.py        # Spread + drift check
│   └── order_router.py         # Place / manage orders via CLOB
├── dashboard/
│   ├── api/                     # FastAPI endpoints
│   └── ui/                      # React + TypeScript frontend
├── telegram/
│   └── bot.py                   # Approval flow + alerts
├── db/
│   ├── models.py                # SQLAlchemy models
│   └── migrations/              # Alembic migrations
├── config/
│   └── config.yaml              # Hot-reloadable parameters
├── tests/                       # Mirrors src structure
├── scripts/
│   └── bootstrap_wallets.py     # Seed wallet registry from Dune/leaderboard
├── docker-compose.yml
├── .env.example
├── CLAUDE.md                    # This file
└── STATUS.md                    # Current session state (update every session)
```

---

## Key Data Models (Reference)

**Raw whale trade event** (emitted by data layer):
```json
{
  "event_type": "raw_whale_trade",
  "wallet_address": "0x...",
  "market_id": "...",
  "outcome": "YES",
  "size_usdc": 25000.00,
  "timestamp_ms": 1709123456789,
  "tx_hash": "0x...",
  "block_number": 12345678,
  "market_price_at_trade": 0.43
}
```

**Whale qualification thresholds** (all hot-configurable in config.yaml):
- Min win rate: 55%
- Min closed positions: 50
- Min total volume: $100,000 USDC
- Min profitable months (trailing 6): 3
- Exclude: ARBITRAGE and MANIPULATOR archetypes

**Composite score threshold:** 0.45 minimum to proceed. Signals below this are logged as FILTERED, never executed.

**Signal TTL:** 2 hours default. Expired signals are never executed regardless of score.

---

## Build Order (v1 Sequence)

Build in this order — each layer depends on the previous:

1. **Repo scaffolding** — folder structure, docker-compose, .env.example, base config.yaml
2. **DB schema** — PostgreSQL tables: wallets, trades, wallet_scores, whale_trap_events, signal_outcomes
3. **Data Layer** — Polygon feed (websocket), CLOB API client, wallet registry CRUD
4. **Pre-Filter Gates** — market quality, arb exclusion, intent classifier (in order)
5. **Signal Engine** — each module independently, then composite scorer
6. **Agent Core** — aggregator, risk controller, trap/saturation/crowding detectors
7. **Execution Layer** — entry filter, slippage guard, order router (paper mode first)
8. **Telegram Bot** — approval flow, alerts, emergency pause
9. **Dashboard** — FastAPI API first, React UI second
10. **Bootstrap script** — seed wallet registry from public sources

Do NOT skip ahead. Paper trading mode must work before any live execution is written.

---

## Critical Conventions

- **Never hardcode credentials.** API keys, wallet keys, DB passwords → `.env` only. In prod: AWS Secrets Manager.
- **Never crash the feed.** Malformed events → log with full context, skip, continue. The polygon feed must never raise an unhandled exception.
- **All config values are hot-reloadable.** Nothing that affects signal behavior should require a restart to change.
- **Paper trading is the default.** `PAPER_TRADING=true` in env. Live mode requires explicit flag + confirmation.
- **Every signal gets logged.** Whether FILTERED or EXECUTED, every signal event writes to `signal_outcomes`. This is the training data moat.
- **Redis keys follow this pattern:** `market:{id}:mid_price`, `wallet:{address}:score`, `signal:{id}:state`
- **Tests mirror src structure.** `tests/signal_engine/test_lead_lag_scorer.py` mirrors `signal_engine/lead_lag_scorer.py`
- **No direct layer coupling.** Layers communicate only via Redis pub/sub events. Never import from a downstream layer.
- **Type everything.** Every function signature has type hints. Every event schema is a Pydantic model.

---

## gstack Skills

gstack is installed in this repo (`.claude/skills/gstack`). Use these slash commands:

| Command | When to use |
|---|---|
| `/plan-ceo-review` | Before starting any new feature or module. Forces product-quality thinking: "what is this actually for?" Use this especially before building signal engine modules to ensure they serve the intelligence goal, not just the spec. |
| `/plan-eng-review` | After `/plan-ceo-review`, before writing code. Locks in architecture, data flow, edge cases, and test plan for the specific module. |
| `/review` | After completing any module or significant chunk of code. Full staff-engineer-level code review for correctness, security, and maintainability. |
| `/ship` | When ready to commit a completed, reviewed module. Handles the full PR/commit workflow. |
| `/browse` | For ALL web browsing tasks (Polymarket docs, Polygon RPC docs, py-clob-client docs, any external URL). |
| `/retro` | Weekly — analyze commit velocity, hotspot files, shipping streaks, what to improve. |

**Web browsing rule:** Always use `/browse` for web browsing. NEVER use `mcp__claude-in-chrome__*` tools directly.

**If gstack skills aren't working:** run `cd .claude/skills/gstack && ./setup`

---

## Model Selection Rules

Use these rules automatically — do not ask the user which model to use:

### Use Sonnet for:
- Scaffolding folders and boilerplate files
- Writing straightforward CRUD (DB models, Redis cache helpers, config loaders)
- Simple API endpoints and Telegram message formatting
- Writing tests for already-designed logic
- Refactoring / renaming / moving code
- Docker and infrastructure config
- Dashboard UI components
- Any task where the logic is well-defined and the work is mechanical

### Use Opus for:
- The intent classifier (SIGNAL / HEDGE / REBALANCE logic)
- Lead-lag scorer and reputation decay formula
- Conviction ratio modeling
- Kelly criterion sizer
- Composite score formula and weight calibration
- Whale trap detection pattern logic
- Signal crowding and market saturation detection
- Contrarian divergence detection
- Any module where incorrect logic = real money lost
- Debugging non-obvious failures in signal flow
- Architectural decisions that affect multiple layers
- Anything involving the information half-life framework

**Default to Sonnet.** Switch to Opus only for the modules listed above. When in doubt: if the code touches scoring, risk, or money — use Opus.

---

## Context Management Protocol

Follow this protocol every session without being asked:

### During a session:
1. **Start every session** by reading `CLAUDE.md` and `STATUS.md`, then run `ls -la` to orient. Do this before writing a single line of code.
2. **Check `/cost` every ~15 messages** or after completing any module. Do this silently.
3. **When context is getting long** (you notice response quality degrading or you're losing track of earlier decisions), run `/compact` immediately — do not wait until the window is full.
4. **After completing any module**, update `STATUS.md` before moving to the next task.

### Before the context window ends:
When you notice context is near its limit (via `/cost` showing high usage, or `/compact` has been run multiple times), generate the End-of-Window Handoff Report (see below) as your final message before the window closes.

### End-of-Window Handoff Report format:

```
## MEG Handoff Report — [timestamp]

### Completed This Session
- [bullet list of what was built/finished]

### Current State
- Last file modified: [filename]
- Tests passing: [yes/no/partial — which ones]
- Known broken: [anything currently broken]

### In Progress (incomplete)
- [what was being worked on when window ended]
- [exact line/function where you stopped if mid-implementation]

### Next 3 Tasks (in order)
1. [specific, actionable task]
2. [specific, actionable task]
3. [specific, actionable task]

### Decisions Made This Session
- [any architectural or design decisions made that aren't obvious from the code]

### To Resume in Claude.ai Chat
Paste this report into claude.ai and say: "Review this MEG handoff and help me [design/spec/review] [next task] so I'm ready to resume in Claude Code when my window resets."
```

This report is for the human operator to continue work on claude.ai chat while the Claude Code window resets.

---

## Open Questions (from PRD)

These are unresolved. Do not make unilateral decisions on these — flag them:

- **OQ-01:** RPC provider — Alchemy vs QuickNode vs Infura (Alchemy preferred but not locked)
- **OQ-03:** Paper trading and live trading simultaneously? (Recommendation: single mode at a time)
- **OQ-04:** Wallet history backfill strategy (Dune Analytics + Bitquery)
- **OQ-05:** Trading wallet private key custody model (multi-operator, AWS Secrets Manager)
- **OQ-10:** News latency module — Twitter/X API ($100+/mo) vs RSS feeds (cheaper, sufficient for v1.5)
- **OQ-12:** Stop-loss auto-execution in v1? (Recommendation: yes for stops, human approval for take-profits)

---

## What MEG Does NOT Do (v1)

- Does not trade on news, fundamentals, or LLM predictions
- Does not operate on Kalshi or any platform other than Polymarket
- Does not make fully autonomous trades — all trades require human approval
- Does not do cluster detection (v2)
- Does not implement shadow entry / sub-500ms execution (v2)
- Does not expose any public-facing interface

---

## Key External Resources

- Polymarket CLOB Client: https://github.com/Polymarket/py-clob-client
- Polymarket CLOB Contract: `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E`
- Polymarket Agents Framework: https://github.com/Polymarket/agents
- web3.py docs: https://web3py.readthedocs.io
- Dune Polymarket dashboards: https://dune.com/search?q=polymarket
