"""
Database Queries – CRUD helpers
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from database.models import ChatMessage, ChatSession, Document, User


# =====================================================
# Users
# =====================================================

def get_or_create_default_user(db: Session) -> User:
    user = db.query(User).filter(User.username == "default").first()
    if not user:
        user = User(
            username="default",
            email="default@knowledgecopilot.ai",
            password_hash="",
            created_at=datetime.utcnow(),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


# =====================================================
# Documents
# =====================================================

def create_document(
    db: Session,
    filename: str,
    document_type: str,
    total_chunks: int,
    collection: str,
    total_pages: int = 0,
    user_id: int = 1,
) -> Document:
    # If the document already exists in this collection, update its metadata
    existing = (
        db.query(Document)
        .filter(Document.filename == filename, Document.collection == collection)
        .first()
    )
    if existing:
        existing.document_type = document_type
        existing.total_chunks = total_chunks
        existing.total_pages = total_pages
        existing.upload_time = datetime.utcnow()
        existing.status = "Indexed"
        db.commit()
        db.refresh(existing)
        return existing

    doc = Document(
        filename=filename,
        document_type=document_type,
        total_pages=total_pages,
        total_chunks=total_chunks,
        collection=collection,
        upload_time=datetime.utcnow(),
        status="Indexed",
        uploaded_by=user_id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_all_documents(db: Session) -> List[Document]:
    return db.query(Document).order_by(Document.upload_time.desc()).all()


def delete_document(db: Session, doc_id: int) -> bool:
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc:
        db.delete(doc)
        db.commit()
        return True
    return False


def get_document_count(db: Session) -> int:
    return db.query(Document).count()


def get_total_chunks(db: Session) -> int:
    result = db.query(Document).all()
    return sum(d.total_chunks or 0 for d in result)


# =====================================================
# Chat Sessions
# =====================================================

def create_session(db: Session, session_name: str, user_id: int = 1) -> ChatSession:
    session = ChatSession(
        session_name=session_name,
        created_at=datetime.utcnow(),
        user_id=user_id,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_all_sessions(db: Session) -> List[ChatSession]:
    return db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()


def get_session_by_id(db: Session, session_id: int) -> Optional[ChatSession]:
    return db.query(ChatSession).filter(ChatSession.id == session_id).first()


def delete_session(db: Session, session_id: int) -> bool:
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if session:
        db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
        db.delete(session)
        db.commit()
        return True
    return False


def get_session_count(db: Session) -> int:
    return db.query(ChatSession).count()


# =====================================================
# Chat Messages
# =====================================================

def add_message(
    db: Session,
    session_id: int,
    role: str,
    message: str,
) -> ChatMessage:
    msg = ChatMessage(
        role=role,
        message=message,
        created_at=datetime.utcnow(),
        session_id=session_id,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_messages_by_session(db: Session, session_id: int) -> List[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )


def get_total_messages(db: Session) -> int:
    return db.query(ChatMessage).count()
