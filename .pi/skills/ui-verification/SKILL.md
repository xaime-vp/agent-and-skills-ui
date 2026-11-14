---
name: ui-verification
description: Verify changes in constant-integration-ui across the FastAPI backend tests, export bundle contract checks, and React/TypeScript frontend (typecheck, Vitest, Vite build). Read-only validation; does not commit, push, or modify worker state.
---

# Constant Integration UI verification

Run targeted, honest verification inside `constant-integration-ui/` before updating a PR or delegating test/documentation work.

## 1. Backend & export contract checks

Run from `constant-integration-ui/`:

```sh
python -m unittest discover -s tests -v
python tools/contract_check.py fixtures/v1/01-successful-draft
```

- On Windows, use `py -3` if `python` is not on `PATH` or points to the wrong interpreter.
- Validate any newly added or modified fixture directories under `fixtures/v1/` with `contract_check.py`.
- If `.live-exports/` exists locally for smoke-checking sanitized export ingestion, treat its contents as local-only test data: never commit `.live-exports/` or paste private paths/logs into PRs.

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
