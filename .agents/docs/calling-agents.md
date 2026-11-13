# Call a Bonsai agent for a UI PR

Run this workflow from the UI developer workspace in `agent-and-skills` on
`pi-constant-integration-ui`. Application issues and PRs belong to
`xaime-vp/constant-integration-ui`; the harness branch is not their delivery branch.
The root developer implements application code and opens its parent draft PR
before requesting contributions.

## Invoke the handoff skill

In a client that supports named skill invocation, use `$bonsai-ci`. Otherwise ask
the client to read [the skill](../skills/bonsai-ci/SKILL.md) and follow its linked
references. This selects preparation guidance in the coding client; it does not
launch a runtime role. The external supervisor admits approved GitHub issues and
owns model execution, protected checks, Git and publication.

Choose the assignment:

| Request | Current source role / issue label | Expected contribution |
| --- | --- | --- |
| Add regression coverage | `agent:test-specialist` | Tests, fixtures or test configuration; protected checks and embedded read-only review |
| Document the change | `agent:documentation` | Documentation only; protected checks, no embedded model reviewer |
| Review PR commits | Separate automatic PR Reviewer | Advisory commit-bound `COMMENT` review; no implementation or check execution |

Verify sealed installed support and target binding before choosing an executable
route. Do not use retired `agent:generalist`/`agent:tests` aliases, start Pi roles
directly, or spawn local subagents to duplicate an issue assignment.

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
research. Select the matching role label before preparation. Keep unresolved
proposals blocked and unready. Select this existing parent with --target-pr NUMBER;
for a verified legacy schema-2/3 envelope use numeric pull_request instead.

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
   destination. Resolve gaps before execution. The owner posts the exact returned
   `/approve-agent <full-digest>` after sealing and the final issue edit.
4. For a complete verified legacy envelope, validate it with the
   [offline validator](../tools/README.md) and use standalone owner `/approve-agent`
   after the final edit. This command cannot approve a saved prose proposal.
5. Set `ready`, remove `blocked` and retain exactly the selected matching role
   label only when prerequisites are satisfied. An already authorized running
   listener handles admission; this guide does not authorize startup or upgrade.
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
