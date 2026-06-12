"""Offline Weather Bot Stage 2 real-ingestion descriptor validation.

This module validates caller-supplied, already-reviewed source descriptor
mappings. It is deterministic standard-library code only: it performs no source
retrieval, provider integration, credential loading, forecast pulls, market
observation, probability work, historical replay, or execution behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

ALLOWED_SOURCE_CATEGORIES = frozenset(
    (
        "official_resolution_source",
        "venue_rule_source",
        "weather_station_source",
        "market_metadata_source",
        "forecast_provider_source",
        "exchange_market_source",
        "manual_research_note",
        "human_reviewed_fixture_source",
        "not_applicable",
    )
)

ALLOWED_SOURCE_INTAKE_MODES = frozenset(
    (
        "human_reviewed_manual_entry",
        "offline_static_descriptor",
        "future_provider_connector_after_approval",
        "future_source_fetch_after_approval",
        "future_manual_upload_after_approval",
        "not_applicable",
    )
)

PROHIBITED_SOURCE_INTAKE_MODES = frozenset(
    (
        "unauthenticated_runtime_scrape",
        "private_credentials_without_approval",
        "live_market_feed_without_approval",
        "unreviewed_bulk_dataset",
        "unattributed_social_post",
        "unverified_ai_summary",
        "unknown_source",
    )
)

BLOCKER_CODES = frozenset(
    (
        "missing_source_identity",
        "missing_source_name",
        "missing_source_category",
        "missing_source_intake_mode",
        "missing_access_date",
        "missing_retrieval_context",
        "missing_source_provenance",
        "missing_no_lookahead_statement",
        "missing_human_reviewed_flag",
        "missing_static_caller_supplied_flag",
        "unsupported_source_category",
        "unsupported_source_intake_mode",
        "prohibited_source_intake_mode",
        "private_credentials_required",
        "source_conflict",
        "provider_conflict",
        "time_window_conflict",
        "fixture_real_ingestion_confusion",
        "static_loader_real_ingestion_confusion",
        "static_skeleton_real_ingestion_confusion",
        "runtime_drift",
        "connector_drift",
        "scoring_drift",
        "trading_drift",
        "other_unclear",
    )
)

EVIDENCE_STATUSES = frozenset(
    (
        "source_backed",
        "reviewer_inferred",
        "missing",
        "conflicting",
        "not_applicable",
    )
)

VALIDATION_SEVERITIES = frozenset(("info", "warning", "blocker"))
VALIDATION_STATES = frozenset(("pass", "caution", "blocked"))
CAUTION_SOURCE_INTAKE_MODES = frozenset(
    (
        "future_provider_connector_after_approval",
        "future_source_fetch_after_approval",
        "future_manual_upload_after_approval",
    )
)

_CONNECTOR_DRIFT_TERMS = (
    "api call",
    "api calls",
    "api client",
    "connector",
    "external api",
    "fetch data",
    "fetch source",
    "fetch sources",
    "forecast pull",
    "forecast pulls",
    "live fetch",
    "provider api",
    "provider apis",
    "provider client",
    "provider integration",
    "pull forecast",
    "pull forecasts",
    "retrieve source",
    "retrieve sources",
    "runtime scrape",
    "scrape data",
    "scraping",
    "source fetch",
    "source fetching",
    "source retrieval",
    "source scraping",
    "web scraping",
)
_RUNTIME_DRIFT_TERMS = (
    "background job",
    "background jobs",
    "market observation",
    "observe markets",
    "polling",
    "production behavior",
    "queue job",
    "queue jobs",
    "runtime observation",
    "runtime",
    "schedule jobs",
    "scheduled job",
    "scheduled jobs",
    "scheduling",
    "streaming",
)
_SCORING_DRIFT_TERMS = (
    "backtest",
    "forecast model output",
    "model forecast output",
    "paper simulation",
    "probability score",
    "score probabilities",
)
_TRADING_DRIFT_TERMS = (
    "autonomous",
    "autonomously",
    "auto_execute",
    "broker position",
    "execution behavior",
    "order placement",
    "place orders",
    "trade execution",
    "unsupervised execution",
)
_PRIVATE_CREDENTIAL_TERMS = (
    "credential required",
    "credentials",
    "load config",
    "load secrets",
    "loading config",
    "loading secrets",
    "private credential",
    "requires credential",
    "secret required",
)
_CONFLICT_TERMS = (
    ("source_conflict", ("source conflict", "conflicting source")),
    ("provider_conflict", ("provider conflict", "conflicting provider")),
    ("time_window_conflict", ("time window conflict", "lookahead conflict")),
    ("fixture_real_ingestion_confusion", ("fixture is real ingestion",)),
    ("static_loader_real_ingestion_confusion", ("static loader is real ingestion",)),
    ("static_skeleton_real_ingestion_confusion", ("static skeleton is real ingestion",)),
)


@dataclass(frozen=True)
class RealIngestionSourceDescriptor:
    """Caller-supplied real-ingestion source descriptor for offline checks only."""

    source_id: str
    source_name: str
    source_category: str
    source_intake_mode: str
    provenance_url: str | None
    provenance_note: str | None
    access_date: str
    retrieval_context: str
    no_lookahead_statement: str
    human_reviewed: bool
    static_caller_supplied: bool
    evidence_status: str
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RealIngestionValidationResult:
    """Closed-set fail-closed validation result."""

    validation_state: str
    severity: str
    blocker_codes: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()

    @property
    def passed(self) -> bool:
        return self.validation_state == "pass"

    @property
    def blocked(self) -> bool:
        return self.validation_state == "blocked"



def _as_clean_string(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()



def _as_optional_clean_string(value: object) -> str | None:
    clean = _as_clean_string(value)
    return clean or None



def _as_bool(value: object) -> bool:
    return value is True



def _as_note_tuple(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        clean = value.strip()
        return (clean,) if clean else ()
    try:
        iterator = iter(value)  # type: ignore[arg-type]
    except TypeError:
        clean = _as_clean_string(value)
        return (clean,) if clean else ()

    notes: list[str] = []
    for item in iterator:
        clean = _as_clean_string(item)
        if clean:
            notes.append(clean)
    return tuple(notes)



def real_ingestion_source_descriptor_from_mapping(
    mapping: Mapping[str, object]
) -> RealIngestionSourceDescriptor:
    """Build a descriptor from an already-reviewed caller-supplied mapping."""

    return RealIngestionSourceDescriptor(
        source_id=_as_clean_string(mapping.get("source_id")),
        source_name=_as_clean_string(mapping.get("source_name")),
        source_category=_as_clean_string(mapping.get("source_category")),
        source_intake_mode=_as_clean_string(mapping.get("source_intake_mode")),
        provenance_url=_as_optional_clean_string(mapping.get("provenance_url")),
        provenance_note=_as_optional_clean_string(mapping.get("provenance_note")),
        access_date=_as_clean_string(mapping.get("access_date")),
        retrieval_context=_as_clean_string(mapping.get("retrieval_context")),
        no_lookahead_statement=_as_clean_string(mapping.get("no_lookahead_statement")),
        human_reviewed=_as_bool(mapping.get("human_reviewed")),
        static_caller_supplied=_as_bool(mapping.get("static_caller_supplied")),
        evidence_status=_as_clean_string(mapping.get("evidence_status")),
        notes=_as_note_tuple(mapping.get("notes")),
    )



def _append_once(values: list[str], code: str) -> None:
    if code not in values:
        values.append(code)



def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)



def _descriptor_text(descriptor: RealIngestionSourceDescriptor) -> str:
    parts = (
        descriptor.source_id,
        descriptor.source_name,
        descriptor.provenance_url or "",
        descriptor.provenance_note or "",
        descriptor.access_date,
        descriptor.retrieval_context,
        descriptor.no_lookahead_statement,
        descriptor.evidence_status,
        *descriptor.notes,
    )
    return "\n".join(parts)



def _validate_required_fields(
    descriptor: RealIngestionSourceDescriptor,
    blockers: list[str],
    messages: list[str],
) -> None:
    required_text_fields = (
        ("source_id", descriptor.source_id, "missing_source_identity"),
        ("source_name", descriptor.source_name, "missing_source_name"),
        ("source_category", descriptor.source_category, "missing_source_category"),
        ("source_intake_mode", descriptor.source_intake_mode, "missing_source_intake_mode"),
        ("access_date", descriptor.access_date, "missing_access_date"),
        ("retrieval_context", descriptor.retrieval_context, "missing_retrieval_context"),
        (
            "no_lookahead_statement",
            descriptor.no_lookahead_statement,
            "missing_no_lookahead_statement",
        ),
    )
    for field_name, value, code in required_text_fields:
        if not value:
            _append_once(blockers, code)
            messages.append(f"{field_name} is required")

    if not (descriptor.provenance_url or descriptor.provenance_note):
        _append_once(blockers, "missing_source_provenance")
        messages.append("provenance_url or provenance_note is required")
    if descriptor.human_reviewed is not True:
        _append_once(blockers, "missing_human_reviewed_flag")
        messages.append("human_reviewed must be true")
    if descriptor.static_caller_supplied is not True:
        _append_once(blockers, "missing_static_caller_supplied_flag")
        messages.append("static_caller_supplied must be true")



def _validate_closed_sets(
    descriptor: RealIngestionSourceDescriptor,
    blockers: list[str],
    messages: list[str],
) -> None:
    if descriptor.source_category and descriptor.source_category not in ALLOWED_SOURCE_CATEGORIES:
        _append_once(blockers, "unsupported_source_category")
        messages.append("source_category is not supported")

    if descriptor.source_intake_mode in PROHIBITED_SOURCE_INTAKE_MODES:
        _append_once(blockers, "prohibited_source_intake_mode")
        messages.append("source_intake_mode is prohibited")
    elif descriptor.source_intake_mode and descriptor.source_intake_mode not in ALLOWED_SOURCE_INTAKE_MODES:
        _append_once(blockers, "unsupported_source_intake_mode")
        messages.append("source_intake_mode is not supported")

    if descriptor.evidence_status and descriptor.evidence_status not in EVIDENCE_STATUSES:
        _append_once(blockers, "other_unclear")
        messages.append("evidence_status is not supported")



def _validate_drift_terms(
    descriptor: RealIngestionSourceDescriptor,
    blockers: list[str],
    messages: list[str],
) -> None:
    text = _descriptor_text(descriptor)
    drift_checks = (
        ("connector_drift", _CONNECTOR_DRIFT_TERMS, "connector or source-retrieval behavior is implied"),
        ("runtime_drift", _RUNTIME_DRIFT_TERMS, "runtime behavior is implied"),
        ("scoring_drift", _SCORING_DRIFT_TERMS, "probability work is implied"),
        ("trading_drift", _TRADING_DRIFT_TERMS, "execution behavior is implied"),
        ("private_credentials_required", _PRIVATE_CREDENTIAL_TERMS, "private credentials are implied"),
    )
    for code, terms, message in drift_checks:
        if _contains_any(text, terms):
            _append_once(blockers, code)
            messages.append(message)

    lowered = text.lower()
    for code, terms in _CONFLICT_TERMS:
        if any(term in lowered for term in terms):
            _append_once(blockers, code)
            messages.append(f"{code} is implied")



def validate_real_ingestion_source_descriptor(
    descriptor: RealIngestionSourceDescriptor,
) -> RealIngestionValidationResult:
    """Validate an offline real-ingestion descriptor and fail closed on drift."""

    blockers: list[str] = []
    messages: list[str] = []
    _validate_required_fields(descriptor, blockers, messages)
    _validate_closed_sets(descriptor, blockers, messages)
    _validate_drift_terms(descriptor, blockers, messages)

    if blockers:
        return RealIngestionValidationResult(
            validation_state="blocked",
            severity="blocker",
            blocker_codes=tuple(blockers),
            messages=tuple(messages),
        )
    caution_messages: list[str] = []
    if descriptor.source_intake_mode in CAUTION_SOURCE_INTAKE_MODES:
        caution_messages.append("source_intake_mode requires later approval before use")
    if descriptor.evidence_status in {"reviewer_inferred", "not_applicable"}:
        caution_messages.append("evidence_status warrants reviewer caution")
    if caution_messages:
        return RealIngestionValidationResult(
            validation_state="caution",
            severity="warning",
            messages=tuple(caution_messages),
        )
    return RealIngestionValidationResult(validation_state="pass", severity="info")



def validate_real_ingestion_source_mapping(
    mapping: Mapping[str, object]
) -> RealIngestionValidationResult:
    """Validate an offline real-ingestion descriptor mapping."""

    return validate_real_ingestion_source_descriptor(
        real_ingestion_source_descriptor_from_mapping(mapping)
    )
