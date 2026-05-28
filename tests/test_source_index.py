from pathlib import Path

import pytest

from maa_azurlane.calibration import AssetSource, SourceIndex


def test_load_reference_source_index() -> None:
    index = SourceIndex.load(Path("reference/source_index.json"))

    assert index.schema_version == 1
    assert [source.id for source in index.upstreams] == ["alas", "azurpilot"]
    assert [source.license for source in index.upstreams] == ["GPL-3.0", "GPL-3.0"]
    assert [asset.id for asset in index.assets] == [
        "main.btn_campaign",
        "main.btn_build",
        "main.btn_mission",
        "main.btn_shop",
        "main.btn_dock",
        "main.btn_fleet",
        "main.bottom_menu",
    ]
    campaign = index.assets[0]
    assert campaign.upstream == "azurpilot"
    assert campaign.source_path == "assets/cn/ui/MAIN_GOTO_CAMPAIGN.BUTTON.png"
    assert campaign.status == "modified"
    fleet = index.assets[5]
    assert fleet.source_path == "assets/cn/ui/MAIN_GOTO_FLEET.BUTTON.png"


def test_copied_asset_requires_upstream_and_source_path() -> None:
    asset = AssetSource(
        id="main.btn_campaign",
        kind="template",
        target_path="reference/image/main/btn_campaign.png",
        upstream=None,
        source_path=None,
        license="GPL-3.0",
        status="copied",
        usage="Template for campaign button.",
    )

    with pytest.raises(ValueError, match="requires upstream"):
        asset.validate({"alas"})


def test_asset_target_path_uses_posix_relative_path() -> None:
    asset = AssetSource(
        id="bad.path",
        kind="template",
        target_path=r"reference\image\bad.png",
        upstream=None,
        source_path=None,
        license="GPL-3.0-only",
        status="placeholder",
        usage="Invalid path example.",
    )

    with pytest.raises(ValueError, match="relative POSIX"):
        asset.validate(set())


def test_asset_status_must_be_known() -> None:
    asset = AssetSource(
        id="bad.status",
        kind="template",
        target_path="reference/image/bad.png",
        upstream=None,
        source_path=None,
        license="GPL-3.0-only",
        status="todo",
        usage="Invalid status example.",
    )

    with pytest.raises(ValueError, match="invalid status"):
        asset.validate(set())
