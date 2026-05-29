# PRD-P1-WX-STAGE1-03: Reviewer Checklist / Adjudication Protocol

## 1. Status and scope

`PRD-P1-WX-STAGE1-03` is **Stage 1 only** reviewer checklist/adjudication protocol work for static Weather Bot planning. It builds directly on:

- `PRD-P1-WX-STAGE1-01` static canonical weather-event manual-label schema and example template.
- `PRD-P1-WX-STAGE1-02` static trap-label fixture/template.
- The **standalone MEG Weather Bot PRD** (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`) as the controlling Stage ladder and strategic framing source.

This document defines a reviewer protocol only. It does not create seed examples, historical labels, JSON/YAML/CSV fixtures, provider integration, connectors, data ingestion, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.

The protocol is for static documentation review of proposed manual labels and static trap labels. It is not an implementation behavior, ingestion behavior, validation service, runtime service, connector abstraction, provider adapter, scoring engine, or trading workflow.

## 2. Strategic framing

The standalone MEG Weather Bot PRD frames Weather Bot as a system for modeling prediction-market weather contracts as **source-defined settlement objects**, not as a generic weather API wrapper and not as a trading bot. The target object is not simply `P(weather variable crosses threshold)`. The target is `P(the venue-defined source/station/window/threshold/revision/classification rule resolves Yes)`.

`PRD-P1-WX-STAGE1-01` defines the static manual-label vocabulary and template for canonical weather-event mapping. `PRD-P1-WX-STAGE1-02` defines the static trap-label vocabulary and template for ambiguity, false-equivalence, and false-edge risks. This ticket defines the reviewer checklist and adjudication protocol that reviews both before any future seed examples are selected.

Reviewer adjudication exists to prevent:

- **False equivalence**: treating near-matching city, station, provider, time-window, unit, or classification concepts as identical settlement objects.
- **False edge**: claiming apparent opportunity from source mismatch, revision mismatch, timing mismatch, or convenience-provider mismatch rather than from a validated source-compatible probability process.
- **Unsupported source assumptions**: filling missing resolver/source/station/window/threshold/revision/classification semantics with undocumented defaults.
- **Premature actionability**: presenting static labels as if they authorize ingestion, scoring, paper simulation, runtime observation, trading, order placement, or autonomy.

Reviewer adjudication is needed before seed examples, scoring, and backtesting because later work can only be meaningful if the static labels preserve the venue-defined settlement rule. A mislabeled event can make historical labels, score diagnostics, and simulated outcomes look precise while measuring the wrong object.

## 3. Stage ladder position

The standalone MEG Weather Bot PRD defines the Stage ladder:

- **Stage 0**: documentation and source-backed research only.
- **Stage 1**: static examples and manual labels.
- **Stage 2**: source-compatible historical labels with point-in-time provenance.
- **Stage 3**: retrospective probability scoring on strict OOS splits.
- **Stage 4**: trap-filtered paper simulation with executable quotes, fees, spreads, and depth assumptions.
- **Stage 5**: human-reviewed dry run with reviewer packets and override logs.
- **Stage 6**: runtime observation only under separate approval.
- **Stage 7**: execution/trading only after separate explicit approval.

This ticket is **Stage 1 only**. It supplies static reviewer checklist/adjudication protocol guidance for manual labels and trap labels. Stage 2 historical labels, Stage 3 scoring, Stage 4 paper simulation, Stage 5 dry run, Stage 6 runtime observation, and Stage 7 execution/trading remain unapproved and outside this ticket.

## 4. Reviewer protocol purpose

The reviewer checklist/adjudication protocol is for deciding whether a proposed static manual label or static trap label is sufficiently faithful to the source-defined settlement object thesis to be used later as a candidate seed example.

It applies to:

- Static manual labels from `PRD-P1-WX-STAGE1-01`, which describe canonical event mapping.
- Static trap labels from `PRD-P1-WX-STAGE1-02`, which describe ambiguity, false-edge, false-equivalence, and non-actionability risks.

It is not an ingestion, validation, scoring, probability, backtesting, runtime, or execution protocol. Adjudication decisions are reviewer decisions for static docs only. They do not turn a label into historical data, model input, executable data, or operational permission.

## 5. Closed reviewer-adjudication field vocabulary

No other actual values are allowed for the fields in this section. Hybrid, custom, and slash-combined values are forbidden as actual field values. If a condition is mixed or partially supported, reviewers must choose the single most conservative exact value and place nuance in reviewer notes, source notes, or prose.

### adjudication stage

Allowed value:

- `stage_1_reviewer_adjudication`

### checklist item category

Allowed values:

- `settlement_rule`
- `resolver_source`
- `station_location`
- `time_window`
- `threshold_unit`
- `measurement_method`
- `revision_finality`
- `classification_authority`
- `source_compatibility`
- `trap_review`
- `false_edge_review`
- `canonical_mapping`
- `evidence_quality`
- `non_approval_boundary`
- `reviewer_note`
- `other_unclear`

### review decision

Allowed values:

- `pass`
- `caution`
- `block`
- `needs_more_evidence`
- `not_applicable`

### adjudication outcome

Allowed values:

- `accepted`
- `revised`
- `escalated`
- `blocked`
- `deferred`

### evidence status

Allowed values:

- `source_backed`
- `reviewer_inferred`
- `missing`
- `conflicting`
- `not_applicable`

### disagreement status

Allowed values:

- `no_disagreement`
- `minor_disagreement`
- `material_disagreement`
- `unresolved_disagreement`

### label confidence

Allowed values:

- `confirmed`
- `unclear`
- `unknown`

Use `confirmed` only when the adjudication label is directly source-backed in the static example or source note. Use `unclear` for partial or mixed interpretation. Use `unknown` when support is unavailable or unsupported.

### review posture

Allowed values from `PRD-P1-WX-04`:

- `informational`
- `review_only`
- `blocked`

### reviewer workflow state

Allowed values from the standalone MEG Weather Bot PRD:

- `unreviewed`
- `caution_under_review`
- `blocking_under_review`
- `reviewed_pass`
- `reviewed_caution`
- `reviewed_block`

## 6. Forbidden reviewer-adjudication values

The following examples are forbidden as actual field values. They may appear only as forbidden examples in prose, not as machine-checkable assignments or template values:

- `pass/caution`
- `caution/block`
- `accepted/revised`
- `source_backed/reviewer_inferred`
- `no_disagreement/minor_disagreement`
- `confirmed/unclear`
- `review_only/blocked`
- `partial`
- `mixed`
- `likely`
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

A reviewer must not invent a hybrid value to describe nuance. Nuance belongs in `[reviewer_notes]`, `[source_notes]`, or other prose notes while the closed-set field remains one exact allowed value.

## Machine-checkable reviewer-adjudication field assignments

- adjudication stage: stage_1_reviewer_adjudication
- checklist item category: settlement_rule
- checklist item category: resolver_source
- checklist item category: station_location
- checklist item category: time_window
- checklist item category: threshold_unit
- checklist item category: measurement_method
- checklist item category: revision_finality
- checklist item category: classification_authority
- checklist item category: source_compatibility
- checklist item category: trap_review
- checklist item category: false_edge_review
- checklist item category: canonical_mapping
- checklist item category: evidence_quality
- checklist item category: non_approval_boundary
- checklist item category: reviewer_note
- checklist item category: other_unclear
- review decision: pass
- review decision: caution
- review decision: block
- review decision: needs_more_evidence
- review decision: not_applicable
- adjudication outcome: accepted
- adjudication outcome: revised
- adjudication outcome: escalated
- adjudication outcome: blocked
- adjudication outcome: deferred
- evidence status: source_backed
- evidence status: reviewer_inferred
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- disagreement status: no_disagreement
- disagreement status: minor_disagreement
- disagreement status: material_disagreement
- disagreement status: unresolved_disagreement
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown
- review posture: informational
- review posture: review_only
- review posture: blocked
- reviewer workflow state: unreviewed
- reviewer workflow state: caution_under_review
- reviewer workflow state: blocking_under_review
- reviewer workflow state: reviewed_pass
- reviewer workflow state: reviewed_caution
- reviewer workflow state: reviewed_block

## 8. Reviewer checklist

A reviewer should apply the following checklist to every proposed manual label and trap label:

- Does the label identify the venue-defined settlement object rather than a generic weather phenomenon?
- Does the label preserve raw market wording so future reviewers can distinguish headline wording, rules-summary wording, and contract terms?
- Does the label identify the resolver/source role and avoid substituting convenience-provider data for official resolver truth?
- Does the label identify source/station/location semantics, including whether a city label, station ID, airport, zone, basin, or official source geography controls resolution?
- Does the label identify the measurement window and timezone/local-day rule?
- Does the label identify threshold/comparator/unit semantics, including equality, rounding, trace handling, brackets, and source-native units where relevant?
- Does the label identify measurement method issues, such as accumulated precipitation versus observation at a timestamp, snowfall versus snow depth, temperature maximum versus instantaneous value, or event occurrence versus official classification?
- Does the label identify revision/finality issues, including preliminary postings, final archives, later corrections, source replacements, and venue freeze rules?
- Does the label identify classification authority issues, if applicable, for severe, tropical, drought, air-quality, or event-classification contracts?
- Does the label distinguish official resolver truth from convenience-provider data?
- Does the label identify trap sources using the Stage 1 trap-label vocabulary from `PRD-P1-WX-STAGE1-02`?
- Does the label identify false-edge risk without claiming that an edge exists?
- Does the label avoid false equivalence between near-matching stations, products, windows, units, thresholds, revisions, or classifications?
- Does the label avoid actionability claims and avoid implying that static adjudication authorizes any operational step?
- Does the label preserve non-approval boundaries for provider integration, connectors, external API calls, provider credentials, config loading, secret reading, data ingestion, historical labels, seed examples, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, and autonomy?
- Does the label use only allowed closed-set values for manual-label, trap-label, and reviewer-adjudication fields?
- Does the label include enough reviewer notes, source notes, and ambiguity notes for future seed examples in `PRD-P1-WX-STAGE1-04`?

## 9. Adjudication workflow

The static adjudication workflow is conceptual and docs-only:

1. **Initial reviewer pass**: confirm the proposed manual label or trap label is within Stage 1 static scope and is not presented as ingested, historical, runtime, scored, or actionable data.
2. **Checklist completion**: evaluate each checklist item category and assign exact closed-set review decisions.
3. **Trap-label cross-check**: compare manual-label mapping with trap-label risks from `PRD-P1-WX-STAGE1-02`, especially source, station, time-window, threshold, revision, classification, false-equivalence, and false-edge risks.
4. **Source/support review**: classify support as `source_backed`, `reviewer_inferred`, `missing`, `conflicting`, or `not_applicable`; do not fill missing settlement semantics with undocumented defaults.
5. **Conservative decision assignment**: choose the most conservative exact value for review decision, adjudication outcome, evidence status, disagreement status, label confidence, review posture, and reviewer workflow state.
6. **Disagreement handling**: record minor, material, or unresolved disagreement without inventing custom field values.
7. **Adjudicator escalation, if needed**: escalate labels with material disagreement, unresolved disagreement, missing support for load-bearing settlement fields, or blocking traps.
8. **Final reviewer workflow state**: mark a final workflow state only after the checklist, source/support review, trap cross-check, and disagreement handling are complete.
9. **Handoff to seed-example selection only if accepted/reviewed**: pass candidates to `PRD-P1-WX-STAGE1-04` only when they are static-docs candidates with an accepted or revised outcome and a reviewed workflow state; this handoff does not create seed example data files.

## 10. Decision rules

Reviewers must choose exact allowed values using conservative rules.

### Review decision

- Use `pass` only when the relevant checklist item is source-backed or not applicable, no load-bearing ambiguity remains, and no blocking trap applies.
- Use `caution` when the label is usable for static review but has reviewer-inferred support, minor ambiguity, non-blocking trap risk, or notes that future seed-example authors must preserve.
- Use `block` when a load-bearing settlement field is unsupported, conflicting, non-equivalent, or affected by a blocking trap.
- Use `needs_more_evidence` when the reviewer cannot decide without additional source notes.
- Use `not_applicable` only when the checklist item truly does not apply to the market family or label type.

### Adjudication outcome

- Use `accepted` only when the label can be used as a future static seed-example candidate without changing the closed-set fields.
- Use `revised` when the reviewer corrected notes or conservative field choices while keeping the label within Stage 1 static scope.
- Use `escalated` when adjudicator review is required before acceptance, deferral, or blocking.
- Use `blocked` when the label should not be used for future seed examples without a new source-backed mapping.
- Use `deferred` when the label is not blocked but should wait for later source clarification or a later ticket.

### Evidence status

- If source support is directly present in the static example or source note, use `source_backed`.
- If evidence is reviewer-inferred, use `reviewer_inferred` and put nuance in reviewer notes.
- If source support is missing, evidence status should be `missing` and label confidence should be `unknown`.
- If source support conflicts, evidence status should be `conflicting` and label confidence should be `unclear`.
- Use `not_applicable` only when the evidence question does not apply to the checklist item.

### Disagreement status

- Use `no_disagreement` when reviewers agree on the settlement mapping, trap severity, and non-approval posture.
- Use `minor_disagreement` for wording, note placement, or non-load-bearing interpretation differences that do not alter the conservative field choice.
- Use `material_disagreement` for differences that may alter canonical mapping, trap severity, review posture, label confidence, or final workflow state.
- Use `unresolved_disagreement` when reviewers cannot reconcile material differences in the static review record.

### Label confidence

- Use `confirmed` only when the adjudication label is directly source-backed in the static example or source note.
- Use `unclear` for partial, mixed, or conflicting interpretation.
- Use `unknown` when support is unavailable, unsupported, or missing.

### Review posture

- Use `informational` when a label or checklist item is context-only and creates no actionability posture.
- Use `review_only` for labels suitable for static human review but not operational use.
- Use `blocked` when the label or trap must not proceed as a seed-example candidate until the blocker is resolved.
- If a blocking trap is present, review posture should be `blocked` or review decision should be `block`.

### Reviewer workflow state

- Use `unreviewed` before any reviewer pass.
- Use `caution_under_review` when caution issues are actively being reviewed.
- Use `blocking_under_review` when possible blockers are actively being reviewed.
- Use `reviewed_pass` only when there is no material or unresolved disagreement and no blocking trap.
- Use `reviewed_caution` when caution remains documented but the label can stay in static-review consideration.
- Use `reviewed_block` when the label is blocked.
- If canonical mapping is unclear, review decision should not be `pass`.
- If disagreement is material or unresolved, do not mark `reviewed_pass`.

## 11. Disagreement and escalation protocol

A disagreement is **minor** when reviewers differ only on wording, reviewer-note emphasis, or non-load-bearing interpretation and the conservative closed-set assignments remain unchanged.

A disagreement is **material** when reviewers differ on resolver/source identity, station/location semantics, time window, threshold/comparator/unit semantics, measurement method, revision/finality rule, classification authority, trap severity, false-edge risk, canonical mapping, evidence status, label confidence, review posture, or final workflow state.

A disagreement is **unresolved** when reviewers cannot reconcile a material disagreement using the static label, trap label, and source notes available in Stage 1.

Escalate to an adjudicator when:

- Any load-bearing settlement field is missing, conflicting, or only reviewer-inferred in a way that could change canonical mapping.
- A trap label indicates blocking false-edge risk, non-equivalence, or blocked mapping.
- Reviewers have material or unresolved disagreement.
- The proposed label appears to imply ingestion, scoring, runtime use, trading, order placement, autonomy, or another non-approved activity.

Defer when the label may be useful later but Stage 1 lacks enough static source notes to complete review. Block when the current label would misrepresent the settlement object, create false equivalence, create false-edge claims, or cross non-approval boundaries. Preserve all nuance in notes without inventing custom field values.

## 12. Static adjudication template

Template/example only; not real ingested data, not a live/current market claim, not a seed example, and not a JSON/YAML/CSV fixture.

- `adjudication_id`: [adjudication_id]
- `manual_label_id`: [manual_label_id]
- `trap_label_id`: [trap_label_id]
- `reviewer_id`: [reviewer_id_or_placeholder]
- `adjudication_stage`: stage_1_reviewer_adjudication
- `checklist_item_category`: settlement_rule
- `checklist_item`: [checklist_item]
- `review_decision`: needs_more_evidence
- `adjudication_outcome`: deferred
- `evidence_status`: reviewer_inferred
- `disagreement_status`: no_disagreement
- `label_confidence`: unclear
- `review_posture`: review_only
- `reviewer_workflow_state`: caution_under_review
- `reviewer_notes`: [reviewer_notes]
- `source_notes`: [source_notes]
- `non_approval_notes`: Static adjudication template only; it does not approve provider integration, connectors, external API calls, provider credentials, config loading, secret reading, data ingestion, historical labels, seed examples, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.

## 13. Relationship to manual labels and trap labels

Manual labels describe canonical event mapping: the raw market wording, resolver/source identity, station/location semantics, measurement window, threshold/comparator/unit semantics, measurement method, revision/finality rule, classification authority, and non-approval posture for a venue-defined settlement object.

Trap labels describe ambiguity, risk, false-equivalence conditions, false-edge conditions, and actionability boundaries that may affect manual-label interpretation.

The adjudication protocol reviews both manual labels and trap labels. It does not create historical labels. It does not create model labels. It does not approve ingestion, scoring, runtime behavior, or actionability. It only records whether static labels are accepted, revised, escalated, blocked, or deferred for future static seed-example consideration.

## 14. Non-approval boundaries for adjudication

Reviewer adjudication does not approve:

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
- seed examples as data files or implementation artifacts
- forecast pulls
- forecast modeling
- model scoring
- probability modeling
- probability scoring
- backtesting
- paper simulation
- runtime observation
- trading strategy
- position sizing
- order placement
- live market execution
- autonomy
- profitability claims

Static acceptance is not operational readiness. Static review may make a label clearer for future documentation, but it does not grant provider access, data access, source polling, score production, simulated execution, runtime monitoring, trading, order placement, or autonomous authority.

## 15. Later-ticket handoff

- Hand off small manually labeled seed examples to `PRD-P1-WX-STAGE1-04`; those examples must use the schema and adjudication protocol from `PRD-P1-WX-STAGE1-01`, `PRD-P1-WX-STAGE1-02`, and `PRD-P1-WX-STAGE1-03`.
- Hand off Stage 2 source-compatible historical labels to a future Stage 2 ticket only after Stage 1 is complete and only after explicit approval.
- Hand off probability scoring and backtesting to later stages only after required gates.
- Hand off implementation-adjacent work to later stages only after explicit approval.

## 16. Acceptance criteria

- [x] `PRD-P1-WX-STAGE1-03` canonical ID is present.
- [x] Standalone Weather Bot PRD is referenced.
- [x] `PRD-P1-WX-STAGE1-01` is referenced.
- [x] `PRD-P1-WX-STAGE1-02` is referenced.
- [x] Stage 1 scope is explicit.
- [x] Source-defined settlement object thesis is preserved.
- [x] Reviewer checklist is defined.
- [x] Adjudication workflow is defined.
- [x] Decision rules are defined.
- [x] Disagreement/escalation protocol is defined.
- [x] Static adjudication template is included.
- [x] All closed sets are listed exactly.
- [x] Machine-checkable assignment section exists.
- [x] Actual machine-checkable assignments use only allowed values.
- [x] Forbidden examples are documented without being used as actual field values.
- [x] Relationship to manual labels and trap labels is defined.
- [x] Non-approval boundaries are explicit.
- [x] Later-ticket handoff is clear.
- [x] No implementation behavior is introduced.
