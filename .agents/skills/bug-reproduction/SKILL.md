---
name: bug-reproduction
description: Reproduce suspected defects with minimal isolated scenarios, real implementation calls, and targeted failure injection when a potential bug is found during review or debugging.
---

# Bug reproduction

Turn the suspicion into a falsifiable statement: input or interruption point,
expected invariant, actual observation and affected revision. Read surrounding
callers first so the scenario represents a reachable application path.

Use a disposable process and temporary state, not a live installation or user
database. Call the actual implementation with the smallest realistic fixture.
Mock external services, clocks or the failing I/O boundary; do not mock away the
behavior under review. Keep harnesses outside tracked implementation/test paths
when repository rules delegate test authoring. Record checkout edits or injected
dependencies; do not call an altered environment an untouched head.

Inject failures at meaningful boundaries: before a write, after publication but
before checkpoint persistence, during atomic replacement, or on retry. Assert
durable state and visible output, not just the exception. Repeat from fresh state
when needed to rule out contamination. Compare against the base if it distinguishes
a regression from an existing defect. Conclusive static defects need not force
expensive runtime reproduction; label static and runtime evidence accurately.

## Isolated runner

Use `scripts/run_probe.py --help` for a bounded subprocess with a fresh temporary
working directory, private HOME/temp area, environment allowlist and JSON evidence.
It uses argument arrays and never invokes a shell implicitly. Example:

```text
python scripts/run_probe.py --source /absolute/review/checkout --evidence /absolute/evidence/repro-1 --timeout 30 -- python /absolute/evidence/reproduce.py
```

Write a task-specific harness first. Import reviewed Python modules via
`REVIEW_SOURCE_ROOT`, which the runner supplies; add it explicitly to `sys.path`.
Use `REVIEW_SCRATCH_ROOT` for state. Evidence contains command, source HEAD/status,
timing, actual exit code, stdout and stderr. A nonzero exit may successfully
reproduce a defect; interpret assertions. A timeout is not proof of the defect.

The runner is process isolation, not an OS sandbox or network blocker. Review
the harness before execution. It terminates the direct child on timeout; use an
existing container/process-group mechanism for scenarios launching descendants.
Pass extra environment values only when needed. Do not pass credentials or put
secrets in arguments or captured output. Scratch is removed after the child exits;
keep useful evidence in its dedicated evidence directory.

Report the minimal trigger, expected versus observed behavior, revision,
environment, evidence and impact. If reproduction is unavailable, state why and
retain the suspicion as unconfirmed rather than inventing a pass.
