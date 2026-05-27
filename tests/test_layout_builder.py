import json
from pathlib import Path

import pytest

from maa_azurlane.calibration import CalibrationManifest, LayoutBuilder
from maa_azurlane.layout import Rect, Size


def test_layout_builder_writes_layout_and_template(tmp_path: Path) -> None:
    manifest = CalibrationManifest.load(Path("reference/calibration.json"))
    item = manifest.items[0]
    builder = LayoutBuilder(
        "device-720p",
        Size(1280, 720),
        manifest_version=manifest.version,
        output_root=tmp_path,
    )

    builder.add_template(item, Rect(1010, 560, 220, 120), b"png-bytes")
    output_dir = builder.flush()

    layout = json.loads((output_dir / "layout.json").read_text(encoding="utf-8"))
    assert layout["device_id"] == "device-720p"
    assert layout["native_resolution"] == [1280, 720]
    assert layout["maa720_resolution"] == [1280, 720]
    assert layout["elements"]["main.btn_campaign"] == {
        "category": "template",
        "native": {"x": 1010, "y": 560, "w": 220, "h": 120},
        "maa720p": {"x": 1010, "y": 560, "w": 220, "h": 120},
        "image": "image/main/btn_campaign.png",
    }
    assert (output_dir / "image/main/btn_campaign.png").read_bytes() == b"png-bytes"


def test_layout_builder_uses_scaler_for_non_720p_templates(
    tmp_path: Path,
) -> None:
    manifest = CalibrationManifest.load(Path("reference/calibration.json"))
    item = manifest.items[0]

    def scaler(image_bytes: bytes, transformer) -> bytes:  # noqa: ANN001
        assert transformer.scale_ratio == 1.5
        return image_bytes + b"-scaled"

    builder = LayoutBuilder(
        "device-1080p",
        Size(1920, 1080),
        manifest_version=manifest.version,
        output_root=tmp_path,
        template_scaler=scaler,
    )

    builder.add_template(item, Rect(1515, 840, 330, 180), b"png-bytes")
    output_dir = builder.flush()
    layout = json.loads((output_dir / "layout.json").read_text(encoding="utf-8"))

    assert layout["scale_ratio"] == 1.5
    assert layout["elements"]["main.btn_campaign"]["maa720p"] == {
        "x": 1010,
        "y": 560,
        "w": 220,
        "h": 120,
    }
    assert (
        output_dir / "image/main/btn_campaign.png"
    ).read_bytes() == b"png-bytes-scaled"


def test_layout_builder_requires_scaler_for_non_720p_template() -> None:
    manifest = CalibrationManifest.load(Path("reference/calibration.json"))
    builder = LayoutBuilder(
        "device-1080p",
        Size(1920, 1080),
        manifest_version=manifest.version,
    )

    with pytest.raises(RuntimeError, match="template_scaler"):
        builder.add_template(manifest.items[0], Rect(1515, 840, 330, 180), b"png")


def test_layout_builder_replaces_existing_layout_atomically(tmp_path: Path) -> None:
    manifest = CalibrationManifest.load(Path("reference/calibration.json"))
    item = manifest.items[0]
    first = LayoutBuilder(
        "device-720p",
        Size(1280, 720),
        manifest_version=manifest.version,
        output_root=tmp_path,
    )
    first.add_template(item, Rect(1010, 560, 220, 120), b"old")
    output_dir = first.flush()

    second = LayoutBuilder(
        "device-720p",
        Size(1280, 720),
        manifest_version=manifest.version,
        output_root=tmp_path,
    )
    second.add_template(item, Rect(1000, 550, 200, 100), b"new")
    output_dir = second.flush()

    layout = json.loads((output_dir / "layout.json").read_text(encoding="utf-8"))
    assert layout["elements"]["main.btn_campaign"]["native"] == {
        "x": 1000,
        "y": 550,
        "w": 200,
        "h": 100,
    }
    assert (output_dir / "image/main/btn_campaign.png").read_bytes() == b"new"


def test_calibration_layout_builds_pipeline_overrides() -> None:
    manifest = CalibrationManifest.load(Path("reference/calibration.json"))
    builder = LayoutBuilder(
        "device-720p",
        Size(1280, 720),
        manifest_version=manifest.version,
    )

    builder.add_template(manifest.items[0], Rect(1010, 560, 220, 120), b"png")
    overrides = builder.build().build_pipeline_overrides(manifest)

    assert overrides == {
        "MainCampaignButton": {
            "recognition": {
                "param": {
                    "roi": [1010, 560, 220, 120],
                    "template": "image/main/btn_campaign.png",
                }
            }
        }
    }


def test_layout_builder_expands_ocr_roi(tmp_path: Path) -> None:
    manifest = CalibrationManifest.load(Path("reference/calibration.json"))
    item = manifest.items[1]
    builder = LayoutBuilder(
        "device-1080p",
        Size(1920, 1080),
        manifest_version=manifest.version,
        output_root=tmp_path,
    )

    builder.add_roi(item, Rect(0, 0, 30, 30), ocr_expand=3)
    layout = builder.build().to_dict()

    assert layout["elements"]["main.bottom_menu"]["maa720p"] == {
        "x": 0,
        "y": 0,
        "w": 23,
        "h": 23,
    }
