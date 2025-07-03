# CLI Tools for PersonaForge RAG System

This directory contains the command-line interface tools for managing the PersonaForge RAG system.

## Files

- **`cli.py`** - Consolidated CLI interface for all system operations
- **`character_manager.py`** - Character management logic and functionality
- **`test_character_manager.py`** - Test script for character manager functionality

## Usage

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

# Export character data
python -m app.cli character export --universe Mytherra --character "Kael Vire" --file "export.json"

# Import character data
python -m app.cli character import --universe Mytherra --file "import.json"
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

## Testing

Run the test script to verify functionality:

```bash
python -m app.test_character_manager
```

## Architecture

The CLI system is organized as follows:

1. **`cli.py`** - Main entry point that routes commands to appropriate handlers
2. **`character_manager.py`** - Contains the `CharacterManager` class with all character operations
3. **`test_character_manager.py`** - Standalone test script for verification

### Command Routing

The CLI uses a modular approach where:
- `python -m app.cli character <action>` routes to character management
- `python -m app.cli universe <action>` routes to universe management

This allows for easy extension with additional modules in the future.

## Integration

The CLI tools integrate with:
- **API endpoints** in `api.py` for programmatic access
- **Character management** logic in `character_manager.py`
- **Universe management** functions in `universe_manager.py`
- **RAG pipeline** in `rag_pipeline.py` and `universe_embedder.py` 