# Constant Integration source capabilities and profile routing

**Compared:** `xaime-vp/constant-integration` `main` at `a0810fccb6ed491dbb552b616b0717cabe976a12` on 2026-11-16. This is a source snapshot, **not an installed-worker audit**. Recheck the current source and the selected installation's sealed release/configuration before executable tasks.

This document is developer-workspace guidance, not a copy of the protected runtime profiles. The [role contract](https://github.com/xaime-vp/constant-integration/blob/main/docs/AGENT_ROLES.md), [runtime profile registry](https://github.com/xaime-vp/constant-integration/blob/main/workers/bonsai/runtime_profiles.py), [intake parser](https://github.com/xaime-vp/constant-integration/blob/main/orchestrator/intake.py), and the selected **installed** policy remain authoritative. Where an older guide disagrees with those source files, inspect the current code rather than executing an example blindly.

## Source-supported roles

| Role / issue label | Writes within approved scope | Review / publication |
| --- | --- | --- |
| `agent:coder` | Application code and directly related tests/docs **only when explicitly in `allowed_files`/`allowed_filetypes`** | Protected checks, frozen candidate, embedded independent read-only Reviewer, supervisor-owned draft PR |
| `agent:test-specialist` | Tests, fixtures and test configuration; not application fixes | Protected checks, frozen candidate, embedded independent read-only Reviewer, supervisor-owned draft PR |
| `agent:documentation` | Documentation (`.md` only); not application changes | Protected checks and draft PR **without** embedded model review |
| `reviewer` | None; read-only source/diff/check evidence and advisory report | Embedded or trusted-configured commit review; no tests, approval, repair or merge |
| `supervisor` | Trusted state, Git, checks and publication operations | Deterministic authority; not an issue implementation route |
| `github-admin`, `planner`, `researcher` | None; operator-invoked advisory reports on a saved issue/PR snapshot (`researcher` adds bounded anonymous public-web retrieval) | Read-only artifact under `private/results/KEY/artifact.json`; they never schedule implementation, push repairs or merge |

`agent:generalist` and `agent:tests` are retired source routes, not aliases. A root-workspace **Git developer** implements its own authorized changes under [AGENTS.md](../../AGENTS.md); that external workflow is distinct from intentionally delegating an entire implementation to `agent:coder`. Do not create both writers for the same files/branch.

The protected [coder prompt](https://github.com/xaime-vp/constant-integration/blob/main/profiles/coder.md) uses *locate → decide → implement → verify → finish*, targeted retrieval, bounded repair and concise evidence. A workspace guide must never impersonate it or give a Pi worker permission to commit, push, publish, launch arbitrary children or merge. Native read-only consultation is selected by the supervisor under explicit installed policy.

## Intake and delivery

- **Target instructions:** root `AGENTS.md` is optional in current Constant Integration source; when present, root/nested instructions are read as context alongside sealed role guidance. The source checkout may legitimately have no root `AGENTS.md`; do not block execution or invent one to satisfy an obsolete preflight rule.
- **Legacy task:** schema 2 is a single run, schema 3 is an ordered plan; schema 4 is an opt-in new-draft post-publication lifecycle. A legacy `pull_request` number selects an existing same-repository PR for schema 2/3; omit it for a new draft. Schema 4 rejects `pull_request`. Read [envelope](https://github.com/xaime-vp/constant-integration/blob/main/docs/submitting-tasks/envelope.md) and [repair contract](https://github.com/xaime-vp/constant-integration/blob/main/docs/POST_PUBLICATION_CONTRACT.md).
- **Free-form issue:** the owner requests research via `/prepare-agent`; an operator performs exclusive, stopped-state `prepare-issue` with selected committed evidence, explicitly choosing `--target-pr NUMBER` for an existing PR. Inspect and verify the sealed proposal and exact destination. The source-preparation path can bind the selected supported implementation label, including coder. An issue/PR mention is not an authority or destination binding.
- **Current readiness:** after final verified preparation or a complete legacy envelope, remove `blocked`, add `ready` and retain **exactly one matching** `agent:*` implementation label. Current source does not use `/approve-agent` for admission; historical installed releases may. Do not post owner-only commands or change the installation as a side effect of a skill.
- **Scope and parallelism:** exact `allowed_files` and optional `allowed_filetypes` form a union within the approved project. Optional `read_filetypes` limits file reads and disables worker shell/self-check tools; the supervisor still runs protected checks. Shared slots support **1–10** (new preparations default 10; omitted legacy config retains 1). The same issue, PR or destination branch serializes; independent pinned PR branches can have overlapping paths, but semantic/external-resource dependencies must still be blocked.
- **Commit reviews:** fresh preparations enable `automatic_pr_reviews` (Compose also defaults `BONSAI_AUTOMATIC_PR_REVIEWS=true`); an installed configuration without the key keeps its historical off state. Observe the selected installation. Review is advisory `COMMENT` on a pinned commit, not a CI check or repair authorization.
- **Automatic repair (opt-in policy):** `review_repair` defaults to high severity, `agent/` branches and two rounds. A trusted policy file may set `"branch_prefixes": []` to allow any same-repository PR head branch except the base branch; older releases reject the empty list, so keep a compatible nonempty policy for rollback. Repairs still require a completed automatic review, eligible findings, exact scope, passing protected checks and a reviewed head.

## Selective Pi role harnesses (integrated in source)

Constant Integration `main` now vendors the reviewed `agent-and-skills`
role bundles as verified release-owned resources. See
[`docs/ROLE_HARNESSES.md`](https://github.com/xaime-vp/constant-integration/blob/main/docs/ROLE_HARNESSES.md)
and `workers/bonsai/harness_resources.py`. Operator-controlled
`harness_roles` is a trusted JSON list drawn from `coder`,
`test-specialist`, `documentation`, `reviewer`. Fresh preparations enable all
four; `--harness-roles '[]'` (Compose `BONSAI_HARNESS_ROLES=[]`) opts out, and an
installed configuration that omits the key preserves the old launch. Each
selected role adds one method skill and six read-only helper tools. The trusted installer seals the pinned bundle before
execution and the supervisor selects exactly one matching role per session.

This is **source support**, not proof that any existing container is using it.
Inspect the installation's release identity and configured `harness_roles`
before asserting activation. The platform vendors upstream
`agent-and-skills` revision
`021f26d76810dd00d025207b013d6afa139e55e5`
with SHA-256 bundle digest
`af06075ccc9f52f2aff93320de260489e667fbcb512e610ce40a4f7129fa5735`.
The workspace exporter and source checkout may be newer; compare the pinned
bundle explicitly when refreshing, and don't infer cost benefits from smoke tests.

## Advisory agents (`agent_harness`)

Fresh preparations enable `github-admin`, `planner` and `researcher` with
read-only defaults (`apply_labels`, `mark_ready` and `request_ci` false, 300s
timeout, web research unavailable). Pass `--no-agent-harness` (Compose
`BONSAI_AGENT_HARNESS=false`) to disable them; an installed configuration keeps
its saved policy across upgrades. To customize, supply an owner-authored policy
file with `--agent-harness-policy` / `BONSAI_AGENT_HARNESS_POLICY`; it cannot be
combined with `--no-agent-harness`.

These roles are **not** issue implementation routes and never run from the
polling loop. An operator invokes one explicitly while stopped, e.g.
`python -m workers.bonsai.controller --config ... --agent-role planner --agent-issue N --agent-question '...'`.
`researcher` additionally needs a `web` policy with an owner-supplied HTTPS
search endpoint and exact host allowlist; without it, direct research fails
clearly instead of inventing sources. A single `github-admin` run may make at
most one researcher and one planner follow-up. See
[`docs/ADVISORY_AGENTS.md`](https://github.com/xaime-vp/constant-integration/blob/main/docs/ADVISORY_AGENTS.md).

## Executing-profile token accounting

Each relay observation now carries the executing role (implementation, embedded
review, specialist, advisory or supervisor), plus phase, span and a per-attempt
`step_seq` ordinal. Attribution lives in existing `model_usage_events.data` JSON,
so there is no runtime SQLite migration and old rows stay unattributed. Both
`model_call.observed.v1` and `usage.observed.v1` export it; absent counters stay
unknown and an explicit zero stays zero. The dependent UI exposes
`/api/v1/analytics/usage-by-profile`, `usage-calls` and `usage-steps` history
reads, which need the normal export/import path and do not prove live freshness.
See [`docs/TOKEN_USAGE_BY_PROFILE.md`](https://github.com/xaime-vp/constant-integration/blob/main/docs/TOKEN_USAGE_BY_PROFILE.md).

## Available source features versus activation

[Repository consultation](repository-consultation.md) is implemented for an
opted-in exact-path schema-2 coder with finite budgets. The supervisor supplies
native `bonsai_call_agent`, captures current candidate bytes and runs a contained
read-only researcher before the same coder continues. The selected parent has no
shell. No researcher issue label, writer delegation, recursive/web call or
automatic process-loss resume is available. Explicit delegation uses schema-6
State and private artifact backups; unknown calls retain reservations. This
support is independent of the optional six-tool role helper bundles.

| Feature | Source status | Do not assume |
| --- | --- | --- |
| Coder profile, test and documentation specialist routes | Implemented in source and guarded by admission/scope | The installed sealed release has that role enabled |
| Coder repository consultation | D1-D5 native tool, durable calls/artifacts, bounded dispatch and same-task continuation under explicit delegation policy | An installation enables it, omitted budgets select it, or consultation grants writes/review/approval |
| Schema-4 post-publication CI/review/repair loop | Source-enabled behind trusted installation policy and per-task schema-4 authorization | Schema-2/3 tasks automatically repair or any installed worker has opted in |
| Reusable workflow components, model inventory/routing, parallel group, migration/projections | Source APIs with offline tests, disabled/explicit supervisor integration path | A merged component is active listener orchestration or automatic multi-model dispatch |
| Selective role helper bundles | Vendored, hash-pinned and opt-in via trusted `harness_roles` config | Any particular installed worker has enabled the helpers, or smoke tests prove successful tasks |
| Model selection and effort | New preparations default to `google/gemini-4-hydrogen:floor`; one configured model serves implementation **and** review; `thinking_level` is trusted policy | Source defaults change an existing installation, or effective hosted effort/cost is known |
| Saved diagnostics, history export, delivery baseline | Read-only APIs/CLIs and synthetic coverage | Saved records prove current CI/liveness, owner acceptance or complete billing |

For workflow details use [routing](https://github.com/xaime-vp/constant-integration/blob/main/docs/agent-workflows/model-routing.md), [rollout](https://github.com/xaime-vp/constant-integration/blob/main/docs/agent-workflows/rollout.md), [worker README](https://github.com/xaime-vp/constant-integration/blob/main/workers/bonsai/README.md), and [delivery baseline](https://github.com/xaime-vp/constant-integration/blob/main/docs/DELIVERY_BASELINE.md). The current source contains some historical prose that still mentions older roles; confirm live behavior in the registry, parser and role contract rather than inferring from those passages.

## Evidence and update checklist

Before telling an operator an action is executable: identify the target repo and task/PR, pinned platform/source SHA, **installed sealed release and enabled profiles**, admission mode, scope/check policy, selected model, active slots and current PR head. Validate envelopes against matching source; preserve approval/revocation/history across migrations. Distinguish model self-report, protected checks, current-head GitHub CI, independent review, actual provider charges and owner acceptance. Unknowns remain unknown.

For a workspace sync PR, compare this capability map with `AGENTS.md`, `agents/*/AGENTS.md`, `.pi/skills/bonsai-ci/`, `docs/agent-setup/` and source references; correct stale role labels/limits/commands before creating extra skills. Keep user-facing skills outside the platform's sealed runtime `profiles/` and `workers/bonsai/pi_assets/skills/`.
