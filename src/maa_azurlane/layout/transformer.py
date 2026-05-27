from __future__ import annotations

from dataclasses import dataclass

from .geometry import Point, Rect, Size


@dataclass(frozen=True)
class CoordinateTransformer:
    """Convert between native device space and Maa's height-720 space."""

    native_size: Size
    target_height: int = 720

    def __post_init__(self) -> None:
        if self.native_size.width <= 0 or self.native_size.height <= 0:
            raise ValueError("native_size must be positive")
        if self.target_height <= 0:
            raise ValueError("target_height must be positive")

    @property
    def scale_ratio(self) -> float:
        return self.native_size.height / self.target_height

    @property
    def maa720_size(self) -> Size:
        return Size(
            width=round(self.native_size.width / self.scale_ratio),
            height=self.target_height,
        )

    def point_to_maa720(self, point: Point) -> Point:
        return Point(
            x=round(point.x / self.scale_ratio),
            y=round(point.y / self.scale_ratio),
        )

    def rect_to_maa720(self, rect: Rect, expand: int = 0) -> Rect:
        converted = Rect(
            x=round(rect.x / self.scale_ratio),
            y=round(rect.y / self.scale_ratio),
            width=round(rect.width / self.scale_ratio),
            height=round(rect.height / self.scale_ratio),
        )
        if expand <= 0:
            return self._clamp_maa720(converted)
        return self._clamp_maa720(
            Rect(
                x=converted.x - expand,
                y=converted.y - expand,
                width=converted.width + expand * 2,
                height=converted.height + expand * 2,
            )
        )

    def rect_to_native(self, rect: Rect) -> Rect:
        return Rect(
            x=round(rect.x * self.scale_ratio),
            y=round(rect.y * self.scale_ratio),
            width=round(rect.width * self.scale_ratio),
            height=round(rect.height * self.scale_ratio),
        )

    def _clamp_maa720(self, rect: Rect) -> Rect:
        size = self.maa720_size
        x = max(0, min(rect.x, size.width))
        y = max(0, min(rect.y, size.height))
        right = max(x, min(rect.right, size.width))
        bottom = max(y, min(rect.bottom, size.height))
        return Rect(x=x, y=y, width=right - x, height=bottom - y)
