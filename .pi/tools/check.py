"""Run the dedicated checkout's offline test runner from the workspace root."""
import os
from pathlib import Path
import runpy
import sys

if __name__ == "__main__":
    checkout = Path(__file__).resolve().parents[2] / "constant-integration"
    target = checkout / "tools" / "check.py"
    if not target.is_file():
        raise SystemExit(f"Missing platform runner: {target}")
    os.chdir(checkout)
    sys.path.insert(0, str(checkout))
    sys.argv[0] = str(target)
    runpy.run_path(str(target), run_name="__main__")
