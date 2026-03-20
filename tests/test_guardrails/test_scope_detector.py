"""Unit tests for out-of-scope query detection."""
import pytest
from guardrails.scope_detector import ScopeGuard

guard = ScopeGuard()


@pytest.mark.parametrize("query", [
    "Write me a Python script to scrape websites",
    "What is the weather in London today?",
    "Can you translate this to French?",
    "Generate an image of a cat",
    "Tell me today's sports news",
])
def test_out_of_scope_queries_are_blocked(query):
    result = guard.check(query)
    assert result.blocked, f"Expected blocked for: {query}"


@pytest.mark.parametrize("query", [
    "What was our Q1 revenue?",
    "Show me the marketing campaign performance",
    "What is the employee attendance rate?",
    "What are the company policies on remote work?",
    "What is the engineering team's deployment process?",
])
def test_in_scope_queries_are_allowed(query):
    result = guard.check(query)
    assert not result.blocked, f"Expected allowed for: {query}"
