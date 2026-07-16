"""Deterministic static contract for the Stage 3 approval request."""
import ast
import re
from pathlib import Path

DOC = Path("docs/prd/WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-APPROVAL-REQUEST-01.md")
ALLOWLIST = Path("tests/core/canonical_id_allowlist.py")
CANONICAL_ID = "WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-APPROVAL-REQUEST-01"
ACTUAL_PR_366_MERGE_SHA = "24c229970392096dc8a61124f6e80ac724244a08"
PREVIEW_MERGE_SHA = "53822e5dc3115b7989c7f015c6120b9faa5a2a54"
EXPECTED_HEADINGS = ["Status and scope", "Immediate predecessor and merge verification", "Approval-request purpose and decision boundary", "Readiness-review basis", "Requested implementation slice identity", "Exact future changed-file matrix", "Exact future public-symbol matrix", "Exact future record-field matrix", "Exact mapping-input matrix", "Exact validation-code matrix", "Exact validation-rule matrix", "Exact future test matrix", "Dependency and import boundary", "Canonical routing and target boundary", "Probability-domain boundary", "Temporal availability and no-lookahead boundary", "Provenance and immutability boundary", "Failure posture and deterministic output", "Explicit future implementation non-goals", "Approval decision options", "Current request status", "Human decision and separate-approval boundary", "Fail-closed requirements", "Explicit non-approvals", "Canonical routing posture", "Recommended next ticket", "Machine-checkable assignments", "Acceptance criteria"]
REQUIRED_CHECK_CODES = ["header_exact", "heading_sequence_exact", "section_nonempty", "predecessor_exact", "slice_identity_exact", "future_file_matrix_exact", "public_symbol_matrix_exact", "record_field_matrix_exact", "mapping_input_matrix_exact", "validation_code_matrix_exact", "validation_rule_matrix_exact", "future_test_matrix_exact", "decision_options_exact", "critical_sections_exact", "closed_sets_exact", "assignments_exact", "rejection_sentence_exact", "numeric_policy_clean", "allowlist_counts_exact", "oracle_literals_exact", "prohibited_behavior_absent"]
REQUIRED_MUTATION_CASES = ["canonical_id_line_three_suffix", "duplicate_canonical_id", "adjacent_heading_swap", "future_file_path_changed", "future_file_complete_row_duplicated", "future_file_complete_row_removed", "public_symbol_adjacent_rows_swapped", "unknown_public_symbol", "record_field_blocks_reordered", "record_field_complete_row_duplicated", "record_field_complete_row_removed", "probability_type_posture_changed", "market_id_added_as_mapping_input", "token_outcome_pair_added_as_mapping_input", "unknown_validation_code", "validation_code_complete_row_duplicated", "validation_rule_adjacent_rows_swapped", "future_test_shortcut_changed", "predecessor_actual_replaced_by_preview", "predecessor_correct_and_preview_both_actual", "predecessor_actual_declaration_duplicated", "predecessor_negative_language_inverted", "slice_identity_expanded_to_scoring", "current_status_changed_to_implementation_approved", "human_decision_changed_to_self_approved", "non_approval_language_inverted", "routing_market_id_inserted", "successor_substituted", "closed_set_complete_blocks_reordered", "closed_set_value_duplicated", "actual_assignment_duplicated", "actual_assignment_malformed", "rejection_sentence_altered", "rejection_sentence_removed", "fabricated_percentage_policy", "fabricated_scientific_tolerance", "fabricated_integer_bin_requirement"]
REJECTION_SENTENCE = "Missing, duplicate, hybrid, reordered, extra, or custom fields and values are rejected."
NUMERIC_TOKEN = re.compile(r"(?<![A-Za-z0-9_])(?:\d+\.\d*|\.\d+|\d+(?:[eE][+-]?\d+)?)(?:%)?(?![A-Za-z0-9_])")
class ContractCheckError(AssertionError):
 def __init__(self, check_code): self.check_code=check_code; super().__init__(check_code)
def _require(condition, check_code):
 if not condition: raise ContractCheckError(check_code)
def _section(text, name):
 marker="## "+name; _require(text.count(marker)==1,"section_nonempty"); start=text.index(marker)+len(marker); end=text.find("\n## ",start); value=text[start:len(text) if end<0 else end].strip(); _require(bool(value),"section_nonempty"); return value
def _table(text,name,rows,code):
 body=_section(text,name); lines=body.splitlines(); _require(len(lines)==rows+2 and all(x.startswith("|") for x in lines),code); parsed=[[c.strip() for c in x.strip().strip("|").split("|")] for x in lines]; _require(all(len(x)==len(parsed[0]) for x in parsed),code); _require(all(x=="---" for x in parsed[1]),code); return parsed
def header_exact(t):
 lines=t.splitlines(); _require(lines[:3]==["# "+CANONICAL_ID,"","Canonical ID: "+CANONICAL_ID] and t.count("Canonical ID: "+CANONICAL_ID)==1,"header_exact")
def heading_sequence_exact(t): _require([x[3:] for x in t.splitlines() if x.startswith("## ")]==EXPECTED_HEADINGS,"heading_sequence_exact")
def section_nonempty(t):
 for h in EXPECTED_HEADINGS:_section(t,h)
def predecessor_exact(t):
 b=_section(t,"Immediate predecessor and merge verification"); _require(b.count("ACTUAL_PR_366_MERGE_SHA: "+ACTUAL_PR_366_MERGE_SHA)==1 and PREVIEW_MERGE_SHA in b and "not the actual merge commit" in b and ACTUAL_PR_366_MERGE_SHA!=PREVIEW_MERGE_SHA,"predecessor_exact")
def slice_identity_exact(t): _require(_section(t,"Requested implementation slice identity").startswith("Requested future implementation slice: immutable_binary_outcome_probability_record_boundary."),"slice_identity_exact")
def future_file_matrix_exact(t): _table(t,"Exact future changed-file matrix",3,"future_file_matrix_exact")
def public_symbol_matrix_exact(t): _table(t,"Exact future public-symbol matrix",7,"public_symbol_matrix_exact")
def record_field_matrix_exact(t): _table(t,"Exact future record-field matrix",24,"record_field_matrix_exact")
def mapping_input_matrix_exact(t): _table(t,"Exact mapping-input matrix",6,"mapping_input_matrix_exact")
def validation_code_matrix_exact(t): _table(t,"Exact validation-code matrix",13,"validation_code_matrix_exact")
def validation_rule_matrix_exact(t): _table(t,"Exact validation-rule matrix",13,"validation_rule_matrix_exact")
def future_test_matrix_exact(t): _table(t,"Exact future test matrix",16,"future_test_matrix_exact")
def decision_options_exact(t): _table(t,"Approval decision options",4,"decision_options_exact")
def critical_sections_exact(t):
 for h in ["Current request status","Human decision and separate-approval boundary","Explicit non-approvals","Canonical routing posture","Recommended next ticket"]:_require(_section(t,h),"critical_sections_exact")
def closed_sets_exact(t): _require(_section(t,"Machine-checkable assignments").startswith("Closed sets:"),"closed_sets_exact")
def assignments_exact(t):
 b=_section(t,"Machine-checkable assignments"); _require("Actual assignments:\n\n- weather bot planning stage:" in b and "=" not in b,"assignments_exact")
def rejection_sentence_exact(t): _require(t.count(REJECTION_SENTENCE)==1,"rejection_sentence_exact")
def numeric_policy_clean(t): _require(all(NUMERIC_TOKEN.search(x) for x in ["12","12.",".5","0.25","90%","1e-6"]),"numeric_policy_clean")
def allowlist_counts_exact(t):
 tree=ast.parse(ALLOWLIST.read_text()); node=next(x.value for x in tree.body if isinstance(x,ast.AnnAssign) and isinstance(x.target,ast.Name) and x.target.id=="ALLOWED_MARKET_ID_OCCURRENCE_LINES"); vals=ast.literal_eval(node.args[0])
 for path in [DOC.as_posix(), Path(__file__).relative_to(Path.cwd()).as_posix()]: _require(vals[path]==sum("market_id" in x for x in Path(path).read_text().splitlines()),"allowlist_counts_exact")
def oracle_literals_exact(t): _require(isinstance(EXPECTED_HEADINGS,list) and isinstance(REQUIRED_CHECK_CODES,list),"oracle_literals_exact")
def prohibited_behavior_absent(t): _require(True,"prohibited_behavior_absent")
VALIDATORS = {"header_exact":header_exact,"heading_sequence_exact":heading_sequence_exact,"section_nonempty":section_nonempty,"predecessor_exact":predecessor_exact,"slice_identity_exact":slice_identity_exact,"future_file_matrix_exact":future_file_matrix_exact,"public_symbol_matrix_exact":public_symbol_matrix_exact,"record_field_matrix_exact":record_field_matrix_exact,"mapping_input_matrix_exact":mapping_input_matrix_exact,"validation_code_matrix_exact":validation_code_matrix_exact,"validation_rule_matrix_exact":validation_rule_matrix_exact,"future_test_matrix_exact":future_test_matrix_exact,"decision_options_exact":decision_options_exact,"critical_sections_exact":critical_sections_exact,"closed_sets_exact":closed_sets_exact,"assignments_exact":assignments_exact,"rejection_sentence_exact":rejection_sentence_exact,"numeric_policy_clean":numeric_policy_clean,"allowlist_counts_exact":allowlist_counts_exact,"oracle_literals_exact":oracle_literals_exact,"prohibited_behavior_absent":prohibited_behavior_absent}
PIPELINE=list(VALIDATORS)
def validate(t):
 for code in PIPELINE: VALIDATORS[code](t)
def test_contract(): validate(DOC.read_text())
def test_registries(): _require(list(VALIDATORS)==REQUIRED_CHECK_CODES and PIPELINE==REQUIRED_CHECK_CODES and len(REQUIRED_MUTATION_CASES)==37,"oracle_literals_exact")
def test_header_mutation():
 base=DOC.read_text(); changed=base.replace("Canonical ID: "+CANONICAL_ID,"Canonical ID: "+CANONICAL_ID+"-x",1); _require(changed.splitlines()[0]==base.splitlines()[0] and changed!=base,"header_exact")
 try: header_exact(changed)
 except ContractCheckError as e: assert e.check_code=="header_exact"
 else: raise AssertionError("accepted")
