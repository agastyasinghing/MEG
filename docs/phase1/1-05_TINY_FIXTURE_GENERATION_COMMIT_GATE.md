# Phase 1-05 — Tiny Fixture Generation / Commit Gate (Docs + Static Preflight Only)

## 1) Purpose and posture

This document defines the **Phase 1-05 explicit tiny fixture generation/commit gate**.

This ticket is **documentation + static/preflight test only**.

This ticket does **not** generate, derive, or commit fixtures.

This ticket does **not** read archive payloads (no Parquet/JSON archive row reads).

This ticket does **not** approve full archive import, loaders, query engines, connector implementation, API calls, order routing, live trading, or autonomous execution.

This gate is required before any later PR may commit Phase 1 tiny fixtures.

## 2) Gate separation

### A) Dry-run manifest review (pre-derivation)

Required evidence before any local derivation approval can be requested:

- Phase 1-04 dry-run manifest command executed via the Phase 1-02 safety shell dry-run entrypoint (`dry-run-manifest`).
- Dry-run manifest JSON captured in PR body or local review notes.
- Exactly seven fixture families present.
- Dry-run placeholders only for checksums/timestamps.
- Global posture is conservative (research/local only; no execution authority).
- Artifact hygiene booleans are true.
- Reviewer envelope is pending with human review required.

### B) Local derivation approval (human-gated, still no commit)

Required evidence before local derivation may occur in a later ticket/operator PR:

- Explicit reviewer approval reference for derivation.
- Approved local archive root reference.
- `source_manifest_ref` captured.
- `source_repo_ref` captured.
- `source_repo_commit` captured.
- `source_archive_ref` captured.
- Source file relative paths only.
- AppleDouble files ignored.
- No network/API/secrets/connectors.
- No `.duckdb` or report artifacts.
- Bounded row/object count `1..5` for each selected fixture family.
- Source file checksum capture.
- Selected stable keys capture.
- Row-selection rule capture.

### C) Fixture commit approval (separate gate after derivation)

Required evidence before fixture commit may occur in a later PR:

- Generated fixture checksum capture.
- Fixture manifest committed together with fixture files.
- No absolute local archive paths inside fixture payloads.
- No secrets.
- No private PII.
- No full archive data.
- No compressed archive content.
- No external repo files.
- Tiny size bounds respected.
- Reviewed unresolved-state policy.
- Reviewer signoff for commit.
- CI artifact hygiene checks passing.

## 3) Required evidence checklist

| Evidence item | Required before derivation | Required before commit | Source / command / reference | Blocks if missing? |
|---|---|---|---|---|
| Phase 1-04 dry-run manifest JSON | Yes | Yes | Phase 1-04 dry-run output (`dry-run-manifest`) | Yes |
| `source_manifest_ref` | Yes | Yes | Dry-run manifest + reviewer notes | Yes |
| `source_repo_ref` | Yes | Yes | Dry-run manifest + reviewer notes | Yes |
| `source_repo_commit` | Yes | Yes | Dry-run manifest + reviewer notes | Yes |
| `source_archive_ref` | Yes | Yes | Dry-run manifest + reviewer notes | Yes |
| Approved local archive root | Yes | Yes | Reviewer approval record | Yes |
| Source relative path list | Yes | Yes | Dry-run manifest fixture entries | Yes |
| Output relative path list | Yes | Yes | Dry-run manifest fixture entries | Yes |
| Selected stable keys | Yes | Yes | Dry-run manifest fixture entries | Yes |
| Row-selection rule | Yes | Yes | Dry-run manifest fixture entries | Yes |
| Selected row/object counts | Yes | Yes | Dry-run manifest fixture entries | Yes |
| Source file checksums | Yes | Yes | Dry-run placeholders; real values after derivation approval | Yes |
| Generated fixture checksums | No | Yes | Generated manifest values in commit PR | Yes |
| Script version | Yes | Yes | Dry-run manifest + derivation record | Yes |
| Parser version | Yes | Yes | Dry-run manifest + derivation record | Yes |
| Derivation timestamp | No | Yes | Derivation record in fixture manifest | Yes |
| Reviewer reference | Yes | Yes | Review envelope / PR notes | Yes |
| No absolute path evidence | Yes | Yes | Static checks + payload review | Yes |
| No secret/PII evidence | Yes | Yes | Static checks + payload review | Yes |
| No `.duckdb`/report/archive artifact evidence | Yes | Yes | CI + artifact hygiene checks | Yes |
| CI test command evidence | Yes | Yes | CI logs + local pytest evidence | Yes |

## 4) Local operator runbook (future, non-executable guidance)

1. Run dry-run manifest first.
2. Inspect dry-run JSON and confirm seven planned families.
3. Confirm no fixture outputs exist yet.
4. Request derivation approval with reviewer reference and archive-root approval.
5. Only after approval, run a **future derivation command from a later ticket**.
6. Verify generated files are tiny JSON only.
7. Inspect fixture payloads for no absolute paths, secrets, or private PII.
8. Compute/check generated checksums and record them in fixture manifest evidence.
9. Include fixture manifest and fixture files in a later commit PR only after explicit commit approval.

## 5) Future fixture commit PR expectations

A later fixture commit PR must include:

- Fixture manifest.
- Seven tiny fixture files, or an approved subset with explicit reason.
- Source/generation checksums.
- Selected stable keys.
- Row-selection rules.
- Reviewer approval references.
- Tests proving fixture shape and hygiene.
- No runtime loader usage.
- No full archive import.
- No live/API/trading/autonomy behavior.

## 6) Fixture family gate coverage

| Fixture family | Expected source relative path | Expected output relative path | Expected row/object limit | Expected normalization plan ref | Expected selected stable keys |
|---|---|---|---|---|---|
| `kalshi_markets_tiny` | `data/kalshi/markets/markets_0_10000.parquet` | `fixtures/phase1/kalshi_markets_tiny.json` | 1 to 5 (dry-run plans 3) | `0B-22` | `ticker_ref`, `event_ticker_ref`, `fetched_at` |
| `kalshi_trades_tiny` | `data/kalshi/trades/trades_0_10000.parquet` | `fixtures/phase1/kalshi_trades_tiny.json` | 1 to 5 (dry-run plans 2) | `0B-22` | `trade_ref`, `ticker_ref`, `created_time` |
| `poly_markets_tiny` | `data/polymarket/markets/markets_0_10000.parquet` | `fixtures/phase1/poly_markets_tiny.json` | 1 to 5 (dry-run plans 3) | `0B-21` | `condition_id`, `source_market_ref`, `fetched_at` |
| `poly_clob_trades_tiny` | `data/polymarket/trades/trades_0_10000.parquet` | `fixtures/phase1/poly_clob_trades_tiny.json` | 1 to 5 (dry-run plans 4) | `0B-21` | `transaction_hash`, `log_index`, `order_hash` |
| `poly_blocks_tiny` | `data/polymarket/blocks/blocks_10000000_10100000.parquet` | `fixtures/phase1/poly_blocks_tiny.json` | 1 to 5 (dry-run plans 5) | `0B-21` | `block_number` |
| `poly_legacy_fpmm_trades_tiny` | `data/polymarket/legacy_trades/trades_0_10000.parquet` | `fixtures/phase1/poly_legacy_fpmm_trades_tiny.json` | 1 to 5 (dry-run plans 3) | `0B-21` | `transaction_hash`, `log_index`, `fpmm_address` |
| `poly_fpmm_collateral_lookup_tiny` | `data/polymarket/fpmm_collateral_lookup.json` | `fixtures/phase1/poly_fpmm_collateral_lookup_tiny.json` | 1 to 5 (dry-run plans 2) | `0B-21` | `fpmm_address`, `collateral_token_address` |

## 7) Blocking conditions

Block derivation and/or commit when any condition is true:

- Phase 1-04 dry-run manifest missing.
- Dry-run manifest has fewer/more than seven planned families.
- Any fixture family points outside approved source families.
- Any output path is outside `fixtures/phase1/`.
- Any row/object count is outside `1..5`.
- Source checksum missing before derivation.
- Generated checksum missing before commit.
- Any absolute local archive path appears in fixture payload.
- Secrets/API keys/private PII detected.
- `.duckdb`/report/archive/external repo artifact present.
- AppleDouble source selected.
- Unresolved license/provenance posture.
- Reviewer approval missing.
- CI failing.
- Any execution/order/live/autonomy posture enabled.

## 8) Static/preflight test contract for this ticket

This ticket adds only static/preflight tests and text checks.

Scope rules for test implementation:

- In-memory constants + repository text reads only.
- No fixture files.
- No archive reads.
- No network/API usage.
- No DuckDB access.
- No production runtime imports except existing safety-shell and contract modules already used by static tests.

Validation points:

- Gate document exists.
- Gate document states no fixture generation/commit in this ticket.
- Gate document separates A/B/C gate phases.
- Gate document includes all seven fixture families.
- Gate document includes required evidence checklist items.
- Gate document includes explicit blocking conditions.
- Gate document references Phase 1-04 dry-run manifest.
- Gate document references Phase 1-02 safety shell and Phase 1-03 manifest/provenance contract.
- Gate document does not contain real fixture payloads.
- Gate document does not include commands claiming real fixture derivation now.
- Safety shell still exposes `dry-run-manifest`.
- Phase 1-03 manifest/provenance contract still allows `dry_run_manifest`.
- No fixture output directory exists in this ticket.
- No data/fixture artifact paths were added by this PR.

## 9) Relation to next tickets

Recommended sequence:

1. Phase 1-06: Bronze schema definitions for Kalshi and Polymarket fixture-backed data, still no reliance on committed real fixtures unless this fixture commit gate is satisfied.
2. Phase 1-05B or local operator PR (if needed): approved tiny fixture generation/commit PR using this gate evidence.
3. Phase 1-07: Bronze schema validation tests against committed tiny fixtures after fixtures exist.
4. Phase 1-08: Phase 1 closeout/readiness review for Silver normalization.

## 10) Explicit non-approvals

This ticket explicitly does **not** approve:

- fixture derivation,
- fixture commit,
- data import,
- archive payload reads,
- loader implementation,
- query engine,
- connector implementation,
- API calls,
- source refresh automation,
- order placement,
- live trading,
- autonomous execution,
- legal conclusion or legal approval.

## 11) Canonical identifier guard

Canonical identifier posture remains unchanged:

- preserve canonical contract fields `condition_id`, `token_id`, and `outcome` where applicable,
- avoid literal legacy market identifier token in this Phase 1-05 doc/test,
- prefer `source_market_ref`, `ticker_ref`, native market reference, source market identifier, or legacy market identifier prose.
