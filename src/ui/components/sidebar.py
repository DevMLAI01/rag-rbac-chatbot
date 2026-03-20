import streamlit as st

ROLE_COLORS = {
    "finance":     "#28a745",
    "marketing":   "#fd7e14",
    "hr":          "#6f42c1",
    "engineering": "#007bff",
    "clevel":      "#dc3545",
    "employee":    "#6c757d",
}

ROLE_ACCESS = {
    "finance":     "Finance docs + General",
    "marketing":   "Marketing docs + General",
    "hr":          "HR docs + General",
    "engineering": "Engineering docs + General",
    "clevel":      "ALL departments",
    "employee":    "General only",
}


def render_sidebar():
    role  = st.session_state.get("role", "")
    user  = st.session_state.get("username", "")
    color = ROLE_COLORS.get(role, "#6c757d")

    with st.sidebar:
        st.markdown(f"**Logged in as:** `{user}`")
        st.markdown(
            f'<span style="background:{color};color:white;padding:4px 10px;border-radius:12px;font-weight:bold;">'
            f'{role.upper()}</span>',
            unsafe_allow_html=True,
        )
        st.caption(f"Access: {ROLE_ACCESS.get(role, '—')}")
        st.markdown("---")

        if st.button("Logout", use_container_width=True):
            for key in ["access_token", "role", "username", "messages", "conversation_id"]:
                st.session_state.pop(key, None)
            st.rerun()
