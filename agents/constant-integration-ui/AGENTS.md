# Constant Integration UI development guide

Supporting instructions for the [root Git developer](../../AGENTS.md). The source checkout is [constant-integration-ui](../../constant-integration-ui/README.md); run repository commands there unless using a workspace launcher. This guide adapts the UI's original agent contract for the surrounding developer workspace.

## Read by affected component

- [Repository README](../../constant-integration-ui/README.md) and [roadmap](../../constant-integration-ui/ROADMAP.md): current behavior, priorities and milestone demonstrations.
- [Architecture](../../constant-integration-ui/docs/ARCHITECTURE.md): runtime, components, data ownership, history ingestion, core screens and deployment boundaries.
- [Source mapping](../../constant-integration-ui/docs/SOURCE_MAPPING.md): runtime facts and capability gaps that the export contract is allowed to represent.
- [History contract](../../constant-integration-ui/contracts/README.md): versioned export/event/artifact schemas with compatibility rules and examples.
- [Fixtures](../../constant-integration-ui/fixtures/README.md): sanitized success, failure, interruption, concurrency and hostile-content scenarios.
- [Development notes](../../constant-integration-ui/docs/DEVELOPMENT.md): local setup, container build and operational boundaries.
- [Container architecture](../../constant-integration-ui/docs/CONTAINER_ARCHITECTURE.md): image/process/volume structure, permission and network boundaries, release lifecycle and UI integration.
- [Submitting worker tasks](../../constant-integration-ui/docs/SUBMITTING_TASKS.md) and [UI coordination](../../constant-integration-ui/docs/submitting-tasks/coordination.md): using the external Bonsai worker against this repository.

## Development boundaries

You implement UI code on the root developer's branch and PR. The deterministic Bonsai supervisor is a program in `constant-integration`, not a role you become by reading its runtime prompt. The supervisor owns worker approval, state, lifecycle, protected reports, credentials and publication. Pi generalist and reviewer assignments cannot authorize themselves or peers.

The UI reads **validated, sanitized export bundles** through a dedicated read-only export boundary. It may write its own history database, artifact archive, projections, import/rejection records and backups. Application read-only behavior does not mean its importer has no local writes.

- Never mount/query the worker's private state database or credential store. Do not expose the Docker socket, a shell terminal or an arbitrary file browser.
- Do not start, retry, cancel, approve or publish worker tasks from UI code. Future controls must use an explicitly designed authenticated supervisor interface; capability metadata alone never grants authority.
- Do not repair runtime state, clear attempts, reset approvals or infer process termination from stale observations. UI failure must not trigger worker cleanup.
- Keep the UI-owned data volume separate from the read-only export mount. Preserve non-root execution and restricted container settings.
- Preserve contract versions and stable source identity. Delivery sequence, stream and ingestion time are not event identity. Replays must not duplicate source facts; conflicts must remain visible.
- Follow the compatibility rules for unknown events, unsupported versions, quarantine and missing artifacts. Never silently skip required bytes or manufacture a successful import.

The access gate is a shared secret (HTTP Basic via `UI_AUTH_PASSWORD`/`UI_AUTH_PASSWORD_FILE`); the server refuses non-loopback serving without one. Keep development on loopback; do not expose real history publicly, treat the secret as per-user identity, or mistake loopback binding for authentication.

Installed behavior must be observed independently of this checkout. Source code, passing offline tests and a running container do not prove a deployed capability or live task delivery. Generalist check observations, read-only model review, exact-head GitHub CI and owner acceptance are distinct evidence.

## Verification

Use **Python 3.12 and Node 22**, matching the UI's CI. From the UI checkout root:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/contract_check.py fixtures/v1/01-successful-draft
cd frontend
npm ci --no-audit --no-fund
npm run typecheck
npm run build
```

Run focused suites while iterating; cross-component work and merge requests require the full Python/contract/fixture checks and the frontend typecheck/build. The M0 gate revalidates committed evidence and provenance; it does not capture a new runtime run, prove current installation capability or authorize a paid model call.

Container build is an operational action, not incidental validation:

```bash
podman build -f deploy/Dockerfile -t constant-integration-history:local .
```

Use disposable UI data for import/backup/restore checks. Keep credentials, private logs and installed state out of commits and issues.

## Workflow

The root Git developer's workflow applies to new code changes in this repository:

1. Create a working branch and open a draft PR into `main`.
2. Implement and commit application code on that branch.
3. Delegate tests and documentation through repository issues using the workspace [`bonsai-ci`](../../.agents/skills/bonsai-ci/SKILL.md) skill.
4. Track the issue workers, review their contributions on the same branch, and validate the combined result.

Use free-form preparation or a legacy executable envelope as supported by the installed release. Both routes target the existing parent PR, require revision-bound owner approval, and must keep test and documentation work sequential because the branch is reserved.

Maintain one coherent task PR. Preserve unrelated work and concurrent commits, report failed/unrun checks and unresolved findings, and leave merging and deployment to the owner unless explicitly authorized.
