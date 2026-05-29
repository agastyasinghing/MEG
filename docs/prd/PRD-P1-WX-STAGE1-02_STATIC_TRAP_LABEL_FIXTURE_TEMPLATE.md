# PRD-P1-WX-STAGE1-02: Static Trap-Label Fixture Template

## 1. Status and scope
- This ticket is **Stage 1 only** and is limited to **static trap-label fixture/template work**.
- This ticket builds directly on `PRD-P1-WX-STAGE1-01`.
- This document defines a trap-label fixture/template only.
- This ticket does not create JSON/YAML/CSV fixtures.
- This ticket does not approve provider integration, data ingestion, historical labels, forecast pulls, model scoring, probability scoring, backtesting, runtime observation, trading, order placement, or autonomy.

## 2. Strategic framing
- Controlling Stage ladder source: **standalone MEG Weather Bot PRD** (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`).
- Prior Stage 1 schema source: `PRD-P1-WX-STAGE1-01`.
- Weather-market traps arise because prediction-market weather contracts are **source-defined settlement objects**, not generic weather questions.
- Trap labels exist to help reviewers avoid false equivalence, false edge, provider-source mismatch, and premature actionability claims.
- Trap labels are required before seed examples, scoring, and backtesting so later work inherits explicit fail-closed ambiguity annotations.

## 3. Stage ladder position
- Stage 0: documentation and source-backed research only.
- Stage 1: static examples and manual labels.
- Stage 2: source-compatible historical labels with point-in-time provenance.
- Stage 3: retrospective probability scoring on strict OOS splits.
- Stage 4: trap-filtered paper simulation with executable quotes, fees, spreads, and depth assumptions.
- Stage 5: human-reviewed dry run with reviewer packets and override logs.
- Stage 6: runtime observation only under separate approval.
- Stage 7: execution/trading only after separate explicit approval.

This ticket is Stage 1 only. Stage 2 historical labels, Stage 3 scoring, Stage 4 paper simulation, Stage 5 dry run, Stage 6 runtime observation, and Stage 7 execution/trading remain unapproved.

## 4. Trap-label template purpose
- This template defines how reviewers capture trap metadata for weather-market ambiguity and risk.
- Trap labels are static reviewer-created annotations, not ingested historical data.
- Trap labels attach to manual canonical event labels defined in `PRD-P1-WX-STAGE1-01`.
- Trap labels are planning artifacts for future review/design/testing only.

## 5. Closed trap-label field vocabulary
No other actual values are allowed for closed-set fields. Hybrid/custom/slash values are forbidden as actual values. Nuance belongs in notes/prose fields.

- trap label stage
  - `stage_1_static_trap_label`
- trap source
  - `market_wording`
  - `resolution_source`
  - `provider_source`
  - `location_station`
  - `time_window`
  - `threshold_unit`
  - `measurement_method`
  - `data_revision`
  - `venue_discretion`
  - `external_event_classification`
  - `market_microstructure`
  - `validation_provenance`
  - `other_unclear`
- trap severity
  - `caution`
  - `blocking`
- trap action
  - `reviewer_note`
  - `caution_flag`
  - `block_mapping`
  - `block_actionability`
  - `needs_adjudication`
- false-edge risk
  - `none_identified`
  - `possible_false_edge`
  - `likely_false_edge`
  - `blocking_false_edge`
  - `unclear`
- canonical mapping impact
  - `no_material_impact`
  - `mapping_unclear`
  - `near_equivalence_only`
  - `non_equivalent`
  - `mapping_blocked`
- label confidence
  - `confirmed`
  - `unclear`
  - `unknown`
- review posture
  - `informational`
  - `review_only`
  - `blocked`
- reviewer workflow state
  - `unreviewed`
  - `caution_under_review`
  - `blocking_under_review`
  - `reviewed_pass`
  - `reviewed_caution`
  - `reviewed_block`

## 6. Forbidden trap-label values
The following may appear only as forbidden examples in prose and must not be used as actual machine-checkable field values:
- `caution/blocking`
- `reviewer_note/caution_flag`
- `possible_false_edge/likely_false_edge`
- `mapping_unclear/non_equivalent`
- `review_only/blocked`
- `market_wording/resolution_source`
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

## Machine-checkable trap-label field assignments
- trap label stage: stage_1_static_trap_label
- trap source: market_wording
- trap source: resolution_source
- trap source: provider_source
- trap source: location_station
- trap source: time_window
- trap source: threshold_unit
- trap source: measurement_method
- trap source: data_revision
- trap source: venue_discretion
- trap source: external_event_classification
- trap source: market_microstructure
- trap source: validation_provenance
- trap source: other_unclear
- trap severity: caution
- trap severity: blocking
- trap action: reviewer_note
- trap action: caution_flag
- trap action: block_mapping
- trap action: block_actionability
- trap action: needs_adjudication
- false-edge risk: none_identified
- false-edge risk: possible_false_edge
- false-edge risk: likely_false_edge
- false-edge risk: blocking_false_edge
- false-edge risk: unclear
- canonical mapping impact: no_material_impact
- canonical mapping impact: mapping_unclear
- canonical mapping impact: near_equivalence_only
- canonical mapping impact: non_equivalent
- canonical mapping impact: mapping_blocked
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

## 8. Static trap-label fixture/template schema
- `trap_label_id`
- `linked_manual_label_id`
- `trap_label_stage`
- `reviewer_workflow_state`
- `review_posture`
- `trap_source`
- `trap_name`
- `trap_summary`
- `affected_canonical_fields`
- `trap_severity`
- `trap_action`
- `false_edge_risk`
- `canonical_mapping_impact`
- `source_defined_settlement_issue`
- `venue_wording_issue`
- `resolver_source_issue`
- `station_location_issue`
- `time_window_issue`
- `threshold_unit_issue`
- `measurement_method_issue`
- `revision_finality_issue`
- `classification_authority_issue`
- `provider_source_issue`
- `market_microstructure_issue`
- `validation_provenance_issue`
- `human_review_note`
- `blocker_or_caution_reason`
- `label_confidence`
- `ambiguity_notes`
- `reviewer_notes`
- `non_approval_notes`
- `source_notes`

## 9. Field definitions
- `trap_label_id`: Unique reviewer label identifier. Required for each trap annotation.
- `linked_manual_label_id`: Foreign-link style reference to the manual label from `PRD-P1-WX-STAGE1-01`. Required.
- `trap_label_stage`: Stage guard field. Required; closed set `trap label stage`.
- `reviewer_workflow_state`: Reviewer-state lifecycle marker. Required; closed set `reviewer workflow state`.
- `review_posture`: Outcome posture for downstream governance summaries. Required; closed set `review posture`.
- `trap_source`: Primary trap origin. Required; closed set `trap source`.
- `trap_name`: Short trap title. Required.
- `trap_summary`: Human-readable summary of risk mechanism. Required.
- `affected_canonical_fields`: Canonical-event fields affected by the trap. Required.
- `trap_severity`: Severity tier for governance routing. Required; closed set `trap severity`.
- `trap_action`: Required reviewer action for this trap. Required; closed set `trap action`.
- `false_edge_risk`: Likelihood that apparent edge is artificial. Required; closed set `false-edge risk`.
- `canonical_mapping_impact`: Impact on mapping certainty/actionability. Required; closed set `canonical mapping impact`.
- `source_defined_settlement_issue`: Yes/no-style prose statement describing settlement-object ambiguity. Required when present.
- `venue_wording_issue`: Describe wording ambiguity and comparator semantics. Required when wording ambiguity exists.
- `resolver_source_issue`: Describe resolver/authority ambiguity. Required when resolver uncertainty exists.
- `station_location_issue`: Describe city-vs-station or station mismatch risk. Required when location ambiguity exists.
- `time_window_issue`: Describe local-day vs UTC-day or window mismatch. Required when timing ambiguity exists.
- `threshold_unit_issue`: Describe threshold/comparator/unit mismatch. Required when threshold ambiguity exists.
- `measurement_method_issue`: Describe methodology mismatch (e.g., snowfall vs snow depth). Required when method ambiguity exists.
- `revision_finality_issue`: Describe preliminary vs final data uncertainty. Required when revision ambiguity exists.
- `classification_authority_issue`: Describe authority/classification ambiguity (e.g., severe event class). Required when classification ambiguity exists.
- `provider_source_issue`: Describe provider-source mismatch relative to resolver. Required when mismatch exists.
- `market_microstructure_issue`: Describe spread/depth/staleness trap relevance as reviewer context only. Required when microstructure ambiguity exists.
- `validation_provenance_issue`: Describe source-note/provenance gaps. Required when provenance uncertainty exists.
- `human_review_note`: Reviewer narrative note for future adjudication packets. Required.
- `blocker_or_caution_reason`: One-paragraph reason for caution/blocking posture. Required.
- `label_confidence`: Confidence for this trap annotation. Required; closed set `label confidence`. Use `confirmed` only when source-backed in template/source note, `unclear` for partial/mixed interpretation, and `unknown` when unsupported/unavailable.
- `ambiguity_notes`: Free-form nuance notes. Use this for mixed conditions instead of hybrid closed-set values.
- `reviewer_notes`: Additional reviewer commentary. Optional but recommended.
- `non_approval_notes`: Explicit reminder that trap labels do not grant implementation approval. Required.
- `source_notes`: Source references or reminder notes for future adjudication. Required.

## 10. Example trap-label template
Template/example only; not real ingested data and not a live/current market claim.

- `trap_label_id`: [trap_label_id]
- `linked_manual_label_id`: [linked_manual_label_id]
- `trap_label_stage`: stage_1_static_trap_label
- `reviewer_workflow_state`: unreviewed
- `review_posture`: review_only
- `trap_source`: location_station
- `trap_name`: [trap_name]
- `trap_summary`: City wording appears broader than the named station observation used by resolver documentation.
- `affected_canonical_fields`: [location_context, resolution_source, time_window]
- `trap_severity`: caution
- `trap_action`: caution_flag
- `false_edge_risk`: possible_false_edge
- `canonical_mapping_impact`: mapping_unclear
- `source_defined_settlement_issue`: Settlement appears tied to venue-defined station source rather than generic city weather.
- `venue_wording_issue`: Wording uses city name while resolver references station-level measurement.
- `resolver_source_issue`: Resolver source note appears station specific.
- `station_location_issue`: Potential city-versus-station mismatch.
- `time_window_issue`: Potential local day versus UTC day interpretation mismatch.
- `threshold_unit_issue`: No unit mismatch identified in this template.
- `measurement_method_issue`: Noted for reviewer check if snowfall versus snow depth phrasing appears.
- `revision_finality_issue`: Review whether preliminary versus final posting is binding.
- `classification_authority_issue`: N/A for this example unless classification language appears.
- `provider_source_issue`: Verify provider source is not substituted for resolver source.
- `market_microstructure_issue`: Context-only note; no actionability approval.
- `validation_provenance_issue`: Add explicit resolver/source note during adjudication.
- `human_review_note`: [human_review_note]
- `blocker_or_caution_reason`: Mapping ambiguity can create false equivalence if city wording is treated as equivalent to station resolution.
- `label_confidence`: unclear
- `ambiguity_notes`: Add any mixed-condition nuance here while keeping closed-set values exact.
- `reviewer_notes`: Placeholder for reviewer packet context.
- `non_approval_notes`: Static template only; no approval for implementation behavior.
- `source_notes`: [source_notes]

## 11. Trap-label reviewer checklist
- Is the trap tied to market wording?
- Is the trap tied to the resolver source?
- Is the trap tied to station/location?
- Is the trap tied to the measurement window?
- Is the trap tied to threshold/comparator/unit semantics?
- Is the trap tied to measurement method?
- Is the trap tied to data revision/finality?
- Is the trap tied to classification authority?
- Is the trap tied to provider/source mismatch?
- Is the trap tied to market microstructure?
- Does the trap create false equivalence?
- Does the trap create false edge?
- Does the trap block canonical mapping?
- Does the trap block actionability?
- What should a future human reviewer see?

## 12. Trap-label to manual-label relationship
- Trap labels link to manual labels via `linked_manual_label_id` from `PRD-P1-WX-STAGE1-01`.
- Trap labels annotate risks/ambiguities, not settlement outcomes.
- Trap labels do not create historical labels.
- Trap labels do not create model labels.
- Trap labels do not approve actionability.

## 13. Non-approval boundaries for trap labels
Trap labels do not approve:
- provider integration
- connectors
- provider credentials
- external API calls
- config loading
- secret reading
- data ingestion
- historical labels
- forecast pulls
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

## 14. Later-ticket handoff
- Hand off reviewer checklist/adjudication protocol to `PRD-P1-WX-STAGE1-03`.
- Hand off small manually labeled seed examples to `PRD-P1-WX-STAGE1-04`.
- Hand off Stage 2 source-compatible historical labels to a future Stage 2 ticket only after Stage 1 completion.
- Hand off probability scoring/backtesting to later stages only after required gates.
- Hand off implementation-adjacent work to later stages only after explicit approval.

## 15. Acceptance criteria
- [x] Canonical ID `PRD-P1-WX-STAGE1-02` is present exactly.
- [x] Standalone Weather Bot PRD is referenced.
- [x] `PRD-P1-WX-STAGE1-01` is referenced.
- [x] Stage 1 scope is explicit.
- [x] Source-defined settlement object thesis is preserved.
- [x] Static trap-label fixture/template is defined.
- [x] Example template is included.
- [x] All closed sets are listed exactly.
- [x] Machine-checkable assignment section exists.
- [x] Actual machine-checkable assignments use only allowed values.
- [x] Forbidden examples are documented without being used as actual field values.
- [x] Trap-label reviewer checklist is included.
- [x] Trap-label to manual-label relationship is defined.
- [x] Non-approval boundaries are explicit.
- [x] Later-ticket handoff is clear.
- [x] No implementation behavior is introduced.
