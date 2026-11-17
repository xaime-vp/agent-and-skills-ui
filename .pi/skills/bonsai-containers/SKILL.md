---
name: bonsai-containers
description: Inspect, stop, restart or upgrade a registered Bonsai installation through the runtime-owned managed lifecycle CLI. Use for authorized worker operations; verify installation and host compatibility first.
---

# Managed worker lifecycle

Follow the [root contract](../../../AGENTS.md). Operations are implemented once in
the trusted runtime checkout's `tools/containers.py`. Workspace paths are thin
adapters; reading this skill does not authorize an operation.

Use Linux/WSL Python and a registered installation with a private Linux registry.
The managed CLI supports native Docker Engine over a local Unix socket; unsupported
hosts, remote engines, Podman and Compose-owned installations remain blocked.
Read [runtime lifecycle guidance](https://github.com/xaime-vp/constant-integration/blob/main/docs/CONTAINER_LIFECYCLE.md)
for registration, supported hosts, operation journals, backups and recovery.

Run from the workspace, selecting the trusted source checkout if necessary:

```sh
python tools/containers.py --platform-root /trusted/constant-integration --json --installation platform inspect
python tools/containers.py --platform-root /trusted/constant-integration --json --installation platform stop
python tools/containers.py --platform-root /trusted/constant-integration --json --installation platform restart
python tools/containers.py --platform-root /trusted/constant-integration --json --installation platform upgrade --revision FULL_COMMIT
python tools/containers.py --platform-root /trusted/constant-integration --json logs OPERATION_ID --tail 40
```

On Windows add `--wsl-distro NAME` and select the Windows path to the runtime
checkout. Keep `--state-dir`, when supplied, a private Linux registry path.
Global runtime options precede the subcommand.

- Inspect before an operation and confirm the bound target, installed revision,
  configuration and active/unknown work. Inspection failure aborts mutation.
- `stop` leaves the same container and release stopped; `restart` starts that same
  release. Neither installs an upgrade. Both refuse active/unknown work; there is
  no force bypass. Stop requires the source revision adding managed stop support.
- `upgrade --revision FULL_COMMIT` builds/checks the pinned source, preserves
  configuration and state through the runtime's journaled process, and leaves the
  replacement stopped. Add `--start` only when listener startup is authorized.
- Resume with the same action and `--operation ID`; recorded parameters govern
  recovery. Never silently retry as a new operation or infer termination from a
  stale record. Preserve private state, artifacts and recorded reservations.
- The Pi tools retain `bonsai_worker_status`, `bonsai_stop_worker` and
  `bonsai_worker_events` (now managed operation logs), and add explicit restart
  and upgrade tools. All require explicit identities; mutation tools start inactive
  and require interactive confirmation. Headless use follows the authorized CLI.

Legacy `tools/docker_worker.py` and the skill script are path aliases for the same
managed CLI. Legacy `relaunch`, standalone `build`, task-event options, container
defaults and `--force` are retired; they are not silently translated into upgrades.
Use the runtime's documented diagnostic/export tools for task events. A successful
operation does not prove task delivery, current target CI or owner acceptance.
