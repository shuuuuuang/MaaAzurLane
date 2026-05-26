from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

from .geometry import Rect

AnchorKind = Literal["template", "ocr", "feature", "color", "manual"]


@dataclass(frozen=True)
class AnchorDefinition:
    """Stable UI target definition in logical coordinates."""

    name: str
    page: str
    kind: AnchorKind
    logical_region: Rect
    description: str = ""
    text: str | None = None
    template: str | None = None
    tags: list[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.name:
            raise ValueError("anchor requires name")
        if not self.page:
            raise ValueError("anchor requires page")
        if self.logical_region.is_empty():
            raise ValueError("anchor logical_region must be non-empty")
        if self.kind == "ocr" and not self.text:
            raise ValueError("ocr anchor requires text")
        if self.kind == "template" and not self.template:
            raise ValueError("template anchor requires template")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AnchorDefinition:
        anchor = cls(
            name=str(data["name"]),
            page=str(data["page"]),
            kind=data["kind"],
            logical_region=Rect(**data["logical_region"]),
            description=str(data.get("description", "")),
            text=_optional_str(data.get("text")),
            template=_optional_str(data.get("template")),
            tags=[str(tag) for tag in data.get("tags", [])],
        )
        anchor.validate()
        return anchor


def load_anchors(path: Path) -> list[AnchorDefinition]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    anchors = [AnchorDefinition.from_dict(item) for item in data["anchors"]]
    names = [anchor.name for anchor in anchors]
    if len(names) != len(set(names)):
        raise ValueError(f"duplicate anchor names in {path}")
    return anchors


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
