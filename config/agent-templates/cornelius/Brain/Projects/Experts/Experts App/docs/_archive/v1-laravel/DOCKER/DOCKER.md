---
title: "🧠 DOCKER Cheat Sheet"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/docker"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🧠 DOCKER Cheat Sheet

A modern Docker helpers and commands to boost your productivity.

## 🌱 Docker Commands

### 🚀 Basic Commands

| Command                                       | Purpose                                                          |
| --------------------------------------------- | ---------------------------------------------------------------- |
| `docker build -t <image-name> .`              | Build a Docker image from a Dockerfile                           |
| `docker run -d <image-name>`                  | Run a Docker container in detached mode                          |
| `docker ps`                                   | List running containers                                          |
| `docker ps -a`                                | List all containers                                              |
| `docker stop <container-id>`                  | Stop a running container                                         |
| `docker rm <container-id>`                    | Remove a stopped container                                       |
| `docker rmi <image-name>`                     | Remove a Docker image                                            |
| `docker logs <container-id>`                  | View logs from a container                                       |
| `docker exec -it <container-id> /bin/bash`    | Access a running container's shell                               |
| `docker-compose up`                           | Start services defined in docker-compose.yml                     |
| `docker-compose down`                         | Stop and remove services                                         |
| `docker-compose build`                        | Build images defined in docker-compose.yml                       |
| `docker-compose logs`                         | View logs from all services                                      |
| `docker-compose exec <service> /bin/bash`     | Access a service's shell                                         |
| `docker-compose ps`                           | List all services defined in docker-compose.yml                  |
| `docker-compose pull`                         | Pull images for services defined in docker-compose.yml           |
| `docker-compose push`                         | Push images for services defined in docker-compose.yml           |
| `docker-compose restart`                      | Restart services defined in docker-compose.yml                   |
| `docker-compose scale <service>=<num>`        | Scale a service to a specified number of instances               |
| `docker-compose up -d`                        | Start services in detached mode                                  |
| `docker-compose down -v`                      | Stop and remove services and volumes                             |
| `docker-compose up --build`                   | Rebuild images before starting services                          |
| `docker-compose up --force-recreate`          | Recreate containers even if their configuration hasn't changed   |
| `docker-compose up --no-deps`                 | Start a service without starting linked services                 |
| `docker-compose up --scale <service>=<num>`   | Scale a service to a specified number of instances               |
| `docker-compose up --remove-orphans`          | Remove containers for services not defined in docker-compose.yml |
| `docker-compose up --abort-on-container-exit` | Stop all services if any service stops                           |
| `docker-compose up --timeout <seconds>`       | Set a timeout for starting services                              |
| `docker-compose up --no-cache`                | Build images without using cache                                 |
| `docker-compose up --build-arg <key>=<value>` | Pass build arguments to Dockerfile during build                  |
| `docker-compose up --env-file <file>`         | Specify an environment file for services                         |
| `docker-compose up --profile <profile>`       | Start services defined in a specific profile                     |

### 🐳 Dockerfile Commands

| Command                | Purpose                                                         |
| ---------------------- | --------------------------------------------------------------- |
| `FROM <image>`         | Specify the base image for the Dockerfile                       |
| `RUN <command>`        | Execute a command during the image build process                |
| `COPY <src> <dest>`    | Copy files from the host to the image during build              |
| `ADD <src> <dest>`     | Copy files and directories from the host to the image           |
| `CMD <command>`        | Specify the default command to run when the container starts    |
| `ENTRYPOINT <command>` | Specify the command to run when the container starts            |
| `ENV <key>=<value>`    | Set environment variables in the image                          |
| `EXPOSE <port>`        | Expose a port for the container                                 |
| `VOLUME <path>`        | Create a mount point for a volume                               |
| `WORKDIR <path>`       | Set the working directory for the container                     |
| `USER <user>`          | Specify the user to run the container as                        |
| `ARG <key>`            | Define a variable that users can pass at build-time             |
| `LABEL <key>=<value>`  | Add metadata to the image                                       |
| `HEALTHCHECK`          | Define a command to check the health of the container           |
| `SHELL <shell>`        | Specify the shell to use for the RUN command                    |
| `ONBUILD <command>`    | Add a trigger instruction to be executed when the image is used |
| `STOPSIGNAL <signal>`  | Specify the system call signal to stop the container            |
| `SHELL`                | Specify the shell to use for the RUN command                    |

### 🔍 Docker Networking Commands

| Command                                                                      | Purpose                                             |
| ---------------------------------------------------------------------------- | --------------------------------------------------- |
| `docker network ls`                                                          | List all Docker networks                            |
| `docker network inspect <network-name>`                                      | Inspect a Docker network                            |
| `docker network create <network-name>`                                       | Create a new Docker network                         |
| `docker network rm <network-name>`                                           | Remove a Docker network                             |
| `docker network connect <network-name> <container-id>`                       | Connect a container to a network                    |
| `docker network disconnect <network-name> <container-id>`                    | Disconnect a container from a network               |
| `docker network prune`                                                       | Remove all unused networks                          |
| `docker network create --driver <driver> <network-name>`                     | Create a network with a specific driver             |
| `docker network create --subnet <subnet> <network-name>`                     | Create a network with a specific subnet             |
| `docker network create --gateway <gateway> <network-name>`                   | Create a network with a specific gateway            |
| `docker network create --attachable <network-name>`                          | Create an attachable network                        |
| `docker network create --internal <network-name>`                            | Create an internal network                          |
| `docker network create --opt <key>=<value> <network-name>`                   | Create a network with specific options              |
| `docker network create --ipv6 <network-name>`                                | Create a network with IPv6 support                  |
| `docker network create --label <key>=<value> <network-name>`                 | Create a network with specific labels               |
| `docker network create --scope <scope> <network-name>`                       | Create a network with a specific scope              |
| `docker network create --ingress <network-name>`                             | Create an ingress network                           |
| `docker network create --driver-opts <key>=<value> <network-name>`           | Create a network with specific driver options       |
| `docker network create --subnet <subnet> --gateway <gateway> <network-name>` | Create a network with a specific subnet and gateway |
| `docker network create --ip-range <ip-range> <network-name>`                 | Create a network with a specific IP range           |
| `docker network create --aux-address <key>=<value> <network-name>`           | Create a network with auxiliary addresses           |
| `docker network create --ipam-driver <driver> <network-name>`                | Create a network with a specific IPAM driver        |

### 🗂️ Docker Volumes Commands

| Command                                                                               | Purpose                                                   |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `docker volume ls`                                                                    | List all Docker volumes                                   |
| `docker volume inspect <volume-name>`                                                 | Inspect a Docker volume                                   |
| `docker volume create <volume-name>`                                                  | Create a new Docker volume                                |
| `docker volume rm <volume-name>`                                                      | Remove a Docker volume                                    |
| `docker volume prune`                                                                 | Remove all unused volumes                                 |
| `docker volume rm $(docker volume ls -qf dangling=true)`                              | Remove all dangling volumes                               |
| `docker volume create --name <volume-name>`                                           | Create a volume with a specific name                      |
| `docker volume create --driver <driver> <volume-name>`                                | Create a volume with a specific driver                    |
| `docker volume create --opt <key>=<value> <volume-name>`                              | Create a volume with specific options                     |
| `docker volume create --label <key>=<value> <volume-name>`                            | Create a volume with specific labels                      |
| `docker volume create --mount <mount-spec> <volume-name>`                             | Create a volume with a specific mount specification       |
| `docker volume create --scope <scope> <volume-name>`                                  | Create a volume with a specific scope                     |
| `docker volume create --name <volume-name> --opt <key>=<value>`                       | Create a volume with a specific name and options          |
| `docker volume create --name <volume-name> --label <key>=<value>`                     | Create a volume with a specific name and labels           |
| `docker volume create --name <volume-name> --driver <driver>`                         | Create a volume with a specific name and driver           |
| `docker volume create --name <volume-name> --opt <key>=<value> --label <key>=<value>` | Create a volume with a specific name, options, and labels |
| `docker volume create --name <volume-name> --driver <driver> --opt <key>=<value>`     | Create a volume with a specific name, driver, and options |
| `docker volume create --name <volume-name> --driver <driver> --label <key>=<value>`   | Create a volume with a specific name, driver, and labels  |
| `docker volume create --name <volume-name> --opt <key>=<value> --label <key>=<value>` | Create a volume with a specific name, options, and labels |
| `docker volume create --name <volume-name> --opt <key>=<value> --driver <driver>`     | Create a volume with a specific name, options, and driver |
| `docker volume create --name <volume-name> --label <key>=<value> --driver <driver>`   | Create a volume with a specific name, labels, and driver  |

### 🖼 Docker Image Commands

| Command                                                          | Purpose                                       |
| ---------------------------------------------------------------- | --------------------------------------------- |
| `docker images`                                                  | List all Docker images                        |
| `docker rmi <image-name>`                                        | Remove a Docker image                         |
| `docker rmi $(docker images -qf dangling=true)`                  | Remove all dangling images                    |
| `docker rmi -f <image-name>`                                     | Force remove a Docker image                   |
| `docker rmi -f $(docker images -qf dangling=true)`               | Force remove all dangling images              |
| `docker rmi -f $(docker images -q -a)`                           | Force remove all images                       |
| `docker rmi -f $(docker images -q)`                              | Force remove all images                       |
| `docker rmi -f $(docker images -q --filter "label=<label>")`     | Force remove images with a specific label     |
| `docker rmi -f $(docker images -q --filter "before=<image>")`    | Force remove images before a specific image   |
| `docker rmi -f $(docker images -q --filter "since=<image>")`     | Force remove images since a specific image    |
| `docker rmi -f $(docker images -q --filter "reference=<image>")` | Force remove images with a specific reference |
| `docker rmi -f $(docker images -q --filter "id=<image-id>")`     | Force remove images with a specific ID        |
| `docker rmi -f $(docker images -q --filter "dangling=true")`     | Force remove dangling images                  |
| `docker rmi -f $(docker images -q --filter "label=<label>")`     | Force remove images with a specific label     |
| `docker rmi -f $(docker images -q --filter "before=<image>")`    | Force remove images before a specific image   |
| `docker rmi -f $(docker images -q --filter "since=<image>")`     | Force remove images since a specific image    |
| `docker rmi -f $(docker images -q --filter "reference=<image>")` | Force remove images with a specific reference |
| `docker rmi -f $(docker images -q --filter "id=<image-id>")`     | Force remove images with a specific ID        |

### 🧩 Docker Compose Commands

| Command                                       | Purpose                                                          |
| --------------------------------------------- | ---------------------------------------------------------------- |
| `docker-compose up`                           | Start services defined in docker-compose.yml                     |
| `docker-compose down`                         | Stop and remove services defined in docker-compose.yml           |
| `docker-compose build`                        | Build images defined in docker-compose.yml                       |
| `docker-compose logs`                         | View logs from all services defined in docker-compose.yml        |
| `docker-compose ps`                           | List all services defined in docker-compose.yml                  |
| `docker-compose exec`                         | Execute a command in a running service                           |
| `docker-compose pull`                         | Pull images for services defined in docker-compose.yml           |
| `docker-compose push`                         | Push images for services defined in docker-compose.yml           |
| `docker-compose scale`                        | Scale a service to a specified number of instances               |
| `docker-compose restart`                      | Restart services defined in docker-compose.yml                   |
| `docker-compose config`                       | Validate and view the configuration of docker-compose.yml        |
| `docker-compose version`                      | Show the version of Docker Compose                               |
| `docker-compose help`                         | Show help for Docker Compose commands                            |
| `docker-compose create`                       | Create services defined in docker-compose.yml                    |
| `docker-compose start`                        | Start services defined in docker-compose.yml                     |
| `docker-compose stop`                         | Stop services defined in docker-compose.yml                      |
| `docker-compose rm`                           | Remove stopped services defined in docker-compose.yml            |
| `docker-compose up -d`                        | Start services in detached mode                                  |
| `docker-compose down -v`                      | Stop and remove services and volumes                             |
| `docker-compose up --build`                   | Rebuild images before starting services                          |
| `docker-compose up --force-recreate`          | Recreate containers even if their configuration hasn't changed   |
| `docker-compose up --no-deps`                 | Start a service without starting linked services                 |
| `docker-compose up --scale <service>=<num>`   | Scale a service to a specified number of instances               |
| `docker-compose up --remove-orphans`          | Remove containers for services not defined in docker-compose.yml |
| `docker-compose up --abort-on-container-exit` | Stop all services if any service stops                           |
| `docker-compose up --timeout <seconds>`       | Set a timeout for starting services                              |
| `docker-compose up --no-cache`                | Build images without using cache                                 |
| `docker-compose up --build-arg <key>=<value>` | Pass build arguments to Dockerfile during build                  |
| `docker-compose up --env-file <file>`         | Specify an environment file for services                         |
| `docker-compose up --profile <profile>`       | Start services defined in a specific profile                     |
| `docker-compose up --detach`                  | Start services in detached mode                                  |
| `docker-compose up --no-recreate`             | Start services without recreating containers                     |
| `docker-compose up --no-build`                | Start services without building images                           |

### Docker Custom Commands

| Command                                                                 | Purpose                                                       |
| ----------------------------------------------------------------------- | ------------------------------------------------------------- |
| `docker run -it --rm <image-name> bash`                                 | Run a temporary container and remove it after exit            |
| `docker run -d --name <container-name> <image-name>`                    | Run a container in detached mode with a specific name         |
| `docker run -p <host-port>:<container-port> <image-name>`               | Map a host port to a container port                           |
| `docker compose -f docker-compose.yml  up -d`                           | Start services defined in docker-compose.yml in detached mode |
| `docker compose -f docker-compose.yml  down`                            | Stop and remove services defined in docker-compose.yml        |
| `docker compose -f docker-compose.yml  build`                           | Build images defined in docker-compose.yml                    |
| `docker compose -f docker-compose.yml  logs`                            | View logs from all services defined in docker-compose.yml     |
| `docker compose -f docker-compose.yml  ps`                              | List all services defined in docker-compose.yml               |
| `docker compose -f docker-compose.yml  exec <service> bash`             | Access a service's shell in docker-compose.yml                |
| `docker compose -f docker-compose.yml  pull`                            | Pull images for services defined in docker-compose.yml        |
| `docker compose -f docker-compose.yml  push`                            | Push images for services defined in docker-compose.yml        |
| `docker compose -f docker-compose.yml  restart`                         | Restart services defined in docker-compose.yml                |
| `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d` | Start services with multiple compose files                    |

### Custom Docker Scripts

```bash
📦 dkr — Docker build & deployment utility

USAGE:
  dkr [OPTIONS] [COMMAND]

OPTIONS:
  --app <name>         Name of the app (e.g. experts-app or experts-api)
  --tag <tag>          Docker image tag (default: dev)
  --prod               Use Dockerfile.prod (default is Dockerfile.dev)
  --build              Build image before command (default: true)
  --push               Push the built image to Docker Hub
  --start              Start Docker Compose stack
  --no-build           Skip Docker build step (use existing image)
  --image <name>       Override image name (for generic container commands)
  --container <name>   Override container name
  -d                   Run Docker Compose in detached mode
  --help               Show this help message

COMMANDS:
  build                Build the Docker image
  run                  Run the container
  shell                Open a shell in the running container
  stop                 Stop the container
  clean                Remove the Docker image
  rebuild              Clean, rebuild and run the container

EXAMPLES:

🔧 Image build/push/deploy flow:
  dkr --app experts-app --tag 1.0.0 --prod --push         # Build prod image & push to Docker Hub
  dkr --app experts-api --tag dev --start -d              # Build & start API service in detached mode
  dkr --no-build --start                                  # Start existing services without rebuilding
  dkr --start -d                                          # Rebuild and start all services in detached mode
  dkr -d                                                  # Alias for docker-compose up -d - similar to above

🛠️  Low-level container control:
  dkr build --image experts-api --container experts-api   # Build a generic image
  dkr run --image experts-api --container experts-api     # Run container from that image
  dkr shell --container experts-api                       # Open bash shell in a running container
  dkr stop --container experts-api                        # Stop the container
  dkr clean --image experts-api                           # Remove the Docker image
  dkr rebuild --image experts-api --container experts-api # Clean, rebuild, and run
```

### Commands Suquence (PROD)

```bash
# Build the image and push to Docker Hub
dkr --app experts-app --tag 1.0.4 --prod --push

# Update image tag in docker-compose.prod.yml

# Run the container
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Commands Suquence (DEV)

```bash
# Build the image
dkr --app experts-app --tag dev --build
# Run the container
dkr --app experts-app --tag dev --start -d
# Run the container with shell
dkr --app experts-app --tag dev --start -d shell
# Stop the container
dkr --app experts-app --tag dev --stop
# Clean the container
dkr --app experts-app --tag dev --clean
# Rebuild the container
dkr --app experts-app --tag dev --rebuild
# Rebuild the container with shell
dkr --app experts-app --tag dev --rebuild shell
```

### Docker Important Commands

```bash
docker build -t loogix/experts-app:1.0.1 -f apps/experts-app/Dockerfile.prod .

# docker buildx build --platform linux/arm64,linux/amd64 -t loogix/experts-app:1.0.1 -f apps/experts-app/Dockerfile.prod --push .

docker build -t experts-app:dev -f apps/experts-app/Dockerfile.dev .

docker-compose -f docker-compose.yml -f docker-compose.override.yml build experts-app

docker inspect experts-app --format '{{ json .Mounts }}' | jq

```

### Frequently Used Commands

```bash
docker ps -a
# Build a specific image
# docker build -t experts-app:dev -f apps/experts-app/Dockerfile.dev .
# docker build -t experts-app:prod -f apps/experts-app/Dockerfile.prod .
# docker-compose -f docker-compose.yml -f docker-compose.override.yml up experts-app

# docker build -t experts-base:staging -f Dockerfile.base  -f docker-compose.staging.yml . && docker-compose up --build

docker build -t experts-base:dev -f Dockerfile.base . && docker-compose up --build

docker build -t experts-base:dev -f Dockerfile.base . && docker-compose build --no-cache && docker-compose up

```

### Build specific image

```bash
docker build -t experts-admin:dev -f apps/experts-admin/Dockerfile.dev .
# up built image
docker-compose -f docker-compose.yml -f docker-compose.override.yml up experts-admin

docker build -t loogix/experts-admin:staging -f apps/experts-admin/Dockerfile.staging .
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up experts-admin

```

### Staging Build

```bash
# Build & Run all staging images
docker build -t loogix/experts-base:staging -f docker/Dockerfile.base . && docker-compose -f docker-compose.yml -f docker-compose.staging.yml up --build
```

### Production Build

```bash
# Build & Run all production images
docker build -t loogix/experts-base:production -f docker/Dockerfile.prod . && docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

### DEV ALL

```sh
docker build -t experts-base:dev -f docker/Dockerfile.base . && docker-compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml -p experts up --build

docker build -t experts-base:dev -f Dockerfile.base .. && cd ./development && docker compose up -d --build
# new CMD
docker build -t loogix/experts-base:dev -f Dockerfile.base .. && cd ./development && docker compose up -d --build --force-recreate
```

### BUILD PROD PER IMG

```sh
docker build -t loogix/experts-api:1.0.8 -f apps/experts-api/Dockerfile.minimal .
docker build -t loogix/experts-app:1.0.6 -f apps/experts-app/Dockerfile.minimal .
docker build -t loogix/experts-auth:1.0.2 -f apps/experts-auth/Dockerfile.minimal .
docker build -t loogix/experts-portal:1.0.1 -f apps/experts-portal/Dockerfile.minimal .
docker build -t loogix/experts-admin:1.0.2 -f apps/experts-admin/Dockerfile.minimal .

```

### RUN PROD LOCALLY

```sh
docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml -p experts up -d --build
```

### PUSH ALL BUILT IMGS

```sh
for img in
 loogix/experts-api:1.0.7   loogix/experts-app:1.0.5   loogix/experts-auth:1.0.1   loogix/experts-admin:1.0.1   loogix/experts-portal:1.0.0; do   docker push $img; done

 for img in \
  loogix/experts-api:1.0.7 \
  loogix/experts-app:1.0.5 \
  loogix/experts-auth:1.0.1 \
  loogix/experts-admin:1.0.1 \
  loogix/experts-portal:1.0.0;
 do
  docker push $img
done

for img in \
  loogix/experts-api:staging \
  loogix/experts-app:staging \
  loogix/experts-server:staging; do
  docker push "$img"
done

for img in \
  loogix/experts-api:production \
  loogix/experts-app:production \
  loogix/experts-auth:production \
  loogix/experts-admin:production \
  loogix/experts-portal:production; do
  docker push "$img"
done

for img in \
  loogix/experts-api:staging \
  loogix/experts-app:staging \
  loogix/experts-server:staging; do
  docker pull "$img"
done

```

### STOP ALL CONTAINERS

```sh
docker stop $(docker ps -a -q)
```

### BRING THEM DOWN

```sh
docker-compose -p experts -f docker-compose.yml -f docker-compose.prod.yml down
```

### RM ORPHANS !!!DANGER - This action will rm dbs

```sh
docker-compose down --volumes --remove-orphans
```

### Build prod single app from root dir

```sh

docker build --build-arg ENV_FILE=.env.production --build-arg APP_ENV=production --target minimal -t loogix/experts-app:production -f apps/experts-app/Dockerfile.minimal .

```

### ENHANCED Build prod single app from root dir

```sh

BUILDKIT_INLINE_CACHE=1 docker build -t loogix/experts-app:staging --build-arg ENV_FILE=.env.staging --build-arg APP_ENV=staging --build-arg TURBO_TEAM=team_OSMA5gfld349VN5IHHKGqqam --build-arg TURBO_TOKEN=Uo99VYCv0WndPWp7RoCP49Df --target minimal -f apps/experts-app/Dockerfile.minimal .

BUILDKIT_INLINE_CACHE=1 docker build -t loogix/experts-app:production --build-arg ENV_FILE=.env.production --build-arg APP_ENV=production --build-arg TURBO_TEAM=team_OSMA5gfld349VN5IHHKGqqam --build-arg TURBO_TOKEN=Uo99VYCv0WndPWp7RoCP49Df --target minimal -f apps/experts-app/Dockerfile.minimal .

BUILDKIT_INLINE_CACHE=1 docker buildx build  \
  -t loogix/experts-app:staging \
  --build-arg ENV_FILE=.env.production \
  --build-arg APP_ENV=production \
  --build-arg TURBO_TEAM=team_OSMA5gfld349VN5IHHKGqqam \
  --build-arg TURBO_TOKEN=Uo99VYCv0WndPWp7RoCP49Df \
  -f apps/experts-app/Dockerfile.minimal \
  --target minimal \
  .

```

### LOOP THROUGH

```sh

for app in \
  experts-api \
  experts-app \
  experts-auth \
  experts-admin \
  experts-portal; do
  BUILDKIT_INLINE_CACHE=1 docker build -t loogix/"$app":production --build-arg ENV_FILE=.env.production --build-arg APP_ENV=production --build-arg TURBO_TEAM=team_OSMA5gfld349VN5IHHKGqqam --build-arg TURBO_TOKEN=Uo99VYCv0WndPWp7RoCP49Df --target minimal -f apps/"$app"/Dockerfile.minimal .
done

```

### HoWA

```sh

 for img in \
  loogix/howa-server:prod \
  loogix/howa-core:prod \
  loogix/howa-app:prod
 do
  docker push $img
 done

for img in loogix/howa-server loogix/howa-core loogix/howa-app; do
  docker image tag ${img}:prod ${img}:backup
done

 for img in \
  loogix/howa-server:prod \
  loogix/howa-core:prod \
  loogix/howa-app:prod
 do
   docker pull $img
 done


 for img in \
  loogix/howa-core:prod \
  loogix/howa-app:prod
 do
  docker push $img
 done

 for img in \
  loogix/howa-core:prod \
  loogix/howa-app:prod
 do

  docker pull $img
 done

 service nginx stop \
 && supervisorctl stop all \
 && docker compose up -d

```
