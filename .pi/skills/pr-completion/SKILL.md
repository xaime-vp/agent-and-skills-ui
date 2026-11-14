---
name: pr-completion
description: Finish an existing Constant Integration UI PR or assess readiness using delivered worker changes, checks and relevant browser evidence. Readiness-only stays read-only; merge and deployment need separate authorization.
---

# Complete an existing PR

Read the [root contract](../../../AGENTS.md) and continue the requested PR's current
branch. Use [pr-repair](../pr-repair/SKILL.md) for conflicts and scoped corrections,
[implementation-completeness](../implementation-completeness/SKILL.md) to compare
promises with delivered behavior, and [pr-validation](../pr-validation/SKILL.md)
for revision-bound checks. Load other supporting skills only when needed.

A readiness/status-only request stays read-only: no source edits, issue creation,
PR metadata updates or posted reviews. A finish request authorizes scoped repairs
under repository ownership; merge, deployment and live worker activation remain
separate. An already-complete PR needs verification, not another commit.

Record the actual repository, PR URL, base/head refs and full SHAs, current draft
state and mergeability. Inspect existing reviews, linked assignments and available
checks. Confirm the local checkout matches that head; use an isolated worktree
when it contains unrelated work. Preserve concurrent commits and never force-push
over another contributor. A closed issue is not delivery evidence: inspect the
actual commit and files on the parent branch.

Own UI application repairs; delegate meaningful new tests/documentation through
existing-PR issues. Preserve sanitized-export and read-only UI boundaries. Use
ui-verification and ui-browser-verification when their conditions apply. Follow
required worker delivery and checks with bounded waits and inspect stalled
prerequisites. Keep the parent informed; stop at complete evidence or a concrete
external blocker. Do not start live workers as an incidental completion step.

Use connected GitHub tools when sufficient. Discover live schemas and capabilities;
do not assume a Codex-only agent role or Pi-only nested-tool API exists. If an
authorized subagent is available, assign one executor per PR and reuse its evidence;
otherwise execute directly. Do not launch duplicate local and repository workers.

Before writing, refresh the head. Review the final combined diff, retain author
provenance and revalidate affected work if the head moved. Update authorized PR
descriptions through [pr-submission](../pr-submission/SKILL.md). Keep required missing
work in draft. Unknown mergeability and missing or pending checks are not passes.

Report URL, branch, reviewed/published SHA, repairs or findings, checks actually
run, observed asynchronous status, linked worker issues and remaining work.
Separate application delivery, review readiness and verified merge readiness.
