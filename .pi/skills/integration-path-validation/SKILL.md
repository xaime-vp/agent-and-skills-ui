---
name: integration-path-validation
description: Validate startup, imports, CI dependency environments and end-to-end integration boundaries when reviewed changes affect runtime wiring or CI behavior.
---

# Integration path validation

Trace each changed boundary from its real entrypoint to observable behavior:
CLI/main, service initialization, configuration/environment parsing, imports,
dependency installation, dispatch and shutdown. Select checks for paths the diff
changes; do not turn every runtime edit into an unrelated system audit.

Passing helper tests do not establish that the application starts. Exercise the
actual entrypoint in a disposable process with minimal valid configuration.
Cover feature-disabled startup and enabled behavior when an optional feature
changes unconditional initialization. Check inspection/one-shot modes sharing
that setup. Stub network/model/process-launch operations at their boundary while
retaining real startup logic. Do not start production listeners or paid services.

For changed imports or test dependencies, read the exact CI job: checkout scope,
runtime version, working directory, install commands, extras and test command.
Reproduce that dependency set in a clean environment instead of a developer
environment with everything installed. Check whether nominally pure modules now
import optional runtime dependencies. Test collection is part of this boundary.

Use pinned lint/type/compile checks where they detect missing names, import cycles
or packaging mistakes; compilation does not prove runtime name resolution.
Exercise cross-package imports from supported installation/working directories.
Preserve standalone/sealed packaging contracts where present.

Use the installed companion `bug-reproduction` skill's bounded subprocess helper
when isolation and evidence capture are useful. Its environment isolation is not
a dependency-clean venv: create the required venv/container and pass its interpreter
explicitly. Distinguish host OS limitations from target failures and deliberately
missing dependencies in a clean environment.

Read failed CI logs at the reviewed head. Tie defects to concrete reachable paths
and propose the missing integration check. Report which startup/config/package/CI
paths ran and which remain unverified. Apply repository rules before authoring
permanent regression tests or corrections; review alone authorizes neither.
