# Autonomous coder assignment

Supporting guidance for a developer preparing or reviewing a **separately authorized** `agent:coder` Bonsai issue. This file does not make the workspace's root Git developer into a Pi worker or override the sealed [source coder profile](https://github.com/xaime-vp/constant-integration/blob/main/profiles/coder.md).

## Choose the owner and destination

- **Developer-led:** the root developer opens and implements its parent PR, then uses independent `agent:test-specialist` or `agent:documentation` contributions when useful. Keep application edits with that developer.
- **Bonsai-led coder:** when implementation is explicitly delegated, create or reuse one `agent:coder` issue with observable acceptance criteria, scoped paths/extensions, and source context. The supervisor owns the isolated worktree, Git, protected checks, independent read-only review and draft PR publication. Do not run a concurrent root-developer writer on the same branch/task.
- For a new PR, omit `pull_request` in legacy schema 2/3 or leave the operator's free-form target unset; for an intentionally existing PR, use numeric `pull_request` (legacy) or operator `--target-pr NUMBER` (free-form). Schema 4 **cannot** target an existing PR and requires both trusted installation opt-in and matching approved task policy. A PR mention is not destination permission.

## Scope and protocol

The coder can implement code fixes, features, refactors and directly related tests/docs **only in approved editable scope**. The supervisor enforces exact `allowed_files`, optional `allowed_filetypes` union and project bounds. Optional `read_filetypes` restricts content reads and disables worker shell/self-checks; the supervisor still runs protected checks. Do not ask the worker to bypass controller-owned credentials, checks, frozen-source review or Git publication.

The sealed coder's concise *locate → decide → implement → verify → finish* work loop prioritizes targeted retrieval, minimal complete edits, risk-proportionate offline verification and a factual handoff. If code outside scope needs changes, capture a blocker rather than silently widening scope. No worker-controlled commit, push, publication, writer delegation or merge.

A compatible opted-in schema-2 coder can receive native `bonsai_call_agent` for
read-only repository research and continue the same task. It requires exact
paths and finite token totals; file-type write allowances, plans, foundation and
schema-4 publication enrollment do not select it. The selected coder has no shell
from first launch even without `read_filetypes`. The researcher sees a bounded
snapshot, cannot edit source or use the web, and supplies evidence rather than
scope or approval. Follow [repository consultation](../../docs/agent-setup/repository-consultation.md)
for tool use, availability, budgets and recovery limits. This is separate from
pre-admission free-form research and does not create a new implementation issue.

## Admission, verification and handoff

Check the **selected installation's** bound target, sealed release, `enabled_profiles`, model/context limits, protected commands, runtime policy, approval mode and current issue revision. Source presence is not proof of installation. Keep unverified issues `blocked` without `ready`. For free-form research, the configured owner must request `/prepare-agent`; the operator performs exclusive stopped-state preparation and inspects the sealed proposal before readiness. On current source, admit only a verified assignment with `ready`, without `blocked`, and with exactly one `agent:coder` label. Older installations may require legacy approval commands. Do not post commands as the owner.

Inspect the actual changed files, protected-check exits, embedded independent read-only Reviewer, and target CI at the **final PR head**. A created draft, model self-report, synthetic fixture or missing billing is neither merge readiness nor owner acceptance. Respect the owner's separate merge and deployment authorization.

See [current capabilities](../../docs/agent-setup/platform-capabilities.md), [Bonsai handoff skill](../../.pi/skills/bonsai-ci/SKILL.md), [legacy envelope](https://github.com/xaime-vp/constant-integration/blob/main/docs/submitting-tasks/envelope.md), and [supervised roles](https://github.com/xaime-vp/constant-integration/blob/main/docs/AGENT_ROLES.md).
