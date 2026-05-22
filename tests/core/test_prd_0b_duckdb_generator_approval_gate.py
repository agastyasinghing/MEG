from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0B-DEP-01_DUCKDB_GENERATOR_APPROVAL_GATE.md")
PYPROJECT_PATH = Path("pyproject.toml")

DECISION_OPTIONS = {
    "A": {
        "label": "optional_local_only",
        "allowed": True,
        "requires_dependency_pr": False,
    },
    "B": {
        "label": "dev_dependency",
        "allowed": True,
        "requires_dependency_pr": True,
    },
    "C": {
        "label": "runtime_dependency",
        "allowed": False,
        "requires_dependency_pr": True,
    },
}

IMMEDIATE_RECOMMENDATION = {
    "dependency_posture": "optional_local_only",
    "output_modes_allowed": ["stdout_only", "tempdir_only_for_tests"],
    "output_modes_blocked": ["committed_dictionary_requires_separate_approval"],
}

POSTURE_FLAGS = {
    "archive_reads_allowed": False,
    "duckdb_execution_allowed": False,
    "generated_outputs_allowed": False,
    "loader_execution_allowed": False,
    "connectors_allowed": False,
    "api_calls_allowed": False,
    "order_routing_allowed": False,
    "live_trading_allowed": False,
    "autonomous_execution_allowed": False,
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_exists_and_is_static_preflight_only() -> None:
    text = _read(DOC_PATH)
    assert DOC_PATH.exists()
    assert "docs/static-preflight only" in text
    assert "not add DuckDB" in text
    assert "not implement the data dictionary generator" in text
    assert "not read archive payloads" in text
    assert "not run DuckDB" in text


def test_document_contains_prd_phase_0b_alignment_and_prior_impls() -> None:
    text = _read(DOC_PATH)
    for token in [
        "DuckDB + Parquet + Becker setup",
        "Bronze/Silver normalization views",
        "data dictionary",
        "seven sanity queries",
        "query latency gate",
        "PRD-0B-IMPL-01",
        "PRD-0B-IMPL-02",
        "PRD-0B-IMPL-03",
        "PRD-0B-IMPL-04",
        "PRD-0B-IMPL-05",
    ]:
        assert token in text


def test_document_defines_dependency_options_and_recommendation() -> None:
    text = _read(DOC_PATH)
    for token in [
        "Option A: Keep DuckDB optional local-only",
        "Option B: Add DuckDB as dev dependency",
        "Option C: Add DuckDB as runtime dependency",
        "keep DuckDB optional local-only",
        "unless a separate dependency PR is explicitly approved first",
        "duckdb_unavailable",
    ]:
        assert token in text


def test_document_contains_gates_scope_policy_and_non_approvals() -> None:
    text = _read(DOC_PATH)
    required = [
        "Generator approval gates",
        "Approved IMPL-05 scope if this gate passes",
        "Generated dictionary output policy",
        "CI/testing policy",
        "Relationship to PRD-0A",
        "Recommended next tickets",
        "Explicit non-approvals",
        "No DuckDB dependency addition",
        "No `pyproject.toml`/lockfile changes",
        "No data dictionary generator",
        "No archive reads",
    ]
    for token in required:
        assert token in text


def test_pyproject_does_not_require_duckdb_for_this_ticket() -> None:
    text = _read(PYPROJECT_PATH).lower()
    assert '"duckdb"' not in text
    assert "duckdb==" not in text


def test_no_generated_dictionary_or_duckdb_report_fixture_output_dirs_exist() -> None:
    forbidden_paths = [
        Path("generated/dictionary/prd_0b"),
        Path("generated/reports/prd_0b"),
        Path("reports/prd_0b"),
        Path("fixtures/output/prd_0b"),
        Path("output/prd_0b"),
        Path("docs/prd/PRD-0B-DEP-01_DUCKDB_GENERATOR_APPROVAL_GATE.json"),
    ]
    for forbidden in forbidden_paths:
        assert not forbidden.exists()
    assert not list(Path(".").rglob("*.duckdb"))


def test_decision_objects_and_posture_flags() -> None:
    assert DECISION_OPTIONS["A"]["allowed"] is True
    assert DECISION_OPTIONS["A"]["label"] == "optional_local_only"

    assert DECISION_OPTIONS["B"]["allowed"] is True
    assert DECISION_OPTIONS["B"]["requires_dependency_pr"] is True

    assert DECISION_OPTIONS["C"]["allowed"] is False

    assert IMMEDIATE_RECOMMENDATION["dependency_posture"] == "optional_local_only"
    assert IMMEDIATE_RECOMMENDATION["output_modes_allowed"] == [
        "stdout_only",
        "tempdir_only_for_tests",
    ]
    assert "committed_dictionary_requires_separate_approval" in IMMEDIATE_RECOMMENDATION["output_modes_blocked"]

    assert all(flag is False for flag in POSTURE_FLAGS.values())
