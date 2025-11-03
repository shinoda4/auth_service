#!/bin/sh
set -e
cd auth_service
uv run python manage.py migrate
uv run gunicorn auth_service.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile - \
    --timeout 60