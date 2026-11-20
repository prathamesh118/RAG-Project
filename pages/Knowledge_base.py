"""
Knowledge Base Page – view and manage indexed documents
"""

import streamlit as st

st.set_page_config(
    page_title="Knowledge Base – Knowledge Copilot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared CSS & Sidebar ──────────────────────────────────────────────────────
from services.ui_helper import inject_custom_ui, render_sidebar, render_header

inject_custom_ui()
render_sidebar()

# ── Header ────────────────────────────────────────────────────────────────────
render_header("Knowledge Base", "Manage your indexed document collection", "📚")

# ── DB Init ───────────────────────────────────────────────────────────────────
from database.db import Base, engine, SessionLocal
import database.models  # noqa
Base.metadata.create_all(bind=engine)

from database.queries import (
    get_or_create_default_user,
    get_all_documents,
    delete_document,
    get_document_count,
    get_total_chunks,
)

if "user_id" not in st.session_state:
    db = SessionLocal()
    user = get_or_create_default_user(db)
    st.session_state.user_id = user.id
    db.close()


# ── Stats ─────────────────────────────────────────────────────────────────────
db = SessionLocal()
all_docs = get_all_documents(db)
doc_count = len(all_docs)
chunk_count = get_total_chunks(db)
db.close()

# Unique collections & types
collections = list(set(d.collection or "General" for d in all_docs))
file_types  = list(set(d.document_type or "?" for d in all_docs))

m1, m2, m3, m4 = st.columns(4)
m1.metric("📄 Documents", doc_count)
m2.metric("🔢 Total Chunks", chunk_count)
m3.metric("📁 Collections", len(collections))
m4.metric("🗂 File Types", len(file_types))

st.markdown("<br>", unsafe_allow_html=True)

if not all_docs:
    st.markdown("""
    <div style="background:rgba(15,22,41,0.5); border:1px dashed rgba(99,102,241,0.2); border-radius:16px; padding:4rem; text-align:center;">
        <div style="font-size:3rem; margin-bottom:1rem;">📭</div>
        <h3 style="color:#f1f5f9 !important; margin:0 0 0.5rem; font-weight:700;">No documents indexed yet</h3>
        <p style="color:#94a3b8 !important; margin:0; font-size:0.88rem;">Upload your first document to get started with RAG search.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📤 Go to Upload", type="primary"):
        st.switch_page("pages/Upload.py")
    st.stop()

# ── Filters ───────────────────────────────────────────────────────────────────
f1, f2, f3 = st.columns([2, 2, 1])
with f1:
    search_q = st.text_input("🔍 Search documents", placeholder="Filter by filename...", label_visibility="collapsed")
with f2:
    filter_col = st.selectbox("Collection", ["All"] + collections, label_visibility="collapsed")
with f3:
    if st.button("📤 Upload More", type="primary"):
        st.switch_page("pages/Upload.py")

# ── Filter logic ──────────────────────────────────────────────────────────────
filtered = all_docs
if search_q:
    filtered = [d for d in filtered if search_q.lower() in (d.filename or "").lower()]
if filter_col != "All":
    filtered = [d for d in filtered if (d.collection or "General") == filter_col]

st.markdown(f"**{len(filtered)} document(s)**")
st.markdown("<br>", unsafe_allow_html=True)

# ── Document Cards ────────────────────────────────────────────────────────────
EXT_ICONS = {
    "PDF": "📄", "DOCX": "📝", "TXT": "📃", "CSV": "📊",
    "MD": "⬇️", "MARKDOWN": "⬇️", "JSON": "🔧",
}

for doc in filtered:
    icon = EXT_ICONS.get((doc.document_type or "").upper(), "📄")
    upload_time = doc.upload_time.strftime("%b %d, %Y %H:%M") if doc.upload_time else "Unknown"

    with st.container():
        c_info, c_del = st.columns([10, 1])
        with c_info:
            st.markdown(f"""
            <div class="glass-card hover-lift" style="padding:1rem 1.2rem; display:flex; align-items:center; gap:1rem; margin-bottom: 0.5rem;">
                <span style="font-size:2rem;">{icon}</span>
                <div style="flex:1; min-width:0;">
                    <p style="margin:0; color:#e2e8f0 !important; font-weight:600; font-size:0.9rem;">{doc.filename}</p>
                    <div style="display:flex; gap:1rem; margin-top:0.3rem; flex-wrap:wrap;">
                        <span style="color:#64748b; font-size:0.75rem;">📁 {doc.collection or 'General'}</span>
                        <span style="color:#64748b; font-size:0.75rem;">🔢 {doc.total_chunks or 0} chunks</span>
                        <span style="color:#64748b; font-size:0.75rem;">📄 {doc.total_pages or 0} pages</span>
                        <span style="color:#64748b; font-size:0.75rem;">🕐 {upload_time}</span>
                        <span style="background:rgba(16,185,129,0.1); color:#34d399; border-radius:6px; padding:0.1rem 0.5rem; font-size:0.7rem; font-weight:600;">✓ {doc.status or 'Indexed'}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c_del:
            if st.button("🗑️", key=f"del_doc_{doc.id}", help="Delete document record and vector embeddings"):
                try:
                    import os
                    from rag.vector_store import VectorStore
                    vs = VectorStore(collection_name=doc.collection or "General")
                    vs.delete_by_filename(doc.filename)
                    target_path = os.path.join("uploads", doc.filename)
                    if os.path.exists(target_path):
                        try:
                            os.remove(target_path)
                        except Exception:
                            pass
                except Exception:
                    pass
                db2 = SessionLocal()
                delete_document(db2, doc.id)
                db2.close()
                st.success(f"Deleted {doc.filename}")
                st.rerun()

# ── Clear Collection ──────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### ⚠️ Danger Zone")

with st.expander("🗑 Clear a ChromaDB collection"):
    st.warning("This will permanently delete all vector data in the selected collection from ChromaDB. Document records in the DB are not affected.")
    del_col = st.selectbox("Select collection to clear", collections, key="del_coll_sel")
    if st.button("🗑 Clear Collection Vectors", key="clear_coll_btn"):
        try:
            from rag.vector_store import VectorStore
            vs = VectorStore(collection_name=del_col)
            vs.delete_collection()
            st.success(f"ChromaDB collection '{del_col}' cleared.")
        except Exception as e:
            st.error(f"Failed: {e}")
