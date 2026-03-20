from __future__ import annotations
import re
import logging
from guardrails.pii_detector import GuardrailResult

logger = logging.getLogger(__name__)

IN_SCOPE_TOPICS = {
    "finance", "budget", "revenue", "expense", "payroll", "salary", "cost",
    "reimbursement", "invoice", "capex", "opex", "profit", "loss", "ebitda",
    "marketing", "campaign", "sales", "customer", "lead", "pipeline", "deal",
    "nps", "churn", "retention", "conversion", "impression", "ctr", "roas",
    "hr", "employee", "attendance", "performance", "leave", "vacation", "hire",
    "onboarding", "review", "promotion", "payroll", "benefits", "headcount",
    "engineering", "architecture", "deployment", "incident", "service", "api",
    "sprint", "feature", "bug", "release", "infrastructure", "monitoring",
    "company", "policy", "event", "faq", "office", "holiday", "training",
    "report", "quarter", "annual", "q1", "q2", "q3", "q4", "2024", "2023",
}

OUT_OF_SCOPE_PATTERNS = [
    r"\b(recipe|cooking|food|restaurant|meal prep)\b",
    r"\b(weather|forecast|temperature|climate)\b",
    r"\b(sports?|football|basketball|soccer|cricket|nba|nfl)\b",
    r"\b(movie|film|tv show|netflix|music|song)\b",
    r"\b(hack|exploit|vulnerability|malware|ransomware|phishing how)\b",
    r"\b(generate.{0,20}image|create.{0,20}image|draw|paint)\b",
    r"\b(translate|translation)\b",
    r"\b(write.{0,20}(story|poem|essay|novel))\b",
    r"\b(stock market|crypto|bitcoin|invest in)\b",
    r"\b(medical advice|diagnosis|symptoms|treatment)\b",
]


class ScopeGuard:
    def check(self, query: str) -> GuardrailResult:
        q_lower = query.lower()

        # Regex blocklist check
        for pattern in OUT_OF_SCOPE_PATTERNS:
            if re.search(pattern, q_lower, re.IGNORECASE):
                logger.info("Out-of-scope query blocked | pattern=%s", pattern)
                return GuardrailResult(
                    blocked=True,
                    reason="out_of_scope",
                    warning="I can only assist with company business queries.",
                )

        # Keyword overlap heuristic for longer queries
        tokens = set(re.findall(r"\b\w+\b", q_lower))
        overlap = tokens & IN_SCOPE_TOPICS
        if len(tokens) > 6 and not overlap:
            logger.info("Out-of-scope query blocked (no keyword overlap) | query=%s", query[:80])
            return GuardrailResult(
                blocked=True,
                reason="out_of_scope",
                warning="I can only assist with company business queries.",
            )

        return GuardrailResult(blocked=False, redacted_text=query)


_scope_guard: ScopeGuard | None = None


def get_scope_guard() -> ScopeGuard:
    global _scope_guard
    if _scope_guard is None:
        _scope_guard = ScopeGuard()
    return _scope_guard
