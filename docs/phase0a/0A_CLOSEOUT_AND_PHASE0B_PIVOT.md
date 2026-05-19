# 0A Closeout and Phase 0B Pivot

## Purpose

This note closes the active Phase 0A shared-rail migration scope and establishes a controlled pivot toward Phase 0B historical-research planning.

Phase 0A has now completed the intended shared-event correctness rail milestones and should not absorb additional runtime approval/execution path migrations without separate design control.

## Phase 0A Completed Items

The following items are considered complete for Phase 0A closeout:

1. Shared event contracts are defined and enforced across the primary Redis/event boundaries.
2. Canonical identifier compatibility is enforced around `condition_id`, `token_id`, and `outcome`.
3. JSON/Redis envelope contracts are validated for the shared rail.
4. Raw whale rail validation is implemented at publisher/consumer boundaries.
5. Qualified whale rail validation is implemented at publisher boundaries.
6. Signal-engine runner skeleton is present and wired into startup.
7. Dashboard `SignalEvent` feed boundary is validated as read-only consumer exposure.
8. `TradeProposal` envelope contract is covered by explicit contract tests.
9. CI/dev dependency guardrail fixes required for contract checks are in place.

## Current Runtime Rail Summary (Phase 0A Boundary)

The runtime-facing shared rail currently validated by contract/boundary work is:

- `raw_whale_trades`
- `qualified_whale_trades`
- `signal_events`
- `trade_proposals` (envelope boundary only)

This is the intended stop point for Phase 0A runtime migrations.

## Explicit Stop Line

**Do not migrate approval, execution, or order-router runtime paths as part of Phase 0A closeout work without a separate design ticket and review.**

Any proposed changes touching Telegram approval semantics, execution request routing, order submission behavior, fill reconciliation behavior, or order-router authority boundaries are out of scope for this closeout note.

## Remaining Deferred Items (Not in Phase 0A Closeout)

The following items remain deferred and should be handled through subsequent scoped tickets/phases:

1. Approval/order-router migration hardening.
2. Live autonomous execution capabilities.
3. DuckDB historical lake implementation.
4. Weather paper engine implementation.
5. Whale lead-lag research implementation.
6. Polymarket bot repository feature-mining backlog intake.
7. Swing bot / volatility sidecar exploration.

## Phase 0B Recommendation

Begin Phase 0B by planning the DuckDB historical data lake as a research-only plane, explicitly separated from live execution semantics.

Recommended planning components:

1. Identify and catalog historical Polymarket and Kalshi data sources.
2. Define normalized DuckDB-facing schemas and a formal data dictionary.
3. Plan lead-lag and forward-return query-layer primitives for repeatable research.
4. Keep all Phase 0B deliverables logically and operationally separated from live execution and approval routing.

## Recommended Next Ticket

**Phase 0B-01: DuckDB Historical Lake Plan**

Minimum ticket objectives:

- source inventory (Polymarket/Kalshi/historical captures),
- bronze/silver/gold schema draft,
- canonical ID mapping rules,
- query blueprint for lead-lag and forward-return analysis,
- boundary statement confirming no live execution coupling.

## Kill Criteria (Runtime Safety Guard)

If future runtime work attempts to change approval or execution semantics during Phase 0A/0B planning tracks, **stop immediately** and require a dedicated approval/execution design review ticket before proceeding.
