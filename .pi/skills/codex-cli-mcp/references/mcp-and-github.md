# MCP JSON to Codex CLI: safe connection and GitHub operations

## Configuration shape and discovery

The user's existing `mcp.json` may look like the following *example* (not a file this repository installs):

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"}
    }
  }
}
```

Some MCP clients use a `servers` object and `type` keys. Identify the actual client schema; do not pretend all formats are accepted by Codex. The example is conceptual and requires an authenticated, locally available GitHub MCP image. Use an existing trusted connection rather than installing a new server automatically.

- Config input may be `./mcp.json`, `./.pi/mcp.json` (Pi workspace MCP config, often `type: "http"` with `url` and `headers`), `~/mcp.json`, or a path the user specifies; the file is not guaranteed to exist.
- Codex CLI uses its own MCP settings, shared with its IDE extension, under `~/.codex/config.toml` (subject to Codex home override).
- **There is no automatic general-purpose `mcp.json` → Codex CLI attachment**. Map and register each approved server; do not commit the config file or embedded secrets. (In Pi, `.pi/mcp.json` is loaded directly by Pi and exposed through `codemode`.)

### Streamable HTTP

If the source contains a trusted HTTPS MCP endpoint:

```sh
codex mcp add github --url https://github-mcp.example.invalid/mcp
codex mcp list
```

The domain above is intentionally nonworking. Replace it only with the actual approved endpoint. Never copy inline `headers` bearer tokens from `.pi/mcp.json` or `mcp.json` into `codex mcp add` or tracked TOML; use OAuth (`codex mcp login`) or an environment-variable reference (`bearer_token_env_var` / `env_http_headers`) in local `config.toml`. For OAuth-enabled endpoints, inspect the installed CLI's login support (`codex mcp --help`) and complete interactive authorization if required.

### stdio

For a local executable server, inspect `codex mcp add --help` for the installed CLI's accepted syntax; pass the real command and args after its separator when supported. A typical pattern is:

```sh
codex mcp add github -- docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server
codex mcp list
```

Use the inherited `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable only if it is already configured securely on the local machine. Do not paste its value into any `codex mcp add --env NAME=VALUE` command; shell history, process arguments or config files may expose it. A documented `env_vars` passthrough entry in local `config.toml`, if supported by the installed Codex version, can be reviewed with the operator. Never store inline secrets in this repository.

Verify by requesting a **read-only** repository lookup first. `codex mcp list` demonstrates registration, not successful authentication or adequate GitHub permissions.

## GitHub capabilities and authorization

Use GitHub MCP server tool names as **capabilities**, not a fixed universal contract. Different GitHub MCP implementations and toolsets have different names or permissions.

| Intent | Preferred operation | Evidence |
| --- | --- | --- |
| Inspect | Get repository, fetch file, list issues/PRs | Actual repo/ref and relevant current state |
| Create issue | Search duplicates, inspect template, create issue | URL, title and branch/PR reference |
| Change issue | Fetch current body/labels, update only requested fields | Updated URL and changed fields |
| Start work | Create branch from exact base; open draft PR before code | Branch and draft PR URL |
| Implement | Scoped commits on explicit head branch | Commit(s), diff and check evidence |
| Deliver | Update draft PR with changed scope and checks | PR URL, actual current-head CI state |

A GitHub MCP connection with write tools does **not** grant automatic permission to mutate every repository it can reach. Follow owner approvals, issue-intake policies and target-specific worker contracts. Do not create duplicate tasks or post synthetic approvals.

## Example PR body

```markdown
## Summary
- <observed change>

## Related work
- Closes #<issue> (only when semantically correct)
- Tests/docs delegated: #<issue numbers> (if applicable)

## Validation
- `<exact command>` — PASS/FAIL/NOT RUN, revision <SHA>
- GitHub checks — PASS/FAIL/PENDING/UNAVAILABLE at <head SHA>

## Risks / follow-up
- <open issues, blockers, rollback requirements>
```

Never claim the model identity, result, review or tests were verified unless the supporting evidence exists. The reviewer/owner retains final approval, merging and deployment.
