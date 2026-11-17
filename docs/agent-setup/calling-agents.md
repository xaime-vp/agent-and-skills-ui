# Use workspace skills and call a Bonsai agent

Use this guide from the `agent-and-skills` developer workspace on `main`.
The default external target is `xaime-vp/constant-integration`, checked out in
`constant-integration/`; use another target only when the user selects it.
Application issues and PRs belong to that selected repository. Changes to this
instruction workspace use their own branch and PR in `agent-and-skills`.

## Choose and invoke a skill

In a client supporting named skill invocation, request the skill with `$name`.
If discovery is unavailable, ask the client to read the linked `SKILL.md` and its
relevant references. Start from this workspace and identify the external checkout
explicitly. Invocation loads guidance; it does not itself launch a worker or
authorize GitHub writes, installation changes, merging or deployment.

| Skill | Use it for | Example request |
| --- | --- | --- |
| [skill-maintenance](../../.pi/skills/skill-maintenance/SKILL.md) | Maintain this harness without changing its role | `Use $skill-maintenance to adapt this skill for the current client.` |
| [pr-repair](../../.pi/skills/pr-repair/SKILL.md) | Coordinate existing-PR review, authorized implementation and repairs | `Use $pr-repair to review PR <URL> and implement scoped corrections.` |
| [pr-completion](../../.pi/skills/pr-completion/SKILL.md) | Delegate PR completion to a subagent with connected GitHub tools and shell/Git access | `Use $pr-completion to finish PR <URL>.` |
| [multi-pr-review](../../.pi/skills/multi-pr-review/SKILL.md) | Review several PRs in separate worktrees with evidence for each | `Use $multi-pr-review to review PRs <URL> and <URL> independently.` |
| [implementation-completeness](../../.pi/skills/implementation-completeness/SKILL.md) | Compare promised behavior with implementation and assertions in every substantive review | `Use $implementation-completeness to compare PR <URL> with its acceptance criteria.` |
| [bug-reproduction](../../.pi/skills/bug-reproduction/SKILL.md) | Reproduce a suspected defect with isolated state and targeted failure injection | `Use $bug-reproduction to verify this suspected startup failure in PR <URL>.` |
| [integration-path-validation](../../.pi/skills/integration-path-validation/SKILL.md) | Exercise changed startup/import/packaging and CI dependency boundaries | `Use $integration-path-validation to check startup and the clean CI environment for PR <URL>.` |
| [state-recovery-validation](../../.pi/skills/state-recovery-validation/SKILL.md) | Check interrupted writes, retries, checkpoint consistency and duplicate delivery | `Use $state-recovery-validation to verify checkpoint recovery in PR <URL>.` |
| [change-impact-analysis](../../.pi/skills/change-impact-analysis/SKILL.md) | Trace changed defaults, concurrency and contracts to consumers | `Use $change-impact-analysis to assess the changed runtime defaults in PR <URL>.` |
| [delegation-triage](../../.pi/skills/delegation-triage/SKILL.md) | Check ownership and existing assignments before issuing specialist work | `Use $delegation-triage to identify documentation gaps not covered by the active workers for PR <URL>.` |
| [pr-validation](../../.pi/skills/pr-validation/SKILL.md) | Select checks and assess evidence for the combined PR revision | `Use $pr-validation to verify PR <URL> against its final head and required checks.` |
| [bonsai-ci](../../.pi/skills/bonsai-ci/SKILL.md) | Prepare a supervised coder task or test/documentation contribution to a parent PR | `Use $bonsai-ci to prepare regression coverage for PR <URL> in <owner/repo>.` |
| [bonsai-containers](../../.pi/skills/bonsai-containers/SKILL.md) | Inspect or perform requested worker lifecycle operations | `Use $bonsai-containers to inspect the installation bound to <owner/repo> and report its sealed revision and enabled profiles.` |
| [pr-submission](../../.pi/skills/pr-submission/SKILL.md) | Prepare/update the parent PR with validation and contribution evidence | `Use $pr-submission to update PR <URL> from its current diff and observed checks.` |
| [github-batch-publish](../../.pi/skills/github-batch-publish/SKILL.md) | Publish multiple explicitly staged files to an existing PR through a compact Pi tool | `Use $github-batch-publish to plan the staged paths in PR <URL>; publish only once authorized.` |
| [codex-cli-mcp](../../.pi/skills/codex-cli-mcp/SKILL.md) | Requested local Codex CLI work and existing approved GitHub MCP connections | `Use $codex-cli-mcp for <task> in <checkout>, using the already-connected GitHub tools.` |
| [agent-file-inspection](../../.pi/skills/agent-file-inspection/SKILL.md) | Read the applicable agent/skill instruction files | `Use $agent-file-inspection to show agents/review/AGENTS.md and its scope.` |
| [skill-tool-invocation](../../.pi/skills/skill-tool-invocation/SKILL.md) | Call an available tool explicitly referenced by another skill | `Use $skill-tool-invocation to run the read_agent_file tool named by $agent-file-inspection.` |

Use connected GitHub tools directly when already available; skill invocation does
not require starting another coding client. Installation/startup and worker
approvals retain their own authorization requirements. Follow the
[root workflow](../../AGENTS.md) and the selected target's instructions.

For existing PRs, start with `pr-repair`; it loads supporting skills only when
their conditions apply. A plain "review PR" stays read-only. "Review and implement"
also requests scoped corrections under the ownership rules. Continue the existing
PR/branch and select quick, standard or deep investigation based on the diff and
risk; all modes retain required repository checks. See
[existing-PR routing](developer-workflow.md#skill-routing-for-existing-pull-requests).

When several PRs are named, also use `multi-pr-review` to isolate their checkouts
and evidence. The review skills include four standard-library Python helpers;
see [review tools](https://github.com/xaime-vp/agent-and-skills/blob/a701dcf2de332cce285b49c0b7c609f2d75d4328/tools/README.md#review-evidence-tools) for their paths and
CLI entrypoints. They do not publish reviews, repair PRs or start Bonsai workers.

## Select the worker role

In the **developer-led** path, the root developer implements application code and related tests/docs
and opens its parent draft PR before specialist contributions. For an explicitly
delegated autonomous coding task, the `agent:coder` supervisor is the alternative
implementation owner and must not compete for the same branch/files. Verify the
selected sealed installation supports the requested route; source support does
not establish deployment. See [current capabilities](platform-capabilities.md).

| Assignment / Role | Current source role / issue label | Delivery evidence & scope |
| --- | --- | --- |
| Scoped implementation | `agent:coder` | Approved application code and explicitly scoped related tests/docs; protected checks and embedded independent read-only review |
| Regression coverage | `agent:test-specialist` | Exact tests/fixtures/test configuration, protected check outcomes, embedded read-only review |
| Documentation | `agent:documentation` | Exact documentation changes and protected check outcomes; no embedded model reviewer |
| Commit / candidate review | `reviewer` (no issue label; `workers/bonsai/reviewer.py`) | Read-only review distinguishing substantive blockers from optional suggestions without expanding approved scope; embedded for `coder` and `test-specialist` or automatic PR commit `COMMENT` when `automatic_pr_reviews: true` |
| Coordinator | `supervisor` (no issue label; `workers/bonsai/supervisor.py`) | Deterministic authority, scope, freeze, termination, and honest evidence; initial front-end assignment/prompting only, no backend review role |
| Admission control | `ready` / `blocked` labels | `ready` + no `blocked` + single matching `agent:*` label admits current revision (`admission_mode: ready`) |

Generalist/tests are retired source routes, not aliases. Runtime roles are
launched by the supervisor after admission, not by invoking a role name in chat
or spawning a duplicate local subagent. The developer owns application repairs in the developer-led path; a separately authorized coder follows its supervisor-owned implementation and repair policy.

An admitted, eligible coder can also receive native `bonsai_call_agent` under an
explicit installed delegation policy. It asks a read-only repository researcher
about a captured candidate and continues the same task; it has no implementation
issue label. Follow [repository consultation](repository-consultation.md) for the
call example and availability checks. It is separate from `/prepare-agent`,
standalone advisory research and developer-client subagents. The helper bundle
does not register it; an unavailable tool is not permission to launch a child.

## Request a contribution

For a deliberately supervised **code** task, use [the coder assignment guide](../../agents/coding/AGENTS.md) and `$bonsai-ci`, select `agent:coder`, and choose **new PR or existing PR** explicitly through the executable envelope/operator. The root developer must not duplicate the implementation. Schema 4 is separate, trusted-opt-in and restricted to new drafts; source workflow components and model routing are not evidence of active installed dispatch.

For a **developer-led test/documentation contribution**, replace the bracketed values and give the coding client this prompt:

```text
Use $bonsai-ci to create or update a [test-specialist | documentation] handoff.
Repository: [owner/repo selected for this task]
Parent PR: [URL and number]
PR base: [exact base branch]
Required delivery branch: [exact parent PR head branch]
Implementation commit: [current SHA]
Goal and evidence: [observable behavior, source paths, reproduction/PR links]
Acceptance: [test assertions/edge cases or documentation claims/examples to verify]
Scope and dependencies: [known candidate files, boundaries and prerequisites]

Search for an existing matching issue first. Verify the target-bound sealed
installation and select agent:test-specialist for tests/fixtures/test configuration
or agent:documentation for documentation. Keep application code with the developer.
Preserve all parent-branch commits and contribute to this existing PR.

Use prose preparation when exact scope or protected checks need research. Select
the matching role label (agent:test-specialist or agent:documentation) and keep
blocked until finalized/prepared; use operator --target-pr NUMBER.
For a verified legacy schema-2/3 envelope, use numeric pull_request instead.
On current source (admission_mode: ready), admit verified issues/proposals by
removing blocked and adding ready (older releases require /approve-agent).
Do not post owner preparation or approval commands for me. Return the issue link,
verified facts, gaps and exact next owner/operator action. Track authorized
delivery and report the delivered SHA, actual check outcomes and final-head
GitHub CI separately.
```

Test assertions should be independently authored; report application defects
instead of widening scope. Documentation acceptance includes verifying paths,
links, commands and supported behavior. Use the
[assignment guides](../../AGENTS.md#repository-and-authority-boundaries)
and [handoff template](handoff.md) for contribution-specific detail.

## Turn the request into executable work

1. Finalize the issue, verify prerequisites, keep `blocked`, and select exactly
   one matching role label (`agent:test-specialist` or `agent:documentation`).
   A label or PR mention alone neither authorizes work nor selects delivery.
2. For prose issues, the configured owner posts standalone `/prepare-agent` after
   the final edit. The operator follows [free-form preparation](free-form-issues.md)
   with committed evidence and `--target-pr NUMBER`. Preparation is exclusive and
   requires confirmed-stopped processes; it does not stop a listener itself.
3. Inspect the sealed role, exact scope, protected checks, limits and pinned PR
   destination (`inspect-preparation KEY`), and resolve any gaps.
4. For a complete verified legacy envelope, validate with the
   [offline validator](https://github.com/xaime-vp/agent-and-skills/blob/a701dcf2de332cce285b49c0b7c609f2d75d4328/tools/README.md).
5. On current source (`admission_mode: ready`), admit the verified proposal or
   legacy envelope by removing `blocked`, adding `ready`, and retaining the
   single matching `agent:*` label (no `/approve-agent` comment is needed;
   older installed releases still require `/approve-agent <full-digest>` or
   standalone `/approve-agent`). The already authorized listener admits work;
   loading a skill does not authorize starting or upgrading it.
6. Serialize tests and documentation targeting one PR. Verify actual delivered
   commits and reprepare stale proposals after head changes. Keep failed/unrun
   checks, applicable model review and final-head CI distinct. Use `pr-submission`
   to reconcile the PR with that evidence. Merge remains an owner decision.

## Follow automatic PR review

There is no issue implementation label or owner slash command for this reviewer.
On a compatible installation, trusted `automatic_pr_reviews: true` enables polling
of unseen commits on open PRs in its bound repository. Direct preparation defaults it off, while container deployment templates currently default it on; inspect
existing configuration read-only; use `bonsai-containers` for separately authorized
configuration/lifecycle changes. A contribution request does not enable reviews.

With the opt-in already enabled, follow the review for the actual PR commit and
report its advisory findings. Fixes belong to the developer or a separately scoped
test/documentation assignment. Preserve review records, attempts and publication
markers; do not reset them to retrigger a commit. See the
[retry and evidence reference](../../.pi/skills/bonsai-ci/references/runtime-and-issue.md#automatic-commit-reviews-and-telemetry).
