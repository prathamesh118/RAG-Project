"""
Document Splitter

Splits LangChain documents into smaller chunks while
preserving metadata.
"""

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        class RecursiveCharacterTextSplitter:
            def __init__(self, chunk_size=1000, chunk_overlap=200, separators=None, length_function=len):
                self.chunk_size = chunk_size
                self.chunk_overlap = chunk_overlap
                self.separators = separators or ["\n\n", "\n", ". ", " ", ""]
                self.length_function = length_function

            def split_documents(self, documents):
                chunks = []
                for doc in documents:
                    text = doc.page_content
                    start = 0
                    while start < len(text):
                        end = min(start + self.chunk_size, len(text))
                        chunk_text = text[start:end]
                        chunks.append(Document(page_content=chunk_text, metadata=dict(doc.metadata)))
                        if end == len(text):
                            break
                        start += max(1, self.chunk_size - self.chunk_overlap)
                return chunks

from langchain_core.documents import Document

from config import settings


class DocumentSplitter:

    def __init__(self):

        self.text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=settings.CHUNK_SIZE,

            chunk_overlap=settings.CHUNK_OVERLAP,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],

            length_function=len,
        )

    def split(
        self,
        documents: list[Document]
    ) -> list[Document]:

        chunks = self.text_splitter.split_documents(documents)

        # Add chunk id metadata
        for index, chunk in enumerate(chunks):

            chunk.metadata["chunk_id"] = index + 1

        return chunks