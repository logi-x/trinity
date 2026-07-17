---
title: "🛠 Contributing to Experts Monorepo"
date: "2026-04-11"
tags: ["project/experts", "topic/contributing"]
category: "projects/experts"
updated: "2026-07-15"
---

# 🛠 Contributing to Experts Monorepo

Welcome! 👋 We're excited to have you contributing to the **Experts Project**. This guide will help you get started with the right branch workflows, coding conventions, and CI setup.

## Table of Contents

- [Contributing](#contributing)
  - [Table of Contents](#table-of-contents)
    - [Monorepo Structure](#monorepo-structure)
    - [Getting Started](#getting-started)
    - [Branching Strategy](#branching-strategy)
    - [Pull Request Checklist](#pull-request-checklist)
    - [CI/CD & Deployment](#ci-cd--deployment)
    - [Communication](#communication)
    - [Other Notes](#other-notes)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
      - [Clone the repository:](#clone-the-repository)
      - [Set Up Environment Variables](#set-up-environment-variables)
      - [Build and Start Containers](#build-and-start-containers)
      - [Access the Services](#access-the-services)
      - [Additional Commands](#additional-commands)
      - [To rebuild containers after changes:](#to-rebuild-containers-after-changes)
        - [To stop the containers:](#to-stop-the-containers)
        - [To run commands inside the containers:](#to-run-commands-inside-the-containers)
        - [To view logs for a specific service (e.g., experts-api):](#to-view-logs-for-a-specific-service-eg-experts-api)
        - [To view logs for all services:](#to-view-logs-for-all-services)
        - [To run artisan commands inside the experts-api container:](#to-run-artisan-commands-inside-the-experts-api-container)
        - [To run npm commands inside the experts-app container:](#to-run-npm-commands-inside-the-experts-app-container)
        - [To access the MySQL database:](#to-access-the-mysql-database)

- [Thank you for contributing 🙌](#thank-you-for-contributing-)

---

## 📦 Repository layout

```bash
experts/
├── apps/
│   ├── experts-app/       # Next.js web app + API routes + Prisma (primary)
│   ├── experts-realtime/  # WebSocket gateway (optional local service)
│   └── experts-prisma/    # Prisma helper image/scripts (optional)
├── docker/                # Compose stacks for staging / workers / data
├── .github/workflows/     # CI (e.g. experts-app.yml)
└── README.md
```

Mobile clients may live in separate repositories. **Default workflow:** `cd apps/experts-app`, `pnpm install`, `pnpm dev` (see root `AGENTS.md`).

---

## 🌱 Getting Started

1. **Fork and clone the repo:**

   ```bash
   git clone git@github.com:logi-x/experts.git
   cd experts
   git checkout development
   ```

2. **Install dependencies for your platform (example for web):**

   ```bash
   cd apps/experts-app
   pnpm install
   pnpm dev
   ```

3. **Create your feature branch:**

   ```bash
   git checkout -b web/feature/my-awesome-feature
   ```

---

## 🔁 Branching Strategy

| Branch        | Purpose                             | Who Works Here   |
| ------------- | ----------------------------------- | ---------------- |
| `development` | Base branch for new features        | ✅ Everyone      |
| `web/dev`     | Active development for Web app      | Web team only    |
| `staging`     | QA-ready code, goes to TestFlight   | Maintainers only |
| `main`        | Production-ready, deployed releases | Maintainers only |

---

## ✅ Pull Request Checklist

Before submitting a PR:

- [ ] Name your branch appropriately: `web/feature/login-form`
- [ ] Code follows existing style guide (Prettier, ESLint)
- [ ] Tests are added or updated if needed
- [ ] Add a changeset with `npx changeset`
- [ ] Link the relevant issue if it exists

---

## 🚀 CI/CD & Deployment

- CI runs on all pull requests via GitHub Actions.
- You must pass all status checks before merging.
- Only maintainers can merge into `staging` and `main`.

---

## 📢 Communication

- PR notifications are sent to Slack for visibility.
- Use labels like `web`, `ios`, `api` to auto-tag your PR.
- Ask questions in the team Slack channel or tag @Ahmed for repo support.

---

## 🧹 Other Notes

- Add `.changeset` entries for all public changes.
- Use squash/rebase to keep history clean.
- Linear history is enforced — no merge commits allowed.

---

## Prerequisites

- Node.js (v22.x)
- npm (v10.x)
- pnpm (v8.x)
- PHP (v8.x)
- MySQL (v8.x)
- composer (v2.x)
- Docker (v4.x)
- Docker Compose (v1.x)

## Installation

1. Clone the repository:

   ```bash
   git clone --branch development --recurse-submodules https://github.com/logi-x/experts.git
   ```

   If you've already cloned the repository without submodules, run:

   ```bash
   git submodule update --init --recursive
   ```

2. Set Up Environment Variables

   For experts-api (/experts-api/.env)

   ```env
   APP_ENV=local

   APP_URL=http://localhost:8000
   FRONTEND_URL=http://localhost:3000

   DB_CONNECTION=mysql
   DB_HOST=db
   DB_PORT=3306
   DB_DATABASE=experts
   DB_USERNAME=root
   DB_PASSWORD=rootpassword
   ```

   For experts-app (/experts-app/.env)

   ```env
   AUTH_URL=http://localhost:3000
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

3. Build and Start Containers

   Run the following command to build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

4. Access the Services
   - Experts API: <http://localhost:8000>
   - Experts Web: <http://localhost:3000>

5. Additional Commands
   To rebuild containers after changes:

   ```bash
   docker-compose up --build
   ```

   To stop the containers:

   ```bash
   docker-compose down
   ```

   To run commands inside the containers:

   ```bash
   docker-compose exec <service> <command>
   ```

   To view logs for a specific service (e.g., experts-api):

   ```bash
   docker-compose logs -f experts-api
   ```

   To view logs for all services:

   ```bash
   docker-compose logs -f
   ```

   To run artisan commands inside the experts-api container:

   ```bash
   docker-compose exec experts-api php artisan <command>
   ```

   To run npm commands inside the experts-app container:

   ```bash
   docker-compose exec experts-app pnpm <command>
   ```

   To access the MySQL database:

   ```bash
   docker-compose exec db mysql -u root -p
   # Enter the password: rootpassword

   # Or

   docker-compose exec mysql bash
   # mysql -u root -p
   # Enter the password: rootpassword

   ```

---

## Loogix Experts Docker Images

This repository provides Docker images for various services in the **Experts** platform by **Logix Inc.**, including:

- `experts-app` (Next.js Frontend)
- `experts-api` (Laravel API Backend)
- `experts-auth` (OAuth/SSO UI)
- `experts-admin` (Admin Dashboard)

All images are production-ready and follow best practices for CI/CD, security, and size optimization.

---

### 🚀 Getting Started

Pull the image you need:

```bash
docker pull loogix/experts-app:latest
docker pull loogix/experts-api:latest
docker pull loogix/experts-auth:latest
docker pull loogix/experts-admin:latest
```

You can also build the images locally using the provided Dockerfiles in the `Dockerfile` directory.

### 🛠 Building the Images

```bash
docker build -t loogix/experts-app:latest -f Dockerfile .
docker build -t loogix/experts-api:latest -f Dockerfile .
docker build -t loogix/experts-auth:latest -f Dockerfile .
docker build -t loogix/experts-admin:latest -f Dockerfile .
```

You can refer to the [Docker Docs](https://github.com/logi-x/experts/blob/main/docs/DOCKER.md) for each service for more details on the build process and configurations.

---

We appreciate your efforts in making the **Experts Project** better. If you have any questions or need assistance, feel free to reach out to the team.

Thank you for contributing 🙌
