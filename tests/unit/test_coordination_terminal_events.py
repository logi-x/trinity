"""Terminal resources re-enter coordination through persisted agent events."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

pytestmark = pytest.mark.unit


def _run(coro):
    return asyncio.run(coro)


def test_linked_terminal_emits_owner_scoped_continuation_event(monkeypatch):
    from services import coordination_run_service as service

    store = MagicMock()
    store.claim_coordination_terminal_notifications.return_value = [
        {
            "run_id": "cr_campaign",
            "resource_type": "execution",
            "resource_id": "exec_marketing",
            "role": "marketing_lead",
            "owner_agent": "atlas",
        }
    ]
    event = SimpleNamespace(id="evt-1")
    persist = MagicMock(return_value=(event, []))
    dispatch = AsyncMock()
    monkeypatch.setattr(service.agent_event_service, "persist", persist)
    monkeypatch.setattr(service.agent_event_service, "dispatch", dispatch)

    emitted = _run(
        service.notify_resource_terminal(
            store, "execution", "exec_marketing", "success"
        )
    )

    assert emitted == 1
    persist.assert_called_once_with(
        source_agent="atlas",
        event_type="coordination.execution.terminal",
        payload={
            "coordination_run_id": "cr_campaign",
            "resource_type": "execution",
            "resource_id": "exec_marketing",
            "resource_status": "success",
            "role": "marketing_lead",
        },
    )
    dispatch.assert_awaited_once_with(event, [])


def test_unlinked_or_replayed_terminal_emits_nothing(monkeypatch):
    from services import coordination_run_service as service

    store = MagicMock()
    store.claim_coordination_terminal_notifications.return_value = []
    persist = MagicMock()
    monkeypatch.setattr(service.agent_event_service, "persist", persist)

    emitted = _run(
        service.notify_resource_terminal(store, "operator_queue", "opq_1", "responded")
    )

    assert emitted == 0
    persist.assert_not_called()


def test_event_persistence_failure_releases_claim_for_retry(monkeypatch):
    from services import coordination_run_service as service

    store = MagicMock()
    store.claim_coordination_terminal_notifications.return_value = [
        {
            "run_id": "cr_campaign",
            "resource_type": "execution",
            "resource_id": "exec_marketing",
            "role": "lead",
            "owner_agent": "atlas",
        }
    ]
    monkeypatch.setattr(
        service.agent_event_service,
        "persist",
        MagicMock(side_effect=RuntimeError("database unavailable")),
    )

    deliveries = service.persist_resource_terminal(
        store, "execution", "exec_marketing", "success"
    )

    assert deliveries == []
    store.release_coordination_terminal_notification.assert_called_once_with(
        "cr_campaign", "execution", "exec_marketing", "success"
    )
