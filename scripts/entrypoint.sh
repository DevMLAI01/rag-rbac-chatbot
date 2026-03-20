#\!/bin/sh
set -e

CHROMA_DIR="${CHROMA_PERSIST_DIR:-/app/data/chroma_db}"
SENTINEL="/app/data/.ingest_complete"
PORT="${API_PORT:-8000}"

if [ \! -f "$SENTINEL" ]; then
  echo "==> First boot: running ingest before starting server..."
  uv run python scripts/generate_data.py
  uv run python scripts/ingest.py
  touch "$SENTINEL"
  echo "==> Ingestion complete."
fi

exec uv run uvicorn src.api.main:app --host 0.0.0.0 --port "$PORT"
