---
name: ui-browser-verification
description: Verify visible behavior and accessibility of Constant Integration UI changes in a browser using sanitized export fixtures. Use for frontend workflows, responsive layouts or visual regressions alongside ui-verification.
---

# Verify the UI in a browser

Read the [root boundaries](../../../AGENTS.md), the
[UI development guide](../../../agents/constant-integration-ui/AGENTS.md)
and [ui-verification](../ui-verification/SKILL.md). Identify the changed user flow,
expected behavior and source revision. Browser observations complement backend,
contract, type and build checks; they do not replace them.

Use the browser automation capability actually available in the client. Read its
instructions before operating it, inspect current state and use observed controls.
Do not claim screenshots or interaction coverage when no browser is available;
report the exact missing verification. Keep new test authorship with issue workers.

Start only the documented local UI services needed for the requested verification,
using loopback binding and synthetic or sanitized export fixtures. Record processes
started for this task and stop those processes afterward. Preserve existing user
services. Use the documented access gate without logging or committing its secret.
Never enable worker task controls, mount private worker state or expose a Docker
socket, terminal, credential store or arbitrary file browser to obtain a preview.

Exercise the changed flow with representative success, empty, loading, failure and
unknown/missing-evidence states when applicable. Inspect a desktop and narrow
viewport if layout changed. Check keyboard reachability, visible focus, labels,
readable contrast, overflow and long identifiers. Verify refresh or navigation
retains the expected selection/history without turning advisory data into actions.
Inspect relevant browser console/network failures and sanitized API responses.

For a defect, record reproducible steps, expected versus observed behavior, viewport
and source revision. Capture only sanitized evidence outside tracked source. After
an authorized fix, repeat the affected interaction and relevant existing checks.
Report exercised flows, outcomes and unverified cases separately from automated CI.
