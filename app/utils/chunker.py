# app/utils/chunker.py
from typing import List, Dict

def chunk_pages(
    pages: List[Dict], 
    max_chars: int = 1000, 
    overlap: int = 200
) -> List[Dict]:
    """
    Split PDF pages into smaller chunks with overlap.
    
    Args:
        pages: [{ "page_number": int, "text": str }]
        max_chars: maximum characters per chunk
        overlap: number of overlapping characters between chunks

    Returns:
        List of chunks:
        [
            {
                "id": "p{page_number}_c{chunk_index}",
                "page_number": int,
                "text": str
            },
            ...
        ]
    """
    chunks = []
    
    for p in pages:
        text = p["text"]
        page_num = p["page_number"]
        
        start = 0
        chunk_idx = 0
        
        while start < len(text):
            end = min(start + max_chars, len(text))
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append({
                    "id": f"p{page_num}_c{chunk_idx}",
                    "page_number": page_num,
                    "text": chunk_text
                })
            
            start += max_chars - overlap
            chunk_idx += 1

    return chunks
