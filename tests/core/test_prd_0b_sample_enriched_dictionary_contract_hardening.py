from __future__ import annotations

from pathlib import Path

from scripts.prd_0b.data_dictionary_sample_enrichment import (
    enrich_data_dictionary_with_samples,
    get_approved_sample_keys,
    validate_sample_enrichment_result,
    validate_sample_enrichment_summary,
)
from tests.core.test_prd_0b_data_dictionary_sample_enrichment import _build_archive


def test_impl14_doc_has_required_sections_and_non_approvals() -> None:
    text = Path("docs/prd/PRD-0B-IMPL-14_SAMPLE_ENRICHED_DICTIONARY_CONTRACT_HARDENING.md").read_text(encoding="utf-8")
    required_snippets = [
        "Purpose and posture",
        "Relationship to PRD-0B-IMPL-13",
        "Frozen approved sample field set",
        "Runtime-vs-committed flag semantics",
        "Forbidden payload classes",
        "No-output/no-artifact contract",
        "Validation helper contract",
        "Test posture using synthetic mini-archives",
        "Safety/no-output guarantees",
        "What counts as success",
        "What remains out of scope",
        "Relationship to PRD-0A",
        "Recommended next tickets",
        "no new archive reads beyond IMPL-13",
        "no generated dictionary files",
        "no final trading readiness claim",
    ]
    for snippet in required_snippets:
        assert snippet in text


def test_approved_sample_keys_are_frozen_exactly() -> None:
    assert get_approved_sample_keys() == {
        "family",
        "source_platform",
        "source_kind",
        "source_relative_path",
        "sample_enrichment_status",
        "sample_source_relative_path",
        "sample_file_kind",
        "sample_row_limit",
        "sample_row_count_observed",
        "sample_column_count_observed",
        "sample_columns_observed",
        "sample_elapsed_ms",
        "sample_warning",
        "sample_generated_from_archive_root",
        "sample_persistent_output_written",
    }


def _valid_sample_result() -> dict[str, object]:
    return {
        "family": "kalshi_markets",
        "source_platform": "kalshi",
        "source_kind": "parquet_family",
        "source_relative_path": "data/kalshi/markets/part-000.parquet",
        "sample_enrichment_status": "pass",
        "sample_source_relative_path": "data/kalshi/markets/part-000.parquet",
        "sample_file_kind": "parquet",
        "sample_row_limit": 1000,
        "sample_row_count_observed": 1,
        "sample_column_count_observed": 2,
        "sample_columns_observed": ["condition_ref", "outcome"],
        "sample_elapsed_ms": 0.1,
        "sample_warning": None,
        "sample_generated_from_archive_root": True,
        "sample_persistent_output_written": False,
    }


def test_validation_helper_accepts_valid_result() -> None:
    assert validate_sample_enrichment_result(_valid_sample_result()) == []


def test_validation_helper_rejects_extra_missing_forbidden_and_persistent_output() -> None:
    bad = _valid_sample_result()
    bad.pop("sample_warning")
    bad["raw_payload"] = {"x": 1}
    bad["sample_persistent_output_written"] = True
    errors = validate_sample_enrichment_result(bad)
    assert "sample_result_keys_must_match_approved_set" in errors
    assert any("sample_result_contains_forbidden_keys" in e for e in errors)
    assert "sample_persistent_output_written_must_be_false" in errors


def test_validation_helper_rejects_summary_output_and_readiness_flags() -> None:
    summary = {
        "wrote_outputs": True,
        "created_duckdb_file": True,
        "generated_artifacts": ["generated.json"],
        "committed_fixtures": True,
        "production_readiness_claim": True,
        "final_trading_readiness_claim": True,
        "sample_enrichment_results": [_valid_sample_result()],
    }
    errors = validate_sample_enrichment_summary(summary)
    assert "wrote_outputs_must_be_false" in errors
    assert "created_duckdb_file_must_be_false" in errors
    assert "generated_artifacts_must_be_empty" in errors
    assert "committed_fixtures_must_be_false" in errors
    assert "production_readiness_claim_must_be_false" in errors
    assert "final_trading_readiness_claim_must_be_false" in errors


def test_runtime_impl13_summary_passes_contract_and_no_outputs(tmp_path: Path) -> None:
    _build_archive(tmp_path)
    summary = enrich_data_dictionary_with_samples(tmp_path)
    assert summary["ok"] is True
    assert validate_sample_enrichment_summary(summary) == []
    assert not list(tmp_path.rglob("*.duckdb"))
    assert not list(tmp_path.rglob("*dictionary*.json"))
