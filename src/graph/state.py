from typing import TypedDict


class RBACChatState(TypedDict):
    # ── Input ─────────────────────────────────────────────────────────────────
    jwt_token: str
    query: str
    request_id: str

    # ── Auth ──────────────────────────────────────────────────────────────────
    user_id: str
    role: str
    auth_valid: bool
    auth_error: str | None

    # ── Guardrails ────────────────────────────────────────────────────────────
    pii_detected: bool
    guardrail_blocked: bool
    guardrail_warning: str

    # ── Retrieval ─────────────────────────────────────────────────────────────
    retrieved_docs: list[dict]   # {"content": str, "metadata": dict}
    retrieval_count: int

    # ── Generation ────────────────────────────────────────────────────────────
    answer: str
    citations: list[dict]        # {"doc_id": str, "title": str, "source_file": str}

    # ── Cost monitoring ───────────────────────────────────────────────────────
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    cost_alert_triggered: bool
    cost_alerts: list[str]

    # ── Control flow ──────────────────────────────────────────────────────────
    error_message: str | None
    is_terminal: bool
