# Developer and worker handoff template

Maintained in `xaime-vp/agent-and-skills-ui`. Use this with the
[root developer contract](../../AGENTS.md) to summarize issue-driven test or
documentation contributions and manual recovery handoffs. It describes evidence
to gather; it does not grant the developer access to protected supervisor state
or make a local model into a runtime supervisor.

For UI contributions, include repository `xaime-vp/constant-integration-ui`,
parent PR URL/number, exact base and delivery branch, and implementation SHA.
Require changes back to that parent branch through the supervisor, preserving
concurrent commits. Search existing issues first and serialize contributions that
reserve the same PR. A prose PR mention alone does not select delivery.

| Assignment | Current source route | Editable contribution | Model review |
| --- | --- | --- | --- |
| Backend/frontend regressions | `agent:test-specialist` | Exact approved tests, fixtures or test configuration | Embedded read-only review |
| User/developer guidance | `agent:documentation` | Exact approved documentation | No embedded model review |

Choose the matching label before preparation and verify the sealed UI-bound
installation enables the profile. Report application defects to the developer;
neither contribution may widen into app code. Fixture assertions remain
independently authored; do not regenerate expectations from implementation merely
to pass. Frontend checks use the UI's existing npm scripts. Documented commands
are candidate checks until matched to installed protected configuration.

Describe observable acceptance criteria, edge cases and known dependencies.
Resolve missing scope/checks through bounded preparation; leave unresolved gaps
blocked and unready. Documentation acceptance includes verifying paths, links,
commands and capability claims even when no model review runs. For both routes,
preserve the UI's read-only export boundary and distinguish unknown data from zero,
saved heartbeats from liveness and draft publication from owner acceptance.

Use a brief supervisor-authored summary for manual owner/specialist handoffs.
Runtime role assignments and reports are persisted privately by the supervisor;
roles do not send messages or files directly to peers. Link evidence rather than
pasting transcripts or unexplained logs.

- **Task / component:** issue, project directory or workspace, desired outcome.
- **Supervisor / assigned role:** task key, current phase and next assignment.
- **Scope / privileges:** readable context, exact writable files and prohibited actions.
- **Instructions / checks:** applicable AGENTS.md paths and existing acceptance commands.
- **Candidate identity:** platform revision, target branch/commit, source hash and PR.
- **Issue route / authorization:** free-form preparation key, selected `--target-pr`, sealed proposal digest, and installed admission/approval evidence (`admission_mode: ready` on current source, or digest/standalone `/approve-agent` on older sealed releases), or legacy envelope `pull_request` and readiness/approval evidence. Record unresolved preparation gaps/questions. A prose issue needs no hand-written envelope; both routes need validated exact scope/checks before execution. See [route guidance](free-form-issues.md).
- **Implementation:** concrete changes and remaining work.
- **Implementation check evidence:** selected profile, exact commands, exit/status and protected
  report/log paths. These ran once in that implementation workspace, not independently.
  Record failed or unrun checks and exact-head target CI separately.
- **Reviewer findings:** applicable embedded or commit-bound advisory findings; report documentation's absent embedded model review explicitly rather than inventing a verdict.
- **Optional telemetry:** captured usage/cost and attempt/span links, with unavailable fields unknown. A history-export heartbeat is not process liveness; verbose bundles remain private evidence to inspect before sharing.
- **Recovery:** whether all role processes stopped, current task state and any unknown outcome.
- **Owner decision / next step:** one scoped action, no overlapping ownership,
  no automatic merge, deployment or unapproved retry.
