import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from maa_azurlane.calibration import (
    CalibrationInjector,
    CalibrationManifest,
    LayoutBuilder,
)
from maa_azurlane.layout import Rect, Size


@dataclass
class FakeResource:
    images: dict[str, bytes] = field(default_factory=dict)
    pipelines: list[dict[str, object]] = field(default_factory=list)

    def override_image(self, name: str, data: bytes) -> None:
        self.images[name] = data

    def override_pipeline(self, pipeline: str) -> None:
        self.pipelines.append(json.loads(pipeline))


def test_calibration_injector_overrides_images_and_pipeline(
    tmp_path: Path,
) -> None:
    manifest = CalibrationManifest.load(Path("reference/calibration.json"))
    builder = LayoutBuilder(
        "device-720p",
        Size(1280, 720),
        manifest_version=manifest.version,
        output_root=tmp_path,
    )
    builder.add_template(
        manifest.items[0],
        Rect(1010, 560, 220, 120),
        b"campaign",
        variants=["main/btn_campaign_pressed"],
    )
    layout_dir = builder.flush()

    resource = FakeResource()
    result = CalibrationInjector(manifest).inject(
        resource,
        builder.build(),
        layout_dir,
    )

    assert result.images == [
        "main/btn_campaign.png",
        "main/btn_campaign_pressed.png",
    ]
    assert result.pipeline_nodes == ["MainCampaignButton"]
    assert result.missing_images == []
    assert resource.images == {
        "main/btn_campaign.png": b"campaign",
        "main/btn_campaign_pressed.png": b"campaign",
    }
    assert resource.pipelines == [
        {
            "MainCampaignButton": {
                "recognition": {
                    "param": {
                        "roi": [1010, 560, 220, 120],
                        "template": "main/btn_campaign.png",
                    }
                }
            }
        }
    ]


def test_calibration_injector_reports_missing_images_in_non_strict_mode(
    tmp_path: Path,
) -> None:
    manifest = CalibrationManifest.load(Path("reference/calibration.json"))
    builder = LayoutBuilder(
        "device-720p",
        Size(1280, 720),
        manifest_version=manifest.version,
        output_root=tmp_path,
    )
    builder.add_template(manifest.items[0], Rect(1010, 560, 220, 120), b"campaign")
    layout_dir = builder.flush()
    (layout_dir / "image/main/btn_campaign.png").unlink()

    resource = FakeResource()
    result = CalibrationInjector(manifest).inject(
        resource,
        builder.build(),
        layout_dir,
        strict=False,
    )

    assert result.images == []
    assert result.pipeline_nodes == ["MainCampaignButton"]
    assert result.missing_images == ["main/btn_campaign.png"]
    assert resource.images == {}
    assert len(resource.pipelines) == 1


def test_calibration_injector_raises_on_missing_images_by_default(
    tmp_path: Path,
) -> None:
    manifest = CalibrationManifest.load(Path("reference/calibration.json"))
    builder = LayoutBuilder(
        "device-720p",
        Size(1280, 720),
        manifest_version=manifest.version,
        output_root=tmp_path,
    )
    builder.add_template(manifest.items[0], Rect(1010, 560, 220, 120), b"campaign")
    layout_dir = builder.flush()
    (layout_dir / "image/main/btn_campaign.png").unlink()

    with pytest.raises(FileNotFoundError, match="main/btn_campaign.png"):
        CalibrationInjector(manifest).inject(
            FakeResource(),
            builder.build(),
            layout_dir,
        )
