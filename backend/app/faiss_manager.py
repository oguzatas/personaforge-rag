import faiss
import numpy as np
from pathlib import Path
import os

class FaissManager:
    def __init__(self, universe: str, dim: int):
        self.universe = universe
        self.index_dir = Path("data") / universe / "faiss_index"
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.index_dir / "index.faiss"
        self.dim = dim
        self.index = None

    def create_index(self, embeddings: np.ndarray):
        """Create a new FAISS index from embeddings (shape: [n, dim])."""
        self.index = faiss.IndexFlatL2(self.dim)
        self.index.add(embeddings)
        faiss.write_index(self.index, str(self.index_path))

    def load_index(self):
        """Load the FAISS index from disk."""
        if not self.index_path.exists():
            raise FileNotFoundError(f"No FAISS index found at {self.index_path}")
        self.index = faiss.read_index(str(self.index_path))

    def query(self, vector: np.ndarray, top_k=5):
        """Query the FAISS index with a single vector (shape: [dim,]). Returns (distances, indices)."""
        if self.index is None:
            self.load_index()
        if vector.ndim == 1:
            vector = vector.reshape(1, -1)
        distances, indices = self.index.search(vector, top_k)
        return distances[0], indices[0] 