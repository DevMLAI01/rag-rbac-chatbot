"""Unit tests for PII detection and redaction."""
import pytest
from guardrails.pii_detector import PIIGuard

guard = PIIGuard()


def test_email_is_redacted():
    result = guard.redact("Contact john@example.com for details")
    assert "john@example.com" not in result
    assert "[EMAIL" in result or "EMAIL" in result


def test_phone_is_redacted():
    result = guard.redact("Call me at 555-123-4567")
    assert "555-123-4567" not in result


def test_clean_text_unchanged():
    text = "What was our Q1 revenue?"
    result = guard.redact(text)
    assert result == text


def test_check_query_detects_pii():
    result = guard.check_query("What is john@example.com's salary?")
    assert result.warning is not None or "EMAIL" in result.redacted_text


def test_check_query_clean_passes():
    result = guard.check_query("What are our Q1 financials?")
    assert not result.blocked
