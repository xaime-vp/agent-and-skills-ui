"""Forward operations to the runtime-owned managed lifecycle CLI; no engine implementation here."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def command(argv, *, root=ROOT, platform=sys.platform):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--platform-root', type=Path)
    parser.add_argument('--wsl-distro')
    options, forwarded = parser.parse_known_args(argv)
    checkout = 'constant-integration'
    config = root / 'harness.config.json'
    if config.is_file():
        checkout = json.loads(config.read_text(encoding='utf-8')).get('targets', {}).get('checkout_dir', checkout)
        if not isinstance(checkout, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+', checkout) or checkout in ('.', '..'):
            raise ValueError('invalid configured runtime checkout')
    selected = options.platform_root or root / checkout
    target = selected.resolve() / 'tools' / 'containers.py'
    if not target.is_file() or target.resolve() == (root / 'tools' / 'containers.py').resolve():
        raise ValueError('Select a trusted runtime checkout with --platform-root; runtime tools/containers.py is missing')
    if options.wsl_distro:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', options.wsl_distro):
            raise ValueError('invalid WSL distribution')
        if platform != 'win32':
            raise ValueError('--wsl-distro is a Windows adapter option; use Linux Python directly on other hosts')
        value = target.as_posix()
        if not re.match(r'^[A-Za-z]:/', value):
            raise ValueError('WSL checkout must have a local drive path')
        value = '/mnt/' + value[0].lower() + value[2:]
        return ['wsl', '-d', options.wsl_distro, '--', 'python3', value, *forwarded], target.parent.parent
    if platform != 'linux' and '--help' not in forwarded and '-h' not in forwarded:
        raise ValueError('Lifecycle operations require Linux/WSL Python; select --wsl-distro on Windows')
    return [sys.executable, str(target), *forwarded], target.parent.parent


def main(argv=None):
    try:
        args, cwd = command(sys.argv[1:] if argv is None else argv)
        return subprocess.run(args, cwd=cwd, check=False).returncode
    except (OSError, ValueError, TypeError) as error:
        print('Lifecycle adapter: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
