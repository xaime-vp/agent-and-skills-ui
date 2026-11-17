# Harness self-checks

The harness is executable configuration: skills, extensions, MCP entries, prompt
templates and instruction files. `tools/harness_check.py` makes its contracts
checkable without the `constant-integration/` checkout, so a fresh clone can
verify the workspace before any task starts.

Pi exposes the same menu as `/check` through [.pi/prompts/check.md](../../.pi/prompts/check.md),
and CI runs it from [.github/workflows/harness-check.yml](https://github.com/xaime-vp/agent-and-skills/blob/a701dcf2de332cce285b49c0b7c609f2d75d4328/.github/workflows/harness-check.yml).

## Run the menu

Use Python 3.12+ and install the pinned YAML parser once. The checker uses
PyYAML's safe loader so malformed YAML fails and multiline descriptions work;
it does not install dependencies itself. On Windows, replace `python3` with
`py -3` in these commands.

```sh
python3 -m pip install -r tools/requirements-harness.txt
python3 tools/harness_check.py            # all checks, human-readable
python3 tools/harness_check.py --strict   # warnings also fail
python3 tools/harness_check.py --json     # machine-readable result
python3 tools/harness_check.py --only skills,links
python3 -m unittest discover -s tools/tests -p 'test_*.py'
node --test .pi/extensions/*.test.mjs       # Node 22+
```

In Pi, start from this workspace, trust the project configuration, and run
`/reload` after adding or changing the template. `/check` runs the menu and its
regression tests; `/check --only skills,links` selects checker categories.
The template uses Pi's native `$@` argument expansion and asks the agent to
report actual command results. It does not register another executable extension
or claim to run checks merely by being loaded. See Pi's
[prompt-template documentation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/prompt-templates.md).

Exit status is `0` when every check passes, `1` when an error (or, with
`--strict`, a warning) is found, and `2` for a usage or environment problem.
The command never contacts GitHub, starts a worker, edits a file or reads
credentials.

## What each check proves

| Check | Proves |
| --- | --- |
| `skills` | Skill frontmatter is a YAML mapping with a directory-matching lowercase-hyphenated string `name` (≤64 characters) and a non-empty string `description` (≤1024 characters); routing cues and placeholders produce advisory warnings |
| `skill-parity` | Every skill ships valid YAML display metadata with non-empty strings under `interface.display_name` and `interface.short_description`; this is metadata coverage, not proof of client discovery |
| `prompts` | Direct `.pi/prompts/*.md` templates have valid optional YAML mappings and string description/hint fields; filenames are valid command names and unsupported `${@}` is rejected |
| `links` | Inline relative Markdown links outside fenced examples resolve inside the repository; optional `constant-integration/` targets are exempt. Fence character and length are respected |
| `mcp` | `.pi/mcp.json` parses; explicit/inferred stdio requires a command and HTTP/SSE requires an absolute HTTP(S) URL; conflicting transports and invalid args/header/env types fail. Transport-free overrides warn; recognized literal secret patterns fail |
| `secrets` | Tracked harness files contain no obvious GitHub, OpenAI or private-key material |
| `extensions` | Pi entries use supported `typebox` imports, referenced sibling `*-core.mjs` modules exist (tests may warn), and deprecated `.pi/tools` or `.pi/hooks` discovery directories are absent; dependency-free Node tests are reported as not run |

Pi registers model-callable custom tools through `pi.registerTool()` in
`.pi/extensions/`. The root `tools/` contains standalone Python CLI utilities,
not Pi custom-tool entry points. Although Pi 1.x compatibility mappings can
accept older pi-ai TypeBox imports, use `typebox` directly.

## What it cannot prove

- Passing checks do not prove that the running Pi session loaded a skill, that an
  MCP server connected, or that an installed Bonsai release supports a route.
- `agents/openai.yaml` is optional Codex display metadata. Pi discovers skills
  from `SKILL.md`; adding display metadata does not enable Codex discovery of
  `.pi/skills/` or change the separate Codex harness's inventory.
- `tools/check.py`, `tools/docker_worker.py` and the E2E probes still need the
  dedicated checkout. This command does not run them and does not treat their
  absence as a harness failure.
- Warnings stay advisory: they mark weak routing descriptions, missing testable
  core modules or placeholder text. `--strict` turns them into failures when a
  branch intends to hold that line.
- The validator's positive/negative regression tests and dependency-free Node
  extension tests are separate from the checker. CI runs all three commands.

Run `python3 tools/harness_check.py --help` for the argument list.
