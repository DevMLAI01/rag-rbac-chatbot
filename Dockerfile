FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock* ./

# Install dependencies (no dev deps, no editable install)
RUN uv sync --no-dev --frozen

# Copy source
COPY . .

# Chroma persistence directory (overridden by Fly.io volume mount)
RUN mkdir -p /app/data/chroma_db

# Entrypoint handles first-time ingest then starts uvicorn
# Use sed to strip Windows CRLF line endings before executing
COPY scripts/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "/entrypoint.sh"]
