# app/conversation_manager.py
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import re
from pathlib import Path
from app.character import Character
from app.universe_manager import save_character

@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    character_name: str
    universe: str

@dataclass
class CharacterEvent:
    """Represents important character events for long-term memory."""
    event_type: str  # "emotion_change", "inventory_change", "relationship_change", "location_change"
    description: str
    timestamp: datetime
    character_name: str
    universe: str
    details: dict  # Additional event-specific details

class ConversationManager:
    def __init__(self, max_history: int = 10, max_events: int = 50):
        self.max_history = max_history
        self.max_events = max_events
        self.conversations: Dict[str, List[Message]] = {}
        self.character_events: Dict[str, List[CharacterEvent]] = {}
        
    def get_conversation_key(self, character_name: str, universe: str) -> str:
        """Generate a unique key for each character conversation."""
        return f"{universe}:{character_name}"
    
    def add_message(self, character_name: str, universe: str, role: str, content: str):
        """Add a message to the conversation history."""
        key = self.get_conversation_key(character_name, universe)
        
        if key not in self.conversations:
            self.conversations[key] = []
        
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            character_name=character_name,
            universe=universe
        )
        
        self.conversations[key].append(message)
        
        # Keep only the last max_history messages
        if len(self.conversations[key]) > self.max_history:
            self.conversations[key] = self.conversations[key][-self.max_history:]
    
    def add_character_event(self, character_name: str, universe: str, event_type: str, 
                          description: str, details: dict = None):
        """Add an important character event for long-term memory."""
        key = self.get_conversation_key(character_name, universe)
        
        if key not in self.character_events:
            self.character_events[key] = []
        
        event = CharacterEvent(
            event_type=event_type,
            description=description,
            timestamp=datetime.now(),
            character_name=character_name,
            universe=universe,
            details=details or {}
        )
        
        self.character_events[key].append(event)
        
        # Keep only the last max_events events
        if len(self.character_events[key]) > self.max_events:
            self.character_events[key] = self.character_events[key][-self.max_events:]
    
    def get_conversation_history(self, character_name: str, universe: str, max_messages: int = 5) -> List[Message]:
        """Get recent conversation history for context."""
        key = self.get_conversation_key(character_name, universe)
        
        if key not in self.conversations:
            return []
        
        # Return the last max_messages messages
        return self.conversations[key][-max_messages:]
    
    def get_important_events(self, character_name: str, universe: str, max_events: int = 10) -> List[CharacterEvent]:
        """Get important character events for long-term memory."""
        key = self.get_conversation_key(character_name, universe)
        
        if key not in self.character_events:
            return []
        
        # Return the last max_events events
        return self.character_events[key][-max_events:]
    
    def format_conversation_context(self, character_name: str, universe: str) -> str:
        """Format conversation history for inclusion in prompt."""
        history = self.get_conversation_history(character_name, universe, max_messages=3)
        
        if not history:
            return ""
        
        context_lines = []
        for msg in history:
            if msg.role == "user":
                context_lines.append(f"User: {msg.content}")
            else:
                context_lines.append(f"{character_name}: {msg.content}")
        
        return "\n".join(context_lines)
    
    def format_important_events(self, character_name: str, universe: str) -> str:
        """Format important events for inclusion in prompt."""
        events = self.get_important_events(character_name, universe, max_events=5)
        
        if not events:
            return ""
        
        event_lines = []
        for event in events:
            event_lines.append(f"- {event.description}")
        
        return "Important recent events:\n" + "\n".join(event_lines)
    
    def analyze_conversation_for_changes(self, character: Character, user_message: str, 
                                       assistant_response: str) -> Tuple[dict, dict]:
        """
        Analyze conversation for potential character state changes.
        Returns (emotion_changes, inventory_changes)
        """
        emotion_changes = {}
        inventory_changes = {}
        
        # Analyze for emotion changes
        emotion_changes = self._detect_emotion_changes(character, user_message, assistant_response)
        
        # Analyze for inventory changes
        inventory_changes = self._detect_inventory_changes(character, user_message, assistant_response)
        
        return emotion_changes, inventory_changes
    
    def _detect_emotion_changes(self, character: Character, user_message: str, assistant_response: str) -> dict:
        """Detect potential emotion changes based on conversation context."""
        changes = {}
        
        # Emotion keywords and their corresponding Plutchik emotions
        emotion_keywords = {
            'joy': ['happy', 'joy', 'excited', 'pleased', 'delighted', 'cheerful'],
            'trust': ['trust', 'believe', 'confident', 'reliable', 'faith'],
            'fear': ['afraid', 'scared', 'fear', 'terrified', 'worried', 'anxious'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned'],
            'sadness': ['sad', 'depressed', 'melancholy', 'grief', 'sorrow', 'unhappy'],
            'disgust': ['disgusted', 'repulsed', 'revolted', 'appalled'],
            'anger': ['angry', 'furious', 'rage', 'irritated', 'mad', 'enraged'],
            'anticipation': ['excited', 'eager', 'anticipating', 'looking forward']
        }
        
        # Check user message for emotion triggers
        user_lower = user_message.lower()
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in user_lower:
                    # Determine intensity based on context
                    intensity = self._determine_emotion_intensity(user_message, keyword)
                    changes[emotion] = intensity
                    break
        
        # Check assistant response for emotional reactions
        response_lower = assistant_response.lower()
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in response_lower:
                    intensity = self._determine_emotion_intensity(assistant_response, keyword)
                    changes[emotion] = intensity
                    break
        
        return changes
    
    def _determine_emotion_intensity(self, text: str, emotion_keyword: str) -> str:
        """Determine the intensity of an emotion based on context."""
        text_lower = text.lower()
        
        # Intensity indicators
        extreme_indicators = ['extremely', 'absolutely', 'completely', 'totally', 'utterly']
        high_indicators = ['very', 'really', 'so', 'quite', 'highly']
        moderate_indicators = ['somewhat', 'kind of', 'sort of', 'a bit']
        
        for indicator in extreme_indicators:
            if indicator in text_lower:
                return 'extreme'
        
        for indicator in high_indicators:
            if indicator in text_lower:
                return 'high'
        
        for indicator in moderate_indicators:
            if indicator in text_lower:
                return 'moderate'
        
        return 'low'
    
    def _detect_inventory_changes(self, character: Character, user_message: str, assistant_response: str) -> dict:
        """Detect potential inventory changes based on conversation context."""
        changes = {}
        
        # Patterns for giving items
        give_patterns = [
            r"give\s+(?:you|him|her|them)\s+([a-zA-Z\s]+)",
            r"hand\s+(?:you|him|her|them)\s+([a-zA-Z\s]+)",
            r"offer\s+(?:you|him|her|them)\s+([a-zA-Z\s]+)",
            r"present\s+(?:you|him|her|them)\s+([a-zA-Z\s]+)",
            r"here\s+is\s+([a-zA-Z\s]+)",
            r"take\s+this\s+([a-zA-Z\s]+)"
        ]
        
        # Patterns for taking items
        take_patterns = [
            r"take\s+(?:your|his|her|their)\s+([a-zA-Z\s]+)",
            r"steal\s+(?:your|his|her|their)\s+([a-zA-Z\s]+)",
            r"remove\s+(?:your|his|her|their)\s+([a-zA-Z\s]+)",
            r"lose\s+(?:your|his|her|their)\s+([a-zA-Z\s]+)"
        ]
        
        # Check for giving items
        for pattern in give_patterns:
            matches = re.findall(pattern, user_message.lower())
            for match in matches:
                item = match.strip()
                if item and len(item) > 2:  # Avoid very short matches
                    changes[f"add_{item}"] = True
        
        # Check for taking items
        for pattern in take_patterns:
            matches = re.findall(pattern, user_message.lower())
            for match in matches:
                item = match.strip()
                if item and len(item) > 2:
                    changes[f"remove_{item}"] = True
        
        return changes
    
    def apply_character_changes(self, character: Character, emotion_changes: dict, 
                              inventory_changes: dict) -> bool:
        """
        Apply detected changes to the character and save to file.
        Returns True if changes were made.
        """
        changes_made = False
        
        # Apply emotion changes
        if emotion_changes:
            current_mood = character.current_mood.copy()
            
            for emotion, intensity in emotion_changes.items():
                current_mood['primary_emotion'] = emotion
                current_mood['intensity'] = intensity
                
                # Update Plutchik axis (simplified - just the primary emotion)
                current_mood['plutchik_axis'] = [emotion]
                
                character.current_mood = current_mood
                changes_made = True
                
                # Add event for emotion change
                self.add_character_event(
                    character.name, character.universe, "emotion_change",
                    f"Emotion changed to {emotion} ({intensity})",
                    {"emotion": emotion, "intensity": intensity}
                )
        
        # Apply inventory changes
        if inventory_changes:
            for change, value in inventory_changes.items():
                if change.startswith("add_"):
                    item = change[4:]  # Remove "add_" prefix
                    if item not in character.inventory:
                        character.inventory.append(item)
                        changes_made = True
                        
                        # Add event for inventory addition
                        self.add_character_event(
                            character.name, character.universe, "inventory_change",
                            f"Added {item} to inventory",
                            {"action": "add", "item": item}
                        )
                
                elif change.startswith("remove_"):
                    item = change[7:]  # Remove "remove_" prefix
                    if item in character.inventory:
                        character.inventory.remove(item)
                        changes_made = True
                        
                        # Add event for inventory removal
                        self.add_character_event(
                            character.name, character.universe, "inventory_change",
                            f"Removed {item} from inventory",
                            {"action": "remove", "item": item}
                        )
        
        # Save character changes if any were made
        if changes_made:
            try:
                save_character(character.universe, character.name, character.to_dict())
            except Exception as e:
                print(f"Warning: Failed to save character changes: {e}")
        
        return changes_made
    
    def clear_conversation(self, character_name: str, universe: str):
        """Clear conversation history for a character."""
        key = self.get_conversation_key(character_name, universe)
        if key in self.conversations:
            del self.conversations[key]
    
    def save_conversations(self, filepath: str = "data/conversations.json"):
        """Save conversations to file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to serializable format
        serializable = {}
        for key, messages in self.conversations.items():
            serializable[key] = [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "character_name": msg.character_name,
                    "universe": msg.universe
                }
                for msg in messages
            ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)
    
    def save_character_events(self, filepath: str = "data/character_events.json"):
        """Save character events to file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to serializable format
        serializable = {}
        for key, events in self.character_events.items():
            serializable[key] = [
                {
                    "event_type": event.event_type,
                    "description": event.description,
                    "timestamp": event.timestamp.isoformat(),
                    "character_name": event.character_name,
                    "universe": event.universe,
                    "details": event.details
                }
                for event in events
            ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)
    
    def load_conversations(self, filepath: str = "data/conversations.json"):
        """Load conversations from file."""
        if not Path(filepath).exists():
            return
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for key, messages_data in data.items():
            messages = []
            for msg_data in messages_data:
                message = Message(
                    role=msg_data["role"],
                    content=msg_data["content"],
                    timestamp=datetime.fromisoformat(msg_data["timestamp"]),
                    character_name=msg_data["character_name"],
                    universe=msg_data["universe"]
                )
                messages.append(message)
            self.conversations[key] = messages
    
    def load_character_events(self, filepath: str = "data/character_events.json"):
        """Load character events from file."""
        if not Path(filepath).exists():
            return
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for key, events_data in data.items():
            events = []
            for event_data in events_data:
                event = CharacterEvent(
                    event_type=event_data["event_type"],
                    description=event_data["description"],
                    timestamp=datetime.fromisoformat(event_data["timestamp"]),
                    character_name=event_data["character_name"],
                    universe=event_data["universe"],
                    details=event_data["details"]
                )
                events.append(event)
            self.character_events[key] = events

# Global conversation manager instance
conversation_manager = ConversationManager() 