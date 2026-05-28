from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE1-01_STATIC_CANONICAL_WEATHER_EVENT_MANUAL_LABEL_SCHEMA.md")


ALLOWED = {
    "manual label stage": {"stage_1_static_manual_label"},
    "market family": {
        "temperature_threshold",
        "precipitation_threshold",
        "snowfall",
        "wind_gust",
        "storm_hurricane",
        "severe_extreme_weather",
        "daily_city_location_binary",
        "monthly_seasonal_aggregate",
        "source_dependent_resolution",
        "other_unclear",
    },
    "canonical mapping decision": {
        "exact_equivalent",
        "near_equivalent",
        "related_non_equivalent",
        "incompatible",
        "unclear",
    },
    "resolver/source role": {
        "official_resolver",
        "official_weather_source",
        "station_observation_source",
        "climate_archive_source",
        "forecast_model_provider",
        "historical_data_provider",
        "convenience_api",
        "venue_discretionary_resolver",
        "unknown",
    },
    "label confidence": {"confirmed", "unclear", "unknown"},
    "trap severity": {"caution", "blocking"},
    "review posture": {"informational", "review_only", "blocked"},
    "reviewer workflow state": {
        "unreviewed",
        "caution_under_review",
        "blocking_under_review",
        "reviewed_pass",
        "reviewed_caution",
        "reviewed_block",
    },
}


def _text() -> str:
    assert PRD_PATH.exists(), f"Missing PRD file: {PRD_PATH}"
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    marker = "## Machine-checkable manual-label field assignments"
    start = text.find(marker)
    assert start != -1, "Missing machine-checkable section heading"
    next_heading = text.find("\n## ", start + len(marker))
    return text[start:] if next_heading == -1 else text[start:next_heading]


def test_stage1_prd_presence_and_core_terms() -> None:
    text = _text().lower()
    required = [
        "prd-p1-wx-stage1-01",
        "standalone meg weather bot prd",
        "stage 1",
        "static examples",
        "manual labels",
        "source-defined settlement object",
        "p(the venue-defined source/station/window/threshold/revision/classification rule resolves yes)",
        "manual-label schema",
        "example template",
        "canonical weather-event mapping",
        "machine-checkable manual-label field assignments",
        "source-defined settlement object checklist",
        "non-approval boundaries",
        "prd-p1-wx-stage1-02",
        "prd-p1-wx-stage1-03",
        "prd-p1-wx-stage1-04",
    ]
    missing = [token for token in required if token not in text]
    assert not missing, f"Missing required terms: {missing}"


def test_machine_checkable_assignments_use_only_allowed_values() -> None:
    section = _machine_section(_text()).lower()

    for field, allowed_values in ALLOWED.items():
        pattern = rf"^- {re.escape(field)}:\s*([a-z0-9_/-]+)\s*$"
        values = [m.group(1).strip() for m in re.finditer(pattern, section, flags=re.MULTILINE)]
        assert values, f"No machine-checkable assignments found for {field}"

        bad = sorted({v for v in values if v not in allowed_values})
        assert not bad, f"Invalid parsed values for {field}: {bad}"

        missing = sorted(allowed_values - set(values))
        assert not missing, f"Missing machine-checkable values for {field}: {missing}"


def test_non_approval_boundary_terms_present() -> None:
    text = _text().lower()
    required_terms = [
        "provider integration",
        "connectors",
        "external api calls",
        "provider credentials",
        "config loading",
        "secret reading",
        "data ingestion",
        "historical labels",
        "forecast pulls",
        "model scoring",
        "backtesting",
        "runtime observation",
        "trading",
        "order placement",
        "autonomy",
    ]
    missing = [term for term in required_terms if term not in text]
    assert not missing, f"Missing non-approval boundary terms: {missing}"
