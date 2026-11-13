# Test contribution assignment

This supports the [root developer](../../AGENTS.md) when preparing a repository issue and reviewing its worker contribution. It is not a new Bonsai runtime role; tests use the existing `agent:generalist` route.

- Identify the changed behavior, regression case, adjacent tests and exact editable test/fixture paths. Give observable assertions and relevant edge cases, rather than tests that merely mirror implementation details.
- Include the parent PR number, current implementation commit and delivery branch. Free-form issues may leave exact editable test paths/checks for preparation: the operator must select `--target-pr NUMBER`, then the owner approves the sealed proposal digest. Legacy envelopes instead set numeric `pull_request`, supply verified protected checks and use offline validation. Follow the [route-specific guidance](../../docs/agent-setup/free-form-issues.md); a PR link alone does not select delivery.
- Stay within the assigned test paths. Report application bugs to the root developer, who owns application fixes. Do not weaken checks to make a failing implementation pass.
- Start from the latest parent PR head and preserve other contributions. Delivery is complete only when the test changes appear on that branch with actual command outcomes and a commit SHA.
- The root developer reviews assertions and runs or inspects the combined checks. Keep failures, skips and environmental limits visible. Serialize this handoff with documentation work targeting the same PR.
