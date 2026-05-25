# MaaAzurLane

MaaAzurLane is a MaaFramework-based automation project for Azur Lane.

The project goal is to rebuild the useful ideas from AzurLaneAutoScript and
AzurPilot on top of the Maa ecosystem, while fixing one of the largest user
pain points: automation that is tightly bound to a single 1280x720 layout.

## Goals

- Use MaaFramework as the automation foundation.
- Target feature coverage comparable to AzurPilot in the long term.
- Support mainstream phone, tablet, and emulator aspect ratios.
- Prefer content-region detection, anchors, OCR, and normalized coordinates
  over fixed absolute coordinates.
- Keep task logic testable through screenshot replay and regression datasets.

## Initial Scope

The first public milestone focuses on:

- MaaFramework project skeleton.
- Game launch and home-page recovery.
- Mainstream resolution adaptation prototype.
- Daily collection tasks such as commissions, research, dorm, academy, and
  daily rewards.

Large-scale Operation Siren automation, intelligent scheduling, MCP service,
custom OCR models, GPU inference, and emulator management are long-term goals.

## Status

This repository is in the planning and scaffolding stage.

## References

- [MaaFramework](https://github.com/MaaXYZ/MaaFramework)
- [AzurLaneAutoScript](https://github.com/LmeSzinc/AzurLaneAutoScript)
- [AzurPilot](https://github.com/wess09/AzurPilot)

## License

GPL-3.0-only. See [LICENSE](LICENSE).

## Disclaimer

This is an unofficial community project. It is not affiliated with, endorsed
by, or sponsored by the Azur Lane developers, publishers, MaaXYZ, ALAS, or
AzurPilot maintainers.
