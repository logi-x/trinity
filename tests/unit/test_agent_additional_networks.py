"""Security and lifecycle contract for AGENT-NETWORKS-001."""

import json
import sqlite3
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from models import AgentConfig
from services.agent_service.networks import (
    ADDITIONAL_NETWORKS_LABEL,
    connect_additional_networks,
    additional_networks_match,
    parse_additional_networks_label,
    validate_additional_networks,
)
from services.template_service import _build_local_template, _build_template


def test_agent_config_defaults_to_no_additional_networks():
    assert AgentConfig(name="plain").additional_networks == []


def test_github_template_surface_preserves_additional_networks():
    template = _build_template(
        "example/project",
        {"additional_networks": ["project-network"]},
    )

    assert template["additional_networks"] == ["project-network"]


def test_local_template_surface_preserves_additional_networks(tmp_path):
    template_dir = tmp_path / "project"
    template_dir.mkdir()
    (template_dir / "template.yaml").write_text(
        "name: project\nadditional_networks:\n  - project-network\n"
    )

    template = _build_local_template(template_dir)

    assert template["additional_networks"] == ["project-network"]


def test_validate_accepts_explicitly_allowlisted_networks(monkeypatch):
    monkeypatch.setenv(
        "AGENT_ADDITIONAL_NETWORK_ALLOWLIST",
        "howa-shared-network, experts-shared-network",
    )

    assert validate_additional_networks(
        ["howa-shared-network", "experts-shared-network"]
    ) == ["howa-shared-network", "experts-shared-network"]


@pytest.mark.parametrize(
    "network",
    ["bridge", "host", "none", "trinity-agent-network", "trinity-platform-network"],
)
def test_validate_rejects_reserved_networks_even_if_allowlisted(monkeypatch, network):
    monkeypatch.setenv("AGENT_ADDITIONAL_NETWORK_ALLOWLIST", network)

    with pytest.raises(HTTPException) as exc:
        validate_additional_networks([network])

    assert exc.value.status_code == 400
    assert exc.value.detail["code"] == "ADDITIONAL_NETWORK_FORBIDDEN"


def test_validate_rejects_network_not_in_operator_allowlist(monkeypatch):
    monkeypatch.setenv("AGENT_ADDITIONAL_NETWORK_ALLOWLIST", "approved-network")

    with pytest.raises(HTTPException) as exc:
        validate_additional_networks(["unapproved-network"])

    assert exc.value.status_code == 403
    assert exc.value.detail["code"] == "ADDITIONAL_NETWORK_NOT_ALLOWED"


def test_validate_rejects_duplicates(monkeypatch):
    monkeypatch.setenv("AGENT_ADDITIONAL_NETWORK_ALLOWLIST", "project-network")

    with pytest.raises(HTTPException) as exc:
        validate_additional_networks(["project-network", "project-network"])

    assert exc.value.status_code == 400
    assert exc.value.detail["code"] == "ADDITIONAL_NETWORK_DUPLICATE"


def test_label_round_trip_is_stable(monkeypatch):
    monkeypatch.setenv("AGENT_ADDITIONAL_NETWORK_ALLOWLIST", "b-network,a-network")
    desired = validate_additional_networks(["b-network", "a-network"])
    label = json.dumps(desired, separators=(",", ":"))

    assert parse_additional_networks_label({ADDITIONAL_NETWORKS_LABEL: label}) == desired


def test_match_compares_actual_external_attachments():
    container = MagicMock()
    container.attrs = {
        "NetworkSettings": {
            "Networks": {
                "trinity-agent-network": {},
                "project-network": {},
            }
        }
    }

    assert additional_networks_match(container, ["project-network"])
    assert not additional_networks_match(container, [])


@pytest.mark.asyncio
async def test_connect_preflights_every_network_before_connecting(monkeypatch):
    monkeypatch.setenv("AGENT_ADDITIONAL_NETWORK_ALLOWLIST", "one,two")
    container = MagicMock()
    one = MagicMock()
    two = MagicMock()
    get_network = AsyncMock(side_effect=[one, two])
    connect_network = AsyncMock()

    await connect_additional_networks(
        container,
        ["one", "two"],
        network_getter=get_network,
        network_connector=connect_network,
    )

    assert get_network.await_args_list[0].args == ("one",)
    assert get_network.await_args_list[1].args == ("two",)
    assert connect_network.await_args_list[0].args == (one, container)
    assert connect_network.await_args_list[1].args == (two, container)


def test_networks_mixin_round_trip(tmp_path, monkeypatch):
    db_path = tmp_path / "trinity.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE agent_ownership (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT UNIQUE NOT NULL,
            owner_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            additional_networks TEXT,
            deleted_at TEXT
        )
        """
    )
    conn.execute(
        "INSERT INTO agent_ownership (agent_name, owner_id, created_at) "
        "VALUES ('atlas', 1, 'now')"
    )
    conn.commit()
    conn.close()

    import db.engine as engine_mod
    from db.agent_settings.networks import NetworksMixin

    engine_mod.dispose_engines()
    try:
        mixin = NetworksMixin()
        assert mixin.get_additional_networks("atlas") == []
        assert mixin.set_additional_networks("atlas", ["project-network"])
        assert mixin.get_additional_networks("atlas") == ["project-network"]
        assert mixin.set_additional_networks("atlas", [])
        assert mixin.get_additional_networks("atlas") == []
    finally:
        engine_mod.dispose_engines()
