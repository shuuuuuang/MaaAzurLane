# Migration from ALAS and AzurPilot

MaaAzurLane should learn from ALAS and AzurPilot, but the implementation should
be MaaFramework-native.

## Keep

- Mature task concepts.
- Long-running stability lessons.
- Recovery flows.
- Scheduling ideas.
- Multi-server experience.
- Operation Siren and event automation knowledge.

## Rebuild

- Fixed absolute-coordinate assumptions.
- Recognition code that cannot be replay-tested.
- Deeply coupled task and device logic.
- Runtime infrastructure already covered by MaaFramework.

## Target

The long-term feature target should be comparable to AzurPilot, while the
runtime architecture should remain aligned with MaaFramework.
