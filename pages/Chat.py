"""
Chat Page – RAG-powered conversation
"""

import os
import streamlit as st

st.set_page_config(
    page_title="Chat – Knowledge Copilot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared CSS ───────────────────────────────────────────────────────────────
from services.ui_helper import inject_custom_ui, render_header, render_sidebar_branding

inject_custom_ui()

# ── DB Init ───────────────────────────────────────────────────────────────────
from database.db import Base, engine, SessionLocal
import database.models  # noqa
Base.metadata.create_all(bind=engine)

from database.queries import (
    get_or_create_default_user,
    get_all_sessions,
    create_session,
    delete_session,
    get_messages_by_session,
    add_message,
    get_document_count,
    get_all_documents,
)
from database.models import ChatMessage
from config import settings

if "user_id" not in st.session_state:
    db = SessionLocal()
    user = get_or_create_default_user(db)
    st.session_state.user_id = user.id
    db.close()

if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "collection" not in st.session_state:
    st.session_state.collection = "General"

# ── Get collections from DB ───────────────────────────────────────────────────
db = SessionLocal()
all_docs = get_all_documents(db)
doc_count = get_document_count(db)
existing_collections = sorted(list(set(d.collection or "General" for d in all_docs)))
if "General" not in existing_collections:
    existing_collections.insert(0, "General")
db.close()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    render_sidebar_branding()

    st.page_link("pages/Dashboard.py", label="🏠 Dashboard")
    st.page_link("pages/Chat.py",      label="💬 Chat")
    st.page_link("pages/Upload.py",    label="📤 Upload")
    st.page_link("pages/Knowledge_base.py", label="📚 Knowledge Base")
    st.page_link("pages/Setting.py",   label="⚙️ Settings")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📁 Target Collection")

    # Collection selector
    sel_idx = existing_collections.index(st.session_state.collection) if st.session_state.collection in existing_collections else 0
    chosen_coll = st.selectbox(
        "Active Collection",
        existing_collections,
        index=sel_idx,
        label_visibility="collapsed",
    )
    if chosen_coll != st.session_state.collection:
        st.session_state.collection = chosen_coll
        st.rerun()

    st.markdown("<hr style='border-color:rgba(99,102,241,0.15); margin: 1rem 0;'>", unsafe_allow_html=True)
    st.markdown("### 💬 Chat Sessions")

    # New session button
    if st.button("＋ New Session", type="primary", use_container_width=True, key="new_sess"):
        db = SessionLocal()
        sess = create_session(db, f"Chat {len(get_all_sessions(db)) + 1}", st.session_state.user_id)
        db.close()
        st.session_state.active_session_id = sess.id
        st.session_state.messages = []
        st.rerun()

    # Session list
    db = SessionLocal()
    sessions = get_all_sessions(db)
    db.close()

    for sess in sessions:
        is_active = st.session_state.active_session_id == sess.id
        sess_label = f"{'▶ ' if is_active else ''}{sess.session_name}"
        col_s, col_d = st.columns([5, 1])
        with col_s:
            if st.button(sess_label, key=f"sess_{sess.id}", use_container_width=True):
                st.session_state.active_session_id = sess.id
                db2 = SessionLocal()
                msgs = get_messages_by_session(db2, sess.id)
                db2.close()
                st.session_state.messages = [
                    {"role": m.role, "content": m.message} for m in msgs
                ]
                st.rerun()
        with col_d:
            if st.button("🗑", key=f"del_{sess.id}", help="Delete chat session"):
                db2 = SessionLocal()
                delete_session(db2, sess.id)
                db2.close()
                if st.session_state.active_session_id == sess.id:
                    st.session_state.active_session_id = None
                    st.session_state.messages = []
                st.rerun()

# ── Main Area ─────────────────────────────────────────────────────────────────
render_header("Chat Assistant", "Ask questions grounded in your document repository", "💬")

# Check if documents exist
if doc_count == 0:
    st.info("📭 No documents indexed yet. Go to **Upload** to add your first document, then come back to chat!")
    if st.button("📤 Go to Upload"):
        st.switch_page("pages/Upload.py")
    st.stop()

# Check API key
if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == "YOUR_API_KEY":
    st.error("⚠️ Google API key not set or invalid. Please configure it in **Settings**.")
    if st.button("⚙️ Go to Settings"):
        st.switch_page("pages/Setting.py")
    st.stop()

# Ensure an active session exists
if st.session_state.active_session_id is None:
    db = SessionLocal()
    sessions = get_all_sessions(db)
    if sessions:
        st.session_state.active_session_id = sessions[0].id
        msgs = get_messages_by_session(db, sessions[0].id)
        st.session_state.messages = [{"role": m.role, "content": m.message} for m in msgs]
    else:
        sess = create_session(db, "Chat Session 1", st.session_state.user_id)
        st.session_state.active_session_id = sess.id
        st.session_state.messages = []
    db.close()

# ── Top Context Pills Bar ──────────────────────────────────────────────────────
db = SessionLocal()
from database.models import Document
coll_docs = db.query(Document).filter(Document.collection == st.session_state.collection).all()
db.close()
doc_names = [d.filename for d in coll_docs]

col_pill1, col_pill2, col_pill3 = st.columns([3, 3, 2])
with col_pill1:
    st.markdown(f"""
    <div style="background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2); border-radius:10px; padding:0.4rem 0.8rem; display:flex; align-items:center; gap:0.5rem;">
        <span style="font-size:0.85rem;">📁 Collection:</span>
        <span style="color:#818cf8; font-weight:700; font-size:0.85rem;">{st.session_state.collection} ({len(doc_names)} doc{'s' if len(doc_names) != 1 else ''})</span>
    </div>
    """, unsafe_allow_html=True)

with col_pill2:
    st.markdown(f"""
    <div style="background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2); border-radius:10px; padding:0.4rem 0.8rem; display:flex; align-items:center; gap:0.5rem;">
        <span style="font-size:0.85rem;">⚡ Model:</span>
        <span style="color:#34d399; font-weight:700; font-size:0.85rem;">{settings.GEMINI_MODEL}</span>
    </div>
    """, unsafe_allow_html=True)

with col_pill3:
    if st.button("🧹 Clear Chat", key="clear_chat_btn", use_container_width=True, help="Clear messages in current session"):
        if st.session_state.active_session_id:
            db = SessionLocal()
            db.query(ChatMessage).filter(ChatMessage.session_id == st.session_state.active_session_id).delete()
            db.commit()
            db.close()
        st.session_state.messages = []
        st.rerun()

if len(doc_names) == 0:
    st.warning(f"⚠️ Collection **'{st.session_state.collection}'** currently has no documents. Please go to **Upload** to add files to this collection, or switch collections in the sidebar.")
else:
    with st.expander(f"📂 Indexed files in collection '{st.session_state.collection}' ({len(doc_names)})"):
        for name in doc_names:
            st.markdown(f"- 📄 `{name}`")

st.markdown("<br>", unsafe_allow_html=True)

# ── Chat Display ──────────────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    if not st.session_state.messages:
        st.markdown(f"""
        <div style="text-align:center; padding:3.5rem 2rem; background:rgba(15,22,41,0.4); border:1px dashed rgba(99,102,241,0.2); border-radius:18px; margin:1rem 0;">
            <div style="font-size:3rem; margin-bottom:0.8rem;">🧠</div>
            <h3 style="color:#818cf8 !important; margin:0 0 0.5rem; font-weight:700;">Knowledge Copilot is Ready</h3>
            <p style="color:#94a3b8 !important; margin:0; font-size:0.88rem;">
                Currently querying collection <strong style="color:#e2e8f0;">"{st.session_state.collection}"</strong> ({len(doc_names)} document(s) loaded).
            </p>
            <p style="color:#64748b !important; margin:0.4rem 0 0; font-size:0.8rem;">
                Ask specific questions, summaries, or analyses grounded in your files.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="🧠" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["content"], unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask a question about your documents...")

if user_input:
    # 1. Display and save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    db = SessionLocal()
    add_message(db, st.session_state.active_session_id, "user", user_input)
    db.close()

    # 2. Generate response with RAG
    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("Searching knowledge base and generating answer..."):
            try:
                from rag.chain import RAGChain
                chain = RAGChain(collection_name=st.session_state.collection)
                answer, sources = chain.ask_with_sources(user_input)

                # Format source references
                if sources:
                    source_lines = []
                    for i, doc in enumerate(sources, 1):
                        raw_src = doc.metadata.get("source", "Document")
                        file_name = os.path.basename(raw_src)
                        page = doc.metadata.get("page", "")
                        page_tag = f" · Page {page}" if page else ""
                        snippet = doc.page_content.strip().replace("\n", " ")[:180]
                        source_lines.append(
                            f"- **[Source {i}]** `{file_name}`{page_tag}\n  *\"{snippet}...\"*"
                        )
                    sources_block = (
                        "\n\n---\n\n"
                        "**📎 Referenced Context:**\n\n" + "\n\n".join(source_lines)
                    )
                    full_answer = f"{answer}{sources_block}"
                else:
                    full_answer = answer

                st.markdown(full_answer, unsafe_allow_html=True)

            except Exception as e:
                full_answer = (
                    f"❌ **An error occurred while answering:** `{str(e)}`\n\n"
                    "Please verify your API key and settings in the **Settings** page."
                )
                st.error(full_answer)

    # 3. Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": full_answer})
    db = SessionLocal()
    add_message(db, st.session_state.active_session_id, "assistant", full_answer)

    # 4. Update session title from first question
    if len(st.session_state.messages) == 2:
        from database.models import ChatSession
        sess = db.query(ChatSession).filter(ChatSession.id == st.session_state.active_session_id).first()
        if sess:
            sess.session_name = user_input[:50] + ("..." if len(user_input) > 50 else "")
            db.commit()

    db.close()
    st.rerun()
