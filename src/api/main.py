from __future__ import annotations
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from monitoring.metrics_store import init_db
from src.graph.workflow import compile_workflow
from src.api.routes import auth, chat, health, monitoring

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    app.state.graph = compile_workflow()
    logging.getLogger(__name__).info("RAG-RBAC API started — graph compiled, DB initialised")
    yield
    # Shutdown — nothing to clean up


app = FastAPI(
    title="RAG-RBAC Chatbot API",
    version="1.0.0",
    description="Enterprise chatbot with role-based access control, guardrails, and monitoring",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(health.router)
app.include_router(monitoring.router)
