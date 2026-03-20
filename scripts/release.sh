#!/bin/sh
set -e

CHROMA_DIR="${CHROMA_PERSIST_DIR:-/app/data/chroma_db}"

if [ ! -d "$CHROMA_DIR" ] || [ -z "$(ls -A "$CHROMA_DIR" 2>/dev/null)" ]; then
  echo "==> First deploy: generating data and ingesting into Chroma..."
  uv run python scripts/generate_data.py
  uv run python scripts/ingest.py
  echo "==> Ingestion complete."
else
  echo "==> Chroma DB already populated. Skipping ingestion."
fi
