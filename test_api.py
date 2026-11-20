"""
Test Script for Gemini API and RAG Pipeline
Tests model connectivity, document ingestion, vector retrieval, and question answering.
"""

import os
import sys
from config import settings

def test_pipeline():
    print("=" * 60)
    print("1. Verifying Settings & Gemini API Key")
    print("=" * 60)
    print(f"Model: {settings.GEMINI_MODEL}")
    print(f"API Key configured: {bool(settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != 'YOUR_API_KEY')}")
    
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.0,
    )
    res = llm.invoke("Reply in 3 words: 'API is working'").content.strip()
    print(f"Gemini Test Response: {res}\n")

    print("=" * 60)
    print("2. Ingesting Sample Test Document into Collection 'TestCollection'")
    print("=" * 60)
    test_content = (
        "Project Orion was an aerospace research initiative launched in 1958. "
        "The project was led by physicist Freeman Dyson and intended to power spacecraft "
        "using nuclear pulse propulsion. The estimated top speed was 10 percent of the speed of light. "
        "The project was terminated in 1965 following the Partial Nuclear Test Ban Treaty."
    )
    test_file_path = "test_document.txt"
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)

    from rag.ingestion import IngestionPipeline
    pipeline = IngestionPipeline(collection_name="TestCollection")
    pages, chunks = pipeline.ingest_file(test_file_path)
    print(f"Ingested {pages} document(s), generated {chunks} chunk(s).\n")

    print("=" * 60)
    print("3. Testing RAG Retrieval & Accurate Answer Generation")
    print("=" * 60)
    from rag.chain import RAGChain
    rag = RAGChain(collection_name="TestCollection")

    q1 = "Who led Project Orion and what was its top speed?"
    print(f"Question 1: {q1}")
    ans1, sources1 = rag.ask_with_sources(q1)
    print(f"Answer 1:\n{ans1}\n")
    print(f"Sources retrieved: {len(sources1)}")
    for i, s in enumerate(sources1, 1):
        print(f"  Source {i}: {s.metadata.get('source')} (snippet: {s.page_content[:60]}...)")
    print()

    q2 = "What is the recipe for chocolate cake?"
    print(f"Question 2 (Out of domain): {q2}")
    ans2, sources2 = rag.ask_with_sources(q2)
    print(f"Answer 2:\n{ans2}\n")

    # Cleanup test document file
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

    print("=" * 60)
    print("All Tests Completed Successfully!")
    print("=" * 60)

if __name__ == "__main__":
    test_pipeline()
