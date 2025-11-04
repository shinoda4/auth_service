
## Build Docker and run

```shell
cp .env.example .env
```

Paste django secret key into `.env`.

Then run following command:

```shell
sudo docker compose build && sudo docker compose up -d
```

## Docker Compose

Expose `8000` post as auth service `web` port.

Expose `5433` port as postgres post of `db` service.

## Permission Class

- user_manage
- role_manage
- permission_manage

## Development web

### Dev all

```shell
#This will also delete database data!
docker compose down -v

docker compose build

docker compose run
```

### Dev web

```shell
docker-compose stop web

docker-compose rm -f web

docker-compose up -d --build web
```