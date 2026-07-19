"""Validation and Docker reconciliation for agent additional networks."""

import json
import os
import re
from typing import Awaitable, Callable, Iterable, List, Mapping

import docker
from fastapi import HTTPException

from services.docker_utils import network_connect, network_get


PRIMARY_AGENT_NETWORK = "trinity-agent-network"
ADDITIONAL_NETWORKS_LABEL = "trinity.additional-networks"
MAX_ADDITIONAL_NETWORKS = 8
_NETWORK_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
_FORBIDDEN_NETWORKS = {
    "bridge",
    "host",
    "none",
    PRIMARY_AGENT_NETWORK,
    "trinity-platform-network",
}


def _operator_allowlist() -> set[str]:
    raw = os.getenv("AGENT_ADDITIONAL_NETWORK_ALLOWLIST", "")
    return {item.strip() for item in raw.split(",") if item.strip()}


def validate_additional_networks(networks: Iterable[str] | None) -> List[str]:
    """Validate and normalize a requested per-agent network list.

    The operator allowlist defaults to empty, so network expansion is always
    opt-in. Reserved Docker/Trinity networks remain forbidden even if an
    operator accidentally includes one in the environment allowlist.
    """
    requested = list(networks or [])
    if len(requested) > MAX_ADDITIONAL_NETWORKS:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "ADDITIONAL_NETWORK_LIMIT",
                "error": f"At most {MAX_ADDITIONAL_NETWORKS} additional networks are allowed.",
            },
        )

    normalized: List[str] = []
    seen: set[str] = set()
    allowlist = _operator_allowlist()
    for raw_name in requested:
        name = raw_name.strip() if isinstance(raw_name, str) else ""
        if not name or not _NETWORK_NAME_RE.fullmatch(name):
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "ADDITIONAL_NETWORK_INVALID",
                    "error": "Additional network names must use Docker-safe name characters.",
                },
            )
        if name in _FORBIDDEN_NETWORKS:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "ADDITIONAL_NETWORK_FORBIDDEN",
                    "error": f"Docker network '{name}' cannot be used as an additional agent network.",
                },
            )
        if name in seen:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "ADDITIONAL_NETWORK_DUPLICATE",
                    "error": f"Docker network '{name}' was requested more than once.",
                },
            )
        if name not in allowlist:
            raise HTTPException(
                status_code=403,
                detail={
                    "code": "ADDITIONAL_NETWORK_NOT_ALLOWED",
                    "error": f"Docker network '{name}' is not in the operator allowlist.",
                },
            )
        seen.add(name)
        normalized.append(name)
    return normalized


def serialize_additional_networks_label(networks: Iterable[str]) -> str:
    return json.dumps(list(networks), separators=(",", ":"))


def parse_additional_networks_label(labels: Mapping[str, str] | None) -> List[str]:
    raw = (labels or {}).get(ADDITIONAL_NETWORKS_LABEL, "")
    if not raw:
        return []
    try:
        value = json.loads(raw)
    except (TypeError, ValueError):
        return []
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def attached_additional_networks(container) -> List[str]:
    networks = (
        container.attrs.get("NetworkSettings", {}).get("Networks", {})
        if container
        else {}
    )
    return sorted(name for name in networks if name != PRIMARY_AGENT_NETWORK)


def additional_networks_match(container, desired: Iterable[str]) -> bool:
    return attached_additional_networks(container) == sorted(desired)


async def preflight_additional_networks(
    networks: Iterable[str] | None,
    *,
    network_getter: Callable[[str], Awaitable[object]] = network_get,
) -> List[object]:
    """Validate every network and resolve all Docker objects before mutation."""
    desired = validate_additional_networks(networks)
    resolved = []
    for name in desired:
        try:
            resolved.append(await network_getter(name))
        except docker.errors.NotFound as exc:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "ADDITIONAL_NETWORK_NOT_FOUND",
                    "error": f"Docker network '{name}' does not exist.",
                },
            ) from exc
    return resolved


async def connect_additional_networks(
    container,
    networks: Iterable[str] | None,
    *,
    network_getter: Callable[[str], Awaitable[object]] = network_get,
    network_connector: Callable[[object, object], Awaitable[None]] = network_connect,
) -> List[str]:
    """Preflight, then attach a container to every approved network."""
    desired = validate_additional_networks(networks)
    resolved = await preflight_additional_networks(
        desired,
        network_getter=network_getter,
    )
    for network in resolved:
        await network_connector(network, container)
    return desired
