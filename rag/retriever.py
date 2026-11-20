"""
RAG Retriever
"""

from langchain_core.vectorstores import VectorStoreRetriever

from config import settings
from rag.vector_store import VectorStore


class Retriever:

    def __init__(self, collection_name: str = "General"):
        self.store = VectorStore(collection_name=collection_name)

    def get_retriever(self, k: int | None = None) -> VectorStoreRetriever:
        return self.store.vector_db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k or settings.TOP_K},
        )
