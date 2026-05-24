from pathlib import Path


PRD_PATH = Path("docs/prd/PRD-P1-WX-02_WEATHER_DATA_PROVIDER_RESEARCH_AND_CONNECTOR_APPROVAL_GATE.md")


def test_prd_p1_wx_02_exists() -> None:
    assert PRD_PATH.exists(), f"Missing PRD file: {PRD_PATH}"


def test_prd_p1_wx_02_required_content() -> None:
    text = PRD_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "PRD-P1-WX-02" in text
    assert "PRD-P1-WX-01" in text

    required_terms = [
        "provider research",
        "connector approval gate",
        "resolution-rule compatibility",
        "canonical event graph",
        "provider evaluation",
        "provider candidate matrix",
        "provider-to-market-family",
        "source notes",
        "access date",
        "confirmed",
        "unclear",
        "unknown",
        "human-review",
        "non-goals",
        "prd-p1-wx-03",
        "prd-p1-wx-04",
        "opus",
    ]

    missing = [term for term in required_terms if term not in lower]
    assert not missing, f"Missing required terms: {missing}"


def test_prd_p1_wx_02_non_approval_language() -> None:
    lower = PRD_PATH.read_text(encoding="utf-8").lower()

    required_non_approvals = [
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
    assert not missing, f"Missing non-approval terms: {missing}"
