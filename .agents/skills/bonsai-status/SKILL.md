---
name: bonsai-status
description: "Read-only status checks for a running Podman Bonsai worker stack: container health, live task slots, per-issue progress and GitHub approval state. Read-only; never restart, stop or upgrade."
---

# Bonsai worker status (read-only)

Use this to answer "is the worker healthy?", "how many tasks are running?",
"which slots are taken?" without disturbing anything. For lifecycle
operations (restart/upgrade) use `bonsai-containers`; for dispatching tasks
use `delegate-to-deepseek`.

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
- `task_process ... --task issue-N-approval-...` = one live task, one slot.
- A bare `pi` process = the agent is actively working.
- `python .agents/tools/check.py` = a check run inside the current task, not a second
  task.
- No matches = worker is idle between polls.

Cross-check slot occupancy with recorded executions:

```bash
podman exec bonsai-worker sh -c \
  "ls -lt --time-style=+%F_%T /var/lib/bonsaiworker/private/executions | head -6"
```

Each entry has a `process.json` (`pid`, `slot`) and `config.json`. Verify a
recorded PID is still alive with `[ -d /proc/<pid> ]` inside the container;
workspace dirs persist after completion (evidence) — their presence alone
does not mean the task is running.

Slot limit: read `max_concurrent_tasks` from any execution `config.json`
(main and UI workers are separate installations with separate limits;
current install: 2 each).

## 3. Cheap host-level count (optional)

`.agents/tools/bonsai_process_count.py` in the workspace root counts launcher processes on any
host (psutil, PowerShell or pgrep fallback). Run it inside the distro from the workspace root:

```bash
wsl -d podman-machine-default -e sh -c \
  'python3 .agents/tools/bonsai_process_count.py --verbose'
```

Expected on this stack: 3 "worker" launchers (one per container) plus one
"ui" match (the UI container's `conmon`). Caveats: it cannot see inside
containers (never use it to count tasks), and it classifies its own
invocation as "ui" if the command line mentions `bonsai-ui` — run it from a
neutral path or ignore the self-match.

## 4. GitHub side (approvals and dispatch state)

```bash
gh issue list -R xaime-vp/constant-integration --state open --json number,title,labels,comments
gh issue view <N> -R xaime-vp/constant-integration --json comments,labels
```

- `ready` + `agent:generalist` labels with **no comments** = dispatchable,
  not yet approved.
- A standalone `/approve-agent` comment from the owner (`xaime-vp`) = the
  worker may pick it up; confirm a matching `issue-N-approval-*` entry
  appeared in `private/executions/`.
- Issues without `ready` (or with `blocked`) are proposals — do not dispatch
  or label them ready without verification.

## Boundaries

- Read-only: never restart, stop, kill, upgrade or "help" a busy worker while
  tasks are in flight (match container names to `private/executions` first).
- Never post `/approve-agent` (or any approval) on the owner's behalf; give
  the owner the exact `gh issue comment ... --body "/approve-agent"` command
  instead.
- A running launcher/listener is not proof of model generation, PR delivery
  or CI success — verify on GitHub before claiming end-to-end completion.
- Do not delete stopped backup containers, worktrees or execution records.
- Protect secrets: never dump config tokens or full environments.
