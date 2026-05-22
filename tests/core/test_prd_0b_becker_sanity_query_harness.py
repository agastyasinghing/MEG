import importlib
import json
import sys
from pathlib import Path

MODULE = "scripts.prd_0b.becker_sanity_query_harness"


def _mk_archive(tmp_path: Path, include_json: bool = True) -> Path:
    root = tmp_path / "archive"
    for family in [
        "data/kalshi/markets",
        "data/kalshi/trades",
        "data/polymarket/blocks",
        "data/polymarket/markets",
        "data/polymarket/trades",
        "data/polymarket/legacy_trades",
    ]:
        p = root / family
        p.mkdir(parents=True, exist_ok=True)
        (p / "sample.parquet").write_text("placeholder", encoding="utf-8")
    if include_json:
        (root / "data/polymarket/fpmm_collateral_lookup.json").write_text("{}", encoding="utf-8")
    return root


def test_import_no_duckdb_side_effects():
    sys.modules.pop("duckdb", None)
    mod = importlib.import_module(MODULE)
    assert mod is not None
    assert "duckdb" not in sys.modules


def test_specs_count_and_uniqueness_and_families():
    mod = importlib.import_module(MODULE)
    specs = mod.get_sanity_check_specs()
    assert len(specs) == 7
    names = [s["check_name"] for s in specs]
    assert len(set(names)) == 7
    assert {s.get("family") for s in specs if s["kind"] == "parquet_schema_count"} == set(mod.EXPECTED_ARCHIVE_FAMILIES)


def test_spec_validation_missing_columns(monkeypatch):
    mod = importlib.import_module(MODULE)
    specs = mod.get_sanity_check_specs()
    specs[0]["expected_columns"] = []
    monkeypatch.setattr(mod, "get_sanity_check_specs", lambda: specs)
    errors = mod.validate_sanity_check_specs()
    assert any(e.startswith("missing_expected_columns") for e in errors)


def test_duckdb_unavailable_and_sidecar_behaviors(tmp_path: Path, monkeypatch):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path, include_json=False)
    monkeypatch.setattr(mod, "try_import_duckdb", lambda: (False, None, "duckdb_unavailable"))
    summary = mod.run_becker_sanity_harness(str(root), require_duckdb=False)
    assert summary["sanity_check_count"] == 7
    statuses = {r["check_name"]: r["status"] for r in summary["sanity_results"]}
    assert statuses["poly_fpmm_collateral_lookup_presence"] == "sidecar_missing"
    assert statuses["kalshi_markets_schema_count_sample"] == "duckdb_unavailable"
    assert summary["ok"] is False


def test_require_duckdb_true_fails(tmp_path: Path, monkeypatch):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)
    monkeypatch.setattr(mod, "try_import_duckdb", lambda: (False, None, "duckdb_unavailable"))
    summary = mod.run_becker_sanity_harness(str(root), require_duckdb=True)
    assert summary["ok"] is False


def test_missing_family_and_missing_sample(tmp_path: Path, monkeypatch):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)
    (root / "data/kalshi/trades").rename(root / "data/kalshi/trades_missing")
    (root / "data/polymarket/blocks/sample.parquet").unlink()
    monkeypatch.setattr(mod, "try_import_duckdb", lambda: (False, None, "duckdb_unavailable"))
    summary = mod.run_becker_sanity_harness(str(root))
    statuses = {r["check_name"]: r["status"] for r in summary["sanity_results"]}
    assert statuses["kalshi_trades_schema_count_sample"] == "missing_family"
    assert statuses["poly_blocks_schema_count_sample"] == "missing_sample"


def test_fake_duckdb_path_and_columns_and_failure(tmp_path: Path, monkeypatch):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)

    class FakeConn:
        def __init__(self):
            self.queries = []

        def execute(self, query):
            self.queries.append(query)
            if "legacy_trades" in query:
                raise RuntimeError("boom")

            class R:
                def __init__(self, q):
                    self.q = q

                def fetchall(self):
                    if self.q.startswith("DESCRIBE"):
                        return [("ticker",), ("event_ticker",), ("market_type",), ("title",), ("yes_sub_title",), ("no_sub_title",), ("status",), ("yes_bid",), ("yes_ask",), ("no_bid",), ("no_ask",), ("last_price",), ("volume",), ("volume_24h",), ("open_interest",), ("result",), ("created_time",), ("open_time",), ("close_time",), ("_fetched_at",)]
                    return [(3,)]

            return R(query)

        def close(self):
            return None

    class FakeDuck:
        def __init__(self):
            self.paths = []

        def connect(self, path):
            self.paths.append(path)
            return FakeConn()

    fake = FakeDuck()
    monkeypatch.setattr(mod, "try_import_duckdb", lambda: (True, fake, None))
    summary = mod.run_becker_sanity_harness(str(root))
    assert fake.paths and all(p == ":memory:" for p in fake.paths)
    statuses = {r["check_name"]: r["status"] for r in summary["sanity_results"]}
    assert statuses["kalshi_markets_schema_count_sample"] == "passed"
    assert statuses["kalshi_trades_schema_count_sample"] == "missing_expected_columns"
    assert statuses["poly_legacy_fpmm_trades_schema_count_sample"] == "query_failed"


def test_cli_json_and_invalid_root(tmp_path: Path, capsys, monkeypatch):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)
    monkeypatch.setattr(mod, "try_import_duckdb", lambda: (False, None, "duckdb_unavailable"))
    rc = mod.main(["run", "--archive-root", str(root), "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    parsed = json.loads(out)
    assert parsed["sanity_check_count"] == 7
    assert list(tmp_path.rglob("*.duckdb")) == []
    bad_rc = mod.main(["run", "--archive-root", str(tmp_path / "missing")])
    assert bad_rc != 0


def test_doc_and_no_prod_runtime_imports():
    text = Path("docs/prd/PRD-0B-IMPL-02_BECKER_SANITY_QUERY_HARNESS.md").read_text(encoding="utf-8")
    assert "local-only" in text.lower()
    assert "no committed data" in text
    assert "no dependency added" in text
    assert "no archive outputs" in text


def test_invalid_specs_fail_closed_before_archive_or_duckdb(tmp_path: Path, monkeypatch):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)

    specs = mod.get_sanity_check_specs()
    specs[0]["expected_columns"] = []
    monkeypatch.setattr(mod, "get_sanity_check_specs", lambda: specs)

    calls = {"duckdb": 0, "archive": 0}

    def _duckdb_probe():
        calls["duckdb"] += 1
        return False, None, "duckdb_unavailable"

    def _archive_probe(_archive_root: str):
        calls["archive"] += 1
        return mod.validate_archive_root_path(_archive_root)

    monkeypatch.setattr(mod, "try_import_duckdb", _duckdb_probe)
    monkeypatch.setattr(mod, "validate_archive_root_path", _archive_probe)

    summary = mod.run_becker_sanity_harness(str(root))
    assert summary["ok"] is False
    assert summary["status"] == "invalid_sanity_check_specs"
    assert summary["sanity_check_count"] == 7
    assert summary["wrote_outputs"] is False
    assert summary["created_duckdb_file"] is False
    assert any(str(reason).startswith("missing_expected_columns") for reason in summary["reasons"])
    assert calls["duckdb"] == 0
    assert calls["archive"] == 0
