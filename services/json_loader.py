"""JSON Loader"""

import json
from typing import List
from langchain_core.documents import Document


def load_json(file_path: str) -> List[Document]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    text = json.dumps(data, indent=2)
    return [Document(page_content=text, metadata={"source": file_path})]
