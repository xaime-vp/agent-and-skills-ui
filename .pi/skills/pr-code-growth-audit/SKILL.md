---
name: pr-code-growth-audit
description: Audit PRs for avoidable code insertions, stacked-branch double counting, duplicated implementations, redundant abstractions and reuse opportunities. Use when asked to reduce lines added or review code growth before merging.
---

# Audit PR code growth

Find the smallest **complete and safe** implementation, not simply the smallest diff. Never weaken test coverage, permission checks, provenance, persistence, recovery, auditability or public compatibility just to reduce line count.

**Authority:** Read-only unless the user separately requests implementation. Reviewing does not authorize branch edits, posting comments, creating issues, CI reruns, merges or deployment. Follow the root AGENTS.md and the target repository instructions. For multiple PRs, use the multi-pr-review skill; for substantive promises, implementation-completeness; for contract changes, change-impact-analysis.

## Pin the evidence

1. Identify the repository, requested PRs (or all open PRs if requested) and merge target. Read repo instructions, relevant architecture and existing issues/PRs to avoid duplicate recommendations.
2. For each PR, capture number/link, title and promise, draft status, exact base branch/SHA, exact head SHA, dependency, diff, changed files, review findings and current-head CI. Refresh if a head moves.
3. Read complete file patches and relevant base/current implementation, callers and tests. Do not make a removal recommendation from a PR title or an absence of static references alone.
4. Categorize additions and deletions as runtime, tests, docs/design/pseudocode, configuration/scripts or generated/other. Account for renames, moved code and unchanged reused files.

## Calculate growth correctly

- Show per-PR additions, deletions and net changes **against each PR's actual base**. Label the aggregate as **summed PR deltas**, not unique merged growth.
- Build a PR dependency DAG. Recognize stacked branches, repeated commits, cherry-picked fixes and inherited implementations. A PR based on another PR contributes its incremental diff; summing all PRs does not necessarily describe what main will gain.
- Compare identical patches and file contents across branch heads. Explain which lines are shared and which are distinct; never double count shared patches in a *unique-footprint estimate*.
- For a definitive unique count, evaluate an authorized, isolated integration checkout with recorded merge order, then compare the resulting tree to the pinned main commit. Do not alter the user's working tree, rewrite branches or imply a conflict-free integration without verifying it.
- If integration is unavailable, state **unique merged footprint not verified**. Distinguish measured line deltas, rough savings ranges and feature deferrals; do not add them into one guaranteed reduction.

## Locate unnecessary insertions

Review opportunities in this order:

1. **Repeated PR repairs:** identical CI, policy or fixture patches carried by many unrelated PRs. Recommend merging a canonical repair first, then updating branches to remove repeated diff noise while preserving tests.
2. **Divergent copies:** two PRs create or replace the same implementation. Compare current file blobs, method inventory, callers and behavior; select an owner only after confirming no important functionality would be lost.
3. **Duplicate design representation:** pseudocode types/functions or prose mirrors executable APIs. Prefer one authoritative implementation and concise design rationale, but preserve intentional stable specifications.
4. **Missed reuse:** new parsers, registries, validation, state, telemetry, transport or scheduling logic duplicates existing tested code. Trace imports and consumers; ensure error semantics, ordering, dependency direction and security boundaries remain valid.
5. **Unnecessary generalization:** speculative adapter layers, large registries, pass-through helpers and configurable abstractions with no supported active use. Do not abstract merely to decrease repeated lines or remove deliberate extension points.
6. **Premature breadth:** subworkflows, parallel execution, migration, observability or advanced routing before the minimal end-to-end path works. Propose deferral explicitly; do not claim deferred behavior remains implemented.
7. **Low-value churn:** unrelated edits, repetitive fixtures or redundant wrappers. Keep meaningful deterministic tests and compatibility aliases where external consumers need them.

Assign one disposition per candidate: **consolidate now**, **simplify with proof**, **defer by scope decision**, **keep**, or **uncertain**.

## Safety and proof obligation

Preserve task/source/attempt identity; approved scopes and trusted policy ceilings; path and tool permissions; credential isolation; atomic ownership, retry and cancellation; durable operation intent and restart reconciliation; external-write safety; artifact integrity and provenance; public schema compatibility; diagnostics; and necessary assertions. Any saving that compromises these is invalid.

For each candidate record the affected PRs, full reviewed head SHA, file/symbol, concrete duplicated or excessive behavior, proposed alternative, dependents, why it remains correct, risk, tests and an honest savings estimate. Use deterministic offline tests where possible; check failing CI and existing review findings. Review the changed path as well as reachable runtime entrypoints. Confirm that an existing PR/issue does not already cover the work.

Do not present code moves as runtime savings. Do not remove tests to meet a line-count target. Treat source, merged source and installed worker release as distinct states.

## Report format

Produce a short evidence-backed review with:

1. **Snapshot** — target repository and pinned main/head revisions, PR scope, limitations.
2. **Numbers** — per-PR +/-/net, breakdown by runtime/tests/docs, summed PR deltas versus verified unique merged footprint or unknown.
3. **Ranked actions** — PR/file links, precise evidence, disposition, savings as measured or estimated, risk, required validation.
4. **Minimal viable merge plan** — canonical PRs, dependency ordering, branch updates, acceptance tests, consciously deferred work.
5. **Bottom line** — what to consolidate, keep, defer and investigate; distinguish mechanical GitHub mergeability from code-review readiness.

Stop when the evidence supports the highest-impact recommendations. No speculative mass deletion, unsolicited edits, or merging. If explicitly asked to implement, switch to the root PR repair/development workflow and preserve ongoing work.

## Example request

Audit all open PRs in xaime-vp/constant-integration for avoidable code growth. Normalize stacked-PR deltas, identify repeated CI fixes and divergent implementations, reuse existing code when safe, and recommend the smallest complete end-to-end delivery. Read-only; do not change PRs.
