import streamlit as st


def render_sidebar():
    """Branding compartilhado, exibido na sidebar de todas as páginas."""
    with st.sidebar:
        st.markdown("## 🪨 rosettAI")
        st.caption("Decifrando atestados médicos com IA.")
        st.divider()
