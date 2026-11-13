---
name: bonsai-ci
description: Prepare and track issue-driven test or documentation contributions to the root developer's existing PR through the Bonsai worker. Use for scoped task handoffs and offline envelope validation; owner approval and installed compatibility remain required.
---

# Bonsai contributions to the parent PR

Support the [root Git developer](../../../AGENTS.md). The developer owns application code, the working branch and parent PR. Repository issues delegate tests and documentation to the external Bonsai supervisor. This skill replaces the workspace's retired `delegate-to-deepseek` guidance without assuming a particular installed model.

## Prepare a concrete handoff

1. Read the target's applicable instructions and the relevant [test](../../../agents/testing/AGENTS.md) or [documentation](../../../agents/documentation/AGENTS.md) guide. Identify the existing parent PR, exact working branch and current implementation commit.
2. Verify the worker's bound repository, sealed release, supported envelope schemas, protected checks and limits. Source defaults are not installed state. Read [runtime and schema details](references/runtime-and-issue.md) only when needed. If required facts are unavailable, create or retain a clearly blocked proposal without `ready` and report what is missing.
3. Search for an existing issue for this PR/category before creating another. Use the root issue template plus exactly one fenced `agent-task` JSON block. Select `agent:generalist`, exact editable test/documentation paths, observed acceptance-command argv arrays, goal, verification plan and installed resource bounds.
4. **Set numeric `pull_request` to the parent PR number** in the envelope. A PR link or branch instruction in prose cannot route publication. Use schema 2 for a single assignment, or a verified schema-3 plan when ordered steps are appropriate. The current schema-4 parser disallows `pull_request`; do not select it for this existing-PR workflow. Read [plan guidance](references/plans.md) when needed.
5. Validate the finalized body from the workspace root:

   ```powershell
   py -3 tools/validate_task.py --repository xaime-vp/constant-integration --body-file path/to/issue.md
   ```

   Substitute the actual target repository. Parsing is offline source-schema evidence, not approval, protected-check verification or installed compatibility.
6. The user's code-task authorization includes its required test/documentation issues under the root contract. Use GitHub MCP to create or update those scoped issues without routine reconfirmation. Use verified routing labels; for Bonsai these are `agent:generalist` plus `ready` only when prerequisites are satisfied. Keep proposals `blocked` and unready otherwise.

## Execution and follow-through

The installed runtime requires a standalone `/approve-agent` comment from the configured owner after the final issue edit. Never post it on the owner's behalf, treat a label as approval, or claim ordinary chat authorization satisfies that runtime check. Report a missing runtime approval as the concrete next owner action after preparing the complete issue. Do not edit an approved issue body without accounting for approval invalidation.

Test and documentation assignments targeting one PR must run sequentially because its branch is reserved. Start the second once the first has delivered or stopped and reservations are clear. If the first contribution changes the head, revalidate the second issue's starting context before approval. Workers publish through their supervisor to the selected existing PR; do not spawn duplicate local agents or create a second PR for the same assignment.

Track issue comments, branch commits and checks in this chat. Review the actual changes and delivered SHA; confirm they reached the parent branch. Record failed/unrun checks, advisory reviewer findings and exact-head target CI separately. Unknown process outcomes require supported confirmed-stop reconciliation, never erased state or replayed approval. Keep credentials and private logs out of issues.

The root developer fixes application bugs and integrates contributions. Leave merge and deployment to the user unless explicitly authorized. A created issue, worker completion message or draft PR alone is not completed delivery.
