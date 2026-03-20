from __future__ import annotations
import chromadb
from langchain_chroma import Chroma
from config.settings import settings
from src.ingestion.embedder import get_embedding_function

_store: Chroma | None = None


def get_vector_store() -> Chroma:
    global _store
    if _store is None:
        _store = Chroma(
            collection_name=settings.chroma_collection_name,
            embedding_function=get_embedding_function(),
            persist_directory=settings.chroma_persist_dir,
        )
    return _store


def get_document_count() -> int:
    store = get_vector_store()
    return store._collection.count()
