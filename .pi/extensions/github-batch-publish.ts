/**
 * Batch publish explicitly staged text files to an existing PR using connected
 * GitHub MCP. Nested results are not model-facing; arguments still reach connector.
 */
import path from "node:path";
import { realpath } from "node:fs/promises";
import { Type } from "typebox";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { buildStagedPlan, publishStagedPlan, boundedSummary } from "./github-batch-core.mjs";

const OPERATIONS = ["get_pr_info", "create_blob", "create_tree", "create_commit", "update_ref"] as const;

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "github_batch_publish",
    label: "GitHub staged batch publisher",
    description: "Plan or publish explicitly listed staged UTF-8 files to an existing PR with create_blob/create_tree/create_commit/update_ref, checking the exact head and returning compact output only.",
    promptSnippet: "Use github_batch_publish to batch staged files into an existing PR without exposing full contents in model-facing tool results.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    executionMode: "sequential",
    reachesTools: () => ["mcp__github", "mcp__GitHub", "codex_apps.github"],
    parameters: Type.Object({
      action: Type.Union([Type.Literal("plan"), Type.Literal("publish")]),
      repositoryFullName: Type.String({ description: "Exact GitHub owner/repo" }),
      repoPath: Type.String({ description: "Local checkout directory relative to Pi workspace" }),
      branch: Type.String({ description: "Existing PR head branch" }),
      expectedHeadSha: Type.String({ description: "Full expected PR head SHA; must match local HEAD" }),
      paths: Type.Array(Type.String(), { minItems: 1, maxItems: 60, description: "Exact staged paths, no globs" }),
      prNumber: Type.Optional(Type.Integer({ minimum: 1, description: "Required for publish" })),
      commitMessage: Type.Optional(Type.String({ description: "Required for publish" })),
      confirmPublish: Type.Optional(Type.Boolean({ description: "Must be true to publish; does not substitute for owner authorization" })),
      maxOutputTokens: Type.Optional(Type.Integer({ minimum: 128, maximum: 2000, description: "Approximate output-token ceiling (default 300)" })),
    }),
    async execute(_toolCallId, args, signal, _onUpdate, ctx) {
      if (signal?.aborted) throw new Error("Cancelled");
      const workspace = await realpath(ctx.cwd);
      if (!args.repoPath || path.isAbsolute(args.repoPath) || path.win32.isAbsolute(args.repoPath) ||
          args.repoPath.split(/[\\/]/).includes("..")) {
        throw new Error("repoPath must remain within Pi workspace");
      }
      const checkout = await realpath(path.resolve(workspace, args.repoPath));
      const rel = path.relative(workspace, checkout);
      if (rel === ".." || rel.startsWith(".." + path.sep) || path.isAbsolute(rel)) throw new Error("Checkout escapes workspace");
      const runGit = async (gitArgs: string[]) => pi.exec("git", ["-C", checkout, ...gitArgs], { signal });
      const willPublish = args.action === "publish";
      if (willPublish) {
        if (!args.confirmPublish || !args.prNumber || !args.commitMessage?.trim()) {
          throw new Error("Publish requires confirmPublish=true, prNumber, and commitMessage");
        }
        if (args.commitMessage.length > 120 || args.commitMessage.includes("\0") || args.commitMessage.includes("\n")) {
          throw new Error("commitMessage must be a single line of up to 120 characters");
        }
      }
      const plan = await buildStagedPlan({
        runGit, repositoryFullName: args.repositoryFullName, branch: args.branch,
        expectedHeadSha: args.expectedHeadSha, paths: args.paths, includeContent: willPublish,
      });
      if (!willPublish) {
        const summary = {status: "planned", repository: plan.repositoryFullName, branch: plan.branch,
          head: plan.expectedHeadSha, files: plan.entries.map(({path: name, status, mode, bytes}) => ({path: name, status, mode, bytes})),
          count: plan.fileCount, bytes: plan.totalBytes};
        return {content: [{type: "text", text: boundedSummary(summary, args.maxOutputTokens)}],
          details: {status: "planned", count: plan.fileCount, head: plan.expectedHeadSha}};
      }
      if (ctx.hasUI !== true || typeof ctx.ui?.confirm !== "function" ||
          !(await ctx.ui.confirm("Publish staged files to GitHub?",
            "Repository: " + args.repositoryFullName + "\nPR: #" + args.prNumber +
            "\nBranch: " + args.branch + "\nExpected head: " + args.expectedHeadSha +
            "\nFiles: " + plan.fileCount + "\nAuthorize this publication?"))) {
        throw new Error("Interactive operator confirmation required for GitHub publication");
      }
      if (typeof ctx.executeTool !== "function") throw new Error("Pi lacks nested ctx.executeTool");
      const available = ctx.tools ?? [];
      const names = Object.fromEntries(OPERATIONS.map(operation => {
        const matched = ["mcp__github__" + operation, "mcp__GitHub__" + operation, "codex_apps.github." + operation]
          .find(candidate => available.some(tool => tool.name === candidate));
        if (!matched) throw new Error("Connected GitHub capability missing: " + operation);
        return [operation, matched];
      }));
      const execute = async (operation: string, values: Record<string, unknown>) => {
        if (signal?.aborted) throw new Error("Cancelled; inspect PR before retrying");
        return ctx.executeTool(names[operation], values, {signal});
      };
      const published = await publishStagedPlan({
        plan: {...plan, commitMessage: args.commitMessage}, prNumber: args.prNumber, execute,
      });
      const summary = {status: "published", repository: published.repositoryFullName,
        branch: published.branch, pr: published.prNumber, files: published.count,
        previousHead: published.previousHead, newHead: published.newHead,
        note: "Commit and ref update confirmed; review and checks not performed by this tool"};
      return {content: [{type: "text", text: boundedSummary(summary, args.maxOutputTokens)}],
        details: {status: "published", files: published.count, newHead: published.newHead}};
    },
  });
}
