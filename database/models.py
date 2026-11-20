"""
Database Models
"""

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import relationship

from database.db import Base


# =====================================================
# User
# =====================================================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String(100), nullable=False)

    email = Column(String(255), unique=True)

    password_hash = Column(String(255))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    documents = relationship(
        "Document",
        back_populates="user"
    )

    sessions = relationship(
        "ChatSession",
        back_populates="user"
    )


# =====================================================
# Documents
# =====================================================

class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    filename = Column(String(255))

    document_type = Column(String(50))

    total_pages = Column(Integer)

    total_chunks = Column(Integer)

    collection = Column(String(100))

    upload_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    status = Column(
        String(50),
        default="Indexed"
    )

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="documents"
    )


# =====================================================
# Chat Session
# =====================================================

class ChatSession(Base):

    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True)

    session_name = Column(String(200))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="sessions"
    )

    messages = relationship(
        "ChatMessage",
        back_populates="session"
    )


# =====================================================
# Chat Messages
# =====================================================

class ChatMessage(Base):

    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)

    role = Column(String(20))

    message = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    session_id = Column(
        Integer,
        ForeignKey("chat_sessions.id")
    )

    session = relationship(
        "ChatSession",
        back_populates="messages"
    )