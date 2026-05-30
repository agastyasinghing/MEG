# PRD-P1-WX-STAGE2-SKELETON-02: Validation Coverage Refinement

## Canonical ID

PRD-P1-WX-STAGE2-SKELETON-02

## Status / scope

Status: implemented as a narrow Stage 2 skeleton refinement and validation-coverage guard.

Scope is limited to the existing supplied-metadata-only historical-label skeleton. This document records conservative validation refinements and static guard coverage only. It is not an approval to build ingestion, provider integrations, data collection, scoring, runtime observation, execution, or any autonomous system behavior.

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
- `docs/prd/PRD-P1-WX-STAGE2-SKELETON-01_HISTORICAL_LABEL_SKELETON_IMPLEMENTATION.md`
- `meg/weather/stage2/historical_label.py`
- `tests/core/test_prd_p1_wx_stage2_skeleton_01_historical_label.py`

## Allowed refinement scope

This refinement only strengthens validation behavior and tests around already-supplied Stage 2 metadata. It keeps the skeleton pure and deterministic: callers supply metadata objects or mappings, and validators return validation results without reading files, contacting services, collecting observations, creating labels, or deriving probabilities.

Allowed changes in this ticket:

- Require nonblank `condition_id`, `token_id`, `outcome`, and `venue_rule_summary` for passing validation.
- Keep mapping builders strict for required supplied fields instead of silently defaulting them.
- Treat additional ambiguous or design-only statuses conservatively so they do not pass.
- Add static guard tests for closed value sets, fail-closed paths, mapping-builder failures, and forbidden implementation tokens.

## Unchanged closed value sets

Source-resolution status remains exactly:

- `source_resolved`
- `source_unresolved`
- `source_conflicting`
- `source_unknown`
- `requires_adjudication`

Point-in-time availability status remains exactly:

- `available_as_of`
- `unavailable_as_of`
- `ambiguous_as_of`
- `not_applicable`
- `design_only`

Label usability posture remains exactly:

- `design_only`
- `usable_after_stage_2_approval`
- `blocked_pending_source_match`
- `blocked_pending_provenance`
- `blocked_pending_adjudication`

Evidence status remains exactly:

- `source_backed`
- `reviewer_inferred`
- `missing`
- `conflicting`
- `not_applicable`

Label confidence remains exactly:

- `confirmed`
- `unclear`
- `unknown`

Validation severity remains exactly:

- `passed`
- `caution`
- `failed`
- `blocked`

No hybrid values, slash-combined values, or new enum/status values are introduced.

## Refined fail-closed / caution behavior

Validation continues to block missing resolver source identity, unresolved/conflicting/unknown/adjudication source-resolution statuses, unavailable/ambiguous point-in-time status, missing/conflicting evidence, unknown confidence, and blocked usability postures.

This refinement adds conservative handling for these previously under-covered cases:

- Missing, blank, or non-string `condition_id` blocks validation.
- Missing, blank, or non-string `token_id` blocks validation.
- Missing, blank, or non-string `outcome` blocks validation.
- Missing, blank, or non-string `venue_rule_summary` blocks validation.
- Missing, blank, or non-string resolver source identity blocks validation.
- Point-in-time `not_applicable` blocks validation.
- Point-in-time `design_only` blocks validation.
- Evidence `reviewer_inferred` blocks validation.
- Evidence `not_applicable` blocks validation.
- Label confidence `unclear` blocks validation.
- Label usability posture `design_only` blocks validation.

A passing result is available only when the supplied metadata is explicitly source-backed, confirmed, source-resolved, available as of the supplied point-in-time posture, and usable after Stage 2 approval. Any status outside that complete pass posture remains nonpassing.

## Explicit non-approval boundaries

This ticket explicitly preserves all of the following boundaries:

- no ingestion
- no provider/API connectors
- no external API calls
- no credentials/secrets/config loading
- no forecast pulls
- no historical-label data
- no fixtures/generated data
- no scoring/backtesting/runtime/trading/order placement/autonomy

It also does not approve data collection, source/provider selection, connector implementation, file loading, fixture loading, timestamp parsing libraries, model or probability outputs, paper simulation, runtime observers, position sizing, execution authority, or C++/Rust components.

## Changed files

- `meg/weather/stage2/historical_label.py`
- `tests/core/test_prd_p1_wx_stage2_skeleton_02_validation_coverage.py`
- `docs/prd/PRD-P1-WX-STAGE2-SKELETON-02_VALIDATION_COVERAGE_REFINEMENT.md`

## Validation commands

- `python -m py_compile meg/weather/stage2/historical_label.py`
- `python -m py_compile tests/core/test_prd_p1_wx_stage2_skeleton_01_historical_label.py`
- `python -m py_compile tests/core/test_prd_p1_wx_stage2_skeleton_02_validation_coverage.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_skeleton_02_validation_coverage.py`
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
- Legacy identifier audit command specified by the ticket prompt.
- Forbidden implementation-token audit command specified by the ticket prompt.
- `git diff --check`
- `git status --short`
- `git show --name-only --pretty=format: HEAD`

## Later-ticket handoff

Hold this refinement for review unless reviewers find additional validation gaps inside the same supplied-metadata-only skeleton. Any later ticket should remain narrow if it is still in skeleton coverage. Ingestion, provider connectors, external API calls, label data creation, scoring, backtesting, runtime observation, trading, order placement, and autonomy remain out of scope until separately approved by the Stage 2 gate process.
