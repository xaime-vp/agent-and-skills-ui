---
name: delegation-triage
description: Decide whether independent test or documentation work needs a specialist handoff, reuse of an existing assignment or no new task. Use when review or implementation identifies specialist work, before creating issues; this skill does not dispatch workers.
---

# Delegation triage

Resolve ownership and overlap before dispatch. Reading an assignment or invoking
this skill does not authorize a new worker, issue or runtime lifecycle operation.
For review-only requests, report the proposed handoff without creating it.

Identify the parent PR, exact head branch/revision, concrete acceptance gap and
candidate editable paths. Read the repository's ownership rules: application repair,
running existing tests and authoring independent tests/documentation can have
different owners. The developer handles tightly coupled tests/docs by default.
Delegate substantial independent work, specialist expertise or an explicit user
assignment. No issue or justification is required just because file types differ.

Inspect linked issues and PR discussion first, then search the selected repository
for matching scope/branch. Check available worker status and delivered commits for
candidate assignments. A closed issue or completion comment alone does not prove
delivery; a lack of fresh comments alone does not prove the worker is idle.

Choose and report one disposition per acceptance gap:

| Evidence | Disposition |
| --- | --- |
| Existing delivered contribution meets the gap on the parent branch | Review/reuse it; create no task |
| Matching active assignment covers the gap | Track it; do not duplicate or edit its admitted scope |
| Existing assignment is editable and not executing/admitted | Reuse it with the missing scope, following preparation/admission rules |
| Distinct uncovered work remains | Prepare one scoped handoff when authorized |
| Optional/unrelated work, or no meaningful independent content change | Report or omit; do not create checklist-only tasks |
| Ownership, reservation or execution state cannot be established | Resolve that uncertainty before dispatching overlapping work |

For partial overlap, identify the uncovered acceptance criteria and exact additional
paths. Prepare a follow-up while the first worker runs, but serialize execution on
the same PR branch when required by its worker protocol. Do not dispatch a second
writer until the first has delivered or stopped and its reservations are clear.
Refresh the follow-up's source/head context after delivery; a changed head or scope
may invalidate a prepared proposal or admission.

Return the existing issue/worker links, covered and uncovered scope, current owner,
delivery evidence and next action. Use [bonsai-ci](../bonsai-ci/SKILL.md) for authorized
handoff execution or tracking in this workspace; it owns installed compatibility,
preparation and release-specific admission. Do not duplicate those mechanics here.
If approval is actually required by the selected installation, prepare the concrete
request and report that requirement; never post owner commands on their behalf.

During tracking, use bounded waits/backoff and prefer changes in worker state,
comments or branch commits over repeated full inspections. Review the actual
delivered diff and commit on the parent branch before accepting completion. Preserve
concurrent commits, and re-triage only when scope, ownership or delivery changes.
