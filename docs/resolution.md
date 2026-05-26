# Resolution Strategy

MaaAzurLane targets mainstream phone, tablet, and emulator aspect ratios rather
than a single 1280x720 layout.

## Supported Targets

Required early targets:

- 1280x720
- 1920x1080
- 2340x1080
- 2400x1080
- 2532x1170
- 2560x1440
- 1920x1200
- 2048x1536

Recommended later targets:

- 2520x1080
- 3200x1440
- 2732x2048

## Core Idea

Automation should adapt to the game content region, not the outer device
screen. The runtime should:

1. Capture the full screen.
2. Detect the visible Azur Lane content region.
3. Resolve page anchors and target regions.
4. Map logical coordinates into the detected content region only as fallback.

## Layout Profile

A layout profile records:

- Screenshot size.
- Detected game content region.
- Detection source, such as `auto` or `manual`.

Profiles let the runtime reuse a previously detected region and make future
anchor detection cheaper and more stable.

## Anchors

Anchors describe stable UI targets in logical coordinates. They are not final
click coordinates by themselves. Runtime code should resolve an anchor through
OCR, template matching, feature matching, color checks, or manual fallback, then
map it into the current game content region.

Anchor definitions live under `resource/config/anchors`.

## Layout Levels

- L1: 16:9 multi-resolution support.
- L2: black-bar or border handling through content-region detection.
- L3: mainstream phone ratios through anchors and normalized safe areas.
- L4: tablet ratios through profiles and additional screenshot tests.

## Rule

No feature should be considered complete if it only works on one fixed absolute
coordinate layout.
