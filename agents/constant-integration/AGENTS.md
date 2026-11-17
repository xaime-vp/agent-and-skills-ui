# Constant Integration development guide

Supporting instructions for the [root Git developer](../../AGENTS.md). The source checkout is [constant-integration](https://github.com/xaime-vp/constant-integration/blob/main/README.md); run repository commands there unless using a workspace launcher. This guide adapts the repository's original agent contract for the surrounding developer workspace.

## Read by affected component

- [Repository README](https://github.com/xaime-vp/constant-integration/blob/main/README.md) and [use cases](https://github.com/xaime-vp/constant-integration/blob/main/USE_CASES.md): current behavior and priorities.
- [Worker README](https://github.com/xaime-vp/constant-integration/blob/main/workers/bonsai/README.md): listener/controller, execution, GitHub publication and recovery.
- [Orchestrator README](https://github.com/xaime-vp/constant-integration/blob/main/orchestrator/README.md): task intake, exact file scope and verified approvals. Workspace [free-form guidance](../../docs/agent-setup/free-form-issues.md) distinguishes explicit owner preparation, sealed proposal inspection and current readiness from legacy envelopes.
- [Role contract](https://github.com/xaime-vp/constant-integration/blob/main/docs/AGENT_ROLES.md) and [delivery contract](https://github.com/xaime-vp/constant-integration/blob/main/docs/GITHUB_DELIVERY.md): external worker responsibilities and evidence.
- [Submission guide](https://github.com/xaime-vp/constant-integration/blob/main/docs/SUBMITTING_TASKS.md): executable issue formats and owner approval.
- [CI guide](https://github.com/xaime-vp/constant-integration/blob/main/docs/CI.md): offline suites and isolated container fixtures.
- [Repository consultation](../../docs/agent-setup/repository-consultation.md): native coder-to-researcher calls, candidate snapshots, schema-6 state, usage holds and real-Pi acceptance when changing dispatch, containment or recovery.

## Development boundaries

You implement platform code on the root developer's branch and PR. The deterministic Bonsai supervisor is a program in this repository, not a role you become by reading its runtime prompt. The supervisor owns worker approval, state, lifecycle, protected reports, credentials and publication. Pi coder, test-specialist, documentation and reviewer assignments cannot authorize themselves or peers. Generalist/tests are retired source routes; inspect sealed installed compatibility before choosing an executable handoff.

Preserve the single-listener lock, repository binding, exact editable scope, source hashes, process-stop confirmation and existing-PR head checks. Unknown execution remains unknown until supported confirmed-stop reconciliation; retain state and evidence. Runtime/configuration schemas, approval grammar and recovery changes require explicit migration and rollback detail in their PR.

Installed behavior must be observed independently of this checkout. Source code, passing offline tests and a running container do not prove a deployed capability or live task delivery. Implementation check observations, applicable read-only model review, exact-head GitHub CI and owner acceptance are distinct evidence. Documentation publishes without an embedded model reviewer; coder and test-specialist receive embedded read-only review. Source supports 1–10 slots (new preparations default to 10; omitted legacy setting retains 1). Automatic PR review is read-only, conditional on installed policy, and never grants implementation authority. The [capability map](../../docs/agent-setup/platform-capabilities.md) distinguishes model routing, schema-4 repair and source-only workflow components.

Keep `profiles/`, `tools/`, `orchestrator/`, `workers/` and sealed `workers/bonsai/pi_assets/skills/` together in the checkout: imports, packaging and CI depend on this layout. Workspace tools launch these originals with the correct working directory. User-facing workspace skills are separate from sealed runtime assets.

An existing checkout may use non-cone sparse rules to omit `/AGENTS.md` and older `/.agents/skills/` bundles locally. These are optional workspace instruction-discovery preferences, not Bonsai preflight requirements. The current platform treats target root `AGENTS.md` as optional, reading applicable root/nested instructions when present; sealed runtime profiles still control Pi roles. Preserve an existing sparse policy on ordinary branch changes and use MCP for deliberate excluded-path edits. Developer prompting and handoff templates are maintained in this workspace's `docs/agent-setup/`.

## Verification

Python 3.12+ is required. From the workspace root on Windows:

```powershell
py -3 tools/check.py --component orchestrator
py -3 tools/check.py --component worker
```

Or run `python tools/check.py` in the checkout with a configured interpreter. Use focused suites while implementing; cross-component work and merge requests require the full runner and pinned Ruff 0.14.4 (`python -m ruff check .`). Worker suites include Linux ownership/locking assumptions; disclose Windows failures and skips accurately rather than weakening those checks.

Tests must be offline and reproducible. A model probe, listener start, container install, release upgrade or live issue execution is an operational action, not incidental validation. Evaluation/benchmark work belongs in the separate `xaime-vp/CI-testing-and-improvement` repository. Keep credentials, private logs and installed state out of commits and issues.

Maintain one coherent task PR. Preserve unrelated work and concurrent commits, report failed/unrun checks and unresolved findings, and leave merging and deployment to the owner unless explicitly authorized. The root developer's test/documentation handoffs apply to developer-led changes. A separately authorized `agent:coder` task is an alternative supervised code writer; it must not overlap that developer's active branch edits.
