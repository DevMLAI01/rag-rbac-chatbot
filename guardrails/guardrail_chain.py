from __future__ import annotations
from guardrails.pii_detector import GuardrailResult, get_pii_guard
from guardrails.scope_detector import get_scope_guard


class GuardrailChain:
    def __init__(self):
        self.pii_guard = get_pii_guard()
        self.scope_guard = get_scope_guard()

    def check_input(self, query: str, role: str = "") -> GuardrailResult:
        """Run scope check then PII check. Returns result with redacted query."""
        scope = self.scope_guard.check(query)
        if scope.blocked:
            return scope
        return self.pii_guard.check_query(query)

    def check_output(self, answer: str) -> str:
        """Always redact PII from LLM answers."""
        return self.pii_guard.check_response(answer)


_chain: GuardrailChain | None = None


def get_guardrail_chain() -> GuardrailChain:
    global _chain
    if _chain is None:
        _chain = GuardrailChain()
    return _chain
