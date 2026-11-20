"""
Knowledge Copilot – Main Streamlit Entry Point
"""

import streamlit as st

# Must be first Streamlit call
st.set_page_config(
    page_title="Knowledge Copilot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database on startup
from database.db import Base, engine
import database.models  # noqa: F401 – registers all models
Base.metadata.create_all(bind=engine)

# Initialize default user in session
from database.db import SessionLocal
from database.queries import get_or_create_default_user

if "user_id" not in st.session_state:
    db = SessionLocal()
    try:
        user = get_or_create_default_user(db)
        st.session_state.user_id = user.id
    finally:
        db.close()

# ── Global CSS ──────────────────────────────────────────────────────────────
from services.ui_helper import inject_custom_ui, render_sidebar

inject_custom_ui()

# ── Sidebar ─────────────────────────────────────────────────────────────────
render_sidebar()

# ── Home redirect ────────────────────────────────────────────────────────────
st.switch_page("pages/Dashboard.py")

