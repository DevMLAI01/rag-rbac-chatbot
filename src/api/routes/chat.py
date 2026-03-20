from __future__ import annotations
import asyncio
import uuid
from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from src.api.dependencies import get_current_user, get_graph, get_raw_token
from src.auth.models import TokenPayload

router = APIRouter(prefix="/chat", tags=["chat"])


class QueryRequest(BaseModel):
    query: str
    conversation_id: str | None = None


class QueryResponse(BaseModel):
    answer: str
    citations: list[dict]
    role: str
    retrieval_count: int
    conversation_id: str
    estimated_cost_usd: float
    cost_alert_triggered: bool
    guardrail_warning: str


@router.post("/query", response_model=QueryResponse)
async def query(
    body: QueryRequest,
    background_tasks: BackgroundTasks,
    user: TokenPayload = Depends(get_current_user),
    raw_token: str = Depends(get_raw_token),
    graph=Depends(get_graph),
):
    request_id = str(uuid.uuid4())
    conversation_id = body.conversation_id or str(uuid.uuid4())

    initial_state = {
        "jwt_token":           raw_token,  # graph re-validates for defense-in-depth
        "query":               body.query,
        "request_id":          request_id,
        "user_id":             user.sub,
        "role":                user.role,
        "auth_valid":          True,
        "auth_error":          None,
        "pii_detected":        False,
        "guardrail_blocked":   False,
        "guardrail_warning":   "",
        "retrieved_docs":      [],
        "retrieval_count":     0,
        "answer":              "",
        "citations":           [],
        "prompt_tokens":       0,
        "completion_tokens":   0,
        "total_tokens":        0,
        "estimated_cost_usd":  0.0,
        "cost_alert_triggered": False,
        "cost_alerts":         [],
        "error_message":       None,
        "is_terminal":         False,
    }

    result = await asyncio.to_thread(graph.invoke, initial_state)

    # Fire-and-forget Ragas evaluation
    if result.get("retrieval_count", 0) > 0 and result.get("answer"):
        from evaluation.ragas_evaluator import evaluate_response
        contexts = [d["content"] for d in result.get("retrieved_docs", [])]
        background_tasks.add_task(
            evaluate_response,
            request_id, user.sub, user.role,
            body.query, result["answer"], contexts,
        )

    return QueryResponse(
        answer=result.get("answer", ""),
        citations=result.get("citations", []),
        role=user.role,
        retrieval_count=result.get("retrieval_count", 0),
        conversation_id=conversation_id,
        estimated_cost_usd=result.get("estimated_cost_usd", 0.0),
        cost_alert_triggered=result.get("cost_alert_triggered", False),
        guardrail_warning=result.get("guardrail_warning", ""),
    )
