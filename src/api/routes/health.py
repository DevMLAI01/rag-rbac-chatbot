from datetime import datetime, timezone
from fastapi import APIRouter
from src.retrieval.vector_store import get_document_count

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.get("/detailed")
async def health_detailed():
    try:
        doc_count = get_document_count()
        vs_status = "healthy"
    except Exception:
        doc_count = 0
        vs_status = "degraded"
    return {
        "api": "healthy",
        "vector_store": vs_status,
        "document_count": doc_count,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
