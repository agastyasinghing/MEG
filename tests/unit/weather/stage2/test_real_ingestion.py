"""Unit tests for the offline real-ingestion descriptor skeleton."""
from __future__ import annotations

import ast
import sys
import sysconfig
from pathlib import Path

from meg.weather.stage2 import real_ingestion

REPO_ROOT = Path(__file__).resolve().parents[4]
MODULE_REL = "meg/weather/stage2/real_ingestion.py"
MODULE_PATH = REPO_ROOT / MODULE_REL

_ALLOWED_IMPORT_ROOTS = {"__future__", "dataclasses", "typing"}


def _valid_mapping(**overrides: object) -> dict[str, object]:
    mapping: dict[str, object] = {
        "source_id": "wx-real-source-001",
        "source_name": "Reviewed official resolution source",
        "source_category": "official_resolution_source",
        "source_intake_mode": "offline_static_descriptor",
        "provenance_url": "https://example.invalid/reviewed-source",
        "provenance_note": None,
        "access_date": "2026-06-10",
        "retrieval_context": "Human reviewer captured the descriptor before label use.",
        "no_lookahead_statement": "No later outcome information was used.",
        "human_reviewed": True,
        "static_caller_supplied": True,
        "evidence_status": "source_backed",
        "notes": ("Offline descriptor validation only.",),
    }
    mapping.update(overrides)
    return mapping


def _assert_blocked_with(overrides: dict[str, object], code: str) -> None:
    result = real_ingestion.validate_real_ingestion_source_mapping(_valid_mapping(**overrides))
    assert result.validation_state == "blocked"
    assert result.severity == "blocker"
    assert code in result.blocker_codes
    assert result.blocked is True


def test_valid_static_caller_supplied_descriptor_passes() -> None:
    result = real_ingestion.validate_real_ingestion_source_mapping(_valid_mapping())
    assert result.validation_state == "pass"
    assert result.severity == "info"
    assert result.blocker_codes == ()
    assert result.passed is True


def test_future_after_approval_mode_returns_caution_without_approval_drift() -> None:
    result = real_ingestion.validate_real_ingestion_source_mapping(
        _valid_mapping(source_intake_mode="future_provider_connector_after_approval")
    )
    assert result.validation_state == "caution"
    assert result.severity == "warning"
    assert result.blocker_codes == ()
    assert "source_intake_mode requires later approval before use" in result.messages


def test_reviewer_inferred_evidence_returns_caution() -> None:
    result = real_ingestion.validate_real_ingestion_source_mapping(
        _valid_mapping(evidence_status="reviewer_inferred")
    )
    assert result.validation_state == "caution"
    assert result.severity == "warning"
    assert result.blocker_codes == ()
    assert "evidence_status warrants reviewer caution" in result.messages


def test_missing_identity_blocks() -> None:
    _assert_blocked_with({"source_id": ""}, "missing_source_identity")


def test_missing_provenance_blocks() -> None:
    _assert_blocked_with(
        {"provenance_url": "", "provenance_note": ""},
        "missing_source_provenance",
    )


def test_missing_access_date_blocks() -> None:
    _assert_blocked_with({"access_date": ""}, "missing_access_date")


def test_missing_retrieval_context_blocks() -> None:
    _assert_blocked_with({"retrieval_context": ""}, "missing_retrieval_context")


def test_missing_no_lookahead_blocks() -> None:
    _assert_blocked_with({"no_lookahead_statement": ""}, "missing_no_lookahead_statement")


def test_missing_required_flags_block() -> None:
    _assert_blocked_with({"human_reviewed": False}, "missing_human_reviewed_flag")
    _assert_blocked_with({"static_caller_supplied": False}, "missing_static_caller_supplied_flag")


def test_unsupported_category_blocks() -> None:
    _assert_blocked_with({"source_category": "custom_hybrid_source"}, "unsupported_source_category")


def test_unsupported_mode_blocks() -> None:
    _assert_blocked_with({"source_intake_mode": "custom_hybrid_mode"}, "unsupported_source_intake_mode")


def test_prohibited_source_intake_mode_blocks() -> None:
    for mode in real_ingestion.PROHIBITED_SOURCE_INTAKE_MODES:
        _assert_blocked_with({"source_intake_mode": mode}, "prohibited_source_intake_mode")


def test_connector_source_retrieval_probability_runtime_and_execution_drift_blocks() -> None:
    cases = (
        ("notes", ("This would add a provider client.",), "connector_drift"),
        ("notes", ("This would fetch sources during validation.",), "connector_drift"),
        ("notes", ("This would scrape data.",), "connector_drift"),
        ("notes", ("This would pull forecasts.",), "connector_drift"),
        ("notes", ("This would call provider APIs.",), "connector_drift"),
        ("notes", ("This would score probabilities.",), "scoring_drift"),
        ("notes", ("This would run a " + "back" + "test.",), "scoring_drift"),
        ("notes", ("This would run a paper simulation.",), "scoring_drift"),
        ("notes", ("This would observe markets at runtime.",), "runtime_drift"),
        ("notes", ("This would schedule jobs.",), "runtime_drift"),
        ("notes", ("This would use queue jobs.",), "runtime_drift"),
        ("notes", ("This would create production behavior.",), "runtime_drift"),
        ("notes", ("This would place orders.",), "trading_drift"),
        ("notes", ("This would act autonomously.",), "trading_drift"),
        ("notes", ("This requires a private credential.",), "private_credentials_required"),
        ("notes", ("This would load secrets.",), "private_credentials_required"),
        ("notes", ("This would load config.",), "private_credentials_required"),
    )
    for field, value, code in cases:
        _assert_blocked_with({field: value}, code)


def test_mapping_helper_works() -> None:
    descriptor = real_ingestion.real_ingestion_source_descriptor_from_mapping(
        _valid_mapping(provenance_url=" ", provenance_note="Reviewed note", notes=[" a ", "", "b"])
    )
    assert descriptor.source_id == "wx-real-source-001"
    assert descriptor.provenance_url is None
    assert descriptor.provenance_note == "Reviewed note"
    assert descriptor.notes == ("a", "b")


def test_module_imports_only_standard_library() -> None:
    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    import_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.module is not None
            import_roots.add(node.module.split(".")[0])

    stdlib_names = set(sys.stdlib_module_names)
    stdlib_dir = Path(sysconfig.get_paths()["stdlib"])
    assert stdlib_dir.exists()
    assert import_roots <= stdlib_names
    assert import_roots <= _ALLOWED_IMPORT_ROOTS


def test_module_has_no_data_access_network_env_provider_or_execution_calls() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    compile(source, MODULE_REL, "exec")
    tree = ast.parse(source)

    forbidden_imports = {
        "requests",
        "httpx",
        "aio" + "http",
        "urllib" + ".request",
        "os",
        "dot" + "env",
        "pan" + "das",
        "pol" + "ars",
        "duck" + "db",
        "sql" + "alchemy",
        "fast" + "api",
        "fla" + "sk",
    }
    import_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            import_names.add(node.module)
    assert forbidden_imports.isdisjoint(import_names)

    forbidden_fragments = (
        "open(",
        ".read_text(",
        ".write_text(",
        "Path(",
        "json" + ".load",
        "read" + "_csv",
        "to" + "_csv",
        "os" + ".environ",
        "api" + "_key",
        "secret" + "_key",
        "weather" + "_api" + "_key",
        "load" + "_dot" + "env",
    )
    lowered = source.lower()
    offenders = [fragment for fragment in forbidden_fragments if fragment.lower() in lowered]
    assert offenders == []
