# Phase 0B-R5 — Concept Planning Tickets from Reference-Repo Findings

## 1) Purpose

This document converts approved Phase 0B-R4 concept findings into MEG-native planning tickets with explicit acceptance criteria.

Guardrails for this ticket:

- planning-only output,
- no implementation,
- no code copying,
- no external repo vendoring,
- no live execution changes,
- no operator-approval bypass,
- no runtime authority changes.

## 2) Source Findings Referenced (Concept-Level Only)

### 2.1 ImMike/polymarket-arbitrage

Concept findings carried forward into planning tickets:

- cross-platform opportunity framing for comparable markets,
- bundle mispricing invariant idea (YES + NO consistency framing),
- threshold/risk-gate configuration idea (edge/spread/exposure caps),
- operator approval risk gap (autonomous framing contrast with MEG hard-gate policy).

### 2.2 Polymarket/agents

Concept findings carried forward into planning tickets:

- connector/interface boundary idea for external services,
- CLI/research utility separation from trade entrypoints,
- runbook/bootstrap artifact idea for operator setup discipline,
- autonomous trade framing as a safety contrast to MEG operator-gated execution.

## 3) Planning Ticket 1 — Cross-platform opportunity detector contract

### Scope

Define a documentation and test-spec contract for opportunity candidate normalization across platforms.

### Required contract elements

- input shape definition,
- normalized market pair candidate schema,
- platform identifiers,
- canonical identifiers: `condition_id`, `token_id`, and `outcome` where available,
- price/odds fields,
- side fields,
- fee assumptions,
- edge estimate,
- confidence score,
- provenance/source fields,
- output shape,
- rejection and fail-closed behavior,
- explicit statement that this contract has no execution authority.

### Acceptance criteria

- contract artifact is documentation/test-spec only,
- no runtime integration,
- no live order routing,
- no connector calls,
- no dependency changes,
- canonical identifier wording is preserved (`condition_id`, `token_id`, `outcome`),
- operator approval remains outside scope.

## 4) Planning Ticket 2 — Threshold and risk-gate configuration spec

### Scope

Define planning-only configuration semantics for opportunity screening and protective limits.

### Required configuration semantics

- minimum edge threshold,
- minimum spread threshold,
- maximum per-market exposure,
- maximum global exposure,
- maximum daily loss,
- fee-adjusted edge requirement,
- confidence threshold,
- dry-run/paper-only default,
- fail-closed behavior for missing configuration,
- audit/logging expectations for threshold evaluations and rejections.

### Acceptance criteria

- configuration spec is planning-only,
- no risk engine change,
- no execution change,
- no default live trading,
- missing/invalid configuration fails closed,
- operator approval remains mandatory.

## 5) Planning Ticket 3 — Connector/interface boundary spec

### Scope

Define interface documentation boundaries for future adapter work while preserving strict safety and review controls.

### Required boundary definitions

- interface boundaries for market metadata,
- price/orderbook snapshots,
- account/wallet read-only state,
- proposal emission,
- external API isolation,
- dependency review gate,
- no external repo code adoption,
- no secrets in docs/tests,
- test doubles/fixtures required before any live connector implementation.

### Acceptance criteria

- interface artifact is docs-only,
- no Polymarket/Kalshi live connector implementation,
- no external dependency adoption,
- no secrets committed,
- all adapters remain read-only until separate approval,
- future implementation requires a separate PR.

## 6) Planning Ticket 4 — Operator-approval boundary checks

### Scope

Define planning-only approval invariants and future test expectations around execution authorization.

### Required boundary checks

- Telegram/operator approval remains hard gate,
- no autonomous order placement,
- proposal-only outputs before approval,
- explicit no-bypass invariant,
- approval-path testing expectations,
- rejection/fail-closed behavior,
- audit evidence requirements for approval decisions,
- separation between analysis, proposal, approval, and execution stages.

### Acceptance criteria

- docs/test-spec only,
- no runtime approval-path modification,
- no order-router modification,
- no autonomous execution,
- future tests must prove proposal-only state before approval,
- future tests must prove order placement cannot occur without approval.

## 7) Cross-ticket dependency order

Recommended sequence:

1. Connector/interface boundary spec first.
2. Opportunity detector contract second.
3. Threshold/risk-gate configuration spec third.
4. Operator-approval boundary checks before any execution-adjacent implementation.

## 8) Safety and non-goals

This ticket explicitly does **not** approve or include:

- implementation,
- runtime/trading changes,
- execution/approval-path changes,
- dependency changes,
- external repo code copying,
- external repo vendoring,
- dataset import,
- loader expansion,
- live API/trading use,
- jurisdiction/ToS decisions (separate review track).

## 9) Recommended next ticket

Recommended next ticket: **Phase 0B-R6 — License/ToS/reference repo review pass**.

Rationale: complete legal/terms posture before drafting connector-spec implementation-adjacent artifacts.
