from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from pypdf import PdfReader
from pypdf.errors import PdfReadError

logger = logging.getLogger(__name__)


def load_pdf(file_path: str) -> list[dict[str, Any]]:
     """
          Load a PDF and extract text page-by-page while preserving page numbers.

          The loader returns a list of dictionaries in the expected LangChain-style
          format:
          [
               {
                    "page_content": "... extracted text ...",
                    "metadata": {"source": "document.pdf", "page": 1}
               }
          ]

          Invalid, missing, or unreadable PDF files return an empty list instead of
          crashing the application.
     """
     pdf_path = Path(file_path)

     if not pdf_path.exists() or not pdf_path.is_file():
          logger.warning("PDF file not found: %s", file_path)
          return []

     if pdf_path.suffix.lower() != ".pdf":
          logger.warning("Unsupported file type for PDF loader: %s", file_path)
          return []

     try:
          reader = PdfReader(str(pdf_path))
          pages: list[dict[str, Any]] = []

          for page_number, page in enumerate(reader.pages, start=1):
               page_text = page.extract_text() or ""
               cleaned_text = " ".join(page_text.split())

               pages.append(
                    {
                         "page_content": cleaned_text,
                         "metadata": {
                         "source": pdf_path.name,
                         "page": page_number,
                         },
                    }
               )

          return pages

     except (PdfReadError, ValueError, OSError) as exc:
          logger.warning("Could not read PDF %s: %s", file_path, exc)
          return []
     except Exception as exc:  # pragma: no cover - final safeguard for unexpected issues
          logger.warning("Unexpected error while reading PDF %s: %s", file_path, exc)
          return []

# Example output:
# [
#     {
#         "page_content": "MongoDB is a NoSQL database...",
#         "metadata": {
#             "source": "mongodb_guide.pdf",
#             "page": 1
#         }
#     },
#     {
#         "page_content": "MongoDB Atlas provides...",
#         "metadata": {
#             "source": "mongodb_guide.pdf",
#             "page": 2
#         }
#     }
# ]