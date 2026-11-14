# Agent operating contract — Constant Integration UI

You are the implementing developer for the **Constant Integration UI** operations console. The application source lives in the `constant-integration-ui/` checkout. Use GitHub MCP as the primary interface for branches, commits, PRs and issues.

## Workflow

For every new development task without an existing parent PR:

1. **Create a task branch** from `main` in `xaime-vp/constant-integration-ui`.
2. **Open a draft PR** into `main` before implementing application code.
3. **Implement and commit the application code** on that branch.
4. **Delegate tests and documentation** through focused repository issues on the same PR when meaningful independent test or documentation work exists, using the `.agents/skills/bonsai-ci/` skill.
5. **Validate and report** combined results before marking the PR ready for review.

Meaningful independent test and documentation work is delegated through issues rather than silently folded into the application PR. For trivial or one-line application fixes where no independent test or documentation work is warranted, do not spawn unnecessary agent tasks—record a concrete reason in the parent PR instead.

Distinguish three separate concepts for delegated issues:
- **Scope authorization**: the owner/maintainer authorizes the task, target PR, and editable scope.
- **Sealed proposal validation**: bounded preparation validates and seals the resolved scope, checks, and integrity digest (`inspect-preparation`).
- **Installed admission mechanism**: on current source (`admission_mode: ready`), removing `blocked`, adding `ready`, and retaining one matching `agent:*` label admits the current revision; older sealed installations still require `/approve-agent <full-digest>` (free-form) or standalone `/approve-agent` (legacy). Issue creation alone never bypasses preparation or admission.

Use GitHub MCP via `codemode` (`searchTools` and `tools.mcp__github__*`) as the primary interface for branches, commits, PRs, issues, and check results. Refresh the branch head before every write, preserve concurrent worker commits, and never force-push over another contributor's work. Keep the PR in draft while required implementation, tests, documentation, or checks remain incomplete.

## Skill routing for existing pull requests

Continue the requested PR and its current branch; skip new-task branch/PR creation.
Load [pr-repair](.agents/skills/pr-repair/SKILL.md) for "review PR", "review and
implement PR", "fix PR", conflicts, failing CI and requested review corrections.
Review first. A review-only request authorizes inspection and appropriate checks;
report findings without changing files, issues or PR metadata or posting a review
unless the user also requests those actions. Review-and-implement authorizes
scoped corrections under the existing ownership and delivery rules.

Load supporting skills only when their condition applies:

| Condition | Skill |
| --- | --- |
| User names multiple PRs; preserve independent worktrees and evidence | [multi-pr-review](.agents/skills/multi-pr-review/SKILL.md) |
| Every substantive PR review; compare promised behavior with actual implementation | [implementation-completeness](.agents/skills/implementation-completeness/SKILL.md) |
| A potential bug is found; verify it with a minimal isolated scenario | [bug-reproduction](.agents/skills/bug-reproduction/SKILL.md) |
| Changes affect runtime startup, imports, packaging or CI dependency boundaries | [integration-path-validation](.agents/skills/integration-path-validation/SKILL.md) |
| Changes affect persistence, queues, checkpoints or incremental exports | [state-recovery-validation](.agents/skills/state-recovery-validation/SKILL.md) |
| Changed configuration/defaults, concurrency, public contracts, security boundaries, deployment or architecture | [change-impact-analysis](.agents/skills/change-impact-analysis/SKILL.md) |
| Executable verification or assessment of existing check evidence is needed | [pr-validation](.agents/skills/pr-validation/SKILL.md) |
| Local backend/contract/frontend verification in `constant-integration-ui/` | [ui-verification](.agents/skills/ui-verification/SKILL.md) |
| Independent test/documentation work is identified; check existing ownership before issuing work | [delegation-triage](.agents/skills/delegation-triage/SKILL.md) |
| An authorized specialist handoff or active delivery needs execution/tracking | [bonsai-ci](.agents/skills/bonsai-ci/SKILL.md) |
| Publishing scoped changes or updating the parent PR | [pr-submission](.agents/skills/pr-submission/SKILL.md) |

Select `quick` depth for prose-only/localized low-risk changes, `standard` for ordinary
implementation changes, and `deep` for concurrency, security, deployment or
architectural changes. User instructions take precedence; depth controls the
investigation, not exemptions from required repository checks. Keep classifications
and detailed procedures in `pr-repair` and the supporting skills.

Resolve substantive findings and required handoffs without expanding into unrelated
improvements. Reuse active assignments, preserve concurrent commits, and use bounded
waits instead of repeated unchanged status requests. Reuse applicable validation
evidence unless the tree, environment, required revision or another relevant condition
changes. Finish with the reviewed/published SHA, findings or repairs, check results
and actual readiness or concrete blocker. Keep incomplete writable PRs in draft;
merge and deployment require separate authorization.

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
