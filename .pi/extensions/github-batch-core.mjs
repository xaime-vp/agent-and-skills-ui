/** Pure batch publication helpers. No credentials, network, or model calls. */
const HEX_SHA = /^(?:[a-f\d]{40}|[a-f\d]{64})$/i;
const REPO = /^[\w.-]+\/[\w.-]+$/;
const BRANCH = /^(?!\/)(?!.*(?:\.\.|@\{|\\|\s|~|\^|:|\?|\*|\[|\/\/|\.$|\.lock(?:\/|$)))[A-Za-z\d._/-]+$/;
const MAX_FILES = 60;
const MAX_TOTAL_BYTES = 2 * 1024 * 1024;
const TOKEN_ESTIMATE_BYTES = 3;

export function validateRequest({repositoryFullName, branch, expectedHeadSha, paths}) {
  if (!REPO.test(repositoryFullName ?? "")) throw new Error("Invalid owner/repo");
  if (!BRANCH.test(branch ?? "") || branch.startsWith("-")) throw new Error("Invalid branch");
  if (!HEX_SHA.test(expectedHeadSha ?? "")) throw new Error("expectedHeadSha must be a full Git SHA");
  if (!Array.isArray(paths) || !paths.length || paths.length > MAX_FILES) throw new Error("Specify 1-60 exact paths");
  if (new Set(paths).size !== paths.length) throw new Error("Duplicate paths");
  for (const p of paths) {
    if (typeof p !== "string" || !p || p.startsWith("/") || p.includes("\\") || p.includes("\0") || p.split("/").some(part => ["", ".", ".."].includes(part))) throw new Error("Invalid staged path");
  }
}

export function parseStatusNul(raw) {
  if (!raw) return [];
  const parts = raw.split("\0");
  if (parts.at(-1) !== "") throw new Error("Unterminated Git -z status output");
  parts.pop();
  if (parts.length % 2) throw new Error("Unexpected Git status output; renames must be disabled");
  const entries = [];
  for (let i = 0; i < parts.length; i += 2) {
    const [status, filePath] = [parts[i], parts[i + 1]];
    if (!/^[AMD]$/.test(status)) throw new Error("Unsupported index status " + status);
    entries.push({status, path: filePath});
  }
  return entries;
}

export function matchingOrigin(origin, repositoryFullName) {
  const trimmed = (origin || "").trim().replace(/\.git$/, "");
  const m = /^(?:https:\/\/github\.com\/|ssh:\/\/git@github\.com\/|git@github\.com:)([^/?#]+\/[^/?#]+)$/i.exec(trimmed);
  return Boolean(m && m[1].toLowerCase() === repositoryFullName.toLowerCase());
}

function requireGit(out, action) {
  if (!out || out.code !== 0) throw new Error("git " + action + " failed; inspect local checkout");
  return out.stdout;
}

/** Read only explicit staged paths from the Git index, never working-tree content. */
export async function buildStagedPlan({runGit, repositoryFullName, branch, expectedHeadSha, paths, includeContent = false}) {
  validateRequest({repositoryFullName, branch, expectedHeadSha, paths});
  const head = requireGit(await runGit(["rev-parse", "HEAD"]), "HEAD").trim();
  if (head !== expectedHeadSha) throw new Error("Local HEAD differs from expected PR head; refresh checkout first");
  const baseTreeSha = requireGit(await runGit(["rev-parse", "HEAD^{tree}"]), "HEAD tree").trim();
  if (!HEX_SHA.test(baseTreeSha)) throw new Error("Invalid local tree SHA");
  const origin = requireGit(await runGit(["remote", "get-url", "origin"]), "origin").trim();
  if (!matchingOrigin(origin, repositoryFullName)) throw new Error("Local origin does not match requested GitHub repository");
  const raw = requireGit(await runGit(["diff", "--cached", "--name-status", "-z", "--no-renames", "HEAD"]), "staged diff");
  const candidates = new Map(parseStatusNul(raw).map(entry => [entry.path, entry]));
  const entries = [];
  let totalBytes = 0;
  for (const stagedPath of paths) {
    const candidate = candidates.get(stagedPath);
    if (!candidate) throw new Error("Path is not staged: " + stagedPath);
    const entry = {path: stagedPath, status: candidate.status};
    if (candidate.status !== "D") {
      const ls = requireGit(await runGit(["ls-files", "--stage", "--", stagedPath]), "index mode").trim();
      const line = ls.split("\n").find(row => row.endsWith("\t" + stagedPath));
      const match = /^(100644|100755) ([a-f\d]{40}|[a-f\d]{64}) 0\t/.exec(line ?? "");
      if (!match) throw new Error("Unsupported staged file mode or index stage: " + stagedPath);
      entry.mode = match[1];
      const source = requireGit(await runGit(["show", ":" + stagedPath]), "staged object");
      if (/[\x00-\x08\x0B\x0C\x0E-\x1F\uFFFD]/.test(source)) throw new Error("Binary/non-UTF-8 staged file unsupported: " + stagedPath);
      entry.bytes = Buffer.byteLength(source, "utf8");
      totalBytes += entry.bytes;
      if (totalBytes > 2 * 1024 * 1024) throw new Error("Batch exceeds 2 MiB limit");
      if (includeContent) entry.content = source;
    }
    entries.push(entry);
  }
  return {repositoryFullName, branch, expectedHeadSha, baseTreeSha, entries, fileCount: entries.length, totalBytes};
}

function responseObject(result) {
  if (!result || result.isError) throw new Error("GitHub tool reported failure (do not retry without checking)");
  if (result.structuredContent && typeof result.structuredContent === "object") return result.structuredContent;
  for (const part of result.content ?? []) {
    if (part.type === "text") {
      try { return JSON.parse(part.text); } catch { /* next part */ }
    }
  }
  if (result.details && typeof result.details === "object") return result.details;
  throw new Error("GitHub tool returned no machine-readable response");
}

function resultField(result, key) {
  const obj = responseObject(result);
  const value = obj?.result?.[key] ?? obj?.[key];
  if (key === "sha" && !HEX_SHA.test(value ?? "")) throw new Error("GitHub returned invalid SHA");
  return value;
}

/** Create blobs + tree + commit; verify PR at both sides of upload; update ref with lease. */
export async function publishStagedPlan({plan, prNumber, execute}) {
  if (!Number.isInteger(prNumber) || prNumber < 1) throw new Error("prNumber required");
  const {repositoryFullName: repo, branch, expectedHeadSha, baseTreeSha} = plan;
  const getPr = async () => {
    const obj = responseObject(await execute("get_pr_info", {repository_full_name: repo, pr_number: prNumber}));
    const pr = obj.result ?? obj;
    if (pr.head !== branch || pr.head_sha !== expectedHeadSha || pr.head_repo_full_name !== repo || pr.state !== "open") {
      throw new Error("PR head or state has changed; no files published to branch");
    }
    return pr;
  };
  await getPr();
  const elements = [];
  for (const entry of plan.entries) {
    if (entry.status === "D") elements.push({path: entry.path, mode: "100644", type: "blob", sha: null});
    else {
      const sha = resultField(await execute("create_blob", {repository_full_name: repo, content: entry.content, encoding: "utf-8"}), "sha");
      elements.push({path: entry.path, mode: entry.mode, type: "blob", sha});
    }
  }
  const treeSha = resultField(await execute("create_tree", {repository_full_name: repo, tree_elements: elements, base_tree_sha: baseTreeSha}), "sha");
  const commitSha = resultField(await execute("create_commit", {repository_full_name: repo, message: plan.commitMessage, tree_sha: treeSha, parent_sha: expectedHeadSha}), "sha");
  await getPr();
  const updated = resultField(await execute("update_ref", {repository_full_name: repo, branch_name: branch, sha: commitSha, force: false, expected_sha: expectedHeadSha}), "success");
  if (updated !== true) throw new Error("Ref update not confirmed; inspect branch before retrying");
  return {repositoryFullName: repo, branch, prNumber, previousHead: expectedHeadSha, newHead: commitSha, count: elements.length};
}

export function boundedSummary(value, maxOutputTokens = 300) {
  if (!Number.isInteger(maxOutputTokens) || maxOutputTokens < 128 || maxOutputTokens > 2000) throw new Error("maxOutputTokens must be 128-2000");
  const text = typeof value === "string" ? value : JSON.stringify(value);
  const maxBytes = maxOutputTokens * TOKEN_ESTIMATE_BYTES;
  if (Buffer.byteLength(text, "utf8") <= maxBytes) return text;
  const suffix = "\n[Summary truncated; request narrower information]";
  let out = "";
  for (const ch of text) {
    if (Buffer.byteLength(out + ch + suffix, "utf8") > maxBytes) break;
    out += ch;
  }
  return out + suffix;
}
