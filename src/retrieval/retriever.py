from __future__ import annotations
from langchain_core.documents import Document
from src.retrieval.vector_store import get_vector_store
from src.retrieval.rbac_filter import build_rbac_filter
from config.settings import settings


class RBACRetriever:
    def __init__(self, k: int = settings.retrieval_k):
        self.k = k

    def retrieve(self, query: str, role: str) -> list[Document]:
        """Retrieve top-k docs accessible to the given role."""
        store = get_vector_store()
        where_filter = build_rbac_filter(role)
        return store.similarity_search(query=query, k=self.k, filter=where_filter)


_retriever: RBACRetriever | None = None


def get_retriever() -> RBACRetriever:
    global _retriever
    if _retriever is None:
        _retriever = RBACRetriever()
    return _retriever
