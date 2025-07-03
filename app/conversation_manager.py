# app/conversation_manager.py
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path

@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    character_name: str
    universe: str

class ConversationManager:
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.conversations: Dict[str, List[Message]] = {}
        
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
    
    def get_conversation_history(self, character_name: str, universe: str, max_messages: int = 5) -> List[Message]:
        """Get recent conversation history for context."""
        key = self.get_conversation_key(character_name, universe)
        
        if key not in self.conversations:
            return []
        
        # Return the last max_messages messages
        return self.conversations[key][-max_messages:]
    
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

# Global conversation manager instance
conversation_manager = ConversationManager() 