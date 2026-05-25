from maa_azurlane.layout import LayoutService, Rect, Size


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
