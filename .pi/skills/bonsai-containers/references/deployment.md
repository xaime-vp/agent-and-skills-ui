# Worker deployment and recovery

Use the [container skill](../SKILL.md) and the runtime's authoritative
[lifecycle guide](https://github.com/xaime-vp/constant-integration/blob/main/docs/CONTAINER_LIFECYCLE.md).
The workspace adapters forward argv and exit codes; they do not implement Docker
inspection, stop, builds, state changes or recovery.

Register and verify the actual bound installation using its supported Linux/WSL
host and private registry. Verify the selected source and installed compatibility.
Never infer an installed feature from a workspace pull or a generated skill.

Read-only inspection and source checks do not authorize restart, upgrade, task
admission, paid probes or listener startup. Keep restart and upgrade distinct;
upgrades remain stopped unless startup was explicitly selected. Unknown work or
failed inspection blocks lifecycle mutation. Preserve backups, private artifacts,
configuration and operation identity when recovering an interrupted action.

For consultation-enabled releases, retain both State and child-call artifacts,
including unknown reservations. See [consultation guidance](../../../../docs/agent-setup/repository-consultation.md).
