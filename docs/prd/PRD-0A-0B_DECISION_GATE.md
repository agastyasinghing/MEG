# PRD-0A/0B Decision Gate — Shared Rail vs Research Lake

## 1) Purpose and posture

This document is **PRD-0A/0B-DECISION-01**, the decision gate for selecting the next PRD-aligned implementation lane after Phase 1R-07.

This ticket is **docs/static-preflight only**.

This document does **not** implement shared rail, research lake, DuckDB queries, fixtures, loaders, connectors, API calls, order routing, live trading, autonomous execution, or weather strategy implementation.

This gate exists because **Phase 1R-07 corrected naming drift** and explicitly warned against skipping master PRD sequencing.

## 2) Inputs reviewed

Inputs reviewed for this decision gate:

- `MEG_MASTER_PRD_v4.1_patched.md`
- `docs/phase1/1R-07_MASTER_PRD_REALIGNMENT_CATCHUP_PLAN.md`
- Phase 1R fixture/Bronze docs and static tests
- Phase 0B planning docs (`0B-19`, `0B-20C`, `0B-21`, `0B-22`, `0B-23`, `0B-26`)
- Current repository structure at a high level (docs/tests lineage and branch history)

This is not a full runtime code audit.

## 3) PRD Phase 0A readiness check (shared rail)

| PRD deliverable | Current evidence | Confidence | Status | Blocking concern | Recommended action |
|---|---|---|---|---|---|
| canonical identifier migration | Master PRD and canonical-id tests define contract and migration intent; no full module-by-module implementation verification in this ticket | medium | partial_or_uncertain | residual legacy market identifier usage may remain in runtime modules pending audit | run PRD-0A-AUDIT-01 to verify rail-wide migration completion |
| event schemas + Redis bus contracts | 1R-07 identifies this as needing code audit; current work is primarily docs/static-preflight | low | unknown_needs_code_audit | contract completeness and runtime conformance unverified | perform focused rail contract audit and create repair tickets |
| CLOB market-state cache writer | Master PRD defines this deliverable; no implementation verification performed here | unknown | unknown_needs_code_audit | runtime behavior and readiness unknown | audit module presence, behavior, and tests |
| CLOB user-stream service | PRD requirement documented; no runtime verification in this ticket | unknown | unknown_needs_code_audit | fill reconciliation path may be incomplete or unverified | audit service path and acceptance coverage |
| Telegram proposal queue infrastructure | PRD + 1R-07 call for operator-approved proposal flow; no completion claim made here | low | partial_or_uncertain | expiry/defer/requeue hardening and telemetry readiness unclear | run scope-limited audit and gap plan |
| Postgres journal schema/writers | PRD requires journaled execution records; this ticket performed docs/static checks only | low | unknown_needs_code_audit | journaling coverage against PRD fields not confirmed | audit schema/writers and map missing items |
| paper execution simulator | PRD requires paper execution path; no runtime inspection completed in this gate | unknown | unknown_needs_code_audit | cannot claim phase readiness without simulator verification | include in PRD-0A-AUDIT-01 module map |
| heartbeat emitter | PRD requires heartbeat; no runtime verification done here | unknown | unknown_needs_code_audit | operator observability readiness uncertain | audit implementation and tests |
| risk envelope skeleton | PRD requires risk envelope skeleton before weather phase; no implementation claim in this ticket | low | unknown_needs_code_audit | gating controls may be incomplete | audit risk modules before weather start |

## 4) PRD Phase 0B readiness check (research lake)

| PRD deliverable | Current evidence | Confidence | Status | Blocking concern | Recommended action |
|---|---|---|---|---|---|
| DuckDB + Parquet + Becker setup | Planned in master PRD and 1R-07; no concrete implementation evidence validated in this ticket | low | planned_only | implementation not yet verified or exercised | start PRD-0B-IMPL-01 local read-only smoke |
| raw partition access / local-only archive read posture | 0B docs establish cautious local-only posture; no implementation confirmation here | medium | static_preflight_only | must avoid committed data and archive outputs | enforce local-only smoke constraints |
| Bronze/Silver normalization views | Bronze schema docs/tests exist as static contracts; live query-stack not claimed | medium | planned_only | no verified DuckDB view implementation in this ticket | implement minimal local views in PRD-0B-IMPL sequence |
| data dictionary | PRD and prior docs specify dictionary expectation; no produced implementation artifact verified here | low | planned_only | schema reference remains planning-level | generate via explicit 0B implementation ticket |
| seven sanity queries | Mentioned in PRD/phase planning trajectory; not implemented/validated in this ticket | low | planned_only | no executed query proof in this gate | implement and run in local-only smoke ticket |
| query latency gate | PRD goal exists; no measured gate evidence in this ticket | unknown | planned_only | latency criteria currently unverified | add measured local checks in follow-on 0B implementation |
| fixture/Bronze foundation from Phase 1R | 1-01/1-05/1-06/1R-07 docs and tests provide static groundwork | high | static_preflight_only | foundation could stall without implementation transition | use foundation to launch PRD-0B-IMPL-01 |

Allowed confidence vocabulary: `high`, `medium`, `low`, `unknown`.

Allowed status vocabulary: `implemented_verified`, `partial_or_uncertain`, `static_preflight_only`, `planned_only`, `missing`, `unknown_needs_code_audit`.

## 5) Decision logic

- If Phase 0A shared rail is unknown/uncertain, do not start weather implementation.
- If Phase 0B research lake is planned/static only, start PRD-0B-IMPL-01 before claiming Phase 0B implementation.
- If both 0A and 0B are uncertain, start a local-only 0B smoke in parallel with scoped 0A audit prep.
- If 0B local smoke requires no runtime rail and no committed data, it may proceed before full 0A completion.
- If any work requires runtime proposals, paper execution, Telegram approval, Postgres journal, or risk gates, it must wait for 0A audit/repair.
- Do not begin master PRD Phase 1 weather paper engine until 0A/0B readiness is explicitly resolved.

## 6) Decision outcome

Recommended immediate path:

- Start **PRD-0B-IMPL-01**: local research lake / DuckDB read-only smoke, no committed data, no archive outputs.
- In parallel or immediately after, start **PRD-0A-AUDIT-01**: shared rail implementation gap audit.
- Do not start weather paper engine yet.

Rationale:

- 0B local smoke is local-only and does not depend on runtime shared rail.
- 0A shared rail completeness remains uncertain and needs a scoped code audit.
- Weather paper engine depends on shared rail confidence and should not begin yet.

## 7) Next-ticket definitions

### A) PRD-0B-IMPL-01 — local research lake / DuckDB read-only smoke

- local-only
- no committed data
- no fixture commit
- no archive outputs
- no full import
- verify DuckDB can query approved local archive sample paths or configurable paths
- produce no generated report artifacts unless explicitly approved
- Python/DuckDB likely appropriate, but dependency posture must be checked

### B) PRD-0A-AUDIT-01 — shared rail implementation gap audit

- code audit only
- no runtime changes
- map current modules to PRD 0A deliverables
- identify implemented/missing/partial items
- produce module-by-module repair sequence

## 8) Phase gate warnings

- Weather work remains blocked until this decision path is acted on.
- Whale Phase 0C work remains separate and should not be mixed into 0A/0B catch-up unless explicitly scoped.
- Fixture/Bronze foundation should not expand indefinitely without moving toward actual PRD deliverables.
- Local archive/DuckDB work must not commit archive data or generated artifacts.

## 9) Language/tooling note

- PRD-0B-IMPL-01 likely uses Python with DuckDB if DuckDB is already an approved dependency or explicitly added/justified.
- If DuckDB is already in project dependencies, use it through the existing dependency workflow.
- If DuckDB is not available, PRD-0B-IMPL-01 must either add it through an explicit dependency ticket or remain a docs/local-command plan.
- PRD-0A-AUDIT-01 is docs/static audit work and needs no new language/tooling.
- Rust/C++ are not warranted for these immediate tickets.

## 10) Explicit non-approvals

- no shared rail implementation
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
- no weather implementation
