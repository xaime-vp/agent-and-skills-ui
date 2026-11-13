---
name: bonsai-containers
description: "Inspect, verify, restart or upgrade a Bonsai container installation using the lifecycle CLI. Initial setup and unsupported engines use deployment references. GitHub issues and approvals are separate."
---

Support the [root developer](../../../AGENTS.md) for requested installation work.
Keep `references/` alongside `SKILL.md`. The source checkout is
`constant-integration/`; the workspace `tools/containers.py` launcher delegates
to its original CLI. Reading this skill does not start or install a worker.

# Bonsai container lifecycle

Use `python tools/containers.py --json --installation NAME ...` from Linux or
WSL, with a private registry on the Linux filesystem. See
[CLI operations](../../../constant-integration/docs/CONTAINER_LIFECYCLE.md) for registration,
supported engines, outputs and recovery.

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
