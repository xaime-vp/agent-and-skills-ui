---
name: bonsai-status
description: Inspect a registered UI-bound worker installation when the user requests worker status. Use the shared managed lifecycle adapter; do not infer liveness from saved UI history.
---

# UI-bound worker status

Use [the shared container skill](../bonsai-containers/SKILL.md) to inspect an
explicitly selected registered installation. Run the workspace `tools/containers.py`
adapter with `--installation NAME inspect` and the selected private Linux registry.
This developer-side operation is separate from UI application behavior. UI code
continues to read sanitized exports and must never read worker private state or
gain container control. Source support and saved observations do not prove liveness.
