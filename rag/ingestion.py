"""
Ingestion Pipeline – loads, splits, and stores documents
"""

import os
from typing import List, Tuple

from langchain_core.documents import Document

from rag.loader import load_document
from rag.splitter import DocumentSplitter
from rag.vector_store import VectorStore


class IngestionPipeline:

    def __init__(self, collection_name: str = "General"):
        self.collection_name = collection_name
        self.splitter = DocumentSplitter()
        self.vector_store = VectorStore(collection_name=collection_name)

    def ingest_file(self, file_path: str) -> Tuple[int, int]:
        """
        Ingest a single file.

        Returns:
            (page_count, chunk_count) tuple
        """
        documents = load_document(file_path)
        chunks = self.splitter.split(documents)
        self.vector_store.add_documents(chunks)
        return len(documents), len(chunks)

    def ingest_bytes(self, file_bytes: bytes, filename: str) -> Tuple[int, int]:
        """
        Ingest from raw bytes (e.g., Streamlit UploadedFile).

        Saves to a temp file, ingests, then deletes.
        """
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        tmp_path = os.path.join(upload_dir, filename)

        with open(tmp_path, "wb") as f:
            f.write(file_bytes)

        try:
            page_count, chunk_count = self.ingest_file(tmp_path)
        finally:
            pass  # Keep file for reference

        return page_count, chunk_count
