---
name: pr-repair
description: Review existing GitHub pull requests and carry authorized corrections through verification on their current branches. Use for review PR, review and implement PR, fix PR, merge conflicts, failing checks or review feedback. Review-only requests remain read-only; this skill does not authorize merging or deployment.
---

# PR review and repair

Coordinate review, scoped remediation and final verification on each existing PR
branch. For review-only requests, inspect and report without modifying source,
creating issues, updating PR metadata or publishing review comments unless requested.
For review-and-implement or repair requests, carry authorized corrections through
publication and verification. A local pass alone does not establish delivery.

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

Choose review depth from the diff and risk, respecting the user's requested depth:

- **Quick:** prose-only or localized low-risk changes; inspect the changed content
  and directly affected references and run relevant required checks.
- **Standard:** ordinary implementation changes; review surrounding behavior,
  assertions, affected callers, documentation and required validation.
- **Deep:** concurrency, security, deployment or architecture changes; trace
  cross-component contracts and failure paths, including defaults and limits.

Depth limits exploratory work; it never waives repository-required validation.
Use [change-impact-analysis](../change-impact-analysis/SKILL.md) when the diff
changes defaults, configuration, concurrency or public/runtime contracts. Load
other supporting skills at the decision that needs them, not all at startup.

Classify findings as blockers, scoped corrections, unrelated follow-ups or optional
improvements. State the affected location, failure mechanism, user impact and a
way to verify each actionable finding. Distinguish a regression introduced by this
diff from an existing limitation. Implement authorized application corrections;
report unrelated limitations without opening additional work unless requested.

Distinguish merge conflicts, application defects, failing test expectations,
environment failures and unfinished worker contributions. For an ambiguous
"fix PR", use its conflict state, failed check logs and actionable review feedback
to identify the concrete problem. Ask if materially different outcomes remain.

Use [delegation-triage](../delegation-triage/SKILL.md) when independent specialist
work is identified, before dispatching anything. Follow
repository ownership rules: repairing application behavior and mechanically
integrating unchanged contributions differ from authoring new assertions,
fixtures or documentation. The developer may author tightly coupled tests/docs;
delegate substantial independent work or an explicit specialist assignment.
Do not weaken assertions to obtain a green check. Even mechanical test integration
must respect stricter repository rules.

In the agent-and-skills workspace, load [bonsai-ci](../bonsai-ci/SKILL.md) only
for an authorized handoff or active delivery tracking. It owns installed-route
selection, preparation and release-specific admission; do not infer approval
requirements from historical transcripts. Use [pr-submission](../pr-submission/SKILL.md)
when publishing or updating the PR. Use another repository's own workflow elsewhere.

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

Use [pr-validation](../pr-validation/SKILL.md) to choose checks and reconcile local,
worker and GitHub evidence. Review the combined diff against the actual base for
lost tests, unrelated changes and unintended behavior, including automatic merges.

After publication, fetch the PR again and inspect checks at its exact head SHA.
Confirm mergeability after GitHub finishes calculating it; unknown is not success.
For a request to fix failing CI, follow the affected runs to a terminal result or
a concrete blocker. For required worker delivery, follow the contribution through
its actual branch commit. Use bounded waits with backoff when nothing changes;
batch independent status reads and avoid repeatedly fetching the same full diff.
A pending run is not itself a blocker. If progress stalls, inspect the relevant
failure or missing prerequisite rather than spinning on status requests.

Keep incomplete work in draft when required by the repository. Do not mark a PR
ready while required worker contributions, checks or repairs remain outstanding.
Update its description with the final behavior, contribution provenance and
validation evidence when updates are authorized. Mark it ready once required work
and checks are complete under the root workflow. Review-only work reports readiness
without changing draft status. Finish independent PRs even if another PR is blocked.

Stop expanding the investigation once the requested behavior, substantive findings,
required checks and handoffs are resolved or have concrete blockers. Optional
improvements and unrelated legacy limitations do not keep the PR workflow open.
Report review-only work as reviewed with findings and validation limits; report
writable work as ready, blocked or incomplete according to the observed evidence.

Report each PR's link and branch, findings or repairs, reviewed/published commit,
validation outcome and concrete remaining blocker. Link worker issues when used. If an
interruption prevents completion, preserve the current merge/tree/commit state,
running check identifiers and exact next action so the repair can resume.
Leave merge into the base and deployment to the user unless separately authorized.
