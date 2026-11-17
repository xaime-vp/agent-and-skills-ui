"""Run a dedicated checkout's offline test runner from the workspace root.

Supports both:
  - constant-integration (default): delegates to constant-integration/tools/check.py
  - constant-integration-ui (--target ui): runs backend unittest, contract_check.py,
    and optionally frontend typecheck/test/build (--frontend).
"""
import argparse
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys

UI_TARGETS = {"ui", "constant-integration-ui"}
PLATFORM_TARGETS = {"platform", "constant-integration"}


def _run_ui_checks(checkout: Path, *, frontend: bool) -> int:
    if not checkout.is_dir():
        raise SystemExit(f"Missing UI checkout: {checkout}")
    commands: list[tuple[Path, list[str]]] = [
        (checkout, [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
        (checkout, [sys.executable, "tools/contract_check.py", "fixtures/v1/01-successful-draft"]),
    ]
    if frontend:
        npm = shutil.which("npm")
        if not npm:
            raise SystemExit("npm not found on PATH for --frontend checks")
        fe_dir = checkout / "frontend"
        commands.extend([
            (fe_dir, [npm, "run", "typecheck"]),
            (fe_dir, [npm, "test"]),
            (fe_dir, [npm, "run", "build"]),
        ])
    for cwd, cmd in commands:
        print(f"+ ({cwd.name}) {' '.join(cmd)}", flush=True)
        res = subprocess.run(cmd, cwd=cwd)
        if res.returncode != 0:
            return res.returncode
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--target", default="constant-integration")
    parser.add_argument("--frontend", action="store_true")
    known, rest = parser.parse_known_args()

    workspace = Path(__file__).resolve().parents[1]
    if known.target in UI_TARGETS:
        if "--help" in rest or "-h" in rest:
            print("Usage: check.py --target ui [--frontend]")
            raise SystemExit(0)
        if rest:
            raise SystemExit(f"Unsupported arguments for --target ui: {' '.join(rest)}")
        raise SystemExit(_run_ui_checks(workspace / "constant-integration-ui", frontend=known.frontend))

    if known.target not in PLATFORM_TARGETS:
        raise SystemExit(f"Unknown --target {known.target!r}; expected constant-integration or ui")

    checkout = workspace / "constant-integration"
    target = checkout / "tools" / "check.py"
    if not target.is_file():
        raise SystemExit(f"Missing platform runner: {target}")
    os.chdir(checkout)
    sys.path.insert(0, str(checkout))
    sys.argv = [str(target), *rest]
    runpy.run_path(str(target), run_name="__main__")
