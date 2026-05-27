# Milestone Review

This review aligns GitHub milestones and repository documentation with the
local `DESIGN.md` phase plan.

## Feasibility

The phase plan is feasible if calibration remains the primary resolution
strategy. The project should not rely on one global auto-detection algorithm to
support every phone layout. Instead, the implementation should use:

- Developer-maintained reference manifests.
- User-side calibration.
- NativeSpace to Maa720Space conversion.
- Runtime image and pipeline overrides.
- Calibration health checks.

## Required Scope Corrections

### Phase 0

`DESIGN.md` Phase 0 mixes infrastructure, OCR, ADB, reference templates,
calibration UI, and coordinate math. That is too broad for one execution unit.

Correction: keep P0 focused on contracts and foundations. UI and full
calibration generation move to P1.

### Phase 1

Phase 1 is feasible but must produce a narrow proof:

- Main page navigation.
- Calibrated button templates.
- Generated layout JSON.
- Runtime override injection.
- Validation on 1280x720, 1920x1080, and 2400x1080.

Community calibration sharing should stay exploratory until the local
calibration format is stable.

### Phase 2

Collection tasks are the right first gameplay milestone. They are lower risk
than battle automation and prove immediate value.

Correction: scheduler work starts here but remains basic. Advanced insertion,
resource thresholds, and recovery move to P4.

### Phase 3 and Phase 4

The original plan separates sortie/battle and daily tasks. This is reasonable,
but scheduler hardening belongs with daily task mixing, not the first battle
prototype.

### Phase 5

Operation Siren must remain a separate milestone. It needs custom map scan,
navigation, and state handling, so folding it into normal sortie work would
hide risk.

### Phase 6

AzurPilot advanced features are feasible only after P5. They should be
opt-in and risk-labelled because several actions affect resources, equipment,
or long-running strategy.

### Phase 7

Multi-server support, regression, and documentation are continuous work, but
they still need a milestone because they define public readiness.

## GitHub Milestone Mapping

The previous M0-M9 milestone list is replaced by P0-P7:

- P0: Foundation and Calibration Contract.
- P1: Calibration System and Core Navigation.
- P2: Collection Tasks and Basic Scheduler.
- P3: Sortie and Battle Core.
- P4: Daily Tasks and Scheduler Hardening.
- P5: Operation Siren.
- P6: AzurPilot Advanced Features and External Control.
- P7: Stability, Multi-server, and Ecosystem.

The older standalone topics are folded into these phases:

- OCR and models: P0/P1 for placement and first use, P7 for regression.
- Emulator and multi-instance: P0 for controller setup, P7 for stable support.
- MCP: P6.
- User experience and release: P1 for calibration UI, P7 for public release.
