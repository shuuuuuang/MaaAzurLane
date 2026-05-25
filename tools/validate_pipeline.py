from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    validate_interface(root / "interface.json")
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


if __name__ == "__main__":
    raise SystemExit(main())
