---
name: bonsai-ci
description: Prepare and track supervised coder tasks and scoped test/documentation contributions using free-form preparation or legacy envelopes, with installed compatibility, admission and delivery checks. Use when preparing, admitting, retrying or tracking an agent issue handoff.
---

# Bonsai supervised coder and specialist assignments

Support the [root Git developer](../../../AGENTS.md). For developer-led tasks, the root developer owns application code, its branch and parent PR and delegates independent test/documentation work. For **explicitly delegated implementation**, an `agent:coder` issue is an alternative supervisor-owned writer; avoid duplicate root-developer changes on the same task/branch. This skill replaces the workspace's retired `delegate-to-deepseek` guidance without assuming a particular installed model.

## Prepare a concrete handoff

For client invocation and a copyable contribution request, use
[using skills and calling agents](../../../docs/agent-setup/calling-agents.md).
Invoking this skill loads guidance; the supervisor launches runtime roles only
after issue admission. Automatic PR review uses a separate trusted opt-in.

For an admitted coder's native `bonsai_call_agent` consultation, read
[repository consultation](../../../docs/agent-setup/repository-consultation.md).
It is a same-task read-only research route, not another issue handoff. Verify
explicit installed policy, exact-path schema-2 scope and finite token totals;
ordinary envelopes with omitted budgets do not select it. Never invent an
`agent:researcher` implementation label or enable installed policy during a handoff.

When updating the harness or checking compatibility with latest platform source,
follow [workspace updates and compatibility](../../../docs/agent-setup/compatibility.md).
Identify the owning repository and compare source and sealed-installation support
separately; validate against the intended parser revision rather than whichever
checkout happens to be active.

1. Read the target's applicable instructions and the relevant [coder](../../../agents/coding/AGENTS.md), [test](../../../agents/testing/AGENTS.md) or [documentation](../../../agents/documentation/AGENTS.md) guide. For developer-led contributions, identify the existing parent PR, exact branch and implementation commit; for coder-owned work, establish whether the requested destination is a new draft or explicitly selected existing PR.
2. Verify the worker's bound repository, sealed release and supported route. Source defaults are not installed state. Current source supports `agent:coder` for approved application code and related scoped tests/docs, `agent:test-specialist` for tests/fixtures/test configuration and `agent:documentation` for docs; retired Generalist/tests are not aliases. Coder and test-specialist have embedded read-only review; documentation does not; the advisory admin/planner/researcher roles are operator-invoked only and never admission routes. Fresh preparations now enable all harness roles plus those advisory roles with read-only defaults (`--harness-roles '[]'` and `--no-agent-harness` opt out), so verify the sealed installation's saved config rather than assuming an old default. With Docker containers, inspect the selected container's image/revision using the container skill and verify the sealed `release_root`/`enabled_profiles`; image identity alone is insufficient. Choose free-form preparation when research should establish scope/checks, or a complete legacy envelope when those are known. Keep unverified/dependent requests blocked without `ready`; a legacy installed route must be identified explicitly, never inferred from old examples.
3. Search for an existing matching issue and task/destination before creating another. For developer-led contributions use the root parent-PR context; for coder-owned work document the requested new-draft or existing-PR destination, goal, observable acceptance criteria and boundaries. Free-form issues need no executable JSON or guessed paths/checks/budgets; preparation must resolve gaps before producing an executable proposal.
4. **Bind the destination explicitly:** for a developer-led contribution or authorized update to an existing PR, free-form preparation requires operator `--target-pr NUMBER` and legacy schema 2/3 requires numeric `pull_request`. For a new coder-owned draft, omit those existing-PR selectors. A PR link or branch instruction in prose supplies context only. Read [free-form issue guidance](../../../docs/agent-setup/free-form-issues.md) for selected evidence, exclusive preparation, sealed proposal review, and release-specific admission (`admission_mode: ready` on current source, or digest-bound approval on older releases). Use [runtime and schema details](references/runtime-and-issue.md) for legacy single tasks or [plan guidance](references/plans.md) for ordered legacy steps. Schema 4 cannot select an existing PR.
5. For a legacy envelope, validate the finalized body from the workspace root (works in both PowerShell and Git Bash on Windows):

   ```sh
   py -3 tools/validate_task.py --repository xaime-vp/constant-integration --body-file path/to/issue.md
   ```

   Substitute the actual target repository and select `--platform-root` when the default checkout is stale. Parsing is offline source-schema evidence, not approval, protected-check verification or installed compatibility. This tool parses legacy envelopes only; free-form proposals are validated and sealed by preparation.
6. The root developer's code-task authorization includes its meaningful independent test/documentation issues under that workflow. A separate coder issue requires an explicitly selected supervised implementation owner. Use GitHub MCP to create or update those scoped issues without routine reconfirmation. Use exactly one verified matching route label (`agent:coder`, `agent:test-specialist` or `agent:documentation` on current source), plus `ready` only when prerequisites are satisfied. Keep proposals `blocked` and unready otherwise. The separate trusted-opt-in PR Reviewer is not an issue implementation route.

## Keep one compact handoff record

Record the target repository, PR destination, branch and current head when applicable; requested
category and exact scope; selected parser/source revision; observed installed
release/admission mode or `unknown`; check argv; and the existing issue, proposal
digest and task key when available. Return only changed facts, evidence links,
missing prerequisites and the next responsible action.

Read [the runtime decision table](references/runtime-and-issue.md#source-defaults-and-installed-decisions)
when selecting admission, capacity or review behavior. Do not reload all runtime
or container guidance for a wording-only request. Read-only review/status work
does not admit an issue. If installation evidence or a required tool is missing,
keep the handoff unready and report the exact missing observation; do not invent
a command, infer readiness from source defaults, or perform a lifecycle change.

## Execution and follow-through

Free-form preparation requires the configured owner's `/prepare-agent` request and operator `prepare-issue`. On current source (`admission_mode: ready`), once a validated proposal or finalized legacy envelope is verified, admit it by removing `blocked`, adding `ready`, and retaining the single matching implementation label (`agent:coder`, `agent:test-specialist` or `agent:documentation`); standalone and digest `/approve-agent` comments are ignored. On older sealed releases, free-form proposals still require `/approve-agent <full-digest>` and legacy envelopes require standalone `/approve-agent` after the final issue edit. Never post owner request/approval commands on their behalf or claim chat authorization satisfies runtime checks. Issue edits invalidate the prepared/ready assignment; prepared source/PR/policy changes require fresh preparation.

Test and documentation assignments targeting one PR must run sequentially because its branch is reserved. Start the second once the first has delivered or stopped and reservations are clear. Preparation itself requires a stopped listener, confirmed-stopped role processes and no active/unknown tasks or publication reservations; it does not stop a service, regardless of 1–10 configured slot capacity. For authorized lifecycle work use the current [container skill](../bonsai-containers/SKILL.md), then preparation through the selected installation's documented entrypoint; issue preparation alone does not authorize stop, restart or upgrade. If the first contribution changes the head, refresh the second issue's context and reprepare any stale sealed proposal before readiness. Workers publish through their supervisor to the approved destination (new draft or selected existing PR); do not spawn duplicate local agents or a second PR for the same assignment.

Track issue comments, branch commits and checks in this chat. Review the actual changes and delivered SHA; confirm they reached the parent branch. Record failed/unrun checks, advisory reviewer findings and exact-head target CI separately. Unknown process outcomes require supported confirmed-stop reconciliation, never erased state or replayed approval. Keep credentials and private logs out of issues.

In developer-led work the root developer fixes application bugs and integrates contributions; in a separately authorized coder task, the supervisor controls its scoped implementation and publication. Leave merge and deployment to the user unless explicitly authorized. A created issue, worker completion message or draft PR alone is not completed delivery.
