"""Resolution and game content-region helpers."""

from .detector import ContentRegionDetector
from .geometry import Point, Rect, Size
from .profile import LayoutProfile
from .service import LayoutService

__all__ = [
    "ContentRegionDetector",
    "LayoutProfile",
    "LayoutService",
    "Point",
    "Rect",
    "Size",
]
