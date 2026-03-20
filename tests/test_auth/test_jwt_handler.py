"""Unit tests for JWT encode/decode round-trip."""
import pytest
from src.auth.jwt_handler import create_token, decode_token


def test_token_round_trip():
    token = create_token(user_id="user1", role="finance")
    decoded = decode_token(token)
    assert decoded.sub == "user1"
    assert decoded.role == "finance"


def test_invalid_token_raises():
    with pytest.raises(Exception):
        decode_token("not.a.valid.token")


def test_tampered_token_raises():
    token = create_token(user_id="user1", role="finance")
    tampered = token[:-5] + "XXXXX"
    with pytest.raises(Exception):
        decode_token(tampered)
