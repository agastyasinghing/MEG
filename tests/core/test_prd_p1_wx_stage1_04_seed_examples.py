from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE1-04_STATIC_MANUALLY_LABELED_SEED_EXAMPLES.md")

ALLOWED = {
    "seed example stage": {"stage_1_static_seed_example"},
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
    "trap source": {
        "market_wording",
        "resolution_source",
        "provider_source",
        "location_station",
        "time_window",
        "threshold_unit",
        "measurement_method",
        "data_revision",
        "venue_discretion",
        "external_event_classification",
        "market_microstructure",
        "validation_provenance",
        "other_unclear",
    },
    "trap severity": {"caution", "blocking"},
    "false-edge risk": {
        "none_identified",
        "possible_false_edge",
        "likely_false_edge",
        "blocking_false_edge",
        "unclear",
    },
    "canonical mapping impact": {
        "no_material_impact",
        "mapping_unclear",
        "near_equivalence_only",
        "non_equivalent",
        "mapping_blocked",
    },
    "adjudication outcome": {"accepted", "revised", "escalated", "blocked", "deferred"},
    "evidence status": {"source_backed", "reviewer_inferred", "missing", "conflicting", "not_applicable"},
    "label confidence": {"confirmed", "unclear", "unknown"},
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

EXPECTED_ASSIGNMENT_LINES = [
    "- seed example stage: stage_1_static_seed_example",
    "- market family: temperature_threshold",
    "- market family: precipitation_threshold",
    "- market family: snowfall",
    "- market family: wind_gust",
    "- market family: storm_hurricane",
    "- market family: severe_extreme_weather",
    "- market family: daily_city_location_binary",
    "- market family: monthly_seasonal_aggregate",
    "- market family: source_dependent_resolution",
    "- market family: other_unclear",
    "- canonical mapping decision: exact_equivalent",
    "- canonical mapping decision: near_equivalent",
    "- canonical mapping decision: related_non_equivalent",
    "- canonical mapping decision: incompatible",
    "- canonical mapping decision: unclear",
    "- resolver/source role: official_resolver",
    "- resolver/source role: official_weather_source",
    "- resolver/source role: station_observation_source",
    "- resolver/source role: climate_archive_source",
    "- resolver/source role: forecast_model_provider",
    "- resolver/source role: historical_data_provider",
    "- resolver/source role: convenience_api",
    "- resolver/source role: venue_discretionary_resolver",
    "- resolver/source role: unknown",
    "- trap source: market_wording",
    "- trap source: resolution_source",
    "- trap source: provider_source",
    "- trap source: location_station",
    "- trap source: time_window",
    "- trap source: threshold_unit",
    "- trap source: measurement_method",
    "- trap source: data_revision",
    "- trap source: venue_discretion",
    "- trap source: external_event_classification",
    "- trap source: market_microstructure",
    "- trap source: validation_provenance",
    "- trap source: other_unclear",
    "- trap severity: caution",
    "- trap severity: blocking",
    "- false-edge risk: none_identified",
    "- false-edge risk: possible_false_edge",
    "- false-edge risk: likely_false_edge",
    "- false-edge risk: blocking_false_edge",
    "- false-edge risk: unclear",
    "- canonical mapping impact: no_material_impact",
    "- canonical mapping impact: mapping_unclear",
    "- canonical mapping impact: near_equivalence_only",
    "- canonical mapping impact: non_equivalent",
    "- canonical mapping impact: mapping_blocked",
    "- adjudication outcome: accepted",
    "- adjudication outcome: revised",
    "- adjudication outcome: escalated",
    "- adjudication outcome: blocked",
    "- adjudication outcome: deferred",
    "- evidence status: source_backed",
    "- evidence status: reviewer_inferred",
    "- evidence status: missing",
    "- evidence status: conflicting",
    "- evidence status: not_applicable",
    "- label confidence: confirmed",
    "- label confidence: unclear",
    "- label confidence: unknown",
    "- review posture: informational",
    "- review posture: review_only",
    "- review posture: blocked",
    "- reviewer workflow state: unreviewed",
    "- reviewer workflow state: caution_under_review",
    "- reviewer workflow state: blocking_under_review",
    "- reviewer workflow state: reviewed_pass",
    "- reviewer workflow state: reviewed_caution",
    "- reviewer workflow state: reviewed_block",
]


def _text() -> str:
    assert PRD_PATH.exists(), f"Missing PRD file: {PRD_PATH}"
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    marker = "## Machine-checkable seed-example field assignments"
    assert text.count(marker) == 1, "Expected exactly one machine-checkable section heading"
    start = text.find(marker)
    after_start = text[start + len(marker) :]
    next_heading = re.search(r"^##\s+", after_start, flags=re.MULTILINE)
    return after_start if next_heading is None else after_start[: next_heading.start()]


def _seed_example_sections(text: str) -> list[str]:
    matches = list(re.finditer(r"^###\s+Seed example\b.*$", text, flags=re.MULTILINE))
    sections = []
    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(text[match.start() : next_start])
    return sections


def test_stage1_04_prd_presence_and_core_terms() -> None:
    text = _text().lower()
    required = [
        "prd-p1-wx-stage1-04",
        "standalone meg weather bot prd",
        "prd-p1-wx-stage1-01",
        "prd-p1-wx-stage1-02",
        "prd-p1-wx-stage1-03",
        "stage 1",
        "static seed-example work",
        "static seed examples",
        "source-defined settlement object",
        "manual-label summary",
        "trap-label summary",
        "reviewer adjudication summary",
        "machine-checkable seed-example field assignments",
        "representative synthetic example",
        "non-approval boundaries",
    ]
    missing = [token for token in required if token not in text]
    assert not missing, f"Missing required terms: {missing}"


def test_seed_example_count_and_required_families() -> None:
    sections = _seed_example_sections(_text())
    assert 4 <= len(sections) <= 6

    required_families = {
        "temperature_threshold",
        "precipitation_threshold",
        "snowfall",
        "wind_gust",
    }
    example_text = "\n".join(sections).lower()
    missing = sorted(family for family in required_families if family not in example_text)
    assert not missing, f"Missing required seed market families in seed examples: {missing}"


def test_each_seed_example_contains_required_static_sections() -> None:
    required_terms = [
        "representative synthetic example, not live market data",
        "`market family`",
        "`synthetic raw market wording`",
        "`source-defined settlement object summary`",
        "`manual-label summary`",
        "`trap-label summary`",
        "`reviewer adjudication summary`",
        "`closed-set values used`",
        "`human-review note`",
        "`non-approval reminder`",
        "`source notes or synthetic-example note`",
    ]
    for index, section in enumerate(_seed_example_sections(_text()), start=1):
        lower_section = section.lower()
        missing = [term for term in required_terms if term not in lower_section]
        assert not missing, f"Seed example {index} missing required terms: {missing}"


def test_seed_example_closed_set_values_are_allowed() -> None:
    allowed_values = set().union(*ALLOWED.values())
    pattern = r"^- `closed-set values used`:\s*(.+)$"
    for index, section in enumerate(_seed_example_sections(_text()), start=1):
        match = re.search(pattern, section, flags=re.MULTILINE)
        assert match is not None, f"Seed example {index} missing closed-set values line"
        values = re.findall(r"`([^`]+)`", match.group(1))
        assert values, f"Seed example {index} has no closed-set values"
        bad = sorted({value for value in values if value not in allowed_values})
        assert not bad, f"Seed example {index} uses invalid closed-set values: {bad}"


def test_closed_set_values_are_documented() -> None:
    text = _text().lower()
    missing = []
    for field, allowed_values in ALLOWED.items():
        if field not in text:
            missing.append(field)
        missing.extend(sorted(value for value in allowed_values if value not in text))
    assert not missing, f"Missing closed-set field names or values: {missing}"


def test_machine_checkable_section_contains_exact_assignment_lines() -> None:
    section = _machine_section(_text())
    section_lines = [line.strip() for line in section.splitlines() if line.strip()]
    assert section_lines == EXPECTED_ASSIGNMENT_LINES


def test_machine_checkable_assignments_use_only_allowed_values() -> None:
    section = _machine_section(_text()).lower()

    for field, allowed_values in ALLOWED.items():
        pattern = rf"^\s*-\s*{re.escape(field)}:\s*([a-z0-9_/-]+)\s*$"
        values = [m.group(1).strip() for m in re.finditer(pattern, section, flags=re.MULTILINE)]
        assert values, f"No machine-checkable assignments found for {field}"

        bad = sorted({value for value in values if value not in allowed_values})
        assert not bad, f"Invalid parsed values for {field}: {bad}"

        missing = sorted(allowed_values - set(values))
        assert not missing, f"Missing machine-checkable values for {field}: {missing}"


def test_forbidden_examples_documented_but_not_globally_rejected() -> None:
    text = _text().lower()
    forbidden_examples = [
        "confirmed/unclear",
        "caution/blocking",
        "accepted/revised",
        "source_backed/reviewer_inferred",
        "exact_equivalent/near_equivalent",
        "review_only/blocked",
        "possible_false_edge/likely_false_edge",
        "market_wording/resolution_source",
        "partial",
        "mixed",
        "likely",
        "maybe",
        "approved",
        "configured",
        "available",
        "trade_ready",
        "auto_execute",
        "autonomous",
        "live",
        "production",
        "provider_ready",
        "model_ready",
        "backtest_ready",
        "ready_for_ingestion",
        "ready_for_scoring",
    ]
    missing = [example for example in forbidden_examples if example not in text]
    assert not missing, f"Forbidden examples section missing examples: {missing}"


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
        "probability scoring",
        "backtesting",
        "paper simulation",
        "runtime observation",
        "trading",
        "order placement",
        "autonomy",
    ]
    missing = [term for term in required_terms if term not in text]
    assert not missing, f"Missing non-approval boundary terms: {missing}"


def test_non_approval_boundaries_do_not_use_approval_phrasing() -> None:
    text = _text().lower()
    forbidden_approval_phrases = [
        "provider integration is approved",
        "connectors are approved",
        "connector implementation is approved",
        "external api calls are approved",
        "provider credentials are approved",
        "config loading is approved",
        "secret reading is approved",
        "data ingestion is approved",
        "historical labels are approved",
        "forecast pulls are approved",
        "model scoring is approved",
        "probability scoring is approved",
        "backtesting is approved",
        "paper simulation is approved",
        "runtime observation is approved",
        "trading is approved",
        "order placement is approved",
        "autonomy is approved",
    ]
    bad = [phrase for phrase in forbidden_approval_phrases if phrase in text]
    assert not bad, f"Forbidden approval language found: {bad}"
