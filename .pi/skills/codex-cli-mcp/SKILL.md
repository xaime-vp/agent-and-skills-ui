---
name: codex-cli-mcp
description: Run or delegate coding work to the local Codex CLI, use an existing user/workspace mcp.json to connect approved GitHub MCP servers, and create or update GitHub issues, branches, and draft PRs with verified evidence. Use when asked to work through Codex CLI or GitHub MCP. Never assume mcp.json is automatically loaded.
---

# Codex CLI with GitHub MCP

Follow the [workspace root contract](../../../AGENTS.md) and the [PR submission skill](../pr-submission/SKILL.md). This skill describes **how to use** Codex, not permission to publish, approve, merge, deploy, or bypass the Bonsai supervisor. If acting inside a Bonsai worker role, do not perform GitHub writes that the supervisor owns.

## Choose the execution path

- **Already in an agent with a connected GitHub MCP:** use the existing GitHub MCP tools directly. In `codemode`-based clients such as Pi, discover and call them via `codemode` (`searchTools` and `tools.mcp__github__*`). Do not spawn a second Codex process just to perform an MCP operation.
- **Codex CLI requested or useful for a local checkout:** confirm `codex --version`, installation and authentication, then work in the selected repository checkout. Do not assume a ChatGPT account grants limitless usage, that an API key is configured, or that an interactive login can be done unattended.
- **Issue/PR publication:** prefer the connected GitHub MCP tools once authorized; otherwise use authenticated `gh` if installed, or report the missing capability. GitHub MCP access is separate from Codex's ChatGPT login.

## Codex bootstrap

```sh
npm install -g @openai/codex
codex --version
codex login
codex login status
codex mcp list
```

For a human using ChatGPT subscription benefits, select **Sign in with ChatGPT** during interactive login. For unattended tasks, first confirm that an existing supported authenticated session is available. Never copy token material or Codex authentication cache into an issue, PR, skill, trace or repo.

Start interactive mode in the MCP-connected `./codex` folder (which holds `./codex/.mcp.json` for GitHub PR/issue write access) using [scripts/run_codex.py](scripts/run_codex.py):

```sh
py -3 .pi/skills/codex-cli-mcp/scripts/run_codex.py check
py -3 .pi/skills/codex-cli-mcp/scripts/run_codex.py interactive
```

Or launch directly from `codex/`:

```sh
codex -C codex
```

For a bounded non-interactive code task targeting a checkout while keeping `./codex`'s MCP connection:

```sh
py -3 .pi/skills/codex-cli-mcp/scripts/run_codex.py exec --repo constant-integration --full-auto "Read the applicable AGENTS.md, make only the requested scoped implementation changes, run existing relevant checks, and report changed files and test results. Do not merge or deploy."
```

`--full-auto` permits workspace writes under Codex's sandbox; it is **not** a blanket grant to change unrelated paths or publish to GitHub. Use a controlled working directory/worktree, inspect the diff, and keep commit/push/PR operations in the responsible publisher's workflow. Avoid `--dangerously-bypass-approvals-and-sandbox`. If `codex exec` cannot access a tool because of a sandbox or approval boundary, surface the blocker rather than silently loosening permissions.

For instruction reuse in a fresh Codex session, ask for `$codex-cli-mcp` by name or describe a task matching its description. Codex discovers project skills in `.pi/skills/`; start from the workspace root when using this workspace skill, and explicitly point Codex to the external checkout.

## Connect existing `mcp.json`

A user's root `mcp.json` is **input configuration**, not a credential to commit and not automatically ingested by ordinary Codex CLI sessions. Refer to [MCP connection details](references/mcp-and-github.md) before changing configuration.

1. Identify the intended file explicitly: workspace-root `./mcp.json`, `./codex/.mcp.json` (Codex's MCP-connected folder), `./.pi/mcp.json` (Pi's workspace MCP config), user-home `~/mcp.json`, or a user-specified absolute path. Check `.mcp.json` only when the user identifies it. Do not search unrelated locations for credentials.
2. Inspect server **names and nonsecret connection fields** under `mcpServers` (some clients use `servers`); do not print actual tokens, keys, raw authorization headers or resolved environment values. If you are already running inside Pi with `.pi/mcp.json` loaded, `mcp__github` is already available via `codemode` and needs no `codex mcp` registration unless you also run `codex` CLI separately.
3. Detect the GitHub MCP entry and confirm the local CLI and server are available. For streamable HTTP use `codex mcp add github --url https://<approved-server>/mcp`; substitute the **real user-approved endpoint**, not this placeholder, and never copy inline `headers` tokens (such as `Authorization: Bearer ...`) from `mcp.json` into `codex mcp add` or TOML. For stdio use the CLI's current `codex mcp add --help` to map its command/args and environment names. Do not blindly copy client-specific schemas into TOML.
4. The Codex CLI/IDE shared MCP configuration lives at `~/.codex/config.toml` (or the active Codex home, if configured). Before any configuration write, check for a pre-existing `github` server and ask/stop on conflicting definitions rather than overwrite. A separate plugin package's root `mcp.json` may be interpreted by the plugin packaging system; that does not make a raw workspace `mcp.json` an automatic Codex CLI config.
5. Prefer environment references or the server's OAuth login over plaintext credentials. Never import embedded secrets from an existing JSON file into tracked TOML, command-line arguments or logs. If the source includes inline secrets, request secure reconfiguration instead.
6. Verify with `codex mcp list` and a nonmutating repository lookup. Configured does not imply authenticated or that the tool is authorized to perform writes. If the server is unavailable, state which step failed and fall back only to another **approved** GitHub interface.

Do **not** modify a user's `mcp.json` just to satisfy Codex. Treat it as an existing source of truth; configure Codex separately and keep it out of Git. If both user and workspace files exist, do not silently merge them.

## GitHub issue and PR workflow

1. Identify `owner/repo`, base, existing task branch/PR, scope and applicable target instructions. The current default external target is `xaime-vp/constant-integration-ui` unless the user selects another. Use the target repo's checkout, not the `agent-and-skills-ui` root, for product code.
2. Read the relevant issue/PR, inspect related work and labels, and establish permission for the requested mutation. Do not infer that an MCP token's capabilities imply user authorization.
3. For a new code change, create a branch, then a **draft PR before implementation**, per root `AGENTS.md`. If GitHub requires a diff, use an acceptable minimal planning file; never silently implement before opening the draft. For ongoing work, reuse the existing branch/PR.
4. Implement in scope, commit to the **explicit working branch**, verify the actual final diff, then run targeted checks. Codex may author code locally, while connected GitHub MCP or an authorized publisher performs remote actions.
5. Search for duplicate issues. When explicitly asked to write issues, follow the repository issue template and routing/approval rules. Issue creation does not automatically dispatch an agent. Link issues to the exact parent PR and branch, and use known labels only.
6. For delegated test/documentation work in this workspace, read the `bonsai-ci` skill. Request contributions targeting the **same parent PR branch**; do not invent automatic merge or approvals.
7. Maintain PR title/body with actual changes, linked issues, validation commands and outcomes, and honest contribution attribution. Inspect CI on the current PR head; do not claim checks passed because a worker said so.
8. Report repository, branch, issue/PR links, checks actually executed, risks, and owner actions needed. Do **not** merge, approve on the user's behalf, deploy, or force-push without separate authorization.

## Reusable prompts

**Implementation (CLI)**

```text
Use $codex-cli-mcp. Work in the selected target repository and follow its AGENTS.md.
Inspect the requested issue and current PR first. Implement only the agreed code scope
on the parent branch. Run relevant existing checks. Report changed files, exact
commands, results, and blockers. Do not publish, merge or deploy unless authorized.
```

**GitHub issue or PR (MCP)**

```text
Use $codex-cli-mcp and the already-connected GitHub MCP. Find the target repository's
existing issue/PR templates, search for duplicates, and make only the GitHub writes
I requested. Use the parent PR's exact branch for linked handoffs. Return the created
URLs and distinguish checks actually observed from checks not run.
```

## Failure handling and controls

- Missing `codex` or `gh`: report installation/authentication separately from task success.
- Missing `mcp.json`: do not fabricate a server; use already-connected approved tools or request the file location.
- MCP server listed but inaccessible: check process launch, network access, supported transport and authorization **without exposing tokens**.
- Usage/limits: check status where supported; limit concurrent Codex jobs. Subscription windows are usage quotas, **not** guaranteed wall-clock work time.
- Concurrent changes: refresh branch head before writes, never overwrite another worker's work or force-update without approval.
- Any unexpected credential exposure, production mutation or broad repository access: stop and report it.

Official references: [OpenAI Docs MCP setup](https://developers.openai.com/learn/docs-mcp), [Agent skills guidance](https://developers.openai.com/blog/eval-skills).
