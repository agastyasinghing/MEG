# PRD-P1-WX-STAGE2-03: Source-Resolution Audit Checklist Design

## 1. Status and scope

- Canonical ID: **PRD-P1-WX-STAGE2-03**.
- This is **Stage 2 source-resolution audit checklist design only**.
- This follows `PRD-P1-WX-STAGE2-01`, the source-compatible historical-label design contract, and `PRD-P1-WX-STAGE2-02`, the point-in-time provenance example design.
- This document defines a reviewer checklist design only.
- This document does **not** create historical labels.
- This document does **not** create JSON/YAML/CSV/Parquet fixtures, seed example data, archive outputs, generated data, provider output, or research output.
- This document does **not** approve provider integration, connectors, data ingestion, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, live market execution, or autonomy.
- This document does **not** approve provider credentials, external API calls, config loading, secret reading, historical label implementation, production behavior, profitability claims, or C++/Rust runtime components.
- The only implementation-like artifact paired with this document is a lightweight Python standard-library static validation test for this Markdown contract.

## 2. Strategic framing

The controlling source for the Weather Bot stage ladder and evidence gates is the **standalone MEG Weather Bot PRD** (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`). `PRD-P1-WX-STAGE1-CLOSEOUT-01` confirms that Stage 1 static/manual-labeling artifacts can hand off into Stage 2 design work without approving ingestion, scoring, runtime, or execution. `PRD-P1-WX-STAGE2-01` defines the source-compatible historical-label design contract. `PRD-P1-WX-STAGE2-02` defines point-in-time provenance example designs that separate valid time, availability time, source publication time, and archive revision time.

Weather Bot is not a generic weather API wrapper and is not a trading bot. It models prediction-market weather contracts as **source-defined settlement objects**. The future target remains:

`P(the venue-defined source/station/window/threshold/revision/classification rule resolves Yes)`

It is not:

`P(weather variable crosses threshold)`

The source-resolution audit checklist protects that source-defined settlement object from resolver/source drift, hindsight station selection, archive/finality leakage, and unresolved source conflicts. Future historical labels must pass this checklist before they can be considered usable beyond design review. This document gives a Markdown-only design checklist, not implementation, ingestion, provider integration, forecast access, scoring, or execution behavior.

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

## 4. Source-resolution audit purpose

The source-resolution audit checklist is a reviewer-facing design artifact for future source-compatible historical labels. It checks whether a proposed label has enough source-resolution evidence to be reviewed without silently changing the settlement object.

At minimum, the checklist verifies resolver source identity, source role, station/source selection, source publication timestamp, observation valid time versus observation available time, archive/finality layer, revision/finality handling, classification authority when applicable, source conflicts, provenance blockers, and label usability posture.

The checklist is not data ingestion, provider integration, connector implementation, scoring, probability modeling, backtesting, runtime, paper simulation, or trading work. It creates no labels and no fixtures. Its job is to make future labels fail closed when resolver/source/station/publication/finality evidence is missing, conflicting, or hindsight-selected.

## 5. Closed Stage 2 source-resolution audit vocabulary

No other actual values are allowed for the machine-checkable fields below. Hybrid values, custom values, slash-combined values, and implementation-readiness terms are forbidden as actual values. If a condition is nuanced, mixed, or partially supported, the single most conservative exact field value must be selected and the nuance must be written in reviewer notes or prose fields.

### source-resolution audit stage

Allowed values:

- `stage_2_source_resolution_audit_design`

### audit checklist category

Allowed values:

- `resolver_source_identity`
- `source_role`
- `station_source_selection`
- `publication_timestamp`
- `observation_availability`
- `archive_finality_layer`
- `revision_handling`
- `classification_authority`
- `source_conflict`
- `provenance_blocker`
- `label_usability`
- `reviewer_escalation`
- `other_unclear`

### audit item decision

Allowed values:

- `pass`
- `caution`
- `block`
- `needs_more_evidence`
- `not_applicable`

### source-resolution status

Allowed values:

- `source_resolved`
- `source_unresolved`
- `source_conflicting`
- `source_unknown`
- `requires_adjudication`

### station/source selection status

Allowed values:

- `explicit_pre_result`
- `inferred_pre_result`
- `hindsight_risk`
- `unresolved`
- `not_applicable`

### archive/finality status

Allowed values:

- `preliminary_layer`
- `final_layer`
- `revised_layer`
- `conflicting_layers`
- `unknown_layer`
- `not_applicable`

### provenance blocker status

Allowed values:

- `none_identified`
- `missing_publication_timestamp`
- `missing_observation_availability`
- `missing_station_selection_time`
- `missing_archive_revision_record`
- `unresolved_source_conflict`
- `final_archive_leakage_risk`
- `hindsight_selection_risk`
- `other_unclear`

### label usability posture

Allowed values from `PRD-P1-WX-STAGE2-01`:

- `design_only`
- `usable_after_stage_2_approval`
- `blocked_pending_source_match`
- `blocked_pending_provenance`
- `blocked_pending_adjudication`

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

## 6. Forbidden Stage 2 source-resolution audit values

The examples below may appear only as forbidden examples in prose. They must not be used as actual machine-checkable field values.

- `pass/caution`
- `source_resolved/source_unresolved`
- `explicit_pre_result/inferred_pre_result`
- `preliminary_layer/final_layer`
- `source_backed/reviewer_inferred`
- `confirmed/unclear`
- `design_only/usable_after_stage_2_approval`
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

## Machine-checkable Stage 2 source-resolution audit assignments

- source-resolution audit stage: stage_2_source_resolution_audit_design
- audit checklist category: resolver_source_identity
- audit checklist category: source_role
- audit checklist category: station_source_selection
- audit checklist category: publication_timestamp
- audit checklist category: observation_availability
- audit checklist category: archive_finality_layer
- audit checklist category: revision_handling
- audit checklist category: classification_authority
- audit checklist category: source_conflict
- audit checklist category: provenance_blocker
- audit checklist category: label_usability
- audit checklist category: reviewer_escalation
- audit checklist category: other_unclear
- audit item decision: pass
- audit item decision: caution
- audit item decision: block
- audit item decision: needs_more_evidence
- audit item decision: not_applicable
- source-resolution status: source_resolved
- source-resolution status: source_unresolved
- source-resolution status: source_conflicting
- source-resolution status: source_unknown
- source-resolution status: requires_adjudication
- station/source selection status: explicit_pre_result
- station/source selection status: inferred_pre_result
- station/source selection status: hindsight_risk
- station/source selection status: unresolved
- station/source selection status: not_applicable
- archive/finality status: preliminary_layer
- archive/finality status: final_layer
- archive/finality status: revised_layer
- archive/finality status: conflicting_layers
- archive/finality status: unknown_layer
- archive/finality status: not_applicable
- provenance blocker status: none_identified
- provenance blocker status: missing_publication_timestamp
- provenance blocker status: missing_observation_availability
- provenance blocker status: missing_station_selection_time
- provenance blocker status: missing_archive_revision_record
- provenance blocker status: unresolved_source_conflict
- provenance blocker status: final_archive_leakage_risk
- provenance blocker status: hindsight_selection_risk
- provenance blocker status: other_unclear
- label usability posture: design_only
- label usability posture: usable_after_stage_2_approval
- label usability posture: blocked_pending_source_match
- label usability posture: blocked_pending_provenance
- label usability posture: blocked_pending_adjudication
- evidence status: source_backed
- evidence status: reviewer_inferred
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown

## 8. Source-resolution audit checklist

Future reviewers should apply this Markdown-only checklist before any future source-compatible historical label can move beyond design review:

1. **Resolver source identity**
   - Is the resolver source explicitly named?
   - Does the evidence tie that resolver source to the venue-defined settlement rule rather than to a convenient weather data page?
   - If the resolver source is unnamed, ambiguous, or only inferred from context, choose a conservative status and document the blocker.
2. **Source role**
   - Is the resolver source role known?
   - Is the resolver source official, venue-discretionary, station-based, archive-based, forecast-based, or unknown?
   - Does the role affect whether future labels need classification authority, archive revision evidence, or station-selection evidence?
3. **Station/source selection**
   - Is the station or observation point explicitly specified before the result?
   - Is station/source selection pre-result, inferred, hindsight-risk, unresolved, or not applicable?
   - Does the reviewer have evidence for when the station/source choice became knowable?
4. **Publication timestamp**
   - Is the relevant source publication timestamp known?
   - Is the timestamp tied to the source used by the venue-defined settlement object?
   - If the source value exists but publication timing is missing, the item must not pass.
5. **Observation availability**
   - Is the observation valid time distinguished from observation available time?
   - Does the label avoid treating a measurement window as proof that the observation was inspectable at that time?
6. **Archive/finality layer**
   - Is the archive/finality layer identified?
   - Is the reviewer looking at a preliminary layer, final layer, revised layer, conflicting layers, unknown layer, or a not-applicable case?
7. **Revision/finality handling**
   - Is the revision or correction path known?
   - Is there an archive revision time or finality evidence sufficient to avoid final archive leakage?
8. **Classification authority**
   - Is the classification authority identified, if applicable?
   - For event-classification markets, does the source define who classifies the event rather than relying on reviewer interpretation?
9. **Source conflicts**
   - Are there conflicting sources?
   - Are source conflicts resolved or escalated?
   - If conflict resolution is not source-backed, label usability should remain blocked or require adjudication.
10. **Provenance blockers**
    - Are provenance blockers present?
    - Does any blocker require label usability to be `blocked_pending_source_match`, `blocked_pending_provenance`, or `blocked_pending_adjudication`?
11. **Evidence status and confidence**
    - What evidence status and label confidence should apply?
    - Use `confirmed` only when the source-resolution audit design claim is directly supported by inspected docs.
    - Use `unclear` for partial or mixed interpretation and `unknown` when unsupported or unavailable.
12. **Reviewer notes**
    - What reviewer notes are required?
    - Notes must capture source notes, uncertainty, escalation rationale, and why the conservative closed-set value was selected.

## 9. Audit item decision rules

### audit item decision

- Choose `pass` only when the item is supported by inspected source or planning evidence and no blocker applies.
- Choose `caution` when the item has support but has a non-blocking ambiguity that must be retained in notes.
- Choose `block` when evidence is missing, conflicting, hindsight-selected, or would change the settlement object.
- Choose `needs_more_evidence` when the reviewer cannot complete the item without additional source evidence.
- Choose `not_applicable` only when the category genuinely does not apply to the settlement object.

### source-resolution status

- Choose `source_resolved` only when the resolver source identity and role are source-backed.
- Choose `source_unresolved` when the resolver source is absent or cannot be tied to settlement.
- Choose `source_conflicting` when competing sources imply different settlement objects.
- Choose `source_unknown` when the source cannot be inspected or reconstructed from available planning evidence.
- Choose `requires_adjudication` when a human reviewer must resolve a supported but material ambiguity.
- An unresolved resolver source must not pass.

### station/source selection status

- Choose `explicit_pre_result` when the station or observation point was specified before the outcome was known.
- Choose `inferred_pre_result` when evidence supports a pre-result source selection but does not explicitly name every detail.
- Choose `hindsight_risk` when the station/source could have been selected after seeing outcome-relevant evidence.
- Choose `unresolved` when selection timing cannot be established.
- Choose `not_applicable` only for settlement objects with no station/source-selection concept.
- Hindsight station/source selection must block or require adjudication.

### archive/finality status

- Choose `preliminary_layer` when evidence comes from an initial or non-final layer.
- Choose `final_layer` when the settlement object explicitly depends on final data and the finality timing is established.
- Choose `revised_layer` when a correction or revision is material to the source value.
- Choose `conflicting_layers` when preliminary, final, or revised layers disagree in a way that could affect settlement.
- Choose `unknown_layer` when the archive/finality layer cannot be established.
- Choose `not_applicable` only where no archive/finality question applies.
- Conflicting archive/finality layers require caution or block, depending on whether source-backed notes resolve settlement use.

### provenance blocker status

- Choose `none_identified` only when the checklist finds no source-resolution or point-in-time blocker.
- Choose `missing_publication_timestamp` when the relevant source publication timestamp is absent; missing publication timestamp must not pass.
- Choose `missing_observation_availability` when the observation valid time is known but observation available time is not.
- Choose `missing_station_selection_time` when station/source selection timing is needed but missing.
- Choose `missing_archive_revision_record` when revision/finality evidence is material but absent.
- Choose `unresolved_source_conflict` when sources conflict and source-backed notes do not resolve the conflict.
- Choose `final_archive_leakage_risk` when final data may be imported into a pre-final decision context.
- Choose `hindsight_selection_risk` when station/source choice may be outcome-dependent.
- Choose `other_unclear` only when the blocker is real but not captured by the more specific values.

### label usability posture

- Choose `design_only` for this ticket and any future audit draft that has not passed Stage 2 approval gates.
- Choose `usable_after_stage_2_approval` only in a later separately approved Stage 2 context where all required source-resolution and provenance checks pass.
- Choose `blocked_pending_source_match` when the source does not match the venue-defined settlement object.
- Choose `blocked_pending_provenance` when point-in-time source, publication, availability, station-selection, or revision evidence is missing.
- Choose `blocked_pending_adjudication` when a reviewer must resolve a material ambiguity or conflict.
- Missing or conflicting evidence should not be treated as usable.

### evidence status

- Choose `source_backed` only when inspected docs or source-resolution notes directly support the claim.
- Choose `reviewer_inferred` when the reviewer has a documented inference but not direct source backing.
- Choose `missing` when required evidence is absent.
- Choose `conflicting` when evidence supports incompatible readings.
- Choose `not_applicable` only when no evidence is required for the category.
- Reviewer-inferred evidence should not become confirmed.

### label confidence

- Choose `confirmed` only when the source-resolution audit design claim is directly supported by inspected docs.
- Choose `unclear` for partial, ambiguous, or reviewer-inferred interpretation.
- Choose `unknown` when unsupported or unavailable.

## 10. Source-resolution audit template

The following is a Markdown-only checklist template, not JSON/YAML/CSV and not a fixture. Closed-set fields must use one exact allowed value; nuance belongs in notes.

```text
# Source-resolution audit template

- audit_id: [audit_id]
- linked_historical_label_design_id: [linked_historical_label_design_id]
- linked_provenance_example_id: [linked_provenance_example_id]
- source-resolution audit stage: stage_2_source_resolution_audit_design
- audit checklist category: resolver_source_identity
- audit item decision: needs_more_evidence
- source-resolution status: source_unknown
- station/source selection status: not_applicable
- archive/finality status: not_applicable
- provenance blocker status: other_unclear
- label usability posture: design_only
- evidence status: missing
- label confidence: unknown

## Source identity
- resolver_source_name: [resolver_source_name]
- source_role: [source_notes]
- station_or_observation_point: [station_or_observation_point]

## Timing and finality
- source_publication_time: [source_publication_time]
- observation_valid_time: [observation_valid_time]
- observation_available_time: [observation_available_time]
- archive_revision_time: [archive_revision_time]

## Notes
- source_notes: [source_notes]
- reviewer_notes: [reviewer_notes]
- non_approval_reminder: this checklist template creates no historical label, fixture, ingestion, provider integration, forecast pull, scoring, runtime observation, trading, order placement, or autonomy.
```

## 11. Representative audit scenarios

The scenarios below are representative synthetic audit scenario designs, not historical label data. They do not create source-backed rows, fixtures, provider records, or market labels.

### Representative audit scenario 1: resolver_source_identity

Representative synthetic audit scenario, not historical label data.

- audit checklist category: `resolver_source_identity`
- source-resolution status: `source_unresolved`
- station/source selection status: `not_applicable`
- archive/finality status: `not_applicable`
- provenance blocker status: `other_unclear`
- label usability posture: `blocked_pending_source_match`
- What would block future label use: the venue-defined resolver source is not explicitly named, so a future label could silently substitute a different settlement object.
- Non-approval reminder: this scenario does not approve historical label implementation, data ingestion, provider integration, connectors, forecast pulls, scoring, runtime observation, trading, order placement, or autonomy.

### Representative audit scenario 2: station_source_selection

Representative synthetic audit scenario, not historical label data.

- audit checklist category: `station_source_selection`
- source-resolution status: `source_resolved`
- station/source selection status: `hindsight_risk`
- archive/finality status: `not_applicable`
- provenance blocker status: `hindsight_selection_risk`
- label usability posture: `blocked_pending_adjudication`
- What would block future label use: the station or observation point appears selected after outcome-relevant evidence was known, so reviewer notes must not convert a hindsight choice into a source-compatible settlement object.
- Non-approval reminder: this scenario is only a Markdown design example and does not approve provider credentials, external API calls, config loading, secret reading, data ingestion, forecast pulls, scoring, runtime observation, trading, order placement, or autonomy.

### Representative audit scenario 3: publication_timestamp

Representative synthetic audit scenario, not historical label data.

- audit checklist category: `publication_timestamp`
- source-resolution status: `source_resolved`
- station/source selection status: `explicit_pre_result`
- archive/finality status: `preliminary_layer`
- provenance blocker status: `missing_publication_timestamp`
- label usability posture: `blocked_pending_provenance`
- What would block future label use: the observed value is present, but the source publication timestamp is missing, so the reviewer cannot prove the observation was available at the claimed point in time.
- Non-approval reminder: this scenario creates no label data, no JSON/YAML/CSV/Parquet fixtures, no ingestion path, no probability scoring, no backtesting, no paper simulation, no runtime observation, and no trading/order/autonomy behavior.

### Representative audit scenario 4: archive_finality_layer

Representative synthetic audit scenario, not historical label data.

- audit checklist category: `archive_finality_layer`
- source-resolution status: `requires_adjudication`
- station/source selection status: `explicit_pre_result`
- archive/finality status: `conflicting_layers`
- provenance blocker status: `missing_archive_revision_record`
- label usability posture: `blocked_pending_adjudication`
- What would block future label use: preliminary and final archive layers could imply different settlement outcomes, and the archive revision record is missing.
- Non-approval reminder: this scenario does not approve historical label implementation, fixtures, provider integration, connectors, data ingestion, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, live market execution, or autonomy.

### Representative audit scenario 5: source_conflict

Representative synthetic audit scenario, not historical label data.

- audit checklist category: `source_conflict`
- source-resolution status: `source_conflicting`
- station/source selection status: `inferred_pre_result`
- archive/finality status: `unknown_layer`
- provenance blocker status: `unresolved_source_conflict`
- label usability posture: `blocked_pending_adjudication`
- What would block future label use: two plausible sources point to different source roles or values, and the conflict has not been resolved by source-backed notes.
- Non-approval reminder: this scenario is not a connector design, provider adapter, external API call, weather forecast pull, model, backtest, paper simulation, runtime service, order placement path, or autonomous workflow.

### Representative audit scenario 6: classification_authority

Representative synthetic audit scenario, not historical label data.

- audit checklist category: `classification_authority`
- source-resolution status: `requires_adjudication`
- station/source selection status: `not_applicable`
- archive/finality status: `not_applicable`
- provenance blocker status: `other_unclear`
- label usability posture: `blocked_pending_adjudication`
- What would block future label use: an event-classification settlement object needs a named classification authority, but the authority is ambiguous or only reviewer-inferred.
- Non-approval reminder: this scenario does not approve provider integration, connectors, data ingestion, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading strategy, position sizing, order placement, live market execution, autonomy, profitability claims, or C++/Rust runtime components.

## 12. Relationship to Stage 2 historical-label design

`PRD-P1-WX-STAGE2-01` defines the historical-label design contract. `PRD-P1-WX-STAGE2-02` defines point-in-time provenance example designs. This ticket defines a source-resolution audit checklist that future labels must pass before use.

Future labels must pass source-resolution audit before they can be considered usable beyond design review. No labels are created here. No ingestion is created here. No data files are created here. No JSON/YAML/CSV/Parquet fixtures are created here. No provider integration, connector behavior, scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy is created here.

## 13. Relationship to future Stage 3 scoring

Stage 3 scoring remains unapproved. Future scoring requires source-compatible historical labels. Source-compatible labels require source-resolution audit success and point-in-time provenance. Scoring without source-resolution audit risks false settlement truth and lookahead leakage because it can evaluate decisions against a resolver, source, station, archive layer, or classification rule that differs from the venue-defined settlement object.

This ticket only prepares audit design. It does not approve Stage 3 probability scoring, model scoring, forecast modeling, backtesting, paper simulation, runtime observation, trading, position sizing, order placement, or autonomy.

## 14. Language/tooling posture

Stage 2 source-resolution audit design remains Markdown plus Python standard-library static tests only. No C++/Rust or other performance-oriented language is appropriate at this stage. Python remains the default for future design/static validation because the work is document validation, not runtime computation. Any C++/Rust consideration requires a later approved implementation stage, profiling evidence, a proven hot path, and a separate approval gate. This ticket adds no C++/Rust runtime components.

## 15. Non-approval boundaries for source-resolution audit

Stage 2 source-resolution audit checklist design does not approve:

- provider integration
- connectors
- connector implementation
- provider credentials
- external API calls
- live weather API use
- config loading
- secret reading
- data ingestion
- historical labels
- historical label implementation
- JSON/YAML/CSV/Parquet fixtures
- JSON/YAML/CSV/Parquet fixture creation
- forecast pulls
- forecast modeling
- model scoring
- probability modeling
- probability scoring
- backtesting
- paper simulation
- runtime observation
- trading
- trading strategy
- position sizing
- order placement
- live market execution
- autonomy
- profitability claims
- C++/Rust runtime components

## 16. Later-ticket handoff

Later tickets may address the following only after explicit approval and within their own allowed scope:

- Future Stage 2 historical-label schema refinement only if needed.
- Future source-resolution audit static example expansion only if needed.
- Future historical-label implementation or fixture creation only after separate approval.
- Future ingestion design only after separate approval.
- Future Stage 3 probability scoring only after Stage 2 labels exist and pass gates.
- Any implementation-adjacent work to later stages only after explicit approval.

## 17. Acceptance criteria

This document is complete only if:

- [x] `PRD-P1-WX-STAGE2-03` canonical ID is present.
- [x] Standalone Weather Bot PRD is referenced.
- [x] Stage 1 closeout is referenced.
- [x] `PRD-P1-WX-STAGE2-01` is referenced.
- [x] `PRD-P1-WX-STAGE2-02` is referenced.
- [x] Stage 2 design scope is explicit.
- [x] Source-resolution audit checklist is included.
- [x] Audit item decision rules are included.
- [x] Source-resolution audit template is included.
- [x] 4 to 6 representative synthetic audit scenarios are included.
- [x] Required scenarios are covered: `resolver_source_identity`, `station_source_selection`, `publication_timestamp`, and `archive_finality_layer`.
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
