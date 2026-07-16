#!/usr/bin/env python3
"""Reconcile the live agent permission graph to a system manifest's explicit map.

The manifest is declared truth; this is the only writer of the live graph. We do not
re-deploy the system to apply permissions, because a redeploy may duplicate running agents.

Usage:
    python scripts/reconcile-permissions.py --manifest config/manifests/logix-consulting.yaml [--apply]

Without --apply it prints the delta and exits non-zero if the graph differs.
"""
import argparse
import os
import sys

import requests
import yaml

BASE = os.environ.get("TRINITY_URL", "http://localhost:8000")
# Agents exempt from reconciliation: ops orchestrator, managed out of band.
EXEMPT_SOURCES = {"logix-system"}


def token() -> str:
    r = requests.post(
        f"{BASE}/api/token",
        data={
            "username": os.environ["ADMIN_USERNAME"],
            "password": os.environ["ADMIN_PASSWORD"],
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def desired(manifest_path: str) -> dict[str, set[str]]:
    m = yaml.safe_load(open(manifest_path))
    system = m["name"]
    members = set(m["agents"])
    out: dict[str, set[str]] = {}

    def final(short: str) -> str:
        # Manifest members are prefixed with the system name at deploy; anything
        # else is already a deployed agent name (e.g. logix-cornelius).
        return f"{system}-{short}" if short in members else short

    for source, targets in m["permissions"]["explicit"].items():
        out[final(source)] = {final(t) for t in targets}
    return out


def live(tok: str) -> dict[str, set[str]]:
    r = requests.get(
        f"{BASE}/api/agents/permissions-edges",
        headers={"Authorization": f"Bearer {tok}"},
        timeout=30,
    )
    r.raise_for_status()
    out: dict[str, set[str]] = {}
    for e in r.json()["edges"]:
        out.setdefault(e["source"], set()).add(e["target"])
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    tok = token()
    want = desired(args.manifest)
    have = live(tok)

    add, remove = [], []
    for source in sorted(set(want) | set(have)):
        if source in EXEMPT_SOURCES:
            continue
        if source not in want:
            continue  # not ours to manage
        for t in sorted(want[source] - have.get(source, set())):
            add.append((source, t))
        for t in sorted(have.get(source, set()) - want[source]):
            remove.append((source, t))

    for s, t in add:
        print(f"+ {s} -> {t}")
    for s, t in remove:
        print(f"- {s} -> {t}")
    if not add and not remove:
        print("in sync")
        return 0

    if not args.apply:
        print(f"\n{len(add)} to add, {len(remove)} to remove. Re-run with --apply.")
        return 1

    h = {"Authorization": f"Bearer {tok}"}
    for s, t in add:
        r = requests.post(f"{BASE}/api/agents/{s}/permissions/{t}", headers=h, timeout=30)
        r.raise_for_status()
        print(f"added {s} -> {t}")
    for s, t in remove:
        r = requests.delete(f"{BASE}/api/agents/{s}/permissions/{t}", headers=h, timeout=30)
        r.raise_for_status()
        print(f"removed {s} -> {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
