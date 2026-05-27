from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

RectSequence: TypeAlias = (
    list[int | float] | tuple[int | float, int | float, int | float, int | float]
)


@dataclass(frozen=True)
class Size:
    width: int
    height: int

    @classmethod
    def from_sequence(cls, values: list[int] | tuple[int, int]) -> Size:
        return cls(width=int(values[0]), height=int(values[1]))

    def to_list(self) -> list[int]:
        return [self.width, self.height]


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    width: float
    height: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def top(self) -> float:
        return self.y

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center(self) -> Point:
        return Point(self.x + self.width / 2, self.y + self.height / 2)

    def is_empty(self) -> bool:
        return self.width <= 0 or self.height <= 0

    @classmethod
    def from_sequence(cls, values: RectSequence) -> Rect:
        return cls(
            x=float(values[0]),
            y=float(values[1]),
            width=float(values[2]),
            height=float(values[3]),
        )

    def to_list(self) -> list[int | float]:
        return [self.x, self.y, self.width, self.height]
