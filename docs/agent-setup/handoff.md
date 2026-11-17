# Developer and worker handoff template

Maintained in `xaime-vp/agent-and-skills`. Use this with the
[root developer contract](../../AGENTS.md) to summarize independently delegated coder, test or
documentation contributions and manual recovery handoffs. It describes evidence
to gather; it does not grant the developer access to protected supervisor state
or make a local model into a runtime supervisor.

Use a brief supervisor-authored summary for manual owner/specialist handoffs.
Runtime role assignments and reports are persisted privately by the supervisor;
roles do not send messages or files directly to peers. Link evidence rather than
pasting transcripts or unexplained logs.

- **Task / component:** issue, project directory or workspace, desired outcome.
- **Supervisor / assigned role:** task key, current phase and next assignment; coder is an alternative implementation owner, not a second writer alongside the root developer.
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
