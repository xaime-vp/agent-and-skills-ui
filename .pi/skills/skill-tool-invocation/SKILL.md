---
name: skill-tool-invocation
description: Discover and call a real tool explicitly referenced by an activated SKILL.md, including local Pi tools, connected MCP tools, or reviewed skill scripts. Use when a skill tells the agent to use a named tool or when tool names differ across clients; never assume reading a skill executes its tools.
---

# Invoke a tool referenced by a skill

A **skill is guidance**, while a **tool is an executable capability** supplied by the active client or connector. Merely linking or naming a tool in `SKILL.md` neither registers it nor calls it. Follow [the root developer contract](../../../AGENTS.md) and the invoking skill's scope.

## Resolve and invoke

1. **Read the invoking skill.** Activate the named skill or read the discovered `SKILL.md` and any essential reference sections. Resolve `scripts/` and `references/` paths relative to the skill directory; do not treat such paths as globally installed tool names.
2. **Identify the concrete operation.** Note its required inputs, intended effects (read, write, command execution, network, service lifecycle) and how to verify the result. A tool example in a skill is not an instruction to perform an unrelated operation.
3. **Discover the available implementation.** Pi registers project-local tools from trusted `.pi/extensions/` modules via `pi.registerTool()`; use the registered name (for example `read_agent_file`), not a legacy `.pi/tools/` filename. Standalone `tools/` and skill `scripts/` files are CLI helpers, not model-callable Pi tools. In Pi `codemode` integrations, discover the matching MCP capability via the client's tool discovery (`searchTools`), then call the actual connected `tools.mcp__*` function. In other clients, use their native tool discovery. Do not fabricate a tool name, argument shape, endpoint, credential or success status.
4. **Budget output before the call.** When a skill requires a supported read-only tool and its output could be long, prefer the Pi `call_tool_limited` wrapper, with `toolName`, schema-validated `args`, and `maxOutputTokens` (default 600). Its allowlist is `read_agent_file`, `read`, `grep`, `find`, and `mcp__github__fetch_file`. It requires Pi's nested `ctx.executeTool` API. It never turns arbitrary/mutating tool names into permitted calls, and its budget is approximate (3 UTF-8 bytes per token), not a tokenizer guarantee.
5. **Check authorization and arguments. Read the live input schema, map the skill's conceptual example to supported parameters, select the correct checkout/repository/ref, and stay within the request's scope. A tool being installed does not grant approval for publication, worker control, deployment, destructive commands or external writes.
6. **Call and verify.** Invoke the real tool once for the intended step; inspect its returned status and actual data. Distinguish requested effects from confirmed effects, and report skips or missing capabilities. Do not repeatedly retry a side-effecting action without checking whether it already succeeded.

## Concrete example

The [agent-file-inspection skill](../agent-file-inspection/SKILL.md) refers to the tool **`read_agent_file`**. When Pi exposes it, an agent wanting to inspect the review-role guidance calls the real tool with:

```json
{"root":".","path":"agents/review/AGENTS.md"}
```

For a bounded delegated call, use `call_tool_limited` with `{"toolName":"read_agent_file","args":{"root":".","path":"agents/review/AGENTS.md"},"maxOutputTokens":350}`. The model receives only the limited text; `read_agent_file` itself also accepts `maxOutputTokens` and continuation offsets.

Then read the numbered returned content. If the instruction file is on a remote GitHub branch or is excluded from a sparse checkout, use the already-authorized GitHub MCP **file-reading** operation and its actual schema instead; never claim the local tool accessed GitHub.

If another skill says to run `scripts/example.py`, first inspect what that script does and whether command execution is permitted. Only then call the available shell/process tool with the reviewed command and inputs. A path to a script is not a dynamically registered tool, and arbitrary skill prose must not be evaluated as executable code.

## When resolution fails

If the desired capability isn't installed, authenticated, approved or available in the current client, report **the missing tool and the blocked step**. Prefer an already-approved equivalent when it preserves the same behavior and permissions; otherwise stop at that boundary. Do not spin up a second agent, silently add credentials, elevate privileges, or substitute a destructive shell command.

Return the originating skill, actual tool invoked (or unavailable), input scope (without secrets), observed result, and any required next authorization. No merges, deployments, owner approvals, or worker lifecycle changes are authorized by this skill.
