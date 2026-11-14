# Runtime discovery and task schema

Verify model, repository binding, protected checks and listener status when used.
This workspace does not assume a previously used target, engine or model is current.

- Platform repository: `xaime-vp/constant-integration`.
- UI issue and parent-PR repository: `xaime-vp/constant-integration-ui`.
  Harness-only changes target the `main` branch of
  `xaime-vp/agent-and-skills-ui`; do not send runtime edits to the UI-bound worker.
- In this workspace its source checkout is `constant-integration/`, and the
  offline validator is `.agents/tools/validate_task.py` at the workspace root. The root
  developer's currently selected target determines issue and PR destinations.
- Locate the platform checkout from the current workspace or configured project.
  Its checked-out branch may be older than the sealed runtime. Read current
  instructions and installed revision before assuming behavior.
- Inventory the configured engine and identify the container whose installed
  target matches the selected repository. Windows scheduled-task status is not
  evidence that the Linux listener is running. Each target needs its own binding
  and state; never substitute another target's worker or protected checks.
- Confirm the installed model instead of pinning work to a historical name.
  There is no `agent:deepseek` dispatch label.
- In the selected container, `/var/lib/bonsaiworker/config.json` selects the installed
  release, bound target repository, model and protected `checks`. Only read the
  fields needed. Credentials and task state are under its `private/` directory;
  never print credential files or export them into issue bodies.
- Before dispatch, distinguish a running container from a ready listener, an
  unblocked supervisor, model metadata readiness, and successful generation.
  An offline registry/readiness probe is not a successful implementation.

Use the platform's current documented entrypoint/CLI for inspection, startup and
reconciliation. Preserve one active listener per repository and its state volume. Starting an
existing listener does not install newer source code; installed releases are
sealed and must be updated through the documented procedure. Runtime permission
or capability changes are a separate authorized operation, not an incidental
step in creating an application task.

## Choose the issue route

Current source accepts `agent:test-specialist` for tests/fixtures/test
configuration or `agent:documentation` for documentation. Select exactly one
matching issue label before preparation; it binds the proposal's implementation
profile. Test-specialist work gets an embedded read-only review after protected
checks and freeze; documentation publishes without a model reviewer. Reviewer
and supervisor are not implementation routes. Application code stays with the
root developer. Generalist/tests are retired source routes, not aliases.
If the sealed installation still uses a historical Generalist release, identify
that release/parser explicitly; do not describe its route as current source or
reinterpret its approvals. A source update does not upgrade the installation.

An ordinary prose issue can use [free-form preparation](../../../docs/free-form-issues.md)
on a compatible sealed installation. It needs no author-supplied envelope or
guessed exact scope/checks. The operator selects bounded evidence and
`--target-pr NUMBER` for the existing parent PR. The owner requests research
with `/prepare-agent` and approves a sealed executable proposal with the exact
returned `/approve-agent <full-digest>`. Preparation is exclusive and requires
the listener and role processes stopped; it cannot bypass active/unknown task
or publication reservations. Assessment-only preparation cannot implement.

## Legacy issue envelope

This section describes single-run schema-2 tasks. For multiple subsections of
one approved change, use [schema-3 plan submission](plans.md) instead: one parent
issue, checkpointed steps and one PR. Do not split a coherent plan into separate
PRs. Confirm the installed release supports the chosen schema/retry behavior;
the local platform checkout and installed configuration version are insufficient.

Copy this shape, replacing every example with the actual task and parent PR.
The paths below exist in the UI checkout; no example is an approved assignment.
The acceptance
command below is illustrative; use it only if it exactly matches the protected
check configuration for that project. Do not dispatch an unadapted example.

````markdown
```agent-task
{
  "schema_version": 2,
  "pull_request": 123,
  "project": "workspace",
  "role": "agent:test-specialist",
  "capabilities": ["tests"],
  "complexity": 1,
  "risk": "low",
  "goal": "Add regression coverage for existing UI backend unavailable-data responses.",
  "allowed_files": ["tests/test_backend.py"],
  "acceptance_commands": [
    ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]
  ],
  "verification_plan": "Run protected checks once in the implementation workspace and record actual exits; check target CI separately.",
  "provider": "openrouter",
  "timeout_seconds": 600
}
```
````

For a documentation contribution, use a separate issue with matching label,
documentation-only scope and the same actual parent PR. The illustrative
check set below still needs to match installed protected checks; it does not
prove links or commands were verified and grants no schema-4 repair pipeline.

````markdown
```agent-task
{
  "schema_version": 2,
  "pull_request": 123,
  "project": "workspace",
  "role": "agent:documentation",
  "capabilities": ["docs"],
  "complexity": 1,
  "risk": "low",
  "goal": "Document the parent PR behavior and verification limits in the UI development guide.",
  "allowed_files": ["docs/DEVELOPMENT.md"],
  "acceptance_commands": [
    ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]
  ],
  "verification_plan": "Verify documented commands against committed source; record protected check exits and no embedded model review. Inspect final-head target CI separately.",
  "provider": "openrouter",
  "timeout_seconds": 600
}
```
````

- Legacy bodies require exactly one fenced `agent-task` JSON block; no credentials,
  repository or issue identity fields inside it. Identity comes from GitHub and
  trusted policy.
- `project` is a top-level component directory. `workspace` means repository-root
  scope. `allowed_files` are exact paths relative to that component, or to the
  repository for `workspace`. Do not use globs or traversal.
- `acceptance_commands` is a list of argv lists, not shell command strings. It
  must match the protected checks for the original project key (`workspace`
  remains the key even though the runtime uses `.` as its working directory).
- Current source implementation profiles accept complexity up to 3 and reject high
  risk. Timeout and any explicit token limits must fit installed policy. On a
  compatible release, omitted `input_tokens`/`output_tokens` use automatic model
  context and no per-task response cap; provider/model limits still apply. The
  example assumes that support. Older releases may require explicit fields.
- For the root developer's test/documentation handoffs, include numeric
  `pull_request` for the existing open same-repository parent PR. Omitting it
  starts from the default branch and creates an unwanted separate draft.
  Only omit it for an explicitly requested independent new task.
- Use the selected test-specialist or documentation route and matching scope;
  examples must be adapted to the real parent PR and installed checks. Schema-4
  documentation repair is rejected, and schema 4 cannot target an existing PR.
- Required labels: `ready`, exactly one supported implementation profile.
  Required separate legacy owner comment: `/approve-agent`. Approval
  must be strictly after the issue's latest revision; same timestamps fail
  closed. A new issue revision or consumed approval may require a fresh comment.
  This standalone approval cannot approve a saved free-form proposal.

Current source supports `max_concurrent_tasks` of 1, 2 or 3, with separate
UID/GID and loopback relay per task. Old installed configs missing the field keep
one slot. Confirm actual installed state. Conflicting scopes/issues/PR branches
wait; keep semantic dependencies and shared external resources blocked/unready.

## Completion evidence

Record the issue, approval ID, installed release revision, task key, candidate
identity, implementation check commands/exits, applicable reviewer findings, draft PR
link/head, and target CI result. Keep unavailable evidence explicitly unknown.
If a reviewer report is malformed or contradicts itself, it remains inconclusive
even when implementation checks succeeded. For documentation, report no embedded
model review rather than inventing a verdict.

## Automatic commit reviews and telemetry

The trusted `automatic_pr_reviews` opt-in defaults false. It schedules read-only
reviews of open same-repository PR commits in shared slots and publishes advisory
commit-bound `COMMENT` reviews. It runs no tests, implements no changes and grants
no approval/repair/merge authority. New records allow three total attempts with
30/60-second delays after eligible pre-launch failure, fresh attempt identities
and one PR+commit publication marker. Already marked #203 fetch-recovery records
retain their pinned 60-second/three-attempt contract; neither route resets a
budget. Unknown stops, post-launch/results/stages/intents and unmarked historical
failures never gain replay permission. Only unknown tasks can use supported
confirmed-stop reconciliation; terminal `needs_attention` records cannot be reset
that way. See the [review retry contract](https://github.com/xaime-vp/constant-integration/blob/main/workers/bonsai/references/concurrency.md#automatic-commit-reviews)
and [recovery](https://github.com/xaime-vp/constant-integration/blob/main/workers/bonsai/references/plans-recovery.md#automatic-review-retries-and-reconciliation).

[Local history export](https://github.com/xaime-vp/constant-integration/blob/main/docs/HISTORY_EXPORT.md)
reads a SQLite backup without listener startup. Structured evidence is the
default; explicit `--include-verbose` adds sanitized logs/diffs and tool events.
Limits are 5000 events, 500 artifacts and 8 MiB per artifact. Captured provider
usage/cost is observed, not estimated; absent/malformed values stay unknown.
Capability flags do not guarantee complete accounting. Specialist task/attempt
capture gaps and capacity-3 representation limits remain explicit. Inspect
private bundles before sharing; redaction is not publication permission, and an
export heartbeat does not prove listener liveness. Telemetry tables are additive;
preserve state/history, consumed approvals, deduplication and intents through
stopped upgrades/rollback. No source edit authorizes installation changes.
