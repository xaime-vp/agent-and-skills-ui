# Constant Integration development guide

Supporting instructions for the [root Git developer](../../AGENTS.md). The source checkout is [constant-integration](../../constant-integration/README.md); run repository commands there unless using a workspace launcher. This guide adapts the repository's original agent contract for the surrounding developer workspace.

## Read by affected component

- [Repository README](../../constant-integration/README.md) and [use cases](../../constant-integration/USE_CASES.md): current behavior and priorities.
- [Worker README](../../constant-integration/workers/bonsai/README.md): listener/controller, execution, GitHub publication and recovery.
- [Orchestrator README](../../constant-integration/orchestrator/README.md): task envelopes, exact file scope and verified approvals.
- [Role contract](../../constant-integration/docs/AGENT_ROLES.md) and [delivery contract](../../constant-integration/docs/GITHUB_DELIVERY.md): external worker responsibilities and evidence.
- [Submission guide](../../constant-integration/docs/SUBMITTING_TASKS.md): executable issue formats and owner approval.
- [CI guide](../../constant-integration/docs/CI.md): offline suites and isolated container fixtures.

## Development boundaries

You implement platform code on the root developer's branch and PR. The deterministic Bonsai supervisor is a program in this repository, not a role you become by reading its runtime prompt. The supervisor owns worker approval, state, lifecycle, protected reports, credentials and publication. Pi generalist and reviewer assignments cannot authorize themselves or peers.

Preserve the single-listener lock, repository binding, exact editable scope, source hashes, process-stop confirmation and existing-PR head checks. Unknown execution remains unknown until supported confirmed-stop reconciliation; retain state and evidence. Runtime/configuration schemas, approval grammar and recovery changes require explicit migration and rollback detail in their PR.

Installed behavior must be observed independently of this checkout. Source code, passing offline tests and a running container do not prove a deployed capability or live task delivery. Generalist check observations, read-only model review, exact-head GitHub CI and owner acceptance are distinct evidence.

Keep `profiles/`, `tools/`, `orchestrator/`, `workers/` and sealed `workers/bonsai/pi_assets/skills/` together in the checkout: imports, packaging and CI depend on this layout. Workspace tools launch these originals with the correct working directory. User-facing workspace skills are separate from sealed runtime assets.

The checkout uses non-cone sparse rules to omit its target `/AGENTS.md` and any older `/.agents/skills/` bundles locally. The extraction cleanup removes the external skills upstream, while retaining a short committed target contract required by Bonsai preflight. Preserve the exclusions on pulls and branch changes; use MCP for explicit upstream edits. This keeps the local Git worktree clean while the root contract and workspace skills remain the active guidance. Developer prompting and handoff templates are maintained in this workspace's `docs/agent-setup/`.

## Verification

Python 3.12+ is required. From the workspace root on Windows:

```powershell
py -3 tools/check.py --component orchestrator
py -3 tools/check.py --component worker
```

Or run `python tools/check.py` in the checkout with a configured interpreter. Use focused suites while implementing; cross-component work and merge requests require the full runner and pinned Ruff 0.14.4 (`python -m ruff check .`). Worker suites include Linux ownership/locking assumptions; disclose Windows failures and skips accurately rather than weakening those checks.

Tests must be offline and reproducible. A model probe, listener start, container install, release upgrade or live issue execution is an operational action, not incidental validation. Evaluation/benchmark work belongs in the separate `xaime-vp/CI-testing-and-improvement` repository. Keep credentials, private logs and installed state out of commits and issues.

Maintain one coherent task PR. Preserve unrelated work and concurrent commits, report failed/unrun checks and unresolved findings, and leave merging and deployment to the owner unless explicitly authorized. The root agent's test/documentation issue workflow applies to new code changes.
