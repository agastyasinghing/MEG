"""Static, deterministic approval-request contract; no production imports."""
import ast
import re
from pathlib import Path

DOC = Path("docs/prd/WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-APPROVAL-REQUEST-01.md")
ALLOWLIST = Path("tests/core/canonical_id_allowlist.py")
CANONICAL_ID = "WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-APPROVAL-REQUEST-01"
ACTUAL_PR_366_MERGE_SHA = "24c229970392096dc8a61124f6e80ac724244a08"
PREVIEW_MERGE_SHA = "53822e5dc3115b7989c7f015c6120b9faa5a2a54"
EXPECTED_HEADINGS = ['Status and scope',
 'Immediate predecessor and merge verification',
 'Approval-request purpose and decision boundary',
 'Readiness-review basis',
 'Requested implementation slice identity',
 'Exact future changed-file matrix',
 'Exact future public-symbol matrix',
 'Exact future record-field matrix',
 'Exact mapping-input matrix',
 'Exact validation-code matrix',
 'Exact validation-rule matrix',
 'Exact future test matrix',
 'Dependency and import boundary',
 'Canonical routing and target boundary',
 'Probability-domain boundary',
 'Temporal availability and no-lookahead boundary',
 'Provenance and immutability boundary',
 'Failure posture and deterministic output',
 'Explicit future implementation non-goals',
 'Approval decision options',
 'Current request status',
 'Human decision and separate-approval boundary',
 'Fail-closed requirements',
 'Explicit non-approvals',
 'Canonical routing posture',
 'Recommended next ticket',
 'Machine-checkable assignments',
 'Acceptance criteria']
EXPECTED_EXACT_FUTURE_CHANGED_FILE_MATRIX = [['Future file', 'Future action if separately approved', 'Permitted purpose', 'Prohibited expansion'],
 ['---', '---', '---', '---'],
 ['meg/weather/stage3/__init__.py',
  'create',
  'declare the Stage 3 package boundary only',
  'no imports with runtime side effects and no re-export of unrelated capabilities'],
 ['meg/weather/stage3/binary_probability_record.py',
  'create',
  'define the immutable caller-supplied binary probability-record container and pure validation boundary',
  'no probability generation, scoring, label joining, persistence, file access, service access, or runtime orchestration'],
 ['tests/core/test_weather_bot_stage3_binary_probability_record.py',
  'create',
  'test only the approved immutable record and fail-closed validation boundary',
  'no network, subprocess, Git, database, fixture mutation, environment dependency, or production execution']]
EXPECTED_EXACT_FUTURE_PUBLIC_SYMBOL_MATRIX = [['Future public symbol', 'Kind', 'Permitted responsibility', 'Explicit limit'],
 ['---', '---', '---', '---'],
 ['PredictionRepresentation',
  'string enum',
  'expose only binary_outcome_probability for this initial slice',
  'no full-distribution or ensemble implementation'],
 ['ProbabilityRecordValidationSeverity', 'string enum', 'expose passed and blocked', 'no caution, approval, readiness, or evidence status'],
 ['ProbabilityRecordValidationCode',
  'string enum',
  'expose the exact closed validation-code set defined in this request',
  'no custom or dynamically generated code'],
 ['BinaryOutcomeProbabilityRecord',
  'frozen dataclass',
  'hold one caller-supplied immutable binary probability record',
  'no generated identity, timestamp, probability, derived routing replacement, or persistence behavior'],
 ['ProbabilityRecordValidationResult',
  'frozen dataclass',
  'return severity, passed, and ordered validation codes',
  'no scoring result, claim disposition, or evidence-gate meaning'],
 ['binary_outcome_probability_record_from_mapping',
  'pure function',
  'adapt one exact caller-supplied mapping into the frozen record',
  'no file reading, source fetching, implicit defaults, unknown-key tolerance, or probability generation'],
 ['validate_binary_outcome_probability_record',
  'pure function',
  'validate one supplied record and return deterministic fail-closed codes',
  'no mutation, normalization, scoring, label joining, persistence, or external access']]
EXPECTED_EXACT_FUTURE_RECORD_FIELD_MATRIX = [['Record field', 'Type posture', 'Requirement', 'Explicit limit'],
 ['---', '---', '---', '---'],
 ['prediction_record_id', 'nonblank string', 'required and caller supplied', 'never generated'],
 ['condition_id', 'nonblank string', 'required canonical routing field', 'never replaced by market_id or a derived identifier'],
 ['token_id', 'nonblank string', 'required canonical routing field', 'never replaced by market_id or a derived identifier'],
 ['outcome', 'nonblank string', 'required canonical routing field and predicted outcome identity', 'never inferred'],
 ['settlement_rule_id', 'nonblank string', 'required venue-defined settlement-rule identity', 'not generic weather identity'],
 ['settlement_rule_version', 'nonblank string', 'required caller-supplied version', 'no default version'],
 ['prediction_as_of', 'timezone-aware ISO-8601 string', 'required prediction information cutoff', 'no naive timestamp'],
 ['input_publication_available_at',
  'timezone-aware ISO-8601 string',
  'required legitimate input-availability time',
  'must not be after prediction_as_of'],
 ['market_family', 'nonblank string', 'required caller-supplied market-family identity', 'not market_id routing'],
 ['threshold', 'nonblank string', 'required caller-supplied target threshold representation', 'no numeric interpretation in this slice'],
 ['unit', 'nonblank string', 'required caller-supplied target unit', 'no conversion'],
 ['comparator', 'nonblank string', 'required caller-supplied target comparator', 'no inferred comparator'],
 ['measurement_window', 'nonblank string', 'required caller-supplied target window', 'no inferred window'],
 ['source_compatibility_posture', 'nonblank string', 'required opaque upstream compatibility posture', 'no compatibility adjudication'],
 ['station_compatibility_posture', 'nonblank string', 'required opaque upstream compatibility posture', 'no station lookup'],
 ['archive_finality_layer', 'nonblank string', 'required expected verification-layer identity', 'no archive access'],
 ['prediction_representation',
  'PredictionRepresentation',
  'must equal binary_outcome_probability',
  'no hybrid or alternate representation'],
 ['probability',
  'finite Decimal',
  'required in the closed interval from zero through one',
  'no float coercion, normalization, clipping, or generation'],
 ['method_id', 'nonblank string', 'required caller-supplied method identity', 'no model execution'],
 ['method_version', 'nonblank string', 'required caller-supplied method version', 'no implicit version'],
 ['provenance_refs', 'nonempty tuple of nonblank strings', 'required caller-supplied provenance references', 'no lookup or dereferencing'],
 ['created_at', 'timezone-aware ISO-8601 string', 'required caller-supplied record-creation time', 'must not be before prediction_as_of'],
 ['record_version', 'nonblank string', 'required caller-supplied record version', 'no automatic increment'],
 ['supersedes_prediction_record_id',
  'optional nonblank string',
  'permitted only for explicit correction linkage',
  'must not equal prediction_record_id']]
EXPECTED_EXACT_MAPPING_INPUT_MATRIX = [['Mapping boundary', 'Accepted posture', 'Rejected posture', 'Failure result'],
 ['---', '---', '---', '---'],
 ['root value',
  'Mapping with the exact approved key set',
  'non-mapping roots, missing required keys, and any unexpected key',
  'blocked with the corresponding exact validation code'],
 ['probability input',
  'Decimal or canonical base-ten string parsed with Decimal',
  'bool, int, float, NaN, Infinity, signed Infinity, malformed text, implicit conversion, clipping, or normalization',
  'blocked without creating an accepted record'],
 ['prediction representation input',
  'PredictionRepresentation.BINARY_OUTCOME_PROBABILITY or the exact string binary_outcome_probability',
  'every other value, hybrid value, or custom value',
  'blocked'],
 ['provenance_refs input',
  'nonempty tuple or list containing only nonblank strings',
  'empty collection, scalar string, non-string entry, or blank entry',
  'blocked'],
 ['timestamp input',
  'timezone-aware ISO-8601 strings accepted by the explicitly documented standard-library parser posture',
  'naive, malformed, blank, or non-string timestamps',
  'blocked'],
 ['extra identifier input',
  'no market_id and no token_outcome_pair key',
  'either field supplied as an input key',
  'blocked as unexpected_field']]
EXPECTED_EXACT_VALIDATION_CODE_MATRIX = [['Validation code', 'Trigger', 'Severity', 'Ordering posture'],
 ['---', '---', '---', '---'],
 ['missing_required_field', 'one or more required keys are absent', 'blocked', 'field-order deterministic'],
 ['unexpected_field', 'one or more keys outside the exact approved set are present', 'blocked', 'lexical key order within this code'],
 ['blank_required_text', 'a required text field is blank', 'blocked', 'record-field order'],
 ['invalid_prediction_representation', 'representation is not binary_outcome_probability', 'blocked', 'fixed validation order'],
 ['invalid_probability_type', 'probability input is not Decimal or canonical decimal text', 'blocked', 'fixed validation order'],
 ['non_finite_probability', 'probability is NaN or infinite', 'blocked', 'fixed validation order'],
 ['probability_out_of_range', 'finite probability is below zero or above one', 'blocked', 'fixed validation order'],
 ['invalid_timestamp',
  'a required timestamp is malformed or timezone-naive',
  'blocked',
  'prediction_as_of then input_publication_available_at then created_at'],
 ['input_available_after_prediction', 'input_publication_available_at is later than prediction_as_of', 'blocked', 'fixed validation order'],
 ['created_before_prediction', 'created_at is earlier than prediction_as_of', 'blocked', 'fixed validation order'],
 ['empty_provenance_refs', 'provenance_refs is empty', 'blocked', 'fixed validation order'],
 ['invalid_provenance_ref', 'a provenance entry is blank or non-string', 'blocked', 'entry order'],
 ['self_supersession', 'supersedes_prediction_record_id equals prediction_record_id', 'blocked', 'fixed validation order']]
EXPECTED_EXACT_VALIDATION_RULE_MATRIX = [['Rule', 'Required behavior', 'Accepted result', 'Failure behavior'],
 ['---', '---', '---', '---'],
 ['exact_mapping_shape',
  'inspect the complete supplied key set before record construction',
  'exact approved required keys plus the one optional supersedes key',
  'return deterministic blocking codes without silently dropping keys'],
 ['canonical_route',
  'require nonblank condition_id, token_id, and outcome',
  'all three supplied independently',
  'never route by market_id or token_outcome_pair'],
 ['settlement_target',
  'require nonblank settlement-rule identity and version',
  'explicit venue-defined target identity',
  'never infer generic weather semantics'],
 ['representation',
  'require binary_outcome_probability',
  'exact one-value representation posture',
  'reject every alternate or hybrid representation'],
 ['probability_domain',
  'require a finite Decimal from zero through one inclusive',
  'exact boundary values and interior finite values',
  'reject type ambiguity, non-finite values, clipping, and out-of-range values'],
 ['temporal_parse',
  'parse all three timestamps as timezone-aware values',
  'every timestamp valid and aware',
  'block malformed or naive timestamps'],
 ['input_availability',
  'compare legitimate input availability with prediction_as_of',
  'input availability is not later than prediction_as_of',
  'block lookahead'],
 ['creation_order',
  'compare created_at with prediction_as_of',
  'created_at is not earlier than prediction_as_of',
  'block contradictory record chronology'],
 ['required_text', 'require every required string to be nonblank', 'all required strings nonblank', 'return codes in record-field order'],
 ['provenance',
  'require at least one nonblank provenance reference',
  'complete caller-supplied tuple',
  'block missing or malformed provenance'],
 ['immutability',
  'construct frozen dataclasses only after successful adaptation',
  'accepted record cannot be mutated',
  'no setters or mutation helpers'],
 ['correction_link',
  'permit explicit supersession without self-reference',
  'absent or different prior record identity',
  'block self-supersession'],
 ['deterministic_result',
  'preserve exact validation-code ordering',
  'same input produces equal result',
  'no sets, nondeterministic iteration, or environment-dependent output']]
EXPECTED_EXACT_FUTURE_TEST_MATRIX = [['Future test group', 'Required coverage', 'Prohibited shortcut'],
 ['---', '---', '---'],
 ['import boundary', 'module imports with standard library only', 'no service, database, runtime, provider, or Stage 2 loader import'],
 ['package boundary', 'Stage 3 package has no import side effects', 'no startup or registration behavior'],
 ['accepted record',
  'one complete valid caller-supplied mapping creates a frozen record and passed result',
  'no fixture or file dependency'],
 ['exact mapping keys', 'missing and unexpected keys fail with exact ordered codes', 'no permissive get-based defaults'],
 ['canonical routing', 'missing route fields fail and market_id or token_outcome_pair inputs are rejected', 'no substring-only assertion'],
 ['representation', 'only binary_outcome_probability is accepted', 'no alternate representation accepted'],
 ['probability boundaries', 'exact zero and exact one pass', 'no approximate comparison'],
 ['probability failures',
  'below-zero, above-one, malformed, bool, int, float, NaN, and Infinity fail as specified',
  'no silent Decimal coercion from float'],
 ['timestamp parsing', 'aware valid timestamps pass and naive or malformed values fail', 'no system-time dependency'],
 ['no-lookahead', 'input availability after prediction fails', 'no current-time comparison'],
 ['creation ordering', 'created_at before prediction fails', 'no current-time comparison'],
 ['provenance', 'empty, scalar, blank, and non-string entries fail', 'no implicit tuple creation from scalar text'],
 ['immutability', 'frozen record and result reject mutation', 'no custom mutator'],
 ['correction linkage', 'self-supersession fails and distinct supersession passes', 'no generated predecessor identity'],
 ['deterministic codes', 'multiple failures return the exact expected code order', 'no set or sorted substitute'],
 ['non-goals',
  'source contains no file, network, database, persistence, scoring, label-join, report, simulation, trading, or runtime behavior',
  'no broad keyword-only substitute without AST/import inspection']]
EXPECTED_APPROVAL_DECISION_OPTIONS = [['Human decision option', 'Meaning', 'Allowed next action'],
 ['---', '---', '---'],
 ['approve_later_binary_probability_record_implementation_ticket',
  'approve only the writing and execution of the exact later implementation ticket defined by this request',
  'proceed only to WEATHER-BOT-STAGE3-BINARY-PROBABILITY-RECORD-IMPLEMENTATION-01'],
 ['request_approval_request_revision', 'require corrections to this document or its static test', 'update this approval-request PR only'],
 ['hold', 'make no approval decision yet', 'create no implementation ticket'],
 ['block', 'reject this requested slice in its current form', 'create no implementation ticket']]
EXPECTED_CRITICAL_SECTIONS = {'Immediate predecessor and merge verification': 'Immediate predecessor: pr_366.\n'
                                                 '\n'
                                                 'ACTUAL_PR_366_MERGE_SHA: 24c229970392096dc8a61124f6e80ac724244a08\n'
                                                 '\n'
                                                 'PR #366 merged at actual merge commit 24c229970392096dc8a61124f6e80ac724244a08, which is '
                                                 'reachable from the current branch base. The former open-PR preview merge SHA '
                                                 '53822e5dc3115b7989c7f015c6120b9faa5a2a54 is not the actual merge commit and must not be '
                                                 'used. No newer controlling Weather Bot artifact supersedes PR #366 for this '
                                                 'approval-request scope.',
 'Requested implementation slice identity': 'Requested future implementation slice: immutable_binary_outcome_probability_record_boundary.\n'
                                            '\n'
                                            'The requested slice is limited to three future files, seven future public symbols, one frozen '
                                            'binary-outcome record shape, caller-supplied exact mappings, deterministic pure validation, '
                                            'and focused tests. It does not generate probabilities, execute models, read data, join '
                                            'labels, score records, create results or claims, evaluate an evidence gate, persist records, '
                                            'create reports, simulate markets, add runtime behavior, or trade.',
 'Current request status': 'Request status: request_prepared_implementation_not_approved.\n'
                           '\n'
                           'This document asks a human reviewer whether a later separate implementation ticket may create only the '
                           'immutable_binary_outcome_probability_record_boundary defined here. No implementation is approved by this '
                           'document, no production file may be created from this document alone, and no successor implementation ticket '
                           'may begin without an explicit human approval outside this artifact.',
 'Human decision and separate-approval boundary': 'A human decision outside this document is required. The reviewer may approve a later '
                                                  'ticket limited exactly to the requested slice, request revisions to this approval '
                                                  'request, hold the sequence, or block the request. This document does not record its own '
                                                  'approval and cannot convert request_prepared_implementation_not_approved into '
                                                  'implementation approval. Any later implementation must remain limited to the exact '
                                                  'future files, public symbols, fields, validation codes, rules, tests, dependencies, and '
                                                  'non-goals recorded here.',
 'Explicit non-approvals': 'This ticket does not approve or create the Stage 3 package; production modules; dataclasses; enums; validation '
                           'functions; probability records; probability generation; model execution; feature calculation; source fetching; '
                           'provider connectors; file access; fixture access; data acquisition; corpus expansion; split execution; '
                           'baseline execution; scoring; diagnostics; label joining; evaluation results; claim evaluation; claim records; '
                           'evidence-gate evaluation; decision records; persistence; serialization; database tables; migrations; APIs; '
                           'reports; exports; scheduling; queues; background tasks; simulation; runtime observation; paper trading; '
                           'trading; order placement; autonomy; runtime behavior; or production behavior.',
 'Canonical routing posture': 'Canonical routing fields remain exactly:\n'
                              '\n'
                              '- condition_id\n'
                              '- token_id\n'
                              '- outcome\n'
                              '\n'
                              'market_id is non-routing only.\n'
                              '\n'
                              'token_outcome_pair is derived only.',
 'Recommended next ticket': 'WEATHER-BOT-STAGE3-BINARY-PROBABILITY-RECORD-IMPLEMENTATION-01\n'
                            '\n'
                            'This ticket may be created only after an explicit human approval outside this approval-request artifact. If '
                            'approved, it must remain limited exactly to the three proposed future files and the '
                            'immutable_binary_outcome_probability_record_boundary. Without explicit human approval, no implementation '
                            'ticket may be created.'}
EXPECTED_CLOSED_SETS = {'weather bot planning stage': ['weather_bot_stage3_retrospective_scoring_implementation_approval_request'],
 'immediate predecessor pr': ['pr_366'],
 'ticket lifecycle status': ['docs_static_test_only', 'approval_request_only'],
 'request status': ['request_prepared', 'implementation_not_approved', 'human_decision_required'],
 'requested implementation slice': ['immutable_binary_outcome_probability_record_boundary'],
 'proposed future file': ['meg/weather/stage3/__init__.py',
                          'meg/weather/stage3/binary_probability_record.py',
                          'tests/core/test_weather_bot_stage3_binary_probability_record.py'],
 'proposed future public symbol': ['PredictionRepresentation',
                                   'ProbabilityRecordValidationSeverity',
                                   'ProbabilityRecordValidationCode',
                                   'BinaryOutcomeProbabilityRecord',
                                   'ProbabilityRecordValidationResult',
                                   'binary_outcome_probability_record_from_mapping',
                                   'validate_binary_outcome_probability_record'],
 'prediction representation': ['binary_outcome_probability'],
 'scoring target posture': ['venue_defined_settlement_outcome'],
 'mapping input posture': ['exact_key_set_only', 'caller_supplied_values_only', 'no_implicit_defaults'],
 'probability domain': ['closed_unit_interval', 'finite_decimal_only'],
 'temporal posture': ['timezone_aware_timestamps_required', 'input_availability_not_after_prediction', 'creation_not_before_prediction'],
 'immutability posture': ['frozen_record_required', 'frozen_result_required', 'explicit_supersession_only'],
 'approval decision posture': ['not_decided_in_document'],
 'implementation approval posture': ['not_approved'],
 'probability generation posture': ['not_approved'],
 'scoring execution posture': ['not_approved'],
 'label join posture': ['not_approved'],
 'persistence posture': ['not_approved'],
 'report export posture': ['not_approved'],
 'canonical routing field': ['condition_id', 'token_id', 'outcome'],
 'non routing field': ['market_id'],
 'derived identifier field': ['token_outcome_pair'],
 'next ticket recommendation': ['stage3_binary_probability_record_implementation'],
 'evidence status': ['stage3_binary_probability_record_implementation_approval_request_recorded'],
 'label confidence': ['confirmed']}
EXPECTED_REMAINING_SECTION_BODIES = {'Status and scope': 'This is a docs/static-test-only, approval-request-only artifact. It requests a human decision only and does not '
                     'approve implementation.',
 'Approval-request purpose and decision boundary': 'This document requests a human decision only. This document does not approve '
                                                   'implementation. No implementation work may begin because this document exists. A later '
                                                   'implementation ticket requires an explicit human approval outside this document. The '
                                                   'proposed slice is limited to one immutable in-memory binary probability-record '
                                                   'boundary, accepts caller-supplied values only, and does not generate or infer any '
                                                   'probability, determine scoring readiness, join labels, calculate a metric, establish '
                                                   'evidence sufficiency, make or pass an evidence-gate decision, or approve persistence, '
                                                   'reporting, runtime behavior, or trading. The target remains the venue-defined '
                                                   'settlement outcome, not generic weather. No existing file may be modified by the later '
                                                   'implementation slice.',
 'Readiness-review basis': 'The PR #366 readiness review found the Stage 3 planning chain coherent enough only to request a separate human '
                           'approval for one narrow implementation slice; it did not approve implementation or evidence-gate passage.',
 'Dependency and import boundary': 'Only dataclasses, datetime, decimal, enum, typing, and collections.abc when needed; no third-party or '
                                   'MEG production dependencies.',
 'Canonical routing and target boundary': 'Canonical routing is condition_id, token_id, and outcome; market_id is non-routing and '
                                          'token_outcome_pair is derived only. The target is venue-defined settlement outcome.',
 'Probability-domain boundary': 'Probability is caller-supplied finite Decimal in the closed unit interval; no coercion, clipping, '
                                'normalization, or generation.',
 'Temporal availability and no-lookahead boundary': 'All timestamps are timezone-aware; input availability must not be after prediction '
                                                    'and creation must not be before prediction.',
 'Provenance and immutability boundary': 'Provenance is caller supplied and immutable; no dereference, generated identity, or mutation is '
                                         'permitted.',
 'Failure posture and deterministic output': 'Validation is deterministic, pure, ordered, and fail closed.',
 'Explicit future implementation non-goals': 'The future slice may not create or perform probability generation; model execution; model '
                                             'loading; feature calculation; source fetching; provider connectors; file reading; file '
                                             'writing; fixture loading; fixture creation or modification; data acquisition; corpus '
                                             'expansion; split generation or execution; baseline calculation; metric calculation; '
                                             'calibration diagnostics; label joining; result-record creation; claim evaluation; '
                                             'claim-record creation; evidence-gate evaluation; decision-record creation; persistence; '
                                             'serialization formats; database tables; migrations; API endpoints; reports; exports; '
                                             'scheduling; queues; background tasks; runtime observation; simulation; paper trading; '
                                             'trading; order placement; autonomy; or production behavior.',
 'Fail-closed requirements': 'Fail closed for missing required field, unexpected field, blank required text, market_id input, '
                             'token_outcome_pair input, unknown or hybrid representation, invalid probability type including bool, int, '
                             'float, malformed decimal text, non-finite or out-of-range probability, malformed or timezone-naive '
                             'timestamp, lookahead, contradictory creation order, empty or malformed provenance, self-supersession, '
                             'nondeterministic ordering, implicit defaults, generated values, clipping, mutation, and scope expansion.',
 'Acceptance criteria': 'The artifact remains docs/static-test-only and approval-request-only; it preserves the exact requested slice, '
                        'three future files, canonical routing, and human decision boundary.'}
EXACT_TABLE_SECTION_HEADINGS = ['Exact future changed-file matrix',
 'Exact future public-symbol matrix',
 'Exact future record-field matrix',
 'Exact mapping-input matrix',
 'Exact validation-code matrix',
 'Exact validation-rule matrix',
 'Exact future test matrix',
 'Approval decision options']
EXACT_CRITICAL_SECTION_HEADINGS = ['Immediate predecessor and merge verification',
 'Requested implementation slice identity',
 'Current request status',
 'Human decision and separate-approval boundary',
 'Explicit non-approvals',
 'Canonical routing posture',
 'Recommended next ticket']
EXACT_REMAINING_SECTION_HEADINGS = ['Status and scope',
 'Approval-request purpose and decision boundary',
 'Readiness-review basis',
 'Dependency and import boundary',
 'Canonical routing and target boundary',
 'Probability-domain boundary',
 'Temporal availability and no-lookahead boundary',
 'Provenance and immutability boundary',
 'Failure posture and deterministic output',
 'Explicit future implementation non-goals',
 'Fail-closed requirements',
 'Acceptance criteria']
MACHINE_SECTION_HEADINGS = ['Machine-checkable assignments']
EXPECTED_ASSIGNMENTS = ['- weather bot planning stage: weather_bot_stage3_retrospective_scoring_implementation_approval_request',
 '- immediate predecessor pr: pr_366',
 '- ticket lifecycle status: docs_static_test_only',
 '- ticket lifecycle status: approval_request_only',
 '- request status: request_prepared',
 '- request status: implementation_not_approved',
 '- request status: human_decision_required',
 '- requested implementation slice: immutable_binary_outcome_probability_record_boundary',
 '- proposed future file: meg/weather/stage3/__init__.py',
 '- proposed future file: meg/weather/stage3/binary_probability_record.py',
 '- proposed future file: tests/core/test_weather_bot_stage3_binary_probability_record.py',
 '- proposed future public symbol: PredictionRepresentation',
 '- proposed future public symbol: ProbabilityRecordValidationSeverity',
 '- proposed future public symbol: ProbabilityRecordValidationCode',
 '- proposed future public symbol: BinaryOutcomeProbabilityRecord',
 '- proposed future public symbol: ProbabilityRecordValidationResult',
 '- proposed future public symbol: binary_outcome_probability_record_from_mapping',
 '- proposed future public symbol: validate_binary_outcome_probability_record',
 '- prediction representation: binary_outcome_probability',
 '- scoring target posture: venue_defined_settlement_outcome',
 '- mapping input posture: exact_key_set_only',
 '- mapping input posture: caller_supplied_values_only',
 '- mapping input posture: no_implicit_defaults',
 '- probability domain: closed_unit_interval',
 '- probability domain: finite_decimal_only',
 '- temporal posture: timezone_aware_timestamps_required',
 '- temporal posture: input_availability_not_after_prediction',
 '- temporal posture: creation_not_before_prediction',
 '- immutability posture: frozen_record_required',
 '- immutability posture: frozen_result_required',
 '- immutability posture: explicit_supersession_only',
 '- approval decision posture: not_decided_in_document',
 '- implementation approval posture: not_approved',
 '- probability generation posture: not_approved',
 '- scoring execution posture: not_approved',
 '- label join posture: not_approved',
 '- persistence posture: not_approved',
 '- report export posture: not_approved',
 '- canonical routing field: condition_id',
 '- canonical routing field: token_id',
 '- canonical routing field: outcome',
 '- non routing field: market_id',
 '- derived identifier field: token_outcome_pair',
 '- next ticket recommendation: stage3_binary_probability_record_implementation',
 '- evidence status: stage3_binary_probability_record_implementation_approval_request_recorded',
 '- label confidence: confirmed']
REJECTION_SENTENCE = 'Missing, duplicate, hybrid, reordered, extra, or custom fields and values are rejected.'
REQUIRED_CHECK_CODES = ['header_exact',
 'heading_sequence_exact',
 'section_nonempty',
 'predecessor_exact',
 'slice_identity_exact',
 'future_file_matrix_exact',
 'public_symbol_matrix_exact',
 'record_field_matrix_exact',
 'mapping_input_matrix_exact',
 'validation_code_matrix_exact',
 'validation_rule_matrix_exact',
 'future_test_matrix_exact',
 'decision_options_exact',
 'critical_sections_exact',
 'closed_sets_exact',
 'assignments_exact',
 'rejection_sentence_exact',
 'numeric_policy_clean',
 'allowlist_counts_exact',
 'oracle_literals_exact',
 'prohibited_behavior_absent']
REQUIRED_MUTATION_CASES = ['canonical_id_line_three_suffix',
 'duplicate_canonical_id',
 'adjacent_heading_swap',
 'future_file_path_changed',
 'future_file_complete_row_duplicated',
 'future_file_complete_row_removed',
 'public_symbol_adjacent_rows_swapped',
 'unknown_public_symbol',
 'record_field_blocks_reordered',
 'record_field_complete_row_duplicated',
 'record_field_complete_row_removed',
 'probability_type_posture_changed',
 'market_id_added_as_mapping_input',
 'token_outcome_pair_added_as_mapping_input',
 'unknown_validation_code',
 'validation_code_complete_row_duplicated',
 'validation_rule_adjacent_rows_swapped',
 'future_test_shortcut_changed',
 'predecessor_actual_replaced_by_preview',
 'predecessor_correct_and_preview_both_actual',
 'predecessor_actual_declaration_duplicated',
 'predecessor_negative_language_inverted',
 'slice_identity_expanded_to_scoring',
 'current_status_changed_to_implementation_approved',
 'human_decision_changed_to_self_approved',
 'non_approval_language_inverted',
 'routing_market_id_inserted',
 'successor_substituted',
 'closed_set_complete_blocks_reordered',
 'closed_set_value_duplicated',
 'actual_assignment_duplicated',
 'actual_assignment_malformed',
 'rejection_sentence_altered',
 'rejection_sentence_removed',
 'fabricated_percentage_policy',
 'fabricated_scientific_tolerance',
 'fabricated_integer_bin_requirement']

NUMERIC_TOKEN = re.compile(r"(?<![A-Za-z0-9_])(?:\d+\.\d*|\.\d+|\d+(?:[eE][+-]?\d+)?)(?:%)?(?![A-Za-z0-9_])")
ASSIGNMENT_RE = re.compile(r"- ([^:\n]+): ([^\n]+)")
FIELD_RE = re.compile(r"- ([^:\n]+):")
VALUE_RE = re.compile(r"  - ([^\n]+)")

class ContractCheckError(AssertionError):
    def __init__(self, check_code: str):
        self.check_code = check_code
        super().__init__(check_code)

def _require(condition: bool, check_code: str):
    if not condition:
        raise ContractCheckError(check_code)

def _read() -> str:
    return DOC.read_text()

def _section(text: str, name: str) -> str:
    marker = "## " + name
    _require(text.count(marker) == 1, "section_nonempty")
    start = text.index(marker) + len(marker)
    end = text.find("\n## ", start)
    body = text[start:end if end >= 0 else len(text)].strip()
    _require(body != "", "section_nonempty")
    return body

def _table_rows(text: str, name: str) -> list[list[str]]:
    body = _section(text, name)
    lines = body.splitlines()
    parsed = []
    for line in lines:
        _require(line.startswith("|") and line.endswith("|"), "section_nonempty")
        parsed.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return parsed

def _table(text: str, name: str, expected: list[list[str]], code: str):
    body = _section(text, name)
    lines = body.splitlines()
    _require(lines != [], code)
    _require(all(line.startswith("|") and line.endswith("|") for line in lines), code)
    parsed = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    _require(parsed == expected, code)
    _require(all(len(row) == len(expected[0]) for row in parsed), code)

def _machine_body(text: str) -> str:
    return _section(text, "Machine-checkable assignments")

def _split_machine(text: str):
    body = _machine_body(text)
    delimiter = "\n\nActual assignments:\n\n"
    _require(body.count(delimiter) == 1, "closed_sets_exact")
    closed_part, rest = body.split(delimiter, 1)
    return closed_part, rest

def _parse_closed_sets(text: str):
    closed_part, rest = _split_machine(text)
    _require(closed_part.splitlines()[0] == "Closed sets:", "closed_sets_exact")
    _require("Actual assignments:" not in closed_part, "closed_sets_exact")
    _require(rest != "", "closed_sets_exact")
    parsed = {}
    current = None
    field_seen = []
    value_seen = {}
    for line in closed_part.splitlines()[1:]:
        field_match = FIELD_RE.fullmatch(line)
        value_match = VALUE_RE.fullmatch(line)
        if field_match:
            field = field_match.group(1)
            _require(field.strip() == field and field != "", "closed_sets_exact")
            _require(field not in parsed, "closed_sets_exact")
            parsed[field] = []
            value_seen[field] = []
            field_seen.append(field)
            current = field
        elif value_match:
            _require(current is not None, "closed_sets_exact")
            value = value_match.group(1)
            _require(value.strip() == value and value != "", "closed_sets_exact")
            _require(value not in value_seen[current], "closed_sets_exact")
            parsed[current].append(value)
            value_seen[current].append(value)
        else:
            raise ContractCheckError("closed_sets_exact")
    _require(all(parsed[field] for field in field_seen), "closed_sets_exact")
    return parsed

def _parse_actual_assignments(text: str):
    body = _machine_body(text)
    delimiter = "\n\nActual assignments:\n\n"
    _require(body.count(delimiter) == 1, "assignments_exact")
    after = body.split(delimiter, 1)[1]
    lines_after = after.splitlines()
    boundary = len(lines_after)
    for index, line in enumerate(lines_after):
        if line == "":
            boundary = index
            break
    assignment_lines = lines_after[:boundary]
    _require(assignment_lines != [], "assignments_exact")
    seen = []
    for line in assignment_lines:
        match = ASSIGNMENT_RE.fullmatch(line)
        _require(match is not None, "assignments_exact")
        field, value = match.group(1), match.group(2)
        _require(field.strip() == field and value.strip() == value and field != "" and value != "", "assignments_exact")
        _require(line not in seen, "assignments_exact")
        seen.append(line)
    return assignment_lines

def _parse_rejection_tail(text: str) -> str:
    body = _machine_body(text)
    delimiter = "\n\nActual assignments:\n\n"
    _require(body.count(delimiter) == 1, "rejection_sentence_exact")
    after = body.split(delimiter, 1)[1]
    lines = after.splitlines()
    index = 0
    while index < len(lines) and ASSIGNMENT_RE.fullmatch(lines[index]):
        index += 1
    _require(index < len(lines) and lines[index] == "", "rejection_sentence_exact")
    tail = "\n".join(lines[index + 1:])
    return tail

def _flatten_closed_sets(parsed):
    flattened = []
    for field, values in parsed.items():
        for value in values:
            flattened.append("- " + field + ": " + value)
    return flattened

def header_exact(text: str):
    lines = text.splitlines()
    expected = ["# " + CANONICAL_ID, "", "Canonical ID: " + CANONICAL_ID]
    _require(lines[:3] == expected, "header_exact")
    _require(text.count("Canonical ID: " + CANONICAL_ID) == 1, "header_exact")

def heading_sequence_exact(text: str):
    _require([line[3:] for line in text.splitlines() if line.startswith("## ")] == EXPECTED_HEADINGS, "heading_sequence_exact")

def section_nonempty(text: str):
    for heading in EXPECTED_HEADINGS:
        _section(text, heading)

def predecessor_exact(text: str):
    body = _section(text, "Immediate predecessor and merge verification")
    expected = EXPECTED_CRITICAL_SECTIONS["Immediate predecessor and merge verification"]
    _require(body == expected, "predecessor_exact")
    declaration = "ACTUAL_PR_366_MERGE_SHA: " + ACTUAL_PR_366_MERGE_SHA
    prose = "PR #366 merged at actual merge commit " + ACTUAL_PR_366_MERGE_SHA
    negative = PREVIEW_MERGE_SHA + " is not the actual merge commit"
    _require(body.count(declaration) == 1, "predecessor_exact")
    _require(body.count(prose) == 1, "predecessor_exact")
    _require(body.count(negative) == 1, "predecessor_exact")
    _require(("ACTUAL_PR_366_MERGE_SHA: " + PREVIEW_MERGE_SHA) not in body, "predecessor_exact")
    _require(ACTUAL_PR_366_MERGE_SHA != PREVIEW_MERGE_SHA, "predecessor_exact")

def slice_identity_exact(text: str):
    _require(_section(text, "Requested implementation slice identity") == EXPECTED_CRITICAL_SECTIONS["Requested implementation slice identity"], "slice_identity_exact")

def future_file_matrix_exact(text: str):
    _table(text, "Exact future changed-file matrix", EXPECTED_EXACT_FUTURE_CHANGED_FILE_MATRIX, "future_file_matrix_exact")

def public_symbol_matrix_exact(text: str):
    _table(text, "Exact future public-symbol matrix", EXPECTED_EXACT_FUTURE_PUBLIC_SYMBOL_MATRIX, "public_symbol_matrix_exact")

def record_field_matrix_exact(text: str):
    _table(text, "Exact future record-field matrix", EXPECTED_EXACT_FUTURE_RECORD_FIELD_MATRIX, "record_field_matrix_exact")

def mapping_input_matrix_exact(text: str):
    _table(text, "Exact mapping-input matrix", EXPECTED_EXACT_MAPPING_INPUT_MATRIX, "mapping_input_matrix_exact")

def validation_code_matrix_exact(text: str):
    _table(text, "Exact validation-code matrix", EXPECTED_EXACT_VALIDATION_CODE_MATRIX, "validation_code_matrix_exact")

def validation_rule_matrix_exact(text: str):
    _table(text, "Exact validation-rule matrix", EXPECTED_EXACT_VALIDATION_RULE_MATRIX, "validation_rule_matrix_exact")

def future_test_matrix_exact(text: str):
    _table(text, "Exact future test matrix", EXPECTED_EXACT_FUTURE_TEST_MATRIX, "future_test_matrix_exact")

def decision_options_exact(text: str):
    _table(text, "Approval decision options", EXPECTED_APPROVAL_DECISION_OPTIONS, "decision_options_exact")

def critical_sections_exact(text: str):
    for name, expected in EXPECTED_CRITICAL_SECTIONS.items():
        _require(_section(text, name) == expected, "critical_sections_exact")

def closed_sets_exact(text: str):
    parsed = _parse_closed_sets(text)
    _require(parsed == EXPECTED_CLOSED_SETS, "closed_sets_exact")
    _require(list(parsed) == list(EXPECTED_CLOSED_SETS), "closed_sets_exact")
    for field in EXPECTED_CLOSED_SETS:
        _require(parsed[field] == EXPECTED_CLOSED_SETS[field], "closed_sets_exact")

def assignments_exact(text: str):
    parsed_assignments = _parse_actual_assignments(text)
    parsed_closed_sets = _parse_closed_sets(text)
    _require(parsed_assignments == EXPECTED_ASSIGNMENTS, "assignments_exact")
    _require(_flatten_closed_sets(parsed_closed_sets) == EXPECTED_ASSIGNMENTS, "assignments_exact")

def rejection_sentence_exact(text: str):
    _require(text.count(REJECTION_SENTENCE) == 1, "rejection_sentence_exact")
    _require(_parse_rejection_tail(text) == REJECTION_SENTENCE, "rejection_sentence_exact")

def numeric_policy_clean(text: str):
    examples = ["12", "12.", ".5", "0.25", "90%", "1e-6"]
    _require(all(NUMERIC_TOKEN.fullmatch(value) for value in examples), "numeric_policy_clean")
    scanned = [
        _section(text, "Failure posture and deterministic output"),
        _section(text, "Fail-closed requirements"),
        _section(text, "Acceptance criteria"),
    ]
    for body in scanned:
        scrubbed = re.sub(r"(?m)^\d+\.\s+", "", body)
        _require(NUMERIC_TOKEN.search(scrubbed) is None, "numeric_policy_clean")

def _allowlist_literal_values():
    tree = ast.parse(ALLOWLIST.read_text())
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "ALLOWED_MARKET_ID_OCCURRENCE_LINES":
            return ast.literal_eval(node.value.args[0])
    raise ContractCheckError("allowlist_counts_exact")

def _downstream_artifacts():
    tree = ast.parse(ALLOWLIST.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "_ARCH_ALIGN_03_DOWNSTREAM_ARTIFACTS":
            _require(isinstance(node.value, ast.Set), "allowlist_counts_exact")
            artifacts = []
            for element in node.value.elts:
                _require(isinstance(element, ast.Constant) and isinstance(element.value, str), "allowlist_counts_exact")
                artifacts.append(element.value)
            return artifacts
    raise ContractCheckError("allowlist_counts_exact")

def allowlist_counts_exact(text: str):
    values = _allowlist_literal_values()
    doc_path = DOC.as_posix()
    test_path = Path(__file__).relative_to(Path.cwd()).as_posix()
    for path in [doc_path, test_path]:
        direct = sum("market_id" in line for line in Path(path).read_text().splitlines())
        _require(values[path] == direct, "allowlist_counts_exact")
    artifacts = list(_downstream_artifacts())
    _require(artifacts.count(doc_path) == 1, "allowlist_counts_exact")
    _require(artifacts.count(test_path) == 1, "allowlist_counts_exact")
    readiness_doc = "docs/prd/WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-READINESS-REVIEW-01.md"
    readiness_test = "tests/core/test_weather_bot_stage3_retrospective_scoring_implementation_readiness_review_01.py"
    index = artifacts.index(readiness_doc)
    _require(artifacts[index:index + 4] == [readiness_doc, readiness_test, doc_path, test_path], "allowlist_counts_exact")
    _require(values["tests/core/test_prd_p1_wx_stage2_source_fetching_implementation_approval_request_01.py"] == 1, "allowlist_counts_exact")

def _assignment_for(tree: ast.Module, name: str):
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id == name:
            return node.value
    raise ContractCheckError("oracle_literals_exact")

def _reject_oracle_constructs(node: ast.AST, oracle_names: list[str]):
    forbidden = (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp, ast.Call, ast.Attribute, ast.Subscript, ast.BinOp, ast.JoinedStr, ast.FormattedValue)
    for child in ast.walk(node):
        _require(not isinstance(child, forbidden), "oracle_literals_exact")
        if isinstance(child, ast.Name):
            _require(child.id not in oracle_names, "oracle_literals_exact")

def _literal_string_list(node: ast.AST) -> bool:
    return isinstance(node, (ast.List, ast.Tuple)) and all(isinstance(item, ast.Constant) and isinstance(item.value, str) for item in node.elts)

def _literal_matrix(node: ast.AST) -> bool:
    return isinstance(node, ast.List) and all(_literal_string_list(row) for row in node.elts)

def oracle_literals_exact(text: str):
    tree = ast.parse(Path(__file__).read_text())
    oracle_names = [
        "EXPECTED_HEADINGS",
        "EXPECTED_EXACT_FUTURE_CHANGED_FILE_MATRIX",
        "EXPECTED_EXACT_FUTURE_PUBLIC_SYMBOL_MATRIX",
        "EXPECTED_EXACT_FUTURE_RECORD_FIELD_MATRIX",
        "EXPECTED_EXACT_MAPPING_INPUT_MATRIX",
        "EXPECTED_EXACT_VALIDATION_CODE_MATRIX",
        "EXPECTED_EXACT_VALIDATION_RULE_MATRIX",
        "EXPECTED_EXACT_FUTURE_TEST_MATRIX",
        "EXPECTED_APPROVAL_DECISION_OPTIONS",
        "EXPECTED_CRITICAL_SECTIONS",
        "EXPECTED_CLOSED_SETS",
        "EXPECTED_REMAINING_SECTION_BODIES",
        "EXACT_TABLE_SECTION_HEADINGS",
        "EXACT_CRITICAL_SECTION_HEADINGS",
        "EXACT_REMAINING_SECTION_HEADINGS",
        "MACHINE_SECTION_HEADINGS",
        "EXPECTED_ASSIGNMENTS",
        "REJECTION_SENTENCE",
        "REQUIRED_CHECK_CODES",
        "REQUIRED_MUTATION_CASES",
    ]
    matrices = oracle_names[1:9]
    for name in oracle_names:
        node = _assignment_for(tree, name)
        _reject_oracle_constructs(node, oracle_names)
    _require(_literal_string_list(_assignment_for(tree, "EXPECTED_HEADINGS")), "oracle_literals_exact")
    for name in matrices:
        _require(_literal_matrix(_assignment_for(tree, name)), "oracle_literals_exact")
    _require(_literal_string_list(_assignment_for(tree, "EXPECTED_ASSIGNMENTS")), "oracle_literals_exact")
    _require(_literal_string_list(_assignment_for(tree, "REQUIRED_CHECK_CODES")), "oracle_literals_exact")
    _require(_literal_string_list(_assignment_for(tree, "REQUIRED_MUTATION_CASES")), "oracle_literals_exact")
    critical_node = _assignment_for(tree, "EXPECTED_CRITICAL_SECTIONS")
    _require(isinstance(critical_node, ast.Dict), "oracle_literals_exact")
    for key, value in zip(critical_node.keys, critical_node.values):
        _require(isinstance(key, ast.Constant) and isinstance(key.value, str), "oracle_literals_exact")
        _require(isinstance(value, ast.Constant) and isinstance(value.value, str), "oracle_literals_exact")
    closed_node = _assignment_for(tree, "EXPECTED_CLOSED_SETS")
    _require(isinstance(closed_node, ast.Dict), "oracle_literals_exact")
    for key, value in zip(closed_node.keys, closed_node.values):
        _require(isinstance(key, ast.Constant) and isinstance(key.value, str), "oracle_literals_exact")
        _require(_literal_string_list(value), "oracle_literals_exact")
    remaining_node = _assignment_for(tree, "EXPECTED_REMAINING_SECTION_BODIES")
    _require(isinstance(remaining_node, ast.Dict), "oracle_literals_exact")
    for key, value in zip(remaining_node.keys, remaining_node.values):
        _require(isinstance(key, ast.Constant) and isinstance(key.value, str), "oracle_literals_exact")
        _require(isinstance(value, ast.Constant) and isinstance(value.value, str), "oracle_literals_exact")
    for name in ["EXACT_TABLE_SECTION_HEADINGS", "EXACT_CRITICAL_SECTION_HEADINGS", "EXACT_REMAINING_SECTION_HEADINGS", "MACHINE_SECTION_HEADINGS"]:
        _require(_literal_string_list(_assignment_for(tree, name)), "oracle_literals_exact")
    _validate_heading_partition("oracle_literals_exact")
    rejection_node = _assignment_for(tree, "REJECTION_SENTENCE")
    _require(isinstance(rejection_node, ast.Constant) and isinstance(rejection_node.value, str), "oracle_literals_exact")

def _validate_heading_partition(check_code: str):
    _require(EXACT_CRITICAL_SECTION_HEADINGS == list(EXPECTED_CRITICAL_SECTIONS), check_code)
    _require(EXACT_REMAINING_SECTION_HEADINGS == list(EXPECTED_REMAINING_SECTION_BODIES), check_code)
    _require(EXACT_TABLE_SECTION_HEADINGS == [
        "Exact future changed-file matrix",
        "Exact future public-symbol matrix",
        "Exact future record-field matrix",
        "Exact mapping-input matrix",
        "Exact validation-code matrix",
        "Exact validation-rule matrix",
        "Exact future test matrix",
        "Approval decision options",
    ], check_code)
    _require(MACHINE_SECTION_HEADINGS == ["Machine-checkable assignments"], check_code)
    categories = EXACT_TABLE_SECTION_HEADINGS + EXACT_CRITICAL_SECTION_HEADINGS + EXACT_REMAINING_SECTION_HEADINGS + MACHINE_SECTION_HEADINGS
    projected = [heading for heading in EXPECTED_HEADINGS if heading in categories]
    _require(projected == EXPECTED_HEADINGS, check_code)
    _require(len(categories) == len(EXPECTED_HEADINGS), check_code)
    _require(all(categories.count(heading) == 1 for heading in EXPECTED_HEADINGS), check_code)
    _require(all(heading in EXPECTED_HEADINGS for heading in categories), check_code)

def _audit_static_test_source(source: str):
    tree = ast.parse(source)
    allowed_imports = {"ast", "re", "pathlib"}
    forbidden_import_roots = {"sub" + "process", "os", "socket", "requests", "urllib", "http", "meg"}
    dangerous_calls = {"system", "popen", "run", "check_call", "check_output", "getenv", "environ", "urlopen", "request", "connect", "__import__"}
    command_patterns = [
        r"^\s*git\s+(?:status|fetch|checkout|branch|log|show|rev-parse|merge-base|cat-file|diff|ls-files)\b",
        r"^\s*gh\s+(?:pr|api|issue|workflow|run|repo)\b",
    ]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                _require(root in allowed_imports and root not in forbidden_import_roots, "prohibited_behavior_absent")
        if isinstance(node, ast.ImportFrom):
            _require(node.module is not None, "prohibited_behavior_absent")
            root = node.module.split(".")[0]
            _require(root in allowed_imports and root not in forbidden_import_roots, "prohibited_behavior_absent")
        if isinstance(node, ast.Name):
            _require(node.id not in {"environ", "getenv"}, "prohibited_behavior_absent")
        if isinstance(node, ast.Subscript):
            value = node.value
            _require(not (isinstance(value, ast.Name) and value.id == "environ"), "prohibited_behavior_absent")
            _require(not (isinstance(value, ast.Attribute) and value.attr == "environ"), "prohibited_behavior_absent")
        if isinstance(node, ast.Call):
            function = node.func
            if isinstance(function, ast.Name):
                _require(function.id not in dangerous_calls, "prohibited_behavior_absent")
            if isinstance(function, ast.Attribute):
                _require(function.attr not in dangerous_calls, "prohibited_behavior_absent")
        if isinstance(node, ast.Attribute):
            _require(node.attr not in dangerous_calls, "prohibited_behavior_absent")
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            lowered = node.value.lower()
            _require(("." + "git") not in lowered, "prohibited_behavior_absent")
            for pattern in command_patterns:
                _require(re.search(pattern, lowered) is None, "prohibited_behavior_absent")

def prohibited_behavior_absent(text: str):
    _validate_heading_partition("prohibited_behavior_absent")
    for name, expected in EXPECTED_REMAINING_SECTION_BODIES.items():
        _require(_section(text, name) == expected, "prohibited_behavior_absent")
    _audit_static_test_source(Path(__file__).read_text())

VALIDATORS = {
    "header_exact": header_exact,
    "heading_sequence_exact": heading_sequence_exact,
    "section_nonempty": section_nonempty,
    "predecessor_exact": predecessor_exact,
    "slice_identity_exact": slice_identity_exact,
    "future_file_matrix_exact": future_file_matrix_exact,
    "public_symbol_matrix_exact": public_symbol_matrix_exact,
    "record_field_matrix_exact": record_field_matrix_exact,
    "mapping_input_matrix_exact": mapping_input_matrix_exact,
    "validation_code_matrix_exact": validation_code_matrix_exact,
    "validation_rule_matrix_exact": validation_rule_matrix_exact,
    "future_test_matrix_exact": future_test_matrix_exact,
    "decision_options_exact": decision_options_exact,
    "critical_sections_exact": critical_sections_exact,
    "closed_sets_exact": closed_sets_exact,
    "assignments_exact": assignments_exact,
    "rejection_sentence_exact": rejection_sentence_exact,
    "numeric_policy_clean": numeric_policy_clean,
    "allowlist_counts_exact": allowlist_counts_exact,
    "oracle_literals_exact": oracle_literals_exact,
    "prohibited_behavior_absent": prohibited_behavior_absent,
}
PIPELINE = [
    "header_exact",
    "heading_sequence_exact",
    "section_nonempty",
    "predecessor_exact",
    "slice_identity_exact",
    "future_file_matrix_exact",
    "public_symbol_matrix_exact",
    "record_field_matrix_exact",
    "mapping_input_matrix_exact",
    "validation_code_matrix_exact",
    "validation_rule_matrix_exact",
    "future_test_matrix_exact",
    "decision_options_exact",
    "critical_sections_exact",
    "closed_sets_exact",
    "assignments_exact",
    "rejection_sentence_exact",
    "numeric_policy_clean",
    "allowlist_counts_exact",
    "oracle_literals_exact",
    "prohibited_behavior_absent",
]

def validate(text: str):
    for code in PIPELINE:
        VALIDATORS[code](text)

def _replace_once(text: str, old: str, new: str) -> str:
    _require(text.count(old) == 1, "section_nonempty")
    return text.replace(old, new, 1)

def _replace_section_body(text: str, name: str, new_body: str) -> str:
    marker = "## " + name
    start = text.index(marker) + len(marker)
    end = text.find("\n## ", start)
    stop = end if end >= 0 else len(text)
    return text[:start] + "\n" + new_body.strip() + "\n" + text[stop:]

def _duplicate_table_row(text: str, heading: str, row_index: int) -> str:
    body = _section(text, heading)
    lines = body.splitlines()
    row = lines[row_index]
    lines.insert(row_index + 1, row)
    return _replace_section_body(text, heading, "\n".join(lines))

def _remove_table_row(text: str, heading: str, row_index: int) -> str:
    body = _section(text, heading)
    lines = body.splitlines()
    del lines[row_index]
    return _replace_section_body(text, heading, "\n".join(lines))

def _swap_table_rows(text: str, heading: str, first_index: int) -> str:
    body = _section(text, heading)
    lines = body.splitlines()
    lines[first_index], lines[first_index + 1] = lines[first_index + 1], lines[first_index]
    return _replace_section_body(text, heading, "\n".join(lines))

def _change_table_cell(text: str, heading: str, row_index: int, cell_index: int, new_value: str) -> str:
    rows = _table_rows(text, heading)
    rows[row_index][cell_index] = new_value
    lines = ["| " + " | ".join(row) + " |" for row in rows]
    return _replace_section_body(text, heading, "\n".join(lines))

def _critical_sections_equal_except(base: str, mutated: str, affected: list[str]):
    for name in EXPECTED_CRITICAL_SECTIONS:
        if name not in affected:
            _require(_section(base, name) == _section(mutated, name), "section_nonempty")

def _all_tables_equal_except(base: str, mutated: str, affected_heading: str):
    tables = {
        "Exact future changed-file matrix": EXPECTED_EXACT_FUTURE_CHANGED_FILE_MATRIX,
        "Exact future public-symbol matrix": EXPECTED_EXACT_FUTURE_PUBLIC_SYMBOL_MATRIX,
        "Exact future record-field matrix": EXPECTED_EXACT_FUTURE_RECORD_FIELD_MATRIX,
        "Exact mapping-input matrix": EXPECTED_EXACT_MAPPING_INPUT_MATRIX,
        "Exact validation-code matrix": EXPECTED_EXACT_VALIDATION_CODE_MATRIX,
        "Exact validation-rule matrix": EXPECTED_EXACT_VALIDATION_RULE_MATRIX,
        "Exact future test matrix": EXPECTED_EXACT_FUTURE_TEST_MATRIX,
        "Approval decision options": EXPECTED_APPROVAL_DECISION_OPTIONS,
    }
    for heading in tables:
        if heading != affected_heading:
            _require(_table_rows(base, heading) == _table_rows(mutated, heading), "section_nonempty")

def _assert_changed(base: str, mutated: str):
    _require(mutated != base, "section_nonempty")

def _assert_header_case(base: str, mutated: str):
    _assert_changed(base, mutated)
    _require(mutated.splitlines()[0] == base.splitlines()[0], "section_nonempty")
    _critical_sections_equal_except(base, mutated, [])

def _assert_table_duplicate(base: str, mutated: str, heading: str, row_index: int):
    before = _table_rows(base, heading)
    after = _table_rows(mutated, heading)
    row = before[row_index]
    _require(before.count(row) == 1, "section_nonempty")
    _require(after.count(row) == 2, "section_nonempty")
    _require(len(after) == len(before) + 1, "section_nonempty")
    expected = before[:row_index + 1] + [row] + before[row_index + 1:]
    _require(after == expected, "section_nonempty")
    _all_tables_equal_except(base, mutated, heading)
    _critical_sections_equal_except(base, mutated, [])

def _assert_table_removed(base: str, mutated: str, heading: str, row_index: int):
    before = _table_rows(base, heading)
    after = _table_rows(mutated, heading)
    row = before[row_index]
    _require(before.count(row) == 1, "section_nonempty")
    _require(row not in after, "section_nonempty")
    _require(len(after) == len(before) - 1, "section_nonempty")
    expected = before[:row_index] + before[row_index + 1:]
    _require(after == expected, "section_nonempty")
    _all_tables_equal_except(base, mutated, heading)
    _critical_sections_equal_except(base, mutated, [])

def _assert_table_swapped(base: str, mutated: str, heading: str, first_index: int):
    before = _table_rows(base, heading)
    after = _table_rows(mutated, heading)
    expected = before[:]
    expected[first_index], expected[first_index + 1] = expected[first_index + 1], expected[first_index]
    _require(after == expected, "section_nonempty")
    _require(len(after) == len(before), "section_nonempty")
    _all_tables_equal_except(base, mutated, heading)
    _critical_sections_equal_except(base, mutated, [])

def _assert_table_cell_changed(base: str, mutated: str, heading: str, row_index: int, cell_index: int, new_value: str):
    before = _table_rows(base, heading)
    after = _table_rows(mutated, heading)
    expected = [row[:] for row in before]
    expected[row_index][cell_index] = new_value
    _require(after == expected, "section_nonempty")
    _all_tables_equal_except(base, mutated, heading)
    _critical_sections_equal_except(base, mutated, [])

def _assert_critical_mutation(base: str, mutated: str, affected: str):
    _assert_changed(base, mutated)
    _critical_sections_equal_except(base, mutated, [affected])
    _require(_section(base, affected) != _section(mutated, affected), "section_nonempty")

def _assert_closed_sets_unchanged(base: str, mutated: str):
    _require(_parse_closed_sets(base) == _parse_closed_sets(mutated), "section_nonempty")

def _assert_assignments_unchanged(base: str, mutated: str):
    _require(_parse_actual_assignments(base) == _parse_actual_assignments(mutated), "section_nonempty")

def _assert_matrices_critical_machine_unchanged(base: str, mutated: str):
    for heading in ["Exact future changed-file matrix", "Exact future public-symbol matrix", "Exact future record-field matrix", "Exact mapping-input matrix", "Exact validation-code matrix", "Exact validation-rule matrix", "Exact future test matrix", "Approval decision options"]:
        _require(_table_rows(base, heading) == _table_rows(mutated, heading), "section_nonempty")
    _critical_sections_equal_except(base, mutated, [])
    _assert_closed_sets_unchanged(base, mutated)
    _assert_assignments_unchanged(base, mutated)

# Mutators and structural proofs.

def _mutate_canonical_id_line_three_suffix(text: str) -> str:
    lines = text.splitlines()
    lines[2] = lines[2] + "-MUTATED"
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")

def _assert_canonical_id_line_three_suffix(base: str, mutated: str):
    _assert_header_case(base, mutated)
    _require(mutated.splitlines()[2] == base.splitlines()[2] + "-MUTATED", "section_nonempty")

def _mutate_duplicate_canonical_id(text: str) -> str:
    return _replace_once(text, "Canonical ID: " + CANONICAL_ID, "Canonical ID: " + CANONICAL_ID + "\nCanonical ID: " + CANONICAL_ID)

def _assert_duplicate_canonical_id(base: str, mutated: str):
    _assert_header_case(base, mutated)
    _require(mutated.count("Canonical ID: " + CANONICAL_ID) == 2, "section_nonempty")

def _mutate_adjacent_heading_swap(text: str) -> str:
    lines = text.splitlines()
    indices = [index for index, line in enumerate(lines) if line.startswith("## ")]
    lines[indices[0]], lines[indices[1]] = lines[indices[1]], lines[indices[0]]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")

def _assert_adjacent_heading_swap(base: str, mutated: str):
    _assert_changed(base, mutated)
    base_lines = base.splitlines()
    mutated_lines = mutated.splitlines()
    base_indices = [index for index, line in enumerate(base_lines) if line.startswith("## ")]
    _require(mutated_lines[base_indices[0]] == base_lines[base_indices[1]], "section_nonempty")
    _require(mutated_lines[base_indices[1]] == base_lines[base_indices[0]], "section_nonempty")
    for index, line in enumerate(base_lines):
        if index not in base_indices[:2]:
            _require(mutated_lines[index] == line, "section_nonempty")

def _mutate_future_file_path_changed(text: str) -> str:
    return _change_table_cell(text, 'Exact future changed-file matrix', 2, 0, 'meg/weather/stage3/altered.py')

def _assert_future_file_path_changed(base: str, mutated: str):
    _assert_table_cell_changed(base, mutated, 'Exact future changed-file matrix', 2, 0, 'meg/weather/stage3/altered.py')

def _mutate_future_file_complete_row_duplicated(text: str) -> str:
    return _duplicate_table_row(text, 'Exact future changed-file matrix', 2)

def _assert_future_file_complete_row_duplicated(base: str, mutated: str):
    _assert_table_duplicate(base, mutated, 'Exact future changed-file matrix', 2)

def _mutate_future_file_complete_row_removed(text: str) -> str:
    return _remove_table_row(text, 'Exact future changed-file matrix', 2)

def _assert_future_file_complete_row_removed(base: str, mutated: str):
    _assert_table_removed(base, mutated, 'Exact future changed-file matrix', 2)

def _mutate_public_symbol_adjacent_rows_swapped(text: str) -> str:
    return _swap_table_rows(text, 'Exact future public-symbol matrix', 2)

def _assert_public_symbol_adjacent_rows_swapped(base: str, mutated: str):
    _assert_table_swapped(base, mutated, 'Exact future public-symbol matrix', 2)

def _mutate_unknown_public_symbol(text: str) -> str:
    return _change_table_cell(text, 'Exact future public-symbol matrix', 2, 0, 'UnknownPublicSymbol')

def _assert_unknown_public_symbol(base: str, mutated: str):
    _assert_table_cell_changed(base, mutated, 'Exact future public-symbol matrix', 2, 0, 'UnknownPublicSymbol')

def _mutate_record_field_blocks_reordered(text: str) -> str:
    return _swap_table_rows(text, 'Exact future record-field matrix', 2)

def _assert_record_field_blocks_reordered(base: str, mutated: str):
    _assert_table_swapped(base, mutated, 'Exact future record-field matrix', 2)

def _mutate_record_field_complete_row_duplicated(text: str) -> str:
    return _duplicate_table_row(text, 'Exact future record-field matrix', 2)

def _assert_record_field_complete_row_duplicated(base: str, mutated: str):
    _assert_table_duplicate(base, mutated, 'Exact future record-field matrix', 2)

def _mutate_record_field_complete_row_removed(text: str) -> str:
    return _remove_table_row(text, 'Exact future record-field matrix', 2)

def _assert_record_field_complete_row_removed(base: str, mutated: str):
    _assert_table_removed(base, mutated, 'Exact future record-field matrix', 2)

def _mutate_probability_type_posture_changed(text: str) -> str:
    return _change_table_cell(text, 'Exact future record-field matrix', 19, 1, 'finite float')

def _assert_probability_type_posture_changed(base: str, mutated: str):
    _assert_table_cell_changed(base, mutated, 'Exact future record-field matrix', 19, 1, 'finite float')

def _mutate_market_id_added_as_mapping_input(text: str) -> str:
    return _change_table_cell(text, 'Exact mapping-input matrix', 2, 1, 'Mapping with the exact approved key set plus market_id')

def _assert_market_id_added_as_mapping_input(base: str, mutated: str):
    _assert_table_cell_changed(base, mutated, 'Exact mapping-input matrix', 2, 1, 'Mapping with the exact approved key set plus market_id')

def _mutate_token_outcome_pair_added_as_mapping_input(text: str) -> str:
    return _change_table_cell(text, 'Exact mapping-input matrix', 2, 1, 'Mapping with the exact approved key set plus token_outcome_pair')

def _assert_token_outcome_pair_added_as_mapping_input(base: str, mutated: str):
    _assert_table_cell_changed(base, mutated, 'Exact mapping-input matrix', 2, 1, 'Mapping with the exact approved key set plus token_outcome_pair')

def _mutate_unknown_validation_code(text: str) -> str:
    return _change_table_cell(text, 'Exact validation-code matrix', 2, 0, 'unknown_validation_code')

def _assert_unknown_validation_code(base: str, mutated: str):
    _assert_table_cell_changed(base, mutated, 'Exact validation-code matrix', 2, 0, 'unknown_validation_code')

def _mutate_validation_code_complete_row_duplicated(text: str) -> str:
    return _duplicate_table_row(text, 'Exact validation-code matrix', 2)

def _assert_validation_code_complete_row_duplicated(base: str, mutated: str):
    _assert_table_duplicate(base, mutated, 'Exact validation-code matrix', 2)

def _mutate_validation_rule_adjacent_rows_swapped(text: str) -> str:
    return _swap_table_rows(text, 'Exact validation-rule matrix', 2)

def _assert_validation_rule_adjacent_rows_swapped(base: str, mutated: str):
    _assert_table_swapped(base, mutated, 'Exact validation-rule matrix', 2)

def _mutate_future_test_shortcut_changed(text: str) -> str:
    return _change_table_cell(text, 'Exact future test matrix', 2, 2, 'shortcut accepted')

def _assert_future_test_shortcut_changed(base: str, mutated: str):
    _assert_table_cell_changed(base, mutated, 'Exact future test matrix', 2, 2, 'shortcut accepted')

def _mutate_predecessor_actual_replaced_by_preview(text: str) -> str:
    return _replace_section_body(text, "Immediate predecessor and merge verification", _section(text, "Immediate predecessor and merge verification").replace(ACTUAL_PR_366_MERGE_SHA, PREVIEW_MERGE_SHA))

def _assert_predecessor_actual_replaced_by_preview(base: str, mutated: str):
    _assert_critical_mutation(base, mutated, "Immediate predecessor and merge verification")
    _require(_section(mutated, "Immediate predecessor and merge verification").count("ACTUAL_PR_366_MERGE_SHA: " + PREVIEW_MERGE_SHA) == 1, "section_nonempty")

def _mutate_predecessor_correct_and_preview_both_actual(text: str) -> str:
    return _replace_once(text, "ACTUAL_PR_366_MERGE_SHA: " + ACTUAL_PR_366_MERGE_SHA, "ACTUAL_PR_366_MERGE_SHA: " + ACTUAL_PR_366_MERGE_SHA + "\nACTUAL_PR_366_MERGE_SHA: " + PREVIEW_MERGE_SHA)

def _assert_predecessor_correct_and_preview_both_actual(base: str, mutated: str):
    _assert_critical_mutation(base, mutated, "Immediate predecessor and merge verification")
    body = _section(mutated, "Immediate predecessor and merge verification")
    _require(body.count("ACTUAL_PR_366_MERGE_SHA: " + ACTUAL_PR_366_MERGE_SHA) == 1, "section_nonempty")
    _require(body.count("ACTUAL_PR_366_MERGE_SHA: " + PREVIEW_MERGE_SHA) == 1, "section_nonempty")

def _mutate_predecessor_actual_declaration_duplicated(text: str) -> str:
    return _replace_once(text, "ACTUAL_PR_366_MERGE_SHA: " + ACTUAL_PR_366_MERGE_SHA, "ACTUAL_PR_366_MERGE_SHA: " + ACTUAL_PR_366_MERGE_SHA + "\nACTUAL_PR_366_MERGE_SHA: " + ACTUAL_PR_366_MERGE_SHA)

def _assert_predecessor_actual_declaration_duplicated(base: str, mutated: str):
    _assert_critical_mutation(base, mutated, "Immediate predecessor and merge verification")
    _require(_section(mutated, "Immediate predecessor and merge verification").count("ACTUAL_PR_366_MERGE_SHA: " + ACTUAL_PR_366_MERGE_SHA) == 2, "section_nonempty")

def _mutate_predecessor_negative_language_inverted(text: str) -> str:
    return _replace_once(text, "is not the actual merge commit", "is the actual merge commit")

def _assert_predecessor_negative_language_inverted(base: str, mutated: str):
    _assert_critical_mutation(base, mutated, "Immediate predecessor and merge verification")
    _require(PREVIEW_MERGE_SHA + " is the actual merge commit" in _section(mutated, "Immediate predecessor and merge verification"), "section_nonempty")

def _mutate_slice_identity_expanded_to_scoring(text: str) -> str:
    return _replace_once(text, "or trade.", "or trade. It also approves scoring.")

def _assert_slice_identity_expanded_to_scoring(base: str, mutated: str):
    _assert_critical_mutation(base, mutated, "Requested implementation slice identity")
    _require("approves scoring" in _section(mutated, "Requested implementation slice identity"), "section_nonempty")

def _mutate_current_status_changed_to_implementation_approved(text: str) -> str:
    return _replace_once(text, "Request status: request_prepared_implementation_not_approved.", "Request status: implementation_approved.")

def _assert_current_status_changed_to_implementation_approved(base: str, mutated: str):
    _assert_critical_mutation(base, mutated, "Current request status")
    _require("Request status: implementation_approved." in _section(mutated, "Current request status"), "section_nonempty")

def _mutate_human_decision_changed_to_self_approved(text: str) -> str:
    return _replace_once(text, "A human decision outside this document is required.", "This document records its own implementation approval.")

def _assert_human_decision_changed_to_self_approved(base: str, mutated: str):
    _assert_critical_mutation(base, mutated, "Human decision and separate-approval boundary")
    _require("records its own implementation approval" in _section(mutated, "Human decision and separate-approval boundary"), "section_nonempty")

def _mutate_non_approval_language_inverted(text: str) -> str:
    return _replace_once(text, "This ticket does not approve or create", "This ticket approves and creates")

def _assert_non_approval_language_inverted(base: str, mutated: str):
    _assert_critical_mutation(base, mutated, "Explicit non-approvals")
    _require("This ticket approves and creates" in _section(mutated, "Explicit non-approvals"), "section_nonempty")

def _mutate_routing_market_id_inserted(text: str) -> str:
    return _replace_once(text, "- outcome\n\nmarket_id is non-routing only.", "- outcome\n- market_id\n\nmarket_id is non-routing only.")

def _assert_routing_market_id_inserted(base: str, mutated: str):
    _assert_critical_mutation(base, mutated, "Canonical routing posture")
    body = _section(mutated, "Canonical routing posture")
    _require("- market_id" in body.split("\n\nmarket_id is non-routing only.")[0], "section_nonempty")

def _mutate_successor_substituted(text: str) -> str:
    return _replace_section_body(text, "Recommended next ticket", _section(text, "Recommended next ticket").replace("WEATHER-BOT-STAGE3-BINARY-PROBABILITY-RECORD-IMPLEMENTATION-01", "WEATHER-BOT-STAGE3-SCORING-IMPLEMENTATION-01"))

def _assert_successor_substituted(base: str, mutated: str):
    _assert_critical_mutation(base, mutated, "Recommended next ticket")
    _require("WEATHER-BOT-STAGE3-SCORING-IMPLEMENTATION-01" in _section(mutated, "Recommended next ticket"), "section_nonempty")

def _mutate_closed_set_complete_blocks_reordered(text: str) -> str:
    body = _machine_body(text)
    closed_part, rest = body.split("\n\nActual assignments:\n\n", 1)
    lines = closed_part.splitlines()
    first = lines[1:3]
    second = lines[3:5]
    new_closed = "\n".join([lines[0]] + second + first + lines[5:])
    return _replace_section_body(text, "Machine-checkable assignments", new_closed + "\n\nActual assignments:\n\n" + rest)

def _assert_closed_set_complete_blocks_reordered(base: str, mutated: str):
    _assert_changed(base, mutated)
    _require(_parse_actual_assignments(base) == _parse_actual_assignments(mutated), "section_nonempty")
    base_fields = list(_parse_closed_sets(base))
    mutated_fields = list(_parse_closed_sets(mutated))
    expected = base_fields[:]
    expected[0], expected[1] = expected[1], expected[0]
    _require(mutated_fields == expected, "section_nonempty")
    for field in base_fields:
        _require(_parse_closed_sets(base)[field] == _parse_closed_sets(mutated)[field], "section_nonempty")
    _critical_sections_equal_except(base, mutated, [])

def _mutate_closed_set_value_duplicated(text: str) -> str:
    target = "  - weather_bot_stage3_retrospective_scoring_implementation_approval_request"
    return _replace_once(text, target, target + "\n" + target)

def _assert_closed_set_value_duplicated(base: str, mutated: str):
    _assert_changed(base, mutated)
    _assert_assignments_unchanged(base, mutated)
    body = _machine_body(mutated).split("\n\nActual assignments:\n\n", 1)[0]
    _require(body.count("  - weather_bot_stage3_retrospective_scoring_implementation_approval_request") == 2, "section_nonempty")
    _critical_sections_equal_except(base, mutated, [])

def _mutate_actual_assignment_duplicated(text: str) -> str:
    first = EXPECTED_ASSIGNMENTS[0]
    return _replace_once(text, first, first + "\n" + first)

def _assert_actual_assignment_duplicated(base: str, mutated: str):
    _assert_changed(base, mutated)
    _assert_closed_sets_unchanged(base, mutated)
    body = _machine_body(mutated).split("Actual assignments:", 1)[1]
    _require(body.count(EXPECTED_ASSIGNMENTS[0]) == 2, "section_nonempty")
    _critical_sections_equal_except(base, mutated, [])

def _mutate_actual_assignment_malformed(text: str) -> str:
    return _replace_once(text, EXPECTED_ASSIGNMENTS[0], EXPECTED_ASSIGNMENTS[0].replace(": ", " = ", 1))

def _assert_actual_assignment_malformed(base: str, mutated: str):
    _assert_changed(base, mutated)
    _assert_closed_sets_unchanged(base, mutated)
    _require(EXPECTED_ASSIGNMENTS[0].replace(": ", " = ", 1) in _machine_body(mutated), "section_nonempty")
    _critical_sections_equal_except(base, mutated, [])

def _mutate_rejection_sentence_altered(text: str) -> str:
    return _replace_once(text, REJECTION_SENTENCE, "Missing fields are accepted.")

def _assert_rejection_sentence_altered(base: str, mutated: str):
    _assert_changed(base, mutated)
    _assert_closed_sets_unchanged(base, mutated)
    _assert_assignments_unchanged(base, mutated)
    assignments_exact(mutated)
    _require(_parse_rejection_tail(mutated) == "Missing fields are accepted.", "section_nonempty")
    _critical_sections_equal_except(base, mutated, [])

def _mutate_rejection_sentence_removed(text: str) -> str:
    return _replace_once(text, "\n\n" + REJECTION_SENTENCE, "")

def _assert_rejection_sentence_removed(base: str, mutated: str):
    _assert_changed(base, mutated)
    _assert_closed_sets_unchanged(base, mutated)
    _assert_assignments_unchanged(base, mutated)
    assignments_exact(mutated)
    _require(REJECTION_SENTENCE not in _machine_body(mutated), "section_nonempty")
    _critical_sections_equal_except(base, mutated, [])

def _mutate_fabricated_percentage_policy(text: str) -> str:
    body = _section(text, "Failure posture and deterministic output") + "\n\n90% confidence"
    return _replace_section_body(text, "Failure posture and deterministic output", body)

def _assert_fabricated_percentage_policy(base: str, mutated: str):
    _assert_changed(base, mutated)
    _assert_matrices_critical_machine_unchanged(base, mutated)
    _require("90% confidence" in _section(mutated, "Failure posture and deterministic output"), "section_nonempty")

def _mutate_fabricated_scientific_tolerance(text: str) -> str:
    body = _section(text, "Failure posture and deterministic output") + "\n\n1e-6 tolerance"
    return _replace_section_body(text, "Failure posture and deterministic output", body)

def _assert_fabricated_scientific_tolerance(base: str, mutated: str):
    _assert_changed(base, mutated)
    _assert_matrices_critical_machine_unchanged(base, mutated)
    _require("1e-6 tolerance" in _section(mutated, "Failure posture and deterministic output"), "section_nonempty")

def _mutate_fabricated_integer_bin_requirement(text: str) -> str:
    body = _section(text, "Failure posture and deterministic output") + "\n\n12 bins"
    return _replace_section_body(text, "Failure posture and deterministic output", body)

def _assert_fabricated_integer_bin_requirement(base: str, mutated: str):
    _assert_changed(base, mutated)
    _assert_matrices_critical_machine_unchanged(base, mutated)
    _require("12 bins" in _section(mutated, "Failure posture and deterministic output"), "section_nonempty")

MUTATION_CASES = {
    'canonical_id_line_three_suffix': (_mutate_canonical_id_line_three_suffix, _assert_canonical_id_line_three_suffix, header_exact, 'header_exact'),
    'duplicate_canonical_id': (_mutate_duplicate_canonical_id, _assert_duplicate_canonical_id, header_exact, 'header_exact'),
    'adjacent_heading_swap': (_mutate_adjacent_heading_swap, _assert_adjacent_heading_swap, heading_sequence_exact, 'heading_sequence_exact'),
    'future_file_path_changed': (_mutate_future_file_path_changed, _assert_future_file_path_changed, future_file_matrix_exact, 'future_file_matrix_exact'),
    'future_file_complete_row_duplicated': (_mutate_future_file_complete_row_duplicated, _assert_future_file_complete_row_duplicated, future_file_matrix_exact, 'future_file_matrix_exact'),
    'future_file_complete_row_removed': (_mutate_future_file_complete_row_removed, _assert_future_file_complete_row_removed, future_file_matrix_exact, 'future_file_matrix_exact'),
    'public_symbol_adjacent_rows_swapped': (_mutate_public_symbol_adjacent_rows_swapped, _assert_public_symbol_adjacent_rows_swapped, public_symbol_matrix_exact, 'public_symbol_matrix_exact'),
    'unknown_public_symbol': (_mutate_unknown_public_symbol, _assert_unknown_public_symbol, public_symbol_matrix_exact, 'public_symbol_matrix_exact'),
    'record_field_blocks_reordered': (_mutate_record_field_blocks_reordered, _assert_record_field_blocks_reordered, record_field_matrix_exact, 'record_field_matrix_exact'),
    'record_field_complete_row_duplicated': (_mutate_record_field_complete_row_duplicated, _assert_record_field_complete_row_duplicated, record_field_matrix_exact, 'record_field_matrix_exact'),
    'record_field_complete_row_removed': (_mutate_record_field_complete_row_removed, _assert_record_field_complete_row_removed, record_field_matrix_exact, 'record_field_matrix_exact'),
    'probability_type_posture_changed': (_mutate_probability_type_posture_changed, _assert_probability_type_posture_changed, record_field_matrix_exact, 'record_field_matrix_exact'),
    'market_id_added_as_mapping_input': (_mutate_market_id_added_as_mapping_input, _assert_market_id_added_as_mapping_input, mapping_input_matrix_exact, 'mapping_input_matrix_exact'),
    'token_outcome_pair_added_as_mapping_input': (_mutate_token_outcome_pair_added_as_mapping_input, _assert_token_outcome_pair_added_as_mapping_input, mapping_input_matrix_exact, 'mapping_input_matrix_exact'),
    'unknown_validation_code': (_mutate_unknown_validation_code, _assert_unknown_validation_code, validation_code_matrix_exact, 'validation_code_matrix_exact'),
    'validation_code_complete_row_duplicated': (_mutate_validation_code_complete_row_duplicated, _assert_validation_code_complete_row_duplicated, validation_code_matrix_exact, 'validation_code_matrix_exact'),
    'validation_rule_adjacent_rows_swapped': (_mutate_validation_rule_adjacent_rows_swapped, _assert_validation_rule_adjacent_rows_swapped, validation_rule_matrix_exact, 'validation_rule_matrix_exact'),
    'future_test_shortcut_changed': (_mutate_future_test_shortcut_changed, _assert_future_test_shortcut_changed, future_test_matrix_exact, 'future_test_matrix_exact'),
    'predecessor_actual_replaced_by_preview': (_mutate_predecessor_actual_replaced_by_preview, _assert_predecessor_actual_replaced_by_preview, predecessor_exact, 'predecessor_exact'),
    'predecessor_correct_and_preview_both_actual': (_mutate_predecessor_correct_and_preview_both_actual, _assert_predecessor_correct_and_preview_both_actual, predecessor_exact, 'predecessor_exact'),
    'predecessor_actual_declaration_duplicated': (_mutate_predecessor_actual_declaration_duplicated, _assert_predecessor_actual_declaration_duplicated, predecessor_exact, 'predecessor_exact'),
    'predecessor_negative_language_inverted': (_mutate_predecessor_negative_language_inverted, _assert_predecessor_negative_language_inverted, predecessor_exact, 'predecessor_exact'),
    'slice_identity_expanded_to_scoring': (_mutate_slice_identity_expanded_to_scoring, _assert_slice_identity_expanded_to_scoring, slice_identity_exact, 'slice_identity_exact'),
    'current_status_changed_to_implementation_approved': (_mutate_current_status_changed_to_implementation_approved, _assert_current_status_changed_to_implementation_approved, critical_sections_exact, 'critical_sections_exact'),
    'human_decision_changed_to_self_approved': (_mutate_human_decision_changed_to_self_approved, _assert_human_decision_changed_to_self_approved, critical_sections_exact, 'critical_sections_exact'),
    'non_approval_language_inverted': (_mutate_non_approval_language_inverted, _assert_non_approval_language_inverted, critical_sections_exact, 'critical_sections_exact'),
    'routing_market_id_inserted': (_mutate_routing_market_id_inserted, _assert_routing_market_id_inserted, critical_sections_exact, 'critical_sections_exact'),
    'successor_substituted': (_mutate_successor_substituted, _assert_successor_substituted, critical_sections_exact, 'critical_sections_exact'),
    'closed_set_complete_blocks_reordered': (_mutate_closed_set_complete_blocks_reordered, _assert_closed_set_complete_blocks_reordered, closed_sets_exact, 'closed_sets_exact'),
    'closed_set_value_duplicated': (_mutate_closed_set_value_duplicated, _assert_closed_set_value_duplicated, closed_sets_exact, 'closed_sets_exact'),
    'actual_assignment_duplicated': (_mutate_actual_assignment_duplicated, _assert_actual_assignment_duplicated, assignments_exact, 'assignments_exact'),
    'actual_assignment_malformed': (_mutate_actual_assignment_malformed, _assert_actual_assignment_malformed, assignments_exact, 'assignments_exact'),
    'rejection_sentence_altered': (_mutate_rejection_sentence_altered, _assert_rejection_sentence_altered, rejection_sentence_exact, 'rejection_sentence_exact'),
    'rejection_sentence_removed': (_mutate_rejection_sentence_removed, _assert_rejection_sentence_removed, rejection_sentence_exact, 'rejection_sentence_exact'),
    'fabricated_percentage_policy': (_mutate_fabricated_percentage_policy, _assert_fabricated_percentage_policy, numeric_policy_clean, 'numeric_policy_clean'),
    'fabricated_scientific_tolerance': (_mutate_fabricated_scientific_tolerance, _assert_fabricated_scientific_tolerance, numeric_policy_clean, 'numeric_policy_clean'),
    'fabricated_integer_bin_requirement': (_mutate_fabricated_integer_bin_requirement, _assert_fabricated_integer_bin_requirement, numeric_policy_clean, 'numeric_policy_clean'),
}


def _expect_contract_error(function, text: str, expected_code: str):
    raised = None
    try:
        function(text)
    except ContractCheckError as error:
        raised = error
    _require(raised is not None, "section_nonempty")
    _require(raised.check_code == expected_code, "section_nonempty")

def _validator_name(function) -> str:
    for name, validator in VALIDATORS.items():
        if validator is function:
            return name
    raise ContractCheckError("oracle_literals_exact")

def _anti_stub_ast_audit():
    tree = ast.parse(Path(__file__).read_text())
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    for case in REQUIRED_MUTATION_CASES:
        mutator_name = "_mutate_" + case
        proof_name = "_assert_" + case
        _require(mutator_name in functions, "oracle_literals_exact")
        _require(proof_name in functions, "oracle_literals_exact")
        for function_name in [mutator_name, proof_name]:
            function = functions[function_name]
            _require(not any(isinstance(node, ast.Pass) for node in ast.walk(function)), "oracle_literals_exact")
            _require(not any(isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name) and node.exc.func.id == "NotImplementedError" for node in ast.walk(function)), "oracle_literals_exact")
            if len(function.body) == 1 and isinstance(function.body[0], ast.Return):
                returned = function.body[0].value
                _require(not (isinstance(returned, ast.Name) and returned.id in {argument.arg for argument in function.args.args}), "oracle_literals_exact")
    for code in REQUIRED_CHECK_CODES:
        function = functions[code]
        for node in ast.walk(function):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "_require":
                _require(not (node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value is True), "oracle_literals_exact")
        _require(not (len(function.body) == 1 and isinstance(function.body[0], ast.Return)), "oracle_literals_exact")

def test_contract():
    validate(_read())

def test_registries():
    _require(list(VALIDATORS) == REQUIRED_CHECK_CODES, "oracle_literals_exact")
    _require(PIPELINE == REQUIRED_CHECK_CODES, "oracle_literals_exact")
    _require(len(REQUIRED_MUTATION_CASES) == 37, "oracle_literals_exact")
    _require(list(MUTATION_CASES) == REQUIRED_MUTATION_CASES, "oracle_literals_exact")
    mutators = []
    proofs = []
    for name, entry in MUTATION_CASES.items():
        mutator, proof, validator, expected_code = entry
        _require(callable(mutator), "oracle_literals_exact")
        _require(callable(proof), "oracle_literals_exact")
        _require(callable(validator), "oracle_literals_exact")
        _require(isinstance(expected_code, str) and expected_code != "", "oracle_literals_exact")
        _require(expected_code == _validator_name(validator), "oracle_literals_exact")
        _require(mutator.__name__ == "_mutate_" + name, "oracle_literals_exact")
        _require(proof.__name__ == "_assert_" + name, "oracle_literals_exact")
        mutators.append(mutator.__name__)
        proofs.append(proof.__name__)
    _require(len(mutators) == len(set(mutators)) == 37, "oracle_literals_exact")
    _require(len(proofs) == len(set(proofs)) == 37, "oracle_literals_exact")
    _anti_stub_ast_audit()

def test_all_registered_mutations_are_validator_specific():
    base = _read()
    executed = []
    for name, entry in MUTATION_CASES.items():
        mutator, proof, validator, expected_code = entry
        mutated = mutator(base)
        _require(mutated != base, "section_nonempty")
        proof(base, mutated)
        _expect_contract_error(validator, mutated, expected_code)
        raised = None
        try:
            validate(mutated)
        except ContractCheckError as error:
            raised = error
        _require(raised is not None, "section_nonempty")
        executed.append(name)
    _require(executed == REQUIRED_MUTATION_CASES, "oracle_literals_exact")


def _replace_actual_assignments_block(text: str, assignment_lines: list[str], tail: str | None = None) -> str:
    closed_part, rest = _split_machine(text)
    if tail is None:
        tail = _parse_rejection_tail(text)
    new_rest = "\n".join(assignment_lines)
    if tail != "":
        new_rest = new_rest + "\n\n" + tail
    return _replace_section_body(text, "Machine-checkable assignments", closed_part + "\n\nActual assignments:\n\n" + new_rest)

def _assert_assignment_error(mutated: str):
    raised = None
    try:
        assignments_exact(mutated)
    except ContractCheckError as error:
        raised = error
    _require(raised is not None, "section_nonempty")
    _require(raised.check_code == "assignments_exact", "section_nonempty")
    complete = None
    try:
        validate(mutated)
    except ContractCheckError as error:
        complete = error
    _require(complete is not None, "section_nonempty")

def test_assignment_parser_rejects_escape_lines():
    base = _read()
    cases = []
    first = EXPECTED_ASSIGNMENTS[:]
    first[0] = first[0].replace(": ", " = ", 1)
    cases.append(("malformed_first", first, first[0]))
    middle = EXPECTED_ASSIGNMENTS[:]
    middle[len(middle) // 2] = "  " + middle[len(middle) // 2]
    cases.append(("malformed_middle", middle, middle[len(middle) // 2]))
    final = EXPECTED_ASSIGNMENTS[:]
    final[-1] = final[-1].replace(": ", " = ", 1)
    cases.append(("malformed_final", final, final[-1]))
    extra_bad = EXPECTED_ASSIGNMENTS[:] + ["- malformed = value"]
    cases.append(("malformed_extra", extra_bad, "- malformed = value"))
    prose = EXPECTED_ASSIGNMENTS[:] + ["This prose must not be skipped."]
    cases.append(("prose_extra", prose, "This prose must not be skipped."))
    extra_valid = EXPECTED_ASSIGNMENTS[:] + ["- unexpected field: unexpected_value"]
    cases.append(("unexpected_valid", extra_valid, "- unexpected field: unexpected_value"))
    second_delimiter = EXPECTED_ASSIGNMENTS[:] + ["Actual assignments:"]
    cases.append(("second_delimiter", second_delimiter, "Actual assignments:"))
    early_blank = EXPECTED_ASSIGNMENTS[:5] + [""] + EXPECTED_ASSIGNMENTS[5:]
    cases.append(("early_blank", early_blank, ""))
    for name, lines, marker in cases:
        mutated = _replace_actual_assignments_block(base, lines)
        _require(mutated != base, "section_nonempty")
        if marker != "":
            _require(marker in _machine_body(mutated), "section_nonempty")
        else:
            _require("\n\n".join([EXPECTED_ASSIGNMENTS[4], EXPECTED_ASSIGNMENTS[5]]) in _machine_body(mutated), "section_nonempty")
        _assert_assignment_error(mutated)

def test_assignment_parser_rejection_tail_isolation_controls():
    base = _read()
    assignments_exact(base)
    altered = _replace_actual_assignments_block(base, EXPECTED_ASSIGNMENTS[:], "Altered rejection tail.")
    assignments_exact(altered)
    removed = _replace_actual_assignments_block(base, EXPECTED_ASSIGNMENTS[:], "")
    assignments_exact(removed)

def _insert_noncritical_sentence(text: str, sentence: str) -> str:
    body = _section(text, "Status and scope") + "\n\n" + sentence
    return _replace_section_body(text, "Status and scope", body)

def _assert_safety_error_from_source(source: str):
    raised = None
    try:
        _audit_static_test_source(source)
    except ContractCheckError as error:
        raised = error
    _require(raised is not None, "section_nonempty")
    _require(raised.check_code == "prohibited_behavior_absent", "section_nonempty")

def _mutate_remaining_section_body(body: str, mutation_name: str) -> str:
    if mutation_name == "append_affirmative":
        return body + "\n\nThis frozen section approves implementation."
    if mutation_name == "append_negative":
        return body + "\n\nThis frozen section does not approve implementation."
    if mutation_name == "delete_final_line":
        lines = body.splitlines()
        nonblank = [line for line in lines if line.strip() != ""]
        if len(nonblank) == 1:
            return nonblank[0].rsplit(" ", 1)[0]
        for index in range(len(lines) - 1, -1, -1):
            if lines[index].strip() != "":
                del lines[index]
                return "\n".join(lines).strip()
        return ""
    if mutation_name == "replace_token":
        if "." in body:
            return body.replace(".", "!", 1)
        return body[:-1] + "X"
    if mutation_name == "insert_explanatory":
        return "Additional explanatory sentence is not part of the frozen artifact.\n\n" + body
    raise AssertionError(mutation_name)

def test_remaining_sections_are_exactly_frozen():
    base = _read()
    mutation_names = ["append_affirmative", "append_negative", "delete_final_line", "replace_token", "insert_explanatory"]
    for heading, expected in EXPECTED_REMAINING_SECTION_BODIES.items():
        _require(_section(base, heading) == expected, "section_nonempty")
        for mutation_name in mutation_names:
            mutated_body = _mutate_remaining_section_body(expected, mutation_name)
            mutated = _replace_section_body(base, heading, mutated_body)
            _require(mutated != base, "section_nonempty")
            _require(_section(mutated, heading) != _section(base, heading), "section_nonempty")
            for other_heading in EXPECTED_HEADINGS:
                if other_heading != heading:
                    _require(_section(mutated, other_heading) == _section(base, other_heading), "section_nonempty")
            raised = None
            try:
                prohibited_behavior_absent(mutated)
            except ContractCheckError as error:
                raised = error
            _require(raised is not None, "section_nonempty")
            _require(raised.check_code == "prohibited_behavior_absent", "section_nonempty")
            complete = None
            try:
                validate(mutated)
            except ContractCheckError as error:
                complete = error
            _require(complete is not None, "section_nonempty")

def test_natural_language_safety_parser_is_removed():
    tree = ast.parse(Path(__file__).read_text())
    removed_functions = [
        "_sentences",
        "_clauses",
        "_capabilities",
        "_predicate_forms",
        "_claim_is_negated_or_conditional",
        "_active_document_claim_is_affirmative",
        "_capability_claim_is_affirmative",
        "_has_affirmative_safety_claim",
    ]
    removed_assignments = [
        "AFFIRMATIVE_SAFETY_EXAMPLES",
        "NEGATIVE_SAFETY_EXAMPLES",
        "MIXED_AFFIRMATIVE_SAFETY_EXAMPLES",
        "MULTICLAUSE_NEGATIVE_SAFETY_EXAMPLES",
        "FLEXIBLE_AFFIRMATIVE_SAFETY_EXAMPLES",
        "LOCAL_NEGATIVE_SAFETY_EXAMPLES",
        "LOCAL_AFFIRMATIVE_SAFETY_EXAMPLES",
    ]
    function_names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    assignment_names = [node.targets[0].id for node in tree.body if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)]
    _require(not any(name in function_names for name in removed_functions), "oracle_literals_exact")
    _require(not any(name in assignment_names for name in removed_assignments), "oracle_literals_exact")

def test_static_test_source_audit_rejects_prohibited_snippets():
    prohibited = [
        "import " + "sub" + "process",
        "import " + "os",
        "import socket",
        "import requests",
        "import urllib",
        "import http",
        "import meg",
        "from meg.weather import stage2",
        "import pytest",
        "__import__(\"ast\")",
        "import " + "os\n" + "os.environ",
        "getenv(\"HOME\")",
        "system(\"true\")",
        "popen(\"true\")",
        "run([\"true\"])",
        "check_call([\"true\"])",
        "check_output([\"true\"])",
        "urlopen(\"https://example.invalid\")",
        "request(\"GET\")",
        "connect(())",
        "from pathlib import Path\nPath(\"." + "git\")",
        "command = \"git " + "status\"",
        "command = \"git " + "fetch\"",
        "command = \"git " + "checkout\"",
        "command = \"git " + "branch\"",
        "command = \"git " + "log\"",
        "command = \"git " + "show\"",
        "command = \"git " + "rev-parse\"",
        "command = \"git " + "merge-base\"",
        "command = \"git " + "cat-file\"",
        "command = \"git " + "diff\"",
        "command = \"git " + "ls-files\"",
        "command = \"gh " + "pr view\"",
        "command = \"gh " + "api repos\"",
        "command = \"gh " + "issue list\"",
        "command = \"gh " + "workflow list\"",
        "command = \"gh " + "run list\"",
        "command = \"gh " + "repo view\"",
        "environ[\"HOME\"]",
        "environ.get(\"HOME\")",
        "os.environ[\"HOME\"]",
        "os.getenv(\"HOME\")",
    ]
    for source in prohibited:
        _assert_safety_error_from_source(source)

def test_static_test_source_audit_allows_static_controls():
    allowed = [
        "import ast",
        "import re",
        "from pathlib import Path",
        "DOC.read_text()",
        "ALLOWLIST.read_text()",
        "ast.parse(source)",
        "ast.literal_eval(node)",
        "values = [text.strip() for text in lines]",
        "joined = \" | \".join(values)",
        "note = \"Git is discussed in prose\"",
    ]
    for source in allowed:
        _audit_static_test_source(source)

def test_pre_commit_completeness_gate():
    base = _read()
    validate(base)
    _require(EXPECTED_CLOSED_SETS == _parse_closed_sets(base), "closed_sets_exact")
    _require(EXPECTED_ASSIGNMENTS == _parse_actual_assignments(base), "assignments_exact")
    oracle_literals_exact(base)
    _anti_stub_ast_audit()
    allowlist_counts_exact(base)
    test_registries()
    test_all_registered_mutations_are_validator_specific()
