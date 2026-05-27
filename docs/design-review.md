# Design Review

This document records design corrections from the first architecture review of
`DESIGN.md`.

## Verdict

The device-side calibration strategy is feasible and should become the primary
resolution-adaptation path.

The previous content-region detection and anchor work remains useful, but it is
now auxiliary. The main path is:

1. Developer-maintained reference definitions.
2. User-side calibration on the actual device.
3. Conversion into MaaFramework's 720p-equivalent coordinate space.
4. Runtime image and pipeline overrides.
5. Calibration health checks.

## Coordinate Spaces

Do not use the ambiguous phrase "720p coordinates" in code or persisted data.
Use explicit names:

- `NativeSpace`: original screenshot and input coordinates.
- `Maa720Space`: MaaFramework's height-720 equivalent recognition space.
- `LogicalSpace`: project reference design coordinates, currently 1280x720.
- `ContentSpace`: detected game content region inside the native screenshot.

`Maa720Space` is not assumed to be 1280x720. Its width is derived from the
native aspect ratio:

```text
scale_ratio = native_height / 720
maa720_width = round(native_width / scale_ratio)
maa720_height = 720
```

If a future pipeline needs a fixed 1280x720 canvas, that must be represented as
a separate canonical space and tested explicitly.

## Pipeline Override Mapping

Calibration item IDs are not pipeline node names. A calibration item must carry
explicit `pipeline_refs` entries so the override builder knows which pipeline
node and field to patch.

Example:

```json
{
  "id": "main.btn_campaign",
  "pipeline_refs": [
    {
      "node": "MainCampaignButton",
      "field": "recognition.param.roi"
    }
  ]
}
```

## API Injection Layers

MaaFramework supports runtime overrides, but they should be used at the right
layer:

- Stable user calibration data: resource-level override.
- One-off task options: task-level `pipeline_override`.
- Custom runtime correction: context-level override.

## Calibration UX Constraint

The project must not require full calibration before first value. Calibration
should be grouped into packs:

- `core`: main page and commission, enough to prove automation value quickly.
- `daily`: research, dorm, academy, mission, and routine collection.
- `battle`: sortie, events, Operation Siren, and advanced navigation.

## Implementation Order

1. Coordinate transformer.
2. Calibration manifest schema.
3. Calibration item to pipeline override mapping.
4. Layout builder for JSON and ROI.
5. Template resize.
6. Calibration wizard UI.
7. Calibration health checks.
