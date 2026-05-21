# Phase 0B-26 — Source Appendix Maintenance Plan for Integration, Rate-Limit, Fee, Venue-Mode, and Legal/Regulatory Assumptions (Docs-Only)

## 1) Purpose and posture

This ticket is **documentation-only**.

This document defines a **maintenance plan** for source appendices and external-source assumptions that MEG depends on for future integration-adjacent work.

This document does **not** implement source refresh automation.

This document does **not** approve connectors, integrations, import, fixtures, loaders, query engines, order routing, live trading, or autonomous execution.

This plan exists to prevent stale assumptions from propagating into later implementation phases.

## 2) Source appendix scope

The source appendix maintenance scope includes the following source categories:

- Kalshi API docs
- Kalshi market data docs
- Kalshi auth/API key docs
- Kalshi rate limits and tiers
- Kalshi fee schedule / fee docs
- Kalshi market lifecycle / exchange status / pause docs
- Kalshi member agreement / legal docs
- Polymarket API docs
- Polymarket auth / SDK docs
- Polymarket markets/events docs
- Polymarket price/orderbook docs
- Polymarket fees
- Polymarket rate limits
- Polymarket geographic restrictions
- Polymarket matching engine / restart / venue-mode docs
- Polymarket resolution / UMA-related docs
- Polymarket negative-risk docs
- Polymarket US vs international surface docs
- CFTC/regulatory sources
- Polygon/RPC/supporting chain sources
- Any future venue docs added to MEG

## 3) Source record schema

Planned source appendix record shape (for future tracked records):

- `source_ref`
- `source_title`
- `publisher_or_platform`
- `durable_url`
- `source_category`
- `claim_supported`
- `claim_type`
- `access_date`
- `last_verified_at`
- `verification_method`
- `stability_class`
- `refresh_cadence`
- `owner_or_reviewer`
- `change_sensitivity`
- `stale_if_older_than_days`
- `implementation_blocker_if_stale`
- `execution_blocker_if_stale`
- `notes`

## 4) Claim types

Planned `claim_type` allowlist:

- `api_endpoint`
- `authentication`
- `rate_limit`
- `fee_model`
- `orderbook_semantics`
- `price_semantics`
- `market_lifecycle`
- `venue_mode`
- `resolution_process`
- `geographic_restriction`
- `legal_terms`
- `regulatory_status`
- `chain_infrastructure`
- `data_dictionary`
- `unknown_or_other`

## 5) Stability classes and refresh cadence

Planned `stability_class` values:

- `volatile`
- `moderate`
- `stable`
- `archival`

Suggested refresh cadence guidance:

- `volatile`: refresh before any implementation use and at least weekly during active connector work.
- `moderate`: refresh before phase-gate use and at least monthly during active work.
- `stable`: refresh before major phase gates.
- `archival`: verify once, then re-check only when relied on for new implementation claims.

Examples:

- Fees: typically `volatile` or `moderate`.
- Rate limits: typically `volatile` or `moderate`.
- Geographic restrictions: typically `volatile` or `moderate`.
- API endpoint docs: typically `moderate`.
- Legal/member agreements: typically `moderate` or `stable` depending on source behavior.
- CFTC historical press releases: typically `archival`.
- Current regulatory listings/status pages: typically `moderate`.
- Polygon RPC references: typically `moderate`.

## 6) Change sensitivity

Planned `change_sensitivity` values:

- `low`
- `medium`
- `high`
- `critical`

High/critical sensitivity examples include:

- fee model changes,
- rate limit changes,
- geographic restriction changes,
- legal/ToS changes,
- exchange status / venue mode changes,
- orderbook semantics changes,
- resolution process changes,
- auth/API key changes,
- Polymarket US vs international access changes.

## 7) Refresh triggers

The following triggers require source re-check before downstream use:

- before implementing a connector,
- before implementing source-specific loaders,
- before enabling live API calls,
- before relying on fee calculations,
- before relying on rate-limit assumptions,
- before using source assumptions in opportunity scoring,
- before cross-platform equivalence or opportunity labeling,
- before any order-routing or execution-adjacent work,
- before any Phase 6 autonomy work,
- when official docs update,
- when API behavior differs from docs,
- when CI/test failures suggest stale assumptions,
- when platform news/legal/regulatory posture changes,
- when a source URL breaks or redirects unexpectedly.

## 8) Staleness and blocker rules

Rules:

- Stale fee/rate-limit/legal/geographic-restriction/venue-mode sources should block implementation work that depends on those assumptions.
- Stale execution-adjacent sources should block any execution design work.
- Stale or missing source metadata should block live trading and autonomous execution.
- Broken URLs should set source status to `needs_review` until re-verified.
- Secondary sources cannot override official/primary sources.
- Source appendix entries are not legal approval.
- Historical/archival regulatory sources do not prove current authorization unless paired with current listing/status sources.

## 9) Source review workflow

Planned maintenance workflow:

1. Identify the source claim being relied on.
2. Classify source category and `claim_type`.
3. Assign `stability_class` and `refresh_cadence`.
4. Record durable URL and access date.
5. Capture claim supported text.
6. Mark implementation/execution blocker flags.
7. Reviewer verifies current source against the claim.
8. Reviewer records `last_verified_at` and notes.
9. If assumptions changed, update downstream docs/tests/plans accordingly.

## 10) Maintenance table seed (from 0B-20C source appendix)

This seed table uses durable source titles and broad categories for planning, not full content restatement.

| Source title | Platform/publisher | Source category | claim_type | stability_class | refresh_cadence | implementation_blocker_if_stale | execution_blocker_if_stale | Notes |
|---|---|---|---|---|---|---|---|---|
| Welcome to Kalshi API Documentation | Kalshi | API docs | api_endpoint | moderate | pre-phase-gate + monthly during active work | true | true | Baseline API surface reference. |
| Kalshi Quick Start: Market Data | Kalshi | Market data docs | data_dictionary | moderate | pre-phase-gate + monthly during active work | true | true | Market data access assumptions. |
| Kalshi API Keys | Kalshi | Auth/API key docs | authentication | moderate | pre-phase-gate + monthly during active work | true | true | Key/auth workflow can change. |
| Kalshi Rate Limits and Tiers | Kalshi | Rate limit docs | rate_limit | volatile | pre-implementation + weekly during connector work | true | true | High-sensitivity throttling assumptions. |
| Kalshi Glossary | Kalshi | Terminology docs | data_dictionary | stable | pre-major-phase-gate | false | false | Vocabulary aid; still verify when used for parser assumptions. |
| Kalshi Market Lifecycle | Kalshi | Lifecycle docs | market_lifecycle | moderate | pre-phase-gate + monthly during active work | true | true | State semantics can affect market gating. |
| Kalshi Orderbook Responses | Kalshi | Orderbook docs | orderbook_semantics | moderate | pre-phase-gate + monthly during active work | true | true | Execution-price interpretation dependency. |
| Kalshi Maintenance and Pauses | Kalshi | Venue-mode docs | venue_mode | volatile | pre-implementation + weekly during connector work | true | true | Maintenance/pause behavior is execution-adjacent. |
| Kalshi Get Exchange Status | Kalshi | Exchange status docs | venue_mode | volatile | pre-implementation + weekly during connector work | true | true | Operational status assumptions. |
| Kalshi Fees / Fee Schedule | Kalshi | Fee docs | fee_model | volatile | pre-implementation + weekly during connector work | true | true | Fee model affects edge and execution checks. |
| Kalshi Member Agreement | Kalshi | Legal docs | legal_terms | moderate | pre-phase-gate + monthly during active work | true | true | Contract/legal boundaries for use assumptions. |
| Polymarket API Introduction | Polymarket | API docs | api_endpoint | moderate | pre-phase-gate + monthly during active work | true | true | API surface planning anchor. |
| Polymarket Authentication | Polymarket | Auth docs | authentication | moderate | pre-phase-gate + monthly during active work | true | true | Auth requirements and signatures may evolve. |
| Polymarket Clients/SDKs | Polymarket | SDK docs | data_dictionary | moderate | pre-phase-gate + monthly during active work | false | false | Supporting reference for integration tooling context. |
| Polymarket Markets & Events | Polymarket | Markets/events docs | data_dictionary | moderate | pre-phase-gate + monthly during active work | true | true | Hierarchy and shape assumptions. |
| Polymarket Prices & Orderbook | Polymarket | Price/orderbook docs | price_semantics | moderate | pre-phase-gate + monthly during active work | true | true | Display vs executable pricing constraints. |
| Polymarket Resolution | Polymarket | Resolution docs | resolution_process | moderate | pre-phase-gate + monthly during active work | true | true | Rules/resolution evidence requirement. |
| Polymarket Fees | Polymarket | Fee docs | fee_model | volatile | pre-implementation + weekly during connector work | true | true | Net-edge and viability impacts. |
| Polymarket Rate Limits | Polymarket | Rate limit docs | rate_limit | volatile | pre-implementation + weekly during connector work | true | true | Sampling/freshness constraints. |
| Polymarket Geographic Restrictions | Polymarket | Geographic restriction docs | geographic_restriction | volatile | pre-implementation + weekly during connector work | true | true | Legal availability assumptions are high-sensitivity. |
| Polymarket Matching Engine Restarts | Polymarket | Venue-mode docs | venue_mode | volatile | pre-implementation + weekly during connector work | true | true | Restart mode may block execution assumptions. |
| Polymarket Create Order | Polymarket | Trading API docs | orderbook_semantics | moderate | pre-phase-gate + monthly during active work | true | true | Order semantics evidence source. |
| Polymarket Negative-Risk Markets | Polymarket | Advanced market docs | market_lifecycle | moderate | pre-phase-gate + monthly during active work | true | true | Special structure can alter comparability assumptions. |
| Polymarket USA surface | Polymarket | US vs international surface docs | geographic_restriction | volatile | pre-implementation + weekly during connector work | true | true | US/international surface distinction must stay current. |
| CFTC Kalshi DCM designation press release | U.S. CFTC | Regulatory source | regulatory_status | archival | verify once + re-check when relied on for new claims | false | false | Historical context only; not current authorization alone. |
| CFTC current DCM listings | U.S. CFTC | Regulatory source | regulatory_status | moderate | pre-phase-gate + monthly during active work | true | true | Current regulatory status reference. |
| CFTC Kalshi current listing page | U.S. CFTC | Regulatory source | regulatory_status | moderate | pre-phase-gate + monthly during active work | true | true | Current listing detail source. |
| CFTC Polymarket enforcement action | U.S. CFTC | Regulatory source | regulatory_status | archival | verify once + re-check when relied on for new claims | false | false | Historical enforcement context. |
| Polygon PoS documentation | Polygon | Chain infrastructure docs | chain_infrastructure | moderate | pre-phase-gate + monthly during active work | true | true | Chain context dependencies for settlement metadata assumptions. |
| Polygon RPC documentation | Polygon | RPC docs | chain_infrastructure | moderate | pre-phase-gate + monthly during active work | true | true | RPC assumptions may affect availability/latency planning. |

## 11) Integration implications

- Later connector plans must reference current source records for integration assumptions.
- Later fee/rate-limit code paths must record `source_ref` and `last_verified_at` for relied-upon assumptions.
- Later opportunity scoring must not rely on stale fee/liquidity/venue-mode assumptions.
- Later cross-platform matching must capture `source_ref` entries for rule/resolution evidence.
- Later Phase 6 autonomy work must require fresh source verification for fees, rate limits, venue modes, legal/geographic restrictions, order semantics, and execution constraints.
- Any uncertainty should fail closed.

Future refreshes of fees, rate limits, API limits, legal/ToS, and venue-mode assumptions must use current official/primary sources at the time of implementation and review.

## 12) Relation to Phase 0B tests/docs

This plan supports and extends:

- 0B-20C source appendix and cross-platform semantic matching plan,
- 0B-21 Polymarket normalization plan,
- 0B-22 Kalshi normalization plan,
- 0B-23 fixture derivation plan,
- 0B-24 candidate-pair schema tests,
- 0B-25 rejection taxonomy tests.

Specifically, 0B-26 adds a repeatable maintenance posture so assumptions used by those docs/tests can be re-verified before later implementation phases.

## 13) Future test candidates (not added in this ticket)

Potential static/preflight tests for future tickets:

- source appendix record shape tests,
- `claim_type` allowlist tests,
- `stability_class` allowlist tests,
- `refresh_cadence` presence tests,
- `stale_if_older_than_days` presence tests,
- implementation/execution blocker flag tests,
- no-execution-if-source-stale tests,
- no fee/rate-limit assumption without `source_ref` tests,
- no cross-platform opportunity without rule/resolution source refs tests,
- broken URL status taxonomy tests.

This ticket does not add these tests.

## 14) Phase 0B closure note

- After this ticket, Phase 0B has completed the planned research/preflight foundation.
- Phase 1 may begin only after this PR is merged and CI is green.
- Phase 1 should remain conservative and must not skip explicit approval gates for fixture generation/import/loader work.

## 15) Explicit non-approvals

This plan explicitly does **not** approve:

- source refresh automation,
- connector implementation,
- API calls,
- data import,
- fixture derivation,
- fixture commit,
- loader implementation,
- query engine implementation,
- order placement,
- live trading,
- autonomous execution,
- legal conclusions or legal approval.

## 16) Static canonical-ID guard

Canonical-ID guard for this plan:

- avoid literal legacy routing identifier token in this document,
- use `source_market_ref`, `ticker_ref`, native market reference, source market identifier, or legacy market identifier prose instead,
- if literal legacy routing identifier token becomes unavoidable in a future edit, update `tests/core/canonical_id_allowlist.py` exactly and narrowly,
- do not increase legacy identifier count casually.
