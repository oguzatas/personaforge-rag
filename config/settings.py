# config/settings.py
import os
from pathlib import Path

# LLM Configuration
LLM_ENDPOINT_URL = os.getenv("LLM_ENDPOINT_URL", "https://646f-34-125-62-103.ngrok-free.app/generate")
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "100"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Frontend Configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Data Paths
DATA_DIR = Path("data")
MODELS_DIR = Path("models")

# FAISS Configuration
FAISS_TOP_K = int(os.getenv("FAISS_TOP_K", "5"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2") 