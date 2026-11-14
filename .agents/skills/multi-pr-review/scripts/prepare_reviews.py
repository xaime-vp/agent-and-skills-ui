"""Create detached review worktrees and independent evidence directories."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys


def git(repo, *args):
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    )
    return result.stdout.strip()


def pinned(repo, value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value):
        raise ValueError("head_sha and base_sha must be full lowercase commit hashes")
    if git(repo, "rev-parse", "--verify", value + "^{commit}") != value:
        raise ValueError(f"not an available commit: {value}")
    return value


def save(path, data):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path, help="existing local checkout")
    parser.add_argument("--prs", required=True, type=Path, help="JSON object with a prs array")
    parser.add_argument("--out", required=True, type=Path, help="fresh review root; never overwritten")
    args = parser.parse_args()
    repo = Path(git(args.repo.resolve(), "rev-parse", "--show-toplevel")).resolve()
    out = args.out.resolve()
    if out.exists():
        raise ValueError(f"review root already exists: {out}")
    if out.is_relative_to(repo):
        ignored = subprocess.run(
            ["git", "-C", str(repo), "check-ignore", "--quiet", "--", str(out)], check=False,
        )
        if ignored.returncode != 0:
            raise ValueError("a review root inside the source checkout must be Git-ignored")
    spec = json.loads(args.prs.read_text(encoding="utf-8-sig"))
    rows = spec.get("prs") if isinstance(spec, dict) else None
    if not isinstance(rows, list) or not rows:
        raise ValueError("prs must be a nonempty array")
    reviews = []
    numbers = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each PR must be an object")
        number = row.get("number")
        if type(number) is not int or number < 1 or number in numbers:
            raise ValueError("PR numbers must be unique positive integers")
        numbers.add(number)
        head = pinned(repo, row.get("head_sha"))
        base = pinned(repo, row.get("base_sha"))
        reviews.append({
            "number": number, "url": row.get("url"), "head_sha": head, "base_sha": base,
            "merge_base_sha": git(repo, "merge-base", base, head),
            "checkout": str(out / f"pr-{number}" / "checkout"),
            "evidence": str(out / f"pr-{number}" / "evidence"), "status": "pending",
        })
    out.mkdir(parents=True)
    manifest = {
        "schema_version": 1, "created_at": datetime.now(timezone.utc).isoformat(),
        "repository_checkout": str(repo), "status": "partial", "prs": reviews,
    }
    manifest_path = out / "manifest.json"
    save(manifest_path, manifest)
    for review in reviews:
        evidence = Path(review["evidence"])
        evidence.mkdir(parents=True)
        git(repo, "worktree", "add", "--detach", review["checkout"], review["head_sha"])
        review["status"] = "prepared"
        save(manifest_path, manifest)
    manifest["status"] = "prepared"
    save(manifest_path, manifest)
    print(json.dumps({"manifest": str(manifest_path), "count": len(reviews)}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"review setup failed: {error}", file=sys.stderr)
        sys.exit(2)
