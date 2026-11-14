---
name: state-recovery-validation
description: Validate interrupted writes, retries, checkpoint consistency and duplicate delivery when reviewed changes affect persistence, queues or incremental exports.
---

# State recovery validation

Map durable and externally visible steps: read checkpoint, select pending work,
assign identity/sequence, write payload, publish/rename, persist acknowledgement,
resume. Identify transaction and lock boundaries. Atomic replacement of one file
does not make publication plus checkpoint update atomic. Derive invariants from
the actual delivery contract; do not assume every queue promises exactly-once.

Use temporary state and real persistence/delivery code. Inject failure at changed
boundaries, especially after output becomes visible but before the checkpoint is
durable. Restart with a new instance against the same state. Inspect initial and
retry output for event loss, changed bodies under stable IDs, reused sequences,
duplicate business actions and inaccessible recovery state. Account for the
consumer's actual deduplication rules.

Choose other cases from the diff: a later chunk failing after earlier success,
unchanged retries, malformed JSON and invalid field types, missing checkpoints,
mismatched stream identity, and concurrent writers if multiple entrypoints share
state. Treat booleans separately from integers in Python schemas. Missing,
foreign and corrupt matching state may need different policies. A documented
reset must not silently reuse an existing stream's delivery positions.

Keep dependency/write failures distinguishable from corruption. Check rollback
and migration when formats change. Do not delete unknown live state to force a
pass or mock away the transaction whose behavior is under review.

## Delivery evidence helper

`scripts/audit_delivery.py --help` audits history-v1-style batch directories
(`manifest.json`, `events.jsonl`) for repeated event IDs, conflicting bodies,
sequence collisions/gaps, declared ranges and an optional matching checkpoint.
Provide `--stream-id` to select the checkpoint stream when input includes several.
It never modifies files. It does not replace the application's schema validator
or business-level idempotency assertions. Repeated identical delivery is reported
as an observation; conflicting identities or positions fail the audit.

Use the installed companion `bug-reproduction` skill for harness/capture when
useful. Report the failure point, before/retry state, broken invariant, consumer
impact, revision and recovery strategy to verify. Distinguish idempotent replay
from conflicting duplicate delivery.
