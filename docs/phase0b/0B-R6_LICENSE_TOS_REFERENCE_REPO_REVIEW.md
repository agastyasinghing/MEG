# Phase 0B-R6 — License/ToS/Reference Repo Review Pass

## 1) Purpose

This document records a conservative review of license, terms-of-service (ToS), jurisdiction, and reference-repository usage posture for Phase 0B planning.

This is explicitly:

- planning-only,
- not a legal conclusion,
- not implementation approval,
- not live API/trading approval.

## 2) Scope boundary

Current boundary for this ticket:

- idea-mining from public documentation is allowed for planning,
- code copying is not approved,
- vendoring external repositories is not approved,
- dependency adoption is not approved,
- live API or trading use is not approved,
- jurisdiction/ToS compliance requires separate review before any runtime usage.

## 3) Reviewed sources table

| source/repo | review status | license status | ToS/jurisdiction status | allowed MEG usage now | blocked usage | follow-up needed |
|---|---|---|---|---|---|---|
| `ImMike/polymarket-arbitrage` | `completed_partial` (idea pass) | `pending_review` (not conclusively verified in prior pass) | `pending_review` | concept-level planning only | code copying, vendoring, dependency adoption, execution logic reuse | explicit license confirmation + ToS/jurisdiction review before any runtime-adjacent use |
| `Polymarket/agents` | `completed_partial` (idea pass) | `pending_review` (README states MIT; separate compatibility check still required) | `pending_review` (README notes US persons and persons from certain other jurisdictions are prohibited from trading via UI/API/agents, while data/information is globally viewable) | architecture/backlog planning only | live agent/API trading use, code copying, vendoring, dependency adoption | separate ToS/jurisdiction eligibility review + operator/runtime approvals before any live usage |
| `Jon-Becker/prediction-market-analysis` | `completed_partial` (manual code/docs review) | `repo_code_license_reviewed_acceptable` (per operator note) | `pending_review` for dataset/archive terms and provenance | research planning and source-manifest planning | dataset import, fixture derivation, loader expansion until archive/provenance review passes | inspect archive provenance/checksums/terms; then re-evaluate fixture/import gates |
| local Polymarket/Kalshi historical archive placeholder | `not_started` / uninspected | `pending_review` | `pending_review` | none beyond planning | import, fixture derivation, loader expansion | local path/checksum/provenance capture and archive terms review |
| `skharchikov/polymarket-bot` | `pending_review` | `pending_review` | `pending_review` | none beyond future review planning | any code/dependency/runtime use | complete inspection and license/ToS review pass |
| `Drakkar-Software/OctoBot-Prediction-Market` | `pending_review` | `pending_review` | `pending_review` | none beyond future review planning | any code/dependency/runtime use | complete inspection and license/ToS review pass |

## 4) Source-specific notes

### 4.1 ImMike/polymarket-arbitrage

- Inspected as an idea source only.
- License was not conclusively verified in the prior pass.
- Allowed usage now: concept-level planning only.
- Blocked usage now: code copying, vendoring, dependency adoption, and execution logic reuse.

### 4.2 Polymarket/agents

- Inspected as an idea source only.
- Repository was observed archived/read-only as of prior inspection.
- README states MIT; separate ToS/jurisdiction review still remains required.
- README states US persons and persons from certain other jurisdictions are prohibited from trading via UI/API/agents, while data/information is viewable globally.
- Restriction posture is not framed as US-only.
- Allowed usage now: architecture/backlog planning only.
- Blocked usage now: live agent/API trading use, code copying, vendoring, dependency adoption.

### 4.3 Jon-Becker/prediction-market-analysis

- Repository code/docs were manually reviewed.
- Repo-code license review looked acceptable per operator note.
- Dataset/archive terms and provenance remain pending.
- Allowed usage now: research planning and source-manifest planning.
- Blocked usage now: dataset import, fixture derivation, and loader expansion until archive/provenance review passes.

### 4.4 Local Polymarket/Kalshi archive placeholder

- Uninspected in this pass.
- Local path/checksum/provenance are pending.
- Allowed usage now: none beyond planning.
- Blocked usage now: import, fixture derivation, loader expansion.

### 4.5 skharchikov/polymarket-bot and Drakkar-Software/OctoBot-Prediction-Market

- Not inspected yet.
- Kept as `pending_review`.
- Allowed usage now: none beyond future review planning.

## 5) Usage boundary matrix

| usage item | allowed now? | conditions | required follow-up before use |
|---|---|---|---|
| concept-level ideas | yes | keep planning-only, MEG-native restatement, no code transfer | none beyond standard planning review |
| documentation summaries | yes | summary-only; no legal conclusions | none beyond standard doc review |
| code snippets | no | blocked in this phase | license + ToS + internal review policy decision |
| copied files | no | blocked | explicit approval path (not in Phase 0B-R6 scope) |
| vendored external repos | no | blocked | separate architecture/legal/security decision ticket |
| new dependencies | no | blocked | dependency/license/security review |
| live API calls | no | blocked | connector/interface spec + ToS/jurisdiction/eligibility review + explicit runtime approval |
| live trading/order placement | no | blocked | operator-approval boundary tests + ToS/jurisdiction review + explicit execution approval |
| dataset import | no | blocked | provenance/checksum/terms review for selected dataset/archive |
| tiny fixture derivation | no | blocked | source provenance + terms review + documented deterministic derivation plan |

## 6) Jurisdiction/ToS posture

- User/operator location alone is not enough to approve usage.
- Actual trading/API/agent use requires separate review of applicable ToS, account eligibility, jurisdiction constraints, and platform access rules.
- Phase 0B documentation approves planning only.
- Live use remains blocked until separate explicit approval.

## 7) Recommended unblock sequence

1. Finish this R6 review and keep planning-only posture explicit.
2. Draft connector/interface boundary spec as docs-only.
3. Inspect local ~36 GiB archive metadata once SSD is available.
4. Perform separate dependency/security review before any connector implementation.
5. Perform separate operator-approval boundary tests before any execution-adjacent implementation.

## 8) Safety and non-goals

This ticket does **not** approve or include:

- implementation,
- runtime/trading changes,
- execution/approval changes,
- dependency changes,
- external code copying,
- vendoring,
- dataset import,
- loader expansion,
- live API/trading approval,
- legal advice or legal conclusion.

## 9) Recommended next ticket

Recommended next ticket: **Phase 0B-R7 — Draft connector/interface boundary spec**.

Rationale: it preserves docs-only progression after this review while keeping runtime/API/trading behavior blocked pending separate approvals.
