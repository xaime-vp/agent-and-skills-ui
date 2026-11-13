# Documentation contribution assignment

This supports the [root developer](../../AGENTS.md) when preparing a documentation issue and reviewing its worker contribution. Documentation uses Bonsai's existing `agent:generalist` route; it does not require a separate runtime profile.

- Describe the implemented behavior, intended readers, exact documentation files, affected examples and acceptance criteria. Link the relevant code and current implementation commit.
- Include the parent PR number and delivery branch. For Bonsai, set the executable envelope's `pull_request` to that number and verify installed checks and scope before dispatch.
- Document observed supported behavior. Distinguish planned capabilities, local source, installed releases, passing checks and live delivery. Update examples and relative links after moves or removals.
- Keep application code and runtime policies outside the documentation assignment. Report inconsistencies to the root developer.
- Deliver onto the latest parent PR branch, preserve other contributions, and report the commit SHA, changed sections and actual verification. The root developer checks the final prose against the implementation. Run this handoff after conflicting test work has released the PR reservation.
