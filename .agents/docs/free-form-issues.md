# Free-form issues and legacy envelopes

Issues can start as ordinary prose. The merged [free-form preparation contract](https://github.com/xaime-vp/constant-integration/blob/main/docs/submitting-tasks/free-form.md) supports bounded read-only research, a privately sealed executable proposal and owner approval of that proposal's digest. Legacy `agent-task` envelopes remain supported. Verify the reviewed image and sealed installation support the selected route; a source checkout or merged PR does not prove activation.

For the [root developer workflow](../../AGENTS.md), both routes contribute tests or documentation to the existing parent PR. Create/reuse a scoped issue with the repository, parent PR, exact delivery branch, implementation SHA, desired outcome, examples, acceptance criteria and boundaries. Human-readable headings are a useful template, not parser syntax. Free-form issues need no envelope, exact writable paths or token calculations at creation; identify questions rather than inventing those details.

| Decision | Free-form preparation | Legacy executable envelope |
| --- | --- | --- |
| Issue body | Clear prose and assignment context | Context plus exactly one complete fenced `agent-task` JSON block |
| Parent PR destination | Operator selects `--target-pr NUMBER` during preparation | Numeric `pull_request` in schema 2/3 JSON |
| Executable scope/checks | Supervisor validates and seals the proposal using selected evidence and installed protected checks | Author supplies exact paths and protected acceptance-command argv arrays |
| Owner action to request research | `/prepare-agent`; assessment-only uses `/prepare-agent review` | None |
| Owner approval for implementation | Exact returned `/approve-agent <full-digest>` after sealing and final issue edit | Standalone `/approve-agent` after final issue edit |
| Validation | Preparation validates/seals the internal envelope and entire context | Workspace `.agents/tools/validate_task.py` parses the body against selected source |

A PR mention supplies context only. Omitting `--target-pr` or legacy `pull_request` selects a new draft instead of the required parent PR. Schema 4 cannot target an existing PR. Standalone legacy approval cannot approve a saved proposal. Do not post owner request/approval commands on their behalf.

## Prepare and review a prose issue

1. Finalize the issue and keep it blocked/unready. The configured owner posts standalone `/prepare-agent` after the final title/body edit; record the numeric comment ID. Assessment-only work instead requires `/prepare-agent review` and `--assessment-only`; it produces no executable proposal.
2. An operator selects committed research files, the parent PR and explicit low/medium execution risk. Use the installed entrypoint with its normal target/environment arguments.

   On a Docker Compose host, from the platform checkout:

   ```sh
   docker compose -f workers/bonsai/compose.yaml run --rm worker prepare-issue 17 \
     --request-comment 70 --target-pr 42 \
     --research-file app/src/parser.py --research-file app/tests/test_parser.py \
     --execution-risk medium
   ```

   On Windows with Podman in WSL (`podman-machine-default`, where `podman` is not on the Windows `PATH`), first inspect the installed image (`wsl -d podman-machine-default -e podman inspect bonsai-worker --format '{{.ImageName}}'`), safely stop the worker in place using `bonsai_stop_worker(container="bonsai-worker")` (without `backupSuffix`) or `.pi/skills/bonsai-podman-ops/scripts/stop_worker.sh bonsai-worker`, and then run against the existing container's state volume:

   ```sh
   wsl -d podman-machine-default -e podman run --rm --volumes-from bonsai-worker \
     -e PODMAN_IGNORE_CGROUPSV1_WARNING=1 \
     -e BONSAI_TARGET_REPOSITORY=xaime-vp/constant-integration \
     localhost/bonsai-worker:<tag> prepare-issue 17 \
     --request-comment 70 --target-pr 42 \
     --research-file app/src/parser.py --research-file app/tests/test_parser.py \
     --execution-risk medium
   ```

   Only run preparation after the listener is stopped and all role processes are confirmed stopped. Preparation takes the listener lock, refuses active/unknown tasks or publication reservations and does not stop the service itself. It is exclusive even on a two-slot installation. Lifecycle changes follow the separately authorized container workflow.
3. Inspect the returned preparation record using `inspect-preparation KEY`:

   ```sh
   # Docker Compose
   docker compose -f workers/bonsai/compose.yaml run --rm worker inspect-preparation KEY

   # Podman in WSL (podman-machine-default)
   wsl -d podman-machine-default -e podman run --rm --volumes-from bonsai-worker \
     -e PODMAN_IGNORE_CGROUPSV1_WARNING=1 \
     -e BONSAI_TARGET_REPOSITORY=xaime-vp/constant-integration \
     localhost/bonsai-worker:<tag> inspect-preparation KEY
   ```

   Review original requirements, assessment, questions/gaps, exact files, protected checks, limits and pinned source/PR destination. Research reads an operator-selected committed corpus and saved same-repository PR evidence; it does not run repository commands or browse arbitrary URLs. Missing evidence must become a gap/question. Any gap/question prevents an executable proposal; request another pass with appropriate evidence.
4. Only a validated non-null proposal has an approval command. Present the exact returned full lowercase SHA-256 command to the owner. Approval must be strictly later than sealing and the final issue edit; equal timestamps require reposting. Set `ready` and exactly `agent:generalist` among role labels, remove `blocked` and use the normal listener for execution once prerequisites are satisfied (for Podman in WSL when authorized to resume: `wsl -d podman-machine-default -e podman start bonsai-worker`). Research requests, assessments and chat authorization do not authorize implementation.
5. Track the delivered commit and actual parent-branch diff, then inspect exact-head target CI. Serialize tests and documentation for one PR. Prepare the second contribution after the first releases reservations; a head change requires fresh preparation of any stale proposal.

Preparation does not publish or implement. Requests are single-use even after failure; another bounded pass needs a new owner request. The supervisor saves immutable context/proposal evidence. Issue edits, changed source, captured PR head/base or bound check/resource policy require fresh preparation and digest approval. Ordinary status comments do not rewrite the assignment; changing requirements requires an issue edit and replacement preparation/approval, with revocation to stop active work. Preserve unknown-stop evidence and use supported reconciliation rather than retrying or deleting state.

## Keep legacy support precise

Free-form intake does not relax the legacy JSON parser. Use the [schema reference](../skills/bonsai-ci/references/task-preparation.md) and installed release's rules. Identity/extra fields and duplicate keys remain invalid; repository/issue identity comes from trusted policy and GitHub.

On releases with optional token budgets, omit `input_tokens` and `output_tokens` for automatic model context and no per-task response cap; provider/model limits still apply. Explicit positive limits remain supported. Omitted or null plan-step values inherit parent token values and cannot erase an explicit parent cap. Other required legacy fields remain required. Older releases may require explicit token fields: select a compatible source with `--platform-root` for offline validation, and verify installed compatibility separately. The workspace validator cannot validate prose or inspect saved proposals.

See the product [submission guide](https://github.com/xaime-vp/constant-integration/blob/main/docs/SUBMITTING_TASKS.md), [legacy envelope contract](https://github.com/xaime-vp/constant-integration/blob/main/docs/submitting-tasks/envelope.md) and [free-form operator contract](https://github.com/xaime-vp/constant-integration/blob/main/docs/submitting-tasks/free-form.md) for operational limits and recovery. This guide authorizes no upgrade, owner impersonation, merge or deployment.
