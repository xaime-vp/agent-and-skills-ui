"""Deprecated path alias; accepts managed CLI arguments, never legacy force/relaunch options."""
import runpy
from pathlib import Path

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parents[4] / 'tools' / 'containers.py'), run_name='__main__')
