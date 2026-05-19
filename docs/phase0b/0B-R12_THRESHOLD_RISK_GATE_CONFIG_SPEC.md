# Phase 0B-R12 — Threshold and Risk-Gate Configuration Spec (Docs-Only)

## 1) Purpose

This document defines a **documentation-only threshold and risk-gate configuration specification** for Phase 0B opportunity proposal screening.

This ticket is planning-only and exists to define candidate screening semantics before any detector/runtime implementation work.

This document does **not**:

- implement configuration loading,
- implement detector behavior,
- implement risk engine behavior,
- change runtime behavior,
- approve live trading,
- approve autonomous trading in Phase 0B.

## 2) Relationship to prior docs

- **R10** defines cross-platform opportunity candidate input/output contract fields.
- **R11** statically enforces the R10 detector contract language.
- **R12 (this doc)** defines configuration semantics for screening or rejecting candidates.
- R12 does not set production runtime defaults and does not implement runtime behavior.

## 3) Configuration groups (planning-only)

Planning-only groups for future config schema and validation:

1. edge thresholds
2. spread thresholds
3. confidence thresholds
4. semantic match thresholds
5. liquidity thresholds
6. data quality thresholds
7. exposure caps
8. loss caps
9. market allowlists/blocklists
10. mode controls
11. audit/logging controls
12. kill-switch controls (future phases only)

## 4) Required config fields

Future config contracts should include these required fields:

- `config_id`
- `config_version`
- `mode`: `planning` / `fixture` / `paper` / `read_only_live_blocked` / `live_blocked`
- `source_id`
- `provenance`
- `created_at`
- `updated_at`
- `min_edge_bps`
- `min_fee_adjusted_edge_bps`
- `min_spread_bps`
- `min_confidence_score`
- `min_semantic_match_score`
- `min_liquidity_score`
- `min_data_quality_score`
- `max_per_market_exposure`
- `max_global_exposure`
- `max_daily_loss`
- `market_allowlist`
- `market_blocklist`
- `platform_allowlist`
- `platform_blocklist`
- `dry_run_default`
- `require_operator_approval`
- `live_trading_enabled`
- `autonomous_trading_enabled`
- `kill_switch_enabled`
- `audit_log_required`
- `rejection_reason_required`

## 5) Required default posture for Phase 0B

In Phase 0B, the required default posture is:

- `dry_run_default` must be `true`.
- `require_operator_approval` must be `true`.
- `live_trading_enabled` must be `false`.
- `autonomous_trading_enabled` must be `false`.
- missing config must fail closed.
- invalid config must fail closed.
- unknown mode must fail closed.

## 6) Candidate screening and rejection behavior

A candidate should be rejected (fail closed) if any of the following applies:

- edge below `min_edge_bps`,
- fee-adjusted edge below `min_fee_adjusted_edge_bps`,
- spread below `min_spread_bps`,
- confidence below `min_confidence_score`,
- semantic match below `min_semantic_match_score`,
- liquidity below `min_liquidity_score`,
- data quality below `min_data_quality_score`,
- market or platform not in allowlist,
- market or platform present in blocklist,
- per-market or global exposure cap exceeded,
- daily loss cap exceeded,
- missing fee assumptions,
- missing liquidity assumptions,
- missing `provenance` or missing `source_id`,
- missing operator approval requirement,
- `live_trading_enabled` or `autonomous_trading_enabled` set true in Phase 0B.

## 7) Output/rejection contract (planning)

Future screening outputs should include:

- `candidate_id` or `opportunity_id`
- `config_id`
- `accepted` (`true`/`false`)
- `rejection_reasons`
- `fail_closed_reason`
- `thresholds_evaluated`
- `observed_values`
- `decision_timestamp`
- `audit_log_reference` (if available)
- `proposal_allowed` (`true`/`false`)
- `execution_allowed` (must be `false` in Phase 0B)

## 8) Fail-closed behavior

Configuration interpretation must fail closed for at least:

- missing config,
- invalid type/range,
- unknown `config_version`,
- unknown mode,
- missing required threshold,
- negative exposure cap,
- `live_trading_enabled: true` in Phase 0B,
- `autonomous_trading_enabled: true` in Phase 0B,
- `dry_run_default: false` in Phase 0B,
- `require_operator_approval: false` in Phase 0B,
- missing audit/rejection reason policy.

## 9) Future Phase 6/v3 autonomy compatibility (not approved here)

Phase 0B config fields should remain compatible with future autonomy-mode extensions.

Future modes may include:

- `paper_autonomous`
- `limited_autonomous`
- `full_autonomous`

Any future autonomous mode requires a **separate explicit approval** in a dedicated **Phase 6/v3** milestone. That future milestone must include separate risk, approval, ToS/jurisdiction, monitoring, kill-switch, and execution-gate reviews.

Future autonomy gate requirements must include at minimum:

- paper trading validation,
- position limits,
- daily loss limits,
- market allowlist,
- confidence/edge thresholds,
- kill switch,
- audit logging,
- drift monitoring,
- manual override,
- explicit config flag default off,
- ToS/jurisdiction approval,
- dependency/security review.

None of the future autonomy modes are approved by this ticket. In Phase 0B, config semantics remain proposal-screening/planning only.

## 10) Testing strategy for future tickets

Future tickets should enforce:

- static config contract tests first,
- tiny deterministic config fixtures,
- invalid config fail-closed tests,
- no network in unit tests,
- no secrets in CI,
- no live connector requirement,
- no order authority tests,
- proposal-only boundary tests,
- future runtime tests must prove live/autonomous flags cannot enable execution in Phase 0B.

## 11) Non-goals

This ticket explicitly prohibits and does not approve:

- implementation,
- config loader changes,
- risk engine changes,
- detector implementation changes,
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

## 12) Recommended next ticket

**Recommended next ticket: Phase 0B-R13 — Static threshold/risk-gate config preflight tests.**

Rationale:

- it immediately converts this docs-only contract into deterministic static enforcement,
- it preserves fail-closed posture before implementation,
- it keeps the proposal-only Phase 0B boundary explicit and testable.
