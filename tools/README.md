# Client workspace tools

Generated adapters forward to the selected application/runtime checkout. Run
Python 3.12+ from this workspace. Use `tools/harness_check.py` for workspace
contracts and `tools/check_harness_export.py` for generated-resource drift.

Lifecycle operations use `tools/containers.py --platform-root PATH --json
--installation NAME inspect|stop|restart|upgrade`. Global options precede the
action; upgrade requires an exact `--revision COMMIT` and leaves the listener
stopped without explicit `--start`. Use a private Linux registry and Linux/WSL
Python; Windows can select `--wsl-distro NAME`. Stop requires the runtime source
change adding managed stop. Older source fails without operating.

The old docker-worker path is an alias for managed arguments; legacy force,
relaunch and standalone build flags are unsupported. See the runtime's
[lifecycle guide](https://github.com/xaime-vp/constant-integration/blob/main/docs/CONTAINER_LIFECYCLE.md).
