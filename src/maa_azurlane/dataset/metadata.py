from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from maa_azurlane.layout import Rect, Size


@dataclass(frozen=True)
class ScreenshotMetadata:
    """Sidecar metadata for one replayable screenshot."""

    image: str
    page: str
    server: str
    language: str
    screenshot_size: Size
    device: str | None = None
    emulator: str | None = None
    game_region: Rect | None = None
    tags: list[str] = field(default_factory=list)
    notes: str = ""
    schema_version: int = 1

    def validate(self) -> None:
        if self.schema_version != 1:
            raise ValueError("unsupported screenshot metadata schema_version")
        if not self.image:
            raise ValueError("screenshot metadata requires image")
        if not self.page:
            raise ValueError("screenshot metadata requires page")
        if not self.server:
            raise ValueError("screenshot metadata requires server")
        if not self.language:
            raise ValueError("screenshot metadata requires language")
        if self.screenshot_size.width <= 0 or self.screenshot_size.height <= 0:
            raise ValueError("screenshot_size must be positive")
        if self.game_region is not None and self.game_region.is_empty():
            raise ValueError("game_region must be non-empty when present")

    def image_path(self, metadata_path: Path) -> Path:
        return (metadata_path.parent / self.image).resolve()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ScreenshotMetadata:
        game_region = data.get("game_region")
        return cls(
            schema_version=int(data.get("schema_version", 1)),
            image=str(data["image"]),
            page=str(data["page"]),
            server=str(data["server"]),
            language=str(data["language"]),
            device=_optional_str(data.get("device")),
            emulator=_optional_str(data.get("emulator")),
            screenshot_size=Size(**data["screenshot_size"]),
            game_region=Rect(**game_region) if game_region else None,
            tags=[str(tag) for tag in data.get("tags", [])],
            notes=str(data.get("notes", "")),
        )

    @classmethod
    def load(cls, path: Path) -> ScreenshotMetadata:
        with path.open("r", encoding="utf-8") as file:
            metadata = cls.from_dict(json.load(file))
        metadata.validate()
        return metadata

    def save(self, path: Path) -> None:
        self.validate()
        with path.open("w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=2, ensure_ascii=False)
            file.write("\n")


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
