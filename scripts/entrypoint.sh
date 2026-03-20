#\!/bin/sh
set -e

CHROMA_DIR="${CHROMA_PERSIST_DIR:-/app/data/chroma_db}"

if [ \! -d "$CHROMA_DIR" ] || [ -z "$(ls -A "$CHROMA_DIR" 2>/dev/null)" ]; then
  echo "==> First boot: generating + ingesting data (takes 5-10 min)..."
  uv run python scripts/generate_data.py
  uv run python scripts/ingest.py
  echo "==> Ingestion complete."
fi

exec uv run uvicorn src.api.main:app --host 0.0.0.0 --port "${API_PORT:-8000}"
