# Shared developer workflow

The [root contract](../../AGENTS.md) selects the application repository and client
delivery policy. Target instructions govern its code. These developer procedures
do not broaden supervised worker permissions or change installed admission.

## Choose ownership and scope

The developer owns application code, tightly coupled regression tests, fixtures,
test configuration and small documentation updates within the authorized task.
Choose a specialist for substantial independent coverage or documentation,
specialist expertise, or an explicit user assignment. Do not create an issue just
to separate file types. Never overlap an active assignment's write scope.

An explicitly delegated `agent:coder` is an alternative implementation owner.
Its supervisor selects scope, checks, review, Git and publication; it can change
related tests/docs only within that approved scope. See [coder guidance](../../agents/coding/AGENTS.md).

## New developer-led task

1. Inspect the selected repository, instructions, existing branches, PRs and work.
2. Create a task branch from the intended base. Preserve unrelated local changes.
3. Implement and validate a meaningful initial change, including related tests or
   documentation, and commit it. A documentation-only task can start with its
   actual documentation change.
4. Open a draft PR once that meaningful difference exists. Do not add planning
   files or empty commits merely to satisfy GitHub's branch-difference requirement.
5. Open the parent PR before dispatching any specialist whose contribution must
   target it. Record its exact repository, head branch and implementation SHA.
6. Integrate delivered contributions, inspect the combined diff and validate the
   final head. Keep required unfinished work in draft.

## Existing PR, review and completion

Reuse the existing PR branch; use an isolated worktree when local work conflicts.
Review-only means no edits, issues, metadata changes or posted reviews. Use
[pr-repair](../../.pi/skills/pr-repair/SKILL.md) for authorized corrections and
[pr-validation](../../.pi/skills/pr-validation/SKILL.md) for appropriate checks.
Choose quick investigation for localized prose, standard for ordinary changes,
and deep for concurrency, security, persistence or deployment. Depth does not
waive required target checks.

Use [pr-completion](../../.pi/skills/pr-completion/SKILL.md) for completion or
readiness. Discover available agent/tool capabilities rather than assuming a
particular client's API. A client root may require asynchronous handoff and one
status inspection instead of waiting; that stopping rule overrides supporting
skills. Always distinguish delivered work, pending workers and verified readiness.
Use [pr-submission](../../.pi/skills/pr-submission/SKILL.md) for publication.

## Optional specialist work

Use [delegation triage](../../.pi/skills/delegation-triage/SKILL.md) before creating
an assignment. Reuse matching delivered or active work. Tests and documentation
may be prepared when their inputs are stable; documentation need not wait for all
tests unless it depends on their results. Serialize writes to the same PR branch
under the selected worker's reservation protocol. A dependent assignment can be
prepared as guidance without admitting a competing writer.

Use [test](../../agents/testing/AGENTS.md), [documentation](../../agents/documentation/AGENTS.md)
and [Bonsai handoff](../../.pi/skills/bonsai-ci/SKILL.md) guides only for actual
specialist assignments. Verify the bound installation, sealed release, role,
scope, protected checks and admission mode before dispatch. Source features,
issue creation and a model's report are not execution authority.

## Validation and reporting

Use relevant repository checks and inspect current-head CI. Report exact commands,
observed outcomes, unrun checks and pending work. Never weaken tests for a green
result or treat a closed issue as proof that its commit reached the parent branch.
Do not merge, deploy or operate a worker as incidental validation.

## Required issue handoff

Search for an existing issue for the same task, category, and branch before creating a new one. Reuse it when appropriate to avoid triggering duplicate workers.

Select exactly one matching route label (`agent:test-specialist` or `agent:documentation`), initially **`blocked` without `ready`** until scope, protected checks, current issue revision, target PR and installed compatibility are verified. Free-form issues need an owner's `/prepare-agent`, stopped-state operator preparation and proposal inspection; legacy envelopes need installed-parser/policy validation. On current source, admit only a verified current proposal/envelope by removing `blocked` and adding `ready` with that role label; older installed releases may still require route-specific owner `/approve-agent`. Do not impersonate the owner or infer approval from chat. Serialize test/documentation work targeting one PR.

Include the assignment context below for either route. **For a legacy schema-2/3 envelope only**, include one fenced `agent-task` JSON block with numeric `pull_request` selecting the existing parent PR, and validate it offline with `py -3 tools/validate_task.py --repository <owner/repo> --body-file <file>`. A free-form issue uses prose and later sealed preparation **without** an author-written JSON envelope:

```markdown
## Assignment
Type: Tests | Documentation
Repository: <owner/repo>
Parent PR: <URL>
PR base branch: <base branch>
Working branch / required delivery branch: <exact branch name>
Implementation commit: <SHA>

## Objective and scope
<What to change, why, and the relevant files or interfaces.>

## Acceptance criteria
- <Concrete, observable requirement.>
- <Required verification and expected result.>

## Delivery instructions
Start from the current head of the working branch named above.
Contribute changes back to that same branch so they appear in the parent PR.
Do not commit to the PR base branch or the repository default branch.
Keep changes within the assigned test or documentation scope.
Preserve commits made by the parent developer and other workers.
Report the delivered commit SHA, changed files, and verification results here.
```

**Legacy-envelope example only:** include exactly one fenced `agent-task` JSON block and validate against the matching platform source and installed checks. Do **not** include this block for a free-form issue:

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

Link any specialist assignments actually used from the parent PR. Creating these task-related issues is part of this developer workflow; do not ask for routine reconfirmation once the user has authorized the code task. Use repository automation for these handoffs rather than spawning a duplicate local subagent for the same assignment.

## 5. Integrate, validate, and report

- Monitor the issues, worker responses, branch commits, and PR checks until the delegated work is delivered or a concrete blocker requires user input.
- Review the actual contributed diff. An issue being closed or a worker claiming completion is not proof that changes reached the correct branch.
- Refresh the branch head before every write. Preserve concurrent worker commits, serialize overlapping file changes, and retry stale writes against the latest head. Never force-push over another contributor's work.
- Run or inspect the appropriate tests and CI checks for the final combined branch. If execution is unavailable, state exactly what was and was not verified.
- When the change touches this workspace's own skills, prompts, extensions, links or MCP configuration, run `python3 tools/harness_check.py`, `python3 -m unittest discover -s tools/tests -p 'test_*.py'` and the extension tests before publishing; a warning is advisory, an error is not. See the harness self-checks guide for pinned dependencies and Windows commands.
- Keep the PR in draft while required implementation, tests, documentation, or checks remain incomplete. Do not report completion merely because issues were created.
- Once the combined work meets acceptance criteria, update the PR with the implemented behavior, linked issues, delivered contributions, and validation evidence, and mark it ready for review.
- Report the PR URL, working branch, test and documentation issue URLs, validation outcome, and any unresolved blockers.
- Leave merging into the base branch and deployment to the user unless explicitly authorized.

## GitHub MCP is the primary interface

Use the connected GitHub MCP tools for repository reads, branches, commits, PRs, issues, and check results. Discover available tools as needed. In `codemode`-based clients (such as Pi), discover and invoke GitHub MCP operations via `codemode` (`searchTools` and `tools.mcp__github__*`). Use a local checkout when needed for execution or validation, while keeping the external repository and working branch as the source of truth. Never claim a remote action succeeded without a confirming tool result. If a required MCP capability is unavailable, explain the limitation and use an available authorized fallback without changing the branch, PR, or issue workflow.
