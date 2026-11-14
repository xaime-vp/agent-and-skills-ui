# Workspace tools

Run these from the workspace root with Python 3.12+ (`py -3` on Windows):

```powershell
py -3 .pi/tools/bonsai_process_count.py --verbose
py -3 .pi/tools/validate_task.py --repository xaime-vp/constant-integration-ui --body-file path/to/issue.md --platform-root path/to/constant-integration
```

`bonsai_process_count.py` counts host-level `bonsai` and `bonsai-ui` launcher processes without inspecting inside containers; see the `.pi/skills/bonsai-status/` skill for live container/slot inspection.

`.pi/tools/validate_task.py` parses a legacy executable issue envelope against a selected platform source checkout. It defaults to `constant-integration/` at the workspace root; pass `--platform-root` to use another checkout. A successful parse proves only schema validity, not installed compatibility, approval or protected-check configuration.

`check.py` and `containers.py` are optional platform launchers. They expect a sibling `constant-integration/` checkout and simply run that checkout's own tools with the correct working directory. They have no effect unless that platform source checkout exists.

This validator accepts legacy executable envelopes only. Free-form prose issues follow the separate [preparation workflow](../docs/free-form-issues.md).

Keep private env files, MCP configs and worker state outside Git.
