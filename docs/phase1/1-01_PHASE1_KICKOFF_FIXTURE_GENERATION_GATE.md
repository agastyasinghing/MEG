# Phase 1-01 — Phase 1 Kickoff and Fixture Generation Gate (Docs-Only)

## 1) Purpose and posture

This document is the **Phase 1 kickoff/gate document** for MEG.

This ticket is **documentation-only**.

This ticket does **not** implement scripts, loaders, query engines, connectors, fixture derivation, archive import, order routing, live trading, or autonomous execution.

Phase 1 begins only after **Phase 0B-26 is merged and CI is green**.

Phase 1 remains conservative and approval-gated. No execution authority is granted by this document.

## 2) Phase 0B closure summary

Phase 0B established the foundation required for conservative Phase 1 kickoff:

- local Jon-Becker archive metadata/schema inspection completed,
- source manifest placeholders created,
- tiny fixture candidate groups planned,
- cross-platform semantic matching research plan completed,
- Polymarket token/outcome normalization plan completed,
- Kalshi normalized fills/markets mapping plan completed,
- tiny fixture derivation script plan completed,
- cross-platform candidate-pair schema tests added,
- semantic matching rejection-reason taxonomy tests added,
- source appendix maintenance plan completed.

## 3) Phase 1 scope

Phase 1 is defined as **controlled local data foundation work**.

Allowed Phase 1 direction (subject to explicit follow-on tickets and approvals):

- implement a local-only fixture derivation script safety shell,
- implement dry-run/provenance/checksum behavior,
- derive tiny deterministic fixtures only after explicit approval,
- commit tiny fixture files only after explicit approval,
- implement Bronze schema definitions only after fixture/source gates are satisfied,
- add static/preflight tests for fixture manifests and Bronze schemas.

Not allowed by this kickoff alone:

- full archive import,
- production loaders,
- live API connectors,
- source refresh automation,
- execution logic,
- order routing,
- live trading,
- autonomous execution,
- geoblock/ToS/jurisdiction workarounds,
- treating source appendix entries as legal approval.

## 4) Phase 1 gate checklist

Before any fixture derivation script can be implemented:

- Phase 0B-23 script plan must be referenced,
- approved local archive root must be configured through an explicit future gate,
- source manifest entry must be reviewed,
- license/provenance posture must be reviewed,
- no network/API/secrets/trading connector dependencies allowed,
- AppleDouble files must be ignored,
- absolute local archive paths must not be embedded in fixture payloads,
- checksum/provenance manifest shape must be defined,
- output directory must be explicitly approved,
- tiny row/object limits must be explicit,
- CI must prove no data/archive/.duckdb/report artifacts were committed.

## 5) Fixture generation approval gate

Fixture derivation approval and fixture commit approval are separate gates.

### A) Script implementation approval

Script implementation approval may allow code to:

- validate paths,
- dry-run,
- calculate checksums,
- emit planned manifest output.

Script implementation approval must **not** create fixture files unless separately approved.

### B) Fixture derivation approval

Fixture derivation approval may allow a local operator to run an approved script against an approved local archive.

Fixture derivation approval must record:

- source manifest ID,
- source file checksums,
- selected row keys,
- generated fixture checksums,
- script version,
- parser version,
- reviewer reference,
- derivation timestamp.

### C) Fixture commit approval

Fixture commit approval may allow tiny JSON fixtures to be committed only after review.

Fixture commit approval must prove:

- bounded size,
- no secrets,
- no private PII,
- no full local absolute archive paths,
- no ToS/redistribution conflict,
- no execution implication.

## 6) Planned Phase 1 ticket sequence

Recommended sequence (may be adjusted, but approvals must not be skipped):

1. **Phase 1-02**: local fixture derivation script safety shell, no fixture output.
2. **Phase 1-03**: fixture manifest/provenance contract tests, static/preflight only.
3. **Phase 1-04**: tiny fixture derivation dry-run implementation, no committed fixture outputs.
4. **Phase 1-05**: explicit tiny fixture generation/commit gate, only if approval criteria pass.
5. **Phase 1-06**: Bronze schema definitions for Kalshi and Polymarket fixture-backed data.
6. **Phase 1-07**: Bronze schema validation tests against committed tiny fixtures.
7. **Phase 1-08**: Phase 1 closeout/readiness review for Silver normalization.

## 7) Language/tooling note

- This ticket is docs-only.
- Python is the likely default for upcoming local fixture tooling because the repo already uses Python/pytest and archive inspection used Python/DuckDB.
- Rust/C++ are not needed for Phase 1 fixture gating unless later performance-sensitive large-scale scanning/backtesting work justifies them.
- No new dependencies should be added casually.
- Any dependency addition must be justified in its own ticket.

## 8) Relation to Phase 0B artifacts

This Phase 1 gate depends directly on the following Phase 0B artifacts:

- 0B-19 fixture candidate plan,
- 0B-21 Polymarket normalization plan,
- 0B-22 Kalshi normalization plan,
- 0B-23 fixture derivation script plan,
- 0B-24 candidate-pair schema tests,
- 0B-25 rejection taxonomy tests,
- 0B-26 source appendix maintenance plan.

Together, these define the baseline assumptions and preflight guardrails that must hold before any fixture derivation or Bronze schema implementation begins.

## 9) Artifact and repository hygiene

Phase 1 hygiene rules:

- never commit `data.tar.zst`,
- never commit extracted archive data,
- never commit arbitrary local outputs,
- never commit `.duckdb` files,
- never commit generated reports unless explicitly approved,
- never commit external repo files,
- fixture outputs must be tiny, deterministic, reviewable, and explicitly approved,
- local archive paths may appear in docs/plans but must not be embedded in fixture payloads.

## 10) Phase 1 non-approvals

This kickoff does **not** approve:

- script implementation in this ticket,
- fixture derivation,
- fixture commit,
- data import,
- loader implementation,
- query engine implementation,
- connector implementation,
- API calls,
- source refresh automation,
- order placement,
- live trading,
- autonomous execution,
- legal conclusion or legal approval.

## 11) Static canonical-ID guard

Canonical-ID guard posture for this document:

- avoid the literal legacy identifier token,
- prefer `source_market_ref`, `ticker_ref`, native market reference, source market identifier, or legacy market identifier prose,
- if a future change unavoidably requires the literal legacy identifier token, update `tests/core/canonical_id_allowlist.py` exactly and narrowly in that future ticket only,
- do not increase legacy identifier counts casually.
