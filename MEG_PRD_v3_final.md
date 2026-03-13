# MEG — Product Requirements Document
### Megalodon: Market Intelligence Engine
**Version:** 3.0 — Final  
**Authors:** Krishna · Bowen · Agastya  
**Status:** Draft — Circulate for Review  
**Last Updated:** March 2026  
**Replaces:** ORCA PRD v1.0, MEG PRD v2.0

---

> *The Megalodon was the apex predator of the ocean — not because it was the biggest, but because it was the most intelligent hunter. It didn't chase prey. It read behavior, anticipated movement, and struck at exactly the right moment. MEG is that system for prediction markets.*

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [The Reframe: From Copy Bot to Intelligence Engine](#2-the-reframe-from-copy-bot-to-intelligence-engine)
3. [Problem Statement](#3-problem-statement)
4. [Opportunity & Market Context](#4-opportunity--market-context)
5. [Product Vision & Phases](#5-product-vision--phases)
6. [Goals & Success Metrics](#6-goals--success-metrics)
7. [User Personas](#7-user-personas)
8. [System Architecture Overview](#8-system-architecture-overview)
9. [Feature Specifications — v1](#9-feature-specifications--v1)
   - 9.1 Pre-Filter Gates
   - 9.2 Data Layer
   - 9.3 Signal Engine
   - 9.4 Agent Core
   - 9.5 Execution Layer
   - 9.6 Dashboard & Observability
10. [Risk Management Framework](#10-risk-management-framework)
11. [Technical Stack](#11-technical-stack)
12. [Data Models](#12-data-models)
13. [API & Integration Contracts](#13-api--integration-contracts)
14. [Paper Trading Mode](#14-paper-trading-mode)
15. [Configuration & Hot Reload System](#15-configuration--hot-reload-system)
16. [Plugin Socket Architecture](#16-plugin-socket-architecture)
17. [Non-Functional Requirements](#17-non-functional-requirements)
18. [Signal Versioning Roadmap](#18-signal-versioning-roadmap)
19. [v2 Roadmap](#19-v2-roadmap)
20. [v3 Roadmap — Public SaaS](#20-v3-roadmap--public-saas)
21. [Open Questions & Decisions Log](#21-open-questions--decisions-log)
22. [Appendix](#22-appendix)

---

## 1. Executive Summary

MEG (Megalodon) is a prediction market intelligence engine and automated trading system. It identifies, scores, and executes trades by extracting actionable intelligence from the on-chain behavior of statistically proven whale traders on Polymarket — not by blindly copying them.

The distinction matters. Every existing whale-tracking tool in the Polymarket ecosystem — Polywhaler, PolyTrack, WhaleWatch Poly, PolyIntel, PolyCopy — is a monitoring dashboard. They surface what whales do. MEG understands *why* they did it, *how confident* they were, *whether* the signal is still valid, and *when* to act on it. Then it acts.

MEG's intelligence extraction pipeline includes:

- **Lead-lag scoring** — ranking whales by how early they historically enter before price moves
- **Intent classification** — distinguishing signal trades from hedges and inventory rebalancing
- **Reputation decay** — automatically downweighting whales whose edge has gone stale
- **Conviction ratio modeling** — treating a $200k bet from a $1M wallet differently than the same bet from a $10M wallet
- **Multi-whale consensus filtering** — requiring independent confirmation before acting
- **Whale archetype classification** — information whales, momentum whales, arbitrage whales, each weighted differently
- **Entry ladder detection** — identifying whales building positions with escalating conviction
- **Contrarian divergence detection** — flagging when smart money moves against market consensus
- **Entry distance filtering** — never chasing a signal the market has already priced
- **Signal crowding detection** — identifying when a signal has been saturated by copy followers
- **Whale trap detection** — protecting against deliberate pump-and-exit manipulation
- **Market saturation monitoring** — reducing position size when a market is overrun by reactive traders
- **Market quality pre-filtering** — refusing to trade illiquid, thin, or structurally risky markets

In v1, MEG operates in semi-autonomous mode — it generates scored trade proposals that a human operator approves via dashboard or Telegram. In v2, it trades fully autonomously 24/7. In v3, it becomes a platform that external traders can subscribe to.

The dual goal is to generate real trading returns while building a defensible, portfolio-grade engineering artifact with a clear path to a quant-grade public SaaS product.

---

## 2. The Reframe: From Copy Bot to Intelligence Engine

This distinction is the philosophical foundation of MEG and should inform every architecture decision.

**What whale monitoring tools do:**
> "Whale X bought $200k YES on market Y at 14:22 UTC."

**What MEG does:**
> "Wallet 0x4f2a, classified as an information-type whale with a 71% win rate in politics markets, a 6.2-hour average lead time before price moves, and a current reputation score of 0.84 (stable, not decaying), just committed 18% of their tracked capital to YES on market Y — expressing unusually high conviction. Two cluster-linked wallets independently confirmed the same position within 4 minutes. The market has not yet repriced. Order book shows net selling pressure, making this a contrarian entry. News feed shows no coverage of this event in the past 2 hours. Entry distance from whale's fill is 1.2%. Composite signal score: 0.81. Recommended size: $340 USDC (quarter-Kelly). Slippage estimate: 0.4%."

The first is surveillance. The second is intelligence. MEG is built to produce the second.

### The Information Hierarchy

MEG's entire value proposition can be understood through one framework:

```
Insiders / Primary Sources
        ↓
Professional Traders / Whales      ← MEG detects signal here
        ↓
Prediction Markets Begin Moving    ← MEG executes here
        ↓
Retail Traders React
        ↓
News Coverage
        ↓
Casual Participants
```

MEG sits in the gap between layer 2 and layer 3. Everything in the signal engine is a different method of reading that gap more accurately and acting on it faster. The 4–12 hour window between when a sophisticated whale enters and when the market fully reprices is MEG's operating environment.

### Why The Gap Exists: Sparse Intelligence Density

Prediction markets suffer from what can be called **sparse intelligence density** — a structural condition where the overwhelming majority of participants are not serious, information-driven traders. Most fall into one of these categories:

- Casual bettors and recreational gamblers
- Political partisans betting with conviction rather than probability
- Momentum chasers reacting to visible price moves
- Headline reactors with no independent research
- Small-stake recreational participants

Only a tiny minority are genuine **information traders** — people with probabilistic reasoning, domain expertise, research advantages, or quantitative models. This is the fundamental reason whale-following works at all, and why it works far better in prediction markets than in liquid equity or futures markets where thousands of professionals compete simultaneously.

In a mature market, information advantages are competed away in milliseconds. In Polymarket's current state, a handful of genuine information traders can have meaningful predictive power over entire market categories for extended periods. **Identifying even 20–30 high-quality information traders with confidence gives MEG a dataset that most participants will never have.**

### The Cascade Mechanism: What MEG Is Actually Exploiting

The precise timing edge MEG is designed to capture is not simply "enter after the whale." It is entering between the whale's trade and the retail cascade that inevitably follows. Understanding this cascade is critical to understanding what MEG is optimizing for:

```
① Information trader identifies edge, places trade
        ↓  (price barely moves — thin liquidity)
② MEG detects trade, scores it, executes         ← MEG enters here
        ↓  (price begins moving)
③ Polywhaler / PolyTrack dashboards light up
        ↓
④ Retail copy traders pile in                    ← price overshoots
        ↓
⑤ Information trader exits into retail liquidity
        ↓
⑥ Price reverts to true value
        ↓
⑦ Retail copy traders left holding losses
```

MEG's goal is to consistently execute at step ②. Tools like Polywhaler and PolyTrack operate at step ③ — by which point the best entry has already passed. Naive copy bots that act on step ③ notifications become the exit liquidity at step ⑦.

This cascade also creates a secondary opportunity. The overshoot at step ④ is predictable — it's driven by behavioral dynamics, not information. A signal module that detects the onset of the retail cascade (the herd detector, v1.5) and triggers an exit near the peak of the overshoot extracts additional alpha from the same original signal. One information trader's trade becomes two distinct profitable MEG trades: the entry at step ② and the exit before step ⑦.

### The Three Structural Inefficiencies MEG Exploits

**1. Public transaction data** — All Polymarket trades settle on Polygon and are fully visible on-chain. This is extraordinarily rare in finance. In stock markets, individual institutional trades are invisible until delayed 13F filings. In prediction markets, every trade is public and timestamped in real-time. Every information trader's strategy leaves a complete, permanent footprint.

**2. Small professional pool** — The number of genuine information traders on Polymarket is small enough that identifying them individually is tractable. MEG doesn't need to model "the market" — it needs to model a few dozen high-quality wallets. That is a solvable problem.

**3. Systematic probability reasoning failure** — Most participants think in binary terms (YES or NO) rather than probabilistic terms (65% chance). This leads to persistent, structural mispricings — particularly in markets far from resolution where casual participants haven't engaged yet. Information traders exploit these mispricings. MEG exploits information traders exploiting these mispricings.

### The Learning Loop Is The Real Moat

MEG's architecture is built around a fast learning loop: ship → observe → adjust → repeat. The `signal_outcomes` table is not just an observability feature — it is the core mechanism by which MEG becomes more accurate over time. Every signal that fires, whether it is executed or filtered, gets linked to a market outcome. Over months of operation, this creates a proprietary labeled dataset for calibrating every weight in the composite score formula, validating every archetype classification, and eventually training the ML whale scoring model (v2).

No competitor can replicate this dataset by building a tool today. The data advantage compounds with time. **The longer MEG runs, the harder it becomes to displace.**

### Information Half-Life: The Unifying Theory

Every component of MEG can be understood through a single framework: **information half-life** — the amount of time it takes for half of an informational edge to be priced into the market. Like radioactive decay, every signal MEG detects is decaying from the moment it is generated.

Different edge types have fundamentally different half-lives:

```
Edge Type                  Half-Life          MEG Suitability
──────────────────────────────────────────────────────────────
Micro-latency arb          Milliseconds       ✗ Poor — infrastructure arms race
Whale-reaction             2–15 minutes       ~ Moderate — tight window
Event cascade              30 min – 3 hours   ✓ Excellent — core operating zone
Behavioral drift           4–24 hours         ✓ Excellent — core operating zone
Resolution asymmetry       Days – weeks       ✓ Good — persistent structural edge
```

MEG is optimized for the middle three rows. This is a deliberate architectural choice. Micro-latency edges require dedicated HFT infrastructure and are being systematically closed by Polymarket's fee changes. Event-cascade and behavioral drift edges require intelligence depth — exactly what MEG is built to provide.

This framework answers the most important question in every trade: **how much time is left before the market fully prices this information?** The composite score estimates edge magnitude. Half-life estimates edge duration. Together they determine expected value:

```
expected_value = edge_magnitude × f(remaining_half_life)
```

A 20% mispricing with 5 minutes of half-life remaining is worth less than a 10% mispricing with 6 hours remaining. Every sizing and timing decision in MEG flows from this principle.

MEG estimates half-life dynamically from four real-time signals:
- **Trade velocity** — rapid repricing compresses half-life
- **Liquidity depth** — deep order books slow repricing, extending half-life
- **Social/news spread** — information spreading publicly compresses half-life fast
- **Whale density** — many qualified whales already in position means the market is already adjusting

This framework also provides the decision rule for every future feature evaluation: *what half-life regime does this target, and is MEG architected to capture it?*

---

## 3. Problem Statement

Prediction markets like Polymarket are structurally inefficient in a specific and exploitable way. A small number of sophisticated traders consistently outperform the market, often entering positions hours before prices move. Their trades are publicly visible on the Polygon blockchain. Yet the vast majority of participants either lack the infrastructure to act on this data or act on it too late — after the signal has already been crowded out.

### The Crowding Problem

Signal crowding is the primary failure mode for naive copy systems. The timeline:

```
Whale trades
    ↓
Dashboards show whale trade (5-30 second delay)
    ↓
Copy traders buy  →  price overshoots
    ↓
Whale exits into copy trader liquidity
    ↓
Price reverts  →  copy traders lose
```

A whale buying $200k YES at 0.45 moves the market to 0.55. Copy bots entering at 0.55 push it to 0.60. The whale exits at 0.60 with a 33% gain. Copy bots bought at 0.55 and now hold a position worth 0.52 after the reversion. The copy traders became the exit liquidity.

MEG addresses this through entry distance filtering, signal crowding detection, market saturation monitoring, and whale trap detection — all mechanisms that distinguish early, high-quality signals from crowded, late, or manipulated ones.

### The Intelligence Gap

No existing tool in the 170+ tool Polymarket ecosystem closes the loop from signal detection to automated, sized, risk-managed execution. Every tool is a dashboard. MEG is the execution layer that the ecosystem is missing.

### The Quality Gap

Existing tools treat all whale activity equally. A whale with a 6-month lucky streak in election markets is scored the same as a whale with a 3-year track record across 500+ diverse positions. MEG's whale scoring system — with lead-lag analysis, reputation decay, archetype classification, and conviction ratio modeling — surfaces the difference.

### The Three-Category Edge Taxonomy

Most participants and tools in the Polymarket ecosystem focus on only one type of edge. MEG is designed to exploit all three:

**Category 1 — Behavioral edges:** Edges that arise from human psychology and trading behavior. Herding, momentum, overreaction, whale signaling, probability anchoring. These are the most commonly discussed but also the most competed-for edges. MEG's whale intelligence pipeline is the primary mechanism for capturing behavioral edges.

**Category 2 — Structural edges:** Edges that arise from market microstructure — latency, liquidity gaps, cross-market probability inconsistencies, spread arbitrage, market maker absence. These do not depend on predicting event outcomes or reading whale behavior. MEG's v1.5 structural signal modules target this category.

**Category 3 — Contract-design edges:** The least exploited category. Edges that arise from how prediction market contracts are structured and resolved — resolution asymmetry, hazard-rate mispricing, time decay, early resolution premiums, path-dependent probability drift. These require understanding the contract itself, not just monitoring price or order flow. Most bots cannot exploit this category because it requires semantic understanding of resolution criteria and actuarial reasoning about event timing. MEG's v1.5 contract analysis modules target this category.

The combination of all three categories is what makes MEG's edge durable. When behavioral edges are sparse (low whale activity), structural and contract-design edges continue to generate signals independently. The three categories are largely uncorrelated — they fail under different conditions and recover at different times.

---

## 4. Opportunity & Market Context

### Market Scale

- Polymarket processed over **$44 billion in trading volume** in 2025
- Platform valuation of approximately **$9 billion** following a $2 billion investment from Intercontinental Exchange (NYSE parent)
- **86% of Polymarket accounts have negative P&L** — only 0.51% profit more than $1,000
- Top whales enter positions **4–12 hours before major market moves** on average
- Cross-platform arbitrage generated over **$40 million in documented profits** between April 2024 and April 2025
- The single largest documented whale profit: **$85 million** (Théo, 2024 US election, $30M deployed across 11 wallets)

### Why The Window Exists Now

Prediction markets are structurally early. Most participants are casual, slow, and manually trading. Automation adoption is low. Well-built intelligent systems can operate in a relatively inefficient environment — but this window compresses over time as the market matures and institutional participants enter. The correct time to build MEG is now.

### Competitive Landscape

| Tool | Capability | Missing |
|---|---|---|
| Polywhaler | Real-time $10k+ feed, insider detection, Deep Trade PRO | No execution, no scoring, no sizing |
| PolyTrack | Cluster detection, leaderboard, real-time alerts | No execution, no consensus filter, no Kelly |
| WhaleWatch Poly | Large trade monitoring | Minimal analytics, no execution |
| PolyIntel | Telegram alerts, scoring | Telegram-only, no execution |
| PolyCopy | Real-time trader tracking | No execution, no quant layer |
| Chrome extensions | Passive notification | Human action required |

**The universal gap:** Every tool in the ecosystem is observability infrastructure. None close the loop to execution. MEG is the execution layer.

### MEG's Defensible Moat

MEG's moat is not speed — it is intelligence depth. By the time competitors build execution layers, MEG will have months of proprietary whale scoring data, archetype classifications, cluster mappings, and signal performance history that cannot be replicated from scratch. The data flywheel is the moat.

---

## 5. Product Vision & Phases

### Phase 1 — v1: Semi-Autonomous Intelligence Engine (Current Scope)

A private system used exclusively by the core team. MEG monitors Polymarket in real-time, runs all whale trades through the full intelligence pipeline, and surfaces high-confidence trade proposals with complete scoring breakdowns. Operators approve or reject via dashboard or Telegram. Paper trading runs first to validate signal quality before any real capital is deployed.

**Capital:** Paper trading → $1,000–$5,000 live  
**Team:** Krishna + Bowen + Agastya  
**Autonomy:** Human approval required for all trades

### Phase 2 — v2: Full Autonomy

Human approval is removed from the trade flow. MEG executes trades the moment a signal clears all intelligence and risk gates. Cluster detection is live. The system runs 24/7 on AWS and alerts the team only on anomalies and circuit breaker events. Shadow entry strategy enabled for sub-500ms execution from signal detection to filled order.

**Capital:** $5,000–$25,000+  
**Autonomy:** Fully autonomous with hardcoded risk guardrails

### Phase 3 — v3: Public Market Intelligence Platform

MEG's intelligence engine is exposed to external subscribers. Users access MEG's signal feed, whale leaderboard, and optionally connect their wallets for automated copy execution. Monetization through subscription tiers and performance fees.

**Target users:** Non-technical Polymarket traders who want systematic edge without building it themselves

---

## 6. Goals & Success Metrics

### Primary Metrics

| Metric | Target | Measurement |
|---|---|---|
| Signal win rate (paper) | >55% before going live | Closed position P&L |
| Net P&L (live, 3 months) | Positive | Realized + unrealized |
| Bot uptime | >99% | CloudWatch |
| Average slippage vs signal mid | <2% | Per-trade execution log |
| Max single-day drawdown | Never exceeds circuit breaker | Risk controller log |
| Signal false positive rate | <40% reach execution | Signal log FILTERED vs EXECUTED |

### Secondary Metrics

| Metric | Target |
|---|---|
| Whale score prediction accuracy | Lead-lag score correlates >0.6 with actual trade profitability |
| Intent classifier accuracy | >80% correct SIGNAL vs HEDGE vs REBALANCE classification |
| Reputation decay validity | Decayed whales underperform active whales in retrospective analysis |
| Dashboard response time | <200ms for all API endpoints |

### Anti-Goals — What MEG v1 Does NOT Do

- MEG does not trade on fundamental research, news, or LLM predictions in v1
- MEG does not operate on Kalshi or any platform other than Polymarket in v1
- MEG does not make fully autonomous trades in v1 — all trades require human approval
- MEG does not expose any public-facing interface in v1
- MEG does not attempt cluster detection in v1 (v2)
- MEG does not implement shadow entry / sub-500ms execution in v1 (requires v2 autonomy)

---

## 7. User Personas

### The Operator (Krishna / Bowen / Agastya)

Technical builders with Python and AWS experience. Familiar with trading concepts but not professional quants. Primary workflow: check dashboard periodically, review signal log for tuning insights, approve or reject trade proposals via Telegram when away from a screen. Primary concern during paper trading: validating that signal scores actually correlate with trade outcomes. Primary concern during live trading: understanding every loss well enough to improve the system.

Each operator should be able to:
- Read and interpret any signal's full score breakdown
- Update any hot config parameter without help
- Identify from the signal log why a specific trade was filtered or blocked
- Trigger an emergency pause via Telegram in under 10 seconds

### The Future SaaS Subscriber (v3)

A non-technical Polymarket trader generating $500–$5,000/month who wants systematic edge without building infrastructure. Interacts only through a clean UI showing signal feed, suggested trades, and their portfolio performance. Does not need to understand internals. Primary concern: "is this actually making me money."

---

## 8. System Architecture Overview

MEG is organized into five stages: Pre-Filter Gates, Data Layer, Signal Engine, Agent Core, and Execution Layer. Each stage has explicit input/output contracts, is independently testable, and exposes plugin sockets for extensibility. Stages communicate via an internal event bus (Redis pub/sub) — no stage has a direct dependency on another's implementation.

```
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
│  Polygon RPC · Polymarket CLOB API · Whale Wallet Registry      │
│  [SOCKET: Alt data sources — news feeds, Kalshi, sentiment]     │
└──────────────────────────┬──────────────────────────────────────┘
                           │ raw_whale_trade_event
┌──────────────────────────▼──────────────────────────────────────┐
│                    PRE-FILTER GATES                             │
│  Market Quality Filter · Arbitrage Whale Exclusion              │
│  Intent Classifier (SIGNAL / HEDGE / REBALANCE)                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │ qualified_whale_trade_event
┌──────────────────────────▼──────────────────────────────────────┐
│                     SIGNAL ENGINE                               │
│  Lead-Lag Scorer · Reputation Decay · Conviction Ratio          │
│  Kelly Criterion Sizer · Multi-Whale Consensus Filter           │
│  Contrarian Divergence Detector · Entry Ladder Detector         │
│  Whale Archetype Weighter · Signal Decay Timer                  │
│  [SOCKET: Quant modules — news boost, momentum, liquidity shock] │
└──────────────────────────┬──────────────────────────────────────┘
                           │ signal_event (scored + sized)
┌──────────────────────────▼──────────────────────────────────────┐
│                      AGENT CORE                                 │
│  Signal Aggregator · Decision Agent · Position Manager          │
│  Risk Controller · Whale Trap Detector                          │
│  Market Saturation Monitor · Signal Crowding Detector           │
│  [SOCKET: LLM reasoning layer — Claude on Bedrock, v2]          │
└──────────────────────────┬──────────────────────────────────────┘
                           │ trade_proposal (PENDING_APPROVAL in v1)
┌──────────────────────────▼──────────────────────────────────────┐
│                   EXECUTION LAYER                               │
│  Entry Distance Filter · Slippage Guard · Order Router          │
│  Hot Config · Position Exit Manager                             │
│  [SOCKET: Exchange adapters — Kalshi, Manifold, v2]             │
└─────────────────────────────────────────────────────────────────┘
           │                              │
    Dashboard                       Telegram Bot
 (FastAPI + React/TS)           (alerts + approval)
```

### Event Flow — Full Happy Path

1. Whale trade detected on Polygon blockchain ($10k+ default threshold)
2. **Pre-Filter Gate 1 — Market Quality:** Is this market liquid enough, spread tight enough, participant count sufficient? If not → DROP
3. **Pre-Filter Gate 2 — Arbitrage Whale Exclusion:** Is this wallet classified as an arbitrage whale? If yes → DROP
4. **Pre-Filter Gate 3 — Intent Classifier:** Is this trade a SIGNAL, HEDGE, or REBALANCE? If HEDGE or REBALANCE → DROP
5. **Lead-Lag Scorer:** Score wallet by historical early-entry accuracy (with reputation decay applied)
6. **Conviction Ratio:** Weight score by bet_size / wallet_capital
7. **Kelly Sizer:** Calculate optimal position size
8. **Consensus Filter:** Check for 2+ independent qualified whales on same side in rolling window
9. **Entry Ladder Detector:** Check if this wallet is building a ladder pattern (conviction multiplier)
10. **Contrarian Detector:** Check if trade goes against order flow (signal boost)
11. **Archetype Weighter:** Adjust weights based on whale's classified archetype
12. **Signal Decay Timer:** Tag signal with TTL (default 2 hours) — if not executed before TTL, auto-expire
13. **Composite score calculated** — if below 0.45 threshold → LOG as FILTERED, stop
14. **Agent Core — Signal Aggregator:** Combine all scores into final composite
15. **Agent Core — Risk Controller:** Check all five risk gates in priority order
16. **Agent Core — Whale Trap Detector:** Check for rapid entry/exit pattern on this wallet
17. **Agent Core — Market Saturation Monitor:** Check for price velocity spike, order book thinning, trade frequency spike
18. **Agent Core — Signal Crowding Detector:** Check entry distance from whale's actual fill price
19. **Trade proposal generated** with full score breakdown, suggested size, risk check results
20. **Semi-auto:** Proposal sent to dashboard approval queue + Telegram alert
21. **Operator approves** → passes to Execution Layer
22. **Entry Distance Filter:** Re-check distance from whale fill. If >6% → EXPIRE
23. **Slippage Guard:** Check current spread + price drift. If exceeds thresholds → CANCEL
24. **Order Router:** Place limit order at mid + taker spread
25. **Position Manager:** Track position, monitor contributing whale exits, apply take-profit/stop-loss

### Latency Budget (v1)

| Step | Target |
|---|---|
| On-chain detection → pre-filter completion | <50ms |
| Pre-filter → signal scoring | <100ms |
| Signal scoring → composite + agent decision | <50ms |
| Agent decision → human notification | <200ms |
| Human approval → order placed | <500ms |
| **Total system latency (excl. human)** | **<400ms** |

Latency is a near-future optimization priority. Correctness and signal quality take precedence in v1.

---

## 9. Feature Specifications — v1

### 9.1 Pre-Filter Gates

Pre-filter gates run before any signal scoring. They are cheap, fast checks that eliminate low-quality events before they consume computational resources or human attention.

#### Gate 1 — Market Quality Filter

**Purpose:** Prevent MEG from ever trading in illiquid, structurally risky, or thin markets that generate fake signals and amplify losses.

**Filter criteria (all must pass):**

```python
class MarketQualityFilter:
    def passes(self, market: MarketState, config: Config) -> FilterResult:
        checks = [
            market.volume_24h_usdc >= config.mq_min_volume_24h,        # default $50k
            market.liquidity_usdc >= config.mq_min_liquidity,           # default $10k
            market.spread <= config.mq_max_spread,                      # default 0.06
            market.participant_count >= config.mq_min_participants,      # default 20
            market.days_to_resolution >= config.mq_min_days_to_resolve, # default 1
            market.resolution_source not in config.flagged_sources,
        ]
        passed = all(checks)
        return FilterResult(passed=passed, failed_checks=[c for c in checks if not c])
```

Markets that fail quality checks are cached in Redis with a 1-hour TTL — they won't be re-evaluated until the cache expires, saving computational overhead.

#### Gate 2 — Arbitrage Whale Exclusion

**Purpose:** Remove wallets whose trading pattern indicates they are arbitrage traders, not directional signal traders. Arbitrage wallets generate high volume, trade both sides, and carry no information edge for directional trading.

**Detection heuristics:**
- Wallet has placed trades on both YES and NO of the same market within 24 hours, more than 3 times in the past 30 days
- Wallet's average hold time is under 2 hours
- Wallet has >80% of volume in markets with tight spreads (classic arb behavior)

**Action:** Tag wallet as `ARCHETYPE=ARBITRAGE` in wallet registry. All events from this wallet are dropped at pre-filter. Wallet is removed from leaderboard's directional signal rankings.

#### Gate 3 — Intent Classifier

**Purpose:** The most important pre-filter. Classify every whale trade as SIGNAL, HEDGE, or REBALANCE. Only SIGNAL trades proceed to the signal engine.

**Classification logic:**

```python
def classify_intent(event: WhaleTradedEvent, wallet_history: WalletHistory) -> Intent:
    recent_trades = wallet_history.get_recent(market_id=event.market_id, hours=6)
    
    # REBALANCE: Rapid opposite trades in same market
    opposite_trades = [t for t in recent_trades if t.outcome != event.outcome]
    if opposite_trades and (event.timestamp - opposite_trades[-1].timestamp).seconds < 1800:
        return Intent.REBALANCE
    
    # HEDGE: Small trade relative to existing position in correlated market
    correlated_exposure = wallet_history.get_correlated_exposure(event.market_id)
    if correlated_exposure > 0 and event.size_usdc < correlated_exposure * 0.3:
        return Intent.HEDGE
    
    # LADDER BUILD: Trade in same direction as recent trades (conviction building)
    same_direction = [t for t in recent_trades if t.outcome == event.outcome]
    if same_direction and all(t.size_usdc <= event.size_usdc for t in same_direction):
        return Intent.SIGNAL_LADDER  # Special: high-conviction signal
    
    # Default: directional signal
    return Intent.SIGNAL

```

**Output attached to event:** `intent: SIGNAL | SIGNAL_LADDER | HEDGE | REBALANCE`  
Only `SIGNAL` and `SIGNAL_LADDER` proceed. `SIGNAL_LADDER` carries a conviction multiplier of +0.15 on composite score.

---

### 9.2 Data Layer

#### 9.2.1 Polygon On-Chain Feed

**Purpose:** Stream all Polymarket-related transactions from the Polygon blockchain in real-time and detect whale-sized activity above the configurable threshold.

**Implementation:**
- Connect to Polygon RPC via websocket subscription to the Polymarket CLOB contract (`0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E`)
- Filter transactions by value against configurable `whale_tracking_threshold_usdc` (default $10,000, hot-configurable)
- Parse transaction data: wallet address, market ID, direction (YES/NO), size in USDC, timestamp, tx hash, block number
- Emit `raw_whale_trade_event` to Redis pub/sub

**Raw event schema:**
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

**Failure handling:**
- RPC node down: exponential backoff reconnect (1s, 2s, 4s, 8s, max 60s), Telegram alert, ring buffer to avoid missed events
- Missed blocks on reconnect: reconcile against Polymarket REST API for the gap period
- Malformed transaction: log with full context, skip, never crash feed

**RPC provider selection:** Alchemy preferred for reliability and websocket stability. Fallback to QuickNode. Never rely on public RPC endpoints for production — rate limits make them unsuitable for persistent websocket connections. (See Open Questions OQ-01)

#### 9.2.2 Polymarket CLOB API

**Purpose:** Real-time order book data for all active markets — bid, ask, mid-price, depth, volume — used by the Slippage Guard, Contrarian Detector, Market Quality Filter, and Saturation Monitor.

**Implementation:**
- Official `py-clob-client` SDK for order book subscriptions and order placement
- Maintain active websocket subscriptions for all markets with whale activity in the past 24 hours
- Cache latest market state in Redis (sub-millisecond lookup):

```
market:{id}:mid_price       → float
market:{id}:bid             → float
market:{id}:ask             → float
market:{id}:spread          → float
market:{id}:volume_24h      → float
market:{id}:liquidity       → float
market:{id}:participants    → int
market:{id}:last_updated_ms → int
market:{id}:price_history   → sorted set (timestamp → price, last 24h)
```

- Poll for new market listings every 15 minutes and add to active subscription list
- Maintain a 1-hour price history per active market for momentum calculations

#### 9.2.3 Whale Wallet Registry

**Purpose:** Persistent database of all tracked whale wallets with complete trade history, computed performance scores, archetype classifications, and cluster relationships.

**Full PostgreSQL schema:**

```sql
-- Core wallet identity and classification
CREATE TABLE wallets (
    address             VARCHAR(42) PRIMARY KEY,
    first_seen_at       TIMESTAMP NOT NULL,
    last_active_at      TIMESTAMP NOT NULL,
    total_volume_usdc   DECIMAL(18,2) DEFAULT 0,
    total_trades        INTEGER DEFAULT 0,
    total_capital_usdc  DECIMAL(18,2),          -- tracked wallet balance
    is_tracked          BOOLEAN DEFAULT FALSE,
    archetype           VARCHAR(32),             -- INFORMATION | MOMENTUM | ARBITRAGE | MANIPULATOR
    cluster_id          VARCHAR(64),             -- v2: populated by cluster detection
    funding_wallet      VARCHAR(42),             -- v2: parent wallet if known
    is_excluded         BOOLEAN DEFAULT FALSE,   -- ARBITRAGE or MANIPULATOR wallets
    exclusion_reason    TEXT,
    notes               TEXT
);

-- Complete per-trade history
CREATE TABLE trades (
    id                  SERIAL PRIMARY KEY,
    wallet_address      VARCHAR(42) REFERENCES wallets(address),
    market_id           VARCHAR(128) NOT NULL,
    outcome             VARCHAR(8) NOT NULL,
    size_usdc           DECIMAL(18,2) NOT NULL,
    entry_price         DECIMAL(6,4) NOT NULL,
    exit_price          DECIMAL(6,4),
    entry_at            TIMESTAMP NOT NULL,
    exit_at             TIMESTAMP,
    resolved_at         TIMESTAMP,
    resolution          VARCHAR(8),              -- YES | NO | INVALID | UNRESOLVED
    pnl_usdc            DECIMAL(18,2),
    pnl_pct             DECIMAL(8,4),
    tx_hash_entry       VARCHAR(66),
    tx_hash_exit        VARCHAR(66),
    market_category     VARCHAR(64),
    intent_classified   VARCHAR(32),             -- SIGNAL | SIGNAL_LADDER | HEDGE | REBALANCE
    price_at_market_end DECIMAL(6,4),
    lead_time_hours     DECIMAL(8,2)             -- hours before market moved >5% in trade direction
);

-- Computed scores (daily batch + real-time top-50 refresh)
CREATE TABLE wallet_scores (
    wallet_address          VARCHAR(42) REFERENCES wallets(address),
    computed_at             TIMESTAMP NOT NULL,
    win_rate                DECIMAL(5,4),
    avg_lead_time_hours     DECIMAL(8,2),
    lead_time_score         DECIMAL(5,4),        -- normalized vs all qualified whales
    roi_30d                 DECIMAL(8,4),
    roi_90d                 DECIMAL(8,4),
    roi_all_time            DECIMAL(8,4),
    total_closed_positions  INTEGER,
    consistency_score       DECIMAL(5,4),        -- % of months with positive P&L
    avg_conviction_ratio    DECIMAL(6,4),        -- avg bet_size / wallet_capital
    reputation_decay_factor DECIMAL(5,4),        -- exp(-time_since_last_good_trade / tau)
    composite_whale_score   DECIMAL(5,4),        -- final scored rank
    is_qualified            BOOLEAN,
    category_scores         JSONB,               -- {politics: 0.71, sports: 0.55, crypto: 0.62}
    PRIMARY KEY (wallet_address, computed_at)
);

-- Trap detection history
CREATE TABLE whale_trap_events (
    id                  SERIAL PRIMARY KEY,
    wallet_address      VARCHAR(42) REFERENCES wallets(address),
    market_id           VARCHAR(128),
    detected_at         TIMESTAMP NOT NULL,
    entry_size_usdc     DECIMAL(18,2),
    exit_size_usdc      DECIMAL(18,2),
    time_delta_minutes  INTEGER,
    confidence          DECIMAL(5,4),
    score_penalty       DECIMAL(5,4)
);

-- Signal performance tracking (for score calibration)
CREATE TABLE signal_outcomes (
    signal_id           VARCHAR(64) PRIMARY KEY,
    fired_at            TIMESTAMP NOT NULL,
    composite_score     DECIMAL(5,4),
    lead_lag_score      DECIMAL(5,4),
    consensus_score     DECIMAL(5,4),
    kelly_score         DECIMAL(5,4),
    divergence_score    DECIMAL(5,4),
    was_executed        BOOLEAN,
    pnl_usdc            DECIMAL(18,2),
    was_profitable      BOOLEAN,
    exit_reason         VARCHAR(64)
);
```

**Wallet qualification thresholds (all hot-configurable):**

| Threshold | Default | Rationale |
|---|---|---|
| Minimum win rate | 55% | Statistical significance floor |
| Minimum closed positions | 50 | Enough history to score reliably |
| Minimum total volume | $100,000 USDC | Skin-in-the-game filter |
| Minimum profitable months (trailing 6) | 3 | Consistency not just total P&L |
| Maximum archetype | Not ARBITRAGE or MANIPULATOR | Intent filter |

**Bootstrap strategy:** Seed the registry using Polymarket's public leaderboard, Dune Analytics Polymarket dashboards, Bitquery on-chain data, and known high-profile wallet addresses from public research (Domer, Théo's documented accounts). Do not depend on scraping any third-party tool UI.

**Wallet capital tracking:** Query wallet USDC balance via Polygon RPC on a daily schedule for all tracked wallets. Store as `total_capital_usdc` in the wallets table. Used for conviction ratio calculation.

---

### 9.3 Signal Engine

The Signal Engine receives `qualified_whale_trade_event` objects from the pre-filter gates and produces `signal_event` objects carrying a composite intelligence score and a recommended position size. Six modules run in parallel, each scoring independently.

#### 9.3.1 Lead-Lag Scorer with Reputation Decay

**Purpose:** Score each whale by how consistently and how early they enter positions before the market moves in their direction. Apply exponential decay to downweight whales whose edge has gone stale.

**Reputation decay formula:**
```python
def reputation_decay(wallet: WalletScore, config: Config) -> float:
    days_since_last_good_trade = (now() - wallet.last_profitable_trade_at).days
    tau = config.reputation_decay_tau_days  # default: 30 days
    return math.exp(-days_since_last_good_trade / tau)

# Effect:
# 0 days inactive  → decay = 1.00 (full score)
# 30 days inactive → decay = 0.37 (significant reduction)
# 60 days inactive → decay = 0.14 (nearly excluded)
# 90 days inactive → decay = 0.05 (effectively excluded)
```

**Lead-lag score formula:**
```python
def lead_lag_score(wallet: WalletScore, event: WhaleTradedEvent) -> float:
    # Component 1: How early do they enter vs the market average?
    avg_lead_normalized = normalize(wallet.avg_lead_time_hours, 
                                     all_qualified_wallets_lead_times)
    
    # Component 2: Directional accuracy in this specific market category
    category_win_rate = wallet.category_scores.get(event.market_category, wallet.win_rate)
    
    # Component 3: Long-term consistency
    consistency = wallet.consistency_score
    
    # Component 4: Recency weight (30d vs all-time)
    recency = wallet.roi_30d / (wallet.roi_all_time + 0.001)
    recency_normalized = sigmoid(recency)
    
    raw_score = (
        avg_lead_normalized  * 0.35 +
        category_win_rate    * 0.35 +
        consistency          * 0.20 +
        recency_normalized   * 0.10
    )
    
    # Apply reputation decay
    decayed_score = raw_score * reputation_decay(wallet, config)
    
    return clamp(decayed_score, 0.0, 1.0)
```

**Minimum gate:** If `lead_lag_score < 0.40` after decay, drop. Do not proceed.

**Output:** `lead_lag_score` ∈ [0.0, 1.0]

#### 9.3.2 Conviction Ratio Modifier

**Purpose:** Weight the signal by what fraction of the whale's total tracked capital they are committing. A $10k bet from a $10M wallet expresses different conviction than a $500k bet from the same wallet.

```python
def conviction_ratio(event: WhaleTradedEvent, wallet: Wallet) -> float:
    if not wallet.total_capital_usdc or wallet.total_capital_usdc == 0:
        return 0.50  # default if capital unknown
    
    ratio = event.size_usdc / wallet.total_capital_usdc
    
    # Normalize: 1% commitment = 0.2 score, 5% = 0.5, 15%+ = 0.9+
    return clamp(sigmoid((ratio - 0.05) * 20), 0.10, 1.00)
```

**Output:** `conviction_score` ∈ [0.0, 1.0] — used as a multiplier on the composite score, not a standalone signal.

#### 9.3.3 Kelly Criterion Sizer

**Purpose:** Calculate the mathematically optimal position size for the signal. Never over-bet. Never under-bet.

**Formula:**
```python
def kelly_size(event: WhaleTradedEvent, wallet: WalletScore, 
               portfolio: PortfolioState, config: Config) -> KellyResult:
    
    win_prob = wallet.category_scores.get(event.market_category, wallet.win_rate)
    entry_price = event.market_price_at_trade
    
    # For a binary market: odds of winning = (1 - price) / price
    odds_multiplier = (1 - entry_price) / entry_price
    loss_prob = 1 - win_prob
    
    # Full Kelly fraction
    kelly_fraction = (win_prob * odds_multiplier - loss_prob) / odds_multiplier
    
    # Apply fractional Kelly (default: 0.25 — quarter Kelly)
    fractional_kelly = kelly_fraction * config.kelly_fractional_multiplier
    
    # Raw suggested size
    raw_size = fractional_kelly * portfolio.available_capital_usdc
    
    # Hard cap: never exceed max_single_trade_pct of portfolio
    max_size = portfolio.total_value_usdc * config.max_single_trade_pct
    final_size = min(raw_size, max_size)
    
    # Kelly confidence: how positive is the expected value?
    kelly_confidence = clamp(kelly_fraction * 3, 0.0, 1.0)
    
    return KellyResult(
        suggested_size_usdc=final_size,
        kelly_fraction=kelly_fraction,
        fractional_kelly=fractional_kelly,
        confidence=kelly_confidence
    )
```

**Output:** `suggested_size_usdc`, `kelly_fraction`, `kelly_confidence` ∈ [0.0, 1.0]

#### 9.3.4 Multi-Whale Consensus Filter

**Purpose:** Boost confidence dramatically when multiple independent, high-scoring whales take the same side of the same market within a rolling time window. This is the strongest noise filter in the system.

**Rolling window logic:**
```python
def consensus_score(event: WhaleTradedEvent, config: Config) -> ConsensusResult:
    # Pull all qualified whale trades in same market + direction in window
    window_trades = redis.get_window(
        key=f"consensus:{event.market_id}:{event.outcome}",
        window_hours=config.consensus_window_hours  # default: 4h
    )
    
    # Filter for independence: basic check (full cluster detection in v2)
    # Heuristic: different funding wallets
    independent_wallets = deduplicate_by_funding_wallet(window_trades)
    qualified_count = len([w for w in independent_wallets if w.is_qualified])
    
    # Sigmoid scaling: 1 whale = 0.27, 2 = 0.50, 3 = 0.73, 4+ = 0.88+
    threshold = config.consensus_min_whales  # default: 2
    sensitivity = config.consensus_sensitivity  # default: 1.5
    score = sigmoid((qualified_count - threshold) * sensitivity)
    
    return ConsensusResult(
        score=score,
        whale_count=qualified_count,
        contributing_wallets=[w.address for w in independent_wallets]
    )
```

**Important design decision:** A single whale with no confirmation still produces a signal (consensus_score ~0.27) — it is not blocked. The composite score will naturally be low, likely below the execution threshold. This preserves the ability to paper-trade single-whale signals and observe whether they correlate with outcomes.

**Output:** `consensus_score` ∈ [0.0, 1.0], `whale_count`, `contributing_wallets`

#### 9.3.5 Contrarian Divergence Detector

**Purpose:** Boost signal confidence when a whale enters against prevailing order flow. Information whales are often contrarian — they're buying what the market is selling because they know something the market doesn't.

```python
def divergence_score(event: WhaleTradedEvent, market: MarketState) -> float:
    # Component 1: Order book imbalance
    # If whale is buying YES but ask_volume >> bid_volume: strongly contrarian
    if event.outcome == "YES":
        book_imbalance = market.ask_volume / (market.bid_volume + 0.001)
    else:
        book_imbalance = market.bid_volume / (market.ask_volume + 0.001)
    order_flow_divergence = clamp((book_imbalance - 1) / 3, 0.0, 1.0)
    
    # Component 2: Price momentum inverse
    # If price has moved <1% in trade direction: contrarian (no momentum)
    # If price has moved >5% in trade direction: late follower
    price_1h_change = market.get_price_change(hours=1, direction=event.outcome)
    momentum_inverse = clamp(1 - (price_1h_change / 0.08), 0.0, 1.0)
    
    score = (order_flow_divergence * 0.60) + (momentum_inverse * 0.40)
    is_contrarian = score > 0.55
    
    return DivergenceResult(score=score, is_contrarian=is_contrarian)
```

**Output:** `divergence_score` ∈ [0.0, 1.0], `is_contrarian` bool

#### 9.3.6 Entry Ladder Detector

**Purpose:** Detect when a whale is building a position with escalating size across multiple trades in the same market — a behavioral pattern indicating increasing conviction.

```python
def ladder_detection(event: WhaleTradedEvent, wallet_history: WalletHistory,
                     config: Config) -> LadderResult:
    
    recent = wallet_history.get_recent_same_direction(
        market_id=event.market_id,
        outcome=event.outcome,
        hours=config.ladder_window_hours  # default: 6h
    )
    
    if len(recent) < 2:
        return LadderResult(is_ladder=False, multiplier=1.0)
    
    sizes = [t.size_usdc for t in recent] + [event.size_usdc]
    is_monotonic = all(sizes[i] <= sizes[i+1] for i in range(len(sizes)-1))
    
    if is_monotonic and len(sizes) >= 3:
        trade_count = len(sizes)
        total_committed = sum(sizes)
        # Each additional rung adds 0.15 to conviction multiplier
        multiplier = 1.0 + (trade_count - 2) * config.ladder_conviction_per_rung  # default: 0.15
        return LadderResult(
            is_ladder=True, 
            trade_count=trade_count,
            total_committed_usdc=total_committed,
            multiplier=clamp(multiplier, 1.0, 2.0)  # max 2x
        )
    
    return LadderResult(is_ladder=False, multiplier=1.0)
```

**Output:** `is_ladder` bool, `ladder_multiplier` ∈ [1.0, 2.0], applied to composite score post-calculation.

#### 9.3.7 Whale Archetype Weighter

**Purpose:** Adjust signal weights based on the whale's classified archetype. Information whales should receive highest weight; momentum whales should receive discounted weight; arbitrage whales should already be excluded.

**Archetype definitions:**

| Archetype | Entry timing | Hold period | Trade frequency | Signal weight |
|---|---|---|---|---|
| INFORMATION | Hours before move | Long (days) | Rare | 1.0x (full weight) |
| MOMENTUM | After price moves | Short (hours) | Moderate | 0.65x (discounted) |
| ARBITRAGE | Both sides | Very short | Very high | EXCLUDED (pre-filter) |
| MANIPULATOR | Rapid entry/exit | Very short | Variable | EXCLUDED (trapped) |

**Classification criteria:**
```python
def classify_archetype(wallet: WalletScore) -> str:
    if wallet.avg_lead_time_hours > 4 and wallet.avg_hold_time_hours > 24:
        return "INFORMATION"
    elif wallet.avg_lead_time_hours < 1 and wallet.trade_frequency_daily > 5:
        return "MOMENTUM"
    elif wallet.pct_trades_both_sides > 0.40:
        return "ARBITRAGE"
    else:
        return "INFORMATION"  # default to full weight if unclear
```

**Output:** Archetype label applied as `signal_weight_multiplier` to composite score.

#### 9.3.8 Signal Decay Timer (Half-Life-Aware)

**Purpose:** Every signal has a time-to-live based on its estimated information half-life. A signal generated at 2am that sits in the approval queue until 9am has already been priced in by the market. Stale signals must expire automatically — and the TTL should match the half-life of the signal type, not a uniform fixed value.

**The problem with fixed TTL:** A uniform 2-hour TTL is miscalibrated for most signal types. A whale-reaction signal (half-life: ~10 minutes) should expire in 20-30 minutes. A resolution asymmetry signal (half-life: days) should live for 48+ hours. A fixed 2-hour TTL cuts off valid long-duration signals and keeps invalid short-duration signals alive too long.

```python
# Half-life baseline by signal type (in minutes)
HALF_LIFE_BASELINES = {
    SignalType.WHALE_REACTION:        15,
    SignalType.EVENT_CASCADE:         90,
    SignalType.BEHAVIORAL_DRIFT:     480,   # 8 hours
    SignalType.RESOLUTION_ASYMMETRY: 4320,  # 3 days
    SignalType.CROSS_MARKET_ARB:      10,
    SignalType.CONTRACT_HAZARD_RATE: 2880,  # 2 days
    SignalType.ORACLE_LATENCY:        20,
    SignalType.MARKET_MAKER_SPREAD:   15,
}

def estimate_half_life(signal: SignalEvent, market: MarketState, 
                        config: Config) -> float:
    """Returns estimated half-life in minutes, adjusted for market conditions."""
    base = HALF_LIFE_BASELINES.get(signal.signal_type, 
                                    config.signal_default_half_life_minutes)
    
    # Compression factors: shorten half-life when information is spreading fast
    if market.trades_per_minute_5min > market.avg_tpm_baseline * 2:
        base *= 0.6   # fast repricing underway
    if signal.social_activity_spike:
        base *= 0.5   # information spreading publicly
    if signal.whale_count >= 4:
        base *= 0.7   # many whales already in, market adjusting fast
    
    # Extension factors: lengthen half-life when market is slow to reprice
    if market.liquidity_usdc > config.deep_liquidity_threshold:
        base *= 1.3   # deep liquidity slows repricing
    if market.trades_per_minute_5min < market.avg_tpm_baseline * 0.5:
        base *= 1.4   # unusually thin activity
    
    return max(base, config.signal_min_half_life_minutes)  # floor: 5 min

def half_life_adjusted_size(base_size: float, signal: SignalEvent,
                              half_life_minutes: float) -> float:
    """Reduce position size as edge decays. Same math as reputation decay."""
    elapsed_minutes = (now() - signal.fired_at).seconds / 60
    remaining_edge_fraction = math.exp(
        -elapsed_minutes * math.log(2) / half_life_minutes
    )
    return base_size * remaining_edge_fraction

class SignalDecayTimer:
    def tag_signal(self, signal: SignalEvent, market: MarketState,
                   config: Config) -> SignalEvent:
        half_life = estimate_half_life(signal, market, config)
        # TTL = 3× half-life: edge is ~12% of original at expiry
        ttl_minutes = half_life * config.signal_ttl_half_life_multiplier  # default: 3.0
        signal.estimated_half_life_minutes = half_life
        signal.expires_at = signal.fired_at + timedelta(minutes=ttl_minutes)
        signal.status = SignalStatus.PENDING
        return signal
    
    async def monitor_expiry(self):
        """Background task: expire pending signals past TTL."""
        while True:
            expired = await db.get_signals_past_ttl()
            for signal in expired:
                signal.status = SignalStatus.EXPIRED
                await notify_telegram(
                    f"Signal {signal.signal_id} expired "
                    f"(half-life: {signal.estimated_half_life_minutes:.0f}min, "
                    f"age at expiry: {signal.age_at_expiry_minutes:.0f}min)"
                )
            await asyncio.sleep(30)
```

**Half-life is also used at execution time** to adjust the final position size (see `half_life_adjusted_size` above). A signal that has been sitting in the approval queue for 80% of its estimated half-life gets proportionally smaller position sizing — the edge has been decaying the whole time.

Signals that expire are logged as EXPIRED with their half-life estimate and age — never REJECTED. This distinction is critical for signal performance analysis and half-life calibration over time.

#### 9.3.9 Composite Score Calculation

All module scores are combined into a single `composite_signal_score`:

```python
def composite_score(scores: SignalScores, archetype_multiplier: float,
                    ladder_multiplier: float, conviction_ratio: float) -> float:
    
    base_score = (
        scores.lead_lag     * 0.35 +
        scores.consensus    * 0.30 +
        scores.kelly        * 0.20 +
        scores.divergence   * 0.15
    )
    
    # Apply multipliers
    adjusted = base_score * archetype_multiplier * ladder_multiplier
    
    # Conviction ratio as a blend modifier (not a full multiplier — prevents over-leverage)
    final = adjusted * 0.85 + conviction_ratio * 0.15
    
    return clamp(final, 0.0, 1.0)
```

**Minimum execution threshold:** `composite_score >= 0.45` (configurable). Signals below this are logged as FILTERED.

**Ideal signal checklist** — the highest-scoring signals will exhibit:

```
Early whale entry (high lead-lag)        → +0.35 max
Second+ whale confirmation (consensus)   → +0.30 max  
Contrarian position (divergence)         → +0.15 max
Strong Kelly EV (kelly confidence)       → +0.20 max
Information archetype                    → 1.0x multiplier
Entry ladder detected                    → up to 2.0x multiplier
High conviction ratio                    → +0.15 blend boost
─────────────────────────────────────────────────────────
Theoretical maximum:                     → 1.0 (rare, high conviction)
Practical strong signal:                 → 0.65–0.80
Minimum for execution:                   → 0.45
```

**Full signal event emitted:**
```json
{
  "signal_id": "meg_sig_abc123",
  "market_id": "will-trump-win-2026-midterms",
  "outcome": "YES",
  "composite_score": 0.74,
  "lead_lag_score": 0.81,
  "consensus_score": 0.73,
  "kelly_confidence": 0.65,
  "divergence_score": 0.60,
  "archetype_multiplier": 1.0,
  "ladder_multiplier": 1.30,
  "conviction_ratio": 0.72,
  "suggested_size_usdc": 340.00,
  "kelly_fraction": 0.068,
  "triggering_wallet": "0x...",
  "contributing_wallets": ["0x...", "0x..."],
  "whale_count": 3,
  "is_contrarian": true,
  "is_ladder": true,
  "ladder_trade_count": 3,
  "market_price_at_signal": 0.43,
  "intent": "SIGNAL_LADDER",
  "whale_archetype": "INFORMATION",
  "signal_type": "EVENT_CASCADE",
  "estimated_half_life_minutes": 85,
  "expires_at": "2026-03-07T06:07:00Z",
  "fired_at": "2026-03-07T02:22:00Z",
  "saturation_score": 0.12,
  "saturation_size_multiplier": 1.0,
  "trap_warning": false,
  "status": "PENDING"
}
```

---

### 9.4 Agent Core

The Agent Core receives scored signal events and makes the final execution decision. It also manages open positions, monitors for whale exit signals, detects market saturation, and enforces all portfolio-level risk rules.

#### 9.4.1 Decision Agent

**Purpose:** Apply final decision logic before generating a trade proposal. In v1, this is a deterministic rules engine. In v2, an optional Claude on Bedrock reasoning layer can be plugged in for high-conviction signals.

```python
def evaluate(signal: SignalEvent, portfolio: PortfolioState, 
             config: Config) -> Decision:
    
    # Hard blocks — evaluated in priority order
    if portfolio.daily_pnl_usdc <= config.circuit_breaker_daily_loss_usdc:
        return Decision.BLOCK("circuit_breaker_triggered")
    
    if config.system_paused:
        return Decision.BLOCK("system_paused")
    
    if signal.market_id in config.blacklisted_markets:
        return Decision.BLOCK("market_blacklisted")
    
    if portfolio.get_market_exposure_pct(signal.market_id) >= config.max_market_exposure_pct:
        return Decision.BLOCK("max_market_exposure_reached")
    
    if portfolio.total_exposure_pct >= config.max_portfolio_exposure_pct:
        return Decision.BLOCK("max_portfolio_exposure_reached")
    
    if portfolio.has_open_position(signal.market_id, signal.outcome):
        return Decision.BLOCK("duplicate_position")
    
    # Soft adjustments
    if signal.suggested_size_usdc > portfolio.available_capital * config.max_single_trade_pct:
        signal.suggested_size_usdc = portfolio.available_capital * config.max_single_trade_pct
    
    return Decision.PROPOSE(signal)
```

#### 9.4.2 Whale Trap Detector

**Purpose:** Detect when a whale who triggered a pending signal has begun rapidly exiting — indicating the signal may have been a deliberate pump designed to attract followers.

```python
def detect_trap(wallet: str, market_id: str, entry_event: WhaleTradedEvent,
                config: Config) -> TrapResult:
    
    recent_sells = get_sells(wallet, market_id, 
                             since=entry_event.timestamp_ms,
                             minutes=config.trap_window_minutes)  # default: 30min
    
    total_sold = sum(t.size_usdc for t in recent_sells)
    entry_size = entry_event.size_usdc
    
    if total_sold >= entry_size * config.trap_exit_threshold:  # default: 0.5
        time_delta = recent_sells[-1].timestamp - entry_event.timestamp
        
        # Rapid exit confirmed — penalize wallet score
        apply_score_penalty(wallet, config.trap_score_penalty)  # default: -0.20
        
        # If repeated behavior: flag as MANIPULATOR
        trap_count = get_trap_count(wallet)
        if trap_count >= config.trap_manipulator_threshold:  # default: 3
            flag_as_manipulator(wallet)
        
        return TrapResult(
            is_trap=True,
            confidence=min(total_sold / entry_size, 1.0),
            time_delta_minutes=time_delta.seconds // 60
        )
    
    return TrapResult(is_trap=False)
```

**Effect on pending signals:** If a trap is detected for the triggering wallet of a PENDING signal, that signal is immediately set to status `TRAP_DETECTED` and the operator is notified. The signal is not auto-cancelled (operator decides), but a strong warning is surfaced.

#### 9.4.3 Market Saturation Monitor

**Purpose:** Detect when a market is becoming overcrowded with reactive copy traders following the same signal. When saturation is detected, position size is automatically reduced — the signal is not blocked.

```python
def saturation_score(market: MarketState, config: Config) -> SaturationResult:
    
    # Signal 1: Price velocity spike (abnormal speed of price movement)
    recent_price_change = market.price_change_pct(minutes=5)
    baseline_velocity = market.avg_price_change_pct_5min_30d
    velocity_spike = recent_price_change / (baseline_velocity + 0.001)
    normalized_velocity = clamp((velocity_spike - 1) / 4, 0.0, 1.0)
    
    # Signal 2: Order book thinning (ask side depleting)
    ask_depth_pct_remaining = market.current_ask_depth / market.baseline_ask_depth
    book_thinning = clamp(1 - ask_depth_pct_remaining, 0.0, 1.0)
    
    # Signal 3: Trade frequency spike (abnormal trades per minute)
    current_tpm = market.trades_per_minute_5min
    baseline_tpm = market.avg_trades_per_minute_30d
    freq_spike = clamp((current_tpm / (baseline_tpm + 0.001) - 1) / 5, 0.0, 1.0)
    
    score = (normalized_velocity * 0.40 + book_thinning * 0.35 + freq_spike * 0.25)
    
    # Size reduction: proportional to saturation
    if score > config.saturation_threshold:  # default: 0.60
        size_multiplier = 1 - ((score - config.saturation_threshold) * 
                                config.saturation_size_reduction_sensitivity)
        size_multiplier = clamp(size_multiplier, 0.25, 1.0)  # never reduce below 25%
    else:
        size_multiplier = 1.0
    
    return SaturationResult(score=score, size_multiplier=size_multiplier)
```

#### 9.4.4 Position Manager

**Purpose:** Track all open positions, monitor for whale exit signals, and execute take-profit / stop-loss logic.

**Position lifecycle:**
1. `PENDING_APPROVAL` → operator approves → `OPENING`
2. Order confirmed on CLOB → `OPEN`
3. Take-profit price reached → `PENDING_EXIT` (or auto-exit for TP if configured)
4. Stop-loss price reached → `PENDING_EXIT` (auto-exit for SL in v1)
5. Contributing whale detected selling → `WHALE_EXIT_FLAGGED`
6. Operator approves exit → `CLOSING`
7. Exit confirmed → `CLOSED`

**Trailing take-profit (drift continuation):** When post-signal drift is detected — price moving steadily in the direction of the trade with no saturation indicators and no whale exit — the take-profit threshold trails upward dynamically rather than sitting fixed at +40%. This captures the full drift move rather than exiting prematurely in the middle of an ongoing information cascade.

```python
def update_trailing_tp(position: Position, market: MarketState,
                        config: Config) -> Position:
    if not config.position_trailing_tp_enabled:
        return position
    
    # Drift continuation conditions: price moving in right direction,
    # no saturation, no whale exit, signal half-life not yet exhausted
    price_drifting = (
        market.price_change_pct(hours=1, direction=position.outcome) > 0.005
    )
    no_saturation = position.saturation_score_at_entry < config.saturation_threshold
    half_life_remaining = position.signal_half_life_pct_remaining > 0.25
    
    if price_drifting and no_saturation and not position.whale_exit_detected \
            and half_life_remaining:
        # Trail TP upward: lock in new floor 10% below current price
        new_tp = market.mid_price * (1 - config.trailing_tp_floor_pct)  # default: 0.10
        if new_tp > position.take_profit_price:
            position.take_profit_price = new_tp
    
    return position
```

**Fair-value-adjusted entry distance:** The standard entry distance filter uses the whale's fill price as reference. For markets with known strong drift patterns, an optional fair value estimate can replace the reference point — calculated from composite signal score and historical drift magnitude for this whale archetype and market category. This prevents MEG from blocking valid late-stage drift entries that still have significant upside remaining.

```python
def fair_value_estimate(signal: SignalEvent, historical_drift: DriftStats) -> float:
    """Estimate where price should move given this signal strength and archetype."""
    base_drift = historical_drift.avg_total_drift_pct_for_archetype(
        signal.whale_archetype, signal.market_category
    )
    score_adjusted = base_drift * signal.composite_score
    return signal.market_price_at_signal + score_adjusted

# In entry distance check: if config.use_fair_value_reference is True,
# compare current price to fair_value_estimate rather than whale fill price.
# This widens valid entry window for high-conviction, high-drift signals.
```

**Whale exit detection:** When any contributing whale for an open position begins selling their position, emit `WHALE_EXIT_SIGNAL` event. This event:
- Flags the position as `WHALE_EXIT_FLAGGED`
- Sends Telegram alert with context (which whale, how much they sold, current P&L)
- Can be treated as a signal peak — the information edge may be dissipating
- Does NOT automatically close the position in v1 (operator decides)

**Position state schema:**
```json
{
  "position_id": "meg_pos_xyz789",
  "market_id": "...",
  "outcome": "YES",
  "entry_price": 0.43,
  "current_price": 0.54,
  "size_usdc": 340.00,
  "shares": 790.70,
  "unrealized_pnl_usdc": 86.97,
  "unrealized_pnl_pct": 0.256,
  "entry_signal_id": "meg_sig_abc123",
  "contributing_whales": ["0x...", "0x..."],
  "whale_archetype": "INFORMATION",
  "opened_at": "2026-03-07T02:28:00Z",
  "take_profit_price": 0.60,
  "stop_loss_price": 0.32,
  "whale_exit_detected": false,
  "saturation_score_at_entry": 0.12,
  "status": "OPEN"
}
```

---

### 9.5 Execution Layer

#### 9.5.1 Entry Distance Filter

**Purpose:** Pre-execution check that validates the current market price has not moved too far from the whale's original fill price. Prevents MEG from chasing already-priced-in moves.

```python
def entry_distance_check(proposal: TradeProposal, market: MarketState,
                          config: Config) -> FilterResult:
    
    whale_entry = proposal.signal.market_price_at_signal
    current_price = market.mid_price
    
    # Direction-aware distance
    if proposal.signal.outcome == "YES":
        distance = (current_price - whale_entry) / whale_entry
    else:
        distance = (whale_entry - current_price) / whale_entry
    
    if distance > config.max_entry_distance:  # default: 0.06 (6%)
        return FilterResult(
            passed=False, 
            reason=f"Price moved {distance:.1%} since signal — exceeds max {config.max_entry_distance:.0%}"
        )
    
    return FilterResult(passed=True, distance=distance)
```

This check runs AFTER human approval because:
1. The market may have moved during the approval delay
2. It gives operators accurate slippage context at approval time (distance shown in dashboard)
3. It catches signals that expired during a long approval queue

#### 9.5.2 Slippage Guard

**Purpose:** Final execution gate. Validates that current market spread and price drift are acceptable before placing the order.

```python
def validate_execution(proposal: TradeProposal, market: MarketState,
                        config: Config) -> ValidationResult:
    
    current_spread = market.ask - market.bid
    price_drift = abs(market.mid_price - proposal.signal.market_price_at_signal) / \
                  proposal.signal.market_price_at_signal
    
    if current_spread > config.max_spread_pct:  # default: 0.04
        return ValidationResult(False, f"Spread {current_spread:.3f} too wide")
    
    if price_drift > config.max_price_drift_since_signal:  # default: 0.08
        return ValidationResult(False, f"Price drifted {price_drift:.1%} since signal")
    
    estimated_slippage = current_spread / 2 + (config.taker_spread * market.mid_price)
    
    return ValidationResult(
        passed=True,
        estimated_slippage_pct=estimated_slippage / market.mid_price
    )
```

#### 9.5.3 Order Router

**Purpose:** Place approved and validated trade proposals on Polymarket's CLOB.

**Order strategy:**
- **Default:** Limit order at `mid_price + taker_spread` (default: +0.5%)
- **Fallback:** If limit order unfilled after `limit_timeout_seconds` (default: 30s), convert to market order
- **Stop-loss exits:** Always market order — speed over price
- **Take-profit exits:** Limit order at target price
- **Whale-exit-triggered exits:** Limit order at current mid

**Retry logic:** Failed orders retry up to 3 times with exponential backoff (1s, 2s, 4s). After 3 failures, alert via Telegram and log as `EXECUTION_FAILED`.

#### 9.5.4 Exchange Adapter Socket

```python
class ExchangeAdapter(ABC):
    exchange_id: str
    
    @abstractmethod
    async def place_order(self, order: Order) -> OrderResult: pass
    
    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool: pass
    
    @abstractmethod
    async def get_positions(self) -> list[Position]: pass
    
    @abstractmethod
    async def get_order_book(self, market_id: str) -> OrderBook: pass
    
    @abstractmethod
    async def subscribe_trades(self, callback: Callable) -> None: pass
```

`PolymarketAdapter` is the v1 implementation. `KalshiAdapter` and `ManifoldAdapter` are v2.

---

### 9.6 Dashboard & Observability

The dashboard is a FastAPI backend + React/TypeScript frontend, accessible only to the core team via authenticated session. It is the primary interface for signal monitoring, trade approval, system tuning, and performance analysis.

#### Panels

**Live Whale Feed**
Real-time stream of all detected whale trades above threshold. Columns: timestamp, wallet (score badge + archetype icon), market, direction, size, intent classification, lead-lag score. Color-coded by signal strength. Click any row to expand full wallet profile and trade history.

**Signal Log**
Every signal evaluated — whether it passed all gates, was filtered, blocked, expired, or executed. Columns: timestamp, signal ID, market, direction, composite score (expandable breakdown), suggested size, status. This is the most critical panel during paper trading for understanding signal quality and tuning thresholds. Filterable by status, score range, market category, whale archetype, date.

**Intelligence Breakdown**
For any signal, a detailed view showing: all six module scores, why each scored as it did, the archetype and ladder multipliers applied, the conviction ratio, the saturation score at time of signal, and the final composite. This is the "explain the decision" view.

**Trade Approval Queue**
All PENDING trade proposals awaiting operator approval. Each proposal shows: market question, direction, composite score + breakdown, suggested size, current price, entry distance from whale fill, estimated slippage, saturation score, any trap warnings. One-click APPROVE or REJECT with optional note. Auto-highlights signals with trap warnings in red.

**Open Positions & P&L**
All open positions with real-time P&L. Columns: market, direction, entry price, current price, unrealized P&L ($ and %), size, hours open, contributing whales, whale archetype, whale exit status. Total portfolio P&L: today / week / all-time. Equity curve chart.

**Whale Intelligence Leaderboard**
All tracked and qualified wallets with full scoring breakdown. Sortable by: composite whale score, win rate, lead time, ROI (30d/90d/all-time), volume, conviction ratio, reputation decay factor. Filter by archetype, category specialist, active vs inactive. Click any wallet for full profile: complete trade history, monthly P&L chart, category breakdown, score history over time, any trap events.

**Market Map**
Active markets currently being monitored. Shows: whale activity level, current consensus count, saturation score, quality filter status. Highlights markets with active whale positioning.

**Hot Config Panel**
Live view and editor for all configurable parameters. Edit any value in-place with immediate effect. Changes logged with timestamp and operator identity. Save/load named config presets (e.g., `conservative`, `aggressive`, `paper-tuning`).

**System Health**
RPC connection status, Redis lag, Postgres connection pool, last block processed, event bus queue depth, API rate limit status. Any degraded component shown in red with alert time.

#### Telegram Bot

Complete mobile interface for operators away from the dashboard.

**Commands:**
```
/status           — Health, uptime, today's P&L, active positions
/positions        — All open positions with current P&L
/signals          — Last 10 signals with scores
/approve {id}     — Approve a pending trade
/reject {id} {r}  — Reject with reason
/pause            — Pause all new signal processing
/resume           — Resume signal processing
/config {k} {v}   — Update a single config value
/leaderboard      — Top 10 whale scores
/market {id}      — Market details and current whale activity
/help             — Full command list
```

**Automatic Telegram alerts (priority ordered):**
1. Circuit breaker triggered — URGENT
2. Whale trap detected on active position — URGENT
3. System component failure (RPC, Redis, Postgres) — URGENT
4. High-score signal fired (composite > 0.65) — ACTION REQUIRED
5. Signal expired before approval — INFO
6. Position closed (P&L result) — INFO
7. Whale exit detected on open position — ACTION REQUIRED
8. Market saturation spike — INFO
9. Daily P&L summary (midnight UTC) — INFO

---

## 10. Risk Management Framework

Risk management is not a feature — it is a first-class architectural concern. Every component of MEG is designed to fail safely. The risk framework operates in two modes: **preventive** (pre-trade checks that block bad trades before they happen) and **reactive** (post-trade monitoring that limits damage from trades that go wrong).

### Threat Model

MEG operates in an adversarial financial environment. The following threat vectors are explicitly modeled:

**Signal crowding and copy cascade**
The primary failure mode for any copy system. MEG mitigates through entry distance filtering, market saturation detection, signal decay timers, and the slippage guard. A signal that has already been crowded out will fail multiple checks before ever reaching execution.

**Whale trap / deliberate manipulation**
Documented cases in Polymarket's history (UFO disclosure market Dec 2025, Ukraine mineral deal Mar 2025). MEG's whale trap detector monitors for rapid entry/exit patterns and applies score penalties. Repeat offenders are flagged as MANIPULATOR archetype and excluded permanently.

**Resolution divergence**
The failure mode from the original LinkedIn arb bot case study. When two markets track the same event but resolve off different data sources, paired positions can pay opposite outcomes. MEG mitigates by only trading single-market directional signals in v1 (no cross-market arb). The market quality filter flags markets with non-standard or unusual resolution sources.

**Whale strategy decay**
A whale's edge can disappear from lucky streaks ending, strategy becoming public, or market conditions changing. Reputation decay (exponential decay function) and 30-day recency weighting in the lead-lag scorer provide natural downweighting of stale alpha.

**Infrastructure failure**
RPC node down, Redis data loss, EC2 crash, network partition. Handled by: exponential backoff reconnection, Redis AOF persistence, EC2 auto-recovery, ring buffer for missed events, health monitoring with Telegram alerts for all infrastructure events.

**Key compromise**
Private keys stored only in AWS Secrets Manager, never in code, environment files, or version control. Trading wallet maintains only the capital currently deployed — never the team's full holdings. Wallet is view-only for all non-execution operations.

**Signal engine bugs**
A misconfigured weight or buggy scoring function could produce systematically wrong scores. Mitigated by: paper trading phase (validates scores against real outcomes), signal performance tracking in `signal_outcomes` table (correlates scores with P&L), circuit breaker (halts system if daily losses exceed threshold regardless of cause).

### Five Risk Gates (Priority Order)

#### Gate 1 — Circuit Breaker (Highest Priority)
**Trigger:** `portfolio.daily_pnl_usdc <= config.circuit_breaker_daily_loss_usdc`  
**Default threshold:** -$200 (paper trading), configurable for live  
**Action:** Immediately halt ALL new signal processing. Do not close existing positions (forced liquidation can cause worse outcomes). Alert ALL operators via Telegram with URGENT flag. System requires manual `/resume` command from an authenticated operator to restart.  
**Log:** `CIRCUIT_BREAKER_TRIGGERED` with full portfolio snapshot

#### Gate 2 — Max Loss Per Trade
**Trigger:** `proposed_size > portfolio.total_value * config.max_single_trade_pct`  
**Default threshold:** 5% of portfolio per trade  
**Action:** Reduce position size to maximum allowed. Do not block the trade. Kelly sizing should naturally stay within this — this is the hard backstop.  
**Note:** This is a size reducer, not a blocker. The signal is still valid; it's just right-sized.

#### Gate 3 — Max Total Portfolio Exposure
**Trigger:** `portfolio.total_exposure_pct >= config.max_portfolio_exposure_pct`  
**Default threshold:** 60% of capital deployed simultaneously  
**Action:** Block ALL new trades until existing positions reduce portfolio exposure below threshold. Other risk gates still active for existing position management.  
**Rationale:** Maintains a 40%+ cash buffer against correlated market moves or simultaneous resolution events.

#### Gate 4 — Max Market Exposure
**Trigger:** `portfolio.get_market_exposure(market_id) >= config.max_market_exposure_pct`  
**Default threshold:** 15% in any single market  
**Action:** Block new trades in that specific market. Other markets completely unaffected.  
**Rationale:** Prevents overconcentration in a single event outcome.

#### Gate 5 — Manipulation Detection (Monitoring + Flagging)
**Triggers:**
- Whale trap detected (rapid entry/exit within 30 minutes)
- Resolution source flagged as non-standard
- New wallet (<10 prior trades) placing >$50k bet
- Same market has >3 whale trades in opposite directions within 1 hour
- Market is on `blacklisted_markets` config list

**Action:** Flag signal as `MANIPULATION_RISK`. Apply -0.30 penalty to composite score. Add prominent WARNING badge in dashboard and Telegram notification. Log to `whale_trap_events` table. Do NOT auto-block (operator decides with full context). Add market to 24-hour watchlist.  
**Rationale:** Full auto-blocking on manipulation suspicion generates too many false positives during early operation. Flagging + score penalty + alert gives operators the information they need to decide.

### Position-Level Risk

| Parameter | Default | Description |
|---|---|---|
| `take_profit_pct` | +40% | Auto-flag for exit at 40% gain on entry price |
| `stop_loss_pct` | -25% | Auto-exit at 25% loss on entry price |
| `auto_exit_stop_loss` | false in v1 | Requires operator approval for stop-loss exit in v1 |
| `auto_exit_take_profit` | false in v1 | Requires operator approval for TP exit in v1 |

---

## 11. Technical Stack

### Core System

| Component | Technology | Rationale |
|---|---|---|
| Bot runtime | Python 3.11+ asyncio | Best ecosystem for on-chain data, websockets, quant libs |
| Polymarket integration | `py-clob-client` (official) | Stable, maintained, official SDK |
| Polygon on-chain | `web3.py` websocket provider | Industry standard EVM library |
| Event bus | Redis pub/sub | Sub-millisecond messaging with persistent buffer |
| Whale registry | PostgreSQL 15 | Relational data, complex score queries, ACID |
| Real-time cache | Redis | Score lookup, market state, rolling windows |
| Config management | `pydantic-settings` + Redis | Type-safe hot-reload |
| Telegram bot | `python-telegram-bot` (async) | Mature, async-native |
| Quant calculations | `numpy`, `scipy` | Kelly, sigmoid, normalization |
| Graph analysis (v2) | `networkx` | Cluster detection |

### Dashboard

| Component | Technology | Rationale |
|---|---|---|
| Backend API | FastAPI | Async, fast, automatic OpenAPI docs |
| Frontend | React 18 + TypeScript | Team familiarity, component ecosystem |
| Real-time updates | Server-Sent Events | Live feed without polling overhead |
| Charts | TradingView Lightweight Charts | Professional-grade financial charting |
| Styling | Tailwind CSS | Fast iteration, consistent design |
| State management | Zustand | Lightweight, fits the dashboard use case |

### Infrastructure

| Component | Technology | Rationale |
|---|---|---|
| Bot runtime (prod) | AWS EC2 t3.medium | Persistent process, websocket connections, 24/7 |
| Database | AWS RDS PostgreSQL | Managed, automated backups, Multi-AZ |
| Cache | AWS ElastiCache Redis | Managed Redis, low-latency, AOF persistence |
| Dashboard | AWS EC2 or ECS (same VPC) | Keeps latency to DB/cache minimal |
| Secrets | AWS Secrets Manager | Trading wallet private key, API credentials |
| Monitoring | AWS CloudWatch + Telegram | Uptime, error rates, resource usage |
| Local dev | Docker Compose | Mirrors prod exactly: Postgres + Redis + bot + dashboard |

### Development Standards

| Tool | Purpose |
|---|---|
| `poetry` | Python dependency management |
| `pytest` + `pytest-asyncio` | Test suite (target: >70% coverage on signal engine + risk controller) |
| `black` + `ruff` | Formatting and linting |
| `pre-commit` | Enforce code quality on every commit |
| GitHub Actions | CI: lint → test → build → deploy |
| `docker-compose` | Local environment parity |
| Conventional commits | Standardized commit messages for changelog generation |

---

## 12. Data Models

### Core Pydantic Models

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid

class Outcome(str, Enum):
    YES = "YES"
    NO = "NO"

class Intent(str, Enum):
    SIGNAL = "SIGNAL"
    SIGNAL_LADDER = "SIGNAL_LADDER"
    HEDGE = "HEDGE"
    REBALANCE = "REBALANCE"

class WhaleArchetype(str, Enum):
    INFORMATION = "INFORMATION"
    MOMENTUM = "MOMENTUM"
    ARBITRAGE = "ARBITRAGE"
    MANIPULATOR = "MANIPULATOR"

class SignalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FILTERED = "FILTERED"
    BLOCKED = "BLOCKED"
    EXECUTED = "EXECUTED"
    EXPIRED = "EXPIRED"
    TRAP_DETECTED = "TRAP_DETECTED"

class RawWhaleTradedEvent(BaseModel):
    wallet_address: str
    market_id: str
    outcome: Outcome
    size_usdc: float
    timestamp_ms: int
    tx_hash: str
    block_number: int
    market_price_at_trade: float

class QualifiedWhaleTradedEvent(RawWhaleTradedEvent):
    intent: Intent
    market_quality_passed: bool
    is_arbitrage_wallet: bool = False

class SignalScores(BaseModel):
    lead_lag: float = Field(ge=0, le=1)
    consensus: float = Field(ge=0, le=1)
    kelly_confidence: float = Field(ge=0, le=1)
    divergence: float = Field(ge=0, le=1)
    archetype_multiplier: float = Field(ge=0, le=2)
    ladder_multiplier: float = Field(ge=1, le=2)
    conviction_ratio: float = Field(ge=0, le=1)

class SignalEvent(BaseModel):
    signal_id: str = Field(default_factory=lambda: f"meg_sig_{uuid.uuid4().hex[:8]}")
    market_id: str
    outcome: Outcome
    composite_score: float
    scores: SignalScores
    suggested_size_usdc: float
    kelly_fraction: float
    triggering_wallet: str
    contributing_wallets: list[str]
    whale_count: int
    is_contrarian: bool
    is_ladder: bool
    ladder_trade_count: int = 0
    market_price_at_signal: float
    intent: Intent
    whale_archetype: WhaleArchetype
    saturation_score: float = 0.0
    saturation_size_multiplier: float = 1.0
    fired_at: datetime
    expires_at: datetime
    status: SignalStatus = SignalStatus.PENDING
    trap_warning: bool = False

class TradeProposal(BaseModel):
    proposal_id: str = Field(default_factory=lambda: f"meg_prop_{uuid.uuid4().hex[:8]}")
    signal: SignalEvent
    final_size_usdc: float
    order_type: str
    limit_price: Optional[float]
    estimated_slippage_pct: float
    entry_distance_pct: float
    risk_checks_passed: list[str]
    risk_checks_blocked: list[str]
    created_at: datetime
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    rejection_reason: Optional[str] = None

class Position(BaseModel):
    position_id: str = Field(default_factory=lambda: f"meg_pos_{uuid.uuid4().hex[:8]}")
    market_id: str
    outcome: Outcome
    entry_price: float
    current_price: float
    size_usdc: float
    shares: float
    unrealized_pnl_usdc: float
    unrealized_pnl_pct: float
    entry_signal_id: str
    contributing_whales: list[str]
    whale_archetype: WhaleArchetype
    opened_at: datetime
    take_profit_price: float
    stop_loss_price: float
    whale_exit_detected: bool = False
    whale_exit_detected_at: Optional[datetime] = None
    saturation_score_at_entry: float
    status: str

class WalletScore(BaseModel):
    wallet_address: str
    computed_at: datetime
    win_rate: float
    avg_lead_time_hours: float
    lead_time_score: float
    roi_30d: float
    roi_90d: float
    roi_all_time: float
    total_closed_positions: int
    consistency_score: float
    avg_conviction_ratio: float
    reputation_decay_factor: float
    composite_whale_score: float
    is_qualified: bool
    archetype: WhaleArchetype
    category_scores: dict[str, float]
```

---

## 13. API & Integration Contracts

All endpoints authenticated via `X-MEG-Key` header. Rate limited: 60 req/min per key.

```
# System
GET  /api/v1/status                          → health, uptime, mode, today P&L

# Signals
GET  /api/v1/signals                         → signal log (filter: status, score, category, date)
GET  /api/v1/signals/{signal_id}             → full signal detail with score breakdown
POST /api/v1/signals/{signal_id}/approve     → approve pending trade
POST /api/v1/signals/{signal_id}/reject      → reject with reason
GET  /api/v1/signals/{signal_id}/explain     → human-readable explanation of score

# Positions
GET  /api/v1/positions                       → all positions (filter: status)
GET  /api/v1/positions/{position_id}         → single position detail
POST /api/v1/positions/{position_id}/exit    → request manual exit

# Whale Intelligence
GET  /api/v1/whales                          → leaderboard (sort, filter)
GET  /api/v1/whales/{address}                → full wallet profile
GET  /api/v1/whales/{address}/trades         → complete trade history
GET  /api/v1/whales/{address}/scores/history → score over time

# Performance
GET  /api/v1/pnl                             → P&L summary (period: day/week/month/all)
GET  /api/v1/pnl/equity-curve                → data points for equity curve chart
GET  /api/v1/signals/performance             → signal score vs outcome correlation

# Markets
GET  /api/v1/markets                         → active monitored markets
GET  /api/v1/markets/{market_id}             → market detail + whale activity

# Configuration
GET  /api/v1/config                          → all current config values
PATCH /api/v1/config                         → update one or more values (hot reload)
GET  /api/v1/config/presets                  → list saved presets
POST /api/v1/config/presets/{name}/apply     → apply a preset
POST /api/v1/config/presets/{name}/save      → save current config as preset

# Streams
GET  /api/v1/feed/whales                     → SSE: live whale trade events
GET  /api/v1/feed/signals                    → SSE: live signal events
GET  /api/v1/feed/positions                  → SSE: position P&L updates
WS   /ws/feed                                → combined live feed (all event types)
```

---

## 14. Paper Trading Mode

Paper trading is the mandatory first phase of MEG's deployment. It runs the complete system — every pre-filter gate, every signal module, every risk check, every dashboard panel — against real market data, with simulated execution instead of real orders.

### What Changes in Paper Mode

- `system.mode = paper` in config
- `Order Router` calls `paper_execute()` instead of live CLOB order placement
- `paper_execute()` simulates fill at `mid_price + simulated_slippage` (default 0.5%)
- All positions, P&L, signal log, and performance data tracked identically to live
- Dashboard shows persistent `[PAPER TRADING]` banner
- Telegram alerts sent identically — this is intentional, it trains the team's workflow

### What Does NOT Change in Paper Mode

Everything else is identical. Real data feeds. Real signal scoring. Real risk controls (circuit breaker fires on simulated losses — this catches misconfiguration). Real human approval workflow. The only difference is that the Order Router doesn't touch the CLOB.

### Graduation Checklist

The team must agree all of the following conditions are met before switching `system.mode` to `live`:

```
Infrastructure
□ Bot has run continuously for 14+ days without crashes
□ All three operators have connected Telegram and successfully used it to approve/reject trades
□ Circuit breaker has been manually triggered and recovery procedure validated
□ AWS prod environment verified against local dev via environment parity checklist
□ Trading wallet funded with initial capital (separate from personal wallets)
□ Private key confirmed in AWS Secrets Manager, not in any file or env var

Signal Quality
□ 20+ signals have been evaluated (not necessarily all executed)
□ Paper trading win rate across all executed signals is >50%
□ Simulated P&L is positive over the full paper trading period
□ At least 5 signals have been manually reviewed in full Intelligence Breakdown view
□ Team agrees on what a "good" vs "bad" signal looks like from the score breakdown
□ At least 2 filtered/blocked signals have been reviewed to validate filter logic

Operations
□ Each operator has approved at least 5 trades via dashboard AND Telegram
□ Each operator can explain the composite score of any signal without help
□ Each operator knows the emergency pause procedure (/pause command)
□ Hot config has been used at least once to tune a parameter based on observation
□ Signal log has been used to identify at least one parameter to adjust
```

---

## 15. Configuration & Hot Reload System

All parameters stored in Redis hash `meg:config` and editable via dashboard Hot Config panel or `/config` Telegram command. Changes propagate within 1 second. Every change is logged with timestamp, operator identity, previous value, and new value.

### Full Configuration Reference

```yaml
# ─── SIGNAL THRESHOLDS ───────────────────────────────────
signal.min_composite_score: 0.45
signal.min_lead_lag_score: 0.40
signal.ttl_hours: 2.0                         # legacy fallback only

# Signal module weights
signal.weights.lead_lag: 0.35
signal.weights.consensus: 0.30
signal.weights.kelly: 0.20
signal.weights.divergence: 0.15

# ─── HALF-LIFE SYSTEM ────────────────────────────────────
signal.half_life.ttl_multiplier: 3.0          # TTL = half_life × multiplier
signal.half_life.min_minutes: 5               # floor on any half-life estimate
signal.half_life.default_minutes: 60          # fallback if type unknown
signal.half_life.deep_liquidity_threshold: 500000   # USDC — extends half-life
signal.half_life.fast_repricing_tpm_ratio: 2.0      # compresses half-life

# ─── CONSENSUS FILTER ────────────────────────────────────
signal.consensus.window_hours: 4.0
signal.consensus.min_whales: 2
signal.consensus.sensitivity: 1.5

# ─── KELLY SIZING ────────────────────────────────────────
signal.kelly.fractional_multiplier: 0.25

# ─── REPUTATION DECAY ────────────────────────────────────
signal.reputation.decay_tau_days: 30

# ─── ENTRY LADDER ────────────────────────────────────────
signal.ladder.window_hours: 6.0
signal.ladder.conviction_per_rung: 0.15
signal.ladder.max_multiplier: 2.0

# ─── WHALE QUALIFICATION ─────────────────────────────────
whale.min_win_rate: 0.55
whale.min_closed_positions: 50
whale.min_volume_usdc: 100000
whale.min_profitable_months_trailing_6: 3
whale.tracking_threshold_usdc: 10000

# ─── MARKET QUALITY ──────────────────────────────────────
market.min_volume_24h_usdc: 50000
market.min_liquidity_usdc: 10000
market.max_spread: 0.06
market.min_participants: 20
market.min_days_to_resolution: 1

# ─── RISK CONTROLS ───────────────────────────────────────
risk.circuit_breaker_daily_loss_usdc: -200
risk.max_single_trade_pct: 0.05
risk.max_market_exposure_pct: 0.15
risk.max_portfolio_exposure_pct: 0.60

# ─── POSITION MANAGEMENT ─────────────────────────────────
position.take_profit_pct: 0.40
position.stop_loss_pct: 0.25
position.auto_exit_stop_loss: false
position.auto_exit_take_profit: false
position.trailing_tp_enabled: false           # enable after paper trading validation
position.trailing_tp_floor_pct: 0.10          # trail TP 10% below current price
position.use_fair_value_reference: false      # use fair value vs whale fill for entry distance

# ─── EXECUTION ───────────────────────────────────────────
execution.default_order_type: limit
execution.taker_spread: 0.005
execution.limit_timeout_seconds: 30
execution.max_entry_distance: 0.06
execution.max_spread_pct: 0.04
execution.max_price_drift_since_signal: 0.08

# ─── SATURATION DETECTION ────────────────────────────────
saturation.threshold: 0.60
saturation.size_reduction_sensitivity: 1.5

# ─── CONTRACT ANALYSIS (v1.5) ────────────────────────────
contract.hazard_min_mispricing_threshold: 0.05   # 5% gap to flag as edge
contract.early_resolution_min_annual_return: 1.50 # 150% annualized floor
contract.near_certain_threshold: 0.94             # above this = near-certain check
contract.resolution_risk_size_reduction: 0.50     # halve size if dispute risk high

# ─── STRUCTURAL EDGE MODULES (v1.5) ──────────────────────
structural.cross_market_min_inconsistency: 0.03   # 3% probability gap to flag
structural.oracle_latency_enabled: false          # enable per market category
structural.market_maker_min_spread: 0.02          # YES+NO > 1.02 to flag arb

# ─── WHALE TRAP ──────────────────────────────────────────
trap.window_minutes: 30
trap.exit_threshold: 0.50
trap.score_penalty: 0.20
trap.manipulator_threshold: 3

# ─── SYSTEM ──────────────────────────────────────────────
system.mode: paper
system.paper_slippage_pct: 0.005
system.blacklisted_markets: []
system.paused: false
system.telegram_alert_min_score: 0.65
system.score_refresh_top_n: 50
```

### Config Presets

**`conservative`** — Lower position sizes, higher score thresholds, tighter quality filters. Use when market conditions are uncertain.

**`aggressive`** — Higher Kelly multiplier (0.33), lower composite threshold (0.40), wider consensus window. Use in high-conviction periods.

**`paper-tuning`** — Very low circuit breaker (-$50), all exits require approval, verbose Telegram alerts. Use during initial paper trading.

**`live-standard`** — Balanced defaults for live trading. Start here.

---

## 16. Plugin Socket Architecture

Every layer exposes a plugin interface. New capabilities are added by implementing the interface and dropping a file in the `plugins/` directory. No changes to core system code are ever required to add a plugin.

### Plugin Interfaces

```python
# Data Layer Socket
class DataSourcePlugin(ABC):
    source_id: str
    
    @abstractmethod
    async def start_stream(self, event_bus: EventBus) -> None: pass
    
    @abstractmethod
    async def get_market_state(self, market_id: str) -> dict: pass

# Signal Module Socket  
class SignalModule(ABC):
    name: str
    version: str
    
    @abstractmethod
    async def score(self, event: QualifiedWhaleTradedEvent,
                    context: MarketContext) -> SignalScore: pass

# Reasoning Plugin Socket (Agent Core)
class ReasoningPlugin(ABC):
    @abstractmethod
    async def evaluate(self, proposal: TradeProposal,
                       context: FullContext) -> ReasoningResult: pass

# Exchange Adapter Socket
class ExchangeAdapter(ABC):
    exchange_id: str
    
    @abstractmethod
    async def place_order(self, order: Order) -> OrderResult: pass
    
    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool: pass
    
    @abstractmethod
    async def get_positions(self) -> list[Position]: pass
    
    @abstractmethod
    async def subscribe_trades(self, callback: Callable) -> None: pass
```

### Plugin Registry

```python
class PluginRegistry:
    def register(self, plugin: Any) -> None:
        """Auto-detect plugin type and register to correct registry."""
        if isinstance(plugin, DataSourcePlugin):
            self._data_sources[plugin.source_id] = plugin
        elif isinstance(plugin, SignalModule):
            self._signal_modules[plugin.name] = plugin
            # Weight pulled from config: signal.weights.{plugin.name}
        elif isinstance(plugin, ReasoningPlugin):
            self._reasoning = plugin
        elif isinstance(plugin, ExchangeAdapter):
            self._exchange_adapters[plugin.exchange_id] = plugin

    def discover_plugins(self, plugins_dir: str = "plugins/") -> None:
        """Scan directory, import modules, call register() on each."""
        for module in scan_python_modules(plugins_dir):
            if hasattr(module, "register"):
                module.register(self)
```

### v1 Registered Plugins

| Socket | Plugin | Status |
|---|---|---|
| Data Source | `PolygonRPCSource` | ✅ v1 |
| Data Source | `PolymarketCLOBSource` | ✅ v1 |
| Signal Module | `LeadLagScorer` | ✅ v1 |
| Signal Module | `KellySizer` (half-life-aware) | ✅ v1 |
| Signal Module | `ConsensusFilter` | ✅ v1 |
| Signal Module | `ContrarianDetector` | ✅ v1 |
| Signal Module | `EntryLadderDetector` | ✅ v1 |
| Signal Module | `ArchetypeWeighter` | ✅ v1 |
| Signal Module | `SignalDecayTimer` (dynamic TTL) | ✅ v1 |
| Signal Module | `CrossMarketArbDetector` | v1.5 |
| Signal Module | `OracleLatencySignal` | v1.5 |
| Signal Module | `MarketMakerSpreadMonitor` | v1.5 |
| Signal Module | `HazardRateMispricingDetector` | v1.5 |
| Signal Module | `ContractAgingMonitor` | v1.5 |
| Signal Module | `EarlyResolutionPremiumScorer` | v1.5 |
| Signal Module | `CascadeRidingModule` | v2 |
| Signal Module | `LastDayDecayShort` | v2 |
| Reasoning Plugin | `LLMSignalEvaluator` (Claude on Bedrock) | v2 |
| Reasoning Plugin | `LLMContractAnalyzer` (Claude on Bedrock) | v2 |
| Exchange Adapter | `PolymarketAdapter` | ✅ v1 |
| Exchange Adapter | `KalshiAdapter` | v2 |
| Exchange Adapter | `ManifoldAdapter` | v2 |

---

## 17. Non-Functional Requirements

### Reliability
- Bot core uptime target: >99% (≤7 hours downtime/month)
- No silent failures: all uncaught exceptions caught at top level, logged, and trigger Telegram alert
- No single point of failure: Redis, Postgres, EC2 all have AWS-managed failover or recovery
- Ring buffer on RPC feed ensures no missed events during reconnection

### Observability
- Structured JSON logging on all events: signal fires, trade approvals, order placements, errors, config changes
- CloudWatch log groups for all services, 30-day retention
- Every decision by every module is logged with full context — the system should be fully explainable from logs alone
- Signal performance table (`signal_outcomes`) enables retrospective analysis of score calibration

### Security
- Trading wallet private key: AWS Secrets Manager only, never in code, env files, or git
- Dashboard: accessible only via VPN or SSH tunnel, never publicly exposed in v1
- Telegram bot: responds only to whitelisted chat IDs
- API key rotation: every 30 days
- Principle of least privilege: trading wallet holds only deployed capital

### Testability
- All signal modules independently unit-testable with mock events
- Historical whale trade data can be replayed against the signal engine (event sourcing pattern supports this natively)
- Paper trading mode is the primary integration test environment
- `signal_outcomes` table enables backtesting of score calibration

### Code Quality
- All modules: docstrings + full type annotations
- Signal engine + risk controller: >70% test coverage minimum
- No production deploys without passing CI (lint + test)
- Signal module weights, thresholds, and all magic numbers must be named constants — never hardcoded inline

---

## 18. Signal Versioning Roadmap

```
╔══════════════════════════════════════════════════════════════════╗
║  v1 CORE — Ship at launch                                        ║
╠══════════════════════════════════════════════════════════════════╣
║  Pre-filters:                                                    ║
║    Market Quality Filter                                         ║
║    Arbitrage Whale Exclusion                                     ║
║    Intent Classifier (SIGNAL / SIGNAL_LADDER / HEDGE / REBALANCE)║
║                                                                  ║
║  Signal Modules:                                                 ║
║    Lead-Lag Scorer + Reputation Decay                            ║
║    Conviction Ratio Modifier                                     ║
║    Kelly Criterion Sizer (half-life-adjusted)                    ║
║    Multi-Whale Consensus Filter                                  ║
║    Contrarian Divergence Detector                                ║
║    Entry Ladder Detector                                         ║
║    Whale Archetype Weighter                                      ║
║    Signal Decay Timer (dynamic half-life TTL)                    ║
║                                                                  ║
║  Agent Core:                                                     ║
║    Decision Agent (rules-based)                                  ║
║    Whale Trap Detector                                           ║
║    Market Saturation Monitor                                     ║
║    Signal Crowding / Entry Distance Filter                       ║
║    Position Manager + Whale Exit Detection                       ║
║    Trailing Take-Profit (drift continuation)                     ║
╠══════════════════════════════════════════════════════════════════╣
║  v1.5 — Behavioral Edge Extensions                               ║
╠══════════════════════════════════════════════════════════════════╣
║    News Latency Boost (modifier on whale signal)                 ║
║    Liquidity Shock Detector                                      ║
║    Momentum Score                                                ║
║    Price Impact Scorer                                           ║
║    Herd Detector (exit signal trigger)                           ║
║    Archetype-weighted consensus (INFORMATION > MOMENTUM)         ║
║    Fair-Value-Adjusted Entry Distance                            ║
║    Event-Latency Signal Classifier                               ║
╠══════════════════════════════════════════════════════════════════╣
║  v1.5 — Structural Edge Modules (new category)                   ║
╠══════════════════════════════════════════════════════════════════╣
║    Cross-Market Probability Arb Detector                         ║
║      (P(>90k) ≤ P(>85k) ≤ P(>80k) consistency enforcement)      ║
║    Oracle Latency Signal (sports/politics, non-crypto)           ║
║    Market Maker Spread Monitor (YES+NO > $1 arbitrage)           ║
╠══════════════════════════════════════════════════════════════════╣
║  v1.5 — Contract-Design Edge Modules (new category)              ║
╠══════════════════════════════════════════════════════════════════╣
║    Hazard Rate Mispricing Detector                               ║
║      (actuarial P(event) vs market price gap detection)          ║
║    Contract Aging / Path Drift Monitor                           ║
║      (structural probability drift as time elapses)              ║
║    Early Resolution Premium Scorer                               ║
║      (instant-trigger YES + near-certain unconfirmed markets)    ║
║    Resolution Dispute Risk Flag                                  ║
║      (oracle manipulation risk on near-certain markets)          ║
╠══════════════════════════════════════════════════════════════════╣
║  v2 — Full Autonomy Release                                      ║
╠══════════════════════════════════════════════════════════════════╣
║    Full Autonomy Mode (remove human approval)                    ║
║    Shadow Entry Strategy (sub-500ms execution)                   ║
║    Cluster Detection (Louvain wallet graph clustering)           ║
║    Market Probability Graph (cross-market consistency, full)     ║
║    ML Whale Scoring Model (replace rule-based scorer)            ║
║    LLM Contract Analysis (Claude on Bedrock — hazard rates,      ║
║      resolution criteria parsing, fair value estimation)         ║
║    LLM Reasoning Layer (high-conviction signal evaluation)       ║
║    Last-Day YES Decay Shorting Strategy                          ║
║    Cascade Riding Signal Module (retail overshoot exit)          ║
║    Bet Size / Wallet Capital conviction scoring (full)           ║
║    Kalshi Exchange Adapter                                       ║
╠══════════════════════════════════════════════════════════════════╣
║  v3 — Public SaaS                                                ║
╠══════════════════════════════════════════════════════════════════╣
║    Multi-tenant data model                                       ║
║    Public signal feed API (all three edge categories)            ║
║    Subscriber wallet connection + copy execution                 ║
║    Subscription tier management                                  ║
║    Mobile-first public UI                                        ║
║    Trader intelligence dataset API (whale registry licensing)    ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 19. v2 Roadmap

### Full Autonomy Mode
Remove human approval from the trade flow. All decisions made by the Agent Core and Risk Controller operating within hardcoded guardrails. Operators receive Telegram alerts only for anomalies, trap detections, circuit breaker events, and daily summaries.

**Gate:** All paper trading and live semi-auto performance targets must be met and documented before autonomy is enabled.

### Shadow Entry Strategy
In v2 full autonomy, MEG can place orders within 500ms of whale detection — before the market has fully repriced. This is the execution edge that semi-auto mode cannot access (human approval latency makes it impossible). Architecture already supports this: the event pipeline is async end-to-end, and the only blocking step is the human approval gate, which is removed in v2.

### Cluster Detection
The most technically significant v2 feature and the most powerful moat. Build a wallet relationship graph to identify multi-wallet whales (Théo's 11 accounts is the canonical example). Without cluster detection, three wallets each with $500k in the same position look like three whales with moderate conviction. With cluster detection, they reveal one whale with $1.5M conviction — a qualitatively different signal.

**Implementation approach:**
1. Build wallet graph in Postgres: `wallet_relationships` table with `wallet_a`, `wallet_b`, `relationship_type`, `confidence_score`
2. Populate via four signals: shared funding wallet (highest confidence), trade timing correlation, behavioral fingerprint similarity, gas/transaction pattern matching
3. Run Louvain community detection (via `networkx`) on the wallet graph weekly
4. Assign `cluster_id` to all wallets in a detected cluster
5. Aggregate cluster conviction: `cluster_conviction = log(sum(capital_deployed_by_cluster))`
6. Update consensus filter to use cluster count, not wallet count

**Schema addition:**
```sql
CREATE TABLE wallet_relationships (
    wallet_a            VARCHAR(42) REFERENCES wallets(address),
    wallet_b            VARCHAR(42) REFERENCES wallets(address),
    relationship_type   VARCHAR(32),  -- FUNDING_WALLET | TIMING | BEHAVIORAL | GAS
    confidence          DECIMAL(5,4),
    detected_at         TIMESTAMP,
    PRIMARY KEY (wallet_a, wallet_b, relationship_type)
);
```

### Market Probability Graph
Build a graph of Polymarket markets connected by logical relationships (mutual exclusivity, conditional probability, shared underlying event). Use this graph to:
- Detect probability inconsistencies (sum of mutually exclusive markets ≠ 1)
- Identify when a whale's trade in one market has pricing implications for related markets
- Flag markets with high resolution source divergence risk before entering

**Approach:** Start with manually curated market groupings (election markets are the clearest case), then build an ML-based automatic grouping system.

### ML Whale Scoring Model
Replace the rule-based lead-lag scoring formula with a trained gradient boosting model (XGBoost or LightGBM) that predicts `P(trade is profitable)` for a given whale entry. Features: historical win rate, lead time distribution, category performance, market liquidity at entry, time-of-day patterns, recent performance trend, archetype classification, conviction ratio.

Train on the `signal_outcomes` table accumulated during paper trading and v1 live operation. Retrain monthly.

### LLM Reasoning Layer (Claude on Bedrock)
For signals with composite score >0.75, invoke Claude via AWS Bedrock as a final reasoning layer. Provide full context: signal breakdown, market question and resolution criteria, contributing whale profiles, recent news context (via web search tool). Claude outputs a structured assessment and recommended position size adjustment.

Implemented as a `ReasoningPlugin` — zero changes to core system code required. Adds ~2-3 second latency to high-conviction signal processing, which is acceptable in semi-auto mode and can be made optional in full-auto mode.

### LLM Contract Analysis (Claude on Bedrock)
A second, distinct use of Claude — not for signal evaluation but for **contract-design edge detection**. For each new market that enters MEG's monitoring scope, Claude parses the resolution criteria and outputs:

```json
{
  "has_early_resolution_trigger": true,
  "trigger_description": "Resolves YES immediately upon bankruptcy filing",
  "estimated_weekly_hazard_rate": 0.024,
  "weeks_to_deadline": 14,
  "hazard_adjusted_probability": 0.29,
  "resolution_source_risk": "low",
  "path_dependent": false,
  "near_certain_threshold": null,
  "notes": "Classic early-resolution asymmetry market. YES side benefits from instant payout on trigger."
}
```

This output feeds directly into the Contract Analysis signal modules. The LLM does the semantic work of reading resolution criteria that no rule-based parser could handle reliably. This is a concrete, well-scoped use case where LLM reasoning provides genuine value that cannot be replaced by heuristics.

### Contract-Design Edge Modules (v1.5 → v2 Full Implementation)

The v1.5 modules detect contract-design edges using heuristics and baseline hazard rate tables. The v2 versions use LLM contract analysis as the input, making them accurate across any market category rather than just the few categories with pre-built hazard rate tables.

**Hazard Rate Mispricing Detector:**
```python
def hazard_adjusted_probability(market_price: float, weekly_hazard: float,
                                 weeks_remaining: int) -> float:
    """
    Actuarial probability vs market price.
    Example: market at 0.22, weekly hazard 0.03, 12 weeks left
    True probability = 1 - (0.97^12) = 0.306
    Mispricing = 0.306 - 0.22 = 0.086 (8.6% edge, no behavioral assumption required)
    """
    true_probability = 1 - (1 - weekly_hazard) ** weeks_remaining
    mispricing = true_probability - market_price
    return HazardResult(
        true_probability=true_probability,
        market_probability=market_price,
        mispricing=mispricing,
        is_underpriced=mispricing > config.hazard_min_mispricing_threshold
    )
```

Hazard rate baselines by category (v1.5 heuristic table, v2 LLM-derived):

| Market Category | Weekly Hazard Baseline | Notes |
|---|---|---|
| Corporate bankruptcy | 1.5–3.5% | Varies by credit rating / news context |
| Political resignation | 0.5–2.0% | Context-dependent |
| Sports injury/retirement | 0.8–2.5% | Sport and age dependent |
| Government shutdown | 2.0–8.0% | Deadline-driven, spikes near end |
| Regulatory action | 1.0–4.0% | Varies by regulator and case stage |

**Early Resolution Premium Scorer:**
Three patterns scored independently:
1. *Instant trigger YES:* Contract resolves immediately when event occurs. Annualized return calculation: `annual_return = (1/entry_price - 1) × (365 / expected_days_to_resolution)`. Markets where annualized return exceeds 150% on near-certain instant-trigger contracts are flagged.
2. *Near-certain unconfirmed:* Market trading at 94–98% where event is effectively confirmed but oracle not yet official. Captures 2–6% nearly-risk-free with flag for resolution dispute risk.
3. *Last-day decay short (v2):* Predictable YES price collapse in final 48–72 hours before deadline on non-triggered markets. Structured short with known timeline.

**Contract Aging / Path Drift Monitor:**
Tracks how a market's probability *should* evolve structurally over time — independent of any whale trades or news. For path-dependent markets (government shutdown, ongoing negotiations, cumulative risk events), the structural probability increases as time elapses without resolution. MEG monitors the gap between actual price and structural drift model, flagging markets where the price is lagging behind where it should be.

**Resolution Dispute Risk Flag:**
Near-certain markets (>90% price) carry elevated oracle manipulation risk — the incentive to dispute resolution is highest when large capital is at stake. Any near-certain contract signal is automatically cross-checked against:
- UMA dispute history for this market's resolution source
- Whether resolution criteria are clearly binary or ambiguous
- Whether this market's category has prior dispute incidents

If risk is elevated, signal is tagged `RESOLUTION_RISK_HIGH` and position size is reduced by 50% regardless of composite score.

---

## 20. v3 Roadmap — Public SaaS

The v3 SaaS product exposes MEG's intelligence engine to external subscribers. The key architectural decisions that v1 must make with v3 in mind:

**Multi-tenancy:** The `signal_outcomes`, `positions`, and `trades` tables must support a `user_id` or `tenant_id` column from the start. Adding multi-tenancy to a single-tenant schema later is painful. In v1, all records have `tenant_id = "core_team"`.

**API design:** The v1 internal API should already follow RESTful conventions and versioning (`/api/v1/`) so that external exposure in v3 is a matter of auth layer addition, not API redesign.

**Signal feed latency tiers:** v3 monetization likely involves free (delayed 30-60 min signals) vs paid (real-time signals). The signal pipeline should tag each signal with `fired_at` from day one so that delay-based tiering is implementable without architectural changes.

### The Dataset Is The Real Asset

The most strategically valuable output of MEG's operation is not the trading returns. It is the **dataset** that accumulates as a byproduct of the intelligence pipeline running continuously.

After 6–12 months of operation, MEG will have produced something that has never existed before: a comprehensive, performance-ranked, behaviorally annotated directory of every serious prediction market trader on Polymarket — with historical accuracy scores, lead time distributions, category expertise profiles, archetype classifications, conviction ratio histories, and full trade records.

This dataset has standalone commercial value that is entirely independent of MEG's trading operations. Consider what it enables:

**Trader intelligence product** — A public or subscription leaderboard of the most accurate prediction market traders, updated in real-time with full performance breakdowns. This is the "Bloomberg terminal for prediction market smart money." No equivalent exists. The data is assembled from public on-chain records but the intelligence layer — scoring, classification, decay, archetype assignment — is entirely proprietary.

**Signal subscription feed** — External traders pay to receive MEG's scored signal feed in real-time. They don't need to understand the scoring model. They receive: market, direction, composite score, whale count, archetype, and recommended sizing. They execute manually. Tiered by latency and detail depth.

**API licensing** — Other prediction market tools, analytics platforms, and research firms pay to query MEG's whale registry and scoring data via API. Analogous to how financial data vendors license proprietary datasets to institutional clients.

**Prediction market fund infrastructure** — MEG's dataset could eventually power a structured vehicle where external capital is allocated based on MEG's whale rankings — essentially a fund-of-prediction-market-signals. This is speculative but architecturally natural as a v4+ evolution.

### V1 Data Design Decisions That Enable The Dataset Product

These decisions should be made now, not retrofitted later:

**Rich behavioral metadata at capture time** — Every trade event stored in the `trades` table should capture the full market context at entry: order book depth, spread, 1-hour price momentum, time of day, days to resolution, market category. This contextual metadata is what enables retrospective behavioral fingerprinting and ML feature engineering later. Storing it at capture time costs nothing extra. Trying to reconstruct it later is impossible.

**No pruning of historical data** — The wallet registry and signal outcomes table should retain full history indefinitely. Storage cost on RDS is trivial relative to the value of a complete longitudinal dataset. Never auto-archive or delete wallet trade history, even for inactive wallets.

**Snapshot-based scoring history** — The `wallet_scores` table already stores one row per computation timestamp. Preserve this. A time-series of a wallet's score is far more valuable than just the current score — it shows when an edge emerged, how it evolved, and when it decayed. This is what makes the dataset a genuine research asset, not just a leaderboard.

**Behavioral fingerprint table** — Add a `wallet_behavioral_snapshots` table that stores a feature vector for each wallet computed monthly: average trade size, time-of-day distribution, market category mix, holding period distribution, entry timing relative to news events. This becomes the training data for the ML archetype classifier and cluster detection system.

```sql
CREATE TABLE wallet_behavioral_snapshots (
    wallet_address      VARCHAR(42) REFERENCES wallets(address),
    snapshot_month      DATE NOT NULL,
    avg_trade_size_usdc DECIMAL(18,2),
    trade_hour_dist     JSONB,           -- {0: 0.02, 1: 0.01, ... 23: 0.08}
    category_mix        JSONB,           -- {politics: 0.60, sports: 0.25, ...}
    avg_hold_hours      DECIMAL(8,2),
    avg_entry_lead_hrs  DECIMAL(8,2),
    trades_per_week     DECIMAL(6,2),
    pct_contrarian      DECIMAL(5,4),
    pct_ladder_entries  DECIMAL(5,4),
    feature_vector      VECTOR(32),      -- pgvector embedding for similarity search
    PRIMARY KEY (wallet_address, snapshot_month)
);
```

### Cascade Riding Signal Module (v2 Socket)

The retail cascade described in Section 2 creates a secondary trade opportunity that is distinct from the original entry signal. Once MEG has entered a position at step ② (after the information trader, before the retail cascade), a separate signal module can detect the onset of the retail wave at step ④ and trigger a staged exit to capture the overshoot.

```python
# v2 signal socket: CascadeRidingModule
class CascadeRidingModule(SignalModule):
    name = "cascade_rider"
    
    async def score(self, position: Position, 
                    market: MarketState) -> CascadeSignal:
        
        # Detect retail cascade onset: rapid trade frequency + order book thinning
        tpm_ratio = market.trades_per_minute_5min / market.avg_tpm_baseline
        book_consumed = 1 - (market.ask_depth / market.baseline_ask_depth)
        
        cascade_onset_score = (tpm_ratio - 1) * 0.5 + book_consumed * 0.5
        
        if cascade_onset_score > config.cascade_exit_threshold:
            return CascadeSignal(
                recommend_exit=True,
                confidence=cascade_onset_score,
                reason="retail_cascade_detected"
            )
        return CascadeSignal(recommend_exit=False)
```

This module is a v2 feature (requires the herd detector from v1.5 as a dependency) but the socket architecture means it can be dropped in without touching core system code.

### Monetization Options

| Model | Target User | Complexity | Revenue Potential |
|---|---|---|---|
| Flat monthly subscription | Retail Polymarket traders | Low | $29–$99/month per subscriber |
| Performance fee | Traders following MEG signals | Medium | % of profits from MEG-sourced trades |
| API access tiering | Tool builders, researchers | Medium | Per-query or monthly access tiers |
| White-label intelligence feed | Other prediction market platforms | High | Enterprise licensing |
| Dataset licensing | Academic researchers, quant firms | Medium | One-time or annual data licenses |



## 21. Open Questions & Decisions Log

| ID | Question | Status | Decision / Notes |
|---|---|---|---|
| OQ-01 | RPC provider: Alchemy vs QuickNode vs Infura? | Open | Evaluate on websocket stability and latency. Alchemy preferred. Public RPC not suitable for production. |
| OQ-02 | How to handle Polymarket API rate limits under heavy simultaneous whale activity? | Open | Implement async request queue with rate limiter and priority scoring — high-score markets get priority |
| OQ-03 | Paper trading and live trading simultaneously? | Open | Recommendation: single mode at a time. Avoids confusion about which trades are real. |
| OQ-04 | How to backfill whale wallet history pre-launch? | Open | Dune Analytics + Bitquery Polymarket API. Target: seed with top 200 wallets by historical volume before first signal fires. |
| OQ-05 | Who holds the trading wallet private key? | Open | Shared custody model TBD. Minimum: two operators must approve key access. Key stored in AWS Secrets Manager. |
| OQ-06 | Rollback plan if v2 autonomy upgrade misbehaves? | Open | Define kill switch, state snapshot procedure, and position freeze protocol before v2 launch. |
| OQ-07 | Dashboard: mobile-responsive or desktop-only in v1? | Open | Recommendation: desktop-only v1 (Telegram covers mobile). Mobile-first in v3. |
| OQ-08 | Whale score recalculation frequency? | Open | Daily batch for all wallets. Real-time for top 50 by volume. Configurable. |
| OQ-09 | How to classify a wallet's archetype with limited history? | Open | Default to INFORMATION (full weight) if <50 trades. Reclassify once sufficient history accumulated. |
| OQ-10 | News latency module: Twitter/X API vs RSS vs newswire? | Open | Twitter/X API expensive (~$100+/month). RSS + political newswire feeds cheaper and sufficient for v1.5. Evaluate cost vs signal quality. |
| OQ-11 | How often to snapshot wallet capital balances for conviction ratio? | Open | Daily for all tracked wallets. More frequent for top 50. |
| OQ-12 | Should stop-loss exits be auto-executed in v1? | Open | Recommendation: yes, auto-execute stop-losses only (speed matters for risk). Take-profit requires approval. |

---

## 22. Appendix

### A. Key External Resources

- **Polymarket CLOB Client (official):** https://github.com/Polymarket/py-clob-client
- **Polymarket Agents Framework (official):** https://github.com/Polymarket/agents
- **Polymarket CLOB Contract:** `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E`
- **Dune Analytics Polymarket Dashboards:** https://dune.com/search?q=polymarket
- **Bitquery Polymarket API:** https://bitquery.io/blog/polymarket-api
- **Arkham Intelligence (on-chain wallet analysis):** https://intel.arkm.com
- **Polymarket Analytics:** https://polymarketanalytics.com
- **web3.py documentation:** https://web3py.readthedocs.io
- **py-clob-client documentation:** https://github.com/Polymarket/py-clob-client

### B. Known High-Value Seed Wallets (Public Record)

The following wallets are documented in public research and can seed the wallet registry bootstrap:
- `Fredi9999`, `Theo4`, `PrincessCaro`, `Michie` + 7 others — Théo's documented election accounts (cluster example)
- `Domer` — #1 all-time Polymarket trader by volume ($300M+) and profit ($3M+), former professional poker player
- Additional addresses discoverable via Polymarket public leaderboard and community research on Dune

### C. Competitive Analysis Summary

| Dimension | Polywhaler | PolyTrack | MEG |
|---|---|---|---|
| Real-time whale detection | ✅ | ✅ | ✅ |
| Whale scoring / leaderboard | Basic | Advanced | Advanced + decay |
| Cluster detection | ❌ | ✅ | v2 |
| Intent classification | ❌ | ❌ | ✅ v1 |
| Reputation decay | ❌ | ❌ | ✅ v1 |
| Whale archetype classification | ❌ | ❌ | ✅ v1 |
| Entry ladder detection | ❌ | ❌ | ✅ v1 |
| Conviction ratio modeling | ❌ | ❌ | ✅ v1 |
| Kelly criterion sizing | ❌ | ❌ | ✅ v1 |
| Signal crowding detection | ❌ | ❌ | ✅ v1 |
| Whale trap detection | ❌ | ❌ | ✅ v1 |
| Market saturation monitoring | ❌ | ❌ | ✅ v1 |
| Automated execution | ❌ | ❌ | ✅ v1 (semi-auto) |
| Full autonomy | ❌ | ❌ | v2 |
| LLM reasoning layer | ❌ | ❌ | v2 |
| Public SaaS | ❌ | ❌ (free tool) | v3 |

### D. Glossary

| Term | Definition |
|---|---|
| Whale | A Polymarket trader meeting qualification thresholds: 55%+ win rate, 50+ closed positions, $100k+ volume |
| Information whale | Whale archetype: enters early (hours before move), holds long, trades rarely — highest signal value |
| Momentum whale | Whale archetype: enters after price moves, rides momentum, exits quickly — discounted signal value |
| Arbitrage whale | Whale archetype: trades both sides, high volume, no directional edge — excluded from signals |
| Lead time | Hours between a whale's entry and a significant price move (>5%) in their direction |
| Reputation decay | Exponential reduction in whale score based on time since last profitable trade |
| Conviction ratio | bet_size_usdc / wallet_total_capital_usdc — measures how much the whale is risking |
| Composite score | Weighted combination of all signal module outputs, applying archetype and ladder multipliers |
| Consensus | Two or more independent qualified whales on the same side of the same market |
| Entry ladder | Whale building a position via escalating sequential trades — indicates increasing conviction |
| Contrarian | Whale entering against prevailing order book direction — often indicates information edge |
| Kelly fraction | Mathematically optimal bet size as fraction of bankroll given win probability and odds |
| Fractional Kelly | Conservative scaling (0.25×) applied to Kelly fraction to account for model uncertainty |
| Signal crowding | When too many copy traders follow the same signal, becoming exit liquidity for the original whale |
| Entry distance | (current_price - whale_fill_price) / whale_fill_price — measures how much the signal has been priced in |
| Market saturation | Abnormal combination of price velocity, order book thinning, and trade frequency indicating crowding |
| Whale trap | Deliberate pattern: whale enters large, attracts followers, rapidly exits into follower liquidity |
| Circuit breaker | Daily loss threshold that halts all new trading activity and requires manual restart |
| Hot config | Configuration parameters changeable at runtime without restart |
| Plugin socket | Abstract interface allowing new capabilities to be added without modifying core system code |
| Paper trading | Simulated trading using real market data but no real order placement |
| Resolution divergence | When two markets tracking the same event resolve to different outcomes due to different data sources |
| Signal TTL | Time-to-live on a signal — expired signals are never executed regardless of score |
| Information hierarchy | The flow: insiders → professional traders → prediction markets → retail → news. MEG operates in the gap between layer 2 and 3 |

### E. All Decisions Made During PRD Development

| Decision | Choice | Rationale |
|---|---|---|
| System name | MEG (Megalodon) | Apex predator that ate whales — the system hunts whale signals |
| Primary framing | Market intelligence engine, not copy bot | More accurate, more defensible, better SaaS pitch |
| Primary goal | Both money and portfolio value | Equal weight, neither dominates design decisions |
| Bot autonomy | Semi-auto v1 → full auto v2 | Validate signal quality before trusting it with autonomous capital |
| Platform scope | Platform-agnostic architecture, Polymarket v1 | Best whale data is on Polymarket; architecture stays open |
| Capital strategy | Paper trade first → $1k–$5k live | Risk discipline, validate before deploying real money |
| v1 signal stack | All four core modules + archetype + ladder | Modular, each adds distinct value, all implementable in v1 |
| Data approach | Polygon + Polymarket OSS foundation, proprietary quant layer | Stable foundation + defensible moat |
| Hosting | AWS prod (EC2 + RDS + ElastiCache), Docker local | Team has prior AWS experience; prod/dev parity via Docker |
| Dashboard scope | All panels + Telegram | Maximum observability during paper trading and tuning phase |
| Whale threshold | Configurable via hot config | Tunable — right value depends on capital deployed |
| Latency stance | Correctness first, optimize in v2 | Signal quality > speed in semi-auto mode |
| Risk controls | All five gates, priority-ordered | Non-negotiable with real money on the line |
| Timeline | Ship when ready, no artificial deadline | Quality over speed |
| Language | Python async core, TypeScript dashboard | Best fit per layer; team familiar with both |
| v1.5 signals | News boost, momentum, liquidity shock, herd detector | Add after paper trading validates core stack |
| v2 features | Cluster detection, autonomy, ML scorer, LLM layer, Kalshi | Full quant system architecture |
| v3 vision | Public SaaS market intelligence platform | Multi-tenant architecture decisions made in v1 |

---

*MEG PRD v2.0 — Definitive — Confidential Internal Document*  
*Supersedes: ORCA PRD v1.0*  
*Next review: After paper trading phase completion*  
*Distribution: Krishna · Bowen · Agastya*
