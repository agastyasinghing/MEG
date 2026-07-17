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
EXPECTED_CRITICAL_SECTIONS = {'Canonical routing posture': 'Canonical routing fields remain exactly:\n'
                              '\n'
                              '- condition_id\n'
                              '- token_id\n'
                              '- outcome\n'
                              '\n'
                              'market_id is non-routing only.\n'
                              '\n'
                              'token_outcome_pair is derived only.',
 'Current request status': 'Request status: request_prepared_implementation_not_approved.\n'
                           '\n'
                           'This document asks a human reviewer whether a later separate implementation ticket may create only the '
                           'immutable_binary_outcome_probability_record_boundary defined here. No implementation is approved by this '
                           'document, no production file may be created from this document alone, and no successor implementation ticket '
                           'may begin without an explicit human approval outside this artifact.',
 'Explicit non-approvals': 'This ticket does not approve or create the Stage 3 package; production modules; dataclasses; enums; validation '
                           'functions; probability records; probability generation; model execution; feature calculation; source fetching; '
                           'provider connectors; file access; fixture access; data acquisition; corpus expansion; split execution; '
                           'baseline execution; scoring; diagnostics; label joining; evaluation results; claim evaluation; claim records; '
                           'evidence-gate evaluation; decision records; persistence; serialization; database tables; migrations; APIs; '
                           'reports; exports; scheduling; queues; background tasks; simulation; runtime observation; paper trading; '
                           'trading; order placement; autonomy; runtime behavior; or production behavior.',
 'Human decision and separate-approval boundary': 'A human decision outside this document is required. The reviewer may approve a later '
                                                  'ticket limited exactly to the requested slice, request revisions to this approval '
                                                  'request, hold the sequence, or block the request. This document does not record its own '
                                                  'approval and cannot convert request_prepared_implementation_not_approved into '
                                                  'implementation approval. Any later implementation must remain limited to the exact '
                                                  'future files, public symbols, fields, validation codes, rules, tests, dependencies, and '
                                                  'non-goals recorded here.',
 'Immediate predecessor and merge verification': 'Immediate predecessor: pr_366.\n'
                                                 '\n'
                                                 'ACTUAL_PR_366_MERGE_SHA: 24c229970392096dc8a61124f6e80ac724244a08\n'
                                                 '\n'
                                                 'PR #366 merged at actual merge commit 24c229970392096dc8a61124f6e80ac724244a08, which is '
                                                 'reachable from the current branch base. The former open-PR preview merge SHA '
                                                 '53822e5dc3115b7989c7f015c6120b9faa5a2a54 is not the actual merge commit and must not be '
                                                 'used. No newer controlling Weather Bot artifact supersedes PR #366 for this '
                                                 'approval-request scope.',
 'Recommended next ticket': 'WEATHER-BOT-STAGE3-BINARY-PROBABILITY-RECORD-IMPLEMENTATION-01\n'
                            '\n'
                            'This ticket may be created only after an explicit human approval outside this approval-request artifact. If '
                            'approved, it must remain limited exactly to the three proposed future files and the '
                            'immutable_binary_outcome_probability_record_boundary. Without explicit human approval, no implementation '
                            'ticket may be created.',
 'Requested implementation slice identity': 'Requested future implementation slice: immutable_binary_outcome_probability_record_boundary.\n'
                                            '\n'
                                            'The requested slice is limited to three future files, seven future public symbols, one frozen '
                                            'binary-outcome record shape, caller-supplied exact mappings, deterministic pure validation, '
                                            'and focused tests. It does not generate probabilities, execute models, read data, join '
                                            'labels, score records, create results or claims, evaluate an evidence gate, persist records, '
                                            'create reports, simulate markets, add runtime behavior, or trade.'}
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
REJECTION_SENTENCE = "Missing, duplicate, hybrid, reordered, extra, or custom fields and values are rejected."
REQUIRED_CHECK_CODES = ["header_exact", "heading_sequence_exact", "section_nonempty", "predecessor_exact", "slice_identity_exact", "future_file_matrix_exact", "public_symbol_matrix_exact", "record_field_matrix_exact", "mapping_input_matrix_exact", "validation_code_matrix_exact", "validation_rule_matrix_exact", "future_test_matrix_exact", "decision_options_exact", "critical_sections_exact", "closed_sets_exact", "assignments_exact", "rejection_sentence_exact", "numeric_policy_clean", "allowlist_counts_exact", "oracle_literals_exact", "prohibited_behavior_absent"]
REQUIRED_MUTATION_CASES = ["canonical_id_line_three_suffix", "duplicate_canonical_id", "adjacent_heading_swap", "future_file_path_changed", "future_file_complete_row_duplicated", "future_file_complete_row_removed", "public_symbol_adjacent_rows_swapped", "unknown_public_symbol", "record_field_blocks_reordered", "record_field_complete_row_duplicated", "record_field_complete_row_removed", "probability_type_posture_changed", "market_id_added_as_mapping_input", "token_outcome_pair_added_as_mapping_input", "unknown_validation_code", "validation_code_complete_row_duplicated", "validation_rule_adjacent_rows_swapped", "future_test_shortcut_changed", "predecessor_actual_replaced_by_preview", "predecessor_correct_and_preview_both_actual", "predecessor_actual_declaration_duplicated", "predecessor_negative_language_inverted", "slice_identity_expanded_to_scoring", "current_status_changed_to_implementation_approved", "human_decision_changed_to_self_approved", "non_approval_language_inverted", "routing_market_id_inserted", "successor_substituted", "closed_set_complete_blocks_reordered", "closed_set_value_duplicated", "actual_assignment_duplicated", "actual_assignment_malformed", "rejection_sentence_altered", "rejection_sentence_removed", "fabricated_percentage_policy", "fabricated_scientific_tolerance", "fabricated_integer_bin_requirement"]
NUMERIC_TOKEN = re.compile(r"(?<![A-Za-z0-9_])(?:\d+\.\d*|\.\d+|\d+(?:[eE][+-]?\d+)?)(?:%)?(?![A-Za-z0-9_])")
class ContractCheckError(AssertionError):
    def __init__(self, check_code: str): self.check_code = check_code; super().__init__(check_code)
def _require(condition: bool, check_code: str):
    if not condition: raise ContractCheckError(check_code)
def _section(text: str, name: str) -> str:
    marker = "## " + name; _require(text.count(marker) == 1, "section_nonempty"); start = text.index(marker) + len(marker); end = text.find("\n## ", start); body = text[start:end if end >= 0 else len(text)].strip(); _require(body != "", "section_nonempty"); return body
def _table(text, name, expected, code):
    body = _section(text, name); lines = body.splitlines(); _require(all(line.startswith("|") for line in lines), code); parsed = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]; _require(parsed == expected, code)
def header_exact(text):
    lines=text.splitlines(); _require(lines[:3] == ["# "+CANONICAL_ID,"","Canonical ID: "+CANONICAL_ID] and text.count("Canonical ID: "+CANONICAL_ID)==1,"header_exact")
def heading_sequence_exact(text): _require([x[3:] for x in text.splitlines() if x.startswith("## ")] == EXPECTED_HEADINGS,"heading_sequence_exact")
def section_nonempty(text):
    for h in EXPECTED_HEADINGS: _section(text,h)
def predecessor_exact(text):
    body=_section(text,"Immediate predecessor and merge verification"); _require(body == EXPECTED_CRITICAL_SECTIONS["Immediate predecessor and merge verification"] and body.count("ACTUAL_PR_366_MERGE_SHA: "+ACTUAL_PR_366_MERGE_SHA)==1 and body.count(PREVIEW_MERGE_SHA)==1 and ACTUAL_PR_366_MERGE_SHA != PREVIEW_MERGE_SHA,"predecessor_exact")
def slice_identity_exact(text): _require(_section(text,"Requested implementation slice identity") == EXPECTED_CRITICAL_SECTIONS["Requested implementation slice identity"],"slice_identity_exact")
def future_file_matrix_exact(text): _table(text,"Exact future changed-file matrix",EXPECTED_EXACT_FUTURE_CHANGED_FILE_MATRIX,"future_file_matrix_exact")
def public_symbol_matrix_exact(text): _table(text,"Exact future public-symbol matrix",EXPECTED_EXACT_FUTURE_PUBLIC_SYMBOL_MATRIX,"public_symbol_matrix_exact")
def record_field_matrix_exact(text): _table(text,"Exact future record-field matrix",EXPECTED_EXACT_FUTURE_RECORD_FIELD_MATRIX,"record_field_matrix_exact")
def mapping_input_matrix_exact(text): _table(text,"Exact mapping-input matrix",EXPECTED_EXACT_MAPPING_INPUT_MATRIX,"mapping_input_matrix_exact")
def validation_code_matrix_exact(text): _table(text,"Exact validation-code matrix",EXPECTED_EXACT_VALIDATION_CODE_MATRIX,"validation_code_matrix_exact")
def validation_rule_matrix_exact(text): _table(text,"Exact validation-rule matrix",EXPECTED_EXACT_VALIDATION_RULE_MATRIX,"validation_rule_matrix_exact")
def future_test_matrix_exact(text): _table(text,"Exact future test matrix",EXPECTED_EXACT_FUTURE_TEST_MATRIX,"future_test_matrix_exact")
def decision_options_exact(text): _table(text,"Approval decision options",EXPECTED_APPROVAL_DECISION_OPTIONS,"decision_options_exact")
def critical_sections_exact(text):
    for name, expected in EXPECTED_CRITICAL_SECTIONS.items(): _require(_section(text,name) == expected,"critical_sections_exact")
def closed_sets_exact(text):
    body=_section(text,"Machine-checkable assignments"); _require(body.startswith("Closed sets:\n- ") and "Actual assignments:" in body,"closed_sets_exact")
def assignments_exact(text):
    body=_section(text,"Machine-checkable assignments"); actual=body.split("Actual assignments:\n\n",1)[1].split("\n\n"+REJECTION_SENTENCE,1)[0].splitlines(); _require(actual == EXPECTED_ASSIGNMENTS and all(re.fullmatch(r"- [^:]+: .+",x) for x in actual),"assignments_exact")
def rejection_sentence_exact(text): _require(text.count(REJECTION_SENTENCE)==1,"rejection_sentence_exact")
def numeric_policy_clean(text):
    _require(all(NUMERIC_TOKEN.fullmatch(x) for x in ["12","12.",".5","0.25","90%","1e-6"]),"numeric_policy_clean"); policy=_section(text,"Failure posture and deterministic output")+_section(text,"Fail-closed requirements"); _require(NUMERIC_TOKEN.search(policy) is None,"numeric_policy_clean")
def allowlist_counts_exact(text):
    tree=ast.parse(ALLOWLIST.read_text()); node=next(x.value for x in tree.body if isinstance(x,ast.AnnAssign) and isinstance(x.target,ast.Name) and x.target.id=="ALLOWED_MARKET_ID_OCCURRENCE_LINES"); values=ast.literal_eval(node.args[0]);
    for path in [DOC.as_posix(),Path(__file__).relative_to(Path.cwd()).as_posix()]: _require(values[path] == sum("market_id" in line for line in Path(path).read_text().splitlines()),"allowlist_counts_exact")
def oracle_literals_exact(text):
    tree=ast.parse(Path(__file__).read_text()); assigns={x.targets[0].id:x.value for x in tree.body if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Name)}; names=["EXPECTED_HEADINGS","EXPECTED_ASSIGNMENTS","REQUIRED_CHECK_CODES","REQUIRED_MUTATION_CASES"]; _require(all(isinstance(assigns[n],(ast.List,ast.Tuple)) for n in names),"oracle_literals_exact")
def prohibited_behavior_absent(text):
    forbidden=["This ticket creates production files","This ticket approves Stage 3 implementation","This ticket approves probability generation","This ticket approves scoring","This ticket approves trading"]; _require(not any(x in text for x in forbidden),"prohibited_behavior_absent")
VALIDATORS = {"header_exact": header_exact,"heading_sequence_exact": heading_sequence_exact,"section_nonempty": section_nonempty,"predecessor_exact": predecessor_exact,"slice_identity_exact": slice_identity_exact,"future_file_matrix_exact": future_file_matrix_exact,"public_symbol_matrix_exact": public_symbol_matrix_exact,"record_field_matrix_exact": record_field_matrix_exact,"mapping_input_matrix_exact": mapping_input_matrix_exact,"validation_code_matrix_exact": validation_code_matrix_exact,"validation_rule_matrix_exact": validation_rule_matrix_exact,"future_test_matrix_exact": future_test_matrix_exact,"decision_options_exact": decision_options_exact,"critical_sections_exact": critical_sections_exact,"closed_sets_exact": closed_sets_exact,"assignments_exact": assignments_exact,"rejection_sentence_exact": rejection_sentence_exact,"numeric_policy_clean": numeric_policy_clean,"allowlist_counts_exact": allowlist_counts_exact,"oracle_literals_exact": oracle_literals_exact,"prohibited_behavior_absent": prohibited_behavior_absent}
PIPELINE = ["header_exact","heading_sequence_exact","section_nonempty","predecessor_exact","slice_identity_exact","future_file_matrix_exact","public_symbol_matrix_exact","record_field_matrix_exact","mapping_input_matrix_exact","validation_code_matrix_exact","validation_rule_matrix_exact","future_test_matrix_exact","decision_options_exact","critical_sections_exact","closed_sets_exact","assignments_exact","rejection_sentence_exact","numeric_policy_clean","allowlist_counts_exact","oracle_literals_exact","prohibited_behavior_absent"]
def validate(text):
    for code in PIPELINE: VALIDATORS[code](text)
def test_contract(): validate(DOC.read_text())
def test_registries(): _require(list(VALIDATORS)==REQUIRED_CHECK_CODES and PIPELINE==REQUIRED_CHECK_CODES,"oracle_literals_exact")
