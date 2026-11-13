# Test contribution assignment

This supports the [root developer](../../AGENTS.md) when preparing a repository issue and reviewing its worker contribution. It is not a new Bonsai runtime role; tests use the existing `agent:generalist` route.

- Identify the changed behavior, regression case, adjacent tests and exact editable test/fixture paths. Give observable assertions and relevant edge cases, rather than tests that merely mirror implementation details.
- Include the parent PR number, current implementation commit and delivery branch. For Bonsai, set the executable envelope's `pull_request` to that number. Copy protected checks from the verified target installation and validate the issue with the workspace tool.
- Stay within the assigned test paths. Report application bugs to the root developer, who owns application fixes. Do not weaken checks to make a failing implementation pass.
- Start from the latest parent PR head and preserve other contributions. Delivery is complete only when the test changes appear on that branch with actual command outcomes and a commit SHA.
- The root developer reviews assertions and runs or inspects the combined checks. Keep failures, skips and environmental limits visible. Serialize this handoff with documentation work targeting the same PR.
