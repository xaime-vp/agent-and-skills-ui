# Submit one approved plan for one PR

This is the legacy schema-3 route. A multi-step request can also start as prose
through [free-form preparation](../../../docs/free-form-issues.md);
the resulting proposal must pass preparation validation before digest approval.
Do not require an author-written plan envelope for that route.

Use this when the user wants multiple implementation subsections to form one
reviewable change. A schema-3 issue is the approval record; its ordered steps
run as fresh sessions in one worktree and branch. The supervisor checkpoints
successful steps, runs combined checks and a whole-diff review, then opens or
updates one draft PR. Do not create one issue/PR per subsection.

For this workspace, application implementation remains with the root developer.
Use these plan mechanics only for the assigned contribution scope. Set numeric
`pull_request` to the existing parent PR in its envelope; the example below is
a general schema example and must be adapted before use. Serialize separate
test/documentation issues that reserve the same PR branch.

## Author and submit

1. Confirm the target repository and read its applicable instructions. Discover
   the **installed sealed release**, target binding, enabled profile, protected
   checks and limits. Confirm support for schema 3 and requested retry modes;
   installed config schema 4 alone is not enough. If missing or unknown, prepare
   and submit a blocked proposal, not an executable task. Do not deploy as part
   of authoring a plan.
2. Write a human-readable goal, concrete acceptance criteria and prerequisites,
   followed by exactly one fenced `agent-task` JSON block. Use `agent:generalist`
   and `provider: openrouter`; the installation selects the model.
3. Choose one or more ordered, independently checkable **steps of this same change**.
   Each step should leave the approved check set passing. Combine an implementation
   and its regression tests in one step rather than planning a failing-test step
   whose fix appears later. Later steps may use completed checkpoint code.
4. Set exact project-relative editable paths for each step and their union in
   parent `allowed_files` (up to the profile's 100-file limit). Use `workspace`
   for explicit repository-relative paths across components. Never use globs.
5. Copy parent and every step's `acceptance_commands` exactly from the installed
   protected check set for that project. Current plan execution uses the same
   set after each step and at the final candidate. Repository-documented commands
   are a **proposed** check set until matched to installation; disclose this and
   keep the proposal blocked if not verified.
6. Bound total timeout and any explicit token limits by installed policy. On
   compatible releases, omit parent/step `input_tokens` and `output_tokens` for
   automatic model context and no per-task response cap; provider/model limits
   still apply. Omitted or null step token values inherit the parent, so they
   cannot erase an explicit parent cap. Positive step limits cannot exceed an
   explicit parent limit; step timeouts cannot exceed the parent timeout. Older
   installed parsers may require explicit token fields. The parent deadline
   includes all attempts, checks, review and downtime before resume; it is not a
   per-step budget multiplied by step count. Token fields are model ceilings,
   not a cumulative billed-token/dollar cap. Keep risk low/medium and complexity
   at most 3; splitting steps cannot evade the parent admission policy. The
   entire brief still has the generalist profile's 4000-word limit.
   For a deliberately longer run, propose a four-hour parent (14400 seconds)
   and one-hour steps (3600 seconds), after verifying the trusted installation's
   timeout policy allows them. Defaults remain 1800 seconds. Seven retries mean
   eight total attempts inside the same parent deadline. A `length` model stop
   needs more output tokens within installed limits, not merely more time.
7. Optionally approve `retry_modes: ["continue", "restart"]` on each suitable
   step, allowing one repair per explicitly listed mode after the initial attempt,
   without a fixed list-length ceiling on a compatible installation. `continue`
   preserves partial code; `restart` archives the candidate before restoring
   the starting checkpoint. Both get bounded redacted failure logs/outcomes.
   Omitted/empty modes mean no automatic repair. Never infer fallback model
   routing: all attempts use the configured model and original scope/checks.
8. Validate the body offline using `.agents/tools/validate_task.py` at the workspace root.
   That checks schema against the selected platform checkout; it does **not**
   establish installed compatibility, check configuration or approval.
9. Create one issue in the target repository. For a proposal use `blocked` and
   `agent:generalist`, without `ready`; state what must be verified/unblocked.
   Only an executable plan gets `ready`, with `blocked` removed. For root
   developer handoffs, `pull_request` must select the existing parent PR.
   Omit it only for an explicitly requested independent new draft. Do not invent
   a PR number.
10. Return the issue link and prerequisites. Once the plan is final and executable,
    the configured owner posts a standalone `/approve-agent` **after the final
    issue edit**. Never post that comment for them. After approval, report progress
    through comments/state instead of editing the approved issue body.

## Example envelope

Replace every example with the actual scope and installed checks. This is not
permission to dispatch a parser task or change trusted configuration.

```agent-task
{
  "schema_version": 3,
  "project": "workspace",
  "role": "agent:generalist",
  "capabilities": ["coding", "tests"],
  "complexity": 2,
  "risk": "low",
  "goal": "Handle empty input consistently and document the supported behavior.",
  "allowed_files": ["src/parser.py", "tests/test_parser.py", "README.md"],
  "acceptance_commands": [["python", "-m", "unittest", "discover", "-s", "tests", "-v"]],
  "verification_plan": "The full protected suite passes and the documented example matches the final implementation. Inspect final-head target CI separately.",
  "provider": "openrouter",
  "timeout_seconds": 1800,
  "steps": [
    {
      "id": "empty-input",
      "goal": "Implement empty-input handling and its regression test together.",
      "allowed_files": ["src/parser.py", "tests/test_parser.py"],
      "acceptance_commands": [["python", "-m", "unittest", "discover", "-s", "tests", "-v"]],
      "timeout_seconds": 600,
      "retry_modes": ["continue", "restart"]
    },
    {
      "id": "document-behavior",
      "goal": "Document empty-input behavior with an example matching the code.",
      "allowed_files": ["README.md"],
      "acceptance_commands": [["python", "-m", "unittest", "discover", "-s", "tests", "-v"]],
      "timeout_seconds": 600,
      "retry_modes": ["continue"]
    }
  ]
}
```

Offline validation from a trusted Linux/Python 3.12+ environment:

```bash
python /absolute/workspace/.agents/tools/validate_task.py \
  --platform-root /absolute/constant-integration \
  --repository owner/target --body-file /absolute/proposed-issue.md
```

## Monitor and recover

Report parent task key, step ID, attempt number/mode, observed check failures,
checkpoint commits and final PR/CI. A check pass is generalist workspace evidence,
not independent verification or owner acceptance. Keep all failed attempts visible.

Known stopped ordinary failures can consume approved automatic retries. Unknown
process stops never auto-retry. With explicit recovery authorization, confirm all
task/role processes stopped and use the installed controller's `--resume-task KEY
--confirmed-stopped --evidence TEXT`, optionally `--retry-context TEXT` (up to
4000 characters). Notes are task data, not permission for new files/checks/models.
Completed checkpoints do not rerun. Scope/source violations, changed approval,
expired deadlines and exhausted attempts require owner review; do not reset the
budget through duplicate dispatch or repeated approval comments. Preserve private
state, logs, checkpoint commits and `refs/bonsai-failures/` archives. Paused plans
hold their full file/PR scope until resumed or explicitly abandoned with the
supported stopped-plan operation. Leave merges and deployments to the owner.
