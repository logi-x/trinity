# Trinity Enterprise Modules — Installation & Verification

Trinity is open-core. The open-source platform in this repository is complete
and fully functional on its own. Customers with an enterprise agreement
additionally receive access to a **private companion repository**
(`Abilityai/trinity-enterprise`) that mounts into this repo as an **optional
git submodule** at `src/backend/enterprise/`.

This document covers the *generic installation mechanism only*: how the
optional submodule mounts, how the backend detects it, and how to verify which
edition an instance is running. The catalog of enterprise capabilities and
their designs are documented privately in the enterprise repository.

## How the seam works

- `src/backend/main.py` wraps the enterprise loader in a conditional import:
  if the submodule is present, `register_enterprise(app)` runs and each
  enterprise module registers itself with the entitlement registry
  (`services/entitlement_service.py`); if the submodule is absent, the
  `ImportError` is caught and the platform runs **OSS-only** — this is normal,
  not an error.
- Registration state drives two API surfaces (same source, never divergent):
  - `GET /api/settings/feature-flags` → `enterprise_features: [...]` (empty
    list in OSS-only builds)
  - `GET /api/version` → `edition: "oss" | "enterprise"` plus the same
    `enterprise_features` list (#1443)
- A **bug** during enterprise registration never takes down the platform: the
  backend logs `Trinity Enterprise registration FAILED — continuing OSS-only`
  and boots with whatever registered before the failure (possibly nothing).

## OSS installs: nothing to do

The submodule entry in `.gitmodules` sets `update = none`, so:

```bash
git clone --recurse-submodules https://github.com/abilityai/trinity.git   # OK
# or
git clone https://github.com/abilityai/trinity.git
cd trinity
git submodule update --init --recursive                                   # OK — prints "Skipping submodule"
```

both complete **without credentials**. The `src/backend/enterprise/` directory
stays empty and the backend boots OSS-only, logging:

```
Trinity Enterprise submodule not present — OSS-only build (this is normal; enterprise modules are an optional private submodule)
```

## Mounting the enterprise submodule (entitled customers)

> `update = none` means git skips this submodule on *every* plain
> `git submodule update`, including `--init` — and a one-shot
> `--init --checkout` copies `none` into your local config, so later updates
> would silently skip again. Set the local override **first**; it is durable.

### 1. Set the durable local override

```bash
git config submodule.src/backend/enterprise.update checkout
```

### 2. Choose an auth transport

**Option A — SSH (default URL in `.gitmodules`):** ensure your SSH key has
read access to the private repository, then initialize:

```bash
git submodule update --init src/backend/enterprise
```

**Option B — HTTPS with a personal access token** (CI hosts, servers without
SSH keys): override the submodule URL locally, then initialize:

```bash
git config submodule.src/backend/enterprise.url \
  "https://x-access-token:<YOUR_GITHUB_PAT>@github.com/Abilityai/trinity-enterprise.git"
git submodule update --init src/backend/enterprise
```

The URL override lives only in your clone's `.git/config` — never commit a
token anywhere. Prefer a credential helper over embedding the token in the URL
where possible.

### 3. Rebuild and restart the backend

The backend image copies the source tree at build time, so mounting the
submodule requires a rebuild:

```bash
docker-compose build backend
./scripts/deploy/start.sh
```

### 4. Verify

```bash
# Boot log — one line per outcome:
docker logs trinity-backend 2>&1 | grep "Trinity Enterprise"
#   "Trinity Enterprise modules registered"            → enterprise active
#   "Trinity Enterprise submodule not present …"       → OSS-only
#   "Trinity Enterprise registration FAILED …"         → degraded to OSS-only (see traceback above it)

# API (any authenticated user):
curl -s -H "Authorization: Bearer <token>" http://localhost:8000/api/version
#   → { "edition": "enterprise", "enterprise_features": ["..."], ... }
```

### Keeping it updated

With the step-1 override in place, routine updates just work:

```bash
git pull
git submodule update --init --recursive
```

**Existing clones (mounted before #1443):** the `update = none` default
applies to your clone too — plain `git submodule update` starts *skipping*
the enterprise submodule (exit 0, working tree left stale). Run the step-1
`git config` line once to restore normal syncing.

## Forcing OSS-only mode

`TRINITY_OSS_ONLY=1` (backend environment) empties the entitlement registry
even when the submodule is mounted — every enterprise feature reports
not-entitled, `enterprise_features` returns `[]`, and `edition` reports
`"oss"`. Useful for compliance lockdowns and for CI that exercises the
OSS-only path (`.github/workflows/build-without-submodule.yml`).

## For maintainers: the `.claude` submodule

The dev-tooling submodule at `.claude/` (skills, methodology guides) is also
private and also `update = none`, so OSS clones skip it too. Core-team setup
is documented in `CLAUDE.md` → "Development Skills". External contributors
don't need it — the public
[abilities](https://github.com/abilityai/abilities) marketplace ships the
`dev-methodology` plugin with the equivalent workflow skills.
