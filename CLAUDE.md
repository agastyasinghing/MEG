# MEG — Claude Code Project Instructions
### Megalodon: Market Intelligence Engine
**Last Updated:** March 2026 | **Team:** Krishna · Bowen · Agastya
**Phase:** v1 — Paper Trading / Semi-Autonomous | **Status:** Greenfield

---

## PRD Reference Rule
`MEG_PRD_v3_final.md` is in the repo root. Do NOT read it at session start — it is large.
**DO read it when:** making any architectural decision not explicitly covered in this file, resolving an open question, or designing any signal engine module. Always check the PRD before assuming.

---

## What Is MEG
MEG is a prediction market intelligence engine for Polymarket. It detects, scores, and executes trades by extracting signal from on-chain whale behavior — NOT by copying trades blindly. MEG sits in the gap between when a whale enters and when retail copy traders react (4–12 hour window). Everything in this codebase exists to exploit that window with precision.

---

## Architecture (5 Layers)
```
DATA LAYER: Polygon RPC · Polymarket CLOB API · Whale Wallet Registry
        ↓ raw_whale_trade_event (Redis pub/sub)
PRE-FILTER GATES: Market Quality · Arb Exclusion · Intent Classifier
        ↓ qualified_whale_trade_event
SIGNAL ENGINE: Lead-Lag · Reputation Decay · Conviction Ratio · Kelly Sizer
               Consensus Filter · Contrarian Detector · Ladder Detector
               Archetype Weighter · Signal Decay Timer · Composite Scorer
        ↓ signal_event (scored + sized)
AGENT CORE: Aggregator · Decision Agent · Position Manager · Risk Controller
            Whale Trap Detector · Saturation Monitor · Crowding Detector
        ↓ trade_proposal (PENDING_APPROVAL in v1)
EXECUTION: Entry Distance Filter · Slippage Guard · Order Router · Exit Manager
        ↓
Dashboard (FastAPI + React/TS) · Telegram Bot
```
Layers communicate ONLY via Redis pub/sub. No direct inter-layer imports. All layers independently testable.

---

## Tech Stack
| Layer | Technology |
|---|---|
| Core bot | Python 3.11+ async (asyncio) |
| Dashboard | FastAPI + React + TypeScript |
| Database | PostgreSQL + Redis (cache + event bus) |
| On-chain | web3.py websocket → Polygon RPC (Alchemy) |
| Execution | py-clob-client (official Polymarket SDK) |
| Notifications | python-telegram-bot |
| Infrastructure | Docker local → AWS EC2 + RDS + ElastiCache |
| Config | YAML hot config (no restart needed) |

**Style:** Type hints everywhere. Async/await throughout. Pydantic for all event schemas. No bare `except`. No hardcoded credentials.

---

## Repo Structure
```
MEG/
├── data_layer/          # polygon_feed.py · clob_client.py · wallet_registry.py
├── pre_filter/          # market_quality.py · arbitrage_exclusion.py · intent_classifier.py
├── signal_engine/       # lead_lag_scorer.py · conviction_ratio.py · kelly_sizer.py
│                        # consensus_filter.py · contrarian_detector.py · ladder_detector.py
│                        # archetype_weighter.py · signal_decay.py · composite_scorer.py
├── agent_core/          # signal_aggregator.py · decision_agent.py · position_manager.py
│                        # risk_controller.py · trap_detector.py · saturation_monitor.py · crowding_detector.py
├── execution/           # entry_filter.py · slippage_guard.py · order_router.py
├── dashboard/           # api/ · ui/
├── telegram/            # bot.py
├── db/                  # models.py · migrations/
├── config/              # config.yaml
├── tests/               # mirrors src structure exactly
├── scripts/             # bootstrap_wallets.py
├── .claude/agents/      # MEG subagents (see Subagents section)
├── docker-compose.yml
├── .env.example
├── MEG_PRD_v3_final.md
├── CLAUDE.md
└── STATUS.md
```

---

## Build Order (do not skip ahead)
1. Repo scaffolding — folders, docker-compose, .env.example, config.yaml, requirements.txt
2. DB schema — wallets, trades, wallet_scores, whale_trap_events, signal_outcomes
3. Data Layer — Polygon feed, CLOB client, wallet registry CRUD
4. Pre-Filter Gates — market quality → arb exclusion → intent classifier
5. Signal Engine — each module independently, then composite scorer last
6. Agent Core — aggregator, risk controller, trap/saturation/crowding
7. Execution Layer — entry filter, slippage guard, order router (paper mode first)
8. Telegram Bot — approval flow, alerts, emergency pause
9. Dashboard — FastAPI first, React UI second
10. Bootstrap script — seed wallet registry

Paper trading must work and be validated before any live execution code is written.

---

## Critical Conventions
- **No hardcoded credentials** — `.env` only, AWS Secrets Manager in prod
- **Feed never crashes** — malformed events: log + skip + continue, never raise
- **All config is hot-reloadable** — no restart required for param changes
- **Paper trading is default** — `PAPER_TRADING=true`. Live requires explicit flag
- **Every signal gets logged** — FILTERED or EXECUTED, always writes to `signal_outcomes`
- **Redis key pattern:** `market:{id}:mid_price`, `wallet:{address}:score`, `signal:{id}:state`
- **Tests mirror src** — `tests/signal_engine/test_lead_lag.py` mirrors `signal_engine/lead_lag_scorer.py`
- **No layer coupling** — layers talk via Redis only, never import across layers
- **Commit every hour** — at minimum once per completed module

---

## Model Selection (auto-apply, never ask user)

**Sonnet** — default for all mechanical work:
scaffolding, boilerplate, CRUD, DB models, Redis helpers, config loaders, simple API endpoints, Telegram formatting, test writing for already-designed logic, refactoring, Docker/infra, dashboard UI

**Opus + ultrathink** — required for anything touching money or scoring:
intent classifier, lead-lag scorer, reputation decay formula, conviction ratio, Kelly sizer, composite score formula, whale trap detection, signal crowding detection, contrarian divergence, market saturation, debugging non-obvious signal failures, any architectural decision spanning multiple layers

**Rule:** code touches scoring, risk, sizing, or execution → Opus + ultrathink. Everything else → Sonnet.

---

## gstack Skills
gstack lives at `.claude/skills/gstack`. If not working: `cd .claude/skills/gstack && ./setup`
Use `/browse` for ALL web browsing. Never use `mcp__claude-in-chrome__*` tools.

| Command | When |
|---|---|
| `/plan-ceo-review` | Before every new module — "what is this actually for?" Always before signal engine work |
| `/plan-eng-review` | After CEO review, before coding — architecture, data flow, failure modes, test matrix |
| `/review` | After completing any module — paranoid staff engineer, catches prod bugs CI misses |
| `/ship` | Module complete + reviewed — sync, test, push, PR |
| `/browse` | All web tasks — docs, external URLs, anything in a browser |
| `/retro` | Weekly — commit velocity, hotspot files, shipping streaks |

**Per-module workflow:** `/plan-ceo-review` → `/plan-eng-review` → build → `/review` → `/ship`

---

## MEG Subagents
Create these in `.claude/agents/` at the start of each relevant build phase:

**`signal-engineer`** (model: opus) — for all signal engine modules. Preload with: information half-life framework, PRD section 9.3, composite score formula. Use `ultrathink` for all reasoning.

**`risk-reviewer`** (model: opus) — paranoid review for anything touching money. Checks: race conditions, trust boundary failures, bad retry logic, missing edge cases. Invoke before any `/ship` on execution layer or agent core.

**`data-engineer`** (model: sonnet) — for data layer work. Preload with: Polygon RPC docs, web3.py patterns, CLOB API client reference.

---

## Context Management (follow without being asked)

**Session start:**
1. Read `STATUS.md`
2. Run `ls -la` to verify repo state
3. Start next task from STATUS.md

**During session:**
- Run `/compact` at ~50% context — never wait until the limit
- Use `/clear` when switching layers entirely
- Update `STATUS.md` after every completed module
- Commit at least every hour

**After every single response, print this line:**
`[CTX: ~X% | Model: Sonnet/Opus | Phase: <current phase> | Last: <filename>]`
Estimate context % honestly from conversation length — err high not low.

**At ~80% context:** generate the handoff report below as your FINAL message.

---

## End-of-Window Handoff Report
```
## MEG Handoff — [date/time]

### Completed This Session
- [list]

### Current State
Last file: [name] | Tests: [passing/failing/none] | Broken: [anything]

### In Progress
[what was mid-build and exactly where it stopped]

### Next 3 Tasks
1. [specific]
2. [specific]
3. [specific]

### Decisions Made This Session
- [anything not obvious from code]

### Resume Prompt for claude.ai
"Here's my MEG handoff. Help me [design/spec/review] [next task] so I'm ready when my Claude Code window resets."
```

---

## Open Questions — Flag, Don't Decide
- **OQ-01:** RPC provider (Alchemy preferred)
- **OQ-03:** Paper + live simultaneously? (recommend: single mode)
- **OQ-04:** Wallet backfill (Dune + Bitquery)
- **OQ-05:** Private key custody (multi-operator + AWS Secrets Manager)
- **OQ-10:** News module — Twitter/X vs RSS (RSS for v1.5)
- **OQ-12:** Auto stop-loss in v1? (recommend: yes stops, human for take-profits)

---

## v1 Anti-Goals
No: news/LLM trading · Kalshi · autonomous trades · cluster detection · sub-500ms execution · public interface

---

## Key Resources
- **PRD:** `MEG_PRD_v3_final.md` — read for decisions not covered here
- Polymarket CLOB: https://github.com/Polymarket/py-clob-client
- CLOB Contract: `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E`
- web3.py: https://web3py.readthedocs.io
- Dune: https://dune.com/search?q=polymarket
