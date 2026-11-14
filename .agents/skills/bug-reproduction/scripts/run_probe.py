"""Run a reviewed harness with temporary state and capture commit-bound evidence.

This is not a sandbox. Timeout termination covers the direct child only.
"""
import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time


def git_observation(source, *args):
    try:
        result = subprocess.run(
            ["git", "-C", str(source), *args], capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=10, check=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def write_report(path, report):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path, help="fresh evidence directory")
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--pass-env", action="append", default=[], metavar="NAME",
                        help="allow a necessary non-secret parent environment variable")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="-- executable argument ...")
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a command after -- is required")
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("timeout must be positive and finite")
    source = args.source.resolve(strict=True)
    if not source.is_dir():
        parser.error("source must be a directory")
    executable = shutil.which(command[0])
    if executable is None:
        parser.error(f"executable not found: {command[0]}")
    command[0] = str(Path(executable).resolve())
    evidence = args.evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    report_path = evidence / "result.json"
    report = {
        "schema_version": 1, "started_at": datetime.now(timezone.utc).isoformat(),
        "command": command, "source": str(source), "source_head": git_observation(source, "rev-parse", "HEAD"),
        "source_status": git_observation(source, "status", "--porcelain"),
        "host": platform.platform(), "runner_python": sys.version,
        "stdout": str(evidence / "stdout.txt"), "stderr": str(evidence / "stderr.txt"),
        "status": "starting", "exit_code": None,
    }
    allowed = {"PATH", "SystemRoot", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT",
               "LANG", "LC_ALL", "TZ", "PROCESSOR_ARCHITECTURE", "NUMBER_OF_PROCESSORS"}
    allowed.update(args.pass_env)
    environment = {key: value for key, value in os.environ.items() if key in allowed}
    report["passed_environment_names"] = sorted(environment)
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="codex-review-probe-") as directory:
        scratch = Path(directory)
        home = scratch / "home"
        home.mkdir()
        temp = scratch / "tmp"
        temp.mkdir()
        environment.update({
            "HOME": str(home), "USERPROFILE": str(home), "APPDATA": str(home),
            "LOCALAPPDATA": str(home), "TMP": str(temp), "TEMP": str(temp), "TMPDIR": str(temp),
            "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1",
            "REVIEW_SOURCE_ROOT": str(source), "REVIEW_SCRATCH_ROOT": str(scratch),
        })
        report["cwd"] = str(scratch)
        write_report(report_path, report)
        with (evidence / "stdout.txt").open("wb") as stdout, (evidence / "stderr.txt").open("wb") as stderr:
            try:
                result = subprocess.run(
                    command, cwd=scratch, env=environment, stdout=stdout, stderr=stderr,
                    timeout=args.timeout, check=False,
                )
                report.update(status="exited", exit_code=result.returncode)
            except subprocess.TimeoutExpired:
                report.update(status="timed_out", error="direct child exceeded timeout")
            except OSError as error:
                report.update(status="launch_failed", error=str(error))
    report["duration_seconds"] = round(time.monotonic() - start, 6)
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    report["source_head_after"] = git_observation(source, "rev-parse", "HEAD")
    report["source_status_after"] = git_observation(source, "status", "--porcelain")
    write_report(report_path, report)
    print(json.dumps({"evidence": str(report_path), "status": report["status"], "exit_code": report["exit_code"]}))
    if report["status"] == "timed_out":
        return 124
    if report["status"] == "launch_failed":
        return 2
    return report["exit_code"] if 0 <= report["exit_code"] <= 255 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"probe failed: {error}", file=sys.stderr)
        sys.exit(2)
