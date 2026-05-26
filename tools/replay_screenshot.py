from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    from maa_azurlane.dataset import ScreenshotMetadata

    parser = argparse.ArgumentParser(
        description="Validate replayable screenshot metadata files.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("tests/screenshots")],
        help="Metadata JSON files or directories to scan.",
    )
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Validate sidecar metadata without requiring image files to exist.",
    )
    args = parser.parse_args()

    metadata_paths = list(iter_metadata_paths(args.paths))
    if not metadata_paths:
        print("no screenshot metadata files found")
        return 0

    for path in metadata_paths:
        metadata = ScreenshotMetadata.load(path)
        image_path = metadata.image_path(path)
        if not args.metadata_only and not image_path.exists():
            raise FileNotFoundError(f"missing screenshot image: {image_path}")
        print(
            "valid replay case: "
            f"{path} page={metadata.page} "
            f"size={metadata.screenshot_size.width}x{metadata.screenshot_size.height}"
        )

    return 0


def iter_metadata_paths(paths: list[Path]) -> list[Path]:
    metadata_paths: list[Path] = []
    for path in paths:
        if path.is_file():
            metadata_paths.append(path)
        elif path.is_dir():
            metadata_paths.extend(sorted(path.glob("**/*.json")))
    return metadata_paths


if __name__ == "__main__":
    raise SystemExit(main())
