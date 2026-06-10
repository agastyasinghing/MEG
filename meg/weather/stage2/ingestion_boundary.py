"""Static Weather Bot Stage 2 ingestion boundary descriptor validation.

This module validates already-human-reviewed descriptor mappings against a
closed vocabulary. It does not ingest data, fetch sources, call providers, load
configuration, score labels, run jobs, or perform runtime behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Mapping

ALLOWED_SOURCE_CATEGORIES = frozenset(
    (
        "human_reviewed_fixture_source",
        "official_resolution_source",
        "venue_rule_source",
        "weather_station_source",
        "market_metadata_source",
        "manual_research_note",
    )
)

PROHIBITED_SOURCE_CATEGORIES = frozenset(
    (
        "unattributed_social_post",
        "unverified_ai_summary",
        "live_market_feed",
        "broker_execution_feed",
        "private_credentials_source",
        "runtime_scrape",
        "unreviewed_bulk_dataset",
        "unknown_source",
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

LABEL_CONFIDENCE_VALUES = frozenset(("confirmed", "unclear", "unknown"))
VALIDATION_SEVERITIES = frozenset(("pass", "caution", "blocked"))

BLOCKER_CODES = frozenset(
    (
        "missing_source_identity",
        "missing_access_date",
        "missing_source_category",
        "missing_source_provenance",
        "missing_no_lookahead_note",
        "unsupported_source_category",
        "prohibited_source_category",
        "unknown_source_category",
        "missing_evidence_status",
        "unsupported_evidence_status",
        "missing_label_confidence",
        "unsupported_label_confidence",
        "fixture_ingestion_confusion",
        "loader_ingestion_confusion",
        "runtime_drift",
        "connector_drift",
        "scoring_drift",
        "trading_drift",
        "other_unclear",
    )
)

CAUTION_CODES = frozenset(("conflicting_evidence", "unclear_label_confidence", "unknown_label_confidence"))

_RUNTIME_DRIFT_TERMS = (
    "runtime",
    "polling",
    "streaming",
    "schedule",
    "scheduler",
    "queue",
    "background job",
)
_CONNECTOR_DRIFT_TERMS = (
    "connector",
    "provider client",
    "api client",
    "api clients",
    "external api",
    "live fetch",
    "live fetching",
    "source fetch",
    "source fetching",
    "fetch source",
    "fetching source",
)
_SCORING_DRIFT_TERMS = ("score", "scoring", "probability", "model output")
_TRADING_DRIFT_TERMS = ("trade", "trading", "order", "broker", "position sizing", "autonomy")


@dataclass(frozen=True)
class StaticIngestionSourceDescriptor:
    """Human-reviewed source descriptor for static boundary validation only."""

    source_id: str
    source_name: str
    source_category: str
    source_identity: str
    source_provenance: str
    access_date: str
    retrieval_context: str
    evidence_status: str
    label_confidence: str
    no_lookahead_note: str
    fixture_ingestion_boundary_note: str
    loader_ingestion_boundary_note: str
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class StaticIngestionValidationResult:
    """Fail-closed validation result for a static source descriptor."""

    severity: str
    blocker_codes: tuple[str, ...] = ()
    caution_codes: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()

    @property
    def passed(self) -> bool:
        return self.severity == "pass"

    @property
    def blocked(self) -> bool:
        return self.severity == "blocked"


def _as_clean_string(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


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


def static_ingestion_source_descriptor_from_mapping(
    mapping: Mapping[str, object]
) -> StaticIngestionSourceDescriptor:
    """Build a descriptor from an already-human-reviewed mapping."""

    return StaticIngestionSourceDescriptor(
        source_id=_as_clean_string(mapping.get("source_id")),
        source_name=_as_clean_string(mapping.get("source_name")),
        source_category=_as_clean_string(mapping.get("source_category")),
        source_identity=_as_clean_string(mapping.get("source_identity")),
        source_provenance=_as_clean_string(mapping.get("source_provenance")),
        access_date=_as_clean_string(mapping.get("access_date")),
        retrieval_context=_as_clean_string(mapping.get("retrieval_context")),
        evidence_status=_as_clean_string(mapping.get("evidence_status")),
        label_confidence=_as_clean_string(mapping.get("label_confidence")),
        no_lookahead_note=_as_clean_string(mapping.get("no_lookahead_note")),
        fixture_ingestion_boundary_note=_as_clean_string(mapping.get("fixture_ingestion_boundary_note")),
        loader_ingestion_boundary_note=_as_clean_string(mapping.get("loader_ingestion_boundary_note")),
        notes=_as_note_tuple(mapping.get("notes")),
    )


def _append_once(values: list[str], code: str) -> None:
    if code not in values:
        values.append(code)


def _validate_access_date(access_date: str, blockers: list[str], messages: list[str]) -> None:
    if not access_date:
        _append_once(blockers, "missing_access_date")
        messages.append("access_date is required")
        return
    try:
        date.fromisoformat(access_date)
    except ValueError:
        _append_once(blockers, "missing_access_date")
        messages.append("access_date must be an ISO date")


def _validate_drift_text(text_values: tuple[str, ...], blockers: list[str], messages: list[str]) -> None:
    joined = " ".join(text_values).lower()
    if not joined:
        return
    for terms, code, message in (
        (_RUNTIME_DRIFT_TERMS, "runtime_drift", "descriptor suggests runtime behavior"),
        (_CONNECTOR_DRIFT_TERMS, "connector_drift", "descriptor suggests connectors or source fetching"),
        (_SCORING_DRIFT_TERMS, "scoring_drift", "descriptor suggests scoring behavior"),
        (_TRADING_DRIFT_TERMS, "trading_drift", "descriptor suggests trading or order behavior"),
    ):
        if any(term in joined for term in terms):
            _append_once(blockers, code)
            messages.append(message)


def validate_static_ingestion_source_descriptor(
    descriptor: StaticIngestionSourceDescriptor,
) -> StaticIngestionValidationResult:
    """Validate a static descriptor and return pass, caution, or blocked."""

    blockers: list[str] = []
    cautions: list[str] = []
    messages: list[str] = []

    if not descriptor.source_id:
        _append_once(blockers, "other_unclear")
        messages.append("source_id is required")
    if not descriptor.source_name:
        _append_once(blockers, "other_unclear")
        messages.append("source_name is required")

    if not descriptor.source_category:
        _append_once(blockers, "missing_source_category")
        messages.append("source_category is required")
    elif descriptor.source_category in PROHIBITED_SOURCE_CATEGORIES:
        if descriptor.source_category == "unknown_source":
            _append_once(blockers, "unknown_source_category")
        _append_once(blockers, "prohibited_source_category")
        messages.append("source_category is prohibited")
    elif descriptor.source_category not in ALLOWED_SOURCE_CATEGORIES:
        _append_once(blockers, "unsupported_source_category")
        messages.append("source_category is unsupported")

    if not descriptor.source_identity:
        _append_once(blockers, "missing_source_identity")
        messages.append("source_identity is required")
    if not descriptor.source_provenance:
        _append_once(blockers, "missing_source_provenance")
        messages.append("source_provenance is required")
    _validate_access_date(descriptor.access_date, blockers, messages)
    if not descriptor.retrieval_context:
        _append_once(blockers, "other_unclear")
        messages.append("retrieval_context is required")

    if not descriptor.evidence_status:
        _append_once(blockers, "missing_evidence_status")
        messages.append("evidence_status is required")
    elif descriptor.evidence_status not in EVIDENCE_STATUSES:
        _append_once(blockers, "unsupported_evidence_status")
        messages.append("evidence_status is unsupported")
    elif descriptor.evidence_status == "missing":
        _append_once(blockers, "missing_evidence_status")
        messages.append("evidence_status missing is blocking")
    elif descriptor.evidence_status == "conflicting":
        _append_once(cautions, "conflicting_evidence")
        messages.append("evidence_status conflicting requires caution")

    if not descriptor.label_confidence:
        _append_once(blockers, "missing_label_confidence")
        messages.append("label_confidence is required")
    elif descriptor.label_confidence not in LABEL_CONFIDENCE_VALUES:
        _append_once(blockers, "unsupported_label_confidence")
        messages.append("label_confidence is unsupported")
    elif descriptor.label_confidence == "unknown":
        _append_once(cautions, "unknown_label_confidence")
        messages.append("label_confidence unknown requires caution")
    elif descriptor.label_confidence == "unclear":
        _append_once(cautions, "unclear_label_confidence")
        messages.append("label_confidence unclear requires caution")

    if not descriptor.no_lookahead_note:
        _append_once(blockers, "missing_no_lookahead_note")
        messages.append("no_lookahead_note is required")
    if not descriptor.fixture_ingestion_boundary_note:
        _append_once(blockers, "fixture_ingestion_confusion")
        messages.append("fixture_ingestion_boundary_note is required")
    if not descriptor.loader_ingestion_boundary_note:
        _append_once(blockers, "loader_ingestion_confusion")
        messages.append("loader_ingestion_boundary_note is required")

    _validate_drift_text(
        (
            descriptor.no_lookahead_note,
            descriptor.fixture_ingestion_boundary_note,
            descriptor.loader_ingestion_boundary_note,
            *descriptor.notes,
        ),
        blockers,
        messages,
    )

    severity = "blocked" if blockers else "caution" if cautions else "pass"
    return StaticIngestionValidationResult(
        severity=severity,
        blocker_codes=tuple(blockers),
        caution_codes=tuple(cautions),
        messages=tuple(messages),
    )


def validate_static_ingestion_source_mapping(mapping: Mapping[str, object]) -> StaticIngestionValidationResult:
    """Convenience wrapper for mapping-to-descriptor validation."""

    return validate_static_ingestion_source_descriptor(static_ingestion_source_descriptor_from_mapping(mapping))
