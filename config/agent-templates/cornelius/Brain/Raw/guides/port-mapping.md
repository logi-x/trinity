---
title: "Port Mapping — Guide"
date: "2026-06-19"
source: "draft"
tags: [project/experts, guide, port-mapping]
category: "guide"
---

# Port Mapping

## TL;DR

Three environments, three **serving topologies** — not just three port numbers:

| Env     | Runs on      | Local bind   | Public URL                 | Served by                          |
| ------- | ------------ | ------------ | -------------------------- | ---------------------------------- |
| **dev** | your machine | `127.0.0.1`  | none — local only          | direct `http://127.0.0.1:PORT`     |
| **stg** | your machine | `127.0.0.1`  | `app.stg.<domain>`         | **SSH reverse tunnel → VPS Traefik** |
| **prd** | the VPS      | internal net | `<domain>`                 | VPS Traefik, directly (`:443`)     |

Two rules:

1. **Local is numeric.** Everything that runs on your machine (`dev` + `stg`) gets a deterministic `127.0.0.1:PORT` from the formula. No local proxy.
2. **The VPS does hostnames.** Traefik on the VPS routes by hostname — for `prd` directly, and for `stg` by reaching back down your SSH tunnel.

The source of truth is the **project-ID registry**. Everything derives from it; two projects can never collide.

---

## Registries (the source of truth)

### Projects

| ID    | Project            | Slug      | Envs            |
| ----- | ------------------ | --------- | --------------- |
| `01`  | Logix App          | `logix`   | dev, prd        |
| `02`  | Experts            | `experts` | dev, stg, prd   |
| `03`  | HOWA               | `howa`    | dev, prd        |
| `04`  | Logix Intelligence | `lucy`    | dev, prd        |
| `05`  | n8n-core           | `n8n`     | dev, prd        |
| `06`  | mcp-core           | `mcp`     | dev, prd        |
| `07`+ | _reserved_         | —         | —               |

`PROJECT_ID` is the numeric id with its leading zero dropped (`01` → `1`). The **slug** is the VPS hostname label. `stg` exists only for projects you publicly stage over a tunnel — add it to a project's **Envs** when you do.

### Environments

| ID  | Env | Allocated a local port? | Public                        |
| --- | --- | ----------------------- | ----------------------------- |
| `1` | dev | yes (`127.0.0.1`)       | no                            |
| `2` | stg | yes (`127.0.0.1`)       | yes, via tunnel → VPS Traefik |
| `3` | prd | no — runs on the VPS    | yes, VPS Traefik `:443`       |

> `canary` and `test` are retired. Only `dev` and `stg` ever consume a local port (they co-reside on your machine); `prd` lives on its own host and uses `:443`, so `ENV_ID 3` is conceptual — never a local port.

### Service bases (local ports)

| Service            |    Base |
| ------------------ | ------: |
| Web                | `30000` |
| API                | `31000` |
| Realtime / WS      | `32000` |
| Postgres           | `15000` |
| Redis              | `16000` |
| MySQL              | `13000` |

Thousands-aligned, no decorative digits. `prd` has no base — it's hostname-routed on the VPS.

---

## The formula (local ports)

```
HOST_PORT = SERVICE_BASE + PROJECT_ID*10 + ENV_ID        (ENV_ID: dev=1, stg=2)
```

The `*10 + ENV_ID` suffix is unique for up to 9 projects × the local envs; bases are ≥1000 apart, so services never overlap.

### Worked example — Experts (`02`, has all three envs)

| Service       | dev (`…1`) | stg (`…2`) | prd                         |
| ------------- | ---------: | ---------: | --------------------------- |
| Web           |    `30021` |    `30022` | `experts.com.sa` (`:443`)   |
| API           |    `31021` |    `31022` | `api.experts.com.sa`        |
| Realtime / WS |    `32021` |    `32022` | `ws.experts.com.sa`         |
| Postgres      |    `15021` |    `15022` | internal (VPS, not exposed) |
| Redis         |    `16021` |    `16022` | internal (VPS, not exposed) |

### Simpler example — Logix App (`01`, dev + prd, no stg)

| Service  | dev     | prd                     |
| -------- | ------: | ----------------------- |
| Web      | `30011` | `logi-x.org` (`:443`)   |
| API      | `31011` | `api.logi-x.org`        |
| Postgres | `15011` | internal (VPS)          |

No `stg` row — Logix isn't tunnel-staged.

---

## dev — pure localhost

Bind published ports to `127.0.0.1` explicitly (never `0.0.0.0`), so dev is unreachable from the network. Reach services directly by port.

```yaml
services:
  web:
    ports:
      - "127.0.0.1:30021:3000"   # 30000 + 02*10 + dev(1)  → http://127.0.0.1:30021
  api:
    ports:
      - "127.0.0.1:31021:4000"
  postgres:
    ports:
      - "127.0.0.1:15021:5432"   # attach with TablePlus → 127.0.0.1:15021
```

No proxy, no hostnames — just `127.0.0.1:<port>`.

---

## stg — local Docker, exposed via SSH reverse tunnel

`stg` runs on your machine exactly like dev (bound to `127.0.0.1`, `ENV_ID 2` ports), then a reverse tunnel hands its HTTP entrypoints to the VPS, where Traefik serves them under a public hostname.

### 1. The tunnel (reuse the local port number on both ends)

```bash
ssh -N \
  -R 172.17.0.1:30022:127.0.0.1:30022 \   # experts stg web
  -R 172.17.0.1:31022:127.0.0.1:31022 \   # experts stg api (only if served publicly)
  experts
```

- `-R 172.17.0.1:30022:127.0.0.1:30022` → bind `172.17.0.1:30022` on the **VPS** (docker0's gateway, reachable by the Traefik *container*), forwarding back to `127.0.0.1:30022` on **your machine**.
- **Same number both ends** — no separate VPS port registry to maintain.
- Tunnel only the HTTP entrypoints Traefik must reach. The stg app talks to its own stg DB locally; DBs are **not** tunnelled.

### 2. VPS Traefik routes the hostname to the tunnel

```yaml
# on the VPS Traefik (dynamic config or labels on a dummy service)
http:
  routers:
    experts-stg-web:
      rule: "Host(`app.stg.experts.com.sa`)"
      service: experts-stg-web
      tls: { certResolver: le }
  services:
    experts-stg-web:
      loadBalancer:
        servers:
          - url: "http://172.17.0.1:30022"
```

### 3. Make `-R 172.17.0.1` actually bind (one-time VPS setup)

On the VPS, `/etc/ssh/sshd_config`:

```
GatewayPorts clientspecified
```

then `sudo systemctl reload ssh`. **Without this, `-R` silently falls back to loopback-only** and Traefik (in its container) can't reach `172.17.0.1:port`.

### 4. Keep it alive

```bash
autossh -M 0 -N \
  -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes \
  -R 172.17.0.1:30022:127.0.0.1:30022 \
  experts
```

Wrap in a systemd user unit on your machine if you want it to survive reboots.

> **Why `172.17.0.1` and not `0.0.0.0`:** binding the docker bridge gateway keeps stg reachable only from *inside* the VPS (the bridge + host) — never the public internet. The public reaches it solely through Traefik, which terminates TLS and can enforce auth. A `0.0.0.0` bind would expose the raw app port to the world.

---

## prd — on the VPS

Runs on the VPS itself. Compose there uses **Traefik labels, no published ports** — Traefik fronts everything on `:443` with Let's Encrypt.

```yaml
services:
  web:
    labels:
      - traefik.enable=true
      - traefik.http.routers.experts-prd-web.rule=Host(`experts.com.sa`)
      - traefik.http.routers.experts-prd-web.tls.certresolver=le
    networks: [edge, internal]
  postgres:
    networks: [internal]   # internal only — never published
```

One env per host, so prd needs no port math.

### VPS hostname convention (stg + prd)

```
web        →  {slug}.com[.sa]                 experts.com.sa
api        →  api.{slug}.com[.sa]             api.experts.com.sa
realtime   →  ws.{slug}.com[.sa]              ws.experts.com.sa
stg        →  {svc}.stg.{slug}.com[.sa]       app.stg.experts.com.sa
```

---

## Adding a new project

1. Claim the next `PROJECT_ID` in the **Projects** registry (e.g. `07`, slug `visora`).
2. Decide its envs — `dev, prd` by default; add `stg` only if you'll tunnel-stage it.
3. **dev** (+ **stg** if used) local ports from the formula: Web `30071`/`30072`, Postgres `15071`/`15072`, …
4. **stg:** add `-R 172.17.0.1:<port>:127.0.0.1:<port>` lines reusing those numbers + a VPS Traefik router for `app.stg.visora.…`.
5. **prd:** VPS Traefik label on `:443`, no numeric port.

The registry is the only file that needs a human decision.

---

## Gotchas

- **`GatewayPorts clientspecified` on the VPS is mandatory** for `-R 172.17.0.1:…`. Forget it and the tunnel binds loopback-only — Traefik can't see it.
- **`172.17.0.1` assumes Traefik is on the default docker0 bridge.** If your VPS Traefik runs on a custom compose network, use *that* network's gateway (e.g. `172.18.0.1`), or add `extra_hosts: ["host.docker.internal:host-gateway"]` to Traefik and target `host.docker.internal` instead.
- **dev binds `127.0.0.1` explicitly.** A bare `30021:3000` binds `0.0.0.0` and exposes dev to your LAN. Always prefix `127.0.0.1:`.
- **Don't tunnel databases.** stg apps use their local stg DB; only HTTP entrypoints cross the tunnel. Attach to any local DB (dev or stg) via `127.0.0.1:<port>`.
- **prd DBs stay internal** — never a published port, never a tunnel.
- **Tunnel persistence:** plain `ssh -R` dies on network blips; use `autossh` + `ExitOnForwardFailure=yes` + `ServerAliveInterval`.

---

## Related

- [[Entities/Organizations/Logix]]
- [[Wiki/Concepts/Docker]]
