"""Check exported resource hashes locally; use the source exporter to verify against the pinned Git commit."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def check(root):
    manifest = json.loads((root / 'harness-source.json').read_text(encoding='utf-8'))
    if manifest.get('schema_version') != 1 or not isinstance(manifest.get('files'), list):
        raise ValueError('Invalid export manifest')
    errors, seen = [], set()
    for entry in manifest['files']:
        name = entry['path']
        if not isinstance(name, str) or PurePosixPath(name).is_absolute() or any(p in ('.', '..') for p in name.split('/')) or '\\' in name or ':' in name or name in seen:
            raise ValueError('Invalid/duplicate managed path')
        seen.add(name)
        path = root / name
        if any(p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()) for p in (path, *path.parents)):
            raise ValueError('Linked export path')
        if not path.is_file() or hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest() != entry['sha256']:
            errors.append(name)
    return errors


if __name__ == '__main__':
    try:
        errors = check(Path(__file__).resolve().parents[1])
        print('Export drift: ' + ', '.join(errors) if errors else 'Exported resources match the recorded hashes')
        raise SystemExit(1 if errors else 0)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('Export check failed: ' + str(error), file=sys.stderr)
        raise SystemExit(2) from None
