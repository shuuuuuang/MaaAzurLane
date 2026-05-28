# Dataset Guidelines

Resolution support must be driven by screenshots, not assumptions.

## Naming

Use descriptive names:

```text
home_cn_1920x1080_mumu12_001.png
commission_cn_2400x1080_android_001.png
research_cn_2048x1536_ipad_001.png
```

## Metadata

Record:

- Page name.
- Server and language.
- Device or emulator.
- Screenshot resolution.
- Game content region if known.
- Important anchors and OCR regions.

Each screenshot should have a JSON sidecar with the same base name:

```text
home_cn_2400x1080_mumu12_001.png
home_cn_2400x1080_mumu12_001.json
```

Minimal metadata:

```json
{
  "schema_version": 1,
  "image": "home_cn_2400x1080_mumu12_001.png",
  "page": "home",
  "server": "cn",
  "language": "zh-CN",
  "device": "Windows",
  "emulator": "MuMu 12",
  "screenshot_size": {
    "width": 2400,
    "height": 1080
  },
  "game_region": {
    "x": 240,
    "y": 0,
    "width": 1920,
    "height": 1080
  },
  "tags": [
    "home",
    "20:9"
  ],
  "notes": ""
}
```

Validate metadata without requiring the image file:

```powershell
python tools/replay_screenshot.py --metadata-only
```

Validate metadata and require image files:

```powershell
python tools/replay_screenshot.py tests/screenshots
```

## Privacy

Contributors should remove or mask account-private information before sharing
screenshots publicly.

## Upstream Assets

Screenshots or templates adapted from AzurLaneAutoScript or AzurPilot must be
registered in `reference/source_index.json`. See
[asset-sources.md](asset-sources.md) for the required upstream, license, and
source path fields.
