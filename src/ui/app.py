import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
from src.ui.api_client import APIClient
from src.ui.components.login import render_login
from src.ui.components.sidebar import render_sidebar
from src.ui.components.citations import render_citations

st.set_page_config(
    page_title="RAG-RBAC Chatbot",
    page_icon="🔐",
    layout="wide",
)

client = APIClient()

# ── Session state defaults ────────────────────────────────────────────────────
for key, default in [
    ("access_token", None), ("role", None), ("username", None),
    ("messages", []), ("conversation_id", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Route ─────────────────────────────────────────────────────────────────────
if not st.session_state.access_token:
    render_login(client)
    st.stop()

render_sidebar()

st.title("Enterprise Knowledge Assistant")

# API health check
health = client.health()
if health.get("status") != "healthy":
    st.error("API is not reachable at localhost:8000. Make sure the FastAPI server is running.")
    st.stop()

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("citations"):
            render_citations(msg["citations"])
        if msg.get("cost"):
            st.caption(f"Cost: ${msg['cost']:.5f} | Tokens: {msg.get('tokens', 0)}")
        if msg.get("guardrail_warning"):
            st.warning(f"Note: {msg['guardrail_warning']}")

# ── Input ─────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question about company data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving and generating answer..."):
            try:
                result = client.query(
                    st.session_state.access_token,
                    prompt,
                    st.session_state.conversation_id,
                )
                st.session_state.conversation_id = result.get("conversation_id")
                answer = result.get("answer", "No answer returned.")
                citations = result.get("citations", [])
                cost = result.get("estimated_cost_usd", 0.0)
                tokens = result.get("retrieval_count", 0)
                warning = result.get("guardrail_warning", "")

                st.markdown(answer)
                render_citations(citations)
                if cost:
                    st.caption(f"Cost: ${cost:.5f}")
                if warning:
                    st.warning(f"Note: {warning}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "citations": citations,
                    "cost": cost,
                    "guardrail_warning": warning,
                })

                if result.get("cost_alert_triggered"):
                    st.error("Cost alert triggered for this request. Admin has been notified.")

            except Exception as e:
                err = f"Error: {e}"
                st.error(err)
                st.session_state.messages.append({"role": "assistant", "content": err})
