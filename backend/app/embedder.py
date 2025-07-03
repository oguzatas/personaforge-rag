# app/embedder.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from app.utils.loader import load_documents
from app.utils.chunking import chunk_text
import os

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = "data/index/faiss.index"

def build_and_save_index(data_dir="data/lore/"):
    model = SentenceTransformer(MODEL_NAME)
    docs = load_documents(data_dir)
    
    chunks = []
    for doc in docs:
        chunks.extend(chunk_text(doc))

    embeddings = model.encode(chunks, show_progress_bar=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    os.makedirs("data/index/", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open("data/index/chunks.txt", "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk + "\n---\n")

    print(f"✅ {len(chunks)} chunk embedded and saved to FAISS index.")
