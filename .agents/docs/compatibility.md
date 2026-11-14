# Update the workspace and verify compatibility

Start by identifying which repository the request names. This UI developer
harness is the `main` branch of `xaime-vp/agent-and-skills-ui`;
its application target is `xaime-vp/constant-integration-ui` in
`constant-integration-ui/`, and the platform runtime source is
`xaime-vp/constant-integration` in `constant-integration/`. Confirm each
checkout's remote before pulling or creating a PR. Changes belong in the
repository that owns the affected instructions or code; an ambiguous reference
to "the harness" needs context.

## Refresh source without disturbing ongoing work

From the developer workspace, inspect the workspace and target repositories:

```powershell
git remote get-url origin
git status --short --branch
git -C constant-integration-ui remote get-url origin
git -C constant-integration-ui status --short --branch
git -C constant-integration remote get-url origin
git -C constant-integration status --short --branch
```

When this workspace is clean and already on `main`, update
with `git pull --ff-only origin main`. Otherwise fetch and
use an isolated task checkout; preserve local edits and ongoing PR branches.
Inspect the new base before deciding what to change: compatibility guidance may
already have merged. Follow the [root branch/PR workflow](../../AGENTS.md) for
any new implementation.

Fetching the platform does not change its worktree. To inspect latest platform
source while its normal checkout contains staged edits or an ongoing task:

```powershell
git -C constant-integration fetch origin main
git -C constant-integration rev-parse origin/main
git -C constant-integration worktree add --detach ../../constant-integration-compat origin/main
```

This example creates a sibling of the developer workspace. Choose an unused path
and record its exact commit; detached worktrees are for inspection/validation,
while implementation uses the task's working branch. Keep target worktrees out
of workspace commits.

## Compare source and installed behavior separately

| Evidence | What to verify |
| --- | --- |
| Updated workspace | Workspace SHA and applicable skills/assignment guides |
| Platform source | Exact SHA, [role contract](https://github.com/xaime-vp/constant-integration/blob/main/docs/AGENT_ROLES.md), task parser and protected-check documentation |
| Selected installation | Bound repository (`xaime-vp/constant-integration-ui`), image revision, sealed release, enabled profiles, admission mode, protected check argv and limits |
| Delivered contribution | Parent PR/branch, actual commit/diff, worker observations and exact-head target CI |

Read [runtime discovery](../skills/bonsai-ci/references/runtime-and-issue.md)
and use the [container skill](../skills/bonsai-containers/SKILL.md) for
read-only installation inspection. Select the container bound to
`xaime-vp/constant-integration-ui`; do not assume the default container serves
every repository. Image revision alone does not establish the volume's sealed
release.

Current source uses `agent:test-specialist` and `agent:documentation`, with
`admission_mode: ready` (removing `blocked`, adding `ready`, and keeping the
single matching `agent:*` label). A historical installation can still require
`agent:generalist`, explicit token fields, `/approve-agent <full-digest>` or
standalone `/approve-agent`, or a legacy envelope without free-form preparation
support. Verify those facts against its sealed parser/configuration before
authoring executable work. Do not silently rewrite approvals or enable a new
route. Unknown support stays unready; selecting a supported older route does
not authorize an upgrade.

For legacy schema validation, explicitly select the source revision under review:

```powershell
py -3 .agents/tools/validate_task.py --platform-root ../../constant-integration-compat --repository xaime-vp/constant-integration-ui --body-file path/to/issue.md
```

The isolated latest source checkout proves only latest-source parsing. For an
older installation, separately validate against its matching reviewed source or
sealed parser and match its configured checks/limits. A successful parse does not
verify approval, admission, installed readiness or delivery. Prose preparation
uses its separate [preparation workflow](free-form-issues.md), not this legacy
validator.

Report the workspace/platform/installed revisions separately, commands and actual
results, failed or unrun checks, and any required owner action. Offline parsing,
unit tests and synthetic evaluations do not establish live issue-to-PR delivery.
Pulling source does not stop, start, upgrade or reconfigure an installed worker.
