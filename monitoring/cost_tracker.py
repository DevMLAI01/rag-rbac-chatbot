from __future__ import annotations

COST_PER_1M: dict[str, dict[str, float]] = {
    "gpt-4o":            {"input": 2.50,  "output": 10.00},
    "gpt-4o-mini":       {"input": 0.15,  "output": 0.60},
    "claude-sonnet-4-6": {"input": 3.00,  "output": 15.00},
    "claude-opus-4-6":   {"input": 15.00, "output": 75.00},
    "claude-haiku-4-5":  {"input": 0.80,  "output": 4.00},
}


def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    rates = COST_PER_1M.get(model, {"input": 3.00, "output": 15.00})
    return (prompt_tokens * rates["input"] + completion_tokens * rates["output"]) / 1_000_000


def extract_token_usage(llm_response) -> tuple[int, int]:
    """Extract (prompt_tokens, completion_tokens) from an LLM response object."""
    try:
        usage = llm_response.usage_metadata
        return usage.get("input_tokens", 0), usage.get("output_tokens", 0)
    except AttributeError:
        pass
    try:
        usage = llm_response.response_metadata.get("usage", {})
        return usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
    except AttributeError:
        return 0, 0
