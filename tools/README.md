# Workspace tools

Run these from the workspace root with Python 3.12+ (`py -3` on Windows):

```powershell
py -3 tools/check.py --component orchestrator
py -3 tools/check.py --component worker
py -3 tools/containers.py --help
py -3 tools/validate_task.py --repository xaime-vp/constant-integration --body-file path/to/issue.md
```

`check.py` and `containers.py` launch the dedicated checkout's originals with their expected imports and working directory. Keep the checkout's `tools/` intact: container packaging, platform imports and isolated E2E fixtures depend on those paths. E2E probes remain there and should be selected deliberately using the platform CI guide.

`validate_task.py` was relocated from the retired `delegate-to-deepseek` bundle. It defaults to the sibling `constant-integration/` checkout and accepts `--platform-root` to validate against another source revision. It only parses an issue offline; success proves neither installed compatibility nor approval, readiness or protected-check configuration. Set the installed timeout ceiling with `--max-timeout-seconds` when applicable.

Keep private env files and worker state outside Git. A lifecycle action that starts or upgrades an installation is an operational change; loading these tools does not authorize it.
