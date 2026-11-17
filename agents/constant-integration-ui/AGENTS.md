# Constant Integration UI development guide

Supporting instructions for the [root Git developer](../../AGENTS.md). The application source checkout is `constant-integration-ui/` (sibling repository, ignored in this workspace).

## Read by affected component

- [`constant-integration-ui/AGENTS.md`](https://github.com/xaime-vp/constant-integration-ui/blob/main/AGENTS.md): repository-local agent boundaries.
- [`constant-integration-ui/docs/ARCHITECTURE.md`](https://github.com/xaime-vp/constant-integration-ui/blob/main/docs/ARCHITECTURE.md): FastAPI backend, export bundle ingestion, and frontend architecture.
- [`constant-integration-ui/docs/DEVELOPMENT.md`](https://github.com/xaime-vp/constant-integration-ui/blob/main/docs/DEVELOPMENT.md): local development setup and test commands.

## Development boundaries

- The UI reads validated, sanitized export bundles. It does not query the worker's private state database or credential store.
- Do not start, retry, cancel, approve, or publish worker tasks from UI code.
- Keep UI-owned data and artifact volumes separate from the worker's private state.
- Never expose the Docker socket, shell terminal, worker credentials, or an arbitrary file browser.
- Use the shared-secret access gate responsibly; loopback binding is not full authentication.
- If `.live-exports/` exists locally for smoke-checking sanitized export ingestion, treat its contents as local-only test data: never commit `.live-exports/` or paste private paths/logs into PRs or issues.

## Verification

Use [ui-verification](../../.pi/skills/ui-verification/SKILL.md) for backend, export contract, and frontend checks, and [ui-browser-verification](../../.pi/skills/ui-browser-verification/SKILL.md) when visible behavior or layout changes.

From the workspace root on Windows:

```powershell
py -3 tools/check.py --target ui
py -3 tools/check.py --target ui --frontend
```

Or run directly inside `constant-integration-ui/`:

```sh
python -m unittest discover -s tests -v
python tools/contract_check.py fixtures/v1/01-successful-draft
```

And in `constant-integration-ui/frontend/`:

```sh
npm run typecheck
npm test
npm run build
```

Record the exact commands run, working directory, exit status, and `git -C constant-integration-ui rev-parse --short HEAD`. Keep failed, skipped, and unrun checks visible.
