# Development

This document describes the baseline local development flow for MaaAzurLane.

## Requirements

- Git
- Python 3.11 or newer
- GitHub CLI, optional but recommended for issue and release management
- MaaFramework runtime, required once runnable pipelines are added
- ADB and an Android emulator or device, required once device integration starts

Windows is the first-class development platform during the early milestones.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e . pytest ruff
```

## Validation

Validate Maa pipeline JSON files:

```powershell
python tools/validate_pipeline.py
```

Run Python tests:

```powershell
python -m pytest
```

Run lint checks:

```powershell
python -m ruff check .
```

## Current Notes

- Pipeline files are placeholders until MaaFramework runtime integration is
  validated against real tasks.
- Resolution-sensitive code should be covered by offline screenshot replay
  tests whenever practical.
- Do not add task code that directly depends on absolute runtime coordinates.
