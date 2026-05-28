from pathlib import Path

import pytest

from maa_azurlane.calibration import CalibrationItem, CalibrationManifest
from maa_azurlane.layout import Rect


def test_load_reference_calibration_manifest() -> None:
    manifest = CalibrationManifest.load(Path("reference/calibration.json"))

    assert manifest.version == "0.1.0"
    assert manifest.base_resolution.to_list() == [1280, 720]
    assert [item.id for item in manifest.items] == [
        "main.btn_campaign",
        "main.btn_build",
        "main.btn_mission",
        "main.btn_shop",
        "main.btn_dock",
        "main.btn_fleet",
        "main.bottom_menu",
    ]
    assert manifest.items[0].reference_roi.to_list() == [1021.0, 292.0, 139.0, 140.0]
    assert manifest.items[1].reference_image == "main/btn_build.png"
    assert manifest.items[5].pipeline_refs[0].node == "MainFleetButton"
    assert manifest.items[0].pipeline_refs[0].node == "MainCampaignButton"


def test_template_item_requires_reference_image() -> None:
    item = CalibrationItem(
        id="main.invalid",
        category="template",
        description="Invalid template.",
        reference_roi=Rect(0, 0, 100, 100),
    )

    with pytest.raises(ValueError, match="reference_image"):
        item.validate()
