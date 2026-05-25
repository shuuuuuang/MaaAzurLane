# Architecture

MaaAzurLane uses MaaFramework as the automation runtime and separates work into
four layers:

1. Maa pipeline tasks for stable UI flows.
2. Python extensions for recognition, action, scheduling, OCR post-processing,
   emulator integration, and domain logic.
3. Resource packs for templates, masks, anchors, models, and per-server assets.
4. Screenshot replay and regression tests for resolution-sensitive behavior.

## Design Rules

- Task logic should not directly depend on a single screenshot resolution.
- UI targets should be resolved by anchors, OCR, template matching, feature
  matching, or layout profiles before falling back to normalized coordinates.
- Daily tasks, Operation Siren, events, emulator management, and MCP integration
  should be independently testable modules.

## Target Modules

- `layout`: content-region detection and coordinate mapping.
- `recognizer`: custom recognition strategies.
- `action`: custom actions that Maa pipeline can call.
- `scheduler`: task queue, cooldowns, priorities, and retry policy.
- `emulator`: ADB and emulator lifecycle management.
- `ocr`: OCR adapters, custom models, and post-processing.
- `domain`: Azur Lane concepts such as resources, fleets, tasks, and maps.
