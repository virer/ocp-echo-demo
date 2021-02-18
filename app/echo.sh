#!/bin/sh

GUNICORN_CMD_ARGS="--bind=0.0.0.0:8080 --workers=1 --log-config /app/logger.ini" gunicorn echo:app

# EOF