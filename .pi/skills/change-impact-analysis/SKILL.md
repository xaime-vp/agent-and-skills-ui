---
name: change-impact-analysis
description: Trace changed configuration, defaults, concurrency, public APIs, schemas, security boundaries, deployment behavior or architecture to affected consumers, tests and documentation. Use during review or implementation of those changes; ordinary prose edits do not need this analysis.
---

# Change impact analysis

Establish what the requested diff changes and which dependent contracts must
change with it. This is analysis, not permission to repair every discovered gap.

Compare the intended base and current head. Start from changed symbols, settings,
limits and schemas; inspect their direct callers and consumers before broadening
searches. Trace further only where a concrete dependency or unresolved failure
path warrants it. Use repository/component guidance to identify important invariants.

For changed defaults, trace precedence through configuration, environment parsing,
entrypoints and effective runtime behavior. Check explicit overrides, absent values
and supported boolean forms when relevant. Inspect operator instructions and
examples: a default can change what a service does even with no newly queued work.

For changed capacity or concurrency, check limits, per-task identity, resource
ownership and branch/publication serialization. Inspect public schemas and UI/export
consumers for narrower representations of the new range. For API or schema changes,
check compatibility and downstream interpretation, not just producer validation.
Review security or deployment consequences when the diff changes those boundaries.

Distinguish source behavior, merged source and the selected installed release.
Source defaults do not prove deployed configuration. A historical transcript is
evidence of a past observation, not a current compatibility contract.

Produce a compact impact matrix:

| Changed behavior | Affected consumer/path | Evidence and consequence | Disposition |
| --- | --- | --- | --- |
| Actual setting, limit or contract | Exact caller, schema, guide or interface | Location and observable effect | Blocker, scoped correction, existing limitation or optional follow-up |

Determine whether each mismatch is introduced, exposed or unchanged by the PR.
Use base-revision evidence where necessary; say when causality is uncertain.
An existing limitation becomes blocking when the requested behavior depends on it.
Do not classify a legacy UI limit as harmless without checking the changed execution
path, or automatically expand an execution change into an unrelated UI redesign.

Return required corrections and relevant compatibility limits to the PR coordinator.
When independent test/documentation work is needed, use
[delegation-triage](../delegation-triage/SKILL.md) before creating an assignment.
Stop tracing when relevant consumers and invariants are accounted for and remaining
questions no longer affect the requested behavior or readiness decision.
