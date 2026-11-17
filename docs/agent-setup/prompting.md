# Prompting a coding agent for a Bonsai task

This developer-side guide is maintained in `xaime-vp/agent-and-skills`.
Follow the [root developer contract](../../AGENTS.md) for the active workflow:
in the developer-led path the root agent implements application code and uses
scoped test/documentation issues for its existing parent PR. Separately delegated
`agent:coder` implementation follows the supervisor-owned [coder guide](../../agents/coding/AGENTS.md). Free-form preparation
selects it with operator `--target-pr NUMBER`; legacy envelopes use numeric
`pull_request`. A PR mention alone does not select the destination. The general
preparation prompts below apply when explicitly preparing a task or ordered
plan; they do not replace that branch/PR workflow.

Current source supports `agent:coder` for deliberately delegated code tasks and
explicitly authorized related tests/docs, `agent:test-specialist` for test work,
and `agent:documentation` for documentation. Select one matching label and
verify sealed installed support. In the **developer-led** workflow, keep code
with the root developer and tests/docs with their scoped specialists; do not
run a competing coder writer. Generalist/tests are retired source routes.
See the [capability map](platform-capabilities.md). The separate automatic PR Reviewer is trusted-opt-in and
read-only, not an implementation request.

Use this guide to turn a request into a clear issue for the
[supervised worker](https://github.com/xaime-vp/constant-integration/blob/main/docs/SUBMITTING_TASKS.md). It is written for compatible coding
agents, but skill-discovery and invocation syntax differs by product; follow the
instructions for the agent you actually use. The repository's
[reusable skills](https://github.com/xaime-vp/agent-and-skills/blob/a701dcf2de332cce285b49c0b7c609f2d75d4328/README.md) can provide more specific
guidance where supported.

A prompt prepares a request; it does not approve or dispatch work. A skill,
issue label, generated task envelope, successful local test, or passing platform
CI cannot substitute for the configured owner's route-specific approval or
target-repository CI at the exact final PR head.

## Prompt for a free-form issue

Use this when an issue should start with the desired outcome and leave exact
scope/check selection to bounded preparation. The author need not supply an
envelope or token budgets. Follow [free-form issue guidance](free-form-issues.md)
for the operator workflow; preparation is explicit, not automatic on issue creation.

```text
Prepare a prose Bonsai issue for [owner/repository], contributing [tests or
documentation] to existing parent PR [URL], branch [exact branch], at
implementation commit [SHA].

Desired outcome and evidence:
[observable behavior, examples/reproduction and relevant source/PR links]

Acceptance criteria and boundaries:
[what must be verified/documented, non-goals and known dependencies]

Return a clear issue body and any questions. Do not invent exact writable files,
protected checks or resource limits; identify what bounded preparation must
resolve. Do not require agent-task JSON. Do not submit or approve the issue as
part of this preparation-only request.

Identify the operator's required parent destination (--target-pr NUMBER),
matching role label (agent:coder for explicitly delegated code work,
agent:test-specialist or agent:documentation), and
candidate committed research files, distinguishing suggestions from verified
evidence. Keep the issue blocked without ready. The configured owner must
request research with /prepare-agent, then inspect the sealed proposal
(inspect-preparation). On current source (admission_mode: ready), admit by
removing blocked and adding ready with the single matching agent:* label
(older installed releases require /approve-agent <full-digest>).
Assessment-only research cannot authorize implementation. Do not post owner
request/approval commands or assume a merged capability is installed.
```

## Prompt for one legacy bounded task

Adapt this template, replacing every bracketed item. Ask the agent to inspect
the target repository's own instructions and CI configuration; do not assume
this platform's checks apply to another repository.

```text
Help me prepare one reviewable Bonsai task for [owner/repository].

Requested outcome:
[observable behavior and who benefits]

Current behavior / evidence:
[reproduction, links, or "unknown"]

Please inspect the target repository's applicable AGENTS.md, README, nearby
code/tests, and protected-check guidance. Do not modify files or submit/approve
an issue as part of preparation.

Return:
- a concise goal and acceptance criteria;
- exact candidate editable paths, only if verified from the repository;
- existing protected check commands and their source; mark suggested commands
  as unverified rather than presenting them as protected checks;
- dependencies, non-goals, risks, and evidence still needed;
- whether the request is one task or needs an ordered plan;
- the human-readable issue sections and one complete schema-2 agent-task envelope,
  only if exact paths, checks and installed limits/support are verified. Set
  numeric pull_request for an existing parent PR. On a compatible release, omit
  input_tokens/output_tokens; retain all other required fields.

If installed schema/capability, target binding, file scope, or protected checks
cannot be verified, leave the proposal blocked and unready. Do not invent
checks, permissions, approvals, resource limits, or runtime capabilities. Do not
include credentials, private logs, or real .env contents.
```

## Prompt for one legacy ordered plan

Use a plan only when several dependent implementation steps should form **one
coherent change and one PR**. Aim for the smallest number of steps that each
leave tests green (typically 2–6 steps; reserve larger counts for multi-module
migrations). The installed worker must support the selected
schema and any retry behavior. Steps are not a way to bypass task limits or
create an implicit dependency scheduler.

```text
Help me prepare one Bonsai multi-step plan for [owner/repository].

Final outcome:
[observable behavior that belongs in one PR]

Dependencies / evidence:
[what is known, what must merge first, and how that will be verified]

Inspect the target instructions, current implementation and protected checks.
Propose one or more ordered, time-bounded steps within the brief-size limit. Each step must include its exact verified
file scope within the selected test or documentation profile and leave the
protected checks passing. Application fixes stay with the root developer in
  the developer-led workflow; an independently authorized coder plan may edit
  code only within its approved scope.
Use the same protected command set at each step and for
the final candidate. Do not claim local/documented commands are protected until
matched to the installed configuration.

Return the human-readable issue sections and one schema-3 agent-task envelope
only if schema-3 support, exact paths, checks, limits and dependencies are
verified. On a compatible release, token fields may be omitted in the parent and
steps; other required fields remain required. Otherwise return a blocked/unready
proposal listing the missing facts.
Do not approve, dispatch, add retries, update an existing PR, or split the plan
into separate issues unless explicitly requested.
```

## Final checks before submitting

- Choose the route explicitly. Free-form issues use clear prose, selected
  research and a sealed proposal; legacy requests use verified human-readable
  sections plus one complete `agent-task` fence. Follow the target's submission
  guide and adapt examples to the actual task.
- Verify the target binding, installed sealed release, exact editable paths,
  protected check argv, limits, and any prerequisite PR merge before setting a
  task ready. A PR link in issue prose does not enforce dependency order.
- Keep unknown or dependent proposals `blocked` and without `ready`. Free-form
  research may resolve unknown details; gaps/questions block an executable
  proposal. On current source (`admission_mode: ready`), admit a verified
  sealed proposal or finalized legacy envelope by removing `blocked`, adding
  `ready`, and retaining the single matching `agent:*` label (no
  `/approve-agent` comment is required; older installed releases still require
  `/approve-agent <full-digest>` or standalone `/approve-agent`). Never post
  owner commands for them.
- After a draft PR exists, distinguish worker checks/review from exact-head
  target CI. Do not report a pass when a check is missing, pending, failed, or
  observed on an older head.

See [single-task submission](https://github.com/xaime-vp/constant-integration/blob/main/docs/SUBMITTING_TASKS.md),
[plan guidance](https://github.com/xaime-vp/constant-integration/blob/main/docs/submitting-tasks/plans.md),
[the task envelope](https://github.com/xaime-vp/constant-integration/blob/main/docs/submitting-tasks/envelope.md), and the
[role and evidence contract](https://github.com/xaime-vp/constant-integration/blob/main/docs/AGENT_ROLES.md).
