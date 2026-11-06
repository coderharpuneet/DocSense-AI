from __future__ import annotations

from typing import Any

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from document_loader import load_pdf


def split_documents(
     pages: list[dict[str, Any]],
     chunk_size: int = 1000,
     chunk_overlap: int = 200,
) -> list[Document]:
     """
     Convert extracted PDF pages into LangChain Documents and split them into
     smaller chunks while preserving page metadata.

     Args:
          pages: List of page dictionaries from the PDF loader, with shape:
               {"page_content": "...", "metadata": {"source": "x.pdf", "page": 1}}
          chunk_size: Maximum size of each chunk in characters.
          chunk_overlap: Number of overlapping characters between adjacent chunks.

     Returns:
          A flat list of LangChain Document objects, each with chunk text and
          preserved metadata.
     """
     if not pages:
          return []

     splitter = RecursiveCharacterTextSplitter(
          chunk_size=chunk_size,
          chunk_overlap=chunk_overlap,
          length_function=len,
          separators=["\n\n", "\n", " ", ""],
     )

     all_chunks: list[Document] = []

     for page in pages:
          page_content = page.get("page_content", "")
          metadata = page.get("metadata", {})

          if not page_content.strip():
               continue

          page_doc = Document(page_content=page_content, metadata=metadata)
          split_chunks = splitter.split_documents([page_doc])

          for chunk in split_chunks:
               chunk.metadata = {
                    "source": metadata.get("source", "unknown.pdf"),
                    "page": metadata.get("page", 1),
               }
               all_chunks.append(chunk)

     return all_chunks


def process_pdf(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
     """
     Full ingestion pipeline only linking the loader to the splitter.
     The actual PDF extraction remains in document_loader.py.
     """
     pages = load_pdf(file_path)
     if not pages:
          return []

     return split_documents(
          pages=pages,
          chunk_size=chunk_size,
          chunk_overlap=chunk_overlap,
     )

chunks=process_pdf("./data/documents/Fundamentals of Deep Learning O'Reilly.pdf", chunk_size=1000, chunk_overlap=100)
for i, chunk in enumerate(chunks):
     print(f"Chunk {i+1}:")
     print(f"Source: {chunk.metadata.get('source')}, Page: {chunk.metadata.get('page')}")
     print(f"Content: {chunk.page_content}")  
     print("-" * 80)