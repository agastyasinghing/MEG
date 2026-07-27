"""Static contract for the Stage 3 evaluation-result approval request."""
import ast
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "docs/prd/WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-IMPLEMENTATION-APPROVAL-REQUEST-01.md"
ALLOWLIST_PATH = ROOT / "tests/core/canonical_id_allowlist.py"
SELF_PATH = pathlib.Path(__file__).resolve()
TITLE = "WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-IMPLEMENTATION-APPROVAL-REQUEST-01"
MERGE_SHA = "96935708eea4b197283a5a399c8ef57e63b6e795"
APPROVED_HEAD = "e1bbd931813dc79d0254592a51584653bddb5dab"
HEADINGS = ["Status and decision boundary", "Predecessor and base", "Authority and requested future slice", "Exact public API", "Exact enums", "Immutable payloads", "Evaluation result record", "Validation result and signatures", "Mapping keys, shape, and adaptation", "Text, timestamp, posture, and supersession", "Counts, reasons, uncertainty, and provenance", "Compatibility matrices", "Payload validation", "Validation codes", "Validation order", "Safety, dependencies, and non-goals", "Machine assignments", "Acceptance criteria"]
API = ["EvaluationResultKind", "EvaluationResultSupportStatus", "EvaluationResultMethodRole", "EvaluationResultValidationSeverity", "EvaluationResultValidationCode", "ScalarScoreResultPayload", "CalibrationBinResultPayload", "DecompositionResultPayload", "DistributionDiagnosticResultPayload", "EnsembleDiagnosticResultPayload", "PairedComparisonResultPayload", "EvaluationResultRecord", "EvaluationResultValidationResult", "evaluation_result_record_from_mapping", "validate_evaluation_result_record"]
KINDS = ["scalar_score_result", "calibration_bin_result", "decomposition_result", "distribution_diagnostic_result", "ensemble_diagnostic_result", "paired_comparison_result"]
SUPPORT = ["supported", "insufficient", "blocked", "unavailable"]
ROLES = ["candidate", "climatology_baseline", "persistence_baseline", "paired_comparison"]
PAYLOADS = {
    "ScalarScoreResultPayload": ["result_value: float", "score_direction: str", "result_domain_posture: str"],
    "CalibrationBinResultPayload": ["bin_id: str", "bin_index: int", "bin_boundary_policy_id: str", "sample_count: int", "mean_predicted_probability: float", "observed_outcome_frequency: float", "ordered_bin_posture: str"],
    "DecompositionResultPayload": ["decomposition_policy_id: str", "reliability_value: float", "resolution_value: float", "uncertainty_value: float", "component_posture: str"],
    "DistributionDiagnosticResultPayload": ["pit_treatment_policy_id: str", "ordered_bin_ids: tuple[str, ...]", "ordered_bin_counts: tuple[int, ...]", "ordered_content_posture: str"],
    "EnsembleDiagnosticResultPayload": ["tie_treatment_policy_id: str", "ordered_rank_ids: tuple[str, ...]", "ordered_rank_counts: tuple[int, ...]", "ensemble_comparability_posture: str", "ordered_content_posture: str"],
    "PairedComparisonResultPayload": ["candidate_result_id: str", "baseline_result_id: str", "baseline_type: BaselineType", "comparison_direction: str", "paired_comparison_value: float", "paired_scope_posture: str"],
}
FIELDS = ["evaluation_result_id: str", "result_kind: EvaluationResultKind", "artifact_id: ScoringArtifact", "artifact_version: str", "evaluation_definition_id: str", "evaluation_definition_version: str", "evaluation_run_id: str", "method_role: EvaluationResultMethodRole", "method_id: str", "method_version: str", "prediction_representation: ScoringPredictionRepresentation", "target_posture: str", "split_id: str", "split_version: str", "fold_id: str", "cutoff_identity: str", "paired_test_record_set_id: str", "eligibility_policy_id: str", "aggregation_rule_id: str", "weighting_rule_id: str", "stratum_id: str", "eligible_record_count: int", "excluded_record_count: int", "blocked_record_count: int", "total_considered_record_count: int", "exclusion_block_reason_summary: tuple[str, ...]", "uncertainty_method_id: str | None", "uncertainty_level_id: str | None", "support_status: EvaluationResultSupportStatus", "result_payload: ScalarScoreResultPayload | CalibrationBinResultPayload | DecompositionResultPayload | DistributionDiagnosticResultPayload | EnsembleDiagnosticResultPayload | PairedComparisonResultPayload", "provenance: tuple[str, ...]", "result_created_at: str", "supersedes_result_id_when_applicable: str | None = None"]
CODES = ["MISSING_REQUIRED_FIELD", "UNEXPECTED_FIELD", "BLANK_REQUIRED_TEXT", "INVALID_RESULT_KIND", "INVALID_ARTIFACT", "INVALID_METHOD_ROLE", "INVALID_PREDICTION_REPRESENTATION", "INVALID_SUPPORT_STATUS", "INVALID_FIXED_POSTURE", "INVALID_RECORD_COUNT", "SAMPLE_ACCOUNTING_MISMATCH", "INVALID_REASON_SUMMARY", "MISSING_REQUIRED_REASON", "UNCERTAINTY_FIELDS_MISMATCH", "EMPTY_PROVENANCE", "INVALID_PROVENANCE_REF", "INVALID_RESULT_CREATED_AT", "RESULT_KIND_ARTIFACT_MISMATCH", "REPRESENTATION_MISMATCH", "METHOD_ROLE_MISMATCH", "INVALID_PAYLOAD_TYPE", "INVALID_SCALAR_SCORE_PAYLOAD", "INVALID_CALIBRATION_BIN_PAYLOAD", "INVALID_DECOMPOSITION_PAYLOAD", "INVALID_DISTRIBUTION_DIAGNOSTIC_PAYLOAD", "INVALID_ENSEMBLE_DIAGNOSTIC_PAYLOAD", "INVALID_PAIRED_COMPARISON_PAYLOAD", "PAIR_BASELINE_NOT_APPROVED", "PAIR_RESULT_IDENTITY_COLLISION", "SELF_SUPERSESSION"]
DECISIONS = ["approve_later_evaluation_result_record_implementation_ticket", "request_approval_request_revision", "hold", "block"]
NON_GOALS = ["score calculation", "diagnostic calculation", "comparison calculation", "uncertainty calculation", "support-status selection", "probability generation", "label joining", "split or baseline execution", "evaluation execution", "claim creation or evaluation", "evidence-gate evaluation", "data or corpus creation", "source fetching", "persistence", "serialization", "database tables or migrations", "reports or exports", "backtesting or simulation", "market-price comparison execution", "paper trading", "trading", "order placement", "runtime orchestration", "autonomy", "production behavior"]


def section(text, heading):
    match = re.search(rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)", text, re.M | re.S)
    assert match
    return match.group("body")


def numbered(body):
    return re.findall(r"^\d+\. `([^`]+)`$", body, re.M)


def table(body):
    rows = [tuple(c.strip().strip("`") for c in line.strip("|").split("|")) for line in body.splitlines() if line.startswith("|") and "---" not in line]
    return rows[1:]


def test_exact_identity_headings_predecessor_and_decision_boundary():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert text.startswith(f"# {TITLE}\n\nCanonical ID: {TITLE}\n")
    assert [line[3:] for line in text.splitlines() if line.startswith("## ")] == HEADINGS
    predecessor = section(text, "Predecessor and base")
    assert predecessor.count(MERGE_SHA) == 2 and APPROVED_HEAD in predecessor
    assert "Externally verified" in predecessor and "locally confirmed" in predecessor
    assert "Remote fetch was unavailable in the sandbox" in predecessor and "preview merge SHA" in predecessor
    status = section(text, "Status and decision boundary")
    assert numbered(status) == DECISIONS
    assert "request_prepared_implementation_not_approved" in status


def test_future_scope_api_enums_and_payload_literal_oracles():
    text = DOC_PATH.read_text(encoding="utf-8")
    future = section(text, "Authority and requested future slice")
    assert numbered(future) == ["meg/weather/stage3/evaluation_result_record.py", "tests/core/test_weather_bot_stage3_evaluation_result_record.py"]
    assert "No existing file may be modified" in future and "must not calculate" in future
    assert numbered(section(text, "Exact public API")) == API
    enums = table(section(text, "Exact enums"))
    assert [r[2] for r in enums[:6]] == KINDS
    assert [r[2] for r in enums[6:10]] == SUPPORT
    assert [r[2] for r in enums[10:14]] == ROLES
    assert enums[14:] == [("EvaluationResultValidationSeverity", "PASSED", "passed"), ("EvaluationResultValidationSeverity", "BLOCKED", "blocked")]
    payload = section(text, "Immutable payloads")
    for name, fields in PAYLOADS.items():
        line = next(line for line in payload.splitlines() if line.startswith(f"- `{name}`"))
        positions = [line.index(f"`{field}`") for field in fields]
        assert positions == sorted(positions)
    assert payload.count("@dataclass(frozen=True)") == 1 and "no validation or normalization in `__post_init__`" in payload


def test_record_result_signatures_keys_and_mapping_rules():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert numbered(section(text, "Evaluation result record")) == FIELDS
    result = section(text, "Validation result and signatures")
    assert numbered(result) == ["severity: EvaluationResultValidationSeverity", "passed: bool", "codes: tuple[EvaluationResultValidationCode, ...] = ()"]
    assert "def evaluation_result_record_from_mapping(\n    mapping: object," in result
    assert "def validate_evaluation_result_record(\n    record: EvaluationResultRecord," in result
    assert "public source position 14" in result and "position 15" in result
    mapping = section(text, "Mapping keys, shape, and adaptation")
    assert numbered(mapping) == [field.split(":")[0] for field in FIELDS[:32]]
    for phrase in ["type(key) is str", "lexical order", "original Mapping iteration order", "string-subclass key", "exactly 32 ordered", "never `BaseException`", "no enum or list adaptation", "never adapt a nested mapping", "partial record"]:
        assert phrase in mapping


def test_text_accounting_provenance_matrices_and_payload_rules():
    text = DOC_PATH.read_text(encoding="utf-8")
    text_rules = section(text, "Text, timestamp, posture, and supersession")
    for phrase in ["type(value) is str", "RFC3339/ISO-8601", "explicit UTC offset", "venue_defined_settlement_outcome", "BLANK_REQUIRED_TEXT", "INVALID_FIXED_POSTURE", "SELF_SUPERSESSION", "exactly once"]:
        assert phrase in text_rules
    grouped = section(text, "Counts, reasons, uncertainty, and provenance")
    for phrase in ["exact built-in integers >= 0", "SAMPLE_ACCOUNTING_MISMATCH", "INVALID_REASON_SUMMARY", "MISSING_REQUIRED_REASON", "UNCERTAINTY_FIELDS_MISMATCH", "EMPTY_PROVENANCE", "mutually exclusive", "sort, or deduplicate"]:
        assert phrase in grouped
    matrix = table(section(text, "Compatibility matrices"))
    assert len(matrix) == 6 and [r[0] for r in matrix] == KINDS
    payload = section(text, "Payload validation")
    for code in CODES[21:29]:
        assert f"`{code}`" in payload
    for boundary in ["[0.0, 1.0]", "NaN", "infinities", "summing to eligible count", "Never calculate or recompute comparison"]:
        assert boundary in payload


def test_codes_order_assignments_non_goals_and_targeted_mutations():
    text = DOC_PATH.read_text(encoding="utf-8")
    items = numbered(section(text, "Validation codes"))
    assert [item.split(" = ")[0] for item in items] == CODES
    assert [item.split('"')[1] for item in items] == [code.lower() for code in CODES]
    order = section(text, "Validation order")
    assert all(f"({i})" in order for i in range(1, 26))
    assert "Preserve repeated occurrences" in order and "never finally sort or deduplicate" in order
    safety = section(text, "Safety, dependencies, and non-goals")
    assert all(goal in safety for goal in NON_GOALS)
    assert "Phase 0A rail" in safety and "either Phase 0A job" in safety and "Phase 0B and DuckDB remain unaffected" in safety
    assert "`condition_id`, `token_id`, and `outcome`" in safety and "`market_id` remains non-routing" in safety and "`token_outcome_pair` remains derived only" in safety
    assignments = section(text, "Machine assignments")
    for literal in ["public_symbol_count: `15`", "payload_count: `6`", "record_field_count: `33`", "required_mapping_key_count: `32`", "validation_code_count: `30`", "validation_group_count: `25`"]:
        assert literal in assignments
    mutations = [("public_symbol_count: `15`", "public_symbol_count: `16`"), ("exactly 32 ordered", "exactly 31 ordered"), ("Never calculate or recompute", "Calculate or recompute"), ("candidate_minus_baseline_lower_is_better", "baseline_minus_candidate")]
    for old, new in mutations:
        assert old in text and new not in text and text.replace(old, new, 1) != text


def test_standard_library_only_and_direct_allowlist_counts():
    tree = ast.parse(SELF_PATH.read_text(encoding="utf-8"))
    imports = {alias.name.split(".")[0] for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom)) for alias in node.names}
    assert imports <= {"ast", "pathlib", "re"}
    source = ALLOWLIST_PATH.read_text(encoding="utf-8")
    allow_tree = ast.parse(source)
    assignment = next(node for node in allow_tree.body if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "ALLOWED_MARKET_ID_OCCURRENCE_LINES")
    allowlist = ast.literal_eval(assignment.value.args[0])
    downstream_node = next(node for node in allow_tree.body if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_ARCH_ALIGN_03_DOWNSTREAM_ARTIFACTS" for t in node.targets))
    downstream = ast.literal_eval(downstream_node.value)
    expected = {
        str(DOC_PATH.relative_to(ROOT)): 1,
        str(SELF_PATH.relative_to(ROOT)): 2,
    }
    for path, count in expected.items():
        assert list(downstream).count(path) == 1
        assert type(allowlist[path]) is int and allowlist[path] == count
        assert source.count(f'"{path}"') == 2
        assert (ROOT / path).read_text(encoding="utf-8").count("market_id") == count
