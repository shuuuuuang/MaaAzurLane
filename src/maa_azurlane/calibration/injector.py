from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from maa_azurlane.calibration.layout import CalibrationLayout
from maa_azurlane.calibration.manifest import CalibrationManifest


class CalibrationResource(Protocol):
    """Subset of MaaResource used by calibration injection."""

    def override_image(self, name: str, data: bytes) -> object:
        """Override one image resource by Maa image namespace path."""

    def override_pipeline(self, pipeline: str) -> object:
        """Override pipeline JSON with calibrated ROI/template fields."""


@dataclass(frozen=True)
class InjectionResult:
    """Summary of user calibration data injected into a Maa resource."""

    images: list[str] = field(default_factory=list)
    pipeline_nodes: list[str] = field(default_factory=list)
    missing_images: list[str] = field(default_factory=list)

    @property
    def injected_anything(self) -> bool:
        return bool(self.images or self.pipeline_nodes)


class CalibrationInjector:
    """Inject user calibration images and pipeline overrides into MaaResource."""

    def __init__(self, manifest: CalibrationManifest) -> None:
        self.manifest = manifest

    def inject(
        self,
        resource: CalibrationResource,
        layout: CalibrationLayout,
        layout_dir: Path | str,
        *,
        strict: bool = True,
    ) -> InjectionResult:
        layout_path = Path(layout_dir)
        image_root = layout_path / "image"
        injected_images: list[str] = []
        missing_images: list[str] = []

        for image_name in _iter_image_names(layout):
            image_path = image_root / image_name
            if not image_path.exists():
                missing_images.append(image_name)
                continue
            resource.override_image(image_name, image_path.read_bytes())
            injected_images.append(image_name)

        if strict and missing_images:
            missing = ", ".join(missing_images)
            raise FileNotFoundError(f"missing calibrated image(s): {missing}")

        pipeline_overrides = layout.build_pipeline_overrides(self.manifest)
        if pipeline_overrides:
            resource.override_pipeline(
                json.dumps(pipeline_overrides, ensure_ascii=False)
            )

        return InjectionResult(
            images=injected_images,
            pipeline_nodes=sorted(pipeline_overrides),
            missing_images=missing_images,
        )


def _iter_image_names(layout: CalibrationLayout) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for element in layout.elements.values():
        for name in [element.image, *element.variants]:
            if name and name not in seen:
                seen.add(name)
                names.append(name)
    return names
