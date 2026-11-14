"""Inventory an immutable PR diff; categories are hints, not completeness verdicts."""
import argparse
from collections import Counter
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    ).stdout


def category(path):
    value = PurePosixPath(path.lower())
    if any(part in {"test", "tests", "__tests__", "fixtures", "spec", "specs"} for part in value.parts):
        return "tests"
    if value.name.startswith("test_") or re.search(r"\.(test|spec)\.", value.name):
        return "tests"
    if "docs" in value.parts or "documentation" in value.parts or value.suffix in {".md", ".rst", ".adoc"}:
        return "documentation"
    if ".github" in value.parts or value.suffix in {".yaml", ".yml", ".toml", ".json", ".ini", ".cfg"}:
        return "configuration"
    if value.suffix in {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".c", ".h", ".cpp", ".cs", ".rb", ".sh", ".ps1", ".sql", ".swift", ".kt"}:
        return "source"
    return "other"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--base", required=True, help="full pinned target-base commit hash")
    parser.add_argument("--head", required=True, help="full pinned PR-head commit hash")
    parser.add_argument("--out", required=True, type=Path, help="new JSON output file")
    args = parser.parse_args()
    repo = args.repo.resolve()
    for value in (args.base, args.head):
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value):
            parser.error("base and head must be full lowercase commit hashes")
        if git(repo, "rev-parse", "--verify", value + "^{commit}").strip() != value:
            parser.error("commit hash does not resolve to an available commit")
    merge_base = git(repo, "merge-base", args.base, args.head).strip()
    tokens = git(repo, "diff", "--name-status", "-z", "--find-renames", merge_base, args.head, "--").split("\0")
    changed = []
    offset = 0
    while offset < len(tokens) and tokens[offset]:
        status, path = tokens[offset:offset + 2]
        offset += 2
        previous = None
        if status.startswith(("R", "C")):
            previous, path = path, tokens[offset]
            offset += 1
        row = {"status": status, "path": path, "category": category(path)}
        if previous is not None:
            row["previous_path"] = previous
            row["previous_category"] = category(previous)
        changed.append(row)
    commits = []
    for line in git(repo, "log", "--format=%H%x09%s", f"{merge_base}..{args.head}").splitlines():
        sha, subject = line.split("\t", 1)
        commits.append({"sha": sha, "subject": subject})
    output = {
        "schema_version": 1, "repository_checkout": str(repo), "base_sha": args.base,
        "head_sha": args.head, "merge_base_sha": merge_base, "commits": commits,
        "changed_files": changed, "category_counts": dict(Counter(row["category"] for row in changed)),
        "limitation": "Heuristic file categories do not prove implementation completeness.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as target:
        target.write(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"inventory": str(args.out.resolve()), "changed_files": len(changed), "category_counts": output["category_counts"]}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"inventory failed: {error}", file=sys.stderr)
        sys.exit(2)
