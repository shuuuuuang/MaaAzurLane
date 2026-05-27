from maa_azurlane.layout import CoordinateTransformer, Rect, Size


def test_native_to_maa720_sizes() -> None:
    cases = [
        (Size(1280, 720), Size(1280, 720), 1.0),
        (Size(1920, 1080), Size(1280, 720), 1.5),
        (Size(2400, 1080), Size(1600, 720), 1.5),
        (Size(2560, 1440), Size(1280, 720), 2.0),
        (Size(2048, 1536), Size(960, 720), 1536 / 720),
    ]

    for native_size, maa720_size, scale_ratio in cases:
        transformer = CoordinateTransformer(native_size)

        assert transformer.maa720_size == maa720_size
        assert transformer.scale_ratio == scale_ratio


def test_rect_roundtrip_between_native_and_maa720() -> None:
    transformer = CoordinateTransformer(Size(2400, 1080))
    native = Rect(1700, 480, 700, 600)

    maa720 = transformer.rect_to_maa720(native)
    restored = transformer.rect_to_native(maa720)

    assert maa720 == Rect(1133, 320, 467, 400)
    assert restored == Rect(1700, 480, 700, 600)


def test_ocr_expand_is_clamped_to_maa720_space() -> None:
    transformer = CoordinateTransformer(Size(1920, 1080))

    expanded = transformer.rect_to_maa720(Rect(0, 0, 30, 30), expand=3)

    assert expanded == Rect(0, 0, 23, 23)
