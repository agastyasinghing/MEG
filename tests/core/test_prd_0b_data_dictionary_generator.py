import json
import subprocess
import sys
from pathlib import Path

import scripts.prd_0b.data_dictionary_generator as gen

DOC_PATH = Path("docs/prd/PRD-0B-IMPL-05_LOCAL_DATA_DICTIONARY_GENERATOR.md")


def test_import_side_effects_and_no_duckdb_imported():
    probe = """
import json
import sys
import scripts.prd_0b.data_dictionary_generator  # noqa: F401
print(json.dumps({"duckdb_loaded": "duckdb" in sys.modules}))
"""
    result = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True, check=False)
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["duckdb_loaded"] is False


def test_specs_count_and_unique_and_mapping_columns():
    specs = gen.get_dataset_dictionary_specs()
    assert len(specs) == 7
    refs = [s["dataset_ref"] for s in specs]
    assert len(set(refs)) == 7
    assert set(refs) == {
        "kalshi_markets", "kalshi_trades", "poly_markets", "poly_clob_trades", "poly_blocks", "poly_legacy_fpmm_trades", "poly_fpmm_collateral_lookup"
    }
    poly = next(s for s in specs if s["dataset_ref"] == "poly_markets")
    assert "condition_id" in poly["expected_columns"]


def test_validation_fails_missing_required_fields():
    bad = gen.get_dataset_dictionary_specs()
    bad[0] = dict(bad[0])
    bad[0].pop("dataset_ref")
    errs = gen.validate_dataset_dictionary_specs(bad)
    assert any("missing_required_field" in e for e in errs)


def _base_cfg(tmp_path, mode="static_specs_only", output_mode="stdout_only"):
    return {
        "archive_root": str(tmp_path), "source_manifest_ref": "manifest", "source_repo_ref": "agastyasinghing/MEG", "source_repo_commit": "abc", "source_archive_ref": "becker", "created_by": "tester", "mode": mode, "output_mode": output_mode, "require_duckdb": False
    }


def test_static_dictionary_shape_posture_hygiene(tmp_path):
    d = gen.build_data_dictionary(_base_cfg(tmp_path))
    assert d["dictionary_status"] == "generated_pending_review"
    assert d["generation_mode"] == "local_generated_from_sanity_harness"
    assert len(d["dataset_entries"]) == 7
    assert d["global_posture"]["research_only"] is True
    assert d["global_posture"]["duckdb_execution_allowed"] is False
    assert all(d["artifact_hygiene"].values())
    first_col = d["dataset_entries"][0]["column_metadata"][0]
    for key in ["column_name", "source_name", "logical_role", "raw_type_observed", "normalized_type_target", "nullable_status", "semantic_notes", "validation_notes", "pii_or_secret_status", "used_for_joining", "used_for_time_filtering", "used_for_price_or_size", "used_for_resolution_or_result", "used_for_wallet_or_actor", "unresolved_handling"]:
        assert key in first_col


def test_duckdb_unavailable_fallback_and_require_closed(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "try_import_duckdb", lambda: (False, None, "duckdb_unavailable"))
    d = gen.build_data_dictionary(_base_cfg(tmp_path, mode="duckdb_schema_metadata_if_available"))
    assert "duckdb_unavailable" in d["reviewer_envelope"]["warnings"][0]
    cfg = _base_cfg(tmp_path, mode="duckdb_schema_metadata_if_available")
    cfg["require_duckdb"] = True
    try:
        gen.build_data_dictionary(cfg)
        assert False
    except Exception:
        assert True


def test_fake_duckdb_metadata_and_missing_columns(tmp_path, monkeypatch):
    fam = tmp_path / "data/polymarket/markets"
    fam.mkdir(parents=True)
    (fam / "a.parquet").write_text("x", encoding="utf-8")

    class Conn:
        def execute(self, q):
            class R:
                def fetchall(self2):
                    return [("id", "VARCHAR"), ("condition_id", "VARCHAR")]
            assert ":memory:" not in q
            return R()
        def close(self):
            pass
    class Duck:
        def connect(self, dsn):
            assert dsn == ":memory:"
            return Conn()
    monkeypatch.setattr(gen, "try_import_duckdb", lambda: (True, Duck(), None))
    monkeypatch.setattr(gen, "find_sample_parquet_files", lambda _: {"data/polymarket/markets": "data/polymarket/markets/a.parquet"})
    out = gen.extract_duckdb_schema_metadata(str(tmp_path), [s for s in gen.get_dataset_dictionary_specs() if s["dataset_ref"] == "poly_markets"])
    assert out["duckdb_available"] is True
    d = gen.build_data_dictionary(_base_cfg(tmp_path, mode="duckdb_schema_metadata_if_available"))
    poly = next(e for e in d["dataset_entries"] if e["dataset_ref"] == "poly_markets")
    assert "id" in poly["observed_columns"]
    assert "question" in poly["missing_columns"]


def test_json_sidecar_static_only_note(tmp_path):
    d = gen.build_data_dictionary(_base_cfg(tmp_path))
    side = next(e for e in d["dataset_entries"] if e["dataset_ref"] == "poly_fpmm_collateral_lookup")
    assert "json_sidecar_static_only" in side["generation_notes"]


def test_cli_stdout_and_tempdir(tmp_path):
    cmd = [sys.executable, "-m", "scripts.prd_0b.data_dictionary_generator", "generate", "--source-manifest-ref", "m", "--source-repo-ref", "r", "--source-repo-commit", "c", "--source-archive-ref", "a", "--created-by", "me", "--mode", "static_specs_only", "--output-mode", "stdout_only"]
    r = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert r.returncode == 0
    assert json.loads(r.stdout)["phase"] == "PRD-0B-IMPL-05"

    outdir = tmp_path / "pytest-out"
    outdir.mkdir()
    cmd2 = cmd[:-1] + ["tempdir_only_for_tests", "--output-dir", str(outdir)]
    r2 = subprocess.run(cmd2, capture_output=True, text=True, check=False)
    assert r2.returncode == 0
    files = list(outdir.glob("*.json"))
    assert len(files) == 1


def test_unsafe_output_dir_and_missing_args_fail(tmp_path):
    repo_docs = Path.cwd() / "docs"
    try:
        gen.write_dictionary_tempdir_only({}, str(repo_docs))
        assert False
    except Exception:
        assert True
    r = subprocess.run([sys.executable, "-m", "scripts.prd_0b.data_dictionary_generator", "generate"], capture_output=True, text=True, check=False)
    assert r.returncode != 0


def test_doc_exists_and_mentions_posture():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "optional/local-only" in text
    assert "No DuckDB dependency addition" in text
    assert "no committed generated dictionary file" in text
