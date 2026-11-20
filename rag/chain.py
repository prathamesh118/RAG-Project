"""
RAG Chain – LCEL-based pipeline
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

from config import settings
from rag.prompt import get_rag_prompt
from rag.retriever import Retriever


def _format_docs(docs) -> str:
    parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown")
        parts.append(f"[Source {i}: {source}]\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


class RAGChain:

    def __init__(self, collection_name: str = "General"):
        self.collection_name = collection_name
        self._retriever = Retriever(collection_name=collection_name).get_retriever()
        self._llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=settings.TEMPERATURE,
        )
        self._prompt = get_rag_prompt()
        self._chain = (
            {
                "context": self._retriever | _format_docs,
                "question": RunnablePassthrough(),
            }
            | self._prompt
            | self._llm
            | StrOutputParser()
        )

    def ask(self, question: str) -> str:
        """Run a question through the RAG chain."""
        answer, _ = self.ask_with_sources(question)
        return answer

    def ask_with_sources(self, question: str):
        """Return answer + source documents."""
        docs = self._retriever.invoke(question)

        # Double-lock: verify chunks belong to an active document in the database (if registered)
        try:
            import os
            from database.db import SessionLocal
            from database.models import Document
            db = SessionLocal()
            valid_docs = db.query(Document).filter(Document.collection == self.collection_name).all()
            if valid_docs:
                valid_filenames = {
                    os.path.basename(d.filename).lower()
                    for d in valid_docs
                }
                docs = [
                    d for d in docs
                    if os.path.basename(d.metadata.get("source", "")).lower() in valid_filenames
                ]
            db.close()
        except Exception:
            pass

        if not docs or len(docs) == 0:
            return "I don't have enough information in the uploaded documents to answer that.", []
        context_str = _format_docs(docs)
        prompt_val = self._prompt.invoke({"context": context_str, "question": question})
        answer = (self._llm | StrOutputParser()).invoke(prompt_val)
        return answer, docs
