from src.graph.state import RBACChatState


def after_auth(state: RBACChatState) -> str:
    return "guardrail_input" if state.get("auth_valid") else "error"


def after_guardrail_input(state: RBACChatState) -> str:
    return "error" if state.get("guardrail_blocked") else "validate_query"


def after_validate(state: RBACChatState) -> str:
    return "error" if state.get("error_message") else "retrieve"


def after_retrieve(state: RBACChatState) -> str:
    return "error" if state.get("retrieval_count", 0) == 0 else "generate"


def after_generate(state: RBACChatState) -> str:
    return "error" if state.get("error_message") else "guardrail_output"
