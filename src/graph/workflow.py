from __future__ import annotations
from langgraph.graph import StateGraph, START, END
from src.graph.state import RBACChatState
from src.graph.nodes import (
    authenticate_node,
    guardrail_input_node,
    validate_query_node,
    retrieve_node,
    generate_node,
    guardrail_output_node,
    extract_citations_node,
    cost_tracking_node,
    error_node,
)
from src.graph.edges import after_auth, after_guardrail_input, after_validate, after_retrieve, after_generate

_graph = None


def compile_workflow():
    builder = StateGraph(RBACChatState)

    builder.add_node("authenticate",      authenticate_node)
    builder.add_node("guardrail_input",   guardrail_input_node)
    builder.add_node("validate_query",    validate_query_node)
    builder.add_node("retrieve",          retrieve_node)
    builder.add_node("generate",          generate_node)
    builder.add_node("guardrail_output",  guardrail_output_node)
    builder.add_node("extract_citations", extract_citations_node)
    builder.add_node("cost_tracking",     cost_tracking_node)
    builder.add_node("error",             error_node)

    builder.add_edge(START, "authenticate")
    builder.add_conditional_edges("authenticate",    after_auth,            {"guardrail_input": "guardrail_input", "error": "error"})
    builder.add_conditional_edges("guardrail_input", after_guardrail_input, {"validate_query": "validate_query",   "error": "error"})
    builder.add_conditional_edges("validate_query",  after_validate,        {"retrieve": "retrieve",               "error": "error"})
    builder.add_conditional_edges("retrieve",        after_retrieve,        {"generate": "generate",               "error": "error"})
    builder.add_conditional_edges("generate", after_generate, {"guardrail_output": "guardrail_output", "error": "error"})
    builder.add_edge("guardrail_output",  "extract_citations")
    builder.add_edge("extract_citations", "cost_tracking")
    builder.add_edge("cost_tracking",     END)
    builder.add_edge("error",             END)

    return builder.compile()


def get_graph():
    global _graph
    if _graph is None:
        _graph = compile_workflow()
    return _graph
