from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .geometry import Rect, Size


@dataclass(frozen=True)
class LayoutProfile:
    """Persisted mapping between a screenshot size and its game content region."""

    name: str
    screenshot_size: Size
    game_region: Rect
    source: str = "auto"

    @property
    def aspect_ratio(self) -> float:
        return self.screenshot_size.width / self.screenshot_size.height

    @property
    def game_aspect_ratio(self) -> float:
        return self.game_region.width / self.game_region.height

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LayoutProfile:
        return cls(
            name=str(data["name"]),
            screenshot_size=Size(**data["screenshot_size"]),
            game_region=Rect(**data["game_region"]),
            source=str(data.get("source", "auto")),
        )
