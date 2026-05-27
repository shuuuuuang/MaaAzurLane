from __future__ import annotations

import json
import shutil
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

from maa_azurlane.calibration.manifest import CalibrationItem, CalibrationManifest
from maa_azurlane.layout import CoordinateTransformer, Rect, Size

TemplateScaler = Callable[[bytes, CoordinateTransformer], bytes]


@dataclass(frozen=True)
class LayoutElement:
    """One user-calibrated UI element in native and Maa height-720 space."""

    id: str
    category: str
    native: Rect
    maa720p: Rect
    image: str | None = None
    variants: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        data: dict[str, object] = {
            "category": self.category,
            "native": _rect_to_dict(self.native),
            "maa720p": _rect_to_dict(self.maa720p),
        }
        if self.image:
            data["image"] = self.image
        if self.variants:
            data["variants"] = list(self.variants)
        return data


@dataclass(frozen=True)
class CalibrationLayout:
    """Persisted user calibration data for one device fingerprint."""

    device_id: str
    native_size: Size
    maa720_size: Size
    scale_ratio: float
    manifest_version: str
    elements: dict[str, LayoutElement]
    version: str = "0.1.0"

    def to_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "device_id": self.device_id,
            "manifest_version": self.manifest_version,
            "native_resolution": self.native_size.to_list(),
            "maa720_resolution": self.maa720_size.to_list(),
            "target_height": self.maa720_size.height,
            "scale_ratio": self.scale_ratio,
            "elements": {
                element_id: element.to_dict()
                for element_id, element in sorted(self.elements.items())
            },
        }

    def build_pipeline_overrides(
        self, manifest: CalibrationManifest
    ) -> dict[str, object]:
        """Build Maa resource pipeline overrides from calibrated elements."""

        overrides: dict[str, object] = {}
        by_id = {item.id: item for item in manifest.items}
        for element_id, element in self.elements.items():
            item = by_id.get(element_id)
            if item is None:
                continue
            for ref in item.pipeline_refs:
                value: object
                if ref.field.endswith(".roi"):
                    value = element.maa720p.to_list()
                elif ref.field.endswith(".template"):
                    value = element.image
                else:
                    continue
                if value is not None:
                    _set_nested(overrides, ref.node, ref.field, value)
        return overrides


class LayoutBuilder:
    """Generate layout.json and calibrated template images for one device."""

    def __init__(
        self,
        device_id: str,
        native_size: Size,
        *,
        manifest_version: str,
        output_root: Path | str = "user_data",
        template_scaler: TemplateScaler | None = None,
    ) -> None:
        if not device_id:
            raise ValueError("device_id is required")
        self.device_id = device_id
        self.output_root = Path(output_root)
        self.manifest_version = manifest_version
        self.transformer = CoordinateTransformer(native_size)
        self.template_scaler = template_scaler or _identity_scaler
        self._elements: dict[str, LayoutElement] = {}
        self._images: dict[str, bytes] = {}

    def add_roi(
        self,
        item: CalibrationItem,
        native_roi: Rect,
        *,
        ocr_expand: int = 0,
    ) -> LayoutElement:
        element = self._build_element(item, native_roi, ocr_expand=ocr_expand)
        self._elements[item.id] = element
        return element

    def add_template(
        self,
        item: CalibrationItem,
        native_roi: Rect,
        image_bytes: bytes,
        *,
        variants: list[str] | None = None,
    ) -> LayoutElement:
        if not image_bytes:
            raise ValueError("template image bytes are required")
        element = self._build_element(item, native_roi, variants=variants)
        if not element.image:
            raise ValueError(f"template item {item.id} requires reference_image")

        scaled = self.template_scaler(image_bytes, self.transformer)
        self._images[element.image] = scaled
        for variant in element.variants:
            self._images[variant] = scaled
        self._elements[item.id] = element
        return element

    def build(self) -> CalibrationLayout:
        return CalibrationLayout(
            device_id=self.device_id,
            native_size=self.transformer.native_size,
            maa720_size=self.transformer.maa720_size,
            scale_ratio=self.transformer.scale_ratio,
            manifest_version=self.manifest_version,
            elements=dict(self._elements),
        )

    def flush(self) -> Path:
        """Atomically write user_data/{device_id}/layout.json and images."""

        layout = self.build()
        self.output_root.mkdir(parents=True, exist_ok=True)
        final_dir = self.output_root / self.device_id
        tmp_dir = self.output_root / f".{self.device_id}.tmp-{uuid4().hex[:8]}"
        backup_dir = self.output_root / f".{self.device_id}.bak-{uuid4().hex[:8]}"

        try:
            self._write_to(tmp_dir, layout)
            if final_dir.exists():
                final_dir.replace(backup_dir)
            tmp_dir.replace(final_dir)
        except Exception:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            if backup_dir.exists() and not final_dir.exists():
                backup_dir.replace(final_dir)
            raise
        else:
            shutil.rmtree(backup_dir, ignore_errors=True)
        return final_dir

    def _build_element(
        self,
        item: CalibrationItem,
        native_roi: Rect,
        *,
        ocr_expand: int = 0,
        variants: list[str] | None = None,
    ) -> LayoutElement:
        item.validate()
        if native_roi.is_empty():
            raise ValueError(f"calibration item {item.id} requires non-empty roi")
        image = _image_path_for(item)
        variant_paths = [
            f"image/{variant}.png" for variant in variants or []
        ]
        return LayoutElement(
            id=item.id,
            category=item.category,
            native=native_roi,
            maa720p=self.transformer.rect_to_maa720(native_roi, expand=ocr_expand),
            image=image,
            variants=variant_paths,
        )

    def _write_to(self, target_dir: Path, layout: CalibrationLayout) -> None:
        image_dir = target_dir / "image"
        image_dir.mkdir(parents=True)
        for relative_path, image_bytes in self._images.items():
            path = target_dir / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(image_bytes)
        layout_path = target_dir / "layout.json"
        layout_path.write_text(
            json.dumps(layout.to_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


def _identity_scaler(
    image_bytes: bytes, transformer: CoordinateTransformer
) -> bytes:
    if transformer.scale_ratio != 1.0:
        raise RuntimeError(
            "template_scaler is required when native height differs from 720"
        )
    return image_bytes


def _image_path_for(item: CalibrationItem) -> str | None:
    if item.category != "template":
        return None
    if not item.reference_image:
        return None
    return f"image/{item.reference_image}"


def _rect_to_dict(rect: Rect) -> dict[str, int]:
    return {
        "x": round(rect.x),
        "y": round(rect.y),
        "w": round(rect.width),
        "h": round(rect.height),
    }


def _set_nested(
    overrides: dict[str, object], node: str, dotted_field: str, value: object
) -> None:
    current = overrides.setdefault(node, {})
    if not isinstance(current, dict):
        raise ValueError(f"pipeline override node {node} is not a mapping")
    parts = dotted_field.split(".")
    for part in parts[:-1]:
        nested = current.setdefault(part, {})
        if not isinstance(nested, dict):
            raise ValueError(f"pipeline override field {dotted_field} conflicts")
        current = nested
    current[parts[-1]] = value
