# app/utils/chunking.py
import textwrap

def chunk_text(text: str, chunk_size=500, overlap=100) -> list[str]:
    """
    Creates fixed-length chunks with overlap / Can be used for token-aware chunking
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
