---
name: bonsai-containers
description: "Inspect, verify, restart or upgrade a Bonsai container installation using the lifecycle CLI. Initial setup and unsupported engines use deployment references. GitHub issues and approvals are separate."
---

Support the [root developer](../../../AGENTS.md) for requested installation work.
Keep `references/` alongside `SKILL.md`. The source checkout is
`constant-integration/`; the workspace `.pi/tools/containers.py` launcher delegates
to its original CLI. Reading this skill does not start or install a worker.

# Bonsai container lifecycle

Use `python .pi/tools/containers.py --json --installation NAME ...` from Linux or
WSL, with a private registry on the Linux filesystem. See
[CLI operations](https://github.com/xaime-vp/constant-integration/blob/main/docs/CONTAINER_LIFECYCLE.md) for registration,
supported engines, outputs and recovery.

On Windows with Podman running inside WSL (`podman-machine-default`), use
[scripts/podman_wsl.py](scripts/podman_wsl.py) from the workspace root:

```sh
py -3 .pi/skills/bonsai-containers/scripts/podman_wsl.py inspect
py -3 .pi/skills/bonsai-containers/scripts/podman_wsl.py task-status bonsai-ui-worker --issue 204
py -3 .pi/skills/bonsai-containers/scripts/podman_wsl.py logs bonsai-ui-worker --controller --tail 50
py -3 .pi/skills/bonsai-containers/scripts/podman_wsl.py build --check
py -3 .pi/skills/bonsai-containers/scripts/podman_wsl.py stop bonsai-ui-worker --backup-suffix 20f8bf5
py -3 .pi/skills/bonsai-containers/scripts/podman_wsl.py relaunch bonsai-ui-worker
py -3 .pi/skills/bonsai-containers/scripts/podman_wsl.py upgrade bonsai-ui-worker --start
py -3 .pi/skills/bonsai-containers/scripts/podman_wsl.py action bonsai-ui-worker inspect-preparation KEY
```

- `podman_wsl.py` checks `/proc` for active `task_process`/`pi`/`check.py` work before stopping (`--force` overrides), backs up the previous container as `<container>-before-<suffix>`, preserves `/var/lib/bonsaiworker` volume mounts and `BONSAI_*` settings without exposing secrets, and refuses `prepare-issue` while the target worker is still running.
- Use `upgrade` (not `relaunch`) whenever you want the volume's sealed release (`/var/lib/bonsaiworker/config.json` `app_root`/`release_root`) updated from the new image via `prepare` + `install`; `upgrade` leaves the container stopped unless `--start` is passed.

For UI handoffs, verify the selected container is bound to
`xaime-vp/constant-integration-ui`. Read only the needed sealed configuration
fields (`release_root`, `enabled_profiles`, `max_concurrent_tasks` and
`automatic_pr_reviews`) without exposing credentials. Current source supports
test-specialist/documentation routes and 1/2/3 shared slots; old installations can
differ. An environment edit does not install a new profile. Preserve the automatic
PR Reviewer setting during lifecycle work; it is off by default. Role preparation
does not authorize an upgrade, stop, restart or enabling reviews.

1. Identify **restart** (same image/release, no migration), **recreation** (new
   container, preserved settings/volume), or **upgrade** (pinned source build,
   checks, backup, install/migration and recreation).
2. Run `inspect` for the selected installation; `verify` checks actual readiness.
   Stop on ambiguity, drift, active/unknown work, competing listeners or
   unconfirmed termination. The checkout branch is not the installed release.
3. Run the authorized operation: `restart`, or `upgrade --revision COMMIT`.
   Add `--start` only when startup is authorized: it can execute approved issues.
   Upgrade otherwise leaves the installation stopped. Never silently upgrade a
   restart request or migrate `docker run` to Compose.
4. For failure/interruption, use `operation-status ID`, then
   `logs ID --failed --tail 80`. Resume the **same** operation with
   `upgrade --operation ID` (or `restart --operation ID`). Read
   [exceptional deployment details](references/deployment.md) only for initial
   setup, unsupported engines/layouts or unexpected drift.
5. Report revision, checks, preservation outcomes, readiness and blockers
   concisely. A listener/relay is not model generation or issue-to-PR delivery.

Never change credentials, target binding, capabilities, checks or approval policy
incidentally. Preserve consumed approvals, unknown tasks, releases, worktrees,
checkpoints and evidence. Never clear state, declare stop from silence, start a
second listener, auto-merge or promise automatic schema rollback.

Keep issue editing, `/approve-agent`, handoff and PR repair outside deployment.
Use the workspace `bonsai-ci` skill for a separately requested task handoff; never post
approval for the owner. Loading this skill does not authorize startup or upgrade.
