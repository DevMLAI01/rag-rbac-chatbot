from __future__ import annotations
import re
import logging
from datetime import datetime, timezone
from typing import Any

from src.graph.state import RBACChatState
from config.settings import settings

logger = logging.getLogger(__name__)

INJECTION_PATTERNS = [
    r"ignore.{0,30}(previous|above|prior).{0,20}instruction",
    r"system\s*:",
    r"<\|im_start\|>",
    r"you are now",
    r"forget.{0,20}(everything|all|previous)",
    r"disregard.{0,20}instruction",
    r"new\s+persona",
    r"pretend.{0,20}(you are|to be)",
]


# ── Node 1: Authenticate ───────────────────────────────────────────────────────

def authenticate_node(state: RBACChatState) -> dict[str, Any]:
    from src.auth.jwt_handler import decode_token
    from jose import JWTError
    try:
        payload = decode_token(state["jwt_token"])
        return {"user_id": payload.sub, "role": payload.role, "auth_valid": True, "auth_error": None}
    except Exception as e:
        return {"auth_valid": False, "auth_error": str(e), "error_message": "Authentication failed."}


# ── Node 2: Guardrail Input ────────────────────────────────────────────────────

def guardrail_input_node(state: RBACChatState) -> dict[str, Any]:
    from guardrails.guardrail_chain import get_guardrail_chain
    from monitoring.metrics_store import insert_guardrail_event

    chain = get_guardrail_chain()
    result = chain.check_input(state["query"], state.get("role", ""))

    if result.blocked:
        insert_guardrail_event({
            "request_id": state["request_id"],
            "user_id": state.get("user_id", "unknown"),
            "role": state.get("role", "unknown"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "guard_type": "scope",
            "action": "blocked",
            "reason": result.reason,
        })
        return {
            "guardrail_blocked": True,
            "error_message": result.warning or "Query out of scope.",
        }

    updates: dict[str, Any] = {"guardrail_blocked": False, "query": result.redacted_text}
    if result.pii_found:
        updates["pii_detected"] = True
        updates["guardrail_warning"] = result.warning
        insert_guardrail_event({
            "request_id": state["request_id"],
            "user_id": state.get("user_id", "unknown"),
            "role": state.get("role", "unknown"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "guard_type": "pii",
            "action": "redacted",
            "reason": f"PII types: {', '.join(result.pii_found)}",
        })
    else:
        updates["pii_detected"] = False
    return updates


# ── Node 3: Validate Query ────────────────────────────────────────────────────

def validate_query_node(state: RBACChatState) -> dict[str, Any]:
    query = state["query"].strip()
    if not query:
        return {"error_message": "Query cannot be empty."}
    if len(query) > 2000:
        return {"error_message": "Query too long (max 2000 characters)."}
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, query, re.IGNORECASE):
            logger.warning("Prompt injection attempt | user=%s", state.get("user_id"))
            return {"error_message": "Invalid query."}
    return {"query": query}


# ── Node 4: Retrieve ──────────────────────────────────────────────────────────

def retrieve_node(state: RBACChatState) -> dict[str, Any]:
    from src.retrieval.retriever import get_retriever
    retriever = get_retriever()
    docs = retriever.retrieve(state["query"], state["role"])
    formatted = [
        {"content": doc.page_content, "metadata": doc.metadata}
        for doc in docs
    ]
    return {"retrieved_docs": formatted, "retrieval_count": len(formatted)}


# ── Node 5: Generate ──────────────────────────────────────────────────────────

def generate_node(state: RBACChatState) -> dict[str, Any]:
    context_parts = []
    for i, doc in enumerate(state["retrieved_docs"], 1):
        meta = doc["metadata"]
        context_parts.append(
            f"[{i}] Source: {meta.get('doc_id','?')} | {meta.get('title','?')}\n{doc['content']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    system_prompt = f"""You are an enterprise knowledge assistant. The current user has role: {state['role'].upper()}.

RULES:
1. Answer ONLY using the provided context below.
2. Cite every factual claim with [Source: doc_id] inline.
3. If the context does not contain the answer, respond: "I don't have that information in my authorized knowledge base."
4. Do NOT reveal the existence of documents you cannot access.
5. Never speculate or use knowledge outside the context.

CONTEXT:
{context}"""

    user_message = state["query"]

    if settings.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(
            model=settings.llm_model,
            anthropic_api_key=settings.anthropic_api_key,
            max_tokens=1024,
        )
    else:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model=settings.llm_model,
            openai_api_key=settings.openai_api_key,
            max_tokens=1024,
        )

    try:
        from langchain_core.messages import SystemMessage, HumanMessage
        response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_message)])
        answer = response.content

        from monitoring.cost_tracker import extract_token_usage
        prompt_tokens, completion_tokens = extract_token_usage(response)

        return {
            "answer": answer,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        }
    except Exception as e:
        logger.error("LLM call failed: %s", e)
        return {"error_message": "The AI service is temporarily unavailable. Please try again later."}


# ── Node 6: Guardrail Output ──────────────────────────────────────────────────

def guardrail_output_node(state: RBACChatState) -> dict[str, Any]:
    from guardrails.guardrail_chain import get_guardrail_chain
    chain = get_guardrail_chain()
    clean_answer = chain.check_output(state["answer"])
    return {"answer": clean_answer}


# ── Node 7: Extract Citations ──────────────────────────────────────────────────

def extract_citations_node(state: RBACChatState) -> dict[str, Any]:
    answer = state["answer"]
    cited_ids = set(re.findall(r"\[Source:\s*([^\]]+)\]", answer))
    citations = []
    for doc in state["retrieved_docs"]:
        meta = doc["metadata"]
        if meta.get("doc_id") in cited_ids:
            citations.append({
                "doc_id": meta.get("doc_id", ""),
                "title": meta.get("title", ""),
                "source_file": meta.get("source_file", ""),
                "department": meta.get("department", ""),
            })
    return {"citations": citations}


# ── Node 8: Cost Tracking ──────────────────────────────────────────────────────

def cost_tracking_node(state: RBACChatState) -> dict[str, Any]:
    from monitoring.cost_tracker import calculate_cost
    from monitoring.cost_alerts import check_alerts
    from monitoring.metrics_store import insert_cost

    cost = calculate_cost(settings.llm_model, state.get("prompt_tokens", 0), state.get("completion_tokens", 0))
    alerts = check_alerts(state.get("user_id", ""), state.get("role", ""), cost)

    insert_cost({
        "request_id": state["request_id"],
        "user_id": state.get("user_id", ""),
        "role": state.get("role", ""),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt_tokens": state.get("prompt_tokens", 0),
        "completion_tokens": state.get("completion_tokens", 0),
        "total_tokens": state.get("total_tokens", 0),
        "model": settings.llm_model,
        "estimated_cost_usd": cost,
        "cost_alert_triggered": int(bool(alerts)),
    })

    return {
        "estimated_cost_usd": cost,
        "cost_alerts": alerts,
        "cost_alert_triggered": bool(alerts),
    }


# ── Node 9: Error ─────────────────────────────────────────────────────────────

def error_node(state: RBACChatState) -> dict[str, Any]:
    logger.error("Error node | user=%s error=%s", state.get("user_id"), state.get("error_message"))
    return {
        "answer": state.get("error_message") or "Sorry, I could not process your request.",
        "citations": [],
        "is_terminal": True,
    }
