# Runtime discovery and task schema

Verify model, repository binding, protected checks and listener status when used.
This workspace does not assume a previously used target, engine or model is current.

- Platform repository: `xaime-vp/constant-integration`.
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

Copy this shape, replacing every example with the actual task. The acceptance
command below is illustrative; use it only if it exactly matches the protected
check configuration for that project. Do not dispatch an unadapted example.

````markdown
```agent-task
{
  "schema_version": 2,
  "project": "example-project",
  "role": "agent:generalist",
  "capabilities": ["coding", "tests"],
  "complexity": 1,
  "risk": "low",
  "goal": "Fix the parser's empty-input error without changing other behavior.",
  "allowed_files": ["src/parser.py", "tests/test_parser.py"],
  "acceptance_commands": [["python", "-m", "unittest", "discover", "-s", "tests", "-v"]],
  "verification_plan": "Run protected checks once in the generalist workspace and record actual exits; check target CI separately.",
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
- The observed generalist profile accepts complexity up to 3 and rejects high
  risk. Timeout and any explicit token limits must fit installed policy. On a
  compatible release, omitted `input_tokens`/`output_tokens` use automatic model
  context and no per-task response cap; provider/model limits still apply. The
  example assumes that support. Older releases may require explicit fields.
- For the root developer's test/documentation handoffs, include numeric
  `pull_request` for the existing open same-repository parent PR. Omitting it
  starts from the default branch and creates an unwanted separate draft.
  Only omit it for an explicitly requested independent new task.
- Generalist is the only implementation route, including documentation.
  Retired docs-writer, Codex and verifier roles are not dispatchable. The only
  platform roles are generalist, reviewer and supervisor.
- Required labels: `ready`, exactly one supported implementation profile.
  Required separate legacy owner comment: `/approve-agent` for generalist. Approval
  must be strictly after the issue's latest revision; same timestamps fail
  closed. A new issue revision or consumed approval may require a fresh comment.
  This standalone approval cannot approve a saved free-form proposal.

New runtime preparations support `max_concurrent_tasks` of 1 or 2, with separate
UID/GID and loopback relay per task. Old installed configs missing the field keep
one slot. Confirm actual installed state. Conflicting scopes/issues/PR branches
wait; keep semantic dependencies and shared external resources blocked/unready.

## Completion evidence

Record the issue, approval ID, installed release revision, task key, candidate
identity, generalist check commands/exits, reviewer verdict, draft PR
link/head, and target CI result. Keep unavailable evidence explicitly unknown.
If a reviewer report is malformed or contradicts itself, it remains inconclusive
even when the implementation and generalist checks succeeded.
