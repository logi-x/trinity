"""Agent-scoped API for durable cross-agent work correlation.

This API owns no workflow semantics. It persists generic lifecycle, opaque
agent context, and links to existing execution/operator-queue records.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from database import db
from dependencies import (
    AuthorizedAgentByName,
    OwnedAgentByName,
    get_current_user,
)
from models import (
    CoordinationResourceAttach,
    CoordinationRun,
    CoordinationRunCreate,
    CoordinationRunDetail,
    CoordinationRunResource,
    CoordinationRunStatus,
    CoordinationRunUpdate,
    User,
)


router = APIRouter(prefix="/api/agents/{agent_name}/coordination-runs", tags=["coordination-runs"])


def _assert_agent_self_mutation(current_user: User, agent_name: str) -> None:
    """An agent-scoped credential may mutate only its own coordination runs."""
    if current_user.agent_name and current_user.agent_name != agent_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agent-scoped key may only mutate its own coordination runs",
        )


def _owned_run_or_404(run_id: str, agent_name: str) -> dict:
    run = db.get_coordination_run(run_id)
    if not run or run["owner_agent"] != agent_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordination run not found",
        )
    return run


def _resource_agent(resource_type: str, resource_id: str) -> str | None:
    if resource_type == "execution":
        resource = db.get_execution(resource_id)
    else:
        resource = db.get_operator_queue_item(resource_id)
    if not resource:
        return None
    if isinstance(resource, dict):
        return resource.get("agent_name")
    return getattr(resource, "agent_name", None)


def _assert_resource_accessible(
    resource_type: str,
    resource_id: str,
    current_user: User,
) -> None:
    resource_agent = _resource_agent(resource_type, resource_id)
    if not resource_agent or not db.can_user_access_agent(
        current_user.username, resource_agent
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )


@router.post("", response_model=CoordinationRun, status_code=201)
async def create_coordination_run(
    data: CoordinationRunCreate,
    agent_name: OwnedAgentByName,
    current_user: User = Depends(get_current_user),
):
    _assert_agent_self_mutation(current_user, agent_name)
    if data.root_execution_id:
        _assert_resource_accessible(
            "execution", data.root_execution_id, current_user
        )
    actor = (
        f"agent:{current_user.agent_name}"
        if current_user.agent_name
        else f"user:{current_user.id}"
    )
    return db.create_coordination_run(
        owner_agent=agent_name,
        outcome=data.outcome,
        root_execution_id=data.root_execution_id,
        context=data.context,
        created_by=actor,
    )


@router.get("", response_model=list[CoordinationRun])
async def list_coordination_runs(
    agent_name: AuthorizedAgentByName,
    run_status: CoordinationRunStatus | None = Query(None, alias="status"),
    limit: int = Query(100, ge=1, le=500),
):
    return db.list_coordination_runs(
        agent_name, status=run_status, limit=limit
    )


@router.get("/{run_id}", response_model=CoordinationRunDetail)
async def get_coordination_run(
    run_id: str,
    agent_name: AuthorizedAgentByName,
):
    run = _owned_run_or_404(run_id, agent_name)
    return {**run, "resources": db.list_coordination_resources(run_id)}


@router.patch("/{run_id}", response_model=CoordinationRun)
async def update_coordination_run(
    run_id: str,
    data: CoordinationRunUpdate,
    agent_name: OwnedAgentByName,
    current_user: User = Depends(get_current_user),
):
    _assert_agent_self_mutation(current_user, agent_name)
    _owned_run_or_404(run_id, agent_name)
    changes = data.model_dump(exclude={"expected_version"}, exclude_unset=True)
    updated = db.update_coordination_run(
        run_id,
        expected_version=data.expected_version,
        **changes,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Coordination run version conflict",
        )
    return updated


@router.post(
    "/{run_id}/resources",
    response_model=CoordinationRunResource,
    status_code=201,
)
async def attach_coordination_resource(
    run_id: str,
    data: CoordinationResourceAttach,
    agent_name: OwnedAgentByName,
    current_user: User = Depends(get_current_user),
):
    _assert_agent_self_mutation(current_user, agent_name)
    _owned_run_or_404(run_id, agent_name)
    _assert_resource_accessible(
        data.resource_type, data.resource_id, current_user
    )
    attached = db.attach_coordination_resource(
        run_id, data.resource_type, data.resource_id, data.role
    )
    if not attached:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordination run not found",
        )
    return attached
