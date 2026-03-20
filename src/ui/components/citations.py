import streamlit as st

DEPT_COLORS = {
    "finance":     "#28a745",
    "marketing":   "#fd7e14",
    "hr":          "#6f42c1",
    "engineering": "#007bff",
    "clevel":      "#dc3545",
    "general":     "#6c757d",
}


def render_citations(citations: list[dict]):
    if not citations:
        return
    with st.expander(f"View Sources ({len(citations)})"):
        for c in citations:
            dept = c.get("department", "")
            color = DEPT_COLORS.get(dept, "#6c757d")
            st.markdown(
                f'**{c.get("title", c.get("doc_id", "?"))}**  '
                f'`{c.get("doc_id", "")}` &nbsp;'
                f'<span style="background:{color};color:white;padding:2px 7px;border-radius:8px;font-size:0.8em;">'
                f'{dept}</span>  '
                f'`{c.get("source_file", "")}`',
                unsafe_allow_html=True,
            )
