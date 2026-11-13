---
name: bonsai-ci
description: Prepare and track Bonsai test or documentation contributions to an existing parent PR, using free-form issue preparation or legacy executable envelopes. Verify installed compatibility, delivery and route-specific owner approval.
---

# Bonsai contributions to the parent PR

Support the [root Git developer](../../../AGENTS.md). The developer owns application code, the working branch and parent PR. Repository issues delegate tests and documentation to the external Bonsai supervisor. This skill replaces the workspace's retired `delegate-to-deepseek` guidance without assuming a particular installed model.

## Prepare a concrete handoff

For a client invocation and copyable UI contribution request, use
[calling an agent](../../docs/calling-agents.md). Skill invocation selects this
guidance; runtime execution still requires supervisor admission of the approved
issue. Automatic PR reviews use a separate trusted opt-in, not an issue role.

1. Read the target's applicable instructions and the relevant [test or documentation handoff guide](../../docs/handoff.md). Identify the existing parent PR, exact working branch and current implementation commit.
2. Verify the worker's bound repository, sealed release and supported route. Source defaults are not installed state. Current source uses `agent:test-specialist` for tests/fixtures/test configuration and `agent:documentation` for documentation; retired Generalist/tests are not aliases. Test-specialist work includes embedded read-only review; documentation does not. On Windows with Podman-in-WSL, inspect the selected container's image/revision using the container skill and verify the sealed `release_root`/`enabled_profiles`; image identity alone is insufficient. Choose free-form preparation when research should establish scope/checks, or a complete legacy envelope when those are known. Keep unverified/dependent requests blocked without `ready`; a legacy installed route must be identified explicitly, never inferred from old examples.
3. Search for an existing issue for this PR/category before creating another. Use the root assignment context, goal, observable acceptance criteria and boundaries. Free-form issues need no executable JSON or guessed paths/checks/budgets; preparation must resolve gaps before producing an executable proposal.
4. **Select the existing parent PR through the chosen route:** free-form preparation requires the operator's `--target-pr NUMBER`; legacy schema 2/3 requires numeric `pull_request`. A PR link or branch instruction in prose supplies context only. Read [free-form issue guidance](../../docs/free-form-issues.md) for selected evidence, exclusive preparation, sealed proposal review and digest-bound owner approval. Use [runtime and schema details](references/runtime-and-issue.md) for legacy single tasks or [plan guidance](references/plans.md) for ordered legacy steps. Schema 4 cannot select an existing PR.
5. For a legacy envelope, validate the finalized body from the workspace root (works in both PowerShell and Git Bash on Windows):

   ```sh
   py -3 .agents/tools/validate_task.py --repository xaime-vp/constant-integration-ui --body-file path/to/issue.md
   ```

   Substitute the actual target repository and select `--platform-root` when the default checkout is stale. Parsing is offline source-schema evidence, not approval, protected-check verification or installed compatibility. This tool parses legacy envelopes only; free-form proposals are validated and sealed by preparation.
6. The user's code-task authorization includes its required test/documentation issues under the root contract. Use GitHub MCP to create or update those scoped issues without routine reconfirmation. Use exactly one verified matching route label (`agent:test-specialist` or `agent:documentation` on current source), plus `ready` only when prerequisites are satisfied. Keep proposals `blocked` and unready otherwise. The separate trusted-opt-in PR Reviewer is not an issue implementation route.

## Execution and follow-through

Free-form preparation requires the configured owner's `/prepare-agent` request and, once a validated proposal is sealed, the exact returned `/approve-agent <full-digest>` command. Legacy envelopes require standalone `/approve-agent` after the final issue edit. Standalone legacy approval cannot approve a saved proposal. Never post owner request/approval commands on their behalf, treat labels as approval, or claim chat authorization satisfies runtime checks. Prepare the concrete issue/proposal before reporting a missing owner action. Issue edits invalidate the approved assignment; prepared source/PR/policy changes require fresh preparation and approval.

Test and documentation assignments targeting one PR must run sequentially because its branch is reserved. Start the second once the first has delivered or stopped and reservations are clear. Preparation itself requires a stopped listener, confirmed-stopped role processes and no active/unknown tasks or publication reservations; it does not stop a service, regardless of 1/2/3 capacity. For authorized lifecycle work use the current [container skill](../bonsai-containers/SKILL.md), then preparation through the selected installation's documented entrypoint; issue preparation alone does not authorize stop, restart or upgrade. If the first contribution changes the head, refresh the second issue's context and reprepare any sealed proposal before approval. Workers publish through their supervisor to the selected existing PR; do not spawn duplicate local agents or create a second PR for the same assignment.

Track issue comments, branch commits and checks in this chat. Review the actual changes and delivered SHA; confirm they reached the parent branch. Record failed/unrun checks, advisory reviewer findings and exact-head target CI separately. Unknown process outcomes require supported confirmed-stop reconciliation, never erased state or replayed approval. Keep credentials and private logs out of issues.

The root developer fixes application bugs and integrates contributions. Leave merge and deployment to the user unless explicitly authorized. A created issue, worker completion message or draft PR alone is not completed delivery.
