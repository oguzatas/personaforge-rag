# PersonaForge

A comprehensive RAG (Retrieval-Augmented Generation) system for creating and managing AI-powered characters with rich personalities, backstories, and interactive conversations.

## Project Structure

```
PersonaForge/
├── backend/           # Python FastAPI backend with RAG system
├── frontend/          # React frontend for user interface
├── Documentation/     # Project documentation and reports
├── phi2-personaforge-rag/  # Additional RAG implementations
└── roadmap.md         # Project roadmap
```

## Quick Start

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