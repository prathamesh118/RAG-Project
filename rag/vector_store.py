"""
ChromaDB Vector Store Manager
"""

import re
from typing import List

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from rag.embeddings import EmbeddingModel


def sanitize_collection_name(name: str) -> str:
    """Ensure collection name meets ChromaDB requirements:
    - 3 to 63 characters
    - Only alphanumeric, underscores, hyphens
    - Starts and ends with alphanumeric
    """
    if not name or not str(name).strip():
        return "General"
    cleaned = re.sub(r"[^a-zA-Z0-9._-]", "_", str(name).strip())
    cleaned = re.sub(r"^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$", "", cleaned)
    if len(cleaned) < 3:
        cleaned = f"col_{cleaned}".rstrip("_")
        if len(cleaned) < 3:
            cleaned = "col_general"
    return cleaned[:63]


class VectorStore:

    def __init__(self, collection_name: str = "General"):

        self.collection_name = sanitize_collection_name(collection_name)

        self.embedding_model = EmbeddingModel().get_embeddings()

        from config import settings
        self.vector_db = Chroma(
            persist_directory=settings.CHROMA_DB_PATH,
            collection_name=self.collection_name,
            embedding_function=self.embedding_model,
        )

    # ---------------------------------------
    # Add Documents
    # ---------------------------------------

    def add_documents(self, documents: List[Document]):
        if not documents:
            return
        self.vector_db.add_documents(documents)

    # ---------------------------------------
    # Similarity Search
    # ---------------------------------------

    def similarity_search(
        self,
        query: str,
        k: int = 4,
    ):

        return self.vector_db.similarity_search(
            query,
            k=k,
        )

    # ---------------------------------------
    # Similarity Search with Score
    # ---------------------------------------

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
    ):

        return self.vector_db.similarity_search_with_score(
            query,
            k=k,
        )

    # ---------------------------------------
    # Delete Documents by Filename / Source
    # ---------------------------------------

    def delete_by_source(self, source_path: str):
        """Delete chunks matching source metadata."""
        self.delete_by_filename(source_path)

    def delete_by_filename(self, filename: str):
        """Delete all chunks where source metadata matches or contains the filename."""
        import os
        try:
            normalized_name = os.path.basename(filename).lower()
            results = self.vector_db._collection.get()
            ids_to_del = []
            if results and "ids" in results and "metadatas" in results:
                for chunk_id, meta in zip(results["ids"], results["metadatas"]):
                    if meta:
                        src = str(meta.get("source", ""))
                        if os.path.basename(src).lower() == normalized_name or normalized_name in src.lower():
                            ids_to_del.append(chunk_id)
            if ids_to_del:
                self.vector_db._collection.delete(ids=ids_to_del)
        except Exception:
            try:
                self.vector_db._collection.delete(where={"source": filename})
            except Exception:
                pass

    # ---------------------------------------
    # Delete Collection
    # ---------------------------------------

    def delete_collection(self):

        self.vector_db.delete_collection()

    # ---------------------------------------
    # Count Chunks
    # ---------------------------------------

    def count(self):

        return self.vector_db._collection.count()

    # ---------------------------------------
    # Get All Metadata
    # ---------------------------------------

    def get_metadata(self):

        return self.vector_db.get()