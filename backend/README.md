# PersonaForge Backend

The backend service for PersonaForge, providing a comprehensive RAG (Retrieval-Augmented Generation) system for AI-powered character interactions.

## Features

- **Character Management**: Create, update, and manage characters with rich schemas
- **RAG Pipeline**: Semantic search and context retrieval for conversations
- **Multi-Universe Support**: Organize characters into different universes
- **REST API**: Full CRUD operations for characters and universes
- **CLI Tools**: Command-line interface for management tasks

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running the API Server

```bash
python -m app.api
```

The server will start on `http://localhost:8000`

### API Documentation

Once running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/health`

## CLI Tools

### Character Management

```bash
# List all characters in a universe
python -m app.cli character list --universe Mytherra

# Create a new character (interactive)
python -m app.cli character create --universe Mytherra

# Show character details
python -m app.cli character show --universe Mytherra --character "Kael Vire"

# Delete a character
python -m app.cli character delete --universe Mytherra --character "Character Name"

# Get character statistics
python -m app.cli character stats --universe Mytherra

# Rebuild character registry
python -m app.cli character registry --universe Mytherra
```

### Universe Management

```bash
# List all universes
python -m app.cli universe list

# Build FAISS index for a specific universe
python -m app.cli universe build-index --universe Mytherra

# Build FAISS indices for all universes
python -m app.cli universe build-all-indices
```

## Project Structure

```
backend/
├── app/                    # Main application code
│   ├── api.py             # FastAPI endpoints
│   ├── cli.py             # Command-line interface
│   ├── character.py       # Character data model
│   ├── character_manager.py # Character management logic
│   ├── conversation_manager.py # Conversation history
│   ├── rag_pipeline.py    # RAG processing pipeline
│   ├── retriever.py       # Document retrieval
│   ├── universe_manager.py # Universe management
│   ├── universe_embedder.py # FAISS index building
│   ├── faiss_manager.py   # FAISS operations
│   ├── llm_interface.py   # LLM integration
│   ├── prompt_templates.py # Prompt formatting
│   ├── roles.py           # Role definitions
│   ├── embedder.py        # Legacy embedder
│   └── utils/             # Utility functions
│       ├── chunking.py    # Text chunking
│       └── loader.py      # Document loading
├── config/                # Configuration files
│   ├── config.yaml        # Main configuration
│   ├── logging.yaml       # Logging configuration
│   └── settings.py        # Settings module
├── data/                  # Data storage
│   ├── conversations.json # Conversation history
│   └── universes/         # Universe data
│       └── Mytherra/      # Example universe
│           ├── manifest.json
│           ├── character_registry.json
│           ├── characters/
│           └── faiss_index/
├── reports/               # Test reports and evaluations
├── notebooks/             # Jupyter notebooks
├── requirements.txt       # Python dependencies
└── manage_characters.py   # Legacy CLI entry point
```

## Character Schema

### Required Fields
```json
{
  "name": "Character Name",
  "role": "Character Role",
  "universe": "Universe Name",
  "location": "Character Location",
  "backstory": "Character backstory and personality description",
  "inventory": ["item1", "item2"],
  "current_mood": {
    "primary_emotion": "emotion_name",
    "intensity": "low|moderate|high",
    "plutchik_axis": ["emotion1", "emotion2"]
  }
}
```

### Optional Enhanced Fields
```json
{
  "personality_traits": ["trait1", "trait2", "trait3"],
  "key_quotes": ["quote1", "quote2"],
  "knowledge_domains": ["domain1", "domain2"],
  "relationships": {
    "faction": "Faction Name",
    "allies": ["ally1", "ally2"],
    "enemies": ["enemy1", "enemy2"],
    "mentor": "mentor_name",
    "apprentices": ["apprentice1"]
  },
  "metadata": {
    "created": "2024-01-01T00:00:00",
    "last_updated": "2024-01-01T00:00:00",
    "version": "1.0"
  }
}
```

## API Endpoints

### Character Management
- `GET /api/universes/{universe}/characters` - List all characters
- `POST /api/universes/{universe}/characters` - Create new character
- `GET /api/universes/{universe}/characters/{character}` - Get character details
- `PUT /api/universes/{universe}/characters/{character}` - Update character
- `DELETE /api/universes/{universe}/characters/{character}` - Delete character

### Character Analytics
- `GET /api/universes/{universe}/character-stats` - Get character statistics
- `GET /api/universes/{universe}/character-registry` - Get character registry
- `POST /api/universes/{universe}/rebuild-registry` - Rebuild character registry

### Chat Interface
- `POST /api/chat` - Chat with a character
- `POST /api/chat/clear` - Clear conversation history

### Universe Management
- `GET /api/universes` - List all universes
- `POST /api/universes` - Create new universe
- `GET /api/universes/{universe}` - Get universe details

### Index Management
- `POST /api/universes/{universe}/build-index` - Build FAISS index
- `POST /api/build-all-indices` - Build all indices

## Configuration

Edit `config/config.yaml` to customize:
- API settings
- Database paths
- Model configurations
- Logging levels

## Development

### Running Tests

```bash
python -m app.test_character_manager
```

### Building Indices

```bash
# Build index for specific universe
python -m app.cli universe build-index --universe Mytherra

# Build all indices
python -m app.cli universe build-all-indices
```

### Adding New Characters

```bash
# Interactive creation
python -m app.cli character create --universe Mytherra

# Or use the API
curl -X POST http://localhost:8000/api/universes/Mytherra/characters \
  -H "Content-Type: application/json" \
  -d '{"name": "New Character", "role": "Hero", ...}'
```

## Dependencies

- **FastAPI**: Web framework
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

See `requirements.txt` for complete list.
