# Delegated contribution examples

Use the target PR template and adapt these examples to observed evidence.
Names, paths and outcomes below are illustrative, not records of actual work.

## Mixed implementation and integration

| Function or work unit | Contribution | Executor / identity | Evidence |
| --- | --- | --- | --- |
| `src/parser.py::parse_empty_input` | Application implementation | Root developer; observed model identity or unknown | Implementation commit link |
| `tests/test_parser.py::test_empty_input` and fixtures | Regression coverage | Bonsai test-specialist; configured model `<observed model ID>`, hosted identity unknown | Task/approval and worker commit links |
| `src/parser.py::validate_options` | Integration repair after reviewing the delegated diff | Codex; model identity unknown | Integrator commit link |
| Parser diff | Advisory review; no source edits or checks executed | Read-only worker reviewer; configured model `<observed model ID>` | Sanitized finding summary or published review |

Validation separately records, for example:

- Worker protected checks: command, observed exit/status and candidate revision;
  executed in the selected implementation workspace, not independent verification.
- Integrator checks: command, actual exit/status, tested revision and skips.
- Target GitHub CI: exact PR head SHA, run link and observed conclusion.
- Unrun checks or unresolved review findings and their practical impact.

If the exact model is unavailable, say so. If only a delegate's statement exists,
label it self-reported until corroborated by a diff, commit or trusted execution
record. Do not invent an evidence link or claim a fresh rerun.

## Documentation or other delegated work

Use a locator such as `docs/setup.md — Linux setup section` or
`.github/workflows/check.yml — test job` instead of inventing a code symbol.
An executor running a formatter, reviewer inspecting the result, and integrator
publishing the PR are distinct contributions when those distinctions matter.

## Revision updates

Keep the table aligned with the current diff. Remove attribution rows for work
that was dropped; retain credit for contributions still present after integration.
Describe material rewrites without assigning the whole change to the publisher.
Refresh validation/CI revisions when the PR head changes. Attribution documents
provenance; it does not certify security, correctness or owner acceptance.
