# WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-APPROVAL-REQUEST-01

Canonical ID: WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-APPROVAL-REQUEST-01

## Status and scope
This is a docs/static-test-only, approval-request-only artifact. It requests a human decision only and does not approve implementation.

## Immediate predecessor and merge verification
Immediate predecessor: pr_366.

ACTUAL_PR_366_MERGE_SHA: 24c229970392096dc8a61124f6e80ac724244a08

PR #366 merged at actual merge commit 24c229970392096dc8a61124f6e80ac724244a08, which is reachable from the current branch base. The former open-PR preview merge SHA 53822e5dc3115b7989c7f015c6120b9faa5a2a54 is not the actual merge commit and must not be used. No newer controlling Weather Bot artifact supersedes PR #366 for this approval-request scope.

## Approval-request purpose and decision boundary
This document requests a human decision only. This document does not approve implementation. No implementation work may begin because this document exists. A later implementation ticket requires an explicit human approval outside this document. The proposed slice is limited to one immutable in-memory binary probability-record boundary, accepts caller-supplied values only, and does not generate or infer any probability, determine scoring readiness, join labels, calculate a metric, establish evidence sufficiency, make or pass an evidence-gate decision, or approve persistence, reporting, runtime behavior, or trading. The target remains the venue-defined settlement outcome, not generic weather.

## Readiness-review basis
The PR #366 readiness review found the Stage 3 planning chain coherent enough only to request a separate human approval for one narrow implementation slice; it did not approve implementation or evidence-gate passage.

## Requested implementation slice identity
Requested future implementation slice: immutable_binary_outcome_probability_record_boundary.

The requested slice is limited to three future files, seven future public symbols, one frozen binary-outcome record shape, caller-supplied exact mappings, deterministic pure validation, and focused tests. It does not generate probabilities, execute models, read data, join labels, score records, create results or claims, evaluate an evidence gate, persist records, create reports, simulate markets, add runtime behavior, or trade.

## Exact future changed-file matrix
| Future file | Future action if separately approved | Permitted purpose | Prohibited expansion |
| --- | --- | --- | --- |
| meg/weather/stage3/__init__.py | create | declare the Stage 3 package boundary only | no imports with runtime side effects and no re-export of unrelated capabilities |
| meg/weather/stage3/binary_probability_record.py | create | define the immutable caller-supplied binary probability-record container and pure validation boundary | no probability generation, scoring, label joining, persistence, file access, service access, or runtime orchestration |
| tests/core/test_weather_bot_stage3_binary_probability_record.py | create | test only the approved immutable record and fail-closed validation boundary | no network, subprocess, Git, database, fixture mutation, environment dependency, or production execution |

No existing file may be modified by the later implementation slice.

## Exact future public-symbol matrix
| Future public symbol | Kind | Permitted responsibility | Explicit limit |
| --- | --- | --- | --- |
| PredictionRepresentation | string enum | expose only binary_outcome_probability for this initial slice | no full-distribution or ensemble implementation |
| ProbabilityRecordValidationSeverity | string enum | expose passed and blocked | no caution, approval, readiness, or evidence status |
| ProbabilityRecordValidationCode | string enum | expose the exact closed validation-code set defined in this request | no custom or dynamically generated code |
| BinaryOutcomeProbabilityRecord | frozen dataclass | hold one caller-supplied immutable binary probability record | no generated identity, timestamp, probability, derived routing replacement, or persistence behavior |
| ProbabilityRecordValidationResult | frozen dataclass | return severity, passed, and ordered validation codes | no scoring result, claim disposition, or evidence-gate meaning |
| binary_outcome_probability_record_from_mapping | pure function | adapt one exact caller-supplied mapping into the frozen record | no file reading, source fetching, implicit defaults, unknown-key tolerance, or probability generation |
| validate_binary_outcome_probability_record | pure function | validate one supplied record and return deterministic fail-closed codes | no mutation, normalization, scoring, label joining, persistence, or external access |

## Exact future record-field matrix
| Record field | Type posture | Requirement | Explicit limit |
| --- | --- | --- | --- |
| prediction_record_id | nonblank string | required and caller supplied | never generated |
| condition_id | nonblank string | required canonical routing field | never replaced by market_id or a derived identifier |
| token_id | nonblank string | required canonical routing field | never replaced by market_id or a derived identifier |
| outcome | nonblank string | required canonical routing field and predicted outcome identity | never inferred |
| settlement_rule_id | nonblank string | required venue-defined settlement-rule identity | not generic weather identity |
| settlement_rule_version | nonblank string | required caller-supplied version | no default version |
| prediction_as_of | timezone-aware ISO-8601 string | required prediction information cutoff | no naive timestamp |
| input_publication_available_at | timezone-aware ISO-8601 string | required legitimate input-availability time | must not be after prediction_as_of |
| market_family | nonblank string | required caller-supplied market-family identity | not market_id routing |
| threshold | nonblank string | required caller-supplied target threshold representation | no numeric interpretation in this slice |
| unit | nonblank string | required caller-supplied target unit | no conversion |
| comparator | nonblank string | required caller-supplied target comparator | no inferred comparator |
| measurement_window | nonblank string | required caller-supplied target window | no inferred window |
| source_compatibility_posture | nonblank string | required opaque upstream compatibility posture | no compatibility adjudication |
| station_compatibility_posture | nonblank string | required opaque upstream compatibility posture | no station lookup |
| archive_finality_layer | nonblank string | required expected verification-layer identity | no archive access |
| prediction_representation | PredictionRepresentation | must equal binary_outcome_probability | no hybrid or alternate representation |
| probability | finite Decimal | required in the closed interval from zero through one | no float coercion, normalization, clipping, or generation |
| method_id | nonblank string | required caller-supplied method identity | no model execution |
| method_version | nonblank string | required caller-supplied method version | no implicit version |
| provenance_refs | nonempty tuple of nonblank strings | required caller-supplied provenance references | no lookup or dereferencing |
| created_at | timezone-aware ISO-8601 string | required caller-supplied record-creation time | must not be before prediction_as_of |
| record_version | nonblank string | required caller-supplied record version | no automatic increment |
| supersedes_prediction_record_id | optional nonblank string | permitted only for explicit correction linkage | must not equal prediction_record_id |

## Exact mapping-input matrix
| Mapping boundary | Accepted posture | Rejected posture | Failure result |
| --- | --- | --- | --- |
| root value | Mapping with the exact approved key set | non-mapping roots, missing required keys, and any unexpected key | blocked with the corresponding exact validation code |
| probability input | Decimal or canonical base-ten string parsed with Decimal | bool, int, float, NaN, Infinity, signed Infinity, malformed text, implicit conversion, clipping, or normalization | blocked without creating an accepted record |
| prediction representation input | PredictionRepresentation.BINARY_OUTCOME_PROBABILITY or the exact string binary_outcome_probability | every other value, hybrid value, or custom value | blocked |
| provenance_refs input | nonempty tuple or list containing only nonblank strings | empty collection, scalar string, non-string entry, or blank entry | blocked |
| timestamp input | timezone-aware ISO-8601 strings accepted by the explicitly documented standard-library parser posture | naive, malformed, blank, or non-string timestamps | blocked |
| extra identifier input | no market_id and no token_outcome_pair key | either field supplied as an input key | blocked as unexpected_field |

## Exact validation-code matrix
| Validation code | Trigger | Severity | Ordering posture |
| --- | --- | --- | --- |
| missing_required_field | one or more required keys are absent | blocked | field-order deterministic |
| unexpected_field | one or more keys outside the exact approved set are present | blocked | lexical key order within this code |
| blank_required_text | a required text field is blank | blocked | record-field order |
| invalid_prediction_representation | representation is not binary_outcome_probability | blocked | fixed validation order |
| invalid_probability_type | probability input is not Decimal or canonical decimal text | blocked | fixed validation order |
| non_finite_probability | probability is NaN or infinite | blocked | fixed validation order |
| probability_out_of_range | finite probability is below zero or above one | blocked | fixed validation order |
| invalid_timestamp | a required timestamp is malformed or timezone-naive | blocked | prediction_as_of then input_publication_available_at then created_at |
| input_available_after_prediction | input_publication_available_at is later than prediction_as_of | blocked | fixed validation order |
| created_before_prediction | created_at is earlier than prediction_as_of | blocked | fixed validation order |
| empty_provenance_refs | provenance_refs is empty | blocked | fixed validation order |
| invalid_provenance_ref | a provenance entry is blank or non-string | blocked | entry order |
| self_supersession | supersedes_prediction_record_id equals prediction_record_id | blocked | fixed validation order |

## Exact validation-rule matrix
| Rule | Required behavior | Accepted result | Failure behavior |
| --- | --- | --- | --- |
| exact_mapping_shape | inspect the complete supplied key set before record construction | exact approved required keys plus the one optional supersedes key | return deterministic blocking codes without silently dropping keys |
| canonical_route | require nonblank condition_id, token_id, and outcome | all three supplied independently | never route by market_id or token_outcome_pair |
| settlement_target | require nonblank settlement-rule identity and version | explicit venue-defined target identity | never infer generic weather semantics |
| representation | require binary_outcome_probability | exact one-value representation posture | reject every alternate or hybrid representation |
| probability_domain | require a finite Decimal from zero through one inclusive | exact boundary values and interior finite values | reject type ambiguity, non-finite values, clipping, and out-of-range values |
| temporal_parse | parse all three timestamps as timezone-aware values | every timestamp valid and aware | block malformed or naive timestamps |
| input_availability | compare legitimate input availability with prediction_as_of | input availability is not later than prediction_as_of | block lookahead |
| creation_order | compare created_at with prediction_as_of | created_at is not earlier than prediction_as_of | block contradictory record chronology |
| required_text | require every required string to be nonblank | all required strings nonblank | return codes in record-field order |
| provenance | require at least one nonblank provenance reference | complete caller-supplied tuple | block missing or malformed provenance |
| immutability | construct frozen dataclasses only after successful adaptation | accepted record cannot be mutated | no setters or mutation helpers |
| correction_link | permit explicit supersession without self-reference | absent or different prior record identity | block self-supersession |
| deterministic_result | preserve exact validation-code ordering | same input produces equal result | no sets, nondeterministic iteration, or environment-dependent output |

## Exact future test matrix
Focused tests must use no services or runtime imports.

## Dependency and import boundary
Only dataclasses, datetime, decimal, enum, typing, and collections.abc when needed; no third-party or MEG production dependencies.

## Canonical routing and target boundary
Canonical routing is condition_id, token_id, and outcome; market_id is non-routing and token_outcome_pair is derived only. The target is venue-defined settlement outcome.

## Probability-domain boundary
Probability is caller-supplied finite Decimal in the closed unit interval; no coercion, clipping, normalization, or generation.

## Temporal availability and no-lookahead boundary
All timestamps are timezone-aware; input availability must not be after prediction and creation must not be before prediction.

## Provenance and immutability boundary
Provenance is caller supplied and immutable; no dereference, generated identity, or mutation is permitted.

## Failure posture and deterministic output
Validation is deterministic, pure, ordered, and fail closed.

## Explicit future implementation non-goals
The future slice may not create or perform probability generation; model execution; model loading; feature calculation; source fetching; provider connectors; file reading; file writing; fixture loading; fixture creation or modification; data acquisition; corpus expansion; split generation or execution; baseline calculation; metric calculation; calibration diagnostics; label joining; result-record creation; claim evaluation; claim-record creation; evidence-gate evaluation; decision-record creation; persistence; serialization formats; database tables; migrations; API endpoints; reports; exports; scheduling; queues; background tasks; runtime observation; simulation; paper trading; trading; order placement; autonomy; or production behavior.

## Approval decision options
| Human decision option | Meaning | Allowed next action |
| --- | --- | --- |
| approve_later_binary_probability_record_implementation_ticket | approve only the writing and execution of the exact later implementation ticket defined by this request | proceed only to WEATHER-BOT-STAGE3-BINARY-PROBABILITY-RECORD-IMPLEMENTATION-01 |
| request_approval_request_revision | require corrections to this document or its static test | update this approval-request PR only |
| hold | make no approval decision yet | create no implementation ticket |
| block | reject this requested slice in its current form | create no implementation ticket |

## Current request status
Request status: request_prepared_implementation_not_approved.

This document asks a human reviewer whether a later separate implementation ticket may create only the immutable_binary_outcome_probability_record_boundary defined here. No implementation is approved by this document, no production file may be created from this document alone, and no successor implementation ticket may begin without an explicit human approval outside this artifact.

## Human decision and separate-approval boundary
A human decision outside this document is required. The reviewer may approve a later ticket limited exactly to the requested slice, request revisions to this approval request, hold the sequence, or block the request. This document does not record its own approval and cannot convert request_prepared_implementation_not_approved into implementation approval. Any later implementation must remain limited to the exact future files, public symbols, fields, validation codes, rules, tests, dependencies, and non-goals recorded here.

## Fail-closed requirements
Fail closed for missing required field, unexpected field, blank required text, market_id input, token_outcome_pair input, unknown or hybrid representation, invalid probability type including bool, int, float, malformed decimal text, non-finite or out-of-range probability, malformed or timezone-naive timestamp, lookahead, contradictory creation order, empty or malformed provenance, self-supersession, nondeterministic ordering, implicit defaults, generated values, clipping, mutation, and scope expansion.

## Explicit non-approvals
This ticket does not approve or create the Stage 3 package; production modules; dataclasses; enums; validation functions; probability records; probability generation; model execution; feature calculation; source fetching; provider connectors; file access; fixture access; data acquisition; corpus expansion; split execution; baseline execution; scoring; diagnostics; label joining; evaluation results; claim evaluation; claim records; evidence-gate evaluation; decision records; persistence; serialization; database tables; migrations; APIs; reports; exports; scheduling; queues; background tasks; simulation; runtime observation; paper trading; trading; order placement; autonomy; runtime behavior; or production behavior.

## Canonical routing posture
Canonical routing fields remain exactly:

- condition_id
- token_id
- outcome

market_id is non-routing only.

token_outcome_pair is derived only.

## Recommended next ticket
WEATHER-BOT-STAGE3-BINARY-PROBABILITY-RECORD-IMPLEMENTATION-01

This ticket may be created only after an explicit human approval outside this approval-request artifact. If approved, it must remain limited exactly to the three proposed future files and the immutable_binary_outcome_probability_record_boundary. Without explicit human approval, no implementation ticket may be created.

## Machine-checkable assignments
Closed sets precede Actual assignments. Missing, duplicate, hybrid, reordered, extra, or custom fields and values are rejected.

- weather bot planning stage: weather_bot_stage3_retrospective_scoring_implementation_approval_request
- immediate predecessor pr: pr_366
- ticket lifecycle status: docs_static_test_only; approval_request_only
- request status: request_prepared; implementation_not_approved; human_decision_required
- requested implementation slice: immutable_binary_outcome_probability_record_boundary
- proposed future file: meg/weather/stage3/__init__.py; meg/weather/stage3/binary_probability_record.py; tests/core/test_weather_bot_stage3_binary_probability_record.py
- proposed future public symbol: PredictionRepresentation; ProbabilityRecordValidationSeverity; ProbabilityRecordValidationCode; BinaryOutcomeProbabilityRecord; ProbabilityRecordValidationResult; binary_outcome_probability_record_from_mapping; validate_binary_outcome_probability_record
- prediction representation: binary_outcome_probability
- scoring target posture: venue_defined_settlement_outcome
- mapping input posture: exact_key_set_only; caller_supplied_values_only; no_implicit_defaults
- probability domain: closed_unit_interval; finite_decimal_only
- temporal posture: timezone_aware_timestamps_required; input_availability_not_after_prediction; creation_not_before_prediction
- immutability posture: frozen_record_required; frozen_result_required; explicit_supersession_only
- approval decision posture: not_decided_in_document
- implementation approval posture: not_approved
- probability generation posture: not_approved
- scoring execution posture: not_approved
- label join posture: not_approved
- persistence posture: not_approved
- report export posture: not_approved
- canonical routing field: condition_id; token_id; outcome
- non routing field: market_id
- derived identifier field: token_outcome_pair
- next ticket recommendation: stage3_binary_probability_record_implementation
- evidence status: stage3_binary_probability_record_implementation_approval_request_recorded
- label confidence: confirmed

Actual assignments:
weather bot planning stage=weather_bot_stage3_retrospective_scoring_implementation_approval_request
immediate predecessor pr=pr_366

## Acceptance criteria
The artifact remains docs/static-test-only and approval-request-only; it preserves the exact requested slice, three future files, canonical routing, and human decision boundary.
