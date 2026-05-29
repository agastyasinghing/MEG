# PRD-P1-WX-STAGE2-SKELETON-APPROVAL-01: Narrow Implementation Skeleton Approval Request

## Status and scope

PRD-P1-WX-STAGE2-SKELETON-APPROVAL-01 is a Markdown-only skeleton approval request for Weather Bot Stage 2. This is a skeleton approval request only. Skeleton implementation is not approved by this document. Implementation code is not created. Implementation has not started. Historical labels are not created. Fixtures/generated data are not created. Ingestion is not created. Provider/API connectors are not created. External API calls are not created. Forecast pulls are not created.

This ticket creates no production code, no implementation skeleton files, no data artifacts, no fixtures, and no generated outputs. Scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved. A later skeleton implementation ticket requires separate explicit human approval before any code, label structure module, validator module, schema module, test-local example, or changed production/library path may be created.

## Strategic framing

The controlling source for Weather Bot staging, evidence boundaries, and source-backed posture remains the **standalone MEG Weather Bot PRD** (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`). `PRD-P1-WX-STAGE1-CLOSEOUT-01` (`PRD-P1-WX-STAGE1-CLOSEOUT-01_STAGE_1_CLOSURE_GATES_AND_STAGE_2_READINESS_REVIEW.md`) closed Stage 1 for Stage 2 handoff only; it did not approve ingestion, scoring, runtime, execution, order placement, or autonomy.

This request follows the Stage 2 design/gate/approval/planning arc: `PRD-P1-WX-STAGE2-01`, `PRD-P1-WX-STAGE2-02`, `PRD-P1-WX-STAGE2-03`, `PRD-P1-WX-STAGE2-04`, `PRD-P1-WX-STAGE2-GATE-01`, `PRD-P1-WX-STAGE2-APPROVAL-01`, and `PRD-P1-WX-STAGE2-PLAN-01`. It asks whether a later, separately approved ticket may create a narrow non-runtime, non-ingestion, non-scoring Stage 2 historical-label skeleton for metadata structures and validators only.

## Stage ladder position

| Stage | Meaning | Posture in this skeleton approval request |
|---|---|---|
| Stage 0 | Documentation and source-backed research only. | Complete before this request. |
| Stage 1 | Static examples and manual labels. | Closed for Stage 2 handoff by `PRD-P1-WX-STAGE1-CLOSEOUT-01`; no new Stage 1 examples or data are created here. |
| Stage 2 | Source-compatible historical labels with point-in-time provenance. | Design/gate/approval/planning artifacts exist; this document requests human review for a possible later skeleton ticket only. |
| Stage 3 | Retrospective probability scoring on strict OOS splits. | Not approved and not requested here. |
| Stage 4 | Trap-filtered paper simulation with executable quote assumptions. | Not approved and not requested here. |
| Stage 5 | Human-reviewed dry run with reviewer packets and override logs. | Not approved and not requested here. |
| Stage 6 | Runtime observation only under separate approval. | Not approved and not requested here. |
| Stage 7 | Execution/trading only after separate explicit approval. | Not approved and not requested here. |

## Skeleton approval-request boundary

The user authorization for this ticket allows only this Markdown approval-request document and a Python standard-library-only static validation test under `tests/core`. This request does not create implementation code and does not create implementation skeleton files.

The approval-request boundary is deliberately narrower than `PRD-P1-WX-STAGE2-PLAN-01`: it asks whether a future ticket may be proposed for a minimal Stage 2 skeleton. The human decision requested here, if later granted outside this document, would still be limited to a future skeleton implementation ticket with its own changed-file allowlist, tests, and explicit non-approval boundaries.

## Requested future skeleton scope

This document requests permission for a future skeleton implementation ticket only. The maximum possible future skeleton scope under that later ticket would be:

- domain model skeleton for historical-label metadata;
- static schema skeleton for closed sets and required fields;
- source-resolution validator skeleton for supplied metadata only;
- point-in-time provenance validator skeleton for supplied metadata only;
- label-usability validator skeleton for supplied metadata only;
- static tests for non-approval boundaries and closed sets.

The future skeleton, if separately approved later, would not collect data, create label values, connect to providers, call external services, evaluate forecasts, score probabilities, run backtests, observe runtime markets, place orders, trade, or operate autonomously.

## Explicitly excluded future skeleton scope

The future skeleton scope requested for review explicitly excludes:

- ingestion;
- provider/API connectors;
- external API calls;
- credentials/secrets/config loading;
- forecast pulls;
- historical label data;
- JSON/YAML/CSV/Parquet fixtures or generated data;
- scoring;
- backtesting;
- paper simulation;
- runtime observation;
- trading;
- order placement;
- autonomy;
- C++/Rust runtime components.

These exclusions apply to this request and to the maximum possible future skeleton ticket that this request asks a human to consider.

## Source-document dependency map

| Source document | Dependency use in this request | Boundary preserved |
|---|---|---|
| Standalone MEG Weather Bot PRD (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`) | Controls Weather Bot stage ladder, source-defined settlement posture, and global non-approval posture. | No connector, runtime, trading, or autonomy approval is inferred. |
| `PRD-P1-WX-STAGE1-CLOSEOUT-01` | Confirms Stage 1 can hand off into Stage 2 design. | No ingestion, scoring, runtime, or execution approval is inferred. |
| `PRD-P1-WX-STAGE2-01` | Defines source-compatible historical-label design requirements. | No label data is created. |
| `PRD-P1-WX-STAGE2-02` | Defines point-in-time provenance example design. | No forecast pulls or external history lookups are created. |
| `PRD-P1-WX-STAGE2-03` | Defines source-resolution audit checklist design. | No provider/API connector is created. |
| `PRD-P1-WX-STAGE2-04` | Defines label-usability and blocking matrix design. | No scoring or readiness upgrade is inferred. |
| `PRD-P1-WX-STAGE2-GATE-01` | Defines readiness/implementation-gate review posture. | Human review remains required. |
| `PRD-P1-WX-STAGE2-APPROVAL-01` | Defines the explicit Stage 2 implementation approval request lineage. | It did not approve implementation code. |
| `PRD-P1-WX-STAGE2-PLAN-01` | Defines historical-label implementation planning and points to this narrower approval request. | Planning is not converted into implementation approval. |

## Proposed future skeleton components

If a later ticket receives separate explicit human approval, it may propose only these non-runtime skeleton components:

- a domain model skeleton that names historical-label metadata fields without creating label data;
- a static schema skeleton that enumerates closed sets and required fields without loading files or providers;
- a source-resolution validator skeleton that checks supplied metadata only;
- a point-in-time provenance validator skeleton that checks supplied metadata only;
- a label-usability validator skeleton that checks supplied metadata only;
- static tests that enforce closed sets and non-approval boundaries.

This list is a proposed future maximum, not approval to create those components in this ticket.

## Proposed future changed-file allowlist

A later skeleton implementation ticket, if separately approved by a human, should provide its own exact changed-file allowlist before edits. A conservative future allowlist could include only:

- a new Stage 2 historical-label metadata domain module under a later-approved production or library path;
- a new static schema module for closed sets and required fields under a later-approved production or library path;
- a new source-resolution validator module for supplied metadata only;
- a new point-in-time provenance validator module for supplied metadata only;
- a new label-usability validator module for supplied metadata only;
- focused tests under `tests/core` for the skeleton and non-approval boundaries.

The future allowlist must continue to exclude fixtures, generated data, provider/API connector files, ingestion jobs, runtime observers, scoring modules, backtesting modules, execution modules, trading modules, scripts, notebooks, SQL, migrations, workflow files, dependency files, and configuration/secrets files unless a separate human approval explicitly changes that boundary.

## Proposed future static-test requirements

A later skeleton implementation ticket should include static tests that verify:

- the skeleton references the standalone MEG Weather Bot PRD and all Stage 2 source documents;
- the skeleton uses only approved closed sets for Stage 2 metadata and validator outcomes;
- source-resolution, point-in-time provenance, and label-usability uncertainty fail closed;
- validators operate only on supplied metadata;
- no ingestion, provider/API connector, external API call, credential loading, config loading, forecast pull, historical-label data, fixture, generated data, scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy path appears;
- no C++/Rust runtime component appears;
- the future changed-file allowlist is enforced.

These are proposed future static-test requirements only. They do not create implementation code or label data now.

## Human approval checklist

A human reviewer should answer all checklist items before a later skeleton implementation ticket is opened:

- Is the request limited to a future Stage 2 skeleton implementation ticket only?
- Is the future maximum scope limited to metadata structures, static schema, supplied-metadata validators, and static tests?
- Are ingestion, provider/API connectors, external API calls, credentials/secrets/config loading, and forecast pulls excluded?
- Are historical labels, fixtures, generated data, JSON/YAML/CSV/Parquet artifacts, and data collection excluded?
- Are scoring, backtesting, paper simulation, runtime observation, trading, order placement, production behavior, and autonomy excluded?
- Are C++/Rust runtime components excluded?
- Are all later-ticket permissions blocked until separate explicit human approval is granted outside this document?

## Skeleton approval decision options

The human reviewer may choose one of these decision paths outside this document:

1. Hold: do not authorize a skeleton implementation ticket; continue with schema refinement or no action.
2. Revise: request targeted wording or boundary changes before any future skeleton ticket is considered.
3. Separately approve a narrow future skeleton implementation ticket: authorize only a later ticket with its own changed-file allowlist, static tests, and explicit non-approval boundaries.

This document itself does not choose option 3 and does not approve skeleton implementation.

## Explicit non-approval boundaries

This skeleton approval request does not approve implementation code now.

This skeleton approval request does not approve historical label implementation.

This skeleton approval request does not approve data ingestion.

This skeleton approval request does not approve provider integration.

This skeleton approval request does not approve connectors.

This skeleton approval request does not approve external API calls.

This skeleton approval request does not approve credentials, secrets, config loading, or forecast pulls.

This skeleton approval request does not approve historical-label data, fixtures/generated data, JSON/YAML/CSV/Parquet artifacts, or generated outputs.

This skeleton approval request does not approve model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, production behavior, C++/Rust runtime components, or autonomy.

A later skeleton implementation ticket requires separate explicit human approval.

## Closed Stage 2 skeleton approval-request vocabulary

No other actual values are allowed for these machine-checkable fields. Hybrid, custom, and slash values are forbidden as actual values. If a condition is partially supported, the reviewer must choose the single most conservative exact value and put nuance in notes or prose.

### skeleton approval stage

- `stage_2_skeleton_approval_request`

### request status

- `request_prepared`
- `skeleton_not_approved`
- `human_review_required`
- `blocked_pending_fix`
- `unclear`

### requested skeleton scope

- `domain_model_skeleton`
- `static_schema_skeleton`
- `source_resolution_validator_skeleton`
- `provenance_validator_skeleton`
- `label_usability_validator_skeleton`
- `static_test_skeleton`
- `no_ingestion_no_runtime_no_scoring`

### approval boundary status

- `not_approved`
- `separate_human_approval_required`
- `explicitly_out_of_scope`
- `blocked`

### future skeleton permission

- `may_request_skeleton_ticket`
- `must_not_create_code_now`
- `must_not_create_ingestion`
- `must_not_create_runtime`
- `must_not_create_scoring`
- `must_not_create_trading`
- `blocked_until_human_decision`

### non-approval category

- `implementation_code_now`
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

## Forbidden Stage 2 skeleton approval-request values

The following examples may appear only as forbidden examples in prose, not as actual machine-checkable field values:

- `request_prepared/skeleton_not_approved`
- `not_approved/separate_human_approval_required`
- `domain_model_skeleton/static_schema_skeleton`
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
- `skeleton_ready`
- `skeleton_approved`

## Machine-checkable Stage 2 skeleton approval-request assignments

- skeleton approval stage: stage_2_skeleton_approval_request
- request status: request_prepared
- request status: skeleton_not_approved
- request status: human_review_required
- request status: blocked_pending_fix
- request status: unclear
- requested skeleton scope: domain_model_skeleton
- requested skeleton scope: static_schema_skeleton
- requested skeleton scope: source_resolution_validator_skeleton
- requested skeleton scope: provenance_validator_skeleton
- requested skeleton scope: label_usability_validator_skeleton
- requested skeleton scope: static_test_skeleton
- requested skeleton scope: no_ingestion_no_runtime_no_scoring
- approval boundary status: not_approved
- approval boundary status: separate_human_approval_required
- approval boundary status: explicitly_out_of_scope
- approval boundary status: blocked
- future skeleton permission: may_request_skeleton_ticket
- future skeleton permission: must_not_create_code_now
- future skeleton permission: must_not_create_ingestion
- future skeleton permission: must_not_create_runtime
- future skeleton permission: must_not_create_scoring
- future skeleton permission: must_not_create_trading
- future skeleton permission: blocked_until_human_decision
- non-approval category: implementation_code_now
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

## Skeleton approval-request matrix

| Review area | Request status | Requested skeleton scope | Approval boundary status | Future skeleton permission | Evidence status | Label confidence | Notes |
|---|---|---|---|---|---|---|---|
| Approval-request document | request_prepared | static_test_skeleton | separate_human_approval_required | may_request_skeleton_ticket | source_backed | confirmed | Prepared from Stage 2 design/gate/planning sources only. |
| Human decision | human_review_required | no_ingestion_no_runtime_no_scoring | not_approved | blocked_until_human_decision | reviewer_inferred | unclear | A human decision is still required before any future skeleton ticket. |
| Domain metadata skeleton | skeleton_not_approved | domain_model_skeleton | separate_human_approval_required | must_not_create_code_now | source_backed | confirmed | Future-only maximum scope; no code now. |
| Static schema skeleton | skeleton_not_approved | static_schema_skeleton | separate_human_approval_required | must_not_create_code_now | source_backed | confirmed | Future-only maximum scope; no code now. |
| Source-resolution validator skeleton | skeleton_not_approved | source_resolution_validator_skeleton | separate_human_approval_required | must_not_create_code_now | source_backed | confirmed | Supplied metadata only if later approved. |
| Provenance validator skeleton | skeleton_not_approved | provenance_validator_skeleton | separate_human_approval_required | must_not_create_code_now | source_backed | confirmed | Supplied metadata only if later approved. |
| Label-usability validator skeleton | skeleton_not_approved | label_usability_validator_skeleton | separate_human_approval_required | must_not_create_code_now | source_backed | confirmed | Supplied metadata only if later approved. |
| Ingestion/runtime/scoring | skeleton_not_approved | no_ingestion_no_runtime_no_scoring | explicitly_out_of_scope | must_not_create_ingestion | not_applicable | confirmed | Ingestion, runtime, and scoring remain out of scope. |
| Trading boundary | skeleton_not_approved | no_ingestion_no_runtime_no_scoring | explicitly_out_of_scope | must_not_create_trading | not_applicable | confirmed | Trading, order placement, and autonomy remain out of scope. |
| Unclear future wording | blocked_pending_fix | static_test_skeleton | blocked | blocked_until_human_decision | missing | unknown | Ambiguity must be resolved before a future skeleton ticket. |

## If approved later, next-ticket boundaries

If a human reviewer later grants separate approval, the next ticket may only be a narrow Stage 2 skeleton implementation ticket. It must repeat this document's non-approval boundaries, include an exact changed-file allowlist, create no data artifacts, and include static tests that prevent expansion into ingestion, provider/API connectors, external API calls, forecast pulls, scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.

If separate approval is not granted, the next step should be hold or targeted schema refinement. No skeleton implementation work should begin from this document alone.

## Relationship to future implementation

This request is implementation-adjacent only as an approval question. It does not start implementation, does not create implementation code, and does not create implementation skeleton files.

A future skeleton implementation ticket, if separately approved, would still be limited to metadata structures, static schema, supplied-metadata validators, and static tests. Any later move beyond a skeleton would require another explicit human approval and another ticket.

## Relationship to future Stage 3 scoring

Stage 3 scoring remains outside this request. This document does not approve retrospective probability scoring, model scoring, OOS split evaluation, calibration analysis, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.

A later Stage 3 request would require its own source-specific PRD, human review, acceptance criteria, and static tests. Nothing in this approval request creates Stage 3 readiness.

## Later-ticket handoff

If a human reviewer does not grant separate approval, the handoff is hold or targeted Stage 2 schema refinement. If a human reviewer separately grants approval, the handoff is a narrow Stage 2 skeleton implementation ticket only.

The later ticket must not recommend or include ingestion, provider/API connectors, external API calls, forecast pulls, scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.

## Acceptance criteria

- This document includes canonical ID `PRD-P1-WX-STAGE2-SKELETON-APPROVAL-01`.
- This document references the standalone MEG Weather Bot PRD, `PRD-P1-WX-STAGE1-CLOSEOUT-01`, `PRD-P1-WX-STAGE2-01`, `PRD-P1-WX-STAGE2-02`, `PRD-P1-WX-STAGE2-03`, `PRD-P1-WX-STAGE2-04`, `PRD-P1-WX-STAGE2-GATE-01`, `PRD-P1-WX-STAGE2-APPROVAL-01`, and `PRD-P1-WX-STAGE2-PLAN-01`.
- This document clearly states that this is a skeleton approval request only.
- This document clearly states that skeleton implementation is not approved by this document.
- This document clearly states that implementation code is not created.
- This document clearly states that implementation has not started.
- This document clearly states that historical labels are not created.
- This document clearly states that fixtures/generated data are not created.
- This document clearly states that ingestion is not created.
- This document clearly states that provider/API connectors are not created.
- This document clearly states that external API calls are not created.
- This document clearly states that forecast pulls are not created.
- This document clearly states that scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved.
- This document clearly states that a later skeleton implementation ticket requires separate explicit human approval.
- This document includes proposed future skeleton components, proposed future changed-file allowlist, and proposed future static-test requirements.
- A standard-library-only static test enforces section-scoped closed values for the machine-checkable assignment section.
