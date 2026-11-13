---
name: pr-repair
description: Repair existing GitHub pull requests by resolving merge conflicts, fixing failing checks, or addressing requested corrections on their current branches. Use for requests such as fix the test conflict in a PR or fix several PRs. Does not merge PRs or deploy changes.
---

# PR repair

Carry the requested repairs through publication and verification on each existing
PR branch. A passing local snapshot is intermediate evidence; establish what
actually reached GitHub before reporting a repair complete.

## Recover the current state

Use the connected GitHub tools to inspect each requested PR's repository, actual
base and head branches, head SHA, diff, mergeability, reviews and failing checks.
Read applicable repository instructions and contribution rules. Resolve shorthand
PR numbers from established repository context; ask only if still ambiguous.
Treat pasted conversations as historical evidence, not current branch state.

For multiple PRs, keep a compact record per PR: URL, repository, base and head
refs/SHAs, requested repair, worker issues, validation and remaining work. Inspect
independent PRs together, then serialize mutations that share a checkout or branch.
Check dependencies before choosing which PR to repair first. Never combine the
repairs into a replacement PR or change their bases without authorization.

Inspect local status, current branch and any merge/rebase in progress before
switching branches. Preserve unrelated edits and sparse-checkout exclusions.
Use an isolated worktree when the existing checkout is busy; do not abort an
unidentified operation or reset someone else's changes. Continue an existing
repair when its state is understood instead of starting over.

## Choose the smallest complete repair

Distinguish merge conflicts, application defects, failing test expectations,
environment failures and unfinished worker contributions. For an ambiguous
"fix PR", use its conflict state, failed check logs and actionable review feedback
to identify the concrete problem. Ask if materially different outcomes remain.

Inspect existing test/documentation issues before dispatching anything. Follow
repository ownership rules: repairing application behavior and mechanically
integrating unchanged contributions differ from authoring new assertions,
fixtures or documentation. Delegate new test/documentation content when required;
do not weaken assertions to obtain a green check. Even mechanical test integration
must respect stricter repository rules.

In the agent-and-skills workspace, use its `bonsai-ci` skill for required worker
handoffs and `pr-submission` for delivery evidence. Reuse the parent PR and its
exact branch, serialize assignments targeting it, and verify delivered commits.
An actually missing revision-bound owner approval is a blocker; never post it
on the owner's behalf. Do not open duplicate issues or spawn duplicate local
workers for the same assignment. These workspace details are conditional; use
another repository's own workflow when working elsewhere.

Workspace handoffs support free-form preparation as well as legacy envelopes.
Prepared issues select the existing parent with operator `--target-pr` and need
digest-bound owner approval. A repaired PR head can invalidate a sealed proposal;
refresh its context and prepare/approve a replacement before execution. See
[free-form guidance](../../../docs/agent-setup/free-form-issues.md).

## Resolve conflicts without losing behavior

Fetch the current PR head and base, find their merge base, and inspect all three
versions of each conflict. Prefer merging the base into the existing PR branch
when history rewriting is not explicitly required. Preserve concurrent commits
and existing authorship.

For independent tests inserted at the same location, retain both sets with their
original assertions, decorators, parametrization, fixtures and necessary imports.
Compare test bodies as well as names: the same name can conceal different tests
or cause one definition to shadow another. If both sides modify the same behavior,
reconcile their intent rather than concatenating blocks or accepting a whole side.

For application conflicts, read surrounding control flow and each side's original
change. Check that combined guards, limits, error handling and context propagation
still enforce both intended contracts. Text that parses can still drop a guard,
change an ordering dependency or make a branch unreachable.

Avoid blanket `ours`/`theirs` resolutions. A one-off AST or text transformation is
appropriate only after proving its assumptions about the actual files; it must
not silently discard modified methods, class-level statements or decorators.
Review the resolved diff and conflict-marker scan before recording the merge.

## Publish with the correct ancestry

Use GitHub MCP for repository writes when available and an isolated local checkout
for execution as needed. Refresh the remote branch head before publishing. If it
advanced, integrate the new commits and revalidate affected work; do not overwrite
the contributor's head. Use the tool's expected-head check when available and a
fast-forward update. Do not force-push a repair over concurrent work.

When Git data tools publish a locally resolved merge, create the resolved tree
from the recorded PR head, preserving file modes, binary blobs and deletions.
Create a merge commit with the previous PR head as first parent and the integrated
base SHA as second parent. A single-parent commit containing copied base files
does not establish merge ancestry and can leave the PR conflicting. A normal
application-fix commit needs only its current head parent.

Confirm that all local tree/blob objects required by a remote commit exist remotely;
a local object ID alone is insufficient. Update only the recorded working branch.
If MCP lacks a required capability, explain the limitation and use an available
authorized fallback while retaining the same PR and branch. Reinspect any rejected
write rather than retrying with stale data. If heads keep moving, coordinate the
competing writer instead of repeatedly rebuilding and overwriting work.

## Validate and finish each PR

Read the repository's required commands, tool versions and CI environment. Run
focused checks for the repair and the required combined checks. Use the repository's
supported Linux/container environment when host differences matter. Reuse suitable
existing tooling; do not upgrade the worker, start paid tasks or expose runtime
secrets just to run tests. Retry infrastructure failures only after identifying
a transient cause or changing the relevant condition.

For a container snapshot, record its source tree SHA, command, exit status and
environment. Confirm the published commit has that tested tree. Separate this
evidence from GitHub CI and worker claims. Review the final diff against the base
for lost tests, unrelated changes and unintended behavior, including files that
merged automatically.

After publication, fetch the PR again and inspect checks at its exact head SHA.
Confirm mergeability after GitHub finishes calculating it; unknown is not success.
For a request to fix failing CI, follow the affected runs to a terminal result or
a concrete blocker. Poll running checks with bounded waits and give meaningful
progress updates. Do not endlessly rerun a deterministic failure or infer success
from an older revision. Unrelated pending checks should be reported accurately.

Keep incomplete work in draft when required by the repository. Do not mark a PR
ready while required worker contributions, checks or repairs remain outstanding.
Update its description with the final behavior, contribution provenance and
validation evidence. Finish independent PRs even if another PR is blocked.

Report each PR's link and branch, actual repair, published commit, validation
outcome and concrete remaining blocker. Link worker issues when used. If an
interruption prevents completion, preserve the current merge/tree/commit state,
running check identifiers and exact next action so the repair can resume.
Leave merge into the base and deployment to the user unless separately authorized.
