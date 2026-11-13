#!/usr/bin/env python3
"""Helper for managing Bonsai worker Podman containers in WSL (podman-machine-default)."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_MACHINE = "podman-machine-default"
SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/-]*$")
SAFE_SUFFIX = re.compile(r"^[A-Za-z0-9._-]+$")
SAFE_BONSAI_KEYS = (
    "BONSAI_TARGET_REPOSITORY",
    "BONSAI_SOURCE_REVISION",
    "BONSAI_MAX_CONCURRENT_TASKS",
    "BONSAI_PI_RELEASE",
    "BONSAI_NODE",
)
ALLOWED_ACTIONS = ("once", "explain", "probe", "prepare-issue", "inspect-preparation")


def to_wsl_path(path: Path) -> str:
    resolved = str(path.resolve())
    match = re.match(r"^([A-Za-z]):[\\/](.*)$", resolved)
    if not match:
        return resolved.replace("\\", "/")
    drive = match.group(1).lower()
    rest = match.group(2).replace("\\", "/")
    return f"/mnt/{drive}/{rest}"


def validate_name(value: str, label: str) -> str:
    if not SAFE_NAME.match(value):
        raise SystemExit(f"Invalid {label}: {value!r}")
    return value


def validate_suffix(value: str) -> str:
    if not SAFE_SUFFIX.match(value):
        raise SystemExit(f"Invalid backup suffix: {value!r}")
    return value


def run_wsl(machine: str, argv: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    cmd = ["wsl", "-d", machine, "-e", *argv]
    env = os.environ.copy()
    env.setdefault("PODMAN_IGNORE_CGROUPSV1_WARNING", "1")
    return subprocess.run(
        cmd,
        env=env,
        text=True,
        capture_output=capture,
        check=False,
    )


def podman_inspect(machine: str, names: list[str]) -> list[dict]:
    res = run_wsl(machine, ["podman", "inspect", *names], capture=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr.strip() or f"podman inspect failed for {names}")
    return json.loads(res.stdout)


def extract_safe_env(env_list: list[str]) -> dict[str, str]:
    found: dict[str, str] = {}
    for item in env_list:
        if "=" not in item:
            continue
        k, v = item.split("=", 1)
        if k in SAFE_BONSAI_KEYS:
            found[k] = v
    return found


def active_worker_processes(machine: str, container: str) -> list[str]:
    script = (
        'for p in /proc/[0-9]*; do '
        'c=$(tr "\\0" " " < "$p/cmdline" 2>/dev/null || true); '
        '[ -n "$c" ] && echo "$c"; '
        "done"
    )
    res = run_wsl(machine, ["podman", "exec", container, "sh", "-c", script], capture=True)
    if res.returncode != 0:
        return []
    matches = []
    for line in res.stdout.splitlines():
        if re.search(r"task_process|pi |check\.py", line):
            matches.append(line.strip())
    return matches


def cmd_inspect(args: argparse.Namespace) -> int:
    if args.container:
        names = [validate_name(args.container, "container")]
    else:
        res = run_wsl(
            args.machine,
            ["podman", "ps", "-a", "--filter", "name=bonsai-", "--format", "{{.Names}}"],
            capture=True,
        )
        if res.returncode != 0:
            raise SystemExit(res.stderr.strip() or "Failed to list containers")
        names = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        if not names:
            print("No bonsai-* containers found.")
            return 0

    data = podman_inspect(args.machine, names)
    summary = []
    for item in data:
        name = item.get("Name", "").lstrip("/")
        status = item.get("State", {}).get("Status", "unknown")
        mounts = [
            f"{m.get('Name') or m.get('Source')}:{m.get('Destination')}"
            for m in item.get("Mounts", [])
        ]
        safe_env = extract_safe_env(item.get("Config", {}).get("Env", []))
        active = active_worker_processes(args.machine, name) if status == "running" else []
        summary.append(
            {
                "name": name,
                "status": status,
                "image": item.get("ImageName"),
                "restart_policy": item.get("HostConfig", {}).get("RestartPolicy", {}).get("Name"),
                "mounts": mounts,
                "env": safe_env,
                "active_processes": len(active),
            }
        )
    print(json.dumps(summary, indent=2))
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    if not (repo / "workers" / "bonsai" / "Dockerfile").is_file():
        raise SystemExit(f"Missing workers/bonsai/Dockerfile under {repo}")
    rev = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    short = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "--short=7", "HEAD"], text=True
    ).strip()
    tag = validate_name(args.tag or f"localhost/bonsai-worker:main-{short}", "image tag")
    repo_wsl = to_wsl_path(repo)

    print(f"Building {tag} from {repo_wsl} (revision {rev})...")
    build = run_wsl(
        args.machine,
        [
            "podman",
            "build",
            "-t",
            tag,
            "--build-arg",
            f"BONSAI_SOURCE_REVISION={rev}",
            "-f",
            f"{repo_wsl}/workers/bonsai/Dockerfile",
            repo_wsl,
        ],
    )
    if build.returncode != 0:
        return build.returncode
    if args.check:
        print(f"Running offline container check on {tag}...")
        chk = run_wsl(args.machine, ["podman", "run", "--rm", tag, "check"])
        return chk.returncode
    return 0


def stop_container(machine: str, container: str, backup_suffix: str | None, force: bool) -> None:
    exists = run_wsl(machine, ["podman", "container", "exists", container], capture=True)
    if exists.returncode != 0:
        raise SystemExit(f"Container not found: {container}")
    info = podman_inspect(machine, [container])[0]
    status = info.get("State", {}).get("Status")
    if status == "running":
        active = active_worker_processes(machine, container)
        if active and not force:
            joined = "\n".join(active)
            raise SystemExit(
                f"Refusing to stop {container}: active tasks detected (pass --force to override):\n{joined}"
            )
        print(f"Stopping {container}...")
        res = run_wsl(machine, ["podman", "stop", container])
        if res.returncode != 0:
            raise SystemExit(f"Failed to stop {container}")
    else:
        print(f"Container {container} is already {status}.")

    if backup_suffix:
        target = f"{container}-before-{backup_suffix}"
        print(f"Renaming {container} -> {target}")
        res = run_wsl(machine, ["podman", "rename", container, target])
        if res.returncode != 0:
            raise SystemExit(f"Failed to rename {container} -> {target}")


def cmd_stop(args: argparse.Namespace) -> int:
    container = validate_name(args.container, "container")
    suffix = validate_suffix(args.backup_suffix) if args.backup_suffix else None
    stop_container(args.machine, container, suffix, args.force)
    return 0


def cmd_relaunch(args: argparse.Namespace) -> int:
    container = validate_name(args.container, "container")
    info = podman_inspect(args.machine, [container])[0]
    safe_env = extract_safe_env(info.get("Config", {}).get("Env", []))
    target_repo = safe_env.get("BONSAI_TARGET_REPOSITORY")
    if not target_repo:
        raise SystemExit(f"Container {container} has no BONSAI_TARGET_REPOSITORY")
    mounts = info.get("Mounts", [])
    vol_mounts = [m for m in mounts if m.get("Destination") == "/var/lib/bonsaiworker"]
    if not vol_mounts:
        raise SystemExit(f"Container {container} has no /var/lib/bonsaiworker mount")
    vol_src = vol_mounts[0].get("Name") or vol_mounts[0].get("Source")
    if not vol_src:
        raise SystemExit(f"Could not determine volume source for {container}")
    restart_policy = (
        info.get("HostConfig", {}).get("RestartPolicy", {}).get("Name") or "unless-stopped"
    )
    max_tasks = safe_env.get("BONSAI_MAX_CONCURRENT_TASKS", "2")

    if args.image:
        image = validate_name(args.image, "image")
    else:
        repo = Path(args.repo).resolve()
        short = subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "--short=7", "HEAD"], text=True
        ).strip()
        image = f"localhost/bonsai-worker:main-{short}"

    suffix = validate_suffix(args.backup_suffix) if args.backup_suffix else image.split(":")[-1].replace("main-", "")
    stop_container(args.machine, container, suffix, args.force)

    print(f"Launching {container} with {image} (target={target_repo}, volume={vol_src})...")
    res = run_wsl(
        args.machine,
        [
            "podman",
            "run",
            "-d",
            "--name",
            container,
            "--restart",
            restart_policy,
            "-v",
            f"{vol_src}:/var/lib/bonsaiworker",
            "-e",
            f"BONSAI_TARGET_REPOSITORY={target_repo}",
            "-e",
            f"BONSAI_MAX_CONCURRENT_TASKS={max_tasks}",
            image,
            "run",
        ],
    )
    return res.returncode


def cmd_action(args: argparse.Namespace) -> int:
    container = validate_name(args.container, "container")
    action = args.action
    info = podman_inspect(args.machine, [container])[0]
    status = info.get("State", {}).get("Status")
    if action == "prepare-issue" and status == "running":
        raise SystemExit(
            f"Refusing prepare-issue while {container} is running; stop it first without --backup-suffix."
        )
    safe_env = extract_safe_env(info.get("Config", {}).get("Env", []))
    target_repo = safe_env.get("BONSAI_TARGET_REPOSITORY")
    if not target_repo:
        raise SystemExit(f"Container {container} has no BONSAI_TARGET_REPOSITORY")
    image = args.image or info.get("ImageName")
    if not image:
        raise SystemExit(f"Could not determine image for {container}")
    validate_name(image, "image")

    res = run_wsl(
        args.machine,
        [
            "podman",
            "run",
            "--rm",
            "--volumes-from",
            container,
            "-e",
            f"BONSAI_TARGET_REPOSITORY={target_repo}",
            image,
            action,
            *args.action_args,
        ],
    )
    return res.returncode


_ISSUE_STATUS_PY = r"""
import json
import sqlite3
import sys
from pathlib import Path

issue_num = int(sys.argv[1])
events_limit = int(sys.argv[2])
private = Path("/var/lib/bonsaiworker/private")
db_path = private / "state.db"

tasks_out = []
keys = []
if db_path.is_file():
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT key, issue, approval, status, updated_at, data FROM tasks WHERE issue = ? ORDER BY updated_at DESC",
        (issue_num,),
    ).fetchall()
    for row in rows:
        key = row["key"]
        keys.append(key)
        data = {}
        try:
            data = json.loads(row["data"] or "{}")
        except json.JSONDecodeError:
            pass
        events = [
            dict(ev)
            for ev in conn.execute(
                "SELECT id, status, reason, recorded_at FROM task_events WHERE key = ? ORDER BY id ASC",
                (key,),
            ).fetchall()
        ]
        res_dir = private / "results" / key
        checks = None
        checks_path = res_dir / "checks.json"
        if checks_path.is_file():
            try:
                checks = json.loads(checks_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                pass
        result_summary = None
        result_path = res_dir / "result.json"
        if result_path.is_file():
            try:
                r = json.loads(result_path.read_text(encoding="utf-8"))
                agent = r.get("agent") or {}
                review = r.get("review") or {}
                rev_proc = review.get("process") or {}
                report = review.get("report") or {}
                result_summary = {
                    "profile": r.get("profile"),
                    "finished_at": r.get("finished_at"),
                    "checks_origin": r.get("checks_origin"),
                    "publication_policy": r.get("publication_policy"),
                    "agent": {
                        "status": agent.get("status"),
                        "exit_code": agent.get("exit_code"),
                        "seconds": agent.get("seconds"),
                    },
                    "review_process": {
                        "status": rev_proc.get("status"),
                        "exit_code": rev_proc.get("exit_code"),
                        "seconds": rev_proc.get("seconds"),
                    },
                    "review_report": {
                        "verdict": report.get("verdict"),
                        "summary": report.get("summary"),
                        "reason": report.get("reason"),
                        "findings_count": len(report.get("findings") or []),
                    },
                }
            except (OSError, json.JSONDecodeError):
                pass
        sup_events = []
        sup_path = res_dir / "supervisor-events.jsonl"
        if sup_path.is_file():
            for line in sup_path.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.strip():
                    try:
                        sup_events.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        tasks_out.append(
            {
                "key": key,
                "issue": row["issue"],
                "approval": row["approval"],
                "status": row["status"],
                "updated_at": row["updated_at"],
                "profile": data.get("profile"),
                "slot": data.get("slot"),
                "stage": data.get("stage"),
                "execution_outcome": data.get("execution_outcome"),
                "trusted_completion": data.get("trusted_completion"),
                "pull_request": data.get("pull_request"),
                "publish_branch": data.get("publish_branch"),
                "publish_attempts": data.get("publish_attempts"),
                "task_events": events,
                "supervisor_events": sup_events,
                "checks": checks,
                "result": result_summary,
                "artifacts": sorted(p.name for p in res_dir.iterdir()) if res_dir.is_dir() else [],
            }
        )

matched_events = []
events_path = private / "events.jsonl"
if events_path.is_file():
    issue_str = str(issue_num)
    key_prefix = f"issue-{issue_num}-"
    key_set = set(keys)
    for line in events_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        task_val = ev.get("task")
        if task_val == issue_str or (isinstance(task_val, str) and (task_val in key_set or task_val.startswith(key_prefix))):
            matched_events.append(ev)

print(
    json.dumps(
        {
            "issue": issue_num,
            "tasks": tasks_out,
            "events": matched_events[-events_limit:] if events_limit > 0 else matched_events,
        },
        indent=2,
    )
)
"""


def cmd_issue_status(args: argparse.Namespace) -> int:
    container = validate_name(args.container, "container")
    if args.issue <= 0:
        raise SystemExit(f"Invalid issue number: {args.issue}")
    info = podman_inspect(args.machine, [container])[0]
    status = info.get("State", {}).get("Status", "unknown")
    if status != "running":
        raise SystemExit(f"Container {container} is {status}; must be running to exec inspection.")
    active = active_worker_processes(args.machine, container)
    res = run_wsl(
        args.machine,
        [
            "podman",
            "exec",
            container,
            "python3",
            "-c",
            _ISSUE_STATUS_PY,
            str(args.issue),
            str(args.events_limit),
        ],
        capture=True,
    )
    if res.returncode != 0:
        raise SystemExit(res.stderr.strip() or "Failed to inspect issue status in container")
    payload = json.loads(res.stdout)
    payload["container"] = container
    payload["container_status"] = status
    payload["active_processes"] = active
    print(json.dumps(payload, indent=2))
    return 0


_EVENTS_PY = r"""
import json
import sys
from pathlib import Path

tail_n = int(sys.argv[1])
needle = sys.argv[2]
events_path = Path("/var/lib/bonsaiworker/private/events.jsonl")
if not events_path.is_file():
    print("[]")
    raise SystemExit(0)

out = []
for line in events_path.read_text(encoding="utf-8", errors="replace").splitlines():
    if not line.strip():
        continue
    if needle and needle not in line:
        continue
    try:
        out.append(json.loads(line))
    except json.JSONDecodeError:
        out.append({"raw": line})

if tail_n > 0:
    out = out[-tail_n:]
print(json.dumps(out, indent=2))
"""


def cmd_events(args: argparse.Namespace) -> int:
    container = validate_name(args.container, "container")
    res = run_wsl(
        args.machine,
        [
            "podman",
            "exec",
            container,
            "python3",
            "-c",
            _EVENTS_PY,
            str(args.tail),
            args.filter or "",
        ],
        capture=True,
    )
    if res.returncode != 0:
        raise SystemExit(res.stderr.strip() or "Failed to read events.jsonl")
    print(res.stdout.rstrip())
    return 0


def cmd_logs(args: argparse.Namespace) -> int:
    container = validate_name(args.container, "container")
    res = run_wsl(
        args.machine,
        ["podman", "logs", "--tail", str(args.tail), container],
    )
    return res.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage Bonsai Podman worker containers in WSL (podman-machine-default)."
    )
    parser.add_argument("--machine", default=DEFAULT_MACHINE, help="WSL distro name")
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_inspect = sub.add_parser("inspect", help="Inspect bonsai-* containers without exposing secrets")
    p_inspect.add_argument("--container", help="Specific container name")
    p_inspect.set_defaults(func=cmd_inspect)

    p_build = sub.add_parser("build", help="Build localhost/bonsai-worker:<tag> from local checkout")
    p_build.add_argument("--repo", default="constant-integration", help="Checkout path")
    p_build.add_argument("--tag", help="Explicit image tag")
    p_build.add_argument("--check", action="store_true", help="Run `podman run --rm <tag> check`")
    p_build.set_defaults(func=cmd_build)

    p_stop = sub.add_parser("stop", help="Safely stop (and optionally backup-rename) a worker")
    p_stop.add_argument("container")
    p_stop.add_argument("--backup-suffix", help="Rename container to <container>-before-<suffix>")
    p_stop.add_argument("--force", action="store_true", help="Stop even if active tasks exist")
    p_stop.set_defaults(func=cmd_stop)

    p_relaunch = sub.add_parser("relaunch", help="Stop, backup, and relaunch a worker with preserved config")
    p_relaunch.add_argument("container")
    p_relaunch.add_argument("--repo", default="constant-integration", help="Checkout path for default tag")
    p_relaunch.add_argument("--image", help="Explicit image tag")
    p_relaunch.add_argument("--backup-suffix", help="Backup suffix (default: tag short SHA)")
    p_relaunch.add_argument("--force", action="store_true", help="Stop even if active tasks exist")
    p_relaunch.set_defaults(func=cmd_relaunch)

    p_action = sub.add_parser("action", help="Run a one-shot action using --volumes-from <container>")
    p_action.add_argument("container")
    p_action.add_argument("action", choices=ALLOWED_ACTIONS)
    p_action.add_argument("--image", help="Override image (default: container's current image)")
    p_action.add_argument("action_args", nargs=argparse.REMAINDER)
    p_action.set_defaults(func=cmd_action)

    p_issue = sub.add_parser(
        "issue-status",
        help="Inspect a GitHub issue's worker task state, timeline, checks, and review summary",
    )
    p_issue.add_argument("issue", type=int, help="GitHub issue number")
    p_issue.add_argument("--container", default="bonsai-worker", help="Container name")
    p_issue.add_argument("--events-limit", type=int, default=20, help="Max matching events.jsonl entries")
    p_issue.set_defaults(func=cmd_issue_status)

    p_events = sub.add_parser("events", help="Read or filter /var/lib/bonsaiworker/private/events.jsonl")
    p_events.add_argument("--container", default="bonsai-worker", help="Container name")
    p_events.add_argument("--tail", type=int, default=30, help="Show last N matching events")
    p_events.add_argument("--filter", help="Substring filter")
    p_events.set_defaults(func=cmd_events)

    p_logs = sub.add_parser("logs", help="Show container stdout/stderr logs")
    p_logs.add_argument("--container", default="bonsai-worker", help="Container name")
    p_logs.add_argument("--tail", type=int, default=80, help="Number of log lines")
    p_logs.set_defaults(func=cmd_logs)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
