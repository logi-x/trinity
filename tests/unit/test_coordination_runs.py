"""Unit tests for durable coordination-run correlation."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

pytestmark = pytest.mark.unit


@pytest.fixture
def coordination_store(monkeypatch):
    from db import coordination_runs as module
    from db.tables import metadata

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    metadata.create_all(engine)
    monkeypatch.setattr(module, "get_engine", lambda: engine)
    return module.CoordinationRunOperations()


def test_create_run_links_root_execution(coordination_store):
    run = coordination_store.create_run(
        owner_agent="atlas",
        outcome="Rotate a shared credential safely",
        root_execution_id="exec-root",
        context={"acceptance_criteria": ["both systems verified"]},
        created_by="agent:atlas",
    )

    assert run["id"].startswith("cr_")
    assert run["owner_agent"] == "atlas"
    assert run["status"] == "active"
    assert run["version"] == 1
    assert run["context"] == {
        "acceptance_criteria": ["both systems verified"]
    }

    resources = coordination_store.list_resources(run["id"])
    assert resources == [
        {
            "run_id": run["id"],
            "resource_type": "execution",
            "resource_id": "exec-root",
            "role": "root",
            "created_at": resources[0]["created_at"],
            "notified_status": None,
            "notified_at": None,
        }
    ]


def test_attach_resource_is_idempotent(coordination_store):
    run = coordination_store.create_run(
        owner_agent="atlas",
        outcome="Coordinate an outcome",
        root_execution_id=None,
        context=None,
        created_by="user:1",
    )

    first = coordination_store.attach_resource(
        run["id"], "execution", "exec-child", "contributor"
    )
    second = coordination_store.attach_resource(
        run["id"], "execution", "exec-child", "contributor"
    )

    assert second == first
    assert len(coordination_store.list_resources(run["id"])) == 1


def test_update_run_uses_optimistic_version(coordination_store):
    run = coordination_store.create_run(
        owner_agent="atlas",
        outcome="Coordinate an outcome",
        root_execution_id=None,
        context={"stage": "intake"},
        created_by="agent:atlas",
    )

    updated = coordination_store.update_run(
        run["id"],
        expected_version=1,
        status="waiting",
        context={"stage": "approval"},
    )
    stale = coordination_store.update_run(
        run["id"],
        expected_version=1,
        status="blocked",
        context={"stage": "stale"},
    )

    assert updated["version"] == 2
    assert updated["status"] == "waiting"
    assert stale is None
    assert coordination_store.get_run(run["id"])["context"] == {
        "stage": "approval"
    }


def test_terminal_notification_claim_is_exactly_once_per_status(
    coordination_store,
):
    run = coordination_store.create_run(
        owner_agent="atlas",
        outcome="Coordinate an outcome",
        root_execution_id=None,
        context=None,
        created_by="agent:atlas",
    )
    coordination_store.attach_resource(
        run["id"], "execution", "exec-child", "lead"
    )

    first = coordination_store.claim_terminal_notifications(
        "execution", "exec-child", "success"
    )
    replay = coordination_store.claim_terminal_notifications(
        "execution", "exec-child", "success"
    )
    corrected = coordination_store.claim_terminal_notifications(
        "execution", "exec-child", "failed"
    )

    assert [item["run_id"] for item in first] == [run["id"]]
    assert replay == []
    assert [item["run_id"] for item in corrected] == [run["id"]]


def test_failed_event_persistence_can_release_and_reclaim(coordination_store):
    run = coordination_store.create_run(
        owner_agent="atlas",
        outcome="Coordinate an outcome",
        root_execution_id=None,
        context=None,
        created_by="agent:atlas",
    )
    coordination_store.attach_resource(
        run["id"], "execution", "exec-child", "lead"
    )
    coordination_store.claim_terminal_notifications(
        "execution", "exec-child", "success"
    )

    released = coordination_store.release_terminal_notification(
        run["id"], "execution", "exec-child", "success"
    )
    retried = coordination_store.claim_terminal_notifications(
        "execution", "exec-child", "success"
    )

    assert released is True
    assert [item["run_id"] for item in retried] == [run["id"]]


def test_context_is_stored_as_json_not_double_encoded(coordination_store):
    run = coordination_store.create_run(
        owner_agent="atlas",
        outcome="Coordinate an outcome",
        root_execution_id=None,
        context={"nested": {"value": 1}},
        created_by="agent:atlas",
    )

    assert run["context"] == {"nested": {"value": 1}}
    assert not isinstance(run["context"], str)


def test_context_can_be_explicitly_cleared(coordination_store):
    run = coordination_store.create_run(
        owner_agent="atlas",
        outcome="Coordinate an outcome",
        root_execution_id=None,
        context={"stage": "done"},
        created_by="agent:atlas",
    )

    updated = coordination_store.update_run(
        run["id"], expected_version=1, context=None
    )

    assert updated["context"] is None
