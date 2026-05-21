from __future__ import annotations

from pathlib import Path
import re

import pytest

from scripts.phase1.fixture_derivation_safety_shell import (
    validate_fixture_output_path,
    validate_relative_source_path,
    validate_row_limit,
)


MANIFEST_REQUIRED_FIELDS = {
    "manifest_ref",
    "schema_version",
    "phase",
    "manifest_status",
    "created_by",
    "created_at",
    "source_manifest_ref",
    "source_repo_ref",
    "source_repo_commit",
    "source_archive_ref",
    "fixture_derivation_approval_ref",
    "fixture_commit_approval_ref",
    "fixture_entries",
    "global_posture",
    "artifact_hygiene",
    "reviewer_envelope",
}

MANIFEST_STATUS_ALLOWLIST = {
    "planned_contract_only",
    "dry_run_manifest",
    "derived_pending_commit_review",
    "committed_tiny_fixture_manifest",
}
BLOCKED_STATUSES = {
    "import_ready",
    "loader_ready",
    "production_ready",
    "execution_ready",
    "live_trading_ready",
    "autonomous_ready",
}

GLOBAL_POSTURE_REQUIRED_FIELDS = {
    "research_only",
    "local_only",
    "network_allowed",
    "api_calls_allowed",
    "secrets_allowed",
    "connector_import_allowed",
    "archive_import_allowed",
    "fixture_writes_allowed",
    "loader_execution_allowed",
    "order_routing_allowed",
    "live_trading_allowed",
    "autonomous_execution_allowed",
}

ARTIFACT_HYGIENE_REQUIRED_FIELDS = {
    "no_compressed_archives_committed",
    "no_extracted_archive_data_committed",
    "no_absolute_archive_paths_in_payloads",
    "no_duckdb_artifacts",
    "no_generated_reports",
    "no_external_repo_files",
    "no_network_outputs",
    "no_secret_material",
    "appledouble_files_ignored",
}

REVIEWER_ENVELOPE_REQUIRED_FIELDS = {
    "human_review_required",
    "reviewer_ref",
    "reviewed_at",
    "review_decision",
    "review_rationale",
}
REVIEW_DECISION_ALLOWLIST = {
    "pending",
    "approved_for_derivation",
    "approved_for_commit",
    "rejected",
    "deferred",
}

FIXTURE_ENTRY_REQUIRED_FIELDS = {
    "fixture_ref",
    "fixture_family",
    "platform",
    "source_relative_path",
    "source_file_checksum",
    "checksum_algorithm",
    "row_selection_rule",
    "selected_row_count",
    "selected_stable_keys",
    "output_relative_path",
    "generated_fixture_checksum",
    "script_version",
    "parser_version",
    "derivation_timestamp",
    "source_record_shape_version",
    "normalization_plan_ref",
    "unresolved_state_policy",
    "entry_posture",
}
FIXTURE_FAMILY_ALLOWLIST = {
    "kalshi_markets_tiny",
    "kalshi_trades_tiny",
    "poly_markets_tiny",
    "poly_clob_trades_tiny",
    "poly_blocks_tiny",
    "poly_legacy_fpmm_trades_tiny",
    "poly_fpmm_collateral_lookup_tiny",
}
PLATFORM_ALLOWLIST = {"kalshi", "polymarket"}
CHECKSUM_ALGORITHM_ALLOWLIST = {"sha256"}

ENTRY_POSTURE_REQUIRED_FIELDS = {
    "fixture_derivation_approved",
    "fixture_commit_approved",
    "fixture_written",
    "archive_rows_read",
    "source_payload_read",
    "normalization_applied",
    "runtime_loader_used",
}


def _looks_like_absolute_or_network_path_key(value: str) -> bool:
    if value.startswith(("/", "\\", "//")):
        return True
    return bool(re.match(r"^[a-zA-Z]:[\\/]", value))


def _build_valid_manifest_contract() -> dict[str, object]:
    entries = [
        {
            "fixture_ref": "fixture-kalshi-markets-tiny",
            "fixture_family": "kalshi_markets_tiny",
            "platform": "kalshi",
            "source_relative_path": "data/kalshi/markets/markets_0_10000.parquet",
            "source_file_checksum": "placeholder_sha256_kalshi_markets",
            "checksum_algorithm": "sha256",
            "row_selection_rule": "sort ticker_ref, event_ticker_ref, fetched_at then first_n",
            "selected_row_count": 3,
            "selected_stable_keys": ["ticker_ref", "event_ticker_ref", "fetched_at"],
            "output_relative_path": "fixtures/phase1/kalshi_markets_tiny.json",
            "generated_fixture_checksum": "placeholder_sha256_generated_kalshi_markets",
            "script_version": "phase1-03-contract-only",
            "parser_version": "v0-contract",
            "derivation_timestamp": "2026-05-21T00:00:00Z",
            "source_record_shape_version": "phase0b-19-v1",
            "normalization_plan_ref": "0B-22",
            "unresolved_state_policy": "preserve_as_unresolved",
            "entry_posture": {k: False for k in ENTRY_POSTURE_REQUIRED_FIELDS},
        },
        {
            "fixture_ref": "fixture-kalshi-trades-tiny",
            "fixture_family": "kalshi_trades_tiny",
            "platform": "kalshi",
            "source_relative_path": "data/kalshi/trades/trades_0_10000.parquet",
            "source_file_checksum": "placeholder_sha256_kalshi_trades",
            "checksum_algorithm": "sha256",
            "row_selection_rule": "sort trade_ref, ticker_ref, created_time then first_n",
            "selected_row_count": 2,
            "selected_stable_keys": ["trade_ref", "ticker_ref", "created_time"],
            "output_relative_path": "fixtures/phase1/kalshi_trades_tiny.json",
            "generated_fixture_checksum": "placeholder_sha256_generated_kalshi_trades",
            "script_version": "phase1-03-contract-only",
            "parser_version": "v0-contract",
            "derivation_timestamp": "2026-05-21T00:00:00Z",
            "source_record_shape_version": "phase0b-19-v1",
            "normalization_plan_ref": "0B-22",
            "unresolved_state_policy": "preserve_as_unresolved",
            "entry_posture": {k: False for k in ENTRY_POSTURE_REQUIRED_FIELDS},
        },
        {
            "fixture_ref": "fixture-poly-markets-tiny",
            "fixture_family": "poly_markets_tiny",
            "platform": "polymarket",
            "source_relative_path": "data/polymarket/markets/markets_0_10000.parquet",
            "source_file_checksum": "placeholder_sha256_poly_markets",
            "checksum_algorithm": "sha256",
            "row_selection_rule": "sort condition_id, source_market_ref, fetched_at then first_n",
            "selected_row_count": 3,
            "selected_stable_keys": ["condition_id", "source_market_ref", "fetched_at"],
            "output_relative_path": "fixtures/phase1/poly_markets_tiny.json",
            "generated_fixture_checksum": "placeholder_sha256_generated_poly_markets",
            "script_version": "phase1-03-contract-only",
            "parser_version": "v0-contract",
            "derivation_timestamp": "2026-05-21T00:00:00Z",
            "source_record_shape_version": "phase0b-19-v1",
            "normalization_plan_ref": "0B-21",
            "unresolved_state_policy": "preserve_as_unresolved",
            "entry_posture": {k: False for k in ENTRY_POSTURE_REQUIRED_FIELDS},
        },
        {
            "fixture_ref": "fixture-poly-clob-trades-tiny",
            "fixture_family": "poly_clob_trades_tiny",
            "platform": "polymarket",
            "source_relative_path": "data/polymarket/trades/trades_0_10000.parquet",
            "source_file_checksum": "placeholder_sha256_poly_clob_trades",
            "checksum_algorithm": "sha256",
            "row_selection_rule": "sort transaction_hash, log_index, order_hash then first_n",
            "selected_row_count": 4,
            "selected_stable_keys": ["transaction_hash", "log_index", "order_hash"],
            "output_relative_path": "fixtures/phase1/poly_clob_trades_tiny.json",
            "generated_fixture_checksum": "placeholder_sha256_generated_poly_clob_trades",
            "script_version": "phase1-03-contract-only",
            "parser_version": "v0-contract",
            "derivation_timestamp": "2026-05-21T00:00:00Z",
            "source_record_shape_version": "phase0b-19-v1",
            "normalization_plan_ref": "0B-21",
            "unresolved_state_policy": "preserve_as_unresolved",
            "entry_posture": {k: False for k in ENTRY_POSTURE_REQUIRED_FIELDS},
        },
        {
            "fixture_ref": "fixture-poly-blocks-tiny",
            "fixture_family": "poly_blocks_tiny",
            "platform": "polymarket",
            "source_relative_path": "data/polymarket/blocks/blocks_10000000_10100000.parquet",
            "source_file_checksum": "placeholder_sha256_poly_blocks",
            "checksum_algorithm": "sha256",
            "row_selection_rule": "sort block_number then first_n",
            "selected_row_count": 5,
            "selected_stable_keys": ["block_number"],
            "output_relative_path": "fixtures/phase1/poly_blocks_tiny.json",
            "generated_fixture_checksum": "placeholder_sha256_generated_poly_blocks",
            "script_version": "phase1-03-contract-only",
            "parser_version": "v0-contract",
            "derivation_timestamp": "2026-05-21T00:00:00Z",
            "source_record_shape_version": "phase0b-19-v1",
            "normalization_plan_ref": "0B-21",
            "unresolved_state_policy": "preserve_as_unresolved",
            "entry_posture": {k: False for k in ENTRY_POSTURE_REQUIRED_FIELDS},
        },
        {
            "fixture_ref": "fixture-poly-legacy-fpmm-trades-tiny",
            "fixture_family": "poly_legacy_fpmm_trades_tiny",
            "platform": "polymarket",
            "source_relative_path": "data/polymarket/legacy_trades/trades_0_10000.parquet",
            "source_file_checksum": "placeholder_sha256_poly_legacy_fpmm",
            "checksum_algorithm": "sha256",
            "row_selection_rule": "sort transaction_hash, log_index, fpmm_address then first_n",
            "selected_row_count": 3,
            "selected_stable_keys": ["transaction_hash", "log_index", "fpmm_address"],
            "output_relative_path": "fixtures/phase1/poly_legacy_fpmm_trades_tiny.json",
            "generated_fixture_checksum": "placeholder_sha256_generated_poly_legacy_fpmm",
            "script_version": "phase1-03-contract-only",
            "parser_version": "v0-contract",
            "derivation_timestamp": "2026-05-21T00:00:00Z",
            "source_record_shape_version": "phase0b-19-v1",
            "normalization_plan_ref": "0B-21",
            "unresolved_state_policy": "preserve_as_unresolved",
            "entry_posture": {k: False for k in ENTRY_POSTURE_REQUIRED_FIELDS},
        },
        {
            "fixture_ref": "fixture-poly-fpmm-collateral-lookup-tiny",
            "fixture_family": "poly_fpmm_collateral_lookup_tiny",
            "platform": "polymarket",
            "source_relative_path": "data/polymarket/fpmm_collateral_lookup.json",
            "source_file_checksum": "placeholder_sha256_poly_fpmm_lookup",
            "checksum_algorithm": "sha256",
            "row_selection_rule": "sort address key lexicographically then first_n",
            "selected_row_count": 2,
            "selected_stable_keys": ["address_key"],
            "output_relative_path": "fixtures/phase1/poly_fpmm_collateral_lookup_tiny.json",
            "generated_fixture_checksum": "placeholder_sha256_generated_poly_fpmm_lookup",
            "script_version": "phase1-03-contract-only",
            "parser_version": "v0-contract",
            "derivation_timestamp": "2026-05-21T00:00:00Z",
            "source_record_shape_version": "phase0b-19-v1",
            "normalization_plan_ref": "0B-21",
            "unresolved_state_policy": "preserve_as_unresolved",
            "entry_posture": {k: False for k in ENTRY_POSTURE_REQUIRED_FIELDS},
        },
    ]
    return {
        "manifest_ref": "phase1_fixture_manifest_contract_v1",
        "schema_version": "phase1-03-contract-v1",
        "phase": "phase1-03",
        "manifest_status": "planned_contract_only",
        "created_by": "pytest_contract",
        "created_at": "2026-05-21T00:00:00Z",
        "source_manifest_ref": "local_poly_kalshi_historical_archive_placeholder",
        "source_repo_ref": "jon_becker_prediction_market_analysis_snapshot",
        "source_repo_commit": "placeholder_commit_sha",
        "source_archive_ref": "local_approved_archive_placeholder",
        "fixture_derivation_approval_ref": "approval_pending",
        "fixture_commit_approval_ref": "approval_pending",
        "fixture_entries": entries,
        "global_posture": {
            "research_only": True,
            "local_only": True,
            "network_allowed": False,
            "api_calls_allowed": False,
            "secrets_allowed": False,
            "connector_import_allowed": False,
            "archive_import_allowed": False,
            "fixture_writes_allowed": False,
            "loader_execution_allowed": False,
            "order_routing_allowed": False,
            "live_trading_allowed": False,
            "autonomous_execution_allowed": False,
        },
        "artifact_hygiene": {key: True for key in ARTIFACT_HYGIENE_REQUIRED_FIELDS},
        "reviewer_envelope": {
            "human_review_required": True,
            "reviewer_ref": None,
            "reviewed_at": None,
            "review_decision": "pending",
            "review_rationale": "Awaiting explicit derivation and commit approvals.",
        },
    }


def _validate_manifest(manifest: dict[str, object]) -> None:
    assert MANIFEST_REQUIRED_FIELDS.issubset(set(manifest))
    assert manifest["manifest_status"] in MANIFEST_STATUS_ALLOWLIST
    assert manifest["manifest_status"] not in BLOCKED_STATUSES

    posture = manifest["global_posture"]
    assert isinstance(posture, dict)
    assert GLOBAL_POSTURE_REQUIRED_FIELDS.issubset(set(posture))
    assert posture["research_only"] is True
    assert posture["local_only"] is True
    for flag in GLOBAL_POSTURE_REQUIRED_FIELDS - {"research_only", "local_only"}:
        assert posture[flag] is False

    hygiene = manifest["artifact_hygiene"]
    assert isinstance(hygiene, dict)
    assert ARTIFACT_HYGIENE_REQUIRED_FIELDS.issubset(set(hygiene))
    for flag in ARTIFACT_HYGIENE_REQUIRED_FIELDS:
        assert hygiene[flag] is True

    reviewer = manifest["reviewer_envelope"]
    assert isinstance(reviewer, dict)
    assert REVIEWER_ENVELOPE_REQUIRED_FIELDS.issubset(set(reviewer))
    assert reviewer["human_review_required"] is True
    assert reviewer["review_decision"] in REVIEW_DECISION_ALLOWLIST
    assert reviewer["review_decision"] == "pending"

    entries = manifest["fixture_entries"]
    assert isinstance(entries, list) and entries
    _validate_fixture_entries(entries)


def _validate_fixture_entries(entries: list[dict[str, object]]) -> None:
    families = set()
    for entry in entries:
        assert FIXTURE_ENTRY_REQUIRED_FIELDS.issubset(set(entry))
        family = entry["fixture_family"]
        assert family in FIXTURE_FAMILY_ALLOWLIST
        families.add(family)

        assert entry["platform"] in PLATFORM_ALLOWLIST
        assert entry["checksum_algorithm"] in CHECKSUM_ALGORITHM_ALLOWLIST
        assert isinstance(entry["source_file_checksum"], str) and entry["source_file_checksum"].strip()
        assert isinstance(entry["generated_fixture_checksum"], str) and entry["generated_fixture_checksum"].strip()

        row_count = entry["selected_row_count"]
        assert validate_row_limit(row_count).allowed

        keys = entry["selected_stable_keys"]
        assert isinstance(keys, list) and keys
        assert all(isinstance(key, str) and key.strip() for key in keys)
        assert all(not _looks_like_absolute_or_network_path_key(key) for key in keys)

        assert validate_relative_source_path(str(entry["source_relative_path"])).allowed
        assert validate_fixture_output_path(str(entry["output_relative_path"])).allowed

        posture = entry["entry_posture"]
        assert isinstance(posture, dict)
        assert ENTRY_POSTURE_REQUIRED_FIELDS.issubset(set(posture))
        for flag in ENTRY_POSTURE_REQUIRED_FIELDS:
            assert posture[flag] is False

    assert families == FIXTURE_FAMILY_ALLOWLIST


def test_valid_fixture_manifest_contract_passes() -> None:
    _validate_manifest(_build_valid_manifest_contract())


def test_missing_top_level_field_fails() -> None:
    manifest = _build_valid_manifest_contract()
    manifest.pop("manifest_ref")
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_missing_global_posture_field_fails() -> None:
    manifest = _build_valid_manifest_contract()
    manifest["global_posture"].pop("network_allowed")
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


@pytest.mark.parametrize("blocked", sorted(BLOCKED_STATUSES))
def test_blocked_manifest_statuses_fail(blocked: str) -> None:
    manifest = _build_valid_manifest_contract()
    manifest["manifest_status"] = blocked
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


@pytest.mark.parametrize(
    "flag",
    sorted(
        GLOBAL_POSTURE_REQUIRED_FIELDS
        - {
            "research_only",
            "local_only",
        }
    ),
)
def test_global_posture_drift_fails(flag: str) -> None:
    manifest = _build_valid_manifest_contract()
    manifest["global_posture"][flag] = True
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_artifact_hygiene_false_fails() -> None:
    manifest = _build_valid_manifest_contract()
    manifest["artifact_hygiene"]["no_duckdb_artifacts"] = False
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_missing_reviewer_envelope_field_fails() -> None:
    manifest = _build_valid_manifest_contract()
    manifest["reviewer_envelope"].pop("review_decision")
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_fixture_family_coverage_exactly_seven_required() -> None:
    manifest = _build_valid_manifest_contract()
    manifest["fixture_entries"] = manifest["fixture_entries"][:-1]
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_missing_fixture_entry_field_fails() -> None:
    manifest = _build_valid_manifest_contract()
    manifest["fixture_entries"][0].pop("fixture_ref")
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_unknown_fixture_family_fails() -> None:
    manifest = _build_valid_manifest_contract()
    manifest["fixture_entries"][0]["fixture_family"] = "unknown_family"
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_unsupported_platform_fails() -> None:
    manifest = _build_valid_manifest_contract()
    manifest["fixture_entries"][0]["platform"] = "kalshi_production"
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_unsupported_checksum_algorithm_fails() -> None:
    manifest = _build_valid_manifest_contract()
    manifest["fixture_entries"][0]["checksum_algorithm"] = "md5"
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


@pytest.mark.parametrize("bad_count", [0, 6, "3"])
def test_selected_row_count_bounds_fail(bad_count: object) -> None:
    manifest = _build_valid_manifest_contract()
    manifest["fixture_entries"][0]["selected_row_count"] = bad_count
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_empty_selected_stable_keys_fail() -> None:
    manifest = _build_valid_manifest_contract()
    manifest["fixture_entries"][0]["selected_stable_keys"] = []
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


@pytest.mark.parametrize(
    "bad_key",
    [
        "/absolute/path",
        "C:\\Users\\sagas\\archive",
        "C:/Users/sagas/archive",
        r"\\server\share\archive",
    ],
)
def test_selected_stable_keys_absolute_or_network_like_path_fails(bad_key: str) -> None:
    manifest = _build_valid_manifest_contract()
    manifest["fixture_entries"][0]["selected_stable_keys"] = [bad_key]
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_unsafe_source_relative_path_fails() -> None:
    manifest = _build_valid_manifest_contract()
    manifest["fixture_entries"][0]["source_relative_path"] = "../data/kalshi/markets/markets_0_10000.parquet"
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_unsafe_output_relative_path_fails() -> None:
    manifest = _build_valid_manifest_contract()
    manifest["fixture_entries"][0]["output_relative_path"] = "fixtures/phase1/generated_report.csv"
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


@pytest.mark.parametrize("flag", sorted(ENTRY_POSTURE_REQUIRED_FIELDS))
def test_entry_posture_drift_fails(flag: str) -> None:
    manifest = _build_valid_manifest_contract()
    manifest["fixture_entries"][0]["entry_posture"][flag] = True
    with pytest.raises(AssertionError):
        _validate_manifest(manifest)


def test_blocked_statuses_do_not_appear_in_allowlist() -> None:
    assert MANIFEST_STATUS_ALLOWLIST.isdisjoint(BLOCKED_STATUSES)


def test_doc_script_alignment_contract_markers_present() -> None:
    phase101 = Path("docs/phase1/1-01_PHASE1_KICKOFF_FIXTURE_GENERATION_GATE.md").read_text(encoding="utf-8").lower()
    phase0b23 = Path("docs/phase0b/0B-23_TINY_FIXTURE_DERIVATION_SCRIPT_PLAN.md").read_text(encoding="utf-8").lower()
    shell = Path("scripts/phase1/fixture_derivation_safety_shell.py").read_text(encoding="utf-8")

    assert "fixture derivation approval" in phase101
    assert "fixture commit approval" in phase101
    assert "provenance" in phase101
    assert "checksum" in phase101

    assert "manifest/provenance output" in phase0b23
    assert "source file checksum" in phase0b23
    assert "generated fixture checksum" in phase0b23

    assert "def validate_relative_source_path" in shell
    assert "def validate_fixture_output_path" in shell
    assert "def validate_row_limit" in shell
    assert "fixture writing remain disallowed in phase 1-02" in shell.lower()
