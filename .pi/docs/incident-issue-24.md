# Run accounting incident: issue #24 dispatch produced issue #25's work

**Date:** 2026-11-12 · **Repository:** `xaime-vp/constant-integration-ui` · **Severity:** low (docs-only change; no code path affected) · **Status:** accounting recorded, corrective actions pending

## Summary

An agent run was approved and dispatched for issue **#24** ("[Task] [P2] `import-dir` recursively sweeps nested directories, contradicting its documentation and the coordinator"), but the work it produced implements the task described in issue **#25** ("[Task] [P2] ARCHITECTURE.md still describes the ingestion coordinator as planned and omits delivered endpoints"). The resulting draft PR **#30** changes only `docs/ARCHITECTURE.md`; it contains none of #24's `import-dir` work.

## Timeline

| Time (UTC) | Event |
| --- | --- |
| 06:3x | Issues #21–#25 opened from a code-review pass, each with a schema-2 `agent-task` envelope. |
| ~06:35 | `/approve-agent` posted on **#24**; controller dispatched a run with ID `issue-24-approval-6816471383-44df631c9dd9`. |
| 06:35:24Z | Branch `agent/generalist/issue-24-approval-6816471383-44df631c9dd9` pushed. |
| 06:35:24Z | Draft **PR #30** opened: "[Generalist] [Task] [P2] ARCHITECTURE.md still describes the ingestion coordinator as planned and omits delivered endpoints", diff = `docs/ARCHITECTURE.md` only. |
| later | `bonsai-result` comment posted on **#24** linking PR #30. |
| after review | Mismatch identified during PR/branch accounting: the diff matches #25's envelope, not #24's. Tracking labels corrected and an accounting comment left on #24. |

## What mismatched

| | Approved for the run (#24) | Actually produced (PR #30) |
| --- | --- | --- |
| Task | Fix `import-dir` recursive sweep vs docs/coordinator semantics | Update stale delivered/pending claims in `docs/ARCHITECTURE.md` |
| Allowed files | `backend/__main__.py`, `docs/DEVELOPMENT.md`, `tests/test_backend.py`, `tests/test_cli.py` | `docs/ARCHITECTURE.md` |
| Issue whose envelope matches the diff | — | **#25** |

Two candidate explanations, not distinguishable from the repository record alone:

1. The controller selected **#25's envelope** while binding the run to #24's approval and run ID.
2. The controller sent #24's envelope correctly, but the agent executed a different task than approved (in which case it also wrote outside #24's `allowed_files`).

The run-ID string (`issue-24-approval-…`) and the `/approve-agent` target both point at #24; the envelope contents point at #25.

## Current state

- **PR #30** is open, draft, mergeable/clean, and its content is a correct implementation of **#25**. It was produced under #24's approval; #25 itself never received an `/approve-agent`.
- **#24's** task (`import-dir` semantics, `backend/__main__.py` + `docs/DEVELOPMENT.md` + tests) is **outstanding** — no branch or PR contains it.
- Labels applied during accounting: #21 and #25 → `agent-commit` (ready removed); #24 → `agent-feedback` (ready removed, parked).
- Branch `agent/generalist/issue-24-approval-6816471383-44df631c9dd9` is reserved by the open PR #30.

## Recommended follow-ups

1. **Review PR #30 on its content** (it is #25's task). If accepted, merge it and credit #25; keep the audit trail of which approval produced it.
2. **Investigate the dispatch path**: check the controller/listener logs for run `issue-24-approval-6816471383-44df631c9dd9` to confirm which envelope was sent. If the agent executed a task other than the approved envelope, that is an envelope-integrity failure in the delegation pipeline and must be fixed before further dispatches.
3. **Re-dispatch #24** with its correct envelope after PR #30 is merged or closed, freeing the branch reservation.
4. **Guardrail suggestion**: before a run starts, the controller (or the agent as a first step) should echo back the issue number, title and `allowed_files` from the envelope it received, so envelope/issue binding is verifiable in the run output.
