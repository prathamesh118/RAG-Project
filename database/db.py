"""
Database Connection – SQLite fallback (no MySQL required)
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------------------------
# Try MySQL first; fall back to SQLite so the app works without a DB server
# ---------------------------------------------------------------------------

_MYSQL_OK = False

try:
    from config import settings
    import pymysql  # noqa: F401

    _url = (
        f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}"
        f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"
    )
    engine = create_engine(_url, pool_pre_ping=True)
    # Try a quick connection to verify credentials
    with engine.connect():
        pass
    _MYSQL_OK = True

except Exception:
    # Fall back to SQLite stored in the project root
    _sqlite_path = os.path.join(os.path.dirname(__file__), "..", "knowledge_copilot.db")
    _sqlite_path = os.path.abspath(_sqlite_path)
    engine = create_engine(f"sqlite:///{_sqlite_path}", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Yield a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
