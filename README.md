# Agent and skills workspace

Developer-agent setup for working on external GitHub repositories through GitHub MCP. The setup is maintained in [xaime-vp/agent-and-skills](https://github.com/xaime-vp/agent-and-skills).

The root [AGENTS.md](AGENTS.md) defines the workflow: open a branch and draft PR, implement application code, delegate tests and documentation through scoped issues targeting that same PR, then review the combined result. The external Bonsai supervisor owns execution and publication for its workers.

Issue handoffs support [free-form preparation](docs/agent-setup/free-form-issues.md)
as well as legacy executable envelopes. Prose issues need no hand-written JSON:
an operator selects evidence and the parent PR, then the owner approves the sealed
proposal digest. Legacy envelopes retain their own schema and standalone approval.
Verify installed support before execution; issue creation alone does not dispatch
approved work.

## Workspace layout

| Path | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Primary Git developer contract |
| [agents/](agents/) | Platform, testing, documentation and review assignment guides |
| [.agents/skills/](.agents/skills/) | `bonsai-ci`, `bonsai-containers`, `pr-submission` and `codex-cli-mcp` skills |
| [tools/](tools/README.md) | Offline task validation and platform CLI launchers |
| [docs/agent-setup/](docs/agent-setup/prompting.md) | Relocated prompting and manual handoff templates |
| `constant-integration/` | Separately cloned product source; ignored by this repository |
| `constant-integration-ui/` | Optional UI operations console checkout; ignored by this repository |

## Codex CLI and existing GitHub MCP

The [Codex CLI MCP skill](.agents/skills/codex-cli-mcp/SKILL.md) explains how to run Codex with a local checkout, connect approved GitHub MCP servers from an existing local `mcp.json` into Codex's own MCP configuration, and create or update issues and draft PRs under the root workflow. A workspace `mcp.json` is not automatically loaded by Codex CLI. Never commit local MCP credentials.

## Start a workspace

Clone this repository, then clone the current platform target into its dedicated subfolder:

```sh
git clone https://github.com/xaime-vp/agent-and-skills.git
cd agent-and-skills
git clone https://github.com/xaime-vp/constant-integration.git constant-integration
```

The UI operations console, [constant-integration-ui](https://github.com/xaime-vp/constant-integration-ui), can be checked out the same way when you are working on it:

```sh
git clone https://github.com/xaime-vp/constant-integration-ui.git constant-integration-ui
```

Python 3.12+ is required for the workspace tools. On Windows, use `py -3`; on Linux use a configured Python interpreter. For example:

```powershell
py -3 tools/check.py --component orchestrator
py -3 tools/validate_task.py --repository xaime-vp/constant-integration --body-file path/to/issue.md
```

The launchers use `constant-integration/` without copying or relocating its runtime modules. The validator accepts `--platform-root` for a different source checkout. A successful offline parse does not verify an installed worker, its checks or owner approval. CLI installation and worker startup are separate operational actions.

To keep the upstream target contract out of local instruction discovery, this workspace's existing checkout uses optional non-cone sparse rules. Apply the same rules inside a fresh target checkout if desired:

```powershell
@'
/*
!/AGENTS.md
!/.agents/skills/
'@ | git -C constant-integration sparse-checkout set --no-cone --stdin
```

This changes only the local worktree; the product retains its short committed `AGENTS.md` because Bonsai requires it before processing target tasks.

## Repository boundaries

Constant Integration retains `profiles/`, sealed Pi skills under `workers/bonsai/pi_assets/`, its runtime tools, and product documentation for installation, task schemas, approvals, delivery, CI and recovery. Those are dependencies of the worker. Developer skills, detailed coding-agent setup and prompt/handoff templates live here.

The extraction cleanup in Constant Integration must be merged after this setup is preserved on this repository's base branch. PR links document that dependency; they do not enforce merge order.

Keep `.env*`, `.mcp.json`, credentials, worker state, logs, caches and nested target checkouts out of commits. The ignore rules protect local configuration; connect GitHub MCP in the agent client without publishing credentials. Changes to this setup use a PR in `agent-and-skills`; application changes use a PR in the selected target repository. Neither workflow authorizes merging or deployment by itself.
