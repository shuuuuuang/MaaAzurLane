from __future__ import annotations

from .geometry import Point, Rect, Size


class LayoutService:
    """Map MaaAzurLane logical coordinates into the detected game region."""

    def __init__(self, logical_size: Size | None = None) -> None:
        self.logical_size = logical_size or Size(width=1280, height=720)

    def to_runtime(self, logical: Rect, game_region: Rect) -> Rect:
        scale_x = game_region.width / self.logical_size.width
        scale_y = game_region.height / self.logical_size.height
        return Rect(
            x=game_region.x + logical.x * scale_x,
            y=game_region.y + logical.y * scale_y,
            width=logical.width * scale_x,
            height=logical.height * scale_y,
        )

    def to_logical(self, runtime: Rect, game_region: Rect) -> Rect:
        scale_x = self.logical_size.width / game_region.width
        scale_y = self.logical_size.height / game_region.height
        return Rect(
            x=(runtime.x - game_region.x) * scale_x,
            y=(runtime.y - game_region.y) * scale_y,
            width=runtime.width * scale_x,
            height=runtime.height * scale_y,
        )

    def point_to_runtime(self, logical: Point, game_region: Rect) -> Point:
        rect = self.to_runtime(Rect(logical.x, logical.y, 0, 0), game_region)
        return Point(rect.x, rect.y)
