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
    "BONSAI_AUTOMATIC_PR_REVIEWS",
    "BONSAI_CLOSE_ISSUE_ON_SUCCESS",
    "BONSAI_EXPORT_DIR",
    "BONSAI_EXPORT_INCLUDE_VERBOSE",
    "BONSAI_EXPORT_INSTALLATION_ID",
    "BONSAI_EXPORT_INTERVAL_SECONDS",
    "BONSAI_MODEL",
    "BONSAI_THINKING_LEVEL",
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


def run_wsl(
    machine: str,
    argv: list[str],
    *,
    capture: bool = False,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    cmd = ["wsl", "-d", machine, "-e", *argv]
    env = os.environ.copy()
    env.setdefault("PODMAN_IGNORE_CGROUPSV1_WARNING", "1")
    return subprocess.run(
        cmd,
        env=env,
        text=True,
        input=input_text,
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


def find_worker_volume(info: dict) -> str | None:
    for m in info.get("Mounts", []):
        if m.get("Destination") == "/var/lib/bonsaiworker":
            return m.get("Name") or m.get("Source")
    return None


def build_mount_flags(info: dict, export_dir: str | None) -> list[str]:
    vol_src = find_worker_volume(info)
    if not vol_src:
        raise SystemExit("Container has no /var/lib/bonsaiworker mount")
    flags: list[str] = ["-v", f"{vol_src}:/var/lib/bonsaiworker"]
    for m in info.get("Mounts", []):
        dest = m.get("Destination")
        if not dest or dest == "/var/lib/bonsaiworker":
            continue
        if export_dir and dest == "/export":
            continue
        src = m.get("Name") or m.get("Source")
        if src:
            rw = "rw" if m.get("RW", True) else "ro"
            flags.extend(["-v", f"{src}:{dest}:{rw}"])
    if export_dir:
        wsl_export = to_wsl_path(Path(export_dir))
        flags.extend(["-v", f"{wsl_export}:/export:rw"])
    return flags


def apply_safe_env_overrides(safe_env: dict[str, str], env_args: list[str] | None) -> dict[str, str]:
    updated = dict(safe_env)
    for item in env_args or []:
        if "=" not in item:
            raise SystemExit(f"Invalid --env format (expected KEY=VALUE): {item!r}")
        k, v = item.split("=", 1)
        if k not in SAFE_BONSAI_KEYS:
            raise SystemExit(f"Unsupported --env key {k!r}; allowed: {', '.join(SAFE_BONSAI_KEYS)}")
        updated[k] = v
    return updated


def cmd_relaunch(args: argparse.Namespace) -> int:
    container = validate_name(args.container, "container")
    info = podman_inspect(args.machine, [container])[0]
    safe_env = extract_safe_env(info.get("Config", {}).get("Env", []))
    if args.export_dir:
        safe_env["BONSAI_EXPORT_DIR"] = "/export"
    safe_env = apply_safe_env_overrides(safe_env, args.env)
    target_repo = safe_env.get("BONSAI_TARGET_REPOSITORY")
    if not target_repo:
        raise SystemExit(f"Container {container} has no BONSAI_TARGET_REPOSITORY")
    mount_flags = build_mount_flags(info, args.export_dir)
    restart_policy = (
        info.get("HostConfig", {}).get("RestartPolicy", {}).get("Name") or "unless-stopped"
    )

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

    print(f"Launching {container} with {image} (target={target_repo})...")
    env_flags: list[str] = []
    for k, v in sorted(safe_env.items()):
        env_flags.extend(["-e", f"{k}={v}"])
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
            *mount_flags,
            *env_flags,
            image,
            "run",
        ],
    )
    return res.returncode


def cmd_upgrade(args: argparse.Namespace) -> int:
    container = validate_name(args.container, "container")
    info = podman_inspect(args.machine, [container])[0]
    safe_env = extract_safe_env(info.get("Config", {}).get("Env", []))
    if args.export_dir:
        safe_env["BONSAI_EXPORT_DIR"] = "/export"
    safe_env = apply_safe_env_overrides(safe_env, args.env)
    target_repo = safe_env.get("BONSAI_TARGET_REPOSITORY")
    if not target_repo:
        raise SystemExit(f"Container {container} has no BONSAI_TARGET_REPOSITORY")
    mount_flags = build_mount_flags(info, args.export_dir)
    restart_policy = (
        info.get("HostConfig", {}).get("RestartPolicy", {}).get("Name") or "unless-stopped"
    )

    if args.image:
        image = validate_name(args.image, "image")
    else:
        repo = Path(args.repo).resolve()
        short = subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "--short=7", "HEAD"], text=True
        ).strip()
        image = f"localhost/bonsai-worker:main-{short}"

    suffix = validate_suffix(args.backup_suffix) if args.backup_suffix else image.split(":")[-1].replace("main-", "")
    backup_name = f"{container}-before-{suffix}"
    stop_container(args.machine, container, suffix, args.force)

    env_flags: list[str] = []
    for k, v in sorted(safe_env.items()):
        env_flags.extend(["-e", f"{k}={v}"])

    print(f"Staging sealed release for {container} from {image} (prepare)...")
    prep = run_wsl(
        args.machine,
        [
            "podman",
            "run",
            "--rm",
            "--volumes-from",
            backup_name,
            *env_flags,
            "--entrypoint",
            "sh",
            image,
            "-c",
            "set -eu; set -a; . /var/lib/bonsaiworker/private/secrets.env; set +a; exec /opt/bonsai/workers/bonsai/docker-entrypoint.sh prepare",
        ],
    )
    if prep.returncode != 0:
        return prep.returncode

    print(f"Installing sealed release for {container} from {image} (install)...")
    inst = run_wsl(
        args.machine,
        [
            "podman",
            "run",
            "--rm",
            "--volumes-from",
            backup_name,
            *env_flags,
            image,
            "install",
        ],
    )
    if inst.returncode != 0:
        return inst.returncode

    verb = "run" if args.start else "create"
    extra = ["-d"] if args.start else []
    print(f"Recreating {container} ({'started' if args.start else 'stopped'}) with {image}...")
    res = run_wsl(
        args.machine,
        [
            "podman",
            verb,
            *extra,
            "--name",
            container,
            "--restart",
            restart_policy,
            *mount_flags,
            *env_flags,
            image,
            "run",
        ],
    )
    return res.returncode


def cmd_logs(args: argparse.Namespace) -> int:
    container = validate_name(args.container, "container")
    if args.controller:
        info = podman_inspect(args.machine, [container])[0]
        status = info.get("State", {}).get("Status")
        image = info.get("ImageName")
        if status == "running":
            cmd = ["podman", "exec", container, "tail", "-n", str(args.tail), "/var/lib/bonsaiworker/private/controller.log"]
        else:
            if not image:
                raise SystemExit(f"Could not determine image for stopped container {container}")
            cmd = [
                "podman", "run", "--rm", "--entrypoint", "tail", "--volumes-from", container,
                image, "-n", str(args.tail), "/var/lib/bonsaiworker/private/controller.log",
            ]
        return run_wsl(args.machine, cmd).returncode
    return run_wsl(args.machine, ["podman", "logs", "--tail", str(args.tail), container]).returncode


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


def cmd_task_status(args: argparse.Namespace) -> int:
    container = validate_name(args.container, "container")
    info = podman_inspect(args.machine, [container])[0]
    status = info.get("State", {}).get("Status")
    image = info.get("ImageName")

    py_snippet = r"""
import json, pathlib, sqlite3, sys

issue_filter = int(sys.argv[1]) if sys.argv[1] != "none" else None
key_filter = sys.argv[2] if sys.argv[2] != "none" else None
tail_n = int(sys.argv[3])

shared = pathlib.Path("/var/lib/bonsaiworker")
cfg_path = shared / "config.json"
cfg = json.loads(cfg_path.read_text(encoding="utf-8-sig")) if cfg_path.is_file() else {}
db_path = shared / "private" / "state.db"
if not db_path.is_file():
    print(json.dumps({"error": "state.db not found", "release_root": cfg.get("release_root")}, indent=2))
    sys.exit(0)

con = sqlite3.connect(str(db_path))
if key_filter:
    rows = con.execute(
        "SELECT key, issue, status, updated_at, data FROM tasks WHERE key = ? ORDER BY updated_at DESC LIMIT 5",
        (key_filter,),
    ).fetchall()
elif issue_filter is not None:
    rows = con.execute(
        "SELECT key, issue, status, updated_at, data FROM tasks WHERE issue = ? ORDER BY updated_at DESC LIMIT 5",
        (issue_filter,),
    ).fetchall()
else:
    rows = con.execute(
        "SELECT key, issue, status, updated_at, data FROM tasks ORDER BY updated_at DESC LIMIT 5"
    ).fetchall()

tasks = []
for key, issue, st, updated_at, raw_data in rows:
    d = json.loads(raw_data)
    events = con.execute(
        "SELECT id, status, reason, recorded_at FROM task_events WHERE key = ? ORDER BY id DESC LIMIT ?",
        (key, tail_n),
    ).fetchall()
    res_dir = shared / "private" / "results" / key
    progress = {}
    if res_dir.is_dir():
        for pf in sorted(res_dir.glob("progress-*.jsonl")):
            lines = [ln for ln in pf.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
            progress[pf.name] = [json.loads(ln) for ln in lines[-tail_n:]]
    tasks.append({
        "key": key,
        "issue": issue,
        "status": st,
        "stage": d.get("stage"),
        "pull_request": d.get("pull_request"),
        "draft_url": d.get("draft_url"),
        "dispatched_at": d.get("dispatched_at"),
        "updated_at": updated_at,
        "recent_events": [
            {"id": e[0], "status": e[1], "reason": e[2], "recorded_at": e[3]}
            for e in events
        ],
        "progress_tail": progress,
    })

print(json.dumps({
    "release_root": cfg.get("release_root"),
    "app_root": cfg.get("app_root"),
    "tasks": tasks,
}, indent=2))
""".strip()

    issue_arg = str(args.issue) if args.issue is not None else "none"
    key_arg = args.key or "none"
    tail_arg = str(args.tail)

    if status == "running":
        cmd = ["podman", "exec", "-i", container, "python", "-I", "-B", "-", issue_arg, key_arg, tail_arg]
    else:
        if not image:
            raise SystemExit(f"Could not determine image for stopped container {container}")
        cmd = [
            "podman", "run", "--rm", "-i", "--entrypoint", "python", "--volumes-from", container,
            image, "-I", "-B", "-", issue_arg, key_arg, tail_arg,
        ]
    return run_wsl(args.machine, cmd, input_text=py_snippet).returncode


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

    p_relaunch = sub.add_parser("relaunch", help="Stop, backup, and relaunch a worker with preserved config (no sealed-release upgrade)")
    p_relaunch.add_argument("container")
    p_relaunch.add_argument("--repo", default="constant-integration", help="Checkout path for default tag")
    p_relaunch.add_argument("--image", help="Explicit image tag")
    p_relaunch.add_argument("--backup-suffix", help="Backup suffix (default: tag short SHA)")
    p_relaunch.add_argument("--export-dir", help="Host directory to mount at /export and set BONSAI_EXPORT_DIR=/export")
    p_relaunch.add_argument("--env", action="append", help="Override non-secret BONSAI_* env var (KEY=VALUE)")
    p_relaunch.add_argument("--force", action="store_true", help="Stop even if active tasks exist")
    p_relaunch.set_defaults(func=cmd_relaunch)

    p_upgrade = sub.add_parser("upgrade", help="Stop, backup, prepare+install sealed release from image, and recreate container")
    p_upgrade.add_argument("container")
    p_upgrade.add_argument("--repo", default="constant-integration", help="Checkout path for default tag")
    p_upgrade.add_argument("--image", help="Explicit image tag")
    p_upgrade.add_argument("--backup-suffix", help="Backup suffix (default: tag short SHA)")
    p_upgrade.add_argument("--export-dir", help="Host directory to mount at /export and set BONSAI_EXPORT_DIR=/export")
    p_upgrade.add_argument("--env", action="append", help="Override non-secret BONSAI_* env var (KEY=VALUE)")
    p_upgrade.add_argument("--force", action="store_true", help="Stop even if active tasks exist")
    p_upgrade.add_argument("--start", action="store_true", help="Start the recreated container after upgrade (default: leave stopped)")
    p_upgrade.set_defaults(func=cmd_upgrade)

    p_logs = sub.add_parser("logs", help="Show container logs or controller.log tail")
    p_logs.add_argument("container")
    p_logs.add_argument("--tail", type=int, default=80, help="Number of trailing lines")
    p_logs.add_argument("--controller", action="store_true", help="Read /var/lib/bonsaiworker/private/controller.log instead of podman logs")
    p_logs.set_defaults(func=cmd_logs)

    p_action = sub.add_parser("action", help="Run a one-shot action using --volumes-from <container>")
    p_action.add_argument("container")
    p_action.add_argument("action", choices=ALLOWED_ACTIONS)
    p_action.add_argument("--image", help="Override image (default: container's current image)")
    p_action.add_argument("action_args", nargs=argparse.REMAINDER)
    p_action.set_defaults(func=cmd_action)

    p_status = sub.add_parser(
        "task-status",
        help="Query state.db, release_root, and progress-*.jsonl inside a worker container without exposing secrets",
    )
    p_status.add_argument("container")
    p_status.add_argument("--issue", type=int, help="Filter by GitHub issue number")
    p_status.add_argument("--key", help="Filter by task key")
    p_status.add_argument("--tail", type=int, default=5, help="Number of recent events/progress lines per task")
    p_status.set_defaults(func=cmd_task_status)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
