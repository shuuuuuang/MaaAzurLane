# Roadmap

This roadmap follows the local `DESIGN.md` phase plan, with milestone scopes
adjusted so each phase has a clear engineering acceptance boundary.

## P0: Foundation and Calibration Contract

Goal: make the project loadable, testable, and aligned around the calibration
architecture before gameplay tasks expand.

- MaaFramework project skeleton and ProjectInterface.
- CI, validation tools, issue and PR workflow.
- Coordinate-space terminology and `CoordinateTransformer`.
- `reference/calibration.json` manifest schema.
- Initial reference template manifest entries.
- ADB/controller configuration draft.
- OCR model placement contract.
- Local development and validation documentation.

Acceptance:

- `interface.json`, pipeline JSON, and calibration manifests validate locally
  and in CI.
- Native-to-Maa720 coordinate conversion is covered for common resolutions.
- Calibration item IDs are explicitly mapped to pipeline references.

## P1: Calibration System and Core Navigation

Goal: prove the user-side calibration path on real navigation flows.

- Reference templates for common buttons.
- Calibration wizard prototype.
- `LayoutBuilder` for layout JSON generation.
- Template resize into Maa720Space.
- User calibration data injection through image and pipeline overrides.
- Main-page recognition and navigation pipeline.
- Cross-resolution validation for 1280x720, 1920x1080, and 2400x1080.
- Basic UI integration path, preferably MXU.

Acceptance:

- A calibrated device can return to the main page and navigate to key screens
  without fixed native-resolution coordinates.
- Calibration can be resumed or repeated without corrupting existing data.

## P2: Collection Tasks and Basic Scheduler

Goal: deliver the first practical automation value through low-risk collection
tasks.

- Commission collection and dispatch.
- Research collection and selection.
- Tactical class, dorm, meowfficer, guild, shop, build, and retire pipelines.
- Basic scheduler with cooldown and priority handling.
- Core Pack and Daily Pack calibration dependencies.

Acceptance:

- Users can run a daily collection loop from calibrated navigation data.
- Scheduler records next-run times and can resume after interruption.

## P3: Sortie and Battle Core

Goal: implement battle entry flows and the first generation of map navigation.

- Campaign and event entry pipelines.
- Fleet selection and morale checks.
- Basic map recognition and navigation custom modules.
- Emergency commission and repeat sortie support.
- Oil and resource gate checks.

Acceptance:

- A configured normal or event stage can be entered, completed, and repeated
  under resource and morale limits.

## P4: Daily Tasks and Scheduler Hardening

Goal: broaden daily gameplay coverage and make scheduling robust.

- Daily raids.
- Hard mode.
- Exercise.
- Submarine stages.
- War archives.
- Event daily tasks.
- Scheduler interruption, resource thresholds, and task insertion.

Acceptance:

- Daily task groups can be mixed with collection tasks without blocking or
  starving higher-priority work.

## P5: Operation Siren

Goal: make Operation Siren a first-class module.

- Operation Siren map scan and navigation custom modules.
- Daily Operation Siren tasks.
- Monthly reset progression.
- Hidden zones, abyssal zones, strongholds, and port supply flows.
- AP control and Operation Siren specific scheduler strategy.

Acceptance:

- Daily and monthly Operation Siren flows can run with recoverable navigation
  and state tracking.

## P6: AzurPilot Advanced Features and External Control

Goal: catch up with AzurPilot-inspired advanced automation and expose external
control surfaces.

- Island plan.
- Co-op and special event flows.
- Operation Siren advanced strategy such as Monte Carlo style planning.
- Equipment box dismantling.
- Corrosion 1 auto fleet planning.
- Siren research device support.
- Timed restart.
- MCP service.

Acceptance:

- Advanced modules are opt-in, risk-labelled, and externally observable.

## P7: Stability, Multi-server, and Ecosystem

Goal: prepare for public long-running use and community contribution.

- CN, EN, JP, and TW server adaptation.
- Multi-resolution regression test sets.
- `CalibrationHealth` and incremental recalibration.
- Community calibration sharing design.
- Documentation for MaaDebugger and MaaPipelineEditor workflows.
- Release channels and migration guides.

Acceptance:

- The project has repeatable regression coverage, health checks, and enough
  documentation for external contributors to extend modules safely.

## Calendar Target

- 2026 Q2: P0.
- 2026 Q3: P1 and P2.
- 2026 Q4: P3, P4, community calibration library, and v0.5 Alpha.
- 2027 Q1: P5, P6, and v0.8 Beta.
- 2027 Q2: P7 and v1.0.
