"""
Settings Page – configure API keys and RAG parameters
"""

import os
import streamlit as st

st.set_page_config(
    page_title="Settings – Knowledge Copilot",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared CSS & Sidebar ──────────────────────────────────────────────────────
from services.ui_helper import inject_custom_ui, render_sidebar, render_header
from config import settings

inject_custom_ui()
render_sidebar()

# ── DB Init ───────────────────────────────────────────────────────────────────
from database.db import Base, engine, SessionLocal
import database.models  # noqa
Base.metadata.create_all(bind=engine)

from database.queries import get_or_create_default_user

if "user_id" not in st.session_state:
    db = SessionLocal()
    user = get_or_create_default_user(db)
    st.session_state.user_id = user.id
    db.close()

# ── Header ────────────────────────────────────────────────────────────────────
render_header("Settings", "Configure API keys, Gemini models, and RAG parameters", "⚙️")

# ── Read current .env values ───────────────────────────────────────────────────
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
env_path = os.path.abspath(env_path)

def read_env_value(key: str, default: str = "") -> str:
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"{key}="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return default

def write_env_values(updates: dict):
    """Update specific keys in the .env file and live settings."""
    try:
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

        new_lines = []
        updated_keys = set()
        for line in lines:
            stripped = line.strip()
            key = stripped.split("=", 1)[0] if "=" in stripped else ""
            if key in updates:
                new_lines.append(f"{key}={updates[key]}\n")
                updated_keys.add(key)
            else:
                new_lines.append(line)

        # Add any new keys not already in file
        for k, v in updates.items():
            if k not in updated_keys:
                new_lines.append(f"{k}={v}\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        # Update in-memory settings
        if "GOOGLE_API_KEY" in updates:
            settings.GOOGLE_API_KEY = updates["GOOGLE_API_KEY"]
        if "GEMINI_MODEL" in updates:
            settings.GEMINI_MODEL = updates["GEMINI_MODEL"]
        if "TEMPERATURE" in updates:
            settings.TEMPERATURE = float(updates["TEMPERATURE"])
        if "CHUNK_SIZE" in updates:
            settings.CHUNK_SIZE = int(updates["CHUNK_SIZE"])
        if "CHUNK_OVERLAP" in updates:
            settings.CHUNK_OVERLAP = int(updates["CHUNK_OVERLAP"])
        if "TOP_K" in updates:
            settings.TOP_K = int(updates["TOP_K"])
        if "EMBEDDING_MODEL" in updates:
            settings.EMBEDDING_MODEL = updates["EMBEDDING_MODEL"]
        if "CHROMA_DB_PATH" in updates:
            settings.CHROMA_DB_PATH = updates["CHROMA_DB_PATH"]

        return True
    except Exception as e:
        st.error(f"Failed to write .env: {e}")
        return False

# ── Gemini Settings ───────────────────────────────────────────────────────────
st.markdown("### 🔑 Gemini API Configuration")
st.markdown("""
<div style="background:rgba(99,102,241,0.07); border:1px solid rgba(99,102,241,0.2); border-radius:12px; padding:1rem 1.2rem; margin-bottom:1.2rem;">
    <p style="margin:0; color:#818cf8 !important; font-size:0.85rem;">
        Get your free API key at <a href="https://aistudio.google.com" target="_blank" style="color:#a78bfa; text-decoration:underline;">aistudio.google.com</a>.
        Keys typically start with <code>AIza...</code>.
    </p>
</div>
""", unsafe_allow_html=True)

current_key = read_env_value("GOOGLE_API_KEY", settings.GOOGLE_API_KEY)
current_model = read_env_value("GEMINI_MODEL", settings.GEMINI_MODEL)
try:
    current_temp = float(read_env_value("TEMPERATURE", str(settings.TEMPERATURE)))
except ValueError:
    current_temp = 0.2

col_k1, col_k2 = st.columns([3, 2])
with col_k1:
    api_key = st.text_input(
        "Google API Key",
        value=current_key if current_key != "YOUR_API_KEY" else "",
        type="password",
        placeholder="AIza...",
        help="Your Google Gemini API key from AI Studio",
    )

with col_k2:
    gemini_models = [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
    ]
    model_idx = gemini_models.index(current_model) if current_model in gemini_models else 0
    gemini_model = st.selectbox("Gemini Model", gemini_models, index=model_idx)

temperature = st.slider(
    "Creativity / Temperature",
    min_value=0.0,
    max_value=1.0,
    value=current_temp,
    step=0.05,
    help="Higher = more creative; Lower = more precise and deterministic",
)

st.markdown("<br>", unsafe_allow_html=True)

# ── RAG Settings ──────────────────────────────────────────────────────────────
st.markdown("### 🔧 RAG & Chunking Parameters")

try:
    current_chunk_size = int(read_env_value("CHUNK_SIZE", str(settings.CHUNK_SIZE)))
    current_chunk_overlap = int(read_env_value("CHUNK_OVERLAP", str(settings.CHUNK_OVERLAP)))
    current_top_k = int(read_env_value("TOP_K", str(settings.TOP_K)))
except ValueError:
    current_chunk_size = 1000
    current_chunk_overlap = 200
    current_top_k = 4

current_embed_model = read_env_value("EMBEDDING_MODEL", settings.EMBEDDING_MODEL)

col_r1, col_r2, col_r3 = st.columns(3)
with col_r1:
    chunk_size = st.slider(
        "Chunk Size (characters)",
        200, 3000, current_chunk_size, step=100,
        help="Size of each text chunk fed to the vector store",
    )

with col_r2:
    chunk_overlap = st.slider(
        "Chunk Overlap",
        0, 500, current_chunk_overlap, step=50,
        help="Character overlap between consecutive chunks to preserve context",
    )

with col_r3:
    top_k = st.slider(
        "Top K Results",
        1, 10, current_top_k,
        help="Number of most relevant chunks retrieved per query",
    )

embed_models = [
    "BAAI/bge-small-en-v1.5",
    "BAAI/bge-base-en-v1.5",
    "BAAI/bge-large-en-v1.5",
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2",
]
embed_idx = embed_models.index(current_embed_model) if current_embed_model in embed_models else 0
embed_model = st.selectbox(
    "Embedding Model",
    embed_models,
    index=embed_idx,
    help="Note: Changing the embedding model requires re-indexing existing documents",
)

st.markdown("<br>", unsafe_allow_html=True)

# ── ChromaDB ──────────────────────────────────────────────────────────────────
st.markdown("### 🗄 Vector Storage")
current_chroma_path = read_env_value("CHROMA_DB_PATH", settings.CHROMA_DB_PATH)
chroma_path = st.text_input("ChromaDB Storage Directory", value=current_chroma_path)

st.markdown("<br>", unsafe_allow_html=True)

# ── Save Button ───────────────────────────────────────────────────────────────
btn_col1, btn_col2 = st.columns([2, 1])
with btn_col1:
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        updates = {
            "GOOGLE_API_KEY": api_key.strip() if api_key else current_key,
            "GEMINI_MODEL": gemini_model,
            "TEMPERATURE": str(temperature),
            "CHUNK_SIZE": str(chunk_size),
            "CHUNK_OVERLAP": str(chunk_overlap),
            "TOP_K": str(top_k),
            "EMBEDDING_MODEL": embed_model,
            "CHROMA_DB_PATH": chroma_path.strip(),
        }
        if write_env_values(updates):
            st.success("✅ Settings saved successfully! Changes are applied live.")
            st.balloons()

with btn_col2:
    if st.button("🧪 Test Gemini API", use_container_width=True):
        key_to_test = (api_key.strip() if api_key else current_key)
        if not key_to_test or key_to_test == "YOUR_API_KEY":
            st.error("Please enter a valid Google API key first.")
        else:
            with st.spinner("Connecting to Gemini API..."):
                try:
                    from langchain_google_genai import ChatGoogleGenerativeAI
                    llm = ChatGoogleGenerativeAI(
                        model=gemini_model,
                        google_api_key=key_to_test,
                        temperature=0.0,
                    )
                    response = llm.invoke("Say 'Connection successful!' in exactly those words.")
                    st.success(f"✅ Gemini Response: {response.content}")
                except Exception as e:
                    st.error(f"❌ Connection failed: {e}")

# ── Architecture Info ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="glass-card" style="padding:1.5rem 1.8rem; margin-top:1rem;">
    <h3 style="margin:0 0 1rem; color:#818cf8 !important; font-size:1.1rem;">📋 System Architecture</h3>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:1rem;">
        <div>
            <p style="margin:0; font-size:0.75rem; text-transform:uppercase; color:#64748b; font-weight:600;">LLM Provider</p>
            <p style="margin:0.2rem 0 0; color:#e2e8f0; font-weight:600; font-size:0.9rem;">Google Gemini (Flash & Pro)</p>
        </div>
        <div>
            <p style="margin:0; font-size:0.75rem; text-transform:uppercase; color:#64748b; font-weight:600;">Vector Database</p>
            <p style="margin:0.2rem 0 0; color:#e2e8f0; font-weight:600; font-size:0.9rem;">ChromaDB Persistent Store</p>
        </div>
        <div>
            <p style="margin:0; font-size:0.75rem; text-transform:uppercase; color:#64748b; font-weight:600;">Embedding Model</p>
            <p style="margin:0.2rem 0 0; color:#e2e8f0; font-weight:600; font-size:0.9rem;">HuggingFace BGE-Small (384d)</p>
        </div>
        <div>
            <p style="margin:0; font-size:0.75rem; text-transform:uppercase; color:#64748b; font-weight:600;">Orchestration</p>
            <p style="margin:0.2rem 0 0; color:#e2e8f0; font-weight:600; font-size:0.9rem;">LangChain LCEL Pipeline</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
