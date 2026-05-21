# Phase 1R-07 — Master PRD Realignment and Catch-up Plan

## 1) Purpose and posture

This document defines the **Phase 1R-07 master PRD realignment and catch-up plan** for the current repository state.

Posture: **docs/static-preflight only**.

This ticket does **not** implement weather strategy code, research lake implementation code, DuckDB query code, fixture derivation/commit flows, loader or connector logic, API calls, order routing, live trading, or any autonomous execution behavior.

`MEG_MASTER_PRD_v4.1_patched.md` is the canonical roadmap source unless an explicit superseding governance decision is recorded.

## 2) Naming correction (required)

Recent tickets labeled “Phase 1” (1-01 through 1-06) are not the master PRD’s real Phase 1 weather paper engine.

They are better classified as **Phase 1R** (research fixture/Bronze foundation) and should be treated as conservative preparation and contract-hardening work.

This naming drift must not continue. Future tickets must explicitly separate:
- **Master PRD Phase 1** (weather paper engine implementation), versus
- **Phase 1R** (fixture/research foundation, static/preflight, and contract scaffolding).

## 3) Master PRD phase summary for catch-up

### A) Phase 0A — Shared rail
- canonical identifier migration (`condition_id`, `token_id`, `outcome`)
- event schemas + Redis bus contracts
- CLOB market-state cache writer
- CLOB user-stream service
- Telegram proposal queue infrastructure
- Postgres journal schema/writers
- paper execution simulator
- heartbeat emitter
- risk envelope skeleton

### B) Phase 0B — Research lake
- DuckDB + Parquet + Becker setup
- Bronze/Silver normalization views
- data dictionary
- seven sanity queries
- query latency gate

### C) Phase 0C — MEG whale spine repair
- Polygon receipt decoder
- `signal_engine` runner
- `signal_aggregator` session fix
- whale-specific Redis channels

### D) Master PRD Phase 1 — Weather paper engine
- weather forecast pipeline
- EMOS calibration module
- resolution source registry
- weather strategy module
- anomaly veto
- 50 paper trade exit gate
- proposal expiry/defer/rejection exercise
- paper P&L attribution

## 4) Completed repository work summary (conservative)

The repository has completed useful preparatory work, but primarily as static/preflight foundation:
- archive inspection and schema-note style planning
- source manifest/source appendix posture documentation
- Polymarket normalization plan
- Kalshi normalization plan
- fixture derivation script plan
- fixture derivation safety shell
- dry-run manifest tooling and tests
- fixture generation/commit gate controls
- Bronze schema static contracts
- candidate-pair and rejection-taxonomy preflight tests
- source appendix maintenance plan

**Do not overclaim implementation**: unless runtime codepaths are present and validated, classify work as `static_preflight_only` or `planned_only`.

## 5) Gap classification matrix

| PRD area | PRD deliverable | Current repo status | Evidence in repo | Gap type | Recommended next action |
|---|---|---|---|---|---|
| Naming/governance | Accurate phase labels aligned to PRD | static_preflight_only | `docs/phase1` ticket lineage 1-01..1-06 | naming_drift | Rename future stream to Phase 1R and reserve “Phase 1” for weather engine |
| Phase 0A | Canonical identifier migration across rail payloads and journals | unknown_needs_code_audit | PRD + canonical-id guard tests indicate intent, but not full rail audit here | verification_gap | Run PRD-0A-AUDIT-01 and produce module-by-module implementation map |
| Phase 0A | Event schemas + Redis bus contracts | unknown_needs_code_audit | existing tests/docs focus mainly on fixture/Bronze preflight | implementation_gap | Audit contracts and add implementation tickets where missing |
| Phase 0A | Telegram proposal queue hardening + expiry/defer/requeue | unknown_needs_code_audit | no claim of completed runtime hardening in this ticket | phase_gate_gap | Audit current bot behavior against PRD exit criteria |
| Phase 0A | Postgres journal writers + paper execution + heartbeat + risk skeleton | unknown_needs_code_audit | no runtime verification added in this ticket | blocked_by_prior_phase | Create readiness plan before weather implementation |
| Phase 0B | DuckDB + Parquet + Becker setup | planned_only | 0B planning docs and fixture-centric preflight tests | implementation_gap | Start PRD-0B-IMPL-01 local-only smoke |
| Phase 0B | Bronze/Silver views, dictionary, sanity queries, latency gate | planned_only | Bronze schema definition docs/tests are static contracts, not live query stack | implementation_gap | Execute PRD-0B-IMPL-02..04 sequence |
| Phase 0C | Whale spine repair (decoder/runner/aggregator/channels) | missing | no completion evidence in current 1R scope | blocked_by_prior_phase | Schedule focused 0C audit + implementation track |
| Master PRD Phase 1 | Weather paper engine | missing | current completed track is fixture/Bronze preparation, not weather engine runtime | phase_gate_gap | Begin only after 0A/0B readiness decision gate |

Allowed status vocabulary used in this matrix: `implemented_verified`, `static_preflight_only`, `planned_only`, `missing`, `unknown_needs_code_audit`.

Allowed gap-type vocabulary used in this matrix: `none`, `naming_drift`, `implementation_gap`, `verification_gap`, `phase_gate_gap`, `research_gap`, `blocked_by_prior_phase`.

## 6) Required catch-up conclusions

- We should **not** claim master PRD Phase 1 is underway until weather paper engine work actually starts.
- We should **not** claim Phase 0B research lake is implemented until DuckDB/Parquet queries and Bronze/Silver views exist and are exercised.
- We should **not** claim Phase 0A shared rail is complete unless shared rail components are implemented and tested.
- We should **not** claim Phase 0C whale spine repair is complete unless receipt decoder, runner, aggregator fix, and whale channels are implemented and tested.
- The fixture/Bronze foundation is useful and should be retained, but it is **preparatory** rather than final product delivery.

## 7) Recommended next PRD-aligned ticket sequence

### Option A — Catch up PRD Phase 0B first
1. **PRD-0B-IMPL-01**: research lake local environment and DuckDB read-only smoke (no committed data)
2. **PRD-0B-IMPL-02**: Becker archive sanity-query harness (local-only, no committed archive outputs)
3. **PRD-0B-IMPL-03**: data-dictionary generation plan/static contract
4. **PRD-0B-IMPL-04**: Bronze/Silver view implementation plan

### Option B — Audit/repair PRD Phase 0A first
1. **PRD-0A-AUDIT-01**: shared rail implementation gap audit against existing code
2. **PRD-0A-AUDIT-02**: canonical identifier migration implementation plan
3. **PRD-0A-AUDIT-03**: paper execution/journal/risk-gate readiness plan

### Option C — Prepare real PRD Phase 1 weather
1. **PRD-P1-WX-01**: weather source verification and resolution registry research
2. **PRD-P1-WX-02**: weather paper engine architecture/spec
3. **PRD-P1-WX-03**: forecast pipeline skeleton

**Immediate next ticket recommendation:** run a **PRD-0A/0B decision gate**; if audit confidence is low, start with **PRD-0B-IMPL-01** local research-lake smoke while preparing 0A audit scoping.

## 8) Phase-gate warning

- Skipping directly to weather code without confirming shared-rail and research-lake prerequisites risks violating master PRD sequencing.
- Continuing fixture/Bronze-only work indefinitely risks accumulating scaffolding without implementing product behavior.
- Next work should move toward actual PRD deliverables while preserving conservative approval gates.

## 9) Language/tooling planning note

- Python remains the default for near-term local research-lake and weather-pipeline implementation because this repo is Python/pytest-oriented and the data stack is DuckDB/Parquet oriented.
- Rust/C++ are not warranted for immediate catch-up tickets.
- Rust/C++ can be revisited later only for proven high-throughput parsing/backtesting or latency-sensitive execution bottlenecks.
- Any new dependency must be justified by ticket scope and approval.

## 10) Explicit non-approvals (this ticket)

This ticket explicitly approves **none** of the following:
- no weather implementation
- no research lake implementation
- no DuckDB query implementation
- no fixture derivation
- no fixture commit
- no data import
- no archive payload reads
- no loader implementation
- no query engine implementation
- no connector implementation
- no API calls
- no order placement
- no live trading
- no autonomous execution

## 11) Canonical-ID guard note

This document preserves the canonical identifier posture (`condition_id`, `token_id`, `outcome`) and avoids direct use of deprecated legacy market identifier literals in new planning text.
