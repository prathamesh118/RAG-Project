"""PDF Loader with Scanned Page / Image Intelligence"""

import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
import pypdf

from services.image_loader import describe_image_bytes


def load_pdf(file_path: str) -> List[Document]:
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Check for empty / scanned pages that contain images
    try:
        reader = pypdf.PdfReader(file_path)
        for i, page in enumerate(reader.pages):
            doc = docs[i] if i < len(docs) else None
            page_text = doc.page_content.strip() if doc else ""

            # If page text is very sparse (< 50 chars) and page has images, run vision OCR/description
            if len(page_text) < 50 and len(page.images) > 0:
                visual_descriptions = []
                for img_idx, img_file in enumerate(page.images, 1):
                    try:
                        desc = describe_image_bytes(
                            image_bytes=img_file.data,
                            mime_type="image/png" if img_file.name.lower().endswith(".png") else "image/jpeg",
                            filename=f"{os.path.basename(file_path)} Page {i+1} Image {img_idx}",
                        )
                        visual_descriptions.append(f"### Visual Content (Image {img_idx}):\n{desc}")
                    except Exception:
                        continue

                if visual_descriptions:
                    combined_visual = "\n\n".join(visual_descriptions)
                    augmented_content = (
                        f"{page_text}\n\n"
                        f"[Scanned Page / Visual Elements on Page {i+1}]\n"
                        f"{combined_visual}"
                    ).strip()

                    if doc:
                        doc.page_content = augmented_content
                    else:
                        docs.append(Document(
                            page_content=augmented_content,
                            metadata={"source": file_path, "page": i + 1}
                        ))
    except Exception:
        # Fall back cleanly to standard extracted documents if image inspection encounters any issue
        pass

    return docs
