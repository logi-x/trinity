# Agent Additional Networks

## Purpose

Project-owner agents sometimes need private, container-to-container access to a project's database, Redis, or other development services. Trinity preserves its normal agent isolation while allowing only operator-approved external Docker networks.

## Configuration flow

1. The operator lists approved network names in `AGENT_ADDITIONAL_NETWORK_ALLOWLIST` on the backend.
2. Agent creation accepts `additional_networks`, or an owner updates the setting through `PUT /api/agents/{name}/additional-networks`.
3. The backend rejects malformed, built-in, Trinity-internal, unallowlisted, missing, or excessive network lists before changing the container.
4. The desired JSON list is persisted in `agent_ownership` and mirrored in the `trinity.additional-networks` Docker label.
5. The container is created on `trinity-agent-network`, then connected to each approved additional network through the Docker service layer.
6. On agent start, Trinity compares desired and actual attachments. Drift triggers the existing recreation path, which restores all approved networks while preserving the workspace volume.

## Security boundaries

- Additional networks never replace `trinity-agent-network`.
- `bridge`, `host`, `none`, `trinity-agent-network`, and `trinity-platform-network` cannot be requested.
- The global allowlist defaults to empty (deny all).
- Network names, not credentials, are stored in the database and Docker labels.
- Removing a name from the global allowlist prevents future create/recreate operations from attaching it.

## Verification

After restart, `GET /api/agents/{name}/additional-networks` reports `restart_needed: false`, and Docker shows the agent attached to its desired networks plus `trinity-agent-network`.
