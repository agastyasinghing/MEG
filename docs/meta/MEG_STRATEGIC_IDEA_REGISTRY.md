# MEG Strategic Idea Registry

## 1) Purpose and usage
Store high-upside ideas so they are not lost. This registry is not implementation approval. Ideas must become PRD tickets before implementation. Each idea should include status, likely phase, dependencies, and risk.

## 2) Idea status taxonomy
- active_next
- candidate_near_term
- parked
- needs_research
- blocked_by_dependency
- rejected_for_now

## 3) Idea categories
- MEG-core architecture
- Weather-core
- Quant/research depth
- Product/resume polish
- Later execution/trading governance

## 4) Strategic idea table
| Idea | Category | Status | Why it matters | Likely phase | Dependencies | Risks | Possible future tickets |
|---|---|---|---|---|---|---|---|
| Canonical cross-market event graph (weather bot as first proving ground) | MEG-core architecture | active_next | First-class mapping between real-world events and venue markets | Phase 1 planning | PRD approval + taxonomy work | Premature scope expansion | PRD-MEG-EVENT-GRAPH-01, PRD-MEG-EVENT-GRAPH-02, PRD-P1-WX-EVENT-GRAPH-PILOT |
| Proposal envelope schema with event identity, venue markets, odds snapshot, liquidity snapshot, confidence score, risk flags, no-trade reason, human-review summary | MEG-core architecture | candidate_near_term | Typed candidate/opportunity contract | Phase 1 | Event identity groundwork | Overfitting early schema | PRD-MEG-PROPOSAL-ENVELOPE-01 |
| Runtime topology documentation | Product/resume polish / architecture clarity | candidate_near_term | Explains services/processes/queues/stores clearly | Phase 1 docs | Stable topology draft | Drift with implementation | DOCS-RUNTIME-TOPOLOGY-01 |
| Research vs production boundary | MEG-core architecture | active_next | Separates DuckDB research from production ingestion/signal/execution | Phase 1 gates | Current boundary docs | Ambiguity across tickets | PRD-MEG-BOUNDARY-01 |
| Golden path tests | Engineering maturity | needs_research | One end-to-end story per phase avoids test sprawl | Phase 1+ | Stable scenarios | Brittle over-constraint | TEST-GOLDEN-PATH-01, TEST-GOLDEN-PATH-WX-01 |
| Reviewer-facing README section | Product/resume polish | candidate_near_term | Helps reviewers understand MEG quickly | Phase 1 docs | Finalized narrative | Oversimplification | DOCS-README-REVIEWER-01 |
| Multi-market vision section | Product/strategy | parked | Clarifies venue roadmap and discrepancy priorities | Phase 1-2 | Strategic alignment | Premature commitments | DOCS-MULTI-MARKET-VISION-01 |
| Weather canonical event taxonomy | Weather-core | active_next | Define weather event identity before provider/API work | PRD-P1-WX-01 | Kickoff plan | Taxonomy churn | PRD-P1-WX-01 |
| Weather resolution rule risk classifier | Weather-core | candidate_near_term | Markets resolve on exact stations/windows/sources/thresholds | Phase 1 | Taxonomy + rule parsing | False confidence | PRD-P1-WX-RESOLUTION-RISK-01 |
| Weather provider compatibility matrix | Weather-core | blocked_by_dependency | Provider value depends on resolution compatibility | Phase 1 | Taxonomy + resolution classifier | Connector pull-in too early | PRD-P1-WX-02 |
| Forecast uncertainty / probability distribution model | Weather-core / quant research | needs_research | Threshold markets need distributions, not only point forecasts | Phase 1-2 | Historical weather framing | Poor calibration | PRD-P1-WX-FORECAST-DISTRIBUTION-01 |
| Weather market trap taxonomy | Weather-core | candidate_near_term | Detect ambiguous location/source mismatch/stale odds/low liquidity/time-zone traps | Phase 1 | Taxonomy baseline | Excess false positives | PRD-P1-WX-TRAP-TAXONOMY-01 |
| Regime detection and regime-aware signals | Quant/research depth | parked | Behavior varies by volatility/news/liquidity regime | Phase 2+ | Robust feature rails | Spurious regimes | PRD-MEG-REGIME-01 |
| Synthetic fair-value engine | Quant/research depth | needs_research | Compare model-implied probability vs venue odds | Phase 2+ | Feature + uncertainty rails | Model risk | PRD-MEG-FAIR-VALUE-01 |
| Simulation and counterfactual backtesting engine | Quant/research depth | needs_research | Replay historical data and simulate decisions | Phase 2+ | Clean historical rails | Overfit simulation | PRD-MEG-SIM-01 |
| Meta-whale / cross-venue identity tracking | Quant/research depth | parked | Cluster cohorts/wallets and estimate signal quality | Phase 2+ | Identity data contracts | Attribution errors | PRD-MEG-IDENTITY-01 |
| Hero end-to-end story | Product/resume polish / research validation | candidate_near_term | One historical event narrative for README/blog/resume | Phase 1 docs | Stable narrative | Cherry-picking perception | DOCS-HERO-STORY-01 |

## 5) Weather bot-specific strategic notes
- Weather bot should likely be canonical event graph proving ground.
- Weather provider research should prioritize resolution compatibility, not only accuracy/price.
- Human review output should include no-trade reasons.
- Weather trap taxonomy should likely be near-term.
- Forecast distributions matter more than point forecasts.

## 6) Parking lot rules
- Do not implement directly from this registry.
- Convert idea to PRD ticket first.
- Any idea touching external API, runtime execution, trading, autonomy, secrets, or generated artifacts needs an approval gate.
- Update registry after major phase transitions.
