#!/bin/sh
set -e

# Ensure working directory is project root
cd "$(dirname "$0")/.."

# Ensure Python can import the local app package
export PYTHONPATH="${PYTHONPATH:-/app}"

# Apply database migrations with explicit config
alembic -c /app/alembic.ini upgrade head

# Start the API server
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
