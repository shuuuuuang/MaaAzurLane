from __future__ import annotations

from io import BytesIO

from PIL import Image

from maa_azurlane.layout import CoordinateTransformer


def resize_template_to_maa720p(
    image_bytes: bytes,
    transformer: CoordinateTransformer,
) -> bytes:
    """Resize a native cropped template into Maa's height-720 image space."""

    with Image.open(BytesIO(image_bytes)) as image:
        width, height = image.size
        target_size = (
            max(1, round(width / transformer.scale_ratio)),
            max(1, round(height / transformer.scale_ratio)),
        )
        if target_size == image.size:
            resized = image.copy()
        else:
            resized = image.resize(target_size, Image.Resampling.LANCZOS)

        output = BytesIO()
        resized.save(output, format="PNG")
        return output.getvalue()
