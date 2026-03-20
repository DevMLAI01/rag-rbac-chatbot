from __future__ import annotations
import re
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# PII regex patterns (fallback when Presidio is not installed)
_PII_PATTERNS: list[tuple[str, str]] = [
    (r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b", "[EMAIL]"),
    (r"\b(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE]"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]"),
    (r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b", "[CREDIT_CARD]"),
    (r"\b(?:19|20)\d{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])\b", "[DATE]"),
    (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[IP_ADDRESS]"),
]


@dataclass
class PIIMatch:
    entity_type: str
    start: int
    end: int


@dataclass
class GuardrailResult:
    blocked: bool
    redacted_text: str = ""
    warning: str = ""
    pii_found: list[str] = field(default_factory=list)
    reason: str = ""


class PIIGuard:
    def __init__(self):
        self._presidio = self._try_load_presidio()

    def _try_load_presidio(self):
        try:
            from presidio_analyzer import AnalyzerEngine
            from presidio_anonymizer import AnonymizerEngine
            analyzer = AnalyzerEngine()
            anonymizer = AnonymizerEngine()
            logger.info("Presidio loaded for PII detection")
            return (analyzer, anonymizer)
        except ImportError:
            logger.info("Presidio not available — using regex PII detection")
            return None

    def detect(self, text: str) -> list[PIIMatch]:
        if self._presidio:
            analyzer, _ = self._presidio
            results = analyzer.analyze(text=text, language="en")
            return [PIIMatch(r.entity_type, r.start, r.end) for r in results]
        # Regex fallback
        matches = []
        for pattern, label in _PII_PATTERNS:
            for m in re.finditer(pattern, text):
                matches.append(PIIMatch(label.strip("[]"), m.start(), m.end()))
        return matches

    def redact(self, text: str) -> str:
        if self._presidio:
            analyzer, anonymizer = self._presidio
            results = analyzer.analyze(text=text, language="en")
            if not results:
                return text
            from presidio_anonymizer.entities import OperatorConfig
            anonymized = anonymizer.anonymize(
                text=text,
                analyzer_results=results,
                operators={"DEFAULT": OperatorConfig("replace", {"new_value": "[REDACTED]"})},
            )
            return anonymized.text
        # Regex fallback
        redacted = text
        for pattern, replacement in _PII_PATTERNS:
            redacted = re.sub(pattern, replacement, redacted)
        return redacted

    def check_query(self, query: str) -> GuardrailResult:
        matches = self.detect(query)
        if matches:
            types = list({m.entity_type for m in matches})
            redacted = self.redact(query)
            logger.warning("PII detected in query | types=%s", types)
            return GuardrailResult(
                blocked=False,
                redacted_text=redacted,
                warning=f"PII detected and redacted: {', '.join(types)}",
                pii_found=types,
            )
        return GuardrailResult(blocked=False, redacted_text=query)

    def check_response(self, answer: str) -> str:
        return self.redact(answer)


_pii_guard: PIIGuard | None = None


def get_pii_guard() -> PIIGuard:
    global _pii_guard
    if _pii_guard is None:
        _pii_guard = PIIGuard()
    return _pii_guard
