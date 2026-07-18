"""Central persistence facades notify linked coordination resources."""

from unittest.mock import MagicMock, patch

import pytest

pytestmark = pytest.mark.unit


def _manager():
    from database import DatabaseManager

    manager = DatabaseManager.__new__(DatabaseManager)
    manager._schedule_ops = MagicMock()
    manager._operator_queue_ops = MagicMock()
    return manager


def test_execution_terminal_notifies_only_when_cas_wins():
    manager = _manager()
    manager._schedule_ops.update_execution_status.side_effect = [True, False]

    with patch("database._schedule_coordination_terminal") as notify:
        assert manager.update_execution_status("exec-1", "success") is True
        assert manager.update_execution_status("exec-1", "failed") is False

    notify.assert_called_once_with(manager, "execution", "exec-1", "success")


def test_operator_response_notifies_after_successful_transition():
    manager = _manager()
    manager._operator_queue_ops.respond_to_item.return_value = {
        "id": "opq-1",
        "status": "responded",
    }

    with patch("database._schedule_coordination_terminal") as notify:
        item = manager.respond_to_operator_queue_item(
            "opq-1", "approve", None, "7", "owner@example.com"
        )

    assert item["status"] == "responded"
    notify.assert_called_once_with(
        manager, "operator_queue", "opq-1", "responded"
    )


def test_expiry_notifies_each_row_won_by_update():
    manager = _manager()
    manager._operator_queue_ops.mark_expired_item_ids.return_value = [
        "opq-1",
        "opq-2",
    ]

    with patch("database._schedule_coordination_terminal") as notify:
        count = manager.mark_operator_queue_expired()

    assert count == 2
    assert notify.call_count == 2
