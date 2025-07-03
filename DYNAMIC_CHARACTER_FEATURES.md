# Dynamic Character State Management in PersonaForge

This document describes the enhanced dynamic character state management features that have been added to PersonaForge, allowing characters to evolve and change based on conversations and interactions.

## Overview

The enhanced system now supports:
- **Dynamic emotion changes** based on conversation context
- **Inventory manipulation** (giving/taking items)
- **Long-term memory** with important events
- **Character state persistence** to files
- **Real-time character updates** during conversations

## Key Features

### 1. Dynamic Emotion Changes

Characters now automatically change their emotions based on conversation context. The system analyzes both user messages and character responses to detect emotional triggers.

#### Supported Emotions (Plutchik Wheel)
- **Joy**: happy, excited, pleased, delighted, cheerful
- **Trust**: trust, believe, confident, reliable, faith
- **Fear**: afraid, scared, terrified, worried, anxious
- **Surprise**: surprised, shocked, amazed, astonished, stunned
- **Sadness**: sad, depressed, melancholy, grief, sorrow, unhappy
- **Disgust**: disgusted, repulsed, revolted, appalled
- **Anger**: angry, furious, rage, irritated, mad, enraged
- **Anticipation**: excited, eager, anticipating, looking forward

#### Emotion Intensity Levels
- **Low**: Default intensity for detected emotions
- **Moderate**: Triggered by words like "somewhat", "kind of", "sort of"
- **High**: Triggered by words like "very", "really", "so", "quite"
- **Extreme**: Triggered by words like "extremely", "absolutely", "completely"

#### Example Usage
```python
# User says: "You look very happy today!"
# System detects: emotion="joy", intensity="high"
# Character's mood updates to: primary_emotion="joy", intensity="high"
```

### 2. Inventory Manipulation

Characters can now receive and lose items through conversation. The system uses pattern matching to detect inventory-related actions.

#### Supported Patterns

**Giving Items:**
- "give you [item]"
- "hand you [item]"
- "offer you [item]"
- "present you [item]"
- "here is [item]"
- "take this [item]"

**Taking Items:**
- "take your [item]"
- "steal your [item]"
- "remove your [item]"
- "lose your [item]"

#### Example Usage
```python
# User says: "Here is a magical sword for you"
# System detects: add_item="magical sword"
# Character's inventory updates to include "magical sword"
```

### 3. Long-term Memory

The system now maintains a history of important character events, separate from conversation history. This provides long-term memory that persists across sessions.

#### Event Types
- **emotion_change**: When character's mood changes
- **inventory_change**: When items are added/removed
- **relationship_change**: When relationships are modified
- **location_change**: When character moves locations

#### Event Structure
```json
{
  "event_type": "emotion_change",
  "description": "Emotion changed to joy (high)",
  "timestamp": "2024-01-15T10:30:00",
  "character_name": "Kael Vire",
  "universe": "Mytherra",
  "details": {
    "emotion": "joy",
    "intensity": "high"
  }
}
```

### 4. Character State Persistence

All character changes are automatically saved to files, ensuring that:
- Emotion changes persist across sessions
- Inventory modifications are permanent
- Important events are remembered
- Character state is consistent

## Technical Implementation

### Enhanced Conversation Manager

The `ConversationManager` class has been extended with:

```python
class ConversationManager:
    def __init__(self, max_history: int = 10, max_events: int = 50):
        self.max_history = max_history
        self.max_events = max_events
        self.conversations: Dict[str, List[Message]] = {}
        self.character_events: Dict[str, List[CharacterEvent]] = {}
    
    def analyze_conversation_for_changes(self, character, user_message, assistant_response):
        """Analyze conversation for potential character state changes."""
        
    def apply_character_changes(self, character, emotion_changes, inventory_changes):
        """Apply detected changes to character and save to file."""
```

### Enhanced RAG Pipeline

The RAG pipeline now includes:

```python
def answer_question(query: str, universe: str, character: Character, debug: bool = False):
    # ... existing RAG processing ...
    
    # Analyze conversation for character state changes
    emotion_changes, inventory_changes = conversation_manager.analyze_conversation_for_changes(
        character, query, response
    )
    
    # Apply changes to character
    changes_made = conversation_manager.apply_character_changes(
        character, emotion_changes, inventory_changes
    )
    
    return {
        "response": response,
        "character_updated": changes_made,
        "emotion_changes": emotion_changes,
        "inventory_changes": inventory_changes
    }
```

### Enhanced Prompt Templates

The prompt templates now include character state and important events:

```python
def format_prompt_character_focused(query, context_chunks, role_description, 
                                   conversation_history="", important_events="", 
                                   character_state=""):
    # Include current character state and important events in context
```

## API Endpoints

### Enhanced Chat Endpoint

The `/api/chat` endpoint now returns additional information:

```json
{
  "response": "Character response",
  "character": "Character name",
  "universe": "Universe name",
  "character_updated": true,
  "emotion_changes": {"joy": "high"},
  "inventory_changes": {"add_magical_sword": true}
}
```

### New Events Endpoint

Get important events for a character:

```
GET /api/universes/{universe_name}/characters/{character_name}/events?max_events=10
```

Response:
```json
{
  "events": [
    {
      "event_type": "emotion_change",
      "description": "Emotion changed to joy (high)",
      "timestamp": "2024-01-15T10:30:00",
      "details": {"emotion": "joy", "intensity": "high"}
    }
  ]
}
```

## Frontend Enhancements

### Character State Panel

The frontend now includes a "Character State" panel that shows:
- Current character mood and inventory
- Recent important events
- Real-time updates when character state changes

### State Change Notifications

When character state changes during conversation, the system:
1. Automatically refreshes character data
2. Updates the character state panel
3. Shows a notification message
4. Refreshes the events list

## Usage Examples

### Testing the Features

Run the test script to see all features in action:

```bash
cd backend
python ../test_dynamic_character.py
```

### Manual Testing

1. **Test Emotion Changes:**
   ```
   User: "You look very happy today!"
   System: Detects joy emotion, updates character mood
   ```

2. **Test Inventory Changes:**
   ```
   User: "Here is a magical sword for you"
   System: Adds "magical sword" to character inventory
   ```

3. **Test Long-term Memory:**
   ```
   User: "I'm giving you this legendary weapon!"
   System: Creates inventory_change event, remembers the gift
   ```

## Configuration

### Memory Limits

Configure memory limits in `ConversationManager`:

```python
conversation_manager = ConversationManager(
    max_history=10,    # Keep last 10 conversation messages
    max_events=50      # Keep last 50 important events
)
```

### Emotion Detection

Customize emotion keywords in `_detect_emotion_changes()`:

```python
emotion_keywords = {
    'joy': ['happy', 'joy', 'excited', 'pleased', 'delighted', 'cheerful'],
    'anger': ['angry', 'furious', 'rage', 'irritated', 'mad', 'enraged'],
    # ... add more emotions and keywords
}
```

### Inventory Patterns

Customize inventory detection patterns in `_detect_inventory_changes()`:

```python
give_patterns = [
    r"give\s+(?:you|him|her|them)\s+([a-zA-Z\s]+)",
    r"hand\s+(?:you|him|her|them)\s+([a-zA-Z\s]+)",
    # ... add more patterns
]
```

## File Structure

### New Data Files

- `data/conversations.json`: Conversation history
- `data/character_events.json`: Important character events

### Updated Character Files

Character files are automatically updated when changes occur:
- `data/universes/{universe}/characters/{character}.json`

## Benefits

1. **More Dynamic Characters**: Characters now respond to emotional context and remember important interactions
2. **Persistent State**: All changes are saved and persist across sessions
3. **Better Memory**: Long-term memory separate from conversation history
4. **Real-time Updates**: Character state updates immediately during conversations
5. **Enhanced Immersion**: Characters feel more alive and responsive

## Future Enhancements

Potential future improvements:
- **Relationship dynamics**: Characters forming friendships, rivalries, etc.
- **Location tracking**: Characters moving between locations
- **Skill progression**: Characters learning new abilities
- **Reputation system**: Characters building reputation with others
- **Advanced emotion modeling**: More complex emotional states and transitions

## Troubleshooting

### Common Issues

1. **Character not updating**: Check file permissions for character JSON files
2. **Events not saving**: Ensure `data/character_events.json` is writable
3. **Emotion detection not working**: Verify emotion keywords in the detection logic
4. **Inventory changes not detected**: Check regex patterns for inventory manipulation

### Debug Mode

Enable debug mode to see detailed information about:
- Detected emotion changes
- Inventory modifications
- Character state updates
- Event creation
- Full conversation context

This enhanced system makes PersonaForge characters much more dynamic and responsive, creating a more immersive and engaging experience for users. 