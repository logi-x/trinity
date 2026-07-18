"""Persist and dispatch Trinity agent events independently of HTTP routers."""

from __future__ import annotations

import asyncio
import json
import logging
import re

from database import db
from db_models import AgentEvent, EventSubscription


logger = logging.getLogger(__name__)

_websocket_manager = None
_filtered_websocket_manager = None


def set_websocket_manager(manager) -> None:
    global _websocket_manager
    _websocket_manager = manager


def set_filtered_websocket_manager(manager) -> None:
    global _filtered_websocket_manager
    _filtered_websocket_manager = manager


def _interpolate_template(template: str, payload: dict) -> str:
    def replacer(match):
        parts = match.group(1).split(".")[1:]
        value = payload
        for part in parts:
            if not isinstance(value, dict) or part not in value:
                return match.group(0)
            value = value[part]
        return str(value)

    return re.sub(
        r"\{\{(payload(?:\.[a-zA-Z0-9_]+)+)\}\}", replacer, template
    )


def _get_internal_token() -> str:
    from datetime import datetime, timedelta

    from config import ALGORITHM, SECRET_KEY
    from jose import jwt

    return jwt.encode(
        {"sub": "admin", "exp": datetime.utcnow() + timedelta(minutes=5)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


async def _trigger_subscription(
    subscription: EventSubscription,
    event: AgentEvent,
) -> None:
    """Submit an async task to a matching subscriber."""
    import httpx

    message = subscription.target_message
    if event.payload:
        message = _interpolate_template(message, event.payload)
    message = f"[Event from {event.source_agent}: {event.event_type}]\n\n{message}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"http://localhost:8000/api/agents/{subscription.subscriber_agent}/task",
                json={
                    "message": message,
                    "async_mode": True,
                    "system_prompt": (
                        "This task was triggered by an event subscription. "
                        f"Source agent: {event.source_agent}, "
                        f"Event type: {event.event_type}, Event ID: {event.id}"
                    ),
                },
                headers={
                    "Authorization": f"Bearer {_get_internal_token()}",
                    "X-Source-Agent": event.source_agent,
                    "X-Via-MCP": "true",
                },
            )
            if response.status_code >= 400:
                logger.warning(
                    "[EVT-001] Failed to trigger subscription %s on %s: %s %s",
                    subscription.id,
                    subscription.subscriber_agent,
                    response.status_code,
                    response.text[:200],
                )
            else:
                logger.info(
                    "[EVT-001] Triggered subscription %s: %s.%s -> %s",
                    subscription.id,
                    event.source_agent,
                    event.event_type,
                    subscription.subscriber_agent,
                )
    except Exception as exc:  # noqa: BLE001 - event delivery is best-effort
        logger.error(
            "[EVT-001] Error triggering subscription %s on %s: %s",
            subscription.id,
            subscription.subscriber_agent,
            exc,
        )


async def _broadcast(event: AgentEvent, subscriptions_triggered: int) -> None:
    ws_event = {
        "type": "agent_event",
        "event_id": event.id,
        "source_agent": event.source_agent,
        "event_type": event.event_type,
        "subscriptions_triggered": subscriptions_triggered,
        "timestamp": event.created_at,
    }
    if _websocket_manager:
        await _websocket_manager.broadcast(json.dumps(ws_event))
    if _filtered_websocket_manager:
        await _filtered_websocket_manager.broadcast_filtered(ws_event)


def persist(
    *, source_agent: str, event_type: str, payload: dict | None
) -> tuple[AgentEvent, list[EventSubscription]]:
    """Persist an event synchronously before any best-effort delivery work."""
    matching = db.find_matching_event_subscriptions(source_agent, event_type)
    event = db.create_agent_event(
        source_agent=source_agent,
        event_type=event_type,
        payload=payload,
        subscriptions_triggered=len(matching),
    )
    logger.info(
        "[EVT-001] Event emitted: %s.%s (%s subscriptions matched)",
        source_agent,
        event_type,
        len(matching),
    )
    return event, matching


async def dispatch(
    event: AgentEvent,
    matching: list[EventSubscription],
    *,
    wait_for_subscriptions: bool = False,
) -> None:
    """Best-effort delivery for an event that is already durable."""
    tasks = [
        asyncio.create_task(_trigger_subscription(subscription, event))
        for subscription in matching
    ]
    await _broadcast(event, len(matching))
    if wait_for_subscriptions and tasks:
        await asyncio.gather(*tasks, return_exceptions=True)


async def emit(*, source_agent: str, event_type: str, payload: dict | None) -> AgentEvent:
    """Persist an event, then dispatch all currently matching subscriptions."""
    event, matching = persist(
        source_agent=source_agent,
        event_type=event_type,
        payload=payload,
    )
    await dispatch(event, matching)
    return event
