"""CSV Loader"""

from typing import List
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.documents import Document


def load_csv(file_path: str) -> List[Document]:
    try:
        loader = CSVLoader(file_path=file_path, encoding="utf-8")
        return loader.load()
    except UnicodeDecodeError:
        loader = CSVLoader(file_path=file_path, encoding="latin-1")
        return loader.load()
