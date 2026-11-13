---
name: bonsai-status
description: "Read-only status checks for a running Podman Bonsai worker stack: container health, live task slots, per-issue progress and GitHub approval state. Read-only; never restart, stop or upgrade."
---

# Bonsai worker status (read-only)

Use this to answer "is the worker healthy?", "how many tasks are running?",
"which slots are taken?" without disturbing anything. For lifecycle
operations (restart/upgrade) use `bonsai-containers`; for dispatching tasks
use `bonsai-ci` for scoped test/documentation handoffs.

## Where the stack runs

Workers live inside the WSL distro `podman-machine-default`, **not** on the
Windows host. Prefix commands with:

```bash
wsl -d podman-machine-default -e sh -c 'export PODMAN_IGNORE_CGROUPSV1_WARNING=1; ...'
```

The lifecycle CLI (`.agents/tools/containers.py`) rejects Podman hosts, so it cannot
be used here — everything below is manual inspection via `podman`.

## 1. Container health

```bash
podman ps --format "{{.Names}}|{{.Image}}|{{.Status}}"
podman inspect --format "Status={{.State.Status}} Pid={{.State.Pid}} OOM={{.State.OOMKilled}}" <container>
```

Typical containers: `bonsai-worker`, `bonsai-evals-worker`, `bonsai-ui-worker`
(all from `localhost/bonsai-worker:<release>` images), plus many stopped
`bonsai-*-before-*` / `-rollback-*` containers — those are pre-upgrade
backups, normal to keep. No container healthchecks are defined
(`Health=none` is expected). `podman stats`/`top` fail under rootless
cgroups-v1; use `podman exec` instead.

These are historical names/layouts, not a current inventory. For this workspace,
select the installation bound to `xaime-vp/constant-integration-ui` and substitute
its verified container name in all examples below. Prefer connected GitHub tools
for issue/PR reads; `gh` examples are a fallback.

## 2. Live task slots (per worker)

Processes inside a container are hidden by the PID namespace, so enumerate
them via `/proc` *inside* the container:

```bash
podman exec bonsai-worker sh -c \
  "for p in /proc/[0-9]*; do c=\$(tr '\\0' ' ' < \$p/cmdline 2>/dev/null); \
   [ -n \"\$c\" ] && echo \"\$c\"; done" \
  | grep -E 'task_process|pi |check.py'
```

Interpretation:
- A live `task_process` launcher is a candidate slot occupant; correlate its
  task key and recorded slot with current process/state evidence. Automatic PR
  reviews can also occupy shared slots without an issue implementation.
- A `pi` process shows execution, not successful generation or delivery.
- A protected check process belongs to its existing task, not a second slot.
- No matches is an observation, not confirmed stop or proof of safe admission.

Cross-check slot occupancy with recorded executions:

```bash
podman exec bonsai-worker sh -c \
  "ls -lt --time-style=+%F_%T /var/lib/bonsaiworker/private/executions | head -6"
```

Each entry has a `process.json` (`pid`, `slot`) and `config.json`. Verify a
recorded PID is still alive with `[ -d /proc/<pid> ]` inside the container;
workspace dirs persist after completion (evidence) — their presence alone
does not mean the task is running.

Read the selected installation's current `max_concurrent_tasks`; historical
execution snapshots can differ. Current source accepts 1/2/3 shared slots and a
missing field retains one. Main and UI workers have separate bindings and limits.
Read only needed configuration fields, including enabled profiles and the
`automatic_pr_reviews` opt-in; source defaults do not establish installed state.

## 3. Cheap host-level count (optional)

`.agents/tools/bonsai_process_count.py` in the workspace root counts launcher processes on any
host (psutil, PowerShell or pgrep fallback). Run it inside the distro from the workspace root:

```bash
wsl -d podman-machine-default -e sh -c \
  'python3 .agents/tools/bonsai_process_count.py --verbose'
```

Compare counts against the current inventory, not a historical expected total.
The counter cannot see inside
containers (never use it to count tasks), and it classifies its own
invocation as "ui" if the command line mentions `bonsai-ui` — run it from a
neutral path or ignore the self-match.

## 4. GitHub side (approvals and dispatch state)

```bash
gh issue list -R xaime-vp/constant-integration-ui --state open --json number,title,labels,comments
gh issue view <N> -R xaime-vp/constant-integration-ui --json comments,labels
```

- `ready` plus exactly one supported matching implementation label
  (`agent:test-specialist` or `agent:documentation` on current source) expresses
  readiness only. With no owner approval it is not executable. Generalist/tests
  are retired source routes; verify sealed compatibility.
- Legacy envelopes need current standalone owner `/approve-agent`; prepared prose
  issues need the exact `/approve-agent <full-digest>` after sealing and the final
  edit. `/prepare-agent` authorizes research only. Check revision, revocation,
  consumption, source, scope, parent-PR and stop/reservation evidence; labels or
  a comment alone do not prove admission. See [preparation](../../docs/free-form-issues.md).
- Issues without `ready` (or with `blocked`) are proposals — do not dispatch
  or label them ready without verification.

Test-specialist delivery includes protected checks and embedded read-only review;
documentation has protected checks and no embedded model verdict. The separate
trusted-opt-in PR Reviewer publishes commit-bound advisory `COMMENT` reviews and
runs no checks or repairs. These are distinct observations.

New automatic-review records permit three total attempts with 30/60-second delays
only after eligible pre-launch failures. Already marked legacy fetch recovery
keeps its pinned 60-second contract. Unknown/post-launch/publication evidence
blocks replay; do not reset budgets. See the [retry and export reference](../bonsai-ci/references/runtime-and-issue.md#automatic-commit-reviews-and-telemetry).
Exported heartbeats are snapshots, not liveness; absent role/cost/capacity evidence
stays unknown. Neither UI capability flags nor history can authorize worker actions.

## Boundaries

- Read-only: never restart, stop, kill, upgrade or "help" a busy worker while
  tasks are in flight (match container names to `private/executions` first).
- Never post owner request/approval commands; present the route-appropriate exact
  command only after the concrete issue/proposal is ready.
- A running launcher/listener is not proof of model generation, PR delivery
  or CI success — verify on GitHub before claiming end-to-end completion.
- Do not delete stopped backup containers, worktrees or execution records.
- Protect secrets: never dump config tokens or full environments.
