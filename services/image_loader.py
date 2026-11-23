"""
Image Loader – analyzes and describes image documents using Gemini Vision
"""

import base64
from io import BytesIO
import os
from typing import List
from PIL import Image
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from config import settings

MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".gif": "image/gif",
}

VISION_ANALYSIS_PROMPT = """You are an expert visual document intelligence and OCR engine.
Analyze this document/image thoroughly for indexing into a Knowledge Base RAG system.

Provide a comprehensive, structured breakdown in Markdown:

1. **Document Classification & Overview**:
   - What type of image is this? (e.g., Architecture diagram, workflow flowchart, infographic, scanned form, invoice/receipt, screenshot, data chart/graph, photo, presentation slide).
   - High-level summary of what it represents.

2. **OCR - Full Text Transcription**:
   - Extract and transcribe EVERY piece of visible text, title, label, subtitle, table header, numbers, button text, annotation, or caption accurately.
   - Transcribe all legible text verbatim so it is 100% searchable in retrieval.
   - Preserve hierarchy (headings, subheadings, bullet items).

3. **Visual Structure & Components**:
   - Describe the layout, sections, boxes, containers, colors, and design arrangement.
   - If there are icons, logos, or visual badges, note them.

4. **Diagram / Process / Data Breakdown (if applicable)**:
   - For diagrams/flowcharts: List all nodes/steps and explain connections, inputs, outputs, and direction of arrows.
   - For charts/tables: List axes, columns, data rows, numbers, percentages, and trends.

5. **Key Takeaways & In-Depth Details**:
   - Synthesize the core meaning, conclusions, and important insights from this visual document.

Be extremely thorough and accurate so users can ask any specific or general question about this image.
"""


def describe_image_bytes(
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    filename: str = "image",
    custom_prompt: str = VISION_ANALYSIS_PROMPT,
) -> str:
    """Analyze image bytes using Gemini Vision and return a rich markdown description with OCR."""
    if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == "YOUR_API_KEY":
        return f"[Image Document: {filename}] (API key not configured for vision analysis)"

    try:
        b64_data = base64.b64encode(image_bytes).decode("utf-8")
        llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.1,
        )

        message = HumanMessage(
            content=[
                {"type": "text", "text": custom_prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{b64_data}"},
                },
            ]
        )

        response = llm.invoke([message])
        return response.content.strip()

    except Exception as e:
        return (
            f"[Image Document: {filename}]\n"
            f"Vision OCR analysis could not be completed. Error: {str(e)}"
        )


def load_image(file_path: str) -> List[Document]:
    """Load an image file, generate a detailed visual analysis via Gemini, and return a Document."""
    filename = os.path.basename(file_path)
    ext = os.path.splitext(file_path)[-1].lower()
    mime_type = MIME_TYPES.get(ext, "image/jpeg")

    with open(file_path, "rb") as f:
        image_bytes = f.read()

    width, height = 0, 0
    img_format = ext.lstrip(".").upper()

    # Get image dimensions and optimize size if excessively large
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            img_format = img.format or ext.lstrip(".").upper()
            if max(width, height) > 2200:
                img_copy = img.copy()
                img_copy.thumbnail((2200, 2200), Image.Resampling.LANCZOS)
                buf = BytesIO()
                save_fmt = "PNG" if ext == ".png" else "JPEG"
                if save_fmt == "JPEG" and img_copy.mode in ("RGBA", "P"):
                    img_copy = img_copy.convert("RGB")
                img_copy.save(buf, format=save_fmt, quality=90)
                image_bytes = buf.getvalue()
                mime_type = "image/png" if ext == ".png" else "image/jpeg"
    except Exception:
        pass

    description = describe_image_bytes(
        image_bytes=image_bytes,
        mime_type=mime_type,
        filename=filename,
    )

    full_content = (
        f"# Visual Document & OCR: {filename}\n\n"
        f"**Format**: {img_format} ({width}x{height}px)\n\n"
        f"## Detailed Visual & OCR Content Analysis\n\n"
        f"{description}"
    )

    doc = Document(
        page_content=full_content,
        metadata={
            "source": file_path,
            "filename": filename,
            "document_type": img_format,
            "page": 1,
            "is_image": True,
            "dimensions": f"{width}x{height}",
        },
    )

    return [doc]
