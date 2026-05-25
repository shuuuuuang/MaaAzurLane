# Contributing

Thanks for helping build MaaAzurLane.

## Principles

- Prefer MaaFramework-native pipeline and extension patterns.
- Do not add new absolute-coordinate logic without a layout abstraction.
- Every task module should be testable with saved screenshots where practical.
- Keep server, language, emulator, and resolution assumptions explicit.
- Document the source of copied or adapted code, assets, and models.

## Pull Requests

Please include:

- What changed.
- Which task module is affected.
- Tested resolution and aspect ratio.
- Tested server or language.
- Tested emulator or device.
- Screenshots or logs for recognition-sensitive changes.

## Resolution Support

New task implementations should use:

- Game content-region detection.
- Anchor-based target resolution.
- OCR/template/feature recognition as appropriate.
- Normalized logical coordinates only as fallback.

PRs that only work on one fixed resolution may be rejected unless they are
clearly marked as prototypes.
