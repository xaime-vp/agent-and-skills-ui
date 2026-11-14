---
name: pr-submission
description: Prepare, submit or update a GitHub pull request with concise change and validation evidence, including function-level attribution for delegated implementation, review and checks. Use for PR delivery; this skill does not dispatch workers or authorize merging or deployment.
---

Keep `references/` alongside `SKILL.md` (see the workspace `README.md`; this skill guides PR prep and grants no GitHub credentials, approval, or merge authority).

# PR submission

Support the [root Git developer](../../../AGENTS.md). Source changes live in
`constant-integration-ui/`; GitHub MCP owns remote branch, commit, PR and issue
operations. Open the parent draft before application implementation, then
maintain that PR throughout the task. Use workspace `bonsai-ci` for required
test/documentation handoffs to its existing branch. This submission skill
does not independently create another worker task or another PR.

Handoffs can use free-form preparation with operator-selected `--target-pr` and
digest-bound proposal approval, or legacy envelopes with numeric `pull_request`
and standalone approval. Follow `bonsai-ci` for the selected route; issue creation
does not require a hand-written envelope in the free-form workflow. Record the
actual sealed proposal/approval and delivery evidence when used.

The UI harness lives on the `main` branch of
`xaime-vp/agent-and-skills-ui`, with skills, tools and guides under `.agents/`.
UI application changes belong in `xaime-vp/constant-integration-ui`. Keep
harness and application changes in separate scoped PRs against their
respective bases. Runtime changes belong in `xaime-vp/constant-integration`.
Select exact task paths and preserve unrelated local work.

Produce a reviewable PR against the intended repository and base, with an honest
account of behavior, validation and delegated contributions. Follow the target
repository's instructions and PR template. This skill grants no new authority
to delegate, publish, approve worker execution, merge or deploy.

## Prepare the change

1. Confirm the target repository, base branch, requested outcome and applicable
   instructions. Inspect the current branch, diff and worktree status. Preserve
   unrelated edits; use a separate branch/worktree when needed. In Constant
   Integration, use a `codex/` branch and read its delivery and role contracts.
2. Inspect existing open PRs for the same work before creating another. Update
   the intended PR when requested; keep one coherent change per PR. Record
   dependencies explicitly. A PR that depends on unmerged work is not independent.
3. Review the actual final diff, including delegated changes. Check scope,
   correctness and sensitive data; an agent's completion message is not evidence
   that the diff or checks are correct. Disclose unresolved findings.
4. Run the target's appropriate checks and required pre-merge checks. Record the
   command, exit/status, source revision and environment limitations. Distinguish
   tests you ran from worker check records, advisory model review and target CI.
   Keep failed, skipped and unrun checks visible. Do not run live workers, paid
   models, installations or external mutations as incidental validation.

## Attribute delegated functions

On current Bonsai source, test-specialist work has embedded read-only review;
documentation publishes without a model reviewer. Preserve that distinction
instead of fabricating a verdict. Separate opt-in automatic PR reviews are
advisory commit-bound `COMMENT` reviews and execute no checks.

Use [the attribution examples](references/attribution.md) when work was delegated
or contribution provenance is unclear. Maintain a small record while integrating
work, then reconcile it against the final diff.

- Identify each meaningful delegated function, symbol or work unit and its file
  path. Describe the contribution in terms a reviewer can locate. Group closely
  related helpers; avoid a row for every trivial function. For non-code work,
  identify the guide section, workflow, configuration or other artifact.
- Name the actual executor: worker/agent/tool and the configured model only when
  observed. Separate requested identity, configured identity and provider-attested
  identity; a configured model is not proof of which hosted model served a call.
  Use `unknown` for unavailable identity instead of inferring it from a skill
  name, PR author, branch name or default configuration.
- Distinguish implementation, integration/repair, review and check execution.
  Reading delegated code is review, not authorship. A CLI publishing the PR is
  not its implementer. If an integrator materially rewrites delegated code,
  credit the original contribution and describe the rewrite.
- Link available task/approval, worker PR, commit or redacted report evidence.
  Worker approval proves authorization, not authorship, correctness or acceptance.
  Do not publish prompts, reasoning, credentials, private host paths or raw logs.
- Put a compact `Contributions` table in the PR body for delegated work. Keep
  check outcomes under validation and identify who actually executed them.
  If nothing was delegated, omit the table or state that briefly when the target
  template requires attribution. Do not create fictional delegated contributors.
- Preserve existing author metadata and trailers. Add model trailers such as
  `Generated-By` only when the target's convention or explicit instruction calls
  for them, using known identity. Never invent `Co-authored-by` identities or
  emails, rewrite historical commits for attribution, or imply all code in a
  mixed contribution came from one model. Do not add source comments solely as
  attribution unless the repository requires them.

## Submit or update

Lead the title/body with the concrete problem and resulting behavior. Describe
the final implementation, relevant tradeoffs and material limitations. Use the
repository template; include a task reference, validation and contribution
provenance where applicable. Omit planning transcripts and abandoned approaches
unless needed to explain a tradeoff.

Use existing authorization for the requested PR publication; do not ask again
merely because this skill is loaded. If publication was not authorized, prepare
the concrete diff and PR body before seeking that permission. Prefer a connected
GitHub tool when sufficient. With `gh`, pass multiline bodies through a file
using `--body-file`; do not interpolate untrusted text into shell code.

Push only the scoped branch, create/update the intended PR, and use draft status
when required by the repository or when the change is incomplete. Disclose
semantic, state/configuration and rollback changes. Do not overwrite a
concurrently changed PR head. In a Bonsai worker task, the supervisor alone owns
Git and publication; model-driven roles supply their assigned implementation or
review output without publishing themselves. Preserve mandatory draft findings.

After publication, inspect GitHub checks at the exact PR head. Record success,
failure, pending or unavailable status without treating old-head results as
current. Follow explicit requests to watch CI through completion; otherwise
report the observed status without implying a pass. If the active client
provides a PR artifact tool, attach the PR to the chat; otherwise return the PR
link, brief scope, validation limits and any action needed from the owner. Owner
acceptance, merge and deployment remain separate decisions.
