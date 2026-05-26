from pathlib import Path

import pytest

from maa_azurlane.layout import AnchorDefinition, Rect, load_anchors


def test_load_home_anchors() -> None:
    anchors = load_anchors(Path("resource/config/anchors/home.json"))

    assert [anchor.name for anchor in anchors] == [
        "home.bottom_menu",
        "home.battle_entry",
    ]
    assert anchors[1].text == "出击"


def test_ocr_anchor_requires_text() -> None:
    anchor = AnchorDefinition(
        name="home.invalid",
        page="home",
        kind="ocr",
        logical_region=Rect(0, 0, 100, 100),
    )

    with pytest.raises(ValueError, match="text"):
        anchor.validate()


def test_template_anchor_requires_template() -> None:
    anchor = AnchorDefinition(
        name="home.invalid_template",
        page="home",
        kind="template",
        logical_region=Rect(0, 0, 100, 100),
    )

    with pytest.raises(ValueError, match="template"):
        anchor.validate()
