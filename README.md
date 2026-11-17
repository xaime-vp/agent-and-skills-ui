# agent-and-skills-ui

This is a client adapter consuming reviewed resources from
[agent-and-skills](https://github.com/xaime-vp/agent-and-skills).
The local [root contract](AGENTS.md) selects the target, tool discovery and delivery
policy; generated skills and procedures are recorded in `harness-source.json`.

Run `python tools/check_harness_export.py` and `python tools/harness_check.py`.
Update shared content through the canonical source and
[export procedure](docs/agent-setup/shared-exports.md), then review the generated
diff. Client overrides belong outside managed paths. Runtime role bundles and
installed worker configuration retain their separate review/release process.

The developer handles tightly coupled tests/docs. Specialist issues are optional
for substantial independent work. Open a draft after a meaningful initial commit
and before dispatch that needs a parent PR. Existing PR work reuses its branch.

Lifecycle commands use the trusted runtime's managed CLI through
`tools/containers.py`; legacy force, container-default, relaunch and standalone
build commands are retired. See [workspace tools](tools/README.md).

The obsolete Pi Podman extension has been removed. The managed lifecycle CLI
supports native Docker on Linux/WSL; unsupported engines retain manual deployment.
