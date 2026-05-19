# Phase 0B-R8 — Connector Fixture/Test-Double Contract (Docs-Only)

## 1) Purpose

This document defines a **fixture/test-double contract** for future connector testing in Phase 0B.

This ticket is strictly **documentation-only** and does not:

- implement connector code,
- authorize connector implementation,
- authorize live API calls,
- authorize real connector runtime usage,
- authorize trading/execution,
- authorize order placement or approval-path changes.

## 2) Relationship to R7

Phase 0B-R7 defined planning-only connector/interface boundaries.

Phase 0B-R8 defines deterministic, test-facing fixture/test-double contracts for those R7 boundaries.

R8 keeps connector modes offline in this phase and does not approve any live path. Any live or read-only-live mode remains blocked until separate review and approval tickets explicitly allow it.

## 3) Test-double categories

Future tests should use explicit categories:

1. **Market metadata fixture connector**
2. **Price/orderbook snapshot fixture connector**
3. **Trade/fill history fixture connector**
4. **Account/wallet read-only state fixture connector**
5. **Resolution/outcome fixture connector**
6. **Proposal-emission fixture boundary**
7. **Error/fail-closed fixture connector**
8. **Blocked live connector sentinel**

## 4) Common test-double contract fields

Each future fixture/test-double definition should include the following required fields:

- `test_double_name`
- `connector_category`
- `platform`
- `mode` (for R8 fixture doubles: `fixture` only)
- `source_id`
- `fixture_id`
- `fixture_version`
- `schema_version`
- `deterministic_seed` (when deterministic generation requires a seed)
- `supported_operations`
- `blocked_operations`
- `expected_failures`
- `provenance`
- `approval_status`
- `live_network_allowed` (must be `false`)
- `order_authority` (must be `false`)

Contract intent:

- `supported_operations` is limited to deterministic local fixture reads/transforms.
- `blocked_operations` must include network access and any order/execution operation.
- `approval_status` remains non-executable/planning-only in this phase.

## 5) Fixture record expectations

Future connector fixtures should follow these constraints:

- tiny deterministic records only,
- explicit row counts per fixture,
- explicit checksum placeholders,
- explicit provenance and source references,
- explicit regeneration instructions,
- no secrets,
- no live credentials,
- no large datasets,
- no external repository files copied into MEG.

## 6) Output-shape fixtures (minimal required shapes)

Fixture output shapes should align with R7 planning shapes and include canonical identifiers where available (`condition_id`, `token_id`, `outcome`).

### 6.1 Market metadata fixture shape

Minimum fields (when available):

- `platform`
- `source_id`
- `condition_id`
- `token_id`
- `outcome` and/or `outcomes`
- `title`
- `status`
- `provenance`
- `schema_version`
- `observed_at` and/or `fetched_at`

### 6.2 Price/orderbook snapshot fixture shape

Minimum fields (when available):

- `platform`
- `source_id`
- `condition_id`
- `token_id`
- `outcome`
- `bid_price`
- `ask_price`
- `mid_price` and/or `last_price`
- `observed_at`
- `snapshot_id`
- `provenance`
- `schema_version`

### 6.3 Trade/fill history fixture shape

Minimum fields (when available):

- `platform`
- `source_id`
- `condition_id`
- `token_id`
- `outcome`
- `side` and/or `taker_side`
- `price`
- `size` and/or `amount`
- `timestamp`
- `trade_id` and/or `tx_id`
- `provenance`
- `schema_version`

If historical compatibility fields are needed, use "legacy market identifier" wording and keep canonical routing centered on `condition_id`, `token_id`, and `outcome`.

### 6.4 Account/wallet read-only state fixture shape

Minimum fields (when available):

- `platform`
- `source_id`
- `account_id` and/or `wallet_address`
- `balances`
- `positions`
- `exposure_summary`
- `observed_at`
- `provenance`
- `schema_version`
- explicit read-only marker
- explicit no-order-authority marker

### 6.5 Resolution/outcome metadata fixture shape

Minimum fields (when available):

- `platform`
- `source_id`
- `condition_id`
- `token_id`
- `outcome` and/or `outcomes`
- `resolution_status`
- `resolution_at`
- `provenance`
- `schema_version`

## 7) Fail-closed test cases (future)

Future static/preflight and behavior tests should fail closed for at least:

- missing `condition_id` / `token_id` / `outcome` when required,
- unsupported `schema_version`,
- unsupported connector `mode`,
- `live_network_allowed: true`,
- `order_authority: true`,
- missing `provenance`,
- missing `source_id`,
- missing `fixture_id`,
- invalid timestamp format/value,
- attempted proposal-to-approval bypass,
- attempted order placement operation.

## 8) Blocked live connector sentinel

Define a future sentinel double category for explicit live-path blocking:

- `mode: live_blocked`,
- any network call raises explicit blocked error,
- any order operation raises explicit blocked error,
- missing ToS/jurisdiction approval fails closed,
- sentinel cannot be enabled by default config.

This sentinel is a safety contract, not a live connector implementation.

## 9) Testing strategy sequence

Recommended sequence for future tickets:

1. docs/static contract tests,
2. tiny deterministic fixture tests,
3. test-double behavior tests,
4. local archive fixture tests,
5. only later, `read_only_live` tests after separate review/approval.

Additional testing constraints:

- unit tests must not require network,
- CI must not require secrets,
- any future live tests must be explicit opt-in only.

## 10) Safety boundaries and non-goals

This ticket explicitly prohibits and does not approve:

- connector implementation,
- runtime/trading changes,
- live API calls,
- order placement,
- execution/approval-path changes,
- dependency changes,
- dataset import,
- loader expansion,
- real fixture data commits in this ticket,
- legal conclusions,
- live API/trading approval.

## 11) Recommended next ticket

**Recommended next ticket: Phase 0B-R9 — Static connector contract preflight tests.**

Rationale:

- directly validates this R8 contract with deterministic fail-closed checks,
- keeps progression docs-first and test-first,
- preserves live connector blocking while enforcement coverage improves.
