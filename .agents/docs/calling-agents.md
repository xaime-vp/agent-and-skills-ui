# Call a Bonsai agent for a UI PR

Run this workflow from the UI developer workspace in `agent-and-skills-ui` on
`main`. Application issues and PRs belong to
`xaime-vp/constant-integration-ui`; the harness branch is not their delivery branch.
The root developer implements application code and opens its parent draft PR
before requesting contributions.

## Choose and invoke a skill

In a client that supports named skill invocation, request the skill with `$name`.
Otherwise ask the client to read the linked `SKILL.md` and follow its linked
references. Start from this workspace and identify `constant-integration-ui/`
explicitly. Invocation loads guidance; it does not launch a runtime role or
authorize GitHub writes, installation changes, merging or deployment.

| Skill | Use it for | Example request |
| --- | --- | --- |
| [bonsai-ci](../skills/bonsai-ci/SKILL.md) | Prepare and track test/documentation contributions to a parent PR | `Use $bonsai-ci to prepare regression coverage for PR <URL> in xaime-vp/constant-integration-ui.` |
| [bonsai-containers](../skills/bonsai-containers/SKILL.md) | Inspect or perform requested worker lifecycle operations | `Use $bonsai-containers to inspect the installation bound to xaime-vp/constant-integration-ui and report its sealed revision and enabled profiles.` |
| [bonsai-status](../skills/bonsai-status/SKILL.md) | Read-only worker health, slot occupancy and GitHub dispatch state | `Use $bonsai-status to inspect the UI-bound worker stack.` |
| [pr-submission](../skills/pr-submission/SKILL.md) | Prepare/update the parent PR with validation and contribution evidence | `Use $pr-submission to update PR <URL> from its current diff and observed checks.` |
| [codex-cli-mcp](../skills/codex-cli-mcp/SKILL.md) | Requested local Codex CLI work and existing approved GitHub MCP connections | `Use $codex-cli-mcp for <task> in constant-integration-ui, using the already-connected GitHub tools.` |

Use connected GitHub tools directly when already available; skill invocation does
not require starting another coding client. Installation/startup and worker
approvals retain their own authorization requirements. Follow the
[root workflow](../../AGENTS.md) and the UI repository's instructions.

## Select the worker role

The external supervisor admits ready/approved GitHub issues and owns model
execution, protected checks, Git and publication. Verify sealed installed
support and target binding before choosing an executable route.

| Assignment / Role | Current source role / issue label | Delivery evidence & scope |
| --- | --- | --- |
| Add regression coverage | `agent:test-specialist` | Tests, fixtures or test configuration; protected checks and embedded read-only review |
| Document the change | `agent:documentation` | Documentation only; protected checks, no embedded model reviewer |
| Commit / candidate review | `reviewer` (no issue label) | Read-only review distinguishing substantive blockers from optional suggestions without expanding approved scope; embedded for `test-specialist` or automatic PR commit `COMMENT` when `automatic_pr_reviews: true` |
| Coordinator | `supervisor` (no issue label) | Deterministic authority, scope, freeze, termination, and honest evidence; initial front-end assignment/prompting only, no backend review role |
| Admission control | `ready` / `blocked` labels | `ready` + no `blocked` + single matching `agent:*` label admits current revision (`admission_mode: ready`) |

Do not use retired `agent:generalist`/`agent:tests` aliases, start Pi roles
directly, or spawn local subagents to duplicate an issue assignment. The
developer owns application repairs.

## Request a test or documentation contribution

Replace the bracketed values, then give the coding client this prompt:

```text
Use $bonsai-ci to create or update a [test-specialist | documentation] handoff
for xaime-vp/constant-integration-ui.

Parent PR: [URL and number]
PR base: [exact base branch]
Required delivery branch: [exact parent PR head branch]
Implementation commit: [current SHA]
Goal: [observable behavior to cover or document]
Evidence: [implementation paths, reproduction or source/PR references]
Acceptance: [edge cases/assertions for tests, or commands/examples/claims to verify for docs]
Scope and dependencies: [known candidate files, boundaries and prerequisites]

Search for an existing matching issue first. Use agent:test-specialist for tests,
fixtures and test configuration, or agent:documentation for documentation. Verify
the UI-bound sealed installation supports the selected role. Keep application
code with the developer and preserve all parent-branch commits.

Use free-form preparation when exact writable scope or protected checks need
research. Select the matching role label (agent:test-specialist or
agent:documentation) before preparation. Keep unresolved proposals blocked and
unready. Select this existing parent with --target-pr NUMBER; for a verified
legacy schema-2/3 envelope use numeric pull_request instead. On current source
(admission_mode: ready), admit verified issues/proposals by removing blocked
and adding ready (older releases require /approve-agent).

Return the issue link, selected route, verified facts, unresolved gaps and next
owner/operator action. Do not post owner preparation/approval commands for me.
Track authorized work through delivery, review the actual parent-branch diff and
report the delivered SHA, check results and exact-head GitHub CI separately.
```

For tests, request independently authored assertions for the changed behavior;
report application defects to the developer instead of widening worker scope.
For documentation, identify the intended reader and changed behavior and require
source/link/command verification. A missing embedded model review is expected for
documentation; it is not a request for another implementation issue.

## From request to execution

1. Finalize the issue, select exactly one matching implementation label and verify
   prerequisites. A label or a PR link alone does not authorize or select delivery.
2. For prose issues, the owner posts standalone `/prepare-agent` after the final
   edit. An operator runs bounded preparation with `--target-pr NUMBER` against
   the selected UI installation. Follow [the preparation procedure](free-form-issues.md)
   for committed evidence and confirmed-stopped/exclusive preparation conditions.
3. Inspect the sealed proposal: exact role, scope, checks, limits and pinned PR
   destination (`inspect-preparation KEY`), and resolve any gaps before
   execution.
4. For a complete verified legacy envelope, validate it with the
   [offline validator](../tools/README.md).
5. On current source (`admission_mode: ready`), admit the verified proposal or
   legacy envelope by removing `blocked`, adding `ready`, and retaining the
   single matching `agent:*` label (no `/approve-agent` comment is needed;
   older installed releases still require `/approve-agent <full-digest>` after
   sealing and the final edit, or standalone `/approve-agent` for a legacy
   envelope). An already authorized running listener handles admission; this
   guide does not authorize startup or upgrade.
6. Serialize tests and documentation targeting one PR. Verify delivered commits,
   refresh the second assignment after head changes, and reprepare stale sealed
   proposals. Record failed/unrun checks and applicable review evidence using
   [the handoff guide](handoff.md). Merge remains an owner decision.

## Request PR review

The automatic PR Reviewer has no issue implementation label or owner slash
command to invoke it. On a compatible installation, trusted configuration
`automatic_pr_reviews: true` enables polling of unseen commits on open PRs in its
bound repository. It defaults off. Confirm existing configuration read-only; use
the [container skill](../skills/bonsai-containers/SKILL.md) for separately
authorized configuration/lifecycle changes. Do not enable it merely because a
user requested a handoff.

With that opt-in already enabled, follow the review for the actual PR commit and
report its advisory findings. A request to fix findings becomes developer work
or a separately scoped test/documentation assignment. Do not delete review
records or reset attempts to retrigger a commit; preserve the
[retry and reconciliation rules](../skills/bonsai-ci/references/runtime-and-issue.md#automatic-commit-reviews-and-telemetry).
