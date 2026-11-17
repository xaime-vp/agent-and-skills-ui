# Inspect agent files and invoke tools from skills

This workspace includes a **read-only Pi tool** called `read_agent_file` and two complementary skills:

- [agent-file-inspection](../../.pi/skills/agent-file-inspection/SKILL.md) loads and interprets local `AGENTS.md` and `SKILL.md` files.
- [skill-tool-invocation](../../.pi/skills/skill-tool-invocation/SKILL.md) resolves a tool named by a skill and calls it only when available and authorized.

## Tool contract

Pi loads project extensions in `.pi/extensions/` when started from this workspace (or when the extension is installed in the active Pi configuration). The `read_agent_file` tool accepts:

| Parameter | Meaning |
| --- | --- |
| `root` | Optional relative checkout directory within the workspace; default `.` |
| `path` | Relative path to an `AGENTS.md` or `SKILL.md`; default `AGENTS.md` |
| `startLine` | Optional 1-based first line, default 1 |
| `maxLines` | Optional count, default 160, maximum 400 |
| `maxOutputTokens` | Approximate output token ceiling, default **600**, minimum 128, maximum 4000 |
| `startChar` | Zero-based character offset when continuing partway through a long line; default 0 |

For example, call `read_agent_file` with `{"root":".","path":"agents/review/AGENTS.md"}` to inspect an agent role guide, or `{"path":".agents/skills/pr-repair/SKILL.md"}` to inspect a skill. Paths must stay within the workspace, including after symlink resolution. The tool cannot mutate files or fetch remote content.

When the source file is absent from a sparse checkout, use an already-authorized GitHub MCP file-read operation on the **correct repository and ref**, rather than removing sparse exclusions or assuming the root workspace and target checkout are the same repository. For ordinary code files, use the client's normal read/search tools instead.

## Limit tool output before it enters model context

The Pi extension also registers **`call_tool_limited`**. It invokes an allowlisted read-only tool through Pi's nested-tool interface and returns only the token-budgeted text. Nested results are not separate model-visible tool-result messages. Arguments are `toolName`, `args` (matching the target's actual schema), and optional `maxOutputTokens` (default 600).

For example:

```json
{"toolName":"read_agent_file","args":{"root":".","path":".agents/skills/pr-repair/SKILL.md"},"maxOutputTokens":350}
```

The read-only allowlist is `read_agent_file`, `read`, `grep`, `find`, and `mcp__github__fetch_file`. The wrapper refuses arbitrary/mutating names; nested calls still undergo Pi's normal argument validation and permission handling. This requires a Pi version with `ctx.executeTool` and accepts text-only results.

**Token budget semantics:** Both tools use a conservative estimate of **3 UTF-8 bytes per token** on the model-facing text, including any header and truncation hint. Real token counts depend on the active model's tokenizer and are **not guaranteed exact**. The wrapper does not impose a global cap on direct calls to other tools. The reader provides `nextStartLine` and `nextStartChar` continuation offsets; for other tools, narrow their query or use their native pagination.

## Referenced tool invocation

A skill's mention of a tool **describes a capability**, not a call or a grant of permission. First read the skill, follow its relative references selectively, then discover an actual connected tool and its live input schema. A Pi-local tool such as `read_agent_file` may be invoked by its registered name. For GitHub MCP operations in a `codemode`-based client, discover the matching `mcp__github__*` capability; do not assume names are universal. Read-only inspection can proceed within task scope. Publishing, process execution, lifecycle actions, and other mutations require their own authorization.

If a referenced tool cannot be found, stop that step and report the missing capability; do not invent a function, run unreviewed shell snippets, or launch a second agent to simulate it. Report what was read or executed and distinguish observed results from unrun work.

## Local validation

From the workspace root, run:

```sh
node --test .pi/extensions/agent-file-reader-core.test.mjs
```

The tests exercise path containment, accepted filename types, line-window bounds and symlink escaping. They do not verify that an external Pi installation has loaded this extension, nor that an MCP server is connected.
