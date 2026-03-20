from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-4-6"
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # Embeddings
    embedding_provider: str = "local"  # "openai" | "local"
    embedding_model: str = "all-MiniLM-L6-v2"

    # Chroma
    chroma_persist_dir: str = "./data/chroma_db"
    chroma_collection_name: str = "rag_rbac_docs"

    # JWT
    jwt_secret_key: str = "change-me-in-production-use-32-chars-min"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 8

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Retrieval
    retrieval_k: int = 5
    chunk_size: int = 512
    chunk_overlap: int = 64

    # Cost alert thresholds (USD)
    cost_alert_per_request: float = 0.10
    cost_alert_per_user_daily: float = 5.00
    cost_alert_system_daily: float = 50.00

    # Ragas alert thresholds
    ragas_faithfulness_min: float = 0.7
    ragas_relevancy_min: float = 0.7
    ragas_precision_min: float = 0.6

    # Metrics DB
    metrics_db_path: str = "./data/metrics.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
