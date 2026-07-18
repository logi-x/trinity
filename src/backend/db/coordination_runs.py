"""Durable correlation records for cross-agent business work.

Coordination runs deliberately store only generic lifecycle, opaque context,
and links to resources owned by other Trinity subsystems. Execution output,
logs, cost, and agent-defined pipeline transitions remain in their existing
systems of record.
"""

from __future__ import annotations

import json
import secrets
from typing import Any, Optional

from sqlalchemy import and_, insert, or_, select, update

from .engine import get_engine
from .tables import coordination_run_resources, coordination_runs
from utils.helpers import utc_now_iso


_CLOSED_STATUSES = {"completed", "cancelled"}
_UNSET = object()


def _insert_resource_on_conflict_do_nothing(conn, values):
    """Dialect-local upsert keeps concurrent attachment idempotent."""
    if conn.dialect.name == "sqlite":
        from sqlalchemy.dialects.sqlite import insert as dialect_insert
    else:
        from sqlalchemy.dialects.postgresql import insert as dialect_insert
    return dialect_insert(coordination_run_resources).values(**values).on_conflict_do_nothing(
        index_elements=["run_id", "resource_type", "resource_id"]
    )


class CoordinationRunOperations:
    """SQLAlchemy Core operations shared by SQLite and PostgreSQL."""

    @staticmethod
    def _decode_context(value: Optional[str]) -> Optional[dict[str, Any]]:
        return json.loads(value) if value is not None else None

    @classmethod
    def _run_to_dict(cls, row) -> dict[str, Any]:
        data = dict(row._mapping)
        data["context"] = cls._decode_context(data["context"])
        return data

    @staticmethod
    def _resource_to_dict(row) -> dict[str, Any]:
        return dict(row._mapping)

    def create_run(
        self,
        *,
        owner_agent: str,
        outcome: str,
        root_execution_id: Optional[str],
        context: Optional[dict[str, Any]],
        created_by: str,
    ) -> dict[str, Any]:
        run_id = f"cr_{secrets.token_urlsafe(12)}"
        now = utc_now_iso()
        values = {
            "id": run_id,
            "owner_agent": owner_agent,
            "root_execution_id": root_execution_id,
            "outcome": outcome,
            "status": "active",
            "context": (
                json.dumps(context, separators=(",", ":"))
                if context is not None
                else None
            ),
            "version": 1,
            "created_by": created_by,
            "created_at": now,
            "updated_at": now,
            "closed_at": None,
        }

        with get_engine().begin() as conn:
            conn.execute(insert(coordination_runs).values(**values))
            if root_execution_id:
                conn.execute(
                    insert(coordination_run_resources).values(
                        run_id=run_id,
                        resource_type="execution",
                        resource_id=root_execution_id,
                        role="root",
                        created_at=now,
                        notified_status=None,
                        notified_at=None,
                    )
                )

        values["context"] = context
        return values

    def get_run(self, run_id: str) -> Optional[dict[str, Any]]:
        with get_engine().connect() as conn:
            row = conn.execute(
                select(coordination_runs).where(coordination_runs.c.id == run_id)
            ).first()
        return self._run_to_dict(row) if row else None

    def list_runs(
        self,
        owner_agent: str,
        *,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        stmt = select(coordination_runs).where(
            coordination_runs.c.owner_agent == owner_agent
        )
        if status is not None:
            stmt = stmt.where(coordination_runs.c.status == status)
        stmt = stmt.order_by(coordination_runs.c.updated_at.desc()).limit(limit)
        with get_engine().connect() as conn:
            rows = conn.execute(stmt).all()
        return [self._run_to_dict(row) for row in rows]

    def update_run(
        self,
        run_id: str,
        *,
        expected_version: int,
        status: Optional[str] = None,
        context: Any = _UNSET,
        outcome: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        values: dict[str, Any] = {
            "version": expected_version + 1,
            "updated_at": utc_now_iso(),
        }
        if status is not None:
            values["status"] = status
            values["closed_at"] = (
                values["updated_at"] if status in _CLOSED_STATUSES else None
            )
        if context is not _UNSET:
            values["context"] = (
                json.dumps(context, separators=(",", ":"))
                if context is not None
                else None
            )
        if outcome is not None:
            values["outcome"] = outcome

        with get_engine().begin() as conn:
            result = conn.execute(
                update(coordination_runs)
                .where(
                    and_(
                        coordination_runs.c.id == run_id,
                        coordination_runs.c.version == expected_version,
                    )
                )
                .values(**values)
            )
            if result.rowcount != 1:
                return None
            row = conn.execute(
                select(coordination_runs).where(coordination_runs.c.id == run_id)
            ).first()
        return self._run_to_dict(row)

    def attach_resource(
        self,
        run_id: str,
        resource_type: str,
        resource_id: str,
        role: str,
    ) -> Optional[dict[str, Any]]:
        now = utc_now_iso()
        table = coordination_run_resources

        with get_engine().begin() as conn:
            existing = conn.execute(
                select(table).where(
                    and_(
                        table.c.run_id == run_id,
                        table.c.resource_type == resource_type,
                        table.c.resource_id == resource_id,
                    )
                )
            ).first()
            if existing:
                return self._resource_to_dict(existing)

            run_exists = conn.execute(
                select(coordination_runs.c.id).where(
                    coordination_runs.c.id == run_id
                )
            ).first()
            if not run_exists:
                return None

            conn.execute(
                _insert_resource_on_conflict_do_nothing(
                    conn,
                    {
                        "run_id": run_id,
                        "resource_type": resource_type,
                        "resource_id": resource_id,
                        "role": role,
                        "created_at": now,
                        "notified_status": None,
                        "notified_at": None,
                    },
                )
            )
            row = conn.execute(
                select(table).where(
                    and_(
                        table.c.run_id == run_id,
                        table.c.resource_type == resource_type,
                        table.c.resource_id == resource_id,
                    )
                )
            ).first()
        return self._resource_to_dict(row)

    def list_resources(self, run_id: str) -> list[dict[str, Any]]:
        with get_engine().connect() as conn:
            rows = conn.execute(
                select(coordination_run_resources)
                .where(coordination_run_resources.c.run_id == run_id)
                .order_by(coordination_run_resources.c.created_at)
            ).all()
        return [self._resource_to_dict(row) for row in rows]

    def claim_terminal_notifications(
        self,
        resource_type: str,
        resource_id: str,
        status: str,
    ) -> list[dict[str, Any]]:
        """Atomically claim each linked run once for a terminal status.

        A corrected terminal status may be emitted once again. Replays of the
        same status are ignored.
        """
        table = coordination_run_resources
        now = utc_now_iso()
        claimed: list[dict[str, Any]] = []

        with get_engine().begin() as conn:
            candidates = conn.execute(
                select(
                    table.c.run_id,
                    table.c.resource_type,
                    table.c.resource_id,
                    table.c.role,
                    coordination_runs.c.owner_agent,
                )
                .join(coordination_runs, coordination_runs.c.id == table.c.run_id)
                .where(
                    and_(
                        table.c.resource_type == resource_type,
                        table.c.resource_id == resource_id,
                        or_(
                            table.c.notified_status.is_(None),
                            table.c.notified_status != status,
                        ),
                    )
                )
            ).all()

            for candidate in candidates:
                result = conn.execute(
                    update(table)
                    .where(
                        and_(
                            table.c.run_id == candidate.run_id,
                            table.c.resource_type == resource_type,
                            table.c.resource_id == resource_id,
                            or_(
                                table.c.notified_status.is_(None),
                                table.c.notified_status != status,
                            ),
                        )
                    )
                    .values(notified_status=status, notified_at=now)
                )
                if result.rowcount == 1:
                    claimed.append(dict(candidate._mapping))

        return claimed

    def release_terminal_notification(
        self,
        run_id: str,
        resource_type: str,
        resource_id: str,
        status: str,
    ) -> bool:
        """Release a claim when its durable event could not be persisted."""
        table = coordination_run_resources
        with get_engine().begin() as conn:
            result = conn.execute(
                update(table)
                .where(
                    and_(
                        table.c.run_id == run_id,
                        table.c.resource_type == resource_type,
                        table.c.resource_id == resource_id,
                        table.c.notified_status == status,
                    )
                )
                .values(notified_status=None, notified_at=None)
            )
        return result.rowcount == 1
