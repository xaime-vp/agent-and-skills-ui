# Shared skills and client adapters

Author shared methods under `.pi/skills/`, role guides under `agents/`, and shared
developer procedures under `docs/agent-setup/`. Consumer roots remain small local
adapters selecting the application target, available tools and delivery policy.
Codex's asynchronous stopping rule and the UI's sanitized-export boundary remain
explicit consumer policy. A generated skill never overrides that root policy.

`tools/export_harness.py` reads committed Git objects, not dirty worktree bytes.
It exports an explicit resource set and records the exact source commit and every
generated path/hash in `harness-source.json`. It never exports credentials, MCP
settings, root instructions, nested application checkouts or installed resources.
It performs no installation, network/model call or worker operation.

Profiles:
- `codex`: `.agents/skills/`, shared guides and offline workspace adapters.
- `ui`: `.pi/skills/`, Pi extensions/templates, guides and workspace adapters.
- `reference`: nine reusable investigation methods plus the hash checker.
  Generic deployment configuration, guides, extensions, delivery policy and role
  bundles remain local adaptations with their own provenance and checks.

Initial adoption is deliberate and should be inspected as a PR diff:

```sh
python tools/export_harness.py --profile codex --destination ../agent-and-skills-codex --revision REVIEWED_COMMIT
python tools/export_harness.py --profile codex --destination ../agent-and-skills-codex --revision REVIEWED_COMMIT --write --adopt
```

The default command is read-only: exit 0 means current, 1 means drift, 2 means
invalid input. Subsequent checks default to the consumer's recorded revision.
Supply a new reviewed commit explicitly to update; `--write` refuses locally
edited managed files. `--adopt` is for a reviewed migration, not routine updates.
Only previously managed files may be removed; unowned client files are preserved.
Markdown links are resolved from their source paths and rewritten for the target;
references to unexported source resources use the pinned source URL.

Consumers run `python tools/check_harness_export.py` in CI for local byte drift.
This is consistency with the manifest, not authenticity. For source parity, run
the source exporter against an independently reviewed commit and inspect its diff.
Line endings normalize to LF for hashes so Windows checkout settings do not create
false drift. Keep deliberate client overrides outside generated paths.

The workspace's role exporter remains separate. Never dynamically load resources
from task-controlled repositories or update a sealed worker by copying these files.
