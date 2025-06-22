# Configuration Guide

## Environment Variables

You can configure the system using environment variables. Create a `.env` file in the `rag-end` directory:

```bash
# LLM Configuration
LLM_ENDPOINT_URL=https://your-ngrok-url.ngrok-free.app/generate
LLM_MAX_TOKENS=512
LLM_TEMPERATURE=0.7

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
FRONTEND_URL=http://localhost:3000

# FAISS Configuration
FAISS_TOP_K=5
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## Configuration Options

### LLM Configuration
- `LLM_ENDPOINT_URL`: The URL of your deployed Phi-2 model endpoint
- `LLM_MAX_TOKENS`: Maximum number of tokens to generate (default: 512)
- `LLM_TEMPERATURE`: Sampling temperature for response generation (default: 0.7)

### API Configuration
- `API_HOST`: Host address for the FastAPI server (default: 0.0.0.0)
- `API_PORT`: Port for the FastAPI server (default: 8000)

### Frontend Configuration
- `FRONTEND_URL`: URL of the React frontend for CORS (default: http://localhost:3000)

### FAISS Configuration
- `FAISS_TOP_K`: Number of top chunks to retrieve (default: 5)
- `EMBEDDING_MODEL`: Sentence transformer model for embeddings (default: all-MiniLM-L6-v2)

## Updating the LLM Endpoint

To change the LLM endpoint URL:

1. **Using Environment Variable** (Recommended):
   ```bash
   export LLM_ENDPOINT_URL=https://your-new-url.ngrok-free.app/generate
   ```

2. **Using .env file**:
   ```bash
   echo "LLM_ENDPOINT_URL=https://your-new-url.ngrok-free.app/generate" > .env
   ```

3. **Direct code change**:
   Edit `config/settings.py` and change the default value.

## Testing Configuration

You can test your configuration by running:
```bash
python test_phi.py
```

This will use the configured endpoint URL to test the connection. 