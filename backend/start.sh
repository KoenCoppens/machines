#!/bin/sh
set -e

python -m app.services.init_db
alembic upgrade head

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
