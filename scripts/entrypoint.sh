#\!/bin/sh
set -e

CHROMA_DIR="${CHROMA_PERSIST_DIR:-/app/data/chroma_db}"
PORT="${API_PORT:-8000}"

if [ \! -d "$CHROMA_DIR" ] || [ -z "$(ls -A "$CHROMA_DIR" 2>/dev/null)" ]; then
  echo "==> First boot: starting uvicorn in background while ingest runs..."
  uv run uvicorn src.api.main:app --host 0.0.0.0 --port "$PORT" &
  UVICORN_PID=$\!
  sleep 10
  uv run python scripts/generate_data.py
  uv run python scripts/ingest.py
  echo "==> Ingestion complete. Restarting uvicorn with fresh data..."
  kill "$UVICORN_PID" 2>/dev/null || true
  wait "$UVICORN_PID" 2>/dev/null || true
fi

exec uv run uvicorn src.api.main:app --host 0.0.0.0 --port "$PORT"
