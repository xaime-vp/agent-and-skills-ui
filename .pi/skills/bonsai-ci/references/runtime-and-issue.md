# Runtime discovery and task schema

Verify model, repository binding, protected checks and listener status when used.
This workspace does not assume a previously used target, engine or model is current.

- Platform repository: `xaime-vp/constant-integration`.
- In this workspace its source checkout is `constant-integration/`, and the
  offline validator is `tools/validate_task.py` at the workspace root. The root
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

## Source defaults and installed decisions

Source checked against Constant Integration main
`a0810fccb6ed491dbb552b616b0717cabe976a12` on 2026-11-16. Recheck the pinned
source for future updates. The selected sealed release/configuration remains
the authority for execution; a container image or environment edit alone does
not update it.

| Decision | Current source/preparation behavior | Action for this handoff |
| --- | --- | --- |
| Task capacity | Configure accepts 1..10, default 10; missing installed `max_concurrent_tasks` retains one | Read the selected installed setting; never assume ten running tasks or increase it during a handoff |
| Commit reviews | Compose deployment preparation defaults `BONSAI_AUTOMATIC_PR_REVIEWS=true`; direct `configure.py` defaults false; missing installed `automatic_pr_reviews` stays false | Inspect installed policy; labels do not enable reviews, and read-only reviews grant no implementation authority |
| Ready admission | Current `admission_mode: ready` uses a validated current revision, `ready`, one matching implementation label and no `blocked`; owner revocation still applies | Admit only after prerequisites are verified; approval comments are ignored on this route |
| Historical admission | Older sealed releases may require standalone legacy approval or a sealed-proposal digest approval | Use only the matching released contract; never add a comment requirement to current ready admission |
| Preparation | Exclusive preparation requires a stopped listener/role processes and clear active/unknown task/publication reservations | Capacity does not permit concurrent preparation; lifecycle changes need their own authorization |
| Parent PR | Schema 2/3 uses numeric `pull_request`; free-form preparation uses operator `--target-pr`; schema 4 cannot select an existing PR | Keep test/docs contributions serial on the same branch and refresh source identity after each contribution |
| Repository consultation | Explicit installed delegation policy selects eligible schema-2 coders with exact paths and finite budgets; no parent shell | Use the native tool only when exposed; consult the [guide](../../../../docs/agent-setup/repository-consultation.md), not a new issue/label or manual child |

Source references:
[configuration](https://github.com/xaime-vp/constant-integration/blob/a0810fccb6ed491dbb552b616b0717cabe976a12/workers/bonsai/configure.py),
[deployment defaults](https://github.com/xaime-vp/constant-integration/blob/a0810fccb6ed491dbb552b616b0717cabe976a12/workers/bonsai/compose.yaml),
[review policy](https://github.com/xaime-vp/constant-integration/blob/a0810fccb6ed491dbb552b616b0717cabe976a12/workers/bonsai/pr_reviewer.py),
[capacity tests](https://github.com/xaime-vp/constant-integration/blob/a0810fccb6ed491dbb552b616b0717cabe976a12/workers/bonsai/tests/test_async_execution.py),
and [delivery/admission contract](https://github.com/xaime-vp/constant-integration/blob/a0810fccb6ed491dbb552b616b0717cabe976a12/docs/GITHUB_DELIVERY.md).

## Choose the issue route

Current source (`main` 727f32c, 2026-11-17) accepts `agent:coder` for scoped
application implementation and related approved tests/docs,
`agent:test-specialist` for tests/fixtures/test configuration, or
`agent:documentation` for documentation. Select exactly one matching issue label
before preparation; it binds the proposal's implementation profile. Coder and
test-specialist work get an embedded read-only review after protected checks and
freeze; documentation publishes without a model reviewer. Reviewer, supervisor
and the advisory `github-admin`/`planner`/`researcher` roles are not
implementation routes. Fresh preparations enable all four harness roles and the
three advisory roles with read-only defaults; that is configuration, not an
admission route or extra writer. Application code stays with the root developer **only in developer-led tasks**;
a deliberately delegated coder task must not overlap that writer. Generalist/tests
are retired source routes, not aliases.
If the sealed installation still uses a historical Generalist release, identify
that release/parser explicitly; do not describe its route as current source or
reinterpret its approvals. A source update does not upgrade the installation.

An ordinary prose issue can use [free-form preparation](../../../../docs/agent-setup/free-form-issues.md)
on a compatible sealed installation. It needs no author-supplied envelope or
guessed exact scope/checks. The operator selects bounded evidence and
`--target-pr NUMBER` for the existing parent PR. The owner requests research with `/prepare-agent`. On current source, the operator
inspects the sealed executable proposal and admits it with matching `ready` and
exactly one role label, without `blocked`; **no `/approve-agent` comment** is
required. Older verified sealed releases may require digest approval. Preparation is exclusive and requires
the listener and role processes stopped; it cannot bypass active/unknown task
or publication reservations. Assessment-only preparation cannot implement.

## Legacy issue envelope

This section describes single-run schema-2 tasks. For multiple subsections of
one approved change, use [schema-3 plan submission](plans.md) instead: one parent
issue, checkpointed steps and one PR. Do not split a coherent plan into separate
PRs. Confirm the installed release supports the chosen schema/retry behavior;
the local platform checkout and installed configuration version are insufficient.

Copy this shape, replacing every example with the actual task. The acceptance
command below is illustrative; use it only if it exactly matches the protected
check configuration for that project. Do not dispatch an unadapted example.

````markdown
```agent-task
{
  "schema_version": 2,
  "pull_request": 123,
  "project": "example-project",
  "role": "agent:test-specialist",
  "capabilities": ["tests"],
  "complexity": 1,
  "risk": "low",
  "goal": "Cover the parser's existing empty-input behavior with a deterministic fixture.",
  "allowed_files": ["tests/test_parser.py", "tests/fixtures/empty-input.txt"],
  "acceptance_commands": [["python", "-m", "unittest", "discover", "-s", "tests", "-v"]],
  "verification_plan": "Run protected checks once in the implementation workspace and record actual exits; check target CI separately.",
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
- Use the selected coder, test-specialist or documentation route and matching scope;
  examples must be adapted to the real parent PR and installed checks. Schema-4
  documentation repair is rejected, and schema 4 cannot target an existing PR.
- Current-source admission requires `ready`, no `blocked`, exactly one matching
  implementation role label and an executable current revision. Older installed
  releases may require standalone `/approve-agent` after the last issue edit;
  this legacy comment cannot approve a sealed free-form proposal.

Current source supports `max_concurrent_tasks` from 1 through 10 (new
preparations default 10), with separate UID/GID and loopback relay per task. Old installed configs missing the field keep
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

For direct `configure.py` preparation, `automatic_pr_reviews` defaults off;
container deployment templates currently default `BONSAI_AUTOMATIC_PR_REVIEWS=true`.
An installed config without the setting stays off; inspect its effective value. It schedules read-only
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
capture gaps and history-contract-v1 capacity representation limits (including
capacity 3) remain explicit. Inspect
private bundles before sharing; redaction is not publication permission, and an
export heartbeat does not prove listener liveness. Telemetry tables are additive;
preserve state/history, consumed approvals, deduplication and intents through
stopped upgrades/rollback. No source edit authorizes installation changes.
