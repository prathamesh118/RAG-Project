"""TXT Loader"""

from typing import List
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document


def load_txt(file_path: str) -> List[Document]:
    loader = TextLoader(file_path, encoding="utf-8")
    return loader.load()
