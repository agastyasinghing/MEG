# Phase 0B-R10 — Cross-Platform Opportunity Detector Contract (Docs-Only)

## 1) Purpose

This document defines a **documentation-only detector contract** for cross-platform opportunity candidate analysis in Phase 0B.

This contract exists to:

- define what a cross-platform opportunity candidate means,
- define detector input/output shapes using normalized connector and test-double outputs,
- preserve canonical identifier usage (`condition_id`, `token_id`, `outcome`) where available,
- keep all outputs in analysis/proposal-candidate scope only.

This document does **not**:

- implement detector code,
- approve runtime detector integration,
- approve live API calls,
- approve connector API calls,
- approve order placement,
- approve autonomous trading in Phase 0B.

## 2) Relationship to R7 / R8 / R9

- **R7** defines connector/interface output boundaries and safety mode framing.
- **R8** defines fixture/test-double shapes and deterministic offline safety constraints.
- **R9** statically enforces connector-contract documentation terms and canonical identifier language.
- **R10 (this doc)** defines the cross-platform opportunity detector input/output contract using those R7/R8 normalized shapes under R9-style fail-closed expectations.

## 3) Input contract

Detector input records are normalized records produced by connector/test-double boundaries and passed to analysis logic as data-only payloads.

### 3.1 Required input record families

1. **Market metadata records**
2. **Price/orderbook snapshot records**
3. **Optional trade/fill history records**
4. **Optional resolution/outcome metadata records**

### 3.2 Required shared fields (all required unless explicitly unavailable in source)

- `platform` (platform identifier)
- `source_id`
- `provenance`
- `observed_at` and/or `fetched_at`
- `schema_version`
- `condition_id` (where available)
- `token_id` (where available)
- `outcome` (where available)

If a source exposes historical compatibility fields, use **legacy market identifier** wording only for reference context. Canonical alignment/routing remains centered on `condition_id`, `token_id`, and `outcome`.

## 4) Normalized market pair candidate contract

A normalized market pair candidate represents a candidate semantic/canonical pairing between two platform markets/outcomes for opportunity screening.

### 4.1 Required fields

- `pair_id`
- `platforms_compared` (exactly two platform identifiers)
- `source_ids` (source IDs used for each leg)
- `market_titles`
- `market_questions`
- `market_slugs`
- `category`
- `semantic_match_score`
- `canonical_match_evidence` (where available)
- `condition_id_alignment` (where available)
- `token_id_alignment` (where available)
- `outcome_alignment` (where available)
- `mismatch_flags`
- `provenance`
- `observed_at`
- `rejection_reasons` (if not eligible)

### 4.2 Pair-candidate interpretation boundary

A pair candidate is an analysis artifact only. It is not approval, not execution, and not an order instruction.

## 5) Opportunity candidate output contract

An opportunity candidate is a structured proposal candidate derived from one eligible pair candidate and its normalized pricing/liquidity context.

### 5.1 Required output fields

- `opportunity_id`
- `pair_id`
- `opportunity_type`
  - `cross_platform_price_gap`
  - `bundle_mispricing`
  - `stale_price_divergence`
  - `liquidity_gap`
  - `research_only_anomaly`
- `legs` (list)
  - `platform` per leg
  - `outcome` per leg
  - `side` per leg
  - `price` and/or `odds` per leg
- `estimated_edge_bps`
- `fee_adjusted_edge_bps`
- `confidence_score`
- `liquidity_score`
- `data_quality_score`
- `source_ids`
- `provenance`
- `observed_at`
- `detector_schema_version`
- `fail_closed_reason` (required when invalid)
- `rejection_reasons` (required when rejected)

## 6) Opportunity type definitions (candidate-only)

All types below are **candidate detections only** and never trade instructions:

1. `cross_platform_price_gap`
   - Detects materially divergent normalized prices/odds for semantically/canonically aligned outcomes across platforms.
2. `bundle_mispricing`
   - Detects potential invariant violations in outcome bundles (for example, complement consistency framing) under normalized assumptions.
3. `stale_price_divergence`
   - Detects divergence where one side appears stale relative to newer observations on another platform/source.
4. `liquidity_gap`
   - Detects asymmetry where an apparent edge is constrained by depth/liquidity mismatch.
5. `research_only_anomaly`
   - Flags unusual patterns requiring manual investigation without immediate edge/execution interpretation.

## 7) Required validation and fail-closed behavior

Detector contract consumers must fail closed when any of the following applies:

- missing required platform/source/provenance fields,
- missing required price/odds fields,
- unsupported `schema_version`,
- unsupported `opportunity_type`,
- invalid timestamp format/value,
- low `semantic_match_score` per future config threshold,
- conflicting outcome mapping,
- missing fee assumptions,
- missing liquidity assumptions,
- ToS/jurisdiction not approved for live use,
- connector mode is `live_blocked`,
- any requested order authority,
- any attempt to bypass proposal/approval boundary.

Fail-closed outputs must include machine-readable `fail_closed_reason` and/or `rejection_reasons`.

## 8) Scoring fields and thresholds (planning-only)

This ticket defines planning-only scoring fields:

- `semantic_match_score`
- `edge_score`
- `fee_adjusted_edge_bps`
- `liquidity_score`
- `data_quality_score`
- `confidence_score`
- `rejection_thresholds`
- `threshold_config_source`

Exact threshold values are **not** set in this ticket and are future configuration-spec work.

## 9) Output authority boundary

In Phase 0B:

- detector output is **not** a trade,
- detector output is **not** approval,
- detector output is **not** an order,
- detector output cannot call connector APIs,
- detector output cannot place orders,
- detector output cannot bypass Telegram/operator approval.

Future autonomous operation belongs only to a separate explicit **Phase 6/v3** milestone with separate risk, approval, ToS/jurisdiction, monitoring, kill-switch, and execution-gate reviews.

## 10) Future autonomy compatibility note

Phase 0B detector outputs should be designed so they can later support:

- manual review,
- paper-autonomous mode,
- limited-autonomous mode,
- full-autonomous mode.

However, only manual/proposal planning is approved in Phase 0B.

Any future autonomous mode requires separate milestone gates, including at minimum:

- paper trading validation,
- max position limits,
- max daily loss,
- market allowlist,
- confidence/edge thresholds,
- kill switch,
- audit logging,
- drift monitoring,
- manual override,
- explicit config flag default off,
- ToS/jurisdiction approval,
- dependency/security review.

## 11) Testing strategy for future tickets

Future follow-on tickets should enforce:

- static contract tests first,
- tiny deterministic fixtures,
- R8 test doubles,
- no network in unit tests,
- no secrets in CI,
- invalid/missing data fail-closed tests,
- no order authority tests,
- proposal-only boundary tests.

## 12) Non-goals

This ticket explicitly prohibits and does not approve:

- implementation,
- runtime/trading changes,
- live API calls,
- connector calls,
- order placement,
- execution/approval changes,
- dependency changes,
- dataset import,
- loader expansion,
- real fixture data commits in this ticket,
- legal conclusion,
- live API/trading approval,
- Phase 0B autonomous trading approval.

## 13) Recommended next ticket

**Recommended next ticket: Phase 0B-R11 — Static opportunity detector contract preflight tests.**

Rationale:

- it continues docs-contract enforcement with deterministic static checks,
- it validates fail-closed and boundary language before any implementation,
- it preserves proposal-only behavior and no-order-authority guarantees in Phase 0B.
