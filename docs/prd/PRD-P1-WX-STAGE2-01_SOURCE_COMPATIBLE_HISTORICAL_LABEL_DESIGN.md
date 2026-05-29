# PRD-P1-WX-STAGE2-01: Source-Compatible Historical-Label Design

## 1. Status and scope

- Canonical ID: **PRD-P1-WX-STAGE2-01**.
- This is **Stage 2 source-compatible historical-label design only**.
- This follows `PRD-P1-WX-STAGE1-CLOSEOUT-01`, the Stage 1 closure gates and Stage 2 readiness review.
- This document defines future historical-label design requirements only.
- This document does **not** create actual historical labels.
- This document does **not** create JSON/YAML/CSV/Parquet fixtures, data files, provider integration, connectors, data ingestion, forecast pulls, model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement, or autonomy.
- This document does **not** approve historical label implementation, provider credentials, external API calls, config loading, secret reading, runtime services, production behavior, C++/Rust runtime components, or implementation-adjacent work.
- The only implementation-like artifact paired with this document is a lightweight Python standard-library static validation test that checks this Markdown contract.

## 2. Strategic framing

The controlling source for the Weather Bot stage ladder and evidence gates is the **standalone MEG Weather Bot PRD** (`PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`). `PRD-P1-WX-STAGE1-CLOSEOUT-01` confirms that Stage 1 artifacts are ready for a Stage 2 design ticket but do not authorize Stage 2 implementation.

This design references and builds on the Stage 1 static/manual-labeling artifacts:

- `PRD-P1-WX-STAGE1-01`: static canonical weather-event manual-label schema and example template.
- `PRD-P1-WX-STAGE1-02`: static trap-label fixture/template.
- `PRD-P1-WX-STAGE1-03`: reviewer checklist and adjudication protocol.
- `PRD-P1-WX-STAGE1-04`: small manually labeled seed examples across early candidate market families.

Weather Bot is not a generic weather API wrapper and is not a trading bot. It models prediction-market weather contracts as **source-defined settlement objects**. Stage 2 historical labels must represent the venue-defined source/station/window/threshold/revision/classification rule. The label target is **source-compatible settlement truth**, not generic weather truth. In probability notation, the future target remains:

`P(the venue-defined source/station/window/threshold/revision/classification rule resolves Yes)`

It is not:

`P(weather variable crosses threshold)`

Point-in-time provenance is mandatory before any future scoring or backtesting because a label that uses facts unavailable at the claimed decision time would leak final settlement knowledge into later validation. Historical labels that cannot prove source compatibility and availability timing must remain blocked or require adjudication.

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

Stage 2 implementation, Stage 3 scoring, Stage 4 paper simulation, Stage 5 dry run, Stage 6 runtime observation, and Stage 7 execution/trading remain unapproved.

## 4. Stage 2 design purpose

Source-compatible historical-label design defines the contract future labels must satisfy before they can be used for later evaluation. It is for specifying required fields, closed vocabularies, reviewer posture, provenance expectations, and blocking rules.

This document prepares for future source-compatible historical labels with point-in-time provenance, but it creates no labels. It is not an ingestion design, provider design, scoring design, runtime design, connector abstraction, forecast-pull design, model design, backtesting design, paper-simulation design, or trading design.

## 5. Historical-label design principles

Future Stage 2 historical labels must follow these principles:

- **Resolver-first truth:** the venue-defined resolver/source rule controls label truth.
- **Source compatibility before usability:** a label is not usable if the observed evidence does not match the venue-defined settlement source.
- **Station/location specificity:** station, observation point, city rule, or location text must be explicitly represented rather than inferred from convenience geography.
- **Measurement-window specificity:** start, end, timezone, local-day rule, and aggregation window must be represented.
- **Threshold/comparator/unit specificity:** threshold value, comparator, unit, rounding rule, and trace treatment must be explicit where applicable.
- **Revision/finality tracking:** preliminary, revised, final, archive, or discretionary finality layers must not be collapsed.
- **Classification authority tracking:** hurricane, storm, severe-weather, or other classification markets must identify the official authority that controls the resolved classification.
- **Point-in-time provenance:** source availability and observation availability must be tied to as-of reasoning.
- **No-lookahead protection:** labels must not use future facts at earlier decision times.
- **Trap-aware labeling:** ambiguity, wrong-source, wrong-window, stale-data, station mismatch, and discretionary-resolution traps must be representable.
- **Reviewer auditability:** every future label must be traceable to reviewer notes, source notes, adjudication posture, and evidence status.
- **No implementation without later approval:** this design does not authorize implementation, ingestion, provider integration, scoring, runtime behavior, or trading.

## 6. Closed Stage 2 historical-label design vocabulary

No other actual values are allowed for these fields. Hybrid, custom, or slash-combined values are forbidden as actual values. If a condition is mixed or partially supported, the single most conservative exact value must be selected and nuance must appear in notes or prose fields.

### historical label design stage

Allowed values:

- `stage_2_historical_label_design`

### historical label target type

Allowed values:

- `source_compatible_resolution_label`
- `source_compatible_nonresolution_label`
- `resolver_source_reference`
- `station_metadata_reference`
- `point_in_time_provenance_reference`
- `revision_finality_reference`
- `trap_annotation_reference`
- `other_unclear`

### provenance requirement

Allowed values:

- `required`
- `optional_for_context`
- `not_applicable`
- `missing_blocks_label`
- `unclear`

### point-in-time status

Allowed values:

- `required_before_label_use`
- `unavailable`
- `ambiguous`
- `not_applicable`
- `design_only`

### source compatibility status

Allowed values:

- `compatible`
- `incompatible`
- `unresolved`
- `requires_adjudication`
- `unknown`

### label usability posture

Allowed values:

- `design_only`
- `usable_after_stage_2_approval`
- `blocked_pending_source_match`
- `blocked_pending_provenance`
- `blocked_pending_adjudication`

### no-lookahead risk

Allowed values:

- `none_identified`
- `possible`
- `likely`
- `blocking`
- `unknown`

### stage 2 readiness posture

Allowed values:

- `design_only`
- `ready_for_future_label_planning`
- `blocked`
- `unclear`

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

## 7. Forbidden Stage 2 historical-label design values

The following examples may appear only as forbidden examples in prose, not as actual machine-checkable field values:

- `compatible/incompatible`
- `required/optional`
- `source_backed/reviewer_inferred`
- `confirmed/unclear`
- `possible/likely`
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

These examples are forbidden as actual values even when they seem descriptively convenient. Notes may explain nuance, but the machine-checkable value must remain one exact allowed value.

## Machine-checkable Stage 2 historical-label design assignments

- historical label design stage: stage_2_historical_label_design
- historical label target type: source_compatible_resolution_label
- historical label target type: source_compatible_nonresolution_label
- historical label target type: resolver_source_reference
- historical label target type: station_metadata_reference
- historical label target type: point_in_time_provenance_reference
- historical label target type: revision_finality_reference
- historical label target type: trap_annotation_reference
- historical label target type: other_unclear
- provenance requirement: required
- provenance requirement: optional_for_context
- provenance requirement: not_applicable
- provenance requirement: missing_blocks_label
- provenance requirement: unclear
- point-in-time status: required_before_label_use
- point-in-time status: unavailable
- point-in-time status: ambiguous
- point-in-time status: not_applicable
- point-in-time status: design_only
- source compatibility status: compatible
- source compatibility status: incompatible
- source compatibility status: unresolved
- source compatibility status: requires_adjudication
- source compatibility status: unknown
- label usability posture: design_only
- label usability posture: usable_after_stage_2_approval
- label usability posture: blocked_pending_source_match
- label usability posture: blocked_pending_provenance
- label usability posture: blocked_pending_adjudication
- no-lookahead risk: none_identified
- no-lookahead risk: possible
- no-lookahead risk: likely
- no-lookahead risk: blocking
- no-lookahead risk: unknown
- stage 2 readiness posture: design_only
- stage 2 readiness posture: ready_for_future_label_planning
- stage 2 readiness posture: blocked
- stage 2 readiness posture: unclear
- evidence status: source_backed
- evidence status: reviewer_inferred
- evidence status: missing
- evidence status: conflicting
- evidence status: not_applicable
- label confidence: confirmed
- label confidence: unclear
- label confidence: unknown

## 9. Future historical-label conceptual schema

This is a Markdown conceptual schema only. It does not create JSON/YAML/CSV schemas, Parquet layouts, data files, fixtures, loaders, provider connectors, or ingestion code.

| Conceptual field | Future design requirement |
| --- | --- |
| `historical_label_id` | Stable identifier for a future historical-label record, assigned only in a later approved label-creation ticket. |
| `linked_manual_label_id` | Link back to the Stage 1 manual-label concept when a future historical label derives from or validates a manual mapping. |
| `linked_trap_label_ids` | Links to relevant Stage 1 trap-label concepts for ambiguity, false-edge, or blocking risks. |
| `linked_adjudication_id` | Link to reviewer adjudication when source compatibility, evidence conflict, or confidence requires review. |
| `market_reference` | Human-readable market reference without routing or execution semantics. |
| `raw_market_wording` | Exact market wording or quoted settlement wording available to the reviewer. |
| `venue_defined_settlement_rule` | The settlement rule as stated by the venue, including source, station, window, threshold, revision, and classification conditions. |
| `market_family` | Weather market family, aligned with Stage 1 taxonomy where applicable. |
| `resolver_source_name` | Official resolver or source name used for settlement. |
| `resolver_source_role` | Role such as official resolver, station observation source, climate archive source, or venue discretionary resolver. |
| `resolver_source_url_or_reference` | Source URL or durable reference for the resolver/source identity. |
| `station_or_observation_point` | Station, observation point, named location, or authority-defined location used for settlement. |
| `station_metadata_reference` | Reference that supports station identity and metadata. |
| `location_text` | Location text from the market or settlement rule. |
| `geographic_precision_note` | Reviewer note on station/city/area ambiguity or precision. |
| `measurement_variable` | Temperature, precipitation, snowfall, wind gust, storm classification, or other settlement variable. |
| `threshold_value` | Numeric or categorical threshold from the market rule. |
| `threshold_unit` | Unit such as degrees, inches, mph, category, or not applicable. |
| `comparator` | Comparator such as greater-than, at-least, below, exactly, named classification, or not applicable. |
| `measurement_window_start` | Start of the settlement measurement window. |
| `measurement_window_end` | End of the settlement measurement window. |
| `timezone_or_local_day_rule` | Timezone, local-day interpretation, or authority-defined day rule. |
| `aggregation_method` | Maximum, minimum, total, average, first report, final report, classification state, or other method. |
| `revision_or_finality_rule` | Preliminary, revised, archive, final, or discretionary finality rule. |
| `classification_authority` | Authority controlling non-numeric classification labels when applicable. |
| `observed_resolution_value_reference` | Reference to the value or classification used for future source-compatible resolution truth. |
| `resolved_yes_no_or_unresolved` | Future resolved outcome state; unresolved and conflicting evidence must remain representable. |
| `label_confidence` | One exact value from the `label confidence` closed set. |
| `evidence_status` | One exact value from the `evidence status` closed set. |
| `source_compatibility_status` | One exact value from the `source compatibility status` closed set. |
| `point_in_time_status` | One exact value from the `point-in-time status` closed set. |
| `provenance_requirement` | One exact value from the `provenance requirement` closed set. |
| `no_lookahead_risk` | One exact value from the `no-lookahead risk` closed set. |
| `trap_annotations` | Trap-aware notes or links to trap labels. |
| `reviewer_notes` | Reviewer reasoning, cautions, and adjudication references. |
| `source_notes` | Source compatibility, source ambiguity, and source-finality notes. |
| `non_approval_notes` | Explicit reminder that the label record does not approve ingestion, scoring, runtime behavior, or execution. |

## 10. Point-in-time provenance requirements

Future labels must preserve point-in-time provenance sufficient to show what was knowable at the claimed as-of time. Future requirements include:

- **Source availability timestamp:** when the resolver/source reference was published or available.
- **Observation availability timestamp:** when the observation or classification value became available to a reviewer or future system.
- **Forecast/publication timestamp if applicable later:** if a later approved ticket uses forecast context, publication time must be distinguished from initialization time and availability time.
- **Market close timestamp:** the last market time relevant to any later scoring or evaluation claim.
- **Market resolution timestamp:** when the venue resolved or changed the market outcome.
- **Archive revision timestamp:** when revised or final archive values became available.
- **Station/source selection timestamp:** when the station/source mapping was selected, to prevent hindsight source selection.
- **Reviewer label timestamp:** when the reviewer made or changed the label decision.
- **As-of reasoning:** prose explaining which facts were available at the claimed decision time.
- **No final archive leakage:** final or revised archive values must not be treated as real-time truth before their availability timestamp.

Future labels must not use facts that were unavailable at the claimed decision time.

## 11. Source-compatible truth requirements

Source-compatible truth requirements define how future labels must handle settlement truth:

- **Official resolver source:** if the venue names an official resolver, future labels must prioritize that source for settlement truth.
- **Station observation source:** if the market resolves from a station or observation point, future labels must preserve station identity and metadata.
- **Climate archive source:** if an archive or climate product controls finality, future labels must track preliminary versus revised archive layers.
- **Venue discretionary resolver:** if the venue retains discretionary authority, future labels must represent that discretion and may require adjudication.
- **Source URL/reference:** future labels must include durable source references rather than unsupported memory or convenience provider output.
- **Station metadata:** station identity, location, naming changes, and observation-point ambiguity must be represented.
- **Revision/finality rule:** labels must identify the finality layer that the venue-defined settlement rule uses.
- **Classification authority:** classification markets must identify the authority that determines the classification.
- **Unresolved or conflicting sources:** unresolved or conflicting evidence must not be forced into confirmed Yes/No labels.
- **Unknown source treatment:** unknown source identity requires conservative posture, usually `unknown`, `requires_adjudication`, or a blocked usability posture depending on the field.

## 12. No-lookahead and leakage controls

No-lookahead and leakage controls are mandatory design constraints:

- No final observation before availability.
- No revised archive value treated as real-time truth.
- No future forecast cycles.
- No future market prices.
- No post-resolution labels before resolution time.
- No hindsight station/source choice.
- No provider selected after seeing outcomes.
- No threshold tuning using future outcomes.
- No convenience source substituted for a venue-defined source without explicit source-compatibility adjudication.
- No reviewer confidence upgrade without source-backed or reviewer-inferred evidence recorded in the label notes.

## 13. Label usability and blocking rules

Future labels must use one exact `label usability posture` value:

- `design_only`: the concept is documentation-only and not a usable historical label.
- `usable_after_stage_2_approval`: the label may become usable only after a later Stage 2 approval confirms source compatibility, provenance, and adjudication gates.
- `blocked_pending_source_match`: missing or incompatible source compatibility blocks label use.
- `blocked_pending_provenance`: missing point-in-time provenance blocks label use.
- `blocked_pending_adjudication`: unresolved reviewer or source conflict blocks label use.

Missing source compatibility blocks label use. Missing point-in-time provenance blocks label use. Unresolved adjudication blocks label use. Unclear or conflicting evidence requires the most conservative posture available in the closed set and explanatory notes.

## 14. Relationship to Stage 1 artifacts

Relationship to Stage 1 artifacts:

- Manual labels from `PRD-P1-WX-STAGE1-01` provide canonical mapping structure.
- Trap labels from `PRD-P1-WX-STAGE1-02` provide ambiguity and false-edge risk structure.
- The adjudication protocol from `PRD-P1-WX-STAGE1-03` provides reviewer decision structure.
- Seed examples from `PRD-P1-WX-STAGE1-04` provide static examples only.
- Stage 2 design must not mutate Stage 1 docs.
- Future Stage 2 labels should link back to Stage 1 label and adjudication concepts through conceptual identifiers such as `linked_manual_label_id`, `linked_trap_label_ids`, and `linked_adjudication_id`.

## 15. Relationship to Stage 3 scoring

Relationship to Stage 3 scoring:

- Stage 2 labels are prerequisites for future Stage 3 scoring.
- Stage 3 remains unapproved.
- Scoring must not begin until source-compatible historical labels exist and pass no-lookahead checks.
- Labels should be designed so that a later approved Stage 3 ticket can evaluate calibration, threshold-bucket behavior, and market-family splits.
- No scoring, probability scoring, model scoring, backtesting, paper simulation, forecast modeling, or runtime evaluation is implemented here.

## 16. Language/tooling posture

Stage 2 design remains Markdown plus Python static tests only. Python standard-library static validation is sufficient for this planning contract.

No C++/Rust or performance-oriented language is appropriate at this stage because there is no approved implementation stage, no profiled runtime hot path, and no approved runtime component. Python remains the default for future design/static validation. Any C++/Rust consideration requires a later approved implementation stage, profiling evidence, a proven hot path, and a separate safety review.

## 17. Non-approval boundaries for Stage 2 design

Stage 2 design does not approve:

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
- forecast pulls
- forecast modeling
- model scoring
- probability modeling
- probability scoring
- backtesting
- paper simulation
- runtime observation
- trading strategy
- trading
- position sizing
- order placement
- live market execution
- autonomy
- profitability claims
- C++/Rust runtime components

## 18. Later-ticket handoff

Later-ticket handoff:

- Future Stage 2 historical-label implementation or fixture creation may occur only after separate approval.
- Future point-in-time provenance examples may occur only after separate approval.
- Future ingestion design may occur only after separate approval.
- Future Stage 3 probability scoring may occur only after Stage 2 labels exist and pass source compatibility, provenance, adjudication, and no-lookahead gates.
- Any implementation-adjacent work must remain in later stages and requires explicit approval.

## 19. Acceptance criteria

This document is complete only if:

- [x] `PRD-P1-WX-STAGE2-01` canonical ID is present.
- [x] The standalone Weather Bot PRD is referenced.
- [x] Stage 1 closeout is referenced.
- [x] Stage 2 design scope is explicit.
- [x] Future historical-label conceptual schema is included.
- [x] Point-in-time provenance requirements are included.
- [x] Source-compatible truth requirements are included.
- [x] No-lookahead and leakage controls are included.
- [x] Label usability/blocking rules are included.
- [x] Relationship to Stage 1 artifacts is defined.
- [x] Relationship to Stage 3 scoring is defined without approving scoring.
- [x] Language/tooling posture is included.
- [x] All closed sets are listed exactly.
- [x] Machine-checkable assignment section exists.
- [x] Actual machine-checkable assignments use only allowed values.
- [x] Forbidden examples are documented without being used as actual field values.
- [x] Non-approval boundaries are explicit.
- [x] Later-ticket handoff is clear.
- [x] No implementation behavior is introduced.
