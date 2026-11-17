"""Offline schema validation using the selected platform's actual parser."""
import argparse
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--platform-root', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'constant-integration',
                        help='Platform source checkout (default: workspace/constant-integration)')
    parser.add_argument('--repository', required=True)
    parser.add_argument('--body-file', type=Path, required=True)
    parser.add_argument('--title', default='Proposed implementation plan')
    parser.add_argument('--max-timeout-seconds', type=int, default=1800)
    args = parser.parse_args()
    root = args.platform_root.resolve()
    if not (root / 'orchestrator/intake.py').is_file():
        parser.error('--platform-root must contain orchestrator/intake.py')
    sys.path.insert(0, str(root))
    from orchestrator.intake import IntakePolicy, TaskEnvelope
    try:
        # Synthetic identity is used only for parsing. No approval proof,
        # GitHub connection, controller or runtime database is constructed.
        policy = IntakePolicy(args.repository, 'offline-validation', 1,
                              max_timeout_seconds=args.max_timeout_seconds)
        task = TaskEnvelope.from_issue({'number': 1, 'title': args.title,
            'body': args.body_file.read_text(encoding='utf-8')}, policy)
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps({'schema_valid': True, 'schema_version': task.schema_version,
        'steps': len(task.steps) if task.steps else 1,
        'editable_files': len(task.repository_paths), 'approval_verified': False,
        'installed_compatibility_verified': False, 'protected_checks_verified': False}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
