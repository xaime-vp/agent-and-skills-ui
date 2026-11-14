# Agent operating contract — Constant Integration UI

You are the implementing developer for the **Constant Integration UI** operations console. The application source lives in the `constant-integration-ui/` checkout. Use GitHub MCP as the primary interface for branches, commits, PRs and issues.

## Workflow

For every code change:

1. **Create a task branch** from `main` in `xaime-vp/constant-integration-ui`.
2. **Open a draft PR** into `main` before implementing application code.
3. **Implement the application code** on that branch.
4. **Delegate tests and documentation** through focused repository issues on the same PR, using the `.agents/skills/bonsai-ci/` skill.
5. **Validate and report** combined results before marking the PR ready for review.

## Worker roles

Current platform source uses `agent:test-specialist` for tests, fixtures and test
configuration, and `agent:documentation` for documentation. Application code stays
with the root developer. Select exactly one matching issue label before free-form
preparation seals a proposal; Generalist/tests are retired source routes, not
aliases. Verify the UI-bound installation's sealed release and enabled profiles
before selecting an executable route.

For the client invocation, request template and owner/operator sequence, follow
[calling an agent](.agents/docs/calling-agents.md). Use `$bonsai-ci` where the
client supports it, or read its `SKILL.md`; the supervisor launches runtime roles
only after issue admission. When writing an executable issue, include **one** fenced `agent-task` JSON block in the issue body and validate it offline with `py -3 .agents/tools/validate_task.py --repository <owner/repo> --body-file <file>`:

````markdown
```agent-task
{
  "schema_version": 2,
  "project": "workspace",
  "role": "agent:test-specialist | agent:documentation",
  "capabilities": ["coding", "tests"],
  "complexity": 2,
  "risk": "low | medium | high",
  "goal": "<Concise objective for the worker>",
  "allowed_files": ["<exact writable test or doc path>"],
  "acceptance_commands": [["python", "tools/check.py"]],
  "verification_plan": "<Checks to run and evidence to report>",
  "provider": "openrouter",
  "timeout_seconds": 1800,
  "pull_request": 123
}
```
````

Use `"capabilities": ["coding"]` for `agent:documentation`, set numeric `pull_request` to the existing parent PR number, and keep `timeout_seconds` within controller policy (e.g. `1800`).

On current source (`admission_mode: ready`), verified proposals and legacy
envelopes are admitted by removing `blocked`, adding `ready`, and retaining the
single matching `agent:*` label (older sealed releases still require
`/approve-agent`). For safe workspace updates and release-specific compatibility
checks, follow [compatibility](.agents/docs/compatibility.md).

Test-specialist contributions receive embedded read-only review. Documentation
contributions publish without a model reviewer. Both retain protected checks,
exact scope and route-specific owner approval. Keep assignments to one parent PR
sequential and verify their actual delivered commits. See the
[handoff guide](.agents/docs/handoff.md) and
[issue preparation](.agents/docs/free-form-issues.md).

Source supports 1/2/3 shared slots; a missing configuration setting retains one.
The separate trusted-opt-in automatic PR Reviewer shares that capacity and emits
commit-bound advisory `COMMENT` reviews. It runs no checks and grants no task
approval, repair or merge authority. Source support does not prove installation
or complete export/UI capture of a capability.

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
| `.agents/skills/` | Agent skills for CI delegation, containers, status, Codex CLI, PR repair, PR submission and UI verification |
| `.agents/tools/` | Offline validators and process counters |
| `.agents/docs/` | Prompting, handoff and free-form issue guidance |
| `constant-integration-ui/` | Application checkout (separate repository, ignored here) |

Use the skills and tools from the workspace root. Do not commit credentials, local MCP config or worker state.
