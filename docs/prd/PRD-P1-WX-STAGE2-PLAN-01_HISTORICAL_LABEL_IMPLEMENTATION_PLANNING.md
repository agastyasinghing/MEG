# PRD-P1-WX-STAGE2-PLAN-01: Historical-Label Implementation Planning

## Status and scope

PRD-P1-WX-STAGE2-PLAN-01 is a Markdown-only implementation-planning document for Weather Bot Stage 2. This is implementation planning only. Implementation code is not created. Implementation has not started. Historical labels are not created. Fixtures/generated data are not created. Ingestion is not created. Provider/API connectors are not created. External API calls are not created. Forecast pulls are not created.

This ticket creates no production code and no data artifacts. Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved. A later implementation ticket requires separate explicit approval before any code, label data, provider/API connector, external API call, forecast pull, scoring, evaluation run, runtime observation, paper simulation, trading, order placement, or autonomous behavior can be considered.

## Strategic framing

The controlling source for Weather Bot staging, evidence boundaries, and source-backed posture remains the **standalone MEG Weather Bot PRD** (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`). `PRD-P1-WX-STAGE1-CLOSEOUT-01` (`PRD-P1-WX-STAGE1-CLOSEOUT-01_STAGE_1_CLOSURE_GATES_AND_STAGE_2_READINESS_REVIEW.md`) closed Stage 1 for Stage 2 handoff only; it did not approve ingestion, scoring, runtime, execution, or autonomy.

This planning document follows the Stage 2 design/gate/approval arc and converts already-approved planning posture into a future implementation-plan outline only. It preserves the venue-defined settlement object, source-resolution discipline, point-in-time provenance requirements, and label-usability gates without creating implementation code or label artifacts now.

## Stage ladder position

| Stage | Meaning | Posture in this planning document |
|---|---|---|
| Stage 0 | Documentation and source-backed research only. | Complete before this planning document. |
| Stage 1 | Static examples and manual labels. | Closed for Stage 2 handoff by `PRD-P1-WX-STAGE1-CLOSEOUT-01`; no new Stage 1 examples or data are created here. |
| Stage 2 | Source-compatible historical labels with point-in-time provenance. | Design/gate/approval artifacts exist; this document plans a later implementation path only. |
| Stage 3 | Retrospective probability scoring on strict OOS splits. | Not approved and not planned for implementation here. |
| Stage 4 | Trap-filtered paper simulation with executable quote assumptions. | Not approved and not planned for implementation here. |
| Stage 5 | Human-reviewed dry run with reviewer packets and override logs. | Not approved and not planned for implementation here. |
| Stage 6 | Runtime observation only under separate approval. | Not approved and not planned for implementation here. |
| Stage 7 | Execution/trading only after separate explicit approval. | Not approved and not planned for implementation here. |

## Planning authorization boundary

The user has separately approved proceeding to this Stage 2 implementation-planning ticket only. That authorization allows this Markdown planning PRD and a Python standard-library-only static validation test under `tests/core`.

The authorization does not approve implementation code, historical-label data, JSON/YAML/CSV/Parquet fixtures, generated data, ingestion, provider integration, connectors, external API calls, credentials or secret configuration, forecast pulls, scoring, backtesting, runtime observation, paper simulation, trading, order placement, production behavior, C++/Rust runtime components, or autonomy.

## Future implementation-planning goal

The goal is to define how a future, separately approved Stage 2 implementation ticket could translate the Stage 2 source documents into a narrow source-compatible historical-label skeleton. The plan is intentionally limited to proposed future boundaries, proposed future files, proposed future static tests, and blocked conditions.

A later implementation ticket would still need its own explicit approval, acceptance criteria, changed-file allowlist, and static tests before any code or label data work begins.

## Existing Stage 2 source documents

The future planning outline is source-backed by the following existing documents:

- `PRD-P1-WX-STAGE2-01` (`PRD-P1-WX-STAGE2-01_SOURCE_COMPATIBLE_HISTORICAL_LABEL_DESIGN.md`) for source-compatible historical-label design.
- `PRD-P1-WX-STAGE2-02` (`PRD-P1-WX-STAGE2-02_POINT_IN_TIME_PROVENANCE_EXAMPLE_DESIGN.md`) for point-in-time provenance example design.
- `PRD-P1-WX-STAGE2-03` (`PRD-P1-WX-STAGE2-03_SOURCE_RESOLUTION_AUDIT_CHECKLIST_DESIGN.md`) for source-resolution audit checklist design.
- `PRD-P1-WX-STAGE2-04` (`PRD-P1-WX-STAGE2-04_LABEL_USABILITY_BLOCKING_MATRIX_DESIGN.md`) for label-usability/blocking matrix design.
- `PRD-P1-WX-STAGE2-GATE-01` (`PRD-P1-WX-STAGE2-GATE-01_STAGE_2_READINESS_IMPLEMENTATION_GATE_REVIEW.md`) for readiness-gate posture.
- `PRD-P1-WX-STAGE2-APPROVAL-01` (`PRD-P1-WX-STAGE2-APPROVAL-01_EXPLICIT_IMPLEMENTATION_APPROVAL_REQUEST.md`) for the explicit request that allowed this planning-only ticket.

## Planned future component boundaries

A later implementation ticket could propose a source-compatible historical-label skeleton only if it remains inside Stage 2 and receives separate explicit approval. The planned future component boundary is:

- domain model planning for label metadata fields that mirror Stage2-01 design without adding provider calls;
- static schema planning for shape checks that can run on in-memory examples supplied by tests in the later ticket, if such examples are explicitly approved then;
- source-resolution validator planning for deterministic checks against provided metadata only;
- provenance validator planning for point-in-time fields supplied by an approved caller only;
- label-usability validator planning for blocking states and conservative handoff categories;
- static test planning for closed value sets, required fields, and non-approval boundaries;
- fixture strategy planning that defaults to no fixture files unless a later approval explicitly permits them.

No boundary in this document authorizes ingestion, provider/API connectors, external API calls, forecast pulls, historical-label creation, scoring, backtesting, runtime observation, trading, order placement, or autonomy.

## Historical-label design-to-code mapping plan

A future implementation ticket could map `PRD-P1-WX-STAGE2-01` to code by first defining a narrow schema contract for historical-label metadata. That later mapping should be reviewed field by field against the source-compatible design before any code is written.

The future mapping should preserve the label object as a source-resolution and provenance record, not as a trade signal. It should plan fields for settlement source identity, event window, outcome representation, data cutoff, reviewer confidence, and blocking reasons. It should also explicitly avoid any probability score, strategy signal, runtime observer, or order path.

This document writes no schema module, no class, no parser, no fixture, and no label row.

## Source-resolution validation planning

A future implementation ticket could map `PRD-P1-WX-STAGE2-03` to validation by checking that each approved input record identifies its settlement source, resolution rule, fallback posture, and unresolved-source status. The later validator, if approved, should reject ambiguous or unsupported source-resolution states rather than infer them silently.

This document does not write validators, does not query providers, does not call external APIs, and does not collect resolution-source data.

## Point-in-time provenance validation planning

A future implementation ticket could map `PRD-P1-WX-STAGE2-02` to validation by checking that each approved input record carries point-in-time fields such as observation cutoff, source publication posture, reviewer timestamp, and provenance notes. The later validator, if approved, should block any record whose source timing cannot be reconstructed from supplied metadata.

This document does not write provenance validators, does not pull forecasts, does not load external history, and does not create historical labels.

## Label-usability validation planning

A future implementation ticket could map `PRD-P1-WX-STAGE2-04` to validation by preserving conservative blocking outcomes. The later validator, if approved, should distinguish usable, blocked, unclear, conflicting, and not-applicable evidence states according to the approved Stage 2 matrix rather than convert uncertainty into readiness.

This document does not implement label-usability code, scoring, backtesting, runtime observation, trading, order placement, or autonomy.

## Planned changed-file allowlist for a later implementation ticket

A later implementation ticket may propose a planned changed-file allowlist, clearly marked as future only. A conservative proposed allowlist could include:

- a new Stage 2 historical-label schema module under a later-approved production or library path;
- a new Stage 2 validation module for source-resolution metadata only;
- a new Stage 2 validation module for point-in-time provenance metadata only;
- a new Stage 2 validation module for label-usability/blocking metadata only;
- focused tests under `tests/core` or another later-approved test path;
- no fixture files unless separately and explicitly approved in that later ticket.

This proposed future allowlist is not approval to create those files now. It is not approval for ingestion, provider integration, connectors, external API calls, forecast pulls, historical-label data, generated artifacts, scoring, backtesting, runtime observation, trading, order placement, or autonomy.

## Planned static-test requirements for a later implementation ticket

A later implementation ticket should include static tests that verify:

- the new implementation references the Stage 2 source documents;
- the implementation uses closed value sets from the approved Stage 2 design;
- ambiguous source-resolution, provenance, and label-usability states fail closed;
- no provider/API connector, external API call, credential loading, forecast pull, ingestion path, scoring path, backtesting path, runtime observer, trading path, order placement path, or autonomous execution path appears;
- no generated data or historical-label fixture is added unless separately approved;
- any future examples remain test-local and non-operational if such examples are explicitly approved later.

These are proposed future static-test requirements only. They do not create implementation code or label data now.

## Explicit non-approval boundaries

This implementation-planning ticket does not approve implementation code.

This implementation-planning ticket does not approve historical label implementation.

This implementation-planning ticket does not approve data ingestion.

This implementation-planning ticket does not approve provider integration.

This implementation-planning ticket does not approve connectors.

This implementation-planning ticket does not approve external API calls.

This implementation-planning ticket does not approve credentials, secrets, config loading, or forecast pulls.

This implementation-planning ticket does not approve historical-label data, fixtures/generated data, JSON/YAML/CSV/Parquet artifacts, or generated outputs.

This implementation-planning ticket does not approve model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, production behavior, C++/Rust runtime components, or autonomy.

A later implementation ticket requires separate explicit approval.

## Closed Stage 2 implementation-planning vocabulary

No other actual values are allowed for these machine-checkable fields. Hybrid, custom, and slash values are forbidden as actual values. If a condition is partially supported, the reviewer must choose the single most conservative exact value and put nuance in notes or prose.

### planning stage

- `stage_2_historical_label_implementation_planning`

### planning status

- `planning_only`
- `implementation_not_started`
- `human_approval_limited_to_planning`
- `blocked_pending_fix`
- `unclear`

### planned future scope

- `historical_label_schema_mapping`
- `source_resolution_validation`
- `point_in_time_provenance_validation`
- `label_usability_validation`
- `static_test_planning`
- `changed_file_allowlist_planning`
- `no_ingestion_no_runtime_no_scoring`

### implementation boundary status

- `not_implemented`
- `separate_approval_required`
- `explicitly_out_of_scope`
- `blocked`

### future component category

- `domain_model_planning`
- `static_schema_planning`
- `source_resolution_validator_planning`
- `provenance_validator_planning`
- `label_usability_validator_planning`
- `static_test_planning`
- `fixture_strategy_planning`
- `other_unclear`

### non-approval category

- `implementation_code`
- `ingestion`
- `provider_integration`
- `connectors`
- `external_api_calls`
- `credentials_secrets_config`
- `forecast_pulls`
- `historical_label_data`
- `fixtures_or_generated_data`
- `model_scoring`
- `probability_scoring`
- `backtesting`
- `paper_simulation`
- `runtime_observation`
- `trading_order_autonomy`
- `production_behavior`
- `cplusplus_rust_runtime`
- `other_unclear`

### evidence status

- `source_backed`
- `reviewer_inferred`
- `missing`
- `conflicting`
- `not_applicable`

### label confidence

- `confirmed`
- `unclear`
- `unknown`

## Forbidden Stage 2 implementation-planning values

The following examples may appear only as forbidden examples in prose, not as actual machine-checkable field values:

- `planning_only/implementation_not_started`
- `not_implemented/separate_approval_required`
- `historical_label_schema_mapping/source_resolution_validation`
- `source_backed/reviewer_inferred`
- `confirmed/unclear`
- `partial`
- `mixed`
- `likely_confirmed`
- `maybe`
- `approved`
- `configured`
- `available`
- `trade_ready`
- `auto_execute`
- `autonomous`
- `live`
- `production`
- `provider_ready`
- `model_ready`
- `backtest_ready`
- `ready_for_ingestion`
- `ready_for_scoring`
- `ready_for_runtime`
- `ready_for_trading`
- `implementation_ready`
- `ingestion_ready`
- `scoring_ready`
- `simulation_ready`
- `runtime_ready`
- `trading_ready`
- `approved_for_implementation`
- `approved_for_ingestion`
- `approved_for_runtime`
- `approved_for_scoring`
- `approved_for_trading`

## Machine-checkable Stage 2 implementation-planning assignments

- planning stage: stage_2_historical_label_implementation_planning
- planning status: planning_only
- planning status: implementation_not_started
- planning status: human_approval_limited_to_planning
- planning status: blocked_pending_fix
- planning status: unclear
- planned future scope: historical_label_schema_mapping
- planned future scope: source_resolution_validation
- planned future scope: point_in_time_provenance_validation
- planned future scope: label_usability_validation
- planned future scope: static_test_planning
- planned future scope: changed_file_allowlist_planning
- planned future scope: no_ingestion_no_runtime_no_scoring
- implementation boundary status: not_implemented
- implementation boundary status: separate_approval_required
- implementation boundary status: explicitly_out_of_scope
- implementation boundary status: blocked
- future component category: domain_model_planning
- future component category: static_schema_planning
- future component category: source_resolution_validator_planning
- future component category: provenance_validator_planning
- future component category: label_usability_validator_planning
- future component category: static_test_planning
- future component category: fixture_strategy_planning
- future component category: other_unclear
- non-approval category: implementation_code
- non-approval category: ingestion
- non-approval category: provider_integration
- non-approval category: connectors
- non-approval category: external_api_calls
- non-approval category: credentials_secrets_config
- non-approval category: forecast_pulls
- non-approval category: historical_label_data
- non-approval category: fixtures_or_generated_data
- non-approval category: model_scoring
- non-approval category: probability_scoring
- non-approval category: backtesting
- non-approval category: paper_simulation
- non-approval category: runtime_observation
- non-approval category: trading_order_autonomy
- non-approval category: production_behavior
- non-approval category: cplusplus_rust_runtime
- non-approval category: other_unclear
- evidence status: source_backed
- evidence status: reviewer_inferred
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown

## Planning matrix

| Planning area | Planning status | Planned future scope | Implementation boundary status | Evidence status | Label confidence | Notes |
|---|---|---|---|---|---|---|
| Stage2-01 design mapping | planning_only | historical_label_schema_mapping | separate_approval_required | source_backed | confirmed | Future schema mapping only; no code now. |
| Stage2-03 source-resolution checks | planning_only | source_resolution_validation | separate_approval_required | source_backed | confirmed | Future validation planning only; no provider calls. |
| Stage2-02 point-in-time provenance | planning_only | point_in_time_provenance_validation | separate_approval_required | source_backed | confirmed | Future validation planning only; no forecast pulls. |
| Stage2-04 label-usability checks | planning_only | label_usability_validation | separate_approval_required | source_backed | confirmed | Future blocking validation planning only; no scoring. |
| Static-test posture | planning_only | static_test_planning | separate_approval_required | reviewer_inferred | confirmed | Later ticket should fail closed on forbidden behavior. |
| Changed-file allowlist | planning_only | changed_file_allowlist_planning | separate_approval_required | reviewer_inferred | confirmed | Later ticket must enumerate any files before edits. |
| Ingestion/runtime/scoring | implementation_not_started | no_ingestion_no_runtime_no_scoring | explicitly_out_of_scope | not_applicable | confirmed | Remains blocked unless separately approved. |
| Unclear future scope | blocked_pending_fix | static_test_planning | blocked | missing | unknown | Ambiguity must be resolved before implementation. |

## Later-ticket handoff

If this planning PR is accepted, the safest later-ticket handoff is either a narrow Stage 2 implementation skeleton approval request or a targeted schema refinement. The later ticket must repeat that separate explicit approval is required and must not broaden into ingestion, provider/API connectors, external API calls, forecast pulls, scoring, backtesting, runtime observation, trading, order placement, or autonomy.

The later ticket should first decide whether the Stage 2 source documents are sufficiently precise to authorize a skeleton implementation. If not, it should request targeted schema refinement instead of code.

## Acceptance criteria

- This document includes canonical ID `PRD-P1-WX-STAGE2-PLAN-01`.
- This document references the standalone MEG Weather Bot PRD, `PRD-P1-WX-STAGE1-CLOSEOUT-01`, `PRD-P1-WX-STAGE2-01`, `PRD-P1-WX-STAGE2-02`, `PRD-P1-WX-STAGE2-03`, `PRD-P1-WX-STAGE2-04`, `PRD-P1-WX-STAGE2-GATE-01`, and `PRD-P1-WX-STAGE2-APPROVAL-01`.
- This document clearly states that this is implementation planning only.
- This document clearly states that implementation code is not created.
- This document clearly states that implementation has not started.
- This document clearly states that historical labels are not created.
- This document clearly states that fixtures/generated data are not created.
- This document clearly states that ingestion is not created.
- This document clearly states that provider/API connectors are not created.
- This document clearly states that external API calls are not created.
- This document clearly states that forecast pulls are not created.
- This document clearly states that scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved.
- This document clearly states that a later implementation ticket requires separate explicit approval.
- A standard-library-only static test enforces section-scoped closed values for the machine-checkable assignment section.
