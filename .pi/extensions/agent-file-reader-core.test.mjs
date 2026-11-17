import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, symlink, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { readAgentFile, capTextToEstimatedTokens } from "./agent-file-reader-core.mjs";

async function withWorkspace(fn) {
  const workspace = await mkdtemp(path.join(tmpdir(), "read-agent-file-"));
  try {
    await mkdir(path.join(workspace, "repo", "agents", "review"), {recursive: true});
    await mkdir(path.join(workspace, ".agents", "skills", "review"), {recursive: true});
    await writeFile(path.join(workspace, "repo", "AGENTS.md"), "# Root\nsecond\nthird\n");
    await writeFile(path.join(workspace, "repo", "agents", "review", "AGENTS.md"), "# Reviewer\nScoped guidance\n");
    await writeFile(path.join(workspace, ".agents", "skills", "review", "SKILL.md"), "---\nname: review\n---\n");
    await fn(workspace);
  } finally {
    await rm(workspace, {recursive: true, force: true});
  }
}

test("reads agent and skill files with line numbers and bounded windows", async () => {
  await withWorkspace(async cwd => {
    const file = await readAgentFile({cwd, root: "repo", startLine: 2, maxLines: 1});
    assert.equal(file.content, "L2: second");
    assert.equal(file.totalLines, 3);
    assert.equal(file.truncated, true);
    assert.equal(file.nextStartLine, 3);
    const nested = await readAgentFile({cwd, root: "repo", filePath: "agents/review/AGENTS.md"});
    assert.match(nested.content, /L2: Scoped guidance/);
    const skill = await readAgentFile({cwd, filePath: ".agents/skills/review/SKILL.md"});
    assert.match(skill.content, /L2: name: review/);
    assert.equal(skill.truncated, false);
  });
});

test("rejects outside paths, other file types, bad windows and missing lines", async () => {
  await withWorkspace(async cwd => {
    for (const filePath of ["../AGENTS.md", "agents/../AGENTS.md", "/tmp/AGENTS.md", "not-secret.txt", "C:\\temp\\AGENTS.md"]) {
      await assert.rejects(readAgentFile({cwd, root: "repo", filePath}));
    }
    await assert.rejects(readAgentFile({cwd, root: "../escape"}));
    await assert.rejects(readAgentFile({cwd, root: "repo", maxLines: 401}));
    await assert.rejects(readAgentFile({cwd, root: "repo", startLine: 4}));
    await assert.rejects(readAgentFile({cwd, root: "repo", startLine: 0}));
    await assert.rejects(readAgentFile({cwd, root: "repo", maxOutputTokens: 127}));
    await assert.rejects(readAgentFile({cwd, root: "repo", startChar: 99}));
  });
});

test("rejects symlinks that escape either repository root or workspace", async t => {
  await withWorkspace(async cwd => {
    const external = await mkdtemp(path.join(tmpdir(), "outside-agent-"));
    try {
      await writeFile(path.join(external, "AGENTS.md"), "private");
      try {
        await symlink(external, path.join(cwd, "outside"), "dir");
        await symlink(external, path.join(cwd, "repo", "escape"), "dir");
      } catch (e) {
        if (e.code === "EPERM" || e.code === "EACCES") { t.skip("Symlinks not available"); return; }
        throw e;
      }
      await assert.rejects(readAgentFile({cwd, root: "outside", filePath: "AGENTS.md"}), /outside the workspace/);
      await assert.rejects(readAgentFile({cwd, root: "repo", filePath: "escape/AGENTS.md"}), /outside the selected root/);
    } finally {
      await rm(external, {recursive: true, force: true});
    }
  });
});

test("caps estimated tokens and provides complete resumable continuation", async () => {
  await withWorkspace(async cwd => {
    const original = "😊 αβγ ".repeat(800);
    await writeFile(path.join(cwd, "repo", "AGENTS.md"), original);
    let startLine = 1, startChar = 0, recovered = "", calls = 0;
    do {
      const page = await readAgentFile({cwd, root: "repo", startLine, startChar, maxOutputTokens: 128});
      assert.ok(page.estimatedTokens <= 128);
      assert.ok(Buffer.byteLength(page.text, "utf8") <= 128 * 3);
      recovered += page.content.replace(/^L\d+(?:\+\d+)?: /, "");
      calls++;
      if (!page.truncated) break;
      assert.ok(page.nextStartLine > startLine || page.nextStartChar > startChar);
      startLine = page.nextStartLine;
      startChar = page.nextStartChar;
    } while (calls < 100);
    assert.equal(recovered, original);
    assert.ok(calls > 1);
  });
});

test("caps arbitrary text output with a conservative token estimate", () => {
  const huge = "✨".repeat(5000);
  const output = capTextToEstimatedTokens(huge, 128);
  assert.equal(output.truncated, true);
  assert.ok(output.estimatedTokens <= 128);
  assert.ok(Buffer.byteLength(output.text, "utf8") <= 128 * 3);
  assert.equal(capTextToEstimatedTokens("short", 128).truncated, false);
  assert.throws(() => capTextToEstimatedTokens("short", 127));
});

test("rejects oversized input", async () => {
  await withWorkspace(async cwd => {
    await writeFile(path.join(cwd, "repo", "AGENTS.md"), "x".repeat(1024 * 1024 + 1));
    await assert.rejects(readAgentFile({cwd, root: "repo"}), /no larger than 1 MiB/);
  });
});
