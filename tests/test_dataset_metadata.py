from pathlib import Path

import pytest

from maa_azurlane.dataset import ScreenshotMetadata
from maa_azurlane.layout import Rect, Size


def test_screenshot_metadata_roundtrip(tmp_path: Path) -> None:
    metadata = ScreenshotMetadata(
        image="home_cn_2400x1080_mumu12_001.png",
        page="home",
        server="cn",
        language="zh-CN",
        device="Windows",
        emulator="MuMu 12",
        screenshot_size=Size(2400, 1080),
        game_region=Rect(240, 0, 1920, 1080),
        tags=["home", "20:9"],
    )
    path = tmp_path / "home_cn_2400x1080_mumu12_001.json"

    metadata.save(path)
    restored = ScreenshotMetadata.load(path)

    assert restored == metadata
    assert restored.image_path(path) == tmp_path / metadata.image


def test_screenshot_metadata_requires_positive_size() -> None:
    metadata = ScreenshotMetadata(
        image="invalid.png",
        page="home",
        server="cn",
        language="zh-CN",
        screenshot_size=Size(0, 1080),
    )

    with pytest.raises(ValueError, match="screenshot_size"):
        metadata.validate()
