from maa_azurlane.layout import (
    ContentRegionDetector,
    LayoutProfile,
    LayoutService,
    Rect,
    Size,
)


def test_to_runtime_maps_logical_rect_into_game_region() -> None:
    service = LayoutService(Size(1280, 720))
    mapped = service.to_runtime(Rect(640, 360, 128, 72), Rect(100, 50, 1920, 1080))

    assert mapped.x == 1060
    assert mapped.y == 590
    assert mapped.width == 192
    assert mapped.height == 108


def test_to_logical_maps_runtime_rect_back() -> None:
    service = LayoutService(Size(1280, 720))
    mapped = service.to_logical(Rect(1060, 590, 192, 108), Rect(100, 50, 1920, 1080))

    assert mapped.x == 640
    assert mapped.y == 360
    assert mapped.width == 128
    assert mapped.height == 72


def test_layout_profile_roundtrip() -> None:
    profile = LayoutProfile(
        name="2400x1080",
        screenshot_size=Size(2400, 1080),
        game_region=Rect(240, 0, 1920, 1080),
    )

    restored = LayoutProfile.from_dict(profile.to_dict())

    assert restored == profile
    assert round(restored.game_aspect_ratio, 3) == 1.778


def test_content_region_detector_returns_full_screen_without_borders() -> None:
    image = SyntheticImage(1280, 720, Rect(0, 0, 1280, 720))

    region = ContentRegionDetector().detect(image)

    assert region == Rect(0, 0, 1280, 720)


def test_content_region_detector_detects_horizontal_letterbox() -> None:
    image = SyntheticImage(2400, 1080, Rect(240, 0, 1920, 1080))

    region = ContentRegionDetector(scan_step=8).detect(image)

    assert region.x == 240
    assert region.y == 0
    assert 1912 <= region.width <= 1920
    assert region.height == 1080


class SyntheticImage:
    def __init__(self, width: int, height: int, content: Rect) -> None:
        self.width = width
        self.height = height
        self.content = content

    def getpixel(self, xy: tuple[int, int]) -> tuple[int, int, int]:
        x, y = xy
        in_x = self.content.left <= x < self.content.right
        in_y = self.content.top <= y < self.content.bottom
        if in_x and in_y:
            return (80, 120, 180)
        return (0, 0, 0)
