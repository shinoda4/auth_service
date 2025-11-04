
## Build Docker and run

```shell
cp .env.example .env
```

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