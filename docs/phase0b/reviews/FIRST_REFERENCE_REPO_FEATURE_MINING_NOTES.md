# Phase 0B-R3 — First Reference Repo Feature-Mining Notes (Placeholder)

## 1) Purpose

This document creates the first concrete first-batch feature-mining review notes container for Phase 0B planning continuity.

Current status and constraints:

- placeholder/pending only,
- ideas only,
- no code copying,
- no vendoring,
- no dependency adoption,
- no runtime or trading behavior changes,
- no execution-authority changes.

All findings from future inspection must be converted into MEG-native planning tickets before any implementation work is considered.

## 2) Batch metadata

| Field | Value |
|---|---|
| `batch_id` | `phase0b-r3-first-reference-repo-batch` |
| `review_status` | `completed_partial` |
| `reviewer` | `public/manual web inspection` |
| `review_date` | `2026-05-19` |
| `scope_summary` | `Public/manual inspection completed for ImMike/polymarket-arbitrage and Polymarket/agents; remaining repos stay not_started in this ticket.` |
| `source_template` | `docs/phase0b/reviews/REFERENCE_REPO_FEATURE_MINING_TEMPLATE.md` |

## 3) Repos in first batch

1. `Jon-Becker/prediction-market-analysis`
2. `ImMike/polymarket-arbitrage`
3. `Polymarket/agents`
4. `skharchikov/polymarket-bot`
5. `Drakkar-Software/OctoBot-Prediction-Market` (alternate)

## 4) Per-repo placeholder sections

### 4.1 Jon-Becker/prediction-market-analysis

- `repo_url`: `https://github.com/Jon-Becker/prediction-market-analysis`
- `inspected_commit_or_snapshot`: `TODO`
- `license_status`: `pending_review` (partially reviewed in prior Phase 0B work)
- `review_status`: `not_started`
- `scope_summary`: `Reusable research-methodology idea mining only; no import authorization decisions in this section.`

#### Repository structure findings

| Area | Findings | Evidence/path | Confidence | Notes |
|---|---|---|---|---|
| README/docs quality | `TODO` | `TODO` | `TODO` | `TODO` |
| Source layout | `TODO` | `TODO` | `TODO` | `TODO` |
| Dependency stack | `TODO` | `TODO` | `TODO` | `TODO` |
| Tests | `TODO` | `TODO` | `TODO` | `TODO` |
| CI/deployment | `TODO` | `TODO` | `TODO` | `TODO` |
| Data/model/schema docs | `TODO` | `TODO` | `TODO` | `TODO` |
| Examples/scripts | `TODO` | `TODO` | `TODO` | `TODO` |
| Config/secrets handling | `TODO` | `TODO` | `TODO` | `TODO` |

#### Feature-mining findings

| idea_id | useful idea | evidence/path | MEG destination area | confidence | implementation risk | copy/license risk | follow-up ticket |
|---|---|---|---|---|---|---|---|
| `IDEA-001` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |

#### Architecture checklist

| Area | Status | Evidence/path | Notes |
|---|---|---|---|
| Agent architecture | `TODO` | `TODO` | `TODO` |
| Bot lifecycle | `TODO` | `TODO` | `TODO` |
| Exchange/client abstraction | `TODO` | `TODO` | `TODO` |
| Data model | `TODO` | `TODO` | `TODO` |
| Strategy framing | `TODO` | `TODO` | `TODO` |
| Risk controls | `TODO` | `TODO` | `TODO` |
| Order/execution boundary | `TODO` | `TODO` | `TODO` |
| Backtesting/simulation | `TODO` | `TODO` | `TODO` |
| Monitoring/logging | `TODO` | `TODO` | `TODO` |
| Deployment/CI | `TODO` | `TODO` | `TODO` |

#### Decision matrix

| Decision | Status (`yes` / `no` / `needs_review` / `defer`) | Rationale | Follow-up |
|---|---|---|---|
| Useful for MEG backlog | `needs_review` | `TODO` | `TODO` |
| Safe to convert into planning ticket | `needs_review` | `TODO` | `TODO` |
| Needs license review | `needs_review` | `TODO` | `TODO` |
| Too risky / do not use | `needs_review` | `TODO` | `TODO` |
| Defer until later phase | `needs_review` | `TODO` | `TODO` |

### 4.2 ImMike/polymarket-arbitrage

- `repo_url`: `https://github.com/ImMike/polymarket-arbitrage`
- `inspected_commit_or_snapshot`: `7e4acc19aec11c770e9ce41c6c04634e24bfed39`
- `license_status`: `pending_review` (license file visibility not conclusively captured in this pass)
- `review_status`: `completed_partial`
- `scope_summary`: `Manual web inspection focused on cross-platform arbitrage framing, market matching, spread thresholds, and execution-safety gaps; evidence precision polished with commit-level and README-section references.`
- `evidence_note`: `Latest inspected commit found via GitHub commit search; commit message references Kalshi integration and cross-platform arbitrage.`

#### Repository structure findings

| Area | Findings | Evidence/path | Confidence | Notes |
|---|---|---|---|---|
| README/docs quality | `README Features enumerates cross-platform arbitrage, bundle arbitrage, market making, risk management, dashboard, fee accounting, logging, and market matching` | `README Features section (public web view, inspected 2026-05-19)` | `medium` | `Sufficient for idea mining without code reuse.` |
| Source layout | `README Project Structure lists polymarket_client, kalshi_client, core/data_feed.py, core/arb_engine.py, core/cross_platform_arb.py, core/execution.py, core/risk_manager.py, core/portfolio.py` | `README Project Structure section + README run instructions` | `medium` | `No local clone/vendoring performed.` |
| Dependency stack | `Python-based bot implied` | `Repo subtitle and README getting-started context` | `low` | `Do not infer exact package set without file-level review.` |
| Tests | `not confirmed` | `no explicit test evidence captured in this pass` | `low` | `Leave for future deeper inspection.` |
| CI/deployment | `not confirmed` | `no explicit CI evidence captured in this pass` | `low` | `Leave as follow-up.` |
| Data/model/schema docs | `Strategy-level docs present; schema discipline not explicit` | `README strategy tables and examples` | `low` | `Canonical ID alignment must stay MEG-native.` |
| Examples/scripts | `README Data Modes/Real Mode describes Gamma API market discovery, CLOB order book fetching, and 5,000+ market scan workflow` | `README Data Modes / Real Mode sections (public web view, inspected 2026-05-19)` | `high` | `Use as conceptual inspiration only.` |
| Config/secrets handling | `README Configuration lists trading_mode, min_edge, min_spread, max_position_per_market, max_global_exposure, max_daily_loss` | `README Configuration section (public web view, inspected 2026-05-19)` | `medium` | `No secret handling endorsement from this pass.` |

#### Feature-mining findings

| idea_id | useful idea | evidence/path | MEG destination area | confidence | implementation risk | copy/license risk | follow-up ticket |
|---|---|---|---|---|---|---|---|
| `IMMIKE-IDEA-001` | `Cross-platform opportunity lane can be modeled as normalized YES/NO comparison after semantic market pair matching.` | `README cross-platform arbitrage section, text-similarity matching claim` | `Phase 0B planning: opportunity detector contracts` | `medium` | `medium` | `low if reimplemented MEG-native` | `Phase0B-R5-planning-ticket-candidate` |
| `IMMIKE-IDEA-002` | `Bundle mispricing checks (YES+NO vs 1.00) suggest a reusable invariant monitor for pricing sanity alerts.` | `README bundle arbitrage condition table` | `risk/monitoring planning` | `high` | `low` | `low` | `Phase0B-R5-planning-ticket-candidate` |
| `IMMIKE-IDEA-003` | `Threshold framing (minimum edge after fees, minimum spread) is useful for explicit guardrail configuration in paper-only execution paths.` | `README configuration parameters min_edge/min_spread` | `execution/risk-gate planning` | `high` | `low` | `low` | `Phase0B-R5-planning-ticket-candidate` |
| `IMMIKE-IDEA-004` | `Risk gap observed: strategy text implies fast arbitrage but does not itself prove operator-approval enforcement; MEG must keep Telegram approval as hard gate.` | `README “go trade” framing and autonomous strategy language` | `operator approval boundary` | `medium` | `high if misapplied` | `low` | `Phase0B-R5-approval-boundary-ticket` |

#### Architecture checklist

| Area | Status | Evidence/path | Notes |
|---|---|---|---|
| Agent architecture | `partial` | `README strategy sections` | `Single-bot strategy framing observed.` |
| Bot lifecycle | `partial` | `README dashboard + mode toggles` | `Dry-run/live and data mode ideas are notable.` |
| Exchange/client abstraction | `partial` | `Cross-platform Polymarket/Kalshi narrative` | `Conceptual abstraction idea only.` |
| Data model | `needs_review` | `no explicit schema capture` | `Keep canonical identifiers in MEG docs/tickets.` |
| Strategy framing | `yes` | `Cross-platform + bundle + MM sections` | `Good source of idea vocabulary.` |
| Risk controls | `partial` | `min_edge/min_spread parameters` | `Threshold gating ideas useful.` |
| Order/execution boundary | `needs_review` | `no explicit operator approval control shown` | `MEG must preserve Telegram approvals.` |
| Backtesting/simulation | `partial` | `data_mode includes simulation/real` | `Potential planning input only.` |
| Monitoring/logging | `partial` | `dashboard metrics list` | `Useful operational metrics shortlist.` |
| Deployment/CI | `needs_review` | `not inspected` | `Out of scope this pass.` |

#### Decision matrix

| Decision | Status (`yes` / `no` / `needs_review` / `defer`) | Rationale | Follow-up |
|---|---|---|---|
| Useful for MEG backlog | `yes` | `Clear conceptual ideas for opportunity detection and threshold gates.` | `Phase0B-R5` |
| Safe to convert into planning ticket | `yes` | `Evidence sufficient for MEG-native ticket drafting only.` | `Phase0B-R5` |
| Needs license review | `yes` | `License compatibility not conclusively verified in this pass.` | `Phase0B-R6-license-pass` |
| Too risky / do not use | `no` | `Ideas are usable if limited to concept-level and no code reuse.` | `N/A` |
| Defer until later phase | `yes` | `Any execution/runtime adoption deferred pending approval architecture and risk review.` | `Phase0B-implementation-later` |

### 4.3 Polymarket/agents

- `repo_url`: `https://github.com/Polymarket/agents`
- `inspected_commit_or_snapshot`: `30118b308bbb3dbb339980d0adf9d3daf8be9926`
- `license_status`: `pending_review` (README states MIT; ToS/jurisdiction and compatibility still require internal legal/compliance confirmation)
- `review_status`: `completed_partial`
- `scope_summary`: `Manual web inspection focused on agent-role decomposition, tooling boundaries, connector layers, and reasoning-versus-execution separation cues; archived/read-only status and ToS caveats captured for planning-only use.`
- `evidence_note`: `Repo appeared archived/read-only on GitHub page inspection; treat as historical architecture reference only.`
- `evidence_note`: `README states MIT and also states US persons and persons from certain other jurisdictions are prohibited from trading via UI/API/agents while data/information is viewable globally.`
- `jurisdiction_note`: `This review does not assert US-only blocking; any live trading/API/agent usage requires separate jurisdiction-specific ToS/legal/compliance review.`
- `approval_note`: `Phase 0B-R4 output is architecture/backlog planning only and does not approve live agent trading or API execution.`

#### Repository structure findings

| Area | Findings | Evidence/path | Confidence | Notes |
|---|---|---|---|---|
| README/docs quality | `README Features lists Polymarket API integration, AI agent utilities, local/remote RAG, betting/news/web data sourcing, and LLM prompt tooling` | `README Features section (public web view, inspected 2026-05-19)` | `high` | `Good high-level design signal.` |
| Source layout | `Top-level folders include agents, docs, scripts, tests, and .github` | `repository tree on root page` | `high` | `Supports modular framing.` |
| Dependency stack | `Python 3.9 + requirements.txt + Dockerfile` | `README getting started + root files list` | `high` | `No dependency adoption in MEG from this ticket.` |
| Tests | `tests directory present` | `repository tree` | `medium` | `No test internals inspected.` |
| CI/deployment | `.github workflows present; containerization support present` | `repository tree includes .github and Dockerfile` | `medium` | `Workflow details not deep-inspected.` |
| Data/model/schema docs | `README Architecture/APIs describes Chroma, Gamma, Polymarket, and Objects/Pydantic models` | `README Architecture/APIs section (public web view, inspected 2026-05-19)` | `high` | `Useful for interface-boundary planning.` |
| Examples/scripts | `README Scripts identifies CLI as primary interface with commands for API interaction, news retrieval, local data queries, LLM prompts, and trade execution` | `README Scripts section (public web view, inspected 2026-05-19)` | `high` | `Indicates clear run surfaces.` |
| Config/secrets handling | `.env.example and required keys documented` | `root file list + README env vars` | `high` | `Security boundary reminder for MEG docs.` |

#### Feature-mining findings

| idea_id | useful idea | evidence/path | MEG destination area | confidence | implementation risk | copy/license risk | follow-up ticket |
|---|---|---|---|---|---|---|---|
| `POLYAGENTS-IDEA-001` | `Explicit connector layer per external service can keep reasoning components isolated from exchange transport logic.` | `README architecture/API connector bullets` | `shared rail interface planning` | `high` | `low` | `low` | `Phase0B-R5-interface-ticket` |
| `POLYAGENTS-IDEA-002` | `Separation of CLI/research utilities from direct trade entrypoints can inform MEG’s analysis-vs-execution boundary.` | `README references CLI path and separate trade script` | `execution boundary planning` | `medium` | `medium` | `low` | `Phase0B-R5-boundary-ticket` |
| `POLYAGENTS-IDEA-003` | `Structured env/bootstrap docs suggest adopting explicit operator runbook artifacts before any new automation is approved.` | `README setup steps with .env workflow` | `ops/runbook planning` | `high` | `low` | `low` | `Phase0B-R5-runbook-ticket` |
| `POLYAGENTS-IDEA-004` | `Autonomous trade framing highlights a safety contrast: MEG must preserve Telegram operator approval as mandatory execution gate.` | `README “Trade autonomously” tagline` | `approval governance` | `high` | `high if ignored` | `low` | `Phase0B-R5-approval-boundary-ticket` |

#### Architecture checklist

| Area | Status | Evidence/path | Notes |
|---|---|---|---|
| Agent architecture | `yes` | `agents/ folder + architecture section` | `Modular decomposition clearly signaled.` |
| Bot lifecycle | `partial` | `CLI + trade entrypoints` | `Lifecycle cues present; deeper flow pending.` |
| Exchange/client abstraction | `yes` | `Gamma/Polymarket connector descriptions` | `Strong candidate idea for MEG-native adapter boundaries.` |
| Data model | `partial` | `market/event metadata references` | `Canonical field mapping to MEG still future work.` |
| Strategy framing | `partial` | `framework-level, not a fixed strategy` | `Useful for orchestration, not strategy logic itself.` |
| Risk controls | `needs_review` | `no hard operator approval control visible in skim` | `Do not infer safety controls without deeper evidence.` |
| Order/execution boundary | `partial` | `trade script separated from other tooling` | `Promising boundary pattern.` |
| Backtesting/simulation | `needs_review` | `not explicitly observed` | `Out of scope for this pass.` |
| Monitoring/logging | `needs_review` | `not explicitly observed` | `Future pass.` |
| Deployment/CI | `partial` | `.github + Dockerfile presence` | `Need deeper workflow review later.` |

#### Decision matrix

| Decision | Status (`yes` / `no` / `needs_review` / `defer`) | Rationale | Follow-up |
|---|---|---|---|
| Useful for MEG backlog | `yes` | `Strong architecture-boundary and orchestration signals.` | `Phase0B-R5` |
| Safe to convert into planning ticket | `yes` | `Public evidence sufficient for concept tickets.` | `Phase0B-R5` |
| Needs license review | `needs_review` | `README indicates MIT, but ToS/jurisdiction/compliance review remains required before any usage beyond planning.` | `Phase0B-R6-license-pass` |
| Too risky / do not use | `no` | `Conceptual use is acceptable with no code copying.` | `N/A` |
| Defer until later phase | `yes` | `Archived/read-only repo and planning-only scope mean live agent trading/API execution remains unapproved in this review.` | `Phase0B-implementation-later` |

### 4.4 skharchikov/polymarket-bot

- `repo_url`: `https://github.com/skharchikov/polymarket-bot`
- `inspected_commit_or_snapshot`: `TODO`
- `license_status`: `pending_review`
- `review_status`: `not_started`
- `scope_summary`: `Idea-mining placeholder for bot lifecycle and execution-boundary architecture patterns.`

#### Repository structure findings

| Area | Findings | Evidence/path | Confidence | Notes |
|---|---|---|---|---|
| README/docs quality | `TODO` | `TODO` | `TODO` | `TODO` |
| Source layout | `TODO` | `TODO` | `TODO` | `TODO` |
| Dependency stack | `TODO` | `TODO` | `TODO` | `TODO` |
| Tests | `TODO` | `TODO` | `TODO` | `TODO` |
| CI/deployment | `TODO` | `TODO` | `TODO` | `TODO` |
| Data/model/schema docs | `TODO` | `TODO` | `TODO` | `TODO` |
| Examples/scripts | `TODO` | `TODO` | `TODO` | `TODO` |
| Config/secrets handling | `TODO` | `TODO` | `TODO` | `TODO` |

#### Feature-mining findings

| idea_id | useful idea | evidence/path | MEG destination area | confidence | implementation risk | copy/license risk | follow-up ticket |
|---|---|---|---|---|---|---|---|
| `IDEA-001` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |

#### Architecture checklist

| Area | Status | Evidence/path | Notes |
|---|---|---|---|
| Agent architecture | `TODO` | `TODO` | `TODO` |
| Bot lifecycle | `TODO` | `TODO` | `TODO` |
| Exchange/client abstraction | `TODO` | `TODO` | `TODO` |
| Data model | `TODO` | `TODO` | `TODO` |
| Strategy framing | `TODO` | `TODO` | `TODO` |
| Risk controls | `TODO` | `TODO` | `TODO` |
| Order/execution boundary | `TODO` | `TODO` | `TODO` |
| Backtesting/simulation | `TODO` | `TODO` | `TODO` |
| Monitoring/logging | `TODO` | `TODO` | `TODO` |
| Deployment/CI | `TODO` | `TODO` | `TODO` |

#### Decision matrix

| Decision | Status (`yes` / `no` / `needs_review` / `defer`) | Rationale | Follow-up |
|---|---|---|---|
| Useful for MEG backlog | `needs_review` | `TODO` | `TODO` |
| Safe to convert into planning ticket | `needs_review` | `TODO` | `TODO` |
| Needs license review | `needs_review` | `TODO` | `TODO` |
| Too risky / do not use | `needs_review` | `TODO` | `TODO` |
| Defer until later phase | `needs_review` | `TODO` | `TODO` |

### 4.5 Drakkar-Software/OctoBot-Prediction-Market (alternate)

- `repo_url`: `https://github.com/Drakkar-Software/OctoBot-Prediction-Market`
- `inspected_commit_or_snapshot`: `TODO`
- `license_status`: `pending_review`
- `review_status`: `not_started`
- `scope_summary`: `Alternate idea-mining placeholder for modular bot extension boundaries.`

#### Repository structure findings

| Area | Findings | Evidence/path | Confidence | Notes |
|---|---|---|---|---|
| README/docs quality | `TODO` | `TODO` | `TODO` | `TODO` |
| Source layout | `TODO` | `TODO` | `TODO` | `TODO` |
| Dependency stack | `TODO` | `TODO` | `TODO` | `TODO` |
| Tests | `TODO` | `TODO` | `TODO` | `TODO` |
| CI/deployment | `TODO` | `TODO` | `TODO` | `TODO` |
| Data/model/schema docs | `TODO` | `TODO` | `TODO` | `TODO` |
| Examples/scripts | `TODO` | `TODO` | `TODO` | `TODO` |
| Config/secrets handling | `TODO` | `TODO` | `TODO` | `TODO` |

#### Feature-mining findings

| idea_id | useful idea | evidence/path | MEG destination area | confidence | implementation risk | copy/license risk | follow-up ticket |
|---|---|---|---|---|---|---|---|
| `IDEA-001` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |

#### Architecture checklist

| Area | Status | Evidence/path | Notes |
|---|---|---|---|
| Agent architecture | `TODO` | `TODO` | `TODO` |
| Bot lifecycle | `TODO` | `TODO` | `TODO` |
| Exchange/client abstraction | `TODO` | `TODO` | `TODO` |
| Data model | `TODO` | `TODO` | `TODO` |
| Strategy framing | `TODO` | `TODO` | `TODO` |
| Risk controls | `TODO` | `TODO` | `TODO` |
| Order/execution boundary | `TODO` | `TODO` | `TODO` |
| Backtesting/simulation | `TODO` | `TODO` | `TODO` |
| Monitoring/logging | `TODO` | `TODO` | `TODO` |
| Deployment/CI | `TODO` | `TODO` | `TODO` |

#### Decision matrix

| Decision | Status (`yes` / `no` / `needs_review` / `defer`) | Rationale | Follow-up |
|---|---|---|---|
| Useful for MEG backlog | `needs_review` | `TODO` | `TODO` |
| Safe to convert into planning ticket | `needs_review` | `TODO` | `TODO` |
| Needs license review | `needs_review` | `TODO` | `TODO` |
| Too risky / do not use | `needs_review` | `TODO` | `TODO` |
| Defer until later phase | `needs_review` | `TODO` | `TODO` |

## 5) Jon-Becker special handling

- Jon-Becker was already partially reviewed for data/research context in Phase 0B-14/15-era review flow.
- Do not duplicate archive inspection from prior/manual local archive tracks.
- Dataset/archive provenance remains pending and must be handled in dedicated provenance-focused follow-up work.
- This R3 notes file is limited to reusable research-methodology idea capture planning and is not import approval.

## 6) Safety and copy/learn rules

1. Mine ideas, not code.
2. No external repository files are copied into MEG.
3. No vendoring of external repositories.
4. No dependency adoption in this placeholder ticket.
5. No runtime or execution-path changes.
6. No bypassing operator approval (Telegram approval remains mandatory).
7. Useful findings must become MEG-native planning tickets only.

## 7) Non-goals

- no deep/full repository inspection in this ticket (targeted public/manual inspection only),
- no implementation,
- no dependency changes,
- no dataset import,
- no loader expansion,
- no generated reports or data-file outputs.

## 8) Recommended next ticket

Choose one based on sequencing preference:

- **Phase 0B-R4**: Fill first reference repo feature-mining notes from manual/web inspection.
- **Phase 0B-17**: Manual local archive metadata inspection once SSD is available.
