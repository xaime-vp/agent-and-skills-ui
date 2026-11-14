---
name: implementation-completeness
description: Compare a PR's promised behavior with its actual implementation files, callers and tests during every substantive PR review, including reviews containing only planning, documentation or worker contributions.
---

# Implementation completeness

Read the PR title/body, linked acceptance criteria and actual merge-base diff.
Separate delivered-behavior promises from explicit follow-ups. For each substantive
promise, find implementing symbols/configuration, reachable callers/entrypoints
and relevant assertions. Follow implementation outside changed files when it
already exists; legitimate tests-only/docs-only PRs need not change production code.

Check that worker contributions reached the PR head. A closed issue, completion
comment, unchecked plan or passing test does not prove implementation. Inspect
whether assertions exercise new behavior or merely confirm unchanged helpers.
Check wiring, packaging and runtime assets for features present but never used.

## Diff inventory helper

Run `scripts/inventory.py --help` with `--repo`, pinned `--base`, `--head` and
`--out`. It records merge base, commits, changed paths/statuses and heuristic
categories (tests, documentation, source, configuration, other). It reads Git
objects independently of unstaged edits and makes no semantic verdict. Inspect
renames, deletions and project-specific extensions before interpreting categories.

Use a small promise-to-evidence mapping when several requirements/contributions
are involved: promise, implementation/wiring, verification, remaining gap.
Report missing behavior as incomplete work, separately from introduced defects
and harmless stale prose. A missing production diff is not a regression for an
intentional tests-only/docs-only PR. Distinguish source, installation and activation.

Finish with the reviewed head, delivered/outstanding scope and material validation
limits. Refresh the mapping if the head moves. Review alone does not authorize
filling gaps, editing the PR, dispatching workers or posting a review.
