# Per-target container deployment

Routine operations use [the lifecycle CLI](../../../../constant-integration/docs/CONTAINER_LIFECYCLE.md).
This reference is for initial setup and exceptional recovery. The first adapter
requires native Docker Engine through a local Unix socket. It explicitly rejects
Podman wrappers, Compose-owned containers and remote engines. Do not bypass a
rejection or register a misleading engine identity. Retain this manual procedure
for unsupported installations until their adapter has isolated integration tests.

Use the current `xaime-vp/constant-integration` runtime source and its root and
component instructions. The evaluation stack lives separately in
`xaime-vp/CI-testing-and-improvement`; a worker may target it without moving the
runtime or running paid evaluations.

## Settings and state

Start from the platform's `workers/bonsai/.env.example`, copied outside the
checkout. These are example values, not discovery of a running installation:

```dotenv
COMPOSE_PROJECT_NAME=bonsai-evals
BONSAI_TARGET_REPOSITORY=xaime-vp/CI-testing-and-improvement
BONSAI_IMAGE=bonsai-worker:local
BONSAI_MAX_CONCURRENT_TASKS=2
BONSAI_POLICY_PATH=/srv/bonsai/evals/intake-policy.json
BONSAI_CHECKS_PATH=/srv/bonsai/evals/checks.json
```

- Policy/check paths must be absolute, existing files as seen by the container
  engine host. Verify resolved paths; Windows app storage can be redirected to
  a package directory that differs from its apparent path. WSL bind mounts need
  the actual Linux-visible path.
- Policy contains the matching repository, trusted owner login/numeric ID and
  resource/approval limits. Preserve known policy; do not invent an owner ID.
- For the eval repository, the documented offline workspace check is
  `{"workspace":[{"cwd":".","command":["python",".agents/tools/check.py"]}]}`.
  It covers unit tests and the identity guard, not Docker fixture oracles or
  paid model evaluation. Confirm the current target README before using it.
- Supply `GH_TOKEN` and `OPENROUTER_API_KEY` through the selected private source.
  Never commit real env files, credentials, installed configuration or reports.
  Use redacted/selected fields for inspection, not a full env/config dump.
- Compose generates `<project>_bonsai-state`. A different target needs a new
  project and volume. Existing deployments keep their original project/volume
  during upgrades. The entrypoint rejects a requested target that differs from
  prepared, installed or bound state.

## Authorized deployment

From the platform root, with a reviewed runtime image and private settings file:

```bash
docker compose --env-file /srv/bonsai/evals.env -f workers/bonsai/compose.yaml run --rm worker prepare
docker compose --env-file /srv/bonsai/evals.env -f workers/bonsai/compose.yaml run --rm worker install
docker compose --env-file /srv/bonsai/evals.env -f workers/bonsai/compose.yaml run --rm worker once
docker compose --env-file /srv/bonsai/evals.env -f workers/bonsai/compose.yaml up -d
```

Stop on a failed step. `once` inspects GitHub eligibility; it never launches or
publishes. Do not start a second listener to inspect an already-running one:
read its protected state/events instead, retaining the singleton lock.

Check repository access before activation using the intended worker credential,
not merely the separate GitHub connector's access. A read of
`GET /repos/owner/name` should succeed; inspect push permission if returned.
Use Contents, Issues and Pull requests permissions appropriate to the approved
workflow. A 404 does not prove the repository is absent. Ask the owner to grant
the selected credential access; never substitute another credential silently.

## Engine differences and readiness

The user's host has used Podman through WSL `podman-machine-default`; discover
the current engine with inventory first. Docker Compose may render successfully
while its attached `run` fails against a Podman API. Inspect whether the attempted
container started before retrying. Native Podman commands are an alternative;
preserve the same image, target, volume, mounts, capabilities and credential
boundaries. Do not add unrelated daemons or repeatedly retry the same failure.

The current controller capability set is `CHOWN,FOWNER,SETUID,SETGID,DAC_OVERRIDE,KILL`
after dropping all others; roles use distinct task-slot UIDs/GIDs (10001 and 10002 by default). Check current Compose code
before deployment. `FOWNER` is required to set modes after ownership transfers.
Installed releases are root-owned readable/executable, while private state stays
restricted. Image builds from Windows must preserve executable shell files and
LF endings; a clean Git archive can provide a Linux build context.

On rootless cgroups v1, configured memory/PID limits may be ignored and process
containment falls back to sessions. Disclose the observed limitation. Some
Podman OCI builds ignore image healthchecks, so verify the listener lock and
actual local relay socket rather than reporting a config-file healthcheck as
runtime readiness. Relay ports stay inside each container, without host ports.

Inspect the installed concurrency setting: preparation supports one or two task
slots; legacy configs without the field keep one. A launch env edit alone does
not replace the sealed release/configuration. For native Podman launches, preserve the 45-second stop grace with
`--stop-timeout 45`. Task relays use separate ephemeral
container-internal ports; the listener keeps its own idle readiness relay.

Separate evidence for repository access, target binding, a held listener lock,
error-free polling, a listening relay socket, model generation, generalist check outcomes,
reviewer outcome, draft publication and exact-head target CI. Do not call a
fresh idle deployment a successful issue-to-PR run.

The three-role runtime stages only generalist, reviewer and supervisor. Old
sealed releases may still run retired phases even after source changes. Stop
and confirm existing execution, prepare/install the reviewed release into the
same target-bound volume, and retain prior release/configuration and task history
for rollback. Generalist protected checks run once in its workspace; do not
report these as independent or repeated verifier checks. Retired pending tasks
need owner review and fresh generalist approval, not translated/replayed approvals.
