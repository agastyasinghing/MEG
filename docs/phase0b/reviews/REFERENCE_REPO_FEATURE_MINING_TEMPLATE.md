# Phase 0B-R2 — Reference Repo Feature-Mining Review Template

## 1) Purpose

Use this template to record feature-mining findings from external reference repositories for **ideas only**.

Guardrails:

- no code copying,
- no repository vendoring,
- no runtime or trading behavior changes,
- no implementation work in this review,
- no execution-authority changes.

This review output is planning input only and must be converted into MEG-native backlog tickets before any implementation ticket is considered.

## 2) Review metadata

| Field | Value |
|---|---|
| `repo` | `TBD` |
| `repo_url` | `TBD` |
| `inspected_commit_or_snapshot` | `TBD` |
| `inspection_date` | `YYYY-MM-DD` |
| `reviewer` | `TBD` |
| `license_status` | `approved` / `pending_review` / `restricted` / `rejected` |
| `review_status` | `not_started` / `in_progress` / `completed` / `blocked` |
| `scope_summary` | `TBD` |

## 3) Repository structure findings

| Area | Findings | Evidence/path | Confidence | Notes |
|---|---|---|---|---|
| README/docs quality | `TBD` | `TBD` | `low/medium/high` | `TBD` |
| Source layout | `TBD` | `TBD` | `low/medium/high` | `TBD` |
| Dependency stack | `TBD` | `TBD` | `low/medium/high` | `TBD` |
| Tests | `TBD` | `TBD` | `low/medium/high` | `TBD` |
| CI/deployment | `TBD` | `TBD` | `low/medium/high` | `TBD` |
| Data/model/schema docs | `TBD` | `TBD` | `low/medium/high` | `TBD` |
| Examples/scripts | `TBD` | `TBD` | `low/medium/high` | `TBD` |
| Config/secrets handling | `TBD` | `TBD` | `low/medium/high` | `TBD` |

## 4) Feature-mining findings

| idea_id | useful idea | evidence/path | MEG destination area | confidence | implementation risk | copy/license risk | follow-up ticket |
|---|---|---|---|---|---|---|---|
| `IDEA-001` | `TBD` | `TBD` | `TBD` | `low/medium/high` | `low/medium/high` | `low/medium/high` | `TBD` |

## 5) Architecture checklist

Mark each item with `yes` / `no` / `partial` and add evidence notes.

| Area | Status | Evidence/path | Notes |
|---|---|---|---|
| Agent architecture | `TBD` | `TBD` | `TBD` |
| Bot lifecycle | `TBD` | `TBD` | `TBD` |
| Exchange/client abstraction | `TBD` | `TBD` | `TBD` |
| Data model | `TBD` | `TBD` | `TBD` |
| Strategy framing | `TBD` | `TBD` | `TBD` |
| Risk controls | `TBD` | `TBD` | `TBD` |
| Order/execution boundary | `TBD` | `TBD` | `TBD` |
| Backtesting/simulation | `TBD` | `TBD` | `TBD` |
| Monitoring/logging | `TBD` | `TBD` | `TBD` |
| Deployment/CI | `TBD` | `TBD` | `TBD` |

## 6) Safety and copy/learn rules

1. Mine ideas, not code.
2. Do not copy files or snippets from external repositories.
3. Do not vendor external repositories into MEG.
4. Do not adopt dependencies without a separate dependency/license/security review ticket.
5. Do not bypass MEG operator approval rules (Telegram approval remains mandatory).
6. Do not create live execution behavior from this review.
7. Convert useful observations into MEG-native planning tickets only.

## 7) First-batch placeholder sections

### 7.1 Jon-Becker/prediction-market-analysis

- Review status: `TBD`
- Summary: `TBD`
- Candidate ideas: `TBD`

### 7.2 ImMike/polymarket-arbitrage

- Review status: `TBD`
- Summary: `TBD`
- Candidate ideas: `TBD`

### 7.3 Polymarket/agents

- Review status: `TBD`
- Summary: `TBD`
- Candidate ideas: `TBD`

### 7.4 skharchikov/polymarket-bot

- Review status: `TBD`
- Summary: `TBD`
- Candidate ideas: `TBD`

### 7.5 Drakkar-Software/OctoBot-Prediction-Market (alternate)

- Review status: `TBD`
- Summary: `TBD`
- Candidate ideas: `TBD`

## 8) Decision matrix

| Decision | Status (`yes` / `no` / `needs_review` / `defer`) | Rationale | Follow-up |
|---|---|---|---|
| Useful for MEG backlog | `TBD` | `TBD` | `TBD` |
| Safe to convert into planning ticket | `TBD` | `TBD` | `TBD` |
| Needs license review | `TBD` | `TBD` | `TBD` |
| Too risky / do not use | `TBD` | `TBD` | `TBD` |
| Defer until later phase | `TBD` | `TBD` | `TBD` |

## 9) Non-goals

- no implementation,
- no runtime or trading behavior changes,
- no external repo vendoring,
- no code copying,
- no dependency changes,
- no dataset import,
- no loader expansion.

## 10) Recommended next ticket

Choose one based on sequencing:

- **Phase 0B-R3**: Fill first reference repo feature-mining review notes.
- **Phase 0B-17**: Manual local archive metadata inspection once SSD is available.
