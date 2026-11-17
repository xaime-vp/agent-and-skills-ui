# Test contribution assignment

This guide applies to an actual specialist assignment. The root developer may write tightly coupled tests and small documentation updates directly; no handoff is required solely by file type.

This supports the [root developer](../../AGENTS.md) when preparing a repository issue and reviewing its worker contribution. Current source uses `agent:test-specialist` for tests, fixtures and test configuration, followed by protected checks and embedded read-only review. Verify the sealed installation supports that route; retired `agent:generalist` and `agent:tests` labels are rejected, never aliased.

Read the target repository's test layout and shared fixtures before extending coverage. Reuse its existing setup and make each regression identify one behavior.

- Identify the changed behavior, regression case, adjacent tests and exact editable test/fixture paths. Give observable assertions and relevant edge cases, rather than tests that merely mirror implementation details.
- Include the parent PR number, current implementation commit and delivery branch. Free-form issues may leave exact editable test paths/checks for preparation: the operator must select `--target-pr NUMBER`, then current-source admission uses verified `ready` and one matching role label without `blocked` (older sealed installations may require digest approval). Legacy envelopes instead set numeric `pull_request`, supply verified protected checks and use offline validation. Follow the [route-specific guidance](../../docs/agent-setup/free-form-issues.md); a PR link alone does not select delivery.
- Stay within the assigned test paths. Report application bugs to the root developer, who owns application fixes. Do not weaken checks to make a failing implementation pass.
- Attribution and accounting changes are covered by `test_token_accounting.py` and `test_intermediate_calls.py`; proxy/export changes also touch `test_export.py`, `test_incremental_export.py` and `test_listener.py`. Check the current source before asserting which suites exist.
- Start from the latest parent PR head and preserve other contributions. Delivery is complete only when the test changes appear on that branch with actual command outcomes and a commit SHA.
- The root developer reviews assertions and runs or inspects the combined checks. Keep failures, skips and environmental limits visible. Serialize this handoff with documentation work targeting the same PR.
