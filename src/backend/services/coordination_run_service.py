"""Lifecycle notifications for resources linked to coordination runs."""

from __future__ import annotations

import logging

from services import agent_event_service


logger = logging.getLogger(__name__)


def persist_resource_terminal(
    store,
    resource_type: str,
    resource_id: str,
    resource_status: str,
) -> list[tuple[object, list]]:
    """Claim and durably persist continuation events before returning."""
    claims = store.claim_coordination_terminal_notifications(
        resource_type, resource_id, resource_status
    )
    event_type = f"coordination.{resource_type}.terminal"
    deliveries: list[tuple[object, list]] = []
    for claim in claims:
        try:
            delivery = agent_event_service.persist(
                source_agent=claim["owner_agent"],
                event_type=event_type,
                payload={
                    "coordination_run_id": claim["run_id"],
                    "resource_type": resource_type,
                    "resource_id": resource_id,
                    "resource_status": resource_status,
                    "role": claim["role"],
                },
            )
            deliveries.append(delivery)
        except Exception:  # noqa: BLE001 - terminal persistence must still win
            logger.exception(
                "Failed to emit coordination terminal for %s/%s",
                resource_type,
                resource_id,
            )
            store.release_coordination_terminal_notification(
                claim["run_id"], resource_type, resource_id, resource_status
            )
    return deliveries


async def dispatch_terminal_events(
    deliveries: list[tuple[object, list]],
    *,
    wait_for_subscriptions: bool = False,
) -> int:
    """Dispatch already-persisted events through existing subscriptions."""
    for event, matching in deliveries:
        try:
            if wait_for_subscriptions:
                await agent_event_service.dispatch(
                    event, matching, wait_for_subscriptions=True
                )
            else:
                await agent_event_service.dispatch(event, matching)
        except Exception:  # noqa: BLE001 - persisted history remains readable
            logger.exception("Failed to dispatch coordination event %s", event.id)
    return len(deliveries)


async def notify_resource_terminal(
    store,
    resource_type: str,
    resource_id: str,
    resource_status: str,
) -> int:
    """Convenience wrapper used by callers that already own an async context."""
    deliveries = persist_resource_terminal(
        store, resource_type, resource_id, resource_status
    )
    return await dispatch_terminal_events(deliveries)
