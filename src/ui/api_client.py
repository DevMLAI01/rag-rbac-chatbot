from __future__ import annotations
import os
import httpx

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
TIMEOUT = 60.0


class APIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    def login(self, username: str, password: str) -> dict:
        r = httpx.post(f"{self.base_url}/auth/login", json={"username": username, "password": password}, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()

    def query(self, token: str, query: str, conversation_id: str | None = None) -> dict:
        r = httpx.post(
            f"{self.base_url}/chat/query",
            json={"query": query, "conversation_id": conversation_id},
            headers={"Authorization": f"Bearer {token}"},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return r.json()

    def health(self) -> dict:
        try:
            r = httpx.get(f"{self.base_url}/health", timeout=5.0)
            return r.json()
        except Exception:
            return {"status": "unreachable"}

    def cost_summary(self, token: str) -> dict:
        r = httpx.get(f"{self.base_url}/monitoring/costs/summary",
                      headers={"Authorization": f"Bearer {token}"}, timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else {}

    def ragas_summary(self, token: str) -> dict:
        r = httpx.get(f"{self.base_url}/monitoring/ragas/summary",
                      headers={"Authorization": f"Bearer {token}"}, timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else {}
