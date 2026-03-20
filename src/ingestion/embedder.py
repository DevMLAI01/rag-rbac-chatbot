from __future__ import annotations
from config.settings import settings


def get_embedding_function():
    """Return a LangChain-compatible embedding object based on settings."""
    if settings.embedding_provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key,
        )
    # Default: local sentence-transformers (no API key required)
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)
