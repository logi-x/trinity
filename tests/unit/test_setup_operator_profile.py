"""trinity-enterprise#38 / #82 Phase 1 — first-run operator profile capture.

The setup endpoint optionally registers the admin email (sign-in identity) and,
only on affirmative consent + a valid email, schedules the fire-and-forget
intake as a background task. None of it may block or break setup.
"""
import asyncio

import pytest
from fastapi import BackgroundTasks, HTTPException

pytestmark = pytest.mark.unit

import routers.setup as setup


class FakeDB:
    def __init__(self):
        self.settings = {"setup_completed": "false"}
        self.users = {}

    def get_setting_value(self, key, default=None):
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value

    def update_user_password(self, username, hashed):
        self.users.setdefault(username, {"username": username, "email": username})["password"] = hashed
        return True

    def update_user(self, username, updates):
        self.users.setdefault(username, {"username": username}).update(updates)
        return self.users[username]


PW = "Sup3rSecret!!"


@pytest.fixture
def patched(monkeypatch):
    db = FakeDB()
    monkeypatch.setattr(setup, "db", db)
    monkeypatch.setattr(setup, "ensure_setup_token", lambda: "tok")
    monkeypatch.setattr(setup, "clear_setup_token", lambda: None)
    monkeypatch.setattr(setup, "validate_password_strength", lambda p: [])
    monkeypatch.setattr(setup, "hash_password", lambda p: "hashed:" + p)
    return db


def _req(**kw):
    return setup.SetAdminPasswordRequest(
        password=PW, confirm_password=PW, setup_token="tok", **kw
    )


def _run(data, bg):
    # request arg is unused by the handler body.
    return asyncio.run(setup.set_admin_password(data, None, bg))


def test_email_registered_and_intake_scheduled(patched):
    bg = BackgroundTasks()
    res = _run(_req(email="Me@Acme.com", company="Acme", consent_updates=True), bg)

    assert res["email_registered"] is True
    assert patched.users["admin"]["email"] == "me@acme.com"  # normalized
    assert patched.settings["setup_completed"] == "true"
    assert len(bg.tasks) == 1  # intake scheduled (runs after response)


def test_consent_without_email_does_not_schedule(patched):
    bg = BackgroundTasks()
    res = _run(_req(consent_updates=True), bg)

    assert res["email_registered"] is False
    assert len(bg.tasks) == 0
    assert patched.settings["setup_completed"] == "true"


def test_email_without_consent_registers_but_no_intake(patched):
    bg = BackgroundTasks()
    res = _run(_req(email="me@acme.com", consent_updates=False), bg)

    assert res["email_registered"] is True
    assert patched.users["admin"]["email"] == "me@acme.com"
    assert len(bg.tasks) == 0


def test_invalid_email_rejected_before_any_write(patched):
    bg = BackgroundTasks()
    with pytest.raises(HTTPException) as ei:
        _run(_req(email="not-an-email", consent_updates=True), bg)

    assert ei.value.status_code == 400
    # Validated before writes — setup not marked complete, no admin email written.
    assert patched.settings["setup_completed"] == "false"
    assert len(bg.tasks) == 0


def test_no_profile_completes_setup_cleanly(patched):
    bg = BackgroundTasks()
    res = _run(_req(), bg)

    assert res["email_registered"] is False
    assert patched.settings["setup_completed"] == "true"
    assert len(bg.tasks) == 0
