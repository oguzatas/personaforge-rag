# app/retriever.py
import numpy as np
from sentence_transformers import SentenceTransformer
from app.faiss_manager import FaissManager
from pathlib import Path

INDEX_PATH = "data/index/faiss.index"
CHUNK_PATH = "data/index/chunks.txt"
MODEL_NAME = "all-MiniLM-L6-v2"

# Legacy function for backward compatibility
def get_relevant_docs(query: str, k: int = 5) -> list[str]:
    # This uses the old global index
    import faiss
    model = SentenceTransformer(MODEL_NAME)
    query_vec = model.encode([query])
    index = faiss.read_index(INDEX_PATH)
    distances, indices = index.search(np.array(query_vec), k)
    with open(CHUNK_PATH, "r", encoding="utf-8") as f:
        chunks = f.read().split("\n---\n")
    return [chunks[i] for i in indices[0]]

def get_relevant_docs_for_universe(query: str, universe: str, k: int = 5) -> list[str]:
    """Retrieve relevant docs for a given universe using its FAISS index and chunk file."""
    model = SentenceTransformer(MODEL_NAME)
    query_vec = model.encode([query])
    faiss_manager = FaissManager(universe, dim=query_vec.shape[1])
    distances, indices = faiss_manager.query(np.array(query_vec[0]), top_k=k)
    chunk_path = Path("data") / universe / "faiss_index" / "chunks.txt"
    with open(chunk_path, "r", encoding="utf-8") as f:
        chunks = f.read().split("\n---\n")
    return [chunks[i] for i in indices]
