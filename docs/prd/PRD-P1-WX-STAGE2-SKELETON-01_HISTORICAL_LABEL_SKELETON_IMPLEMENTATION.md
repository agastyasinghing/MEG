# PRD-P1-WX-STAGE2-SKELETON-01 Historical-Label Skeleton Implementation

## Canonical ID

PRD-P1-WX-STAGE2-SKELETON-01

## Status and scope

Status: implementation skeleton complete for review.

Scope: narrow Stage 2 supplied-metadata skeleton only. The implemented Python module defines source-compatible weather-label metadata structures, closed Stage 2 values, and pure fail-closed validation helpers for explicitly supplied in-memory metadata.

This skeleton preserves the Stage 2 thesis: the target is not P(weather variable crosses threshold). The target is P(the venue-defined source/station/window/threshold/revision/classification rule resolves Yes).

## Source documents read

- `docs/meta/MEG_CURRENT_STATE.md`
- `docs/meta/MEG_CHAT_HANDOFF.md`
- `docs/meta/MEG_WORKFLOW_PLAYBOOK.md`
- `docs/meta/MEG_TICKET_PROMPT_TEMPLATE.md`
- `docs/meta/MEG_PHASE_HISTORY_SUMMARY.md`
- `docs/meta/MEG_STRATEGIC_IDEA_REGISTRY.md`
- `docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`
- `docs/prd/PRD-P1-WX-STAGE2-01_SOURCE_COMPATIBLE_HISTORICAL_LABEL_DESIGN.md`
- `docs/prd/PRD-P1-WX-STAGE2-02_POINT_IN_TIME_PROVENANCE_EXAMPLE_DESIGN.md`
- `docs/prd/PRD-P1-WX-STAGE2-03_SOURCE_RESOLUTION_AUDIT_CHECKLIST_DESIGN.md`
- `docs/prd/PRD-P1-WX-STAGE2-04_LABEL_USABILITY_BLOCKING_MATRIX_DESIGN.md`
- `docs/prd/PRD-P1-WX-STAGE2-GATE-01_STAGE_2_READINESS_IMPLEMENTATION_GATE_REVIEW.md`
- `docs/prd/PRD-P1-WX-STAGE2-APPROVAL-01_EXPLICIT_IMPLEMENTATION_APPROVAL_REQUEST.md`
- `docs/prd/PRD-P1-WX-STAGE2-PLAN-01_HISTORICAL_LABEL_IMPLEMENTATION_PLANNING.md`
- `docs/prd/PRD-P1-WX-STAGE2-SKELETON-APPROVAL-01_NARROW_IMPLEMENTATION_SKELETON_APPROVAL_REQUEST.md`
- Existing package layout under `meg/` and existing `tests/core` conventions.

## Allowed implementation scope

Allowed scope for this ticket:

- Python standard-library-only dataclasses and enums.
- Pure functions over explicitly supplied in-memory metadata.
- Closed Stage 2 value sets.
- Fail-closed validation for missing, unclear, conflicting, or blocked metadata.
- A static PRD guard document and focused tests.

The selected package path is `meg/weather/stage2/` because the repository already has a top-level `meg/` package and no existing non-runtime Weather domain package. A narrow `weather/stage2` package keeps this skeleton separate from runtime, connector, execution, and research-output paths.

## Closed value sets

### Source-resolution status

- `source_resolved`
- `source_unresolved`
- `source_conflicting`
- `source_unknown`
- `requires_adjudication`

### Point-in-time availability status

- `available_as_of`
- `unavailable_as_of`
- `ambiguous_as_of`
- `not_applicable`
- `design_only`

### Label usability posture

- `design_only`
- `usable_after_stage_2_approval`
- `blocked_pending_source_match`
- `blocked_pending_provenance`
- `blocked_pending_adjudication`

### Evidence status

- `source_backed`
- `reviewer_inferred`
- `missing`
- `conflicting`
- `not_applicable`

### Label confidence

- `confirmed`
- `unclear`
- `unknown`

### Validation severity

- `passed`
- `caution`
- `failed`
- `blocked`

## Fail-closed behavior

The skeleton fails closed when supplied metadata has any of the following conditions:

- resolver source identity is missing;
- source-resolution status is `source_unresolved`, `source_conflicting`, `source_unknown`, or `requires_adjudication`;
- point-in-time availability status is `unavailable_as_of` or `ambiguous_as_of`;
- evidence status is `missing` or `conflicting`;
- label confidence is `unknown`;
- label usability posture is `blocked_pending_source_match`, `blocked_pending_provenance`, or `blocked_pending_adjudication`.

The skeleton may return `passed` only when supplied metadata is explicitly source-backed, confirmed, and not blocked. `usable_after_stage_2_approval` means only that supplied metadata passes these non-runtime validation checks. It does not mean production-ready, runtime-ready, scoring-ready, or trading-ready.

## Explicit non-approval boundaries

This ticket explicitly does not approve or add:

- no ingestion
- no provider/API connectors
- no external API calls
- no credentials/secrets/config loading
- no forecast pulls
- no historical-label data
- no fixtures/generated data
- no scoring/backtesting/runtime/trading/order placement/autonomy

It also does not approve position sizing, provider credentials, live market usage, production monitoring, or C++/Rust runtime components.

## Changed files

- `meg/weather/__init__.py`
- `meg/weather/stage2/__init__.py`
- `meg/weather/stage2/historical_label.py`
- `tests/core/test_prd_p1_wx_stage2_skeleton_01_historical_label.py`
- `docs/prd/PRD-P1-WX-STAGE2-SKELETON-01_HISTORICAL_LABEL_SKELETON_IMPLEMENTATION.md`

## Validation commands

- `python -m py_compile meg/weather/stage2/historical_label.py`
- `python -m py_compile tests/core/test_prd_p1_wx_stage2_skeleton_01_historical_label.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_skeleton_01_historical_label.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_skeleton_approval_01_request.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_plan_01_historical_label_planning.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_approval_01_request.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_gate_01_readiness_review.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_04_label_usability_matrix.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_03_source_resolution_audit.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_02_provenance_example_design.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_01_historical_label_design.py`
- `python -m pytest -q tests/core/test_static_canonical_ids.py`
- `python -m pytest -q tests/core`
- `git diff --check`
- `git status --short`
- `git show --name-only --pretty=format: HEAD`

## Later-ticket handoff

A later ticket may refine Stage 2 skeleton coverage, reviewer-note expectations, or additional fail-closed edge cases while preserving supplied-metadata-only behavior. Any later ticket must remain separately approved and must not infer approval for ingestion, providers, service calls, forecast pulls, historical-label data, fixtures/generated data, scoring, retrospective evaluation, runtime observation, trading, order placement, or autonomy.
