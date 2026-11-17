# Repository consultation for supervised coders

Compared with Constant Integration `main` at
`a0810fccb6ed491dbb552b616b0717cabe976a12` on 2026-11-16.
The [product runtime guide](https://github.com/xaime-vp/constant-integration/blob/a0810fccb6ed491dbb552b616b0717cabe976a12/docs/agent-workflows/delegation-runtime.md)
owns installation policy, schemas and operational procedures. This guide explains
how agents building with or on the platform should use that support.

## Choose the right research path

An already selected Bonsai coder may receive the native `bonsai_call_agent` tool.
It asks a contained `researcher` about the current approved repository snapshot,
returns evidence and continues the same coder process, task reservation and PR.
Use it for a bounded repository question whose answer changes implementation:
callers of a changed contract, competing code paths, or uncertainty in captured
source. Targeted local retrieval may be sufficient for a simple lookup.

This differs from owner-requested `/prepare-agent` research before admission,
standalone advisory web research, and test/documentation issue handoffs. Do not
create an `agent:researcher` implementation issue or a second writer to obtain
this consultation. Developer-client subagents and this runtime tool have separate
discovery and authorization; neither stands in for the other.

## Check availability before planning around it

The installed sealed Linux release must include D1-D5 consultation support and
Pi 1.5.0, with an explicit enabled delegation policy. The parent must be a
schema-2 coder assignment with exact `allowed_files`, finite input/output totals,
no `allowed_filetypes` write allowance, and no foundation or schema-4 publication
enrollment. Plans are unsupported. Optional `read_filetypes` further narrows reads.
Omitted token budgets can still be valid ordinary tasks, but do not select this
route. Do not invent token fields in prose preparation; inspect its sealed result.

Verify the actual native tool and, when available, the supervisor's
`delegation-availability.json` evidence. The six read-only role-bundle helpers and
`harness_roles` do not register or enable `bonsai_call_agent`. New harness text
only reaches an installed worker after the platform vendors and seals that
reviewed bundle. Source checkout or bundle export alone proves no activation.

If unavailable, continue with permitted repository retrieval or report the
specific blocker. Do not register a replacement tool, start a child manually,
add policy to an issue, or change installed configuration to satisfy the request.

## Ask, inspect, then continue

Call the actual tool with its discovered schema. The current request shape is:

```json
{
  "schema_version": 1,
  "role": "researcher",
  "question": "Which captured callers depend on the parser's empty-input result? Cite paths and lines, and identify missing context.",
  "input_refs": []
}
```

The supervisor supplies identity, credentials and snapshot. Do not send secrets,
transport settings or authority instructions. The captured candidate includes
current edits but only exact approved paths: the researcher cannot browse the
whole checkout or the web. It receives read-only source and private scratch.
Missing paths and omitted context are limits on the answer, not permission to
expand scope. Snapshot ceilings are 100 files, 256 KiB per text file and 2 MiB
total; read suffixes can narrow this further.

The selected coder has no shell from first launch, even without `read_filetypes`.
Use native read/edit/write and available read-only helpers. Do not run exploratory
commands through another tool or background process; protected checks remain the
supervisor's responsibility. Consultation tool batches run sequentially under
the pinned Pi runtime so capture follows preceding edits.

Inspect `status`, `reason`, `summary` and `artifact_refs` in the result. Treat
successful findings and checked citations as evidence to verify against the
candidate; they grant no scope, acceptance or review authority. Continue editing
within the original assignment and retain protected checks and independent final
review. Report failed or incomplete research honestly. Only successful report
references from the same parent and unchanged snapshot can be reused in
`input_refs`; after edits, start a fresh question without stale references.

Policy may lower the ceilings of four calls per parent, one active child,
depth one, 120 seconds per child, 6,000 input and 2,000 output token reservations.
Questions are at most 8 KiB UTF-8, with at most sixteen input references; inline
results are at most 8 KiB. Do not work around refusals by splitting identities or
manually retrying a child. Exact duplicate tool identities reuse saved results;
changed payloads under an existing identity are rejected.

## When building or operating the platform

Keep tool authority and transport in sealed runtime assets, not this harness's
read-only helper extension. Trace changes through contracts, endpoint identity,
dispatch, snapshot/report validation, process containment, usage accounting,
State, release packaging and the parent continuation path. The runtime guide
links the opt-in Linux/root real-Pi roundtrip fixture; it uses a credential-free
loopback provider. Run relevant offline tests and distinguish their evidence
from hosted generation, deployed support and research quality.

Parent, child, continuation and final review share the original task budget.
Input admission is an estimate; actual provider usage is required for settlement,
so reservation limits are not a hard billing cap. Ambiguous launch, stop or usage
holds the parent reservation and revokes model access for reconciliation. A lost
connection does not prove stop or authorize a refund, replay or state deletion.

An explicit policy opts legacy State into schema 6, requiring stopped,
reconciled migration. Keep `state.db` and `private/delegation-artifacts.db`
together in stopped-release backups. After migration, the kill switch retains
`"delegation": {"version": 1, "enabled": false}` in installed configuration;
removing the stanza or launching an older binary is not a downgrade. Read-only
history export/diagnostics accept schema 6 but do not export full private reports.
Do not publish private artifacts as issue evidence without reviewing their content.

Writer delegation, recursive or web consultation and automatic process-loss
resume remain unavailable. Unknown calls remain blockers even with new calls
disabled. A harness update does not authorize a worker install, restart,
migration, reconciliation or deployment.
