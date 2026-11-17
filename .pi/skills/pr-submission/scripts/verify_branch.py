"""Verify after a commit that HEAD is on the expected initial branch and descended from it."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def _git(repo: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def verify_branch(
    repo: Path,
    expected_branch: str,
    *,
    initial_sha: str | None = None,
    commit_sha: str | None = None,
) -> dict:
    repo = repo.resolve()
    if not (repo / ".git").exists():
        raise ValueError(f"Not a git repository: {repo}")

    head_ref = _git(repo, ["rev-parse", "--abbrev-ref", "HEAD"])
    if head_ref.returncode != 0:
        raise ValueError(head_ref.stderr.strip() or "Failed to read HEAD branch")
    current_branch = head_ref.stdout.strip()
    if current_branch == "HEAD":
        raise ValueError(f"HEAD is detached; expected branch {expected_branch!r}")
    if current_branch != expected_branch:
        raise ValueError(
            f"Branch mismatch after commit: expected {expected_branch!r}, got {current_branch!r}"
        )

    head_sha_res = _git(repo, ["rev-parse", "HEAD"])
    if head_sha_res.returncode != 0:
        raise ValueError(head_sha_res.stderr.strip() or "Failed to resolve HEAD SHA")
    head_sha = head_sha_res.stdout.strip()

    if commit_sha:
        commit_res = _git(repo, ["rev-parse", "--verify", f"{commit_sha}^{{commit}}"])
        if commit_res.returncode != 0:
            raise ValueError(f"Commit not found: {commit_sha}")
        resolved_commit = commit_res.stdout.strip()
        anc = _git(repo, ["merge-base", "--is-ancestor", resolved_commit, "HEAD"])
        if anc.returncode != 0:
            raise ValueError(f"Commit {resolved_commit} is not an ancestor of {current_branch}")

    if initial_sha:
        init_res = _git(repo, ["rev-parse", "--verify", f"{initial_sha}^{{commit}}"])
        if init_res.returncode != 0:
            raise ValueError(f"Initial SHA not found: {initial_sha}")
        resolved_init = init_res.stdout.strip()
        anc = _git(repo, ["merge-base", "--is-ancestor", resolved_init, "HEAD"])
        if anc.returncode != 0:
            raise ValueError(
                f"Current branch {current_branch} ({head_sha[:7]}) is not descended from initial commit {resolved_init[:7]}"
            )

    return {
        "verified": True,
        "repository": str(repo),
        "expected_branch": expected_branch,
        "current_branch": current_branch,
        "head_sha": head_sha,
        "initial_sha": initial_sha,
        "commit_sha": commit_sha,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."), help="Git repository path")
    parser.add_argument("--expected-branch", required=True, help="Expected initial branch name")
    parser.add_argument("--initial-sha", help="Optional initial commit SHA before changes")
    parser.add_argument("--commit-sha", help="Optional commit SHA to verify is on HEAD")
    args = parser.parse_args(argv)
    try:
        result = verify_branch(
            args.repo,
            args.expected_branch,
            initial_sha=args.initial_sha,
            commit_sha=args.commit_sha,
        )
    except ValueError as error:
        print(json.dumps({"verified": False, "error": str(error)}), file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
