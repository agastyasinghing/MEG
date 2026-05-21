# Phase 0B-20C — Cross-Platform Semantic Matching and Opportunity Research Plan (Docs-Only)

## 1) Purpose and posture

This ticket is **documentation-only** and defines a **research plan plus review framework** for Kalshi/Polymarket cross-platform semantic matching and opportunity research.

This ticket is **not implementation** and does not approve:

- data import,
- fixture derivation,
- loaders,
- query engines,
- connector use,
- order routing,
- live trading,
- autonomous execution.

All outputs are reviewer-facing research candidates only:

- candidate market pairs,
- candidate opportunity records,
- candidate rejection reasons.

No output from this plan has execution authority.

Phase 0B posture remains intentionally **under-inclusive**: candidate pairs are non-equivalent until proven equivalent by rules-level evidence.

## 2) Durable source appendix (official/primary first)

Access date for all rows: **2026-05-20**.

| Source title | Publisher/platform | Durable URL | Access date | Claim supported |
|---|---|---|---|---|
| Welcome to Kalshi’s API Documentation | Kalshi Docs | https://docs.kalshi.com/welcome | 2026-05-20 | Kalshi exposes official API docs and product primitives used for metadata acquisition planning. |
| Quick Start: Market Data | Kalshi Docs | https://docs.kalshi.com/getting_started/quick_start_market_data | 2026-05-20 | Kalshi market data access model and baseline API surface for read paths. |
| API Keys | Kalshi Docs | https://docs.kalshi.com/getting_started/api_keys | 2026-05-20 | Kalshi auth/key requirements must be modeled in data provenance and availability assumptions. |
| Rate Limits and Tiers | Kalshi Docs | https://docs.kalshi.com/getting_started/rate_limits | 2026-05-20 | Rate limiting affects polling cadence, freshness parity, and cross-platform comparability. |
| Kalshi Glossary | Kalshi Docs | https://docs.kalshi.com/getting_started/terms | 2026-05-20 | Canonical Kalshi terms for series/event/market semantics. |
| Get Series | Kalshi Docs | https://docs.kalshi.com/api-reference/market/get-series | 2026-05-20 | Kalshi hierarchy includes series-level entities above events/markets. |
| Market Outcomes | Kalshi Help Center | https://help.kalshi.com/en/articles/13823826-market-outcomes | 2026-05-20 | Outcome semantics and payout framing are rules-critical for equivalence review. |
| Market Lifecycle | Kalshi Docs | https://docs.kalshi.com/getting_started/market_lifecycle | 2026-05-20 | Lifecycle states include active/inactive/closed/determined/disputed/amended/finalized and timing transitions. |
| Orderbook Responses | Kalshi Docs | https://docs.kalshi.com/getting_started/orderbook_responses | 2026-05-20 | Kalshi orderbook side representation requires complementary YES/NO reconstruction for implied asks. |
| Maintenance and Pauses | Kalshi Docs | https://docs.kalshi.com/getting_started/maintenance_and_pauses | 2026-05-20 | Venue modes (maintenance/pause behavior) can block executability comparability. |
| Get Exchange Status | Kalshi Docs | https://docs.kalshi.com/api-reference/exchange/get-exchange-status | 2026-05-20 | Exchange status is required for operational mode gating and blockers. |
| Fees | Kalshi Help Center | https://help.kalshi.com/en/articles/13823805-fees | 2026-05-20 | Fee mechanics must be included in fee-adjusted edge checks. |
| Fee Schedule | Kalshi | https://kalshi.com/fee-schedule | 2026-05-20 | Official fee schedule baseline for venue-cost normalization. |
| Get Series Fee Changes | Kalshi Docs | https://docs.kalshi.com/api-reference/exchange/get-series-fee-changes | 2026-05-20 | Dynamic fee updates require timestamped fee-source provenance. |
| Kalshi Member Agreement | Kalshi | https://kalshi.com/docs/kalshi-member-agreement.pdf | 2026-05-20 | Contractual/legal surface constraints influence compliance review boundaries. |
| Introduction | Polymarket Docs | https://docs.polymarket.com/api-reference/introduction | 2026-05-20 | Polymarket API overview and platform access assumptions. |
| Authentication | Polymarket Docs | https://docs.polymarket.com/api-reference/authentication | 2026-05-20 | Auth constraints and signed request requirements affect data acquisition pathways. |
| Clients & SDKs | Polymarket Docs | https://docs.polymarket.com/api-reference/clients-sdks | 2026-05-20 | Client ecosystem details relevant to provenance/version capture. |
| Markets & Events | Polymarket Docs | https://docs.polymarket.com/concepts/markets-events | 2026-05-20 | Polymarket hierarchy is event -> market with tokenized outcome context. |
| Get market by id | Polymarket Docs | https://docs.polymarket.com/api-reference/markets/get-market-by-id | 2026-05-20 | Native Polymarket market lookups and identifiers for source mapping. |
| Prices & Orderbook | Polymarket Docs | https://docs.polymarket.com/concepts/prices-orderbook | 2026-05-20 | Display prices may differ from executable bid/ask; execution checks must use orderbook levels. |
| Resolution | Polymarket Docs | https://docs.polymarket.com/concepts/resolution | 2026-05-20 | Resolution path and oracle process are core equivalence/rejection evidence. |
| Fees | Polymarket Docs | https://docs.polymarket.com/trading/fees | 2026-05-20 | Fee semantics for net-edge evaluation and opportunity survivability. |
| Rate Limits | Polymarket Docs | https://docs.polymarket.com/api-reference/rate-limits | 2026-05-20 | Sampling parity constraints across venues; stale/latency risk context. |
| Geographic Restrictions | Polymarket Docs | https://docs.polymarket.com/api-reference/geoblock | 2026-05-20 | Geo restrictions create platform/regulatory-mode blockers. |
| Geographic Restrictions | Polymarket Help Center | https://help.polymarket.com/en/articles/13364163-geographic-restrictions | 2026-05-20 | Additional geo/legal guidance supporting non-equivalence/regulatory checks. |
| Matching Engine Restarts | Polymarket Docs | https://docs.polymarket.com/trading/matching-engine | 2026-05-20 | Restart and venue-mode behavior must gate opportunity eligibility. |
| Create Order | Polymarket Docs | https://docs.polymarket.com/trading/orders/create | 2026-05-20 | Order placement semantics confirm bid/ask executability requirements. |
| Negative Risk Markets | Polymarket Docs | https://docs.polymarket.com/advanced/neg-risk | 2026-05-20 | Negative-risk market structures require separate caution and blocker logic. |
| USA Waitlist / site legal language | Polymarket | https://polymarket.com/usa | 2026-05-20 | Distinction between international Polymarket context and US-specific surface. |
| CFTC Designates KalshiEX LLC as a Contract Market | U.S. CFTC | https://www.cftc.gov/PressRoom/PressReleases/8302-20 | 2026-05-20 | Kalshi DCM designation context for regulatory-mode modeling. |
| Industry Filings: Designated Contract Markets | U.S. CFTC | https://www.cftc.gov/IndustryOversight/IndustryFilings/TradingOrganizations | 2026-05-20 | Official DCM listing context and regulator source hierarchy. |
| Designated Contract Markets: Kalshi | U.S. CFTC | https://www.cftc.gov/IndustryOversight/IndustryFilings/TradingOrganizations/42993 | 2026-05-20 | Regulator-maintained Kalshi listing for authoritative platform mode context. |
| CFTC Orders Event-Based Binary Options Markets Operator to Pay $1.4 Million Penalty | U.S. CFTC | https://www.cftc.gov/PressRoom/PressReleases/8478-22 | 2026-05-20 | Regulatory enforcement context for legal/compliance risk awareness. |
| Building on PoS | Polygon Developer Docs | https://docs.polygon.technology/pos/get-started/building-on-polygon | 2026-05-20 | Supporting chain context for Polygon-based settlement/data interpretation. |
| RPC endpoints | Polygon Developer Docs | https://docs.polygon.technology/pos/reference/rpc-endpoints | 2026-05-20 | RPC availability and reliability context for supporting timestamp/provenance controls. |

## 3) Platform mechanics comparison

### 3.1 Structural hierarchy and identity

- Kalshi hierarchy: `series -> events -> markets`.
- Polymarket hierarchy: `events -> markets`, with source market, token, and condition identities that must be preserved as separate fields.
- Matching must preserve native IDs and avoid collapsing both venues into a single title/question table.

### 3.2 Price and orderbook interpretation

- Kalshi orderbook responses are bid-side oriented; implied asks require complementary YES/NO reconstruction.
- Polymarket display prices can reflect midpoint or last trade depending on spread state; executable values are bid/ask levels.
- Cross-platform edge checks must use executable bid/ask and visible depth only.

### 3.3 Lifecycle and timing

- Kalshi lifecycle states include: active, inactive, closed, determined, disputed, amended, finalized.
- Kalshi close time can shift earlier when `can_close_early` is true.
- Polymarket final resolution path depends on UMA Optimistic Oracle framing.
- Timing mismatches across close/end/resolution windows are hard blockers unless human review confirms equivalence.

### 3.4 Venue-mode and market-mode cautions

- Polymarket sports markets need extra caution near/after official start boundaries.
- Polymarket negative-risk markets require separate normalization and manual review.
- Venue states such as maintenance, pauses, matching-engine restart, post-only, and close-only must be modeled as non-equivalence/opportunity blockers where relevant.

## 4) Semantic matching framework (planning-only)

### 4.1 Core principles

1. Rule-aware matching, not title-aware matching.
2. Similar titles/questions are insufficient.
3. Non-equivalent until proven equivalent with rules-level evidence.

### 4.2 Required normalized field groups

- platform/regulatory mode,
- native IDs,
- display semantics,
- outcome model,
- timing,
- rule/resolution evidence,
- market mode,
- executability,
- fee fields.

### 4.3 Candidate generation flow

1. Normalize official metadata from each venue.
2. Apply coarse topic/entity/category/time filtering.
3. Apply hard blockers first.
4. Compare rules and resolution evidence.
5. Score only after blockers pass.
6. Send surviving records to a human review queue.

### 4.4 Similarity scoring dimensions

- proposition semantics,
- resolution/rules equivalence,
- temporal window,
- outcome compatibility,
- entity alignment,
- platform-mode compatibility,
- executability/liquidity.

### 4.5 Score bands (internal planning heuristics only)

- `>= 0.90` and no hard blockers: equivalent pending human approval.
- `0.75-0.89`: needs deep human review.
- `< 0.75`: reject.

These thresholds are internal heuristic planning values only and are not production logic.

## 5) Hard blockers and rejection reasons

| Hard blocker | Why it blocks |
|---|---|
| Different rule text or source hierarchy | Core proposition/resolution could differ even when wording looks similar. |
| Different close/end/resolution windows | Time boundary differences can invert outcome truth conditions. |
| Multi-outcome or negative-risk dependency on one side | Structure mismatch invalidates direct binary equivalence unless manually decomposed. |
| One side lacks active orderbook trading | Candidate cannot be evaluated as executable opportunity. |
| Maintenance/pause/restart/post-only mode | Venue status undermines comparability and execution assumptions. |
| Sports market near/after official start | Market integrity and timing semantics may diverge rapidly. |
| Geographic restriction or regulatory-mode mismatch | Platform mode/legal surface mismatch invalidates comparability. |
| Missing authoritative rule URL or rule snapshot | No durable evidence for rules-level equivalence. |
| International Polymarket vs Polymarket US ambiguity | Jurisdiction mode ambiguity blocks equivalence claims. |
| Missing fee/liquidity/executability basis | Edge cannot be trusted without net-cost and depth basis. |

## 6) Cross-platform opportunity taxonomy (research labels only)

- **True arbitrage**: strictly executable cross-venue construction that implies locked-in gross edge under validated equivalence.
- **Fee-adjusted arbitrage**: arbitrage candidate that remains positive after venue fees and slippage reserve.
- **Mispricing**: comparable outcomes priced materially apart without guaranteed lock-in.
- **Stale-price divergence**: one side appears lagged relative to fresher comparable quotes.
- **Liquidity-gap opportunity**: apparent edge exists but depth asymmetry dominates realizability risk.
- **Latency-sensitive opportunity**: edge likely collapses under realistic quote staleness/network latency.
- **Resolution-mismatch risk**: apparent edge likely driven by non-equivalent resolution logic.
- **Non-equivalent-market false positive**: title-level similarity that fails rules-level equivalence.

Rules:

- Labels are downstream research labels only.
- No label may be assigned before equivalence review.
- No label is trading advice.
- No label approves order placement.

## 7) Conservative acceptance criteria

### A) Before calling a pair equivalent

All must be true:

- same real-world event,
- same subject/population,
- same operator/comparator/threshold,
- same effective outcome window,
- materially equivalent rule text,
- materially equivalent authoritative source/resolution logic,
- exact Yes/No polarity,
- no hidden outcome dependency,
- simple binary-to-binary structure unless manually reviewed,
- durable native IDs, market URLs, rule URLs, and rule snapshot,
- operationally valid status on both sides.

### B) Before calling a pair an opportunity candidate

All must be true:

- pair already passed equivalence review,
- both sides have live orderbook trading enabled,
- neither side is paused/restarting/post-only in a disqualifying way,
- executable bid/ask prices are used (not midpoint/last/display),
- fee-adjusted edge survives venue fees plus slippage reserve,
- visible depth exists,
- quote timestamps are comparable,
- human signoff exists.

### C) What remains human-reviewed in Phase 0B

- custom rule text,
- threshold/exclusion/official-boundary qualifiers,
- Polymarket negative-risk or multi-outcome contexts,
- sports markets near game start,
- dynamic fee states,
- unusual venue modes,
- international Polymarket vs Polymarket US assumptions.

## 8) MEG data/model implications

- Keep `source_event`, `source_market`, and `source_outcome` as separate model entities.
- Do not flatten all venue records into one title/question table.
- Store source rule text plus rule URL snapshots.
- Store platform/regulatory mode separately.
- Store venue mode on snapshots.
- Store raw provenance, parser/source version, and reviewer decision history.
- Cross-platform alignment intersects with Polymarket normalization via `condition_id`, `clob_token_ids`, `outcomes`, `maker_asset_id`, `taker_asset_id`.
- Cross-platform alignment intersects with Kalshi normalization via `ticker`, `event_ticker`, `title`, subtitles, yes/no prices, `taker_side`, `result`.

## 9) Review playbook

### 9.1 Reviewer checklist

1. Verify native IDs, URLs, and timestamps for both legs.
2. Capture authoritative rule text snapshots for both sides.
3. Confirm outcome polarity and boundary conditions match.
4. Validate close/end/resolution windows and source hierarchy.
5. Confirm platform/regulatory mode compatibility.
6. Confirm venue modes do not invalidate eligibility.
7. Confirm executable bid/ask plus depth basis.
8. Record acceptance/rejection with taxonomy code and rationale.

### 9.2 Evidence capture requirements

- durable source URL per claim,
- rule URL and rule snapshot per leg,
- quote timestamps and venue-mode snapshot,
- fee basis with source URL and retrieval time,
- reviewer identity and decision timestamp.

### 9.3 Rejection reason taxonomy (minimum)

- `RULE_TEXT_MISMATCH`
- `RULE_SOURCE_HIERARCHY_MISMATCH`
- `TEMPORAL_WINDOW_MISMATCH`
- `OUTCOME_MODEL_MISMATCH`
- `NEGATIVE_RISK_OR_MULTI_OUTCOME_DEPENDENCY`
- `NON_EXECUTABLE_MARKET_STATE`
- `REGULATORY_OR_GEO_MODE_MISMATCH`
- `MISSING_RULE_EVIDENCE`
- `INSUFFICIENT_FEE_OR_LIQUIDITY_EVIDENCE`
- `US_VS_INTL_POLYMARKET_AMBIGUITY`

### 9.4 Decision record template

- Pair candidate ID:
- Review date/time (UTC):
- Reviewer:
- Venue A summary:
- Venue B summary:
- Equivalence decision: `approved` / `rejected` / `defer`
- Rejection taxonomy code(s) if rejected/deferred:
- Opportunity label considered (if applicable, post-equivalence only):
- Required follow-up actions:
- Rationale (required):
- Rule snapshot links/attachments (required):
- Durable source URLs cited (required):

No auto-approval is allowed in Phase 0B.

## 10) Recommended future tickets

- **Phase 0B-21**: Polymarket token/outcome normalization plan.
- **Phase 0B-22**: Kalshi normalized fills/markets mapping plan.
- **Phase 0B-23**: approved tiny fixture derivation script plan (still no fixture commit unless explicitly approved).
- **Phase 0B-24**: cross-platform candidate-pair schema fixture tests (static/preflight only).
- **Phase 0B-25**: semantic matching rejection-reason taxonomy tests (static/preflight only).
- **Phase 0B-26**: integration/rate-limit/fee source appendix maintenance plan.
- Later-phase legal/compliance review before any connector or execution work.
- Future Phase 6 autonomy controls: kill switches, monitoring, audit logs, explicit approval gates.

## 11) Do-not-implement boundaries

This PR does **not** approve:

- automated order placement,
- order routing,
- cancellation,
- execution,
- auto-equivalence,
- legal conclusions,
- geoblock evasion,
- VPN bypass,
- jurisdiction workarounds,
- treating international Polymarket and Polymarket US as interchangeable,
- using display prices as execution prices,
- live trading,
- autonomous execution.

## 12) Static canonical-ID guard

- This document avoids literal legacy market identifier and uses “source market identifier” / “native market identifier” phrasing where needed.
- Canonical alignment remains centered on `condition_id`, `token_id`, and `outcome`.
- No allowlist expansion should be required when this document is committed.
