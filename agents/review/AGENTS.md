# Combined change review

Supporting guidance for the [root developer](../../AGENTS.md). Use it to review the actual final branch diff and issue contributions. This file does not spawn an agent, grant publication authority or change the sealed Pi review contract.

- Compare the combined branch with the intended base and the requested acceptance criteria. Distinguish **substantive blockers** (concrete failure mechanism, unsatisfied critical requirement, security/regression risk, supporting evidence, and actionable correction within scope or explicit scope limitation) from **optional suggestions** (naming, formatting, minor maintainability/refactoring preferences, which must not trigger mandatory repairs).
- Prohibit reviewer-driven scope expansion: reviewers are read-only, and findings never authorize edits outside the approved task scope.
- Confirm issue-worker changes reached the parent PR branch. Preserve author provenance; a worker completion message or closed issue is not delivery evidence.
- For prepared prose issues, confirm the sealed proposal targets the parent PR and is properly admitted (`admission_mode: ready` on current source, or digest-bound approval on older releases). For legacy envelopes, confirm numeric `pull_request` and valid readiness/approval. Review the resolved scope/checks and actual delivery; prose headings or a PR mention alone do not select execution.
- Inspect actual assertions, documentation examples and links. Confirm that tests exercise the requested behavior and that documentation matches it.
- Bind verification to the final head. Distinguish checks you ran, protected worker observations, model findings and GitHub CI. Record pending, failed, skipped and unavailable results honestly.
- Coder and test-specialist contributions have embedded read-only review; documentation does not. A trusted-opt-in automatic PR Reviewer may separately publish commit-bound `COMMENT` reviews, with no checks, repairs or merge authority. Report its advisory findings against the reviewed commit, and do not treat an export heartbeat or missing usage as liveness or zero cost.
- Report concrete actionable findings with a file/location, failure mechanism and proposed verification. A model's approval is advisory and cannot authorize merge or establish owner acceptance.
- Keep the PR in draft while required work remains. In a developer-led PR the root developer owns code repairs and scoped test/documentation handoffs; a supervised `agent:coder` task follows its own approved supervisor policy. Review findings never authorize scope expansion.
