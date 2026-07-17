Now, since everything runs as expected so far,
in /Users/ahmedsulaimani/projects/experts/.github/workflows/experts-app.yml

I think we can enhance the build/deploy stages to include conditional checks or pipes, for example:

- detect prisma schema changes and run migrations, this usually needs to build another image alongside the app image

### Manual way:

```sh

docker compose build prisma - from @docker/staging/docker-compose.yml:93-107
# then run the migrations on VPS (production)
docker run --rm --network experts-shared-network --env-file /home/logix/experts/docker/staging/.env.prsma loogix/core:experts-stg-prisma pnpm db:deploy

#
docker compose build experts-stg-app experts-stg-prisma
docker compose run --rm experts-stg-prisma db:deploy
docker compose up -d experts-stg-app


```

- detect changes in `/Users/ahmedsulaimani/projects/experts/apps/experts-realtime` and build the image

```sh

docker compose build experts-realtime - from @docker/staging/docker-compose.yml:152-167
# then run the migrations on VPS (production)
docker run --rm --network experts-shared-network --env-file /home/logix/experts/docker/staging/.env.realtime loogix/core:experts-stg-realtime pnpm db:deploy

```

- tag & release the new version on Github using the `version-manager.sh` script, doesn't exist yet.

And so on... and let's try to keep things simple and clean as much as possible.
