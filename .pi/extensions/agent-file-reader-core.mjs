/** Filesystem-only reader for scoped agent instructions; testable without Pi. */
import { readFile, realpath, stat } from "node:fs/promises";
import path from "node:path";

const MAX_FILE_BYTES = 1024 * 1024;
const MAX_OUTPUT_BYTES = 32 * 1024;
export const DEFAULT_MAX_LINES = 160;
export const MAX_LINES = 400;
export const DEFAULT_MAX_OUTPUT_TOKENS = 600;
export const MAX_OUTPUT_TOKENS = 4000;
// Approximate budgeting: 3 UTF-8 bytes per estimated token; not a model tokenizer.
const BYTES_PER_ESTIMATED_TOKEN = 3;

function containedIn(parent, candidate) {
  const relative = path.relative(parent, candidate);
  return relative === "" || (relative !== ".." && !relative.startsWith(".." + path.sep) && !path.isAbsolute(relative));
}

function relativePath(value, label) {
  if (typeof value !== "string" || !value.trim() || value.includes("\0")) {
    throw new Error(label + " must be a nonempty relative path");
  }
  if (path.isAbsolute(value) || path.win32.isAbsolute(value)) {
    throw new Error(label + " must be relative to the workspace");
  }
  const parts = value.split(/[\\/]+/).filter(part => part && part !== ".");
  if (parts.includes("..")) {
    throw new Error(label + " cannot contain parent-directory (..) segments");
  }
  return parts.length ? path.join(...parts) : ".";
}

function positiveInteger(value, name, max) {
  if (!Number.isInteger(value) || value < 1 || value > max) {
    throw new Error(name + " must be an integer between 1 and " + max);
  }
}

export function capTextToEstimatedTokens(text, maxOutputTokens = DEFAULT_MAX_OUTPUT_TOKENS) {
  positiveInteger(maxOutputTokens, "maxOutputTokens", MAX_OUTPUT_TOKENS);
  if (maxOutputTokens < 128) throw new Error("maxOutputTokens must be at least 128");
  const maxBytes = Math.min(MAX_OUTPUT_BYTES, maxOutputTokens * BYTES_PER_ESTIMATED_TOKEN);
  const originalBytes = Buffer.byteLength(text, "utf8");
  if (originalBytes <= maxBytes) return {text, truncated: false, estimatedTokens: Math.ceil(originalBytes / BYTES_PER_ESTIMATED_TOKEN)};
  const note = "\n[Output truncated; narrow the request or use a later offset.]";
  let remaining = maxBytes - Buffer.byteLength(note, "utf8");
  const chars = [];
  for (const ch of text) {
    const bytes = Buffer.byteLength(ch, "utf8");
    if (bytes > remaining) break;
    chars.push(ch);
    remaining -= bytes;
  }
  const output = chars.join("") + note;
  return {text: output, truncated: true, estimatedTokens: Math.ceil(Buffer.byteLength(output, "utf8") / BYTES_PER_ESTIMATED_TOKEN)};
}

/**
 * @param {{cwd:string, root?:string, filePath?:string, startLine?:number, startChar?:number, maxLines?:number, maxOutputTokens?:number}} args
 */
export async function readAgentFile({cwd, root = ".", filePath = "AGENTS.md", startLine = 1, startChar = 0, maxLines = DEFAULT_MAX_LINES, maxOutputTokens = DEFAULT_MAX_OUTPUT_TOKENS}) {
  positiveInteger(startLine, "startLine", 10000000);
  positiveInteger(maxLines, "maxLines", MAX_LINES);
  if (!Number.isInteger(startChar) || startChar < 0 || startChar > 10000000) throw new Error("startChar must be 0-10000000");
  positiveInteger(maxOutputTokens, "maxOutputTokens", MAX_OUTPUT_TOKENS);
  if (maxOutputTokens < 128) throw new Error("maxOutputTokens must be at least 128");
  const requestedRoot = relativePath(root, "root");
  const requestedFile = relativePath(filePath, "path");
  const basename = path.basename(requestedFile);
  if (basename !== "AGENTS.md" && basename !== "SKILL.md") {
    throw new Error("Only AGENTS.md and SKILL.md files may be read by this tool");
  }

  const workspace = await realpath(cwd);
  const targetRoot = await realpath(path.resolve(workspace, requestedRoot));
  if (!containedIn(workspace, targetRoot)) {
    throw new Error("root resolves outside the workspace");
  }
  const targetFile = await realpath(path.resolve(targetRoot, requestedFile));
  if (!containedIn(targetRoot, targetFile)) {
    throw new Error("path resolves outside the selected root (possibly via symlink)");
  }
  const info = await stat(targetFile);
  if (!info.isFile() || info.size > MAX_FILE_BYTES) {
    throw new Error("Instruction file must be a regular file no larger than 1 MiB");
  }

  const raw = await readFile(targetFile, "utf8");
  if (raw.includes("\0")) {
    throw new Error("Instruction file contains NUL bytes");
  }
  const lines = raw.replace(/\r?\n$/, "").split(/\r?\n/);
  if (startLine > lines.length) {
    throw new Error("startLine " + startLine + " exceeds file length (" + lines.length + " lines)");
  }
  if (startChar > Array.from(lines[startLine - 1]).length) throw new Error("startChar exceeds the selected line length");
  const displayRoot = path.relative(workspace, targetRoot).split(path.sep).join("/") || ".";
  const displayPath = path.relative(targetRoot, targetFile).split(path.sep).join("/");
  const header = displayRoot + "/" + displayPath + " (L" + startLine + (startChar ? "+" + startChar : "") + "; " + lines.length + " total lines)\n";
  const maxBytes = Math.min(MAX_OUTPUT_BYTES, maxOutputTokens * BYTES_PER_ESTIMATED_TOKEN);
  let remaining = maxBytes - Buffer.byteLength(header, "utf8") - 104;
  if (remaining < 24) throw new Error("maxOutputTokens is too small for the file path and continuation metadata");

  const chunks = [];
  let nextStartLine = startLine;
  let nextStartChar = startChar;
  let shownLines = 0;
  let endLine = startLine;
  for (let i = startLine - 1; i < Math.min(lines.length, startLine + maxLines - 1); i++) {
    const chars = Array.from(lines[i]);
    const charStart = i === startLine - 1 ? startChar : 0;
    const prefix = (chunks.length ? "\n" : "") + "L" + (i + 1) + (charStart ? "+" + charStart : "") + ": ";
    const prefixBytes = Buffer.byteLength(prefix, "utf8");
    if (prefixBytes > remaining) break;
    chunks.push(prefix);
    remaining -= prefixBytes;
    shownLines++;
    endLine = i + 1;
    let index = charStart;
    while (index < chars.length) {
      const bytes = Buffer.byteLength(chars[index], "utf8");
      if (bytes > remaining) break;
      chunks.push(chars[index]);
      remaining -= bytes;
      index++;
    }
    if (index < chars.length) {
      nextStartLine = i + 1;
      nextStartChar = index;
      break;
    }
    nextStartLine = i + 2;
    nextStartChar = 0;
  }
  if (!shownLines) throw new Error("Output budget cannot fit a line prefix; increase maxOutputTokens");
  const hasMore = nextStartLine <= lines.length;
  const trailer = hasMore ? "\n[Truncated; continue with startLine=" + nextStartLine + ", startChar=" + nextStartChar + ".]" : "";
  const content = chunks.join("");
  const text = header + content + trailer;
  const estimatedTokens = Math.ceil(Buffer.byteLength(text, "utf8") / BYTES_PER_ESTIMATED_TOKEN);
  if (estimatedTokens > maxOutputTokens) throw new Error("Internal output-budget violation");
  return {
    root: displayRoot, path: displayPath, content, text, startLine, startChar,
    endLine, totalLines: lines.length, truncated: hasMore,
    maxOutputTokens, estimatedTokens,
    nextStartLine: hasMore ? nextStartLine : null,
    nextStartChar: hasMore ? nextStartChar : null,
  };
}
