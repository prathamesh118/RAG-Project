"""
Document Loader – dispatches to the correct service loader
"""

import os
from typing import List

from langchain_core.documents import Document


def load_document(file_path: str) -> List[Document]:
    """Load a document from a file path based on its extension."""
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        from services.pdf_loader import load_pdf
        return load_pdf(file_path)

    elif ext == ".docx":
        from services.docx_loader import load_docx
        return load_docx(file_path)

    elif ext == ".txt":
        from services.txt_loader import load_txt
        return load_txt(file_path)

    elif ext == ".csv":
        from services.csv_loader import load_csv
        return load_csv(file_path)

    elif ext in (".md", ".markdown"):
        from services.markdown_loader import load_markdown
        return load_markdown(file_path)

    elif ext == ".json":
        from services.json_loader import load_json
        return load_json(file_path)

    else:
        raise ValueError(f"Unsupported file type: {ext}")
