"""Per-agent additional Docker network settings (AGENT-NETWORKS-001)."""

import json
from typing import List

from sqlalchemy import select, update

from ..engine import get_engine
from ..tables import agent_ownership


class NetworksMixin:
    """Persist the desired external Docker networks as a JSON list."""

    def get_additional_networks(self, agent_name: str) -> List[str]:
        stmt = select(agent_ownership.c.additional_networks).where(
            (agent_ownership.c.agent_name == agent_name)
            & (agent_ownership.c.deleted_at.is_(None))
        )
        with get_engine().connect() as conn:
            row = conn.execute(stmt).mappings().first()
        if not row or not row["additional_networks"]:
            return []
        try:
            value = json.loads(row["additional_networks"])
        except (TypeError, ValueError):
            return []
        return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []

    def set_additional_networks(self, agent_name: str, networks: List[str]) -> bool:
        payload = json.dumps(networks, separators=(",", ":")) if networks else None
        stmt = (
            update(agent_ownership)
            .where(
                (agent_ownership.c.agent_name == agent_name)
                & (agent_ownership.c.deleted_at.is_(None))
            )
            .values(additional_networks=payload)
        )
        with get_engine().begin() as conn:
            result = conn.execute(stmt)
            return result.rowcount > 0
