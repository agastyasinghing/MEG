"""Static contract test for the Stage 3 approval request; no runtime imports."""
from pathlib import Path
DOC = Path('docs/prd/WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-APPROVAL-REQUEST-01.md')
CANONICAL_ID = 'WEATHER-BOT-STAGE3-RETROSPECTIVE-SCORING-IMPLEMENTATION-APPROVAL-REQUEST-01'
ACTUAL_PR_366_MERGE_SHA = '24c229970392096dc8a61124f6e80ac724244a08'
class ContractCheckError(AssertionError):
    def __init__(self, check_code: str): self.check_code = check_code; super().__init__(check_code)
def _require(condition: bool, check_code: str):
    if not condition: raise ContractCheckError(check_code)
def header_exact(text: str):
    lines=text.splitlines(); _require(lines[:3] == [f'# {CANONICAL_ID}', '', f'Canonical ID: {CANONICAL_ID}'] and text.count(f'Canonical ID: {CANONICAL_ID}') == 1, 'header_exact')
def predecessor_exact(text: str):
    _require(text.count(f'ACTUAL_PR_366_MERGE_SHA: {ACTUAL_PR_366_MERGE_SHA}') == 1 and '53822e5dc3115b7989c7f015c6120b9faa5a2a54 is not the actual' in text, 'predecessor_exact')
def critical_sections_exact(text: str):
    for item in ['Request status: request_prepared_implementation_not_approved.', 'A human decision outside this document is required.', 'This ticket does not approve or create the Stage 3 package;', 'market_id is non-routing only.', 'WEATHER-BOT-STAGE3-BINARY-PROBABILITY-RECORD-IMPLEMENTATION-01']:
        _require(item in text, 'critical_sections_exact')
def heading_sequence_exact(text: str):
    expected=['Status and scope','Immediate predecessor and merge verification','Approval-request purpose and decision boundary','Readiness-review basis','Requested implementation slice identity','Exact future changed-file matrix','Exact future public-symbol matrix','Exact future record-field matrix','Exact mapping-input matrix','Exact validation-code matrix','Exact validation-rule matrix','Exact future test matrix','Dependency and import boundary','Canonical routing and target boundary','Probability-domain boundary','Temporal availability and no-lookahead boundary','Provenance and immutability boundary','Failure posture and deterministic output','Explicit future implementation non-goals','Approval decision options','Current request status','Human decision and separate-approval boundary','Fail-closed requirements','Explicit non-approvals','Canonical routing posture','Recommended next ticket','Machine-checkable assignments','Acceptance criteria']
    _require([x[3:] for x in text.splitlines() if x.startswith('## ')] == expected, 'heading_sequence_exact')
def complete_validator(text: str):
    header_exact(text); heading_sequence_exact(text); predecessor_exact(text); critical_sections_exact(text)
def test_contract(): complete_validator(DOC.read_text())
def test_line_three_suffix_mutation_rejected():
    text=DOC.read_text(); changed=text.replace(f'Canonical ID: {CANONICAL_ID}', f'Canonical ID: {CANONICAL_ID}-X', 1)
    try: header_exact(changed)
    except ContractCheckError as error: assert error.check_code == 'header_exact'
    else: raise AssertionError('mutation accepted')
