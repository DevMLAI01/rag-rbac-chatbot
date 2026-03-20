import streamlit as st
from src.ui.api_client import APIClient

DEMO_ACCOUNTS = [
    ("finance_user", "finance"),
    ("marketing_user", "marketing"),
    ("hr_user", "hr"),
    ("eng_user", "engineering"),
    ("ceo", "clevel"),
    ("employee1", "employee"),
]


def render_login(client: APIClient):
    st.title("RAG-RBAC Enterprise Chatbot")
    st.markdown("---")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        if not username or not password:
            st.error("Please enter username and password.")
            return
        try:
            result = client.login(username, password)
            st.session_state.access_token   = result["access_token"]
            st.session_state.role           = result["role"]
            st.session_state.username       = username
            st.session_state.conversation_id = None
            st.session_state.messages       = []
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")

    st.markdown("---")
    st.caption("**Demo accounts** (all use password: `Password123`)")
    cols = st.columns(3)
    for i, (user, role) in enumerate(DEMO_ACCOUNTS):
        cols[i % 3].code(f"{user}\n({role})")
