# Python 3.11 is provided by the official python image (Debian Bookworm
# slim). This eliminates the dependency on ppa:deadsnakes/ppa, which has
# no SLA and historically blocked deployment of critical agent-runtime
# fixes for days at a time when the PPA was unreachable. See #658.

# --- Toolchain source stages (copied into the Python base below) ---
# Node 26.5.0 from the official slim image — replaces the NodeSource setup_20.x
# apt install so the whole fleet runs the same Node major as the host and every
# app (experts + howa are both on 26.5.0). Pinned by digest for reproducibility.
FROM node:26.5.0-bookworm-slim@sha256:e999d087492c7227c85adc70574cf9d3cce774c3e6d7b8dfe473ee6b142c8f2c AS node-src

# Composer from the official image — PHP dependency manager copied in below so
# howa no longer needs its own composer overlay.
FROM composer:2.10.2 AS composer

FROM python:3.14-slim-bookworm

# Version tracking - set at build time via --build-arg VERSION=x.y.z
ARG VERSION=latest
LABEL trinity.base-image-version="${VERSION}"

ENV DEBIAN_FRONTEND=noninteractive
# Default TZ; overridden below when mounts/etc/timezone is installed (Asia/Riyadh).
ENV TZ=Asia/Riyadh
ENV TRINITY_BASE_VERSION="${VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    build-essential \
    apt-transport-https \
    ca-certificates \
    procps \
    locales \
    iproute2 \
    grep \
    findutils \
    coreutils \
    gnupg \
    lsb-release \
    sudo \
    openssh-server \
    jq \
    zip \
    unzip \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Node 26.5.0 overlaid from the official slim image. Copying /usr/local/ merges
# node/npm/npx/corepack into the Python base without disturbing Python (which
# also lives under /usr/local — the trees don't collide). pnpm@latest is the
# fleet-standard package manager; experts/howa no longer install their own.
COPY --from=node-src /usr/local/ /usr/local/
RUN npm install -g pnpm@latest && \
    node --version && npm --version && pnpm --version

RUN wget -q https://go.dev/dl/go1.23.4.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz && \
    rm go1.23.4.linux-amd64.tar.gz

# Docker apt repo for debian (was linux/ubuntu when the base was ubuntu:22.04).
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# GitHub CLI (gh) from the vendored .deb. Previously installed per-agent by
# .trinity/setup.sh on every container start; baking it here makes it durable
# across recreate and available to non-interactive (BASH_ENV) shells too.
COPY ./packages/gh_2.96.0_linux_amd64.deb /tmp/gh.deb
RUN apt-get update && \
    apt-get install -y --no-install-recommends /tmp/gh.deb && \
    rm -f /tmp/gh.deb && \
    rm -rf /var/lib/apt/lists/* && \
    gh --version

# PHP 8.5 (Sury) + Composer — lifted from howa's per-agent overlay so the whole
# fleet shares one PHP toolchain (howa's apps now target 8.5). Note: 8.5 has no
# separate php8.5-opcache package (unlike 8.4) — Zend OPcache is bundled into
# php8.5-cli/php8.5-common, so it is not listed here.
COPY --from=composer /usr/bin/composer /usr/local/bin/composer
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates curl lsb-release && \
    curl -fsSLo /tmp/debsuryorg-archive-keyring.deb https://packages.sury.org/debsuryorg-archive-keyring.deb && \
    dpkg -i /tmp/debsuryorg-archive-keyring.deb && \
    echo "deb [signed-by=/usr/share/keyrings/debsuryorg-archive-keyring.gpg] https://packages.sury.org/php/ $(lsb_release -sc) main" \
        > /etc/apt/sources.list.d/php.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        php8.5-cli php8.5-bcmath php8.5-curl php8.5-gd php8.5-intl php8.5-mbstring \
        php8.5-mysql php8.5-readline php8.5-sqlite3 php8.5-xml php8.5-zip && \
    rm -rf /var/lib/apt/lists/* /tmp/debsuryorg-archive-keyring.deb && \
    php --version && composer --version

RUN npm install -g @anthropic-ai/claude-code@latest

# Install Gemini CLI for multi-runtime support
RUN npm install -g @google/gemini-cli

# Install OpenAI Codex CLI for multi-runtime support (#1187).
# Pinned (not @latest) so base-image rebuilds are reproducible and a
# breaking Codex release can't silently change the agent runtime. The npm
# package resolves the platform-specific Rust binary via optional deps;
# the linux-x64 build lands here. Bump deliberately after testing.
RUN npm install -g @openai/codex@0.139.0

RUN useradd -m -s /bin/bash -u 1000 developer && \
    echo "developer:developer" | chpasswd && \
    usermod -aG sudo developer && \
    echo "developer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

RUN mkdir -p /home/developer/.ssh /home/developer/.config /home/developer/mcp-servers && \
    chown -R developer:developer /home/developer

ENV PATH="/usr/local/go/bin:$PATH"
ENV HOME=/home/developer
ENV USER=developer

USER developer
WORKDIR /home/developer

RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install --user \
        fastapi \
        uvicorn \
        httpx \
        pydantic \
        python-multipart \
        pyyaml \
        rich \
        cryptography

RUN mkdir -p /home/developer/.claude-agent

# Install Trinity guardrail hooks (GUARD-001/002/003).
# Hooks live in /opt/trinity/hooks/ (root-owned) so the agent cannot modify
# them at runtime. ~/.claude/settings.json registers them for Claude Code.
USER root
RUN mkdir -p /opt/trinity/hooks
COPY ./hooks/lib.py /opt/trinity/hooks/lib.py
COPY ./hooks/bash-guardrail.py /opt/trinity/hooks/bash-guardrail.py
COPY ./hooks/file-guardrail.py /opt/trinity/hooks/file-guardrail.py
COPY ./hooks/output-scanner.py /opt/trinity/hooks/output-scanner.py
COPY ./hooks/read-only-guard.py /opt/trinity/hooks/read-only-guard.py
COPY ./hooks/write-runtime-config.py /opt/trinity/hooks/write-runtime-config.py
COPY ./hooks/guardrails-baseline.json /opt/trinity/guardrails-baseline.json
RUN chmod 0555 /opt/trinity/hooks/*.py && \
    chmod 0444 /opt/trinity/guardrails-baseline.json && \
    chown -R root:root /opt/trinity

RUN mkdir -p /home/developer/.claude && \
    chown developer:developer /home/developer/.claude
COPY --chown=developer:developer ./hooks/claude-settings.json /home/developer/.claude/settings.json
RUN chmod 0644 /home/developer/.claude/settings.json
USER developer

# Copy agent server code to /app (outside persistent volume)
# This ensures code updates reach agents without volume conflicts
USER root
RUN mkdir -p /app && chown -R developer:developer /app
USER developer

COPY --chown=developer:developer ./agent-server.py /app/agent-server.py
COPY --chown=developer:developer ./agent_server /app/agent_server
COPY --chown=developer:developer ./startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh /app/agent-server.py

# Add /app to Python path so agent_server module can be imported
ENV PYTHONPATH="/app:${PYTHONPATH}"

EXPOSE 22 8000

# Container "running" is not sufficient readiness: startup may still be
# cloning a first workspace. Surface the actual agent API state to Docker.
HEALTHCHECK --interval=10s --timeout=3s --start-period=5m --retries=3 \
    CMD curl -fsS http://127.0.0.1:8000/health >/dev/null || exit 1

USER root

RUN mkdir -p /workspace /data /logs && \
    chown -R developer:developer /workspace /data /logs && \
    chmod 755 /workspace /data /logs

RUN mkdir -p /tmp/secure && \
    chmod 1777 /tmp/secure

# #1089: writable-layer dir for the subscription-token hot-reload override
# (/var/lib/trinity/oauth-token). Owned by the agent (UID 1000) so the
# agent-server process can write it; on the writable layer (NOT /home/developer)
# so it survives a plain stop+start but is wiped on recreate.
RUN mkdir -p /var/lib/trinity && \
    chown developer:developer /var/lib/trinity

# ---------------------------------------------------------------------------
# Shared host-style mounts baked into EVERY agent image (not compose binds).
# Source: docker/base-image/mounts/ — /etc paths survive workspace volume mounts;
# /home/developer/.bashrc is volume-masked, so we also hook /etc/profile,
# /etc/bash.bashrc, and startup.sh (idempotent append on the volume).
# ---------------------------------------------------------------------------
COPY ./mounts/etc/.bash /etc/.bash
COPY ./mounts/etc/profile.d/ /etc/profile.d/
COPY ./mounts/etc/timezone /etc/timezone

# Generic GitHub App token minter (fleet-wide; App ID / Installation ID / key
# come from each agent's env, no per-agent defaults). gh-env.sh (in /etc/.bash/)
# calls it to export GH_TOKEN. BASH_ENV makes non-interactive shells — e.g.
# scheduled agent loops and `bash -c ...` — source gh-env.sh too, closing the
# .bashrc-only gap that left loops running gh unauthenticated.
COPY ./mounts/usr/local/bin/gh-app-token /usr/local/bin/gh-app-token
RUN chmod 0555 /usr/local/bin/gh-app-token
ENV BASH_ENV=/etc/.bash/gh-env.sh

# RUN echo '. /etc/.bash/logix.env.sh' >> /home/developer/.bashrc

RUN TZ_NAME="$(tr -d '[:space:]' </etc/timezone)" && \
    ln -sfn "/usr/share/zoneinfo/${TZ_NAME}" /etc/localtime && \
    chmod 0644 /etc/timezone && \
    chmod 0755 /etc/profile.d/*.sh /etc/.bash/*.sh 2>/dev/null || true && \
    chmod 0644 /etc/.bash/ascii.art /etc/.bash/.bashrc 2>/dev/null || true && \

    echo '[ -f /etc/.bash/logix.env.sh ] && . /etc/.bash/logix.env.sh' >> /home/developer/.bashrc && \
    chown developer:developer /home/developer/.bashrc

USER developer

CMD ["/app/startup.sh"]

    # printf '\n# Trinity / Logix shared env (docker/base-image/mounts)\n[ -f /etc/.bash/logix.env.sh ] && . /etc/.bash/logix.env.sh\n' \
    #   >> /etc/profile && \
    # printf '\n# Trinity / Logix shared env (docker/base-image/mounts)\n[ -f /etc/.bash/logix.env.sh ] && . /etc/.bash/logix.env.sh\n' \
    #   >> /etc/bash.bashrc && \
    # echo '[ -f /etc/.bash/logix.env.sh ] && . /etc/.bash/logix.env.sh' >> /root/.bashrc && \
    # echo '[ -f /etc/.bash/logix.env.sh ] && . /etc/.bash/logix.env.sh' >> /etc/skel/.bashrc && \
    # Seed image home (masked by workspace volume at runtime; startup.sh re-applies).