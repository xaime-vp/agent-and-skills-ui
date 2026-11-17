---
name: ui-verification
description: Verify changes in constant-integration-ui across the FastAPI backend tests, export bundle contract checks, and React/TypeScript frontend (typecheck, Vitest, Vite build). Use for UI backend, fixture contract, or frontend validation; read-only and does not commit, push, or modify worker state.
---

# Constant Integration UI verification

Read the [UI development guide](../../../agents/constant-integration-ui/AGENTS.md)
before editing. Run targeted, honest verification inside `constant-integration-ui/`
(or via `py -3 tools/check.py --target ui [--frontend]` from the workspace root)
before updating a PR or delegating test/documentation work.

## 1. Backend & export contract checks

Run from `constant-integration-ui/`:

```sh
python -m unittest discover -s tests -v
python tools/contract_check.py fixtures/v1/01-successful-draft
```

- On Windows, use `py -3` if `python` is not on `PATH` or points to the wrong interpreter.
- Validate any newly added or modified fixture directories under `fixtures/v1/` with `contract_check.py`.
- The stock worker image lacks `fastapi`/`jsonschema`, so container-hosted protected checks for this repository need a derived image that installs `requirements-app.txt`; a plain `FROM` of the worker image plus that requirements file ran the full suite successfully.
- If `.live-exports/` exists locally for smoke-checking sanitized export ingestion, treat its contents as local-only test data: never commit `.live-exports/` or paste private paths/logs into PRs.
- Executing-profile accounting is a dependent cross-repository change: constant-integration exports the attribution, and the companion UI implementation adds `/api/v1/analytics/usage-by-profile`, `usage-calls` and `usage-steps`. Confirm the endpoint exists on the actual UI head before validating it; the runtime source alone does not establish UI behavior.

## 2. Frontend checks

Run from `constant-integration-ui/frontend/`:

```sh
npm run typecheck
npm test
npm run build
```

- `npm run typecheck` runs `tsc --noEmit`.
- `npm test` runs `vitest run`.
- `npm run build` runs `tsc --noEmit && vite build`.
- If dependencies are missing in a fresh checkout, install with `npm ci --no-audit --no-fund`.

## 3. Reporting requirements

- Record the exact commands run, working directory, exit status, and `git -C constant-integration-ui rev-parse --short HEAD`.
- Keep failed, skipped, and unrun checks visible; never report a pass from a partial subset or an older commit.
- Distinguish local verification from worker check records and exact-head GitHub Actions CI.

## Browser evidence

For changed visible behavior or layout, use
[ui-browser-verification](../ui-browser-verification/SKILL.md) with sanitized
fixtures. Report actual interaction coverage and unavailable browser checks.
