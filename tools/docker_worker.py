"""Deprecated path alias. Use managed arguments documented in tools/README.md."""
import runpy
from pathlib import Path

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).with_name('containers.py')), run_name='__main__')
