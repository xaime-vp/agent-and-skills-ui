---
description: Run the harness validation menu and report every result
argument-hint: "[--only skills,links] [--json] [--strict]"
---
Run the workspace validation menu from the repository root:

Use an available Python 3.12+ interpreter (`py -3` on Windows, `python3` on
Linux/macOS, or `python` when it is Python 3.12+). Use that same interpreter for:

1. `python3 tools/harness_check.py $@` (substitute the selected interpreter).
2. `python3 -m unittest discover -s tools/tests -p 'test_*.py'`.
3. `node --test .pi/extensions/*.test.mjs` (Node 22+).

Report each command, its exit status and any failure text verbatim. Do not start
workers, publish anything, or change files to make a check pass. When a check
needs the `constant-integration/` checkout and it is absent, report it as
unavailable rather than failed. Report missing Python, Node or PyYAML as setup
requirements; do not install them automatically. PyYAML setup is documented in
`docs/agent-setup/harness-checks.md`. Use `/check --only skills,links` to select
checks; `/check` runs all checks. Run `/reload` after changing this template.
