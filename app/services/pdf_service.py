import fitz
from typing import Dict, List

def extract_pages(pdf_path: str) -> List[Dict]:
    """
    Extract text page by page from PDF.
    Returns: [{ "page_number": int, "text": str }, ...]
    """
    doc = fitz.open(pdf_path)
    pages = []

    for i in range(len(doc)):
        page = doc[i]
        text = page.get_text("text")
        if text.strip():  # only keep non-empty
            pages.append({
                "page_number": i + 1,  # 1-based indexing
                "text": text
            })

    doc.close()
    return pages
