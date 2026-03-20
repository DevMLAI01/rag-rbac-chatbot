#\!/bin/sh
set -e
exec uv run uvicorn src.api.main:app --host 0.0.0.0 --port "${API_PORT:-8000}"
