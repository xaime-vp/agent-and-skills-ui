# Pi developer adapter for Constant Integration UI

Target `xaime-vp/constant-integration-ui` in `constant-integration-ui/`.
Read that checkout's AGENTS.md, architecture and development guidance before
editing. Skills live under `.pi/skills/`; discover real Pi/MCP capabilities.

Use the [shared developer workflow](docs/agent-setup/developer-workflow.md).
The developer owns implementation, tightly coupled regression tests and small
documentation updates. Delegate substantial independent work, specialist expertise
or explicit assignments. Never overlap an active writer's scope.

Inspect existing work, create a task branch, implement and commit a meaningful
initial change, then open a draft PR before any specialist dispatch targeting it.
Do not manufacture planning-only files or commits. Reuse existing PR branches.
Review-only requests are read-only, including issues, metadata and review posts.

Honor the target repository's applicable instructions and native checks. Root
target AGENTS.md is optional. Runtime roles, capacity and admission come from
the selected source and installed release, not this client adapter. The Bonsai
supervisor retains worker scope, credentials, protected checks, review, sealed
resources and publication authority. Merge/deployment/worker operation requires
its own task authorization. Preserve concurrent commits and private data.

Shared copies are recorded in [harness-source.json](harness-source.json). Run
`python tools/check_harness_export.py` and `python tools/harness_check.py`.
For changes to shared content, update the canonical source and regenerate using
[shared exports](docs/agent-setup/shared-exports.md); keep local policy here.

## UI and completion policy

Use validated sanitized exports and fixtures for browser verification. The UI
may write its own history but cannot query worker private state, expose the Docker
socket or implement worker control endpoints. Keep volumes separate and preserve
the application's authentication boundary. Use the shared UI verification skills.

Follow selected specialist contributions through delivery and validate the combined
head when completion is requested. Reuse active assignments and bounded waits;
do not start competing executors. Report concrete blockers and unavailable evidence.
