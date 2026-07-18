"""Unit contract for the agent-scoped coordination-runs API."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

pytestmark = pytest.mark.unit


def _run(coro):
    return asyncio.run(coro)


def _user(*, agent_name=None):
    return SimpleNamespace(
        id=7,
        username="owner@example.com",
        email="owner@example.com",
        agent_name=agent_name,
    )


def test_create_is_owned_and_records_agent_actor(monkeypatch):
    from models import CoordinationRunCreate
    from routers import coordination_runs as router

    captured = {}

    def create(**kwargs):
        captured.update(kwargs)
        return {"id": "cr_test", **kwargs, "status": "active", "version": 1}

    monkeypatch.setattr(router.db, "create_coordination_run", create)

    result = _run(
        router.create_coordination_run(
            data=CoordinationRunCreate(outcome="Ship the campaign"),
            agent_name="atlas",
            current_user=_user(agent_name="atlas"),
        )
    )

    assert result["id"] == "cr_test"
    assert captured["owner_agent"] == "atlas"
    assert captured["created_by"] == "agent:atlas"


def test_agent_scoped_caller_cannot_mutate_sibling(monkeypatch):
    from models import CoordinationRunCreate
    from routers import coordination_runs as router

    monkeypatch.setattr(
        router.db,
        "create_coordination_run",
        lambda **kwargs: pytest.fail("storage must not be called"),
    )

    with pytest.raises(HTTPException) as exc:
        _run(
            router.create_coordination_run(
                data=CoordinationRunCreate(outcome="Ship the campaign"),
                agent_name="atlas",
                current_user=_user(agent_name="marketing"),
            )
        )

    assert exc.value.status_code == 403


def test_get_hides_run_owned_by_another_agent(monkeypatch):
    from routers import coordination_runs as router

    monkeypatch.setattr(
        router.db,
        "get_coordination_run",
        lambda run_id: {"id": run_id, "owner_agent": "marketing"},
    )

    with pytest.raises(HTTPException) as exc:
        _run(router.get_coordination_run("cr_test", agent_name="atlas"))

    assert exc.value.status_code == 404


def test_update_returns_conflict_for_stale_version(monkeypatch):
    from models import CoordinationRunUpdate
    from routers import coordination_runs as router

    monkeypatch.setattr(
        router.db,
        "get_coordination_run",
        lambda run_id: {"id": run_id, "owner_agent": "atlas"},
    )
    monkeypatch.setattr(
        router.db, "update_coordination_run", lambda *args, **kwargs: None
    )

    with pytest.raises(HTTPException) as exc:
        _run(
            router.update_coordination_run(
                "cr_test",
                data=CoordinationRunUpdate(expected_version=1, status="waiting"),
                agent_name="atlas",
                current_user=_user(),
            )
        )

    assert exc.value.status_code == 409


def test_resource_type_is_closed_set():
    from models import CoordinationResourceAttach

    with pytest.raises(ValueError):
        CoordinationResourceAttach(
            resource_type="document", resource_id="doc-1", role="input"
        )


def test_context_has_a_storage_bound():
    from models import CoordinationRunCreate

    with pytest.raises(ValueError):
        CoordinationRunCreate(outcome="Bounded", context={"blob": "x" * 70_000})
