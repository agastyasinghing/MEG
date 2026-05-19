# Phase 0B-R7 — Connector/Interface Boundary Spec (Planning-Only)

## 1) Purpose

This document is a **docs-only connector/interface boundary specification** for Phase 0B planning.

It exists to prepare future adapter design for Polymarket, Kalshi, and approved reference-data pathways while keeping current scope strictly non-implementation.

This document does **not**:

- implement connector code,
- authorize live API calls,
- authorize trading or execution,
- change order-routing or operator-approval behavior.

## 2) Scope boundary

This artifact is limited to planning boundaries and contract language.

Explicit constraints:

- Connector specs here are planning artifacts only.
- All adapters remain read-only until separately approved in future tickets/PRs.
- No external API usage is approved by this document.
- No secrets or config files are added by this document.
- No dependencies are added by this document.
- No order routing or order placement is allowed by this document.

## 3) Connector categories (future boundary definitions)

1. **Market metadata connector**
   - Purpose: normalize static/semi-static market descriptors.
   - Boundary: metadata ingestion only; no execution authority.
2. **Price/orderbook snapshot connector**
   - Purpose: normalize top-of-book and related liquidity snapshots.
   - Boundary: read path only; no write/order capabilities.
3. **Trade/fill history connector**
   - Purpose: normalize historical/public trade/fill events.
   - Boundary: event retrieval/normalization only.
4. **Account/wallet read-only state connector**
   - Purpose: surface balances/positions/exposure summaries.
   - Boundary: read-only account state; no order authority.
5. **Resolution/outcome metadata connector**
   - Purpose: capture outcome labels, resolution status, and close metadata.
   - Boundary: metadata/status only.
6. **Proposal emission interface**
   - Purpose: pass normalized observations into analysis/proposal layers.
   - Boundary: proposal payload generation only; not approval/execution.
7. **Paper/simulated connector**
   - Purpose: deterministic offline/paper-mode contract exercise.
   - Boundary: no live network requirement; no live execution.
8. **Live connector placeholder (blocked by default)**
   - Purpose: reserve naming and contract slot for future work.
   - Boundary: mode exists as blocked placeholder; cannot execute.

## 4) Common connector contract fields

Future connector contracts should include:

- `connector_name`
- `platform`
- `mode`: `fixture` / `local_archive` / `paper` / `read_only_live` / `live_blocked`
- `source_id`
- `provenance`
- `fetched_at` and/or `observed_at`
- `schema_version`
- `supported_operations`
- `blocked_operations`
- `error_policy`
- `rate_limit_policy`
- `secrets_required`
- `dependency_status`
- `ToS_jurisdiction_status`
- `approval_status`

Baseline policy intent for these fields:

- `blocked_operations` must always include order placement/cancel/modify for non-approved modes.
- `approval_status` must remain non-executable unless explicit operator-approved execution milestones are completed.
- `ToS_jurisdiction_status` and `dependency_status` must pass review before any implementation-adjacent live mode can be considered.

## 5) Market metadata output shape

Minimum planning shape (fields present when available from source):

- `platform`
- `source_id`
- `condition_id` (if available)
- `token_id` (if available)
- `outcome` and/or `outcomes`
- `market_slug`
- `title`
- `question`
- `category`
- `status`
- `start_at` / `end_at` / `resolution_at` (if available)
- provenance fields (`provenance`, `schema_version`, `fetched_at` or `observed_at`)

## 6) Price/orderbook snapshot output shape

Minimum planning shape (fields present when available from source):

- `platform`
- `source_id`
- `condition_id` (if available)
- `token_id` (if available)
- `outcome`
- `bid_price` / `ask_price` / `mid_price` / `last_price` (as available)
- liquidity/volume fields (for example `bid_size`, `ask_size`, `liquidity`, `volume_24h`) as available
- `observed_at`
- `snapshot_id`
- provenance fields (`provenance`, `schema_version`, optional `fetched_at`)

## 7) Trade/fill history output shape

Minimum planning shape (fields present when available from source):

- `platform`
- `source_id`
- `condition_id` (if available)
- `token_id` or source asset identifier (if available)
- `outcome` (if available)
- wallet/counterparty fields such as `wallet_address`, `maker`, `taker` (if available)
- `side` and/or `taker_side`
- `price`
- `size`, `count`, and/or `amount`
- `timestamp`, `block_timestamp`, and/or `created_time`
- transaction/order identifiers if available (`tx_id`, `order_id`, `trade_id`)
- provenance fields (`provenance`, `schema_version`, `observed_at`)

If historical sources expose legacy market identifier fields, treat them as compatibility/reference context only; canonical routing and normalization must prefer `condition_id`, `token_id`, and `outcome`.

## 8) Account/wallet read-only state output shape

Minimum planning shape (fields present when available from source):

- `platform`
- `account_id` and/or `wallet_address` (if available)
- balances/positions collections (if available)
- open exposure summary (if available)
- `observed_at`
- explicit read-only constraint marker
- explicit no-order-authority marker

Policy boundary:

- account connectors in this phase are state-observation interfaces only,
- no order authority, signing authority, or execution authority is granted.

## 9) Proposal emission interface boundary

Connector outputs may later feed analysis/proposal generation contracts, but:

- proposal emission does **not** equal approval,
- operator approval remains mandatory,
- no connector can place orders,
- no connector can bypass Telegram/operator approval,
- execution and order-router behavior remain out of scope for this document.

## 10) Failure and safety behavior

Future implementations derived from this spec should fail closed by default:

- fail closed on missing required fields,
- fail closed on unknown `schema_version`,
- fail closed on unsupported connector `mode`,
- fail closed on missing ToS/jurisdiction approval,
- fail closed on missing dependency/security review,
- no silent fallback into live behavior,
- no secret leakage in logs, docs, or tests.

## 11) Testing strategy for future tickets

Before any live connector work:

- require test doubles before live connectors,
- require tiny fixtures before real APIs,
- require local archive fixtures before `read_only_live`,
- add static checks that live endpoints are absent from tests unless explicitly allowed,
- add approval-boundary tests before execution-adjacent implementation,
- keep unit tests free of external network requirements.

## 12) Dependency and secrets policy

- No new dependencies without explicit review.
- No secrets committed to repository history.
- Environment variable names may be documented only as placeholders.
- Live credentials are not required for Phase 0B.
- Dependency/license/security review is required before any implementation phase.

## 13) Non-goals

This ticket explicitly excludes:

- implementation,
- connector code,
- runtime/trading changes,
- live API calls,
- order placement,
- execution/approval-path changes,
- dependency changes,
- dataset import,
- loader expansion,
- legal conclusion.

## 14) Recommended next ticket

**Recommended next ticket: Phase 0B-R8 — Connector fixture/test-double contract.**

Rationale:

- directly operationalizes this boundary spec into enforceable test-facing interfaces,
- preserves docs-and-fixtures-first progression,
- keeps live connector implementation blocked until separate review/approval tracks are completed.
