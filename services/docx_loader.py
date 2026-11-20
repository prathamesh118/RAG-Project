"""DOCX Loader"""

import os
from typing import List
from langchain_core.documents import Document


def load_docx(file_path: str) -> List[Document]:
    try:
        import docx
        doc = docx.Document(file_path)
        text_parts = []
        for p in doc.paragraphs:
            if p.text.strip():
                text_parts.append(p.text)
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_text:
                    text_parts.append(" | ".join(row_text))
        content = "\n\n".join(text_parts)
        return [Document(page_content=content, metadata={"source": file_path})]
    except Exception:
        from langchain_community.document_loaders import Docx2txtLoader
        loader = Docx2txtLoader(file_path)
        return loader.load()
