"""Regression tests for bounded, non-blocking agent file listings."""

import asyncio
import importlib.util
import time
from pathlib import Path

import pytest


_FILES_PY = (
    Path(__file__).resolve().parents[2]
    / "docker"
    / "base-image"
    / "agent_server"
    / "routers"
    / "files.py"
)


def _load_files_module():
    spec = importlib.util.spec_from_file_location("agent_files_scalability", _FILES_PY)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_directory_listing_is_shallow_and_paginated(tmp_path):
    files = _load_files_module()
    (tmp_path / "alpha").mkdir()
    (tmp_path / "alpha" / "nested.txt").write_text("nested")
    (tmp_path / "beta").mkdir()
    (tmp_path / "one.txt").write_text("one")
    (tmp_path / "two.txt").write_text("two")

    first = files._list_directory_page(tmp_path, tmp_path, False, 0, 2)
    second = files._list_directory_page(tmp_path, tmp_path, False, 2, 2)

    assert [item["name"] for item in first["tree"]] == ["alpha", "beta"]
    assert first["tree"][0]["children"] == []
    assert first["tree"][0]["children_loaded"] is False
    assert first["has_more"] is True
    assert first["next_offset"] == 2
    assert [item["name"] for item in second["tree"]] == ["one.txt", "two.txt"]
    assert second["has_more"] is False
    assert second["next_offset"] is None
    assert first["total_entries"] == 4


def test_list_files_runs_filesystem_scan_off_event_loop(tmp_path, monkeypatch):
    files = _load_files_module()
    monkeypatch.setattr(files, "WORKSPACE_ROOT", tmp_path)

    def slow_listing(*args, **kwargs):
        time.sleep(0.15)
        return {
            "tree": [],
            "total_files": 0,
            "total_entries": 0,
            "offset": 0,
            "limit": 100,
            "has_more": False,
            "next_offset": None,
        }

    monkeypatch.setattr(files, "_list_directory_page", slow_listing)

    async def exercise():
        task = asyncio.create_task(files.list_files(path=str(tmp_path)))
        started = time.monotonic()
        await asyncio.sleep(0.02)
        event_loop_delay = time.monotonic() - started
        await task
        return event_loop_delay

    assert asyncio.run(exercise()) < 0.08


def test_workspace_prefix_sibling_is_rejected(tmp_path, monkeypatch):
    files = _load_files_module()
    workspace = tmp_path / "developer"
    sibling = tmp_path / "developer-evil"
    workspace.mkdir()
    sibling.mkdir()
    monkeypatch.setattr(files, "WORKSPACE_ROOT", workspace)

    with pytest.raises(files.HTTPException) as exc:
        asyncio.run(files.list_files(path=str(sibling)))

    assert exc.value.status_code == 403


def test_relative_directory_paths_resolve_from_workspace(tmp_path, monkeypatch):
    files = _load_files_module()
    workspace = tmp_path / "developer"
    child = workspace / "apps"
    child.mkdir(parents=True)
    (child / "app.py").write_text("print('ok')")
    monkeypatch.setattr(files, "WORKSPACE_ROOT", workspace)

    result = asyncio.run(files.list_files(path="apps"))

    assert result["requested_path"] == "apps"
    assert [item["name"] for item in result["tree"]] == ["app.py"]
