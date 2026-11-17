---
name: github-batch-publish
description: Publish multiple staged UTF-8 files from a local Git index to an existing GitHub PR using create_blob, create_tree, create_commit, and update_ref. Use when repeated GitHub blob uploads would waste model tokens; requires authorized scoped publication.
---

# GitHub batch publication from the index

This skill captures the repeated `read_git_chunk.py ... INDEX` and GitHub `create_blob` / `create_tree` sequence in the provided coding-session trace. The trace shows blob creation and tree construction starting, **not** confirmed branch publication. A usable publisher must also create a commit, update the intended PR ref, and verify the result.

Follow the [root developer contract](../../../AGENTS.md) and the [PR submission skill](../pr-submission/SKILL.md). The extension is a publishing mechanism, not a reviewer, test runner or grant of authority.

## Tool invocation

The project Pi extension [github-batch-publish.ts](../../extensions/github-batch-publish.ts) registers `github_batch_publish`. It requires local Git and a connected GitHub MCP with `get_pr_info`, `create_blob`, `create_tree`, `create_commit`, and `update_ref`. It uses Pi `ctx.executeTool` so the nested tool results do not appear as standalone model-facing messages. File contents **are sent to GitHub** as blob arguments and may appear in connector/session operational traces; the token reduction concerns model-facing output, not end-to-end confidentiality or API calls.

1. Inspect the **existing PR** and record its exact head SHA, head branch and head repository. Confirm the selected local checkout has that commit as `HEAD`; the tool checks that `origin` matches `owner/repo`. For new tasks, open the draft PR through the root workflow before using this tool. Do not create a second PR merely to use the tool.
2. Stage only intended changes with local Git. Use exact paths (no globs) and review the staged diff, secrets and tests yourself. The tool reads **Git index bytes**, not unstaged working-tree content; it does not review code. It supports added, modified and deleted UTF-8 text files, up to 60 paths and 2 MiB of nondeleted content. It rejects symlinks, submodules and binary/invalid UTF-8.
3. First call the tool with `action: "plan"`; examine its compact path/status/size inventory:

   ```json
   {"action":"plan","repositoryFullName":"owner/repo","repoPath":"target-checkout","branch":"feature","expectedHeadSha":"FULL_PR_HEAD_SHA","paths":["src/a.py","tests/test_a.py"],"maxOutputTokens":300}
   ```

4. Only when authorized to publish, use the same inputs with `action: "publish"`, the PR number, commit subject and `confirmPublish: true`:

   ```json
   {"action":"publish","repositoryFullName":"owner/repo","repoPath":"target-checkout","branch":"feature","expectedHeadSha":"FULL_PR_HEAD_SHA","prNumber":42,"paths":["src/a.py","tests/test_a.py"],"commitMessage":"Fix scoped behavior","confirmPublish":true,"maxOutputTokens":300}
   ```

5. The tool checks the PR head before and after the object uploads, creates a commit with the exact expected parent, and calls `update_ref` with `expected_sha` and `force: false`. On a conflict or unconfirmed result, inspect remote state **before** retrying. Unreferenced blobs/trees/commits may remain; they do not prove changes were published. Never force-push, merge, or deploy from this skill.
6. Read the final PR head and remote diff, run or inspect required checks for the exact published revision, then report observed evidence and any unrun checks. Keep the PR draft until separate owner action.

## Token and scope limitations

`maxOutputTokens` defaults to 300 (128–2000 accepted) and conservatively estimates output using 3 UTF-8 bytes/token. It is **not an exact model tokenizer guarantee**. The extension returns path summaries and SHAs, not source content. It does not limit the number of GitHub API calls, restrict arbitrary other tools, create approvals, or dispatch workers. For unavailable GitHub MCP capability or unsupported Pi nested-tool API, report the blocker and use only an authorized manually reviewed equivalent.

## Offline verification

Run `node --test .pi/extensions/github-batch-core.test.mjs`. These tests exercise a real temporary Git index with simulated GitHub replies; they do not establish that the installed Pi extension, live GitHub MCP or remote PR publication is functioning.

**Interactive publication:** `confirmPublish: true` is necessary but not sufficient: Pi asks the operator to confirm repository, PR, branch, expected head and file count before writing. Noninteractive clients fail closed; use a separately authorized trusted publisher rather than model-supplied confirmation.
