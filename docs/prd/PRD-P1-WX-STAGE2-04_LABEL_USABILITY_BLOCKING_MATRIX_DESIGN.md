# PRD-P1-WX-STAGE2-04: Label-Usability / Blocking Matrix Design

## 1. Status and scope

`PRD-P1-WX-STAGE2-04` is a **Stage 2 label-usability/blocking matrix design** document only. It follows `PRD-P1-WX-STAGE2-01`, `PRD-P1-WX-STAGE2-02`, and `PRD-P1-WX-STAGE2-03` by defining how future source-resolution/provenance blockers map to conservative label usability posture decisions.

This document defines a Markdown-only label-usability/blocking matrix design only. It does **not** create actual historical labels, does **not** create JSON/YAML/CSV/Parquet fixtures, and does **not** approve provider integration, connectors, data ingestion, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.

It also does **not** approve provider credentials, external API calls, config loading, secret reading, historical label implementation, production behavior, profitability claims, C++/Rust runtime components, or any implementation behavior. The only implementation-like companion artifact is a Python standard-library static documentation test under `tests/core/`.

## 2. Strategic framing

The controlling source for Weather Bot staging, evidence gates, and non-approval posture is the **standalone MEG Weather Bot PRD** (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`). `PRD-P1-WX-STAGE1-CLOSEOUT-01` confirms that Stage 1 static/manual-label artifacts can hand off into Stage 2 design work without approving ingestion, scoring, runtime, or execution. `PRD-P1-WX-STAGE2-01` defines the source-compatible historical-label design contract. `PRD-P1-WX-STAGE2-02` defines representative point-in-time provenance example designs. `PRD-P1-WX-STAGE2-03` defines the source-resolution audit checklist design.

Weather Bot is not a generic weather API wrapper and is not a trading bot. It models prediction-market weather contracts as **source-defined settlement objects**. The target is not `P(weather variable crosses threshold)`. The target is:

`P(the venue-defined source/station/window/threshold/revision/classification rule resolves Yes)`

The label-usability/blocking matrix protects future labels from premature usability claims. Blocker mapping must preserve the source-defined settlement object: the reviewer must decide whether the future label can remain design-only, can later be considered usable after a separately approved Stage 2 context, or must be blocked pending source match, provenance, or adjudication. This document gives a Markdown-only design matrix, not implementation.

## 3. Stage ladder position

The standalone MEG Weather Bot PRD defines the Weather Bot stage ladder as follows:

| Stage | Scope | Status in this ticket |
| --- | --- | --- |
| Stage 0 | Documentation and source-backed research only. | Completed before this ticket. |
| Stage 1 | Static examples and manual labels. | Closed by `PRD-P1-WX-STAGE1-CLOSEOUT-01`. |
| Stage 2 | Source-compatible historical labels with point-in-time provenance. | **This ticket is Stage 2 design only.** |
| Stage 3 | Retrospective probability scoring on strict OOS splits. | Unapproved. |
| Stage 4 | Trap-filtered paper simulation with executable quotes, fees, spreads, and depth assumptions. | Unapproved. |
| Stage 5 | Human-reviewed dry run with reviewer packets and override logs. | Unapproved. |
| Stage 6 | Runtime observation only under separate approval. | Unapproved. |
| Stage 7 | Execution/trading only after separate explicit approval. | Unapproved. |

Historical-label implementation, Stage 3 scoring, Stage 4 paper simulation, Stage 5 dry run, Stage 6 runtime observation, and Stage 7 execution/trading remain unapproved.

## 4. Matrix purpose

The label-usability/blocking matrix is a reviewer-facing design artifact for future source-compatible historical labels. It maps blocker sources and blocker severity to label usability posture decisions so future labels fail closed when source matching, point-in-time provenance, station/source selection, publication timing, finality layer, source conflict, trap annotation, adjudication, or no-lookahead controls are missing or unresolved.

The matrix is not data ingestion, provider integration, connector implementation, scoring, probability modeling, backtesting, runtime, paper simulation, or trading work. It creates no labels and no fixtures. Its purpose is to make future reviewers choose one conservative exact posture rather than treating partial evidence as settlement truth.

## 5. Closed Stage 2 label-usability matrix vocabulary

No other actual values are allowed for the machine-checkable fields below. Hybrid values, custom values, slash-combined values, and implementation-readiness terms are forbidden as actual values. If a condition is nuanced, mixed, or partially supported, the single most conservative exact field value must be selected and the nuance must be written in reviewer notes or prose fields.

### label-usability matrix stage

Allowed values:

- `stage_2_label_usability_blocking_matrix_design`

### blocker source

Allowed values:

- `source_resolution`
- `point_in_time_provenance`
- `station_source_selection`
- `publication_timestamp`
- `observation_availability`
- `archive_finality_layer`
- `revision_handling`
- `classification_authority`
- `source_conflict`
- `trap_annotation`
- `reviewer_adjudication`
- `no_lookahead_control`
- `other_unclear`

### blocker severity

Allowed values:

- `none`
- `caution`
- `blocking`
- `unknown`

### label usability posture

Allowed values from `PRD-P1-WX-STAGE2-01`:

- `design_only`
- `usable_after_stage_2_approval`
- `blocked_pending_source_match`
- `blocked_pending_provenance`
- `blocked_pending_adjudication`

### matrix decision

Allowed values:

- `allow_design_only`
- `allow_after_stage_2_approval`
- `block_source_match`
- `block_provenance`
- `block_adjudication`
- `require_more_evidence`
- `unclear`

### escalation requirement

Allowed values:

- `none_required`
- `reviewer_note_required`
- `adjudication_required`
- `source_evidence_required`
- `provenance_evidence_required`
- `blocked_until_resolved`

### no-lookahead risk

Allowed values:

- `none_identified`
- `possible`
- `likely`
- `blocking`
- `unknown`

### evidence status

Allowed values:

- `source_backed`
- `reviewer_inferred`
- `missing`
- `conflicting`
- `not_applicable`

### label confidence

Allowed values:

- `confirmed`
- `unclear`
- `unknown`

## 6. Forbidden Stage 2 label-usability matrix values

The following examples may appear only as forbidden examples in prose, not as actual machine-checkable field values:

- `caution/blocking`
- `design_only/usable_after_stage_2_approval`
- `block_source_match/block_provenance`
- `reviewer_note_required/adjudication_required`
- `source_backed/reviewer_inferred`
- `confirmed/unclear`
- `possible/likely`
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

Forbidden examples are intentionally documented here so future reviewers know which terms not to promote into actual field values. Normal prose may discuss why these examples are forbidden; machine-checkable assignment lines must not use them.

## Machine-checkable Stage 2 label-usability matrix assignments

- label-usability matrix stage: stage_2_label_usability_blocking_matrix_design
- blocker source: source_resolution
- blocker source: point_in_time_provenance
- blocker source: station_source_selection
- blocker source: publication_timestamp
- blocker source: observation_availability
- blocker source: archive_finality_layer
- blocker source: revision_handling
- blocker source: classification_authority
- blocker source: source_conflict
- blocker source: trap_annotation
- blocker source: reviewer_adjudication
- blocker source: no_lookahead_control
- blocker source: other_unclear
- blocker severity: none
- blocker severity: caution
- blocker severity: blocking
- blocker severity: unknown
- label usability posture: design_only
- label usability posture: usable_after_stage_2_approval
- label usability posture: blocked_pending_source_match
- label usability posture: blocked_pending_provenance
- label usability posture: blocked_pending_adjudication
- matrix decision: allow_design_only
- matrix decision: allow_after_stage_2_approval
- matrix decision: block_source_match
- matrix decision: block_provenance
- matrix decision: block_adjudication
- matrix decision: require_more_evidence
- matrix decision: unclear
- escalation requirement: none_required
- escalation requirement: reviewer_note_required
- escalation requirement: adjudication_required
- escalation requirement: source_evidence_required
- escalation requirement: provenance_evidence_required
- escalation requirement: blocked_until_resolved
- no-lookahead risk: none_identified
- no-lookahead risk: possible
- no-lookahead risk: likely
- no-lookahead risk: blocking
- no-lookahead risk: unknown
- evidence status: source_backed
- evidence status: reviewer_inferred
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown

## 8. Label-usability blocking matrix

This Markdown-only label-usability blocking matrix maps future source-resolution/provenance blockers to a conservative required posture. It is a design matrix; it is not a data file, loader, or runtime contract.

| Condition | Blocker source | Blocker severity | No-lookahead risk | Evidence status | Label confidence | Required label usability posture | Matrix decision | Escalation requirement | Reviewer note expectation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| No blockers identified in the source-resolution audit and provenance review. | `other_unclear` | `none` | `none_identified` | `source_backed` | `confirmed` | `usable_after_stage_2_approval` | `allow_after_stage_2_approval` | `none_required` | Note that later use still requires separate Stage 2 approval and does not approve scoring. |
| Design-only row before a future label exists. | `other_unclear` | `unknown` | `unknown` | `not_applicable` | `unknown` | `design_only` | `allow_design_only` | `reviewer_note_required` | Note that no historical label exists and no fixture is created. |
| Missing resolver source identity. | `source_resolution` | `blocking` | `unknown` | `missing` | `unknown` | `blocked_pending_source_match` | `block_source_match` | `source_evidence_required` | Identify the missing venue-defined source identity and block future label use. |
| Source does not match the venue-defined settlement object. | `source_resolution` | `blocking` | `likely` | `conflicting` | `unclear` | `blocked_pending_source_match` | `block_source_match` | `blocked_until_resolved` | Explain the mismatch between reviewer evidence and the settlement source. |
| Station/source selection has hindsight risk. | `station_source_selection` | `blocking` | `likely` | `reviewer_inferred` | `unclear` | `blocked_pending_adjudication` | `block_adjudication` | `adjudication_required` | Record why station/source choice was not pinned before result knowledge. |
| Missing source publication timestamp. | `publication_timestamp` | `blocking` | `blocking` | `missing` | `unknown` | `blocked_pending_provenance` | `block_provenance` | `provenance_evidence_required` | Note the missing publication timestamp needed for point-in-time review. |
| Observation valid time exists but observation availability time is missing. | `observation_availability` | `blocking` | `blocking` | `missing` | `unknown` | `blocked_pending_provenance` | `block_provenance` | `provenance_evidence_required` | Distinguish valid time from availability time and block future label use. |
| Archive/finality layer is unknown. | `archive_finality_layer` | `blocking` | `likely` | `missing` | `unknown` | `blocked_pending_provenance` | `block_provenance` | `provenance_evidence_required` | Identify whether the reviewed value came from preliminary, final, or revised archive layer. |
| Archive/finality layers conflict. | `archive_finality_layer` | `blocking` | `likely` | `conflicting` | `unclear` | `blocked_pending_adjudication` | `block_adjudication` | `adjudication_required` | Describe the conflicting layers and defer usability until adjudicated. |
| Classification authority is unresolved. | `classification_authority` | `blocking` | `unknown` | `missing` | `unknown` | `blocked_pending_source_match` | `block_source_match` | `source_evidence_required` | Identify the missing authority for classification-style contracts. |
| Unresolved source conflict. | `source_conflict` | `blocking` | `likely` | `conflicting` | `unclear` | `blocked_pending_adjudication` | `block_adjudication` | `adjudication_required` | List conflicting evidence and prevent confirmed status. |
| Trap annotation is blocking. | `trap_annotation` | `blocking` | `possible` | `reviewer_inferred` | `unclear` | `blocked_pending_adjudication` | `block_adjudication` | `adjudication_required` | Explain the trap and why it prevents future use. |
| Reviewer adjudication remains unresolved. | `reviewer_adjudication` | `blocking` | `unknown` | `conflicting` | `unclear` | `blocked_pending_adjudication` | `block_adjudication` | `blocked_until_resolved` | Link the unresolved reviewer question and keep the row blocked. |
| No-lookahead control is missing or blocking. | `no_lookahead_control` | `blocking` | `blocking` | `missing` | `unknown` | `blocked_pending_provenance` | `block_provenance` | `blocked_until_resolved` | State the missing as-of control and do not treat final archive evidence as point-in-time evidence. |

## 9. Matrix decision rules

- Design-only work remains `design_only` with `allow_design_only`; it must not imply implementation readiness.
- No blockers identified may only become `usable_after_stage_2_approval` in a later separately approved Stage 2 context; this document does not create that approval.
- Missing resolver source identity maps to `blocked_pending_source_match` and `block_source_match`.
- Source mismatch maps to `blocked_pending_source_match` and `block_source_match`.
- Missing publication timestamp maps to `blocked_pending_provenance` and `block_provenance`.
- Missing observation availability maps to `blocked_pending_provenance` and `block_provenance`.
- Final archive leakage risk maps to `blocked_pending_provenance` when the as-of evidence is absent, or `blocked_pending_adjudication` when evidence conflicts.
- Hindsight station/source selection maps to `blocked_pending_adjudication` when reviewer judgment is needed, or `blocked_pending_source_match` when source notes show the selected source is not the venue-defined settlement object.
- Unresolved source conflict maps to `blocked_pending_adjudication`.
- Blocking trap annotation maps to `blocked_pending_adjudication`.
- Reviewer-inferred evidence cannot become `confirmed`; use `unclear` or `unknown` until source-backed evidence is inspected.
- Missing or conflicting evidence cannot be treated as usable.
- Stage 3 scoring must remain unapproved regardless of label usability posture.

## 10. Label-usability matrix template

Use this Markdown-only label-usability matrix template for future separately approved design examples. Do not serialize it as JSON/YAML/CSV, do not load it as a fixture, and do not treat placeholders as actual machine-checkable assignments.

| Field | Template entry |
| --- | --- |
| matrix row id | `[matrix_row_id]` |
| linked source-resolution audit id | `[linked_source_resolution_audit_id]` |
| linked provenance example id | `[linked_provenance_example_id]` |
| blocker source | `[blocker_source]` selected from the closed `blocker source` set, for example `source_resolution` |
| blocker severity | `[blocker_severity]` selected from the closed `blocker severity` set, for example `blocking` |
| no-lookahead risk | `[no_lookahead_risk]` selected from the closed `no-lookahead risk` set, for example `blocking` |
| evidence status | `[evidence_status]` selected from the closed `evidence status` set, for example `missing` |
| label confidence | `[label_confidence]` selected from the closed `label confidence` set, for example `unknown` |
| label usability posture | `[label_usability_posture]` selected from the closed `label usability posture` set, for example `blocked_pending_provenance` |
| matrix decision | `[matrix_decision]` selected from the closed `matrix decision` set, for example `block_provenance` |
| escalation requirement | `[escalation_requirement]` selected from the closed `escalation requirement` set, for example `provenance_evidence_required` |
| reviewer notes | `[reviewer_notes]` with prose nuance only; do not invent custom closed-set values. |

## 11. Representative matrix scenarios

The scenarios below are synthetic design examples. They are not actual historical label data and do not create fixtures.

### Representative matrix scenario 1: source_resolution blocker

**Representative synthetic matrix scenario, not historical label data.** A future reviewer cannot identify the resolver source named by the venue-defined settlement object.

| Field | Value |
| --- | --- |
| blocker source | `source_resolution` |
| blocker severity | `blocking` |
| no-lookahead risk | `unknown` |
| evidence status | `missing` |
| label confidence | `unknown` |
| required label usability posture | `blocked_pending_source_match` |
| matrix decision | `block_source_match` |
| escalation requirement | `source_evidence_required` |

Future label use is blocked until source identity evidence shows that the reviewed source matches the settlement object. Non-approval reminder: this scenario does not approve ingestion, provider integration, forecast pulls, scoring, runtime, or trading.

### Representative matrix scenario 2: point_in_time_provenance blocker

**Representative synthetic matrix scenario, not historical label data.** A future reviewer has an observation valid time but cannot prove when the value became available to the venue or a hypothetical reviewer.

| Field | Value |
| --- | --- |
| blocker source | `point_in_time_provenance` |
| blocker severity | `blocking` |
| no-lookahead risk | `blocking` |
| evidence status | `missing` |
| label confidence | `unknown` |
| required label usability posture | `blocked_pending_provenance` |
| matrix decision | `block_provenance` |
| escalation requirement | `provenance_evidence_required` |

Future label use is blocked because valid time alone cannot prove point-in-time availability. Non-approval reminder: this scenario does not approve historical label implementation, data ingestion, backtesting, paper simulation, runtime observation, or autonomy.

### Representative matrix scenario 3: station_source_selection blocker

**Representative synthetic matrix scenario, not historical label data.** A future reviewer selects a station/source after knowing the outcome because the original contract language did not pin the station/source enough for source-compatible labeling.

| Field | Value |
| --- | --- |
| blocker source | `station_source_selection` |
| blocker severity | `blocking` |
| no-lookahead risk | `likely` |
| evidence status | `reviewer_inferred` |
| label confidence | `unclear` |
| required label usability posture | `blocked_pending_adjudication` |
| matrix decision | `block_adjudication` |
| escalation requirement | `adjudication_required` |

Future label use is blocked until adjudication establishes whether the selected station/source was known before result knowledge and matches the settlement object. Non-approval reminder: this scenario does not approve connectors, external API calls, provider credentials, config loading, secret reading, or production behavior.

### Representative matrix scenario 4: archive_finality_layer blocker

**Representative synthetic matrix scenario, not historical label data.** A future reviewer can see a final archive value but cannot determine whether the venue would have resolved from preliminary, first-complete, final, or revised evidence.

| Field | Value |
| --- | --- |
| blocker source | `archive_finality_layer` |
| blocker severity | `blocking` |
| no-lookahead risk | `likely` |
| evidence status | `missing` |
| label confidence | `unknown` |
| required label usability posture | `blocked_pending_provenance` |
| matrix decision | `block_provenance` |
| escalation requirement | `provenance_evidence_required` |

Future label use is blocked because final archive evidence may leak information unavailable at resolution time. Non-approval reminder: this scenario does not approve model scoring, probability scoring, Stage 3 scoring, backtesting, paper simulation, or C++/Rust runtime components.

### Representative matrix scenario 5: source_conflict blocker

**Representative synthetic matrix scenario, not historical label data.** Two reviewed sources disagree and the venue-defined fallback or hierarchy is not resolved.

| Field | Value |
| --- | --- |
| blocker source | `source_conflict` |
| blocker severity | `blocking` |
| no-lookahead risk | `likely` |
| evidence status | `conflicting` |
| label confidence | `unclear` |
| required label usability posture | `blocked_pending_adjudication` |
| matrix decision | `block_adjudication` |
| escalation requirement | `adjudication_required` |

Future label use is blocked until a reviewer adjudicates the conflict using source-backed settlement rules. Non-approval reminder: this scenario does not approve trading strategy, position sizing, order placement, live market execution, autonomy, or profitability claims.

## 12. Relationship to Stage 2 historical-label design

`PRD-P1-WX-STAGE2-01` defines the historical-label design contract. `PRD-P1-WX-STAGE2-02` defines point-in-time provenance examples. `PRD-P1-WX-STAGE2-03` defines source-resolution audit design. `PRD-P1-WX-STAGE2-04` defines how blockers from those designs map to label usability postures.

Future labels must pass this matrix before use beyond design review. No labels are created here. No ingestion is created here. No data files are created here. This document only specifies how future source-resolution/provenance blockers should fail closed.

## 13. Relationship to future Stage 3 scoring

Stage 3 scoring remains unapproved. Scoring requires source-compatible historical labels, and source-compatible labels require a label-usability posture that allows future use in a later separately approved Stage 2 context. Scoring without blocker mapping risks false settlement truth, lookahead leakage, or invalid labels.

This ticket only prepares label-usability matrix design. It does not approve model scoring, probability scoring, probability modeling, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.

## 14. Language/tooling posture

Stage 2 label-usability matrix design remains Markdown plus Python standard-library static tests only. No C++/Rust or performance-oriented language is appropriate at this stage. Python remains the default for future design/static validation. C++/Rust consideration requires a later approved implementation stage, profiling evidence, and a proven hot path.

This posture avoids external APIs, weather APIs, provider SDKs, network calls, runtime services, production code, connector abstractions, data ingestion code, secret loading, environment-variable loading, model/scoring code, backtesting code, paper simulation code, trading/order-placement code, new dependencies, C++, Rust, and non-Python build tooling.

## 15. Non-approval boundaries for label-usability matrix

Stage 2 label-usability/blocking matrix design does not approve:

- provider integration
- connectors
- provider credentials
- external API calls
- config loading
- secret reading
- data ingestion
- historical labels
- historical label implementation
- JSON/YAML/CSV/Parquet fixtures
- forecast pulls
- model scoring
- probability modeling
- probability scoring
- backtesting
- paper simulation
- runtime observation
- trading strategy
- position sizing
- trading
- order placement
- live market execution
- autonomy
- profitability claims
- C++/Rust runtime components

## 16. Later-ticket handoff

Later tickets may consider, only after separate explicit approval:

- Future Stage 2 historical-label schema refinement only if needed.
- Future label-usability matrix static example expansion only if needed.
- Future historical-label implementation or fixture creation only after separate approval.
- Future ingestion design only after separate approval.
- Future Stage 3 probability scoring only after Stage 2 labels exist and pass gates.
- Any implementation-adjacent work to later stages only after explicit approval.

## 17. Acceptance criteria

This document is complete only if:

- [x] `PRD-P1-WX-STAGE2-04` canonical ID is present.
- [x] Standalone Weather Bot PRD is referenced.
- [x] `PRD-P1-WX-STAGE1-CLOSEOUT-01` is referenced.
- [x] `PRD-P1-WX-STAGE2-01` is referenced.
- [x] `PRD-P1-WX-STAGE2-02` is referenced.
- [x] `PRD-P1-WX-STAGE2-03` is referenced.
- [x] Stage 2 design scope is explicit.
- [x] Label-usability blocking matrix is included.
- [x] Matrix decision rules are included.
- [x] Label-usability matrix template is included.
- [x] 4 to 6 representative synthetic matrix scenarios are included.
- [x] Required scenarios are covered.
- [x] Relationship to Stage 2 historical-label design is defined.
- [x] Relationship to Stage 3 scoring is defined without approving scoring.
- [x] Language/tooling posture is included.
- [x] All closed sets are listed exactly.
- [x] Machine-checkable assignment section exists.
- [x] Actual machine-checkable assignments use only allowed values.
- [x] Forbidden examples are documented without being used as actual field values.
- [x] Non-approval boundaries are explicit.
- [x] Later-ticket handoff is clear.
- [x] No implementation behavior is introduced.
