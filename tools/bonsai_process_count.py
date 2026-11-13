"""Count running Bonsai and Bonsai-UI worker processes.

Classifies every running process into:

  - "ui"     : a Bonsai UI worker (matches BONSAI and a UI token)
  - "worker" : a Bonsai worker that is not a UI worker
  - (everything else is ignored)

A process matches when its executable name starts with the BONSAI token or its
full command line contains the BONSAI token (case-insensitive; command lines
require a word boundary so a URL mentioning a bonsai host does not count).
Glued executable names such as ``bonsaiworker.exe`` match via the name rule.
A matching process is treated as a UI worker when a UI token additionally
appears (e.g. ``bonsai-ui``, ``bonsai_ui``, ``bonsaiui``, ``bonsai ui``,
``--role ui``).

The classification is heuristic: it inspects names and command lines only.

Primary implementation uses ``psutil`` (``pip install psutil``). Without it,
the script falls back to platform tools: PowerShell (Win32_Process) on
Windows, ``pgrep -af`` on POSIX.

Usage:
    python bonsai_process_count.py             # human-readable summary
    python bonsai_process_count.py --json      # machine-readable
    python bonsai_process_count.py --verbose   # list matched processes
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

# A dot on the left is excluded too, so a hostname such as
# "x.bonsai.example.org" in a command line does not count as a process.
BONSAI_TOKEN = re.compile(r"(?<![a-z0-9_.-])bonsai(?![a-z0-9_-])", re.IGNORECASE)
UI_TOKEN = re.compile(r"(?<![a-z0-9_-])ui(?![a-z0-9_-])", re.IGNORECASE)
# "bonsai-ui", "bonsai_ui", "bonsaiui": a UI suffix glued to the BONSAI token.
UI_SUFFIX = re.compile(r"bonsai[-_]?ui\b", re.IGNORECASE)

MAX_CMDLINE_CHARS = 200


def _classify(name: str, cmdline: str) -> str | None:
    """Return 'ui', 'worker' or None for a (executable name, command line)."""
    name_match = bool(BONSAI_TOKEN.search(name)) or name.lower().startswith("bonsai")
    cmdline_match = bool(BONSAI_TOKEN.search(cmdline)) or bool(UI_SUFFIX.search(cmdline))
    if not (name_match or cmdline_match):
        return None
    haystack = f"{name}\n{cmdline}"
    if UI_SUFFIX.search(haystack) or UI_TOKEN.search(haystack):
        return "ui"
    return "worker"


def _truncate(value: str) -> str:
    value = " ".join(value.split())
    return value if len(value) <= MAX_CMDLINE_CHARS else value[: MAX_CMDLINE_CHARS - 1] + "…"


def _psutil_processes():
    import psutil  # type: ignore import-not-found

    for process in psutil.process_iter(attrs=None):
        try:
            name = process.name() or ""
            cmdline = " ".join(process.cmdline())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        yield process.pid, name, cmdline


def _powershell_processes():
    """Windows fallback: one PowerShell CIM query, tab-separated output."""
    script = (
        "Get-CimInstance Win32_Process | "
        "ForEach-Object { \"$($_.ProcessId)`t$($_.Name)`t$($_.CommandLine)\" }"
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"PowerShell query failed: {result.stderr.strip()[:200]}")
    for line in result.stdout.splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3 and parts[0].isdigit():
            yield int(parts[0]), parts[1], parts[2] or ""


def _pgrep_processes():
    """POSIX fallback: pgrep -af yields 'PID cmdline'; executable name unknown."""
    result = subprocess.run(
        ["pgrep", "-af", "-i", "bonsai"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    for line in result.stdout.splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2 and parts[0].isdigit():
            yield int(parts[0]), "", parts[1]


def collect() -> list[dict]:
    """Return matched processes as dicts: kind, pid, name, cmdline."""
    psutil_error = pgrep_error = powershell_error = None
    rows: list[tuple[int, str, str]] = []
    try:
        rows = list(_psutil_processes())
    except ImportError:
        psutil_error = "psutil not installed"
    except Exception as error:  # noqa: BLE001 - any enumeration failure falls through
        psutil_error = f"psutil failed: {error}"

    if not rows and psutil_error:
        if sys.platform.startswith("win"):
            try:
                rows = list(_powershell_processes())
            except Exception as error:  # noqa: BLE001
                powershell_error = str(error)
        else:
            try:
                rows = list(_pgrep_processes())
            except Exception as error:  # noqa: BLE001
                pgrep_error = str(error)
        if not rows and (powershell_error or pgrep_error):
            detail = powershell_error or pgrep_error
            raise RuntimeError(f"process enumeration failed ({psutil_error}; {detail})")

    seen: set[int] = set()
    matched: list[dict] = []
    for pid, name, cmdline in rows:
        if pid in seen:
            continue
        kind = _classify(name, cmdline)
        if kind is None:
            continue
        seen.add(pid)
        matched.append(
            {
                "kind": kind,
                "pid": pid,
                "name": name,
                "cmdline": _truncate(cmdline) if cmdline else None,
            }
        )
    matched.sort(key=lambda item: (item["kind"], item["pid"]))
    return matched


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Count running Bonsai and Bonsai-UI worker processes."
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument(
        "--verbose", action="store_true", help="list each matched process (pid, name, cmdline)"
    )
    args = parser.parse_args(argv)

    try:
        matched = collect()
    except (RuntimeError, OSError, subprocess.SubprocessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    counts = {"worker": 0, "ui": 0}
    for item in matched:
        counts[item["kind"]] += 1

    if args.json:
        print(json.dumps({"counts": counts, "processes": matched}, indent=2))
        return 0

    print(f"bonsai workers:    {counts['worker']}")
    print(f"bonsai ui workers: {counts['ui']}")
    if args.verbose:
        for item in matched:
            detail = f" {item['name']}" if item["name"] else ""
            cmdline = f" — {item['cmdline']}" if item["cmdline"] else ""
            print(f"  [{item['kind']}] pid {item['pid']}{detail}{cmdline}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
