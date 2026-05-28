from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    root = ROOT
    validate_interface(root / "interface.json")
    validate_calibration(root / "reference/calibration.json")
    validate_source_index(root / "reference/source_index.json")
    for path in sorted(root.glob("resource/pipeline/**/*.json")):
        with path.open("r", encoding="utf-8") as file:
            json.load(file)
        print(f"valid json: {path.relative_to(root)}")
    return 0


def validate_interface(path: Path) -> None:
    with path.open("r", encoding="utf-8") as file:
        data: dict[str, Any] = json.load(file)

    if data.get("interface_version") != 2:
        raise ValueError("interface.json must use ProjectInterface V2")

    resources = data.get("resource")
    if not isinstance(resources, list) or not resources:
        raise ValueError("interface.json resource must be a non-empty list")

    for resource in resources:
        if not isinstance(resource, dict):
            raise ValueError("interface.json resource entries must be objects")
        resource_path = resource.get("path")
        if not isinstance(resource_path, str) or not resource_path:
            raise ValueError("interface.json resource entries require path")

    controllers = data.get("controller")
    if not isinstance(controllers, list) or not controllers:
        raise ValueError("interface.json controller must be a non-empty list")

    tasks = data.get("task")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("interface.json task must be a non-empty list")

    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("interface.json task entries must be objects")
        if not isinstance(task.get("name"), str) or not task["name"]:
            raise ValueError("interface.json task entries require name")
        if not isinstance(task.get("entry"), str) or not task["entry"]:
            raise ValueError("interface.json task entries require entry")

    print(f"valid interface: {path.name}")


def validate_calibration(path: Path) -> None:
    from maa_azurlane.calibration import CalibrationManifest

    manifest = CalibrationManifest.load(path)
    image_root = path.parent / "image"
    for item in manifest.items:
        if item.reference_image:
            image_path = image_root / item.reference_image
            if not image_path.exists():
                raise FileNotFoundError(
                    f"missing reference image for {item.id}: "
                    f"{image_path.relative_to(ROOT)}"
                )
    print(f"valid calibration: {path.relative_to(ROOT)}")


def validate_source_index(path: Path) -> None:
    from maa_azurlane.calibration import SourceIndex

    index = SourceIndex.load(path)
    for asset in index.assets:
        if asset.status == "placeholder":
            continue
        target = ROOT / asset.target_path
        if not target.exists():
            raise FileNotFoundError(
                f"missing source-index target for {asset.id}: {asset.target_path}"
            )
    print(f"valid source index: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    raise SystemExit(main())
