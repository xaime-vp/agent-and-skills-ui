---
name: pr-completion
description: Delegate existing-PR completion or readiness checks to a PR-finisher subagent with GitHub MCP and shell/Git access. Use for "finish PR" and final completion checks; reconcile implementation, delivered issue work, reviews and current-head CI. Does not authorize merging or deployment.
---

# PR completion

Determine what remains on the existing PR, carry authorized work to completion,
and report the evidence at its final head. A PR that is already complete needs
verification, not another commit or duplicate worker assignment.

Use [pr-repair](../pr-repair/SKILL.md) for review depth, scoped corrections,
conflicts and publication. A readiness/status/review-only request stays read-only,
including issues, PR metadata and posted reviews. A request to finish the PR
authorizes scoped completion under the repository's ownership rules; it does not
authorize merge, deployment or live worker activation.

## Parent: dispatch the completion work

The parent coordinates; one completion subagent owns the GitHub reads, local Git
commands, implementation review, authorized repairs and check tracking below.
Delegate once per PR and reuse that agent for follow-ups. Do not perform the same
inspection in both parent and child or launch duplicate workers for one assignment.

Discover the active client's agent/task capability and its live schema. Use one
completion executor with GitHub reads/writes appropriate to the requested mode
and shell/Git access. A Codex `pr_finisher` role is optional when that client
actually provides it; Pi must use its available task mechanism instead. Do not
hardcode a model, promise inherited connectors or launch another CLI merely to
obtain tools. If delegation is unavailable, disclose that and execute directly.

Give the executor the PR URL, requested mode, checkout location, known head,
existing evidence and active assignments. Assign ownership of application repairs
and completion evidence. It shares the codebase and must preserve other edits,
follow selected assignment ownership and execute rather than redispatch this
skill. Keep parent work in separate files/worktrees while it owns the checkout.

The executor verifies actual access through its initial nonmutating GitHub read
and local Git inspection. Git authentication is independent of connector access.
Do not copy credentials or infer write permissions from the parent's access. If
a required capability is absent, report the failed call and use an authorized
fallback; never claim a tool, command or publication succeeded without evidence.

Have the child return compact evidence: repository/PR, branch/head, findings or
repairs, delivered commits/issues, checks with revisions/skips, actual readiness,
and any concrete blocker. The parent relays meaningful progress, waits for required
work, and reviews that evidence without repeating the full tool sequence. Verify
only material gaps or changed state before the final user-facing report.

## Subagent: execute completion

If you were assigned this PR-completion task by a parent, start here and follow
the sections below directly. Do not spawn another completion coordinator. Bonsai
issue workers remain a separate repository workflow, not replacement local agents.

## Establish the evidence revision

Resolve the repository from the PR URL or established session context. Read its
applicable instructions. Fetch the PR and record repository, URL, actual base
and head refs/SHAs, draft/state and mergeability. Continue that PR and branch.
If it is already merged or closed, report that state instead of reopening it.

Discover connected GitHub MCP operations by capability; tool prefixes and argument
names vary between clients. Use the following as operation names, not a fixed
API binding. Inspect only the schemas needed for the next calls.

| Evidence | Operations and interpretation |
| --- | --- |
| PR identity and promises | `fetch_pr`; retain its diff and metadata for reuse |
| Actionable feedback | `list_pull_request_review_threads`, review submissions and `fetch_pr_comments` as needed; distinguish unresolved threads from historical comments |
| Delegated work | `fetch_issue`, `fetch_issue_comments` for linked assignments; search existing issues only when links or ownership are missing |
| Checks at the recorded SHA | `fetch_commit_workflow_runs`, check runs/status contexts and required-check configuration when available |
| Job evidence | `fetch_workflow_run_jobs`, then `fetch_workflow_job_logs` for failures, skips, counts or otherwise unverified claims |

Batch independent reads, for example threads, linked issues and workflows after
the PR has supplied their IDs/SHA. With `functions.exec`, use awaited promises
and inspect every settled result; keep dependent calls and mutations sequential.
Save fetched results and print compact fields or relevant excerpts. Do not repeatedly
dump full PR diffs, comment HTML or passing job logs. Fetch comments separately
only when the initial response lacks the evidence needed.

A workflow listing may cover only PR-triggered runs or its first page. Inspect
other checks/statuses and pagination where relevant; an empty listing is not a
pass. If required-check configuration or a check API is unavailable, disclose the
coverage limit rather than declaring all required checks satisfied.

## Inspect the matching checkout and combined change

Find an existing checkout/worktree before creating another. Inspect missing local
state in one bounded batch, using the following reads as needed rather than
repeating the entire inventory on every status update:

```sh
git status --short
git branch --show-current
git rev-parse HEAD
git sparse-checkout list
git log -6 --oneline
```

An unsparsed worktree can legitimately make `sparse-checkout list` fail. Preserve
configured exclusions, unrelated edits and any in-progress Git operation. Fetch
the recorded refs with `git fetch origin BRANCH` when needed, using the actual
remote/branch from this checkout; use an isolated worktree when the current checkout
is busy. A detached checkout is usable for inspection and validation. Establish
whether its HEAD/tree matches the recorded remote head before using its evidence.

Use the actual base/head SHAs for the merge-base diff, not an assumed `main` or
whatever local HEAD happens to contain:

```sh
git diff BASE_SHA...HEAD_SHA --stat
git diff BASE_SHA...HEAD_SHA -- relevant/paths
git diff --check BASE_SHA...HEAD_SHA
```

Substitute the recorded SHAs and discovered paths. Read surrounding implementation,
callers, actual assertions and affected documentation. Use `rg` and bounded reads
to follow concrete dependencies. Apply
[implementation-completeness](../implementation-completeness/SKILL.md) to substantive
reviews and conditional impact, integration, recovery and reproduction skills
through `pr-repair`; do not load every supporting skill automatically.

For each linked assignment, confirm the delivered commit/content reached this
head and matches its acceptance criteria. A closed issue or completion comment
alone is insufficient; an open issue with delivered content is not automatically
unfinished work. Keep worker checks and advisory model reviews separate from CI.

## Resolve gaps and verify checks

Use [pr-validation](../pr-validation/SKILL.md) to reconcile required commands,
worker observations, local results and exact-head GitHub checks. Inspect workflow
commands and job results before repeating execution. Reuse evidence whose revision,
tree and relevant environment still apply; older-head CI stays older-head CI.
Record failures, skips and unrun coverage, including platform limitations.

For writable completion, fix substantive application gaps through `pr-repair`.
Independent test/documentation gaps follow repository issue ownership: use
delegation triage and Bonsai handoff guidance, reuse matching assignments, and
verify their actual branch delivery. Do not spawn a duplicate local worker.
Preserve concurrent commits and refresh the remote head before every write.

Follow required pending checks or active deliveries with bounded waits and backoff;
inspect stalled prerequisites rather than polling unchanged full responses.
Stop when the requested work and required checks are complete or a concrete
external blocker prevents further useful progress. Optional improvements do not
keep a completed PR open as an implementation task.

## Finish against a fresh head

Fetch the PR again after all work. If its head moved, reconcile new commits and
revalidate affected evidence before claiming completion. Confirm mergeability;
unknown is not success. For authorized writable work, use
[pr-submission](../pr-submission/SKILL.md) to update stale delivery/validation claims
and mark ready only when repository requirements are met. Keep incomplete work in
draft where required. Avoid metadata churn when the description is already accurate.

Report the PR link, branch and reviewed/published SHA; delivered scope or repairs;
check outcomes and material limits; worker issue links when applicable; and actual
readiness or the concrete blocker. Say when no further changes were needed.
Leave merging, deployment, installed activation and live acceptance distinct.
