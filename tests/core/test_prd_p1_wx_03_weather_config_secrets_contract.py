from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-03_WEATHER_BOT_CONFIG_SECRETS_FAIL_CLOSED_CONTRACT.md")
ALLOWED_STATES = {"missing", "disabled", "unapproved", "invalid", "ready"}
FORBIDDEN_PARSED_STATES = {
    "missing/invalid",
    "disabled/unapproved",
    "unapproved/invalid",
    "ready/disabled",
    "ready/invalid",
    "partial",
    "mixed",
    "ready_with_warnings",
    "maybe_ready",
    "approved",
    "configured",
    "available",
    "unknown",
}


def _read() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def _parsed_expected_readiness_states(text: str) -> list[str]:
    parsed: list[str] = []
    for match in re.finditer(r"expected readiness state:\s*([a-z0-9_/-]+)", text.lower()):
        parsed.append(match.group(1).strip())
    return parsed


def test_prd_p1_wx_03_exists() -> None:
    assert PRD_PATH.exists(), f"Missing PRD file: {PRD_PATH}"


def test_prd_p1_wx_03_required_content() -> None:
    text = _read()
    lower = text.lower()

    assert "PRD-P1-WX-03" in text
    assert "PRD-P1-WX-01" in text
    assert "PRD-P1-WX-02" in text

    required_terms = [
        "config/secrets",
        "fail-closed",
        "closed readiness state",
        "approval gate",
        "secrets contract",
        "failure modes",
        "human-review",
        "observability",
        "non-goals",
        "prd-p1-wx-04",
        "opus",
    ]

    missing = [term for term in required_terms if term not in lower]
    assert not missing, f"Missing required terms: {missing}"


def test_prd_p1_wx_03_has_readiness_sections_and_allowed_states() -> None:
    lower = _read().lower()

    assert "forbidden readiness values" in lower
    assert "## machine-checkable readiness-state assignments" in lower

    for state in sorted(ALLOWED_STATES):
        assert re.search(rf"\b{re.escape(state)}\b", lower), f"Missing allowed readiness state: {state}"


def test_prd_p1_wx_03_parsed_readiness_states_are_closed_set() -> None:
    text = _read()
    parsed_states = _parsed_expected_readiness_states(text)

    assert parsed_states, "No parsed 'expected readiness state' values found."

    invalid_states = sorted({state for state in parsed_states if state not in ALLOWED_STATES})
    assert not invalid_states, f"Invalid parsed readiness-state values found: {invalid_states}"

    forbidden_used = sorted({state for state in parsed_states if state in FORBIDDEN_PARSED_STATES})
    assert not forbidden_used, f"Forbidden parsed readiness-state values found: {forbidden_used}"


def test_prd_p1_wx_03_parsed_readiness_states_cover_allowed_set() -> None:
    parsed_states = set(_parsed_expected_readiness_states(_read()))
    missing = sorted(ALLOWED_STATES - parsed_states)
    assert not missing, f"Missing machine-checkable readiness-state coverage for: {missing}"


def test_prd_p1_wx_03_non_approval_boundaries_present() -> None:
    lower = _read().lower()

    required_non_approvals = [
        "config-loading implementation",
        "environment-variable loading",
        "secret reading",
        "connector implementation",
        "external api calls",
        "credentials",
        "runtime execution",
        "forecast pulls",
        "trading",
        "order placement",
        "autonomy",
    ]

    missing = [term for term in required_non_approvals if term not in lower]
    assert not missing, f"Missing non-approval boundary terms: {missing}"
