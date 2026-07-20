"""Static, deterministic approval-request contract; no production imports."""
import ast
import re
from pathlib import Path

DOC = Path("docs/prd/WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01.md")
ALLOWLIST = Path("tests/core/canonical_id_allowlist.py")
CANONICAL_ID = "WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01"
ACTUAL_PR_368_MERGE_SHA = "1676199c89f2d5d472ea14c66ae841c1878c6018"
EXPECTED_HEADINGS = [
    "Status and request scope",
    "Actual PR #368 merge predecessor",
    "Controlling strict-OOS planning contract",
    "Requested future implementation slice identity",
    "Exact future changed-file matrix",
    "Exact future public-symbol matrix",
    "Exact future enum matrices",
    "Exact future record-field matrix",
    "Exact fixed-posture matrix",
    "Exact mapping-input matrix",
    "Exact single-record validation matrix",
    "Exact collection-validation matrix",
    "Exact validation-code matrix",
    "Exact validation-order contract",
    "Exact future test matrix",
    "Dependency and import boundary",
    "Canonical routing boundary",
    "Temporal and no-lookahead boundary",
    "Leakage-group and fold boundary",
    "Assignment and exclusion semantics",
    "Baseline parity boundary",
    "Explicit future implementation non-goals",
    "Approval decision options",
    "Current request status",
    "Human decision and separate-approval boundary",
    "Fail-closed requirements",
    "Explicit non-approvals",
    "Machine-checkable assignments",
    "Acceptance criteria",
]
HEADING_CATEGORIES = {
    "header": ["Status and request scope"],
    "predecessor": ["Actual PR #368 merge predecessor"],
    "controls": ["Controlling strict-OOS planning contract"],
    "identity": ["Requested future implementation slice identity"],
    "future_files": ["Exact future changed-file matrix"],
    "public_symbols": ["Exact future public-symbol matrix"],
    "enums": ["Exact future enum matrices"],
    "record_fields": ["Exact future record-field matrix"],
    "fixed_postures": ["Exact fixed-posture matrix"],
    "mapping": ["Exact mapping-input matrix"],
    "single_validation": ["Exact single-record validation matrix"],
    "collection_validation": ["Exact collection-validation matrix"],
    "validation_codes": ["Exact validation-code matrix"],
    "validation_order": ["Exact validation-order contract"],
    "future_tests": ["Exact future test matrix"],
    "dependency": ["Dependency and import boundary"],
    "canonical": ["Canonical routing boundary"],
    "temporal": ["Temporal and no-lookahead boundary"],
    "leakage": ["Leakage-group and fold boundary"],
    "assignment": ["Assignment and exclusion semantics"],
    "baseline": ["Baseline parity boundary"],
    "non_goals": ["Explicit future implementation non-goals"],
    "decisions": ["Approval decision options"],
    "status": ["Current request status"],
    "human": ["Human decision and separate-approval boundary"],
    "fail_closed": ["Fail-closed requirements"],
    "non_approvals": ["Explicit non-approvals"],
    "machine": ["Machine-checkable assignments"],
    "acceptance": ["Acceptance criteria"],
}
EXPECTED_FUTURE_FILES = [
    "meg/weather/stage3/strict_oos_split.py",
    "tests/core/test_weather_bot_stage3_strict_oos_split.py",
]
EXPECTED_PUBLIC_SYMBOLS = [
    "SplitRole",
    "SplitApplicabilityMode",
    "SplitAssignmentStatus",
    "OverlapControlPosture",
    "SplitValidationSeverity",
    "SplitValidationCode",
    "StrictOOSSplitAssignment",
    "StrictOOSSplitValidationResult",
    "strict_oos_split_assignment_from_mapping",
    "validate_strict_oos_split_assignment",
    "validate_strict_oos_split_assignments",
]
EXPECTED_ENUMS = {
    "SplitRole": [("TRAIN", "train"), ("CALIBRATION", "calibration"), ("TEST", "test")],
    "SplitApplicabilityMode": [("PRIMARY_TEMPORAL", "primary_temporal"), ("LEAVE_STATION_OUT", "leave_station_out"), ("LEAVE_YEAR_OUT", "leave_year_out"), ("FAMILY_STRATIFIED", "family_stratified"), ("SEASON_OR_REGIME_STRATIFIED", "season_or_regime_stratified")],
    "SplitAssignmentStatus": [("ASSIGNED", "assigned"), ("BLOCKED", "blocked")],
    "OverlapControlPosture": [("NOT_REQUIRED", "not_required"), ("SATISFIED", "satisfied"), ("UNSATISFIED", "unsatisfied")],
    "SplitValidationSeverity": [("PASSED", "passed"), ("BLOCKED", "blocked")],
}
EXPECTED_RECORD_FIELDS = [
    ("split_assignment_id", "str"), ("split_id", "str"), ("split_version", "str"), ("fold_id", "str"), ("fold_index", "int"), ("prediction_record_id", "str"), ("condition_id", "str"), ("token_id", "str"), ("outcome", "str"), ("settlement_rule_id", "str"), ("settlement_rule_version", "str"), ("split_role", "SplitRole"), ("applicability_modes", "tuple[SplitApplicabilityMode, ...]"), ("assignment_status", "SplitAssignmentStatus"), ("fold_cutoff", "str"), ("prediction_as_of", "str"), ("input_publication_available_at", "str"), ("target_start_at", "str"), ("target_end_at", "str"), ("label_available_at", "str | None"), ("leakage_group_id", "str"), ("overlap_control_posture", "OverlapControlPosture"), ("primary_split_posture", "str"), ("tuning_posture", "str"), ("calibration_posture", "str"), ("baseline_parity_posture", "str"), ("exclusion_reason", "str | None"), ("provenance_refs", "tuple[str, ...]"), ("created_at", "str"), ("supersedes_split_assignment_id", "str | None = None"),
]
EXPECTED_FIXED_POSTURES = [
    ("primary_split_posture", "rolling_origin_or_walk_forward_required"),
    ("tuning_posture", "train_or_calibration_only"),
    ("calibration_posture", "separate_when_required"),
    ("baseline_parity_posture", "same_folds_and_eligibility_required"),
]
EXPECTED_CODES = [
    "MISSING_REQUIRED_FIELD = \"missing_required_field\"", "UNEXPECTED_FIELD = \"unexpected_field\"", "BLANK_REQUIRED_TEXT = \"blank_required_text\"", "INVALID_SPLIT_ROLE = \"invalid_split_role\"", "INVALID_APPLICABILITY_MODES = \"invalid_applicability_modes\"", "INVALID_ASSIGNMENT_STATUS = \"invalid_assignment_status\"", "INVALID_OVERLAP_CONTROL_POSTURE = \"invalid_overlap_control_posture\"", "INVALID_INTEGER_FIELD = \"invalid_integer_field\"", "INVALID_FIXED_POSTURE = \"invalid_fixed_posture\"", "INVALID_TIMESTAMP = \"invalid_timestamp\"", "INPUT_AVAILABLE_AFTER_PREDICTION = \"input_available_after_prediction\"", "PREDICTION_AFTER_FOLD_CUTOFF = \"prediction_after_fold_cutoff\"", "INVALID_TARGET_WINDOW = \"invalid_target_window\"", "TRAIN_OR_CALIBRATION_AFTER_CUTOFF = \"train_or_calibration_after_cutoff\"", "TRAIN_OR_CALIBRATION_LABEL_UNAVAILABLE_BY_CUTOFF = \"train_or_calibration_label_unavailable_by_cutoff\"", "TEST_NOT_STRICTLY_AFTER_CUTOFF = \"test_not_strictly_after_cutoff\"", "TEST_LABEL_AVAILABLE_BY_CUTOFF = \"test_label_available_by_cutoff\"", "ASSIGNED_WITH_EXCLUSION_REASON = \"assigned_with_exclusion_reason\"", "BLOCKED_WITHOUT_EXCLUSION_REASON = \"blocked_without_exclusion_reason\"", "UNSATISFIED_OVERLAP_CONTROL_ASSIGNED = \"unsatisfied_overlap_control_assigned\"", "EMPTY_PROVENANCE_REFS = \"empty_provenance_refs\"", "INVALID_PROVENANCE_REF = \"invalid_provenance_ref\"", "SELF_SUPERSESSION = \"self_supersession\"", "INVALID_ASSIGNMENT_COLLECTION_TYPE = \"invalid_assignment_collection_type\"", "EMPTY_ASSIGNMENT_COLLECTION = \"empty_assignment_collection\"", "DUPLICATE_ASSIGNMENT_ID = \"duplicate_assignment_id\"", "DUPLICATE_FOLD_RECORD_ASSIGNMENT = \"duplicate_fold_record_assignment\"", "DUPLICATE_TEST_RECORD = \"duplicate_test_record\"", "INCONSISTENT_SPLIT_ID = \"inconsistent_split_id\"", "INCONSISTENT_SPLIT_VERSION = \"inconsistent_split_version\"", "INCONSISTENT_FOLD_DEFINITION = \"inconsistent_fold_definition\"", "NON_MONOTONIC_FOLD_CUTOFF = \"non_monotonic_fold_cutoff\"", "LEAKAGE_GROUP_ROLE_CONFLICT = \"leakage_group_role_conflict\"",
]
EXPECTED_DECISIONS = [
    "approve_later_strict_oos_split_assignment_implementation_ticket",
    "request_approval_request_revision",
    "hold",
    "block",
]
EXPECTED_MACHINE = {
    "ticket": "WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01",
    "actual_pr_368_merge_sha": "1676199c89f2d5d472ea14c66ae841c1878c6018",
    "request_status": "request_prepared_implementation_not_approved",
    "implementation_approved": "false",
    "executes_splits": "false",
    "creates_split_files": "false",
    "partitions_datasets": "false",
    "approves_scoring": "false",
    "separate_human_decision_required": "true",
}
REQUIRED_SECTION_PHRASES = {
    "Status and request scope": ["documentation/static-test-only", "does not approve implementation", "does not execute splits", "does not create split files", "does not partition datasets", "does not approve scoring", "a separate human decision is required"],
    "Controlling strict-OOS planning contract": ["docs/prd/WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01.md", "meg/weather/stage3/binary_probability_record.py", "PR #360 planning contract is requirements only, not implementation approval"],
    "Requested future implementation slice identity": ["No split generator, fold builder, dataset partitioner, scorer, serializer, repository, service, or execution function is requested"],
    "Dependency and import boundary": ["standard-library-only", "No I/O, providers, services, persistence"],
    "Canonical routing boundary": ["condition_id", "token_id", "outcome", "market_id", "must not become a routing key", "token_outcome_pair"],
    "Temporal and no-lookahead boundary": ["timezone-aware", "does not approve implementation", "does not execute splits"],
    "Leakage-group and fold boundary": ["must not generate folds", "choose cutoffs", "partition datasets"],
    "Assignment and exclusion semantics": ["Assigned records", "Blocked records"],
    "Baseline parity boundary": ["same_folds_and_eligibility_required", "without approving baseline calculation, scoring"],
    "Explicit future implementation non-goals": ["generate fold assignments", "grant autonomy"],
    "Current request status": ["request_prepared_implementation_not_approved"],
    "Human decision and separate-approval boundary": ["A separate human decision is required", "does not approve implementation"],
    "Fail-closed requirements": ["fail closed with ordered codes"],
    "Explicit non-approvals": ["does not approve implementation", "does not execute splits", "does not create split files", "does not partition datasets", "does not approve scoring", "A separate human decision is required"],
    "Acceptance criteria": ["no `meg/` changes", "PR opened but not merged"],
}
EXPECTED_ALLOWLIST_PATHS = [
    "docs/prd/WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-IMPLEMENTATION-APPROVAL-REQUEST-01.md",
    "tests/core/test_weather_bot_stage3_strict_oos_split_implementation_approval_request_01.py",
]


def _read_doc():
    return DOC.read_text()


def _headings(text):
    return re.findall(r"^## (.+)$", text, re.MULTILINE)


def _sections(text):
    matches = list(re.finditer(r"^## (.+)$", text, re.MULTILINE))
    result = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1)] = text[start:end]
    return result


def _table_rows(section):
    rows = []
    for line in section.splitlines():
        if line.startswith("|"):
            rows.append([cell.strip().strip("`") for cell in line.strip().strip("|").split("|")])
    return rows


def _numbered_code_rows(section):
    rows = []
    for line in section.splitlines():
        match = re.match(r"^\d+\. `(.+)`$", line)
        if match:
            rows.append(match.group(1))
    return rows


def _bullet_code_rows(section):
    rows = []
    for line in section.splitlines():
        match = re.match(r"^- `(.+)`$", line)
        if match:
            rows.append(match.group(1))
    return rows


def _machine_assignments(section):
    values = {}
    in_block = False
    future_files = []
    for line in section.splitlines():
        if line == "```yaml":
            in_block = True
            continue
        if line == "```":
            in_block = False
            continue
        if not in_block:
            continue
        if line.startswith("  - "):
            future_files.append(line[4:])
        elif ": " in line:
            key, value = line.split(": ", 1)
            values[key] = value
    return values, future_files


def validate_header(text):
    lines = text.splitlines()
    assert lines[0] == "# " + CANONICAL_ID
    assert lines[2] == "Canonical ID: " + CANONICAL_ID
    assert _headings(text) == EXPECTED_HEADINGS


def validate_predecessor(sections):
    section = sections["Actual PR #368 merge predecessor"]
    assert ACTUAL_PR_368_MERGE_SHA in section
    assert "a5d28d50e82c7d0b101036c89d7f61c6fec564af" in section
    assert "not a preview merge SHA" in section


def validate_future_files(sections):
    rows = _table_rows(sections["Exact future changed-file matrix"])
    assert [row[0] for row in rows[2:]] == EXPECTED_FUTURE_FILES
    assert "must not modify `meg/weather/stage3/__init__.py`" in sections["Exact future changed-file matrix"]


def validate_public_symbols(sections):
    rows = _table_rows(sections["Exact future public-symbol matrix"])
    assert [row[1] for row in rows[2:]] == EXPECTED_PUBLIC_SYMBOLS


def validate_enums(sections):
    section = sections["Exact future enum matrices"]
    for enum_name, expected in EXPECTED_ENUMS.items():
        match = re.search(r"^### " + re.escape(enum_name) + r"\n(.+?)(?=^### |\Z)", section, re.MULTILINE | re.DOTALL)
        assert match is not None
        rows = _table_rows(match.group(1))
        assert [tuple(row) for row in rows[2:]] == expected


def validate_record_fields(sections):
    actual = []
    for line in sections["Exact future record-field matrix"].splitlines():
        match = re.match(r"^\| \d+ \| `([^`]+)` \| `([^`]+)` \|$", line)
        if match:
            actual.append((match.group(1), match.group(2)))
    assert actual == EXPECTED_RECORD_FIELDS
    assert "Request one frozen dataclass: `StrictOOSSplitAssignment`" in sections["Exact future record-field matrix"]


def validate_fixed_postures(sections):
    rows = _table_rows(sections["Exact fixed-posture matrix"])
    assert [tuple(row) for row in rows[2:]] == EXPECTED_FIXED_POSTURES


def validate_validation_codes(sections):
    assert _numbered_code_rows(sections["Exact validation-code matrix"]) == EXPECTED_CODES


def validate_decisions(sections):
    assert _bullet_code_rows(sections["Approval decision options"]) == EXPECTED_DECISIONS


def validate_machine(sections):
    values, future_files = _machine_assignments(sections["Machine-checkable assignments"])
    assert values == EXPECTED_MACHINE
    assert future_files == EXPECTED_FUTURE_FILES


def validate_required_phrases(sections):
    for heading, phrases in REQUIRED_SECTION_PHRASES.items():
        body = sections[heading]
        for phrase in phrases:
            assert phrase in body


def validate_allowlist():
    text = ALLOWLIST.read_text()
    for path in EXPECTED_ALLOWLIST_PATHS:
        assert '"' + path + '"' in text


def validate_complete(text):
    validate_header(text)
    sections = _sections(text)
    validate_predecessor(sections)
    validate_future_files(sections)
    validate_public_symbols(sections)
    validate_enums(sections)
    validate_record_fields(sections)
    validate_fixed_postures(sections)
    validate_validation_codes(sections)
    validate_decisions(sections)
    validate_machine(sections)
    validate_required_phrases(sections)


def test_document_contract():
    validate_complete(_read_doc())


def test_allowlist_registration():
    validate_allowlist()


def test_heading_category_partition_is_exact():
    assigned = []
    for headings in HEADING_CATEGORIES.values():
        assigned.extend(headings)
    assert assigned == EXPECTED_HEADINGS
    assert len(set(assigned)) == len(EXPECTED_HEADINGS)


def test_oracles_are_literal_and_not_generated():
    tree = ast.parse(Path(__file__).read_text())
    oracle_names = set()
    for name in globals():
        if name.startswith("EXPECTED_") or name in {"ACTUAL_PR_368_MERGE_SHA", "CANONICAL_ID", "HEADING_CATEGORIES", "REQUIRED_SECTION_PHRASES"}:
            oracle_names.add(name)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in oracle_names:
                    assert isinstance(node.value, (ast.Constant, ast.List, ast.Tuple, ast.Dict, ast.Set))
                    for child in ast.walk(node.value):
                        assert not isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp, ast.BinOp, ast.Call, ast.Name, ast.Subscript, ast.Attribute, ast.JoinedStr))


def _mutate(text, old, new):
    assert old in text
    return text.replace(old, new, 1)


def test_representative_mutations_are_rejected_by_intended_and_complete_validators():
    text = _read_doc()
    mutations = [
        ("predecessor SHA mutation", validate_predecessor, _mutate(text, ACTUAL_PR_368_MERGE_SHA, "0000000000000000000000000000000000000000")),
        ("future file addition", validate_future_files, _mutate(text, "| `tests/core/test_weather_bot_stage3_strict_oos_split.py` | create | static/unit tests for that narrow boundary only |", "| `tests/core/test_weather_bot_stage3_strict_oos_split.py` | create | static/unit tests for that narrow boundary only |\n| `meg/weather/stage3/__init__.py` | modify | forbidden |")),
        ("public symbol addition", validate_public_symbols, _mutate(text, "| 11 | `validate_strict_oos_split_assignments` |", "| 11 | `validate_strict_oos_split_assignments` |\n| 12 | `generate_strict_oos_splits` |")),
        ("enum value mutation", validate_enums, _mutate(text, "| `TRAIN` | `train` |", "| `TRAIN` | `training` |")),
        ("record-field reorder", validate_record_fields, _mutate(text, "| 7 | `condition_id` | `str` |\n| 8 | `token_id` | `str` |", "| 7 | `token_id` | `str` |\n| 8 | `condition_id` | `str` |")),
        ("fixed-posture mutation", validate_fixed_postures, _mutate(text, "rolling_origin_or_walk_forward_required", "rolling_origin_optional")),
        ("validation-code reorder", validate_validation_codes, _mutate(text, "1. `MISSING_REQUIRED_FIELD", "1. `UNEXPECTED_FIELD")),
        ("decision-option mutation", validate_decisions, _mutate(text, "`hold`", "`approve_now`")),
        ("implementation-approval insertion", validate_required_phrases, _mutate(text, "does not approve implementation", "approves implementation")),
        ("split-execution insertion", validate_required_phrases, _mutate(text, "does not execute splits", "executes splits")),
        ("heading insertion", validate_header, _mutate(text, "## Acceptance criteria", "## Extra heading\n\nNo.\n\n## Acceptance criteria")),
        ("heading reorder", validate_header, _mutate(text, "## Status and request scope", "## Actual PR #368 merge predecessor")),
        ("machine-assignment mismatch", validate_machine, _mutate(text, "implementation_approved: false", "implementation_approved: true")),
    ]
    for _name, validator, mutated in mutations:
        sections = _sections(mutated)
        try:
            if validator is validate_header:
                validator(mutated)
            else:
                validator(sections)
        except AssertionError:
            pass
        else:
            raise AssertionError(_name)
        try:
            validate_complete(mutated)
        except AssertionError:
            pass
        else:
            raise AssertionError(_name + " complete")


def test_static_source_safety():
    tree = ast.parse(Path(__file__).read_text())
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in {"write_text", "write_bytes"}
    assert imports == ["ast", "re", "pathlib"]
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.append(node.id)
    assert "eval" not in names
    assert "exec" not in names
