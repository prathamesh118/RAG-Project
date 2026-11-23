"""
Configuration Settings
"""

import os
from dotenv import load_dotenv

load_dotenv()


def _get_env_or_secret(key: str, default: str = "") -> str:
    """Read configuration from environment variable, falling back to Streamlit secrets."""
    val = os.getenv(key, "")
    if val:
        return val
    try:
        import streamlit as st

        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return default


class Settings:

    # Gemini
    GOOGLE_API_KEY: str = _get_env_or_secret("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = _get_env_or_secret("GEMINI_MODEL", "gemini-2.5-flash")
    TEMPERATURE: float = float(_get_env_or_secret("TEMPERATURE", "0.2"))

    # MySQL (optional – falls back to SQLite if not configured)
    MYSQL_HOST: str = _get_env_or_secret("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(_get_env_or_secret("MYSQL_PORT", "3306"))
    MYSQL_USER: str = _get_env_or_secret("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = _get_env_or_secret("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = _get_env_or_secret("MYSQL_DATABASE", "knowledge_copilot")

    # ChromaDB
    CHROMA_DB_PATH: str = _get_env_or_secret("CHROMA_DB_PATH", "chroma_db")

    # Embeddings
    EMBEDDING_MODEL: str = _get_env_or_secret("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

    # RAG
    CHUNK_SIZE: int = int(_get_env_or_secret("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(_get_env_or_secret("CHUNK_OVERLAP", "200"))
    TOP_K: int = int(_get_env_or_secret("TOP_K", "4"))

    # App
    APP_TITLE: str = "Knowledge Copilot"
    APP_ICON: str = "🧠"
    VERSION: str = "1.0.0"


settings = Settings()
