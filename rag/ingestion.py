"""
Ingestion Pipeline – loads, splits, and stores documents with progress tracking
"""

import os
from typing import Callable, Optional, Tuple

from rag.loader import load_document
from rag.splitter import DocumentSplitter
from rag.vector_store import VectorStore, sanitize_collection_name


class IngestionPipeline:

    def __init__(self, collection_name: str = "General"):
        self.collection_name = sanitize_collection_name(collection_name)
        self.splitter = DocumentSplitter()
        self.vector_store = VectorStore(collection_name=self.collection_name)

    def ingest_file(
        self,
        file_path: str,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> Tuple[int, int]:
        """
        Ingest a single file with optional progress callback: callback(percent: int, message: str)

        Returns:
            (page_count, chunk_count) tuple
        """
        filename = os.path.basename(file_path)
        ext = os.path.splitext(file_path)[-1].lower()

        # Step 1: Loading & OCR Extraction
        if progress_callback:
            if ext in (".png", ".jpg", ".jpeg", ".webp", ".bmp"):
                progress_callback(20, f"🔍 Running Gemini Vision OCR & layout analysis on {filename}...")
            elif ext == ".pdf":
                progress_callback(20, f"📄 Extracting text & running OCR on scanned pages in {filename}...")
            else:
                progress_callback(20, f"📖 Parsing content from {filename}...")

        documents = load_document(file_path)

        if not documents:
            raise ValueError(f"Could not extract any readable content or OCR text from {filename}.")

        # Step 2: Splitting into chunks
        if progress_callback:
            progress_callback(50, f"🧩 Splitting {len(documents)} page(s) into semantic chunks...")

        chunks = self.splitter.split(documents)

        # Step 3: Embeddings & Vector Storage
        if progress_callback:
            progress_callback(75, f"🧠 Generating vector embeddings for {len(chunks)} chunks...")

        self.vector_store.add_documents(chunks)

        if progress_callback:
            progress_callback(100, f"✅ Successfully indexed {filename} ({len(chunks)} chunks)!")

        return len(documents), len(chunks)

    def ingest_bytes(
        self,
        file_bytes: bytes,
        filename: str,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> Tuple[int, int]:
        """
        Ingest from raw bytes (e.g., Streamlit UploadedFile).
        """
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        tmp_path = os.path.join(upload_dir, filename)

        with open(tmp_path, "wb") as f:
            f.write(file_bytes)

        return self.ingest_file(tmp_path, progress_callback=progress_callback)
