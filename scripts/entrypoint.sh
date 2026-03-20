#!/bin/sh
set -e

CHROMA_DIR="${CHROMA_PERSIST_DIR:-/app/data/chroma_db}"

# On first deploy the volume is empty — generate data and ingest
if [ ! -d "$CHROMA_DIR" ] || [ -z "$(ls -A "$CHROMA_DIR" 2>/dev/null)" ]; then
  echo "==> Chroma DB not found. Running first-time setup..."
  uv run python scripts/generate_data.py
  uv run python scripts/ingest.py
  echo "==> Ingestion complete."
else
  echo "==> Chroma DB found. Skipping ingestion."
fi

exec uv run uvicorn src.api.main:app --host 0.0.0.0 --port "${API_PORT:-8000}"
