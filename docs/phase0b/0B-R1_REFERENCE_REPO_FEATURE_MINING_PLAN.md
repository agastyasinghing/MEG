# Phase 0B-R1 — Reference Repo Feature-Mining Inspection Plan

## 1) Purpose

This ticket defines a documentation-only plan to inspect selected external reference repositories for **ideas only**.

Guardrails:

- no vendoring external repositories,
- no code copying into MEG,
- no runtime or trading behavior changes,
- no strategy implementation in this ticket,
- no coupling to live execution rails,
- no autonomous execution authority.

The output of this plan is a structured review approach that turns useful observations into MEG-native backlog tickets after review.

## 2) Reference Repositories Inventory

| repo | category | likely useful ideas | what not to copy | license/review status | likely MEG phase | priority |
|---|---|---|---|---|---|---|
| `Polymarket/agents` | agent architecture | Role decomposition, tool boundary patterns, orchestration flow for agent responsibilities | Prompt/tool code, execution flows that bypass operator approval, direct implementation snippets | license + terms review required before any derivative design ticket | Phase 3+ architecture refinement | P1 |
| `skharchikov/polymarket-bot` | bot execution/trading system patterns | Bot lifecycle wiring, config structure, exchange interface separation | Strategy rules, order placement code, risk assumptions, repo-specific implementation | license + terms review required | Phase 2/3 backlog ideation | P1 |
| `Drakkar-Software/OctoBot-Prediction-Market` | bot execution/trading system patterns | Plugin-oriented extension boundaries, modular bot composition ideas | Framework internals, plugin code, direct module transplanting | license + terms review required | Phase 3+ modularity studies | P2 |
| `ImMike/polymarket-arbitrage` | arbitrage/cross-market logic | Opportunity detection framing, spread/path evaluation heuristics, market comparison checklists | Arbitrage implementation code, autonomous order logic, repo-specific risk bypasses | license + terms review required | Phase 6 arbitrage planning | P1 |
| `aulekator/Polymarket-BTC-15-Minute-Trading-Bot` | volatility/swing sidecar inspiration | Short-horizon signal packaging, evaluation cadence ideas, compact bot workflow structure | Hardcoded strategy thresholds, execution code, position sizing assumptions | license + terms review required | Phase 3+ sidecar research | P3 |
| `nautechsystems/nautilus_trader` | production trading engine architecture | Event-driven architecture patterns, replay/simulation design concepts, adapter isolation | Large framework adoption, direct engine code reuse, dependency transplants | license + terms review required | Phase 4/5 infra hardening | P1 |
| `HKUDS/AI-Trader` | swarm/agent inspiration | Multi-agent workflow concepts, experiment coordination patterns, research orchestration templates | Model pipelines/prompts/code assets copied as-is, opaque third-party dependencies | license + terms review required | Phase 5+ experimentation | P3 |
| `Jon-Becker/prediction-market-analysis` | historical dataset/research framework | Data research framing, schema/research method structure, reproducibility patterns | Dataset/code copying, unreviewed ingestion shortcuts, direct script import | partially reviewed in Phase 0B; further provenance/terms review pending | Phase 0B research planning | P0 |
| `666ghj/MiroFish` | swarm/agent inspiration | Agent coordination abstractions, task-routing inspiration, collaboration metaphors | Runtime code adoption, framework vendoring, unreviewed dependencies | license + terms review required | Phase 5+ ideation | P3 |

## 3) Suggested Category Definitions

- **agent architecture**: multi-role agent boundaries, orchestration contracts, and responsibility partitioning.
- **bot execution/trading system patterns**: structural patterns for bot lifecycle and integration boundaries (not strategy code).
- **arbitrage/cross-market logic**: opportunity framing, path analysis concepts, and comparative market heuristics.
- **production trading engine architecture**: event pipelines, replay/simulation scaffolding, adapter and engine isolation.
- **historical dataset/research framework**: schema framing, research process design, reproducibility discipline.
- **swarm/agent inspiration**: collaboration mechanics among multiple specialized agents.
- **volatility/swing sidecar inspiration**: sidecar-oriented signal packaging and short-horizon analysis structure.

## 4) Inspection Checklist (Per Repository)

For each repo inspection, capture:

1. README/docs structure (navigation quality, architecture notes, scope clarity).
2. License and terms posture.
3. Dependency stack and tooling choices.
4. Data model and schema conventions.
5. Strategy logic framing (high level only).
6. Execution/order-management architecture.
7. Risk controls and safety gates.
8. Backtesting/simulation support.
9. Monitoring/logging/observability patterns.
10. Test coverage and testing style.
11. Deployment/CI posture.
12. Unique ideas worth converting into MEG-native tickets.

## 5) Copy/Learn Rules

1. Mine ideas, not code.
2. Do not perform blind copying.
3. Do not adopt license-risk code.
4. Do not vendor external repositories.
5. Do not commit external repository files into MEG.
6. Convert findings into MEG-native tickets only after review.
7. Keep research/data ideas separate from live execution ideas.
8. Preserve canonical identifier vocabulary (`condition_id`, `token_id`, `outcome`) in MEG tickets.

## 6) Output Format Template for Future Repo Reviews

| repo | inspected commit/date | useful idea | MEG destination area | confidence | implementation risk | follow-up ticket |
|---|---|---|---|---|---|---|
| `owner/repo` | `commit_sha @ YYYY-MM-DD` | `short idea statement` | `phase/module/doc area` | `low/medium/high` | `low/medium/high` | `ticket id or TBD` |

Template notes:

- Include both commit SHA and inspection date.
- Record confidence as evidence quality, not enthusiasm.
- Record implementation risk separately to avoid over-committing to borrowed ideas.

## 7) Recommended First Batch

Recommended first 4 repositories for Phase 0B-R2:

1. **`Jon-Becker/prediction-market-analysis`**
   - already partially reviewed in Phase 0B,
   - highest immediate value for research data framing and provenance-linked planning continuity.
2. **`ImMike/polymarket-arbitrage`**
   - likely high value for cross-market/arbitrage opportunity framing,
   - helps shape future arbitrage-phase backlog without implementation.
3. **`Polymarket/agents`**
   - relevant for agent-role decomposition and orchestration patterns,
   - useful for later architecture planning while keeping operator approval constraints.
4. **`skharchikov/polymarket-bot`** (or `Drakkar-Software/OctoBot-Prediction-Market` as alternate)
   - practical reference for bot-system structural patterns,
   - can produce concrete, implementation-agnostic ticket ideas for MEG modules.

## 8) Non-goals

This ticket explicitly excludes:

- implementation work,
- external repo vendoring,
- live trading/execution changes,
- loader expansion,
- dataset import,
- dependency/workflow changes,
- generated report or data artifact commits.

## 9) Recommended Next Ticket

Choose one follow-up based on sequencing preference:

- **Phase 0B-R2**: Inspect first reference repo batch and create feature-mining notes.
- **Phase 0B-17**: Manual local archive metadata inspection once SSD is available.

