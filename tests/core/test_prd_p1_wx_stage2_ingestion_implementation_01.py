"""Static tests for PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01."""
from __future__ import annotations

import ast
import importlib
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PRD_REL = "docs/prd/PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01_STATIC_INGESTION_BOUNDARY_SKELETON.md"
MODULE_REL = "meg/weather/stage2/ingestion_boundary.py"
CANONICAL_ID = "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01"

FORBIDDEN_IMPLEMENTATION_FRAGMENTS = (
    "os." + "environ",
    "load_" + "dot" + "env",
    "dot" + "env",
    "requests" + ".",
    "http" + "x.",
    "aio" + "http",
    "urllib." + "request",
    "api_" + "key",
    "secret_" + "key",
    "weather_" + "api_" + "key",
    "fast" + "api",
    "fl" + "ask",
    "sql" + "alchemy",
    "pan" + "das",
    "pol" + "ars",
    "duck" + "db",
    "read_" + "csv",
    "to_" + "csv",
    "json." + "load",
    "json" + "lines",
    "par" + "quet",
    "pre" + "dict",
    "socket" + ".",
    "subprocess" + ".",
    "url" + "open",
    "write_" + "text",
    "write_" + "bytes",
    "touch" + "(",
    "path" + "lib",
    "Path" + "(",
)

ALLOWED_STANDARD_IMPORT_ROOTS = {"dataclasses", "datetime", "typing", "__future__"}
EXPECTED_FIXTURE_FILES = {
    "tests/fixtures/weather/stage2_historical_labels": {
        "synthetic_blocked_missing_provenance.json",
        "synthetic_unclear_requires_adjudication.json",
        "synthetic_valid_source_backed_confirmed.json",
    },
    "tests/fixtures/weather/stage2_real_source_backed_labels": {
        "polymarket_nyc_may_12_2026_temperature_conflict.json",
        "polymarket_nyc_may_2026_precipitation_less_than_2_no.json",
    },
}
GENERATED_DIR_PARTS = {"generated", "research_outputs"}
HISTORICAL_LABEL_DATA_PART = "historical_label_data"


def _repo_path(rel_path: str) -> str:
    return os.path.join(REPO_ROOT, *rel_path.split("/"))


def _read(rel_path: str) -> str:
    with open(_repo_path(rel_path), encoding="utf-8") as handle:
        return handle.read()


def _module():
    return importlib.import_module("meg.weather.stage2.ingestion_boundary")


def _valid_mapping(**overrides: object) -> dict[str, object]:
    mapping: dict[str, object] = {
        "source_id": "wx-static-source-001",
        "source_name": "Human reviewed source descriptor",
        "source_category": "official_resolution_source",
        "source_identity": "Named source identity reviewed by a human",
        "source_provenance": "Human-reviewed provenance memo",
        "access_date": "2026-06-10",
        "retrieval_context": "Manual review context captured before validation",
        "evidence_status": "source_backed",
        "label_confidence": "confirmed",
        "no_lookahead_note": "Access date is recorded before any later label usage.",
        "fixture_ingestion_boundary_note": "Fixture artifacts remain static examples, not ingestion inputs.",
        "loader_ingestion_boundary_note": "Static loader remains separate from this descriptor boundary.",
        "notes": ("Static validation only.",),
    }
    mapping.update(overrides)
    return mapping


def test_implementation_prd_exists_and_contains_canonical_id() -> None:
    text = _read(PRD_REL)
    assert CANONICAL_ID in text
    for section in (
        "Status and scope",
        "Strategic framing",
        "Stage ladder position",
        "Human approval basis",
        "Static ingestion skeleton implementation boundary",
        "Implemented source module",
        "Implemented public API",
        "Closed source category vocabulary",
        "Evidence and confidence vocabulary",
        "Fail-closed blocker taxonomy",
        "Validation severity behavior",
        "Fixture-to-ingestion separation",
        "Static-loader-to-ingestion separation",
        "No-lookahead safeguard behavior",
        "Static validation tests",
        "Explicit non-approval boundaries",
        "What remains unbuilt",
        "Future gates",
        "Acceptance criteria",
        "Later-ticket handoff",
    ):
        assert section in text


def test_source_module_exists_compiles_and_uses_standard_library_only() -> None:
    source = _read(MODULE_REL)
    compile(source, MODULE_REL, "exec")
    tree = ast.parse(source)
    import_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.module is not None
            import_roots.add(node.module.split(".")[0])
    assert import_roots <= ALLOWED_STANDARD_IMPORT_ROOTS


def test_source_module_contains_no_forbidden_implementation_fragments() -> None:
    source = _read(MODULE_REL)
    offenders = [fragment for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS if fragment.lower() in source.lower()]
    assert offenders == []


def test_module_exposes_required_dataclasses_functions_and_vocabularies() -> None:
    module = _module()
    for name in (
        "StaticIngestionSourceDescriptor",
        "StaticIngestionValidationResult",
        "static_ingestion_source_descriptor_from_mapping",
        "validate_static_ingestion_source_descriptor",
        "validate_static_ingestion_source_mapping",
    ):
        assert hasattr(module, name)
    assert module.ALLOWED_SOURCE_CATEGORIES == {
        "human_reviewed_fixture_source",
        "official_resolution_source",
        "venue_rule_source",
        "weather_station_source",
        "market_metadata_source",
        "manual_research_note",
    }
    assert module.PROHIBITED_SOURCE_CATEGORIES == {
        "unattributed_social_post",
        "unverified_ai_summary",
        "live_market_feed",
        "broker_execution_feed",
        "private_credentials_source",
        "runtime_scrape",
        "unreviewed_bulk_dataset",
        "unknown_source",
    }
    assert module.EVIDENCE_STATUSES == {
        "source_backed",
        "reviewer_inferred",
        "missing",
        "conflicting",
        "not_applicable",
    }
    assert module.LABEL_CONFIDENCE_VALUES == {"confirmed", "unclear", "unknown"}
    assert module.VALIDATION_SEVERITIES == {"pass", "caution", "blocked"}


def test_valid_allowed_source_descriptor_passes() -> None:
    result = _module().validate_static_ingestion_source_mapping(_valid_mapping())
    assert result.severity == "pass"
    assert result.passed is True
    assert result.blocker_codes == ()
    assert result.caution_codes == ()


def test_conflicting_evidence_produces_caution() -> None:
    result = _module().validate_static_ingestion_source_mapping(_valid_mapping(evidence_status="conflicting"))
    assert result.severity == "caution"
    assert "conflicting_evidence" in result.caution_codes


def test_unclear_and_unknown_confidence_produce_caution() -> None:
    module = _module()
    unclear = module.validate_static_ingestion_source_mapping(_valid_mapping(label_confidence="unclear"))
    unknown = module.validate_static_ingestion_source_mapping(_valid_mapping(label_confidence="unknown"))
    assert unclear.severity == "caution"
    assert "unclear_label_confidence" in unclear.caution_codes
    assert unknown.severity == "caution"
    assert "unknown_label_confidence" in unknown.caution_codes


def test_missing_required_fields_block() -> None:
    module = _module()
    for field in (
        "source_id",
        "source_name",
        "source_category",
        "source_identity",
        "source_provenance",
        "access_date",
        "retrieval_context",
        "evidence_status",
        "label_confidence",
    ):
        result = module.validate_static_ingestion_source_mapping(_valid_mapping(**{field: ""}))
        assert result.severity == "blocked", field
        assert result.blocked is True


def test_invalid_iso_access_date_blocks() -> None:
    result = _module().validate_static_ingestion_source_mapping(_valid_mapping(access_date="06/10/2026"))
    assert result.severity == "blocked"
    assert "missing_access_date" in result.blocker_codes


def test_unsupported_source_category_blocks() -> None:
    result = _module().validate_static_ingestion_source_mapping(_valid_mapping(source_category="forum_rumor"))
    assert result.severity == "blocked"
    assert "unsupported_source_category" in result.blocker_codes


def test_prohibited_source_categories_block() -> None:
    module = _module()
    for category in module.PROHIBITED_SOURCE_CATEGORIES:
        result = module.validate_static_ingestion_source_mapping(_valid_mapping(source_category=category))
        assert result.severity == "blocked", category
        assert "prohibited_source_category" in result.blocker_codes


def test_missing_and_unsupported_evidence_status_block() -> None:
    module = _module()
    missing_value = module.validate_static_ingestion_source_mapping(_valid_mapping(evidence_status="missing"))
    unsupported = module.validate_static_ingestion_source_mapping(_valid_mapping(evidence_status="rumored"))
    empty = module.validate_static_ingestion_source_mapping(_valid_mapping(evidence_status=""))
    assert missing_value.severity == "blocked"
    assert "missing_evidence_status" in missing_value.blocker_codes
    assert unsupported.severity == "blocked"
    assert "unsupported_evidence_status" in unsupported.blocker_codes
    assert empty.severity == "blocked"
    assert "missing_evidence_status" in empty.blocker_codes


def test_missing_and_unsupported_label_confidence_block() -> None:
    module = _module()
    unsupported = module.validate_static_ingestion_source_mapping(_valid_mapping(label_confidence="likely"))
    empty = module.validate_static_ingestion_source_mapping(_valid_mapping(label_confidence=""))
    assert unsupported.severity == "blocked"
    assert "unsupported_label_confidence" in unsupported.blocker_codes
    assert empty.severity == "blocked"
    assert "missing_label_confidence" in empty.blocker_codes


def test_missing_no_lookahead_note_blocks() -> None:
    result = _module().validate_static_ingestion_source_mapping(_valid_mapping(no_lookahead_note=""))
    assert result.severity == "blocked"
    assert "missing_no_lookahead_note" in result.blocker_codes


def test_missing_fixture_and_loader_separation_notes_block() -> None:
    module = _module()
    fixture_result = module.validate_static_ingestion_source_mapping(
        _valid_mapping(fixture_ingestion_boundary_note="")
    )
    loader_result = module.validate_static_ingestion_source_mapping(
        _valid_mapping(loader_ingestion_boundary_note="")
    )
    assert fixture_result.severity == "blocked"
    assert "fixture_ingestion_confusion" in fixture_result.blocker_codes
    assert loader_result.severity == "blocked"
    assert "loader_ingestion_confusion" in loader_result.blocker_codes


def test_runtime_source_api_scoring_and_trading_drift_language_in_notes_blocks() -> None:
    module = _module()
    cases = (
        ("runtime schedule is desired", "runtime_drift"),
        ("external API client should fetch sources", "connector_drift"),
        ("probability scoring should happen", "scoring_drift"),
        ("order placement should happen", "trading_drift"),
    )
    for note, code in cases:
        result = module.validate_static_ingestion_source_mapping(_valid_mapping(notes=(note,)))
        assert result.severity == "blocked", note
        assert code in result.blocker_codes


def test_source_module_has_no_file_read_or_write_behavior() -> None:
    source = _read(MODULE_REL)
    tree = ast.parse(source)
    banned_import_roots = {
        "builtins",
        "io",
        "os",
        "sqlite3",
        "csv",
        "json",
        "glob",
    }
    banned_call_names = {
        "open",
        "compile",
        "exec",
        "eval",
        "input",
    }
    imported_roots: set[str] = set()
    calls: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported_roots.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)
    assert imported_roots.isdisjoint(banned_import_roots)
    assert calls.isdisjoint(banned_call_names)
    assert not ({"read", "write", "readline", "readlines", "writelines"} & calls)


def test_no_fixture_json_or_readme_files_are_modified_by_this_ticket() -> None:
    for rel_dir, expected_names in EXPECTED_FIXTURE_FILES.items():
        abs_dir = _repo_path(rel_dir)
        observed = {name for name in os.listdir(abs_dir) if name.endswith(".json")}
        assert observed == expected_names
        readmes = {name for name in os.listdir(abs_dir) if name.lower() == "readme.md"}
        assert readmes == {"README.md"}


def test_no_historical_label_data_or_generated_data_is_created() -> None:
    offenders: list[str] = []
    for root, dirnames, filenames in os.walk(REPO_ROOT):
        rel_root = os.path.relpath(root, REPO_ROOT)
        parts = set(()) if rel_root == "." else set(rel_root.split(os.sep))
        if ".git" in parts or ".pytest_cache" in parts or "__pycache__" in parts:
            continue
        if GENERATED_DIR_PARTS & parts or HISTORICAL_LABEL_DATA_PART in parts:
            for filename in filenames:
                offenders.append(os.path.join(rel_root, filename))
        dirnames[:] = [name for name in dirnames if name not in {".git", ".pytest_cache", "__pycache__"}]
    assert offenders == []


def test_implementation_prd_states_explicit_non_approval_boundaries() -> None:
    text = _read(PRD_REL)
    required_phrases = (
        "static ingestion boundary skeleton implementation only",
        "No real ingestion was created.",
        "No provider/API connectors were created.",
        "No source fetching was created.",
        "No external API calls were created.",
        "No credentials/secrets/config loading was created.",
        "No forecast pulls were created.",
        "No scraping/polling/streaming/scheduling/queues/jobs were created.",
        "No scoring/probability scoring was created.",
        "No backtesting/paper simulation was created.",
        "No runtime observation was created.",
        "No trading/order placement/position sizing/autonomy was created.",
        "No production behavior was created.",
        "No C++/Rust runtime components were created.",
        "No loader expansion was created.",
        "No fixture JSON/README files were created or modified.",
        "No historical-label data/generated data was created.",
        "does not imply readiness for ingestion, providers, sources, scoring, runtime, production, or trading",
    )
    missing = [phrase for phrase in required_phrases if phrase not in text]
    assert missing == []


def test_implementation_prd_requires_later_separate_approval_for_future_work() -> None:
    text = _read(PRD_REL)
    required_phrases = (
        "Future real ingestion requires separate explicit approval.",
        "Future provider/API connector implementation requires separate explicit approval.",
        "Future source fetching requires separate explicit approval.",
        "Future scoring/backtesting requires separate explicit approval.",
        "Future runtime/trading requires separate explicit approval.",
    )
    missing = [phrase for phrase in required_phrases if phrase not in text]
    assert missing == []
