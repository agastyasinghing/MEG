from pathlib import Path


def test_prd_p1_wx_01_weather_taxonomy_contract() -> None:
    path = Path(
        "docs/prd/PRD-P1-WX-01_WEATHER_BOT_REQUIREMENTS_AND_MARKET_TAXONOMY_PLANNING.md"
    )
    assert path.exists(), f"Missing PRD file: {path}"

    text = path.read_text(encoding="utf-8")
    lower = text.lower()

    assert "PRD-P1-WX-01" in text
    assert "canonical event graph" in lower

    required_concepts = [
        "canonical weather event identity",
        "weather market taxonomy",
        "venue-market mapping",
        "resolution-risk",
        "human-review",
        "non-goals",
        "prd-p1-wx-02",
        "prd-p1-wx-03",
        "prd-p1-wx-04",
        "opus",
    ]
    missing = [item for item in required_concepts if item not in lower]
    assert not missing, f"Missing required planning concepts: {missing}"

    required_non_approval_terms = [
        "connectors",
        "external api calls",
        "runtime execution",
        "forecast",
        "trading",
        "order placement",
        "autonomy",
    ]
    missing_non_approval = [
        item for item in required_non_approval_terms if item not in lower
    ]
    assert not missing_non_approval, (
        "Missing non-approval boundary terms: "
        f"{missing_non_approval}"
    )


    forbidden_approval_phrases = [
        "connectors are approved",
        "connector implementation is approved",
        "external api calls are approved",
        "runtime execution is approved",
        "forecasts are approved",
        "forecast pulls are approved",
        "trading is approved",
        "order placement is approved",
        "autonomy is approved",
        "live weather api calls are approved",
    ]
    bad = [item for item in forbidden_approval_phrases if item in lower]
    assert not bad, f"Forbidden approval language found: {bad}"
