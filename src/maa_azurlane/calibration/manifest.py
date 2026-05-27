from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

from maa_azurlane.layout import Rect, Size

CalibrationCategory = Literal["template", "roi", "swipe", "anchor"]
CalibrationPack = Literal["core", "daily", "battle", "opsi", "advanced"]


@dataclass(frozen=True)
class PipelineRef:
    """A concrete pipeline field affected by one calibration item."""

    node: str
    field: str

    def validate(self) -> None:
        if not self.node:
            raise ValueError("pipeline ref requires node")
        if not self.field:
            raise ValueError("pipeline ref requires field")


@dataclass(frozen=True)
class CalibrationItem:
    """Developer-maintained description of one calibratable UI element."""

    id: str
    category: CalibrationCategory
    description: str
    reference_roi: Rect
    pack: CalibrationPack = "core"
    how_to_reach: str = ""
    reference_image: str | None = None
    repeat: bool = False
    pipeline_refs: list[PipelineRef] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.id:
            raise ValueError("calibration item requires id")
        if not self.description:
            raise ValueError(f"calibration item {self.id} requires description")
        if self.reference_roi.is_empty():
            raise ValueError(f"calibration item {self.id} requires non-empty roi")
        if self.category == "template" and not self.reference_image:
            raise ValueError(f"template item {self.id} requires reference_image")
        for ref in self.pipeline_refs:
            ref.validate()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CalibrationItem:
        item = cls(
            id=str(data["id"]),
            category=data["category"],
            description=str(data["description"]),
            reference_roi=Rect.from_sequence(data["reference_roi"]),
            pack=data.get("pack", "core"),
            how_to_reach=str(data.get("how_to_reach", "")),
            reference_image=_optional_str(data.get("reference_image")),
            repeat=bool(data.get("repeat", False)),
            pipeline_refs=[
                PipelineRef(**ref) for ref in data.get("pipeline_refs", [])
            ],
            tags=[str(tag) for tag in data.get("tags", [])],
        )
        item.validate()
        return item

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["reference_roi"] = self.reference_roi.to_list()
        return data


@dataclass(frozen=True)
class CalibrationManifest:
    """Reference calibration manifest maintained by project developers."""

    version: str
    base_resolution: Size
    game_version: str
    items: list[CalibrationItem]

    def validate(self) -> None:
        if not self.version:
            raise ValueError("calibration manifest requires version")
        if self.base_resolution.width <= 0 or self.base_resolution.height <= 0:
            raise ValueError("calibration manifest base_resolution must be positive")
        ids = [item.id for item in self.items]
        if len(ids) != len(set(ids)):
            raise ValueError("calibration manifest contains duplicate item ids")
        for item in self.items:
            item.validate()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CalibrationManifest:
        manifest = cls(
            version=str(data["version"]),
            base_resolution=Size.from_sequence(data["base_resolution"]),
            game_version=str(data.get("game_version", "")),
            items=[CalibrationItem.from_dict(item) for item in data["items"]],
        )
        manifest.validate()
        return manifest

    @classmethod
    def load(cls, path: Path) -> CalibrationManifest:
        with path.open("r", encoding="utf-8") as file:
            return cls.from_dict(json.load(file))

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "base_resolution": self.base_resolution.to_list(),
            "game_version": self.game_version,
            "items": [item.to_dict() for item in self.items],
        }


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
