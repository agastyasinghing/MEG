from pathlib import Path

import pytest

from meg.weather.stage2 import source_identity_runtime as sir


MODULE_PATH = Path("meg/weather/stage2/source_identity_runtime.py")
TEST_PATH = Path("tests/core/test_weather_source_identity_runtime.py")


def _valid_record(**overrides: object) -> sir.SourceIdentityRecord:
    values = {
        "condition_id": "condition-1",
        "token_id": "token-1",
        "outcome": "Yes",
        "source_id": "reviewed-source-1",
        "source_family": sir.SourceFamily.MANUAL_HUMAN_REVIEW_SOURCE_FAMILY,
        "source_uri_descriptor": "human-reviewed static source descriptor",
        "source_access_method": sir.SourceAccessMethod.MANUAL_REVIEW,
        "source_identity_status": sir.SourceIdentityStatus.SOURCE_IDENTITY_RECORDED,
        "runtime_gate_status": sir.RuntimeGateStatus.RUNTIME_GATE_READY,
    }
    values.update(overrides)
    return sir.SourceIdentityRecord(**values)


def _assert_blocked_with_reason(record: sir.SourceIdentityRecord, reason: str) -> None:
    result = sir.validate_source_identity_record(record)
    assert result.passed is False
    assert result.severity is sir.ValidationSeverity.BLOCKED
    assert reason in result.reasons


def test_enums_are_closed_sets() -> None:
    assert sir.SourceFamily.values() == frozenset(
        {
            "forecast_provider_family",
            "historical_observation_provider_family",
            "official_resolution_source_family",
            "market_metadata_source_family",
            "manual_human_review_source_family",
            "unsupported_source_family",
            "unknown_source_family",
        }
    )
    assert sir.SourceAccessMethod.values() == frozenset(
        {
            "manual_review",
            "static_reference",
            "api_call",
            "scraping",
            "file_download",
            "provider_sdk",
            "unknown_requires_review",
        }
    )
    assert sir.SourceIdentityStatus.values() == frozenset(
        {
            "source_identity_recorded",
            "source_identity_missing",
            "source_identity_ambiguous",
            "source_identity_unsupported",
            "source_identity_unknown",
        }
    )
    assert sir.RuntimeGateStatus.values() == frozenset(
        {
            "runtime_gate_ready",
            "runtime_gate_blocked",
            "runtime_gate_requires_manual_review",
            "runtime_gate_unknown",
        }
    )
    assert sir.ValidationSeverity.values() == frozenset(
        {"passed", "caution", "failed", "blocked"}
    )


def test_dataclass_construction() -> None:
    record = _valid_record(provenance_notes="operator reviewed only")

    assert record.condition_id == "condition-1"
    assert record.token_id == "token-1"
    assert record.outcome == "Yes"
    assert record.source_family is sir.SourceFamily.MANUAL_HUMAN_REVIEW_SOURCE_FAMILY
    assert record.provenance_notes == "operator reviewed only"


def test_mapping_construction_coerces_string_enums() -> None:
    record = sir.source_identity_record_from_mapping(
        {
            "condition_id": "condition-1",
            "token_id": "token-1",
            "outcome": "No",
            "source_id": "static-reference-1",
            "source_family": "official_resolution_source_family",
            "source_uri_descriptor": "static descriptor only",
            "source_access_method": "static_reference",
            "source_identity_status": "source_identity_recorded",
            "runtime_gate_status": "runtime_gate_ready",
            "provenance_notes": "review note",
        }
    )

    assert record.source_family is sir.SourceFamily.OFFICIAL_RESOLUTION_SOURCE_FAMILY
    assert record.source_access_method is sir.SourceAccessMethod.STATIC_REFERENCE
    assert record.source_identity_status is sir.SourceIdentityStatus.SOURCE_IDENTITY_RECORDED
    assert record.runtime_gate_status is sir.RuntimeGateStatus.RUNTIME_GATE_READY
    assert record.provenance_notes == "review note"


@pytest.mark.parametrize(
    "access_method",
    (sir.SourceAccessMethod.MANUAL_REVIEW, sir.SourceAccessMethod.STATIC_REFERENCE),
)
def test_minimal_valid_records_pass(access_method: sir.SourceAccessMethod) -> None:
    result = sir.validate_source_identity_record(_valid_record(source_access_method=access_method))

    assert result.passed is True
    assert result.severity is sir.ValidationSeverity.PASSED
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("condition_id", "condition_id is missing"),
        ("token_id", "token_id is missing"),
        ("outcome", "outcome is missing"),
        ("source_id", "source_id is missing"),
        ("source_uri_descriptor", "source_uri_descriptor is missing"),
    ),
)
def test_blank_required_text_fields_fail_closed(field_name: str, reason: str) -> None:
    _assert_blocked_with_reason(_valid_record(**{field_name: "  "}), reason)


@pytest.mark.parametrize(
    "source_family",
    (sir.SourceFamily.UNKNOWN_SOURCE_FAMILY, sir.SourceFamily.UNSUPPORTED_SOURCE_FAMILY),
)
def test_unknown_and_unsupported_source_families_fail_closed(
    source_family: sir.SourceFamily,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(source_family=source_family),
        f"source family is {source_family.value}",
    )


@pytest.mark.parametrize(
    "access_method",
    (
        sir.SourceAccessMethod.API_CALL,
        sir.SourceAccessMethod.SCRAPING,
        sir.SourceAccessMethod.FILE_DOWNLOAD,
        sir.SourceAccessMethod.PROVIDER_SDK,
        sir.SourceAccessMethod.UNKNOWN_REQUIRES_REVIEW,
    ),
)
def test_runtime_access_methods_fail_closed(access_method: sir.SourceAccessMethod) -> None:
    _assert_blocked_with_reason(
        _valid_record(source_access_method=access_method),
        f"source access method is {access_method.value}",
    )


@pytest.mark.parametrize(
    "identity_status",
    (
        sir.SourceIdentityStatus.SOURCE_IDENTITY_MISSING,
        sir.SourceIdentityStatus.SOURCE_IDENTITY_AMBIGUOUS,
        sir.SourceIdentityStatus.SOURCE_IDENTITY_UNSUPPORTED,
        sir.SourceIdentityStatus.SOURCE_IDENTITY_UNKNOWN,
    ),
)
def test_non_recorded_source_identity_statuses_fail_closed(
    identity_status: sir.SourceIdentityStatus,
) -> None:
    _assert_blocked_with_reason(
        _valid_record(source_identity_status=identity_status),
        f"source identity status is {identity_status.value}",
    )


@pytest.mark.parametrize(
    "gate_status",
    (
        sir.RuntimeGateStatus.RUNTIME_GATE_BLOCKED,
        sir.RuntimeGateStatus.RUNTIME_GATE_REQUIRES_MANUAL_REVIEW,
        sir.RuntimeGateStatus.RUNTIME_GATE_UNKNOWN,
    ),
)
def test_non_ready_runtime_gate_statuses_fail_closed(gate_status: sir.RuntimeGateStatus) -> None:
    _assert_blocked_with_reason(
        _valid_record(runtime_gate_status=gate_status),
        f"runtime gate status is {gate_status.value}",
    )


def test_new_files_do_not_contain_noncanonical_identifier_string() -> None:
    forbidden = "market" "_id"

    assert forbidden not in MODULE_PATH.read_text(encoding="utf-8")
    assert forbidden not in TEST_PATH.read_text(encoding="utf-8")


def test_module_source_has_no_network_provider_execution_or_file_io_calls() -> None:
    source_text = MODULE_PATH.read_text(encoding="utf-8")
    forbidden_terms = (
        "requests",
        "httpx",
        "urllib",
        "aiohttp",
        "boto3",
        "polymarket",
        "subprocess",
        "open(",
        ".read_text(",
        ".write_text(",
        "socket",
        "os.environ",
        "dotenv",
    )

    for term in forbidden_terms:
        assert term not in source_text
