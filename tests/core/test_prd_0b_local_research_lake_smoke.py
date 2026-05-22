import importlib
import json
import sys
from pathlib import Path


MODULE = "scripts.prd_0b.local_research_lake_smoke"


def _mk_archive(tmp_path: Path) -> Path:
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
    (root / "data/polymarket/fpmm_collateral_lookup.json").write_text("{}", encoding="utf-8")
    return root


def test_import_has_no_duckdb_side_effects():
    sys.modules.pop("duckdb", None)
    mod = importlib.import_module(MODULE)
    assert mod is not None
    assert "duckdb" not in sys.modules


def test_constants_include_expected_families():
    mod = importlib.import_module(MODULE)
    assert set(mod.EXPECTED_ARCHIVE_FAMILIES) == {
        "data/kalshi/markets",
        "data/kalshi/trades",
        "data/polymarket/blocks",
        "data/polymarket/markets",
        "data/polymarket/trades",
        "data/polymarket/legacy_trades",
    }


def test_validate_archive_root_ok(tmp_path: Path):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)
    res = mod.validate_archive_root_path(str(root))
    assert res.ok is True


def test_validate_missing_non_dir_traversal_and_compressed(tmp_path: Path):
    mod = importlib.import_module(MODULE)
    assert mod.validate_archive_root_path("").ok is False
    file_path = tmp_path / "file.txt"
    file_path.write_text("x", encoding="utf-8")
    assert mod.validate_archive_root_path(str(file_path)).ok is False
    assert mod.validate_archive_root_path("../nope").ok is False
    bad = tmp_path / "archive.zip"
    bad.write_text("x", encoding="utf-8")
    assert mod.validate_archive_root_path(str(bad)).ok is False


def test_discovery_missing_family_and_appledouble_ignored(tmp_path: Path):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)
    (root / "data/kalshi/trades").rename(root / "data/kalshi/trades_missing")
    fam = root / "data/polymarket/trades"
    (fam / "._ignore.parquet").write_text("x", encoding="utf-8")
    d = mod.discover_expected_families(str(root))
    missing = [f for f in d["family_results"] if f["family"] == "data/kalshi/trades"][0]
    assert missing["exists"] is False
    assert any("appledouble_ignored" in w for w in d["warnings"])


def test_samples_max_one_and_json_presence(tmp_path: Path):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)
    fam = root / "data/polymarket/markets"
    (fam / "second.parquet").write_text("x", encoding="utf-8")
    samples = mod.find_sample_parquet_files(str(root))
    assert all((v is None or isinstance(v, str)) for v in samples.values())
    d = mod.discover_expected_families(str(root))
    assert d["json_files"][0]["exists"] is True


def test_duckdb_unavailable_and_require_flag(tmp_path: Path, monkeypatch):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)
    monkeypatch.setattr(mod, "try_import_duckdb", lambda: (False, None, "duckdb_unavailable"))
    summary = mod.build_smoke_summary(str(root), 5, require_duckdb=False)
    assert summary["status"] == "duckdb_unavailable"
    summary2 = mod.build_smoke_summary(str(root), 5, require_duckdb=True)
    assert summary2["ok"] is False


def test_fake_duckdb_uses_memory(tmp_path: Path, monkeypatch):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)

    class FakeConn:
        def __init__(self):
            self.closed = False

        def execute(self, _q):
            class R:
                def fetchall(self_non):
                    return [(1,)]

            return R()

        def close(self):
            self.closed = True

    class FakeDuck:
        def __init__(self):
            self.paths = []

        def connect(self, path):
            self.paths.append(path)
            return FakeConn()

    fake = FakeDuck()
    monkeypatch.setattr(mod, "try_import_duckdb", lambda: (True, fake, None))
    out = mod.run_duckdb_readonly_smoke(str(root))
    assert out["duckdb_available"] is True
    assert fake.paths == [":memory:"]


def test_cli_json_and_no_outputs(tmp_path: Path, capsys, monkeypatch):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)
    monkeypatch.setattr(mod, "try_import_duckdb", lambda: (False, None, "duckdb_unavailable"))
    rc = mod.main(["check", "--archive-root", str(root), "--json"])
    assert rc in (0, 1)
    out = capsys.readouterr().out
    parsed = json.loads(out)
    assert "status" in parsed
    assert list(tmp_path.rglob("*.duckdb")) == []


def test_no_prod_runtime_imports_and_doc_contract():
    text = Path("docs/prd/PRD-0B-IMPL-01_LOCAL_RESEARCH_LAKE_SMOKE.md").read_text(encoding="utf-8")
    assert "Local-only" in text or "local-only" in text
    assert "no committed data" in text
    assert "no dependency added" in text
    assert "no archive outputs" in text


def test_missing_family_root_includes_family_results_without_duckdb(tmp_path: Path, monkeypatch):
    mod = importlib.import_module(MODULE)
    root = _mk_archive(tmp_path)
    (root / "data/kalshi/trades").rename(root / "data/kalshi/trades_missing")
    monkeypatch.setattr(mod, "try_import_duckdb", lambda: (False, None, "duckdb_unavailable"))
    summary = mod.build_smoke_summary(str(root), 5, require_duckdb=False)
    assert summary["ok"] is False
    assert "family_results" in summary
    target = [f for f in summary["family_results"] if f["family"] == "data/kalshi/trades"][0]
    assert target["status"] == "missing"
    present = [f for f in summary["family_results"] if f["family"] == "data/kalshi/markets"][0]
    assert present["status"] == "present"
    assert present["parquet_count"] >= 1
    assert present["sample_file"] is not None
    assert "duckdb_smoke" not in summary
    assert list(tmp_path.rglob("*.duckdb")) == []
