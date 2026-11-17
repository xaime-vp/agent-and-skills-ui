---
name: pr-validation
description: Select and run appropriate PR checks and reconcile local, worker and GitHub evidence against the reviewed or published revision. Use for executable implementation changes, validating delivered contributions, failing checks or assessing final PR readiness.
---

# PR validation

Choose checks from the actual diff, repository requirements and supported execution
environment. Review depth does not waive required checks. Documentation-only changes
need relevant link/example/format checks, not an unrelated application suite unless
the repository requires it.

Read applicable check commands, pinned tool versions and CI workflows. Inspect
existing check evidence before rerunning it. Keep a small record of command/job,
executor, source commit/tree, environment/tool versions, result and material limits.
Distinguish local execution, protected worker checks, advisory model review and
GitHub CI. A model review is not test execution.

Start with focused checks that exercise changed behavior or reproduce a failure.
Add integration or boundary cases where the diff crosses components; run the
repository-required complete validation before declaring the combined change ready.
For constant-integration worker accounting or export changes, focused suites are
`workers.bonsai.tests.test_token_accounting`, `test_intermediate_calls`,
`test_export`, `test_incremental_export` and `test_listener`, followed by
`python tools/check.py --component worker` and `python -m ruff check .`.
Use existing assertions when adequate. Independent new tests follow ownership rules
through [delegation-triage](../delegation-triage/SKILL.md); do not weaken tests for green CI.

When host failures involve process semantics, signals, shells, paths or other
platform behavior, inspect the failure and reproduce in the repository's supported
Linux/container/WSL environment when relevant. Do not assume Windows failures are
benign or run every PR on two platforms. Reuse suitable installed tools without
upgrading workers, starting paid models or exposing secrets as incidental validation.
Document any remaining unsupported-platform limitation.

For an isolated snapshot, record its source commit and Git tree (or a reproducible
description of included uncommitted changes). Transfer only scoped source, excluding
credentials and local runtime state. Confirm the snapshot contains the changes being
claimed; a `git archive HEAD` run excludes uncommitted edits. Bind snapshot results to
the tested tree and check that the published commit contains that tree. If subsequent
changes affect it, revalidate affected behavior and any required combined checks.

Reuse evidence when its tree, relevant environment/dependencies and required revision
still apply. Do not rerun unchanged checks merely while waiting for a worker. Rerun
when relevant conditions change, a repository rule requires it or a diagnosed
transient failure justifies another attempt; record why. Repeating a deterministic
failure without a changed condition is not progress.

After all authorized publications/contributions, refresh the PR head and inspect
GitHub checks at that exact SHA. A matching tree can support local evidence across
commits; older-head GitHub CI remains older-head CI. Pending, failed, skipped and
unavailable checks remain visible. No configured checks is not a CI pass, and
unknown mergeability is not confirmation that the PR is mergeable.

Follow explicitly requested CI watches and affected runs for a CI repair to a
terminal result or concrete blocker. Use bounded waits/backoff, and inspect a
stalled run's failure/prerequisite rather than continually requesting status. Do
not cancel or retrigger runs without task authorization. Required pending checks
keep readiness incomplete; accurately report unrelated pending checks.

Return compact validation evidence with the reviewed/published SHA, check outcomes,
environment limitations and remaining required work. The coordinator and
[pr-submission](../pr-submission/SKILL.md) use that evidence for readiness and delivery;
this skill does not authorize PR mutations, merging or deployment.
