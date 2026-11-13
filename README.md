# Constant Integration UI developer workspace

Agent workspace for developing the **Constant Integration UI** operations console. The application source lives in the `constant-integration-ui/` checkout, which is a separate Git repository and ignored by this workspace.

## What this is

Constant Integration UI is a read-only operations console that explains what each worker did, why it did it, what changed, what failed, and what it cost. It ingests validated, sanitized export bundles from the runtime worker and presents durable history through a FastAPI backend and a React/TypeScript frontend.

This repository holds only the agent harness: instructions, skills, tools and templates needed to work on the UI through GitHub MCP.

## Quick start

Clone the UI source into its dedicated checkout:

```bash
git clone https://github.com/xaime-vp/constant-integration-ui.git constant-integration-ui
```

Then work inside that checkout for application code:

```bash
cd constant-integration-ui
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/contract_check.py fixtures/v1/01-successful-draft

cd frontend
npm ci --no-audit --no-fund
npm run typecheck
npm run build
```

## Workspace layout

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Root developer operating contract |
| `.agents/skills/` | Agent skills for CI delegation, containers, status, Codex CLI, PR repair and PR submission |
| `.agents/tools/` | Workspace utilities: offline validation, process counters |
| `.agents/docs/` | Prompting, handoff and free-form issue templates |
| `constant-integration-ui/` | Application source checkout (separate repo; ignored here) |

## Agent workflow

See [`AGENTS.md`](AGENTS.md).

Local MCP credentials and worker state are kept out of commits. The root `.gitignore` already excludes `constant-integration-ui/` because it is its own repository.
