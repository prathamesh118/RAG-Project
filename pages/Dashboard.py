"""
Dashboard Page – Knowledge Copilot
Comprehensive overview of indexed knowledge, vector stats, and quick actions.
"""

import streamlit as st

st.set_page_config(
    page_title="Dashboard – Knowledge Copilot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared CSS & Sidebar ──────────────────────────────────────────────────────
from services.ui_helper import inject_custom_ui, render_sidebar, render_header

inject_custom_ui()
render_sidebar()

# ── Initialize DB ─────────────────────────────────────────────────────────────
from database.db import Base, engine, SessionLocal
import database.models  # noqa
Base.metadata.create_all(bind=engine)

from database.queries import (
    get_or_create_default_user,
    get_document_count,
    get_total_chunks,
    get_session_count,
    get_total_messages,
    get_all_documents,
    get_all_sessions,
)

if "user_id" not in st.session_state:
    db = SessionLocal()
    user = get_or_create_default_user(db)
    st.session_state.user_id = user.id
    db.close()

db = SessionLocal()
doc_count     = get_document_count(db)
chunk_count   = get_total_chunks(db)
session_count = get_session_count(db)
msg_count     = get_total_messages(db)
recent_docs   = get_all_documents(db)[:5]
recent_sessions = get_all_sessions(db)[:5]
db.close()

# ── Header ────────────────────────────────────────────────────────────────────
render_header("Intelligence Dashboard", "Overview of your indexed knowledge, vector embeddings & conversations", "🧠", badge="Gemini 2.5 Active")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.7) 100%); border: 1px solid rgba(99, 102, 241, 0.2); border-top: 3px solid #6366f1; border-radius: 18px; padding: 1.3rem 1.4rem; backdrop-filter: blur(14px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25); height: 100%;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#94a3b8;">DOCUMENTS</span>
            <span style="background:rgba(99, 102, 241, 0.15); color:#a5b4fc; padding:2px 8px; border-radius:9999px; font-size:0.68rem; font-weight:600;">INDEXED</span>
        </div>
        <div style="font-size:2.4rem; font-weight:800; font-family:'Outfit', sans-serif; color:#ffffff; line-height:1.1; margin-bottom:0.35rem;">
            {doc_count}
        </div>
        <div style="font-size:0.78rem; color:#64748b; font-weight:500;">
            Active knowledge sources
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.7) 100%); border: 1px solid rgba(139, 92, 246, 0.2); border-top: 3px solid #8b5cf6; border-radius: 18px; padding: 1.3rem 1.4rem; backdrop-filter: blur(14px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25); height: 100%;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#94a3b8;">CHUNKS</span>
            <span style="background:rgba(139, 92, 246, 0.15); color:#c4b5fd; padding:2px 8px; border-radius:9999px; font-size:0.68rem; font-weight:600;">384-DIM</span>
        </div>
        <div style="font-size:2.4rem; font-weight:800; font-family:'Outfit', sans-serif; color:#ffffff; line-height:1.1; margin-bottom:0.35rem;">
            {chunk_count}
        </div>
        <div style="font-size:0.78rem; color:#64748b; font-weight:500;">
            Vectorized in ChromaDB
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.7) 100%); border: 1px solid rgba(236, 72, 153, 0.2); border-top: 3px solid #ec4899; border-radius: 18px; padding: 1.3rem 1.4rem; backdrop-filter: blur(14px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25); height: 100%;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#94a3b8;">SESSIONS</span>
            <span style="background:rgba(236, 72, 153, 0.15); color:#f472b6; padding:2px 8px; border-radius:9999px; font-size:0.68rem; font-weight:600;">LIVE</span>
        </div>
        <div style="font-size:2.4rem; font-weight:800; font-family:'Outfit', sans-serif; color:#ffffff; line-height:1.1; margin-bottom:0.35rem;">
            {session_count}
        </div>
        <div style="font-size:0.78rem; color:#64748b; font-weight:500;">
            Conversational threads
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.7) 100%); border: 1px solid rgba(16, 185, 129, 0.2); border-top: 3px solid #10b981; border-radius: 18px; padding: 1.3rem 1.4rem; backdrop-filter: blur(14px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25); height: 100%;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#94a3b8;">MESSAGES</span>
            <span style="background:rgba(16, 185, 129, 0.15); color:#6ee7b7; padding:2px 8px; border-radius:9999px; font-size:0.68rem; font-weight:600;">GROUNDED</span>
        </div>
        <div style="font-size:2.4rem; font-weight:800; font-family:'Outfit', sans-serif; color:#ffffff; line-height:1.1; margin-bottom:0.35rem;">
            {msg_count}
        </div>
        <div style="font-size:0.78rem; color:#64748b; font-weight:500;">
            Queries & AI responses
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 1.8rem;'></div>", unsafe_allow_html=True)

# ── Quick Actions ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem;">
    <span style="font-size:1.3rem;">⚡</span>
    <h2 style="margin:0; font-size:1.3rem; font-weight:700; color:#f1f5f9 !important;">Quick Actions Hub</h2>
</div>
""", unsafe_allow_html=True)

qa1, qa2, qa3 = st.columns(3)

with qa1:
    st.markdown("""
    <div class="glass-card hover-lift" style="text-align:center; padding:1.8rem 1.4rem; margin-bottom:0.75rem; border-color:rgba(99, 102, 241, 0.25);">
        <div style="width:52px; height:52px; margin:0 auto 0.9rem; border-radius:14px; background:linear-gradient(135deg, #4f46e5, #3b82f6); display:flex; align-items:center; justify-content:center; font-size:1.8rem; box-shadow:0 6px 20px rgba(99, 102, 241, 0.35);">
            📤
        </div>
        <h3 style="margin:0 0 0.35rem; font-size:1.1rem; color:#ffffff !important; font-weight:700;">Upload Documents</h3>
        <p style="margin:0 0 0.5rem; font-size:0.82rem; color:#94a3b8 !important; min-height:38px;">
            Ingest and split PDFs, DOCX, TXT, CSV files into dense embeddings.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📤 Upload Documents →", key="dash_upload", type="primary", use_container_width=True):
        st.switch_page("pages/Upload.py")

with qa2:
    st.markdown("""
    <div class="glass-card hover-lift" style="text-align:center; padding:1.8rem 1.4rem; margin-bottom:0.75rem; border-color:rgba(139, 92, 246, 0.25);">
        <div style="width:52px; height:52px; margin:0 auto 0.9rem; border-radius:14px; background:linear-gradient(135deg, #8b5cf6, #d946ef); display:flex; align-items:center; justify-content:center; font-size:1.8rem; box-shadow:0 6px 20px rgba(139, 92, 246, 0.35);">
            💬
        </div>
        <h3 style="margin:0 0 0.35rem; font-size:1.1rem; color:#ffffff !important; font-weight:700;">Ask AI Copilot</h3>
        <p style="margin:0 0 0.5rem; font-size:0.82rem; color:#94a3b8 !important; min-height:38px;">
            Chat with Gemini 2.5 Flash grounded in your documents with citations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💬 Start Conversation →", key="dash_chat", type="primary", use_container_width=True):
        st.switch_page("pages/Chat.py")

with qa3:
    st.markdown("""
    <div class="glass-card hover-lift" style="text-align:center; padding:1.8rem 1.4rem; margin-bottom:0.75rem; border-color:rgba(16, 185, 129, 0.25);">
        <div style="width:52px; height:52px; margin:0 auto 0.9rem; border-radius:14px; background:linear-gradient(135deg, #10b981, #06b6d4); display:flex; align-items:center; justify-content:center; font-size:1.8rem; box-shadow:0 6px 20px rgba(16, 185, 129, 0.35);">
            📚
        </div>
        <h3 style="margin:0 0 0.35rem; font-size:1.1rem; color:#ffffff !important; font-weight:700;">Knowledge Base</h3>
        <p style="margin:0 0 0.5rem; font-size:0.82rem; color:#94a3b8 !important; min-height:38px;">
            Inspect indexed chunks, verify metadata, or manage documents.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📚 Explore Knowledge →", key="dash_kb", type="primary", use_container_width=True):
        st.switch_page("pages/Knowledge_base.py")

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# ── Recent Activity ───────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.9rem;">
        <div style="display:flex; align-items:center; gap:0.5rem;">
            <span style="font-size:1.2rem;">📄</span>
            <h3 style="margin:0; font-size:1.15rem; font-weight:700; color:#f1f5f9 !important;">Recent Documents</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if recent_docs:
        for doc in recent_docs:
            ext = (doc.document_type or "doc").upper()
            ext_color = "#f43f5e" if "PDF" in ext else ("#3b82f6" if "DOC" in ext else "#10b981")
            st.markdown(f"""
            <div class="glass-card hover-lift" style="padding:0.9rem 1.1rem; margin-bottom:0.6rem; display:flex; align-items:center; gap:0.9rem; border-radius:14px;">
                <div style="background:{ext_color}18; color:{ext_color}; border:1px solid {ext_color}40; border-radius:8px; padding:4px 8px; font-size:0.72rem; font-weight:800; letter-spacing:0.04em;">
                    {ext}
                </div>
                <div style="flex:1; min-width:0;">
                    <p style="margin:0; color:#f1f5f9 !important; font-weight:600; font-size:0.88rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{doc.filename}</p>
                    <p style="margin:0.15rem 0 0; color:#64748b !important; font-size:0.75rem;">
                        <span style="color:#94a3b8;">{doc.total_chunks or 0} chunks</span> · Collection: <span style="color:#818cf8;">{doc.collection or 'General'}</span>
                    </p>
                </div>
                <span style="background:rgba(16,185,129,0.12); color:#34d399; border:1px solid rgba(16,185,129,0.3); border-radius:9999px; padding:0.2rem 0.6rem; font-size:0.7rem; font-weight:600; white-space:nowrap;">
                    ✓ Ready
                </span>
            </div>
            """, unsafe_allow_html=True)
        if st.button("View all documents in Knowledge Base →", key="view_all_docs", use_container_width=True):
            st.switch_page("pages/Knowledge_base.py")
    else:
        st.markdown("""
        <div style="background:rgba(17,24,39,0.4); border:1px dashed rgba(99,102,241,0.25); border-radius:16px; padding:2.5rem; text-align:center;">
            <div style="font-size:2.2rem; margin-bottom:0.5rem;">📂</div>
            <p style="color:#f1f5f9 !important; font-weight:600; font-size:0.95rem; margin:0 0 0.25rem;">No documents uploaded yet</p>
            <p style="color:#64748b !important; font-size:0.8rem; margin:0 0 1rem;">Upload PDFs, Word files or text notes to enable semantic search.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Upload Your First Document", key="empty_dash_upload", use_container_width=True):
            st.switch_page("pages/Upload.py")

with col_right:
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.9rem;">
        <div style="display:flex; align-items:center; gap:0.5rem;">
            <span style="font-size:1.2rem;">💬</span>
            <h3 style="margin:0; font-size:1.15rem; font-weight:700; color:#f1f5f9 !important;">Recent Chat Sessions</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if recent_sessions:
        for sess in recent_sessions:
            created = sess.created_at.strftime("%b %d, %Y") if sess.created_at else "Recent"
            col_sess_info, col_sess_btn = st.columns([4, 2])
            with col_sess_info:
                st.markdown(f"""
                <div class="glass-card hover-lift" style="padding:0.9rem 1.1rem; margin-bottom:0.6rem; display:flex; align-items:center; gap:0.8rem; border-radius:14px;">
                    <div style="width:36px; height:36px; border-radius:10px; background:rgba(139,92,246,0.15); border:1px solid rgba(139,92,246,0.3); display:flex; align-items:center; justify-content:center; font-size:1.1rem;">
                        💬
                    </div>
                    <div style="flex:1; min-width:0;">
                        <p style="margin:0; color:#f1f5f9 !important; font-weight:600; font-size:0.88rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{sess.session_name}</p>
                        <p style="margin:0.15rem 0 0; color:#64748b !important; font-size:0.75rem;">Created: {created}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_sess_btn:
                if st.button("Resume →", key=f"dash_resume_{sess.id}", use_container_width=True):
                    st.session_state.active_session_id = sess.id
                    st.switch_page("pages/Chat.py")
        if st.button("Start a new chat session →", key="view_new_chat", use_container_width=True):
            st.switch_page("pages/Chat.py")
    else:
        st.markdown("""
        <div style="background:rgba(17,24,39,0.4); border:1px dashed rgba(139,92,246,0.25); border-radius:16px; padding:2.5rem; text-align:center;">
            <div style="font-size:2.2rem; margin-bottom:0.5rem;">💬</div>
            <p style="color:#f1f5f9 !important; font-weight:600; font-size:0.95rem; margin:0 0 0.25rem;">No active chat sessions</p>
            <p style="color:#64748b !important; font-size:0.8rem; margin:0 0 1rem;">Ask questions and get intelligent answers with document citations.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start New Conversation", key="empty_dash_chat", use_container_width=True):
            st.switch_page("pages/Chat.py")

st.markdown("<div style='height: 2.2rem;'></div>", unsafe_allow_html=True)

# ── RAG Architecture Pipeline ─────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem;">
    <span style="font-size:1.3rem;">⚡</span>
    <h2 style="margin:0; font-size:1.3rem; font-weight:700; color:#f1f5f9 !important;">How Knowledge Copilot Works</h2>
</div>
""", unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)
pipeline_steps = [
    ("1", "📥 Document Ingestion", "Upload PDF, DOCX, TXT, CSV files. Text and tables are extracted cleanly.", "#6366f1"),
    ("2", "✂️ Smart Chunking", "Splits long texts into semantically coherent 500-char chunks with overlap.", "#8b5cf6"),
    ("3", "🧬 Vector Embeddings", "BAAI/bge-small-en-v1.5 generates dense 384-dim embeddings stored in ChromaDB.", "#ec4899"),
    ("4", "⚡ Gemini 2.5 Flash", "Retrieved chunks are grounded into precise answers with source citations.", "#10b981"),
]

for col, (num, title, desc, accent) in zip([p1, p2, p3, p4], pipeline_steps):
    col.markdown(f"""
    <div class="glass-card hover-lift" style="padding:1.4rem 1.2rem; height:180px; display:flex; flex-direction:column; justify-content:space-between; border-top:3px solid {accent};">
        <div>
            <div style="display:inline-flex; align-items:center; justify-content:center; width:26px; height:26px; border-radius:50%; background:{accent}20; color:{accent}; font-weight:800; font-size:0.75rem; margin-bottom:0.6rem;">
                {num}
            </div>
            <h4 style="margin:0 0 0.4rem; font-size:0.95rem; font-weight:700; color:#ffffff !important;">{title}</h4>
            <p style="margin:0; color:#94a3b8 !important; font-size:0.78rem; line-height:1.45;">{desc}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
