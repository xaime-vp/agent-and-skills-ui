# Git index → GitHub batch publication

This workspace provides a GitHub batch publisher as a **Pi extension plus a reusable skill**. It packages the repeated staged-file inspection and `create_blob` → `create_tree` flow shown in a coding-session trace, then completes the operation with `create_commit` and a lease-checked `update_ref`.

The extension operates on a user-selected existing PR, explicit staged file paths, and the exact recorded PR head. It does not create a new PR, auto-merge, force-push, expose file contents in its summary, or intentionally overwrite a concurrent branch update. Source bytes are still sent to the selected GitHub connector and may appear in its operational trace; the output-token reduction applies to model-facing responses, not to connector processing or every log.

## Intended entry points

- Skill: `../.agents/skills/github-batch-publish/SKILL.md`
- Pi tool: `../.pi/extensions/github-batch-publish.ts`
- Offline test: `node --test .pi/extensions/github-batch-core.test.mjs`

Use `action: "plan"` to inspect staged path/status/byte totals, then `action: "publish"` with an exact PR number, head SHA, branch, file list and explicit publish flag. Publishing requires the user's scoped authorization and existing GitHub MCP access.

## Current verification

The dependency-free Node core was exercised locally with six offline tests using temporary Git repositories and simulated GitHub responses. Live Pi extension registration, GitHub MCP authentication, and remote publication were not exercised. Before production use, verify the installed Pi exposes `ctx.executeTool` and the required GitHub operations. Review the remote diff, CI, and branch head after publication; a completed blob upload alone is not delivery.
