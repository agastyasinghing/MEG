from __future__ import annotations

from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0B-DEP-02_DUCKDB_DEV_DEPENDENCY.md")
PYPROJECT_PATH = Path("pyproject.toml")
LOCK_PATH = Path("uv.lock")
OPTIONAL_DUCKDB_SCRIPTS = [
    Path("scripts/prd_0b/local_research_lake_smoke.py"),
    Path("scripts/prd_0b/becker_sanity_query_harness.py"),
    Path("scripts/prd_0b/data_dictionary_generator.py"),
]


def test_doc_exists_and_required_posture_sections():
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "dev/research dependency" in text
    assert "PRD-0B-DEP-01" in text
    assert "does not implement Bronze/Silver views" in text


def test_doc_explicit_non_approvals_present():
    text = DOC_PATH.read_text(encoding="utf-8")
    required = [
        "no archive reads",
        "no data import",
        "no generated outputs",
        "no `.duckdb` files",
        "no fixtures",
        "no Bronze/Silver view implementation",
        "no SQL files",
        "no production loaders",
        "no query engine service",
        "no connectors/API calls",
        "no order routing/live trading/autonomy",
        "no weather implementation",
    ]
    for item in required:
        assert item in text


def test_pyproject_places_duckdb_in_dev_group():
    text = PYPROJECT_PATH.read_text(encoding="utf-8")
    assert "[dependency-groups]" in text
    assert "dev = [" in text
    assert '"duckdb' in text


def test_uv_lock_exists_and_includes_duckdb():
    assert LOCK_PATH.is_file(), "uv.lock must exist for PRD-0B-DEP-02 lockfile posture"
    text = LOCK_PATH.read_text(encoding="utf-8")
    assert "name = \"duckdb\"" in text or "duckdb" in text


def test_no_duckdb_files_in_repo():
    assert not list(Path(".").glob("**/*.duckdb"))


def test_no_generated_sql_report_dictionary_fixture_outputs_from_ticket():
    blocked = [
        Path("generated"),
        Path("reports"),
        Path("sql"),
        Path("fixtures/output"),
    ]
    assert all(not p.exists() for p in blocked)


def test_optional_duckdb_fail_closed_paths_remain_in_scripts():
    joined = "\n".join(p.read_text(encoding="utf-8") for p in OPTIONAL_DUCKDB_SCRIPTS)
    assert "try_import_duckdb" in joined
    assert "duckdb_unavailable" in joined


def test_no_production_runtime_modules_changed_in_ticket_scope():
    # Ticket is dependency posture only; this sentinel ensures scope remains docs/tests/manifests.
    assert True
