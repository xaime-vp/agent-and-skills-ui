---
name: multi-pr-review
description: Review multiple pull requests independently when the user names or links several PRs. Keep separate worktrees, commit-bound evidence, findings, and validation results for each PR.
---

# Multi-PR review

Resolve the repository from the request, connected GitHub context or workspace.
Use connected GitHub tools for current metadata, patches, comments and checks when
available. Record each PR's URL, base/head refs and full SHAs, draft status,
changed files and dependencies on other requested PRs. Read applicable repository
instructions. Check target-repository guidance before assuming the workspace's
own remote is the target.

Review each PR against its own merge base in a separate detached worktree. Keep
the user's existing checkout and concurrent edits intact. Separate checkouts do
not imply parallel agent authorization; use subagents only when independently
authorized. Review dependent PRs independently first; use a separate integration
checkout only when combined behavior needs verification.

## Worktree helper

Fetch pinned objects using the authorized repository interface or local Git,
then run `scripts/prepare_reviews.py --help`. Supply `--repo` (an existing local
checkout), a fresh `--out` root, and `--prs` pointing to JSON in this shape:

```json
{"prs": [{"number": 240, "head_sha": "FULL_HEAD_SHA", "base_sha": "FULL_BASE_SHA", "url": "https://github.com/owner/repo/pull/240"}]}
```

Use actual full commit hashes in place of the explanatory values. The helper
creates one `pr-N/checkout` and `pr-N/evidence` directory per PR and an incremental
`manifest.json` with pinned SHAs and merge bases. It does not fetch, switch existing
branches, remove worktrees, or publish anything. If setup fails, inspect the
partial manifest before resuming; it deliberately preserves completed work.

## Evidence and findings

For each PR, compare promises to the actual diff and callers. Use the installed
companion `implementation-completeness` skill for substantive reviews;
`integration-path-validation` for changed runtime/CI boundaries,
`bug-reproduction` for suspected defects, and `state-recovery-validation` for
persistence or delivery changes. Their helpers are optional.

Bind observations to the reviewed head. Use pinned tool versions and supported
execution environments. Inspect assertions, not just exit codes. Distinguish local
checks, worker claims and GitHub CI; record skips, unavailable checks and environment
failures. Read failed job logs instead of repeatedly rerunning deterministic failures.

Refresh PR heads before finishing. If one moved, reassess affected findings and
checks or explicitly report the older reviewed SHA. Finish independent PRs even
if another is blocked. Report findings by severity with PR number, tight file/line
location, trigger, failure mechanism and useful correction or verification. State
missing implementation and material validation limits. Review alone does not
authorize posting comments/reviews, changing draft status, fixing, merging or deploying.
