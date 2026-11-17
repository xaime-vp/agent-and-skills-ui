---
name: skill-maintenance
description: Create, adapt or audit skills and instruction routing in this developer harness. Use for missing skills, client migrations, conflicting guidance or role-specific skill improvements.
---

# Maintain this harness's skills

Read the [root contract](../../../AGENTS.md), the requested skill and its callers.
Identify the owning repository, client, application target and delivery policy
before adapting guidance. Requested harness instructions can be edited directly;
product test and documentation ownership still follows the root contract.

This Pi harness keeps skills under `.pi/skills/`, targets Constant Integration
by default, and owns implementation plus any explicitly selected issue-worker follow-through.
Keep application code in its separate checkout and use Pi-native capabilities.

## Make the smallest useful addition

Compare the requested behavior with installed skills, active PRs and discovery
tables. Repair or extend an existing skill when it already owns the task. Add a
skill only for a distinct reusable capability. Do not copy unrelated image,
document, database or deployment skills just to increase the inventory.

Use a lowercase hyphenated directory/name and YAML frontmatter containing `name`
and a concise `description` that states its capability and activation conditions.
Include only instructions that change decisions or preserve a concrete invariant.
Put conditional procedures in linked references; add executable helpers only when
they remove repeated or fragile work. Preserve existing metadata and invocation
policy. Normal automatic discovery remains enabled unless the user requests otherwise.

Keep task authorization separate from tool availability. Discover actual tool
names and schemas in the active client; never assume another client's subagent
role, nested-tool API, credentials or MCP configuration is available. Use an
authorized fallback and report missing capabilities. Skill activation alone does
not authorize external messages, live workers, paid services, merge or deployment.

## Promote recurring friction into the harness

A correction you make twice is a harness defect, not a one-off. Capture it, surface
it, then distill it into the cheapest durable form:

- **Capture** at the point of friction: record the request, the file and the exact
  wrong behavior. Keep it outside the skill until you know it recurs.
- **Surface** the pattern when the same correction appears in a second session or
  from a reviewer finding, and check whether an existing skill already owns it.
- **Distill** into the narrowest mechanism that prevents the mistake: a single
  instruction line, an executable helper, a link check, or a `harness_check.py`
  assertion. Prefer an executable check over a reminder when the rule is
  mechanical, and delete the superseded prose once the check exists.

Do not accumulate rules that no longer change a decision. A check that cannot fail
is a comment; a rule that duplicates an existing one adds instruction budget
without adding behavior.

## Verify the result

- Check YAML frontmatter, unique names, narrow descriptions and unfinished placeholders.
- Run `python3 tools/harness_check.py` for metadata, link, MCP and parity regressions,
  and treat its warnings about weak routing descriptions as real routing risk.
- Resolve relative links from their containing file. Distinguish harness-owned
  files from optional application checkouts and required runtime source assets.
- Check AGENTS.md, README and invocation routes agree with actual skill locations.
- Run changed helpers and relevant existing checks without starting live workers.
- Walk through a normal request, a read-only request and a missing-tool case.
  For asynchronous work, verify the role's stopping rule and honest status report.
- Inspect the final diff for lost requirements, secrets, duplicate skill trees and
  client-specific assumptions. Record tested revision and material limits in the PR.

Use a skill validator already available in the environment when useful; this
harness does not assume a system skill package is installed. Behavioral inspection
and real helper execution complement metadata validation. Delegate an independent
scenario only when authorized and proportionate to the change.
