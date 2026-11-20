"""
Upload Page – ingest documents into the RAG system
"""

import os
import streamlit as st

st.set_page_config(
    page_title="Upload – Knowledge Copilot",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared CSS & Sidebar ──────────────────────────────────────────────────────
from services.ui_helper import inject_custom_ui, render_sidebar, render_header

inject_custom_ui()
render_sidebar()

# ── Header ────────────────────────────────────────────────────────────────────
render_header("Upload Documents", "Index documents into vector collections for instant AI retrieval", "📤")

# ── DB Init ───────────────────────────────────────────────────────────────────
from database.db import Base, engine, SessionLocal
import database.models  # noqa
Base.metadata.create_all(bind=engine)

from database.queries import get_or_create_default_user, create_document, get_all_documents

if "user_id" not in st.session_state:
    db = SessionLocal()
    user = get_or_create_default_user(db)
    st.session_state.user_id = user.id
    db.close()

# ── Fetch Existing Collections ────────────────────────────────────────────────
db = SessionLocal()
existing_docs = get_all_documents(db)
db.close()
existing_cols = sorted(list(set(d.collection or "General" for d in existing_docs)))
if "General" not in existing_cols:
    existing_cols.insert(0, "General")

# ── Supported Formats Badges ──────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; gap:0.6rem; flex-wrap:wrap; margin-bottom:1.5rem;">
    <span style="background:rgba(99,102,241,0.12); color:#818cf8; border:1px solid rgba(99,102,241,0.25); border-radius:8px; padding:0.35rem 0.8rem; font-size:0.8rem; font-weight:600;">📄 PDF</span>
    <span style="background:rgba(99,102,241,0.12); color:#818cf8; border:1px solid rgba(99,102,241,0.25); border-radius:8px; padding:0.35rem 0.8rem; font-size:0.8rem; font-weight:600;">📝 DOCX</span>
    <span style="background:rgba(99,102,241,0.12); color:#818cf8; border:1px solid rgba(99,102,241,0.25); border-radius:8px; padding:0.35rem 0.8rem; font-size:0.8rem; font-weight:600;">📃 TXT</span>
    <span style="background:rgba(99,102,241,0.12); color:#818cf8; border:1px solid rgba(99,102,241,0.25); border-radius:8px; padding:0.35rem 0.8rem; font-size:0.8rem; font-weight:600;">📊 CSV</span>
    <span style="background:rgba(99,102,241,0.12); color:#818cf8; border:1px solid rgba(99,102,241,0.25); border-radius:8px; padding:0.35rem 0.8rem; font-size:0.8rem; font-weight:600;">⬇️ Markdown</span>
    <span style="background:rgba(99,102,241,0.12); color:#818cf8; border:1px solid rgba(99,102,241,0.25); border-radius:8px; padding:0.35rem 0.8rem; font-size:0.8rem; font-weight:600;">🔧 JSON</span>
</div>
""", unsafe_allow_html=True)

# ── Collection Selector ───────────────────────────────────────────────────────
col_opt1, col_opt2 = st.columns([2, 3])
with col_opt1:
    collection_options = existing_cols + ["+ Create New Collection..."]
    selected_option = st.selectbox(
        "📁 Target Collection",
        collection_options,
        index=0,
        help="Select an existing collection namespace or create a new one.",
    )

if selected_option == "+ Create New Collection...":
    with col_opt2:
        new_col_name = st.text_input(
            "New Collection Name",
            placeholder="e.g., LegalDocs, FinancialReports, HRManuals",
            help="Enter a clean, descriptive name for the new collection.",
        )
    target_collection = new_col_name.strip()
else:
    target_collection = selected_option.strip()

# ── File Upload Section ───────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Choose files to index",
    type=["pdf", "docx", "txt", "csv", "md", "markdown", "json"],
    accept_multiple_files=True,
    help="Drag and drop or browse files to add to the knowledge base.",
)

if uploaded_files:
    st.markdown(f"**Selected {len(uploaded_files)} file(s):**")
    for f in uploaded_files:
        size_kb = round(f.size / 1024, 1)
        st.markdown(f"""
        <div class="glass-card hover-lift" style="padding:0.75rem 1.2rem; margin:0.4rem 0; display:flex; align-items:center; gap:0.9rem;">
            <span style="font-size:1.4rem;">📄</span>
            <span style="color:#e2e8f0; font-size:0.88rem; font-weight:600;">{f.name}</span>
            <span style="color:#64748b; font-size:0.78rem; margin-left:auto; font-weight:500;">{size_kb} KB</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if not target_collection:
        st.warning("⚠️ Please specify or enter a valid collection name above before indexing.")
    else:
        st.info(f"👉 **Ready**: Click the button below to parse and index these **{len(uploaded_files)} file(s)** into collection **'{target_collection}'**.")

    if st.button("🚀 Index Documents into Knowledge Base", type="primary", use_container_width=True):
        if not target_collection:
            st.error("⚠️ Please specify a collection name above before indexing.")
            st.stop()

        from rag.ingestion import IngestionPipeline

        with st.spinner(f"⚡ Initializing embedding pipeline for '{target_collection}'..."):
            pipeline = IngestionPipeline(collection_name=target_collection)

        progress_bar = st.progress(0, text="Starting document ingestion...")
        results = []

        for i, file in enumerate(uploaded_files):
            progress_bar.progress(
                (i) / len(uploaded_files),
                text=f"Processing {file.name} ({i+1}/{len(uploaded_files)})..."
            )
            try:
                file.seek(0)
                file_bytes = file.read()
                page_count, chunk_count = pipeline.ingest_bytes(file_bytes, file.name)

                # Record in DB
                ext = os.path.splitext(file.name)[-1].upper().lstrip(".")
                db = SessionLocal()
                create_document(
                    db,
                    filename=file.name,
                    document_type=ext,
                    total_chunks=chunk_count,
                    collection=target_collection,
                    total_pages=page_count,
                    user_id=st.session_state.user_id,
                )
                db.close()
                results.append({"file": file.name, "pages": page_count, "chunks": chunk_count, "status": "✅ Indexed"})

            except Exception as e:
                results.append({"file": file.name, "pages": 0, "chunks": 0, "status": f"❌ Error: {e}"})

        progress_bar.progress(1.0, text="Ingestion complete!")
        all_ok = all("✅" in r["status"] for r in results)
        st.session_state["last_ingestion"] = {
            "collection": target_collection,
            "results": results,
            "all_ok": all_ok
        }
        st.session_state.collection = target_collection

    # ── Display Ingestion Results ──
    if "last_ingestion" in st.session_state and st.session_state["last_ingestion"]:
        last = st.session_state["last_ingestion"]
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"### 📊 Ingestion Summary ({last['collection']})")

        for r in last["results"]:
            is_ok = "✅" in r["status"]
            status_color = "#34d399" if is_ok else "#f87171"
            st.markdown(f"""
            <div class="glass-card" style="padding:0.9rem 1.3rem; margin:0.4rem 0; display:flex; align-items:center; gap:1rem;">
                <span style="font-size:1.4rem;">{'✅' if is_ok else '⚠️'}</span>
                <div style="flex:1;">
                    <p style="margin:0; color:#e2e8f0 !important; font-weight:600; font-size:0.9rem;">{r['file']}</p>
                    <p style="margin:0.2rem 0 0; color:#64748b !important; font-size:0.78rem;">{r['pages']} page(s) · {r['chunks']} chunk(s) indexed</p>
                </div>
                <span style="color:{status_color}; font-weight:700; font-size:0.85rem;">{r['status']}</span>
            </div>
            """, unsafe_allow_html=True)

        if last["all_ok"]:
            st.success(f"🎉 Successfully indexed {len(last['results'])} document(s) into '{last['collection']}'!")
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.page_link("pages/Chat.py", label="💬 Start Chatting with this Collection", icon="💬")
            with col_l2:
                st.page_link("pages/Knowledge_base.py", label="📚 View in Knowledge Base", icon="📚")
        else:
            st.warning("Some documents encountered errors during indexing. Check the status above.")
else:
    st.markdown("""
    <div style="background:rgba(15,22,41,0.4); border:2px dashed rgba(99,102,241,0.2); border-radius:18px; padding:3.5rem; text-align:center; margin-top:1rem;">
        <div style="font-size:3rem; margin-bottom:1rem;">☁️</div>
        <h3 style="color:#818cf8 !important; margin:0 0 0.5rem; font-weight:700;">Drag & Drop or Browse Files Above</h3>
        <p style="color:#64748b !important; margin:0; font-size:0.88rem;">
            Supports PDF, Word (DOCX), Plain Text (TXT), Spreadsheets (CSV), Markdown (MD), and JSON.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Tips ──────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("💡 Ingestion Best Practices"):
    st.markdown("""
    - **Use focused collection names**: Group documents by subject matter (e.g. `Finance_2026`, `Product_Docs`, `Contracts`).
    - **Document quality**: Clean text files and machine-readable PDFs produce the highest retrieval precision.
    - **Chunk tuning**: For granular question-answering, smaller chunk sizes (500–800) work best; for high-level summaries, larger chunks (1000–1500) provide broader context.
    - **Incremental updates**: Re-uploading a document adds new chunks without disrupting existing chat sessions.
    """)
