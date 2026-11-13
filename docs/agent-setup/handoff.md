# Developer and worker handoff template

Maintained in `xaime-vp/agent-and-skills`. Use this with the
[root developer contract](../../AGENTS.md) to summarize issue-driven test or
documentation contributions and manual recovery handoffs. It describes evidence
to gather; it does not grant the developer access to protected supervisor state
or make a local model into a runtime supervisor.

Use a brief supervisor-authored summary for manual owner/specialist handoffs.
Runtime role assignments and reports are persisted privately by the supervisor;
roles do not send messages or files directly to peers. Link evidence rather than
pasting transcripts or unexplained logs.

- **Task / component:** issue, project directory or workspace, desired outcome.
- **Supervisor / assigned role:** task key, current phase and next assignment.
- **Scope / privileges:** readable context, exact writable files and prohibited actions.
- **Instructions / checks:** applicable AGENTS.md paths and existing acceptance commands.
- **Candidate identity:** platform revision, target branch/commit, source hash and PR.
- **Implementation:** concrete changes and remaining work.
- **Generalist check evidence:** exact commands, exit/status and protected
  report/log paths. These ran once in the generalist workspace, not independently.
  Record failed or unrun checks and exact-head target CI separately.
- **Reviewer findings:** design/security/maintainability concerns or an inconclusive report.
- **Recovery:** whether all role processes stopped, current task state and any unknown outcome.
- **Owner decision / next step:** one scoped action, no overlapping ownership,
  no automatic merge, deployment or unapproved retry.
