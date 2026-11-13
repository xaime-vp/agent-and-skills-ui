# Agent operating contract — Constant Integration UI

You are the implementing developer for the **Constant Integration UI** operations console. The application source lives in the `constant-integration-ui/` checkout. Use GitHub MCP as the primary interface for branches, commits, PRs and issues.

## Workflow

For every code change:

1. **Create a task branch** from `main` in `xaime-vp/constant-integration-ui`.
2. **Open a draft PR** into `main` before implementing application code.
3. **Implement the application code** on that branch.
4. **Delegate tests and documentation** through focused repository issues on the same PR, using the `.agents/skills/bonsai-ci/` skill.
5. **Validate and report** combined results before marking the PR ready for review.

## Boundaries

- Read [`constant-integration-ui/AGENTS.md`](constant-integration-ui/AGENTS.md), [`constant-integration-ui/docs/ARCHITECTURE.md`](constant-integration-ui/docs/ARCHITECTURE.md) and [`constant-integration-ui/docs/DEVELOPMENT.md`](constant-integration-ui/docs/DEVELOPMENT.md) before editing.
- The UI reads validated, sanitized export bundles. It does not query the worker's private state database or credential store.
- Do not start, retry, cancel, approve or publish worker tasks from UI code.
- Keep UI-owned data and artifact volumes separate from the worker's private state.
- Never expose the Docker socket, shell terminal, worker credentials or an arbitrary file browser.
- Use the shared-secret access gate responsibly; loopback binding is not full authentication.

## Workspace layout

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | This operating contract |
| `.agents/skills/` | Agent skills for CI delegation, containers, status, Codex CLI, PR repair and PR submission |
| `.agents/tools/` | Offline validators and process counters |
| `.agents/docs/` | Prompting, handoff and free-form issue guidance |
| `constant-integration-ui/` | Application checkout (separate repository, ignored here) |

Use the skills and tools from the workspace root. Do not commit credentials, local MCP config or worker state.
