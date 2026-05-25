# Maa Project Interface

MaaAzurLane uses Maa ProjectInterface V2.

The project entry point is `interface.json`. It declares:

- `interface_version`: ProjectInterface version.
- `resource`: resource root directories used by MaaFramework.
- `controller`: supported controller types.
- `task`: user-visible tasks and their pipeline entry nodes.

## Current Tasks

- `Startup`: placeholder startup flow.
- `ReturnHome`: placeholder home recovery flow.
- `DailyBaseline`: placeholder daily task group entry.

## Notes

The current pipeline files are intentionally minimal. They exist to keep the
project loadable while the real recognition, action, and resolution layers are
implemented.

When adding a task:

1. Add or update the corresponding pipeline JSON under `resource/pipeline`.
2. Register the user-visible task in `interface.json`.
3. Keep the `entry` value aligned with the pipeline task node name.
4. Add validation or screenshot replay coverage when the task depends on
   recognition behavior.
