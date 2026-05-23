from __future__ import annotations

import ast
from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0B-QA-01_DUCKDB_LOCKFILE_CONSOLIDATION_SMOKE.md")
PYPROJECT_PATH = Path("pyproject.toml")
LOCK_PATH = Path("uv.lock")
LOCKFILE_TEST_PATH = Path("tests/core/test_prd_0b_duckdb_dependency_posture.py")
LOCAL_SMOKE_PATH = Path("scripts/prd_0b/local_research_lake_smoke.py")
SANITY_HARNESS_PATH = Path("scripts/prd_0b/becker_sanity_query_harness.py")
DICTIONARY_GEN_PATH = Path("scripts/prd_0b/data_dictionary_generator.py")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_consolidation_doc_exists_and_has_required_sections():
    assert DOC_PATH.is_file()
    text = _read(DOC_PATH)
    required_snippets = [
        "QA/static-preflight only",
        "does not add dependencies",
        "does not modify `pyproject.toml` or `uv.lock`",
        "Why this ticket exists",
        "PRD-0B-DEP-02",
        "Required final repo state",
        "PRD Phase 0B alignment",
        "Verification matrix",
        "Explicit non-approvals",
        "PRD-0B-IMPL-06 Bronze/Silver DuckDB view skeleton",
    ]
    for snippet in required_snippets:
        assert snippet in text


def test_pyproject_duckdb_dependency_posture_is_dev_research_scoped():
    text = _read(PYPROJECT_PATH)
    assert "[dependency-groups]" in text
    assert "dev = [" in text
    assert '"duckdb' in text

    deps_start = text.index("dependencies = [")
    deps_end = text.index("]", deps_start)
    deps_block = text[deps_start:deps_end]
    assert "duckdb" not in deps_block


def test_uv_lock_exists_and_contains_duckdb():
    assert LOCK_PATH.is_file()
    assert "duckdb" in _read(LOCK_PATH)


def test_dependency_posture_test_keeps_mandatory_lock_assertion():
    text = _read(LOCKFILE_TEST_PATH)
    assert "assert LOCK_PATH.is_file()" in text


def test_dependency_posture_test_does_not_return_early_when_lock_missing():
    tree = ast.parse(_read(LOCKFILE_TEST_PATH))
    target_fn = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "test_uv_lock_exists_and_includes_duckdb":
            target_fn = node
            break
    assert target_fn is not None
    assert not any(isinstance(node, ast.Return) for node in ast.walk(target_fn))


def test_optional_fail_closed_duckdb_posture_remains_in_scripts():
    local = _read(LOCAL_SMOKE_PATH)
    sanity = _read(SANITY_HARNESS_PATH)
    dictionary = _read(DICTIONARY_GEN_PATH)

    assert "def try_import_duckdb" in local
    assert "duckdb_unavailable" in local

    assert "try_import_duckdb" in sanity
    assert "duckdb_unavailable" in sanity

    assert "try_import_duckdb" in dictionary
    assert "require_duckdb_but_unavailable" in dictionary


def test_no_duckdb_database_files_exist():
    assert not list(Path(".").glob("**/*.duckdb"))


def test_no_generated_output_directories_exist_for_this_ticket_scope():
    blocked_paths = [
        Path("generated/sql"),
        Path("generated/reports"),
        Path("generated/dictionary"),
        Path("fixtures/output"),
    ]
    assert all(not path.exists() for path in blocked_paths)


def test_no_production_runtime_module_imports_in_this_test_file():
    tree = ast.parse(_read(Path(__file__)))
    blocked_prefixes = ("meg", "src", "app")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                assert top not in blocked_prefixes
        if isinstance(node, ast.ImportFrom) and node.module:
            top = node.module.split(".")[0]
            assert top not in blocked_prefixes
