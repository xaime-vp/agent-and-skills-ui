/** Read-only Pi tools for agent instructions and bounded nested calls. */
import { Type } from "typebox";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { readAgentFile, capTextToEstimatedTokens } from "./agent-file-reader-core.mjs";

const READ_ONLY_TOOLS = new Set(["read_agent_file", "read", "grep", "find", "mcp__github__fetch_file"]);

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "read_agent_file",
    label: "Read Agent File",
    description: "Read AGENTS.md or SKILL.md with a default ~600-token output budget and resumable line/character offsets. Estimated from UTF-8 bytes, not an exact tokenizer.",
    annotations: { readOnlyHint: true },
    parameters: Type.Object({
      root: Type.Optional(Type.String({ description: "Checkout directory relative to workspace (default: .)" })),
      path: Type.Optional(Type.String({ description: "AGENTS.md or SKILL.md relative to root" })),
      startLine: Type.Optional(Type.Integer({ minimum: 1, maximum: 10000000 })),
      startChar: Type.Optional(Type.Integer({ minimum: 0, maximum: 10000000 })),
      maxLines: Type.Optional(Type.Integer({ minimum: 1, maximum: 400 })),
      maxOutputTokens: Type.Optional(Type.Integer({ minimum: 128, maximum: 4000, description: "Approximate output token ceiling (default 600)" })),
    }),
    async execute(_toolCallId, params, _signal, _onUpdate, ctx) {
      const result = await readAgentFile({
        cwd: ctx.cwd, root: params.root, filePath: params.path,
        startLine: params.startLine, startChar: params.startChar,
        maxLines: params.maxLines, maxOutputTokens: params.maxOutputTokens,
      });
      const { content, text, ...metadata } = result;
      return { content: [{ type: "text", text }], details: { ...metadata, readOnly: true } };
    },
  });

  pi.registerTool({
    name: "call_tool_limited",
    label: "Call Read-Only Tool With Token Limit",
    description: "Invoke an allowlisted read-only tool with nested execution and expose only its bounded text output. Approximate tokens. Requires a Pi version supporting ctx.executeTool.",
    annotations: { readOnlyHint: true },
    parameters: Type.Object({
      toolName: Type.String({ description: "Read-only tool: read_agent_file, read, grep, find, or mcp__github__fetch_file" }),
      args: Type.Record(Type.String(), Type.Any(), { description: "Target tool arguments matching its live schema" }),
      maxOutputTokens: Type.Optional(Type.Integer({ minimum: 128, maximum: 4000, description: "Approximate token ceiling (default 600)" })),
    }),
    async execute(_toolCallId, params, signal, _onUpdate, ctx) {
      if (!READ_ONLY_TOOLS.has(params.toolName)) throw new Error("Not on the read-only allowlist: " + params.toolName);
      if (typeof ctx.executeTool !== "function") throw new Error("This Pi version lacks ctx.executeTool; use a direct tool with its output bound");
      if (!ctx.tools?.some(tool => tool.name === params.toolName)) throw new Error("Not callable as a nested tool: " + params.toolName);
      const result = await ctx.executeTool(params.toolName, params.args, { signal });
      const items = result.content ?? [];
      if (items.some(item => item.type !== "text")) throw new Error("Non-text results cannot be safely token-limited by this wrapper");
      const rawText = items.map(item => item.text).join("\n");
      const limited = capTextToEstimatedTokens(params.toolName + ":\n" + rawText, params.maxOutputTokens);
      return {
        content: [{ type: "text", text: limited.text }],
        details: {
          toolName: params.toolName, maxOutputTokens: params.maxOutputTokens ?? 600,
          estimatedTokens: limited.estimatedTokens, truncated: limited.truncated,
          nestedError: Boolean(result.isError),
        },
        isError: Boolean(result.isError),
      };
    },
  });
}
