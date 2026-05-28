# Asset Sources

Reference images and screenshots may be derived from upstream GPL-3.0 projects,
but every committed asset must remain traceable.

## Approved Upstreams

The current approved upstreams are recorded in `reference/source_index.json`:

- `alas`: AzurLaneAutoScript, GPL-3.0.
- `azurpilot`: AzurPilot, GPL-3.0.

When adding another upstream, add it to the index before copying or adapting
assets from it.

## Required Records

Every reference template, screenshot, anchor file, pipeline fragment, or derived
metadata entry should have a matching `assets` record in
`reference/source_index.json`.

Use these statuses:

- `placeholder`: planned asset; no binary asset has been committed yet.
- `copied`: copied directly from an upstream path.
- `modified`: adapted from an upstream path.
- `derived`: created locally or derived from behavior/coordinates rather than a
  copied file.

For `copied` and `modified` assets, `upstream` and `source_path` are mandatory.
For locally created assets, use `derived` and explain the origin in `notes`.

## Validation

Run the normal validation command:

```powershell
python tools/validate_pipeline.py
```

This validates the source index along with the interface, calibration manifest,
and pipeline JSON.
