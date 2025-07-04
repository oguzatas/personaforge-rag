# PersonaForge

A comprehensive RAG (Retrieval-Augmented Generation) system for creating and managing AI-powered characters with rich personalities, backstories, and interactive conversations.

## Project Structure

```
PersonaForge/
├── backend/           # Python FastAPI backend with RAG system
├── frontend/          # React frontend for user interface
├── Documentation/     # Project documentation and reports
└── roadmap.md         # Project roadmap
```

## Quick Start

Requires Python 3.10.16


### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m app.api
```

The backend will start on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The frontend will start on `http://localhost:3000`


### Language Model Configuration

You can configure connection to language model in

backend/config/settings.py



## Features

### Character Management
- **Rich Character Schema**: Support for personality traits, relationships, knowledge domains, and mood tracking
- **Interactive Creation**: CLI tools for creating and managing characters
- **Character Registry**: Fast lookup system for character discovery
- **Export/Import**: Character data can be exported and imported

### RAG System
- **Semantic Search**: FAISS-based vector search for relevant context
- **Granular Chunking**: Character information split into searchable chunks
- **Conversation Memory**: Maintains conversation history for context
- **Multi-Universe Support**: Organize characters into different universes

### API Endpoints
- **Character CRUD**: Create, read, update, delete characters
- **Chat Interface**: Interactive conversations with characters
- **Universe Management**: Manage different character universes
- **Analytics**: Character statistics and registry information

## CLI Tools

### Character Management
```bash
# List characters
python -m backend.app.cli character list --universe Mytherra

# Create character (interactive)
python -m backend.app.cli character create --universe Mytherra

# Show character details
python -m backend.app.cli character show --universe Mytherra --character "Kael Vire"
```

### Universe Management
```bash
# List universes
python -m backend.app.cli universe list

# Build RAG index
python -m backend.app.cli universe build-index --universe Mytherra
```

## Character Schema

Characters support rich metadata including:
- Basic info (name, role, location, backstory)
- Mood tracking with Plutchik emotion model
- Personality traits and key quotes
- Knowledge domains and relationships
- Inventory and metadata

## Development

### Backend Structure
```
backend/
├── app/               # Main application code
│   ├── api.py         # FastAPI endpoints
│   ├── cli.py         # Command-line interface
│   ├── character_manager.py  # Character management
│   ├── rag_pipeline.py       # RAG processing
│   └── ...
├── data/              # Character and universe data
├── config/            # Configuration files
└── requirements.txt   # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/               # React source code
│   ├── components/    # React components
│   ├── App.js         # Main application
│   └── ...
├── public/            # Static assets
└── package.json       # Node.js dependencies
```

## API Documentation

Once the backend is running, visit:
- **API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/health`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
# PersonaForge - RAG-Powered NPC Dialog System

A comprehensive RAG (Retrieval-Augmented Generation) backend for building dynamic NPC dialogs in RPG games, featuring universe-driven management, character creation with Plutchik emotion wheel integration, and Phi-2 language model support.

## Features

- **Universe Driven Management**: Create and manage multiple game universes with their own lore, characters, and FAISS indices
- **Character Creation**: Rich character creation with mood/emotion based on Plutchik's wheel, inventory, backstory, and location
- **RAG Integration**: Per-universe semantic search using FAISS for contextual responses
- **Phi-2 Integration**: Local language model support for generating character responses
- **Web UI**: Modern React frontend for easy universe and character management
- **REST API**: FastAPI backend with full CRUD operations

## Architecture

```
rag-end/
├── app/                    # Python backend
│   ├── api.py             # FastAPI REST endpoints
│   ├── universe_manager.py # Universe/character CRUD
│   ├── character.py       # Character class
│   ├── rag_pipeline.py    # Main RAG pipeline
│   ├── retriever.py       # FAISS-based retrieval
│   ├── faiss_manager.py   # Per-universe FAISS indices
│   ├── llm_interface.py   # Phi-2 model interface
│   └── prompt_templates.py # Prompt formatting
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   └── App.js        # Main app
│   └── package.json
├── data/                  # Universe data storage
│   └── {universe_name}/
│       ├── manifest.json  # Universe definition
│       ├── characters/    # Character JSON files
│       └── faiss_index/   # FAISS index & chunks
└── requirements.txt       # Python dependencies
```

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to rag-end directory
cd rag-end

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python -m app.api
```

The API will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

The frontend will be available at `http://localhost:3000`

### 3. Model Setup

The system uses Microsoft's Phi-2 model. On first run, it will automatically download the model (~2.7GB). Ensure you have:

- **GPU**: CUDA-compatible GPU recommended (will fallback to CPU)
- **RAM**: At least 8GB RAM for CPU inference, 4GB VRAM for GPU
- **Storage**: ~3GB for model files

## Usage

### 1. Create a Universe

1. Go to the "Universes" tab
2. Click "Create Universe"
3. Fill in:
   - Universe name (e.g., "realm_of_embers")
   - Description
   - Roles (e.g., "blacksmith", "sorcerer")

### 2. Create Characters

1. Go to the "Characters" tab
2. Select a universe
3. Click "Create Character"
4. Fill in character details:
   - Basic info (name, role, location, backstory)
   - Mood (primary emotion, intensity, Plutchik axis)
   - Inventory items

### 3. Chat with Characters

1. Go to the "Chat" tab
2. Select universe and character
3. Start chatting! The system will:
   - Retrieve relevant context from the universe's knowledge base
   - Use character's mood and backstory to shape responses
   - Generate responses using Phi-2

## API Endpoints

### Universes
- `GET /api/universes` - List all universes
- `POST /api/universes` - Create new universe
- `GET /api/universes/{name}` - Get universe details

### Characters
- `GET /api/universes/{universe}/characters` - List characters
- `POST /api/universes/{universe}/characters` - Create character
- `GET /api/universes/{universe}/characters/{name}` - Get character

### Chat
- `POST /api/chat` - Chat with character

## Character Manifest Structure

```json
{
  "name": "Gorim Ironfist",
  "role": "blacksmith",
  "universe": "realm_of_embers",
  "inventory": ["flame axe", "mithril armor"],
  "current_mood": {
    "primary_emotion": "anger",
    "intensity": "moderate",
    "plutchik_axis": ["anger", "anticipation"]
  },
  "backstory": "Lost his eye in the Great War...",
  "location": "Ironhold"
}
```

## Universe Manifest Structure

```json
{
  "universe_name": "realm_of_embers",
  "description": "A world of fire and ancient magic.",
  "roles": [
    {
      "name": "blacksmith",
      "description": "A master of forging weapons and armor."
    }
  ]
}
```

## Plutchik Emotion Wheel

The system supports 8 primary emotions from Plutchik's wheel:
- Joy, Trust, Fear, Surprise, Sadness, Disgust, Anger, Anticipation

Each character can have:
- **Primary emotion**: Main emotional state
- **Intensity**: low, moderate, high, extreme
- **Plutchik axis**: Multiple emotions that influence behavior

## Development

### Adding New Features

1. **Backend**: Add endpoints in `app/api.py`, logic in respective modules
2. **Frontend**: Create components in `frontend/src/components/`
3. **Data**: Extend manifest structures in `universe_manager.py`

### Extending the System

- **New LLM**: Modify `llm_interface.py`
- **New Retrieval**: Extend `retriever.py` and `faiss_manager.py`
- **New UI**: Add React components and routes

## Troubleshooting

### Common Issues

1. **Model Loading Errors**: Ensure sufficient RAM/VRAM
2. **FAISS Errors**: Install `faiss-cpu` or `faiss-gpu`
3. **Frontend Connection**: Check API is running on port 8000
4. **Character Creation**: Ensure universe exists first

### Performance Tips

- Use GPU for faster inference
- Create FAISS indices for better retrieval
- Limit context chunks for faster responses

## License

MIT License - Feel free to use in your projects!
