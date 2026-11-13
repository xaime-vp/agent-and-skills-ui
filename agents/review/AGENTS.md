# Combined change review

Supporting guidance for the [root developer](../../AGENTS.md). Use it to review the actual final branch diff and issue contributions. This file does not spawn an agent, grant publication authority or change the sealed Pi review contract.

- Compare the combined branch with the intended base and the requested acceptance criteria. Review surrounding source as needed for correctness, scope, security and maintainability.
- Confirm issue-worker changes reached the parent PR branch. Preserve author provenance; a worker completion message or closed issue is not delivery evidence.
- For prepared prose issues, confirm the sealed proposal targets the parent PR and has the required digest-bound owner approval. For legacy envelopes, confirm numeric `pull_request` and standalone approval. Review the resolved scope/checks and actual delivery; prose headings or a PR mention alone do not select execution.
- Inspect actual assertions, documentation examples and links. Confirm that tests exercise the requested behavior and that documentation matches it.
- Bind verification to the final head. Distinguish checks you ran, protected worker observations, model findings and GitHub CI. Record pending, failed, skipped and unavailable results honestly.
- Report concrete actionable findings with a file/location, failure mechanism and proposed verification. A model's approval is advisory and cannot authorize merge or establish owner acceptance.
- Keep the PR in draft while required work remains. The root developer owns repairs to application code and further test/documentation handoffs through issues.
