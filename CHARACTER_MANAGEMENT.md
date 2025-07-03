# Character Management System

The PersonaForge RAG system includes a comprehensive character management system that allows you to create, update, and manage characters within your universes.

## Overview

Characters are stored as individual JSON files in the `data/universes/{universe}/characters/` directory. Each character has a rich schema that supports:

- Basic information (name, role, location, backstory)
- Mood tracking with Plutchik emotion model
- Personality traits
- Key quotes and catchphrases
- Knowledge domains
- Relationships and faction information
- Metadata for versioning

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

## Usage

### Command Line Interface

The character manager provides a CLI for easy character management:

```bash
# List all characters in a universe
python manage_characters.py list --universe Mytherra

# Show detailed character information
python manage_characters.py show --universe Mytherra --character "Kael Vire"

# Create a new character (interactive)
python manage_characters.py create --universe Mytherra

# Delete a character
python manage_characters.py delete --universe Mytherra --character "Character Name"

# Get character statistics
python manage_characters.py stats --universe Mytherra

# Rebuild character registry
python manage_characters.py registry --universe Mytherra
```

### API Endpoints

The system also provides REST API endpoints for programmatic access:

#### Character Management
- `GET /api/universes/{universe}/characters` - List all characters
- `POST /api/universes/{universe}/characters` - Create new character
- `GET /api/universes/{universe}/characters/{character}` - Get character details
- `PUT /api/universes/{universe}/characters/{character}` - Update character
- `DELETE /api/universes/{universe}/characters/{character}` - Delete character

#### Character Analytics
- `GET /api/universes/{universe}/character-stats` - Get character statistics
- `GET /api/universes/{universe}/character-registry` - Get character registry
- `POST /api/universes/{universe}/rebuild-registry` - Rebuild character registry

#### Character Export
- `GET /api/universes/{universe}/characters/{character}/export` - Export character data

## Character Registry

The system maintains a character registry (`character_registry.json`) for each universe that provides:

- Fast character lookups
- Character metadata without loading full files
- Character count and indexing information

The registry is automatically updated when characters are created, updated, or deleted.

## RAG Integration

Characters are automatically integrated into the RAG system:

1. **Granular Chunking**: Each character aspect (personality, quotes, knowledge, etc.) is stored as separate chunks for better retrieval
2. **Semantic Search**: Character information is embedded and searchable through the FAISS index
3. **Context Enhancement**: Character relationships and knowledge domains improve conversation context

## Best Practices

### Character Creation
1. **Use descriptive names** that are unique within the universe
2. **Write detailed backstories** that include personality and motivations
3. **Define personality traits** to help the AI understand character behavior
4. **Add key quotes** that capture the character's voice
5. **Specify knowledge domains** to improve expertise-based responses

### Character Organization
1. **Group related characters** by location or faction
2. **Maintain consistent naming** conventions
3. **Update character relationships** as the story evolves
4. **Use the registry** for fast lookups in large universes

### Performance Optimization
1. **Keep character files focused** - don't include unnecessary information
2. **Use the registry** for character discovery instead of scanning directories
3. **Rebuild indices** after major character updates
4. **Monitor character statistics** to identify areas for improvement

## Testing

Run the test script to verify the character manager is working:

```bash
python test_character_manager.py
```

This will test basic functionality including listing characters, getting statistics, and retrieving character details.

## File Structure

```
data/universes/{universe}/
├── manifest.json              # Universe metadata
├── character_registry.json    # Character lookup index
├── characters/                # Individual character files
│   ├── character1.json
│   ├── character2.json
│   └── ...
└── faiss_index/              # RAG embeddings
    ├── index.faiss
    └── chunks.txt
```

## Troubleshooting

### Common Issues

1. **Character not found**: Check the character name spelling and ensure it exists in the universe
2. **Registry out of sync**: Run `python manage_characters.py registry --universe {universe}` to rebuild
3. **RAG not finding character info**: Rebuild the universe index with `python -m app.universe_embedder`

### Debugging

- Use the `--debug` flag in API calls to get detailed information
- Check the character registry for metadata issues
- Verify character file JSON syntax
- Monitor the logs for import/export errors 