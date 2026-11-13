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
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
