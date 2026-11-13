# Prompting a coding agent for a Bonsai task

This developer-side guide is maintained in `xaime-vp/agent-and-skills`.
Follow the [root developer contract](../../AGENTS.md) for the active workflow:
the root agent implements application code and uses scoped issues for test and
documentation contributions to its existing parent PR. Set the executable
envelope's numeric `pull_request` to that PR number. The general preparation
prompts below apply when explicitly preparing a task or ordered plan; they do
not replace that branch/PR workflow.

Use this guide to turn a request into a clear issue for the
[supervised worker](../../constant-integration/docs/SUBMITTING_TASKS.md). It is written for compatible coding
agents, but skill-discovery and invocation syntax differs by product; follow the
instructions for the agent you actually use. The repository's
[reusable skills](../../README.md) can provide more specific
guidance where supported.

A prompt prepares a request; it does not approve or dispatch work. A skill,
issue label, generated task envelope, successful local test, or passing platform
CI cannot substitute for the configured owner's approval or target-repository
CI at the exact final PR head.

## Prompt for one bounded task

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
- the human-readable issue sections and one schema-2 agent-task envelope,
  only if exact paths, checks, and budgets are verified.

If installed schema/capability, target binding, file scope, or protected checks
cannot be verified, leave the proposal blocked and unready. Do not invent
checks, permissions, approvals, resource limits, or runtime capabilities. Do not
include credentials, private logs, or real .env contents.
```

## Prompt for one ordered plan

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
file scope and leave the protected checks passing; combine implementation and
its regression tests. Use the same protected command set at each step and for
the final candidate. Do not claim local/documented commands are protected until
matched to the installed configuration.

Return the human-readable issue sections and one schema-3 agent-task envelope
only if schema-3 support, exact paths, checks, budgets and dependencies are
verified. Otherwise return a blocked/unready proposal listing the missing facts.
Do not approve, dispatch, add retries, update an existing PR, or split the plan
into separate issues unless explicitly requested.
```

## Final checks before submitting

- Paste the verified human-readable sections and `agent-task` JSON fence into
  the target repository's Agent task or Bonsai plan issue template, following
  its submission guide. Do not copy an example envelope unchanged.
- Verify the target binding, installed sealed release, exact editable paths,
  protected check argv, limits, and any prerequisite PR merge before setting a
  task ready. A PR link in issue prose does not enforce dependency order.
- Keep unknown or dependent proposals `blocked` and without `ready`. The
  configured owner must approve the finalized issue using the documented
  approval procedure; the agent must not post approval on the owner's behalf.
- After a draft PR exists, distinguish worker checks/review from exact-head
  target CI. Do not report a pass when a check is missing, pending, failed, or
  observed on an older head.

See [single-task submission](../../constant-integration/docs/SUBMITTING_TASKS.md),
[plan guidance](../../constant-integration/docs/submitting-tasks/plans.md),
[the task envelope](../../constant-integration/docs/submitting-tasks/envelope.md), and the
[role and evidence contract](../../constant-integration/docs/AGENT_ROLES.md).
