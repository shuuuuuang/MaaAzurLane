"""Resolution and game content-region helpers."""

from .anchor import AnchorDefinition, load_anchors
from .detector import ContentRegionDetector
from .geometry import Point, Rect, Size
from .profile import LayoutProfile
from .service import LayoutService
from .transformer import CoordinateTransformer

__all__ = [
    "AnchorDefinition",
    "ContentRegionDetector",
    "CoordinateTransformer",
    "LayoutProfile",
    "LayoutService",
    "Point",
    "Rect",
    "Size",
    "load_anchors",
]
