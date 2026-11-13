# Task preparation reference

Use the target repository's own issue template and instructions. These links
provide the authoritative Constant Integration formats:

For workspace handoffs, follow the root developer contract. Free-form issues
need no executable envelope: use [preparation and digest approval](../../../../docs/agent-setup/free-form-issues.md)
with operator-selected `--target-pr NUMBER`. For legacy envelopes, set numeric
`pull_request` to the existing parent PR and validate with `tools/validate_task.py`
from the workspace root. Test and documentation issues remain separate,
sequential assignments delivered to that PR.

- [Prompt cookbook](../../../../docs/agent-setup/prompting.md)
- [Free-form operator contract](https://github.com/xaime-vp/constant-integration/blob/main/docs/submitting-tasks/free-form.md)
- [Task submission](https://github.com/xaime-vp/constant-integration/blob/main/docs/SUBMITTING_TASKS.md)
- [Single-task envelope](https://github.com/xaime-vp/constant-integration/blob/main/docs/submitting-tasks/envelope.md)
- [Plan and recovery guidance](https://github.com/xaime-vp/constant-integration/blob/main/docs/submitting-tasks/plans.md)
- [Plan issue template](https://github.com/xaime-vp/constant-integration/blob/main/.github/ISSUE_TEMPLATE/agent-plan.md)

## Single task or plan?

Choose one schema-2 task for one implementation run. Choose one schema-3 plan
only when dependent bounded steps form one coherent change and one PR. Each plan
step needs exact editable files and the same verified protected check set; each
step should leave that check set passing. Do not use multiple issues or plan
steps to bypass approval, task limits, or dependencies.

## Legacy schema summary (offline fallback)

If the links above are unreachable, use these top-level `agent-task` envelope
keys (verify exact values against the target installation):

- **Schema 2 (single task):** `schema_version: 2`, `project`, `capabilities`,
  `complexity`, `risk`, `role`, `goal`,
  `allowed_files`, `acceptance_commands`, `verification_plan`, `provider`,
  `timeout_seconds` (plus optional `pull_request`, `input_tokens`, `output_tokens`
  on a compatible release).
- **Schema 3 (ordered plan):** `schema_version: 3`, same top-level fields plus
  `steps` (`id`, `goal`, `allowed_files`, `acceptance_commands`, `timeout_seconds`,
  optional `retry_modes` and token fields on a compatible release).
- **Schema 4 (opted-in post-publication repair):** `schema_version: 4`, same
  top-level fields plus `post_publication` (`schema_version`, `enabled`, and
  optional limits); `steps` is optional, and `pull_request` is disallowed.

All other listed fields remain required in legacy JSON. Repository and issue
identity come from trusted policy/GitHub; do not add identity or unknown fields.
Omitted token fields use automatic model context/no per-task response cap;
provider/model limits still apply. Omitted or null step token values inherit the
parent values. Older parsers may require explicit token fields; verify the source
revision used for validation separately from the installed sealed release.

## Minimum issue content

- **Goal:** observable final behavior and user benefit.
- **Evidence:** reproduction, current behavior, relevant source/CI references;
  redact credentials and private logs.
- **Scope:** target repository, known files, dependencies, and non-goals. A PR
  mention is not an enforced scheduler dependency.
- **Acceptance:** behavior and regression case, plus protected check commands
  copied from the installed target configuration for legacy execution, or
  resolved by free-form preparation (not guessed from a local checkout).
- **Verification:** distinguish worker checks, reviewer findings, exact-head
  target CI, and owner acceptance.

Unknown installed support, target binding, protected checks or dependencies means
blocked and without `ready`. A generated envelope is only a proposal; the
configured owner must verify and approve the final issue or sealed proposal using
the selected route's command. Free-form research may resolve missing scope/check
details before sealing; unresolved gaps prevent a proposal. Do not post owner
request/approval commands on their behalf.
