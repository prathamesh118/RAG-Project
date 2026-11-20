import os
from typing import Optional
from langchain_huggingface import HuggingFaceEmbeddings

from config import settings

_EMBEDDING_INSTANCE: Optional[HuggingFaceEmbeddings] = None


class EmbeddingModel:

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        global _EMBEDDING_INSTANCE
        if _EMBEDDING_INSTANCE is None:
            _EMBEDDING_INSTANCE = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
        return _EMBEDDING_INSTANCE
