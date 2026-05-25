from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .geometry import Rect

Pixel = tuple[int, int, int] | tuple[int, int, int, int]


class PixelSource(Protocol):
    width: int
    height: int

    def getpixel(self, xy: tuple[int, int]) -> Pixel:
        """Return an RGB or RGBA pixel at the given coordinate."""


@dataclass(frozen=True)
class ContentRegionDetector:
    """Detect the visible game content region inside a captured screen."""

    color_threshold: int = 24
    scan_step: int = 4
    min_content_ratio: float = 0.5

    def detect(self, image: PixelSource) -> Rect:
        width = image.width
        height = image.height
        background = self._corner_background(image)

        left = self._scan_left(image, background)
        right = self._scan_right(image, background)
        top = self._scan_top(image, background)
        bottom = self._scan_bottom(image, background)

        detected = Rect(left, top, right - left + 1, bottom - top + 1)
        full = Rect(0, 0, width, height)

        if detected.is_empty():
            return full

        if detected.width * detected.height < width * height * self.min_content_ratio:
            return full

        return detected

    def _corner_background(self, image: PixelSource) -> tuple[int, int, int]:
        points = [
            (0, 0),
            (image.width - 1, 0),
            (0, image.height - 1),
            (image.width - 1, image.height - 1),
        ]
        pixels = [self._rgb(image.getpixel(point)) for point in points]
        return tuple(sum(pixel[i] for pixel in pixels) // len(pixels) for i in range(3))

    def _scan_left(self, image: PixelSource, background: tuple[int, int, int]) -> int:
        for x in range(0, image.width, self.scan_step):
            if self._column_has_content(image, x, background):
                return x
        return 0

    def _scan_right(self, image: PixelSource, background: tuple[int, int, int]) -> int:
        for x in range(image.width - 1, -1, -self.scan_step):
            if self._column_has_content(image, x, background):
                return x
        return image.width - 1

    def _scan_top(self, image: PixelSource, background: tuple[int, int, int]) -> int:
        for y in range(0, image.height, self.scan_step):
            if self._row_has_content(image, y, background):
                return y
        return 0

    def _scan_bottom(self, image: PixelSource, background: tuple[int, int, int]) -> int:
        for y in range(image.height - 1, -1, -self.scan_step):
            if self._row_has_content(image, y, background):
                return y
        return image.height - 1

    def _column_has_content(
        self,
        image: PixelSource,
        x: int,
        background: tuple[int, int, int],
    ) -> bool:
        for y in range(0, image.height, self.scan_step):
            pixel = self._rgb(image.getpixel((x, y)))
            if self._distance(pixel, background) > self.color_threshold:
                return True
        return False

    def _row_has_content(
        self,
        image: PixelSource,
        y: int,
        background: tuple[int, int, int],
    ) -> bool:
        for x in range(0, image.width, self.scan_step):
            pixel = self._rgb(image.getpixel((x, y)))
            if self._distance(pixel, background) > self.color_threshold:
                return True
        return False

    @staticmethod
    def _rgb(pixel: Pixel) -> tuple[int, int, int]:
        return pixel[0], pixel[1], pixel[2]

    @staticmethod
    def _distance(left: tuple[int, int, int], right: tuple[int, int, int]) -> int:
        return sum(abs(left[i] - right[i]) for i in range(3))
